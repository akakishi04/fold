# C263 acceptance and C264 two-fact deletion boundary

## Formal verdict

C263 ACCEPTED PASS (bounded distinct-assignment capability at the registered budget).
Both lower-rate chronologies pass all five seeds. Both standard-rate chronologies also pass5/5.
This satisfies the preregistered capability gate,NOT a claim that lowering learning rate helped.
C262 and all earlier accepted negatives remain negative. Gate E PASSED;Gate F NOT PASSED.
No optimizer default change,architecture selection,production adoption or general-language claim.

Scientific execution HEAD:abca8d7eb25146fca6f7404790071d1e6f0999d0.
Published log commit:1b47b5e3dc8ee3c6c2edd6972e7521b16e4f1b67.
Publisher log SHA256:d089e8f808170a58bfb292547387642a4d0d6312ec61764564462ba26cc2441b.
Log bytes:875870;lines4160.
Summary SHA256:1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21.
Summary:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.
The publication commit changes only c263/latest.json and latest.log and directly follows execution.
Acceptance is based on immutable published log ranges,metadata and recorded local postchecks.
The reviewer did not independently rerun learned models or rehash the complete published log.
Do not present a publisher-reported SHA256 as an independent full-byte reviewer rehash.

## Execution validity

Own24 PASS in12.872s;focused3477 PASS in292.013s.
424 source pins/710 protected inputs passed. Twenty models each completed800 updates:
16000 updates,768000 training rows,16480 model forwards,871680 row presentations,65920 core calls.
Four-way initial state/exposure matching,rate/order metadata,weight changes,strict final-checkpoint
fingerprint/logit/argmax replay,persisted metrics/contrasts and protected-input checks passed.
One20-state bundle write/load;20 strict state loads. Tracked tree clean;execution HEAD preserved.
run_execution_valid=True;scientific_status=PASS;candidate_gate=True;all_pairs_matched/all_replays=True.

## Deciding capability and comparative evidence

|Arm|Learning rate|Whole-seed passes|HOLDOUT normal correct|All-six groups correct|
|---|---:|---:|---:|---:|
|standard_forward|0.005|5/5|2160/2160|360/360|
|standard_reverse|0.005|5/5|2160/2160|360/360|
|lower_forward|0.001|5/5|2160/2160|360/360|
|lower_reverse|0.001|5/5|2160/2160|360/360|

Each seed/language cell has216 answers and36 all-six groups. All four arms and all five seeds are
retained. Across20 models,HOLDOUT normal answers8640/8640. The fixed per-order/mask/TRAIN criteria
also pass;these were not replaced by the pooled total.
All20 rate contrasts and20 order contrasts have zero accuracy delta,zero answer disagreements and
zero correctness flips. All10 disagreement interactions are zero;both rates have worst-chronology
HOLDOUT accuracy1.0 in every seed/language cell. No positive improvement in these final comparative
metrics is observed. Equal argmax/accuracy does NOT imply equal logits,NLL,weights or learning curves.
For example,the printed lower-rate learning losses differ from the standard-rate trajectory.

## Interpretation and limitations

All20 registered final states solve this finite held-assignment task and satisfy its fixed gate.
The data provide bounded positive capability evidence,not evidence of a learning-rate advantage.
The rate effect on final accuracy/disagreement is unresolved at this ceiling;do not adopt0.001 on
this result alone or claim that the previous chronology sensitivity has universally disappeared.
C262 used a different seed cohort and retains its valid evidence of chronology sensitivity.
Five fresh seeds and repeatedly inspected assignments do not establish initialization-population
robustness,a new independent benchmark,ordinary language,core superiority or Gate F passage.

## Accepted artifacts

-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;126501 bytes.
-evaluations.pt:1681c71811844655081ca5597b6dfbe1ab80fbdc5b5046b1f947b1bf51aefd89;106263991 bytes.
-measurements.json:9b8bab48074a91e1dd5f3c5d389598739b651bcadeed6ec49fbf7ec0c92631ee;118267 bytes.
-rate-plan.json:ca53314f0e2ccda5bc7950f031c443ad70bb4e6c6c7181b53f8e7c0768199305;2779 bytes.
-trained-models.pt:a63519b761bc876b8088fe14432018cd01024bfdecbcf1fca38a0515021dede9;2475525 bytes.
-validation-summary.json:e42f668ec6c2a01f573be92bbcd938f1d991e48cf02d242315d02d740d29066f;15183 bytes.

## Next question, not activation

Freeze all20 final states. Does deleting one unqueried fact preserve correct answers when only
two of the original three named entities remain? No new vocabulary,value,weight or training is
introduced. Retain all three possible entity subsets,both fact orders,both languages and all
ordered distinct value pairs from0..3. This changes visible fact count/effective length/positions;
it is not an isolated neuron intervention or a claim about arbitrary-length reasoning.

Generate288 unique reduced prompts. Deleting irrelevant facts from all original C263 rows produces
1728 provenance edges,six source presentations per reduced prompt. Deduplicate before scoring and
retain provenance;do not label reduced prompts TRAIN/HOLDOUT because projections can cross the
original assignment partition. Original data remain replay anchors,not additional science samples.
Require faithful raw-output replay before and after the new inputs and unchanged final states.
C264 needs separate preregistration,implementation and committed-byte review before activation.
C265 NOT REGISTERED.
