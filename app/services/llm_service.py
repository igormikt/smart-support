import json
from typing import Any

from openai import OpenAI

from app.config import settings
from app.schemas.support import SupportResult


SYSTEM_PROMPT = """
You are the classification and extraction component of Smart Support.

Analyze one customer support request.

Return ONLY valid JSON with exactly these fields:
{
  "category": "string",
  "summary": "string",
  "priority": "low|medium|high|urgent",
  "next_action": "string",
  "fields": {},
  "confidence": "low|medium|high",
  "escalate": true
}

Rules:
1. Never invent facts.
2. Use only information in the request.
3. If information is insufficient for safe automated handling, use confidence="low" and escalate=true.
4. If confidence is low, escalate must be true.
5. Keep summary concise.
6. fields may contain only useful facts explicitly present in the request.
7. Return JSON only, without Markdown.
""".strip()


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.proxy_api_key,
            base_url=settings.proxy_api_base_url,
        )

    def analyze(self, text: str) -> SupportResult:
        response = self.client.chat.completions.create(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )
        content = response.choices[0].message.content or "{}"
        raw: dict[str, Any] = json.loads(content)
        return SupportResult.model_validate(raw)
