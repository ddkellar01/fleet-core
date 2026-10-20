"""Launch the fleet: register agents, print status, run sample missions.

Usage: python scripts/run_fleet.py [mission-count]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.coordinator import Coordinator
from src.core.heartbeat import HeartbeatMonitor
from src.core.node_registry import NodeRegistry

TOPICS = ["releases", "ci-health", "security-advisories"]


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    coord = Coordinator(kb_path=":memory:")
    reg = NodeRegistry()
    for agent in coord.agents:
        reg.register(agent.name, agent.role)
    mon = HeartbeatMonitor(reg, stale_after_s=1e9, down_after_s=1e10)

    print("Fleet status:")
    for h in reg.list_nodes():
        print(f"  {h['name']:14s} {h['role']:9s} {h['status']}")
    print(f"Heartbeat healthy: {mon.healthy()}")

    for i in range(count):
        topic = TOPICS[i % len(TOPICS)]
        report = coord.run_mission(topic)
        print(f"\nMission {i + 1} [{topic}]: {report['status']}")
        for stage, result in report["stages"].items():
            key = {  # one-line summary per stage
                "scout": f"found {result.get('found')}",
                "verify": f"verdict {result.get('verdict')}",
                "learn": f"lesson #{result.get('lesson_id')}",
                "test": f"passed={result.get('passed')}",
                "deploy": f"deployed={result.get('deployed')}",
            }.get(stage, "")
            print(f"  {stage:7s} {key}")


if __name__ == "__main__":
    main()