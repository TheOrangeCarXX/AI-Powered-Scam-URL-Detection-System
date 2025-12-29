from fastapi import FastAPI
from app.api.analyze import router as analyze_router

app=FastAPI(
    title="AI Scam Detector",
    description="Detects scam URLs and webpages using rules + AI analysis.",
    version="1.0"
)

app.include_router(analyze_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI Scam Detector backend running."}