# C250 acceptance and C251 pre-core read-source boundary

## Formal verdict

**C250 ACCEPTED VALID NEGATIVE.** Gate E PASSED; Gate F NOT PASSED.
The unchanged reader shows repeated individual successes, but does not satisfy the registered
all-five Full/token_read seed gate. C248 and all prior verdicts remain unchanged.
No production adoption, seed replacement or reliability guarantee.

Scientific execution HEAD:7a9d48a99c1ca67c9eb05d0f68e7b4fa1284c881.
Published log commit:fc7d48e36e81d7b9fc8188f656771c757c398894.
Publisher log SHA256:45c93f81d69889217e60206cbd035a977ca1b2d1852c5ec464603cc3085d3098.
Log bytes:636029.
Summary SHA256:c965176039448ac99e812ad4abfce78950aafc271c65d4676bd47fe7aa59dc07.
Local summary:runs/c250-v5b-fresh-seed-replication-9bf33a726c614e558f446871954550d7/summary.json.

The log publication is one commit after execution and changes only c250/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges and their recorded user-local postchecks, not an
independent full-log byte hash or reviewer execution of the actual trained checkpoints.

## Execution validity

24 own tests PASS in18.959s;3169 focused tests PASS in180.676s.
346 source pins/550 protected inputs.20 models x400 updates=8000 training steps/256000 presentations.
Ten initial backbone references add30 forwards/1920 rows. Grand total8330 forwards/273280 rows.
All initial and checkpoint/prediction replays,head/whole-model weight updates,reference identity,
protected inputs,tracked tree and execution HEAD checks PASS;run_execution_valid=True.
Scientific status FAIL. All four family/arm aggregate gates are False.

## Deciding metrics

All40 model/language cells pass the original TRAIN criteria. One Full/token_read TRAIN EN cell
(seed250001) scores31/32, the others32/32; do not describe every TRAIN cell as100%.
Reader joint TRAIN/HOLDOUT outcomes:BOTH_PASS12,RECOMBINATION_MISS8.
EOS adapter outcomes:RECOMBINATION_MISS20.

HOLDOUT exact counts, each language out of16:

| Seed | Full reader EN/JA | GRU reader EN/JA | Full EOS EN/JA | GRU EOS EN/JA |
|---:|---:|---:|---:|---:|
|250001|3/8|16/16|4/6|7/9|
|250002|6/8|16/16|4/3|5/5|
|250003|16/16|16/16|9/9|12/14|
|250004|2/2|5/6|4/4|13/12|
|250005|16/16|16/16|2/4|11/11|

The slash in each table entry separates EN and JA counts, not a fraction.
Whole-seed both-language passes:Full reader2/5;GRU reader4/5;both EOS families0/5.
Pooled descriptive reader answers:Full93/160,GRU139/160;EOS49/160 and99/160.
Reader-minus-EOS comparisons:15 improving language/family cells,0 ties,5 worsening cells.
These cells share five paired initialization blocks and are not20 independent replicates.

## Interpretation and non-claims

The reading benefit is not limited to the original C248 seeds, but robustness across initializations
is not established. Successful reader cells reach perfect normal HOLDOUT and all paired/mask gates;
other seeds remain poor. The added reader is not uniformly better than its equal-parameter control.

GRU reader passes more seeds than Full reader in this batch. This motivates a matched Full-model
experiment, not a claim that the FOLD core is harmful or universally inferior. Backbone/head seeds
are linked, optimization trajectories differ, and the repeated small internal fixture is not a
fresh external benchmark. Do not infer a unique mechanism or a population success probability.

## Accepted artifacts

- initial-references.json:bef206a363baa98e58a6e16d1cb98474e7ff30986a478fca18007333234042a0 (6665 bytes)
- measurements.json:ece4a95c50359349bcd7a60ad7059a8613e7d1db1cbe64ad4449340c3a396e0f (63840 bytes)
- replication-plan.json:4f2bffab4fff98193a2756fe65d0403d955711f23b18e548698f45d7f93c9cee (3260 bytes)
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346 (15904 bytes)
- trained-models.pt:a37074f9ab1696622b3de4e16aeb69166659f7e27734bb770b814a5466622f31 (2146589 bytes)
- validation-summary.json:78acad4d8776fc5caf2dcc379ace4bd2dfcf748a84ae18d214949cae014842bb (4449 bytes)

## Next scientific question, not registration

For Full only, does reading keys/values from the causal encoder before the core, while keeping
the query and ordinary residual backbone path after the core, improve the fixed-seed result?

C250 Full uses final core token states as the reader memory and post-core EOS as its query.
The candidate uses masked local-encoder token states as memory, but the same post-core EOS as query.
The core still runs unchanged and is trained jointly. No fact parser,answer-location oracle,new
weights,extra loss,larger hidden width or additional updates are introduced.

Use all five C250 seeds, including both successful seeds, fresh initial backbones and the identical
head initialization. Reuse the immutable C250 Full/token_read final records as the post-core
comparator rather than rerunning accepted models. Candidate work is five fresh models. State-source
selection changes the computation and gradient paths; a gain would not uniquely prove information
loss in the core. This is an adaptive matched comparison, not new independent seed validation.
Separate C251 preregistration,committed-byte authoring review and activation are required.
