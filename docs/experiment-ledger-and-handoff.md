# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C244 ACCEPTED VALID NEGATIVE. C245 ACTIVE / NOT YET JUDGED. C246 NOT REGISTERED.**
C245 is the unique ACTIVE experiment:V5-B frozen selective-evidence diagnostic,not a capability run.
Post-authoring review PASS. Authoritative runtime prechecks/full regression/scientific execution pending.
C243 remains diagnostic-integrity PASS. All earlier verdicts and accepted evidence remain unchanged.

## Latest accepted evidence — C244

Scientific execution HEAD:d89007bc5a04c4f6b99bff966093b0e14174e04b.
Published log commit:d1e2933492cf4f4d0cbfb535c80b800c58bcadf7.
Publisher log SHA256:fad665eeb8a89322079f21425b89ae28336567574a47043b10a479303780b158.
Log bytes:578100.
Summary SHA256:a2c5167bd6e93c09020ca5079cc94d77e692fd18768588536379d4797fd99297.
Local summary:runs/c244-v5b-two-partner-recombination-63a64987412a494291853ed0afb9c639/summary.json.

24 own tests PASS in6.544s;3025 focused tests PASS in134.647s.
310 source pins/478 inputs protected. Six models x400 updates,block_updates=[200,200].
2400 training steps/76800 training presentations/2490 model forwards/81408 total rows.
All checkpoint/prediction replays,weight changes,common-HOLDOUT comparison and postchecks pass.
Tracked tree clean;execution HEAD preserved;run_execution_valid=True.
Scientific status FAIL;both family gates False;cell_outcomes RECOMBINATION_MISS:12.

All12 TRAIN cells:32/32 answers,16/16 fact/query/order pairs,evidence drop0.75,query drop0.50-0.59375.
HOLDOUT correct counts,each out of16:

| Seed | Full EN | Full JA | GRU-only EN | GRU-only JA |
|---:|---:|---:|---:|---:|
|234001|7|8|7|8|
|234002|2|5|6|7|
|234003|8|9|6|7|

All HOLDOUT accuracy values12.5%-56.25%,below90%. Every full TRAIN criterion passes,while all
held-pair cells fail. The same-HOLDOUT comparison with C242 has7 improving cells,2 ties,3 worse.
Pooled correct65/192 ->80/192 is descriptive only,not a significance test or independent replicates.
No universal improvement,unique causal mechanism,core superiority or Gate F claim.

Acceptance/artifact identities:docs/experiment-ledger-addendum-c244-c245.md.
Acceptance/base commit:2d7fc4fabee22a7a5f718748756b952deb979f25.
The log publication is one commit after execution and changes only c244/latest.log/latest.json.
Acceptance uses immutable log ranges,publication metadata and recorded local postchecks,not an
independent full-log byte rehash or reviewer rerun of the user's trained checkpoints.
Do not rerun/rescue C244. Coverage,repetition and alternating-block dynamics changed jointly.

## Preserved earlier evidence

C243:diagnostic PASS;C242 HOLDOUT had215/384 absent-value outputs,166 matching partner_of_other.
That finding applies to C242,not an established mechanism of the new C244 models.
C242:all TRAIN criteria pass,held recombination misses. C241:normal TRAIN100%,evidence drop0,
HOLDOUT0%;full TRAIN criteria miss. C240 diagnostic PASS;C239 order-transfer negative;
C238 seen16-prompt fitting PASS;C237 diagnostic PASS;C236 random-batch negative;C235 diagnostic PASS.
All accepted sources/tests/logs and earlier recovery records remain unchanged.

## Active C245 — frozen selective evidence

Experiment:C245-v5b-frozen-selective-evidence.
Stage:V5-B-FROZEN-SELECTIVE-EVIDENCE.
One question:how do the six frozen C244 final models respond to hiding the queried entity's
value versus hiding only the other entity's value?

Change only diagnostic input erasure and measurement. Keep exact C244 TRAIN64/HOLDOUT32,
source provenance,row order,labels,architectures and all six final checkpoints. No learning,
optimizer operation,checkpoint selection or new checkpoint write.
Original views:normal,evidence_blind,query_blind. New views:queried_value_blind,other_value_blind.
Replace exactly one factual digit with '?',following the entity through reversed order. Keep
names,query,order,byte length and EOS position. No target label selects the field;only the query
already present in the input is used. Cross-check actual C231 prefix_tensor against C234.tensors.

Load the accepted C244 bundle through its own load_bundle,then strict state_dict load. Require
final_sha256,eval mode,requires_grad=False,no gradients,and unchanged fingerprints after inference.
Replay every original saved prediction exactly and all original metrics,including NLL,within1e-9.
Original metrics use actual C234.metrics plus C242's order-pair formula. C244.summarize(refs,fitting)
requires C242 fitting as the second argument;do not assume a one-argument parent summarizer.

For each model/split/language and every view,report correct,accuracy,answer_nll,normal-minus-view
accuracy,answer flips,correct-to-wrong,wrong-to-correct,NLL increase and maximum absolute logit drift.
Save all raw logits so postcheck reconstructs metrics without more model forwards. Common shifts
in raw logits are not probability changes;do not use raw drift alone as an importance measure.
Scoring uses original complete-prompt targets even when a masked prompt is ambiguous;no masked
accuracy is treated as a capability gate.

Critical limits:selective masks were absent from training. Distribution shift and redundant
information prevent unique internal-cause claims. Exact identical-input ceilings:
queried-value hidden:TRAIN50%,HOLDOUT100%;other-value hidden:100% in both splits.
The HOLDOUT pairs0/3 and1/2 allow an oracle to infer an erased target from the remaining value.
A high selective score is not proof of direct target reading;low scores are not an architecture
impossibility proof. This diagnostic does not authorize input masking as a production repair.

Workload:6 models x2 splits x5 views=60 forwards;6x96x5=2880 row presentations.
10 forwards/480 rows per model;24 split/language cells,each with5-view statistics.
One checkpoint bundle load containing6 states;new training steps0;checkpoint writes0;network calls0.
Root hooks verify actual counts and are removed on failure. Precheck/postcheck load no checkpoint.
C245 PASS is integrity only,regardless of which mask changes the answer. Faults are INVALID /
RETRY SAME C245. C244 stays a valid negative and Gate F stays NOT PASSED.

Protection:316 source pins/490 inputs;direct dependency union21;OWN6.
Own tests24;modules130;loaded3050/focused3049,only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:diagnostic-plan.json,intervention-inputs.json,outputs.json,diagnostics.json,
validation-summary.json. outputs.json holds fingerprints,counters,parent metric error and raw logits.
The737280 float64 logits are5898240 raw numeric bytes before JSON/metadata,not a peak-memory claim.
Only console logs/receipts are published. Never commit generated arrays or checkpoints.

Parent summary:a2c5167bd6e93c09020ca5079cc94d77e692fd18768588536379d4797fd99297.
Fixed split:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.
Manifest:50cadf2e5b9bc0c1a1fab5f29652afd5b5c2f0eeaed3be919cdadb3ebcebf1ac.
Design:docs/v5b-selective-evidence-v0.1.md.
Registration:docs/experiment-ledger-addendum-c245-preregistration.md.
Preregistration/review HEAD:3cf7b03eb9c4d52e48258b7d283bf01da392ab17.
Use tools/invoke_active.ps1 with the final activation HEAD,not the review or C244 execution HEAD.

## C245 post-authoring review

`post_authoring_review = PASS`
Review HEAD:3cf7b03eb9c4d52e48258b7d283bf01da392ab17.
Scope:committed-byte authoring review and synthetic execution,not actual C245 scientific results.

All six OWN files were re-fetched at the immutable review HEAD after authoring completion.
Reviewed Git blobs:
-benchmark:9499e495c11f8c8332cecfe1de3e9ef30ec7d7ed
-tests:94aa795e2cf13db34a8631d14e93d1b64f6413d5
-runner:000ac0cbc46507919f7ab066cc04542a6d46ff27
-launcher:c91c425e551c04a745b372dce421f8dc0b94cf19
-design:51da1e8c601229e08ad3e2e4da4aeaed9fb736e2
-preregistration:0142e8d955c364c41154a11760a030fca564cc38.
The four complete local code/script files were hashed using Git blob framing and exactly matched
the returned remote IDs. Base-to-review comparison contains six additions only,no accepted edits.

Actually executed on these matched bytes:
-Python compile/import,UTF-8/NUL checks;symbol-table free-global/import audits:zero unresolved names;
-all24 own tests PASS before publication in2.708s and after remote readback in2.637s;
-actual own unittest count/unique IDs and a constructed3050-case exclusion filter to3049;
-exact parent partition hash,manifest digest and selective-mask ambiguity ceilings;
-mask identity and one-byte/token changes across both languages/orders/queries;target-not-read control;
-original prediction/metric mismatch rejection,trainable-model/wrong-final-ID rejection;
-actual10-forward/480-row frozen score path and instrumentation cleanup on failure;
-synthetic full six-model state-load/diagnostic/persisted-logit replay,wrong-HEAD and artifact-tamper rejection;
-three embedded Python block compiles,CLI argv1 then1/2/3,parser-before-publication and exact parent path;
-AST checks for actual own loader/state-load/freeze/scoring order and no training or torch.save path;
-additional200 synthetic three-view metric comparisons against a reviewer-only transcription of
 the fetched C234 metrics/paired_accuracy functions,with exact agreement;
-480 prefix tensor comparisons against the fetched C231 prefix_tensor excerpt,with exact agreement.

The last two checks use immutable-source excerpts,not a full repository import. Parent C244
writer/state/replay/context semantics and C234 metrics/renderer plus C231 fingerprint/prefix
semantics were source-reviewed. The actual scientific path calls the real protected parent helpers;
synthetic adapters are confined to tests/reviewer work. No actual C244 logits or new scientific
C245 predictions were produced in the reviewer environment.

Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Isolated namespace workspace contains
complete new files,synthetic models/adapters and reviewer-only parent excerpts,not a full checkout.
A git ls-remote attempt failed because github.com DNS could not resolve. Connector tools supplied
committed repository reads/writes. PowerShell was unavailable in the reviewer container.
NOT executed here:full3049-test historical regression,Windows PowerShell AST,accepted user-local
parent artifact precheck or inference on the actual six accepted C244 models. None is called PASS.
The authoritative Windows runner must execute these remaining checks. Count arithmetic3026+24=3050
minus the same one exclusion=3049 is enforced by the real runtime loader,not presumed as a test pass.

Only this unpinned handoff changes after review HEAD. Re-read it and confirm final branch HEAD before
returning ExpectedHead. Do not advance this branch while the user's formal execution is active.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve all accepted evidence and tools/run_c167.ps1.
No extra training,model expansion,paid API,external corpus,cleanup,history rewrite or production change.
24 own tests ->3049 focused tests ->C245 frozen diagnostic ->postcheck ->remote log publication.
Stop same C245 on integrity faults;repair transport-only failure without rerunning completed inference.
Judge C245 before registering C246.
