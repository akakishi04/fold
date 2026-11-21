# V5-B frozen-core policy: replicate before retuning — C307

C306 fixed-core training rescued two five-character seeds but lost another. It reached4/5,not
its registered5/5,although the pooled normal prediction total was4319/4320. The improvement in
seen lengths is promising but does not justify engineering a remedy for the remaining one item.

Repeat both full training and fixed-core training with five new paired initialization/order
seeds. Retain2/3/4 training and unseen5,data,64slots,1200steps,optimizer,schedule algorithm,offsets
and thresholds. Only the seed pairs differ. No learned parent weights or selected donor is used.
This removes the dependence of the comparison on the one observed five-seed cohort,without
introducing another training-policy change whose effect would be harder to distinguish.

Report the new cohort separately and keep C306 negative. Fresh random seeds are not fresh tasks,
a larger language capability test or a blinded independent investigator. New all-five success
would meet this preregistered bounded gate,not automatically establish superiority or complete
Gate F. Keep candidate failures and successful controls as well as rescued models.
