# C261 acceptance and C262 minibatch-order boundary

## Formal verdict

C261 ACCEPTED VALID NEGATIVE. The registered joint new-task gate requires both arms5/5;
with_core passed4/5 and without_core3/5. Prior verdicts,including C260's negative,remain unchanged.
Gate E PASSED;Gate F NOT PASSED. No architecture adoption or core-superiority claim.

Scientific execution HEAD:5de24467fd439378505a2357e898fc618de31d45.
Published log commit:d441c7e5a699bbb55558261a910483057b70e0f3.
Publisher log SHA256:1341aa09aaaab7f78a3aabadaaf4263cd6bdaa2c71fcdc695d1dbda0459d8bb6.
Log bytes:786878.
Summary SHA256:555ea1f2a1ae6970283d9b7784b0e382f6f58be202d493c0157c706c1255f9bf.
Summary:runs/c261-v5b-repeat-value-66e5eb87a146491e833bbd2f32ce6989/summary.json.
Metadata,registered execution HEAD andprinted summary agree. Publication changes only C261 latest.*.
Acceptance uses immutable published log ranges andrecorded local postchecks. The reviewer did not
independently execute the accepted learned states orrehash the entire log;publisher hashes are
reported identities,not a newly computed complete-byte reviewer hash.

## Execution validity

Own24 PASS in10.060s;focused3429 PASS in153.846s.
412 source pins/685 protected inputs passed. All ten frozen states were evaluated:
540 model forwards,95040 row presentations,1080 Full core calls,one learned bundle load,ten strict
state loads. New training0;new learned checkpoint writes0. Accepted-output anchor replay,restoration,
finite-output checks,weight preservation,persisted score recomputation andprotected inputs passed.
Tracked tree clean;scientific execution HEAD preserved;run_execution_valid=True.
scientific_status=FAIL;joint_gate=False;all_replays=True;all_weights_preserved=True.

## Deciding evidence

|Seed|with_core repeated-value gate|without_core repeated-value gate|
|---:|---|---|
|260001|PASS|PASS|
|260002|PASS|FAIL|
|260003|PASS|PASS|
|260004|PASS|FAIL|
|260005|FAIL|PASS|

This is exactly the same per-state pass/fail membership as C260's distinct-value task,although the
new-task metric contract andassignments differ. All seven previously passing states pass the new
repeated-value criteria;the three previously failing states still miss the new gate. This is a
descriptive cross-task correspondence,not an independent replication or a universal predictor.

The three failing new-task total scores are:
-without_core260002:999/1440;
-without_core260004:972/1440;
-with_core260005:836/1440.
These pooled totals do not replace per-language/order/stratum/singleton/triplet/six-order criteria.
For example,without_core260002 EN pair_equal order012 is79/108,with singleton accuracy30/36,
repeated-target accuracy49/72 andcomplete query triplets11/36. Its EN all_equal order012 is8/12.
Thus the observed failure is not solely the invalid old query-mask threshold;that threshold was
correctly descriptive only. The successful with_core260001 state scores1440/1440 including cases
where a minority value must be selected. No universal inability to handle repeated values follows.

## Interpretation and limits

Allowing repeated values did not introduce an additional failed state among the seven states that
met C260's bounded gate. The remaining weakness spans both tested task variants. We have not isolated
why training yields a successful orunsuccessful state. In particular,previous 'seed variability'
changes both model initialization andthe sampled minibatch sequence;it is not evidence that initial
weights alone explain the outcomes. C260's batch_plan uses seed+256000+epoch while make_pair also
uses the seed. C261 freezes those outcomes andcannot isolate either training factor.

Keep both architecture paths. No general-language skill,statistical independence,initialization-
population guarantee,causal internal mechanism orGate F passage is established by C261.

## Accepted artifact identities

-eval-outputs.pt:ad2b19919cae9a258aef91e6c50596ab3624ab4df6b86f1b251c9a5b75c81fd2;194720583 bytes.
-measurements.json:1f0b7d3e23f14ea744683cd90c504e82e95d307b6668cfaa3047e6310d25934b;93956 bytes.
-repeat-dataset.json:1cf918049e4661bd11fc0aba90212e34eccd3e544c41b953f93ff5e3c1e59339;245666 bytes.
-repeat-plan.json:bf8c32a5916d968871daeaa6ecf0c1fe38d75cd98b11d2d26096d578ff1a1301;2708 bytes.
-validation-summary.json:fc1926548185238f6464bdf30900597d4147eb58be767be14aed901d6b6fa962;826 bytes.

## Next question,not activation

With the same Full aligned-reader initialization,exactly the same minibatches and800-update budget,
does changing only their chronological order alter held-assignment performance? Use five fresh
initializations262001..262005 andpaired forward_blocks/reverse_blocks arms,without reusing learned
states. Both arms use the same six-order task andsame per-epoch48-row blocks. Reverse the order of
blocks within each epoch,not the facts within a prompt. Reverse only the consumed two blocks in
the final incomplete epoch so per-prompt exposure totals remain identical even at the800-step tail.

This is a controlled training-order intervention,not a new architecture,additional training of a
failed state,or another frozen-input formatting probe. Report performance changes,answer flips and
both-arm reliability under the unchanged distinct-assignment criteria. A different result can show
sensitivity to this order intervention in these pairs,but cannot establish the cause of all past
failures oruniquely isolate an optimizer mechanism. Equal outcomes do not prove all order choices
irrelevant. Separate preregistration/review controls C262 activation;C263 NOT REGISTERED.
