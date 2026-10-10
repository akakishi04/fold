# V5-B trained last-only readout — C319

C318 shows that removing either branch after joint training reduces six-character reliability.
That is not yet a test of models trained to use a single branch. Train native mean-plus-last
and last-only from matched fresh initializations instead of repeatedly editing frozen outputs.

Both arms use the unchanged two_to_four1200update policy,coreLR.0005/noncore.005 and original
64-slot14256-parameter model. Candidate duplicates the last-byte query in both native attention
calls;the total memory coefficient stays1. Crucially,the selected representation stays attached
to autograd,and the same policy is used during training,evaluation and strict replay.

No one-character mixture change,extra training,new data or checkpoint selection is introduced.
Neither outcome identifies universal architectural necessity. Candidate5/5 at six is a bounded
capability gate,not superiority or Gate F. A valid failure is preserved without seed replacement.
