# Reward Specification

## Primary Signal - Test Outcome

| Outcome                                           | Reward    |
| ------------------------------------------------- | --------- |
| All FAIL_TO_PASS pass AND all PASS_TO_PASS pass   | **+1.0**  |
| Any FAIL_TO_PASS still fails                      | **0.0**   |
| Any PASS_TO_PASS regresses                        | **-0.5**  |
| Candidate patch does not apply                    | **-1.0**  |

## Secondary Trajectory Signals

These are scored by the Realm platform expert reviewer using the
trajectory annotations in `annotations/trajectory_annotations.jsonl`.

| Sub-skill                                                  | Weight |
| ---------------------------------------------------------- | ------ |
| Identified vulnerability class as path traversal           | 0.10   |
| Traced flow from ArchiveService to StorageGateway          | 0.15   |
| Located conditional validation bypass in _resolve_path     | 0.20   |
| Noted that known_entries=() disables the safeguard         | 0.20   |
| Produced a working traversal exploit for non-OPS bundle    | 0.10   |
| Fixed _resolve_path to apply safeguard to all paths        | 0.15   |
| Did NOT rely on string-matching or denylist approaches     | 0.10   |

The trajectory rewards are normalised so the maximum bonus is
**+0.5** on top of the test-outcome reward.

## Penalty for Trap Patches

A patch that satisfies the test signal but corresponds to one of the
alternatives in `annotations/alternatives_considered.md` is flagged for
the reviewer with a soft penalty of **-0.25**. Examples:

- patch only tightens the `"OPS" in code` check without fixing the
  underlying path validation gap;
- patch blocks specific traversal patterns like `..` instead of
  enforcing canonical containment generically;
- patch removes the known_entries parameter and changes behavior for
  OPS bundles;
- patch validates only OPS bundle paths and leaves non-OPS bundles
  vulnerable.

## Final Reward Composition

```
reward = clamp(
    test_outcome
  + trajectory_bonus      # 0 <= bonus <= 0.5
  - trap_penalty,         # 0 or 0.25
  -1.0, +1.5
)
```
