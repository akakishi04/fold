# V5-B frozen two-fact deletion v0.1 — C264

C263 passed its registered capability gate,but both learning rates and both minibatch orders had
perfect final held-assignment answers. That is not evidence that the smaller learning rate helped.
Do not change optimizer defaults or claim universal training robustness from this ceiling result.
The next test asks what the successful frozen models can do beyond the exact three-fact format.

Question:does removing an unqueried fact preserve the correct answer when only two facts remain?
Example:a=0;b=1;c=2;b= and a=0;b=1;b= both have target1. No new information is needed and the answer
is still fully determined. Yet the input is shorter and the model must not assume three facts.

Keep all20 C263 final states,all four rate/order arms and all five seeds. No further training,
model selection or new vocabulary. Use every two-entity subset of the existing three names,
every distinct value pair0..3,both visible fact orders,both languages and both queries:288 prompts.
Each reduced prompt has six full three-fact parents. Store all1728 source edges but score288 unique
prompts only. Reduced prompts can combine provenance from the old TRAIN and HOLDOUT partitions;
do not pretend their projected copies form disjoint train/test sets. No optimization occurs.

Before any reduced input,strictly replay all C263 saved final logits with the actual unchanged
model. After reduced-input evaluation,replay the original inputs again and verify weights did not
change. The model receives visible bytes only,not deletion indices,targets or source metadata.

Score each entity subset/language/order separately. Require90% answer accuracy,80% paired-query
correctness,and35-point drops when evidence or query is hidden. Both values differ,so the latter
query check is mathematically appropriate. Require80% of assignment/query groups correct in both
fact orders. All20 states must pass;report four arm counts,not just the best arm or pooled average.
A completed valid miss does not revoke C263 and does not authorize training on these new questions.

Twenty frozen models require600 wrapper forwards/120960 row presentations including original
anchor and restoration. Core calls2400;new training0,new learned checkpoints0. One accepted
checkpoint-bundle load and20 strict loads. Raw output tensors about248 MB plus metadata;parent
reference replays and historical tests are separate work. Saved postcheck reconstructs all scores
and provenance without model calls. Protect430 source pins/723 inputs;own24 and focused3501 precede
formal evaluation. Keep checkpoints/generated files ignored and publish only execution text logs.

A PASS establishes transfer from three to two facts in this finite symbolic family. It does not
establish arbitrary-length reasoning,ordinary language,an independent benchmark,a better learning
rate or a production-ready FOLD model. Fact count,length and positions change together,so the test
does not isolate one internal mechanism. Keep Gate F NOT PASSED and all earlier evidence intact.
No automatic architecture/optimizer adoption,external corpus,paid API or cleanup. Judge C264 before C265.
