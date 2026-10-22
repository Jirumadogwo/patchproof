"""
Unit tests for PatchProof TaskSpecification schema.
"""

import pytest
from patchproof.schema import TaskMetadata, TaskSpecification


def test_task_metadata_valid():
    """Test that valid metadata parses correctly."""
    meta = TaskMetadata(
        task_id="task_001_sample",
        title="Sample Bug Fix",
        difficulty="Easy",
        author="Jiruma Dogwo",
        created_at="2026-10-16"
    )
    assert meta.task_id == "task_001_sample"
    assert meta.difficulty == "Easy"


def test_task_specification_minimal():
    """Test building a minimal task specification."""
    meta = TaskMetadata(
        task_id="task_002_sample",
        title="Another Bug",
        difficulty="Medium",
        author="Jiruma Dogwo",
        created_at="2026-10-16"
    )
    spec = TaskSpecification(
        metadata=meta,
        problem_description="Fix the string reverser bug."
    )
    assert spec.metadata.task_id == "task_002_sample"
    assert spec.workspace_files == []
    assert spec.public_tests == []
