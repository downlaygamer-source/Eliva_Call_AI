"""
Eliva - Main Flask Web Application & Twilio Webhook Handler
Provides:
1. Twilio Voice Webhooks (Incoming call, Speech Gather, Call Status, Voicemail)
2. Interactive Web Dashboard to monitor calls, read AI summaries, and configure knowledge base
3. Built-in Call Simulator to test Eliva using microphone/text without needing a real phone line
"""

import os
import uuid
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from twilio.twiml.voice_response import VoiceResponse, Gather
from config import Config
from knowledge_base import load_knowledge, save_knowledge
from call_manager import (
    ask_eliva,
    end_and_summarize_call,
    get_or_create_call_session,
    load_call_logs,
    active_calls,
    LANGUAGE_CODES
)

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY


# ══════════════════════════════════════════════════════════════════════
# TWILIO VOICE WEBHOOKS
# ══════════════════════════════════════════════════════════════════════

@app.route("/voice/incoming", methods=["POST", "GET"])
def voice_incoming():
    """
    Twilio Webhook: Initial entry point when someone dials your Eliva Twilio number.
    Plays greeting and starts listening for caller's speech.
    """
    call_sid = request.values.get("CallSid", str(uuid.uuid4()))
    caller = request.values.get("From", "Unknown")

    # Initialize call session
    session = get_or_create_call_session(call_sid, caller)
    knowledge = load_knowledge()
    owner_name = knowledge.get("owner", {}).get("name", "your contact")

    resp = VoiceResponse()

    # Initial greeting from Eliva
    greeting = f"Hello! I am Eliva, an AI assistant for {owner_name}. They are currently busy and unable to take your call right now, but I can answer your questions on the spot or take a message for them. How can I help you today?"

    session["transcript"].append({
        "speaker": "Eliva",
        "text": greeting,
        "time": "Start"
    })
    session["messages"].append({
        "role": "assistant",
        "content": greeting
    })

    # Twilio Gather with speech recognition
    gather = Gather(
        input="speech",
        action="/voice/gather",
        method="POST",
        speech_timeout="auto",
        language=Config.SPEECH_LANGUAGE,
        enhanced=True,
        hints="urgent, call back, message, meeting, appointment, delivery, interview, email"
    )
    gather.say(greeting, voice=Config.SPEECH_VOICE, language=Config.SPEECH_LANGUAGE)
    resp.append(gather)

    # If caller remains silent
    resp.say("I didn't catch that. Please feel free to speak or call back later. Goodbye!", voice=Config.SPEECH_VOICE)
    resp.hangup()

    return str(resp), 200, {"Content-Type": "application/xml"}


@app.route("/voice/gather", methods=["POST", "GET"])
def voice_gather():
    """
    Twilio Webhook: Handles caller speech input, asks Claude (Eliva), and speaks the answer.
    Loops back to listen for follow-up questions until caller hangs up.
    Automatically adapts to the caller's language.
    """
    call_sid = request.values.get("CallSid", "")
    caller = request.values.get("From", "Unknown")
    speech_result = request.values.get("SpeechResult", "").strip()

    resp = VoiceResponse()

    # Get session to check detected language
    session = get_or_create_call_session(call_sid, caller)
    detected_lang = session.get("detected_language", "en")
    lang_config = LANGUAGE_CODES.get(detected_lang, LANGUAGE_CODES["en"])

    twilio_language = lang_config["twilio"]
    twilio_voice = lang_config["voice"]

    if not speech_result:
        # No speech detected
        gather = Gather(
            input="speech",
            action="/voice/gather",
            method="POST",
            speech_timeout="auto",
            language=twilio_language
        )
        gather.say("I'm still here. Is there anything else you would like me to help you with or tell my owner?", voice=twilio_voice, language=twilio_language)
        resp.append(gather)
        resp.say("Thank you for calling. Have a great day!", voice=twilio_voice, language=twilio_language)
        resp.hangup()
        return str(resp), 200, {"Content-Type": "application/xml"}

    # Process caller's speech with Claude (detects language automatically)
    eliva_reply = ask_eliva(call_sid, speech_result, caller)

    # Update language config after detection (might change on first message)
    detected_lang = session.get("detected_language", "en")
    lang_config = LANGUAGE_CODES.get(detected_lang, LANGUAGE_CODES["en"])
    twilio_language = lang_config["twilio"]
    twilio_voice = lang_config["voice"]

    # Check if Eliva or user indicated ending the call (multi-language support)
    closing_phrases = [
        "goodbye", "have a great day", "bye", "take care",
        "धन्यवाद", "अलविदा",  # Hindi
        "ਅਲਵਿਦਾ", "ਧੰਨਵਾਦ", "ਫਿਰ ਮਿਲਾਂਗੇ", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ",  # Punjabi
        "adiós", "gracias",  # Spanish
        "au revoir", "merci",  # French
        "auf wiedersehen", "danke",  # German
        "さようなら", "ありがとう",  # Japanese
        "再见", "谢谢",  # Chinese
        "مع السلامة", "شكرا"  # Arabic
    ]
    should_hangup = any(phrase in eliva_reply.lower() for phrase in closing_phrases) and ("anything else" not in eliva_reply.lower())

    if should_hangup:
        resp.say(eliva_reply, voice=twilio_voice, language=twilio_language)
        resp.hangup()
    else:
        # Continue conversation loop
        gather = Gather(
            input="speech",
            action="/voice/gather",
            method="POST",
            speech_timeout="auto",
            language=twilio_language,
            enhanced=True
        )
        gather.say(eliva_reply, voice=twilio_voice, language=twilio_language)
        resp.append(gather)

        # Fallback if no further input
        resp.say("I have recorded all your notes and will notify my owner right away. Thank you for calling!", voice=twilio_voice, language=twilio_language)
        resp.hangup()

    return str(resp), 200, {"Content-Type": "application/xml"}


@app.route("/voice/status", methods=["POST"])
def voice_status():
    """
    Twilio Webhook: Receives call completion events (hangup, duration, status).
    Triggers automatic call summarization.
    """
    call_sid = request.values.get("CallSid")
    call_status = request.values.get("CallStatus", "completed")
    duration = int(request.values.get("CallDuration", 0))

    if call_sid:
        end_and_summarize_call(call_sid, call_status, duration)

    return "", 200


# ══════════════════════════════════════════════════════════════════════
# SIMULATOR API (For Testing Eliva In-Browser via Text or Mic)
# ══════════════════════════════════════════════════════════════════════

@app.route("/api/simulate/start", methods=["POST"])
def api_simulate_start():
    """Start a simulated phone call session."""
    data = request.json or {}
    caller_name = data.get("caller_name", "Test Caller")
    caller_phone = data.get("caller_phone", "+1-555-0199")

    call_sid = f"sim_{uuid.uuid4().hex[:8]}"
    session = get_or_create_call_session(call_sid, caller_phone)

    knowledge = load_knowledge()
    owner_name = knowledge.get("owner", {}).get("name", "DJ")

    greeting = f"Hello! I am Eliva, an AI assistant for {owner_name}. They are currently busy, but I can answer your questions on the spot or take a message for them. How can I help you today?"

    session["transcript"].append({
        "speaker": "Eliva",
        "text": greeting,
        "time": "Start"
    })
    session["messages"].append({
        "role": "assistant",
        "content": greeting
    })

    return jsonify({
        "call_sid": call_sid,
        "greeting": greeting,
        "transcript": session["transcript"]
    })


@app.route("/api/simulate/talk", methods=["POST"])
def api_simulate_talk():
    """Send user message to simulated call and get Eliva's response."""
    data = request.json or {}
    call_sid = data.get("call_sid")
    user_speech = data.get("speech", "").strip()

    if not call_sid or not user_speech:
        return jsonify({"error": "Missing call_sid or speech"}), 400

    eliva_reply = ask_eliva(call_sid, user_speech)
    session = active_calls.get(call_sid, {})

    return jsonify({
        "reply": eliva_reply,
        "transcript": session.get("transcript", [])
    })


@app.route("/api/simulate/end", methods=["POST"])
def api_simulate_end():
    """End simulated call and generate summary."""
    data = request.json or {}
    call_sid = data.get("call_sid")

    if not call_sid:
        return jsonify({"error": "Missing call_sid"}), 400

    summary = end_and_summarize_call(call_sid, "completed", 60)
    return jsonify({
        "status": "ended",
        "summary": summary
    })


# ══════════════════════════════════════════════════════════════════════
# WEB DASHBOARD & UI ROUTES
# ══════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Main dashboard showing stats, recent calls, and active status."""
    logs = load_call_logs()
    knowledge = load_knowledge()

    total_calls = len(logs)
    urgent_calls = sum(1 for log in logs if log.get("extracted_info", {}).get("is_urgent", False))
    callback_needed = sum(1 for log in logs if log.get("extracted_info", {}).get("callback_needed", False))

    return render_template(
        "index.html",
        logs=logs[:5],
        total_calls=total_calls,
        urgent_calls=urgent_calls,
        callback_needed=callback_needed,
        knowledge=knowledge,
        active_calls_count=len(active_calls)
    )


@app.route("/call-logs")
def call_logs():
    """View full call logs with transcriptions and AI summaries."""
    logs = load_call_logs()
    return render_template("call_logs.html", logs=logs)


@app.route("/simulator")
def simulator():
    """Interactive voice & text simulator to test Eliva."""
    knowledge = load_knowledge()
    return render_template("simulator.html", knowledge=knowledge)


@app.route("/knowledge-base", methods=["GET", "POST"])
def knowledge_base_page():
    """Configure owner profile, FAQs, and custom answering rules."""
    if request.method == "POST":
        owner_name = request.form.get("name")
        owner_title = request.form.get("title")
        owner_status = request.form.get("status")
        owner_available = request.form.get("available")
        owner_email = request.form.get("email")
        custom_instructions = request.form.get("custom_instructions")

        # Rules
        rules_raw = request.form.get("rules", "")
        rules = [r.strip() for r in rules_raw.split("\n") if r.strip()]

        # FAQs
        faq_questions = request.form.getlist("faq_q[]")
        faq_answers = request.form.getlist("faq_a[]")
        faqs = []
        for q, a in zip(faq_questions, faq_answers):
            if q.strip() and a.strip():
                faqs.append({"question": q.strip(), "answer": a.strip()})

        updated_kb = {
            "owner": {
                "name": owner_name,
                "title": owner_title,
                "current_status": owner_status,
                "available_times": owner_available,
                "email": owner_email
            },
            "urgent_contact_rules": rules,
            "faq": faqs,
            "custom_instructions": custom_instructions
        }

        save_knowledge(updated_kb)
        flash("Knowledge base and Eliva answering rules updated successfully!", "success")
        return redirect(url_for("knowledge_base_page"))

    knowledge = load_knowledge()
    return render_template("knowledge_base.html", knowledge=knowledge)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", Config.PORT))
    print(f"🚀 Eliva Call Attendant Server running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
