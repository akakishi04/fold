# C306 formal acceptance — valid negative, promising but not reliable

C306 ACCEPTED VALID NEGATIVE. The registered candidate core_frozen reaches4/5 unseen-five
full gates,not5/5. Concurrent full_train reaches3/5. C305 remains diagnostic ACCEPTED PASS;
C304 remains ACCEPTED VALID NEGATIVE;Gate F NOT PASSED. No C306 rerun is needed.
C307 NOT REGISTERED in this acceptance commit.

## Evidence identity and validity

Scientific execution HEAD:cb2bb51a8beaa888c3a8b1fca382cd20536c923b.
Published log commit:340f9034fc07df63cff928bfd13703dfee5ca379.
Publication changes only docs/experiment-run-logs/c306/latest.json and latest.log.
Metadata log SHA256:c55c5ec3bb92c079ee89cbbca4aad5b8571143adb76fdfc82f612e5ee8b8a864;771898 bytes.
Summary:runs/c306-v5b-broad-core-freeze-f8b13e726f314db09555a293f6d6bdf8/summary.json.
Summary SHA256:5435cf83c02b75c2dd1d3c21105dcdf30e8c567c9d8672993f7676166515cff3.
Manifest:28a55839e6cf0c31ceac29fafb7e535b30d24259a0983589ebd4ae6121080b27.
Own32/focused4813 PASS;focused suite807.467s. Source682/protected1267.
All10 fits,all-length/full-view evaluation and strict replay completed. all_pairs_matched=True;
persisted_broad_core_freeze=PASS;tracked_tree clean;execution_HEAD preserved;run_execution_valid=True.
The implementation pins all inherited deciding helpers,including C305/C304 and C304.PINNED.
Frozen-core invariants and saved result reconstruction were mandatory in the successful run.
Scientific FAIL is a valid unmet capability gate,not an invalid execution.

## Deciding metrics

Length2/3/4/5 full-gate counts(full_train/core_frozen):4/5,3/5,3/5,3/4.
Fitted TRAIN direct4/5 versus5/5;trained-length HOLDOUT direct3/5 versus5/5.
All-length simultaneous passes3/5 versus4/5.
Candidate rescues306002 and306005 at five,loses306003,and both arms pass306001/306004.
No universal per-seed improvement is claimed.

Every candidate model answers all normal TRAIN and HOLDOUT questions correctly at lengths2/3/4.
At five,the candidate answers all normal TRAIN-value questions correctly;its only normal error
is306003 HOLDOUT287/288,which fails a local accuracy/query-pair criterion. The full-train arm
has288/288 there. The candidate's pooled five normal total is4319/4320,not an alternative gate.

306005 full_train:TRAIN correct2/3/4/5=512/514/512/513 out of576;
HOLDOUT correct2/3/4/5=136/130/131/130 out of288. Candidate is perfect in all these partitions.
306002 full_train:HOLDOUT2=288/288 and3/4/5=287/288;candidate is perfect.
The two candidate rescues differ substantially in error severity;show them separately.
Actual gradient-receiver union14256 in every full arm,10928 in every frozen arm. This is not
an equal-backward-FLOP comparison or evidence the core is unnecessary;the core still computes
and conveys gradients to upstream inputs. TRAIN fits do not prove arbitrary-name reasoning.

## Interpretation and next-question boundary

This is encouraging evidence for the fixed-core training policy at broad2/3/4 coverage,but only
five new paired seeds and one held-out task family were measured. Fewer trainable weights,global
clipping and changed optimization remain bundled in the policy. Do not diagnose a unique core
mechanism or select a successful donor. The candidate's one remaining error does not justify
retuning against that exact question or changing original thresholds.

Before another intervention,a separately preregistered fresh-seed replication should repeat the
same two arms,data,64-slot model,1200 updates,optimizer and scheduling algorithm,changing only the
five initialization/order seed pairs. Keep C306 negative permanently;report replication separately
and retain all successes and failures. No new strings,additional training lengths,loss changes,
coefficient search or cherry-picked pooling. C307 requires its own committed-byte review and
activation before a launcher is issued;C308 NOT REGISTERED.
