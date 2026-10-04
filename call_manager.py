"""
Eliva - Call Manager & LLM Engine
Manages call sessions, conversation state, Claude API interactions, and call logs.
"""

import json
import os
import uuid
from datetime import datetime
import anthropic
from config import Config
from knowledge_base import get_system_prompt, load_knowledge

# In-memory session store for active calls (CallSid -> call data)
active_calls = {}

# Language detection mapping for common languages
LANGUAGE_CODES = {
    "en": {"twilio": "en-US", "name": "English", "voice": "Polly.Joanna"},
    "hi": {"twilio": "hi-IN", "name": "Hindi", "voice": "Polly.Aditi"},
    "pa": {"twilio": "hi-IN", "name": "Punjabi", "voice": "Polly.Aditi"},  # Punjabi uses Hindi voice/recognition as fallback
    "es": {"twilio": "es-ES", "name": "Spanish", "voice": "Polly.Lucia"},
    "fr": {"twilio": "fr-FR", "name": "French", "voice": "Polly.Celine"},
    "de": {"twilio": "de-DE", "name": "German", "voice": "Polly.Marlene"},
    "it": {"twilio": "it-IT", "name": "Italian", "voice": "Polly.Carla"},
    "pt": {"twilio": "pt-BR", "name": "Portuguese", "voice": "Polly.Vitoria"},
    "ja": {"twilio": "ja-JP", "name": "Japanese", "voice": "Polly.Mizuki"},
    "ko": {"twilio": "ko-KR", "name": "Korean", "voice": "Polly.Seoyeon"},
    "zh": {"twilio": "zh-CN", "name": "Chinese", "voice": "Polly.Zhiyu"},
    "ar": {"twilio": "ar-AE", "name": "Arabic", "voice": "Polly.Zeina"},
    "ru": {"twilio": "ru-RU", "name": "Russian", "voice": "Polly.Tatyana"},
    "nl": {"twilio": "nl-NL", "name": "Dutch", "voice": "Polly.Lotte"},
    "pl": {"twilio": "pl-PL", "name": "Polish", "voice": "Polly.Ewa"},
    "tr": {"twilio": "tr-TR", "name": "Turkish", "voice": "Polly.Filiz"},
}

LOGS_FILE = os.path.join(os.path.dirname(__file__), "call_logs.json")


def get_anthropic_client():
    """Initialize and return Anthropic SDK client."""
    if Config.ANTHROPIC_API_KEY:
        return anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    return anthropic.Anthropic()


def load_call_logs():
    """Load past call logs and recorded messages."""
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_call_log(log_entry):
    """Save a finished call log."""
    logs = load_call_logs()
    logs.insert(0, log_entry)  # Newest first
    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


def detect_language(text):
    """
    Detect language from user's text using Claude.
    Returns ISO 639-1 language code (e.g., 'en', 'hi', 'es').
    """
    if not text or len(text.strip()) < 3:
        return "en"  # Default to English for very short text

    try:
        client = get_anthropic_client()

        detection_prompt = f"""Detect the language of the following text and respond with ONLY the ISO 639-1 two-letter language code (e.g., 'en' for English, 'hi' for Hindi, 'es' for Spanish, 'fr' for French, 'de' for German, 'ja' for Japanese, 'zh' for Chinese, 'ar' for Arabic, etc.).

Text: "{text}"

Respond with only the two-letter code, nothing else."""

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Use fast model for detection
            max_tokens=10,
            messages=[{"role": "user", "content": detection_prompt}]
        )

        detected = response.content[0].text.strip().lower()

        # Validate it's a known language code
        if detected in LANGUAGE_CODES:
            return detected

        # Default to English if unknown
        return "en"

    except Exception as e:
        print(f"Language detection error: {e}")
        return "en"


def get_or_create_call_session(call_sid, caller_number="Unknown"):
    """Get active session or initialize a new one."""
    if call_sid not in active_calls:
        active_calls[call_sid] = {
            "call_sid": call_sid,
            "caller_number": caller_number,
            "start_time": datetime.now().isoformat(),
            "messages": [],  # Anthropic messages format: [{"role": "user"|"assistant", "content": "..."}]
            "transcript": [],  # Readable transcript: [{"speaker": "Caller"|"Eliva", "text": "...", "timestamp": "..."}]
            "detected_language": None,  # Will be set after first user speech
            "extracted_info": {
                "caller_name": None,
                "reason": None,
                "is_urgent": False,
                "summary": None
            }
        }
    return active_calls[call_sid]


def ask_eliva(call_sid, user_speech, caller_number="Unknown"):
    """
    Process caller speech with Claude (Eliva) and return the response.
    Maintains conversation context across multiple turns during the call.
    Automatically detects and responds in the caller's language.
    """
    session = get_or_create_call_session(call_sid, caller_number)

    # Detect language on first user message
    if session["detected_language"] is None:
        session["detected_language"] = detect_language(user_speech)
        print(f"Detected language: {session['detected_language']} for call {call_sid}")

    # Add user speech to session
    session["messages"].append({
        "role": "user",
        "content": user_speech
    })
    session["transcript"].append({
        "speaker": "Caller",
        "text": user_speech,
        "time": datetime.now().strftime("%H:%M:%S")
    })

    # Get system prompt with language context
    system_prompt = get_system_prompt(caller_number, session["detected_language"])

    try:
        client = get_anthropic_client()

        response = client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=1000,
            system=system_prompt,
            messages=session["messages"]
        )

        # Extract text response
        assistant_reply = ""
        for block in response.content:
            if block.type == "text":
                assistant_reply += block.text

        assistant_reply = assistant_reply.strip()

        # Add assistant reply to history
        session["messages"].append({
            "role": "assistant",
            "content": assistant_reply
        })
        session["transcript"].append({
            "speaker": "Eliva",
            "text": assistant_reply,
            "time": datetime.now().strftime("%H:%M:%S")
        })

        return assistant_reply

    except anthropic.AuthenticationError:
        error_msg = _get_error_message("auth", session["detected_language"])
        return error_msg
    except anthropic.RateLimitError:
        error_msg = _get_error_message("rate_limit", session["detected_language"])
        return error_msg
    except Exception as e:
        print(f"Error calling Claude: {e}")
        error_msg = _get_error_message("general", session["detected_language"])
        return error_msg


def _get_error_message(error_type, language_code):
    """Return error messages in the appropriate language."""
    error_messages = {
        "auth": {
            "en": "I apologize, but my AI service credentials are not configured properly. Please leave your name and number, and my owner will call you back.",
            "hi": "मुझे खेद है, लेकिन मेरी AI सेवा क्रेडेंशियल सही तरीके से कॉन्फ़िगर नहीं हैं। कृपया अपना नाम और नंबर छोड़ें, और मेरे मालिक आपको वापस कॉल करेंगे।",
            "es": "Me disculpo, pero mis credenciales de servicio de IA no están configuradas correctamente. Por favor, deje su nombre y número, y mi propietario le devolverá la llamada.",
            "fr": "Je m'excuse, mais mes informations d'identification du service IA ne sont pas configurées correctement. Veuillez laisser votre nom et numéro, et mon propriétaire vous rappellera.",
            "de": "Entschuldigung, aber meine KI-Serviceanmeldeinformationen sind nicht richtig konfiguriert. Bitte hinterlassen Sie Ihren Namen und Ihre Nummer, und mein Besitzer wird Sie zurückrufen.",
        },
        "rate_limit": {
            "en": "I am experiencing high call volume at the moment. Please send a text message or leave a voicemail.",
            "hi": "इस समय मुझे अधिक कॉल आ रही हैं। कृपया टेक्स्ट मैसेज भेजें या वॉइसमेल छोड़ें।",
            "es": "Estoy experimentando un alto volumen de llamadas en este momento. Por favor, envíe un mensaje de texto o deje un correo de voz.",
            "fr": "Je reçois un volume élevé d'appels en ce moment. Veuillez envoyer un SMS ou laisser un message vocal.",
            "de": "Ich habe derzeit ein hohes Anrufaufkommen. Bitte senden Sie eine SMS oder hinterlassen Sie eine Voicemail.",
        },
        "general": {
            "en": "I understand. I have noted that down for my owner and they will get back to you soon. Is there anything else?",
            "hi": "मैं समझता हूं। मैंने यह अपने मालिक के लिए नोट कर लिया है और वे जल्द ही आपसे संपर्क करेंगे। कुछ और है?",
            "es": "Entiendo. He anotado eso para mi propietario y se pondrán en contacto con usted pronto. ¿Hay algo más?",
            "fr": "Je comprends. J'ai noté cela pour mon propriétaire et ils vous contacteront bientôt. Y a-t-il autre chose?",
            "de": "Ich verstehe. Ich habe das für meinen Besitzer notiert und sie werden sich bald bei Ihnen melden. Gibt es noch etwas?",
        }
    }

    return error_messages.get(error_type, {}).get(language_code, error_messages[error_type]["en"])


def end_and_summarize_call(call_sid, call_status="completed", duration_seconds=0):
    """
    Finalize a call, generate an automated AI summary and action items, and store to logs.
    """
    if call_sid not in active_calls:
        return None

    session = active_calls.pop(call_sid)
    session["end_time"] = datetime.now().isoformat()
    session["status"] = call_status
    session["duration"] = duration_seconds

    # If there was a conversation, let Claude summarize it for the owner
    if len(session["messages"]) > 0:
        try:
            client = get_anthropic_client()
            transcript_text = "\n".join([f"{t['speaker']}: {t['text']}" for t in session["transcript"]])

            summary_prompt = f"""Summarize this phone call that Eliva attended on behalf of the owner.

Transcript:
{transcript_text}

Provide output in JSON format with exactly these keys:
{{
  "caller_name": "extracted name or 'Unknown'",
  "is_urgent": true or false,
  "category": "personal | business | recruiter | delivery | spam | other",
  "summary": "2-3 sentence concise overview of what the caller wanted and what answers were given",
  "action_items": ["action 1", "action 2"],
  "callback_needed": true or false
}}
"""
            res = client.messages.create(
                model=Config.CLAUDE_MODEL,
                max_tokens=1000,
                messages=[{"role": "user", "content": summary_prompt}]
            )

            raw_text = ""
            for block in res.content:
                if block.type == "text":
                    raw_text += block.text

            # Parse JSON
            raw_text = raw_text.strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()

            parsed_summary = json.loads(raw_text)
            session["extracted_info"] = parsed_summary

        except Exception as e:
            print(f"Summary generation error: {e}")
            session["extracted_info"] = {
                "caller_name": "Unknown",
                "is_urgent": False,
                "category": "general",
                "summary": "Call completed. Transcript recorded.",
                "action_items": [],
                "callback_needed": True
            }

    save_call_log(session)
    return session
