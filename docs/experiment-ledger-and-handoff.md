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
- **C216 ACTIVE / NOT YET JUDGED**
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

Harness before -> after:
- C-numbered invoke scripts: **27 -> 16**
- C-numbered run scripts: **73 -> 17**

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
- source pins129;
- protected inputs135;
- artifacts5;
- C216 tests36;
- regression modules101;
- loaded2186 / focused2185;
- manifest `5332239247d95f6bcd98e328e12f8596aed765b4fa8780b71e1bfb5329fe521a`.

## C216 post-authoring review

**post_authoring_review = PASS**

review HEAD:
`7b6ec7b075fb018c489d234bd2505c53a7802b48`

Committed remote review verified accepted C215 checkpoint identity,122 parent source blobs,129/135
C216 protection accounting, all direct repository dependencies, fixed pair split/data hash, Reader
input isolation,1215-forward workload accounting,36 tests /101 modules /2186-loaded/2185-focused
regression contract, Python c### alias bindings, exact runner argv ordering, the complete PowerShell
test35 source contract and C217 non-registration.


## Stop condition

Judge C216 before any C217 registration.

Gate E remains **PASSED**. Gate F remains **NOT PASSED**.
