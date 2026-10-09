# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C315 ACCEPTED VALID NEGATIVE. C316 ACTIVE / NOT YET JUDGED. C317 NOT REGISTERED.**
C316 is the unique ACTIVE fresh-seed short-mixture replication;no scientific outcome yet.
C314 diagnostic PASS;C313/C312 negatives;C308 bounded PASS/C309 negative remain unchanged.
Latest accepted scientific execution:5708562420e530749a8f63b1f4baf3c7e0f28029.
Latest accepted publication:0b4ce1c953d2ccf0eea04747b1194c6dd70729ee. Do not rerun C315.

## Latest accepted evidence — C315

Acceptance:docs/experiment-ledger-addendum-c315-c316.md.
Acceptance commit:0d83544dfeb835a5c74f9690008598872f3e0f2d.
Summary:runs/c315-v5b-single-mix-dbdffe0b88094f729d1dbfbcdba520f0/summary.json.
SHA256:aceda00cebf61b49e5f923bf7c426e2f4522dcac68444fc2e07b27a17b63dd66.
Own32/focused5085 PASS;736sources/1379inputs;run_execution_valid=True;all_pairs_matched=True.
Both arms5/5 at2..5;unseen6 control3/5,candidate4/5. Paired3both,1candidate_only,0control_only,1both_fail.
Candidate rescues315004 (six573/576,284/288 ->576/576,288/288).
315002 remains negative (566/576,283/288 ->574/576,286/288).
Total six normal errors22->4. This does not imply per-row rescue/regression counts not measured.
Every normal2..5 partition perfect. Single-character candidate diagnostics all perfect192/192,
96/96;control misses one315001 HOLDOUT and one315004 TRAIN answer. Length1 is not a six gate.
Fixed1200update allocation differs:control2/3/4x100,candidate1/2/3/4x75. Not isolated breadth or cause.

## Active C316 — unchanged short-mixture replication

Experiment:C316-v5b-single-mix-replication. Stage:V5-B-SINGLE-MIX-REPLICATION.
Registration:docs/experiment-ledger-addendum-c316-preregistration.md.
Design:docs/v5b-single-mix-replication-v0.1.md.
Review:docs/c316-post-authoring-review.md.
Acceptance base:0d83544dfeb835a5c74f9690008598872f3e0f2d.
Authoring/review target:81b37e65a138c19edf22a90ebd1f9871ca02f56a.

One question:does the fixed C315 one-character allocation reproduce unseen-six reliability in
one new paired cohort? Initial seeds316001..316005,order seeds316101..316105. Both original arms
remain:two_to_four control,one_to_four candidate. No old model/checkpoint/good-core reuse.
Only the initial and order seeds change. This is one fixed replication,not repeated seed searching.
Primary:all5 NEW one_to_four states pass six local/masked gates. Never pool C315 successes to
compensate for a failed new state. C315's negative stays regardless of C316 outcome.

Control original TRAIN row exposure by length1/2/3/4:0/100/100/100;candidate75/75/75/75.
Both300epochs*4batches=1200updates and57600training row presentations/model. Actual inherited
C315.plan_for_order uses private randperm96(order+306000+epoch),24 intact two-query pairs/batch.
All original192 TRAIN rows once/epoch. Logical row order matched across arms;length/profile
rendering differs. Check every epoch/exposure and original C312 random control schedule.
Length1 has one canonical repeat profile,not three degenerate copies. Candidate dilution of
longer-length exposure and profile-timing changes remain explicit. Five/six,HOLDOUT and masked
views never enter training. All C3151..6 prompt bytes and original splits remain identical.

Model unchanged:actual C304 LengthReadout,14256parameters/core3328,64slots,all trainable.
Actual C308 core_slow optimizer:coreLR.0005/noncore.005,ordinary meanCE,AdamW betas.9/.999,
eps1e-8,weight_decay0,globalclip1 before step,FIT_RNG612000,CPUfloat64,threads2,deterministic.
No new mechanism,gain,teacher,auxiliaryloss,earlystop,decoderrestriction or budget extension.
Both arms start with identical whole/core fingerprints and independent parameter storage.
Discarded common-input bilingual length1/2 checks compare exact initial outputs,preclip gradients
and first optimizer step. Actual first minibatches/losses may differ as intended.

Reuse actual C315 plan_for_order,schedule_stats,training_tables,validate_prompts,validate_raw,
evaluate,replay. Its old-seed fit/schedule/factory/analyzer are not called with new seeds and
parent globals are never patched. Child explicit-schedule optimize matches C315.fit's numeric
operation order. New seed-aware factory/analyzer and checkpoint loader own the new identities.
Final frozen evaluation1..6 is144forwards/13824rows,with length1 only one profile. Strict parent
replay checks all views<=1e-9 and exact argmax. Report100 length2..6 partitions,20 descriptive
length1 entries and paired six outcomes. Original thresholdsaccuracy.90/query_pair.80/
evidence_drop.35/query_drop.35/two_order.80 remain. One-character scores cannot rescue six failure.

## Parent contract,protection and workload

Verify42 ordered summary hashes BEFORE C315.verify_artifacts(parentdir,41ancestors,acceptedHEAD).
Fixed parent summary seals all7 artifacts. Require acceptedFAIL,exact old ten3/4 six flags,
all_pairs_matched/all_replays. Read canonical dataset.json and length-datasets.json from C315
itself,not a diagnostic-only ancestor. Recheck data/prompt hashes and original renderer contracts.
No parent learned state or saved prediction supplies initialization or new learning labels.

Sole direct import C315;its context supplies the already protected C314/C313/C312/C310/C308/
C304/C296/C287/backend helpers. Retain736source pins/1379inputs with explicit C315 blob,
C315.PINNED,C304.PINNED and actual local/factory-language coverage. Add OWN6+8parentfiles:
742sources/1393inputs. No accepted file modification,new regression exclusion or protection waiver.

Science10models,12000updates,576000training rows,14880model forwards,852480row presentations,
59520core calls,10strict state loads,one new10-state model-bundle write/read,network0.
Final evaluation and replay included;operational probes,tests and recursive verification separate.
Seven artifacts plus summary:architecture-plan.json,dataset.json,length-datasets.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Schemas:
fold-c316-single-replication-models-v1 and fold-c316-single-replication-eval-v1. Actual child loader
is called once after all10fits and before all10replays. Save all1200 losses/LRs/gradient receivers,
events/exposures,full/core initial/final hashes and all final logits. No overwrite. No-neural
postcheck reconstructs scores,schedules,primary and JSON content;hash/size checks include tensors.
Full arrays remain local/ignored;compact receipt and aggregate results are mirrored to the log.
Own32/modules201/loaded5118/focused5117;sole inherited exact C204 exclusion unchanged.
Manifest:e77e05efffb480bce89fb9b16071babfff15dd533d0ac6677798478fd2103718.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus executed local software tests).
All6 OWN refetched at81b37e65a138c19edf22a90ebd1f9871ca02f56a,independently Git-blob-matched6/6.
After matching,an initial full-suite call hit the local45s limit and is not counted as PASS.
Completed nonoverlapping partitions01..16/17..32 cover all32 unique IDs in each mode:
normal16/16 PASS18.515s plus16/16 PASS12.764s;CP93216/16 PASS20.008s plus16/16 PASS13.385s.
No test omission/change. CP932 patch covers import/setup/tests/teardown in each partition.
Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5;PowerShell absent. UTF8/noNUL,Python+3embedded
blocks compile,recursive unresolvedglobals0,manifestselfhash matches;42orderedpaths/CLI verified.
Actual C315 fit/scheduler ASTs versus child loop match all1200 losses/gradient traces/final weights
for BOTH arms on controlled models. Actual train/evaluate/replay counts,42hash guards,742/1393
protection,child loader/run order,semantic suite IDs and persistence/tamper cases pass.
Local parent support is fetched exact function slices,not full modules/repository,and NOT committed.
Synthetic label-encoded toy inputs/padded models and substituted parent/Git/scorer/suite interfaces
are software controls,not actual FOLD competence or actual5117 inherited regression evidence.
Mandatory user gates remain:42real parents/Windowspins,PowerShellParseFile,real bilingual initial
probe,own32/full5117regression and all10 actual fits/evaluations/replays. Activation preserves OWN6.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C316 -> Validate(42parents,742/1393,
unchanged C315 policy,new schedules/initial bilingual probe,own32,focused5117) ->
authoring_runtime_preflight=PASS -> Execute(10newmodels*1200updates,all1..6evaluation,strict
replay,new-only six gates,saved reconstruction) -> log publication.
Validate failure skips science/publication. Integrity failure repairs SAME C316 with conditions
unchanged. Valid new six5/5 failure is ACCEPTED VALID NEGATIVE. No post-result seed/mix/LR/budget/
gate changes. C317 waits for formal C316 judgment. Earlier verdicts and Gate F NOT PASSED stay.
Separate scientific execution HEAD from later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted seals and immutable historical tests.

## Historical state

Pre-activation handoff:docs/handoff-history/c316-pre-activation.md.
Git blob:7ddcb9311c04eea1c7c520241fea997eb065dc2a.
Earlier handoff:docs/handoff-history/c315-pre-acceptance.md.
Git blob:c5c146cad014d825bc0f2fb5320afd95ae87cce7.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
