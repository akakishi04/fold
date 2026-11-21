# C314 preregistration — saved five-to-six boundary profile

Experiment:C314-v5b-saved-six-boundary-profile. Stage:V5-B-SAVED-SIX-BOUNDARY-PROFILE.
Acceptance base:9221bfbe539d3f91fa3a74caa355e4059c9453fe.
C313 and C312 remain ACCEPTED VALID NEGATIVE;Gate F NOT PASSED;C315 NOT REGISTERED.

## One question

Where does the observed five-to-six deterioration occur by language and name profile,
at exactly the same saved weights and logical questions? Pair correctness and the
correct-answer margin before attributing failure to a language or context boundary.
This is an observational diagnostic on already saved outputs,not another training policy.

Retain all10 C312 states in the verified C313 archive:seeds312001..312005,both random_pairs
and value_balanced,including every failed state. Keep all3 profiles and English/Japanese,
original TRAIN192/HOLDOUT96 value splits and all288 source IDs. Use the C313 raw.before['5']
normal logits and raw.six normal logits. Do NOT count raw.after as independent observations.
The exact parent verifier still reconstructs all masked/full gates and before/after controls.
No new prompts are executed,no new model,training,checkpoint,seed or threshold is introduced.

## Paired measurements

Every full256-class argmax keeps the original smallest-index tie rule. Record tied maxima
without changing the selected answer. Correct-answer margin is target logit minus the
largest of all255 non-target logits. It is a score gap,not a calibrated probability.
A zero margin does not alone determine correctness:tie ordering still matters.
Record exact saved prediction and margin for both lengths at every matched source row.

Group by seed,arm,split,profile and language:120 groups. Report five/six correct counts,
both correct,new error,recovered,both wrong,same wrong,each length's answer classes and
tied counts. Answer classes:correct,other_fact,unmentioned_digit (ASCII0..3 absent from facts),
other_output (any other output class,including ASCII4..9). These classes never repair answers.
For each group report mean/min/max margin and paired margin delta,decreased/equal/increased
counts. No tuned margin threshold,probability calibration,significance test or best subgroup.
Raw score scales can differ across trained states;do not treat pooled margins as causal weights.

Read the actual verified old/six prompt strings to count UTF8 bytes plus BOS/EOS,not inferred
character count. Normal English uses24->27 tokens,Japanese54->63,in a64-slot model.
All questions/language groups stay. Language,byte length and EOS position co-vary here;
profile comparisons also change string content. Thus a concentration does NOT distinguish
language weakness,byte length,position,attention or remaining-context effects causally.

## Writer contract and reconstruction

C313 execution:bc6a226b8605b6ae04e64d46a387487533c0bdc0.
Publication:aef7187d19ed49b3ba0f29b5621fc675c4365b2d.
Summary:runs/c313-v5b-frozen-six-8ef41237b7f84f148a0dcdce4b9aed21/summary.json.
SHA256:adfeb06f6db5b77feb172b8ede1f3bf7032c8ca35b299d7ecc692baeca097c97.
C313 source blob:bf514ad80f85140e81b834d00aceb3379f4bfd80.

Verify40 ordered summary hashes BEFORE C313.verify_artifacts(parentdir,39ancestors,acceptedHEAD).
Require accepted FAIL,exact ordered ten seed flags,six counts random2/balanced1,random primary
and all_replays=True. The parent summary seals five artifact descriptors;its verifier reconstructs
original model identities,output controls and local/masked gates. C313 wrote evaluations.pt with
schema fold-c313-six-transfer-eval-v1,raw.before/six/after;it did NOT write a model checkpoint
or the old dataset. Read original dataset.json and length-datasets.json from paths[1] (C312),
and six-dataset.json/evaluations.pt from paths[0] (C313),after their recursive verification.
Recheck all three canonical hashes and each source_id/target binding before pairing.

Each group's six correctness agrees with its actual C313 metrics[i].six_score.totals entry.
C304's scorer maps repeat/shared_prefix/shared_suffix to C270's tripled/shared_prefix2/
shared_suffix2 labels;use that exact adapter. Reconcile all120 local row/correct totals.
Sum language/profile groups per state/split and reproduce every field of the20 original
C313 five_to_six counts,including same_wrong. Do not infer cause from aggregate overlap.

Sole direct child import C313. Its inspected context provides C310.no_neural,C304 and original
backend. Actual repository-local helper coverage,including C312 context and factory-language,
must be in inherited pins. Retain724 source pins and1357 inputs;add OWN6 plus6 C313 summary/
artifact files for730/1369. No accepted source,test,log,preregistration or dispatcher edit;
no new exclusion. Never waive missing deciding-path source protection.

## Work,scope and review gates

8640 matched normal questions =17280 saved answers. 120 diagnostic groups,120 original local
receipts,20 original transition receipts. All ten models remain dependent saved observations.
Science train_steps/model_forward_calls/model_state_loads/new_checkpoint_writes/row_presentations/
core_forward_calls/network_calls are0. JSON/tensor reads and numerical operations still cost work.
Inherited no-neural scope blocks Module calls,state loads and torch.save. No optimizer used.
Operational software tests and recursive old-result verification are separate costs.

Outputs:audit-plan.json,boundary-report.json,validation-summary.json plus summary.json.
JSON only. Report stores all8640 paired row IDs,predictions,margins,ties,classes and token counts,
all120 groups and20 transition receipts. Detailed arrays stay local/ignored;console mirrors
compact receipt,summary and120 groups. Fresh reconstruction from the same protected evidence
must match JSON content,hashes and sizes;no run-directory overwrite.

PASS means diagnostic integrity and exact reconstruction only. It is compatible with arbitrarily
poor capability. Do not replace C313's original2/5 primary or any old Gate with this PASS.
Own24/modules199/loaded5054/focused5053;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:e249986e20378fd3833dfb26183f94a74b93af3702149ce38bf2c03ba07c5a91.
Commit/refetch/review OWN6 before activation. Required checks include explicitUTF8/CP932,zero
unbound globals,embedded Python and40-path CLI alignment,semantic suite-ID counting,actual
child loader/run/persistence order,independent margin/count examples and tamper rejection.
Windows Validate still requires40 actual parent archives/pins,real-data dry-run,own24/full5053
regression and dispatcher/launcher/runner ParseFile. Validate failure skips science/publication.
Integrity failures repair SAME C314;no scientific retuning. C315 waits for formal C314 judgment.
