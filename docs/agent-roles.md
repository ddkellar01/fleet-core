# Agent roles

| Role | Job | Output |
|---|---|---|
| **Scout** | Watches sources for signals: failing CI, advisories, stale repos | Findings saved to the knowledge base |
| **Verifier** | Challenges each candidate on evidence: tests, README, license, CI | Verdict — pass / challenge / reject — plus the hard questions |
| **Learner** | Distills every verdict into a plain-language lesson keyed by pattern | Lessons the next mission reads first |
| **Tester** | Proves a passed candidate in a sandbox, naming failing tests | Pass/fail report |
| **Deployer** | Ships tested candidates; refuses anything untested | Deploy record with a rollback point |

## Verdict rules (verifier)
Score = share of 4 checks present:
- **pass** — score ≥ 0.75 → routes to the tester
- **challenge** — 0.50–0.74 → learner records what to fix; line stops
- **reject** — < 0.50 → deprioritized for future scouting

## Failure behavior
- Agent errors are caught per-task, recorded as outcomes, and the agent
  returns to idle.
- The circuit breaker opens after 3 consecutive failures in a role —
  calls fail fast until the cooldown passes.
- Nodes silent >30s are marked stale, >120s down; the load balancer
  never routes to them.