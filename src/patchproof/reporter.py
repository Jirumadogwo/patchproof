"""
PatchProof Reporter
Generates structured JSON and human-readable reports from evaluation outcomes.
"""

import json
from pathlib import Path
from typing import Dict, Any


class ResultReporter:
    """Generates evaluation output reports."""

    @staticmethod
    def generate_json_report(result_data: Dict[str, Any], output_path: Path) -> None:
        """Saves evaluation results to a structured JSON file."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=4)

    @staticmethod
    def format_human_summary(result_data: Dict[str, Any]) -> str:
        """Formats evaluation results into a clean human-readable summary string."""
        summary = []
        summary.append("=" * 50)
        summary.append("PATCHPROOF EVALUATION REPORT")
        summary.append("=" * 50)
        summary.append(f"Task ID: {result_data.get('task_id', 'Unknown')}")
        summary.append(f"Status:  {result_data.get('status', 'INCONCLUSIVE')}")
        summary.append(f"Public Tests Passed:    {result_data.get('public_passed', False)}")
        summary.append(f"Holdout Tests Passed:   {result_data.get('holdout_passed', False)}")
        summary.append(f"Regression Tests Passed: {result_data.get('regression_passed', False)}")
        summary.append("-" * 50)
        summary.append("Details / Output:")
        summary.append(result_data.get('output', 'No output recorded.'))
        summary.append("=" * 50)
        return "\n".join(summary)

"""
PatchProof Report Generator
"""

import json
from typing import Dict, Any

class ReportGenerator:
    @staticmethod
    def create_report(run_id: str, task_id: str, model: str, status: str, metrics: Dict[str, Any], logs: list) -> Dict[str, Any]:
        return {
            "report_version": "1.0",
            "run_id": run_id,
            "task_id": task_id,
            "model": model,
            "status": status,
            "metrics": metrics,
            "logs": logs
        }
