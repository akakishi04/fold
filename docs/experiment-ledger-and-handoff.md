# FOLD Experiment Ledger and Handoff

> Authoritative current state. Historical experiment detail lives in
> `docs/experiment-ledger-addendum-*.md`. Follow
> `docs/experiment-conversation-handoff-protocol.md` and `AGENTS.md`.

Repository: `akakishi04/fold`  
Branch: `feat/sft-target-loss`  
Local repository: `M:\\asobiba\\fold`  
Authoritative Python: 3.13.15 / PyTorch 2.10.0+cu130 / NumPy 2.3.5.

## Formal state

- Gate A: **PASSED**
- Gate B: **PASSED**
- Gate C: **PASSED in measured scope**
- Gate D: **PASSED in measured scope**
- Gate E: **PASSED**
- Gate F: **NOT PASSED**
- **C215 ACCEPTED PASS**
- **C216 ACTIVE / INVALID ATTEMPT RECOVERY**
- **C217 NOT REGISTERED**

C216 is the unique ACTIVE experiment.

## Gate E checkpoint

C212 formally passed Gate E.

Scientific execution HEAD:
`4d1436c1ba12721b1c802fb5d76e359b3a62841f`

Published log commit:
`3163014d0672ab8905a06c37ae6698e9ea9c80bc`

Summary SHA256:
`3685c37dd6e2c7fea92723548446b86f4ee8d068f7dd00afe3e2337f8bca8bce`

Key deciding result:
-144 independent holdout episodes /432 policy-episode evaluations;
- candidate correct128 / answered128 / wrong abstention0 / wrong answer0;
- zero-margin noninferiority versus FIXED_ACQUISITION passed overall and per-family;
- two registered strict improvements versus INTERNAL_ONLY were +80 episodes each;
- exact paired McNemar + Holm passed;
- hard-zero/output/compute rules passed.

Full resident log intentionally retained at:
`docs/experiment-run-logs/c212/latest.log`.

## Accepted V5-F chain

### C213 — memory operation contract

Scientific execution HEAD:
`f59f615b5d409400c9fc5247270a37960ffac197`

Summary SHA256:
`370ee39bcd32da4ce797ecfb21ce3b863013c788f6daaaf0fb9a10edac643b43`

Accepted claim:
ASSERT/REPLACE/RETRACT/ASSUME/END_SCOPE/QUERY semantics preserve factor identity, scope, revision and
provenance; hypotheses do not enter authoritative EvidenceState.

### C214 — memory capsule closure

Scientific execution HEAD:
`b4a020aeb006ec758e06ce1dc6d1b0ad5784e150`

Summary SHA256:
`bd7a310fc89873b4571d1748a96fa1a121d147a0617d48e2d8824d4769deb37d`

Accepted claim:
accepted C213 observed edits project into the existing fixed-port response capsule and match an
independent full-memory solve within the registered float64 tolerance. OUT_OF_SCOPE and
NUMERIC_UNSAFE remain distinct.

### C215 — H1/H2 chunk commit

Scientific execution HEAD:
`663f42ca21f977b6530e4df8709fc306c2ebd8c9`

Published log commit:
`36f5921677f274538d011c76ba34a77b8ed01ded`

Log SHA256:
`e894c0d10553c7877c410c963f0c75eb810518247f50fd7aa63ca2f8620c2d8e`

Summary SHA256:
`96b3e5b9cf465b9dea33920de095fc5d7d8e4c0cba960d64597c95fc15eda237`

Execution:
- focused regression **2149/2149**;
- source/artifact precheck PASS;
- protected inputs preserved;
- tracked tree clean;
- run_execution_valid True.

Deciding metrics:
-9 snapshots;
- status sequence:
  `SUPPORTED,HOT_REQUIRED,SUPPORTED,SUPPORTED,HOT_REQUIRED,SUPPORTED,SUPPORTED,SUPPORTED,SUPPORTED`;
- two chunk commits, both COMMITTED;
- semantic clocks unchanged across commit;
- commit readout deltas [0.0,0.0];
- final storage_epoch2;
- final semantic clocks memory6/evidence4/time3;
- final H2 factor beta only;
- operation-history entries0;
- capsule/full-reference max abs error `1.1102230246251565e-16` <= `1e-10`;
- OUT_OF_SCOPE and NUMERIC_UNSAFE controls preserved state and exposed no numeric value;
- learned Writer/Reader/Port Selector/Coverage classifier/model-forward calls0.

Accepted claim:
the deterministic H1/H2 chunk-commit boundary can move supported observed records from H1 into H2
without changing semantic clocks or readout, and committed-factor REPLACE/RETRACT can operate from
current protected-factor descriptors without replaying hidden operation history.

Non-claim:
C215 does not establish learned memory routing, natural-language memory extraction, compression
advantage, total memory-cost superiority, or Gate F.

Historical invalid C215 launcher-guard attempts are retained in:
`docs/experiment-ledger-addendum-c215-recovery.md`.

Full resident log intentionally retained at:
`docs/experiment-run-logs/c215/latest.log`.

## C215 maintenance checkpoint

Maintenance working-tree prune commit:
`44075b22bfc619ba5cf14e4c1f2efd65fd7a5c46`

Post-prune accepted-source audit:
- C215 source pins checked: **122/122**
- missing source pins: **0**
- SHA mismatches: **0**

Harness maintenance at C215:
- C-numbered invoke scripts: **27 -> 16**
- C-numbered run scripts: **73 -> 17**

Recovery note:
- `tools/run_c167.ps1` was restored after the first C216 attempt exposed it as historical regression infrastructure; it must not be pruned again.

Retained source-pinned harness:
- `tools/run_c171.ps1`
- `tools/run_c200.ps1` through `tools/run_c215.ps1`
- `tools/invoke_c200.ps1` through `tools/invoke_c215.ps1`
- shared `tools/invoke_active.ps1`
- shared `tools/publish_experiment_log.ps1`

Pruned historical harness remains recoverable from Git history.

Log retention after maintenance:
- compact `latest.json` receipts retained for **27/27** C189-C215 experiments;
- full resident logs retained only for C212 (Gate E decision) and C215 (latest checkpoint);
- resident full-log payload reduced from about **11.89 MiB** to about **1.35 MiB**;
- pruned full logs remain recoverable from Git history.

Maintenance policy:
- `tools/README-experiment-harness.md`
- `docs/experiment-run-logs/README.md`

This cleanup is not a history rewrite; old blobs still exist in Git history / pack storage.

## Current V5-F architecture boundary

Established, deterministic reference path:

```text
MemoryOp semantics
  -> H1 hot relational state
  -> fixed capability / relation-to-port mapping
  -> H2 response-capsule state
  -> SUPPORTED / HOT_REQUIRED / OUT_OF_SCOPE / NUMERIC_UNSAFE
  -> numeric readout
```

Still unestablished:
- learned Writer;
- learned Reader;
- learned Port Selector / Capsule Router;
- learned Coverage classifier;
- natural-language-to-memory operation mapping;
- end-to-end memory bytes/latency advantage versus full-history baseline;
- Gate F deciding holdout.

## Historical references

Detailed C-series history remains in:
- `docs/experiment-ledger-addendum-*.md`
- C215 recovery: `docs/experiment-ledger-addendum-c215-recovery.md`
- protocol: `docs/experiment-conversation-handoff-protocol.md`
- roadmap: `docs/development-roadmap-v0.5.md`

Pruned logs/scripts are recoverable with `git log --all -- <path>` and
`git show <commit>:<path>`.

## Active C216 — learned Reader pilot

Experiment:
`C216-v5f-learned-reader-pilot`

Stage:
`V5-F-LEARNED-READER-PILOT`

One question:
given correct H1/H2 memory and an oracle-selected memory port, can a learned Reader alone decode the
three-way semantic value on held-out alpha/beta pair compositions and remain invariant across
HOT/COMMITTED placement?

Changed variable:
- learned `fold_lm/v05/memory_reader.py` only.

Held constant:
- Writer oracle;
- Port Selector oracle;
- Coverage classifier absent;
- accepted C215 H1/H2 semantics;
- fixed numeric capsule and relation mapping;
- no language mapping.

Data:
- semantic classes [-1,0,+1];
-9 alpha/beta pair combinations;
- TRAIN6 / EVAL3 held-out pair compositions;
- HOT and COMMITTED placements;
-36 rows total,24 TRAIN,12 EVAL;
- balanced classes;
- data SHA `ab0c6da658576d12fc786ad3dfcef94f3acc063d8263dd175d67eec7af6a14eb`.

Training:
- seeds216001/216002/216003;
- Reader1->8->3,43 parameters;
- Adam lr0.02;
-400 full-batch steps per seed;
- total1200 steps /28800 examples /1215 Reader forwards.

Fixed gate per seed:
- TRAIN/EVAL/HOT/COMMITTED accuracy1.0;
- placement prediction mismatches0;
- zero-readout EVAL accuracy exactly1/3;
- checkpoint roundtrip exact.

Authoring:
- source pins130;
- protected inputs136;
- artifacts5;
- C216 tests36;
- regression modules101;
- loaded2186 / focused2185;
- historical regression dependency `tools/run_c167.ps1` blob `7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789`;
- manifest `91e8afd97d667b67f1164e87628f62b4bcf2347e2884537ec3e54c2baa6b385c`.

## Invalid C216 attempt

Scientific execution HEAD:
`8b550a92ab8db94d4a5c8ad7da7dadac1609ad6b`

Published log commit:
`c8f24d453455f97389c2e0935339e379d2a98e47`

Log SHA256:
`7efe5c61f4d8b727124e6030d6a93752bc215a96ef236ba055dda7807ab7ff62`

Failure phase:
- repository preflight PASS;
- Python syntax preflight PASS;
- accepted C215 source/artifact precheck PASS;
- focused regression failed while constructing the inherited module list;
- learned Reader pilot did not run;
- run_execution_valid False.

Root cause:
post-C215 maintenance pruned `tools/run_c167.ps1`, but historical C176-C178
`regression_modules()` reconstruct the immutable 51-module regression seed list from that file.

Formal disposition:
**C216 INVALID EXECUTION / RETRY SAME C216**.

Minimal recovery:
- restore exact historical blob
  `tools/run_c167.ps1 = 7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789`;
- register that file as a protected C216 historical-regression dependency;
- update validity accounting to130 source pins /136 protected inputs;
- keep Reader architecture, data split/hash, seeds, training workload, PASS gate and interpretation
  unchanged.

Recovery detail:
`docs/experiment-ledger-addendum-c216-recovery.md`.

## C216 recovery review

**post_authoring_recovery_review = PENDING**

Do not retry until the restored runner, inherited regression module seed list, updated130/136
accounting, manifest and unchanged scientific blobs are independently re-reviewed.


## Stop condition

Retry **C216 only** after recovery review PASS.

Do not register C217.

Gate E remains **PASSED**. Gate F remains **NOT PASSED**.
