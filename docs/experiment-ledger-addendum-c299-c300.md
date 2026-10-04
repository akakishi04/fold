# C299 formal acceptance — core/remaining-backbone diagnostic

C299 ACCEPTED PASS (diagnostic integrity only). Gate F NOT PASSED.
C298/C297 remain diagnostic ACCEPTED PASS;C296 remains ACCEPTED VALID NEGATIVE.
C300 NOT REGISTERED in this acceptance commit.

## Evidence identity

Scientific execution HEAD:1ef1436febee7b2a70b2b91cb7a5dcb2a9e04d0c.
Published log commit:e1013d119956a3be000667ce6ac468d7eabb8cdf.
Publication changes only docs/experiment-run-logs/c299/latest.json and latest.log.
Log SHA256:4ab5c4c7085a36e56e0af3757198e54c0476644de30c22f34626c88b7da2ab9c;728598 bytes.
Summary:runs/c299-v5b-core-grid-d118c6d85dfa47dbaac6ce40655b2fe6/summary.json.
Summary SHA256:d0b2c055e190a313e5abc399716e2ec0cddfb104cc447a6216f2fab0ed312851.
Manifest:796fc20a254a8d65111d22f4b2754ae12f43975d869c9ca2fd8b7a6e90c7e846.

## Execution validity

Own32/focused4557 PASS;focused suite424.375s. Source640/protected1176.
All9 cells complete:7200 updates,345600 training rows,8658 model forwards,485568 total rows,
34632 core calls. components_matched=True;persisted_core_grid=PASS;tracked tree clean;
execution HEAD preserved;run_execution_valid=True. All3 C298 fixed-reader reproduction controls
match exact initial/final states and800 losses;reported all-view maximum logit error0.0.
No scientific rerun,source repair or changed verdict is needed.

## Deciding observations

Rows=remaining_seed297001..3;columns=core_seed297001..3;reader297001 and order297101 fixed.
Quad full gates:[[T,F,F],[F,F,F],[T,F,T]] (3/9).
Two-character and three-character:[[T,F,F],[T,T,T],[T,T,T]] (7/9 each).
The two combinations remaining297001/core297002 and remaining297001/core297003 also fail
seen-length TRAIN direct gates. This differs from the all-seen-pass C298 grid.
All three same-source diagonals reproduce the appropriate C298 fixed-reader column.

For remaining297001:
- core297001:two/triple TRAIN576/576 and HOLDOUT288/288;quad864/864.
- core297002:two TRAIN525/576,HOLDOUT132/288;triple TRAIN526/576,HOLDOUT136/288;
  quad TRAIN519/576,HOLDOUT147/288 (198 total normal errors).
- core297003:two TRAIN559/576,HOLDOUT157/288;triple TRAIN558/576,HOLDOUT159/288;
  quad TRAIN553/576,HOLDOUT159/288 (152 total normal errors).
For remaining297002:quad correct575+287,576+286,564+281 (2/2/19 errors).
For remaining297003:quad correct576+288,576+287,576+288 (0/1/0 errors).

## Interpretation and limits

There is no universal good or bad core donor in this finite grid. Core297003 works with
remaining297003 but severely fails with remaining297001;the remaining297002 row is not rescued
by any tested core. Joint initialization affects both fit and transfer at these known levels.
This does not identify a unique hidden cause,prove a defective architecture,or establish population
variance. Jointly trained components cannot be interpreted as independently learned skills.
These targeted,dependent outcomes are not fresh-seed replication;no winning donor is deployed.

Before more initialization subdivisions,a separately preregistered frozen inference diagnostic
can test sensitivity to the two tensors added before readout normalization:post-core residual
and added reader output. It must preserve all9 learned states,validate original predictions before
and after interventions,and report improvements AND regressions without changing any old gate.
This tests inference-time contribution,not which training mechanism caused C299's outcome.
C300 requires separate implementation,preregistration and committed-byte review before activation.
