import json

from sqlalchemy.orm import Session

from app.database.models import AuditLog
from app.schemas.support import SupportResult


def save_audit(
    db: Session,
    input_text: str,
    result: SupportResult,
    status: str,
    error: str | None = None,
) -> AuditLog:
    record = AuditLog(
        input_text=input_text,
        output_json=json.dumps(result.model_dump(mode="json"), ensure_ascii=False),
        status=status,
        confidence=result.confidence.value,
        escalate=result.escalate,
        error=error,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
