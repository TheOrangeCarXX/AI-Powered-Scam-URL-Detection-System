from pydantic import BaseModel
from typing import Literal, Optional

class AnalyzeRequest(BaseModel):
    type: Literal["url", "html"]
    data: str
    html: Optional[str] = None

class AnalyzeResponse(BaseModel):
    verdict: str
    final_score: int
    ai_explanation: str

