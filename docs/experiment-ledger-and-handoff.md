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
- **C217 ACCEPTED PASS**
- **C218 ACCEPTED PASS**
- **C219 ACCEPTED PASS**
- **C220 ACTIVE / NOT YET JUDGED**
- **C221 NOT REGISTERED**

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

## Accepted C217 — learned Port Selector pilot

Scientific execution HEAD:
`a6aac1273951b6e321573445e9f759f35fffb726`

Published log commit:
`ab94e753a5996b7e081d9103427c874ad0600dcb`

Log SHA256:
`7f79e076c94aee742aa2a477c0c849104de60f9b849c249d208a55a56a7a2c20`

Summary SHA256:
`cb27e93c9a6dc9d03875938c55c37f146c12278dec4c9ebb5a20da150fd847ab`

Formal disposition:
**C217 ACCEPTED PASS**.

Execution validity:
- focused regression **2221/2221**;
- Python syntax preflight PASS;
- source/artifact precheck PASS;
- protected inputs preserved;
- tracked tree clean;
- run_execution_valid True.

Deciding metrics:
- trained Port Selector models3;
- parameters per selector58;
- total training steps1200;
- training examples7200;
- learned selector calls1209;
- frozen Reader forward calls18;
- all selector checkpoint roundtrips True;
- all Reader checkpoint roundtrips True;
- each selector seed:
  - TRAIN port accuracy1.0;
  - EVAL port accuracy1.0;
  - query-blind EVAL accuracy0.5;
- every selector seed x frozen C216 Reader:
  - downstream overall/HOT/COMMITTED accuracy1.0;
  - forced wrong-port downstream accuracy0.0;
  - placement mismatches0;
- Reader training steps0;
- learned Writer/Coverage classifier calls0.

Accepted claim:
on the registered tiny two-port synthetic task, an isolated learned Port Selector can map a held-out
query descriptor to the correct alpha/beta memory port, and frozen accepted C216 Readers preserve
the correct semantic answer across HOT/COMMITTED placement.

Non-claim:
C217 does not establish learned writing, learned coverage, natural-language query understanding,
many-port scaling, memory-cost advantage or Gate F.

## Accepted C218 — learned semantic Writer pilot

Scientific execution HEAD:
`ce5ae96f5fe3a08213ee41bffa17ba97c10bb368`

Published log commit:
`2cdd28b494cc174694404561c7ee7daab72e1d76`

Log SHA256:
`d26dc7c375bb8d8662fa8a6e8426bbc5174bdf918373e490548d84f81c1bea6d`

Summary SHA256:
`50ec397534901bb865731b615232c555cfcf0222571f42b09098eae77f49f021`

Formal disposition:
**C218 ACCEPTED PASS**.

Execution validity:
- focused regression **2259/2259**;
- Python syntax preflight PASS;
- source/artifact precheck PASS;
- protected inputs preserved;
- tracked tree clean;
- run_execution_valid True.

Deciding metrics:
- trained Writer models3;
- parameters per Writer150;
- training steps1200 / examples21600;
- learned Writer forwards1212;
- frozen Selector forwards3;
- frozen Reader forwards72;
- all Writer/Selector/Reader checkpoint roundtrips True;
- every Writer seed:
  - TRAIN relation accuracy1.0;
  - EVAL relation accuracy1.0;
  - factor-blind EVAL accuracy0.5;
  - semantic-blind EVAL accuracy1/3;
  - ASSERT overall/HOT/COMMITTED downstream accuracy1.0;
  - REPLACE downstream accuracy1.0;
  - write rejections0;
- wrong-semantic downstream accuracy0.0;
- wrong-factor downstream accuracy0.0;
- actual learned Writer attempts54/54;
- successful chunk commits96/96;
- Reader/Selector training steps0.

Accepted claim:
on the registered structured synthetic task, an isolated learned Writer can select factor+relation
for held-out nuisance observations and drive oracle-kind ASSERT/REPLACE through accepted H1/H2
memory while frozen learned Port Selector/Reader components preserve the correct semantic answer.

Non-claim:
C218 does not establish learned operation-kind selection, RETRACT/ASSUME writing, learned Coverage
classification, natural-language extraction, joint training, memory-cost advantage or Gate F.

## Accepted C219 — learned Coverage classifier pilot

Scientific execution HEAD:
`5a613ed07c34d1735d20c5849464116cc00d333c`

Published log commit:
`76f8f793c984a12e1879944f9b117d92241df505`

Log SHA256:
`64dda2bb49d1eec1a6fa3df9c402086bf9bdd2f108102c16223d6970f6584533`

Summary SHA256:
`dbf54bd3cdc5b2fbd82a68a62bcdbaad806b8946b817776d94527a5bdcbaee14`

Formal disposition:
**C219 ACCEPTED PASS**.

Execution validity:
- focused regression **2297/2297**;
- Python syntax preflight PASS;
- source/artifact precheck PASS;
- protected inputs preserved;
- tracked tree clean;
- run_execution_valid True.

Deciding metrics:
- trained Coverage models3;
- parameters/model148;
- training steps1200 / examples28800;
- learned Coverage forwards1215;
- all Coverage/Selector/Reader checkpoint roundtrips True;
- every Coverage seed:
  - TRAIN accuracy1.0;
  - EVAL accuracy1.0;
  - state-blind EVAL0.25;
  - tier-blind readable0.0;
  - scope-blind MISSING/OOS0.5;
  - readable gate accuracy1.0;
  - non-readable suppression accuracy1.0;
  - MISSING/OOS confusions0;
- frozen readable semantic reference accuracy1.0 across all3x3 Selector/Reader combinations;
- NUMERIC_UNSAFE classified rows0;
- Writer/Selector/Reader training steps0.

Accepted claim:
on the registered bounded structured state summary, an isolated learned Coverage classifier can
distinguish SUPPORTED / HOT_REQUIRED / MISSING / OUT_OF_SCOPE, including explicit MISSING versus
OUT_OF_SCOPE separation, while frozen learned Selector/Reader components preserve readable
semantics.

Non-claim:
C219 does not establish numeric-safety classification, natural-language coverage reasoning,
information-acquisition integration, joint training, memory-cost advantage or Gate F.

## Active C220 — frozen learned stack integration

Experiment:
`C220-v5f-frozen-learned-stack-integration`

Stage:
`V5-F-FROZEN-LEARNED-STACK-INTEGRATION`

One question:
can the independently accepted learned Writer, Coverage classifier, Port Selector and Reader compose
end-to-end with all checkpoints frozen and no retraining across ASSERT/HOT/COMMIT/REPLACE plus
MISSING/OUT_OF_SCOPE states?

Changed condition:
- deterministic `fold_lm/v05/memory_stack.py` integration gate only;
- no learned model changes;
- no training.

Frozen checkpoints:
- Writer3;
- Coverage3;
- Selector3;
- Reader3;
-81 Cartesian combinations.

Episode plan:
- MISSING alpha;
- OUT_OF_SCOPE beta;
- HOT alpha;
- SUPPORTED alpha;
- HOT beta;
- SUPPORTED beta;
- REPLACE alpha;
- REPLACE beta.

Episode SHA:
`99f84e9d05327c8c483b45928676009f6be198e5d568a285d2e893e1279e144f`.

Decision accounting:
-8 episodes;
-6 readable /2 non-readable;
-81 checkpoint combinations;
-648 total decisions;
-486 readable;
-162 non-readable.

Fixed gate:
- all checkpoint-family roundtrips true;
- Writer target accuracy1.0;
- Selector route accuracy1.0;
- Coverage teacher accuracy1.0;
- integration accuracy1.0;
- expected Coverage accuracy1.0;
- readable answer accuracy1.0;
- non-readable suppression accuracy1.0;
- MISSING/OOS confusions0;
- HOT/COMMITTED mismatches0;
- operation failures0;
- new training steps0.

Authoring:
- source pins158;
- protected inputs182;
- artifacts5;
- C220 tests38;
- regression modules105;
- loaded2336 / focused2335;
- manifest `12b5995967abba8c89f2a07c01e6e29afbd96b02db4a0561872a70201deeab52`.

## C220 post-authoring review

**post_authoring_review = PASS**

review HEAD:
`1517615f43b3facccec025d69a8ad815a993524b`

Committed-remote review verified accepted C219 parent evidence,151 parent source pins /169
inherited protected inputs, unique four-family checkpoint resolution,158/182 C220 accounting,
14 direct dependencies, independently recomputed episode/manifest hashes, actual-state versus
expected Coverage semantics, distinct MISSING/OOS suppression,81-combination/648-decision
accounting, zero-training scope,38 tests /105 modules /2336-loaded/2335-focused regression
contract, exact runner argv, complete PowerShell source contract and C221 non-registration.


## Stop condition

Judge C220 before any C221 registration.

Gate E remains **PASSED**. Gate F remains **NOT PASSED**.
