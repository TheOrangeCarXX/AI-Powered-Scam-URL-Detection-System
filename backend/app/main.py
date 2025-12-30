from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router

# FastAPI app instance
app = FastAPI(
    title="AI Scam Detector",
    description="Detects scam websites using rules + Gemini AI",
    version="1.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow chrome-extension & localhost
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, OPTIONS
    allow_headers=["*"],          # Content-Type, etc.
)

# Routes
app.include_router(analyze_router, prefix="/analyze")

# Health Check Endpoint
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Scam Detector backend running"
    }
