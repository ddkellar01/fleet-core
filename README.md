# Fleet Core

Shared multi-agent fleet core: scout agents discover work, verifiers challenge it, learners fold in past lessons, testers prove it in sandboxes, and deployers ship it — one coordinator, message bus, and knowledge base consumed by the Autonomous Tech Infrastructure Platform and the IvyTech swarm.

## Pipeline

```
scout discovers -> verifier challenges -> learner records the lesson
-> tester proves it -> deployer ships it (with a rollback point)
```

A candidate advances only on a verifier **pass** and a tester **pass**.
Everything runs in simulation mode by default — no external services
needed to run the fleet end to end.

## Quickstart

```bash
pip install -r requirements.txt
python scripts/smoke_test.py              # component checks
python scripts/run_fleet.py 3             # fleet status + 3 missions
python scripts/benchmark_missions.py 50   # throughput check
uvicorn src.main:app --host 0.0.0.0 --port 8000
pytest tests/                             # full suite
```

## Structure

```
├── config/          settings template (.env)
├── docs/            architecture · agent-roles
├── scripts/         smoke test · fleet launcher · benchmark
├── src/
│   ├── main.py      FastAPI: /missions, /fleet/status, /knowledge/*
│   ├── agents/      scout · verifier · learner · tester · deployer
│   ├── core/        coordinator · bus · registry · heartbeat ·
│   │                task queue · knowledge base · circuit breaker ·
│   │                load balancer
│   ├── ai/          Gemini Pro Thinking (mission planning, 2nd opinions)
│   ├── network/     WireGuard tunnel manager
│   └── plugins/     ATIP + IvyTech adapters
└── tests/           agents · coordinator · pipeline suites
```

## Design notes

- **One core, many platforms.** ATIP and IvyTech keep their own repos;
  both consume this fleet instead of duplicating swarm plumbing.
- **Learning is a role, not a log file.** The learner turns every
  outcome into a lesson the next mission reads first — the pipeline
  gets smarter instead of just longer.
- **Secure by default.** Control traffic rides WireGuard; API keys come
  from the environment and are never committed.