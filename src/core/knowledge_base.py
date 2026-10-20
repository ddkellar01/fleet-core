"""SQLite knowledge base — the fleet's shared memory.

Stores three things every agent reads and writes: findings (what scouts
discovered), lessons (what the learner distilled from outcomes), and
outcomes (the per-stage record of every mission). One persistent
connection so ':memory:' works for tests and simulation.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone


class KnowledgeBase:
    def __init__(self, path: str = "fleet.db"):
        self.path = path
        self._con = sqlite3.connect(path, check_same_thread=False)
        self._init()

    def _init(self) -> None:
        self._con.executescript(
            "CREATE TABLE IF NOT EXISTS findings ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT,"
            " payload TEXT, created_at TEXT);"
            "CREATE TABLE IF NOT EXISTS lessons ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT, pattern TEXT,"
            " lesson TEXT, created_at TEXT);"
            "CREATE TABLE IF NOT EXISTS outcomes ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT, mission TEXT,"
            " stage TEXT, result TEXT, created_at TEXT);"
        )
        self._con.commit()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def save_finding(self, topic: str, payload: dict) -> int:
        cur = self._con.execute(
            "INSERT INTO findings (topic, payload, created_at) VALUES (?,?,?)",
            (topic, json.dumps(payload), self._now()))
        self._con.commit()
        return cur.lastrowid

    def save_lesson(self, pattern: str, lesson: str) -> int:
        cur = self._con.execute(
            "INSERT INTO lessons (pattern, lesson, created_at) VALUES (?,?,?)",
            (pattern, lesson, self._now()))
        self._con.commit()
        return cur.lastrowid

    def record_outcome(self, mission: str, stage: str, result: dict) -> None:
        self._con.execute(
            "INSERT INTO outcomes (mission, stage, result, created_at) VALUES (?,?,?,?)",
            (mission, stage, json.dumps(result), self._now()))
        self._con.commit()

    def lessons_for(self, pattern: str) -> list[str]:
        rows = self._con.execute(
            "SELECT lesson FROM lessons WHERE pattern=? ORDER BY id DESC",
            (pattern,)).fetchall()
        return [r[0] for r in rows]

    def recent_findings(self, limit: int = 20) -> list[dict]:
        rows = self._con.execute(
            "SELECT id, topic, payload FROM findings ORDER BY id DESC LIMIT ?",
            (limit,)).fetchall()
        return [{"id": r[0], "topic": r[1], "payload": json.loads(r[2])}
                for r in rows]