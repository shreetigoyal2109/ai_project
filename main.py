from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.auth.refresh import router as refresh_router
from app.websocket.gemini_routes import router as websocket_router
from app.websocket.chat_routes import router as chat_websocket_router
from app.interview.routes import router as interview_router
from app.interview.practice_routes import router as interview_practice_router

app = FastAPI(title="Auth API", description="Simple authentication API with login and signup")

# Import necessary modules for startup event
import os
from dotenv import load_dotenv
from app.services.gemini_live_service import init_gemini_service
from app.services.openai_report_service import OpenAIReportService

# Load environment variables
load_dotenv()

# Global OpenAI report service instance
openai_report_service = None

@app.on_event("startup")
async def startup_event():
    """
    Initializes services when the application starts.
    """
    global openai_report_service
    
    # Initialize Gemini Live Service
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")
    init_gemini_service(gemini_api_key)
    print("Gemini Live service initialized successfully.")
    
    # Initialize OpenAI Report Service
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Warning: OPENAI_API_KEY not found in environment variables. OpenAI report generation will not be available.")
        openai_report_service = None
    else:
        openai_report_service = OpenAIReportService(api_key=openai_api_key)
        print("OpenAI Report service initialized successfully.")


# Create database tables
Base.metadata.create_all(bind=engine)

# Include only routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(refresh_router, prefix="/auth", tags=["Authentication"])
app.include_router(websocket_router, prefix="/ws", tags=["Gemini Live"])
app.include_router(chat_websocket_router, prefix="/ws", tags=["Text Chat"])
app.include_router(interview_router, prefix="/interview", tags=["Interview Analysis"])
app.include_router(interview_practice_router, prefix="/interview-practice", tags=["Interview Practice"])

from fastapi.middleware.cors import CORSMiddleware

# Add static file serving
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def serve_test_page():
    return FileResponse("test_text_chat.html")

@app.get("/test_websocket.html")
async def serve_test_page_alt():
    return FileResponse("test_text_chat.html")

@app.get("/test_interview_websocket")
async def serve_interview_test():
    return FileResponse("static/test_interview_websocket.html")

@app.get("/test_text_chat.html")
async def serve_text_chat_test():
    return FileResponse("test_text_chat.html")

@app.get("/test_gemini_websocket.html")
async def serve_gemini_test():
    return FileResponse("test_gemini_websocket.html")

@app.get("/test_websocket_simple.html")
async def serve_simple_test():
    return FileResponse("test_websocket_simple.html")

@app.get("/test_gemini_auth.html")
async def serve_gemini_auth_test():
    return FileResponse("test_gemini_auth.html")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)