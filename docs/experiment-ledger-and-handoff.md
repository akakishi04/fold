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
- **C216 ACCEPTED PASS**
- **C217 ACTIVE / NOT YET JUDGED**
- **C218 NOT REGISTERED**

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

## Accepted C216 — learned Reader pilot

Scientific execution HEAD:
`99d4254c09f38a433374fb2a073403d6e0ec764a`

Published log commit:
`02d9719fac61d1b1aed8ac8a68fe7218b9cb40f7`

Log SHA256:
`8102412ae39499947408c35d16c8dc2febe1dca68113f549d983e29e3ad36341`

Summary SHA256:
`7542625a054725d3a70dfa1c19f706fe8fce26af379e24b92aa1ae478483acc9`

Formal disposition:
**C216 ACCEPTED PASS**.

Execution validity:
- focused regression **2185/2185**;
- Python syntax preflight PASS;
- source/artifact precheck PASS;
- protected inputs preserved;
- tracked tree clean;
- run_execution_valid True.

Deciding metrics:
- trained Reader models3;
- parameters per model43;
- total training steps1200;
- training examples28800;
- learned Reader forward calls1215;
- all checkpoint roundtrips True;
- seeds216001/216002/216003 each:
  - TRAIN accuracy1.0;
  - EVAL accuracy1.0;
  - HOT EVAL accuracy1.0;
  - COMMITTED EVAL accuracy1.0;
  - placement prediction mismatches0;
  - zero-readout EVAL accuracy1/3 exactly;
- oracle selector calls36;
- oracle Writer operations18;
- learned Writer/Port Selector/Coverage classifier calls0.

Accepted claim:
on the registered small synthetic three-value task, an isolated learned Reader can decode an
oracle-selected FOLD-R scalar memory readout on held-out alpha/beta pair compositions and produces
identical semantic predictions before and after H1->H2 commit.

Non-claim:
C216 does not establish learned port routing, learned writing, learned coverage, unseen semantic
value extrapolation, natural-language memory behavior, memory-cost advantage or Gate F.

Historical invalid/recovery attempts remain documented in:
`docs/experiment-ledger-addendum-c216-recovery.md`.

## Active C217 — learned Port Selector pilot

Experiment:
`C217-v5f-learned-port-selector-pilot`

Stage:
`V5-F-LEARNED-PORT-SELECTOR-PILOT`

One question:
given correct H1/H2 memory and the frozen accepted C216 Readers, can a learned Port Selector route a
held-out query descriptor to the correct alpha/beta memory port and preserve downstream semantic
answers?

Changed variable:
- learned `fold_lm/v05/memory_port_selector.py` only.

Held constant:
- all three accepted C216 Readers frozen;
- Writer oracle/deterministic;
- Coverage classifier absent;
- accepted C215 H1/H2 memory semantics;
- fixed response capsule;
- no language mapping.

Query registration:
- descriptor width4;
- alpha `[1,0,n1,n2]`;
- beta `[0,1,n1,n2]`;
- TRAIN nuisance `[-1,-1],[-1,+1],[+1,-1]`;
- EVAL nuisance `[+1,+1]`;
-8 rows /6 TRAIN /2 EVAL;
- query data SHA `a9ec25d8079e27177567dd4ca85c7aee18f511eb8e8db6b774a61af82e91ac3d`.

Downstream fixture:
- six unequal alpha/beta semantic pairs;
- HOT and COMMITTED placements;
- both alpha and beta queries;
-24 rows per selector seed;
- all three C216 Reader checkpoints frozen;
- correct routing target accuracy1.0;
- forced wrong-port target accuracy0.0.

Training:
- selector4->8->2,58 parameters;
- seeds217001/217002/217003;
- Adam lr0.02;
-400 full-batch steps/seed;
-1200 steps /7200 examples;
-1209 selector forwards;
-18 frozen Reader forwards;
-1227 total model forwards.

Fixed gate:
- TRAIN port accuracy1.0;
- EVAL port accuracy1.0;
- query-blind EVAL accuracy0.5;
- selector checkpoint roundtrip exact;
- downstream overall/HOT/COMMITTED accuracy1.0 for every frozen Reader;
- forced wrong-port downstream accuracy0.0;
- placement mismatches0.

Authoring:
- source pins137;
- protected inputs143;
- artifacts5;
- C217 tests36;
- regression modules102;
- loaded2222 / focused2221;
- manifest `70af02a697ae8fc97f3d379bdab18dd49bf2261a319f7091819323de5c2b8ab4`.

## C217 post-authoring review

**post_authoring_review = PASS**

review HEAD:
`dd045bd38883b490910147ee429c9641601a0e43`

Committed-remote review verified the accepted C216 checkpoint and frozen Reader artifacts,
all130 parent source blobs,137/143 C217 protection accounting, nine direct dependencies,
independently recomputed query/manifest hashes, selector input isolation, unequal-pair wrong-port
control,36 tests /102 modules /2222-loaded/2221-focused regression accounting, exact runner argv,
the complete PowerShell source contract and C218 non-registration.


## Stop condition

Judge C217 before any C218 registration.

Gate E remains **PASSED**. Gate F remains **NOT PASSED**.
