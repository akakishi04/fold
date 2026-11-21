# C252 acceptance and C253 frozen residual-path boundary

## Formal verdict

**C252 ACCEPTED VALID NEGATIVE.** Gate E PASSED; Gate F NOT PASSED.
Four of five seed blocks meet both-language TRAIN/HOLDOUT criteria, but the registered primary
requires all five. C251/C250/C248 verdicts remain unchanged. No production adoption.

Scientific execution HEAD:2e3102b6f1d7061afcfd0bcf996ad660fcf36a36.
Published log commit:f0882790ca5deae784513c946e5d6e60481d02f2.
Publisher-recorded log SHA256:30416c085e0f1b1cd19b6aa3df73c435a7490414c02b0546dd15c7662e4f11c2.
Log bytes:626938.
Summary SHA256:18c176213aa0c047ddf9fe53f188e933e341f5e8556571c0a8999e7a36164f9e.
Local summary:runs/c252-v5b-precore-query-ea8199d8ca794acba051ca5f65a391b3/summary.json.

The publication commit follows execution by one commit and changes only c252/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges, publisher metadata and recorded local postchecks.
The reviewer did not independently rehash the full log or rerun the actual learned checkpoints.

## Execution validity

24 own tests PASS in24.330s;3217 focused tests PASS in181.128s.
358 source pins/575 protected inputs. Five models x400 updates=2000 updates/64000 training
presentations;2075 full-model forwards/67840 total row presentations.
All initial/checkpoint/prediction replays and weight changes PASS. Persisted query-alignment,
comparator and discrete-metric postchecks PASS. Protected inputs/tracked tree/execution HEAD
preserved;run_execution_valid=True. Scientific status FAIL;candidate_gate=False.

## Deciding metrics

All ten TRAIN language cells have32/32 correct,16/16 fact/query/order pairs, and pass both mask drops.
HOLDOUT counts per language (denominator16):

| Seed | C252 EN | C252 JA | C251 EN | C251 JA | C252 joint seed |
|---:|---:|---:|---:|---:|---|
|250001|16|16|16|16|PASS|
|250002|9|9|10|9|MISS|
|250003|16|16|10|10|PASS|
|250004|15|16|6|5|PASS|
|250005|16|16|16|16|PASS|

C252 language outcomes:BOTH_PASS8,RECOMBINATION_MISS2.
Whole-seed both-language passes4/5 versus C2512/5. Both previously passing seeds are retained;
250003 and250004 newly pass. The latter is NOT perfect:EN15/16,each pair7/8,within fixed thresholds.
Seed250002 remains9/16 each language;fact pairs3/8,query pairs1/8,order pairs4/8;
evidence drop0.3125,query drop0.1875. It fails multiple independent registered conditions.

Descriptive pooled HOLDOUT145/160 versus C251114/160. Language comparisons:4 improve,5 tie,1 worse.
These ten paired cells share five initializations and a repeatedly reused task;they are not ten
independent replications or an estimate of production reliability. No significance claim.

## Interpretation and limits

Using local-encoder EOS as the attention-query source, with pre-core memory already fixed, is a
promising matched change on this fixture. It improves the observed seed-pass count without new
parameters or training budget, but does not meet the all-seed gate. It does not prove that a
representation-space mismatch was the unique cause:the projections and gradient paths also matter.
The shared pre-core source is a design property, not proof that learned query/key spaces are identical.

Both query and K/V now originate before the FOLD core. The core still executes and contributes
through the post-core EOS residual base. Therefore this result alone cannot establish how much
of the achieved answer performance requires that post-core residual. Do not attribute all gains
to the core, remove it as supposedly useless, or adopt the candidate in production yet.

## Accepted artifacts

- alignment-plan.json:f662c4d9c5588bbc0662ae9f578dd59068354a76951bf7192f18f8e53166fd9b (2698 bytes)
- measurements.json:dc88a83ab9d8add4022ba898af9a030b787cd46e088c94b1d26e205c83c29b91 (21499 bytes)
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346 (15904 bytes)
- trained-models.pt:024e8081fae8bc45ce449b3bdf53745499911ca631387620a6575e2312c5b6c3 (619312 bytes)
- validation-summary.json:8442f683dfe0ed9122f476b723083d017a6cd5ef6e1087bca67dfd20fc167fbf (2462 bytes)

## Next question, not registration

In all five frozen C252 models, how much does normal answer performance depend on the post-core
EOS residual base, with the already-trained pre-core reader contribution held fixed?
Measure intact post+read,pre+read,read-only,and restored intact outputs on the unchanged original
three input views and both splits. The core still computes during each diagnostic forward;
only the vector entering the existing readout normalization is substituted. Count its cost.
Keep all seeds, including the failed one. No new training or checkpoint rewriting.

An unchanged score would show dispensability under this specific frozen intervention, not that
training never benefited from the core. A decline could reflect jointly learned dependencies or
normalization/distribution shift, not a uniquely identified causal reasoning mechanism.
C253 needs separate preregistration and committed-byte authoring review before activation.
