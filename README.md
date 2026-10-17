# PatchProof

**Original Software-Repair Evaluation Toolkit for AI Coding Agents**

PatchProof is a modular Python-based evaluation toolkit designed to test whether AI coding agents genuinely fix software defects without introducing regressions, hard-coding answers, or manipulating test suites.

## Features
- **Strict Schema Validation:** Pydantic-powered task specifications.
- **Multi-Tiered Testing:** Supports public candidate tests, private evaluator holdout tests, and regression checks.
- **Result Classification:** Explicit result statuses (`SUCCESS`, `PARTIAL`, `REGRESSION`, `INVALID_PATCH`, `TEST_FAILURE`, `INFRASTRUCTURE_FAILURE`, etc.).
- **Automated CI:** Built-in GitHub Actions workflow running `pytest` test suites.

## Installation

Clone the repository and install it in editable mode with development dependencies:

```bash
git clone [https://github.com/jirumadogwo/patchproof.git](https://github.com/jirumadogwo/patchproof.git)
cd patchproof
pip install -e .[dev]

