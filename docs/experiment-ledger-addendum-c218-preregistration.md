# C218 preregistration — V5-F learned semantic Writer pilot

**C217 ACCEPTED PASS. C218 ACTIVE / NOT YET JUDGED. C219 NOT REGISTERED.**
Gate E remains **PASSED**. Gate F remains **NOT PASSED**.

## One scientific question

Given a structured observation descriptor, can a learned Writer alone choose the correct
factor+relation on held-out nuisance input and preserve correct ASSERT/REPLACE downstream semantics
through frozen accepted C217 Selectors and C216 Readers?

## Parent checkpoint

C217 scientific execution HEAD:
`a6aac1273951b6e321573445e9f759f35fffb726`

C217 summary SHA256:
`cb27e93c9a6dc9d03875938c55c37f146c12278dec4c9ebb5a20da150fd847ab`

C217 validation artifact SHA256:
`7e46f83fc7c6702e36ede2d05f016018cf8d219c51248ef7d395815168409cf0`

C217 selector checkpoint artifact SHA256:
`ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215`

Inherited C216 Reader checkpoint artifact SHA256:
`bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af`

C218 validates:
- accepted C217 summary;
- all five C217 artifacts;
- all137 C217 source pins;
- all143 inherited protected inputs;
then extends the checkpoint with C218 OWN files.

## Changed variable

Learned factor+relation Writer only:
`fold_lm/v05/memory_writer.py`.

Architecture5->12->6; parameters150.

Operation kind remains oracle ASSERT/REPLACE.

## Fixed Writer data

- factors alpha/beta;
- semantic values -1/0/+1;
- six factor+relation classes;
- TRAIN nuisance [-1,-1],[-1,+1],[+1,-1];
- EVAL nuisance [+1,+1];
-24 rows /18 TRAIN /6 EVAL;
- each class exactly3 TRAIN /1 EVAL;
- Writer data SHA
  `06f8df444119f0332168a956e7f32e9690b88fa9c39749d3ecc2283c70213714`.

Controls:
- factor-blind EVAL accuracy0.5;
- semantic-blind EVAL accuracy1/3.

## Fixed downstream

ASSERT:
- six unequal semantic pairs;
- HOT and COMMITTED states;
- alpha/beta queries;
-24 rows per Writer seed;
- overall/HOT/COMMITTED accuracy1.0;
- placement mismatches0;
- write rejections0.

REPLACE:
- six target factor+relation classes;
- initial target value differs from requested replacement;
- downstream accuracy1.0.

Controls:
- forced wrong semantic -> downstream0.0;
- forced wrong factor -> downstream0.0.

All three C217 selector checkpoints and all three C216 Reader checkpoints remain frozen.

## Fixed training

Writer seeds218001/218002/218003.

Adam lr0.02, betas0.9/0.999, eps1e-8, weight decay0,400 full-batch steps, batch18,
CPU float32, threads2, deterministic algorithms.

Registered fixed workload:
- Writer models3;
- parameters150;
- training steps1200;
- training examples21600;
- Writer forward calls1212;
- frozen Selector forwards3;
- frozen Reader forwards72;
- total model forwards1287;
- learned Writer operation slots54;
- oracle initialization writes60;
- control writes12;
- chunk-commit slots96;
- Reader training steps0;
- Selector training steps0;
- network calls0.

Successful operation/commit counts are scientific gate metrics rather than execution-validity
workload requirements.

## PASS gate

Every Writer seed:
- TRAIN relation accuracy1.0;
- EVAL relation accuracy1.0;
- factor-blind0.5;
- semantic-blind1/3;
- checkpoint roundtrip exact;
- write rejections0;
- ASSERT overall/HOT/COMMITTED1.0;
- placement mismatch0;
- REPLACE1.0.

Global:
- wrong-semantic control0.0;
- wrong-factor control0.0;
- actual learned Writer attempts54;
- successful chunk commits96;
- all frozen selector/reader fingerprints unchanged.

Complete but gate-missing execution = scientific FAIL.
Source/artifact/schema/runner defects = INVALID / RETRY SAME C218.

## Scope / non-claims

Reader frozen.
Port Selector frozen.
Writer operation kind oracle.
Coverage classifier absent.
No natural language.
No Gate F decision.

## Authoring registration

OWN7:
- `fold_lm/v05/memory_writer.py`
- `fold_lm/v05_benchmarks/gate_f_c218_learned_writer.py`
- `tests_lm/test_v05_c218_learned_writer.py`
- `tools/run_c218.ps1`
- `tools/invoke_c218.ps1`
- this preregistration
- `docs/v5f-learned-writer-pilot-v0.1.md`

Expected:
- source pins144;
- protected inputs156;
- artifacts5;
- C218 tests38;
- regression modules103;
- loaded tests2260;
- exact historical exclusion1;
- focused regression2259.

Manifest SHA256:
`e855905bc1ff7c1b105608163a4483b7c5dbffb6d4ca5ce1a130ffb542493394`

Direct repository dependencies must all be parent/OWN pinned, including memory Writer, C217 Selector
contract and C216 Reader contract.

## Post-authoring review

`post_authoring_review = PENDING`

Do not issue C218 execution until committed remote bytes are independently reviewed for:
- accepted C217 summary/artifacts/selector checkpoint;
- inherited C216 Reader artifact resolution through parent protection;
- all137 parent source pins;
-144/156 accounting;
- Writer data hash/split/control collapses;
- operation-kind oracle boundary;
- frozen Selector/Reader fingerprints;
- ASSERT/REPLACE and wrong-semantic/wrong-factor paths;
- scientific FAIL versus execution INVALID accounting;
- fixed workload/manifest;
-38 tests /103 modules /2260->2259;
- free-name/import bindings;
- direct dependency coverage;
- runner CLI indexes;
- complete PowerShell source-string contract;
- C219 non-registration.
