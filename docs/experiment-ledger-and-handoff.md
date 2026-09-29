# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C284 ACCEPTED VALID NEGATIVE. C285 NOT REGISTERED. C286 NOT REGISTERED.**
Scientific execution HEAD:3d34f6ba19017fd7d0422f070624ea7b1b494555.
Published log commit:4fe9b2f0d55b98c15855c2f9580572c8e9a9158e.
Primary four-character gates:three_char_only2/5;mixed_length3/5. No C284 rerun,seed selection,
threshold change or Gate F promotion. No active scientific experiment until C285 review/activation.

## Latest accepted science — C284

Acceptance:docs/experiment-ledger-addendum-c284-c285.md.
Summary:runs/c284-v5b-max-length-450fab44535d4dd09c14931b8de1a283/summary.json.
Summary SHA256:83df761b835fa529d72ba1cee5fe618ddaff6936d9db56defc02957b90788c83.
Manifest SHA256:c835e2293c8a379b4173e4030cb687c0bb0bc549ef44298a0d8f8f39b2e6c080.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Own32/focused4013 and persisted scoring passed. Scientific workload:10 fresh models,8000 updates,
384000 training rows,9620 forwards,539520 row presentations,38480 core calls.

Control/candidate pass counts:two3/4;three4/4;four2/3;all1/3.
Candidate-only quad passes284004/284005;control-only quad pass284001;both pass284003;
both fail284002. Candidate284001 passes two/three but fails four;both284002 arms fail all tasks.
One net seed advantage is not uniform superiority. Both maximum trained lengths3;length exposure
allocation/curriculum remain coupled. C285 should attribute matched triple-to-quad criterion failures
from saved outputs before another intervention. It is not registered by this acceptance commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Later lifecycle tests use immutable acceptance addenda.

## Historical state

Full older handoffs remain under docs/handoff-history/c280-pre-acceptance.md through
c284-pre-acceptance.md. The newest history preserves Git blob372b3061355e7334b48e6f5e0eaf02460dc2073e.
Their ACTIVE instructions are historical;only this file's Formal state is authoritative.
C282/C283 remain ACCEPTED VALID NEGATIVE. All accepted source/tests,preregistrations,logs and
protected dispatchers remain unchanged.
