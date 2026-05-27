# Deployment Guide

This guide provides step-by-step instructions for deploying the AI Interview Platform.

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Troubleshooting](#troubleshooting)

## Local Development Setup

### Windows

1. **Prerequisites Check**
   - Python 3.11+ installed (verify: `python --version`)
   - Git installed
   - PostgreSQL 13+ (optional, can skip if using database URL elsewhere)

2. **Automated Setup**
   ```batch
   deploy-windows.bat
   ```

   Or **Manual Setup**:
   ```batch
   # Create virtual environment
   python -m venv venv_deploy
   
   # Activate virtual environment
   venv_deploy\Scripts\activate.bat
   
   # Upgrade pip
   python -m pip install --upgrade pip
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```batch
   # Copy template
   copy .env.example .env
   
   # Edit with your API keys
   notepad .env
   ```

4. **Run the Server**
   ```batch
   # Ensure venv is activated
   venv_deploy\Scripts\activate.bat
   
   # Start FastAPI server
   uvicorn main:app --reload
   ```

### macOS / Linux

1. **Prerequisites Check**
   - Python 3.11+ installed (verify: `python3 --version`)
   - Git installed
   - PostgreSQL 13+ (optional)

2. **Automated Setup**
   ```bash
   chmod +x deploy-unix.sh
   ./deploy-unix.sh
   ```

   Or **Manual Setup**:
   ```bash
   # Create virtual environment
   python3 -m venv venv_deploy
   
   # Activate virtual environment
   source venv_deploy/bin/activate
   
   # Upgrade pip
   python -m pip install --upgrade pip
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Copy template
   cp .env.example .env
   
   # Edit with your API keys
   nano .env
   ```

4. **Run the Server**
   ```bash
   # Ensure venv is activated
   source venv_deploy/bin/activate
   
   # Start FastAPI server
   uvicorn main:app --reload
   ```

## Access the Application

Once the server is running:

- **API Base URL**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

Services will be available at:
- **API**: http://localhost:8000
- **PostgreSQL**: localhost:5432

### Manual Docker Build

```bash
# Build image
docker build -t ai_project:latest .

# Run container
docker run -p 8000:8000 \
  --env-file .env \
  ai_project:latest
```

### Push to Docker Registry

```bash
# Tag image
docker tag ai_project:latest your_registry/ai_project:latest

# Login to registry
docker login

# Push image
docker push your_registry/ai_project:latest
```

## Production Deployment

### AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security group: Allow 80, 443, 22

2. **Install Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3.11 python3-pip git postgresql libsndfile1 ffmpeg
   ```

3. **Clone and Setup**
   ```bash
   git clone https://github.com/shreetigoyal2109/ai_project.git
   cd ai_project
   ./deploy-unix.sh
   ```

4. **Configure Environment**
   ```bash
   nano .env
   # Update database URL, API keys, SECRET_KEY
   ```

5. **Install Gunicorn**
   ```bash
   source venv_deploy/bin/activate
   pip install gunicorn
   ```

6. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/ai_project.service
   ```

   Add:
   ```ini
   [Unit]
   Description=AI Interview Platform
   After=network.target

   [Service]
   Type=notify
   User=ubuntu
   WorkingDirectory=/home/ubuntu/ai_project
   Environment="PATH=/home/ubuntu/ai_project/venv_deploy/bin"
   ExecStart=/home/ubuntu/ai_project/venv_deploy/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start ai_project
   sudo systemctl enable ai_project
   ```

### Google Cloud Run

1. **Create `.gcloudignore`**
   ```
   venv_deploy/
   .env
   __pycache__/
   ```

2. **Deploy**
   ```bash
   gcloud run deploy ai_project \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

3. **Set Environment Variables**
   ```bash
   gcloud run services update ai_project \
     --region us-central1 \
     --set-env-vars GEMINI_API_KEY=your_key,OPENAI_API_KEY=your_key
   ```

### Heroku

1. **Create `Procfile`**
   ```
   web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT main:app
   ```

2. **Deploy**
   ```bash
   heroku login
   heroku create ai-project-app
   git push heroku main
   ```

3. **Set Config Variables**
   ```bash
   heroku config:set GEMINI_API_KEY=your_key
   heroku config:set OPENAI_API_KEY=your_key
   ```

### Kubernetes

1. **Create Docker Image**
   ```bash
   docker build -t your_registry/ai_project:latest .
   docker push your_registry/ai_project:latest
   ```

2. **Create `k8s/deployment.yaml`**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: ai-project
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: ai-project
     template:
       metadata:
         labels:
           app: ai-project
       spec:
         containers:
         - name: api
           image: your_registry/ai_project:latest
           ports:
           - containerPort: 8000
           env:
           - name: DATABASE_URL
             valueFrom:
               secretKeyRef:
                 name: ai-project-secrets
                 key: database-url
   ```

3. **Deploy**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   ```

## Environment Variables

### Required
- `GEMINI_API_KEY` - Google Gemini API key
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `GROQ_API_KEY` - Groq API key (optional)
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret (min 32 characters)

### Optional
- `DEBUG` - Enable debug mode (default: False)
- `ENVIRONMENT` - Set to "production" for prod
- `ALLOWED_ORIGINS` - CORS origins (comma-separated)
- `WS_TIMEOUT` - WebSocket timeout in seconds
- `WS_HEARTBEAT` - WebSocket heartbeat interval

## Troubleshooting

### "ModuleNotFoundError" when running

**Solution**: Ensure virtual environment is activated
```bash
# Windows
venv_deploy\Scripts\activate.bat

# Linux/macOS
source venv_deploy/bin/activate
```

### Database connection error

**Solution**: Check DATABASE_URL format
```
postgresql://username:password@localhost:5432/database_name
```

### Port 8000 already in use

**Solution**: Use a different port
```bash
uvicorn main:app --reload --port 8001
```

### Audio processing fails

**Solution**: Install ffmpeg
```bash
# Windows (with Chocolatey)
choco install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### WebSocket connection refused

**Solution**: Check CORS settings in main.py and ensure frontend origin is in `allow_origins`

## Health Checks

### Verify API is Running
```bash
curl http://localhost:8000/docs
```

### Check API Health
```bash
curl http://localhost:8000/
```

## Performance Tuning

### Production Gunicorn Settings
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  --worker-class uvicorn.workers.UvicornWorker \
  --max-requests 1000 \
  --max-requests-jitter 50 \
  --timeout 60 \
  main:app
```

### Database Connection Pooling
```python
# In database.py
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=0
)
```

## Monitoring & Logging

### Enable Application Logging
```bash
uvicorn main:app --log-level debug
```

### View Docker Logs
```bash
docker-compose logs -f api
```

### Monitor System Resources
```bash
# Watch container stats
docker stats

# Monitor process
ps aux | grep uvicorn
```

## Backup & Recovery

### Database Backup (PostgreSQL)
```bash
pg_dump database_name > backup.sql
```

### Restore Database
```bash
psql database_name < backup.sql
```

---

For more help, visit: https://github.com/shreetigoyal2109/ai_project
