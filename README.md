# AI Interview Platform

A FastAPI-based AI-powered interview preparation and analysis platform with real-time WebSocket communication, audio analysis, and LLM integration.

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

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Docker & Docker Compose (optional)
- API Keys: Gemini, OpenAI, Groq (at least one)

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
   # Edit .env with your API keys and database URL
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

   API will be available at: http://localhost:8000
   Docs at: http://localhost:8000/docs

### Docker Deployment

1. **Using Docker Compose (recommended)**
   ```bash
   docker-compose up -d
   ```

2. **Manual Docker build**
   ```bash
   docker build -t ai_project .
   docker run -p 8000:8000 --env-file .env ai_project
   ```

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

See `.env.example` for complete setup. Key variables:

```
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/ai_project
SECRET_KEY=your_secret_key_min_32_chars
```

## Project Structure

```
├── main.py                 # FastAPI application entry point
├── interview_analyzer.py   # Audio analysis service
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-container setup
├── .env.example           # Environment template
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # GitHub Actions pipeline
└── app/
    ├── auth/              # Authentication routes
    ├── interview/         # Interview endpoints
    ├── websocket/         # WebSocket handlers
    ├── services/          # LLM & analysis services
    └── database.py        # Database configuration
```

## CI/CD Pipeline

GitHub Actions workflow automatically:
- Runs tests on push to main/develop
- Lints code with flake8
- Builds Docker images
- Generates coverage reports

See `.github/workflows/ci-cd.yml` for details.

## Deployment Options

### 1. Docker Compose (Development)
```bash
docker-compose up -d
```

### 2. Cloud Deployment (AWS, Google Cloud, Azure)
See cloud-specific deployment guides in docs/deployment/

### 3. Kubernetes
- Update image registry in deployment manifests
- Apply: `kubectl apply -f k8s/`

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Type Checking
```bash
mypy .
```

### Code Linting
```bash
flake8 .
black . --check
```

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## Troubleshooting

### Audio Processing Issues
- Ensure ffmpeg is installed: `apt-get install ffmpeg`
- Check audio file format support

### Database Connection
- Verify PostgreSQL is running
- Check DATABASE_URL format
- Ensure database exists

### WebSocket Connection
- Check CORS settings in main.py
- Verify frontend origin is in allowed_origins

## License

MIT License - see LICENSE file for details

## Contact

For questions or support, reach out to [@shreetigoyal2109](https://github.com/shreetigoyal2109)

---

**Repository**: [shreetigoyal2109/ai_project](https://github.com/shreetigoyal2109/ai_project)  
**Last Updated**: 2026-05-27
