"""Verify real task loading and candidate/reference evaluation with no skips."""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from patchproof.loader import TaskLoader
from patchproof.evaluator import PatchEvaluator

ROOT = Path(__file__).resolve().parents[2]
TASKS = [("task_001_string_reverser", "string_utils", "public_test_string.py"),
         ("task_002_list_deduplicator", "list_utils", "public_test_list.py")]


@pytest.mark.parametrize("task,module,public", TASKS)
def test_task_files_exist(task, module, public):
    task_dir = ROOT / "tasks/public" / task
    spec = TaskLoader(tasks_root=str(ROOT / "tasks")).load_task(task)
    assert spec.metadata.task_id == task
    for path in spec.workspace_files + spec.public_tests + spec.holdout_tests:
        assert (task_dir / path).is_file(), path


@pytest.mark.parametrize("task,module,public", TASKS)
def test_buggy_candidate_fails_and_reference_passes(task, module, public, tmp_path):
    candidate = tmp_path / task
    shutil.copytree(ROOT / "tasks/public" / task / "workspace", candidate / "workspace")
    suites = candidate / "tests"
    shutil.copytree(ROOT / "tests/unit/benchmarks" / task, suites)
    evaluator = PatchEvaluator(candidate)
    result = evaluator.run_pytest(suites / public)
    assert result["exit_code"] == 1, result["output"]
    shutil.copy2(ROOT / "tasks/evaluator_private" / task / "reference_solution.py",
                 candidate / "workspace" / f"{module}.py")
    shutil.rmtree(candidate / "workspace/__pycache__", ignore_errors=True)
    for test in sorted(suites.glob("*_test_*.py")):
        result = evaluator.run_pytest(test)
        assert result["exit_code"] == 0, result["output"]


@pytest.mark.parametrize("task,module,public", TASKS)
def test_cli_validates_restored_task(task, module, public):
    result = subprocess.run([sys.executable, "-m", "patchproof.cli", "validate-task",
                             str(ROOT / "tasks/public" / task)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert task in result.stdout


def test_missing_test_is_not_success(tmp_path):
    result = PatchEvaluator(tmp_path).run_pytest(tmp_path / "missing.py")
    assert result["exit_code"] == -1
    assert result["passed"] is False
