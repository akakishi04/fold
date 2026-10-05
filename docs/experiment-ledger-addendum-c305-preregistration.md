# C305 preregistration — aligned saved length-error overlap

Experiment:C305-v5b-saved-length-error-overlap. Stage:V5-B-SAVED-LENGTH-ERROR-OVERLAP.
Acceptance base:75b6545c1dc1d570286e76bb0b53473673247d33.
C304 ACCEPTED VALID NEGATIVE;Gate F NOT PASSED;C306 NOT REGISTERED.

## One question

Which five-character errors already occur for the same logical question at four characters,
and which appear or disappear when only the rendered identifier length changes? C304's full
four/five gate flags match in all15 models,but aggregate flags do not establish error overlap.
Use four as the primary reference;two and three are descriptive additional references.
Keep all15 C304 models,all5 seeds304001..304005 and all3 arms,four_only/three_four/two_three_four.
Do not train,execute a model,select successful models or introduce a corrected/restricted decoder.

## Parent evidence and semantic contract

C304 scientific execution:f309fde3e2aa8df33156ce55c703c9c37c6e106b.
Publication:e54f443acbbc5e55d3dcab18d08c418d56867d1e.
Summary:runs/c304-v5b-length-breadth-5090e7ce18a8444e9095afe14ad41266/summary.json.
SHA256:c4b0babc2f7b9ea544c96385ed386a721630ce81bfb26fcb5e1e028450670717.
Parent source:fold_lm/v05_benchmarks/model_c304_length_breadth.py.
Git blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify31 ordered summary hashes BEFORE exact C304.verify_artifacts(parent_directory,30 ancestors,
accepted_execution_HEAD). Tail is C304.parent_hashes(C303). The exact summary seals all7 parent
artifact descriptors;the exact verifier reconstructs prompts,schedules,full/masked scores and
replay attestations. Require FAIL,all_groups_matched/all_replays and exact original15 length-pass
records. Five pass counts3/2/2 are not changed. Read verified dataset.json,length-datasets.json
and fold-c304-length-eval-v1 evaluations.pt. Do not load trained-models.pt into a model.

The writer saves final frozen logits as records.raw[str(length)][split][profile][view]. Each
prompt item has source_id,target and view strings. These are final full256-class outputs,not
intermediate training predictions. The child matches every prompt source_id/target to the same
canonical logical row in every length/profile. It never aligns by rendered text equality or
sorts independently generated logits. Preserve model,split,profile,language,query and target.

C304's nested length_scores intentionally use canonical triple-profile labels. Reconcile all
720 length/profile/language normal totals by an explicit repeat->tripled,shared_prefix->
shared_prefix2,shared_suffix->shared_suffix2 map. Verify rows,correct,pairs and collapsed pairs.
Also reconcile120 model/length/split normal partitions. Existing masked/full gates remain solely
the unchanged parent's gates. This audit does not reinterpret them or lower thresholds.

## Observations and statistics

There are12960 aligned logical questions=15models*3profiles*(192TRAIN+96HOLDOUT),each with four
predictions at lengths2/3/4/5,for51840 saved normal predictions. Preserve exact argmax over256
classes and first-index tie behavior. No new neural row presentation occurs.
Persist one row per aligned question with all four predicted bytes and a four-bit correctness
signature in length order2,3,4,5. All16 signatures,including zero-count ones,are reported in30
model/split groups. No signature is treated as a learned internal program or length rule.

For each reference length2/3/4 versus5,report both_correct,reference_only(new error at5),five_only
(recovered at5),both_wrong. Split both_wrong into identical and different wrong answer bytes.
Count exact answer flips and reconcile net correct-count differences. Report90 model/split/
reference groups and540 profile/language subgroups. Four->five is the deciding descriptive view.
Ratios include persistent errors / all five-errors and newly introduced errors / reference-correct.
Use null,not zero or1,when a denominator is zero. Always retain counts and denominators.
An error persistent across lengths does not prove memorization;an error appearing at5 does not
identify attention or representation failure. Every row is dependent on its model and original
logical facts;these are not12960 independent trials or new seeds. No causal attribution to length
breadth from this diagnostic;C304 allocation and temporal-spacing confounds remain.

## Protection,workload and outputs

Sole repository import C304;retain its full670 source pins and1243 protected inputs. Check actual
repository-local parent/context/core-helper module coverage and unchanged Git blobs/files.
Add OWN6 plus8 parent summary/artifacts:source676/protected1257. No accepted files or dispatchers
are edited. No new historical regression exclusion. Parent helper semantics are inspected rather
than guessed from similarly named older tasks.

Science training,model forwards,row presentations,core calls,model-state loads,new checkpoints
and network calls are all0. Reading saved evaluation tensors and computing argmax is allowed.
Guard torch.nn.Module calls,load_state_dict and torch.save under no_grad. The same guards cover
parent numerical verification and child reconstruction. Operational regression fixtures may use
models separately;they are not part of the scientific workload.
Outputs:audit-plan.json,aligned-answers.json,validation-summary.json plus summary.json. No model
checkpoint or copied dataset. Serialize deterministic UTF-8 JSON;verify every output hash/size and
independently rebuild it from the sealed parent. Full aligned rows and detailed subgroups remain
local/ignored. Console mirrors90 transition groups and30 signature groups plus a compact receipt.
PASS means diagnostic integrity only,regardless of overlap distribution. C304 remains negative,
Gate F remains NOT PASSED,and no per-question best-of prediction is produced.

## Review and execution gate

Own32/modules190/loaded4782/focused4781. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:844119479e6a43fc9fa5d3510ce05d8300ed2108dd819c6058b24b3b449632bd.
Commit all6 OWN,re-fetch immutable remote bytes and complete separate post-authoring review before
activation/command release. Compile both Python files and3 embedded blocks;check free-name binding,
UTF8/CP932,31 argument paths,postcheck slice[2:33]/HEAD[33]/argc34 and semantic suite identities.
Mandatory Windows Validate:31 parent hashes/verifiers,676/1257 protection,full real-data alignment
dry-run,own32 and focused4781. Preserve dispatcher/selected-launcher/runner ParseFile chain.
Validate failure skips scientific execution/publication. Integrity failure retries SAME C305.
Do not change cohort,reference lengths,alignment,thresholds or counting rules after seeing output.
C306 stays unregistered until formal C305 judgment.
