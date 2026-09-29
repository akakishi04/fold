# C287 preregistration — saved fitting/generalization partition

Experiment:C287-v5b-saved-fit-partition-audit. Stage:V5-B-SAVED-FIT-PARTITION-AUDIT.
Acceptance base:6ce09f66e8ea61a9fbfffd1e2de38a9ba8cdef61.
C286 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C288 NOT REGISTERED.

## One question

Where does the residual C286 error first appear:actually optimized normal TRAIN renderings,
held-out value assignments at trained lengths,or untrained length4,when final splitwise scores
are separated from the saved length/profile-stratified training loss history?
This diagnostic does not assume an optimizer cause or add another training intervention.

## Immutable parent contract and writer semantics

C286 execution:7fe7c72ff88e252b3087c9715674510dbba96651.
Published log:672b7cc1bf0f75f55c058e73e30ea69e249b2108.
Summary:runs/c286-v5b-cosine-tail-1664d75f4cf649fb8c5ca98f4be8308b/summary.json.
Summary SHA256:14bfe8920b80c86cc8e297864402c38c53a26c87085b8963cae363cb6fd98a9a.
Parent source:fold_lm/v05_benchmarks/model_c286_cosine_tail_stability.py.
Parent blob:332452219fe1a0b5472abb4a64be2827e6751b9f.
Thirteen ordered summaries:C286,C285,C284,C283,C282,C281,C280,C279,C278,C277,C276,C275,C274.
Their hashes and all8 parent artifact hashes/sizes are sealed in SUMMARY_SHAS/PARENT_ARTIFACTS.
The C286 acceptance addendum records the same8 artifacts;no parent file is modified.

Use C286.verify_artifacts(parent_dir,twelve ancestor paths,accepted execution_HEAD),then validate
its exact published seed_results,FAIL,candidate_gate=False,all_replays/all_pairs_matched/
all_prefixes_matched=True and direct parent source pin. Quad pass counts2/3;seen2/3 counts3/3.
Both arms fail all tasks286002/286003;candidate alone gains quad286005.

The verifier reconstructs task-keyed raw={two_char,triple,quad} via C286.analyze and checks actual
applied LRs,scheduled data exposure,first400 losses and step400 fingerprint. C287 separately reads
fit fields from the hash-verified fold-c286-cosine-tail-eval-v1 archive. This is tensor/archive
reading,not model state loading. No training checkpoint is deserialized into a model.
C286.fit records CE BEFORE each optimizer update on that update's mini-batch. It does not record
a full TRAIN or HOLDOUT loss at every step. Do not interpret last_ce as final-dataset performance.
C267/C270 answer_nll is the final model's mean normal CE within each answer cell;C283's adapter
preserves that field. C287 uses a row-weighted mean of those final cell losses by task and split.

## Fixed diagnostic output

Keep all10 states and seeds286001..286005;arms constant_lr/cosine_tail. Reconstruct3240 records:
10 models x3 tasks x(72 answer cells+36 two-order cells),with every expected split/profile/
language/entity-pair/fact-order key present exactly once. Parent task gates must reconstruct.
Validate finite metrics,integer/discrete counts,denominators,collapsed-pair consistency and NLL.

Create60 final partitions:10 models x3 tasks x2 value splits. Each has36 answer and18 order cells.
TRAIN denominators576 normal rows/288 query pairs;HOLDOUT288 rows/144 pairs per model/task.
Report correct/collapse counts,final row-weighted normal NLL,all5 criterion failure counts,
direct_pass,full_pass and mask_only_cells. Original thresholds stay accuracy.90,query_pair.80,
evidence_drop.35,query_drop.35,two_order.80. Direct_pass covers accuracy/query-pair/two-order;
full_pass additionally requires mask criteria. Neither is substituted for a prior formal gate.

Each model also reports fitted_train_direct_pass (both length2/3 TRAIN),seen_length_holdout_direct_pass
(both2/3 HOLDOUT),and quad_direct_pass (both inherited value splits). The descriptive
first_direct_failure_partition follows fitted_train -> seen_length_holdout -> quad -> none.
All booleans and partitions remain visible;this ordering is not a claim of causal propagation.
Length4 TRAIN is an inherited VALUE split,not a fitted four-character training set.

Training trace windows are fixed inclusive optimizer updates1..400,401..600,601..800. Within each,
stratify by length2/3 and structural profile index0/1/2,using epoch=floor((step-1)/4),
length=epoch%2+2,profile=epoch%3. No smoothing,window search,checkpoint selection or seed filtering.
Create180 bins (18/model),each with count,mean,min,max pre-update CE. Also90 paired candidate-minus-
control mean CE deltas on identical update strata. Verify first400 losses and midpoint fingerprints
still match exactly. Different strata have different counts;always report their denominators.
The trace statistics are descriptive,not independent samples or causal proof of instability.

## Workload,scope and persistence

Scientific neural forwards,row presentations,core calls,training,model-state loads,new checkpoint
writes and network calls are all0. Saved parent logits may be read for reconstruction. Module calls,
load_state_dict and torch.save are blocked during parent verification and the diagnostic path.
Outputs:audit-plan.json,fit-partition-report.json,validation-summary.json,plus summary.json.
PASS means exact diagnostic integrity only;capability_gate_applicable=False;no capability winner,
Gate F promotion or revision of C286's valid negative. Findings may favor either arm or neither.

## Authoring/protection/execution

OWN6:source,test,runner,launcher,preregistration,design. Source568=562+6;protected1016=1001+9+6;
inherited dependency-union63. Direct repository import C286;its reachable pinned helpers remain
protected. Own32;modules172;loaded4118;focused4117;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:98e5768640301fd36d00706305809bd5b4707eb10458bee5abfaef478b1bf430.
Commit/re-fetch OWN6 and complete independent post-authoring review before activation.
Runtime Validate checks actual parent data and a full analysis schema dry-run without neural calls,
then own32 and focused4117 before scientific logging. Dispatcher/launcher/runner use ParseFile.
Operational skip does not publish a scientific log;integrity failure retries SAME C287.
C288 is not registered until C287 is judged. Accepted source/tests/logs are immutable.
