# Render Deployment - Quick Setup Checklist

## 📋 Before You Start

- [ ] GitHub account with repository pushed
- [ ] Render account (free at https://render.com)
- [ ] Gemini API key (get from https://makersuite.google.com/app/apikey)
- [ ] OpenAI API key (optional - get from https://platform.openai.com/api-keys)
- [ ] Groq API key (optional - get from https://console.groq.com)

## 🚀 Deployment Steps (5 minutes)

### Step 1: Create PostgreSQL Database
```
1. Login to https://render.com
2. Click "+ New" → "PostgreSQL"
3. Name: ai_project_db
4. Region: Choose your region
5. Click "Create Database"
6. Copy the External Database URL (you'll need this)
```

### Step 2: Create Web Service
```
1. Click "+ New" → "Web Service"
2. Click "Connect" to authorize GitHub
3. Select "ai_project" repository
4. Fill in:
   - Name: ai-project
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   - Region: Same as database ⚠️
5. Click "Create Web Service"
```

### Step 3: Add Environment Variables
```
Click "Add Environment Variable" for each:

DATABASE_URL → (Paste from Step 1)
GEMINI_API_KEY → (Your Gemini key)
OPENAI_API_KEY → (Your OpenAI key, or skip if you don't have)
GROQ_API_KEY → (Your Groq key, or skip if you don't have)
SECRET_KEY → python -c "import secrets; print(secrets.token_urlsafe(32))"
ENVIRONMENT → production
DEBUG → False
```

### Step 4: Deploy
```
Click "Create Web Service"
Wait 2-3 minutes for deployment
Check logs for "Your service is live" message
```

### Step 5: Access Your App
```
Click service name to get your URL
https://your-service-name.onrender.com/docs
```

## ✅ Verification Checklist

After deployment, verify:

- [ ] Service status is "Live" (green)
- [ ] No errors in Logs tab
- [ ] Can access https://your-app.onrender.com/docs
- [ ] API responds to requests
- [ ] Database is connected (no connection errors in logs)

## 🔧 Environment Variables Reference

| Variable | Required | Example |
|----------|----------|---------|
| DATABASE_URL | Yes | `postgresql://user:pass@...` |
| GEMINI_API_KEY | Yes | `gsk_...` |
| OPENAI_API_KEY | No | `sk_...` |
| GROQ_API_KEY | No | `gsk_...` |
| SECRET_KEY | Yes | 32+ character random string |
| ENVIRONMENT | Yes | `production` |
| DEBUG | Yes | `False` |

## 🆘 Troubleshooting

### Service won't start
- Check Build/Start commands are correct
- Look at Logs tab for errors
- Verify all environment variables are set

### Database connection fails
- Verify DATABASE_URL format: `postgresql://user:pass@host:port/db`
- Check database is created and running
- Try copying URL directly from Render database page

### Module not found error
- Ensure all dependencies are in requirements.txt
- Check gunicorn is included in requirements.txt

### Application crashes on startup
- Check GEMINI_API_KEY is set (app requires it)
- Look for database initialization errors in logs
- Verify API key format is correct

## 🔄 Deploying Updates

Once deployed, any push to `main` branch automatically redeploys:

```bash
git add .
git commit -m "Update feature"
git push origin main
# Automatically deploys in 1-2 minutes
```

## 💾 Database Backups

Render automatically backs up daily:
- Settings → Database → Backups
- Can restore from any backup
- Backups kept for 7 days

## 📊 Monitoring

### View Logs
- Click service → Logs tab
- See real-time application output

### Common Status Messages
```
✅ "Application startup complete" = Running fine
❌ "ERROR: could not translate host name" = Database URL wrong
❌ "No module named..." = Missing dependency
```

## 🎯 Next Steps After Deployment

1. Test your API at `/docs` endpoint
2. Configure custom domain (optional)
3. Set up CRON jobs if needed
4. Monitor logs regularly
5. Plan for scaling if traffic grows

## 📞 Support Resources

- Render Docs: https://render.com/docs
- Render Dashboard: https://dashboard.render.com
- Status Page: https://status.render.com

## 💰 Free Tier Limits

- Web Service: 0.5GB RAM, shared CPU, sleeps after 15 min inactivity
- PostgreSQL: 256MB storage
- Free SSL certificate
- Automatic backups

**For production**: Upgrade to paid plan for 24/7 uptime

---

**You're all set! Deploy and enjoy your live AI Interview Platform on Render! 🚀**
