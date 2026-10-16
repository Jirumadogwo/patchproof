"""
Integration tests for PatchProof TaskLoader and evaluator runner.
Verifies that tasks load correctly and the test runner executes properly.
"""

import pytest
from pathlib import Path
from patchproof.loader import TaskLoader
from patchproof.evaluator import PatchEvaluator


def test_load_task_001():
    """Test loading task_001_string_reverser specification."""
    task_dir = Path("tasks/public/task_001_string_reverser")
    if not (task_dir / "task.json").exists():
        pytest.skip("Task 1 directory not found locally.")
    
    spec = TaskLoader.load_task_from_dir(task_dir)
    assert spec.metadata.task_id == "task_001_string_reverser"
    assert len(spec.workspace_files) > 0


def test_evaluator_runs_pytest():
    """Test running pytest via PatchEvaluator on task 1 public tests."""
    task_dir = Path("tasks/public/task_001_string_reverser")
    test_file = task_dir / "tests" / "public_test_string.py"
    
    if not test_file.exists():
        pytest.skip("Public test file not found.")
        
    evaluator = PatchEvaluator(task_dir)
    # Run pytest on the flawed starter code (should fail public tests initially)
    result = evaluator.run_pytest(test_file)
    # The starter code is intentionally flawed, so pytest should detect failures (non-zero exit code)
    assert result["exit_code"] != 0
