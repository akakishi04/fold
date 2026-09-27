# V5-B paired-query discrimination loss v0.1 — C268

C267 mixed-name training passed only1/5 states. Shared-suffix collapse decreased from163/240 to76/240
held-out query pairs,but answer accuracy was still257/480. Doubled-name accuracy decreased. Reducing
one symptom did not create reliable binding. Do not repeat that completed run or call the data policy
a solved recipe. C268 tests a different training objective,not another frozen diagnostic.

For the same facts,ask both queries in a batch. Example:aa=0;ba=1;aa= targets0 and aa=0;ba=1;ba=
targets1. Both CE-only and candidate models receive the same paired48-row batches,all three naming
profiles,the same initial weights and800 updates. Neither receives correct targets as input.
The only difference within a fresh pair is an auxiliary loss term in the candidate.

Ordinary cross-entropy asks each answer to be correct. The additional term encourages the relative
preference for the two target values to change in the correct direction between the two questions.
It uses d=(z0[t0]-z0[t1])-(z1[t0]-z1[t1]),then adds0.1*mean(max(0,2-d)) to ordinary CE.
The two outputs already exist from the normal batch,so no extra model forward is required.
Margin2 and weight0.1 are preregistered choices,not evidence-based optima. No tuning after results.

A low auxiliary loss is not proof of correct answers:both questions can still choose the same
value even when their relative preference differs enough. Keep CE and all the original answer,
paired-query,masking and two-order gates. Tests include this misleading-low-penalty case explicitly.
A decrease in collapse without improved correctness is also insufficient.

Five fresh seeds268001..268005 produce ten unchanged14256-parameter Full aligned readers.
Both arms use C267's exact192 TRAIN/96 HOLDOUT rows,with the same four held value pairs excluded
from every training profile. Shuffle96 same-facts query pairs per epoch and use24 pairs per batch.
200 complete epochs give each base row200 exposures. All3 profiles cycle268/268/264 updates.
The paired sampler is new relative to C267 but shared by both C268 arms;do not attribute a historical
C267-to-C268 difference solely to the loss or claim pairing itself was isolated.

Primary PASS requires all five candidate models to meet the existing criteria on both splits and
all profiles. HOLDOUT cells have8 questions,so the90% threshold means8/8. Control outcomes and30
paired held-out contrasts are reported separately. Names are trained in both arms;success would
mean held-value-pair performance,not arbitrary or unseen names. No default optimizer or architecture
change follows automatically. This is still a small authored symbolic family,not general language.

Formal workload:8000 updates,384000 training rows,8540 model forwards including final scoring and
strict checkpoint replay,435840 total rows,34160 core calls. Persist final weights and logits;
recompute metrics from saved tensors without further model calls. Own24 and full3597 regression
must pass before formal training. Authoring Tiny/parent-excerpt tests do not replace the Full run.

The earlier duplicate command was issued by the assistant after C267 had already published its
results. Keep the published-result notice and genuine stale-HEAD safety stop. Use the newly activated
C268 HEAD only;do not rerun C267. Parser and full source checks remain mandatory on Windows.
Gate F NOT PASSED. Valid misses are not rescued by modifying the budget,loss or seed set. Judge C268
before C269;no paid API,external corpus,production adoption,cleanup or CI changes.
