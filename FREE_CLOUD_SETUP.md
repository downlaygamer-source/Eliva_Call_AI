# 🆓 FREE Eliva Cloud Deployment Guide
## Complete Step-by-Step Instructions (No Credit Card Required*)

**Last Updated: October 4, 2026**

---

## ⚠️ Important Clarification About "FREE"

### What's Actually FREE:
✅ **Server Hosting**: Railway.app, Render.com, Fly.io (Free tiers)  
✅ **ngrok**: Free temporary URLs for testing  
✅ **Git/GitHub**: Free code hosting  

### What Requires Payment (Cannot Be Avoided):
❌ **Anthropic API**: NO free tier - Minimum $5 required  
❌ **Twilio Phone Number**: $1/month minimum  
❌ **Twilio Call Minutes**: $0.0085 per minute  

### Absolute Minimum Cost: **~$2/month**
- Twilio number: $1/month
- Anthropic API: ~$1/month (for 50-100 calls)

**There is NO way to make a real AI phone system completely free** - phone numbers and AI APIs cost money.

---

## 🎯 Choose Your FREE Hosting Option

I'll show you 3 completely FREE hosting platforms:

1. **Railway.app** (Recommended) ⭐
2. **Render.com** (Alternative)
3. **Fly.io** (For advanced users)

---

## 📋 What You'll Need (One-Time Setup)

### Required (No way around these):
1. **Anthropic Account** - https://console.anthropic.com/
   - Minimum $5 deposit required (NO free tier exists)
   - Get API key
   
2. **Twilio Account** - https://www.twilio.com/
   - Free trial gives $15 credit
   - After trial: ~$1/month for phone number
   - Get Account SID, Auth Token, and buy phone number

### For Deployment (All FREE):
3. **GitHub Account** - https://github.com/ (FREE)
4. **Railway/Render Account** - Deploy here (FREE tier)
5. **Git installed** - https://git-scm.com/ (FREE)

---

## 🚀 METHOD 1: Railway.app (Easiest & Recommended)

### Why Railway?
- ✅ Completely FREE tier (500 hours/month)
- ✅ No credit card required for free tier
- ✅ Automatic deployments from GitHub
- ✅ Easy environment variable management
- ✅ Gets a permanent HTTPS URL

---

### STEP 1: Get Anthropic API Key (5 minutes)

1. Go to: https://console.anthropic.com/settings/keys

2. Click **"Create Key"**

3. Copy the key (starts with `sk-ant-...`)
   ```
   Example: sk-ant-api03-abc123def456...
   ```

4. Add credits:
   - Go to: https://console.anthropic.com/settings/billing
   - Click **"Add credits"**
   - **Minimum: $5** (this is required - no free option)

---

### STEP 2: Get Twilio Credentials (10 minutes)

1. **Sign up at Twilio:**
   - Go to: https://www.twilio.com/try-twilio
   - Sign up (phone verification required)
   - You get **$15 FREE trial credit** 🎉

2. **Get your credentials:**
   - From Twilio Console dashboard, copy:
   - **Account SID** (starts with `AC...`)
   - **Auth Token** (click eye icon to reveal)

3. **Buy a phone number:**
   - Go to: Phone Numbers → Buy a Number
   - Search by country/area code
   - **Filter by**: Voice capability ✓
   - Click **Buy** (uses trial credit - FREE during trial)
   - Copy the phone number (e.g., `+1234567890`)

> **Note**: After trial ends, phone number costs **~$1/month**

---

### STEP 3: Prepare Your Code (5 minutes)

1. **Open Command Prompt and navigate to Eliva:**
   ```bash
   cd D:\eliva
   ```

2. **Initialize Git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial Eliva setup for Railway deployment"
   ```

3. **Create a free GitHub account** (if you don't have one):
   - Go to: https://github.com/signup
   - Sign up (FREE)

4. **Create a new repository on GitHub:**
   - Go to: https://github.com/new
   - Repository name: `eliva-ai-assistant`
   - Keep it **Private** (recommended)
   - Don't initialize with anything
   - Click **Create repository**

5. **Push your code to GitHub:**
   ```bash
   # Replace YOUR_USERNAME with your GitHub username
   git remote add origin https://github.com/YOUR_USERNAME/eliva-ai-assistant.git
   git branch -M main
   git push -u origin main
   ```

   If prompted for credentials, use:
   - Username: Your GitHub username
   - Password: Use a Personal Access Token (GitHub → Settings → Developer Settings → Personal Access Tokens)

---

### STEP 4: Deploy to Railway (10 minutes)

1. **Go to Railway.app:**
   - Visit: https://railway.app/
   - Click **"Start a New Project"**
   - Sign in with GitHub (this is FREE)

2. **Authorize Railway:**
   - Allow Railway to access your GitHub repos
   - Click **"Authorize Railway"**

3. **Create new project:**
   - Click **"Deploy from GitHub repo"**
   - Select **"Configure GitHub App"**
   - Choose your `eliva-ai-assistant` repository
   - Click **"Install & Authorize"**

4. **Select repository:**
   - Click on `eliva-ai-assistant`
   - Railway will automatically detect Python
   - Click **"Deploy Now"**

---

### STEP 5: Configure Environment Variables (5 minutes)

1. **In Railway dashboard, click your project**

2. **Go to the "Variables" tab**

3. **Click "New Variable"** and add each one:

   ```env
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your-auth-token-here
   TWILIO_PHONE_NUMBER=+1234567890
   MY_PHONE_NUMBER=+1987654321
   MY_NAME=Your Name
   PORT=5000
   ```

4. **Click "Deploy"** after adding all variables

---

### STEP 6: Get Your Railway URL (2 minutes)

1. **In Railway, go to "Settings" tab**

2. **Scroll to "Networking" section**

3. **Click "Generate Domain"**

4. **Copy your URL** (e.g., `https://eliva-production.up.railway.app`)

---

### STEP 7: Configure Twilio Webhooks (3 minutes)

1. **Go to Twilio Console:**
   - https://console.twilio.com/

2. **Navigate to Phone Numbers:**
   - Phone Numbers → Manage → Active Numbers
   - Click on your phone number

3. **Scroll to "Voice Configuration"**

4. **Set "A CALL COMES IN":**
   - Select: **Webhook**
   - URL: `https://your-railway-url.up.railway.app/voice/incoming`
   - HTTP Method: **HTTP POST**

5. **Set "Call Status Changes":**
   - URL: `https://your-railway-url.up.railway.app/voice/status`
   - HTTP Method: **HTTP POST**

6. **Click "Save Configuration"**

---

### STEP 8: Test Your Setup! 📞

1. **Call your Twilio number** from any phone

2. **Eliva should answer and greet you!**

3. **Try speaking in different languages:**
   - "Hello, I need to speak with [Your Name]"
   - "नमस्ते, मुझे बात करनी है" (Hindi)
   - "ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਮੈਨੂੰ ਗੱਲ ਕਰਨੀ ਹੈ" (Punjabi)

4. **Check your dashboard:**
   - Open: `https://your-railway-url.up.railway.app/`
   - See call logs and AI summaries

---

## 🚀 METHOD 2: Render.com (Alternative FREE Option)

### Why Render?
- ✅ Completely FREE tier
- ✅ No credit card required
- ✅ Automatic HTTPS
- ⚠️ Slower cold starts (free tier spins down after 15 min)

---

### STEP 1-3: Same as Railway (Get APIs & Prepare Code)

Follow Railway steps 1-3 above to:
- Get Anthropic API key
- Get Twilio credentials
- Push code to GitHub

---

### STEP 4: Deploy to Render

1. **Go to Render.com:**
   - Visit: https://render.com/
   - Sign up with GitHub (FREE)

2. **Create new Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Click **"Connect account"** (GitHub)
   - Select your `eliva-ai-assistant` repository

3. **Configure service:**
   - Name: `eliva-ai-assistant`
   - Region: Choose closest to you
   - Branch: `main`
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`
   - **Plan: FREE** ⭐

4. **Add Environment Variables:**
   Click "Advanced" → Add each variable:
   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   TWILIO_ACCOUNT_SID=AC...
   TWILIO_AUTH_TOKEN=...
   TWILIO_PHONE_NUMBER=+1234567890
   MY_PHONE_NUMBER=+1987654321
   MY_NAME=Your Name
   PORT=5000
   ```

5. **Click "Create Web Service"**

6. **Wait for deployment** (2-3 minutes)

7. **Copy your Render URL** (e.g., `https://eliva-ai-assistant.onrender.com`)

---

### STEP 5: Configure Twilio (Same as Railway Step 7)

Use your Render URL in Twilio webhooks:
- Voice webhook: `https://your-app.onrender.com/voice/incoming`
- Status webhook: `https://your-app.onrender.com/voice/status`

---

## 🚀 METHOD 3: Fly.io (For Advanced Users)

### Why Fly.io?
- ✅ FREE tier (3 VMs included)
- ✅ Fast global deployment
- ⚠️ Requires command-line comfort

---

### STEP 1-3: Same as Above

Get your API keys and prepare code (Railway steps 1-3)

---

### STEP 4: Deploy to Fly.io

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Sign up and login:**
   ```bash
   fly auth signup
   # Or if you have account:
   fly auth login
   ```

3. **Navigate to your project:**
   ```bash
   cd D:\eliva
   ```

4. **Create fly.toml configuration:**
   ```bash
   fly launch --name eliva-ai-assistant --no-deploy
   ```

5. **Edit fly.toml** (created in D:\eliva):
   ```toml
   app = "eliva-ai-assistant"
   
   [build]
   
   [env]
     PORT = "8080"
   
   [[services]]
     internal_port = 8080
     protocol = "tcp"
   
     [[services.ports]]
       handlers = ["http"]
       port = 80
   
     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   ```

6. **Set environment variables:**
   ```bash
   fly secrets set ANTHROPIC_API_KEY=sk-ant-...
   fly secrets set TWILIO_ACCOUNT_SID=AC...
   fly secrets set TWILIO_AUTH_TOKEN=...
   fly secrets set TWILIO_PHONE_NUMBER=+1234567890
   fly secrets set MY_PHONE_NUMBER=+1987654321
   fly secrets set MY_NAME="Your Name"
   ```

7. **Deploy:**
   ```bash
   fly deploy
   ```

8. **Get your URL:**
   ```bash
   fly info
   # Copy the hostname (e.g., eliva-ai-assistant.fly.dev)
   ```

9. **Configure Twilio** with your Fly.io URL

---

## 🎨 Customize Your Eliva

### Access Web Dashboard:
```
https://your-deployment-url/
```

### Update Knowledge Base:
```
https://your-deployment-url/knowledge-base
```

### Add Custom Rules:

1. Go to knowledge base editor
2. Add rules like:
   - "For job offers, ask for email"
   - "For deliveries, tell them to leave at door"
   - "For emergencies, give them my alternate number"
3. Add FAQs your callers commonly ask
4. Click Save

---

## 📊 Monitor Your Free Tiers

### Railway Free Tier Limits:
- ✅ **500 hours/month** (always-on = ~720 hours)
- ✅ **1GB RAM**
- ✅ **1GB disk**
- Perfect for Eliva!

### Render Free Tier Limits:
- ✅ **750 hours/month**
- ✅ **512MB RAM**
- ⚠️ Spins down after 15 min inactive
- ⚠️ Cold start takes ~30 seconds

### Fly.io Free Tier Limits:
- ✅ **3 shared VMs**
- ✅ **256MB RAM each**
- ✅ **3GB storage**

**All three are enough for Eliva!**

---

## 💰 Real Cost Breakdown

### Monthly Costs (You CANNOT avoid these):

| Item | Free Trial | After Trial |
|------|------------|-------------|
| **Anthropic API** | ❌ NO free tier | $1-3/month (light use) |
| **Twilio Phone #** | ✅ Covered by $15 trial | $1/month |
| **Twilio Minutes** | ✅ Covered by trial (100+ calls) | $0.0085/min |
| **Hosting** | ✅ FREE forever | ✅ FREE forever |

### Example Cost After Trial:
- 50 calls/month (100 minutes total): **~$2.85/month**
- 200 calls/month (400 minutes): **~$8.40/month**

**No way to reduce Anthropic cost - they don't have free tier**

---

## 🔧 Troubleshooting

### Railway deployment failed?
```bash
# Check logs in Railway dashboard
# Click on deployment → View logs
# Common issues:
# - Missing Procfile (already included)
# - Wrong Python version (already configured)
```

### Render service won't start?
```bash
# Check "Events" tab for errors
# Common fix: Add PORT=10000 to environment variables
# Render uses port 10000, not 5000
```

### Twilio webhook errors?
```bash
# Check webhook URLs:
# - Must use HTTPS (not HTTP)
# - Must end with /voice/incoming
# - Must be POST method
# 
# Test URL: https://your-url/voice/incoming
# Should return some XML response
```

### Calls not connecting?
```bash
# Check Twilio Console → Monitor → Logs
# Look for webhook errors
# Verify your deployment is online
```

---

## ✅ Deployment Checklist

- [ ] Anthropic API key obtained ($5 minimum added)
- [ ] Twilio account created ($15 free trial credit)
- [ ] Twilio phone number purchased
- [ ] Code pushed to GitHub
- [ ] Deployed to Railway/Render/Fly.io
- [ ] Environment variables configured
- [ ] Deployment is live (check URL)
- [ ] Twilio webhooks configured
- [ ] Test call successful
- [ ] Dashboard accessible
- [ ] Knowledge base customized

---

## 🎯 Summary: What's FREE vs PAID

### ✅ Completely FREE:
- Server hosting (Railway/Render/Fly.io free tiers)
- GitHub repository
- Git version control
- SSL/HTTPS certificate
- Web dashboard
- Call logging
- AI summaries

### ❌ Requires Payment (Minimum $2/month):
- Anthropic Claude API ($5 minimum deposit, ~$1-3/month usage)
- Twilio phone number (~$1/month)
- Twilio call minutes (~$0.0085/minute)

### 💡 FREE Trial Period:
- Twilio: $15 credit = ~100-150 calls FREE
- After that: ~$2-8/month depending on usage

---

## 🚀 You're Done!

Your Eliva AI assistant is now:
- ✅ Deployed to the cloud (FREE hosting)
- ✅ Accessible 24/7
- ✅ Answering real phone calls
- ✅ Speaking 16 languages automatically
- ✅ Taking messages and creating AI summaries

**Make your first call and test it now!** 📞

---

## 📚 Need Help?

**Railway**: https://docs.railway.app/  
**Render**: https://render.com/docs/  
**Fly.io**: https://fly.io/docs/  
**Twilio**: https://www.twilio.com/docs/voice  
**Anthropic**: https://docs.anthropic.com/

---

*Remember: There's no way to make a real AI phone system 100% free. Phone numbers and AI APIs have unavoidable costs (~$2/month minimum).*
