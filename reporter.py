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
