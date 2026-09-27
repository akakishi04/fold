# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold. Branch:feat/sft-target-loss. Local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C265 ACCEPTED VALID NEGATIVE. C266 ACTIVE / NOT YET JUDGED. C267 NOT REGISTERED.**
C266 is the unique ACTIVE experiment:V5-B saved query-pair diagnostic.
C265 all20 states miss the joint compound-identifier gate. C264/C263 bounded PASS and all older
verdicts/recoveries remain unchanged. No optimizer default,architecture or production change.
C266 diagnostic PASS cannot promote capability or identify a causal internal parser.

## Latest accepted evidence — C265

Scientific execution HEAD:e0809d90c552471dee8723ce1b10528488f23be0.
Published log commit:4a51a286efcbe20336dba61699736e02ed51b5fa.
Publisher log SHA256:fb1c50a21c8829aef5a98dccbe189205006c127590fbe7eb9c418e59818fc025.
Log bytes:999513;lines4764.
Summary SHA256:f8c00bbcb311eeaf686ee43ef36d0597180e57c2bd70598d0fc23357c4da7998.
Summary:runs/c265-v5b-identifiers-755ab6d49ab84080ac18ff8f0699953f/summary.json.
Acceptance:docs/experiment-ledger-addendum-c265-c266.md.
Acceptance/base commit:92da414cec60028f813b8196f61b5a432f7c6b90.

Own24 PASS in10.021s;focused3525 PASS in323.929s.436 source pins/736 protected inputs verified.
Twenty frozen states completed600 wrapper forwards,86400 row presentations and2400 Full core calls.
One accepted weight-bundle load,twenty strict state loads;new training0,new learned checkpoints0.
Anchor/reference replay,compound-name evaluation,restoration,unchanged weights and saved metrics
passed. Tracked tree clean;execution HEAD preserved;run_execution_valid=True.
scientific_status=FAIL;joint_gate=False;all_replays=True;all_weights_preserved=True.

Acceptance uses immutable published log ranges,metadata and recorded local postchecks. No independent
learned-state rerun or complete-log byte rehash was performed by the reviewer. Publisher-reported
SHA256 is not a new reviewer hash. Publication is one commit after execution and adds only C265
latest.json/latest.log. Execution metadata and the registered scientific HEAD agree.

|Training arm|Doubled uu/vv|Shared prefix uu/uv|Shared suffix uu/vu|All profiles|
|---|---:|---:|---:|---:|
|standard_forward|5/5|3/5|0/5|0/5|
|standard_reverse|5/5|2/5|0/5|0/5|
|lower_forward|3/5|0/5|0/5|0/5|
|lower_reverse|3/5|1/5|0/5|0/5|
|All states|16/20|6/20|0/20|0/20|

These are whole-profile gate counts,not per-answer accuracy. A failed profile can contain correct
answers. Confirmed example:263001/standard_forward/doubled287/288,PASS. No uninspected grand answer
sum or perfect per-state totals are inferred from flags. All profiles have paired equal normal
lengths and use familiar bytes,but composition,positions and character distributions differ.
The common-suffix pattern is a limitation of this registered probe,not proof of last-character-only
processing. Same-answer collapse,swapped bindings and other errors need separate attribution.
C265 does not revoke two-fact familiar-name transfer or establish a generally superior learning rate.

Accepted C265 artifacts:
-eval-outputs.pt:546f5eb5dd62aa205c046fc5f2c7065837dc9ce578c79725c72ac451f87ae782;177035681 bytes.
-identifier-dataset.json:4bcc707da1814d765c4218f73203e175d092bea096becc593b789fbbcdb729bb;133970 bytes.
-identifier-plan.json:1a6316f251e15e29e67d22eb2d6be02407a6fa4ea6a610759b332f5bd9de53a3;2439 bytes.
-measurements.json:208943819e92e4f5cdd4f299668c86b14cba338180e1686ddd40d776b8315656;200144 bytes.
-validation-summary.json:fd2e2028c442b651b740b7e0e82ea9e326750c0052b22a9d7b072486a2988bbd;3289 bytes.

## Preserved earlier evidence and recovery

C264 bounded frozen two-fact PASS:all four arms5/5,not necessarily perfect answers.
Execution6da6c182f328cccddbdfbd94e232141b0c68c0ea;log5e62210d4b2a5b5d0cf7dbbc0fe6cf7be05d47e1.
Summary:runs/c264-v5b-two-fact-46c2297b66ba41a9b8f66f7bfca48935/summary.json.
SHA256:1c7e3d517bcf764f2b4eb89e432cb8ce303861359957f1fbfd77de9f19eb1503.
Acceptance:docs/experiment-ledger-addendum-c264-c265.md.
C263 bounded capability PASS:all four rate/order arms5/5 and8640/8640 held-assignment normal answers.
Both rates reach ceiling,so no learning-rate advantage or universal training robustness is established.
Executionabca8d7eb25146fca6f7404790071d1e6f0999d0;log1b47b5e3dc8ee3c6c2edd6972e7521b16e4f1b67.
Summary:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.
SHA256:1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21.
Acceptance:docs/experiment-ledger-addendum-c263-c264.md.

C262 valid negative:forward0/5,reverse2/5;639 paired answer differences with initial state/exposures
fixed. Chronology sensitivity is not revoked by a different later seed cohort. C261 repeated-value
4/5 versus3/5 remains negative and not independent retraining. C260 core ablation4/5 versus3/5
remains negative;no global architecture winner. C259 six-order4/5 versus two-order2/5 remains negative.
C258 diagnostic PASS only;C257 unseen-order2/5 negative;C256 bounded three-entity5/5 PASS remains.
C256 precheck INVALID and C255 invalid attempts remain in recovery addenda. C255/C254/C253 diagnostic
passes do not rescue C252. All historical identities/scopes remain in acceptance/recovery addenda
and the previous handoff at e0809d90c552471dee8723ce1b10528488f23be0. Preserve accepted code/tests/logs,
checkpoints,recovery records and tools/run_c167.ps1. No cleanup,history rewrite or CI changes.

## Active C266 — one saved query-pair diagnostic

Experiment:C266-v5b-saved-query-pair-audit. Stage:V5-B-SAVED-QUERY-PAIR-AUDIT.
One question:when only the query name changes,do saved C265 answers collapse to one value,swap the
two values,or fail differently? Use all20 states,3 profiles,2 languages,3 subsets and2 fact orders.
No new prompt is run through a model,no learned weights are loaded,and no training is performed.
This is one decomposition. Do not extend an unbounded chain of frozen-name probes. Any subsequent
training or architecture intervention needs a separate question and preregistration after judgment.

Example:aa=0;ba=1;aa= and aa=0;ba=1;ba= have targets0/1. Outcomes0/1 are both correct,1/0 are swapped,
0/0 and1/1 collapse onto a displayed value. Same outside bytes form collapse_outside;other unequal
predictions form other_different. Classify one of six exclusive pair categories,retaining every case.
entity0/entity1 categories mean first/second logical entity within the selected subset,not global
a/b or presentation positions. Record selected entity and first/last displayed position separately.
Every answer is also correct,other_entity,absent_digit(0..3 but not shown),or other_byte.
Same argmax is not identical logits:record maximum full-vector difference and exact vector equality.
Neither equality nor inequality identifies a hidden internal representation or causal parser.

Source rows are exact C264 metadata,hash8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1.
Group by language,entities,values and visible order,with the two queries sorted by original entity.
144 pairs/profile/state;8640 pairs and17280 normal answers total.720 detailed cells of12 pairs each;
120 profile/language/state summaries of72 pairs each. Reconcile correct-answer totals and every
cell's complete-query accuracy to the accepted C265 metrics. No old capability scoring is replaced.

Keep doubled as matched reference for each collision profile.80 contrasts cover20 states x2languages
x2collision profiles,all72 matched pairs each. Also show transitions within doubled-both-correct
pairs:retained,collapsed,swapped,other. Report eligibility denominator;empty denominators are null.
Keep all unconditional counts too. Do not select successful states or report conditional fractions
as independent confirmations. These are descriptive correlated outputs,not population inference.

## C266 diagnostic gate,interfaces and workload

PASS means complete and reproducible attribution. No minimum collapse fraction or desired pattern
is required. Evidence against collapse can produce a valid diagnostic PASS. capability_pass_claim=False;
causal_parser_claim=False. C265 remains negative and Gate F remains NOT PASSED.

load_reference calls actual C265.verify_artifacts(c265_dir,c264_summary,c263_summary,C265_EXECUTION),
FOUR arguments. Require parent FAIL,all whole-model counts0,and profile counts5/5/3/3,3/2/0/1,0/0/0/0.
Read fold-c265-identifiers-eval-v1 and use records[*].renamed[profile].normal,not anchor/restored.
Every saved view must be finite CPU float64 of shape288x256. Parent verification reconstructs its
original anchors,restoration,dataset and scores before new attribution. The C264/C263 summaries
listed above must already be inherited protected inputs;do not double-count them.

saved_only blocks Module calls and disallows torch.load for learned/unknown archives. Evaluation
loads require CPU weights_only=True. Actual parent verification plus explicit source acquisition
makes6 evaluation-archive loads/pass:two each from C265,C264,C263. By filename4 eval-outputs.pt and
2 evaluations.pt;count actual calls. Analysis plus persisted postcheck are two passes,12 reads total.
New model forwards0,state loads0,learned-bundle loads0,training0,new learned checkpoints0.
Historical tests,source hashing and saved-output reconstruction still consume CPU/RAM/I/O;zero
neural inference is not zero computation. Peak memory and timing are not claimed measured.

Six ignored JSON artifacts plus summary.json:audit-plan.json,pair-attribution.json,cells.json,
profile-summary.json,matched-contrasts.json,validation-summary.json. No new raw-tensor bundle or
learned checkpoint is written. Postcheck reloads source archives,recomputes every attribution and
matches persisted JSON,hashes/sizes and parent score identities. Publish only console text logs.

Protection442 source pins/748 inputs:parent436/736 plus OWN6 and C265 summary+FIVE artifacts.
Direct deciding dependency union42 includes five C231 LM sources,C230..C265 helpers and C266.
Own24;modules151;loaded3550/focused3549. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:85be4d973b9f8ce8a59e1ffa9028faceb1de3fcc8d8b3035264c2af72ed88b3e.
Registration:docs/experiment-ledger-addendum-c266-preregistration.md.
Design:docs/v5b-query-pair-audit-v0.1.md. Acceptance and registration are separate commits.

## C266 post-authoring review

post_authoring_review = PASS
review_target_HEAD = 50f2c88cbfec247f2bcea35b20adfa8984f48441
Scope:committed-byte new-file authoring validation with synthetic saved-logit fixtures,not the
complete historical checkout or actual user-local C265 artifact execution.

All six OWN files were re-fetched and read completely after publication. Complete local UTF-8
files were independently Git-blob hashed and matched to the returned remote identities:
-benchmark:fb210ac11cf443012e40a0634cff5ea13241570d;21266 bytes.
-tests:cef8aa996cb70fe896eeb7b493aaa9035199d93e;18420 bytes.
-runner:4c59ca43411df4797ad0c8b960a0166b8551095d;4518 bytes.
-launcher:b963ebc491242716e56eab2d0b832af1769c42d4;2855 bytes.
-preregistration:b637af2b33bac77ca320719e4bd5c8592405f1f8;9328 bytes.
-design:2f397e63e871c133a71fb4f5ae5484a54a8f609d;2805 bytes.

First exact own suite:24/24 PASS in4.756s.
After all six remote readbacks/blob matches:24/24 PASS in4.337s.
No code/test change was made after the first passing run. UTF-8/NUL,Python compile/import,manifest
and row-data hashes,semantic own24 count,and three embedded Python blocks passed. CLI indices:
precheck1/2/3,regression none,postcheck1/2/3/4/5. Source ordering checks inspect actual run and compute.
Recursive LOAD_GLOBAL audit traversed104 code objects with zero unresolved names using each function's
actual globals and unwrapped decorated functions. The reviewer checker initially used the wrong
namespace for contextlib's wrapper;correcting that checker required no repository code change.

Tests use synthetic saved tensors and independently computed answer/query-pair counts. There is no
learned-model evidence in these fixtures. Actual new classification,aggregation,contrasts,guards,
loader,compute,run and persisted reconstruction are exercised. Test17 verifies the four-argument
parent call. Tests18/19 use five explicitly simulated parent archive reads plus the actual sixth
read to test accounting and orchestration;they do NOT execute the real parent verification chain.
Test16 verifies blocking/restoration of Module calls and rejection of weight/unsafe loads. The
3550 dummy test IDs validate exclusion logic only,NOT execution of3549 historical tests.

Actual C265 record writer/analyze/verify fields and four-argument interface were re-read,as were
C264 reference/verification loads and C263 saved verification. The source chain supports two reads
per reference generation,6/pass in total;full runtime confirmation remains mandatory. Source
protection range/cardinality is checked synthetically and actual pin/input maps must pass on user
runtime. The existing active dispatcher was re-read and parses the selected launcher before use.
Compare C265 log commit to review target:seven additions only,acceptance plus six C266 files.
No accepted source,test,log,shared dispatcher,runner or CI file changed. Only this handoff follows.

Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu. Container raw GitHub access failed DNS resolution;
no complete repository checkout or user-local learned artifacts were available. PowerShell/pwsh
absent;Windows ParseFile was NOT executed here. Standard block parses dispatcher;dispatcher parses
selected launcher;launcher parses runner. Pending authoritative checks:Windows parser chain,actual
442/748 precheck,own24 with full repository dependencies,full3549 regression,real saved-parent
verification and diagnostic,persisted reattribution and log publication. None is claimed completed
by this authoring review. Use FINAL activation branch HEAD,not review_target_HEAD or parent HEAD.
Re-read final branch ref before issuing ExpectedHead. C267 waits for C266 judgment.

## Execution and stop

Use tools/invoke_active.ps1. Formal state has exactly one ACTIVE token resolving to C266.
Parent paths are the accepted C265/C264/C263 summaries above,fixed in tools/invoke_c266.ps1.
Order:dispatcher/launcher/runner ParseFile ->Python compile+parent precheck ->own24 ->focused3549
->saved query-pair attribution ->persisted reattribution ->log publication.
Progress includes '[C266] saved-query attribution; model calls=0; training=0'. There is no model1/20
or800-step learning loop. The final diagnostic PASS means accounting,not new model capability.

Wrong branch,dirty tracked tree,stale ExpectedHead or stale ACTIVE:operational SKIPPED before logging;
no scientific execution or log publication. Source/artifact/schema/nonfinite/count/reconciliation/
test faults require minimal SAME C266 recovery;no C267 on an invalid attempt. Do not alter categories
or discard profiles to obtain a preferred diagnostic story. Log-only publication failures are
repaired without repeating completed analysis. The user normally sends only 'finished';fetch
C266 latest.json/latest.log for judgment. Do not move this branch with unrelated work during execution.
No paid API,external corpus,model expansion,production adoption,cleanup,history rewrite or CI change.
Preserve all accepted evidence/recoveries and tools/run_c167.ps1. Judge C266 before C267.
