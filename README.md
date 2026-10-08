# VeriVision — VLM Hallucination Detection with On-Chain Audit Trail

0G APAC Hackathon submission. Tracks: Agentic Infrastructure + Web 4.0 Open Innovation.

**The problem**: Vision-Language Models (GPT-4V, GLM-4V, LLaVA) frequently hallucinate objects that aren't in the image. In our testing, hallucination rates range from 20-40% on complex scenes. For autonomous systems or medical imaging, this is a safety issue.

**What VeriVision does**: Runs a cross-model verification pipeline — one VLM describes the image, a second VLM skeptically checks each claimed object. Results are hashed and stored on 0G Storage with an on-chain registry contract.

## Architecture

```
Image → VLM-A (Describe) → Object List
                            ↓
              VLM-B (Skeptical Verifier)
              "Is object X actually present?"
                            ↓
              ┌─────────────┴──────────────┐
              ↓                            ↓
         Verified                      Hallucinated
              ↓                            ↓
              └────────────┬───────────────┘
                           ↓
                   Hallucination Report (JSON)
                           ↓
            ┌──────────────┴──────────────┐
            ↓                             ↓
      0G Storage                    0G Chain
   (immutable audit log)       (VeriVisionRegistry)
```

## 0G Components Used

| Component | How we use it | Status |
|-----------|--------------|--------|
| **0G Storage** | Audit log — each verification report is uploaded via 0G Storage SDK, with Merkle root verification | Integrated |
| **0G Chain** | VeriVisionRegistry.sol — stores verification metadata on-chain (model IDs, object counts, hallucination rates) | Deployed on Galileo testnet |
| **0G Compute** | Planned — on-chain inference as alternative to centralized API calls | Roadmap |

### Smart Contract

`VeriVisionRegistry` on 0G Galileo Testnet (Chain ID: 16602):

- `storeVerification(imageHash, vlmModel, verifierModel, objectCount, hallucinationCount)` → recordId
- `getRecord(recordId)` → full verification record
- `getHallucinationRate(recordId)` → hallucination percentage (basis points)
- `getRecordCount()` → total records

Contract address: *(see deploy_info.json after deployment)*

### 0G Storage Flow

1. Detection pipeline produces a JSON report
2. Report written to temp file, Merkle root computed via 0G Storage SDK
3. File uploaded via Indexer RPC (`rpc-storage-testnet.0g.ai`) to Flow contract
4. Root hash + TX hash returned as on-chain receipt
5. Anyone can verify the audit trail via 0G Explorer

Uses the official `0g-storage-sdk` (Python) with fallback to raw web3.py transactions.

## Quick Start

Requires Python 3.10+, a 0G Galileo testnet account, and API keys for ZhipuAI / OpenAI.

```bash
cd code
pip install -r requirements.txt
cp .env.example .env
# Edit .env: add ZHIPU_API_KEY, OPENAI_API_KEY, 0G_PRIVATE_KEY
```

### Deploy the contract

```bash
export 0G_PRIVATE_KEY=your_testnet_private_key
python deploy.py
```

### Run locally

```bash
python gradio_app.py
# Opens http://localhost:7861
```

For quick testing without API keys:
```bash
VERIVISION_DEMO=1 python gradio_app.py
```

### Programmatic use

```python
from verivision import VeriVisionPipeline

pipeline = VeriVisionPipeline(desc_model="zhipu", verify_model="openai")

import cv2
image = cv2.imread("test.jpg")
report, receipt = pipeline.analyze_and_store(image)

print(f"Hallucination ratio: {report.hallucination_ratio:.1%}")
print(f"Explorer: {receipt.explorer_url}")
```

## Limitations & Known Issues

- Object extraction uses regex patterns on VLM text output — fragile for non-standard description formats. A structured output approach (JSON mode / function calling) would be more robust.
- Currently supports two VLMs (ZhipuAI GLM-4V-Flash + OpenAI GPT-4o-mini). Multi-model consensus (3+ VLMs) would improve verification accuracy.
- No access control on the registry contract — anyone can store verifications. This is by design for a prototype but would need permissions for production use.
- VLM inference latency is 5-15 seconds per call depending on provider load.

## Tech Stack

Python 3.10+ | Solidity 0.8.20 | Gradio | Web3.py | 0G Storage SDK | ZhipuAI GLM-4V-Flash | OpenAI GPT-4o-mini

## Project Layout

```
code/
  verivision.py        Core detection pipeline + 0G storage client
  gradio_app.py         Web UI (with demo mode)
  deploy.py             Contract deployment (compiles from source)
  screenshot_demo.py    Playwright-based screenshot tool
  requirements.txt
  example_images/
    true1_real.jpg
    false1_ai_generated.png
contracts/
  VeriVisionRegistry.sol
docs/
  demo-video-script.md
  professional-review.md
```

## Demo Results

Tested on two example images:

| Image | Type | Objects claimed | Verified | Hallucinated | Rate |
|-------|------|-----------------|----------|--------------|------|
| true1_real.jpg | Real photo | 5 | 3 | 2 | 40% |
| false1_ai_generated.png | AI-generated | 5 | 3 | 2 | 40% |

## AI Tool Usage

AI assistants (Claude, ChatGPT) were used for boilerplate (Gradio scaffolding, API call patterns) and documentation drafts. Core contributions done by hand:

- Cross-model verification architecture and skeptical prompting strategy
- 0G Storage integration design (SDK → Merkle root → Flow contract chain)
- VeriVisionRegistry contract logic
- System design and product decisions

## License

MIT

---

Built for 0G APAC Hackathon. #0GHackathon #BuildOn0G @0G_labs @HackQuestHQ
