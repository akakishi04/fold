# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C282 ACCEPTED VALID NEGATIVE. C283 NOT REGISTERED. C284 NOT REGISTERED.**
C282 scientific execution HEAD:aef5aecfc438679641e59b337d7a9eb615c619a3.
C282 published log commit:b8c0462a27246cf6ff9d9024b614dbca244be2b1.
C282 mixed_length:whole4/5,two_char4/5,triple4/5;two_char_only:whole0/5,two_char4/5,triple0/5.
No C282 rerun,threshold relaxation,seed replacement or Gate F promotion.

## Latest accepted science — C282

Acceptance:docs/experiment-ledger-addendum-c282-c283.md.
Summary:runs/c282-v5b-mixed-length-5ad726e62dfa4eacada5a8cda8c4c27f/summary.json.
Summary SHA256:075cb7399f62d048310bdfb1c31c93ac39ab8b3dc400578d60e062ebfdacf3d1.
Manifest SHA256:291ed152bec43b222e54851c5e4699776e220d60937a733599c37f617ed400de.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Own32/focused3949 and persisted reconstruction PASS. Registered10-model workload completed.
Mixed seed282001 fails both tasks;other mixed seeds pass both. Control seed282005 fails two-char;
all control seeds fail triple. This is substantial seen-length learning improvement,not unseen-length
success and not the fixed five-seed gate. All seeds must remain in subsequent comparison.

## Next question — not active

Freeze every C282 final state and compare completely unseen four-character identifier transfer.
No further training,seed selection or model-configuration change. Preserve48 tokens,original tasks
and gates. Four-character candidate PASS cannot revise C282 acceptance or promote Gate F.
Mixed length versus two-only does not isolate diversity from maximum training length/proximity.
C283 requires separate implementation,preregistration,sealing,tests and committed-byte review.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads mutable handoff. Preserve this seal.
Later lifecycle-aware tests use immutable acceptance addenda after acceptance.

## Historical state and recovery

Previous full handoffs:docs/handoff-history/c280-pre-acceptance.md,
docs/handoff-history/c281-pre-acceptance.md,and docs/handoff-history/c282-pre-acceptance.md.
The last file preserves pre-acceptance Git blob d5df20dd7ca7f8350244b05fb4f754b3a581c67e.
Their ACTIVE instructions are historical only;only this Formal state is authoritative.
C281/C279 remain ACCEPTED PASS (diagnostic integrity only);C280/C278 remain ACCEPTED VALID NEGATIVE.
All accepted source/tests,preregistrations,logs and protected dispatchers are unchanged.
