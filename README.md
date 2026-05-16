# Lattice Archive Traversal Task

This directory contains a from-scratch Python vulnerability-remediation task in
the Realm Shield bundle format.

## Task summary

- Vulnerability family: path traversal / file inclusion boundary bypass (`CWE-22`)
- Language: Python
- Repository shape: layered bundle portal code under `repo/src/lattice_archive`
- Hidden test split: 4 `FAIL_TO_PASS`, 7 `PASS_TO_PASS`

## Behavioral prompt

The agent-visible prompt is `prompt.txt`. It describes symptoms only:

- copied bundle file names can return files outside the intended shared export
- reused names can surface drafts or files from another workspace
- inaccessible file names should remain indistinguishable from unknown ones

It intentionally avoids file paths, implementation names, and vulnerability
labels.

## Canonical artifacts

- `repo/`: vulnerable repository snapshot
- `docker/Dockerfile`: task image definition tailored to this repo
- `test_patch.diff`: hidden tests only, added in a brand-new test file
- `gold_patch.diff`: production-code-only remediation patch
- `task_config.json`: metadata, hidden test IDs, and verifier wiring
- `grader/grade.py`: deterministic verifier
- `run_tests.sh`: local verifier entrypoint
- `annotations/`: attack vector, root cause, fix rationale, alternatives
- `reviews/`: peer review and sign-off notes

## Hidden test contract

Broken snapshot expectations after applying `test_patch.diff`:

- the 4 exploit-confirming tests fail
- the 7 regression tests pass

Fixed snapshot expectations after applying both patches:

- all 11 hidden tests pass

## Validation notes

The vulnerable and fixed states were sanity-checked with direct runtime
assertions during authoring and then validated end to end through the
Docker-backed verifier in `grader/grade.py`.
