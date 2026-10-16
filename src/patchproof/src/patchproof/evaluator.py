"""
PatchProof Evaluator
Executes candidate patches against public and holdout tests in a controlled environment.
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List

class PatchEvaluator:
    """Evaluates software-repair candidate patches against test suites."""

    def __init__(self, task_dir: Path):
        self.task_dir = task_dir
        self.workspace_dir = task_dir / "workspace"
        self.tests_dir = task_dir / "tests"

    def run_pytest(self, target_path: Path, timeout_seconds: int = 30) -> Dict[str, Any]:
        """Runs pytest on a given target path and returns the execution results."""
        if not target_path.exists():
            return {
                "exit_code": -1,
                "passed": False,
                "output": f"Test path not found: {target_path}"
            }

        try:
            result = subprocess.run(
                ["pytest", str(target_path)],
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            return {
                "exit_code": result.returncode,
                "passed": result.returncode == 0,
                "output": result.stdout + "\n" + result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "exit_code": -999,
                "passed": False,
                "output": f"Execution timed out after {timeout_seconds} seconds."
            }
        except Exception as e:
            return {
                "exit_code": -500,
                "passed": False,
                "output": f"Infrastructure execution error: {str(e)}"
            }
