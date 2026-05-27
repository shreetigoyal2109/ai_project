# 🚀 Render Deployment - Complete Setup Guide

## Overview

Deploy your AI Interview Platform to Render in **5 simple steps**. Render offers free tier hosting with automatic GitHub integration!

## Why Render?

✅ Free tier for development  
✅ Automatic GitHub integration  
✅ Auto-deploys on every push  
✅ Included PostgreSQL database  
✅ Free SSL certificate  
✅ No credit card required for free tier  
✅ Easy upgrade path for production  

## Quick Deployment Timeline

```
Step 1: Create Database      (1 minute)
Step 2: Create Web Service   (1 minute)
Step 3: Add API Keys         (2 minutes)
Step 4: Deploy               (3 minutes)
Step 5: Access App           (Instant)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Time: ~7-10 minutes
```

## Detailed Steps

### Step 1️⃣ Create PostgreSQL Database

**Location**: https://render.com/dashboard

1. Click **+ New**
2. Select **PostgreSQL**
3. Enter details:
   ```
   Name: ai_project_db
   Database: ai_project
   User: (auto-generated)
   Region: us-east-1 (pick closest to you)
   PostgreSQL Version: 15
   ```
4. Click **Create Database**
5. **⭐ Copy the External Database URL**
   - Format: `postgresql://user:password@hostname:port/database`
   - You'll paste this in Step 3

### Step 2️⃣ Create Web Service

1. Click **+ New**
2. Select **Web Service**
3. Click **Connect** under GitHub
   - Authorize Render to access GitHub
   - Select `ai_project` repository
4. Fill configuration:
   ```
   Name: ai-project
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   Region: ⚠️ SAME AS DATABASE
   Instance Type: Free (Starter)
   Auto-Deploy: Yes
   ```
5. Scroll down and continue

### Step 3️⃣ Add Environment Variables

Before clicking **Create Web Service**, scroll to **Environment** section:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | (Paste from Step 1) |
| `GEMINI_API_KEY` | Your Gemini API key |
| `OPENAI_API_KEY` | Your OpenAI key (optional) |
| `GROQ_API_KEY` | Your Groq key (optional) |
| `SECRET_KEY` | `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `False` |

**How to add each variable:**
```
1. Click "+ Add Environment Variable"
2. Enter Key name
3. Enter Value
4. Repeat for each variable
```

### Step 4️⃣ Deploy

1. Click **Create Web Service** button
2. Render starts building (shows progress)
3. Watch the **Logs** tab:
   ```
   ✅ "Build succeeded"
   ✅ "Deploying..."
   ✅ "Your service is live"
   ```
4. Wait for logs to show "Your service is live"

### Step 5️⃣ Access Your Application

1. Click the service name to open dashboard
2. Find your **Service URL** (top right)
3. Format: `https://ai-project-xyz123.onrender.com`
4. **Open in browser**:
   ```
   https://your-service-name.onrender.com/docs
   ```

## Verification Checklist

After deployment, verify everything works:

```
✅ Service shows "Live" (green status)
✅ Can access /docs endpoint
✅ No errors in Logs tab
✅ Can see database connected
✅ API responds to requests
```

## Getting Your API Keys

### 1. Gemini API Key
```
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Paste in Render environment variables
```

### 2. OpenAI API Key
```
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key immediately (won't show again)
4. Paste in Render environment variables
```

### 3. Groq API Key
```
1. Go to https://console.groq.com
2. Create account / login
3. Navigate to API keys
4. Create new key
5. Copy and paste in Render environment variables
```

### 4. Generate SECRET_KEY
```bash
# Run this locally or in terminal:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy the output and paste in Render
```

## AUTO-DEPLOY: Updates Go Live Automatically!

Once deployed, any push to `main` automatically redeploys:

```bash
# Make changes locally
git add .
git commit -m "Fix feature"
git push origin main

# Automatically deploys in 1-2 minutes!
# No manual redeploy needed
```

## Free Tier Details

### Included in Free Tier
```
✅ Web Service
  - 0.5 GB RAM
  - Shared CPU
  - Sleeps after 15 min inactivity
  - Auto-wakes on request
  
✅ PostgreSQL Database
  - 256 MB storage
  - Automatic daily backups
  - 7-day retention
  
✅ Both with
  - Free SSL certificate
  - Auto-scaling
  - Custom domain support
```

### Limitations
```
⚠️ Service sleeps after 15 min (free tier)
⚠️ 256 MB database storage
⚠️ Shared resources
⚠️ Limited to 750 hours/month
```

### When to Upgrade
```
Upgrade to Paid when:
- App gets traffic (needs 24/7 uptime)
- Service often spins up (wake-up latency)
- Database exceeds 256 MB
- Need dedicated resources
```

## Troubleshooting

### Issue: Service won't deploy

**Solution:**
```
1. Check Build Command in Logs
2. Verify requirements.txt has all dependencies
3. Check Environment variables are set
4. Look for Python errors in logs
```

### Issue: Database connection error

**Solution:**
```
1. Verify DATABASE_URL format
2. Copy directly from Render PostgreSQL page
3. Format should be:
   postgresql://user:password@hostname:port/database
```

### Issue: "ModuleNotFoundError"

**Solution:**
```
1. Add missing module to requirements.txt
2. Push to GitHub
3. Auto-redeploys with new dependency
```

### Issue: "GEMINI_API_KEY not found"

**Solution:**
```
1. Go to Web Service → Settings
2. Verify GEMINI_API_KEY is in Environment
3. Make sure value is not empty
4. Manual redeploy if needed
```

## Monitoring Your App

### View Live Logs
```
1. Open Render Dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time output
```

### Common Messages
```
✅ "Application startup complete" = All good!
❌ "No module named X" = Missing dependency
❌ "Connection refused" = Database issue
❌ "502 Bad Gateway" = Service crashed
```

## Useful Links

| Resource | URL |
|----------|-----|
| Render Dashboard | https://dashboard.render.com |
| Render Docs | https://render.com/docs |
| Status Page | https://status.render.com |
| Render Pricing | https://render.com/pricing |
| Support | support@render.com |

## Custom Domain (Optional)

To use your own domain:

1. **In Render Service Settings**
   - Click "Custom Domain"
   - Enter your domain (e.g., `api.mysite.com`)
   - Click "Add"

2. **Add DNS Records**
   - Render shows CNAME record
   - Add to your domain provider
   - Wait 24 hours for propagation

## Database Backups

Render automatically backs up daily:

```
Access Backups:
1. Open PostgreSQL service
2. Click "Backups"
3. See all backups with timestamps
4. Click to restore if needed
```

## Performance Tips

For production use:

1. **Increase Web Service**
   - Upgrade from Free to Standard
   - Get dedicated resources
   - No more sleep cycles

2. **Upgrade Database**
   - Get more storage
   - Better performance
   - More connections

3. **Add Caching**
   - Reduce database queries
   - Faster response times

4. **Optimize Queries**
   - Add indexes to frequently searched columns
   - Use database query optimization

## Next Steps

1. ✅ Follow setup steps above
2. ✅ Deploy your app
3. ✅ Test at `/docs` endpoint
4. ✅ Monitor logs
5. ✅ Configure custom domain (optional)
6. ✅ Set up backups reminder
7. ✅ Upgrade to paid plan when needed

## Success! 🎉

Your app is now live on Render at:

```
https://your-service-name.onrender.com
Documentation: https://your-service-name.onrender.com/docs
```

### What You Can Do Now

- 📚 View API documentation at `/docs`
- 🔑 Use your API from anywhere
- 💬 Test WebSocket connections
- 🎤 Upload audio files
- 🤖 Chat with AI assistants
- 📊 Get interview analysis

### Share Your App

```
Live URL: https://your-service-name.onrender.com
API Docs: https://your-service-name.onrender.com/docs
Repository: https://github.com/shreetigoyal2109/ai_project
```

---

**Questions?** Check [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed information.

**Need help?** Visit https://render.com/docs or email support@render.com
