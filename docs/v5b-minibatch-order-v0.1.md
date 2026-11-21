# V5-B paired minibatch chronology v0.1 — C262

## Why this comparison

C261 reproduced the same successful andunsuccessful state membership on repeated-value tasks as
C260 had on distinct values. The successful states can transfer across that value restriction;
we still have not isolated what makes a training run reach a successful state.
Previous seeds controlled both initial parameters andthe minibatch generator. Calling all observed
seed variability an initial-weight effect was too specific. C262 keeps the starting model identical
within each pair andchanges only the chronological order of the same training minibatches.

Question:does this order change alter held-assignment scores oranswers at the same800-update budget?
This is not another architecture variant,more training for a failed state,orchoosing only good seeds.

## The two schedules

Both branches use actual C252 Full aligned readers,14256 parameters,andthe C259 six-fact-order
training task. Five fresh seeds262001..262005 each initialize one template,deep-copied into both arms.
Same initial weights,same optimizer,learning rate,precision,task,split andtotal training budget.

Take each epoch's144 logical TRAIN rows andsplit its seeded permutation into three48-row batches:
A,B,C. One arm updates on A then B then C;the other updates on C then B then A. Each batch contains
exactly the same prompt bytes,targets andwithin-batch row order in either arm. This changes the
order in which the optimizer encounters examples,not the order of facts inside an example.

The final800-update budget ends with only two batches from its last epoch. Use A,B versus B,A,
not A,B versus C,B. Otherwise the experiment would change which examples were taught in the tail.
No extra update is added. Exact432-prompt exposure counts are identical across each pair;the
chronological index fingerprints must differ. Every complete epoch preserves its batch multiset.
All six fact-order presentations remain taught in both arms,with267/267/266 pair-update counts.

The models receive different batches at a particular step by design. Their gradients andoptimizer
states may then diverge;those are effects of the tested chronological intervention. There is no
requirement for their final weights oranswers to be identical.

## Gate and useful evidence

Use the original distinct-value assignment partition andthe unchanged C260 per-language,per-order,
mask-drop,query-triplet andall-six-order criteria. This isolates training chronology on the same
reference task;it does not amend C261 oruse its repeated cases as new training examples.

The primary robustness gate requires both schedules to pass all five initializations. Report each
schedule separately. A complete valid miss is accepted negative even if one schedule improves.
Also compare reverse-minus-forward HOLDOUT accuracy,all-six consistency andindividual answers.
Count correct-to-wrong,wrong-to-correct anddifferent wrong answers separately. A tied score can hide
changed answers. A different output logit alone is not a correctness change.

A paired difference can demonstrate sensitivity to this specified order change with initialization
andexample exposures held fixed. It does not identify the cause of every old failure,the best
universal curriculum,oran internal optimizer mechanism. Identical outcomes do not establish that
all data orders are irrelevant. No statistical significance orpopulation guarantee is claimed.

## Execution and preservation

Ten models each train800 updates:8000 updates,384000 training rows. Final scoring andstrict weight
reload/replay bring the total to8240 wrapper forwards and435840 row presentations. Both arms retain
the Full core:32960 core calls total. One ten-state bundle is written/loaded;ten states strictly loaded.
Parent validation uses accepted hashes;old learned weights are not used for initialization.

Save final weights,raw final logits,schedule/exposure metadata,andper-cell/paired results in ignored
runs/. Persisted postcheck regenerates schedules andscores from stored tensors without another
model forward. Keep all accepted source/tests/logs unchanged. Protect418 pins and697 inputs.
Own24 andfocused3453 must pass before training;parse dispatcher,launcher andrunner first.

All evaluated fact orders are training-visible andthe authored task family has been inspected.
No general-language capability,independent benchmark,architecture winner,production readiness or
Gate F passage follows automatically. C261 remains negative. Judge C262 before registering C263.
