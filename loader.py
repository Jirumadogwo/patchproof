"""
PatchProof Task Loader Module
"""

import json
from pathlib import Path
from patchproof.schema import TaskSpecification


class TaskLoader:
    def __init__(self, tasks_root: str = "tasks"):
        self.tasks_root = Path(tasks_root)

    def load_task(self, task_id: str) -> TaskSpecification:
        task_dir = self.tasks_root / "public" / task_id
        config_path = task_dir / "task.json"

        if not config_path.exists():
            raise FileNotFoundError(f"Task configuration not found at {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return TaskSpecification(**data)
