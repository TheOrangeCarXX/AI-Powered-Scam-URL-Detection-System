from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    type: str   # "url" or "html"
    data: str