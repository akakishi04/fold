# V5-B fixed-budget late learning-rate decay — C286

C285 shows37 of43 mixed four-character failing accuracy cells also failed the matched three-character
cells.42 of43 quad accuracy failures belong to284002;the remaining284001 failure is one wrong answer.
This narrows the observable bottleneck but does not prove late-step optimizer instability:the
three-character task includes HOLDOUT values,and co-failure is not necessarily training underfit.

C286 keeps mixed2/3 data,model and800-update budget fixed. It changes only updates401..800 from
constant LR.005 to a preregistered cosine tail ending at.0005. Both arms have identical first400
updates,which are verified by actual state fingerprints and loss traces. There is no warmup,
extra data,model path,auxiliary objective or selection of the formerly problematic seed.

The hypothesis is that smaller late updates may improve final binding/generalization consistency
without losing useful early learning. It is deliberately falsifiable:slowing late adaptation could
also hurt. The comparison tests a learning policy,not a diagnosed root cause. A prior lower constant
LR comparison does not settle this time-dependent schedule question.

Fresh5-seed pairs keep the comparison separate from the particular C284 failure. Four-character
all-five gate remains primary;seen-length and all-task scores remain descriptive. A candidate PASS
alone is not superiority, and a relative benefit is not arbitrary-length competence or Gate F.
Keep all outcomes,including regressions. No gate,LR endpoint,budget or seed is changed after results.

C285 and every older accepted source/test are immutable. The child reuses only schema-compatible
C284 evaluation/replay helpers,C282 TRAIN tables and C283 four-character scoring. The child owns
new schedule/LR/identity/prefix validation. Real parent artifacts and full regression remain
user-local runtime gates even when the reviewer fixture tests pass.
