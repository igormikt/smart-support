from app.schemas.support import SupportResult


class ValidationService:
    @staticmethod
    def safe_result(reason: str) -> SupportResult:
        return SupportResult(
            category="unknown",
            summary="Запрос не прошел автоматическую обработку.",
            priority="medium",
            next_action=f"Передать обращение сотруднику поддержки. Причина: {reason}",
            fields={},
            confidence="low",
            escalate=True,
        )
