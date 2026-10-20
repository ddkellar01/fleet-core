"""Smoke test — every fleet component, one run, simulation mode."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ai.gemini_thinking import GeminiThinking
from src.core.coordinator import Coordinator
from src.core.heartbeat import HeartbeatMonitor
from src.core.node_registry import NodeRegistry
from src.core.task_queue import TaskQueue
from src.network.wireguard_tunnel import Peer, WireGuardTunnel
from src.plugins.atip_adapter import ATIPAdapter
from src.plugins.ivytech_adapter import IvyTechAdapter

# 1. Pipeline
c = Coordinator(kb_path=":memory:")
strong = {"repo": "example/solid", "has_tests": True, "has_readme": True,
          "has_license": True, "ci_green": True}
r = c.run_mission("releases", candidate=strong)
assert r["status"] == "complete", r
print("1. pipeline complete OK")

# 2. Registry + heartbeat
reg = NodeRegistry()
reg.register("scout-1", "scout"); reg.register("scout-2", "scout")
picked = reg.pick("scout")
assert picked and picked.name == "scout-1"
mon = HeartbeatMonitor(reg, stale_after_s=1e9, down_after_s=1e10)
assert mon.healthy()
print("2. registry + heartbeat OK")

# 3. Task queue
q = TaskQueue(":memory:")
qid = q.enqueue("releases", {"repo": "example/solid"})
task = q.dequeue()
assert task and task["id"] == qid
q.complete(task["id"], {"ok": True})
assert q.pending_count() == 0
print("3. task queue OK")

# 4. Gemini thinking fallback
t = GeminiThinking(api_key="")
plan = t.plan_mission("releases")
assert plan.source == "static" and len(plan.roles) == 5
print("4. gemini thinking fallback OK")

# 5. WireGuard config renders
wg = WireGuardTunnel(private_key="TESTKEY")
wg.add_peer(Peer("ops-phone", "PUBKEY1", "10.9.0.2/32"))
assert "[Interface]" in wg.render_config() and "PUBKEY1" in wg.render_config()
print("5. wireguard config OK")

# 6. Adapters
atip = ATIPAdapter()
pipe = atip.full_pipeline(atip.to_fleet_candidate(
    {"full_name": "example/api-gateway", "ci_status": "success", "license": "MIT"}))
assert pipe["ok"]
ivy = IvyTechAdapter()
assert ivy.submit_lesson("releases", "test lesson")["submitted"]
assert len(ivy.request_peer_review({"repo": "example/x"})["questions"]) == 2
print("6. atip + ivytech adapters OK")

print("SMOKE OK: fleet-core scripts 11-20 green.")