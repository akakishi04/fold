# C304 formal acceptance — length-breadth valid negative

C304 ACCEPTED VALID NEGATIVE. Candidate two_three_four passes2/5 five-character gates,
not the registered5/5. Four_only passes3/5;three_four passes2/5. Gate F NOT PASSED.
C305 NOT REGISTERED in this acceptance commit. Do not rerun C304.

## Execution evidence

Scientific execution HEAD:f309fde3e2aa8df33156ce55c703c9c37c6e106b.
Published log commit:e54f443acbbc5e55d3dcab18d08c418d56867d1e.
Publication changes only docs/experiment-run-logs/c304/latest.json and latest.log.
Metadata log SHA256:b54192fb8960369f687c9ceae37c5b985246a1b2e3b43cbe3226cc6afe302732;790487 bytes.
Summary:runs/c304-v5b-length-breadth-5090e7ce18a8444e9095afe14ad41266/summary.json.
Summary SHA256:c4b0babc2f7b9ea544c96385ed386a721630ce81bfb26fcb5e1e028450670717.
Manifest:af8f2ffc7b04e27bdd3597ede0d5b2cd55b6b6b526238dabf11a1b17f3edd9a0.
Own40/focused4749 PASS;focused run982.534s. Source670/protected1243.
All15 models completed1200 updates and all four lengths were scored/replayed.
Persisted_length_breadth=PASS;all_groups_matched=True;tracked tree clean;
execution HEAD preserved;run_execution_valid=True. Capability FAIL is not execution INVALID.

## Deciding metrics

Counts in four_only/three_four/two_three_four order:
length2:0/1/2;length3:2/2/2;length4:3/2/2;length5:3/2/2.
All four length gates simultaneously:0/1/2.
Fitted TRAIN direct (over each arm's trained lengths):3/2/3.
Trained-length HOLDOUT direct:3/2/2.
The same individual model passes/fails length4 and length5 in all15 cells.
This does not imply identical predictions or errors at these lengths.

Five-character passing seeds:
four_only304002/304003/304005;
three_four304003/304005;
two_three_four304003/304005.
Candidate304003 and304005 pass every length. Candidate304001 passes fitted TRAIN direct,
but fails HOLDOUT at trained lengths. Candidate304002 and304004 fail fitted TRAIN direct.
For304002,candidate HOLDOUT correct at lengths2/3/4/5 is152/151/149/144 out of288;
four_only has288/288 at lengths3/4/5. Candidate failure is not isolated to unseen5.
Candidate304001 TRAIN at2/3/4 is576/575/575 out of576 (passes local direct thresholds),
but HOLDOUT is120/123/120 out of288. Do not call TRAIN-direct PASS perfect memorization.

## Interpretation and non-claims

At the registered1200-update common64-slot budget,broader length allocation did not improve
five-character reliability over four-only. It improved full-range coverage for some cells,
not an adopted reliable policy. No arbitrary-length rule,universal harm from diversity,or
causal attribution to a single learning mechanism follows. Exposure allocation and temporal
spacing differ between arms. Historical48-slot cohorts/different seeds are not causal controls.
The observed4/5 gate agreement motivates an aligned saved-output check before another fit:
how many five-character errors were already errors for the exact same facts/query at4,and how
many are newly introduced or repaired by the length change? Preserve all15 models and every
logical row;use2/3 as additional descriptive references. No retraining,threshold changes or
restricted decoding. C305 requires separate preregistration,software tests and remote-byte review.
