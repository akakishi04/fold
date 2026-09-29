# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C283 ACCEPTED VALID NEGATIVE. C284 NOT REGISTERED.**
C283 scientific execution HEAD:24c4acd44905e1d3c4d2a019214eb588d72f9a93.
C283 published log commit:aedfa69557782b7484ee71128b08213a27d8798d.
Four-character whole gates:mixed_length3/5;two_char_only0/5. No rerun or seed selection.
C282 remains ACCEPTED VALID NEGATIVE. No Gate F promotion or retrospective threshold change.

## Latest accepted science — C283

Acceptance:docs/experiment-ledger-addendum-c283-c284.md.
Summary:runs/c283-v5b-frozen-four-bacee738e5a04007ae0f0f3093b0f5a7/summary.json.
Summary SHA256:609718db24ca6e3eda4f8916f04f56b24bff3621ddca4ebe136209617fad4949.
Manifest SHA256:e88244fe1acc677d629e3b0400dc4926be9b26560c05a782122ae1e5042213a4.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False;
all_replays=True;all_weights_preserved=True. Own32/focused3981 and persisted reconstruction PASS.
Scientific workload1350 forwards,129600 rows,5400 core calls,zero training/new checkpoint writes.

Mixed states282002/282003/282004 pass;282001/282005 fail. All control states fail.
All-value-split four-character correct3805/4320->4266/4320;collapse347->5.
HOLDOUT correct1239/1440->1391/1440;shared_suffix3 HOLDOUT325/480->469/480.
All seeds improve pooled normal accuracy/collapse,but not all profile/criteria are solved.
All four-character examples were untrained. Transfer benefit does not isolate diversity from larger
maximum training length. C284 should compare three-character-only with mixed two/three at matched
maximum training length3 and matched total updates. No C284 registration in this acceptance commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads mutable handoff. Preserve this seal.
Later lifecycle-aware tests use immutable acceptance addenda after acceptance.

## Historical state and recovery

Full prior handoffs are preserved under docs/handoff-history/:
c280-pre-acceptance.md,c281-pre-acceptance.md,c282-pre-acceptance.md,c283-pre-acceptance.md.
The last preserves Git blob902e902bfb175f8b127b676c8141ee65ab8dba82 byte-for-byte.
Only this file's Formal state is authoritative;older ACTIVE instructions are historical.
All accepted source/tests,preregistrations,logs and protected dispatchers remain unchanged.
