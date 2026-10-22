"""
PatchProof Command Line Interface (CLI)
Provides simple commands to interact with the PatchProof evaluation engine.
"""

import argparse
import sys
from pathlib import Path
from patchproof.loader import TaskLoader
from patchproof.scoring import ResultClassifier, ResultStatus


def main():
    parser = argparse.ArgumentParser(description="PatchProof: Software-Repair Evaluation Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Validate task command
    validate_parser = subparsers.add_parser("validate-task", help="Validate a task directory specification")
    validate_parser.add_argument("task_dir", type=str, help="Path to the task directory")

    args = parser.parse_args()

    if args.command == "validate-task":
        task_path = Path(args.task_dir)
        print(f"Validating task at: {task_path}...")
        try:
            task_spec = TaskLoader.load_task_from_dir(task_path)
            print(f"[SUCCESS] Task '{task_spec.metadata.task_id}' is valid!")
            print(f"Title: {task_spec.metadata.title}")
            print(f"Difficulty: {task_spec.metadata.difficulty}")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Task validation failed: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
