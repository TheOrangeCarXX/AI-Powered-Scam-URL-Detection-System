from pydantic import BaseModel
from typing import Literal

class AnalyzeRequest(BaseModel):
    type: Literal["url"]
    data: str

class AnalyzeResponse(BaseModel):
    verdict: str
    final_score: int
    ai_explanation: str

