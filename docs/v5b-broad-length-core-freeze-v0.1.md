# V5-B broad-length training with a fixed recurrent core — C306

C305 showed that most candidate five-HOLDOUT errors already existed at four characters:418/430.
This does not prove a core cause or make new-length errors irrelevant. It supports concentrating
on the learning policy at the current2/3/4 setting before adding still longer training lengths.

C303's frozen-core control is a concrete prior lead,not an adopted solution. Retest it against
ordinary training on new paired seeds,common64slots,1200updates and identical2/3/4 examples.
Keep the full inference equation and backward propagation to the encoder;freeze only core weights.
The core is random at initialization,not a pretrained or handpicked successful core.

Both models have14256 saved parameters,but only10928 update in the candidate. Differences in
trainable dimension,clipping and backward work remain part of the intervention. Results cannot
establish that the core is unnecessary or universally harmful to train. All original length5
local and masked gates remain. Failure at trained lengths and HOLDOUT must be reported separately.
