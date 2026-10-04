# 📞 Eliva - AI Call Attendant

**Eliva** is an AI-powered personal call attendant designed to answer phone calls when you are busy, in meetings, or away. Powered by **Anthropic Claude Opus 5.5** and **Twilio Voice**, Eliva interacts naturally with callers, answers questions on the spot using your custom knowledge base, manages urgent situations, and provides clear call transcripts and AI summaries with action items.

---

## 🌟 Key Features

1. **On-the-Spot Q&A**: Answers questions about your availability, ongoing work, callback times, and custom FAQs instantly.
2. **Intelligent Call Handling & Filtering**:
   - **Emergency / Urgent Calls**: Directs callers on how to reach you immediately.
   - **Delivery Drivers**: Instructs where to leave packages or when to retry.
   - **Recruiters / Clients**: Collects job/project details and requests email followup.
   - **Spam / Telemarketers**: Politely declines and ends the call.
3. **Full Conversation Context**: Maintains multi-turn context throughout the phone call.
4. **Post-Call AI Summaries & Action Items**: Automatically summarizes what the caller wanted and highlights if a callback or urgent action is required.
5. **Interactive Web Dashboard**:
   - Live call stats & status indicators
   - Knowledge base editor & custom rules manager
   - Full call history & searchable transcripts
6. **In-Browser Voice & Text Simulator**: Test Eliva immediately in your web browser using your microphone or keyboard before connecting to a real phone number.

---

## 🚀 Quick Start Guide

### 1. Installation

Navigate to the project folder and install dependencies:

```bash
cd C:\Users\djgamer\eliva
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `eliva` directory (or copy from `.env.example`):

```ini
ANTHROPIC_API_KEY=your_anthropic_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid       # Optional for local simulator
TWILIO_AUTH_TOKEN=your_twilio_token      # Optional for local simulator
TWILIO_PHONE_NUMBER=+1234567890          # Optional for local simulator
MY_NAME=DJ
PORT=5000
```

### 3. Launch Eliva

To start the local server with the web dashboard and simulator:

```bash
python run.py
```

Then open your browser at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📱 Connecting to Real Phone Calls (Twilio Setup)

To have Eliva answer real calls to your phone:

### Step 1: Start Server with Public Webhook (ngrok)
```bash
python run.py --tunnel
```
*(Or run `ngrok http 5000` in a separate terminal).*

This will give you a public HTTPS URL such as `https://xyz123.ngrok-free.app`.

### Step 2: Configure Twilio Phone Number
1. Go to your [Twilio Console -> Phone Numbers](https://console.twilio.com/).
2. Select your Twilio phone number.
3. Under **Voice & Fax** -> **A CALL COMES IN**:
   - Select **Webhook**
   - URL: `https://xyz123.ngrok-free.app/voice/incoming`
   - HTTP Method: `HTTP POST`
4. Under **CALL STATUS CHANGES**:
   - URL: `https://xyz123.ngrok-free.app/voice/status`
   - HTTP Method: `HTTP POST`
5. Click **Save**.

### Step 3: Set Up Call Forwarding on Your Mobile Phone
To route calls to Eliva only when you are busy:
- **iPhone / Android**: Go to **Phone Settings** -> **Call Forwarding** -> Enable **"Forward When Busy"** or **"Forward When Unanswered"** and set the forwarding number to your **Twilio Phone Number**.

---

## 🧠 Customizing Knowledge Base & Rules

You can edit your rules either through the Web Dashboard (`/knowledge-base`) or directly in `knowledge/user_profile.json`:

```json
{
  "owner": {
    "name": "DJ",
    "title": "Software Engineer",
    "current_status": "busy in deep focus work",
    "available_times": "after 5 PM on weekdays"
  },
  "urgent_contact_rules": [
    "If it's an emergency, tell the caller to text 'URGENT' to the personal number."
  ],
  "faq": [
    {
      "question": "When can I talk to you?",
      "answer": "Usually free after 5 PM on weekdays."
    }
  ]
}
```

---

## 📁 Project Structure

```
eliva/
├── app.py                 # Flask app & Twilio voice webhook routes
├── call_manager.py        # Claude LLM call engine & AI summarizer
├── knowledge_base.py      # Profile, FAQs & answering rules logic
├── config.py              # Configuration & environment loader
├── run.py                 # Application launcher (with optional ngrok tunnel)
├── requirements.txt       # Python dependencies
├── knowledge/
│   └── user_profile.json  # Stored owner info & FAQ rules
├── static/
│   ├── app.js             # Simulator Web Speech & audio controller
│   └── style.css          # Custom styling & animations
└── templates/
    ├── base.html          # Base layout template with Tailwind CSS
    ├── index.html         # Main dashboard
    ├── simulator.html     # Interactive in-browser phone simulator
    ├── call_logs.html     # Call transcripts & AI summaries
    └── knowledge_base.html# Rules & FAQ configuration UI
```
