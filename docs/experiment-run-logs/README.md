# Experiment run-log retention

Checkpoint: accepted C215 / 2026-09-22.

Each formal run publishes:

```text
docs/experiment-run-logs/c###/latest.json
docs/experiment-run-logs/c###/latest.log
```

## Retention policy

For a **closed** experiment:

- keep `latest.json` in the working tree as the compact execution receipt;
- the full `latest.log` may be pruned after the formal verdict is recorded in the ledger/handoff;
- the pruned full log remains recoverable from Git history.

At the C215 maintenance checkpoint, two full logs remain intentionally resident:

- C212 — decisive Gate E holdout / `GATE_E_PASSED`;
- C215 — latest accepted V5-F maintenance checkpoint.

Full logs for closed C189-C211 and C213-C214 are removed from the current working tree. Their
`latest.json` receipts remain.

## Recovering a pruned log

```powershell
git log --all -- docs/experiment-run-logs/c210/latest.log
git show <log-commit>:docs/experiment-run-logs/c210/latest.log
```

The ledger/addenda retain scientific execution HEADs, published log commit IDs when relevant,
log SHA256 values, summary SHA256 values, formal dispositions, and deciding metrics.

## Active-run rule

Never prune or rewrite the log path of an ACTIVE experiment. Log cleanup happens only after a
formal accepted/valid-negative/invalid-recovery disposition has been recorded and the experiment is
no longer running.

This policy only removes redundant working-tree copies. It is not a Git-history rewrite and does
not reduce historical pack storage already present in `.git`.
