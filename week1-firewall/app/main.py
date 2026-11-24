from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from app.schemas import IngestionRequest, IngestionResult
from app.services import analyze_message

app = FastAPI(
    title="Enterprise Structured Ingestion Firewall",
    description="Week 1 AI Engineer Workshop — Prompt Injection & Triage Firewall",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ingestion-firewall"}


@app.post("/api/analyze", response_model=IngestionResult)
def analyze_endpoint(payload: IngestionRequest):
    try:
        return analyze_message(payload.text)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Upstream analysis error: {str(exc)}") from exc