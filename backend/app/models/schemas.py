from pydantic import BaseModel
from typing import Literal, Optional

# Request Schemas
class AnalyzeRequest(BaseModel):
    type: Literal["url", "html"]
    data: str
    html: Optional[str] = None

# Response schema
class AnalyzeResponse(BaseModel):
    verdict: str
    final_score: int
    ai_explanation: str
