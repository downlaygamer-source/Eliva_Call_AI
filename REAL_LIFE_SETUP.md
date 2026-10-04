# 🚀 Eliva Real-Life Deployment Guide

## Quick Start: Get Eliva Answering Real Calls in 15 Minutes

This guide will help you deploy Eliva to answer actual phone calls (not just the demo simulator).

---

## 📋 What You'll Need

### 1. **Anthropic API Account** (Required)
- Sign up: https://console.anthropic.com/
- Cost: ~$0.015 per minute of conversation
- Minimum: $5 credit purchase

### 2. **Twilio Account** (Required)  
- Sign up: https://www.twilio.com/try-twilio
- Free trial: $15 credit included
- Phone number cost: ~$1/month
- Call cost: ~$0.0085/minute

### 3. **Public Server** (Choose One)
- **Option A**: ngrok (free, temporary URL - best for testing)
- **Option B**: Railway.app (free tier, permanent URL - best for production)
- **Option C**: Your own server/VPS

**Total Cost**: ~$2-5/month for moderate use (50-100 calls)

---

## 🎯 Three Deployment Paths

Choose based on your needs:

### Path 1: Quick Testing (15 minutes) ⚡
**Use ngrok for temporary testing**
- ✅ Fastest to set up
- ✅ No account needed beyond Anthropic + Twilio
- ❌ URL changes when you restart
- **Best for**: Testing before committing to production

### Path 2: Production (30 minutes) 🏭
**Use Railway.app for permanent deployment**
- ✅ Always-on, permanent URL
- ✅ Free tier available
- ✅ Auto-restarts if crashes
- **Best for**: Daily use, giving number to others

### Path 3: Advanced (1 hour+) 🔧
**Use your own VPS with custom domain**
- ✅ Full control
- ✅ Custom domain (your-eliva.com)
- ❌ Requires server management skills
- **Best for**: Maximum customization

---

## 🚀 Path 1: Quick Testing with ngrok

### Step 1: Get Your API Keys

#### Anthropic API Key:
1. Go to https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Copy the key (starts with `sk-ant-...`)
4. Add $5+ credits: https://console.anthropic.com/settings/billing

#### Twilio Credentials:
1. Sign up at https://www.twilio.com/try-twilio
2. From the Console Dashboard, copy:
   - **Account SID** (starts with `AC...`)
   - **Auth Token** (click to reveal)
3. Buy a phone number:
   - Go to Phone Numbers → Buy a Number
   - Filter by "Voice" capability
   - Choose your country/area code
   - Buy the number (~$1/month)

### Step 2: Configure Eliva

Create a `.env` file in `D:\eliva\`:

```env
# Anthropic API
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Twilio Credentials
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-auth-token-here
TWILIO_PHONE_NUMBER=+1234567890

# Your Info
MY_PHONE_NUMBER=+1987654321
MY_NAME=Your Name

# Flask
FLASK_SECRET_KEY=random-secret-key-here
PORT=5000
```

### Step 3: Install Dependencies

```bash
cd D:\eliva
pip install -r requirements.txt
```

### Step 4: Start Eliva

```bash
python run.py
```

Server starts at http://localhost:5000

### Step 5: Create Public URL with ngrok

**Option A: Auto-tunnel (if run.py supports it)**
```bash
python run.py --tunnel
```

**Option B: Manual ngrok**

1. Download ngrok: https://ngrok.com/download
2. In a new terminal:
```bash
ngrok http 5000
```

3. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Step 6: Configure Twilio Webhooks

1. Go to Twilio Console → Phone Numbers → Manage → Active Numbers
2. Click your phone number
3. Scroll to "Voice Configuration"
4. Set **"A CALL COMES IN"**:
   - Webhook: `https://abc123.ngrok.io/voice/incoming`
   - HTTP POST
5. Set **"Call Status Changes"** (optional):
   - Primary: `https://abc123.ngrok.io/voice/status`
   - HTTP POST
6. Click **Save**

### Step 7: Test It! 📞

1. Call your Twilio number from any phone
2. Eliva should answer and greet you
3. Speak in any language (English, Hindi, Punjabi, etc.)
4. Check the dashboard: http://localhost:5000

**Try asking:**
- "When is DJ available?"
- "Can I leave a message?"
- "मुझे DJ से बात करनी है" (Hindi)
- "ਮੈਨੂੰ DJ ਨਾਲ ਗੱਲ ਕਰਨੀ ਹੈ" (Punjabi)

---

## 🏭 Path 2: Production Deployment with Railway

### Step 1-2: Same as Path 1
Complete Steps 1-2 from Path 1 (get API keys, configure `.env`)

### Step 3: Prepare for Deployment

Create `Procfile` in `D:\eliva\`:
```
web: python run.py
```

Create `runtime.txt` in `D:\eliva\`:
```
python-3.11.0
```

### Step 4: Push to GitHub

```bash
cd D:\eliva
git init
git add .
git commit -m "Initial Eliva setup"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/yourusername/eliva.git
git branch -M main
git push -u origin main
```

### Step 5: Deploy on Railway

1. Go to https://railway.app/
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your `eliva` repository
6. Railway auto-detects Python and deploys

### Step 6: Add Environment Variables

1. In Railway dashboard, click your project
2. Go to **"Variables"** tab
3. Click **"New Variable"** and add each:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   TWILIO_ACCOUNT_SID=AC...
   TWILIO_AUTH_TOKEN=...
   TWILIO_PHONE_NUMBER=+1234567890
   MY_PHONE_NUMBER=+1987654321
   MY_NAME=Your Name
   PORT=5000
   ```

### Step 7: Get Your Railway URL

1. Go to **"Settings"** → **"Domains"**
2. Click **"Generate Domain"**
3. Copy the URL (e.g., `https://eliva-production.up.railway.app`)

### Step 8: Configure Twilio

Same as Path 1, Step 6, but use your Railway URL:
- Voice webhook: `https://eliva-production.up.railway.app/voice/incoming`
- Status callback: `https://eliva-production.up.railway.app/voice/status`

### Step 9: Monitor & Maintain

**View Logs:**
```bash
# Install Railway CLI
npm install -g @railway/cli
railway login
railway logs
```

**Access Dashboard:**
- Your Railway URL opens the Eliva web dashboard
- View calls, transcripts, and summaries

**Update Eliva:**
```bash
git add .
git commit -m "Update configuration"
git push
# Railway auto-deploys
```

---

## 🎨 Customize Your Knowledge Base

### Via Web Dashboard:
1. Go to `http://your-url/knowledge-base`
2. Update your profile, FAQs, and rules
3. Click Save

### Common Customizations:

**For Business Use:**
```json
{
  "owner": {
    "name": "Your Name",
    "title": "CEO / Founder",
    "current_status": "in a client meeting",
    "available_times": "after 6 PM EST"
  },
  "urgent_contact_rules": [
    "For urgent matters, ask caller to email urgent@company.com",
    "For deliveries, direct to reception at extension 100"
  ]
}
```

**For Personal Use:**
```json
{
  "owner": {
    "name": "Your Name",
    "title": "Software Engineer",
    "current_status": "focused on coding",
    "available_times": "evenings and weekends"
  },
  "urgent_contact_rules": [
    "For emergencies, tell them to text 'URGENT' to my personal number",
    "For family, let them know I'll call back within an hour"
  ]
}
```

---

## 🔍 Troubleshooting

### Issue: Eliva doesn't answer calls

**Check:**
1. Server is running (check Railway logs or terminal)
2. Twilio webhook URLs are correct and use HTTPS
3. Environment variables are set correctly
4. Test the webhook: `curl https://your-url/voice/incoming`

**Twilio Debugging:**
- Go to Twilio Console → Monitor → Logs
- Check recent calls for errors
- Look for webhook failures

### Issue: Language detection not working

**Solution:**
- Speak clearly for 3-5 seconds minimum
- Check server logs for "Detected language: XX"
- Verify Anthropic API key has credits

### Issue: "Authentication Error"

**Solution:**
- Check Anthropic API key is correct
- Verify you have credits: https://console.anthropic.com/settings/billing
- Check logs for exact error message

### Issue: Poor voice quality

**Solutions:**
1. Enable Enhanced Speech in Twilio:
   - Already enabled in code (`enhanced=True`)
2. Check phone connection quality
3. Adjust `speech_timeout` in `app.py`

### Issue: High costs

**Optimize:**
1. Reduce `max_tokens` in `call_manager.py` (currently 1000)
2. Use shorter responses (already optimized)
3. Set max conversation turns in config
4. Monitor usage: https://console.anthropic.com/settings/billing

---

## 💰 Cost Breakdown

### Minimal Usage (50 calls/month, 2 min avg):
- Twilio Phone Number: $1.00/month
- Twilio Call Minutes (100 min): $0.85
- Anthropic API (100 min): $1.50
- **Total: ~$3.35/month**

### Moderate Usage (200 calls/month, 3 min avg):
- Twilio Phone Number: $1.00/month
- Twilio Call Minutes (600 min): $5.10
- Anthropic API (600 min): $9.00
- **Total: ~$15.10/month**

### Heavy Usage (500 calls/month, 4 min avg):
- Twilio Phone Number: $1.00/month
- Twilio Call Minutes (2000 min): $17.00
- Anthropic API (2000 min): $30.00
- **Total: ~$48.00/month**

**Railway hosting:** Free tier (sufficient for most use)

---

## 📊 Monitoring Your Setup

### Check Call Stats:
```
Dashboard: http://your-url/
- Total calls received
- Urgent calls (marked by AI)
- Callbacks needed
- Active call status
```

### View Call Logs:
```
Call Logs: http://your-url/call-logs
- Full transcripts
- AI summaries
- Extracted caller info
- Action items
```

### Monitor Costs:
- **Twilio**: https://console.twilio.com/us1/monitor/usage
- **Anthropic**: https://console.anthropic.com/settings/billing

---

## 🎯 Next Steps

### 1. Forward Your Personal Number
Set up call forwarding on your mobile:
- iPhone: Settings → Phone → Call Forwarding
- Android: Phone → Settings → Call Settings → Call Forwarding
- Forward "When Busy" or "When Unanswered" to your Twilio number

### 2. Test Multiple Languages
Call and speak in different languages:
- English, Hindi, Punjabi, Spanish, French, German, etc.
- Verify Eliva responds in the same language

### 3. Customize FAQs
Add questions people commonly ask you

### 4. Set Up Monitoring
Use uptime monitoring (https://uptimerobot.com) to get alerts if Eliva goes down

### 5. Share with Others
Once tested, give out your Twilio number or forward your existing number

---

## 🆘 Getting Help

**Twilio Issues:**
- Docs: https://www.twilio.com/docs/voice
- Support: https://support.twilio.com/

**Anthropic Issues:**
- Docs: https://docs.anthropic.com/
- Support: https://support.anthropic.com/

**Railway Issues:**
- Docs: https://docs.railway.app/
- Discord: https://discord.gg/railway

**Eliva GitHub:**
- Open an issue for bugs or questions
- Check existing issues for solutions

---

## ✅ Quick Checklist

Before going live, verify:

- [ ] Anthropic API key is set and has credits
- [ ] Twilio account is configured with phone number
- [ ] Server is running and accessible via public URL
- [ ] Twilio webhooks point to your server
- [ ] Knowledge base is customized with your info
- [ ] Test call works and Eliva responds correctly
- [ ] Language detection works for your use case
- [ ] Dashboard shows call logs correctly
- [ ] Monitoring is set up (optional)
- [ ] Cost limits are understood and acceptable

---

**You're ready! Eliva is now your 24/7 multilingual AI call attendant.** 🎉

For the absolute quickest start, run:
```bash
cd D:\eliva
python setup_wizard.py
```
This interactive wizard will guide you through the setup step-by-step.
