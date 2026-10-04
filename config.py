"""
Eliva - AI Call Attendant
Configuration and settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Anthropic
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    CLAUDE_MODEL = "claude-opus-5-5"

    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # Personal
    MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")
    MY_NAME = os.getenv("MY_NAME", "the person you're trying to reach")

    # Flask
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "eliva-secret-key")
    PORT = int(os.getenv("PORT", 5000))

    # Eliva behavior
    MAX_CONVERSATION_TURNS = 10
    SPEECH_VOICE = "Polly.Joanna"  # Twilio TTS voice
    SPEECH_LANGUAGE = "en-US"
    RECORD_CALLS = True
