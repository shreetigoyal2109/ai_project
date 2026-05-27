# Deploying to Render

Render is a modern cloud platform that makes it easy to deploy applications. This guide walks you through deploying the AI Interview Platform to Render.

## Prerequisites

- Render account (free at https://render.com)
- GitHub account with the repository pushed
- API keys (Gemini, OpenAI, Groq)
- PostgreSQL database (we'll set this up on Render)

## Step 1: Prepare Your Repository

Your repository is already prepared! Ensure these files exist:

✅ `requirements.txt` - Python dependencies  
✅ `Procfile` - (Will create)  
✅ `.env.example` - Environment template  
✅ `main.py` - FastAPI application  

### Create Procfile

Add this file to your repository root:

```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

Push to GitHub:

```bash
git add Procfile
git commit -m "Add Procfile for Render deployment"
git push origin main
```

## Step 2: Set Up PostgreSQL Database on Render

1. **Login to Render Dashboard**
   - Go to https://render.com
   - Sign in with GitHub

2. **Create PostgreSQL Database**
   - Click **+ New** button
   - Select **PostgreSQL**
   - Fill in details:
     - **Name**: `ai_project_db`
     - **Database**: `ai_project`
     - **User**: (auto-generated)
     - **Region**: Select closest to you
     - **PostgreSQL Version**: 15
   - Click **Create Database**

3. **Note Database Credentials**
   - Copy the **External Database URL** (looks like: `postgresql://user:password@host:port/database`)
   - You'll need this for the web service

## Step 3: Create Web Service on Render

1. **Create New Service**
   - Click **+ New**
   - Select **Web Service**

2. **Connect GitHub Repository**
   - Select **GitHub**
   - Search for and select `ai_project` repository
   - Click **Connect**

3. **Configure Service**
   - **Name**: `ai-project` (or your preference)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
   - **Region**: Same as database (important!)
   - **Instance Type**: Starter (free tier) or higher
   - Leave other settings as default

## Step 4: Add Environment Variables

1. **In Render Dashboard**
   - Scroll down to **Environment** section
   - Click **Add Environment Variable** for each:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (Paste PostgreSQL URL from Step 2) |
| `GEMINI_API_KEY` | Your Gemini API key |
| `OPENAI_API_KEY` | Your OpenAI API key (optional) |
| `GROQ_API_KEY` | Your Groq API key (optional) |
| `SECRET_KEY` | Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `False` |

2. **Example DATABASE_URL format**:
   ```
   postgresql://user:password@hostname:port/database
   ```

## Step 5: Deploy

1. **Click "Create Web Service"** button
   - Render will start building and deploying
   - Watch logs in the **Logs** tab

2. **Wait for Deployment**
   - Initial build takes 2-3 minutes
   - You'll see "Your service is live" when ready

3. **Access Your Application**
   - Click the service name to get your URL
   - Format: `https://ai-project.onrender.com`
   - Access docs at: `https://ai-project.onrender.com/docs`

## Step 6: Set Up Custom Domain (Optional)

1. **Add Custom Domain**
   - In service settings, click **Settings**
   - Scroll to **Custom Domain**
   - Enter your domain (e.g., `api.yourdomain.com`)
   - Click **Add Custom Domain**

2. **Configure DNS**
   - Render provides DNS records
   - Add them to your domain provider:
     - Add CNAME record pointing to Render's URL
     - Wait for DNS to propagate (can take 24 hours)

## Deployment Details

### How Render Deploys

1. **GitHub Integration** - Renders watches your repository
2. **Auto-Build** - On every push to main, Render automatically:
   - Pulls latest code
   - Installs dependencies
   - Builds Docker image
   - Deploys new version
3. **Zero Downtime** - Old version stays live until new one is ready

### Database Connection

- Render PostgreSQL URL is automatically configured
- Your `DATABASE_URL` environment variable connects to it
- SQLAlchemy ORM will automatically create tables on startup

## Monitoring & Logs

### View Logs
1. Click your service
2. Click **Logs** tab
3. See real-time application logs

### Common Log Indicators

```
✅ "Application startup complete" - App is running
❌ "No module named 'fastapi'" - Dependency issue
❌ "Connection refused" - Database connection issue
```

### Troubleshooting

**Application won't start**
```
Check logs for errors. Common causes:
- Missing environment variables
- Database URL incorrect
- Dependencies not installed
```

**Database connection fails**
```
Verify DATABASE_URL in environment variables
Format: postgresql://user:pass@host:port/db
```

**Static files not loading**
```
Ensure paths are absolute or relative to app directory
```

## Costs

### Render Pricing

- **Web Service (Free Tier)**
  - 0.5 GB RAM
  - Shared CPU
  - Sleeps after 15 min inactivity
  - Free SSL
  - Free custom domain

- **PostgreSQL (Free Tier)**
  - 256 MB storage
  - Included backup

- **Paid Plans**
  - Web: $7-57/month (no sleeping)
  - PostgreSQL: $15-100/month (more storage)

## Advanced Configuration

### Auto-Deploy on Every Push

Already enabled! Just push to main:

```bash
git commit -m "Update feature"
git push origin main
# Render automatically deploys
```

### Manual Redeploy

1. Click service
2. Click **Manual Deploy** button
3. Select branch (usually `main`)
4. Click **Deploy**

### Environment-Specific Builds

Create different services for different branches:
- `main` → Production
- `develop` → Staging
- `feature/*` → Review

## Scaling

### If Performance Degrades

1. **Increase Instance Size**
   - Service Settings → Instance Type
   - Upgrade from Starter to Standard or higher

2. **Add Worker Processes**
   - Modify Start Command:
   ```
   gunicorn -w 8 -k uvicorn.workers.UvicornWorker main:app
   ```

3. **Database Optimization**
   - Add indexes to frequently queried columns
   - Upgrade PostgreSQL instance

## Backup & Recovery

### Database Backups
- Render automatically backs up daily
- Backups retained for 7 days
- Access in database settings

### Restore from Backup
1. Click database service
2. Click **Settings**
3. Scroll to **Backup/Restore**
4. Select backup date
5. Click **Restore**

## Security Best Practices

1. **Never commit secrets**
   - Use environment variables only
   - Keep `.env` in `.gitignore`

2. **Use strong SECRET_KEY**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Enable HTTPS** (automatic on Render)

4. **Rotate API keys periodically**

5. **Use private GitHub repository**

## Useful Commands

### Test Locally Before Deploying

```bash
# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Check Deployment Status

```bash
# Via Render Dashboard Logs tab
# Or curl the API
curl https://your-app.onrender.com/docs
```

### Debug Database Connection

```python
# Add to main.py temporarily
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Database connected:", result.fetchone())
```

## Post-Deployment Checklist

- ✅ Service deployed and running
- ✅ Database connected and tables created
- ✅ API docs accessible at `/docs`
- ✅ Environment variables set correctly
- ✅ Logs show no errors
- ✅ CORS settings allow your frontend domain
- ✅ Custom domain configured (if needed)
- ✅ SSL certificate active (automatic)
- ✅ Backups enabled for database
- ✅ Monitoring alerts configured (optional)

## Example Deployment Flow

```
1. Create Procfile
   ↓
2. Push to GitHub
   ↓
3. Create PostgreSQL on Render
   ↓
4. Create Web Service
   ↓
5. Add environment variables
   ↓
6. Deploy
   ↓
7. Monitor logs
   ↓
8. Access at https://your-app.onrender.com
```

## Useful Resources

- **Render Docs**: https://render.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **Gunicorn Config**: https://docs.gunicorn.org/en/stable/
- **PostgreSQL Render**: https://render.com/docs/databases

## Support

If you encounter issues:

1. **Check Render Logs**
   - Service → Logs tab
   - Look for error messages

2. **Verify Environment Variables**
   - Settings → Environment
   - Check all required vars are set

3. **Test Database Connection**
   - Check DATABASE_URL format
   - Ensure PostgreSQL service is running

4. **Render Community**
   - https://render.com/community

## Summary

**Your app will be live at**: `https://your-service-name.onrender.com`

**API documentation at**: `https://your-service-name.onrender.com/docs`

**Free tier suitable for**: Development, testing, low-traffic apps

**Upgrade when**: App gets popular, needs 24/7 uptime, or requires more resources

---

**Need help?** Check Render dashboard → Support or visit https://render.com/docs
