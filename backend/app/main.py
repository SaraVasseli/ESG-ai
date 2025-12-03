from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import OPENAI_API_KEY
from .models import (
    GenerateDisclosureRequest,
    GenerateDisclosureResponse,
    HistoryItem,
)
from .llm_client import generate_disclosure

app = FastAPI(title="ESG-ai Backend")

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HISTORY: List[HistoryItem] = []
NEXT_ID = 1


@app.get("/health")
def health():
    return {
        "status": "ok",
        "has_openai_key": bool(OPENAI_API_KEY),
    }


@app.post("/api/generate-disclosure", response_model=GenerateDisclosureResponse)
def api_generate_disclosure(payload: GenerateDisclosureRequest):
    """
    Main endpoint for generating an ESG disclosure.
    """
    global NEXT_ID

    try:
        disclosure_text, suggestions, usage = generate_disclosure(payload)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="LLM generation failed")

    preview = disclosure_text[:200] + ("..." if len(disclosure_text) > 200 else "")

    item = HistoryItem(
        id=NEXT_ID,
        company_name=payload.company_name,
        year=payload.year,
        frameworks=payload.frameworks,
        created_at=datetime.utcnow().isoformat() + "Z",
        disclosure_preview=preview,
    )
    HISTORY.insert(0, item)
    NEXT_ID += 1

    # 👇 include usage in the API response
    return GenerateDisclosureResponse(
        disclosure_text=disclosure_text,
        improvement_suggestions=suggestions,
        model=usage.get("model"),
        prompt_tokens=usage.get("prompt_tokens"),
        completion_tokens=usage.get("completion_tokens"),
        total_tokens=usage.get("total_tokens"),
    )


@app.get("/api/history", response_model=List[HistoryItem])
def api_history(limit: int = 10):
    return HISTORY[:limit]