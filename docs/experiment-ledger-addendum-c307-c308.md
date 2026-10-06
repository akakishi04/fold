# C307 formal acceptance — core-freeze replication

C307 ACCEPTED VALID NEGATIVE. The new core_frozen cohort passes3/5 five-character gates,not5/5.
Full training also passes3/5. C306 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED.
C308 NOT REGISTERED in this acceptance commit. No old experiment is rerun.

## Evidence identity and validity

Scientific execution HEAD:4371ad8de650261f6cdacacfd9972efcdbe970a8.
Published log commit:6cdbde45709579c736d2fc0bd682f992a6d63b25.
Publication changes only docs/experiment-run-logs/c307/latest.json and latest.log.
Log metadata SHA256:2419827fe4263a1d88e1f02b7c3c17d601193000fc384f80ddbd80b20fd7735a;776770 bytes.
Summary:runs/c307-v5b-core-replication-468c370e9c4b491585226c5492a8b52c/summary.json.
Summary SHA256:5cb0683de649361966f2ab549aeab94d20643d64fe68d1d8bbe3497e6d637e42.
Manifest:9662b7d5763768a09c75c961dc8f8453c40506eadcbb44639bbd50f7dca2ab8b.
Own32 and focused4845 PASS;focused run712.036s. Source688/protected1281.
All10 models complete1200updates,original evaluation and strict reload replay.
all_pairs_matched=True;persisted_core_freeze_replication=PASS;tracked_tree clean;
execution_HEAD preserved;run_execution_valid=True. Scientific FAIL is valid negative,not INVALID.

## Deciding metrics

Length2/3/4/5 full_train pass counts3/3/3/3;core_frozen4/4/4/3.
Both arms fitted-TRAIN direct4/5. Trained-length HOLDOUT direct full3/5,frozen4/5.
Five-character paired contingency:both_pass2,full_only1,frozen_only1,both_fail1.
Both pass307003/307004;frozen rescues307002;full alone passes307001;both fail307005.
Thus C306's five-character count advantage does not recur in the preregistered new cohort.
This does not establish that freezing has zero effect:individual outcomes and seen-length gates differ.

Frozen307001 is perfect at seen lengths but five-character TRAIN575/576,HOLDOUT287/288;
full307001 is perfect in those partitions. This is two normal five-character errors,not one.
Full307002 fits TRAIN but has HOLDOUT133/288 at lengths2/3 and136/288 at length4;
frozen307002 passes every length and value split. Keep this rescue visible.
For307005,full TRAIN2/3/4/5 correct518/525/524/517 out576,HOLDOUT103/107/107/105 out288.
Frozen307005 TRAIN517/519/514/509 out576,HOLDOUT115/119/119/124 out288.
Unlike C306,the frozen arm still has a substantial TRAIN failure. It is not a universal stabilizer.

## Interpretation and next boundary

Do not continue changing seeds until a favorable5/5 appears. The fixed-core policy is not adopted
as a general solution. Normal pooled accuracy or combining C306/C307 cannot supersede either
preregistered negative. These are new random seeds on the SAME task family,not external replication.

A separately registered next comparison may test core learning-rate attenuation rather than
complete freezing:ordinary full training,unchanged frozen-core control,and a core-only nominal
learning rate one tenth of the noncore rate. This is a prospective policy hypothesis,not a proven
mechanism or an optimal ratio inferred from C307. Keep broad2/3/4 training,unseen5,all masks and
original thresholds. No coefficient sweep,adaptive unfreezing or winner selection. C308 requires
its own committed-byte review before activation. C309 is not registered.
