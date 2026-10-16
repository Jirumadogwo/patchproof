"""
PatchProof Package Initialization
Exposes core classes and package version.
"""

__version__ = "0.1.0"

from patchproof.schema import TaskSpecification, TaskMetadata
from patchproof.loader import TaskLoader
from patchproof.evaluator import PatchEvaluator
from patchproof.scoring import ResultClassifier, ResultStatus
