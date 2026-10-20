"""FastAPI entrypoint for the fleet core."""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .core.coordinator import Coordinator
from .core.knowledge_base import KnowledgeBase

app = FastAPI(title="Fleet Core",
              description="Scout -> verify -> learn -> test -> deploy agent fleet.",
              version="0.1.0")

_coord = Coordinator(kb_path="fleet.db")


class MissionRequest(BaseModel):
    topic: str
    candidate: dict | None = None


@app.get("/")
def root():
    return {"status": "online", "agents": len(_coord.agents)}


@app.get("/fleet/status")
def fleet_status():
    return {"agents": _coord.fleet_status(),
            "messages": len(_coord.bus.history)}


@app.post("/missions")
def run_mission(req: MissionRequest):
    return _coord.run_mission(req.topic, candidate=req.candidate)


@app.get("/knowledge/lessons")
def lessons(pattern: str):
    return {"pattern": pattern, "lessons": _coord.kb.lessons_for(pattern)}


@app.get("/knowledge/findings")
def findings():
    return {"findings": _coord.kb.recent_findings()}