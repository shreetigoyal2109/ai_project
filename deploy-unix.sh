#!/bin/bash
# AI Project Deployment Setup Script for macOS/Linux

set -e

echo "========================================"
echo "AI Interview Platform - Deployment Setup"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

python3 --version

echo ""
echo "[1/6] Creating virtual environment..."
python3 -m venv venv_deploy

echo "[✓] Virtual environment created"

echo ""
echo "[2/6] Activating virtual environment..."
source venv_deploy/bin/activate

echo "[✓] Virtual environment activated"

echo ""
echo "[3/6] Upgrading pip..."
python -m pip install --upgrade pip

echo "[✓] Pip upgraded"

echo ""
echo "[4/6] Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "[✓] Dependencies installed"

echo ""
echo "[5/6] Setting up environment variables..."
if [ ! -f .env ]; then
    echo "[INFO] Creating .env from .env.example..."
    cp .env.example .env
    echo "[⚠] Created .env - Please edit it with your API keys before running"
    echo "     - GEMINI_API_KEY"
    echo "     - OPENAI_API_KEY"
    echo "     - GROQ_API_KEY"
    echo "     - DATABASE_URL"
    echo "     - SECRET_KEY"
else
    echo "[✓] .env file already exists"
fi

echo ""
echo "[6/6] Deployment setup complete!"

echo ""
echo "========================================"
echo "NEXT STEPS:"
echo "========================================"
echo ""
echo "1. Edit .env file with your configuration:"
echo "   nano .env"
echo ""
echo "2. Start the server:"
echo "   source venv_deploy/bin/activate"
echo "   uvicorn main:app --reload"
echo ""
echo "3. Access the application:"
echo "   - API: http://localhost:8000"
echo "   - Documentation: http://localhost:8000/docs"
echo ""
echo "========================================"
