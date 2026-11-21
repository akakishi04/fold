# V5-B paired name-coverage training v0.1 — C267

C266's saved-output diagnosis found same-answer collapse in2149/2880 shared-suffix query pairs,
compared with19/2880 doubled-name pairs. This describes behavior,not a proven last-character parser.
The promised single diagnostic is complete. The next question tests training coverage instead of
adding another frozen-name probe or modifying the architecture on an unproven causal story.

Question:does teaching examples that require distinguishing whole compound names improve held-out
value-pair answers,relative to equally long but non-colliding doubled names at the same budget?

Create five fresh pairs of the unchanged Full aligned-reader model,14256 parameters each.
Within each pair,the complete initial weights,base questions,targets and logical batch schedule
match. doubled_only sees uu/vv. mixed_names cycles uu/vv,uu/uv,uu/vu,including aa/ab and aa/ba.
Both receive800 updates of48 questions at AdamW learning rate0.005. The sole experimental contrast
is naming coverage under the specified cycle. No existing learned model is continued or selected.

Use an explicit NEW two-fact split. The four held value pairs are(0,2),(1,3),(2,0),(3,1),in every
language,entity subset,order and profile. Train on the other eight distinct pairs from0..3.
Each digit is balanced at both entity positions. TRAIN has192 logical rows,HOLDOUT96.
This small modular split is structured,not a random benchmark;its limitations must be reported.
It does not inherit the invalid assumption that C264's projections preserve old train/test labels.

Each epoch shuffles all192 TRAIN rows and processes four48-row batches. Both arms use the same
per-step base rows;the treatment changes only their visible names.200 complete epochs give every
base row200 presentations. Treatment profiles occupy67/67/66 epochs;no extra updates are added.
The number of doubled strings shown differs by design,but total logical-question exposure is equal.
All rendered HOLDOUT rows stay out of optimization,including mixed-profile versions.

All three profiles are evaluated for both TRAIN and HOLDOUT. Keep90% answer accuracy,80% paired-query
and two-order correctness,and35-point evidence/query masking drops. Small HOLDOUT cells contain
only8 answers,so90% means8/8. Each mixed_names seed must satisfy every criterion;all five are required.
Control results are reported separately. Correct-answer differences and same-answer collapse are
reported together for30 matched held-out profile/language comparisons. A drop in collapse alone
is not improved capability,and a primary PASS alone is not proof of treatment advantage.

Names are training-seen in the treatment. Success would mean transfer to held VALUE combinations
under covered compound names,not transfer to unseen names. No arbitrary-string comprehension,
causal parser mechanism,general language,independent benchmark or Gate F claim is authorized.
Fresh seeds do not erase prior inspection of the symbolic task family.

Total10 models,8000 updates,384000 training presentations. Final scoring and strict replay raise
this to8540 model forwards/435840 rows/34160 core calls. One final10-state bundle;10 strict loads.
Final logits use about53 MB raw payload plus weights and metadata. Historical tests,hashing and
parent JSON validation are extra computational work. Saved metric reconstruction makes no model
calls. Protect448 source pins/761 inputs;own24 and focused3573 precede formal training.

C266 remains diagnostic PASS and C265 remains negative whatever this comparison finds. Do not
retune the data,updates,learning rate or seeds after results. No default architecture/optimizer
change,paid API,external corpus,cleanup or CI action. Judge C267 before C268.
