# C255 acceptance and C256 task-shift boundary

## Formal verdict

**C255 ACCEPTED PASS — diagnostic integrity only.**
C252 remains ACCEPTED VALID NEGATIVE. C253/C254/C255 are diagnostics, not capability promotions.
Gate E PASSED; Gate F NOT PASSED. No production architecture adoption.

Scientific execution HEAD:`6b577da1edc7339dbfd68b3127870074de218e48`.
Published log commit:`48856dd7dabb84f1f8a71158d03a5ee9db2fd255`.
Publisher log SHA256:`a733f750125ccacfc5ce54867bce122c91561bd105e9d1eac1adaf04ab13bc2d`.
Log bytes:651389.
Summary SHA256:`6c4e9a569a7c622259b501f209781b357d183dfbaf5750a6d6c939f5e59e3150`.
Local summary:`runs/c255-v5b-value-residual-8203653a07964d9bb549c272a8b9b943/summary.json`.

The two prior C255 attempts remain INVALID and are preserved in
`docs/experiment-ledger-addendum-c255-execution-recovery.md`.
They are not scientific evidence.

## Execution validity

24 own tests PASS in1.534s;3289 focused tests PASS in122.954s.
376 source pins/611 protected inputs. Five frozen models;120 head evaluations/5760 head rows.
Full-model/encoder/core/reader forwards0;new training0;one accepted checkpoint-bundle load;
five strict model-state loads;new learned checkpoint writes0.
Self,C254-self,coherent-donor,restored and evidence-blind controls replayed;weights and inputs
preserved;persisted recomputation PASS;tracked tree clean;execution HEAD preserved.
`run_execution_valid=True`.

Accepted artifacts:
- contrasts.json:ecc69baf18f5824ad3c94be836ba55b2f05ace64f5b38d42825dbce37c48f228 (15286 bytes)
- diagnostics.json:111b4c2d98087f0d7e90cddda83ba53892eb74961cb4b0a564392eb36ccc51a4 (15433 bytes)
- head-outputs.pt:77a4e8a54e610a40cd7be3965e863d48e4f5058efebbc49637aa40d043cf1241 (11831621 bytes)
- validation-summary.json:69394982329cd77f7ae0d9739f7fe97e898444e331b697fa507287120be99b63 (480 bytes)
- value-plan.json:e5a6589105d534218c9056768c2af3e60da136a2dfb9f9fa8393bba9198a548a (2412 bytes)

## Deciding observations

HOLDOUT self correct =145/160.
Fixed-query reversed-value residual swap correct =140/160.
Transitions:7 correct-to-wrong,2 wrong-to-correct,9 answer flips,9 donor-target matches.

Per seed HOLDOUT EN/JA (/16):
-250001:self16/16,16/16 -> value16/16,16/16.
-250002:self9/16,9/16 -> value7/16,7/16.
-250003:self16/16,16/16 -> value16/16,16/16.
-250004:self15/16,16/16 -> value15/16,15/16.
-250005:self16/16,16/16 -> value16/16,16/16.

TRAIN self320/320 -> value309/320.

For comparison, accepted C254 HOLDOUT:
-order swap141/160;
-query swap96/160.
Thus the frozen residual/read combination is far more sensitive to changing query identity than to
reversing the value assignment under the fixed query. Query- and value-swap donors can have the same
target on this two-entity fixture,so this contrast argues against a simple target-value-only account.
It does not uniquely identify an entity/query code,binding algorithm or training-time core role.

## Interpretation boundary

The three swap diagnostics are correlated frozen interventions on one repeatedly inspected small
fixture. They recombine jointly trained features before LayerNorm and are not independent samples.
C255 PASS means integrity only. Do not convert C252's4/5 capability result into a PASS,do not claim
population reliability,semantic understanding,core superiority or Gate F completion.

The microtask diagnostic chain ends here. No C256 diagnostic is registered to further decompose the
same saved activations.

## Next question, not registration

Use a new task family and new seeds:
Does the C252 pre-core-query/pre-core-memory reader reproduce its binding/recombination advantage
over an equal-parameter EOS-only adapter on a fresh **three-entity** bilingual assignment task?

C256 must:
- use three entities rather than two;
- use fresh seeds256001..256005;
- use a new balanced 12-assignment TRAIN /12-assignment HOLDOUT split over distinct values0..3;
- expose two fact orders and three possible queries;
- keep all object-value marginals represented on both sides while withholding exact assignments;
- train Full candidate and equal-parameter Full EOS adapter from the same backbone initialization;
- use no C252 learned checkpoint or C255 activation;
- fix the training budget and gate before seeing results;
- retain all five seeds and report each language/seed independently.

This is a task-shift capability/stability test,not Gate F and not a general benchmark.
Separate C256 preregistration and committed-byte review control activation.
