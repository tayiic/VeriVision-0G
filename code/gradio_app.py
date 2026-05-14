"""
VeriVision — Gradio Frontend
Decentralized VLM Hallucination Verifier with 0G Storage
"""

import os
import sys
import json
import time
import random
import hashlib
from pathlib import Path

import gradio as gr
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from verivision import VeriVisionPipeline, HallucinationReport, StorageReceipt

DEMO_MODE = os.environ.get("VERIVISION_DEMO", "0") == "1"

_DEMO_SCENARIOS = [
    {
        "desc": "I can see a cat sitting on a windowsill, a red stop sign on the street, and a bicycle parked nearby.",
        "objects": ["cat", "stop sign", "bicycle", "windowsill", "street"],
        "verified": ["cat", "bicycle", "windowsill"],
        "hallucinated": ["stop sign", "street"],
        "confidence": {"cat": 0.92, "stop sign": 0.15, "bicycle": 0.88, "windowsill": 0.75, "street": 0.22},
    },
    {
        "desc": "The image shows a crowded restaurant table with plates of food, wine glasses, and a laptop computer.",
        "objects": ["plates of food", "wine glasses", "laptop computer", "restaurant table", "crowd"],
        "verified": ["plates of food", "wine glasses", "restaurant table"],
        "hallucinated": ["laptop computer", "crowd"],
        "confidence": {"plates of food": 0.95, "wine glasses": 0.87, "laptop computer": 0.18, "restaurant table": 0.91, "crowd": 0.25},
    },
    {
        "desc": "A mirror room with reflections of a person standing in the center, surrounded by ornate golden frames and a chandelier above.",
        "objects": ["mirror", "person", "golden frames", "chandelier", "reflections"],
        "verified": ["mirror", "person", "reflections"],
        "hallucinated": ["golden frames", "chandelier"],
        "confidence": {"mirror": 0.96, "person": 0.89, "golden frames": 0.20, "chandelier": 0.12, "reflections": 0.93},
    },
]

pipeline = None
_analysis_cache = {}


def _get_pipeline():
    global pipeline
    if pipeline is None:
        desc = os.environ.get("DESC_MODEL", "zhipu")
        verify = os.environ.get("VERIFY_MODEL", "openai")
        pipeline = VeriVisionPipeline(desc_model=desc, verify_model=verify)
    return pipeline


def _demo_analyze(image, store_on_chain: bool = True):
    scenario = random.choice(_DEMO_SCENARIOS)
    img_np = np.array(image) if image is not None else np.zeros((100, 100, 3), dtype=np.uint8)
    image_hash = hashlib.sha256(img_np.tobytes()).hexdigest()[:16] if image is not None else "demo_hash"

    report = HallucinationReport(
        image_hash=image_hash,
        vlm_description=scenario["desc"],
        vlm_objects=scenario["objects"],
        verified_objects=scenario["verified"],
        hallucinated_objects=scenario["hallucinated"],
        confidence_scores=scenario["confidence"],
        verifier_model="gpt-4o-mini (demo)",
        describer_model="glm-4v-flash (demo)",
    )
    receipt = StorageReceipt(
        root_hash=hashlib.sha256(report.to_json().encode()).hexdigest(),
        tx_hash="0x" + hashlib.sha256(str(time.time()).encode()).hexdigest()[:64],
        explorer_url=f"https://chainscan-galileo.0g.ai/tx/0x{'a' * 64}",
        timestamp=time.time(),
        size_bytes=len(report.to_0g_payload()),
    )
    return report, receipt


def _format_confidence_bars(report: HallucinationReport) -> str:
    lines = []
    for obj in report.vlm_objects:
        conf = report.confidence_scores.get(obj, 0)
        is_hallucinated = obj in report.hallucinated_objects
        bar_len = int(conf * 10)
        if is_hallucinated:
            bar = "\U0001f7e5" * bar_len + "\u2b1c" * (10 - bar_len)
            lines.append(f"**{obj}** \u2014 HALLUCINATED\n{bar} {conf:.0%}\n")
        else:
            bar = "\U0001f7e9" * bar_len + "\u2b1c" * (10 - bar_len)
            lines.append(f"**{obj}** \u2014 verified\n{bar} {conf:.0%}\n")
    return "\n".join(lines)


def analyze_image(image, store_on_chain: bool = True):
    if image is None:
        return "Please upload an image.", "", "", "", ""

    if DEMO_MODE:
        report, receipt = _demo_analyze(image, store_on_chain)
    else:
        p = _get_pipeline()
        img_np = np.array(image)

        cache_key = str(hash(img_np.tobytes()))
        if cache_key in _analysis_cache:
            report, receipt = _analysis_cache[cache_key]
        else:
            if store_on_chain:
                report, receipt = p.analyze_and_store(img_np)
            else:
                report = p.quick_analyze(img_np)
                receipt = StorageReceipt(
                    root_hash="off-chain",
                    tx_hash="N/A",
                    explorer_url="N/A",
                    timestamp=time.time(),
                    size_bytes=0,
                )
            _analysis_cache[cache_key] = (report, receipt)

    summary = (
        f"## Verification Summary\n"
        f"- **Objects detected by VLM**: {len(report.vlm_objects)}\n"
        f"- **Verified objects**: {len(report.verified_objects)}\n"
        f"- **Hallucinated objects**: {len(report.hallucinated_objects)}\n"
        f"- **Hallucination ratio**: {report.hallucination_ratio:.1%}\n"
        f"- **Describer**: {report.describer_model}\n"
        f"- **Verifier**: {report.verifier_model}\n"
    )

    confidence = _format_confidence_bars(report)

    description = report.vlm_description

    chain_info = (
        f"## 0G Storage Receipt\n"
        f"- **Root Hash**: `{receipt.root_hash}`\n"
        f"- **TX Hash**: `{receipt.tx_hash}`\n"
        f"- **Explorer**: [View on 0G Explorer]({receipt.explorer_url})\n"
        f"- **Size**: {receipt.size_bytes} bytes\n"
        f"- **Timestamp**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(receipt.timestamp))}\n"
    )

    json_output = report.to_json()

    return summary, confidence, description, chain_info, json_output


def create_ui():
    with gr.Blocks(
        title="VeriVision \u2014 Decentralized VLM Hallucination Verifier",
    ) as demo:
        gr.Markdown(
            "# \U0001f441\ufe0f VeriVision \u2014 Decentralized VLM Hallucination Verifier\n"
            "Detect when AI vision models hallucinate, and store verification results immutably on **0G Storage**.\n\n"
            "**Track 1**: Agentic Infrastructure | **Track 4**: Web 4.0 Open Innovation"
            + ("\n\n⚠️ **DEMO MODE** — Using simulated VLM responses for demonstration" if DEMO_MODE else "")
        )

        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(type="pil", label="Upload Image")
                store_checkbox = gr.Checkbox(
                    value=True, label="Store on 0G Chain (immutable audit log)"
                )
                analyze_btn = gr.Button("\U0001f50d Analyze & Verify", variant="primary")

            with gr.Column(scale=2):
                summary_output = gr.Markdown(label="Summary")
                confidence_output = gr.Markdown(label="Object Verification")

        with gr.Row():
            with gr.Column():
                desc_output = gr.Textbox(label="VLM Description", lines=4)
            with gr.Column():
                chain_output = gr.Markdown(label="0G Storage Receipt")

        json_output = gr.Textbox(label="Full Report (JSON)", lines=8, visible=False)

        gr.Markdown(
            "### How it works\n"
            "1. **VLM-A** describes the image (ZhipuAI GLM-4V)\n"
            "2. **VLM-B** skeptically verifies each claimed object (OpenAI GPT-4o-mini)\n"
            "3. Cross-model verification catches hallucinations\n"
            "4. Results stored on **0G Storage** for immutable audit trail\n\n"
            "### 0G Integration\n"
            "- **0G Storage**: Verification reports stored immutably on-chain\n"
            "- **0G Chain**: Smart contract registry for verification records\n"
            "- **0G Compute** (planned): On-chain inference verification"
        )

        analyze_btn.click(
            fn=analyze_image,
            inputs=[image_input, store_checkbox],
            outputs=[summary_output, confidence_output, desc_output, chain_output, json_output],
        )

    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7861,
        share=False,
    )
