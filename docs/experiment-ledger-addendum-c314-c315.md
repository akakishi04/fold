# C314 formal acceptance — diagnostic integrity PASS

C314 ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY). C313/C312 remain valid negatives;
C308 remains a bounded capability PASS and Gate F NOT PASSED. C315 NOT REGISTERED here.

## Evidence identity

Scientific execution:41d132a50b246de5357a3878606a1ac7776c830d.
Published log:ec39b319d333527d4786ac6299ded6faa6a1601b.
Log SHA256:cc707b767464468c8cb7f3127be4bb084f151965fe9070388d2524bc28481785;852789 bytes.
Publication modifies only docs/experiment-run-logs/c314/latest.json and latest.log.
Summary:runs/c314-v5b-six-boundary-31c4ca923fa8459cbe9afde6fade9c83/summary.json.
Summary SHA256:daa6403d0eb00399cecb73e83693db41dbbb42151b979080d904428da5484e51.
Own24 and focused5053 PASS;source730/protected1369. All120 local and20 transition totals
reconstructed. persisted_six_boundary=PASS;run_execution_valid=True;tracked tree clean;
scientific HEAD preserved. No retraining,model forward,state loading or checkpoint writing.
No C314 retry is justified.

## Deciding evidence

8640 matched questions/17280 saved answers. Five correct8637;six correct8548.
Both correct8548;new six errors89;both wrong3;same wrong3;recovered0.
The three parent capability passes at six remain just three;this diagnostic does not promote them.

Representative,not exhaustive subgroup findings:
Random seed312001,shared_suffix,TRAIN/HOLDOUT pooled144 rows per language:
English new errors6 (4 TRAIN,2 HOLDOUT),Japanese19 (11 TRAIN,8 HOLDOUT).
Japanese shared-suffix HOLDOUT mean target-vs-best-wrong margin8.378211460508153 at five
versus3.554789852911447 at six;all48 margins decreased. These are logit gaps,not probabilities.
Random seed312002,shared_prefix:English3 TRAIN+2 HOLDOUT new errors,Japanese0 in that profile.
English six inputs use27 tokens,not close to the64-slot boundary. Thus an explanation limited
to Japanese prompts approaching the frame boundary cannot account for every observed error.
These representative findings are NOT an aggregate claim about all120 diagnostic groups.

Language,byte count,position and name structure remain confounded;the audit cannot identify
attention,context limits,memorization or optimization as the unique cause. All model errors,
original masks and fixed gates remain. No discarded seed,answer repair or threshold change.

## Next registration boundary

The user proposed training single-character names. Test adding length1 to the original
length2/3/4 mix at matched total optimization budget and unchanged core_slow policy.
Use fresh paired seeds;retain maximum trained length4 and held-out lengths5/6. Canonicalize
single-character profile degeneracy rather than counting three identical prompt families.
At equal total updates,per-length exposures differ;report that allocation tradeoff explicitly.
This hypothesis does not follow causally from C314 and is not promised to repair similar-name
confusion. C315 needs its own code,tests,preregistration and committed-byte review before use.
