"""Learner agent — distills mission outcomes into reusable lessons.

After every verification (and later, every test/deploy outcome), the
learner writes a plain-language lesson to the knowledge base keyed by
pattern, so the next scout or verifier starts smarter than the last.
This is the fleet's Recursive Peer Pedagogy, minus the ceremony.
"""
from __future__ import annotations

from .base_agent import BaseAgent


class Learner(BaseAgent):
    role = "learner"

    def process(self, task: dict) -> dict:
        pattern = task.get("pattern", "general")
        outcome = task.get("outcome", {})
        verdict = outcome.get("verdict", "unknown")
        repo = outcome.get("repo", "unknown")
        if verdict == "pass":
            lesson = (f"Pattern '{pattern}': {repo} passed verification — "
                      "well-evidenced candidates route straight to the tester.")
        elif verdict == "challenge":
            missing = [q for q in outcome.get("questions", [])]
            lesson = (f"Pattern '{pattern}': {repo} was challenged. "
                      f"Resolve before testing: {'; '.join(missing) or 'evidence gaps.'}")
        else:
            lesson = (f"Pattern '{pattern}': {repo} rejected at verification — "
                      "deprioritize similar candidates in future scouting.")
        lesson_id = self.kb.save_lesson(pattern, lesson)
        return {"pattern": pattern, "lesson_id": lesson_id, "lesson": lesson}