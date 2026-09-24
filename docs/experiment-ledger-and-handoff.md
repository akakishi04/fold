# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C248 ACCEPTED VALID NEGATIVE. C249 ACTIVE / NOT YET JUDGED. C250 NOT REGISTERED.**
C249 is the unique ACTIVE experiment:a frozen read-path diagnostic,not a training or capability run.
Post-authoring review PASS;authoritative Windows prechecks/full regression/scientific run pending.
No production architecture adoption. Preserve the successful C248 individual cells without
relaxing its preregistered all-seed gate. C247/C246/C244 remain valid negatives.

## Latest accepted evidence — C248

Scientific execution HEAD:23bcc949638ea3e927ec0bb3d846b9f42b552a56.
Published log commit:5a3e7e7ae371b5f5f384d1283d68dd434201e6ec.
Publisher log SHA256:7a1984dd55d93253ea3498503873c0cb41fa3667dfa4f467b7ca0994e3dea99c.
Log bytes:609500.
Summary SHA256:99778defedd9854815f94989567687c64930e3b505449a847dd030be5a47dab6.
Local summary:runs/c248-v5b-residual-token-read-f3cd1bdfb2cf4a068ed091ea75bf8b22/summary.json.

24 own tests PASS in26.019s;3121 focused tests PASS in135.539s.
334 source pins/526 protected inputs. Twelve models x400 updates=4800 training steps,
153600 training presentations,4980 model forwards,162816 total rows. All initial metric replays,
head/whole-model weight updates,checkpoint/prediction replays and paired/discrete postchecks PASS.
Protected inputs,tracked tree and execution HEAD preserved;run_execution_valid=True.
Scientific status FAIL;all four arm/family collection gates False;production_adoption=False.

HOLDOUT correct counts,each language /16:

| Seed | Full reader EN/JA | Full EOS control EN/JA | GRU reader EN/JA | GRU EOS control EN/JA |
|---:|---:|---:|---:|---:|
|234001|16,16|9,9|16,16|6,7|
|234002|5,4|4,4|12,12|8,7|
|234003|16,16|7,8|16,16|6,7|

Reader all12 TRAIN cells:32/32 and all criteria pass. Reader8 BOTH_PASS cells (seeds234001 and
234003,all families/languages) have HOLDOUT16/16,all paired scores1.0 and both mask drops>=0.35.
Four reader cells are RECOMBINATION_MISS. All12 EOS-control TRAIN cells pass;all12 HOLDOUT miss.
The EOS-control GRU234003 English TRAIN is31/32;other11 TRAIN cells32/32.
Reader improves over matched control in11 cells,ties1,worsens0. Descriptive pooled scores:
Full reader73/96 versus41/96;GRU reader88/96 versus41/96;combined161/192 versus82/192.
These correlated cells come from only3 paired seeds,not12 independent learning replicates.

This supports the reader as a promising bounded candidate,not uniform reliability or a proven
binding mechanism. Equal parameter count is not equal compute/optimization geometry. Backbone and
head seeds are linked;the seed234002 failure cause is not isolated. No FOLD-core superiority claim.
Acceptance/artifacts:docs/experiment-ledger-addendum-c248-c249.md.
Acceptance/base commit:812d8a0452962c569303bade157aa802de20ea65.
Publication changes only c248/latest.log/latest.json,one commit after execution. Evidence uses
retrieved immutable log ranges and recorded local postchecks,not a full-log rehash or reviewer
rerun of actual accepted checkpoints. Do not rerun/rescue C248 or replace its failing seed.

## Preserved earlier boundaries

C247:200-normal-update control has4/12 TRAIN passes,8 misses;Full234002 alone passes versus C246.
C246:erasure mixture fails;10 TRAIN criteria misses and2 recombination misses.
C245:frozen masking diagnostic only,with copying/overlap confounds.
C244:400-normal-update TRAIN criteria all pass,HOLDOUT all miss.
C243/C240/C237/C235 remain diagnostics;C242 recombination negative;C241 evidence-use criteria miss
with normal TRAIN100%;C239 order-transfer negative;C238 seen16-prompt fit PASS;C236 random-batch negative.
All earlier evidence and recovery records remain immutable.

## Active C249 — frozen read-path ablation

Experiment:C249-v5b-frozen-read-path-ablation.
Stage:V5-B-FROZEN-READ-PATH-ABLATION.
One question:does original-input performance of frozen C248 models depend on the residual branch
and,for readers,on learned nonuniform token weighting?

Use ALL12 accepted final states,including unsuccessful readers and EOS controls. Instantiate
actual C248.ReadoutPilot,strictly load through the parent bundle contract and freeze all weights.
Final wrapper fingerprints must match final_sha256,not initial_sha256 or backbone_initial_sha256.
C249's own loader reads C248 records;it never calls C248.load_inputs with a wrong-parent schema.
Parent summary replay uses C248.summarize(refs,C242);parent bundle schema fold-c248-residual-read-v1.

Hold fixed TRAIN64/HOLDOUT32,row bytes/order/targets/provenance,C234 renderer,CPU float64,threads2,
deterministic algorithms,all backbone/head/norm/decoder weights and256-way output.
Per model:original three views/both splits -> residual_off normal/both splits -> reader-only
uniform_read normal/both splits -> restore original three views/both splits.
-residual_off,both arms:head returns pooled h,removing its added residual contribution.
-uniform_read,reader only:head returns h+Wo*mean(nonPAD H),retaining learned H and Wo. Same eligible
 BOS/EOS/question positions;PAD excluded. No parser,gold location or masked input aid is added.
Scoped head hooks replace returned representations without editing parameters. Original head
computation still runs;uniform adds an output projection. No efficiency/FLOP advantage is claimed.

Intact predictions exactly reproduce C248 arrays;all original metrics including NLL agree<=1e-9.
Ablations have normal-only metrics;do not invent masked-view drops for them. Report normal accuracy,
NLL,fact/query/order pairs,accuracy drop,NLL change,answer flips,lost/gained correctness,raw-logit drift.
Restore original outputs afterward:argmax exact,raw-logit error<=1e-9. Require unchanged weights,
no gradients,no token mutation and no leftover hooks after successful completion.

C249 PASS is diagnostic integrity only,independent of ablation effects. It does not revise C248,
prove general language or identify a unique semantic/learning mechanism. A co-trained branch
ablation is not a separately trained backbone-only model;uniform intervention is not a model
trained with uniform attention. Internal distribution shifts/co-adaptation remain interpretation limits.
No favorable-seed selection or claim that this diagnostic establishes reliability across new seeds.

Workload:6 readers x16 forwards/768 rows plus6 controls x14/672 =180 model forwards/8640 rows.
12 accepted states loaded,zero new training/optimizer steps/checkpoint writes/network calls.
Store5184 logit rows for intact+intervened passes;3456 restored rows are checked online,not duplicated.
72 normal contrast cells. Postcheck reconstructs all retained metrics/contrasts from saved logits
without additional model forwards. Historical regression/fixture/file-processing work is separate.

Protection:340 source pins/538 inputs;direct dependency union25;OWN6.
Own tests24;modules134;loaded3146/focused3145,only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:ablation-plan.json,logits.json,diagnostics.json,contrasts.json,validation-summary.json.
Manifest:9fd82672124ff0227174d7a9df894c67ca9f1958a36fad6cbc575e1179dfa414.
Design:docs/v5b-frozen-read-ablation-v0.1.md.
Registration:docs/experiment-ledger-addendum-c249-preregistration.md.
Preregistration/review HEAD:eb818cfeb3fcf99eb46649d92140c815960e8c67.
Use tools/invoke_active.ps1 with the final activation HEAD,not the pre-activation review HEAD.

## C249 post-authoring review

`post_authoring_review = PASS`
Review HEAD:eb818cfeb3fcf99eb46649d92140c815960e8c67.
All6 OWN files were re-fetched after completion at this immutable HEAD. Reviewed Git blobs:
-benchmark:d10e728d70e5af9fbcfbddeea8144f608fcd56c3
-tests:6a86160d1fb3261a3519773d18c2b8649cfadb16
-runner:72a411b46a2a9fe74535d3d51dc652c2301584f0
-launcher:79e5efdf8bb15de221208cb1acea54d35a6e2a50
-design:3212ad4c994a96f5cb28c367724fdcb37bdb23ae
-preregistration:ff744165b9f817ad82d158e06f51c200694da64d.
All4 complete local code/script files were Git-blob hashed and matched the fetched IDs. Comparison
from acceptance base to review HEAD has exactly6 new files,no accepted edits.

Actually executed:Python compile/import and UTF-8/NUL checks;free-global/import symbol audit with
0 unresolved names in both new Python files;24 own tests PASS before publication in3.237s and
again after full remote-byte identity checks in3.375s. Actual own loader count24/unique IDs and a
constructed3146-case filter yielding3145 were tested;the latter is NOT historical regression.
Manifest and independent exact partition fixture hashes match. Tests cover off/uniform equations,
PAD exclusion,EOS-control restriction,hook removal on intervention error,restoration,frozen state,
finite/schema rejection,normal/paired/mask metric semantics and logit-versus-answer distinctions.
An independent counterpart-enumeration implementation agrees on20 random HOLDOUT logit cases.

Tests also exercised actual C249 audit_model and all12-model run/postcheck using synthetic
backbones with real torch.nn.GRU and a synthetic Core interface double,transcribed C248
ResidualHead/ReadoutPilot class excerpts,and substituted parent loader/protection/summary adapters.
Strict state-load/identity rejection,real per-model16/14-call counters,restore replay,stored5184-row/
72-cell recomputation,wrong-HEAD/tamper rejection and no-training AST checks passed. The3 embedded
Python blocks compile;precheck argv1 and postcheck argv1/2/3 match actual invocations. Exact parent
path,branch/tree/HEAD/ACTIVE preflight and parser-before-publication ordering were reviewed.

Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. This was an isolated namespace workspace
with complete new files and review-only C248 class excerpts,NOT a complete checkout or execution
of accepted trained models. GitHub DNS resolution failed in the container;connector reads supplied
repository content. PowerShell was unavailable. The original parent source/schema/signatures and
writer timing were inspected,but not every transitive module was imported in the reviewer workspace.
NOT executed here:full3145 historical regression,Windows PowerShell AST,accepted user-local parent
artifact precheck or the12 actual C248 checkpoints. None is reported PASS. All remain mandatory
in the authoritative runner. Historical arithmetic3122+24=3146,minus the same1 exclusion=3145 is
enforced by the real suite loader. No additional historical exclusions or accepted source changes.

Only this unpinned authoritative handoff changes after review HEAD. Re-read it and verify final
branch HEAD before returning ExpectedHead. Do not advance the branch during the user's formal run.

## Stop and scope

Gate F NOT PASSED;numeric-memory and erasure-mixture tuning paused. Preserve accepted sources,
tests,logs and tools/run_c167.ps1. No training,production architecture adoption,external data,paid API,
cleanup/history rewrite or shared runtime modification.24 own tests ->3145 regression ->C249 ->postcheck ->log push.
Integrity faults stop same C249;transport-only failures are repaired without repeating completed
model work. Judge C249 before registering C250.
