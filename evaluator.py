"""
PatchProof Evaluator Core Execution Module
"""

import subprocess
import time
from pathlib import Path
from typing import Dict, Any


class PatchEvaluator:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def run_tests(self, test_path: Path) -> Dict[str, Any]:
        start_time = time.time()
        try:
            result = subprocess.run(
                ["pytest", str(test_path), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            duration_ms = int((time.time() - start_time) * 1000)
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration_ms": duration_ms
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Execution timed out",
                "duration_ms": self.timeout * 1000
            }
