"""
VeriVision — Decentralized VLM Hallucination Verifier
Core hallucination detection + 0G Storage integration

Pipeline:
  Image -> VLM Description -> Object Extraction
       -> Cross-Model Verification (skeptical prompt)
       -> Hallucination Detection
       -> 0G Storage (immutable audit log)

Track: 1 (Agentic Infrastructure) + 4 (Web 4.0 Open Innovation)
0G Components: Storage + Chain
"""

import os
import json
import time
import base64
import hashlib
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Tuple
from pathlib import Path

import cv2
import numpy as np


@dataclass
class HallucinationReport:
    image_hash: str
    vlm_description: str
    vlm_objects: List[str]
    verified_objects: List[str]
    hallucinated_objects: List[str]
    confidence_scores: Dict[str, float]
    timestamp: float = 0.0
    verifier_model: str = ""
    describer_model: str = ""

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()

    @property
    def hallucination_ratio(self) -> float:
        if not self.vlm_objects:
            return 0.0
        return len(self.hallucinated_objects) / len(self.vlm_objects)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)

    def to_0g_payload(self) -> bytes:
        return self.to_json().encode("utf-8")


@dataclass
class StorageReceipt:
    root_hash: str
    tx_hash: str
    explorer_url: str
    timestamp: float
    size_bytes: int


class VLMHallucinationDetector:
    def __init__(self, desc_model: str = "zhipu", verify_model: str = "openai"):
        self.desc_model = desc_model
        self.verify_model = verify_model
        self._desc_api = desc_model
        self._verify_api = verify_model
        self._load_env()

    def _load_env(self):
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        key = key.strip()
                        value = value.strip()
                        if key and value and key not in os.environ:
                            os.environ[key] = value

    def _encode_image(self, image: np.ndarray) -> str:
        _, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 90])
        return base64.b64encode(buffer).decode("utf-8")

    def _call_zhipu(self, img_b64: str, prompt: str, model: str = "glm-4v-flash") -> str:
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=os.environ["ZHIPU_API_KEY"])
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                    {"type": "text", "text": prompt},
                ],
            }],
            max_tokens=500,
            temperature=0.1,
        )
        return response.choices[0].message.content

    def _call_openai(self, img_b64: str, prompt: str, model: str = "gpt-4o-mini") -> str:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                    {"type": "text", "text": prompt},
                ],
            }],
            max_tokens=500,
            temperature=0.1,
        )
        return response.choices[0].message.content

    def _describe(self, img_b64: str) -> str:
        prompt = "Describe all objects you can see in this image. List each object clearly."
        if self._desc_api == "zhipu":
            return self._call_zhipu(img_b64, prompt)
        return self._call_openai(img_b64, prompt)

    def _extract_objects(self, description: str) -> List[str]:
        import re
        patterns = [
            r'(?:there (?:is|are)|I (?:see|can see)|I notice|visible|present|shown)[\s:]*(.+?)(?:\.|,|$)',
            r'(?:a|an|the)\s+([\w\s]+?)(?:\s+(?:is|are|in|on|at|with|and|,|\.))',
        ]
        objects = set()
        for pattern in patterns:
            for match in re.finditer(pattern, description, re.IGNORECASE):
                obj = match.group(1).strip().lower()
                if len(obj) > 2 and len(obj) < 40:
                    objects.add(obj)
        words = re.findall(r'\b(?:a|an|the)\s+(\w+(?:\s+\w+)?)\b', description, re.IGNORECASE)
        for w in words:
            w = w.strip().lower()
            if len(w) > 2 and len(w) < 40:
                objects.add(w)
        return sorted(objects)

    def _verify_objects(self, img_b64: str, objects: List[str]) -> Dict[str, dict]:
        if not objects:
            return {}
        obj_list = ", ".join(objects)
        prompt = (
            f"You are a skeptical verifier. A VLM claimed these objects are in the image: [{obj_list}].\n"
            f"For EACH object, carefully examine the image and determine if it is ACTUALLY present.\n"
            f"Be strict — only confirm objects you can clearly see. Do not assume.\n"
            f"Respond in JSON format: {{\"object_name\": {{\"present\": true/false, \"confidence\": 0.0-1.0, \"reason\": \"...\"}}}}"
        )
        if self._verify_api == "openai":
            response = self._call_openai(img_b64, prompt, model="gpt-4o-mini")
        else:
            response = self._call_zhipu(img_b64, prompt)
        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
        except (json.JSONDecodeError, AttributeError):
            pass
        results = {}
        for obj in objects:
            results[obj] = {"present": True, "confidence": 0.5, "reason": "parse_failed"}
        return results

    def analyze(self, image: np.ndarray) -> HallucinationReport:
        img_b64 = self._encode_image(image)
        image_hash = hashlib.sha256(image.tobytes()).hexdigest()[:16]

        description = self._describe(img_b64)
        vlm_objects = self._extract_objects(description)
        verification = self._verify_objects(img_b64, vlm_objects)

        verified = []
        hallucinated = []
        confidence = {}
        for obj in vlm_objects:
            detail = verification.get(obj, {})
            is_present = detail.get("present", True)
            conf = detail.get("confidence", 0.5)
            confidence[obj] = conf
            if is_present and conf >= 0.5:
                verified.append(obj)
            else:
                hallucinated.append(obj)

        return HallucinationReport(
            image_hash=image_hash,
            vlm_description=description,
            vlm_objects=vlm_objects,
            verified_objects=verified,
            hallucinated_objects=hallucinated,
            confidence_scores=confidence,
            verifier_model=self._verify_api,
            describer_model=self._desc_api,
        )


class OGStorageClient:
    def __init__(self, rpc_url: str = "", private_key: str = ""):
        self.rpc_url = rpc_url or os.environ.get("0G_RPC_URL", "https://evmrpc-testnet.0g.ai")
        self.private_key = private_key or os.environ.get("0G_PRIVATE_KEY", "")
        self.chain_id = 16602
        self._web3 = None

    def _get_web3(self):
        if self._web3 is None:
            try:
                from web3 import Web3
                self._web3 = Web3(Web3.HTTPProvider(self.rpc_url))
            except ImportError:
                raise ImportError("web3 not installed. Run: pip install web3")
        return self._web3

    def store_report(self, report: HallucinationReport) -> StorageReceipt:
        w3 = self._get_web3()
        payload = report.to_0g_payload()
        payload_hash = hashlib.sha256(payload).hexdigest()

        if not self.private_key:
            return StorageReceipt(
                root_hash=payload_hash,
                tx_hash="0x" + "0" * 64,
                explorer_url=f"https://chainscan-galileo.0g.ai/tx/0x{'0'*64}",
                timestamp=time.time(),
                size_bytes=len(payload),
            )

        account = w3.eth.account.from_key(self.private_key)
        nonce = w3.eth.get_transaction_count(account.address)

        tx = {
            "nonce": nonce,
            "to": "0x0000000000000000000000000000000000000000",
            "value": 0,
            "gas": 100000,
            "gasPrice": w3.eth.gas_price,
            "data": payload[:8192],
            "chainId": self.chain_id,
        }

        signed = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return StorageReceipt(
            root_hash=payload_hash,
            tx_hash=receipt.transactionHash.hex(),
            explorer_url=f"https://chainscan-galileo.0g.ai/tx/{receipt.transactionHash.hex()}",
            timestamp=time.time(),
            size_bytes=len(payload),
        )

    def verify_on_chain(self, tx_hash: str) -> dict:
        w3 = self._get_web3()
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        return {
            "block_number": receipt.blockNumber,
            "status": receipt.status,
            "from": receipt["from"],
            "gas_used": receipt.gasUsed,
            "explorer_url": f"https://chainscan-galileo.0g.ai/tx/{tx_hash}",
        }


class VeriVisionPipeline:
    def __init__(self, desc_model: str = "zhipu", verify_model: str = "openai",
                 og_rpc: str = "", og_key: str = ""):
        self.detector = VLMHallucinationDetector(desc_model, verify_model)
        self.storage = OGStorageClient(og_rpc, og_key)

    def analyze_and_store(self, image: np.ndarray) -> Tuple[HallucinationReport, StorageReceipt]:
        report = self.detector.analyze(image)
        receipt = self.storage.store_report(report)
        return report, receipt

    def quick_analyze(self, image: np.ndarray) -> HallucinationReport:
        return self.detector.analyze(image)
