# V5-B learned residual gain — C301

C300 showed one extra quad pass when only the reader term was kept,but a seen-task regression
and severe additional errors in another model. Neither unconditional ablation is adopted.
C301 tests whether training can adjust the contribution without selecting a mode from evaluation.

The original output normalizes r+a. A single global scalar changes this to alpha*r+a,where
alpha=2*sigmoid(g),g starts0,and the initial function is exactly unchanged. Ordinary TRAIN CE
learns g together with the original weights. The candidate adds1 parameter,not a new input-dependent
router. All computations remain;the gain can attenuate or amplify but cannot reverse sign.

Matching initial outputs/common gradients prevents an accidental starting-function change from
being mistaken for a learned benefit. Frozen evaluation and strict reload include the learned
gain. First-gradient equality is checked before global clipping;the scalar's gradient can affect
that clipping later. This is an architectural/learning-policy comparison,not isolated attribution.
Fresh paired seeds,concurrent fixed control and unchanged all-five quad gate are mandatory.
A TRAIN-learned global coefficient might not resolve local failures or improve held-out transfer.
No learned value is chosen post hoc,no per-query best branch is selected,and no speed claim follows.
