# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C284 ACCEPTED VALID NEGATIVE. C285 ACTIVE / NOT YET JUDGED. C286 NOT REGISTERED.**
C284 scientific execution HEAD:3d34f6ba19017fd7d0422f070624ea7b1b494555.
C284 published log commit:4fe9b2f0d55b98c15855c2f9580572c8e9a9158e.
Four-character primary:three_char_only2/5;mixed_length3/5. No C284 rerun,seed selection,
threshold change or Gate F promotion. C285 is the unique ACTIVE saved-output diagnostic.

## Latest accepted science — C284

Acceptance:docs/experiment-ledger-addendum-c284-c285.md.
Acceptance commit:8b16da05d3669e86ee6b9d323c6cb9eeec4766bf.
Summary:runs/c284-v5b-max-length-450fab44535d4dd09c14931b8de1a283/summary.json.
Summary SHA256:83df761b835fa529d72ba1cee5fe618ddaff6936d9db56defc02957b90788c83.
Manifest SHA256:c835e2293c8a379b4173e4030cb687c0bb0bc549ef44298a0d8f8f39b2e6c080.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Own32/focused4013 and persisted scoring passed. Scientific workload:10 fresh models,8000 updates,
384000 training rows,9620 forwards,539520 row presentations,38480 core calls.

Control/candidate pass counts:two3/4;three4/4;four2/3;all1/3.
Candidate-only quad passes284004/284005;control-only quad pass284001;both pass284003;
both fail284002. Candidate284001 passes two/three but fails four;both284002 arms fail all tasks.
A net one-seed advantage is not uniform or established population superiority. Both maximum trained
lengths3;length exposure allocation/curriculum remain coupled. Do not compare C283/C284 rates
as a single-factor comparison:their control and seed cohorts differ.

## Active C285 — saved matched-cell length-transfer attribution

Experiment:C285-v5b-saved-length-transfer-audit.
Stage:V5-B-SAVED-LENGTH-TRANSFER-AUDIT.
Registration:docs/experiment-ledger-addendum-c285-preregistration.md.
Design:docs/v5b-saved-length-transfer-audit-v0.1.md.
Review:docs/c285-post-authoring-review.md.
Acceptance base:8b16da05d3669e86ee6b9d323c6cb9eeec4766bf.
Authoring/review target:8b2b1030fea7166bdd86537290f5b874f6c66266.

One question:which C284 quad fixed-criterion failures are newly introduced relative to the same
model's matched triple cells,and how does this attribution differ between the two arms?
Keep all10 saved states,seeds284001..284005,three_char_only/mixed_length. No training/model change.
Reconstruct3240 fixed records covering two/three/four tasks. Primary quad arm comparison has540
matched records. Within-state triple-to-quad has540 matched records per arm. Profile mapping is
by structural index only;all split/language/entity-pair/fact-order keys must match exactly.

Report both pass,left fail/right pass,left pass/right fail,both fail for each criterion;
normal correct/collapse,ablated correct and mask-only counts;all per-seed views;quad split/profiles.
Criteria unchanged:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
No filtering of failed seeds. Matched-cell co-failure is not proof of the same wrong individual
rows or a causal inheritance mechanism. This is diagnostic evidence,not independent replication.

Scientific model forwards,training,row presentations,core calls,model-state loads,checkpoint writes
and network calls0. Parent reconstruction uses C284.verify_artifacts with neural Module calls,
state loading and checkpoint writes blocked. PASS means diagnostic integrity only,not capability.
Gate F stays NOT PASSED regardless of diagnostic direction.
Registration:source556;protected991;dependency-union61;own32;modules170;loaded4046;focused4045.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own32).
Review target:8b2b1030fea7166bdd86537290f5b874f6c66266. All6 committed OWN files re-fetched;
Git blob identities match tested local bytes6/6. Linux/Python3.13.5/PyTorch2.10.0+cpu:
final own32 run PASS in1.645s;Python and3 embedded blocks compile;unresolved global names0.
Fixtures mock parent archives/Git. No actual C285 saved-parent diagnostic result is claimed.
Real parent provenance,pins,full focused4045,PowerShell ParseFile and real reconstruction remain
pending authoritative Windows execution. Activation must not change reviewed OWN6.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C285 -> Validate(parent/source/input
556/991,own32,focused4045) -> authoring_runtime_preflight=PASS -> Execute(saved matched-cell audit;
model_forward_calls0) -> persisted postcheck -> log publication.

Validate failure skips science/publish. Scientific integrity failure retries SAME C285.
Do not register C286 or change any parent training/threshold/seed before C285 formal judgment.
Keep scientific execution HEAD distinct from the later log publication commit.

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
