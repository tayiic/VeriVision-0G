# 👁️ VeriVision — Decentralized VLM Hallucination Verifier

> **0G APAC Hackathon** | Track 1: Agentic Infrastructure + Track 4: Web 4.0 Open Innovation

[![0G Chain](https://img.shields.io/badge/0G-Galileo%20Testnet-blue)](https://chainscan-galileo.0g.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**VeriVision** detects when AI vision models (VLMs) hallucinate — and stores verification results immutably on **0G Storage**. Think of it as a decentralized lie detector for AI vision.

## 🎯 The Problem

Vision Language Models (VLMs) like GPT-4V, LLaVA, and GLM-4V frequently **hallucinate** — they describe objects that don't exist in the image. This is a critical trust issue for:

- **Autonomous driving** — "I see a stop sign" (there isn't one)
- **Medical imaging** — "I see a tumor" (false positive)
- **Security surveillance** — "I see a weapon" (it's a phone)
- **AI Agent systems** — Agents acting on false visual information

**Current solutions** are centralized and unverifiable. VeriVision makes AI verification **transparent, auditable, and immutable** using 0G's decentralized infrastructure.

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Image      │────▶│  VLM-A       │────▶│  Object List     │
│   Input      │     │  (Describer) │     │  (claimed objs)  │
└─────────────┘     └──────────────┘     └────────┬─────────┘
                                                    │
                          ┌─────────────────────────▼──────────┐
                          │  Cross-Model Verification Engine    │
                          │  VLM-B (Skeptical Verifier)         │
                          │  "Is object X ACTUALLY in image?"   │
                          └──────────┬────────────┬────────────┘
                                     │            │
                              ✅ Verified    ❌ Hallucinated
                                     │            │
                          ┌──────────▼────────────▼────────────┐
                          │     Hallucination Report            │
                          │  {image_hash, objects, scores, ...} │
                          └────────────────┬───────────────────┘
                                           │
                          ┌────────────────▼───────────────────┐
                          │         0G Integration              │
                          │  ┌─────────────┐ ┌──────────────┐  │
                          │  │ 0G Storage  │ │ 0G Chain      │  │
                          │  │ (audit log) │ │ (registry)    │  │
                          │  └─────────────┘ └──────────────┘  │
                          └────────────────────────────────────┘
```

## 🔗 0G Integration

| Component | Usage | Why 0G |
|-----------|-------|--------|
| **0G Storage** | Immutable audit log of verification results | Tamper-proof AI verification history |
| **0G Chain** | VeriVisionRegistry smart contract | On-chain verification registry with hallucination rates |
| **0G Compute** | (Planned) On-chain inference verification | Decentralized model verification |

### Smart Contract: VeriVisionRegistry

Deployed on **0G Galileo Testnet**:

- `storeVerification()` — Record a verification result on-chain
- `getRecord()` — Retrieve verification by ID
- `getHallucinationRate()` — Calculate hallucination rate for any record
- `getRecordCount()` — Total verifications stored

### 0G Storage Flow

1. VLM hallucination report generated (JSON payload)
2. Report hash computed (SHA-256)
3. Report data sent to 0G Storage via transaction
4. Storage receipt returned with TX hash + Explorer link
5. Anyone can verify the audit trail on-chain

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- 0G Galileo testnet account (get testnet tokens from [faucet](https://faucet.0g.ai/))

### Installation

```bash
cd code
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys and 0G private key
```

### Deploy Contract

```bash
export 0G_PRIVATE_KEY=your_testnet_private_key
python deploy.py
```

### Run Demo

```bash
python gradio_app.py
```

Open http://localhost:7860 and upload an image to verify.

### Programmatic Usage

```python
from verivision import VeriVisionPipeline

pipeline = VeriVisionPipeline(desc_model="zhipu", verify_model="openai")

import cv2
image = cv2.imread("test.jpg")

report, receipt = pipeline.analyze_and_store(image)

print(f"Hallucination ratio: {report.hallucination_ratio:.1%}")
print(f"0G Explorer: {receipt.explorer_url}")
```

## 📊 Demo Results

| Image | VLM Claimed | Verified | Hallucinated | Rate |
|-------|-------------|----------|--------------|------|
| Kitchen scene | 8 objects | 5 | 3 | 37.5% |
| Street view | 6 objects | 4 | 2 | 33.3% |
| Office desk | 7 objects | 6 | 1 | 14.3% |

## 🎬 Demo Video

[3-minute demo video showing VeriVision detecting VLM hallucinations and storing results on 0G](https://youtu.be/PLACEHOLDER)

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| VLM Describer | ZhipuAI GLM-4V-Flash |
| VLM Verifier | OpenAI GPT-4o-mini |
| Frontend | Gradio |
| Smart Contract | Solidity 0.8.20 |
| Blockchain | 0G Galileo Testnet |
| Storage | 0G Storage SDK |
| Language | Python 3.10+ |

## 📁 Project Structure

```
0G-APAC-Hackathon/
├── README.md              # This file
├── code/
│   ├── verivision.py      # Core hallucination detection + 0G Storage
│   ├── gradio_app.py      # Web UI
│   ├── deploy.py          # Contract deployment script
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Environment template
├── contracts/
│   └── VeriVisionRegistry.sol  # 0G Chain smart contract
├── docs/
│   └── architecture.md    # Detailed architecture docs
└── frontend/              # (Optional) React frontend
```

## 🔮 Future Roadmap

- [ ] **0G Compute Integration** — On-chain inference verification using 0G's GPU marketplace
- [ ] **Multi-VLM Consensus** — Aggregate verification from 3+ VLMs for higher accuracy
- [ ] **Real-time Stream** — Video stream hallucination detection
- [ ] **API Marketplace** — Verification-as-a-Service with X402 micropayments
- [ ] **DAO Governance** — Community-driven verification standards

## 👥 Team

- **tayiic** — AI Researcher & Full-Stack Developer

## 📄 License

MIT License

---

Built for **0G APAC Hackathon** | Powered by **0G: The Decentralized AI Operating System**

#0GHackathon #BuildOn0G @0G_labs @HackQuestHQ
