# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C286 ACCEPTED VALID NEGATIVE. C287 NOT REGISTERED. C288 NOT REGISTERED.**
Scientific execution:7fe7c72ff88e252b3087c9715674510dbba96651.
Published log:672b7cc1bf0f75f55c058e73e30ea69e249b2108.
C285 remains ACCEPTED PASS (diagnostic integrity only). No C286 rerun or seed filtering.

## Latest accepted science — C286

Acceptance:docs/experiment-ledger-addendum-c286-c287.md.
Summary:runs/c286-v5b-cosine-tail-1664d75f4cf649fb8c5ca98f4be8308b/summary.json.
Summary SHA256:14bfe8920b80c86cc8e297864402c38c53a26c87085b8963cae363cb6fd98a9a.
Manifest SHA256:3d0ecd3f4785967a88e8b84597d9615be79eb7e609c348bf2ca1cdead8cbe94e.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False;all_prefixes_matched=True.
Own40/focused4085 PASS. All10 states,8000 updates,9620 forwards,539520 rows,38480 core calls.
Primary quad gate:constant_lr2/5,cosine_tail3/5. Two3/3;three3/3;all-task2/3.
Both arms pass286001/286004 and fail all tasks286002/286003. Candidate alone passes quad286005.
Whole seen-length failure does not identify normal TRAIN fitting failure;HOLDOUT is included.
C287 should partition final fitting versus generalization error and stratify saved training losses.
No optimizer cause,universal LR benefit or automatic Gate F closure is established.

## Next experiment status

C287 is not activated in this acceptance commit. Separate preregistration and committed-byte
review must complete before a launcher command is issued. C288 is not registered.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Later lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoffs remain under docs/handoff-history/c280-pre-acceptance.md through
c286-pre-acceptance.md. The latest preserves Git blob f54e6fe35e9f005816a050254943e45702ceb098.
Only this Formal state is authoritative;old ACTIVE instructions are historical.
Accepted source/tests,preregistrations,logs and protected dispatchers remain unchanged.
