# C325 preregistration -- equal-budget mixed length-four coverage

Stage: V5-B-MIXED-NAME-COVERAGE. Authoring date: 2026-10-16 (Japan time).
Experiment: C325-v5b-mixed-name-coverage.
This is a new experiment after C324 ACCEPTED VALID NEGATIVE. Do not rerun C324.
Gate F remains NOT PASSED. No production adoption, C326 or new CI is authorized.
This contract is source-protected. Activation/review status belongs in the handoff
and separate post-authoring review, not a later edit to this contract.

## One question

At the same architecture and total training budget, does retaining half of the
original length-four TRAIN exposure recover original-task retention while
preserving interior-order binding, relative to interior-only length-four training?

## Fixed intervention and comparators

Two arms: interior4 (control) and mixed4 (candidate), BOTH native mean_last.
Seeds 325001..325005; order seeds 325101..325105; ten new models from paired fresh
initial weights. No C324 checkpoint is used to initialize fitting. No seed search.

The logical rows, values, targets, query pairs, ordering, length/profile schedule,
optimizer, model, language coverage and total presentations are paired and fixed.
Only the family of length-four TRAIN name templates changes:

- interior4: all 100 complete length-four epochs use C321 interior templates.
- mixed4: the first complete length-four epoch uses original templates, the second
  uses interior templates, alternating over all 100 length-four epochs.
- Each complete epoch has four updates of 48 rows, covering all 192 TRAIN rows.
  Every row therefore sees original4 50 times and interior4 50 times in mixed4.
  A complete two-query pair always uses the same family. No half-pair splitting.
- Length-two and length-three inputs remain the original C324 inputs, 100 exposures
  per TRAIN row at each length. The profile slot and query/value identities never
  select a family. There is no claim of exact 50/50 allocation within every profile
  slot when its occurrence count is odd; the deterministic schedule is saved.

Reuse C324's actual validated renderers, token tables, native readout wrapper,
scorers and checkpoint fingerprint/replay checks. Do not patch accepted module
globals, forward functions, thresholds or source files.

## Scientific conditions and workload

14256 parameters, including 3328 core parameters; 64 slots; four internal core
steps per model forward. CPU float64, two threads, deterministic algorithms.
1200 updates/model, 48 rows/update, ordinary mean cross entropy.
AdamW betas .9/.999, epsilon 1e-8, weight_decay 0, global gradient clipping 1;
other LR .005, core LR .0005; fit RNG 612000. Optimizer creation is once/model.

Child work, excluding preflight, software tests and artifact verification:
10 models; 12000 updates; 576000 training-row presentations;
15420 model forwards; 904320 total row presentations; 61680 core forwards;
10 checkpoint state reloads, one saved model bundle read for replay and one write.
Raw logit payload 336199680 bytes, separate from serialized file sizes.
Each model performs 1371 fit/evaluation forwards and 171 replay forwards.
No model, tensor or dataset outputs are committed to Git.

## Frozen success rule and reporting

Keep the existing scorer thresholds exactly: accuracy >=.90, both-query accuracy
>=.80, evidence-blind drop >=.35, query-blind drop >=.35, two-fact-order accuracy
>=.80, applied to EVERY registered TRAIN/HOLDOUT profile/language/local cell and
fact-order group. Original gate lengths are 2..6. Length1 is descriptive only.

ALL FIVE paired seeds must independently satisfy:
1. mixed4 passes the complete interior gate and every original2..6 gate.
2. Pooling original2..6 HOLDOUT domains within that seed, both correct-answer gain
   and both-query-correct pair gain are strictly positive versus interior4.
3. Interior HOLDOUT correct-answer and both-query-correct pair counts are each
   nondecreasing versus interior4. Equal counts are allowed here, not negative gains.

Record original contrasts separately by length, all rescues and new regressions,
all seed flags and complete cell measurements. Pooled accuracy does not override
failing cells. A finite failure of this composite rule is a VALID NEGATIVE, not a
reason to refit, select a seed, loosen a threshold or change the mixture.
Template families are now seen during training and the logical split is reused.
This is not unseen-template generalization, 1440 independent tasks, sequential
catastrophic forgetting, architectural impossibility or a general LLM benchmark.

## Accepted parent contract and composite inheritance

Parent scientific HEAD: fcef3d5833c31d51e261ce578209bd5acd73f59c.
Parent publication: c67be12c1a08dda49f218699ecb8896ef1cf2061.
Acceptance/handoff base: 6c3198793f0f6b852fa96be125323763cbfdddde.
Parent local folder: runs/c324-scientific-r6-6b241e7f98c94ee3846a852f39456a7f/.
Primary science/summary.json SHA256:
21e752a51809a9b400c798b24c4ff405105458965b54610cfa16f71a349fbbdd.
Mandatory execution-envelope.json SHA256:
2c6013d9b4f33fb20e79e68946ad8596d756d23694d7d04508fcd0ca0e3040c3.

Verify BOTH exact accepted files, identities, original manifest/work, 5490-test
receipt, seven real verifier completions, nine reuse receipts and final1501 input
rereads. The original792-source/1491-input summary is NOT sufficient by itself.
Inherit all802 sources and1501 inputs from the R6 envelope and verify its exact
primary subset/union. Verify all current inherited source Git blobs and raw input
bytes, plus the eight saved immediate-parent outputs and their byte sizes.

From those fixed saved C324 outputs, reconstruct the canonical data and prompts,
load checkpoints with weights_only=True, compare all ten tensor fingerprints,
reanalyze all ten saved evaluation records with the unchanged C324 analyzer, and
reconcile complete measurements, plan and validation summary. This does NOT train,
run a parent model forward or replay the older C316..C322 semantic validator bodies.
The older evidence is inherited by exact accepted identity plus full byte checks,
not a new claim of recursively reexecuted semantic verification. The new C325 model
results are never cached or repaired by parent answers.

All1517 inputs remain under native Windows read leases throughout the worker.
Use the unchanged R4 lock/hash implementation, with an independent SHA check on
every first hash read and final uncached rereads of every locked file. There is no
unlocked fallback or cross-run cache. No accepted verifier function is substituted.

Protection: 808 sources =802 inherited +6 own files.
1517 inputs =1501 inherited +10 immediate-parent files +6 own source files.
The ten parent files are primary summary, eight outputs and R6 execution envelope.
Both the C325 primary result and companion envelope contain the complete union.
All new deciding-path code and the new regression module are included.

## Regression, execution and saved verification

56 own tests. Complete baseline5490 plus56 =5546 selected tests,214 modules.
Before the single inherited C204 exclusion the total is5547. No new exclusion or
skip is introduced. The actual suite is built and its distinct IDs/counts validated;
its ordered-ID SHA256 is printed. Full regression runs in a separate ordinary Python
process without science wrappers. Native TRAIN/native-readout/gradient preflight
runs before the full regression; fitting begins only after ALL5546 pass.

Route: explicit PowerShell7 -> invoke_active_v2 -> invoke_c325 -> run_c325 ->
c325_execution controller -> scientific worker -> ordinary regression subprocess ->
all ten fits/evaluations/replays -> fresh saved bundle/metric reconstruction ->
1517 final input rereads -> saved summary/envelope -> separate byte verifier.

The separate verifier checks exact parent/child source and input unions, all1517
input bytes, summary/envelope contracts, complete regression receipt, all output
hashes/sizes and the unchanged scientific manifest/gate decisions. It does not
claim an additional model replay or recursively rerun the older semantic validators.
A valid execution requires BOTH primary summary and execution envelope.

The eight science outputs are experiment-plan.json, dataset.json,
original-prompts.json, interior-prompts.json, trained-models.pt, evaluations.pt,
measurements.json and validation-summary.json. The containing primary summary and
execution envelope bind their bytes. Per-process science/regression/verify logs and
regression-result.json remain local under runs/c325-mixed-name-<id>/.
Only complete console text is published to docs/experiment-run-logs/c325/latest.*.
Test progress uses streamed dots plus 10-second heartbeats, not 5546 long test-name
lines. Console metrics contain domain minima/totals/counts; complete individual-cell
measurements remain in the hash-verified local artifact. No tests or measurements
are omitted from execution or the saved measurement artifact.

Runtime: Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5, unchanged from accepted R6.
No environment repair, package installation, cache deletion, CI or paid service.
No wall-clock bound, timing-ratio claim or native-crash-cause claim.

## Authoring and stops

Manifest self-hash: 03ed2ba1d2d2951087c70ce41ddf39756674a30ac4cef56671e158eb80fff3d0.
Before activation, reread committed remote bytes for all six own files, check Git
blob identity, compile/free-name bindings and source-level writer/loader/call order,
then rerun all56 own tests, including CP932-default-file-encoding emulation.
Author-side fixtures are not native Windows, full5546 or scientific C325 results.
Dispatcher, selected launcher and runner all retain mandatory PowerShell AST checks
before native execution. Record a separate post-authoring review before activation.

Operational stale branch/HEAD/ACTIVE/dirty-tree cases stop before logging/publication.
Source, input, test, schema, nonfinite, checkpoint, saved-reconstruction or envelope
failure stops SAME C325 as invalid; preserve the log and do not automatically retry.
Scientific FAIL alone does not invalidate execution. A publication-only failure is
repaired without repeating fitting. C326 remains NOT REGISTERED.
