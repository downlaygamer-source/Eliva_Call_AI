# 🎯 Eliva Real-Life Setup - Quick Reference

## 30-Second Overview
Eliva is your AI call attendant that answers phone calls in 16 languages. It needs:
1. **Anthropic API** (AI brain) - ~$0.015/minute
2. **Twilio** (phone service) - ~$1/month + $0.0085/minute  
3. **Public server** (ngrok/Railway/VPS) - Free to $5/month

---

## ⚡ Quick Start (15 minutes)

### Step 1: Get API Keys (10 min)

**Anthropic:**
```
1. Visit: https://console.anthropic.com/settings/keys
2. Create key (starts with sk-ant-...)
3. Add $5 credits: https://console.anthropic.com/settings/billing
```

**Twilio:**
```
1. Sign up: https://www.twilio.com/try-twilio ($15 free credit)
2. Copy Account SID and Auth Token from dashboard
3. Buy a phone number: Console → Phone Numbers → Buy ($1/month)
```

### Step 2: Configure Eliva (2 min)

Create `D:\eliva\.env`:
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
TWILIO_ACCOUNT_SID=ACxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-token-here
TWILIO_PHONE_NUMBER=+1234567890
MY_PHONE_NUMBER=+1987654321
MY_NAME=Your Name
PORT=5000
```

### Step 3: Install & Run (2 min)

```bash
cd D:\eliva
pip install -r requirements.txt
python run.py
```

### Step 4: Make It Public (1 min)

**Option A - Quick Testing:**
```bash
python run.py --tunnel
# Copy the ngrok URL (https://abc123.ngrok.io)
```

**Option B - Production (Railway):**
```bash
# Push to GitHub, deploy on Railway.app
# See REAL_LIFE_SETUP.md for details
```

### Step 5: Connect Twilio (2 min)

```
1. Go to: https://console.twilio.com/
2. Phone Numbers → Your Number → Configure
3. Voice webhook: https://your-url/voice/incoming (POST)
4. Status webhook: https://your-url/voice/status (POST)
5. Save
```

### Step 6: Test! 📞

Call your Twilio number and speak in any language!

---

## 🎨 Customization

### Update Your Info:
```bash
# Via web interface:
http://localhost:5000/knowledge-base

# Or edit directly:
D:\eliva\knowledge\user_profile.json
```

### Add Custom Rules:
```json
{
  "urgent_contact_rules": [
    "For emergencies, tell them to text URGENT",
    "For deliveries, direct to front door",
    "For job offers, ask them to email resume@example.com"
  ]
}
```

---

## 📊 Monitoring

### View Calls:
- **Dashboard**: `http://your-url/`
- **Call Logs**: `http://your-url/call-logs`
- **Simulator**: `http://your-url/simulator` (test without phone)

### Check Costs:
- **Twilio**: https://console.twilio.com/us1/monitor/usage
- **Anthropic**: https://console.anthropic.com/settings/billing

---

## 🌍 Supported Languages (16)

English • Hindi • Punjabi • Spanish • French • German • Italian • Portuguese • Japanese • Korean • Chinese • Arabic • Russian • Dutch • Polish • Turkish

**Auto-detects language** - just speak naturally!

---

## 💰 Monthly Costs

| Usage | Calls | Minutes | Cost |
|-------|-------|---------|------|
| Light | 50 | 100 min | ~$3 |
| Medium | 200 | 600 min | ~$15 |
| Heavy | 500 | 2000 min | ~$48 |

Plus Railway hosting: **Free**

---

## 🔧 Common Issues

### Eliva doesn't answer:
```bash
# Check server is running
python run.py

# Verify webhook URL in Twilio
# Check Twilio logs: console.twilio.com → Monitor → Logs
```

### Language detection fails:
```bash
# Speak clearly for 3+ seconds
# Check server logs for: "Detected language: XX"
# Verify Anthropic API has credits
```

### Authentication errors:
```bash
# Verify API key in .env
# Check credits: console.anthropic.com/settings/billing
```

---

## 🚀 Deployment Options

### 1. ngrok (Testing) - 5 minutes
```bash
python run.py --tunnel
# Perfect for: Quick testing
# Pros: Instant setup
# Cons: URL changes on restart
```

### 2. Railway (Production) - 15 minutes
```bash
# Push to GitHub → Deploy on Railway.app
# Perfect for: Always-on service
# Pros: Free tier, permanent URL
# Cons: Need GitHub account
```

### 3. VPS (Advanced) - 1 hour
```bash
# Deploy to your own server
# Perfect for: Full control
# Pros: Custom domain, full control
# Cons: Requires server management
```

**See REAL_LIFE_SETUP.md for detailed instructions**

---

## ✅ Pre-Deployment Checklist

Run verification:
```bash
python check_setup.py
```

Manual check:
- [ ] `.env` file created with real API keys
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server starts without errors (`python run.py`)
- [ ] Public URL accessible (ngrok or Railway)
- [ ] Twilio webhooks configured
- [ ] Test call works

---

## 📚 Documentation Files

- **REAL_LIFE_SETUP.md** - Complete deployment guide
- **DEPLOYMENT_GUIDE.md** - Detailed technical setup
- **README.md** - Project overview
- **setup_wizard.py** - Interactive setup tool
- **check_setup.py** - Verify configuration

---

## 🆘 Get Help

**Twilio**: https://www.twilio.com/docs/voice  
**Anthropic**: https://docs.anthropic.com/  
**Railway**: https://docs.railway.app/

---

## 🎉 You're All Set!

Your AI call attendant is ready to answer calls in 16 languages, 24/7.

### What Eliva Does:
✅ Answers calls automatically  
✅ Detects caller's language  
✅ Responds naturally in their language  
✅ Takes messages & action items  
✅ Provides AI summaries  
✅ Marks urgent calls  
✅ Follows your custom rules  

### Next Steps:
1. Customize your knowledge base
2. Test with different languages
3. Forward your personal number (optional)
4. Share your Twilio number with others

**Make your first test call now!** 📞

---

*For questions, see the detailed guides or create an issue on GitHub.*
