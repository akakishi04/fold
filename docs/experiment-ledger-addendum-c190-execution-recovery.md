# C190 execution recovery — full-cohort guard

## Formal status

**C190 remains ACTIVE / NOT YET JUDGED.**
First C190 attempt is **INVALID EXECUTION / RETRY SAME C190**.
C191 remains NOT REGISTERED. Gate E remains NOT PASSED.

Invalid attempt:
- scientific execution HEAD: `e0e47b44dbda4a5a4ad470f42911d4ce2687e587`
- published log commit: `8ec5932922231f0f88478bd12c5d3de89f104df7`
- log SHA256: `c875c9fab740753903636a6d9557c621ba85c8655fdd71deb47efb102e2943d6`
- log bytes: 242123
- source/artifact precheck: PASS
- focused regression: **1485/1485 PASS**, 44.696s
- benchmark model work: not started
- failure: `ValueError: C190 cohort drift`

Cause:
C188 `cohort_masks` reports `profile["eval_m2"] = 376` and
`profile["eval_m3"] = 152` for the **discriminating primary subset**, while C190
incorrectly treated those fields as the full multi-missing cohort counts 1152/616.

The actual full C190 mask `evfull` was already the correct 1768-row cohort.
Recovery changes only the runtime guard:
- full cohort counts are checked directly from `miss[evfull]`: 1152 missing2 / 616 missing3;
- inherited discriminating profile is separately checked as 528 total = 376/152.

Unchanged:
- C190 experiment ID/stage;
- manifest object and SHA;
- seeds/checkpoints;
- 1768-row cohort and coherent-world expansion;
- 9536 episodes/selector / 85824 total;
- two-acquisition maximum;
- scoring teachers;
- source snapshots;
- fixed gate / thresholds / interpretation.

This is implementation validity recovery only, not scientific evidence.
Retry SAME C190.
