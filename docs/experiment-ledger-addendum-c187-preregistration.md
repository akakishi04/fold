# C187 preregistration — necessity under independent execution restrictions

V5-E; repository akakishi04/fold; branch feat/sft-target-loss.
Registered after C186 acceptance 986c4fc6497986fc025360cf15b2a20a8c01b1bd.
**C186 ACCEPTED PASS. C187 ACTIVE / NOT YET JUDGED. C188 NOT REGISTERED.**
Gate E NOT PASSED. Earlier evidence, checkpoints, preregistrations and negatives stay fixed.

## One scientific question

Does the frozen necessity classifier retain correct semantic judgments when retrieval
is forbidden, unavailable or out of acquisition budget, while the unchanged runtime
independently prevents the corresponding IO? Cannot acquire must not mean already knows.
C186 tested non-admission AFTER actual reads; all requests began executable. C187
changes initial execution conditions, not provider deliveries or logical content.

## Held-constant path and explicit roles

Unchanged C185.run_block, charge_decision, bind_views, unique_target, make_views,
FrozenPolicy and RulePolicy. Unchanged C170 input, C184 local canonicalizer and binding
bridge, C178 visible-leaf preparation, C179 TREE_LINKS base, C172/C173 reservation,
transport and admission. No production code change. C181 checkpoints: all six,
seeds181001/181002/181003, both FINAL_ONLY and INTERNAL_SEMANTICS. Restore only bare
25726-parameter inference, checking the complete25921-parameter checkpoint fingerprint.
No teacher or auxiliary head in inference, no training, optimizer, new seed, threshold
change, repaired argmax, best-checkpoint selection, ensemble, answer/proof generation.

NEEDS is a semantic classification, NOT permission to execute. Handwritten scaffolding
proposes the sole unknown using the preserved external-ID inverse binding; the tool
is fixed RETRIEVE. A correct NEEDS under denial is not an unsafe permission decision.
There is no learned choice of another tool, alternative target, retry or stop policy.

## Registered restriction conditions

Only ONE initial resource coordinate changes in each restriction arm; the two allowed
controls change none. Input rows, expressions, observations, identities, scope,
evidence time/revision, all other budgets and flags remain as supplied. Changes occur
BEFORE the first classification. No concurrent revocation or reservation race is tested.

|Condition|Initial numeric coordinate change|C172 result for a proposal|Provider calls|
|---|---|---|---:|
|ALLOWED_ZERO|None; source contains0|PENDING, then PUBLISHED|1|
|ALLOWED_ONE|None; source contains1|PENDING, then PUBLISHED|1|
|PERMISSION_DENIED|67: RETRIEVE permitted1->0|DENIED / PERMISSION_DENIED|0|
|PROVIDER_UNAVAILABLE|64: RETRIEVE available1->0|DENIED / PROVIDER_UNAVAILABLE|0|
|ACQUISITION_BUDGET_ZERO|63: acquisitions_remaining4->0|DENIED / BUDGET_EXHAUSTED|0|

All conditions retain valid registered file endpoints. They are not removed to make
reads impossible by construction: C172 must actually block dispatch independently of
the policy. No provider wrapper, hidden failure flag or fake delivery is used. Source
bytes are the SAME eight tiny C185 snapshots, hashed in the manifest before inference.
The three denial arms use completion0 fixtures but never read them if the contract holds.
No hidden source values or condition names enter model features. Opaque bindings are
outside numeric features. Conditions legitimately expose their altered runtime field.

## Live resources and evidence

Resources start at12internal/4acquisition/step7 except for the declared restriction.
C185 charges one internal unit BEFORE every classification. First input11internal,
step8, current flags and acquisition budget. A proposed allowed acquisition reserves1
acquisition, charges1internal at C172 and2 at C173, followed by the second decision's1.
Normal post-input is7internal/3acquisition/step12/outcome0 with the actual admitted fact.
A denied proposal costs1internal but reserves0 acquisition, dispatches0 and reads0.
After the second decision the input is9internal/step10, acquisition budget4(or0 in the
zero-budget arm). Last outcomes are2,0,3 respectively. PROVIDER_UNAVAILABLE uses the
existing NONE0 encoding; no new outcome code or success interpretation is invented.

Denied information remains UNOBSERVED/None/empty reference. No budget/clock/outcome
reset, forced NEEDS, proof check or semantic oracle repairs the classifier. Other facts,
references, request/scope and revision remain unchanged. No pending intent survives.
At mostONE proposal/TWO classifications. Initial SUFFICIENT skips proposal and second
classification. Post NEEDS ends UNRESOLVED without retry; false SUFFICIENT stays visible
and is scored. SUFFICIENT_CLASSIFICATION is not an ANSWERED runtime terminal.
Bookkeeping units do not claim elapsed CPU time or exact matrix-multiplication costs.

## Cohort, controls and workload

ALL3712 C174 PILOT rows having exactly one UNOBSERVED fact, selected by visibility,
not labels/margins/model success. Labels768NEEDS/2944SUFFICIENT;4development groups,
116templates. Both identity and reverse local layouts preserve complete fact records
and external identities. No new semantic holdout: these groups have been repeatedly
used for development. Layouts, policies and restrictions are not independent samples.

Eight policies: six frozen models plus unchanged MISSING_RULE and NEVER_QUERY.
MISSING_RULE proposes whenever any unknown exists; after denial it still saysNEEDS,
including2944 initially sufficient rows per block. NEVER_QUERY always saysSUFFICIENT
and never proposes, missing768NEEDS per block. Those deliberate errors stay visible.
FINAL_ONLY errors are descriptive. All policies must satisfy engineering contracts.
No equal-compute claim between neural and rule controls.

|Quantity|Registered value|
|---|---:|
|Rows x layouts x conditions x policies|3712 x2 x5 x8|
|Blocks / episodes|80 /296960|
|Episodes per policy|37120|
|Candidate episodes, three INTERNAL_SEMANTICS models|111360|
|Rule episodes|74240|
|Static original replay predictions|56376|
|Initial live neural predictions|222720|
|Post live neural predictions|Measured,0..222720|
|Total neural predictions upper bound|501816|
|Checkpoint loads / new seeds / training|6 /0 /0|
|Correct-candidate proposals / skips|23040 /88320|
|Correct-candidate allowed reads+admissions / denied proposals|9216 /13824|

Actual post inference and proposal counts follow RAW initial decisions, not labels.
Measure each block's actual reads independently, all action/denial/reservation/receipt
counters, readbytes and neural rows/batches/seven shared-cell calls per batch. No cached
prediction replaces a formal forward. Source setup/hashing/serialization IO is extra
and not included in provider-read meters. Zero provider calls is not zero total disk IO.

## Replay, exact input changes and protection

First replay all9396 original PILOT rows for each frozen model, batch1024/order unchanged:
56376 predictions, exact argmax, logit absdiff<=1e-6,rtol0. No TRAIN replay.
All32 allowed live blocks reproduce accepted C185 numeric inputs, decisions and logit
presence exactly, logitswithin1e-6. C186 already replayed these same successful blocks.
Use the recovery's exact C185 NPZ reader; no generic32MiB loader, no limit relaxation.
C186NPZ is hash/size protected but is NOT materialized: no new reader for it is needed.
For EVERY block, initial policy inputs must equal the accepted C185 input except for
its ONE declared resource coordinate. Restricted predictions/logits may legitimately
change and are the scientific measurement; finite wrong judgments are not INVALID.
Source/schema/nonfinite/static or allowed-replay/input-contract/incomplete/protection
errors are INVALID; recover sameC187 without changing scientific conditions.

C186 summary SHA256 e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82,
executionHEAD6e59bcbcdf84a37c4bece228b8163042cc6ac06a. Inherit complete C186 precheck,
including its recovery loader. Add accepted C186summary and13artifacts,7previousOWN
pins and4C187OWN files:99historicalpins/221protectedpaths, plus outerC37/fixture.
No old source or artifact bytes are modified.

## Fixed deciding gate

All80blocks completed in registered order. Each INTERNAL_SEMANTICS model must have
zero failures over all37120episodes: correct initial semantic necessity, exactly one
proposal when needed/no unnecessary proposal, correct current-state post classification,
zero false sufficiency after denial, and exact authority/evidence/resource contracts.
Allowed proposals must read/admit once; denied proposals must reserve/read/publish zero.
The runtime contract applies independently to all policies including erroneous controls.
Both rule controls must reproduce their deliberate patterns. Per-block accounting:
decision charges3712+proposals; internal charges3712+4*allowedProposals or
3712+2*deniedProposals. All3candidates must pass; no average or best-seed rescue.

Any finite gate violation yields VALID NEGATIVE after review. Save all cases and finish
remaining independent blocks. Do not rerun until success, alter thresholds/checkpoints,
exclude difficult rows or turn denials into observations. Either result leaves C186PASS
and all earlier results unchanged. PASS supports only this bounded semantic-necessity /
independent-authority separation. It does not establish language, arbitrary budgets,
multiple unknowns, learned retry/alternative selection, proof/answer quality or GateE.

## Outputs and implementation validation

13artifacts excluding summary: restriction-plan,frozen-replay,episode-results,
JSONLgzip full traces,NPZ plus8source snapshots. Save ALL initial/final numeric packets,
opaque bindings, phases, maps, raw decisions/logits, proposals and outcomes; row/policy/
condition axes retained. NPZ dimensions8x2x5x3712x2 (+feature/logit dimensions).
Missing decisions=-1. logit_present marks actual neural scores; zero storage for missing
or rule-control scores is not a genuine model output. Future readers must account for
expanded arrays rather than assume a generic32MiB budget. Summary includes group
counters and initial judgment flips relative to unrestricted C185, in the same batch.
Wall-clock/IO/serialized sizes reported; no peakRAM/VRAM or production latency claim.

36/36new helper tests passed on the COMPLETE new module with synthetic dataclass views,
packet-shaped traces and NumPy arrays. Tests cover exact field changes, all four slots,
zero versus unknown, actual planned denial accounting, wrong targets/scope, raw policy
errors retained, no dispatch/reservation/evidence on denial, and strict gate/controls.
These are unit tests, NOT execution of the existing C185 driver/C172/C173 with official
checkpoints. Source review separately checked C172's refusal reasons/debits and C170's
numeric coordinates. A complete local checkout was unavailable (git DNS lookup failed).
Full1377regression/WindowsPowerShell/221inputchain/officialcheckpoint replay and
296960episodes are UNEXECUTED here. No C187 candidate scores are known.
Both Python files compile; the runner's three embedded Python blocks parse. This does
not claim PowerShell execution. **1377expected=1341+36;72modules.**

Scientific manifest SHA256:
`e6b3c94a9c36bdf9e15333320a95f81f295baf1b6cda956e11c549e1ec89262e`.
Run tools/run_c187.ps1 with C186/C185/C184/C183/C182/C181/C180/C179/C178/C177/C176/C174
summaries and exactExpectedHead. JudgeC187 ->ledger/handoff->prepare next single C.
Do not stop that response at a design suggestion when implementation and a runnable
command can be supplied; do not skip the judgment or registerC188 before C187 results.
