"""
PatchProof Command Line Interface Entrypoint
"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="PatchProof Software Repair Evaluator")
    parser.add_argument("--task", type=str, required=True, help="Task ID to evaluate")
    parser.add_argument("--model", type=str, default="agent-v1", help="Model name identifier")
    args = parser.parse_args()

    print(f"Running PatchProof evaluation for task: {args.task} with model: {args.model}")
    sys.exit(0)

if __name__ == "__main__":
    main()
