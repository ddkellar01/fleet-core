"""Benchmark — time the fleet over N missions and report throughput."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.coordinator import Coordinator

STRONG = {"repo": "example/solid", "has_tests": True, "has_readme": True,
          "has_license": True, "ci_green": True}


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    coord = Coordinator(kb_path=":memory:")
    statuses: dict[str, int] = {}
    start = time.perf_counter()
    for _ in range(n):
        status = coord.run_mission("bench", candidate=dict(STRONG))["status"]
        statuses[status] = statuses.get(status, 0) + 1
    elapsed = time.perf_counter() - start
    print(f"Missions: {n} in {elapsed:.2f}s -> {n / elapsed:.1f} missions/s")
    print(f"Statuses: {statuses}")
    print(f"Bus messages: {len(coord.bus.history)} "
          f"-> {len(coord.bus.history) / n:.1f} msgs/mission")
    assert statuses.get("complete", 0) == n, "Not all missions completed!"


if __name__ == "__main__":
    main()