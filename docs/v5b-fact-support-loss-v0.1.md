# V5-B fact-support component reweighting — C293

C292's failing answer_margin seed291003 outputs an absent known value in205 of212 HOLDOUT errors
across lengths2/3/4. This is not merely choosing the other given fact. It is still not evidence
for a uniquely identified hidden mechanism;the diagnostic cannot establish memorization.

C293 makes a bounded training intervention without a hard copy/pointer decoder or inference filter.
The old individual CE decomposes exactly into support mass and conditional choice within support:
-log P(y) = -log(P(y0)+P(y1)) -log(P(y)/(P(y0)+P(y1))).
The candidate increases the first component's weight from1 to1.25 and leaves the second at1.
A correct query must still win the conditional choice;support mass alone is insufficient.
No new labels or training examples are introduced:the original intact query pair supplies both
fact values. The model still sees only tokens and its original task ID and predicts all256 bytes.

Compare concurrent ordinary CE and1.25*CE on the same fresh seeds. The latter makes simple loss
scaling visible but cannot make optimizer trajectories or clipped gradients perfectly comparable.
This tests a complete weighting policy,not a mathematically isolated causal factor. A lower absent
output count is not enough to pass:the fixed full four-character gate and all old masks remain.
Retain trained-length performance and every output-role count so shifts to the wrong in-context
fact cannot masquerade as improvement. No automatic production adoption or Gate F promotion.
