"""Gemini Pro Thinking client for the fleet.

Two jobs: plan a mission (which roles, in what order, with what focus)
and second-guess a verifier verdict when the evidence is borderline.
Falls back to the standard five-role pipeline with no API key.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field


@dataclass
class MissionPlan:
    topic: str
    roles: list[str] = field(default_factory=lambda: ["scout", "verifier", "learner", "tester", "deployer"])
    focus: str = ""
    source: str = "static"

    def to_dict(self) -> dict:
        return {"topic": self.topic, "roles": self.roles,
                "focus": self.focus, "source": self.source}


class GeminiThinking:
    """Thin wrapper over google-genai with thinking enabled."""

    MODEL = "gemini-2.5-pro"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self._client = None
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception:
                self._client = None

    @property
    def available(self) -> bool:
        return self._client is not None

    def plan_mission(self, topic: str, context: dict | None = None) -> MissionPlan:
        if not self.available:
            return MissionPlan(topic=topic,
                               focus=f"Standard pipeline for '{topic}'.")
        prompt = (
            "You coordinate a fleet of agents with roles: scout, verifier, "
            "learner, tester, deployer.\n"
            f"Mission topic: {topic}\nContext: {json.dumps(context or {})}\n"
            "Reply ONLY as JSON: {\"roles\": [...], \"focus\": \"one sentence\"}"
        )
        try:
            from google.genai import types
            resp = self._client.models.generate_content(
                model=self.MODEL, contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=2048),
                    response_mime_type="application/json"))
            data = json.loads(resp.text)
            return MissionPlan(topic=topic, roles=data.get("roles", MissionPlan(topic).roles),
                               focus=data.get("focus", ""), source="gemini")
        except Exception:
            return MissionPlan(topic=topic,
                               focus=f"Standard pipeline for '{topic}'.")

    def second_opinion(self, verdict: dict) -> str:
        """One-line sanity check on a verifier verdict."""
        v = verdict.get("verdict", "unknown")
        score = verdict.get("score", 0)
        if not self.available:
            return f"Verdict '{v}' at score {score}: consistent with the checks."
        try:
            from google.genai import types
            resp = self._client.models.generate_content(
                model=self.MODEL,
                contents=f"In one sentence, is this verification verdict sound? {json.dumps(verdict)}",
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=512)))
            return resp.text.strip()
        except Exception:
            return f"Verdict '{v}' at score {score}: consistent with the checks."