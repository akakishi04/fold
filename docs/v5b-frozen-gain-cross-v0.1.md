# V5-B frozen coefficient versus learned-weight outcome — C302

C301's learned scalar ended below1 in all five runs. Seen-length task passes improved2->3,but
quad passes fell2->1. This combines a different final inference coefficient with different jointly
learned common weights. The final scalar alone cannot explain that comparison.

Evaluate every paired saved weight set at unit gain and its own seed's TRAIN-learned gain.
Within a weight set,the switch tests the immediate inference coefficient. Across weight sets
at the same gain,it describes the effect of the whole earlier learning policy on the common
weights. Neither is a decomposition into unique training causes or proof of architectural necessity.

Do not retrain,mutate stored weights,choose a better donor or search extra gains. Reproduce original
C301 outputs before and after each switch. Apply each condition to all original questions and masks;
report rescues and regressions,not per-question best-of outputs. Restored passes are controls,not
additional independent trials. An off-diagonal is not automatically deployable. Gate F stays unmet.
