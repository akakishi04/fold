# C338 acceptance and C339 direction

Date: 2026-10-26 Japan time.
C338 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C339 NOT REGISTERED.
No automatic retry, production adoption or alteration of earlier verdicts.

## Identity and execution validity

Execution f81a49e383e78ff503a4e4c6fe1156e7a8b75849.
Publication 579edc8f611cfc0a513ce52661582de70f8a8b50; its sole parent equals execution.
Metadata docs/experiment-run-logs/c338/latest.json and corresponding latest.log.
Publisher SHA256 9fdef99dd0eadce42ef5e3cd3feee8c1442a889a0e811ca80248e7e35ed60684,
244109 original Windows bytes; Git log blob 6b1d21acf47fb75808e014010be4971e9c3754c0.
Native locks/preflight passed; 6170 tests/228 modules, failures/errors/skips 0,
1916.467 seconds including process orchestration. Ordered test-ID SHA:
6f9f4fb4184d9ac262bf88eb7ec49e6ee0cd5099754fbb09545461dbc147d89b.
Ten models/24000 updates/27420 forwards completed; saved reconstruction passed;
all 5296 final uncached rereads and fresh verifier 889 sources/5296 inputs passed.
Science and verifier exited 0; run_execution_valid=true. scientific_status=FAIL,
candidate_gate=false, eligible_seed_count=0. This is valid science, not an invalid run.

Folder runs/c338-support-training-5d84afb5a34c4dc0a291ca0f35b24829/.
Primary science/summary.json SHA:
67e369808641a781dd144084a4e1a77d8347a07675740b8c3c694eaedbdf3137.
Envelope SHA:
11977e359dbb65236803fb7eaa1d085728a72d27a582dcc2d76d01906e3329e5.
Scientific manifest d2c6bcbadfa3f04c35cad137fece59c9499f8b5de37589425479b05376b9fe73.

## Deciding HOLDOUT measurements

All five paired seeds are retained. Each domain denominator is 1440 answers/720 pairs.
Numbers are native -> support_loss:
- original2/3/4 and interior4: each 1440->1440 correct,720->720 both-query-correct,
  outside-pair errors0->0. All local gates passed in these four domains, both arms.
- original5:1426->1423 correct;706->705 pairs;outside errors2->7.
- original6:1389->1375 correct;673->666 pairs;outside errors27->49.
- all six domains:8575->8558 correct/8640;4259->4251 pairs/4320;
  outside errors29->56; wrong-observed errors36->26. No outside_catalog winner in
  the sixty printed HOLDOUT state/domain support counts; outside errors there are absent_digit.
Full gate passed by native338002 only (1/5); candidate full gate0/5.
Original6 seedwise answer gains -1,-7,+18,-21,-3; pair gains -1,-7,+14,-14,+1.
Original6 rescues38/regressions52; original5 rescues11/regressions14.
Aggregate improvement conditions and all-candidate gate conditions are not met.
Do not pick seed338003 or change the coefficient after inspecting these results.

## Interpretation and limits

Fixed additional support-loss coefficient1 did not improve this registered cohort.
It preserved short-name/interior accuracy but increased long-name outside-value errors.
This does not prove that every support objective or coefficient fails, nor identify
an internal cause. C338 uses fresh initializations/order seeds, so its stronger
controls than C335 do not establish a causal cross-experiment improvement.
Unchanged update counts do not imply equal objective scale or clipping behavior.
Current public summaries do not locate failures by language/profile or reveal whether
support margins improved on TRAIN while worsening on longer HOLDOUT examples.

Remote review inspected metadata, commit lineage, preflight/registration, full test
receipt, all five paired comparisons, all ten state results and terminal verification.
Counts above were summed from those records. No independent whole-Windows-log hash,
local module-proof inspection, checkpoint replay or native training was performed here.
Attached historical C323/C324 files are not current C338 evidence.

## Next question, not yet execution permission

C339 will use all ten saved C338 states without fitting or model forward to locate
paired changes in supplied-value support and within-pair ranking across TRAIN/HOLDOUT,
original2..6/interior4, languages and profiles. Preserve raw256-class predictions,
exact ties and per-answer rescue/regression, reconcile all30 parent contrasts and
all60 support partitions. Diagnose training/evaluation transfer, not corrected accuracy.
Do not register until implementation, tests, preregistration and committed-byte review pass.
