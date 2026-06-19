# Acceptance Test Plan

## Purpose
This document shows that features were actually verified to work, not just
implemented. It also tracks bugs that were found along the way and whether
they were fixed.

## How to fill this out
Add one row per feature or major component. Update "Result" once tested, and
note any bugs found (even minor ones) in the "Bugs found / fixed" column.

| Feature | How it was tested | Result | Bugs found / fixed |
|---|---|---|---|
| Hybrid retrieval (BM25 + dense) | Ran moulinette evaluator on test queries | Pass — Recall@5 = 0.81 | None |
| Query rewriting (Qwen3-0.6B) | Manual spot-check on 10 sample queries | Pass | Stemmer broke on accented characters — fixed in commit abc123 |

## Notes
- "Tested" can mean automated tests, manual checks, or evaluator scripts —
  just say which.
- Don't only log passing tests — bugs you found and fixed are good evidence
  too, they show the process worked.
- If something fails and isn't fixed by the deadline, say so honestly and
  note why (time constraint, blocked by another issue, etc.).
