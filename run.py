"""
Eliva - Application Launcher
Starts the Flask server and optionally creates an ngrok public tunnel for Twilio webhooks.
"""

import sys
import os
import argparse
from app import app
from config import Config


def main():
    parser = argparse.ArgumentParser(description="Run Eliva AI Call Attendant")
    parser.add_argument("--tunnel", action="store_true", help="Start an ngrok public HTTPS tunnel for Twilio webhooks")
    parser.add_argument("--port", type=int, default=Config.PORT, help="Port to run the server on")
    args = parser.parse_args()

    port = args.port

    if args.tunnel:
        try:
            from pyngrok import ngrok
            public_url = ngrok.connect(port, "http").public_url
            print("\n" + "═" * 60)
            print("📞 ELIVA PUBLIC TWILIO WEBHOOK URLS:")
            print(f"  Voice Webhook:  {public_url}/voice/incoming")
            print(f"  Status Callback: {public_url}/voice/status")
            print("═" * 60 + "\n")
        except Exception as e:
            print(f"⚠️  Could not start ngrok tunnel: {e}")
            print("You can run ngrok manually: ngrok http 5000\n")

    print(f"\n✨ Eliva is running locally at: http://127.0.0.1:{port}")
    print(f"👉 Open your browser to test with the Simulator or configure Knowledge Base.\n")

    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
