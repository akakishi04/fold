# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C280 ACCEPTED VALID NEGATIVE. C281 ACTIVE / NOT YET JUDGED. C282 NOT REGISTERED.**
C280 scientific execution HEAD:2c2eb8a86a03910ba9c63ff277c137d1e842a32f.
C280 published log commit:ae0a53cd8e0beb65ac4e1909edadecd51d833fdf.
Both arms:two-char4/5,triple0/5,whole0/5. Seed280004 fails two-char in both arms.
C281 is the unique ACTIVE saved-output diagnostic. Do not rerun C280,select seeds,retune the
support boundary or promote Gate F. C282 is not registered.

## Latest accepted science — C280

Acceptance:docs/experiment-ledger-addendum-c280-c281.md.
Acceptance commit:3b06f8d34f2b4ce0bc7a234c3e29c2b5234df95d.
Summary:runs/c280-v5b-evidence-only-dual-bb662d609be24ad9a1fd20d4aef54174/summary.json.
Summary SHA256:00410f3d879cb9571186e2ebf08a1ca9df0b31b64a639adae53f503c068bc7db.
Manifest SHA256:c02aa9b88d7eeb9a7671674b982b5d7dad420c88cae10b4e40b4c6130219e1ac.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Published own24/focused3885 and persisted reconstruction PASS. Gate F NOT PASSED.
The initial manifest guard failure was operational preflight only,not scientific evidence.
Evidence-only direct attention support was insufficient for the fixed gate; gate totals alone do
not identify which criterion improved or regressed. Shared seed280004 failure is not candidate-only.

## Active C281 — saved support-intervention transitions

Experiment:C281-v5b-saved-support-transition-audit.
Stage:V5-B-SAVED-SUPPORT-TRANSITION-AUDIT.
Registration:docs/experiment-ledger-addendum-c281-preregistration.md.
Design:docs/v5b-saved-support-transition-audit-v0.1.md.
Review:docs/c281-post-authoring-review.md.
Authoring/review target:5e16246a8f7d6ccc4c9ac652d9bf9de3be2e5042.
Acceptance base:3b06f8d34f2b4ce0bc7a234c3e29c2b5234df95d.

One question:which C280 fixed-criterion failures does evidence-only support rescue or introduce,
especially shared_suffix2,and how much of the residual is shared seed280004 failure rather than
candidate-specific regression?

All C280 seeds280001..280005 and both arms remain primary. No new model,training,forward,state load,
checkpoint write or network call. Parent C280 and C279..C274 artifacts are validated with neural
Module calls,state loading and checkpoint writes blocked. The child reconstructs2160 fixed records
and1080 matched control/candidate records. Count both rescues and newly introduced failures;
reconstruct normal/ablated accuracy and mask-only versus answer-involving failures.

Primary views:two_char_all,triple_all,shared_prefix2 HOLDOUT,shared_suffix2 TRAIN/HOLDOUT.
Per-seed triple views and280004/rest are explanatory;no seed exclusion or revised capability gate.
Thresholds unchanged:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
C281 PASS means diagnostic integrity only. Gate F remains NOT PASSED regardless of diagnostic values.

Registration:source532;protected940;inherited dependency-union57;own32;modules166;
loaded3918;focused3917;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:ff14c1b8c6ed2a2c36f72b716732e8ae624d3ab9e2f96675a7f0763a17a10ea2.

## C281 post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static + local fixture own32).
review_target_HEAD=5e16246a8f7d6ccc4c9ac652d9bf9de3be2e5042.
All OWN6 fetched after commit;6/6 match locally tested Git blob identities.
Local Python3.13.5/PyTorch2.10.0+cpu:own32 PASS;Python/embedded blocks compile;unresolved global names0.
Fixtures mock parent artifacts/Git context;this is NOT authoritative Windows execution.
Actual parent artifact verification,full focused3917 and native PowerShell parsing remain PENDING.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7,after ParseFile on the dispatcher.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C281 -> Validate(source/artifact532/940,
own32,focused3917) -> authoring_runtime_preflight=PASS -> Execute(saved audit;no neural execution)
-> persisted postcheck -> log publication.

Validate failure skips science and scientific log publication. Execute integrity failure retries
SAME C281. No new seeds,training,thresholds or C282 registration before C281 is judged.
Keep scientific execution HEAD separate from the subsequent published log commit.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## Historical state and recovery

The complete pre-C280-acceptance handoff is preserved byte-for-byte at
`docs/handoff-history/c280-pre-acceptance.md` (Git blob af114ae862372baa3d49106776b078b127f8f050).
Its ACTIVE and execution instructions are historical;only this file's Formal state is current.
C279 remains ACCEPTED PASS (diagnostic integrity only);C278 remains ACCEPTED VALID NEGATIVE.
Earlier acceptances/preregistrations,accepted source/tests,logs and protected dispatchers are unchanged.
