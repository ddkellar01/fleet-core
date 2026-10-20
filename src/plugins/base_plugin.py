"""Plugin base — one interface every platform adapter implements.

A plugin maps foreign records into fleet candidates, exposes its native
stages, and runs a full pipeline. Plugins register themselves with
@register so the coordinator can discover them by name.
"""
from __future__ import annotations

from typing import Callable

PLUGIN_REGISTRY: dict[str, "BasePlugin"] = {}


def register(name: str) -> Callable[["BasePlugin"], "BasePlugin"]:
    def deco(cls: "BasePlugin") -> "BasePlugin":
        PLUGIN_REGISTRY[name] = cls()
        return cls
    return deco


def get_plugin(name: str) -> "BasePlugin | None":
    return PLUGIN_REGISTRY.get(name)


class BasePlugin:
    name = "base"
    STAGES: tuple[str, ...] = ()

    def to_fleet_candidate(self, record: dict) -> dict:
        raise NotImplementedError

    def run_stage(self, stage: str, candidate: dict) -> dict:
        raise NotImplementedError

    def full_pipeline(self, candidate: dict) -> dict:
        results = [self.run_stage(s, candidate) for s in self.STAGES]
        return {"adapter": self.name,
                "repo": candidate.get("repo", "unknown"),
                "stages": results,
                "ok": all(r.get("ok") for r in results)}