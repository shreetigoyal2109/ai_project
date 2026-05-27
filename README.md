# AI Interview Platform

A FastAPI-based AI-powered interview preparation and analysis platform with real-time WebSocket communication, audio analysis, and LLM integration.

## 🚀 Deploy to Render in 5 Minutes

**New to deployment? Start here:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

**Quick links:**
- 📖 [Render Setup Guide](RENDER_GUIDE.md) - Step-by-step with screenshots
- ✅ [Render Checklist](RENDER_SETUP_CHECKLIST.md) - Quick reference
- 📚 [Render Deployment](RENDER_DEPLOYMENT.md) - Detailed documentation

## Features

- 🔐 **JWT Authentication**: Secure login and signup with token refresh
- 🎤 **Audio Analysis**: Comprehensive speech analysis including:
  - Pitch and tone analysis
  - Filler word detection
  - Speech quality metrics
  - Spectral features analysis
- 💬 **Real-time Chat**: WebSocket-based chat with multiple LLM backends:
  - Google Gemini Live
  - OpenAI GPT
  - Groq
- 🎯 **Interview Practice**: Practice mode with feedback and recommendations
- 📊 **Detailed Reports**: AI-generated performance reports

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Real-time**: WebSockets
- **Audio Processing**: librosa, SpeechRecognition, pydub
- **LLM Integration**: Gemini, OpenAI, Groq
- **Authentication**: JWT with bcrypt
- **Containerization**: Docker, Docker Compose
- **Deployment**: Render, AWS, Google Cloud, Heroku, Kubernetes

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+ (optional - use Render's free PostgreSQL)
- API Keys: Gemini (required), OpenAI/Groq (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/shreetigoyal2109/ai_project.git
   cd ai_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

   API: http://localhost:8000  
   Docs: http://localhost:8000/docs

### Docker Deployment

1. **Using Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Manual Docker build**
   ```bash
   docker build -t ai_project .
   docker run -p 8000:8000 --env-file .env ai_project
   ```

## 🌐 Deployment Guides

| Platform | Setup Time | Guide | Free Tier |
|----------|-----------|-------|-----------|
| **Render** | 5 min | [RENDER_GUIDE.md](RENDER_GUIDE.md) | ✅ Yes |
| Docker Compose | 5 min | [DEPLOYMENT.md](DEPLOYMENT.md#docker-deployment) | ✅ Local |
| AWS EC2 | 15 min | [DEPLOYMENT.md](DEPLOYMENT.md#aws-ec2) | ❌ Paid |
| Google Cloud Run | 10 min | [DEPLOYMENT.md](DEPLOYMENT.md#google-cloud-run) | ✅ Free tier |
| Heroku | 10 min | [DEPLOYMENT.md](DEPLOYMENT.md#heroku) | ⚠️ Paid |
| Kubernetes | 20 min | [DEPLOYMENT.md](DEPLOYMENT.md#kubernetes) | ✅ Local |

**👉 [See all deployment options](DEPLOYMENT.md)**

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new account
- `POST /auth/login` - Login with credentials
- `POST /auth/refresh` - Refresh JWT token

### Interview Analysis
- `POST /interview/upload` - Upload audio for analysis
- `GET /interview/{interview_id}` - Get analysis results
- `POST /interview-practice/start` - Start practice session

### WebSocket
- `WS /ws/chat` - Real-time text chat
- `WS /ws/gemini` - Gemini Live integration
- `WS /ws/interview` - Interview practice session

## Environment Variables

See `.env.example` for complete setup:

```
# Required
GEMINI_API_KEY=your_gemini_key_here
SECRET_KEY=generate_with_python_secrets

# Optional
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
DATABASE_URL=postgresql://user:password@localhost/db

# Configuration
ENVIRONMENT=production
DEBUG=False
```

## Project Structure

```
ai_project/
├── main.py                      # FastAPI entry point
├── interview_analyzer.py        # Audio analysis
├── requirements.txt             # Dependencies
├── Procfile                     # Render/Heroku config
├── Dockerfile                   # Container image
├── docker-compose.yml           # Dev stack
├── .env.example                 # Env template
├── .gitignore                   # Git rules
├── deploy-windows.bat           # Windows setup
├── deploy-unix.sh               # Unix setup
├── README.md                    # This file
├── RENDER_GUIDE.md              # Render deployment
├── RENDER_SETUP_CHECKLIST.md    # Render checklist
├── DEPLOYMENT.md                # All platforms
├── STATUS.md                    # Project status
├── QUICK_REFERENCE.md           # Quick reference
├── .github/workflows/ci-cd.yml  # GitHub Actions
└── app/                         # Application code
    ├── auth/                    # Auth routes
    ├── interview/               # Interview endpoints
    ├── websocket/               # WebSocket
    ├── services/                # Services
    └── database.py              # DB config
```

## Deployment Comparison

| Feature | Local | Docker | Render | AWS | GCP |
|---------|-------|--------|--------|-----|-----|
| Setup Time | 5 min | 10 min | 5 min | 20 min | 15 min |
| Free Tier | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| 24/7 Uptime | ❌ | ✅ | ⚠️ | ✅ | ✅ |
| Auto-Deploy | ❌ | ❌ | ✅ | ⚠️ | ✅ |
| Database | ⚠️ | ⚠️ | ✅ | ✅ | ✅ |

**⚠️ = Free tier has limitations**

## CI/CD Pipeline

GitHub Actions automatically:
- Runs linting and tests
- Builds Docker images
- Generates coverage reports
- Deploys on push to main

See `.github/workflows/ci-cd.yml`

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Linting
```bash
flake8 .
black . --check
```

### Type Checking
```bash
mypy .
```

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Troubleshooting

### Audio Processing Issues
```bash
# Install ffmpeg
apt-get install ffmpeg      # Linux
brew install ffmpeg         # macOS
choco install ffmpeg        # Windows
```

### Database Connection Error
```
Check DATABASE_URL format:
postgresql://user:password@host:port/database
```

### WebSocket Connection Issues
```
1. Check CORS settings in main.py
2. Verify frontend origin is allowed
3. Check network connectivity
```

### Render Deployment Issues
See [RENDER_GUIDE.md](RENDER_GUIDE.md#troubleshooting)

## Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | This file - Overview |
| [RENDER_GUIDE.md](RENDER_GUIDE.md) | Render deployment guide |
| [RENDER_SETUP_CHECKLIST.md](RENDER_SETUP_CHECKLIST.md) | Quick Render checklist |
| [DEPLOYMENT.md](DEPLOYMENT.md) | All deployment platforms |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick commands |
| [STATUS.md](STATUS.md) | Project status & features |

## License

MIT License - see LICENSE file for details

## Support

- 📖 Documentation: See files above
- 🐛 Issues: https://github.com/shreetigoyal2109/ai_project/issues
- 👤 Contact: [@shreetigoyal2109](https://github.com/shreetigoyal2109)

---

**Ready to deploy?** Start with [RENDER_GUIDE.md](RENDER_GUIDE.md) 🚀

**Repository**: [shreetigoyal2109/ai_project](https://github.com/shreetigoyal2109/ai_project)  
**Last Updated**: 2026-05-27
