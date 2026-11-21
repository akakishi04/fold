# C285 preregistration — saved matched-cell length-transfer attribution

Experiment:C285-v5b-saved-length-transfer-audit.
Stage:V5-B-SAVED-LENGTH-TRANSFER-AUDIT.
Acceptance base:8b16da05d3669e86ee6b9d323c6cb9eeec4766bf.
C284 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C286 NOT REGISTERED.

## One question

Which C284 four-character fixed-criterion failures are newly introduced relative to the same
model's matched three-character cells, and how does this attribution differ between the arms?
This is saved-output diagnostic attribution, not another training intervention or replication.

## Parent identity and writer semantics

Scientific execution:3d34f6ba19017fd7d0422f070624ea7b1b494555.
Published log:4fe9b2f0d55b98c15855c2f9580572c8e9a9158e.
Summary:runs/c284-v5b-max-length-450fab44535d4dd09c14931b8de1a283/summary.json.
Summary SHA256:83df761b835fa529d72ba1cee5fe618ddaff6936d9db56defc02957b90788c83.
C284 source blob:cc560842a4f2b4e9b0ba6ae9481c42e2f3bb1df1.
All eleven independent summary hashes (C284 down to C274) and eight parent artifact hashes/sizes
are sealed in SUMMARY_SHAS/PARENT_ARTIFACTS. The C284 acceptance records the same eight artifacts.

Use C284.verify_artifacts(parent_directory,ten ancestor paths,accepted execution_HEAD).
The parent validates and reconstructs its task-keyed raw={two_char,triple,quad} archive through
unchanged C267/C270/C283 scorers. C285 consumes the returned seed/arm/task metric records, not a
similarly named older loader. C284 metrics have no required whole-model passed field; its summary
seed_results.passed means quad_pass, while all_tasks_pass is descriptive. Preserve this distinction.
Require exact published flags for all10 states, FAIL, candidate_gate=False, all_pairs_matched=True,
all_replays=True, and the explicit direct C284 source pin. Never load a training checkpoint.

## Fixed matched-cell analysis

Retain all seeds284001..284005 and arms three_char_only,mixed_length, including failed states.
Reconstruct3240 records:10 models x3 tasks x(72 answer cells+36 two-order cells).
Require every unique split/profile/language/entity-pair/fact-order key, finite numeric metrics,
integer denominators, consistent correct/query-pair/collapse counts and exact parent PASS flags.
Answer-cell denominators16 TRAIN/8 HOLDOUT; query pairs8/4; two-order groups16/8.
Reconstruct ablated correct counts via normal accuracy minus the registered drop, with integer checks.

Thresholds stay accuracy.90,query_pair_accuracy.80,evidence_drop.35,query_drop.35,two_order_accuracy.80.
Profiles map by the fixed structural index:
-doubled/tripled/quadrupled ->0;
-shared_prefix/shared_prefix2/shared_prefix3 ->1;
-shared_suffix/shared_suffix2/shared_suffix3 ->2.
This relabels analysis keys only, not raw inputs, scorer thresholds or model behavior.

Primary views:
-quad_between_arms:540 matched records, left=three_char_only,right=mixed_length;
-triple_to_quad per arm:540 matched records, left=three-character,right=four-character.
Each criterion reports both_pass,left_fail_right_pass,left_pass_right_fail,both_fail,denominator,
left/right failure counts and right-minus-left delta. Accuracy/query/mask criteria have360 pairs;
two-order has180 pairs per full view. Report normal correct/collapse totals and mask-only failures.
Per-seed versions of all primary views and six quad split/profile arm-comparison tables are fixed.
Persist every record, including successful records. All five seeds remain primary; no post-hoc filter.

## Interpretation boundary

Within-state triple-to-quad transitions identify newly failing MATCHED CELLS, not necessarily
newly failing individual rows. Co-failure is not proof that the same wrong prediction or causal
mechanism is inherited. Criteria overlap and the small correlated cells are not independent seeds.
The diagnostics cannot prove mixed-training superiority, distinguish all curriculum effects,
repair C284's3/5 gate, or create new independent replication evidence. Any favorable/unfavorable
attribution is reportable; no sign of improvement is required for diagnostic PASS.

## Workload and persistence

Scientific model forwards,training steps,row presentations,core calls,model-state loads,
new checkpoint writes and network calls all0. Reading saved logits for parent reconstruction is
allowed; torch.nn.Module calls,load_state_dict and torch.save are blocked during that reconstruction.
Authoring/regression workload is separate from zero-neural scientific workload.
Outputs:audit-plan.json,cell-attribution.json,validation-summary.json,plus summary.json.
PASS means exact diagnostic integrity only;capability_gate_applicable=False,gate_f_candidate=False,
production_adoption=False. Model parameters,training,thresholds,seeds and prior verdicts are untouched.

## Protection and execution

OWN6:source,test,runner,launcher,preregistration,design. All accepted source/tests stay immutable.
Source556=550+6;protected991=976+9 new parent inputs+6 OWN;inherited dependency-union61.
C285 directly imports only C284;its reachable repository helpers remain covered by inherited pins.
Own32;modules170;loaded4046;focused4045. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c.
Validate real parent provenance,own32 and actual focused4045 before science/log publication.
Commit and re-fetch all OWN6 for independent review before activation. Valid/malformed/mismatched
seal checks and actual production run/loader/suite dispatch must be covered by behavioral tests.
Operational failure skips science/publish. Scientific integrity failure retries SAME C285.
Gate F remains NOT PASSED. C286 is not registered until C285 is formally judged.
