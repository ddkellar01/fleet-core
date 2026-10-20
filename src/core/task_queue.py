"""Persistent mission queue — SQLite-backed, FIFO.

Missions are enqueued by topic and payload, dequeued oldest-first,
and marked complete or failed with the result recorded. Survives
restarts, unlike the in-memory bus.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone


class TaskQueue:
    def __init__(self, path: str = "fleet.db"):
        self._con = sqlite3.connect(path, check_same_thread=False)
        self._con.execute(
            "CREATE TABLE IF NOT EXISTS task_queue ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT,"
            " payload TEXT, status TEXT DEFAULT 'pending',"
            " result TEXT, created_at TEXT)")
        self._con.commit()

    def enqueue(self, topic: str, payload: dict) -> int:
        cur = self._con.execute(
            "INSERT INTO task_queue (topic, payload, created_at) VALUES (?,?,?)",
            (topic, json.dumps(payload),
             datetime.now(timezone.utc).isoformat()))
        self._con.commit()
        return cur.lastrowid

    def dequeue(self) -> dict | None:
        row = self._con.execute(
            "SELECT id, topic, payload FROM task_queue "
            "WHERE status='pending' ORDER BY id ASC LIMIT 1").fetchone()
        if not row:
            return None
        self._con.execute("UPDATE task_queue SET status='running' WHERE id=?",
                          (row[0],))
        self._con.commit()
        return {"id": row[0], "topic": row[1], "payload": json.loads(row[2])}

    def complete(self, task_id: int, result: dict) -> None:
        self._con.execute(
            "UPDATE task_queue SET status='done', result=? WHERE id=?",
            (json.dumps(result), task_id))
        self._con.commit()

    def fail(self, task_id: int, error: str) -> None:
        self._con.execute(
            "UPDATE task_queue SET status='failed', result=? WHERE id=?",
            (json.dumps({"error": error}), task_id))
        self._con.commit()

    def pending_count(self) -> int:
        return self._con.execute(
            "SELECT COUNT(*) FROM task_queue WHERE status='pending'"
        ).fetchone()[0]