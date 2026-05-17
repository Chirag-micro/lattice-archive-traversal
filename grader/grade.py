from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT / "repo"
TASK_CONFIG = ROOT / "task_config.json"
IGNORE_PATTERNS = shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__")


def load_config() -> dict[str, Any]:
    with TASK_CONFIG.open(encoding="utf-8") as fh:
        return json.load(fh)


def build_env(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    pythonpath = str(repo_root / "src")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = pythonpath if not existing else f"{pythonpath}{os.pathsep}{existing}"
    return env


def python_executable() -> str:
    configured = os.environ.get("PYTHON")
    if configured:
        return configured

    for candidate in (
        ROOT / ".venv" / "bin" / "python",
        ROOT / ".venv" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate)

    return sys.executable


def apply_patch(repo_root: Path, patch_path: Path) -> None:
    commands = [
        ["git", "apply", "--whitespace=nowarn", str(patch_path)],
        ["patch", "-p1", "-i", str(patch_path)],
    ]
    failures: list[str] = []
    for command in commands:
        try:
            process = subprocess.run(
                command,
                cwd=repo_root,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            failures.append(f"command: {' '.join(command)}\nerror:\n{exc}")
            continue
        if process.returncode == 0:
            return
        failures.append(
            f"command: {' '.join(command)}\nstdout:\n{process.stdout}\n\nstderr:\n{process.stderr}"
        )
    raise RuntimeError(f"failed to apply patch {patch_path.name}\n\n" + "\n\n".join(failures))


def run_test(repo_root: Path, test_id: str) -> dict[str, Any]:
    process = subprocess.run(
        [python_executable(), "-m", "pytest", test_id, "-q"],
        cwd=repo_root,
        env=build_env(repo_root),
        capture_output=True,
        text=True,
    )
    return {
        "test_id": test_id,
        "returncode": process.returncode,
        "stdout": process.stdout.strip(),
        "stderr": process.stderr.strip(),
    }


def evaluate_vulnerable(repo_root: Path, fail_to_pass: list[str], pass_to_pass: list[str]) -> dict[str, Any]:
    failing = [run_test(repo_root, test_id) for test_id in fail_to_pass]
    passing = [run_test(repo_root, test_id) for test_id in pass_to_pass]
    return {
        "FAIL_TO_PASS": failing,
        "PASS_TO_PASS": passing,
        "passed": all(item["returncode"] != 0 for item in failing)
        and all(item["returncode"] == 0 for item in passing),
    }


def evaluate_fixed(repo_root: Path, all_tests: list[str]) -> dict[str, Any]:
    results = [run_test(repo_root, test_id) for test_id in all_tests]
    return {
        "all_tests": results,
        "passed": all(item["returncode"] == 0 for item in results),
    }


def copy_repo() -> tempfile.TemporaryDirectory[str]:
    tempdir = tempfile.TemporaryDirectory()
    workspace = Path(tempdir.name) / "repo"
    shutil.copytree(REPO_ROOT, workspace, ignore=IGNORE_PATTERNS)
    return tempdir


def main() -> int:
    config = load_config()
    parser = argparse.ArgumentParser(description="Grade the Lattice Archive traversal task.")
    parser.add_argument("--mode", choices=("vulnerable", "fixed", "both"), default="both")
    args = parser.parse_args()

    fail_to_pass = config["FAIL_TO_PASS"]
    pass_to_pass = config["PASS_TO_PASS"]
    all_hidden = fail_to_pass + pass_to_pass
    results: dict[str, Any] = {"mode": args.mode}
    overall_pass = True

    if args.mode in {"vulnerable", "both"}:
        tempdir = copy_repo()
        try:
            repo_root = Path(tempdir.name) / "repo"
            apply_patch(repo_root, ROOT / config["hidden_test_patch"])
            vulnerable = evaluate_vulnerable(repo_root, fail_to_pass, pass_to_pass)
        finally:
            tempdir.cleanup()
        results["vulnerable"] = vulnerable
        overall_pass = overall_pass and vulnerable["passed"]

    if args.mode in {"fixed", "both"}:
        tempdir = copy_repo()
        try:
            repo_root = Path(tempdir.name) / "repo"
            apply_patch(repo_root, ROOT / config["hidden_test_patch"])
            apply_patch(repo_root, ROOT / config["golden_patch"])
            fixed = evaluate_fixed(repo_root, all_hidden)
        finally:
            tempdir.cleanup()
        results["fixed"] = fixed
        overall_pass = overall_pass and fixed["passed"]

    print(json.dumps(results, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
