# Experiment harness maintenance

Checkpoint: accepted C215 / 2026-09-22.

The experiment harness is intentionally split into **live/shared infrastructure**, **source-pinned
replay files**, and **historical files recoverable from Git history**.

## Live/shared infrastructure

Keep these at stable paths:

- `tools/invoke_active.ps1` — user-facing active-experiment dispatcher.
- `tools/publish_experiment_log.ps1` — publishes the latest execution receipt/log.

Users should normally call `invoke_active.ps1`; they should not choose a historical C-numbered
launcher manually.

## Source-pinned replay set at the C215 checkpoint

The accepted C215 scientific chain pins these historical harness files, so they remain in the
working tree:

- `tools/run_c167.ps1` — historical regression seed list consumed by C176-C178 `regression_modules()`
- `tools/run_c171.ps1`
- `tools/run_c200.ps1` … `tools/run_c215.ps1`
- `tools/invoke_c200.ps1` … `tools/invoke_c215.ps1`

Do not move, rename, reformat, or delete these while descendants inherit C215 source/protection
contracts.

## Pruned from the working tree after C215

The following closed harness files are no longer part of the accepted C215 source-pinned set and
are removed from the current working tree to reduce clutter:

- `tools/run_c143.ps1` … `tools/run_c166.ps1`
- `tools/run_c168.ps1` … `tools/run_c170.ps1`
- `tools/run_c172.ps1` … `tools/run_c199.ps1`
- `tools/invoke_c189.ps1` … `tools/invoke_c199.ps1`

They are **not erased from Git history**. For forensic replay:

```powershell
git log --all -- tools/run_c199.ps1
git show <commit>:tools/run_c199.ps1
```

## Maintenance rule for future checkpoints

After a formal accepted checkpoint:

1. determine the exact source-pinned/protected harness set from the accepted summary;
2. never prune a file in that set;
3. inspect historical `regression_modules()` builders and any source-level loader/parser logic for direct file reads;
4. keep any file required to reconstruct the historical regression module list, even when it is not in scientific `source_blobs`;
5. retain shared dispatcher/publisher infrastructure;
6. prune only closed, unpinned, regression-unreferenced C-numbered harness files;
7. record the maintenance commit in the authoritative handoff.

This is a working-tree cleanup policy, not a Git-history rewrite. It therefore improves navigation
and checkout clutter but does not retroactively remove old blob storage from `.git`.


## C216 maintenance correction

The first C216 attempt exposed a missed historical dependency:

`fold_lm/v05_benchmarks/gate_e_c176_conditional_loss.py`,
`gate_e_c177_frozen_score_order.py`, and
`gate_e_c178_visible_leaf_binding.py` read `tools/run_c167.ps1` to reconstruct the immutable
51-module regression seed list.

`tools/run_c167.ps1` was restored from exact Git blob
`7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789` and is now protected by the C216 recovery contract.

Lesson: accepted scientific source pins are necessary but not sufficient for harness cleanup;
regression-construction dependencies must also be audited.
