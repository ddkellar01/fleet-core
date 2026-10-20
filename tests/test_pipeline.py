"""Pytest suite for fleet-core scripts 11-20."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ai.gemini_thinking import GeminiThinking
from src.core.heartbeat import HeartbeatMonitor
from src.core.node_registry import NodeRegistry
from src.core.task_queue import TaskQueue
from src.network.wireguard_tunnel import WireGuardTunnel
from src.plugins.atip_adapter import ATIPAdapter
from src.plugins.ivytech_adapter import IvyTechAdapter


def test_registry_picks_least_loaded():
    reg = NodeRegistry()
    reg.register("scout-1", "scout")
    reg.register("scout-2", "scout")
    node = reg.pick("scout")
    assert node is not None
    node.active = 1
    assert reg.pick("scout").name == "scout-2"
    assert reg.pick("nope") is None


def test_heartbeat_marks_stale():
    reg = NodeRegistry()
    reg.register("scout-1", "scout")
    mon = HeartbeatMonitor(reg, stale_after_s=-1, down_after_s=1e9)
    counts = mon.sweep(now=time.time())
    assert counts["stale"] == 1
    reg.touch("scout-1")
    fresh = HeartbeatMonitor(reg, stale_after_s=3600, down_after_s=7200)
    counts = fresh.sweep()
    assert counts["online"] == 1


def test_task_queue_fifo_and_status():
    q = TaskQueue(":memory:")
    a = q.enqueue("t", {"n": 1})
    b = q.enqueue("t", {"n": 2})
    first = q.dequeue()
    assert first["id"] == a
    q.fail(first["id"], "boom")
    assert q.dequeue()["id"] == b
    assert q.pending_count() == 0


def test_gemini_thinking_static_fallback():
    t = GeminiThinking(api_key="")
    plan = t.plan_mission("releases")
    assert plan.source == "static"
    assert plan.roles == ["scout", "verifier", "learner", "tester", "deployer"]
    assert "consistent" in t.second_opinion({"verdict": "pass", "score": 1.0})


def test_wireguard_renders():
    cfg = WireGuardTunnel(private_key="K").render_config()
    assert "[Interface]" in cfg and "K" in cfg


def test_adapters_simulated():
    atip = ATIPAdapter()
    cand = atip.to_fleet_candidate(
        {"full_name": "a/b", "ci_status": "success", "license": "MIT",
         "has_tests": True, "has_readme": True})
    assert cand["ci_green"] and cand["repo"] == "a/b"
    assert atip.full_pipeline(cand)["ok"]
    assert ATIPAdapter().run_stage("nope", {})["ok"] is False
    ivy = IvyTechAdapter()
    assert ivy.submit_lesson("x", "lesson")["submitted"]
    assert ivy.sync_lessons(["a", "b"])["synced"] == 2