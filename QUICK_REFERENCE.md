# AI Interview Platform - Quick Reference Card

## 🚀 Get Started in 5 Minutes

### Windows
```batch
deploy-windows.bat
notepad .env
venv_deploy\Scripts\activate.bat
uvicorn main:app --reload
```

### macOS/Linux
```bash
chmod +x deploy-unix.sh
./deploy-unix.sh
nano .env
source venv_deploy/bin/activate
uvicorn main:app --reload
```

**Then visit**: http://localhost:8000/docs

---

## 📋 Environment Variables Checklist

```
□ GEMINI_API_KEY           (Required)
□ OPENAI_API_KEY           (Optional)
□ GROQ_API_KEY             (Optional)
□ DATABASE_URL             (Optional - uses SQLite if not set)
□ SECRET_KEY               (Required - generate: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

---

## 🔗 Key URLs

| Purpose | URL |
|---------|-----|
| API Base | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| ReDoc Docs | http://localhost:8000/redoc |
| OpenAPI JSON | http://localhost:8000/openapi.json |

---

## 🐳 Docker Commands

```bash
# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Build custom image
docker build -t ai_project .
docker run -p 8000:8000 --env-file .env ai_project
```

---

## 📚 Important Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI entry point |
| `interview_analyzer.py` | Audio analysis engine |
| `requirements.txt` | Python dependencies |
| `.env` | Configuration (create from .env.example) |
| `.gitignore` | Git ignore rules |
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Local development stack |
| `README.md` | Project documentation |
| `DEPLOYMENT.md` | Deployment guide |
| `STATUS.md` | Current status |

---

## 🔧 Common Commands

```bash
# Activate virtual environment
# Windows:
venv_deploy\Scripts\activate.bat
# Unix/macOS:
source venv_deploy/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# Run server on specific port
uvicorn main:app --reload --port 8001

# Run with specific workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Run tests
pytest tests/ -v

# Generate API docs
python -m fastapi generate-docs

# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🧪 API Examples

### Using curl

```bash
# Get docs
curl http://localhost:8000/docs

# Test API health (if implemented)
curl http://localhost:8000/

# Sign up (example)
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass123"}'

# Login (example)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass123"}'
```

### Using Python

```python
import httpx

client = httpx.Client(base_url="http://localhost:8000")

# Sign up
response = client.post("/auth/signup", json={
    "email": "user@example.com",
    "password": "securepass123"
})

# Login
response = client.post("/auth/login", json={
    "email": "user@example.com",
    "password": "securepass123"
})
print(response.json())
```

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Port 8000 in use | `uvicorn main:app --port 8001` |
| venv not activating | Use full path to activate script |
| Module not found | Ensure venv is activated |
| ffmpeg missing | `choco install ffmpeg` (Win) / `brew install ffmpeg` (Mac) |
| Database error | Check DATABASE_URL format |
| API keys not working | Verify in `.env` file is created (not `.env.example`) |

---

## 📊 Project Structure

```
ai_project/
├── main.py                      # Entry point
├── interview_analyzer.py        # Audio analysis
├── requirements.txt             # Dependencies
├── Dockerfile                   # Container config
├── docker-compose.yml           # Dev stack
├── deploy-windows.bat           # Windows setup
├── deploy-unix.sh               # Unix setup
├── README.md                    # Overview
├── DEPLOYMENT.md                # Deployment guide
├── STATUS.md                    # Status
├── QUICK_REFERENCE.md           # This file
├── .env.example                 # Env template
├── .gitignore                   # Git ignore
├── .github/workflows/ci-cd.yml  # GitHub Actions
└── app/                         # Application code
    ├── auth/                    # Auth routes
    ├── interview/               # Interview endpoints
    ├── websocket/               # WebSocket handlers
    ├── services/                # Services
    └── database.py              # DB config
```

---

## 🎯 Development Workflow

1. **Clone repository**
   ```bash
   git clone https://github.com/shreetigoyal2109/ai_project.git
   cd ai_project
   ```

2. **Setup environment**
   ```bash
   # Windows
   deploy-windows.bat
   
   # Unix/macOS
   chmod +x deploy-unix.sh
   ./deploy-unix.sh
   ```

3. **Configure API keys**
   ```bash
   # Edit .env file with your credentials
   ```

4. **Start developing**
   ```bash
   source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
   uvicorn main:app --reload
   ```

5. **Access docs**
   - Open: http://localhost:8000/docs

---

## 📱 WebSocket Examples

### Python WebSocket Client

```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as websocket:
        # Send message
        await websocket.send(json.dumps({
            "message": "Hello, AI!",
            "user_id": "123"
        }))
        
        # Receive response
        response = await websocket.recv()
        print(json.loads(response))

asyncio.run(test_websocket())
```

---

## 🚢 Deployment Checklist

- [ ] Clone repository
- [ ] Run deployment script
- [ ] Configure .env file
- [ ] Add API keys (Gemini, OpenAI, etc.)
- [ ] Test API with Swagger docs
- [ ] Run tests: `pytest tests/`
- [ ] Build Docker image: `docker build -t ai_project .`
- [ ] Deploy to cloud platform
- [ ] Set up monitoring/logging
- [ ] Configure backups
- [ ] Enable HTTPS/TLS

---

## 📞 Support Resources

- **Repository**: https://github.com/shreetigoyal2109/ai_project
- **Issues**: https://github.com/shreetigoyal2109/ai_project/issues
- **Profile**: https://github.com/shreetigoyal2109
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Docker Docs**: https://docs.docker.com/

---

**Last Updated**: 2026-05-27  
**Status**: ✅ Ready for Production
