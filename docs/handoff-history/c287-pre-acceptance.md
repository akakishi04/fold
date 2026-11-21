# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C286 ACCEPTED VALID NEGATIVE. C287 ACTIVE / NOT YET JUDGED. C288 NOT REGISTERED.**
Scientific execution:7fe7c72ff88e252b3087c9715674510dbba96651.
Published log:672b7cc1bf0f75f55c058e73e30ea69e249b2108.
C285 remains ACCEPTED PASS (diagnostic integrity only). No C286 rerun or seed filtering.
C287 is the unique ACTIVE saved fit/generalization diagnostic.

## Latest accepted science — C286

Acceptance:docs/experiment-ledger-addendum-c286-c287.md.
Acceptance commit:6ce09f66e8ea61a9fbfffd1e2de38a9ba8cdef61.
Summary:runs/c286-v5b-cosine-tail-1664d75f4cf649fb8c5ca98f4be8308b/summary.json.
Summary SHA256:14bfe8920b80c86cc8e297864402c38c53a26c87085b8963cae363cb6fd98a9a.
Manifest SHA256:3d0ecd3f4785967a88e8b84597d9615be79eb7e609c348bf2ca1cdead8cbe94e.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False;all_prefixes_matched=True.
Own40/focused4085 PASS. All10 states,8000 updates,9620 forwards,539520 rows,38480 core calls.
Primary quad gate:constant_lr2/5,cosine_tail3/5. Two3/3;three3/3;all-task2/3.
Both arms pass286001/286004 and fail all tasks286002/286003. Candidate alone passes quad286005.
Whole seen-length failure does not identify normal TRAIN fitting failure;HOLDOUT is included.
No optimizer cause,universal LR benefit or automatic Gate F closure is established.

## Active C287 — saved fitting/generalization partition

Experiment:C287-v5b-saved-fit-partition-audit. Stage:V5-B-SAVED-FIT-PARTITION-AUDIT.
Registration:docs/experiment-ledger-addendum-c287-preregistration.md.
Design:docs/v5b-saved-fit-partition-audit-v0.1.md.
Review:docs/c287-post-authoring-review.md.
Acceptance base:6ce09f66e8ea61a9fbfffd1e2de38a9ba8cdef61.
Initial authoring:b325a61090f731c4ee472d00e7b8542c101ab328.
Final review target:496cc0a6cc6b26eb4629495b8254f39591b80d61.

One question:where residual C286 error appears across optimized normal TRAIN,seen-length HOLDOUT,
and untrained length4,with final split scores separated from stratified saved training losses?
Keep all10 states,seeds286001..286005,constant_lr/cosine_tail. No new model,data,training or forwards.
Exact C286 verifier plus thirteen hashes,C286 source identity and8 artifacts are fixed.
Reconstruct3240 records into60 final model/task/split partitions,retaining all original task flags.
Report correct/collapse,final row-weighted NLL,criterion failures,direct/full gates and mask-only cells.
Direct gates use accuracy/query-pair/two-order;mask criteria remain separate. Prior gates unchanged.

For each state,report fitted2/3 TRAIN direct pass,seen2/3 HOLDOUT direct pass,quad direct pass and
first_direct_failure_partition in that fixed ordering. These labels describe failure locations,
not causal propagation. Quad TRAIN means inherited value partition,not optimized four-character data.
Trace windows:updates1..400,401..600,601..800;stratify each by2 lengths x3 profiles.
180 bins total,90 paired mean-CE deltas;counts always explicit. Check exact common400 prefix again.
Pre-update minibatch CE is not final-model full-TRAIN NLL. No checkpoint/window/seed selection.

Scientific workload:all neural forwards,row presentations,core calls,training,model-state loads,
new checkpoint writes and network calls0. Reading saved logits for reconstruction is permitted.
C287 PASS means diagnostic integrity only;capability_gate_applicable=False. Gate F remains NOT PASSED.
Registration:source568;protected1016;dependency-union63;own32;modules172;loaded4118;focused4117.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:98e5768640301fd36d00706305809bd5b4707eb10458bee5abfaef478b1bf430.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own32).
Review target:496cc0a6cc6b26eb4629495b8254f39591b80d61. Final OWN6 Git blobs match local tested bytes6/6.
Review corrected four new-test default read_text calls to explicit UTF-8;no scientific change.
Final identity-matched own32 run PASS in0.955s on Linux/Python3.13.5/PyTorch2.10.0+cpu.
Python and3 embedded blocks compile;unresolved globals0. Parent archives/Git are mocked in fixtures.
Actual parent data/pins,full4117 regression,PowerShell ParseFile and saved reconstruction remain
pending authoritative Windows execution. Do not claim actual C287 diagnostic findings yet.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C287 -> Validate(parent/source/input
568/1016,real partition schema dry-run,own32,focused4117) -> authoring_runtime_preflight=PASS ->
Execute(saved fitting/generalization partition and stratified losses;zero model calls) -> postcheck
-> log publication. Validate failure skips science/publish. Integrity failure retries SAME C287.
Do not register C288 before C287 judgment;do not change parent LR/seeds/thresholds or prior verdicts.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Later lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoffs remain under docs/handoff-history/c280-pre-acceptance.md through
c286-pre-acceptance.md. The latest preserves Git blob f54e6fe35e9f005816a050254943e45702ceb098.
Only this Formal state is authoritative;old ACTIVE instructions are historical.
Accepted source/tests,preregistrations,logs and protected dispatchers remain unchanged.
