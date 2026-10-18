"""
PatchProof Task Schema Definition
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TaskMetadata(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the task")
    title: str = Field(..., description="Concise title of the defect")
    difficulty: str = Field(..., description="Difficulty classification")
    author: str = Field(..., description="Creator or provenance source")
    created_at: str = Field(..., description="Creation date or version tag")


class TaskSpecification(BaseModel):
    metadata: TaskMetadata
    problem_description: str = Field(..., description="Defect explanation and expected behavior")
    workspace_files: List[str] = Field(default_factory=list, description="Workspace file paths")
    public_tests: List[str] = Field(default_factory=list, description="Candidate-visible tests")
    holdout_tests: List[str] = Field(default_factory=list, description="Private evaluation tests")
    anti_gaming_rules: Dict[str, Any] = Field(default_factory=dict, description="Rules to detect test deletion/tampering")
    scoring_rubric: Dict[str, float] = Field(default_factory=dict, description="Weighting guidelines")
    known_limitations: Optional[str] = Field(None, description="Documented limitations")
