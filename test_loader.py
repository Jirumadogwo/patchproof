"""
Unit tests for PatchProof Task Loader
"""

import pytest
from pathlib import Path
from patchproof.loader import TaskLoader


def test_task_loader_initialization():
    loader = TaskLoader(tasks_root="tasks")
    assert isinstance(loader.tasks_root, Path)
