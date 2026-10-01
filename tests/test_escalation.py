from app.schemas.support import SupportResult
from app.services.escalation import apply_escalation_rules


def test_low_confidence_escalates():
    result = SupportResult(
        category="unknown",
        summary="Some request",
        priority="medium",
        next_action="Handle",
        fields={},
        confidence="low",
        escalate=False,
    )
    result = apply_escalation_rules(result)
    assert result.escalate is True
