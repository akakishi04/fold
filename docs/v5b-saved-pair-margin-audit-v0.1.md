# V5-B saved margin/correctness audit — C290

C289 did not rescue reliable four-character transfer by stopping pair supervision after400 steps.
Both auxiliary schedules passed0/5 quad gates,versus3/5 with CE. Seen-length gates improved to4/5
in both auxiliary arms,but early withdrawal lost one always-on TRAIN direct pass. These observations
rule out adoption of this fixed schedule;they do not identify a uniquely harmful late-learning phase.

C290 tests the alignment of the existing auxiliary score with individual answer correctness using
only saved logits. A positive correct-versus-swapped assignment score need not mean either answer
beats all256 classes;one strong pair difference can mask a weak answer. This is a mathematical
limitation already known before seeing C289. The open empirical question is how often it occurs in
these actual outputs,and whether withdrawal changed the specific erroneous answers at all.

Retain all3arms/all5seeds/all3tasks/all value splits. Report the full two-way margin/correctness
cross-tab and exact paired argmax changes,not only examples favorable to a new hypothesis. All old
masked/full gates remain under the original parent verifier. No new coefficient or training sweep.
No claim that objective saturation,representation,overfit or optimization is proved causal.
A negative alignment result can motivate a later bounded intervention;an aligned result can instead
rule out that explanation. Neither outcome changes a prior scientific verdict or closes Gate F.
