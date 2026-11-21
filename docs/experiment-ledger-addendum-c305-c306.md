# C305 formal acceptance — saved cross-length overlap

C305 ACCEPTED PASS (diagnostic integrity only). C304 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C306 NOT REGISTERED in this acceptance commit.

## Evidence and validity

Scientific execution HEAD:9c8beb3c66548c1e68def4ea2ced93acc0067e6e.
Published log commit:f89d33f9dd0dd84a54f045541117ca48a4f0a342.
Publication modifies only docs/experiment-run-logs/c305/latest.json and latest.log.
Metadata log SHA256:a14943c1174ce0ad9643b689b1e1a593ec75284f1d3e872bfa23eb244ce5f8e3;765667 bytes.
Summary:runs/c305-v5b-length-overlap-4d5851c168fc401cbc5926f1d1ca841c/summary.json.
Summary SHA256:dd8580fe7f544b2e94688c4236cb862cfc77bb57984b04e5116a2c2cd8cc4734.
Manifest:844119479e6a43fc9fa5d3510ce05d8300ed2108dd819c6058b24b3b449632bd.
Own32 and focused4781 PASS;focused suite765.668s;source676/protected1257.
Saved reconstruction PASS;diagnostic_complete=True;tracked tree clean;execution HEAD preserved;
run_execution_valid=True. Scientific learning/model forwards/state loads/checkpoint writes are0.
C305 verifies the exact C304 output and original masked/full gates before aligning the final logits.
All15 models,12960 aligned rows/51840 saved normal predictions retained;720 totals/120 partitions reconciled.

## Deciding four-to-five observations

For two_three_four HOLDOUT,each of the three failing seeds:
seed304001:five errors168;persistent168;new0;recovered0;same wrong answer166;changed wrong answer2.
seed304002:five errors144;persistent136;new8;recovered3;same wrong answer133;changed wrong answer3.
seed304004:five errors118;persistent114;new4;recovered1;same wrong answer112;changed wrong answer2.
The other two candidate seeds have no errors at4 or5.
Across all five candidate seeds:430 five-errors,418 already wrong at4 (97.2093023255814%),
12 newly wrong at5,and4 recovered at5. This is a pooled descriptive count of dependent observations,
not an independent success rate or new capability gate. Persisting errors need not predict the same byte.
For candidate TRAIN-value examples:70 five-errors,57 persistent,13 newly wrong and2 recovered.
Length-specific errors therefore also exist;do not say length is irrelevant or solved.

C304 counts remain five3/2/2 in four_only/three_four/two_three_four order. All original verdicts
and local/masked thresholds remain unchanged. Error overlap alone does not establish memorization,
attention failure,or which gradient/initialization mechanism caused these outcomes.

## Next intervention rationale,not registration

The dominant candidate HOLDOUT errors predate the extension from4 to5. Keep2/3/4 training and5
as unseen evaluation rather than extending to6 or adding another output-only audit. A separately
registered fresh-seed paired comparison can test ordinary full training versus fixed core weights
at this broad-length setting. C303's core_frozen control improved seen tasks and reached4/5 quad,
but that was a different48-slot/two-length/800-update cohort,not proof this policy will work here.
C306 must keep common64-slot model,1200 updates,training data and matched schedule;no residual
stop-gradient or inference-path deletion. Candidate core stays at each seed's random initialization;
all other weights learn through it. No selection of previously successful cores. This tests the
whole training policy,including fewer trainable weights,not a uniquely isolated causal mechanism.
C306 requires its own preregistration,tests,remote-byte review and activation. C307 NOT REGISTERED.
