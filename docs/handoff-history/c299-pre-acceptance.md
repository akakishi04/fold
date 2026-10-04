# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C298 ACCEPTED PASS (diagnostic integrity only). C299 ACTIVE / NOT YET JUDGED. C300 NOT REGISTERED.**
C297 remains diagnostic ACCEPTED PASS;C296 remains ACCEPTED VALID NEGATIVE.
C299 is the unique ACTIVE core/remaining-backbone initialization diagnostic.
Latest accepted scientific execution:026dc1983cbdf7c54e6bb6ba6302f04430b17a36.
Latest accepted published log:5113666bdb581526cdc0f2707e493258accbc028. Do not rerun C298.

## Latest accepted evidence — C298

Acceptance:docs/experiment-ledger-addendum-c298-c299.md.
Acceptance commit:315e24172119cd85f040def1ca01a7e4c6a0dfed.
Summary:runs/c298-v5b-components-13bf02bea0764e2cb8fe8802cfa52eb7/summary.json.
Summary SHA256:a57e5f2fc3071c630b6cd083f855511b035a4d8478c91e22f86fe97c373add6e.
Own32/focused4525 PASS;source634/protected1161;run_execution_valid=True.
Manifest:e89e471d5f6e50e028136cf667b7a20f797c444f63b2638c3e29f11736c9cb62.
All3 original diagonals reproduce C297 with max logit error0.0,exact final states and800 losses.
Two/three tasks all9 pass,with perfect normal TRAIN/HOLDOUT answers.
Quad rows(backbone297001..3) x columns(reader297001..3):
[[True,True,True],[False,False,False],[True,True,True]].
Backbone297002 normal quad errors vary2/18/14 across reader choices;reader is not irrelevant.
Its TRAIN-value/HOLDOUT-value correct counts are576/286,566/280,567/283 out of576/288.
The other six cells answer every normal quad question correctly and pass all original full gates.
This bounded fixed-order grid does not establish a universal backbone cause or explain prior
seen-length TRAIN failures. No old gate promotion or best-seed deployment.

## Active C299 — core versus remaining-backbone initialization

Experiment:C299-v5b-core-initialization-grid. Stage:V5-B-CORE-INITIALIZATION-GRID.
Registration:docs/experiment-ledger-addendum-c299-preregistration.md.
Design:docs/v5b-core-initialization-v0.1.md.
Review:docs/c299-post-authoring-review.md.
Acceptance base:315e24172119cd85f040def1ca01a7e4c6a0dfed.
Authoring/review target:be4f0c6ce22632924a217eddeeb49a7125de310a.

One question:does transfer at a fixed reader/order follow recurrent-core initialization,remaining
backbone initialization,or their combination? Cross all3 original levels297001/297002/297003.
Rows=remaining backbone;columns=core. Reader initial seed297001 and order297101 are fixed FIRST
registered levels. Every cell is kept;this is a targeted follow-up,not independent replication.

Actual unchanged C278 MeanFinalDualReadout:core3328 +remaining backbone10160 +added read768=14256.
Remaining backbone means all backbone state except core.*,including input/output components.
Copy a row's full UNTRAINED model,replace core with an independent column copy,and initialize
read from the same fixed reference in all9 cells. No learned checkpoint splicing. All parameters
train afterward;the reader is not frozen. Require actual module/state boundary,parameter counts,
component provenance,distinct factor levels,complete state order and independent parameter storage.

Exact C297 blocked order297101:200epochs*4updates,96 intact pairs,24pairs/48rows per update;
private shuffle order+297000+epoch;length=epoch%2;profile=epoch%3. Each TRAIN row100 exposures per
trained length. Global fitRNG597000 fixed. Ordinary meanCE,one AdamW800steps,lr.005,betas.9/.999,
eps1e-8,weight_decay0,clip1. No auxiliary loss,LR decay,adaptive stop or checkpoint selection.
Optimize only normal two/three-character TRAIN. No HOLDOUT,quad or masked learning inputs.
Labels and component/seed metadata never enter forward;tokens and existing zero task IDs only.

The three same-source core/remainder diagonals reproduce C298's reader297001 COLUMN,not its
previous reader=backbone diagonal. Require exact initial/final full fingerprints,all800 losses,
events/hash,and all task/view logits<=1e-9 with exact argmax. Reproduction includes the failed
backbone297002 cell with2 normal quad errors. No success-only controls or relaxed agreement.

Freeze all9 final models;score old two/three/quad normal,evidence-blind,query-blind tasks. Strict-load
all9 archived states and replay every view. Thresholds unchanged:accuracy.90,query_pair.80,
evidence_drop.35,query_drop.35,two_order.80. C299 PASS means only diagnostic completion,provenance,
reproduction,replay and reconstruction. Capability failures remain separately visible.
Report9 cells,3 task matrices,54 partitions and12 accuracy/final-NLL grids with remaining/core
finite-grid additive decomposition. No population-variance,significance,core-necessity or
architectural-superiority claim. No winning combination is deployed;Gate F remains NOT PASSED.

## Parent contract,protection and workload

Verify25 ordered summary hashes BEFORE exact C298.verify_artifacts(parent_dir,24 ancestors,
accepted execution HEAD). Exact parent summary seals all8 output descriptors. Require diagnostic
PASS,complete old component grid,all_replays/components_matched and original full-task matrices.
Read already-verified canonical input JSONs,recheck hashes,and load fold-c298-components-eval-v1.
All3 reader297001 records become reproduction anchors,not initialization weights.
Sole direct import C298;its context exposes C297 schedule/check_fit/decompose,C296 pair/render,
C294 no-neural,C287 normalizer,C284 scoring/replay,C283 quad,C282 tables and core bundle.
New identities remaining_seed/core_seed use a new analyzer,not C298's cohort validator.

Retain all634 parent source pins and1161 inputs;check repository-local context/core coverage.
Runtime preflight also checks the actual core implementation module's source pin. Add OWN6 and
9 parent files:source640/protected1176. No accepted source/test/log/dispatcher edits or waivers.
Work:9models,7200updates,345600training rows,8658model forwards,485568row presentations,34632core
calls,one9-state bundle write/load,9strict state loads,network0. This diagnostic trains new models.
Operational preflight/tests and old-artifact reconstruction are separate. Numerical comparisons
of diagonals add no forward.

Eight artifacts plus summary:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Schemas:
fold-c299-core-models-v1 and fold-c299-core-eval-v1. Keep all component initial hashes,800CE/events
and final logits. Full tensors/maps remain local/ignored;compact receipt and aggregates are logged.
Own32/modules184/loaded4558/focused4557;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:796fc20a254a8d65111d22f4b2754ae12f43975d869c9ca2fd8b7a6e90c7e846.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local behavioral fixtures).
All6 OWN files re-fetched atbe4f0c6ce22632924a217eddeeb49a7125de310a;whole-file Git blobs match6/6.
Post-match normal own32 PASS in5.127s;whole-suite CP932-emulated own32 PASS in5.151s.
Linux/Python3.13.5/PyTorch2.10.0+cpu;both Python files and3 embedded blocks compile;custom globals0;
UTF-8/no-NUL;manifest self-hash matches. Actual toy800-step loop equals independent reference
losses/weights;fixedRNG/one-optimizer tests pass. Component fingerprints/storage,exact diagonal
identity/trace checks,25hash failures before dispatch,protection including actual core-class pin,
run ordering,nine replay calls,persistence/tampering and explicitUTF8 inventory checks pass.
Toy inputs encode synthetic labels for software tests,not FOLD ability. Parent archives,Git,
scorers/models and inherited suite members are substituted where unavailable.
Real Windows25-parent validation,pins,actual component/diagonal initial verification,PowerShell
ParseFile,the actual4557 regression and9 FOLD training/scoring/replay runs remain mandatory gates.
Activation must preserve all6 reviewed OWN files and every accepted source/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C299 -> Validate(25parents,640/1176
protection,real component grid/diagonal initial hashes/schedule/core implementation pin,own32,
focused4557) -> authoring_runtime_preflight=PASS -> Execute(9cells*800updates,C298-column
reproduction,strict replay,grid reconstruction) -> log publication.
Validate failure skips science/publication. Any integrity or diagonal mismatch repairs SAME C299.
Do not change factor levels,reader,order,cohort,LR,budget,thresholds or select successful cells
after results. C300 remains unregistered until C299 formal judgment. Gate F NOT PASSED.
Separate scientific execution HEAD from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c298-pre-acceptance.md.
Git blob:f1a6fee222da8c7c95c234935751d2c31b0ff7ea. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
