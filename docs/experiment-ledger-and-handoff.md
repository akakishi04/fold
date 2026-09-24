# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C247 ACCEPTED VALID NEGATIVE. C248 ACTIVE / NOT YET JUDGED. C249 NOT REGISTERED.**
C248 is the unique ACTIVE experiment:V5-B residual token readout vs equal-parameter EOS adapter.
This is an experiment-only candidate,not adoption of a new production architecture.
Post-authoring review PASS;authoritative Windows prechecks/full regression/scientific run pending.
C246/C244 remain valid negatives;C245 remains diagnostic-integrity PASS. All earlier boundaries remain.

## Latest accepted evidence — C247

Scientific execution HEAD:6705aa76bf70ec2685100c47e1abe9cec3625523.
Published log commit:539bdb7860f1a9a5d59046c43d006c9989b636d9.
Publisher log SHA256:65402c6ffeb4147e71b3ca1228b4a761e391676d550aef2c7e0cf3908e06150c.
Log bytes:598978.
Summary SHA256:2f77f23ee7b77016ad44e1900b7396bbe07855e13429adc32cded0d0276ce404.
Local summary:runs/c247-v5b-normal-exposure-a3cec4a219a14360bac90cf8d7303da5/summary.json.

24 own tests PASS in3.588s;3097 focused tests PASS in110.436s.
328 source pins/514 protected inputs. Six models x200 normal updates=1200 updates/38400 training
presentations;1290 model forwards/43008 total row presentations. All replays/changed weights PASS;
persisted comparator/discrete replay PASS;protected inputs,tracked tree and execution HEAD
preserved;run_execution_valid=True. Both primary TRAIN family gates and secondary joint gates False.

Exact correct counts,EN/JA per seed and family:

| Seed | Full TRAIN /32 | GRU TRAIN /32 | Full HOLDOUT /16 | GRU HOLDOUT /16 |
|---:|---:|---:|---:|---:|
|234001|27,28|31,32|9,8|7,7|
|234002|32,32|18,17|3,5|4,5|
|234003|16,15|17,23|4,5|4,4|

Full234002 EN/JA passes full TRAIN criteria only in C247,not C246. GRU-only234001 EN/JA passes
in both. Other8 cells pass neither. Exact comparison_counts:BOTH_TRAIN_PASS2,
CONTROL_TRAIN_PASS_ONLY2,NEITHER_TRAIN_PASS8. Four of12 TRAIN cells pass;eight miss.
All12 secondary HOLDOUT cells miss. C247's primary verdict is TRAIN-only;do not claim its FAIL
was decided by HOLDOUT or that any primary control PASS would have established generalization.

Interpretation is mixed. For Full234002,normal exposure reduction alone cannot explain the
corresponding C246 TRAIN miss. For the8 neither-pass cells,insufficient normal budget remains
compatible without excluding mixed-training effects. Removing masked updates changes optimizer
step counts/moments,so no unique internal cause is identified. No architecture-wide impossibility
or core-specific blame follows. The prior architectural suggestions remain hypotheses.

Acceptance/artifact identities:docs/experiment-ledger-addendum-c247-c248.md.
Acceptance/base commit:521eff1865cd13224ff5a2a247c466a6ba330d3e.
The log publication is one commit after execution and changes only c247/latest.log/latest.json.
Acceptance uses immutable log ranges and recorded local postchecks,not an independent full-log
rehash or reviewer execution of actual trained checkpoints. No C247 rerun or threshold rescue.

## Preserved earlier evidence

C246:training-only erasure mixture did not pass;10 TRAIN misses and2 recombination misses.
C245:selective-input diagnostic only;masked scores are confounded by copying cues and input overlap.
C244:all TRAIN criteria pass at400 normal updates,all HOLDOUT cells miss.
C243/C240/C237/C235 are diagnostics;C242 recombination negative;C241 evidence-use criteria miss
with normal TRAIN100%;C239 order-transfer negative;C238 seen16-prompt fit PASS;C236 random-batch negative.
Preserve all original accepted evidence and invalid-attempt recovery records.

## Active C248 — experiment-only residual token readout

Experiment:C248-v5b-residual-token-read-pilot.
Stage:V5-B-RESIDUAL-TOKEN-READ-PILOT.
One question:can a residual reader revisiting actual token states meet the original normal-input
recombination criteria,compared with an equal-parameter EOS-only adapter?
Stop erasure-recipe tuning for now. This is the minimal token-read part of candidate A,not fact
slots,structured memory,an entity parser or adoption of a new FOLD design. Accepted runtime/core/
frontend files remain untouched;the candidate is isolated in new experiment files.

Two arms in each family,each adding exactly768 trainable parameters:
-token_read:EOS query q=Wq*h;keys Wk*H_i;softmax dot scores/4 over nonPAD states;z=h+Wo*sum(alpha_i*H_i).
 Three bias-free16x16 matrices,no separate value projection. Actual final Full post-core token states
 or actual baseline GRU outputs are read. EOS query summarizes the entire prompt;no parsed gold entity.
-eos_adapter:z=h+W2*GELU(W1*h),bias-free16->24->16. It sees only EOS,not other token states.
Both feed the unchanged original LayerNorm/256-byte decoder. Output projections start zero;
private head RNG seed+248000 leaves global RNG unchanged. Initial logits equal the old backbone.
All backbone and head parameters train jointly;this is not a frozen-backbone probe.
Full14256/GRU-only10928 parameters. Arms have equal capacity,not equal compute/memory/latency.
No speed,unique-mechanism or core-superiority claim.

ReadoutPilot calls original backbone.forward. Per-call hooks capture actual NEXT-route final core
states or baseline GRU output and insert one residual before readout_norm. Captured EOS must equal
the original pooled input. Keep autograd intact;finally removes hooks,including on error. No persistent
capture/cache state or simultaneous hooks on a shared model. Only CPU/NEXT tasks in this fixed pilot.
All real nonPAD slots including BOS/EOS and question bytes are eligible. No correct value/location,
row ID,entity metadata or fixed fact slots enter the neural forward. Attention is not binding proof.

Preserve C244 TRAIN64/HOLDOUT32 exactly via the C247 saved partition. For each seed234001/2/3,
construct common Full and GRU-only initial backbones before training,then deep-copy for both arms.
Backbone fingerprints must match C247.initial_sha256,not its trained final. Initial TRAIN metrics
must match C247.initial_train within1e-9. Parent trained models are never loaded or rerun.

Use established C244400-normal-update recipe for BOTH arms,not the shorter C247 control budget.
Alternate old32/added32 for200 cycles;no erasure. Same AdamW lr0.005,betas(0.9,0.999),eps1e-8,
weight_decay0,clip1,batch32,CPU float64,threads2,deterministic algorithms. Fit AST equals C244 except
its progress tag;row schedule matches all400 steps. Actual optimizer token batches are checked.
Only TRAIN initially;HOLDOUT first evaluated after step400 and replay. No heldout-driven tuning,
early stopping,seed replacement or checkpoint choice. This is not extending or rescuing C247.

PRIMARY:all token_read Full seed/language cells meet BOTH TRAIN/HOLDOUT original criteria:
normal accuracy>=0.90;fact/query/order paired both-correct>=0.80;both mask drops>=0.35.
TRAIN32 rows/language,16 pairs/type:minima29/32,13/16. HOLDOUT16 rows/8 pairs:minima15/16,7/8.
Other arm/family gates independent. Control success cannot substitute for reader success;reader
and control both passing does not establish a reader advantage. Report all12 matched HOLDOUT
deltas and per-arm TRAIN_CRITERIA_MISS,RECOMBINATION_MISS,BOTH_PASS. A valid primary miss is
ACCEPTED VALID NEGATIVE;a pass is bounded internal-fixture evidence only,not Gate F or production adoption.

Workload:3 seeds x2 families x2 arms=12 fresh models. Each400 updates,12800 training presentations.
Totals4800 updates/153600 training presentations;180 scoring forwards/9216 scoring rows;
4980 total full-model forwards/162816 total row presentations. Per model409/13280 before replay,
415/13568 after. One12-state bundle,schema fold-c248-residual-read-v1. Wrapper plus its single
backbone invocation is one model execution;extra readout work is not concealed by that count.
This doubles trained model count versus the earlier six-model runs. No scientific network calls.

Protection:334 source pins/526 inputs;direct dependency union24;OWN6. Own tests24;modules133;
loaded3122/focused3121,only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:readout-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Validate shared initial identity,initial metric replay,head/whole-model
updates,exact final predictions/logits/metrics,actual counters and paired summaries. Postcheck
reconstructs child discrete metrics via C243. Reuse C244 per-model replay with C242 fitting,not
six-model collection summarizers. Fit times and artifact bytes recorded;peak RAM/FLOPs unmeasured.

Manifest:bfaafd5c699690553aa072ba74b9707853a2e627b22a6d3d488b646f27047593.
Design:docs/v5b-residual-token-read-v0.1.md.
Registration:docs/experiment-ledger-addendum-c248-preregistration.md.
Preregistration/review HEAD:08532a9826c73bb23d817e60a0f7a2a0ae2946ba.
Use tools/invoke_active.ps1 with the final activation HEAD,not this pre-activation review HEAD.

## C248 post-authoring review

`post_authoring_review = PASS`
Review HEAD:08532a9826c73bb23d817e60a0f7a2a0ae2946ba.
Scope:committed-byte authoring/synthetic-path review,not a scientific C248 result.

All six OWN files re-fetched after completion. Reviewed Git blobs:
-benchmark:550f6e0d151ba498b7618ea93435f89450088923
-tests:ed6730ad4232da69d2319054eb13cb472d68de4d
-runner:8ad4a0e9fd4e913f4a9801f2ccb32f6550d959c5
-launcher:7270186a53a38e903a29a2ded7b09510a8aa8a4b
-design:b18b283ad8333250a9bf6ec5d00e7c272d511a3c
-preregistration:dc8ed9fcd132bc21447535ab786d3d39267f4801.
The four complete code/script bytes were mechanically Git-blob hashed and matched the fetched IDs.
Base-to-review comparison contains exactly six added files across seven commits,no accepted edits.
A publication transcription bracket typo was detected and repaired before readiness. The final
count check was simplified,then matched to locally compiled/tested bytes;no scientific condition changed.

Actually executed on the tested/matched files:
-UTF-8/NUL checks,Python compile/import and symbol-table free-global/import audit:0 unresolved names;
-24 own tests PASS before readback in28.416s and after final byte matching in19.000s;
-actual own unittest count/unique IDs and synthetic3122-case exclusion filter yielding3121;
-exact manifest and independent partition-fixture hashes;
-raw zero-residual logit equality for both families/arms using real torch.nn.GRU in a synthetic
 backbone;Full's core in this test remains a CheapCore interface double,not the production core;
-added768 parameter counts,total14256/10928,output-projection gradients,non-EOS reader dependence,
 EOS-control token independence,exact PAD exclusion and private-RNG preservation;
-per-call hook cleanup on success/error,backbone nonmutation,EOS/NEXT contract and initial barriers;
-actual400-update helper and per-model replay counts409+6/13280+288 using synthetic backbones;
-normal optimizer batch membership,head updates,gate/capacity/count/replay rejection;
-parent-loader adapter and actual12-model run/save/reload/postcheck,including wrong-HEAD/tamper tests;
-three embedded Python blocks compile;precheck argv1,regression noargv,postcheck argv1/2/3 checked;
-parser-before-publication,exact parent path and source loader/ReadoutPilot dispatch checked.

Actual original language_task.py and C233 GRUOnly forward implementations were retrieved and read:
Full supplies Tensor states through NEXT-route core calls;GRU provides its sequence outputs;both
pool EOS and call readout_norm once. C244 fit/replay/helper signatures and C247 initial/final schema
were inspected. This source review is not an actual real-core numerical test.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5,isolated workspace with complete new
files and reviewer-only import scaffolding/transcribed C244 fit/replay excerpt. Tests use synthetic
CheapGRU/CheapCore for fast training and synthetic Binding/Fitting/Factory/protection/parent adapters.
CheapGRU is explicitly not the production GRU algorithm. The raw-parity test additionally uses
real torch.nn.GRU,but never the actual FOLD core. No accepted user-local model or dataset was loaded.
GitHub DNS was unavailable for a full checkout;connector reads supplied repository source.
PowerShell unavailable. NOT executed here:full3121-test historical regression,Windows PowerShell
AST,accepted user-local source/artifact precheck or12 actual scientific FOLD/GRU models. None is
represented as PASS. All remain mandatory in the authoritative ordered runner.

Only this unpinned handoff changes after review HEAD. Re-read it and verify final branch HEAD
before returning ExpectedHead. Do not advance the branch during the user's formal run.

## Stop and scope

Gate F NOT PASSED;numeric-memory and erasure-mixture tuning paused. Preserve accepted sources,
tests,logs and tools/run_c167.ps1. No production architecture adoption,external data,paid API,
cleanup/history rewrite or shared runtime change.24 own tests ->3121 regression ->C248 ->postcheck ->log push.
Integrity faults stop same C248;repair transport-only failure without retraining. Judge C248 before C249.
