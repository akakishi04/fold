# C294 preregistration — saved support/choice audit

Experiment:C294-v5b-saved-support-choice-audit. Stage:V5-B-SAVED-SUPPORT-CHOICE-AUDIT.
Acceptance base:8bdfdeae1daeab051af6407e5101578e66c1d06f.
C293 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C295 NOT REGISTERED.

## One scientific question

When a retained C293 normal output chooses a class outside the two stated fact values,is the
correct fact value still ranked above the other fact value,or is within-fact selection also wrong?
This is a saved-logit diagnostic with oracle fact support,not a new decoder or training policy.
All15 models,seeds293001..293005 and ce_only/scaled_ce/support_weighted remain. No success filtering.
All2/3/4 tasks,three profiles,English/Japanese and original TRAIN/HOLDOUT value splits remain.
Four-character TRAIN refers to trained value combinations at an UNTRAINED length.

## Parent/schema/authority

C293 execution:318d9fd76f4253b30d68645ee34c124457be78a3.
Published log:3d35190c718b8b3c52e5c68120358ba96811466e.
Summary:runs/c293-v5b-fact-support-834c844c03c84023bc4ef1c6d32e3067/summary.json.
Summary SHA256:61a92e5d5775381cc1b7ef0fa19a9fa393197afd05a7642b74b0486ab6d338e6.
Parent source:fold_lm/v05_benchmarks/model_c293_fact_support_loss.py.
Parent Git blob:9514bb3db5abfac91666ee67b1e1973511a2b682.
Verify20 ordered summary hashes BEFORE dispatch:C293,C292,C291,C290,C289,C288..C274. Ancestor
hashes are taken from the immutable C293/C292/C291/C290/C289 constants,never mutable latest files.
Invoke exact C293.verify_artifacts(parent_dir,19 ancestor paths,accepted execution HEAD). It checks
all8 parent artifact names/hash/size descriptors committed by the exact parent summary hash and
reconstructs full original masked gates,loss traces,matching and saved results. Require parent
FAIL,exact15 seed results and all_groups_matched/all_replays True. Parent quad counts2/1/2 and
seen-length4/4/4 remain fixed. Never infer validity from publication alone.

Read verified dataset.json and fold-c293-support-eval-v1 records.raw[task][split][profile][view].
Only final NORMAL logits are used by the new audit. The parent verifier still checks every old
normal/evidence-blind/query-blind capability gate. No checkpoint is loaded into a model.
C267 logical data map target=48+values[entities.index(query)]. Fact values are distinct0..3.
The unordered support is sorted(48+v for v in row.values),independent of the requested target,
predicted answer or fact ordering. Validate target binding but never use it to pick the winner.

## Exact measurements and tie handling

Keep full256-class argmax unchanged. Separately record the higher-scoring class from the two
input fact values. Both argmax operations resolve exact ties to the lowest numeric class index;
the conditional support is sorted,so ties are never resolved by putting the target first.
Record exact within-support and support-versus-best-outside ties,without any fitted tolerance.
Record target-minus-other logit margin and best-supported-minus-best-outside margin.

Each normal answer belongs to exactly one category:
1.full_correct;
2.outside_correct_choice:full winner is outside support,but conditional fact choice is correct;
3.outside_wrong_choice:full winner is outside support,and conditional fact choice is wrong;
4.other_fact:full winner is the other stated value.
A full-correct answer cannot become conditionally wrong under the consistent tie rule. Assert
this and full-in-support implies unchanged conditional winner. These are mathematical consistency
checks,not empirical evidence that a support-restricted decoder is implemented or deployable.

Compute log-softmax stably and derive per-row CE=-log P(y),Lsupport=-log(P(v0)+P(v1)),and
Lchoice=-log(P(y)/(P(v0)+P(v1))). Require CE=Lsupport+Lchoice with rtol/atol1e-10. Check all
numerical inputs/derived values are finite;never silently clamp nonfinite values. Record support
mass and all three losses;support mass above1/2 does not imply the full argmax lies inside support.

Persist38880 normal row observations=15models*3tasks*3profiles*(192+96). Preserve source ID,
language,profile,query,fact values,original prediction,conditional prediction,categories,margins,
ties and losses. Reconstruct all540 original profile/language normal counts and collapse against
parent metrics. Reconcile90 final partitions' original rows,correct counts,output-role counts and
normal NLL against the parent summary. Do not replace or relax old gates using conditional accuracy.

Report90 model/task/split aggregates and540 profile/language aggregates. Compare support_weighted
to CE and scaled CE on aligned source/profile/task/split rows:60 comparisons/25920 rows,including
original and conditional argmax changes,rescues/regressions and complete4x4 category transitions.
All pairings/denominators are fixed. Dependent rows are not additional statistical replicates.
No coefficient sweep,new seed selection,training extension,temperature or answer-time filtering.

## Scope,workload and protection

Scientific model forwards,training,model-state loads,new checkpoint writes,row presentations,
core calls and network calls are0. Reading saved tensors and scoring numerically are allowed.
Block Module calls,load_state_dict and torch.save under no_grad. Operational regression work is
separate. PASS means exact diagnostic integrity only;capability_gate_applicable=False.
The oracle-support view uses privileged task structure from verified data. It is not a capability
score,causal proof,production decoder,or proof a learned support extractor would behave similarly.
An unsupported output with wrong within-support rank can have multiple causes;do not label a
hidden attention/memorization cause from these numerical categories. Gate F remains NOT PASSED.

Outputs:audit-plan.json,support-choice-report.json,validation-summary.json plus full summary.json.
Verify all output hashes/sizes and rebuild every artifact independently from the old saved logits.
Console:compact receipt and90 partitions/60 comparisons;full maps/row reports stay local/ignored.
Only direct repository import:C293. Retain/check all604 parent pins and1091 inputs. Require parent
blob and repository-local modules exposed by its context/core bundle in the inherited map.
Add6 OWN and9 parent summary/artifact files:source610/protected1106. No accepted file changes.
Own32/modules179/loaded4390/focused4389;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:e929d73dabbcc3c6c229c46282854f8c196802e4e52995f10eb94b977b9ba1c6.

## Authoring and execution

Commit,re-fetch all6 OWN and complete independent post-authoring review before activation.
Explicit UTF-8 text reads and a CP932-default emulation test are required. Validate the real
parent,20 hashes,protection and complete numerical dry-run;then own32 and actual focused4389.
Keep dispatcher/selected-launcher/runner ParseFile chain. Validate failure skips science/publish.
Scientific integrity failure retries SAME C294 without changing conditions. No C295 registration
before C294 judgment. No prior verdict changes or automatic Gate F promotion.
