# 🚀 Fleet: Autonomous Multi-Agent Infrastructure Framework

![CI Status](https://github.com/darnellwashingtonjr94-art/fleet/actions/workflows/fleet-ci.yml/badge.svg)
![Docker Build](https://img.shields.io/docker/v/credkellar/fleet?label=docker%20hub)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🤖 What is this about?
**Fleet** is an autonomous, self-healing multi-agent orchestration framework designed to manage, verify, test, and deploy software repositories across a secure network topology[span_0](start_span)[span_0](end_span). Driven by **Gemini Pro Thinking** capabilities and secured via **WireGuard** tunneling, Fleet coordinates specialized AI agents to execute continuous integration missions and audit codebases[span_1](start_span)[span_1](end_span).

# 🚀 fleet-core

## 🧰 Tech Stack Badges & Architecture

### 💻 Core Programming Languages & Core Systems
![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![gRPC](https://img.shields.io/badge/gRPC-2DA6B0?style=for-the-badge&logo=grpc&logoColor=white)
![Protocol Buffers](https://img.shields.io/badge/Protocol_Buffers-4285F4?style=for-the-badge&logo=google&logoColor=white)

### ⛓️ Web3 & Infrastructure
![libp2p](https://img.shields.io/badge/libp2p-3B82F6?style=for-the-badge&logo=libp2p&logoColor=white)
![Ethereum](https://img.shields.io/badge/Ethereum-3C3C3D?style=for-the-badge&logo=ethereum&logoColor=white)
![Web3.js](https://img.shields.io/badge/Web3.js-F16822?style=for-the-badge&logo=web3dotjs&logoColor=white)
![IPFS](https://img.shields.io/badge/IPFS-65C2CB?style=for-the-badge&logo=ipfs&logoColor=white)
![Solidity](https://img.shields.io/badge/Solidity-363636?style=for-the-badge&logo=solidity&logoColor=white)

### ⚙️ Platform Support & Hardware Architecture
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)
![ARM64](https://img.shields.io/badge/ARM64-0091BD?style=for-the-badge&logo=arm&logoColor=white)
![x86_64](https://img.shields.io/badge/x86__64-0071C5?style=for-the-badge&logo=intel&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry_Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)

### ⚡ Low-Level Infrastructure & Performance
![eBPF](https://img.shields.io/badge/eBPF-191919?style=for-the-badge&logo=ebpf&logoColor=white)
![WebAssembly](https://img.shields.io/badge/WebAssembly-654FF0?style=for-the-badge&logo=webassembly&logoColor=white)
![io_uring](https://img.shields.io/badge/io__uring-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![cgroups](https://img.shields.io/badge/cgroups_v2-191919?style=for-the-badge&logo=linux&logoColor=white)

### 🛠️ DevOps & Build Tools
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Make](https://img.shields.io/badge/Make-000000?style=for-the-badge&logo=gnu&logoColor=white)
![Taskfile](https://img.shields.io/badge/Taskfile-2DA6B0?style=for-the-badge&logo=task&logoColor=white)
![GolangCI-Lint](https://img.shields.io/badge/GolangCI--Lint-00ADD8?style=for-the-badge&logo=go&logoColor=white)

### ☁️ Cloud
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=for-the-badge&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)


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
