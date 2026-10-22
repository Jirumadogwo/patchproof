"""Execute trusted local test suites; this subprocess runner is not a security sandbox."""
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict


class PatchEvaluator:
    def __init__(self, task_dir: Path | None = None, timeout: int = 30):
        self.task_dir = Path(task_dir or ".").resolve()
        self.workspace_dir = self.task_dir / "workspace"
        self.tests_dir = self.task_dir / "tests"
        self.timeout = timeout

    def run_pytest(self, target_path: Path, timeout_seconds: int = 30) -> Dict[str, Any]:
        target_path = Path(target_path).resolve()
        if not target_path.exists():
            return {"exit_code": -1, "passed": False, "output": f"Test path not found: {target_path}"}
        env = {**os.environ, "PYTHONPATH": str(self.task_dir) + os.pathsep + os.environ.get("PYTHONPATH", ""),
               "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        env.pop("PYTEST_ADDOPTS", None)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(target_path), "-v", "--tb=short"],
                cwd=self.task_dir, env=env, capture_output=True, text=True, timeout=timeout_seconds,
            )
            return {"exit_code": result.returncode, "passed": result.returncode == 0,
                    "stdout": result.stdout, "stderr": result.stderr,
                    "output": result.stdout + "\n" + result.stderr}
        except subprocess.TimeoutExpired:
            return {"exit_code": -999, "passed": False,
                    "output": f"Execution timed out after {timeout_seconds} seconds."}
        except OSError as error:
            return {"exit_code": -500, "passed": False,
                    "output": f"Infrastructure execution error: {error}"}

    def run_tests(self, test_path: Path) -> Dict[str, Any]:
        start = time.monotonic()
        result = self.run_pytest(test_path, self.timeout)
        return {"returncode": result["exit_code"], "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", result["output"]),
                "duration_ms": int((time.monotonic() - start) * 1000)}
