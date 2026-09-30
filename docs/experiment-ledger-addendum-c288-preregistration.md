# C288 preregistration — supervised query-pair assignment loss

Experiment:C288-v5b-query-pair-assignment-loss. Stage:V5-B-QUERY-PAIR-ASSIGNMENT-LOSS.
Acceptance base:6acdfd588cca0cba3ede448df8e0e066a391fdef.
C287 ACCEPTED PASS (diagnostic integrity only). Gate F NOT PASSED. C289 NOT REGISTERED.

## One scientific question

At fixed architecture,mixed2/3 data,constant learning rate and800 updates,does adding supervised
query-pair assignment loss reduce fitted-query collapse and improve untrained four-character
reliability versus per-row cross-entropy alone? C287 observed actual normal TRAIN failures;it did
not prove that the original objective caused them. This is a bounded intervention,not another audit.

## Immutable parent contract

C287 execution:037e8e3b214af97c5bfb3ad32a202b7cd7ee1d28.
Published log:621ecbf4f43f72b75f4915e3095cc0dd3044fe9b.
Summary:runs/c287-v5b-fit-partition-fb83191e6dd74d3f840c59f9a5282069/summary.json.
Summary SHA256:69fb8b4f8eb4affe1ff340a7b3faf2b301389cc648afed7becf486dab6fce54d.
Parent source blob:05ab28c666203eaf69506c024a2805f31986a3ff.
Fourteen ordered summaries:C287,C286,C285,C284,C283,C282,C281,C280,C279,C278,C277,C276,C275,C274.
All14 exact hashes are independently checked before the parent verifier. The accepted3 artifacts:
-audit-plan.json:98e5768640301fd36d00706305809bd5b4707eb10458bee5abfaef478b1bf430;3375 bytes.
-fit-partition-report.json:3981b2cc4dca74f67ce8072371440ebf19b3c08df11824bfc7037990cd323151;1262551 bytes.
-validation-summary.json:756040d6d4a1f440d7653d9606376a4b0ef3e077fcb3be33d393ce56d6cf9c17;73311 bytes.

Dispatch C287.verify_artifacts(parent_dir,thirteen ancestor paths,accepted execution_HEAD),not an
older similarly named loader. Require PASS,diagnostic_complete,capability_gate_applicable=False,
zero model forwards,explicit parent source pin and all10 observed model partitions:4 fitted_train,
0 seen_length_holdout,1 quad,5 none,with exact seed/arm identities. This parent is a diagnostic,
not a checkpoint source. Fresh initialization only;no failed-seed fine-tuning or selection.
Parent verification blocks Module calls,load_state_dict and torch.save.

## Architecture,data and budget held constant

Fresh paired seeds288001..288005;arms ce_only and ce_pair_assignment.
Actual C278 all-token MeanFinalDualReadout in both arms:14256 parameters,48-token context,float64.
Construct one control and deep-copy the entire state to independent candidate storage. Same initial
fingerprint/state keys;no extra trainable parameters or inference-time path.
Use C282.training_tables of normal mixed2/3 TRAIN renderings,shape[2,3,192,48].
Logical data SHA256:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Triple SHA256:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.
Quad SHA256:86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.

96 complete same-facts/different-query pairs of192 logical rows. For each of200 epochs,
randperm96(seed+288000+epoch),24 pairs per batch,4 batches. profile=epoch%3;length=epoch%2.
Each logical row200 exposures total,100 per length. Length/profile update counts in both arms:
[[136,132,132],[132,136,132]]. Pairs are never split or recombined across facts/values/orders.
TRAIN targets must equal the aligned dataset targets before optimizer creation.
No HOLDOUT,quad or masked input is used by the optimizer. Forward receives only tokens/zero task IDs.
AdamW lr.005 for all800 updates,betas.9/.999,eps1e-8,weight_decay0,global gradient clip1.
Fit RNGseed+289000 reset per arm. CPU float64,2 threads,deterministic algorithms.

## Only changed variable:training objective

For the two rows in each batch pair,let logits be z0,z1 and distinct TRAIN targets y0,y1.
The correct assignment score is z0[y0]+z1[y1];the swapped score is z0[y1]+z1[y0].
D=correct_score-swapped_score.
CE=mean cross-entropy over48 rows.
Lpair=mean softplus(1-D) over24 pairs.
-ce_only:loss=CE exactly (not a modified CE gradient).
-ce_pair_assignment:loss=CE+0.25*Lpair from update1 through800.
Margin1 and coefficient0.25 are fixed before execution;no schedule or tuning after results.
The pair loss uses existing logits and existing TRAIN labels only. No additional forward,negative
example or teacher model is introduced. It is not pair metadata available to inference.
The correct-versus-swapped margin is invariant to each row's common logit offset,and identical
query-independent score vectors yield D=0 regardless of their class preference.

This auxiliary term does NOT replace independent CE and does not guarantee both rows are correct:
one strong difference can compensate for a weak one in the summed margin. CE and original pair
accuracy/order gates remain necessary. Auxiliary gradients and their scale change;matching nominal
LR does not isolate pure information content from gradient weighting. No universal mechanism claim.

Compute CE and Lpair in both arms for reporting,but backpropagate only the registered total.
Record all800 CE,pair,total and applied-LR values. Reconstruct total=CE+weight*pair at1e-12 tolerance.
These are pre-update batch traces,not final-dataset NLL and not checkpoint-selection scores.

## Frozen evaluation and gates

After800 updates,freeze and evaluate unchanged two/three/four-character tasks via C284.evaluate;
strict-load the final checkpoint and use C284.replay_one for all3 tasks. These helpers are task-keyed
and do not constrain the new seeds/arms. C288.analyze owns identities/objective/schedule invariants;
never dispatch an old experiment's analyze onto C288 records.

Primary absolute PASS:all FIVE ce_pair_assignment final states pass every FOUR-character criterion.
Thresholds unchanged:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
passed means quad_pass. Two/three/all-task gates and both trained-length TRAIN/HOLDOUT direct gates
are descriptive and fully reported. An absolute candidate PASS does not establish superiority.
Use C287.normalize_task and partition without its old identity-bound analyze to reconstruct60 final
partitions with correct/collapse,NLL,criterion failures,direct/full flags. This avoids another
mandatory diagnostic just to discover whether fitting or HOLDOUT was affected. Include180 paired
normal/collapse contrasts and all5 seed pairs;no exclusions,early stopping or best-checkpoint choice.

## Workload and output

10 models,8000 optimizer updates,384000 training row presentations.
Per model881 train/eval forwards and81 strict replay. Totals9620 forwards,539520 row presentations,
38480 core calls. One10-state checkpoint bundle write/load,10 strict state loads;network calls0.
Auxiliary loss adds arithmetic/autograd work,not model forwards. Equal step counts do not imply
equal wall-clock or peak memory. Do not claim cost-free learning improvement.
Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json,plus summary.json.
Schemas:fold-c288-pair-assignment-models-v1 and fold-c288-pair-assignment-eval-v1.
Saved postcheck reconstructs metrics,partitions,objective traces and schedules with neural calls blocked.

## Authoring,protection and stop

OWN6:source,test,runner,launcher,preregistration,design. Accepted source/tests remain immutable.
Source574=568+6;protected1026=1016+4 new parent inputs+6 OWN;dependency-union64.
Only direct repository import is C287;reachable C286/C284/C283/C282/C278/C269/C267 and core helpers
are in inherited pins. Own40;modules173;loaded4158;focused4157. Sole inherited exact C204 exclusion.
Manifest SHA256:44b114f22e06b214f3567baea16cc8771da55566e128c3c2d35b47023ba313d5.

Commit/refetch OWN6 for independent review,then activate. Validate real parent provenance,real
training tensors/complete pairs/initial models,own40 and actual focused4157 before science.
The dispatcher/selected launcher/runner need PowerShell ParseFile in the invocation path.
Operational skip does not publish science. Integrity failure retries SAME C288;valid gate miss
is ACCEPTED VALID NEGATIVE. No parameter,loss weight,margin,seed or gate tuning after results.
Gate F stays NOT PASSED. C289 is not registered until C288 is formally judged.
