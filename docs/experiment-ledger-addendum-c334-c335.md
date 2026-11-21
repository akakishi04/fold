# C334 acceptance / C335 authoring boundary

Date:2026-10-20 Japan time.
C334 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C332 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED;no first_mean/off-diagonal/production adoption.
C335 is NOT registered by this acceptance. No C336 authorization.

## Evidence identity and validity

Execution:c6e9ead698ed053d2e96a93ff13febffb3d1b049.
Log publication:82592e96643a9bf7c554e05c432b91b0eb1b79b2;sole parent equals execution.
Publisher metadata:231746 original Windows bytes;SHA256
b4ce80a12d4d089dc31083b0dad204173cf6c103903ddbfe7148eee0e577748d.
Log blob:cdaefd7f2d1a10951487be316b54c989da7f8234.
Metadata blob:8929be0469127adb0008ad538c1517d54785639a.
6010 tests/224 modules,0failures/errors/skips,successful=true;1482.623seconds including
sequential process orchestration. All10 own/cross/own comparisons completed with
unchanged weights. Saved reconstruction,all3430final uncached rereads and fresh
verification passed;all terminal process exits0;run_execution_valid=true.
All10 printed max_control_drift values are0.0. This is replay evidence,not accuracy.

Folder:runs/c334-policy-crossover-2a49146b93204814986d1a320cd5f78f/.
Primary science/summary.json SHA256:
12130d6d096cd287a7f415108b5f71738bcc86d8ef439c7930ba4b0a390fbf81.
Mandatory execution-envelope.json SHA256:
1efb6d154a4c617da3547e9fce3c22fc224caf36fa32aea81d00eabec6bbea68.
Scientific manifest:7cfbcfdd88bcfbe55bc7e7f9e84b839984f4f7cac01510330027622e71cc69ce.
Accepted source/input unions865/3430. Parent output inventory for a successor is457:
4science+primary+envelope+3regression records+224module JSON/log pairs. All451test
proofs are mandatory;do not inherit just the small aggregate receipt.

Review used exact-ref metadata,commit ancestry,registration/terminal records,all30
factorial rows and all10crossover records. Counts were independently added from
published rows. No independent whole-Windows-log rehash,read of every local module
receipt,raw tensor recalculation or model replay is claimed. Older attached C323/
C324 logs are not this run. Publication alone was not used to infer success.

## Deciding HOLDOUT counts

Column order NN,NF,FN,FF: first letter training policy,second inference policy;
N=native,F=first_mean. Each domain has1440answers and720both-query-correct pairs
across5seeds. These are repeated task assessments,not1440independent novel tasks.

|Domain|NN answers|NF answers|FN answers|FF answers|NN pairs|NF pairs|FN pairs|FF pairs|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|original2|1440|1440|1439|1440|720|720|719|720|
|original3|1440|1440|1440|1440|720|720|720|720|
|original4|1440|1439|1436|1440|720|719|716|720|
|original5|1440|1425|1422|1428|720|705|702|708|
|original6|1405|1356|1403|1412|685|639|687|696|
|interior4|1440|1437|1400|1415|720|717|683|696|

On native-trained weights,changing inference to first_mean decreases original6 by
49answers/46pairs;all5seeds have negative original6answer gains(-11,-2,-10,-5,-21).
On first_mean-trained weights,restoring native inference decreases original6 by
9answers/9pairs and interior by15answers/13pairs. Thus neither global swap fixes the
original capability failure. Original6 training-by-inference interaction is+58answers/
+55pairs:FF-FN is+9/+9 while NF-NN is-49/-46. This arithmetic is NOT a mediation claim.

First_mean-trained seed332002 becomes full-pass with native inference,but332003
loses its interior gate and332004 worsens:interior263->251answers,120->110pairs;
original6276->267answers,136->127pairs. Full-pass model counts for NN/NF/FN/FF are
0/0/1/1,with different successful seeds in FN versus FF. No per-seed selection.
The original C332 matched-policy diagonal and its candidate_gate=false remain intact.

## Interpretation and next bounded question

These controlled fixed-state swaps show dependence on training/inference pairing,
not a universal benefit of first-byte blending and not a complete internal-mechanism
explanation. Returning the weak332004model to native does not repair it. Inference
policy selection from observed HOLDOUT performance would be post-hoc selection.

A next equal-budget experiment may test training-time exposure to BOTH readout
policies while keeping evaluation strictly native. Use fresh paired initializations,
the same2400updates and same TRAIN events;alternate policies deterministically with
opposite parity in the second1200-event cycle so every event gets each policy once.
The comparator uses native on both visits. This changes training policy exposure,
not capacity,examples,thresholds or inference selection. It is an untested hypothesis,
not evidence that alternation improves robustness or a registered execution command.
Implementation,preregistration,committed-byte review and activation remain required.
