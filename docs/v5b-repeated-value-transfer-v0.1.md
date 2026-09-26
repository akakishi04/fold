# V5-B frozen repeated-value transfer v0.1 — C261

## Why this question

C260 found Full4/5 and core-free3/5 passes,with a reversal of the comparison for one seed.
Removing the core is not a general solution to the current initialization variability. Rather than
choosing a winner or adding seeds until a gate passes,retain both paths and test an unexamined
restriction:every prior assignment had three distinct values. Ordinary binding must also handle
several entities sharing the same value.

Question:without additional training,can all ten C260 final models answer the repeated-value cases?
Example:a=0;b=0;c=2;c= should return2;the same facts followed by a= should return0.
Always returning the frequent value0 is not sufficient.

## Frozen evidence, changed input distribution

Use all five original seeds260001..260005,both Full and core-free arms,strictly loaded final weights.
Do not filter previously failing models or replace their seeds. No training or architecture change.
Keep entity names,values0..3,all six fact orders,delimiters,query-at-end and48-slot byte encoding.
New assignments are all40 nondistinct triples:36 with one equal pair and4 with all values equal.
For each,use two symbolic identifier languages,six orders andthree queries:1440 new questions.
The old distinct assignments remain separate replay anchors;new questions are not TRAIN data.

The replay sequence is old outputs -> new repeated-value outputs -> old outputs again. Match the
accepted C260 raw logits and argmax before presenting new questions;verify restoration and unchanged
weights afterward. A previously wrong answer faithfully reproduced is valid replay,not a fresh
capability PASS. The new task does not retrospectively alter C260's negative verdict.

## Do not reuse an invalid metric assumption

A pair-equal assignment has one singleton target andtwo repeated targets. Report those question
types separately andrequire90% accuracy for each,not just a high pooled average. Require complete
three-query correctness80% and evidence-mask drop35 points. Each order and language is separate.
Also require80% of assignment/query groups to be correct in all6 presentations.

All-equal assignments have no query-dependent answer. Their query-blind score may correctly be100%,
so they cannot demonstrate query understanding. Score them separately for evidence reading,requiring
90% accuracy,35-point evidence-mask drop,and80% six-order consistency.

Query-mask drops are reported,not gated. A perfect model whose query-blind fallback selects the
repeated value has only a33.33-point drop on pair-equal questions and0 on all-equal questions.
The old35-point query-drop threshold would reject correct behavior here. The replacement is explicit
singleton/repeated-target accuracy and full query-triplet correctness,not post-result gate relaxation.
Singleton accuracy for the all-equal stratum is null,not a zero or an artificial success.

C261's new joint capability gate requires BOTH arms to pass all five seeds. Each arm is also reported
independently. There is no hidden switch to the better-looking arm after results and no selection of
previously successful states. A valid miss remains useful evidence about this input restriction.

## Runtime, persistence and limits

Per model:12 original forwards/2592 rows,30 new forwards/4320 rows,12 restored forwards/2592 rows.
Total540 wrapper forwards/95040 rows,1080 Full core calls andzero core calls on core-free models.
No optimizer steps,new learned checkpoints or external calls. One accepted model-bundle load andten
strict state loads. Stored anchor/new/restored logits have about195 MB raw payload plus metadata;
this is not a disk-space optimization. Postcheck reconstructs all scores from saved tensors without
new inference. Source hashes,412 pins/685 protected inputs andaccepted artifacts must remain intact.

Own24 andfocused3429 are required before formal evaluation. Authoring tests use explicit synthetic
oracle fixtures and do not substitute for real checkpoint evaluation. Parse dispatcher,launcher
andrunner before use. Preserve all accepted source/tests/logs. No cleanup or CI changes.

A PASS would establish transfer to these repeated-value cases in a finite authored symbolic family.
It would not establish ordinary English/Japanese proficiency,arbitrary numeric binding,an independent
benchmark result,core superiority,production adoption or Gate F. No architecture decision follows
automatically. Judge C261 before C262.
