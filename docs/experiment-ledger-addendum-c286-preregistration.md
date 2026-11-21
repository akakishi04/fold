# C286 preregistration — fixed-budget late cosine learning-rate decay

Experiment:C286-v5b-cosine-tail-stability. Stage:V5-B-COSINE-TAIL-STABILITY.
Acceptance base:100ac28eca9015269fd69104edf36645c4f1bf9a.
C285 ACCEPTED PASS (diagnostic integrity only). Gate F NOT PASSED. C287 NOT REGISTERED.

## One scientific question

At identical mixed two/three-character coverage and800 updates,does reducing only the final400
learning rates improve final reliability and untrained four-character transfer versus constant LR?
C285 locates most residual failures at already-covered length3;it does NOT establish an optimizer
cause. This intervention tests one bounded alternative before changing architecture or coverage.

## Parent contract

C285 execution:f2bd32785895c30defa16be7d1eca6279ba4ed23.
Published log:d8a24df7b94a1b8c3d339b868c6db4fc2ed7e3b6.
Summary:runs/c285-v5b-saved-length-audit-94786461780e4110a04f18ca3c92c427/summary.json.
Summary SHA256:702092926265bb893babce1e5b93dd234791527344193ea876d33210e8bfdba1.
Direct source blob:383b4156351c601a26b1f58c2ccdea59206f8538.
Twelve ordered summaries:C285,C284,C283,C282,C281,C280,C279,C278,C277,C276,C275,C274.
All twelve exact hashes and three C285 artifact hashes/sizes are sealed in code/manifest.
-audit-plan.json:cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c;3246 bytes.
-cell-attribution.json:2d733c0d92bf57678ff610153aab95d48ab2b1c17ec67d8bc447cedd2c2f8b15;1687080 bytes.
-validation-summary.json:a814abd30a8a5432722ed35ae0ee19d87706aa4db5a876a58887e4de4e6ebf3b;29907 bytes.

Use actual C285.verify_artifacts(parent_dir,eleven ancestor paths,accepted execution_HEAD).
It returns diagnostic payload/report,not checkpoint models. Require PASS,diagnostic_complete,
capability_gate_applicable=False,zero model forwards and explicit C285 source identity.
Require mixed triple-to-quad accuracy both_fail37,new_fail6,right_fail43. Parent reconstruction
blocks neural Module calls,load_state_dict and torch.save. Older records are provenance only.
The C284 evaluate/replay_one helpers are reused for task-keyed raw={two_char,triple,quad};they
have no seed/arm gate in that path. C286.analyze owns new identities/LR/common-prefix validation.
Never apply an old analyze function to C286 records. No inherited file is edited.

## Changed variable and exact schedule

Fresh paired seeds286001..286005. Arms constant_lr and cosine_tail.
Both use actual C278 all-token MeanFinalDualReadout,14256 parameters,48-token context.
Candidate is an independent copy of the entire control initialization. Both train on mixed2/3.
Use unchanged C282.training_tables,only normal TRAIN examples,shape[2,3,192,48]. No HOLDOUT,
ablated-view or four-character example enters the optimizer. Only tokens/zero task IDs enter forward.

Both use200 complete epochs x4 batches x48 rows.96 complete query pairs per epoch;
randperm96(seed+286000+epoch);profile=epoch%3;length=epoch%2 (0=two characters,1=three).
Every logical row200 exposures,100 per length. Length/profile update matrix in BOTH arms:
[[136,132,132],[132,136,132]]. Logical rows,targets,batches,rendered schedule and capacity match.

1-based optimizer update s,with the LR assigned BEFORE that update:
-constant_lr:eta(s)=0.005 for s=1..800.
-cosine_tail:eta(s)=0.005 for s=1..400.
-cosine_tail for s=401..800:eta(s)=0.0005+0.0045*(1+cos(pi*(s-400)/400))/2.
At s400 eta=.005;at s600 eta=.00275;at s800 eta=.0005. No scheduler post-step indexing.
No warmup,extra updates,early stopping,best checkpoint,seed replacement or endpoint retuning.
AdamW betas.9/.999,eps1e-8,weight_decay0,gradient clip1;mean CE only.
Fit RNGseed+287000 resets per arm. CPU float64,2 threads,deterministic algorithms.

Record all800 actual applied LR values,their hash,all800 minibatch CE values and step400 state
fingerprint without writing an intermediate checkpoint. Require both arms' initial fingerprint,
logical batches,step400 fingerprint and first400 losses to match exactly. Failure is INVALID,
not a scientific negative. Loss traces are descriptive;they never select a checkpoint or stop time.

## Data and evaluation

Logical data SHA256:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Triple SHA256:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.
Quad SHA256:86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.
Freeze after800 updates,evaluate all2/3/4-character tasks,strict-load final state and replay all3.
Use unchanged C267/C270/C283 scorers,all split/profile/language/entity/order/mask cells.
Thresholds:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Primary absolute PASS iff all FIVE cosine_tail final states pass every four-character criterion.
As in C284,passed=quad_pass;two/three/all-task gates are descriptive and fully reported.
An absolute PASS is not comparative superiority. Report all5 paired seed outcomes and180
split/profile/language correct/collapse contrasts. Gate F and prior verdicts remain unchanged.

A favorable result supports this LR policy at this fixed budget/family,not proof of a unique
optimizer mechanism,universal stability or arbitrary-length reasoning. A miss does not disprove
all optimization interventions. Late LR reduction can also slow useful learning;both outcomes
are reportable. This is not another test of mixed-versus-three-only diversity.

## Workload and persistence

10 fresh models,8000 updates,384000 training rows. Per model881 training/evaluation forwards
plus81 strict replay;total9620 forwards,539520 row presentations,38480 core calls.
One10-state checkpoint bundle write/load,10 strict state loads,new_checkpoint_writes1;network0.
No extra evaluation at step400. Fingerprinting and recording traces add no neural forward.
Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json,plus summary.json.
Schemas:fold-c286-cosine-tail-models-v1 and fold-c286-cosine-tail-eval-v1.
Postcheck reconstructs scores and LR/exposure/prefix invariants with new neural calls blocked.

## Protection and execution

OWN6:benchmark,test,runner,launcher,preregistration,design. Source562=556+6;
protected1001=991+4 parent inputs+6 OWN;inherited dependency-union62.
Direct repository import is C285;deciding-path C284,C283,C282,C278,C269,C267 and reachable
core/base/reader/factory/audit helpers remain in inherited source/protection maps.
Own40;modules171;loaded4086;focused4085. Sole exact inherited C204 exclusion unchanged.
Manifest SHA256:3d0ecd3f4785967a88e8b84597d9615be79eb7e609c348bf2ca1cdead8cbe94e.

Commit and re-fetch all OWN6 for independent review before activation. Validate real parent data,
real TRAIN tables/paired initial models/LR schedule,own40 and actual focused4085 before science.
Dispatcher and experiment launcher/runner require PowerShell ParseFile in the execution path.
Operational skip does not publish scientific logs. Scientific integrity failure retries SAME C286;
valid quad gate miss is ACCEPTED VALID NEGATIVE. C287 is not registered until formal judgment.
