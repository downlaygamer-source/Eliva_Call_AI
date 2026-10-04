# Eliva - Real-Life Deployment Guide

## 🚀 How to Use Eliva in Real Life (Not Demo)

This guide will help you set up Eliva to answer real phone calls automatically.

---

## Prerequisites

### 1. **Anthropic API Key** (Required)
- Sign up at: https://console.anthropic.com/
- Create an API key
- Cost: ~$0.015 per minute of conversation (Claude Opus 5.5)
- You'll need to add credits to your Anthropic account

### 2. **Twilio Account** (Required)
- Sign up at: https://www.twilio.com/
- You'll get a free trial with $15 credit
- After trial: ~$1/month for phone number + $0.0085/minute for calls

### 3. **Server with Public URL** (Required - Choose One)

#### Option A: **ngrok** (Easiest for Testing)
- Free temporary URL
- Download: https://ngrok.com/download
- Good for: Testing and development

#### Option B: **Railway.app** (Recommended for Production)
- Free tier available
- Persistent URL
- Good for: Always-on deployment
- Sign up: https://railway.app/

#### Option C: **Heroku**
- Free tier available
- Sign up: https://www.heroku.com/

#### Option D: **Your Own VPS**
- DigitalOcean, AWS, Google Cloud, etc.
- Needs public IP and domain

---

## 📝 Step-by-Step Setup

### Step 1: Configure Environment Variables

1. Create a `.env` file in the `D:/eliva` directory:

```bash
# Anthropic API (Required)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Twilio Credentials (Required)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Your Personal Info (Required)
MY_PHONE_NUMBER=+1987654321
MY_NAME=Your Name

# Flask (Optional)
FLASK_SECRET_KEY=random_secret_key_here
PORT=5000
```

### Step 2: Get Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign in or create account
3. Go to "API Keys" section
4. Click "Create Key"
5. Copy the key and paste it in `.env` as `ANTHROPIC_API_KEY`
6. Add credits to your account (minimum $5)

### Step 3: Set Up Twilio

1. **Sign Up for Twilio**
   - Go to https://www.twilio.com/try-twilio
   - Sign up for free trial ($15 credit)

2. **Get a Phone Number**
   - In Twilio Console, go to "Phone Numbers" → "Buy a number"
   - Choose your country
   - Select a number with "Voice" capability
   - For India: Choose a number from your region
   - Cost: ~$1/month

3. **Get Twilio Credentials**
   - In Twilio Console dashboard, find:
     - Account SID
     - Auth Token
   - Copy both to your `.env` file

### Step 4: Deploy Eliva (Choose Your Method)

---

#### 🟢 Method A: Using ngrok (Quick Testing)

**Best for: Testing how it works before committing to a server**

1. **Install ngrok**
   ```bash
   # Download from https://ngrok.com/download
   # Or install via chocolatey on Windows:
   choco install ngrok
   ```

2. **Start Eliva**
   ```bash
   cd D:/eliva
   python run.py
   ```
   (Server starts on http://localhost:5000)

3. **Start ngrok in another terminal**
   ```bash
   ngrok http 5000
   ```

4. **Copy the ngrok URL**
   - You'll see something like: `https://abc123.ngrok.io`
   - Copy this URL

5. **Configure Twilio Webhook**
   - Go to Twilio Console → Phone Numbers → Your Number
   - Under "Voice & Fax", set:
     - **A CALL COMES IN**: Webhook
     - URL: `https://abc123.ngrok.io/voice/incoming`
     - HTTP: `POST`
   - Under "Call Status Changes":
     - URL: `https://abc123.ngrok.io/voice/status`
     - HTTP: `POST`
   - Click "Save"

6. **Test It!**
   - Call your Twilio number from any phone
   - Eliva should answer and speak to you

⚠️ **Note**: ngrok URL changes every time you restart it (unless you pay for a static URL)

---

#### 🟢 Method B: Using Railway.app (Recommended for Production)

**Best for: Always-on, persistent deployment**

1. **Prepare for Deployment**
   
   Create `Procfile` in D:/eliva:
   ```
   web: python run.py
   ```

   Create `runtime.txt` in D:/eliva:
   ```
   python-3.11.0
   ```

2. **Push to GitHub** (if not already)
   ```bash
   cd D:/eliva
   git init
   git add .
   git commit -m "Initial Eliva setup"
   # Create repo on GitHub and push
   git remote add origin https://github.com/yourusername/eliva.git
   git push -u origin main
   ```

3. **Deploy on Railway**
   - Go to https://railway.app/
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `eliva` repository
   - Railway will auto-detect Python and deploy

4. **Add Environment Variables on Railway**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add all variables from your `.env` file:
     - ANTHROPIC_API_KEY
     - TWILIO_ACCOUNT_SID
     - TWILIO_AUTH_TOKEN
     - TWILIO_PHONE_NUMBER
     - MY_PHONE_NUMBER
     - MY_NAME
     - PORT=5000

5. **Get Railway URL**
   - In Railway, go to "Settings" → "Domains"
   - Click "Generate Domain"
   - You'll get: `https://eliva-production-abc.up.railway.app`

6. **Configure Twilio with Railway URL**
   - Go to Twilio Console → Phone Numbers → Your Number
   - Set webhooks to your Railway URL:
     - Voice webhook: `https://your-railway-url.railway.app/voice/incoming`
     - Status callback: `https://your-railway-url.railway.app/voice/status`

---

#### 🟢 Method C: Using Your Own Server (VPS)

**Best for: Full control, advanced users**

1. **SSH into your server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **Clone or upload Eliva**
   ```bash
   cd /var/www/
   git clone https://github.com/yourusername/eliva.git
   cd eliva
   ```

4. **Install Python packages**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   nano .env
   # Paste all your environment variables
   ```

6. **Run with gunicorn**
   ```bash
   pip3 install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

7. **Configure Nginx as reverse proxy**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

8. **Set up SSL with Let's Encrypt** (Twilio requires HTTPS)
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

9. **Configure Twilio**
   - Use your domain: `https://your-domain.com/voice/incoming`

---

## 🎯 Step 5: Customize Your Knowledge Base

1. **Access the Web Dashboard**
   - Open: `http://your-server-url/knowledge-base`
   - Or: `http://localhost:5000/knowledge-base` (local)

2. **Update Your Profile**
   - Name: Your actual name
   - Title: Your job title
   - Current Status: What you're usually doing
   - Available Times: When people can reach you
   - Email: Your contact email

3. **Add Custom Rules**
   Examples:
   ```
   If it's family, tell them I'll call back within an hour
   If it's a job opportunity, ask them to email the details
   If it's a delivery, tell them to leave it at the door
   If it's urgent, ask them to text "URGENT" to my number
   ```

4. **Add FAQs**
   - Common questions people ask you
   - Your standard answers

5. **Set Custom Instructions**
   - How Eliva should behave
   - Tone and style preferences
   - Any special handling rules

---

## 🧪 Testing Your Setup

### Test 1: Call Your Number
```
1. Call your Twilio number
2. Eliva should answer with greeting
3. Speak naturally in any language
4. Eliva responds in the same language
5. Try asking questions from your FAQ
```

### Test 2: Check the Dashboard
```
1. Go to http://your-server-url/
2. See call statistics
3. View recent calls
4. Read AI summaries
```

### Test 3: Review Call Logs
```
1. Go to http://your-server-url/call-logs
2. See full transcripts
3. Check if language detection worked
4. Review action items Eliva created
```

---

## 💰 Cost Breakdown (Monthly)

### Minimal Usage (~50 minutes/month):
- Twilio Phone Number: **$1.00**
- Twilio Call Minutes (50 min): **$0.43**
- Anthropic API (50 min): **$0.75**
- **Total: ~$2.20/month**

### Moderate Usage (~200 minutes/month):
- Twilio Phone Number: **$1.00**
- Twilio Call Minutes: **$1.70**
- Anthropic API: **$3.00**
- **Total: ~$5.70/month**

### Heavy Usage (~500 minutes/month):
- Twilio Phone Number: **$1.00**
- Twilio Call Minutes: **$4.25**
- Anthropic API: **$7.50**
- **Total: ~$12.75/month**

---

## 🔧 Troubleshooting

### Issue: Eliva doesn't answer calls
**Check:**
1. Is your server running? (Check Railway/ngrok logs)
2. Is Twilio webhook configured correctly?
3. Are environment variables set?
4. Check Twilio Console → Monitor → Logs for errors

### Issue: Language detection not working
**Check:**
1. Speak clearly for at least 3-5 seconds
2. Anthropic API key is valid
3. Check server logs: `detected language: XX`

### Issue: Voice quality is poor
**Try:**
1. Use enhanced speech recognition in Twilio
2. Adjust `speech_timeout` in app.py
3. Ensure good phone connection

### Issue: Authentication errors
**Check:**
1. Anthropic API key is correct
2. You have credits in Anthropic account
3. Check: https://console.anthropic.com/settings/billing

---

## 📊 Monitoring

### Check Real-Time Status
```bash
# If using Railway
railway logs

# If using ngrok
# Check ngrok dashboard: http://127.0.0.1:4040

# If using your own server
tail -f /var/log/eliva.log
```

### Monitor Costs
- **Twilio**: https://console.twilio.com/us1/monitor/logs/usage
- **Anthropic**: https://console.anthropic.com/settings/billing

---

## 🔒 Security Best Practices

1. **Never commit .env file**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use strong secrets**
   ```bash
   # Generate random secret
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Enable Twilio webhook validation** (Advanced)
   - Add webhook signature validation
   - Prevents unauthorized requests

4. **Use HTTPS only**
   - Twilio requires HTTPS for production
   - Get free SSL with Let's Encrypt

---

## 🎉 You're Live!

Once deployed, Eliva will:
- ✅ Answer all calls to your Twilio number
- ✅ Detect caller's language automatically
- ✅ Respond in their language (16 languages supported)
- ✅ Take messages and action items
- ✅ Provide AI summaries in your dashboard
- ✅ Mark urgent calls
- ✅ Follow your custom rules

### Next Steps:
1. Share your Twilio number with friends/family for testing
2. Monitor the dashboard for call logs
3. Adjust knowledge base based on real calls
4. Consider upgrading to a local phone number (not Twilio)

---

## 🆘 Need Help?

- **Twilio Docs**: https://www.twilio.com/docs/voice
- **Anthropic Docs**: https://docs.anthropic.com/
- **Railway Docs**: https://docs.railway.app/
- **ngrok Docs**: https://ngrok.com/docs

---

## 📱 Advanced: Using Your Real Phone Number

To forward your existing number to Eliva:

### Option 1: Call Forwarding (Simplest)
1. On your phone, enable call forwarding
2. Forward to your Twilio number
3. Your real number → Twilio → Eliva

### Option 2: Port Your Number to Twilio
1. Contact Twilio support
2. Port your existing number (takes 7-10 days)
3. Costs ~$1/month + call fees

### Option 3: Use a Virtual Phone App
1. Get Google Voice / Skype number
2. Forward to Twilio number
3. Give out the virtual number

---

## 🌟 Pro Tips

1. **Test during off-peak hours first**
   - Make sure everything works before giving out the number

2. **Set up monitoring**
   - Use uptimerobot.com to monitor if server is down
   - Get alerts if Eliva stops responding

3. **Backup call logs**
   - Regularly download call_logs.json
   - Important conversations are saved

4. **Optimize costs**
   - Use shorter responses to reduce API calls
   - Set max conversation turns limit

5. **Multi-language testing**
   - Test with friends who speak different languages
   - Verify detection and response quality

---

**You're all set! Eliva is now your 24/7 multilingual AI call attendant!** 🎊
