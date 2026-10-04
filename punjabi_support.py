"""
Punjabi language support additions for Eliva
"""

# Add Punjabi error messages
PUNJABI_ERROR_MESSAGES = {
    "auth": "ਮੈਨੂੰ ਮਾਫੀ ਹੈ, ਪਰ ਮੇਰੀ AI ਸੇਵਾ ਦੇ ਕ੍ਰੇਡੈਂਸ਼ੀਅਲ ਸਹੀ ਢੰਗ ਨਾਲ ਸੰਰਚਿਤ ਨਹੀਂ ਹਨ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣਾ ਨਾਮ ਅਤੇ ਨੰਬਰ ਛੱਡੋ, ਅਤੇ ਮੇਰੇ ਮਾਲਕ ਤੁਹਾਨੂੰ ਵਾਪਸ ਕਾਲ ਕਰਨਗੇ।",
    "rate_limit": "ਇਸ ਸਮੇਂ ਮੈਨੂੰ ਬਹੁਤ ਸਾਰੀਆਂ ਕਾਲਾਂ ਆ ਰਹੀਆਂ ਹਨ। ਕਿਰਪਾ ਕਰਕੇ ਟੈਕਸਟ ਮੈਸੇਜ ਭੇਜੋ ਜਾਂ ਵੌਇਸਮੇਲ ਛੱਡੋ।",
    "general": "ਮੈਂ ਸਮਝਦਾ ਹਾਂ। ਮੈਂ ਇਹ ਆਪਣੇ ਮਾਲਕ ਲਈ ਨੋਟ ਕਰ ਲਿਆ ਹੈ ਅਤੇ ਉਹ ਜਲਦੀ ਹੀ ਤੁਹਾਡੇ ਨਾਲ ਸੰਪਰਕ ਕਰਨਗੇ। ਕੁਝ ਹੋਰ?"
}

# Punjabi closing phrases to add to detection
PUNJABI_CLOSING_PHRASES = [
    "ਅਲਵਿਦਾ",  # goodbye
    "ਧੰਨਵਾਦ",  # thank you
    "ਫਿਰ ਮਿਲਾਂਗੇ",  # see you again
    "ਸਤ ਸ੍ਰੀ ਅਕਾਲ",  # Sikh greeting/goodbye
]
