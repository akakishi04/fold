# C264 acceptance and C265 compound-identifier boundary

## Formal verdict

C264 ACCEPTED PASS (bounded frozen three-to-two-fact transfer).
All four arms pass 5/5, hence all twenty states satisfy the preregistered new-task gate.
This is not a claim of perfect answers,arbitrary-length reasoning,or learning-rate superiority.
C263 bounded PASS and all earlier verdicts/recoveries remain unchanged. Gate E PASSED;
Gate F NOT PASSED. No architecture,optimizer default or production change.

Scientific execution HEAD:6da6c182f328cccddbdfbd94e232141b0c68c0ea.
Published log commit:5e62210d4b2a5b5d0cf7dbbc0fe6cf7be05d47e1.
Publisher log SHA256:f228c6ede8e95546c6e534a4afcde97255e69fe38d0692b2293e71f35c2ad445.
Log bytes:779217;lines3980.
Summary SHA256:1c7e3d517bcf764f2b4eb89e432cb8ce303861359957f1fbfd77de9f19eb1503.
Summary:runs/c264-v5b-two-fact-46c2297b66ba41a9b8f66f7bfca48935/summary.json.
Model-source C263 summary:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.
The log-publication commit immediately follows the registered execution commit and changes only
C264 latest.json/latest.log. Acceptance uses immutable published log ranges,metadata and recorded
local postchecks. The reviewer did not independently execute learned models or rehash the entire
log. The publisher-reported SHA256 is not a new reviewer complete-byte hash.

## Execution validity

Own24 PASS in13.519s;focused3501 PASS in316.942s.430 source pins/723 protected inputs verified.
All20 frozen C263 final states evaluated:600 wrapper forwards,120960 row presentations,2400 core
calls. One accepted model-bundle load,20 strict state loads;new training0,new learned checkpoints0.
Accepted original-output replay,new two-fact scoring,restoration,weight preservation,provenance
reconstruction and saved-output metric reconstruction passed. Tracked tree clean;scientific HEAD
preserved;run_execution_valid=True;scientific_status=PASS;joint_gate=True.

## Deciding metrics

|Arm|Whole-seed passes|
|---|---:|
|standard_forward|5/5|
|standard_reverse|5/5|
|lower_forward|5/5|
|lower_reverse|5/5|

Each state is scored on288 unique two-fact prompts,12 language/subset/order cells and six
language/subset two-order-consistency cells. All meet the unchanged preregistered thresholds.
Do not infer perfect scores from the PASS flags. Confirmed examples:
-standard_forward263001:288/288;
-lower_reverse263005:286/288. Its EN a/c cells each score23/24,paired-query11/12,and the same
assignment/query group misses across both orders,two-order consistency23/24. Other cells shown
for that model are24/24. This is a valid threshold PASS,not an integrity fault.
No uninspected per-state totals or a grand exact-accuracy total are asserted by this acceptance.

## Interpretation and limits

These frozen models can answer with two of the three familiar named entities after deleting an
unqueried fact. They are not restricted to exactly three visible facts on this finite task.
Fact count,effective length and positions changed together;no unique internal mechanism follows.
Reduced prompts use familiar name characters,values and pairwise associations. Projection can
cross the old TRAIN/HOLDOUT partition;the deduplicated reduced task is not a new disjoint split.
It is not evidence for arbitrary names,lengths,ordinary language,core superiority or a learning-rate
advantage. All four existing cohorts remain;no seed selection or parameter update is authorized.

## Accepted artifacts

-deletion-plan.json:a4cfef0b148d7f2130324127f51217d03c191bf788b87d07d52b1d67890095b1;2398 bytes.
-eval-outputs.pt:3123aa3b0c2e74b1a069edeb56da5a52046fc5731f681656abf51d4200db55b3;247882609 bytes.
-measurements.json:34c43a5eea6aa235a7bcf8451f3742393a53255a63299c43874c5bf948b87f99;63095 bytes.
-provenance.json:35f96556b849adeac41cc04cc77d91c94ba4e560783d0f58c67e3898ea479577;114338 bytes.
-two-fact-dataset.json:8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1;39746 bytes.
-validation-summary.json:171731535a0f725e5cfb5912828e8c082c5950507a9dade64cf43463fe304a14;1445 bytes.

## Next question, not activation

Can these same twenty frozen states bind two-symbol identifiers constructed exclusively from
familiar identifier characters,including names sharing a prefix or suffix? Keep two facts,distinct
values,queries,targets,all subsets/orders and both languages. For each source pair of characters
u,v,predefine three equal-length naming profiles:uu/vv (doubled),uu/uv (shared prefix),uu/vu
(shared suffix). For example aa=0;ab=1;ab= must answer1. Replace names consistently in both facts
and query;do not translate the new names back before model inference. Include every profile,
not just the one that works. No new byte value,no training,no checkpoint selection.

The equal-length doubled control distinguishes some consequences of longer identifiers from
shared-character ambiguity;it does not uniquely identify an internal parsing algorithm. New names
and increased token positions remain a joint distribution shift. Define separate per-profile
scoring and whole-model gates before execution. C265 requires separate implementation,
preregistration and committed-byte review before activation. C266 NOT REGISTERED.
