from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.repository import save_audit
from app.schemas.support import IngestResponse, SupportRequest
from app.services.escalation import apply_escalation_rules
from app.services.llm_service import LLMService
from app.services.validation import ValidationService


router = APIRouter()
llm_service = LLMService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: SupportRequest, db: Session = Depends(get_db)):
    try:
        result = llm_service.analyze(request.text)
        result = apply_escalation_rules(result)
        audit = save_audit(db, request.text, result, status="success")

        return IngestResponse(
            **result.model_dump(),
            status="success",
            audit_id=audit.id,
        )

    except Exception as exc:
        safe_result = ValidationService.safe_result(str(exc))
        audit = save_audit(
            db,
            request.text,
            safe_result,
            status="escalated",
            error=str(exc),
        )

        return IngestResponse(
            **safe_result.model_dump(),
            status="escalated",
            audit_id=audit.id,
        )
