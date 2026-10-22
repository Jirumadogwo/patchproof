"""
PatchProof Task Schema Definition
Defines strict Pydantic data models for loading, validating, and managing software-repair tasks.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TaskMetadata(BaseModel):
    """Metadata describing a specific software-repair task."""
    task_id: str = Field(..., description="Unique identifier for the task, e.g., task_001_string_reverser")
    title: str = Field(..., description="Concise title of the software defect")
    difficulty: str = Field(..., description="Difficulty classification (e.g., Easy, Medium, Hard)")
    author: str = Field(..., description="Creator or provenance source")
    created_at: str = Field(..., description="Creation date or version tag")


class TaskSpecification(BaseModel):
    """Complete specification for a PatchProof evaluation task."""
    metadata: TaskMetadata
    problem_description: str = Field(..., description="Detailed explanation of the reported defect and expected behavior")
    workspace_files: List[str] = Field(default_factory=list, description="List of relative file paths provided in the candidate workspace")
    public_tests: List[str] = Field(default_factory=list, description="Test files visible to the candidate agent")
    holdout_tests: List[str] = Field(default_factory=list, description="Private evaluation test files hidden from the candidate agent")
    anti_gaming_rules: Dict[str, Any] = Field(default_factory=dict, description="Rules to detect test deletion, hardcoding, or tampering")
    scoring_rubric: Dict[str, float] = Field(default_factory=dict, description="Weighting guidelines for public, holdout, and regression tests")
    known_limitations: Optional[str] = Field(None, description="Documented assumptions, environment constraints, or edge cases")
