"""
PatchProof Task Loader
Responsible for discovering, loading, and validating task specifications from the filesystem.
"""

import json
from pathlib import Path
from typing import Dict, Any
from patchproof.schema import TaskSpecification


class TaskLoader:
    """Loads and validates PatchProof tasks from disk."""

    @staticmethod
    def load_task_from_dir(task_dir: Path) -> TaskSpecification:
        """
        Loads a task specification from a given directory path.
        Expects a 'task.json' file inside the directory.
        """
        task_json_path = task_dir / "task.json"
        if not task_json_path.exists():
            raise FileNotFoundError(f"Task configuration not found at: {task_json_path}")

        try:
            with open(task_json_path, "r", encoding="utf-8") as f:
                raw_data: Dict[str, Any] = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in task configuration {task_json_path}: {e}")

        # Validate and parse data using our Pydantic TaskSpecification schema
        task_spec = TaskSpecification(**raw_data)
        return task_spec
