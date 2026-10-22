"""
Unit tests for PatchProof Task Schema
"""

import pytest
from patchproof.schema import TaskSpecification, TaskMetadata


def test_task_metadata_creation():
    metadata = TaskMetadata(
        task_id="task_001",
        title="String Reverser",
        difficulty="Easy",
        author="System",
        created_at="2026-10-18"
    )
    assert metadata.task_id == "task_001"
    assert metadata.difficulty == "Easy"


def test_task_specification_defaults():
    metadata = TaskMetadata(
        task_id="task_002",
        title="List Deduplicator",
        difficulty="Medium",
        author="System",
        created_at="2026-10-18"
    )
    spec = TaskSpecification(
        metadata=metadata,
        problem_description="Deduplicate a list while preserving order."
    )
    assert spec.metadata.task_id == "task_002"
    assert spec.workspace_files == []
    assert spec.public_tests == []
