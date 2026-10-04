# V5-B residual-gradient routing — C303

C302's frozen coefficient exchange did not improve quad pass counts or repair301003's lost
quad HOLDOUT answer. The final coefficient alone is not a sufficient explanation. This does
not prove gradient conflict; C303 is a controlled test of a different learning policy.

Keep r+a numerically unchanged. Compare normal training,freezing core weights only,and freezing
core while blocking the residual branch's backward signal at the sum. The intermediate control
matters:otherwise stopping the residual would confound the loss of core learning with the changed
error signal to shared local features. Even with it,global clipping and optimization can differ.

All15 models start fresh in five matched triples. Stop-gradient does not drop the residual at
inference or prevent its activations from changing as shared inputs learn. Stored parameter count
is equal,but trainable/gradient-receiving capacity and backward compute are not. Measure them rather
than implying a free stability gain. No success guarantee,causal mechanism proof,core-necessity
claim,per-question switch or best-seed deployment is authorized. Original all-five quad gate remains.
