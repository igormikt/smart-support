from app.services.validation import ValidationService


def test_safe_result_escalates():
    result = ValidationService.safe_result("test")
    assert result.escalate is True
    assert result.confidence == "low"
