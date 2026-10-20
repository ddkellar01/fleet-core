"""Adapter: Autonomous-Tech-Infrastructure-Platform (ATIP).

Translates fleet missions into ATIP's native pipeline stages —
scout_bot discovery, Docker sandbox testing, security auditor scan —
and translates ATIP results back into fleet findings and outcomes, so
the fleet coordinator can drive ATIP without ATIP knowing the fleet
exists. Simulated stage calls by default.
"""
from __future__ import annotations


class ATIPAdapter:
    name = "atip"
    STAGES = ("scout_bot", "sandbox_runner", "security_auditor", "deployer")

    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url

    def to_fleet_candidate(self, atip_repo: dict) -> dict:
        """Map an ATIP repo record to a fleet candidate."""
        return {
            "repo": atip_repo.get("full_name", "unknown"),
            "signal": atip_repo.get("signal", ""),
            "has_tests": bool(atip_repo.get("has_tests", False)),
            "has_readme": bool(atip_repo.get("has_readme", False)),
            "has_license": bool(atip_repo.get("license")),
            "ci_green": atip_repo.get("ci_status") == "success",
        }

    def run_stage(self, stage: str, candidate: dict) -> dict:
        """Run one ATIP stage against a candidate (simulated)."""
        if stage not in self.STAGES:
            return {"stage": stage, "ok": False, "detail": "Unknown ATIP stage."}
        return {"stage": stage, "ok": True,
                "repo": candidate.get("repo", "unknown"),
                "detail": f"[sim] ATIP {stage} completed."}

    def full_pipeline(self, candidate: dict) -> dict:
        results = [self.run_stage(s, candidate) for s in self.STAGES]
        return {"adapter": self.name, "repo": candidate.get("repo", "unknown"),
                "stages": results,
                "ok": all(r["ok"] for r in results)}