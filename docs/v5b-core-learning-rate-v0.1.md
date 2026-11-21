# V5-B core learning-rate attenuation — C308

C307's fresh replication did not repeat C306's five-character pass-count advantage of freezing.
It also retained a substantial TRAIN failure with both policies. Freezing is not adopted as a
universal stabilizer. Nor does the result prove the core should always be trained at the same rate.

Test one prospective intermediate policy:core AdamW learning rate0.0005,noncore0.005,against
full learning0.005 everywhere and an unchanged frozen-core control. Keep broad2/3/4 learning and
unseen5 evaluation. No additional length,representation,loss or readout modification is bundled.
The0.1ratio is a coarse precommitted comparison,not an optimum inferred from the failed items.

All initial states match within each new seed. Gradient paths and initial forward values are the
same for full and slow;only optimizer step coefficients differ. Global clipping is NOT performed
after manually shrinking core gradients. The frozen control excludes core parameters altogether.
With training,the weights/gradients/moments diverge,so nominal LR ratios are not final update ratios.
A gain could support this bounded policy,not a unique instability mechanism or architecture claim.
Keep all controls and failures and do not search additional ratios in the same experiment.
