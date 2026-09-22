# C217 preregistration — V5-F learned Port Selector pilot

**C216 ACCEPTED PASS. C217 ACTIVE / NOT YET JUDGED. C218 NOT REGISTERED.**
Gate E remains **PASSED**. Gate F remains **NOT PASSED**.

## One scientific question

Given correct H1/H2 memory and frozen accepted C216 Readers, can a learned Port Selector alone
route a held-out query descriptor to the correct alpha/beta memory port and preserve downstream
semantic answers?

## Parent checkpoint

C216 scientific execution HEAD:
`99d4254c09f38a433374fb2a073403d6e0ec764a`

C216 summary SHA256:
`7542625a054725d3a70dfa1c19f706fe8fce26af379e24b92aa1ae478483acc9`

C216 validation artifact SHA256:
`dddd27d04917f810a68dc83aa98cddabf1cd78cd67357c52b913e2ff3fe239be`

C216 Reader checkpoint artifact SHA256:
`bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af`

C217 validates the accepted C216 summary, all five artifacts and all130 C216 source pins, then extends
that checkpoint with C217 OWN files.

## Changed variable

Learned Port Selector only:
`fold_lm/v05/memory_port_selector.py`.

Architecture4->8->2; parameters58.

No memory values, Reader outputs, target classes, placement/status, scope or provenance enter the
selector input.

## Query split

TRAIN nuisance:
`[-1,-1],[-1,+1],[+1,-1]`.

EVAL nuisance:
`[+1,+1]`.

alpha descriptor `[1,0,n1,n2]`; beta descriptor `[0,1,n1,n2]`.

8 query rows /6 TRAIN /2 EVAL.

Query data SHA:
`a9ec25d8079e27177567dd4ca85c7aee18f511eb8e8db6b774a61af82e91ac3d`.

## Frozen Reader / downstream fixture

All three accepted C216 Reader checkpoints are used; Reader training steps0.

Downstream uses exactly six unequal semantic pairs, HOT/COMMITTED placement and both queries:
24 rows per selector model.

Correct routing must yield downstream accuracy1.0 for all frozen Readers.
Forced wrong routing must yield downstream accuracy0.0.

## Training

Selector seeds217001/217002/217003.

Adam lr0.02, betas0.9/0.999, eps1e-8, weight decay0,400 full-batch steps, batch6,
CPU float32, threads2, deterministic algorithms.

Registered workload:
- selector models3;
- selector parameters58;
- training steps1200;
- training examples7200;
- selector forward calls1209;
- frozen Reader forward calls18;
- total model forwards1227;
- oracle Writer operations12;
- chunk commits12;
- network calls0.

## Fixed PASS gate

Every selector seed:
- TRAIN port accuracy1.0;
- EVAL port accuracy1.0;
- query-blind EVAL accuracy0.5;
- checkpoint roundtrip exact.

Every selector seed × frozen Reader:
- downstream overall/HOT/COMMITTED accuracy1.0;
- forced wrong-port downstream accuracy0.0;
- placement prediction mismatches0.

A complete execution missing any criterion is a scientific FAIL.

Syntax/source/artifact/regression/checkpoint defects are INVALID / RETRY SAME C217.

## Scope

Reader frozen.
Writer oracle.
Coverage classifier absent.
No language mapping.
No Gate F decision.

## Authoring registration

OWN7:
- `fold_lm/v05/memory_port_selector.py`
- `fold_lm/v05_benchmarks/gate_f_c217_learned_port_selector.py`
- `tests_lm/test_v05_c217_learned_port_selector.py`
- `tools/run_c217.ps1`
- `tools/invoke_c217.ps1`
- this preregistration
- `docs/v5f-learned-port-selector-pilot-v0.1.md`

Expected:
- source pins137;
- protected inputs143;
- artifacts5;
- C217 tests36;
- regression modules102;
- loaded tests2222;
- exact historical exclusion1;
- focused regression2221.

Manifest SHA256:
`70af02a697ae8fc97f3d379bdab18dd49bf2261a319f7091819323de5c2b8ab4`

Direct repository dependencies must all be pinned, including C216 benchmark/checkpoint contract and
the selector production module.

## Post-authoring review

`post_authoring_review = PASS`

review HEAD:
`dd045bd38883b490910147ee429c9641601a0e43`

Committed remote review verified:
- accepted C216 execution/summary/validation/Reader-checkpoint identity;
- all130 C216 source blobs are present at their registered Git blob IDs;
- C217 OWN7 extends the source union to137 and parent summary+5 artifacts yield143 protected inputs;
- all nine deciding-path repository dependencies are parent/OWN pinned;
- query dataset hash independently recomputes to
  `a9ec25d8079e27177567dd4ca85c7aee18f511eb8e8db6b774a61af82e91ac3d`;
- manifest independently recomputes to
  `70af02a697ae8fc97f3d379bdab18dd49bf2261a319f7091819323de5c2b8ab4`;
- TRAIN/EVAL nuisance split and balanced alpha/beta targets are exact;
- selector production input is query features only; memory values are consumed only after port choice;
- all three C216 Reader fingerprints are frozen and Reader training steps remain0;
- downstream uses only unequal semantic pairs and explicit forced-wrong-port control;
-36 C217 tests,102 regression modules,2222 loaded /2221 focused counts are exact;
- executable c### alias binding defects are0;
- runner argv ordering is precheck argv[1], postcheck argv[1..3];
- complete test35 PowerShell source contract is satisfied;
- C218 remains unregistered.

No scientific threshold, split, seed, model architecture or workload was changed during review.

Do not issue C217 execution until committed remote bytes are independently reviewed for:
- accepted C216 summary/artifacts/Reader checkpoint identity;
- all130 parent source pins;
-137/143 accounting;
- query data hash and held-out nuisance split;
- selector input isolation from memory values;
- frozen Reader fingerprints and zero Reader training;
- unequal-pair downstream/wrong-port controls;
- fixed workload/manifest;
-36 tests /102 modules /2222->2221;
- free-name/import binding;
- direct dependency protection;
- runner CLI indexes;
- complete PowerShell source-string contract;
- C218 non-registration.
