# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C281 ACCEPTED PASS (diagnostic integrity only). C282 NOT REGISTERED.**
C281 scientific execution HEAD:96d02062bf98cf32cfc5173c36db28bb00960f0d.
C281 published log commit:e3b5bd2e67da32ccfdff4f7503a99d364f4b76ec.
C280 remains ACCEPTED VALID NEGATIVE. No rerun,seed exclusion,support retuning or Gate F promotion.

## Latest accepted science — C281

Acceptance:docs/experiment-ledger-addendum-c281-c282.md.
Summary:runs/c281-v5b-saved-support-audit-674eda46d9634e258004cabe55550065/summary.json.
Summary SHA256:f56aca6895d5acd69b3c7e557c04fdb95b2b5e13a8b0bfe56f7c6ea4d5878ea7.
Manifest SHA256:ff14c1b8c6ed2a2c36f72b716732e8ae624d3ab9e2f96675a7f0763a17a10ea2.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False. Own32/focused3917 and persisted reconstruction PASS.
Scientific model forwards,training,state loads and checkpoint writes0.

All triple criterion failures control->candidate:
accuracy92->85 (23 rescue,16 introduced);query_pair92->85;evidence_drop45->29;
query_drop58->43;two_order34->33. Criteria overlap.
Mask-only failing answer cells0 in both arms on both tasks. Direct answer discrimination remains.
Evidence-drop net improvement-16 is dominated by280004 (-18),while other seeds worsen+2.
Triple normal answers3960/4320->3973/4320;both arms evidence_blind1080/4320.
Do not infer identical ablated predictions or a unique causal mechanism from pooled counts.

Next question is two-character-only versus mixed two/three-character TRAIN coverage with
unchanged actual C278 all-token dual readout and fixed update budget. Explicitly distinguish
seen-length learning from the original unseen-length transfer target. C282 requires separate
implementation,preregistration,sealing and review before activation.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## Historical state and recovery

Previous complete handoffs are preserved at docs/handoff-history/c280-pre-acceptance.md and
 docs/handoff-history/c281-pre-acceptance.md. Their ACTIVE instructions are historical only.
C279 remains ACCEPTED PASS (diagnostic integrity only);C278/C280 remain ACCEPTED VALID NEGATIVE.
Accepted source/tests,preregistrations,logs and protected dispatchers are unchanged.
