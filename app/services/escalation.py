from app.schemas.support import SupportResult


def apply_escalation_rules(result: SupportResult) -> SupportResult:
    if result.confidence == "low":
        result.escalate = True

    if not result.summary.strip() or not result.next_action.strip():
        result.escalate = True

    if result.escalate:
        result.next_action = "Передать обращение сотруднику поддержки для ручной проверки."

    return result
