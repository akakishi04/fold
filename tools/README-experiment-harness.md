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

- `tools/run_c171.ps1`
- `tools/run_c200.ps1` … `tools/run_c215.ps1`
- `tools/invoke_c200.ps1` … `tools/invoke_c215.ps1`

Do not move, rename, reformat, or delete these while descendants inherit C215 source/protection
contracts.

## Pruned from the working tree after C215

The following closed harness files are no longer part of the accepted C215 source-pinned set and
are removed from the current working tree to reduce clutter:

- `tools/run_c143.ps1` … `tools/run_c170.ps1`
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
3. verify historical regression does not require a candidate file at its repository path;
4. retain shared dispatcher/publisher infrastructure;
5. prune only closed, unpinned C-numbered harness files;
6. record the maintenance commit in the authoritative handoff.

This is a working-tree cleanup policy, not a Git-history rewrite. It therefore improves navigation
and checkout clutter but does not retroactively remove old blob storage from `.git`.
