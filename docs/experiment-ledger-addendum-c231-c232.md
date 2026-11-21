# C231 acceptance and C232 boundary

## Formal verdict

**C231 ACCEPTED PASS (evaluation-instrument audit). Gate F remains NOT PASSED.**

Scientific execution HEAD: `06a1b674d58f16816a3f47ec36dc3843e7e1dc37`.
Published log commit: `429cb50b326e2013503058c9cebd3468654e73ba`.
Log SHA256: `d3573869fa797567ff2542941f1286a11e9d15b27b0966ed63c9a11d43b13fea`.
Summary SHA256: `53f9c163beeeab1617eb8946e902cb29c2bbc4a94fb869d3325381160107b522`.
Local summary: `runs/c231-v5b-byte-eval-9e4c4cd1513a4b3c97e598252f6300c5/summary.json`.

## Execution validity

Own24 tests passed in1.443s. Focused2689 tests passed in56.379s. Source/artifact precheck reported
232 protected source pins and322 protected inputs. The result, metadata and registration name the
same scientific execution HEAD. Publication changes only the console log and receipt.
Final artifact/input checks, clean-tree check and run_execution_valid all passed.
This verdict uses published execution evidence and the recorded local postchecks. It does not claim
a reviewer rerun or direct access to user-local checkpoints and artifacts.

## Deciding metrics

Three seeds231001/231002/231003;13488 parameters per untrained V5-B model.
Each seed made126 forwards;378 total.246 scored target positions represent82 fixture bytes repeated
across three initializations, not246 independent text examples.

Maximum batch/singleton logit difference:1.3322676295501878e-15.
Maximum independent likelihood scoring difference:1.7763568394002505e-15.
Suffix-control difference0; reload difference0. All12 short generation replays matched exactly.
All checkpoint roundtrips and unchanged-weight checks passed. Training steps0.
byte_evaluation_contract_gate True; meaningful_language_score False.

Artifacts:
- byte-fixture.json: `5dcdbd8223c0e40df8d9e3fb5c98e50873a0a014ce9a3c2e003fe74d3911ce23`
- evaluation-plan.json: `745c97d3aab18c129494357cc91eb48a6e713294e437b17700be22da8bd3bf83`
- measurements.json: `c4bac00541cded4f937d879580cec12e7476319acd1fdccd6d62df955e5e4375`
- untrained-models.pt: `3964642731892977ddf24799465f82e963209dc74b070812a6165401dcc66590`
- validation-summary.json: `316435e0a31e0559a73368171df186336852990f16e4aa55b322e776ba281938`

## Interpretation and non-claims

The existing fixed-slot, teacher-routed V5-B reference can be evaluated with observed-prefix-only
next-byte inputs, consistent likelihood accounting and repeatable serialization/generation.
The four authored sentences and random-model scores demonstrate instrumentation only. This is not
useful language understanding, fluent generation, general reasoning, compressed-core superiority,
learned-memory integration or V5-G completion. Prefix-boundary EOS remains an explicit adapter
convention, not an ordinary uninterrupted autoregressive token stream.

## Next one-question boundary

C232 will ask whether a fixed small training budget on authored bilingual sentences reduces held-out
noun/color-combination byte loss versus the same model's initialization and a train-only smoothed
unigram reference. Split the underlying noun/color pair across all languages/templates as a group,
not random prefix rows. Keep the model, fixed route, prefix encoding and precision unchanged.
No public-corpus download, larger model, parameter-compression change or memory optimization.

C232 is NOT REGISTERED by this acceptance document. Its own preregistration must fix the dataset,
optimizer, seeds, budget, comparisons and negative-result interpretation before execution.
