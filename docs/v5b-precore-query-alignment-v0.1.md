# V5-B pre-core query alignment v0.1 — C252

## Question

Does changing only the Full reader query source from post-core EOS to pre-core local-encoder EOS
improve the same five-seed result while keeping pre-core K/V memory and the post-core residual base?

C251 used pre-core K/V memory with a post-core query and passed2/5 whole seeds. C252 keeps the
same five seeds,model size,data,training budget and K/V memory. Only the query representation changes.

## Candidate

C251:
- K/V memory = masked local causal encoder states.
- query = post-core EOS.
- residual base = post-core EOS.

C252:
- K/V memory = the same masked local causal encoder states.
- query = pre-core local-encoder EOS.
- residual base = the same post-core EOS.

The FOLD core still executes both routes for every internal step and remains trainable.
The candidate reuses the C248 reader weights Wq/Wk/Wo with the same seed+248000 initialization.
No parameter is added:Full remains14256 parameters.

The returned readout is:
q=Wq*h_pre; k_i=Wk*H_pre_i; alpha=softmax(k_i dot q /4);
z=h_post+Wo*sum(alpha_i H_pre_i),with PAD excluded.

## Matched experiment

Use seeds250001..250005. Train five fresh Full candidates.
Reuse accepted C251 endpoints only as immutable comparators;do not retrain them.
Require exact C251 bare-backbone and whole-wrapper initial fingerprints before training.
No accepted trained checkpoint initializes C252.

Keep the exact TRAIN64/HOLDOUT32 rows and original three scoring views.
Use unchanged C248 training:400 updates,batch32,normal old32/added32 alternating,
AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0,clip1,CPU float64,threads2,
deterministic algorithms. No early stopping,seed replacement or HOLDOUT-driven tuning.

## Gate

Primary PASS requires all five seeds to pass both languages on TRAIN and HOLDOUT:
accuracy>=0.90;fact/query/order pair>=0.80;evidence/query drop>=0.35.
Report all10 language cells,whole-seed pass count and deltas versus C251.

A valid miss is ACCEPTED VALID NEGATIVE. A PASS is limited to this reused internal binding task.
It does not prove a unique mechanism,external generalization,production readiness or Gate F.

## Workload

5x400=2000 training updates/64000 presentations.
Total2075 full-model forwards/67840 row presentations including reload checks.
One five-state checkpoint bundle;no parent-model inference and no scientific network calls.

Require exact initial identities,weight changes,batch schedule,prediction replay and <=1e-9 replay
error. Postcheck verifies saved artifacts and comparator identity without new model forwards.
Judge C252 before C253.
