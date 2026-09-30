# C290 preregistration — saved pair margin versus independent answer correctness

Experiment:C290-v5b-saved-pair-margin-audit. Stage:V5-B-SAVED-PAIR-MARGIN-AUDIT.
Acceptance base:4ffae6420500e0233c1b19df07f6f0cfac73c16d.
C289 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C291 NOT REGISTERED.

## One scientific question

On the retained C289 outputs,does satisfying the existing supervised assignment margin coincide
with both individual answers being correct,and which exact answers change when the auxiliary is
withdrawn after400 updates? The margin/correctness cross-tab is primary;aligned withdrawal versus
both anchors is its interpretation control. No new training policy is tested here.

## Exact parent and writer contract

C289 execution:b5026f48e0c8b39bbfb9069f34271d7b6ba9d50f.
Published log:b96ab8b01ec9c9eb876fada8339c8c0e0d0a8e12.
Summary:runs/c289-v5b-early-pair-ac332442137243e68d4ec3bd754ba717/summary.json.
Summary SHA256:151117fcd43177b8e393eeee6935222e54f01caecf8a17b4656149aec5058897.
Parent source:fold_lm/v05_benchmarks/model_c289_early_pair_withdrawal.py.
Parent blob:d5e2231d1d1a1e39b5628129f3ca2ef9838c9951.

All16 ordered summaries are checked:C289 plus C288..C274. The latter15 hashes are obtained from
immutable source-pinned C289.SUMMARY_SHAS,not guessed or taken from a mutable branch tip.
The exact parent summary hash commits every parent artifact name,SHA256 and byte size. Require
exactly its eight OUTPUTS,then invoke C289.verify_artifacts(parent_dir,15 ancestor paths,
accepted execution_HEAD). That verifier checks all eight hashes/sizes and reconstructs complete
old metrics,objective histories,shared400-prefix and original gates before C290 reads any logits.
Using the parent-summary seal avoids copying an unchecked output hash from an older experiment.

Require C289 FAIL,candidate_gate=False,all_replays/all_groups_matched/all_auxiliary_prefixes_matched
True and exact15 published seed_results. Quad3/0/0;two/triple3/4/4;TRAIN direct4/5/4;
seen HOLDOUT direct3/4/4. All15 models are retained,not only the well-fitted models.

Read dataset.json and the hash-verified fold-c289-early-pair-eval-v1 archive. Its records contain
raw[task][split][profile][view] final frozen logits,not scores from the training step400 state.
Only normal logits are used for the new pair analysis. Parent verification still checks every
original masked evaluation and fixed task gate. No checkpoint is loaded into a model.
C290 accesses the exact C289 context's final helper bundle;every reachable helper remains pinned.

## Fixed pair-level measurement

Tasks two_char,triple,quad and their three original profiles remain unchanged. TRAIN/HOLDOUT
are inherited value splits;four-character TRAIN was not optimized at length4.
For each task/profile/split,group the original logical rows by language,entity pair,value pair,
fact permutation. Sort the two rows by query identity and verify distinct labels and exact pairing.
Use all96 TRAIN query pairs and48 HOLDOUT pairs per profile. Do not recombine unrelated rows.

For saved logits z0,z1 and labels y0,y1 compute:
D=z0[y0]+z1[y1]-z0[y1]-z1[y0];penalty=softplus(1-D).
D>=1 means the EXISTING AUXILIARY MARGIN is met. This is a descriptive bin,not a new capability
gate. No threshold,margin,temperature,window or coefficient is fitted from these outputs.
Compute actual256-class argmax independently for both rows;retain0/1/2 correct answers,
prediction equality(collapse),pair penalty and mean normal answer NLL. Preserve exact identities,
labels,predictions,gaps and these values in the per-pair report.

Create19440 pair records:15 models x3 tasks x3 profiles x(96+48).
Create90 model/task/value-split aggregates with denominators,correct answers,0/1/2 correctness,
collapse,margin_met,margin_met_with_error,margin_not_met_with_both_correct,and mean losses.
Validate per-language normal counts against all accepted parent totals;never infer correctness
from the auxiliary margin. A met margin can coexist with a wrong answer or even two wrong answers;
correct answers can also lie below the chosen margin. Both directions must be visible.

Compare identical pair keys for pair_early versus ce_only and versus pair_always. Create60 aggregate
comparisons:5seeds x3tasks x2splits x2anchors,covering12960 matched pairs. Count exact argmax changes,
both-correct rescues and both-correct regressions. Do not call similar NLLs identical predictions.
Pairs are dependent observations,not independent replicates or extra seeds. This audit is not an
independent replication and does not prove why a representation or optimization path failed.

## Scope,workload and outputs

No model forward,training,model-state loading,new checkpoint write,row presentation,core call or
network call in the scientific diagnostic. Reading old tensors and applying numerical scoring is
allowed. Module calls,load_state_dict and torch.save are blocked;torch.no_grad encloses diagnostics.
Outputs:audit-plan.json,pair-margin-report.json,validation-summary.json,plus summary.json.
PASS means exact saved-data integrity/reconstruction only;capability_gate_applicable=False.
All C289 formal gates/verdicts and Gate F remain unchanged regardless of diagnostic findings.

The full source/input maps and per-pair report remain in local persisted artifacts. Console output
uses a compact validated receipt(artifact hashes/sizes,counts,summary hash) plus90 partitions and
60 comparisons,not the huge complete protected maps. This avoids duplicating large records into
console logs. It changes evidence transport only;the full local summary is still hash-verified.
No accepted logger or historical log is edited.

## Protection and execution

OWN6:source,test,runner,launcher,preregistration,design. Source586=580+6;
protected1056=1041+9 parent inputs+6 OWN;inherited dependency-union66.
Only direct repository import:C289. Parent and reachable scorer/core/helper sources remain pinned.
Own40;modules175;loaded4246;focused4245. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:123a8805343a6c7704ff6042d83928d3069aa43fe79e213e2b5798811d35b6f3.

Commit/re-fetch all OWN6 and complete independent post-authoring review before activation.
Validate the real parent and full pair-analysis dry-run without neural calls,then own40 and
actual focused4245. Dispatcher/launcher/runner require PowerShell ParseFile in the invocation path.
Operational preflight failures skip scientific logging/publication. Integrity failures retry
SAME C290. C291 is not registered before C290 formal judgment. Accepted source/tests are immutable.
