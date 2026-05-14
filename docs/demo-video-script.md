# VeriVision Demo Video Script (3 minutes)

## Timeline

| Time | Section | Content | Screen |
|------|---------|---------|--------|
| 0:00-0:20 | Hook | "AI vision models lie. VeriVision catches them." | Title card + hallucination example |
| 0:20-0:50 | Problem | Show VLM hallucination examples: "I see a cat" (no cat), "I see a stop sign" (it's a billboard) | Side-by-side: image vs VLM description |
| 0:50-1:40 | Solution | VeriVision pipeline: VLM-A describes → VLM-B verifies → Hallucination detected! | Live demo: upload image → see results |
| 1:40-2:20 | 0G Integration | "Results stored on 0G Storage — immutable, verifiable, decentralized" | Show: TX hash → 0G Explorer → on-chain record |
| 2:20-2:45 | Smart Contract | VeriVisionRegistry on 0G Galileo testnet | Show contract on explorer, call getHallucinationRate |
| 2:45-3:00 | CTA | "VeriVision — Decentralized AI Verification on 0G" | Logo + #0GHackathon #BuildOn0G |

## Recording Checklist

- [ ] Screen recording tool (OBS / Loom / QuickTime)
- [ ] Browser tabs: Gradio UI, 0G Explorer, GitHub repo
- [ ] Test images prepared (at least 3 with known hallucinations)
- [ ] Clear audio narration
- [ ] Upload to YouTube (unlisted OK) or Loom

## Narration Script

### 0:00-0:20 Hook
"Vision Language Models are powerful — but they hallucinate. They describe objects that don't exist. This is a critical trust problem for AI agents, autonomous systems, and anyone relying on AI vision. VeriVision catches these hallucinations — and stores proof on-chain."

### 0:20-0:50 Problem
"Let me show you. When we ask a VLM to describe this image, it says 'I see a cat on the table.' But look — there's no cat. The VLM hallucinated. This happens 30-40% of the time with complex images. In safety-critical applications, this is dangerous."

### 0:50-1:40 Solution
"VeriVision uses a cross-model verification approach. First, VLM-A describes the image and lists all objects. Then, VLM-B — a skeptical verifier — examines each claimed object independently. 'Is there really a cat? Let me check.' Objects that fail verification are flagged as hallucinations. The result is a detailed report with confidence scores for each object."

### 1:40-2:20 0G Integration
"But here's the key innovation: every verification result is stored on 0G Storage — making it immutable and auditable. No one can tamper with the verification history. Here's a transaction on the 0G Galileo testnet. You can see the report hash, the timestamp, and the full audit trail on the 0G Explorer."

### 2:20-2:45 Smart Contract
"We also deployed VeriVisionRegistry — a smart contract on 0G Chain. It records verification metadata on-chain: which models were used, how many objects were verified, and the hallucination rate. This creates a transparent, queryable database of AI verification results."

### 2:45-3:00 CTA
"VeriVision — making AI vision trustworthy, one verification at a time. Built on 0G, the decentralized AI operating system. #0GHackathon #BuildOn0G"
