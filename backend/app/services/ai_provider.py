from __future__ import annotations
from datetime import date
from typing import List, Dict
import json
import httpx

from ..core.config import get_settings
from ..schemas.ai import AiSuggestionResponse, AiEntrySuggestion

settings = get_settings()


class BaseAiProvider:
    def suggest(self, payload: Dict) -> AiSuggestionResponse:
        raise NotImplementedError


class MockAiProvider(BaseAiProvider):
    def suggest(self, payload: Dict) -> AiSuggestionResponse:
        week_start = payload.get("week_start")
        base_date = date.fromisoformat(week_start)
        entries = []
        for idx in range(5):
            entries.append(
                AiEntrySuggestion(
                    date=base_date.fromordinal(base_date.toordinal() + idx),
                    project=payload.get("project_name", "Internal"),
                    task="Project work",
                    hours=6 + (idx % 2),
                    comment="Progressed key deliverables and collaborated with team",
                    confidence=0.8,
                    reason="Based on previous pattern and allocations",
                )
            )
        return AiSuggestionResponse(week_start=base_date, entries=entries, warnings=[], questions=[])


class AzureOpenAiProvider(BaseAiProvider):
    def suggest(self, payload: Dict) -> AiSuggestionResponse:
        prompt = payload.get("prompt")
        if not settings.azure_openai_endpoint or not settings.azure_openai_api_key:
            raise ValueError("Azure OpenAI not configured")
        headers = {
            "Content-Type": "application/json",
            "api-key": settings.azure_openai_api_key,
        }
        body = {
            "messages": [
                {"role": "system", "content": payload.get("system_prompt", "You are a timesheet assistant.")},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        url = f"{settings.azure_openai_endpoint}/openai/deployments/{settings.azure_openai_deployment}/chat/completions?api-version=2023-05-15"
        response = httpx.post(url, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        data = json.loads(content)
        return AiSuggestionResponse(**data)


def get_ai_provider() -> BaseAiProvider:
    if settings.ai_provider == "azure":
        return AzureOpenAiProvider()
    return MockAiProvider()
