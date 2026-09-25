# V5-B paired order-coverage training v0.1 — C259

## Motivation and question

C256's reader passed value-assignment recombination on two fact orders,while C257 passed unseen
orders on only2/5 saved candidate states. C258 decomposed the saved mistakes:query b is often weaker,
but a universal middle-value shortcut does not explain every seed/language. Stop decomposing those
same answers and test a controlled training-policy change instead of modifying the model blindly.

Question:at identical architecture,initialization,underlying question exposures and800-update budget,
can six-order training produce reliable all-order held-assignment performance versus two-order training?
This is a paired experiment with five fresh seeds259001..259005 and two identical aligned readers
per seed. It is not an EOS-control comparison,continued training of C256,or a failed-seed rescue.

## What changes

Both arms use actual C252.AlignedPrecoreReadout on the existing C231 Full byte backbone:
pre-core query and K/V,reader output added to post-core EOS. Both14256 parameters;no architecture edit.
One fresh complete initial wrapper is deep-copied into both arms. Same optimizer,precision,batches,
steps,targets,entity names and assignment partition. Only the presented fact order policy changes.

A logical batch indexes the144 original C256 TRAIN rows. Each row identifies assignment,language,
query and one of two order bits. At each epoch,shuffle those same144 indices with seed+256000+epoch
and split them into three48-row blocks. Paired arms use identical indices/targets in the same step.
The control always maps the bit into012 or210. The treatment cycles order pairs every epoch:
(012,210),then(021,102),then(120,201),and repeats. Do not reorder the prompt before the model sees it.
Every nine complete updates presents each base question in all6 orders exactly once in treatment.
The800-step budget includes a fixed incomplete tail;pair updates are267/267/266,not an extra epoch.

Example:a=0;b=1;c=2;b= and a=0;c=2;b=1;b= have the same target1. Their visible bytes differ in
fact order,not in the question or answer. No oracle metadata is passed through a second model input.
HOLDOUT assignments never enter optimization,including their extra-order versions.

## Measurement and gate

Retain the existing C256 balanced12/12 assignment split and English/Japanese symbolic spellings.
Score both assignment splits,all six orders,normal/evidence-blind/query-blind views,final weights only.
Original two-order criteria stay fixed. Each of four additional orders independently needs90%
accuracy,80% query-triplet correctness,and35-point evidence/query masking drops. All-six-order
consistency needs80%,and the original criteria still apply. Every treatment seed must pass both
languages and both assignment splits. Valid misses are accepted negatives,not execution faults.

Record controls separately and report ten treatment-minus-control HOLDOUT comparisons for all-order
accuracy and all-six consistency. Treatment PASS is not automatically a comparative advantage:
controls can also pass. Do not replace per-order gates with a pooled average or select the best seed.

## Cost and persistence

Ten models x800 updates x48 rows=384000 training presentations.
Per model final scoring12 forwards/2592 rows;strict-checkpoint replay repeats the same work.
Total8240 full-model forwards/435840 row presentations. One final ten-state bundle;ten strict loads.
Store final original/extra raw logits for all views in a separate evaluation archive. Postcheck
recomputes metrics from these saved tensors without another model evaluation or weight-bundle load.
Source/artifact checks protect400 source pins and659 inputs;all accepted files remain unchanged.
Own24 and focused3381 must pass before formal training. Windows ParseFile chain remains mandatory.

## Interpretation boundary

The treatment has been trained on all six fact orders. Its success would demonstrate held-assignment
recombination under covered orders,not transfer to an unseen order. Fresh seeds do not erase prior
inspection of this authored data family. Testing this order policy does not prove a particular
binding algorithm,core superiority,general language skill,production readiness or Gate F.
A failure would not prove architectural impossibility;it would mean this fixed policy/budget missed.
C256/C257/C258 verdicts remain. Do not add steps,change thresholds or modify the trained states after
reading results. Any later intervention needs separate judgment and preregistration. C260 unregistered.
