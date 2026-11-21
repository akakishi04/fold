# C302 formal acceptance — frozen gain/weight cross

C302 ACCEPTED PASS (diagnostic integrity only). C301 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C303 NOT REGISTERED in this acceptance commit.

## Evidence identity and execution validity

Scientific execution HEAD: cfb1092c859f9e5512dcfdd63858973ab2194710.
Published log commit: 4ce7a79c904dac84c6916825d1d801d202580665.
The publication changes only docs/experiment-run-logs/c302/latest.json and latest.log.
Metadata log SHA256: 741102f8ebb56750c675f937c134702c4e036aa6055b02a412f5ffd61f381b17; 820513 bytes.
Summary: runs/c302-v5b-gain-cross-d81285be58684cbfbb6d3ec7253a42ca/summary.json.
Summary SHA256: 1054849a7c416eb0a32f53e114df5501401b3f4acfeec1f6dc5aa4276d302b10.
Manifest: 283f4ac996eda2ac866a192408fff2368782b8592d350c11af33723f874f2960.
Own32 and focused4669 passed; the log reports focused runtime372.345s.
Source658/protected1217. All10 states and original/swapped/original evaluations completed.
All original/restored outputs matched with error0.0; all_weights_preserved=True;
all_hooks_restored=True; persisted_gain_cross=PASS; tracked tree clean;
execution HEAD preserved; run_execution_valid=True. No C302 rerun is needed.
Science: training0,2430 model forwards,233280 row presentations,9720 core calls,
10 strict model-state loads,one existing checkpoint bundle read,no new model checkpoint.

## Deciding measurements

Counts(two_char,triple,quad) for each fixed weight set and inference gain:
- fixed_gain weights / unit gain: (2,2,2) out of5;
- fixed_gain weights / same-seed trained gain: (2,2,2);
- learned_gain weights / unit gain: (3,2,1);
- learned_gain weights / same-seed trained gain: (3,3,1).
Exchanging the final coefficient does not rescue any additional quad gate in this cohort.
This does not mean the individual predictions are unchanged.

For301003,quad HOLDOUT has288/288 correct with fixed-trained weights at EITHER gain,
and287/288 with gain-trained weights at EITHER gain. Returning the gain to1 does not undo
that loss of a quad pass. At the trained gain,the gain-trained weights also lose one TRAIN-value
quad answer relative to fixed weights; at gain1 the TRAIN-value quad answers are all correct.

For301005,the HOLDOUT counts(two/triple/quad) form this cross:
fixed weights/unit:278/273/262;
fixed weights/trained:279/274/266;
learned weights/unit:288/287/279;
learned weights/trained:288/288/283 (denominator288 each).
Both an immediate coefficient effect and differences between learned weight states remain.
Do not attribute all improvement to one of them or add accuracy differences as causal shares.
For301001 at unit gain,changing fixed-trained to gain-trained weights reduces HOLDOUT correct
counts141->120,135->119,132->121; benefits are not uniform across seeds.

## Interpretation and next boundary

The tested gain exchange is not a correction for the current reliability failures. No further
coefficient sweep or best-of inference is adopted. C301 changed optimization as well as the final
coefficient; C302 makes a purely final-coefficient explanation insufficient for the observed
quad pass difference. It does not identify a unique training mechanism or a defective component.

A next experiment may change gradient flow while retaining the original forward sum,using fresh
paired initializations and unchanged data/gates. Any such intervention must explicitly account
for which components stop receiving gradients; nominal parameter equality is not equality of
actively learned capacity or backward compute. It requires separate preregistration,tests and
committed-byte review before command release. No C303 execution is authorized by this file.
