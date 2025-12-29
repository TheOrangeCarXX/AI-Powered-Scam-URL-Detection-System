from fastapi import FastAPI
from app.api.analyze import router as analyze_router

app = FastAPI(
    title="AI Scam Detector",
    version="1.0"
)

app.include_router(analyze_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Backend running"}
