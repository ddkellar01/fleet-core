# Architecture

```
 scout ─> verifier ─> learner ─> tester ─> deployer
  │          │           │         │          │
  └──────────┴─── coordinator ────┴──────────┘
              │ bus · registry · queue · kb   │
              └── Gemini Thinking · WireGuard ──┘
```

- **Coordinator** runs each mission down the five-role pipeline. A
  candidate advances only on a verifier **pass** and a tester **pass**;
  any other result stops the line and the learner records why.
- **Message bus** carries every stage result on `results.<role>` topics;
  full history is kept for audit/replay.
- **Node registry + heartbeat monitor + load balancer** track which
  agent nodes are alive and route work to the least-loaded healthy one.
- **Task queue** (SQLite) holds missions across restarts; the **knowledge
  base** (SQLite) holds findings, lessons, and outcomes.
- **Circuit breaker** isolates a role after repeated failures so one bad
  agent can't poison the fleet.
- **Gemini Pro Thinking** plans missions and second-guesses borderline
  verdicts; static fallbacks keep everything running without a key.
- **Plugins** bridge other platforms: ATIP (infra pipeline) and IvyTech
  (professor swarm) adapters map their records into fleet candidates.
- **WireGuard** keeps fleet control on a private tunnel, never the
  public internet.