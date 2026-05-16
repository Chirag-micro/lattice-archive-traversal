# Environment Interface

## Observation space

- Files under `repo/`
- `prompt.txt`
- Shell output from search, pytest, and patch commands

## Action space

- Read files
- Search code
- Edit files under `/repo`
- Run shell commands
- Run pytest
- Apply patches

## Episode start

- Container starts with the vulnerable repository snapshot checked out at `/repo`
- Hidden tests are not present in the image
- The agent receives only `prompt.txt`

## Deterministic verifier

- Apply `test_patch.diff`
- Run the configured hidden tests against the broken snapshot
- Apply `gold_patch.diff`
- Re-run the same hidden tests against the fixed snapshot

## Success condition

- Broken snapshot: all `FAIL_TO_PASS` tests fail and all `PASS_TO_PASS` tests pass
- Fixed snapshot: all hidden tests pass
