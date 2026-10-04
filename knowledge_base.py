"""
Eliva - Knowledge Base & Context Store
Manages personal information, FAQs, and rules for answering calls.
"""

import json
import os

KNOWLEDGE_FILE = os.path.join(os.path.dirname(__file__), "knowledge", "user_profile.json")

DEFAULT_KNOWLEDGE = {
    "owner": {
        "name": "DJ",
        "title": "Software Engineer & Builder",
        "current_status": "busy in a meeting / coding session",
        "available_times": "after 5 PM on weekdays, anytime on weekends",
        "email": "contact@example.com",
    },
    "urgent_contact_rules": [
        "If it's an emergency, tell the caller to text 'URGENT' to the personal number.",
        "If it's a delivery driver, tell them to leave the package at the front door or call again in 10 mins.",
        "If it's a recruiter/job offer, politely ask them to send an email with the job description.",
        "If it's a sales/telemarketer, politely decline and end the call.",
        "If it's friends/family, let them know you'll call them back as soon as you're free."
    ],
    "faq": [
        {
            "question": "Where are you?",
            "answer": "Currently busy with work/meetings and unavailable to take direct calls right now."
        },
        {
            "question": "When can I talk to you?",
            "answer": "Usually free after 5 PM on weekdays or anytime on weekends. You can also send a text message."
        },
        {
            "question": "Can you call me back?",
            "answer": "Yes, I will take your message, phone number, and reason for calling, and make sure they get it right away."
        }
    ],
    "custom_instructions": "Be polite, warm, professional, and concise. Keep responses under 2-3 sentences since this is a phone call. Never give out sensitive personal info like home address or passwords."
}


def load_knowledge():
    """Load knowledge from JSON file or return default."""
    if os.path.exists(KNOWLEDGE_FILE):
        try:
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_KNOWLEDGE
    return DEFAULT_KNOWLEDGE


def save_knowledge(data):
    """Save knowledge to JSON file."""
    os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_system_prompt(caller_number=None, language_code="en"):
    """Build the dynamic system prompt for Claude based on knowledge base and detected language."""
    kb = load_knowledge()
    owner = kb.get("owner", {})

    rules_text = "\n".join([f"- {r}" for r in kb.get("urgent_contact_rules", [])])
    faq_text = "\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in kb.get("faq", [])])

    # Language-specific instruction
    language_instruction = _get_language_instruction(language_code)

    prompt = f"""You are Eliva, a smart, polite, and helpful AI personal assistant and call attendant.
You are answering a phone call on behalf of {owner.get('name', 'your owner')}, who is currently busy ({owner.get('current_status', 'unavailable')}).

{language_instruction}

Your primary responsibilities:
1. Greet the caller warmly and introduce yourself: "Hi, I'm Eliva, an AI assistant for {owner.get('name')}. They're currently busy, but I can help you, answer questions, or take a detailed message."
2. Answer the caller's questions on the spot using the knowledge base and common sense.
3. If they need to reach {owner.get('name')} urgently, explain how or follow the urgent contact rules.
4. If they want to leave a message, collect:
   - Caller's name
   - Reason for calling
   - Any specific questions or deadlines
   - Best callback number/time
5. Keep answers short, conversational, and direct (1-3 sentences maximum per turn) since this is a spoken phone conversation.
6. Do NOT use markdown, bullet points, asterisks, or formatting - speak in plain text naturally.
7. Always remain courteous, empathetic, and professional.
8. Be culturally sensitive and adapt your tone to match the caller's communication style.

Owner Profile:
- Name: {owner.get('name')}
- Role: {owner.get('title')}
- Status: {owner.get('current_status')}
- Availability: {owner.get('available_times')}
- Email: {owner.get('email')}

Handling Rules:
{rules_text}

Frequently Asked Questions:
{faq_text}

Custom Instructions:
{kb.get('custom_instructions', '')}

Caller Number: {caller_number or 'Unknown'}
"""
    return prompt


def _get_language_instruction(language_code):
    """Return language-specific instructions for Claude."""
    language_instructions = {
        "en": "IMPORTANT: The caller is speaking English. Respond entirely in English.",
        "hi": "महत्वपूर्ण: कॉल करने वाला हिंदी बोल रहा है। पूरी तरह से हिंदी में जवाब दें। (IMPORTANT: The caller is speaking Hindi. Respond entirely in Hindi.)",
        "pa": "ਮਹੱਤਵਪੂਰਨ: ਕਾਲ ਕਰਨ ਵਾਲਾ ਪੰਜਾਬੀ ਬੋਲ ਰਿਹਾ ਹੈ। ਪੂਰੀ ਤਰ੍ਹਾਂ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ। (IMPORTANT: The caller is speaking Punjabi. Respond entirely in Punjabi.)",
        "es": "IMPORTANTE: La persona que llama está hablando español. Responde completamente en español. (IMPORTANT: The caller is speaking Spanish. Respond entirely in Spanish.)",
        "fr": "IMPORTANT: L'appelant parle français. Répondez entièrement en français. (IMPORTANT: The caller is speaking French. Respond entirely in French.)",
        "de": "WICHTIG: Der Anrufer spricht Deutsch. Antworten Sie vollständig auf Deutsch. (IMPORTANT: The caller is speaking German. Respond entirely in German.)",
        "it": "IMPORTANTE: Il chiamante sta parlando italiano. Rispondi interamente in italiano. (IMPORTANT: The caller is speaking Italian. Respond entirely in Italian.)",
        "pt": "IMPORTANTE: O chamador está falando português. Responda totalmente em português. (IMPORTANT: The caller is speaking Portuguese. Respond entirely in Portuguese.)",
        "ja": "重要: 発信者は日本語を話しています。完全に日本語で応答してください。(IMPORTANT: The caller is speaking Japanese. Respond entirely in Japanese.)",
        "ko": "중요: 발신자가 한국어를 사용하고 있습니다. 전적으로 한국어로 응답하십시오. (IMPORTANT: The caller is speaking Korean. Respond entirely in Korean.)",
        "zh": "重要：来电者正在说中文。完全用中文回复。(IMPORTANT: The caller is speaking Chinese. Respond entirely in Chinese.)",
        "ar": "مهم: المتصل يتحدث العربية. الرد بالكامل باللغة العربية. (IMPORTANT: The caller is speaking Arabic. Respond entirely in Arabic.)",
        "ru": "ВАЖНО: Абонент говорит по-русски. Отвечайте полностью на русском языке. (IMPORTANT: The caller is speaking Russian. Respond entirely in Russian.)",
        "nl": "BELANGRIJK: De beller spreekt Nederlands. Reageer volledig in het Nederlands. (IMPORTANT: The caller is speaking Dutch. Respond entirely in Dutch.)",
        "pl": "WAŻNE: Dzwoniący mówi po polsku. Odpowiedz całkowicie po polsku. (IMPORTANT: The caller is speaking Polish. Respond entirely in Polish.)",
        "tr": "ÖNEMLİ: Arayan Türkçe konuşuyor. Tamamen Türkçe olarak yanıt verin. (IMPORTANT: The caller is speaking Turkish. Respond entirely in Turkish.)",
    }

    return language_instructions.get(language_code, language_instructions["en"])
