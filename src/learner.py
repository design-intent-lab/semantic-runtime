import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge_base"


def _ensure_dir(tx_type: str):
    d = KNOWLEDGE_DIR / "transformations" / tx_type
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_attempts(tx_type: str) -> list[dict]:
    p = _ensure_dir(tx_type) / "attempts.json"
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return []


def save_attempt(tx_type: str, attempt: dict):
    attempts = load_attempts(tx_type)
    attempt["timestamp"] = datetime.utcnow().isoformat()
    attempt["attempt_number"] = len(attempts) + 1
    attempts.append(attempt)
    p = _ensure_dir(tx_type) / "attempts.json"
    with open(p, "w") as f:
        json.dump(attempts, f, indent=2, ensure_ascii=False)


def _scene_signature(scene_desc: dict) -> str:
    light_count = scene_desc.get("light_count", 0)
    total_energy = scene_desc.get("total_energy", 0)
    avg_temp = scene_desc.get("avg_temperature", 5000)
    return f"lights={light_count}_energy={total_energy}_temp={avg_temp}"


def find_best_params(tx_type: str, scene_desc: dict) -> dict | None:
    attempts = load_attempts(tx_type)
    if not attempts:
        return None
    sig = _scene_signature(scene_desc)
    candidates = [a for a in attempts if a.get("scene_signature") == sig and a.get("success")]
    if candidates:
        best = max(candidates, key=lambda a: a.get("confidence", 0))
        return {
            "source": "learned",
            "confidence": best.get("confidence", 0.5),
            "parameters": best.get("parameters", {}),
        }
    successful = [a for a in attempts if a.get("success")]
    if successful:
        best = max(successful, key=lambda a: a.get("confidence", 0))
        return {
            "source": "generalized",
            "confidence": best.get("confidence", 0.3),
            "parameters": best.get("parameters", {}),
        }
    return None


def compute_confidence(tx_type: str) -> float:
    attempts = load_attempts(tx_type)
    if not attempts:
        return 0.0
    recent = attempts[-5:]
    successes = sum(1 for a in recent if a.get("success"))
    rate = successes / len(recent)
    base = rate * 0.7 + 0.1
    return min(base + 0.1 * len(recent), 0.99)


def adapt_params(tx_type: str, params: dict, scene_desc: dict) -> dict:
    best = find_best_params(tx_type, scene_desc)
    if best:
        adapted = dict(best["parameters"])
        adapted["_confidence"] = best["confidence"]
        adapted["_source"] = best["source"]
        return adapted

    energy = scene_desc.get("total_energy", 1000)
    if energy > 500:
        params["energy_multiplier"] = max(params.get("energy_multiplier", 0.5) * 0.8, 0.05)
    else:
        params["energy_multiplier"] = min(params.get("energy_multiplier", 0.5) * 1.2, 0.5)
    params["_confidence"] = compute_confidence(tx_type)
    params["_source"] = "default"
    return params
