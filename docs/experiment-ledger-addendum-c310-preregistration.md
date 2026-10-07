# C310 preregistration — saved value-renaming consistency

Experiment: C310-v5b-saved-value-renaming. Stage: V5-B-SAVED-VALUE-RENAMING.
Acceptance base: 2cffcea33045a75582a94fadd963fa9f2b7d601d.
C309 remains ACCEPTED VALID NEGATIVE; C308 remains its bounded ACCEPTED PASS.
Gate F NOT PASSED. C311 NOT REGISTERED. No new scientific result is claimed here.

## One question

With names, query, fact order, language and identifier length held fixed, does the saved answer
transform with a bijective relabeling of values0..3? Separate comparisons that cross original
TRAIN/HOLDOUT value splits from those that stay within a split. C309 fitted normal TRAIN but
still failed HOLDOUT on some seeds. No memory, attention or initialization mechanism is assumed.
Retain all15 C309 states: seeds309001..309005, full_train/core_frozen/core_slow, lengths2/3/4/5,
all three profiles, English/Japanese and every logical row. Only final normal logits enter the
new comparison. The exact parent verifier reconstructs the old masked/full gates unchanged.
No training, model inference, coefficient search, new seed search or new data.

## Parent identity, semantics and dispatch

Scientific execution HEAD: a38c6ff864ab40efa74397017cfeec9f5628ca11.
Published log commit: c3935db64960b7e90325672aa880318a6eed77e2.
Summary: runs/c309-v5b-core-lr-replication-e24b3b724e47415eae204d3084a68185/summary.json.
SHA256: c8a1a2bd3d6ad4e4d6f714b38af3ce8424d314d1f5771b5fca578d49df37066c.
Parent source: fold_lm/v05_benchmarks/model_c309_core_lr_replication.py.
Parent Git blob: 8c66d64aa7ca3558d914a9b34bc9612ef444a9c2.
C304 wide source Git blob: cacb5852a29171aa8079e634d929fdd54e7f4f58.
Dataset SHA256: 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

Verify36 ordered summary hashes BEFORE C309.verify_artifacts(parent_dir,35ancestors,acceptedHEAD).
The first is C309; the rest come from immutable C309.parent_hashes(C308). The exact summary seals
all7 descriptors. Require parentFAIL, complete15 seed flags, candidate_gate=False, all_replays=True
and all_groups_matched=True. The parent verifies every descriptor and reconstructs all old scores,
schedules, gradient histories and freeze/LR invariants. No missing source protection is waived.
The writer saves FINAL frozen logits in raw[str(length)][split][profile][view], not interim or
selected action outputs, in fold-c309-core-lr-replication-eval-v1. C310 reads this archive with
weights_only=True, plus the verified dataset. It never loads a checkpoint into a model.
C267's exact dataset is validated and hashed. Original metrics are
metrics[i].length_scores[str(length)].totals. C304 maps repeat/shared_prefix/shared_suffix to
C270's tripled/shared_prefix2/shared_suffix2 scorer names; C310 uses this exact adapter.

## Exact relabeling and controls

Every row has two distinct entity values. TRAIN+HOLDOUT includes every ordered distinct value
pair for each fixed language/entity set/fact order/query. Concatenate TRAIN192 then HOLDOUT96,
keeping IDs and split membership. Lookup by (language,entities,values,order,query). For each of
all24 permutations, replace only values and locate the already evaluated counterpart. Require
valid domains and target binding, unique IDs, complete bijections and matching renamed targets.
The names, query, order and language are unchanged in every comparison.

Use full256-class argmax with the original smallest-index tie rule. Permute ASCII48..51 only;
all other252 classes are fixed. No restricted decoding or answer correction. Record every tied
maximum's row index/count: deterministic argmax may break equivariance on a tied distribution.
This is hard-prediction consistency, not full-distribution or hidden-state equivariance.

Each row has22 permutations that change the displayed values. Two preserve the input: identity,
and the swap of the two absent values. Report these separately:
- changed input, divided by source/destination TRAIN/HOLDOUT;
- absent-value-only swap, divided by source split;
- identity controls, which must have zero violations.
An absent-value swap can reveal an unsupported value prediction, but is not evidence of handling
a new input. Each alternative displayed value pair appears under two full permutations because
the absent values can map either way. Keep both: the output maps differ for absent predictions.
Comparisons are directed and dependent, not independent trials, extra seeds or a sample size.

## Correctness and reports

Each group records comparisons, equivariant/violations, both_correct/both_wrong, correct_to_wrong/
wrong_to_correct, equivariant_wrong, left/right correct and same_prediction counts. Validate
integer types and algebraic conservation. Always choosing the other fact is consistent and wrong;
a constant non-value byte is trivially consistent too. Neither is a capability success.

Original observations:15*4lengths*3profiles*(192+96)=51840.
Changed-input comparisons:1140480 in240 model/length/split-transition groups.
Absent swaps:51840 in120 model/length/source-split groups.
Identity controls:51840 in60 model/length groups.
Per model/length changed counts in TT/TH/HT/HH order:8064/4608/4608/1728.
Absent counts TRAIN/HOLDOUT:576/288. Identity count:864.
Reconstruct all720 original split/profile/language totals: correct, rows, pairs and collapsed pairs.

Full report:288 source IDs,24 permutations with288 destination indices each,60 model/length
blocks of predictions for all3 profiles, tied-max indices,720 original totals and aggregate summary.
These arrays reconstruct all comparisons without a million redundant row records. Nothing is
filtered. Masks remain in the original verified archive, not newly evaluated renamed conditions.
Outputs: audit-plan.json, value-renaming-report.json, validation-summary.json, plus summary.json.
JSON only, explicit UTF-8. Verify each output's hash/size and independently rebuild from the old
verified evidence. Console mirrors a compact receipt and all420 groups; full index/prediction
arrays stay local/ignored. Do not commit datasets, weights or evaluation tensors.

## Workload, protection and gates

Scientific model_forward_calls/train_steps/model_state_loads/new_checkpoint_writes/row_presentations/
core_forward_calls/network_calls all0. Saved tensor reads and argmax are allowed. Under no_grad,
block Module calls, load_state_dict and torch.save. No optimizer/backward. CPU numeric work uses
2threads. Operational regression fixtures are separate; zero model calls does not mean zero work.
Sole direct import C309. Check actual repository-local parent/context/wide/core/factory-language
helpers and C304.PINNED. Keep700 parent source pins and1309 inputs; add OWN6 plus8 parent files:
source706/protected1323. No accepted source/test/preregistration/log/dispatcher modifications.
Own32/modules195/loaded4942/focused4941. The sole inherited exact C204 exclusion is unchanged.
Manifest SHA256: 0b4304400ddb57789a52aefb0bfe84690df7bb3fee9ef4c63e842fecfd595596.

Before activation: commit/refetch/review OWN6; test a scalar reference oracle, all bijections and
inverses, exact split denominators, consistent wrong outputs, ties, parent totals,36-hash dispatch,
source/input guards, actual run/loader order, persistence and altered-output rejection. Integrate
the actual accepted C270 score function in a controlled fixture. Local support can be a fetched
function slice, not a full clone. Explicit UTF-8/CP932 checks cover real new files; audit global
bindings, all3 embedded Python blocks and36-parent CLI indices. Never report unexecuted tests PASS.
Windows Validate requires all36 actual parent archives/pins, a full real-data audit dry-run,
own32 and full4941 regression. Maintain the dispatcher/launcher/runner ParseFile chain.
PASS means diagnostic integrity only, regardless of consistency rate. C309's negative and C308's
bounded PASS stay unchanged; Gate F stays NOT PASSED. Do not change cohort, predictions, data
splits, thresholds or output mappings after results. Integrity failure repairs SAME C310.
Validate failure skips science/publication. C311 waits for C310 formal judgment.
