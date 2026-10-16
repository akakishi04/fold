# C326 preregistration -- exact-exposure mixing granularity

Authoring date: 2026-10-16 (Japan time).
Experiment: C326-v5b-mixing-granularity. Stage: V5-B-MIXING-GRANULARITY.
Acceptance base: 1a8d15e46aa0b661d5570bed662e67aa1760fc77.
C325 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED; C327 NOT REGISTERED.
This protected contract does not itself activate execution. Activation requires the
separate committed-byte post-authoring review and authoritative handoff update.

## One scientific question

At identical architecture, optimizer, total workload and per-query-pair/per-profile
family exposure, does mixing original/interior names within each optimizer update
recover interior binding without losing original-task retention, compared with
switching the template family once per complete length-four epoch?

## Fixed control and intervention

Arms: epoch4 (control), batch4 (candidate). Both use native mean_last.
Fresh initialization seeds326001..326005; order seeds326101..326105; ten new models.
Neither arm starts from any accepted checkpoint. No seed search or partial cohort.

The control reproduces the C325 mixed4 family rule: of the100 length-four epochs,
the first uses original templates, the second interior templates, alternating.
An epoch covers192 TRAIN rows in four updates of48 rows /24 intact query pairs.
Every row has100 length2,100 length3,50 original4 and50 interior4 presentations.
The existing length/profile order, logical row order, paired initialization, target,
query identities, values and languages are identical between C326 arms.

Only temporal assignment of the template family to length-four query pairs changes.
The candidate retains EXACT original/interior occurrence counts for EACH canonical
query pair within EACH profile. The profile imbalance from odd occurrence counts
is preserved rather than silently rounding to a different curriculum.

### Deterministic allocation, no model-dependent choices

Use schedule row indices only. Canonical pair IDs are sorted pairs of row indices
and their lexicographic rank; labels, text content, losses and HOLDOUT are not inputs.
For each of the three profiles independently:

1. List its length-four updates chronologically; each update contains24 pair IDs.
2. Count each pair's ORIGINAL-family quota from the control mask.
3. Let T be total original-pair occurrences and M the number of profile updates.
   Original quota for update j is floor((j+1)*T/M)-floor(j*T/M).
4. Solve the integral bipartite flow from update quotas, through unit-capacity
   observed update/pair edges, to the per-pair original quotas. Use deterministic
   Dinic BFS/DFS with chronological update insertion, sorted pair edges, then sorted
   pair-to-sink insertion. No random tie breaking, model query, alternative solver
   selection or hidden fallback. A used edge means ORIGINAL; the remainder INTERIOR.
5. Recount exact per-pair/per-profile exposure and require equality with the control.

For the registered schedule each length-four update contains11,12 or13 original
pairs (and13,12 or11 interior pairs). Of400 updates,48/304/48 have11/12/13 originals.
This is deliberately NOT a claim of12/12 in every update: exact profile exposure
requires the slight variation. Both members of a query pair always use one family.
The total stays50/50. Length2/3 retain original templates exclusively.

All masks, logical schedules, their hashes and exact exposure maps are persisted.
All five actual plans must validate before full regression or fitting. Allocation
infeasibility is INVALID before fitting, not a negative capability measurement and
not permission to choose a different schedule after inspecting outcomes.

## Model and workload

14256 parameters, including3328 core parameters;64 slots;4 internal core steps.
CPU float64,2 threads,deterministic algorithms;1200 updates/model;48 rows/update.
Ordinary mean cross entropy. AdamW betas.9/.999,eps1e-8,weight_decay0;
other LR.005,core LR.0005;global gradient clipping1;fit RNG612000.

Unchanged child work:10 models,12000 updates,576000 training-row presentations,
15420 model forwards,904320 total row presentations,61680 core forwards,
10 checkpoint state reloads,one replay-bundle read,one new model-bundle write.
Raw logit payload336199680 bytes. Masks/metadata and serialized sizes are separate.
Allocation, native preflight, tests, parent/saved verification are outside this
child fit/evaluate/replay work accounting and are not called free computation.
One model's fit/evaluate calls1371/74016 rows; replay171/16416 rows.

## Fixed scientific success rule

ALL FIVE candidate seeds must satisfy BOTH complete existing task gates: interior
and original lengths2..6. Existing thresholds remain accuracy.90,query-pair.80,
evidence-blind drop.35,query-blind drop.35,two-order.80 at every registered local
TRAIN/HOLDOUT/profile/language/masked/order condition. Length1 descriptive only.
Within EACH paired seed, interior HOLDOUT correct answers AND both-query-correct
pairs must strictly increase against epoch4; pooled original2..6 HOLDOUT correct
answers AND both-query-correct pairs must not decrease. Original ties are allowed;
interior ties alone are not an improvement. No failed seed is averaged away.

Report all seed/domain gates, original contrasts separately by length, all rescues
and regressions, and complete local-cell measurements. Retain finite negatives.
This is a test of one deterministic temporal policy. Even success would not prove
a gradient-conflict mechanism, universal mixing advantage, unseen-template
abstraction, independent logical samples, general LLM capability or Gate F.
Failure would not prove structural impossibility or justify seed/ratio/budget search.

## Parent evidence and inheritance

Parent execution:f95895313da81634976d0ff2761efdd793888c2b.
Publication:c030498473daf1155bc5cba6e358f944ec8fce1a.
Folder:runs/c325-mixed-name-26478978a92c42d2980095d76d6e4339/.
Primary science/summary.json SHA256:
e3e9808fea616ecc27e2644f808553f16fb6a11203284bdea5c2cf63b32006e8.
Mandatory execution-envelope.json SHA256:
e40a7e93159cdf33b94b11e8ee8df197da66949d121dd52eb8c6036db99440b9.

Validate both exact hashes, C325 identity/FAIL/gates/work/manifest, complete5546-test
receipt and1517-final-reread/semantic-completion receipts. Both parent records must
carry the same complete808-source/1517-input maps. Verify all inherited Git blobs
and input bytes, including accepted C324 recovery machinery. No792-pin fallback.

Read the eight fixed immediate C325 outputs, canonical data/prompts, checkpoints
and saved evaluations. Invoke unchanged C325.semantic_recheck to reconstruct its
full saved metrics/plan/summary; no parent model forward or refitting. Do not invoke
older semantic validators recursively; their accepted identities and every inherited
byte remain validated. No accepted module global or function is patched.

C326 protects814 sources=808 inherited+6 own files;
1533 inputs=1517 inherited+10 parent files+6 own files.
Ten parent files=primary summary+8 outputs+execution envelope. The six own files are
benchmark,execution helper,test module,runner,launcher,this contract.
All directly called and lazy repository dependencies are protected.
Use unchanged R4 native Windows read leases throughout the scientific worker,
independent reference hashing on first reads, final uncached rereads of ALL1533.
No unlocked fallback, cross-run cache, artifact removal or source mutation.

## Execution and saved verification

64 own tests;5546 inherited+64=5610 selected tests,215 modules;
5611 before the sole inherited C204 exclusion. No new exclusions/skips.
Build actual suites, check unique IDs/counts and print their ordered digest.
Native TRAIN/control-rule/mask/native-readout/gradient preflight precedes the full
regression, which runs in a separate ordinary interpreter without science wrappers.
Only after ALL5610 pass may the ten new models fit, evaluate and replay.

Route:PowerShell7 ->invoke_active_v2 ->invoke_c326 ->run_c326 ->c326_execution
controller ->science worker ->ordinary regression child ->all fits/evaluations/
replays ->saved semantic verification ->final1533rereads ->fresh byte verifier.
Byte-bind every child output immediately before and after semantic reconstruction,
then require the same hashes again before writing the summary/envelope.
Both child primary result and envelope contain the complete814/1533 protection.
Fresh-process verification checks the exact parent/child unions, every source/input
byte, every output hash/size, regression receipt, manifest, cohort and gate binding.
It is not an additional model replay or ancestor semantic rerun.

Local-only runs/c326-mixing-<id>/science/summary.json+8 registered outputs,
execution-envelope.json,regression-result.json,science.log,regression.log,verify.log.
Only console text is published to docs/experiment-run-logs/c326/latest.*.
Stream test dots,ordered-ID digest,10-second heartbeats,200-step fit progress,
all seed/pair results and compact domain minima/totals. Full cell metrics stay in
hashed local measurements.json. No reduction in tested/measured scope.
Runtime remains Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Authoring, review and stops

Manifest SHA256:
2be1555cf0296e55f5adf2e11302d6112b9b49836781199fcb3fc126d384871e.
Before activation reread all6 committed own files, compare Git blob identity,
compile/UTF8/noNUL/free-global audits, manifest/work/counts and writer/loader/call
order; rerun all64 tests including CP932-default-open emulation. Toy/flow/synthetic
worker fixtures are NOT native Windows, full5610 or ten-model scientific results.
The actual worker is exercised with explicitly synthetic parent/lease/science
callbacks, including failed regression that must never reach fitting.
Dispatcher,selected launcher,runner require PowerShell AST checks before execution.

Stale branch/HEAD/dirty tree/ambiguous ACTIVE/missing dependency/AST failure is
SKIPPED before scientific logging/publication. Native/process/source/input/flow/
test/nonfinite/checkpoint/semantic/envelope failure stops SAME C326, preserving
its log. No automatic retry. Scientific FAIL with valid execution is accepted
negative evidence, not a refit instruction. Fix publication alone without retraining.
No CI,environment reinstall,paid service,artifact deletion or C327 activation.
