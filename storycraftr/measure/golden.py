import json
from pathlib import Path
from typing import Any, Dict

GOLDEN_SCORES_PATH = Path(__file__).parent / "golden_scores.json"


def load_golden_scores() -> Dict[str, Any]:
    """Loads the golden standard scores from the JSON file."""
    if not GOLDEN_SCORES_PATH.exists():
        return {}
    with open(GOLDEN_SCORES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_golden_scores(model_name: str, results: list[Dict[str, Any]]):
    """Saves benchmark results as the new golden standard."""
    golden_data = {
        "model_name": model_name,
        "benchmarks": {},
    }
    for result in results:
        benchmark_id = result["benchmark_id"]
        scores = {
            "rouge1": result["scores"]["rouge1"],
            "rouge2": result["scores"]["rouge2"],
            "rougeL": result["scores"]["rougeL"],
        }
        golden_data["benchmarks"][benchmark_id] = scores

    with open(GOLDEN_SCORES_PATH, "w", encoding="utf-8") as f:
        json.dump(golden_data, f, indent=2)
