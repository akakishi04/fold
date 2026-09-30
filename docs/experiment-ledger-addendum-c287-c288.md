# C287 acceptance and the next supervised query-pair comparison

## Formal verdict

C287 ACCEPTED PASS (diagnostic integrity only). Gate F NOT PASSED.
C286 remains ACCEPTED VALID NEGATIVE. No rerun, seed filtering or threshold revision.
C288 is not activated by this acceptance; it requires separate preregistration and review.

Scientific execution HEAD:037e8e3b214af97c5bfb3ad32a202b7cd7ee1d28.
Published log commit:621ecbf4f43f72b75f4915e3095cc0dd3044fe9b.
Log SHA256:6aa46b5e7662d4bdac7eabf3bb5fd1222c0c8a40c1ec387f2279e92535ab744b;989282 bytes.
Summary:runs/c287-v5b-fit-partition-fb83191e6dd74d3f840c59f9a5282069/summary.json.
Summary SHA256:69fb8b4f8eb4affe1ff340a7b3faf2b301389cc648afed7becf486dab6fce54d.
Manifest SHA256:98e5768640301fd36d00706305809bd5b4707eb10458bee5abfaef478b1bf430.

## Execution validity

Read the published result and POSTCHECK, not just the invocation or publication status.
Own32 PASS;focused4117 PASS (435.156s in the published log);parent/source/input568/1016 PASS.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False. Persisted reconstruction PASS;tracked tree clean;execution HEAD preserved.
Scientific neural forwards,row presentations,core calls,training,state loads,checkpoint writes and
network calls are zero. This excludes authoring/regression work, not the scientific workload.
All3240 records,60 final split partitions,180 stratified loss bins and90 paired bins were retained.

## Deciding metrics

First direct-failure partitions across all10 retained states:
- fitted_train:4 states (both arms at286002 and286003);
- seen_length_holdout:0 states;
- quad:1 state (constant_lr at286005);
- none:5 states (both arms286001/286004 and cosine_tail286005).

The4 fitted_train states also fail seen-length HOLDOUT and quad. All6 other states pass both
trained-length TRAIN and HOLDOUT direct gates. These are descriptive partitions,not causal proof.

Final normal TRAIN results (correct/576;collapse/288):
|seed|arm|two-character correct|two collapse|triple correct|triple collapse|
|---|---|---:|---:|---:|---:|
|286002|constant_lr|515|60|515|59|
|286002|cosine_tail|399|139|397|133|
|286003|constant_lr|484|84|484|84|
|286003|cosine_tail|476|70|487|69|

Final normal TRAIN NLL for286002:
-constant_lr:two0.19530556722503223;triple0.21174812294756187.
-cosine_tail:two0.480582533207874;triple0.483479818794618.
Final normal TRAIN NLL for286003:
-constant_lr:two0.23306627220237544;triple0.2333582328369099.
-cosine_tail:two0.2330504998268373;triple0.23334072542561202.
Thus identical whole-task pass counts concealed substantial candidate regressions at286002.

constant_lr286005 has quad TRAIN575/576 correct and HOLDOUT287/288 correct. The TRAIN local
criteria pass,while the HOLDOUT has1 accuracy and1 query-pair criterion failure. The same state's
length2/3 TRAIN and HOLDOUT are fully correct. cosine_tail286005 passes every task as already judged
in C286. This small transfer miss is distinct from the4 broadly failing fitted_train states.

The saved loss trace is pre-update minibatch CE,not final full-data loss. For example,constant_lr
286003 updates601..800 has length/profile mean CE between0.2353970507203162 and0.2361472655992004
(32 or36 updates per stratum). This is descriptive support for residual fitting error,not a proof
of a local minimum,gradient failure or a unique architecture defect. Final split NLL is kept separate.

## Interpretation and corrections

The primary observation is not merely failure at unseen values or a longer name. Some states fail
many examples that were actually optimized,and they collapse distinct queries sharing the same facts.
Late LR decay did not repair those4 states;it worsened fitted accuracy for286002. Do not adopt the
cosine tail as a proven universal stabilization policy.

Earlier chat responses had not inspected the completed C287 log and incorrectly called it execution
pending,or described TRAIN-success/HOLDOUT-only failure. Those statements are superseded by this
accepted evidence. Operational ACTIVE/NOT YET JUDGED never implied the user's run was unexecuted.
The previous speculative C288 failure-clustering suggestion was NOT preregistered and is not binding.

## Accepted artifacts

-audit-plan.json:98e5768640301fd36d00706305809bd5b4707eb10458bee5abfaef478b1bf430;3375 bytes.
-fit-partition-report.json:3981b2cc4dca74f67ce8072371440ebf19b3c08df11824bfc7037990cd323151;1262551 bytes.
-validation-summary.json:756040d6d4a1f440d7653d9606376a4b0ef3e077fcb3be33d393ce56d6cf9c17;73311 bytes.

## Next question, not activation

At fixed model,mixed2/3 coverage,constant LR.005 and800 updates,does an auxiliary supervised
query-pair assignment loss reduce fitted-query collapse and improve untrained four-character
reliability compared with per-row cross-entropy alone?

Use fresh paired seeds;retain all outcomes. Both queries of each existing same-facts pair are
already in the same batch. Compare their correct assignment score against the swapped assignment
using existing logits and TRAIN labels only. The supervision must not enter model.forward or
inference,and must require no extra examples or model forwards. Keep CE as the per-row objective.
Prespecify one coefficient/margin;do not tune them after evaluation. This changes objective and
gradient weighting,not a uniquely isolated mechanism. Matching nominal LR does not match gradient
norms. The candidate may worsen calibration or transfer;report that without changing the gate.

C288 requires separate source/tests/runner/launcher/preregistration/design,committed-byte review
and runtime Validate. C289 NOT REGISTERED. Gate F and all prior verdicts remain unchanged.
