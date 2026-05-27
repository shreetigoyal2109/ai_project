# 🎯 Complete Render Deployment Setup

Everything you need to deploy the AI Interview Platform to Render!

## What You're Getting

✅ **Full FastAPI Application** - Production-ready  
✅ **PostgreSQL Database** - Included  
✅ **GitHub Integration** - Auto-deploy on push  
✅ **Free SSL** - Secure HTTPS  
✅ **24/7 Monitoring** - Built-in logs  
✅ **Auto-scaling** - Handles traffic  

## The 5-Step Deployment Process

### Overview
```
START
  ↓
Step 1: Create Database (1 min)
  ↓
Step 2: Create Web Service (1 min)
  ↓
Step 3: Add API Keys (2 min)
  ↓
Step 4: Deploy (3 min)
  ↓
Step 5: Test & Access (1 min)
  ↓
✅ LIVE ON INTERNET
```

## Step 1: Create PostgreSQL Database ⚡ (1 minute)

**Go to**: https://dashboard.render.com

```
1. Click "+ New"
2. Select "PostgreSQL"
3. Enter:
   Name: ai_project_db
   Database: ai_project
   Region: us-east-1 (or your closest)
4. Click "Create Database"
5. ⭐ COPY the "External Database URL"
```

**What you'll get**:
```
postgresql://user:random_password@hostname.render.com:5432/ai_project
↑↑↑ SAVE THIS - You'll need it in Step 3 ↑↑↑
```

---

## Step 2: Create Web Service ⚡ (1 minute)

**Still in Render Dashboard**:

```
1. Click "+ New"
2. Select "Web Service"
3. Click "Connect" (authorize GitHub)
4. Select "ai_project" repository
5. Fill in:
   Name: ai-project
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   Region: SAME AS DATABASE ⚠️ (important!)
   Instance Type: Free
   Auto Deploy: On
6. Continue to next section (don't deploy yet)
```

**Screenshot your service name** - You'll use it later!

---

## Step 3: Add Environment Variables ⚡ (2 minutes)

**Before clicking "Create Web Service"**, add these variables:

### Required
```
DATABASE_URL
Value: (Paste from Step 1)
```

```
GEMINI_API_KEY
Value: Your Gemini key from https://makersuite.google.com/app/apikey
```

```
SECRET_KEY
Value: python -c "import secrets; print(secrets.token_urlsafe(32))"
(Run locally and paste the output)
```

### Optional (but recommended)
```
OPENAI_API_KEY
Value: Your key from https://platform.openai.com/api-keys
```

```
GROQ_API_KEY
Value: Your key from https://console.groq.com
```

### Configuration
```
ENVIRONMENT = production
DEBUG = False
```

**UI Instructions**:
```
For each variable:
1. Click "+ Add Environment Variable"
2. Enter Key name
3. Enter Value
4. Repeat for all variables
5. Continue
```

---

## Step 4: Deploy! ⚡ (3 minutes)

```
1. Click "Create Web Service" button
2. Render starts building (shows progress)
3. Watch Logs tab for:
   ✅ "Build succeeded"
   ✅ "Deploying..."
   ✅ "Your service is live" ← This is it!
4. Wait for all messages to appear
```

**What's happening**:
- Pulling your code from GitHub
- Installing dependencies
- Building Docker container
- Starting your app
- Connecting to database

**Typical timeline**: 2-3 minutes

---

## Step 5: Test Your App ⚡ (1 minute)

```
Your app is now LIVE!

1. Go to Render Dashboard
2. Click your service name
3. Copy the "Service URL" (top right)
   Format: https://ai-project-xyz123.onrender.com
4. Open in browser with /docs
   https://ai-project-xyz123.onrender.com/docs
5. You should see the API documentation!
```

**Verify everything works**:
```
✅ Service shows "Live" (green status)
✅ Can access /docs endpoint
✅ Can see Swagger UI
✅ Database connected (check logs)
✅ No errors in Logs tab
```

---

## Common Issues & Fixes

### Issue: "Service won't start"

**Cause**: Missing environment variable  
**Fix**:
```
1. Check Settings → Environment
2. Make sure GEMINI_API_KEY is set
3. Make sure SECRET_KEY is set
4. Click "Manual Deploy"
```

### Issue: "Database connection error"

**Cause**: Wrong DATABASE_URL  
**Fix**:
```
1. Go to PostgreSQL service
2. Copy External Database URL again
3. Paste in Web Service → Environment
4. Make sure format is exactly:
   postgresql://user:password@host:port/database
5. Redeploy
```

### Issue: "502 Bad Gateway"

**Cause**: App crashed  
**Fix**:
```
1. Check Logs tab for error messages
2. Look for missing dependencies
3. Verify all API keys are set
4. Check database connection
5. Email support@render.com if stuck
```

---

## After Deployment: Auto-Updates

**Good news**: Any push to GitHub auto-deploys!

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Automatically deploys in 1-2 minutes
# No manual redeploy needed
```

---

## Getting Your API Keys (5 minutes)

### Gemini API Key
```
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy it immediately
4. Paste in Render environment
```

### OpenAI API Key (Optional)
```
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy IMMEDIATELY (won't show again)
4. Paste in Render environment
```

### Groq API Key (Optional)
```
1. Go to https://console.groq.com
2. Sign up / Login
3. Go to API Keys section
4. Create and copy key
5. Paste in Render environment
```

### Generate SECRET_KEY
```bash
# Run this in your terminal:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Output will be something like:
# aBc1234567890_defghijklmnopqrstuvwxyz123456
#
# Copy that and paste in Render
```

---

## Your Live URLs

Once deployed:

```
Main URL:
https://your-service-name.onrender.com

API Documentation (Swagger):
https://your-service-name.onrender.com/docs

Alternative Docs (ReDoc):
https://your-service-name.onrender.com/redoc

OpenAPI JSON:
https://your-service-name.onrender.com/openapi.json
```

---

## Monitoring Your App

### View Logs (Real-time)
```
Render Dashboard → Your Service → Logs tab
See what's happening right now!
```

### Check Status
```
Green dot = All good
Red dot = Something's wrong
Check Logs tab for errors
```

### Database Status
```
Render Dashboard → PostgreSQL service
Shows storage used, backup status, etc.
```

---

## Upgrading Later (Optional)

### When to Upgrade
- App gets users → Upgrade to paid for 24/7
- Need more storage → Upgrade database
- Slow performance → Upgrade web instance

### How to Upgrade
```
Service Settings → Instance Type
Choose Standard, Pro, or Premium
Change takes 5-10 minutes
No downtime
```

### Pricing
```
Free: $0/month (limited)
Standard: $7/month
Pro: $25/month
Premium: $57/month
Database scales separately
```

---

## Backing Up Your Data

### Automatic Backups
```
✅ Render backs up your database daily
✅ Keeps 7 days of backups
✅ Free to restore
```

### How to Restore (if needed)
```
1. PostgreSQL Service → Backups
2. Click the backup date
3. Click "Restore"
4. Takes a few minutes
```

---

## Useful Commands & Links

### Check Your Service Health
```bash
curl https://your-service-name.onrender.com/docs
# Should return HTML page
```

### View Live Logs
```
Dashboard → Service → Logs tab
Scroll to see real-time output
```

### Manually Redeploy
```
Service Settings → Manual Deploy
Select main branch
Click Deploy
```

### Useful Links
```
Render Dashboard: https://dashboard.render.com
Render Docs: https://render.com/docs
Render Status: https://status.render.com
GitHub Integration: https://render.com/docs/deploy-from-github
```

---

## Quick Checklist

Before deploying:
- [ ] Render account created
- [ ] GitHub repository pushed
- [ ] Gemini API key obtained
- [ ] (Optional) OpenAI API key
- [ ] (Optional) Groq API key

After deploying:
- [ ] Service shows "Live"
- [ ] Can access /docs endpoint
- [ ] No errors in Logs
- [ ] Database connected
- [ ] API responds to requests
- [ ] All environment variables set

For production:
- [ ] Custom domain configured
- [ ] Backups enabled
- [ ] Monitoring set up
- [ ] Team invited (if needed)
- [ ] Upgraded to paid plan (if needed for 24/7)

---

## Need Help?

### Check These First
1. [RENDER_GUIDE.md](RENDER_GUIDE.md) - Detailed guide
2. [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Complete reference
3. Render Docs: https://render.com/docs

### Still Stuck?
1. Check Logs tab for specific error
2. Visit https://render.com/support
3. Email support@render.com
4. Open GitHub issue in our repo

---

## You Did It! 🎉

Your AI Interview Platform is now:

```
✅ Live on the internet
✅ Accessible 24/7
✅ Backed by database
✅ Running with AI integrations
✅ Auto-updating from GitHub
✅ Secure with HTTPS
✅ Monitored and logged
```

### Share Your App!

```
Live URL: https://your-service-name.onrender.com
API Docs: https://your-service-name.onrender.com/docs
Repository: https://github.com/shreetigoyal2109/ai_project
Your Profile: https://github.com/shreetigoyal2109
```

### Next Steps

1. Test all API endpoints at `/docs`
2. Configure custom domain (optional)
3. Monitor logs for issues
4. Invite team members
5. Plan scaling for growth

---

**Congratulations! Your app is live! 🚀**

**Questions?** See [RENDER_GUIDE.md](RENDER_GUIDE.md) or visit render.com/docs
