# C281 preregistration — saved support-intervention transitions

Experiment:C281-v5b-saved-support-transition-audit.
Stage:V5-B-SAVED-SUPPORT-TRANSITION-AUDIT.
Acceptance base:3b06f8d34f2b4ce0bc7a234c3e29c2b5234df95d.
C280 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C282 NOT REGISTERED.

## One scientific question

For the accepted C280 paired outputs, which fixed-criterion failures does evidence-only support
rescue or introduce, especially shared_suffix2, and how much of the residual is shared seed280004
failure rather than a candidate-specific regression?

## Immutable parent evidence

Scientific execution:2c2eb8a86a03910ba9c63ff277c137d1e842a32f.
Published log:ae0a53cd8e0beb65ac4e1909edadecd51d833fdf.
C280 summary:runs/c280-v5b-evidence-only-dual-bb662d609be24ad9a1fd20d4aef54174/summary.json.
C280 summary SHA256:00410f3d879cb9571186e2ebf08a1ca9df0b31b64a639adae53f503c068bc7db.
Direct C280 source blob:b0fbd492675ff8d147af13573b26c09c3d4afcab.

Ordered summary SHA256 pins (C280,C279,C278,C277,C276,C275,C274):
- 00410f3d879cb9571186e2ebf08a1ca9df0b31b64a639adae53f503c068bc7db
- a0019e06e4f4b330675daa2235cb4d0cf1952930336d2f0038f17d6ebd11b5bb
- 557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b
- ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13
- 6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f
- 1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb
- 0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0

Seven C280 artifact SHA256/size pins are fixed in PARENT_ARTIFACTS, embedded in the sealed
manifest, and recorded in docs/experiment-ledger-addendum-c280-c281.md. Require exact filenames,
hashes and byte sizes, plus parent candidate_gate=False, all_replays=True, all_pairs_matched=True,
both arms whole0/5,two_char4/5,triple0/5, and the exact per-seed two-character failure at280004.

## Saved-output contract and primary analysis

Load C280.verify_artifacts with neural Module calls, model-state loads and checkpoint writes blocked.
It reconstructs raw evaluation logits through unchanged C267/C270 scorers and validates parent
artifacts before the child analyzes measurements. No substitute parent schema or guessed summary keys.

All 10 models remain in scope: seeds280001..280005 x all_token_dual/evidence_only_dual.
Require the complete unique grid of2160 fixed records:72 answer cells+36 two-order cells per task,
two tasks per model. Join1080 control/candidate records on seed,task,kind,split,profile,language,
entity pair and fact permutation. Reject missing,duplicate,unknown or inconsistent records.

Criteria are unchanged:accuracy>=.90,query_pair_accuracy>=.80,evidence_drop>=.35,
query_drop>=.35,two_order_accuracy>=.80. Margin sign and every parent PASS flag must reconstruct.
For each paired criterion, report both_pass,rescued,introduced,both_fail,denominator,arm failure
counts and delta=introduced-rescued. Criteria overlap and are not independent samples.

Primary views:two_char_all,triple_all,shared_prefix2 HOLDOUT,shared_suffix2 TRAIN/HOLDOUT.
Also print per-seed triple views and the explanatory280004/rest partition. This partition is
chosen after observing C280, not a held-out subgroup hypothesis; it cannot exclude a seed or alter
any primary capability result.

Reconstruct ablated accuracy from normal accuracy minus the respective registered drop. Verify
valid integer numerator/denominator before reporting. Separate mask_only answer-cell failures
from answer_involving failures; two_order records remain a separate record class.
Persist every fixed record,not only failures. Normal correct/collapse totals accompany each view.

## Workload, gate and artifacts

Scientific training steps,model forwards,row presentations,core calls,model-state loads,
checkpoint writes and network calls are all0. Reading existing evaluation tensor archives and
hashing existing checkpoints is allowed; no new neural execution or fit is allowed.
The regression/authoring test phase is separate from this zero-neural scientific workload.

Outputs:audit-plan.json,failure-profile.json,validation-summary.json,and summary.json.
Formal PASS means exact diagnostic integrity only;capability_gate_applicable=False,
gate_f_candidate=False,production_adoption=False. No favorable delta is required to PASS.

## Registration and authoring gates

OWN6:benchmark,test,runner,launcher,preregistration,design.
Source pins532;protected inputs940;inherited dependency-union cardinality57.
The child directly imports only the pinned C280 repository module. Its reachable repository
helpers remain covered by the inherited source/input map. No accepted parent source/test is edited.
Own32;modules166;loaded3918;focused3917. Sole inherited exact C204 exclusion unchanged.
The runtime builds the actual suite and checks unique test IDs/counts, not source-number literals.

Manifest SHA256:ff14c1b8c6ed2a2c36f72b716732e8ae624d3ab9e2f96675a7f0763a17a10ea2.
The seal-shape check and equality check are exercised with valid,malformed and mismatched seals.
Commit all OWN6,fetch those committed bytes,review exact blob identities,then activate separately.
User-local Validate must pass parent precheck,own32 and focused3917 before scientific logging.

## Stop

Operational Validate failure:skip science and log publication. Scientific integrity failure:retry
SAME C281 without changing conditions. PASS:accept diagnostic only;Gate F stays NOT PASSED.
No additional training,seed selection,new support boundary or C282 registration in this run.
