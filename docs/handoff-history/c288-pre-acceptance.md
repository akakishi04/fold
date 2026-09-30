# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C287 ACCEPTED PASS (diagnostic integrity only). C288 ACTIVE / NOT YET JUDGED. C289 NOT REGISTERED.**
C287 scientific execution:037e8e3b214af97c5bfb3ad32a202b7cd7ee1d28.
C287 published log:621ecbf4f43f72b75f4915e3095cc0dd3044fe9b.
C286 remains ACCEPTED VALID NEGATIVE. C287 is complete;do not rerun it.
C288 is the unique ACTIVE supervised query-pair assignment-loss comparison.
Prior chat claims of pending C287 execution or TRAIN-success/HOLDOUT-only failure were incorrect
and are superseded by the actual published results and acceptance below.

## Latest accepted science — C287

Acceptance:docs/experiment-ledger-addendum-c287-c288.md.
Acceptance commit:6acdfd588cca0cba3ede448df8e0e066a391fdef.
Summary:runs/c287-v5b-fit-partition-fb83191e6dd74d3f840c59f9a5282069/summary.json.
Summary SHA256:69fb8b4f8eb4affe1ff340a7b3faf2b301389cc648afed7becf486dab6fce54d.
Manifest SHA256:98e5768640301fd36d00706305809bd5b4707eb10458bee5abfaef478b1bf430.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;capability_gate_applicable=False.
Own32/focused4117 PASS;source568/protected1016;zero scientific forwards,training,state loads,writes.
All3240 fixed records,60 final partitions,180 loss bins and90 paired bins reconstructed.

First direct-failure partitions:fitted_train4,seen_length_holdout0,quad1,none5.
Both arms286002/286003 fail actual optimized normal TRAIN and also fail HOLDOUT/quad.
constant_lr286005 passes both seen-length splits and fails only quad;the other5 states pass direct gates.
Cosine tail286002 reduces two/TRAIN correct515->399 and triple/TRAIN515->397 out of576 each;
two/TRAIN collapse60->139,triple/TRAIN59->133 out of288 pairs. It is not an adopted stability fix.
All seeds stay in scope. These are fitting errors,not proof of a particular gradient/architecture cause.

## Active C288 — supervised query-pair assignment loss

Experiment:C288-v5b-query-pair-assignment-loss. Stage:V5-B-QUERY-PAIR-ASSIGNMENT-LOSS.
Registration:docs/experiment-ledger-addendum-c288-preregistration.md.
Design:docs/v5b-query-pair-assignment-loss-v0.1.md.
Review:docs/c288-post-authoring-review.md.
Acceptance base:6acdfd588cca0cba3ede448df8e0e066a391fdef.
Authoring/review target:072c3d66b205d7438254367f0825d53e2f0c5406.

One question:at fixed architecture,mixed2/3 coverage,constantLR and800 updates,does supervised
query-pair assignment loss reduce fitted collapse and improve unseen-four-character reliability?
Fresh paired seeds288001..288005;arms ce_only,ce_pair_assignment. Actual C278 all-token
MeanFinalDualReadout,14256 parameters,48-token context;independent identical initial states.

192 logical TRAIN rows,96 complete query pairs,200 epochs x4 batches x48 rows.
randperm96(seed+288000+epoch);profile=epoch%3;length=epoch%2. Per-row length exposures100/100;
length/profile counts[[136,132,132],[132,136,132]] in both arms. No HOLDOUT/quad/ablated optimization.
AdamW LR.005 constant,betas.9/.999,eps1e-8,weight_decay0,clip1;fit RNGseed+289000 per arm.
CPU float64,2threads,deterministic. No extra model parameters,examples or forward calls.

For each existing query pair with logits z0,z1 and distinct TRAIN targets y0,y1:
D=z0[y0]+z1[y1]-z0[y1]-z1[y0]. Lpair=mean softplus(1-D) over24 pairs.
Control optimizes exact mean CE over48 rows. Candidate optimizes CE+0.25*Lpair for all800 updates.
Labels/pair metadata never enter model.forward or inference. Margin1/coefficient.25 remain fixed.
Summed assignment margin alone does not guarantee both answers;CE and unchanged cell gates remain.
Auxiliary computation/gradients are extra work even though model-forward and update counts match.
Record800 CE/pair/total/appliedLR traces and reconstruct the registered objective. No model selection.

Freeze final states and evaluate original2/3 and untrained4 tasks,then strict checkpoint replay.
Primary absolute PASS:all5 ce_pair_assignment states pass every FOUR-character criterion.
Thresholds unchanged:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Two/three/all-task gates and trained-length TRAIN/HOLDOUT direct pass counts are descriptive.
Include60 final split partitions and180 paired normal/collapse contrasts in this same result.
Absolute candidate PASS is not superiority. No unique mechanism or automatic Gate F claim.

Workload:10 models,8000 updates,384000 training rows,9620 forwards,539520 row presentations,
38480 core calls,one10-state checkpoint bundle write/load,10 strict state loads,network0.
Registration:source574;protected1026;dependency-union64;own40;modules173;loaded4158;focused4157.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:44b114f22e06b214f3567baea16cc8771da55566e128c3c2d35b47023ba313d5.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own40).
Review target:072c3d66b205d7438254367f0825d53e2f0c5406. All6 committed OWN files fetched back;
whole-file Git blobs match complete local tested bytes6/6. Post-match own40 PASS in4.577s on
Linux/Python3.13.5/PyTorch2.10.0+cpu. Both Python files and3 embedded runner blocks compile;
unresolved global names0. Autograd checked against finite differences. Tests run800 real AdamW
updates per arm on a small query-conditioned toy model and verify objective/LR/exposure traces.
Other paths mock parent archives,Git,inherited models/scorers. This is NOT actual FOLD science.
Real parent artifacts,actual initial models/tables,full4157 regression,PowerShell parsing and
actual10-model training remain authoritative Windows runtime gates. Reviewed OWN6 stays immutable.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C288 -> Validate(parent/source/input
574/1026,real TRAIN tables/complete pairs/initial models,own40,focused4157) ->
authoring_runtime_preflight=PASS -> Execute(10-model paired objective comparison,frozen3-task
evaluation,strict replay,60 final partitions,persisted reconstruction) -> log publication.

Validate failure skips science/publish. Scientific integrity failure retries SAME C288.
Valid fixed-gate miss is ACCEPTED VALID NEGATIVE. Do not alter loss coefficient,margin,LR,seed,
budget or thresholds after results. C289 is not registered before C288 formal judgment.
Keep scientific execution HEAD distinct from the subsequent log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Later lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoffs remain under docs/handoff-history/c280-pre-acceptance.md through
c287-pre-acceptance.md. The latest preserves Git blob759e7820e365de915f8cc903e7f9b24b70c61668.
Only this Formal state is authoritative;old ACTIVE instructions are historical.
Accepted source/tests,preregistrations,logs and protected dispatchers remain unchanged.
