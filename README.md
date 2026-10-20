# 🚀 Fleet: Autonomous Multi-Agent Infrastructure Framework

![CI Status](https://github.com/darnellwashingtonjr94-art/fleet/actions/workflows/fleet-ci.yml/badge.svg)
![Docker Build](https://img.shields.io/docker/v/credkellar/fleet?label=docker%20hub)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🤖 What is this about?
**Fleet** is an autonomous, self-healing multi-agent orchestration framework designed to manage, verify, test, and deploy software repositories across a secure network topology[span_0](start_span)[span_0](end_span). Driven by **Gemini Pro Thinking** capabilities and secured via **WireGuard** tunneling, Fleet coordinates specialized AI agents to execute continuous integration missions and audit codebases[span_1](start_span)[span_1](end_span).

# 🚀 fleet-core — Architecture & Technical Stack

## 🧰 Tech Stack badges & Architecture

[![Go Version](https://img.shields.io/github/go-mod/go-version/fleet-core/fleet-core?style=flat-square&logo=go)](https://golang.org)
[![Build Status](https://img.shields.io/github/actions/workflow/status/fleet-core/fleet-core/ci.yml?style=flat-square&logo=githubactions)](https://github.com/fleet-core/fleet-core/actions)
[![License](https://img.shields.io/github/license/fleet-core/fleet-core?style=flat-square)](LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/fleetcore/core?style=flat-square&logo=docker)](https://hub.docker.com/r/fleetcore/core)
[![Release](https://img.shields.io/github/v/release/fleet-core/fleet-core?style=flat-square)](https://github.com/fleet-core/fleet-core/releases)

---

## 💻 Core Programming Languages & Core Systems

* **Go (Golang)** - Primary language for concurrency-heavy core services, daemons, and control planes.
* **Rust** - High-performance memory-safe execution layers, cryptography modules, and low-level drivers.
* **TypeScript / Node.js** - Operator CLI tooling, administrative dashboards, and developer SDKs.
* **Protocol Buffers (Protobuf) & gRPC** - High-efficiency inter-service communication and strongly-typed contract definitions.

---

## ⛓️ Web3 & Infrastructure

* **libp2p** - Peer-to-peer networking, node discovery, secure encrypted transport channels, and NAT traversal.
* **EVM / Smart Contracts** - On-chain state settlement, registry governance, and protocol interaction layers.
* **Consensus Engines** - Integration pipelines for BFT/PoS consensus state machines and validator node telemetry.
* **Cryptographic Primitives** - Ed25519, secp256k1, and zero-knowledge proof verification modules.

---

## ⚙️ Platform Support & Hardware Architecture

* **Architectures:** `linux/amd64`, `linux/arm64`, `darwin/amd64`, `darwin/arm64` (Apple Silicon native support).
* **Hardware Interfacing:** Bare-metal telemetry collectors, direct kernel event streams, and edge computing nodes.
* **Embedded & IoT Targets:** Low-resource resource-constrained environments and gateway aggregation hardware.

---

## ⚡ Low-Level Infrastructure & Performance

* **eBPF (Extended Berkeley Packet Filter)** - Kernel-level observability, network tracing, and security enforcement without context switching.
* **Linux Kernel Subsystems** - cgroups v2 resource accounting, namespaces isolation, and io_uring high-throughput I/O.
* **Memory Management** - Zero-copy buffer pooling, lock-free ring buffers, and custom memory allocators to eliminate GC overhead.
* **Concurrency Models** - Actor model patterns and CSP (Communicating Sequential Processes) worker pools.

---

## 🛠️ DevOps & Build Tools

* **Makefile & Taskfile** - Standardized build orchestration, code generation hooks, and local development flows.
* **GitHub Actions** - Continuous Integration (CI), automated multi-arch cross-compilation, and regression test suites.
* **GolangCI-Lint & Staticcheck** - Rigorous static code analysis, security linting, and style enforcement.
* **Docker & Buildx** - Multi-architecture container image authoring and optimized layer caching.

---

## ☁️ Cloud

* **Kubernetes & Helm** - Native orchestration, custom controllers (CRDs), and declarative GitOps deployments.
* **Terraform / OpenTofu** - Infrastructure as Code (IaC) for multi-cloud provisioning and network topology management.
* **AWS / GCP / Azure** - Enterprise cloud provider integrations for elastic compute, object storage, and secure key vaults.
* **Prometheus & Grafana** - Real-time metrics scraping, alerting rules, and operational performance dashboards.

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
