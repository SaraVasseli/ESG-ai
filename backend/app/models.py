from typing import List, Literal, Optional
from pydantic import BaseModel

Framework = Literal["CSRD", "SASB", "GRI", "CDP"]
Tone = Literal["regulatory", "investor_friendly"]


class Metric(BaseModel):
    name: str
    value: str
    unit: Optional[str] = None


class GenerateDisclosureRequest(BaseModel):
    company_name: str
    sector: str
    year: int
    frameworks: List[Framework]
    metrics: List[Metric]
    initiatives: str
    tone: Tone = "regulatory"


class GenerateDisclosureResponse(BaseModel):
    disclosure_text: str
    improvement_suggestions: List[str]
    model: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class HistoryItem(BaseModel):
    id: int
    company_name: str
    year: int
    frameworks: List[Framework]
    created_at: str
    disclosure_preview: str
