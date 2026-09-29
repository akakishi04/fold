# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through explicit PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C285 ACCEPTED PASS (diagnostic integrity only). C286 ACTIVE / NOT YET JUDGED. C287 NOT REGISTERED.**
C285 scientific execution HEAD:f2bd32785895c30defa16be7d1eca6279ba4ed23.
C285 published log commit:d8a24df7b94a1b8c3d339b868c6db4fc2ed7e3b6.
C284 remains ACCEPTED VALID NEGATIVE. No C285 rerun,seed exclusions or Gate F promotion.
C286 is the unique ACTIVE fixed-budget late-LR-decay experiment.

## Latest accepted science — C285

Acceptance:docs/experiment-ledger-addendum-c285-c286.md.
Acceptance commit:100ac28eca9015269fd69104edf36645c4f1bf9a.
Summary:runs/c285-v5b-saved-length-audit-94786461780e4110a04f18ca3c92c427/summary.json.
Summary SHA256:702092926265bb893babce1e5b93dd234791527344193ea876d33210e8bfdba1.
Manifest SHA256:cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;capability_gate_applicable=False.
Own32/focused4045 PASS;source556/protected991;zero scientific neural calls,training,state loads,writes.
Quad control/candidate failures:accuracy50/43;query_pair48/43;evidence_drop27/27;query_drop30/38;two_order21/20.
Mixed triple-to-quad accuracy:37 persistent matched-cell failures+6 new=43;no rescues.
Seed284002 accounts for42 mixed quad accuracy failures;284001 accounts for the remaining1 (863/864).
Mixed quad mask-only failing answer cells0. Cell co-failure does not prove identical-row errors,
training-set underfit or an optimizer cause. All prior capability verdicts remain unchanged.

## Active C286 — fixed-budget late cosine LR

Experiment:C286-v5b-cosine-tail-stability. Stage:V5-B-COSINE-TAIL-STABILITY.
Registration:docs/experiment-ledger-addendum-c286-preregistration.md.
Design:docs/v5b-cosine-tail-stability-v0.1.md.
Review:docs/c286-post-authoring-review.md.
Acceptance base:100ac28eca9015269fd69104edf36645c4f1bf9a.
Authoring/review target:041087eb0bfc4baf5c9816515659196d351c7345.

One question:at identical mixed2/3 coverage and800 updates,does reducing only the last400
learning rates improve final reliability and unseen-four-character transfer versus constant LR?
Fresh paired seeds286001..286005;arms constant_lr,cosine_tail. Actual C278 all-token
MeanFinalDualReadout in both,14256 parameters,48-token context,independent identical initial states.
Same192 logical TRAIN rows,96 query pairs,200 epochs x4 batches x48 rows.
randperm96(seed+286000+epoch);profile=epoch%3;length=epoch%2. Both per-length row exposures100/100;
length/profile update matrix[[136,132,132],[132,136,132]]. No quadruple/HOLDOUT/ablated training.

Control LR.005 for updates1..800. Candidate LR.005 for1..400;for401..800:
eta(s)=.0005+.0045*(1+cos(pi*(s-400)/400))/2,assigned BEFORE update s.
No warmup,extra steps,seed selection,loss/model/coverage change or checkpoint selection.
AdamW betas.9/.999,eps1e-8,weight_decay0,clip1,CE only;fit RNGseed+287000 resets per arm.
CPU float64,2 threads,deterministic. Record actual800 LRs,their hash,800 minibatch losses and
step400 fingerprint. Both arms' step400 state and first400 losses must match exactly.

Freeze final states,evaluate unchanged2/3/4 tasks,and strict-replay all3. Primary PASS requires
all5 cosine_tail states pass every FOUR-character fixed criterion. Two/three/all-task gates are
descriptive. Thresholds unchanged:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Report all5 pairs and180 contrasts;absolute candidate PASS is not comparative superiority.
No optimizer-root-cause claim or automatic Gate F completion. Prior verdicts stay unchanged.

Workload:10 models,8000 updates,384000 training rows,9620 forwards,539520 row presentations,
38480 core calls,one10-state checkpoint bundle write/load,10 strict state loads;network0.
Registration:source562;protected1001;dependency-union62;own40;modules171;loaded4086;focused4085.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:3d0ecd3f4785967a88e8b84597d9615be79eb7e609c348bf2ca1cdead8cbe94e.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own40).
Review target:041087eb0bfc4baf5c9816515659196d351c7345. All6 OWN files fetched after commit;
Git blob identities match tested local bytes6/6. Post-match own40 PASS in4.715s.
Linux/Python3.13.5/PyTorch2.10.0+cpu;Python and3 embedded blocks compile;unresolved globals0.
Tests execute800 updates per arm on a small toy model and instrument applied optimizer LRs.
Other fixtures mock parent archives,Git and inherited models/scorers;this is NOT C286 science.
Real parent artifacts,real models/tables,full focused4085,PowerShell parsing and actual10-model
science remain authoritative Windows runtime gates. Reviewed OWN6 must not change at activation.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C286 -> Validate(parent/source/input
562/1001,real TRAIN tables/models/LRs,own40,focused4085) -> authoring_runtime_preflight=PASS ->
Execute(10 fresh models,common400-step-prefix audit,frozen3-task evaluation,strict replay,
persisted reconstruction) -> log publication.

Validate failure skips science/publish. Scientific integrity failure retries SAME C286.
Valid quad gate miss is ACCEPTED VALID NEGATIVE. Do not alter LR endpoints,seeds,steps or thresholds
after results. C287 is not registered until C286 formal judgment. Keep execution HEAD distinct
from the subsequent log publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Later lifecycle tests use immutable acceptance addenda.

## Historical state

Prior full handoffs are preserved under docs/handoff-history/c280-pre-acceptance.md through
c285-pre-acceptance.md. The newest preserves Git blob1f9a2cc8ccb9357141b424435e6700723f385b96.
Their ACTIVE instructions are historical;only this file's Formal state is authoritative.
Accepted source/tests,preregistrations,logs and protected dispatchers are unchanged.
