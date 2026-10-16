"""Data schema for PatchProof repair tasks.

A *task* describes one software-repair problem. It has four logical parts:

* **Metadata**      - identity and classification of the task.
* **Problem**       - the human-readable bug report shown to the repair agent.
* **Public tests**  - tests the agent may see and run while repairing.
* **Holdout tests** - tests used *only* by the evaluator to judge the final
  patch. They must never be exposed to the agent, otherwise the agent could
  overfit to them.

Design notes
------------
* All models are frozen and forbid unknown fields, so a typo in a task file
  fails loudly instead of being silently ignored.
* Test selection follows the common "fail-to-pass / pass-to-pass" convention:
  ``fail_to_pass`` tests fail before a correct patch and pass after it;
  ``pass_to_pass`` tests pass both before and after (regression guards).
* Test identifiers are pytest node IDs, e.g. ``tests/test_calc.py::test_add``.
* :meth:`Task.agent_view` is the only supported way to hand a task to a repair
  agent; it structurally omits the holdout tests.
"""

from __future__ import annotations

from enum import Enum
from pathlib import PurePosixPath
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

__all__ = [
    "SCHEMA_VERSION",
    "AgentTaskView",
    "Difficulty",
    "Language",
    "ProblemDescription",
    "Task",
    "TaskMetadata",
    "TestFile",
    "TestSuite",
]

#: Bump when a backwards-incompatible change is made to any model below.
SCHEMA_VERSION: Literal["1"] = "1"


# ---------------------------------------------------------------------------
# Validators and reusable constrained types
# ---------------------------------------------------------------------------


def _validate_relative_posix_path(value: str) -> str:
    """Ensure ``value`` is a safe, relative, POSIX-style file path.

    Task files are later written to disk inside a sandbox, so we reject
    anything that could escape it (absolute paths, ``..`` segments) as well
    as Windows-style separators, which would make task files non-portable.
    """
    if "\\" in value:
        raise ValueError("path must use forward slashes ('/') only")
    path = PurePosixPath(value)
    if path.is_absolute():
        raise ValueError("path must be relative, not absolute")
    if any(part in ("..", "") for part in value.split("/")):
        raise ValueError("path must not contain '..' or empty segments")
    if path.name in ("", "."):
        raise ValueError("path must point to a file")
    return value


def _validate_pytest_node_id(value: str) -> str:
    """Ensure ``value`` looks like ``relative/path.py::test_name[::more]``."""
    file_part, sep, test_part = value.partition("::")
    if not sep or not test_part.strip():
        raise ValueError("node id must have the form 'path/to/test_file.py::test_name'")
    if not file_part.endswith(".py"):
        raise ValueError("node id must reference a Python file (ending in '.py')")
    _validate_relative_posix_path(file_part)
    return value


#: Lowercase slug used for task identifiers, e.g. ``off-by-one-pagination``.
TaskId = Annotated[
    str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9_-]{2,63}$")
]

#: A non-empty string with surrounding whitespace removed.
NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

RelativePosixPath = Annotated[str, AfterValidator(_validate_relative_posix_path)]
PytestNodeId = Annotated[str, AfterValidator(_validate_pytest_node_id)]


class _StrictModel(BaseModel):
    """Base class applying the project-wide strictness policy."""

    model_config = ConfigDict(
        extra="forbid",  # unknown fields are errors, not silently dropped
        frozen=True,  # tasks are immutable once loaded
        str_strip_whitespace=True,
        validate_default=True,
    )


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class Language(str, Enum):
    """Programming language of the code under repair."""

    PYTHON = "python"


class Difficulty(str, Enum):
    """Rough, author-assigned difficulty of the repair."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------


class TaskMetadata(_StrictModel):
    """Identity and classification of a task. Safe to show to the agent."""

    task_id: TaskId = Field(description="Unique lowercase slug identifying the task.")
    title: NonEmptyStr = Field(max_length=200, description="Short human-readable title.")
    language: Language = Language.PYTHON
    difficulty: Difficulty = Difficulty.MEDIUM
    tags: tuple[NonEmptyStr, ...] = Field(
        default=(), max_length=20, description="Free-form labels, e.g. 'off-by-one'."
    )
    author: NonEmptyStr | None = None
    license: NonEmptyStr | None = Field(
        default=None, description="SPDX identifier of the task's license, if any."
    )

    @model_validator(mode="after")
    def _tags_are_unique(self) -> TaskMetadata:
        if len(set(self.tags)) != len(self.tags):
            raise ValueError("tags must be unique")
        return self


class ProblemDescription(_StrictModel):
    """The bug report presented to the repair agent."""

    summary: NonEmptyStr = Field(max_length=500, description="One-paragraph statement of the bug.")
    details: NonEmptyStr | None = Field(
        default=None, description="Optional extended description (Markdown)."
    )
    expected_behavior: NonEmptyStr | None = None
    observed_behavior: NonEmptyStr | None = None
    reproduction_steps: tuple[NonEmptyStr, ...] = Field(default=(), max_length=50)


class TestFile(_StrictModel):
    """A single test source file, stored inline with its repo-relative path."""

    # Prevent pytest from trying to collect this model as a test class.
    __test__ = False

    path: RelativePosixPath = Field(description="Repo-relative POSIX path, e.g. 'tests/test_x.py'.")
    content: str = Field(max_length=200_000, description="Full source text of the test file.")


class TestSuite(_StrictModel):
    """A set of test files plus the outcomes expected from them."""

    # Prevent pytest from trying to collect this model as a test class.
    __test__ = False

    files: tuple[TestFile, ...] = Field(min_length=1)
    fail_to_pass: tuple[PytestNodeId, ...] = Field(
        min_length=1,
        description="Tests that fail on the buggy code and must pass after a correct patch.",
    )
    pass_to_pass: tuple[PytestNodeId, ...] = Field(
        default=(),
        description="Tests that pass before and must still pass after the patch (regressions).",
    )

    @property
    def paths(self) -> frozenset[str]:
        """All file paths contained in this suite."""
        return frozenset(f.path for f in self.files)

    @property
    def node_ids(self) -> frozenset[str]:
        """Every test node id selected by this suite."""
        return frozenset((*self.fail_to_pass, *self.pass_to_pass))

    @model_validator(mode="after")
    def _check_consistency(self) -> TestSuite:
        paths = [f.path for f in self.files]
        if len(set(paths)) != len(paths):
            raise ValueError("duplicate file paths in test suite")

        all_ids = (*self.fail_to_pass, *self.pass_to_pass)
        if len(set(all_ids)) != len(all_ids):
            raise ValueError(
                "test node ids must be unique across fail_to_pass and pass_to_pass"
            )

        # Every selected test must live in one of the files we actually ship.
        known = set(paths)
        for node_id in all_ids:
            file_part = node_id.partition("::")[0]
            if file_part not in known:
                raise ValueError(f"node id {node_id!r} references unknown file {file_part!r}")
        return self


# ---------------------------------------------------------------------------
# Top-level models
# ---------------------------------------------------------------------------


class Task(_StrictModel):
    """A complete repair task, including evaluator-only holdout tests.

    Never pass a :class:`Task` directly to a repair agent; call
    :meth:`agent_view` instead.
    """

    schema_version: Literal["1"] = SCHEMA_VERSION
    metadata: TaskMetadata
    problem: ProblemDescription
    public_tests: TestSuite = Field(description="Visible to the agent during repair.")
    holdout_tests: TestSuite = Field(
        description="Evaluator-only tests. Must never be shown to the agent."
    )

    @model_validator(mode="after")
    def _holdout_is_disjoint_from_public(self) -> Task:
        """Keep public and holdout tests fully separate.

        Shared file paths could let public files overwrite holdout files (or
        vice versa) when materialised in one working tree, and shared node
        ids would make the holdout signal meaningless.
        """
        shared_paths = self.public_tests.paths & self.holdout_tests.paths
        if shared_paths:
            raise ValueError(
                f"public and holdout tests must not share files: {sorted(shared_paths)}"
            )
        shared_ids = self.public_tests.node_ids & self.holdout_tests.node_ids
        if shared_ids:
            raise ValueError(
                f"public and holdout tests must not share node ids: {sorted(shared_ids)}"
            )
        return self

    def agent_view(self) -> AgentTaskView:
        """Return the sanitised view of this task that a repair agent may see."""
        return AgentTaskView(
            metadata=self.metadata,
            problem=self.problem,
            public_tests=self.public_tests,
        )


class AgentTaskView(_StrictModel):
    """The subset of a :class:`Task` that is safe to expose to a repair agent.

    Holdout tests are omitted *structurally* (the field does not exist), so
    they cannot leak through serialisation by accident.
    """

    metadata: TaskMetadata
    problem: ProblemDescription
    public_tests: TestSuite
