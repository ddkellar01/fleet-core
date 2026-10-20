# 🚀 Fleet: Autonomous Multi-Agent Infrastructure Framework

![CI Status](https://github.com/darnellwashingtonjr94-art/fleet/actions/workflows/fleet-ci.yml/badge.svg)
![Docker Build](https://img.shields.io/docker/v/credkellar/fleet?label=docker%20hub)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🤖 What is this about?
**Fleet** is an autonomous, self-healing multi-agent orchestration framework designed to manage, verify, test, and deploy software repositories across a secure network topology[span_0](start_span)[span_0](end_span). Driven by **Gemini Pro Thinking** capabilities and secured via **WireGuard** tunneling, Fleet coordinates specialized AI agents to execute continuous integration missions and audit codebases[span_1](start_span)[span_1](end_span).

---

## 🎯 What this does?
* **🔍 Autonomous Scouting & Triage:** Scans target repositories for signals (failing CI, missing tests, outdated dependencies) and prioritizes missions using a SQLite-backed task queue[span_2](start_span)[span_2](end_span).
* **⚖️ Rigorous Verification & Learning:** Evaluates candidate code against strict verification rules and distills execution outcomes into plain-language lessons to optimize future agent behavior[span_3](start_span)[span_3](end_span).
* **🧪 Automated Sandbox Testing:** Runs candidate checks in a controlled Docker sandbox environment to ensure zero regressions before deployment[span_4](start_span)[span_4](end_span).
* **🚢 Safe Deployments:** Ships verified code candidates with built-in rollback protection points and strict circuit-breaker failure behaviors[span_5](start_span)[span_5](end_span).
* **🔒 Encrypted Inter-Node Communication:** Keeps the entire fleet operating over a private WireGuard mesh network, completely hidden from public internet exposure[span_6](start_span)[span_6](end_span).

---

## ⚙️ How does this work?
Fleet relies on a modular, decoupled architecture centered around core coordination mechanisms:

* **Coordinator:** Manages each mission down the 5-role agent pipeline (`Scout` $\rightarrow$ `Verifier` $\rightarrow$ `Learner` $\rightarrow$ `Tester` $\rightarrow$ `Deployer`)[span_7](start_span)[span_7](end_span).
* **Node Registry & Load Balancer:** Tracks active worker nodes, monitors heartbeats, and routes tasks to the least-loaded healthy node[span_8](start_span)[span_8](end_span).
* **Circuit Breaker:** Fails fast when error thresholds are exceeded (opening after consecutive failures and cooling down automatically)[span_9](start_span)[span_9](end_span).
* **Gemini Pro Thinking Integration:** Provides second-opinion verification, sanity checks, and fallback mission planning when standard evaluation paths encounter ambiguous states[span_10](start_span)[span_10](end_span).

---

## 📊 Architecture Diagram

```mermaid
graph TD
    subgraph Secure Mesh Network [WireGuard VPN]
        Coordinator -->|Routes Tasks| NodeRegistry[Node Registry & Load Balancer]
        NodeRegistry --> Scout[Scout Agent]
        Scout --> Verifier[Verifier Agent]
        Verifier --> Learner[Learner Agent]
        Learner --> Tester[Tester Agent]
        Tester --> Deployer[Deployer Agent]
    end

    Deployer -->|Rollback Protected| Production[(Target Repositories)]
    Gemini[Gemini Pro Thinking] -.->|Sanity Check / Fallback| Verifier
