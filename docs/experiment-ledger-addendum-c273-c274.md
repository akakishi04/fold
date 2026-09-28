# C273 acceptance and C274 first-vs-last-boundary diagnostic

## Formal verdict

C273 ACCEPTED VALID NEGATIVE. The preregistered dual_boundary candidate passed1/5 whole-state gates;
the matched boundary_pair control passed0/5. Both arms passed5/5 on the original two-character task.
For the unseen three-character task,boundary_pair passed0/5 and dual_boundary passed1/5. The fixed
all-five candidate gate remains false. Gate F NOT PASSED.

Scientific execution HEAD:1106e0898e1698a06b78ac2266c65a983aded275.
Published log commit:22b74e6a2aba7f265edf68994563f472328af241.
Publisher log SHA256:0917e14d23fee4eb07bc87e9c03226a459155636f5bc4ce5ad0318f3aba34c96.
Publisher log bytes:839378.
Git normalized log blob:5ff51a90b84aac52e0556729d0398d5785810693.
Summary:runs/c273-v5b-dual-boundary-b70af8ffe4b047ee95a0044e86de7a8c/summary.json.
Summary SHA256:0e764c595c64818c308779cd5190883edec0654375c82970641efa70b980f82e.

## Execution validity

The pre-science runtime gate passed before science:parent/source/artifact precheck484/840,
sealed manifest fd38d800c08dcf7fb783f6f5c156169e75b29b1208c175d32259e2d4c77eea7f,
own24 PASS and focused3717 PASS. Ten fresh matched models completed800 updates each.
Total8000 optimizer updates,384000 training rows,9080 model forwards,487680 row presentations and
36320 core calls. One10-state bundle write/load and10 strict state loads completed.
all_pairs_matched=True;all_replays=True. Persisted dual-boundary reconstruction passed;tracked tree
and execution HEAD were preserved. run_execution_valid=True;scientific_status=FAIL;
candidate_gate=False.

The prior C273 preflight failures were operational only;no scientific log was published for them.

## Deciding metrics

Whole-state pass counts:
-boundary_pair:0/5;
-dual_boundary:1/5.

Original two-character subgate:
-boundary_pair5/5;
-dual_boundary5/5.

Unseen three-character subgate:
-boundary_pair0/5;
-dual_boundary1/5.

Aggregate HOLDOUT two-character answers:
-doubled:control480/480,candidate480/480;collapse0/240 vs0/240;
-shared_prefix:480/480 vs480/480;collapse0 vs0;
-shared_suffix:480/480 vs480/480;collapse0 vs0.

Aggregate three-character answers:

|split/profile|Boundary correct|Dual correct|Boundary collapse|Dual collapse|
|---|---:|---:|---:|---:|
|TRAIN tripled|960/960|960/960|0/480|0/480|
|TRAIN shared_prefix2|960/960|953/960|0/480|7/480|
|TRAIN shared_suffix2|911/960|885/960|32/480|70/480|
|HOLDOUT tripled|480/480|479/480|0/240|0/240|
|HOLDOUT shared_prefix2|480/480|473/480|0/240|4/240|
|HOLDOUT shared_suffix2|448/480|424/480|10/240|29/240|

dual_boundary therefore does not improve the cohort as a whole. It degrades shared-suffix binding and
slightly worsens shared-prefix/tripled pooled accuracy,despite producing one full passing seed.

Per-seed dual_boundary HOLDOUT triple /288:
-273001=288/288,collapse0;
-273002=276/288,collapse6;
-273003=267/288,collapse13;
-273004=282/288,collapse3;
-273005=263/288,collapse11.

Seed273001 is the sole candidate whole-state PASS. Its success is scientifically interesting but
does not override the preregistered5/5 reliability requirement.

## Scientific interpretation

The C272 hypothesis that pre-softmax boundary averaging might be the main remaining bottleneck is
not supported as a general fix. Keeping first/last attentions separate can produce a fully successful
state, but across fresh initializations it increases shared-suffix collapse and lowers pooled
accuracy. The dominant unresolved issue is therefore not simply the location of the first/last
fusion operation.

C271/C272 together suggest directional boundary information matters. C273 shows that naively
combining two normalized attentions does not reliably exploit that complementarity.

## Non-claims

Do not claim dual attention is solved because seed273001 passes. Do not select that seed,extend
training,change fusion weights,or alter thresholds post hoc. Do not claim boundary_pair is generally
superior either;this cohort's boundary control itself is much stronger than C272's cohort and yet
still fails the triple gate. Arbitrary names,natural language and unbounded lengths remain out of
scope.

## Accepted artifacts

-architecture-plan.json:fd38d800c08dcf7fb783f6f5c156169e75b29b1208c175d32259e2d4c77eea7f;2974 bytes.
-dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024 bytes.
-triple-dataset.json:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;158236 bytes.
-trained-models.pt:4e615c72c7636edf7ce8d3d28baff40f7c02f286c954e61ca9b1d08962857c6e;1238007 bytes.
-evaluations.pt:8cc808e477f5297e4d4f85c35cf0bb33714cb2f7a32c08c35476bc0a7ec1a1fd;106277991 bytes.
-measurements.json:8eb887d84ae4c75f4b7100e4bbd8ed594ffb83fa75d2908810814209fc601cbe;524899 bytes.
-validation-summary.json:ecbb73d07a663c983b7add84ed9e168116e9118a9debeea16537f5f1ed0158cd;22917 bytes.

## Next question, not activation

Before another fusion architecture,measure the directional components directly:

With identical fresh paired CE training,how do FIRST-only and FINAL-only query-boundary states differ
on shared-prefix versus shared-suffix transfer?

C274 should compare:
-first_boundary:read.query receives only the first visible query-byte pre-core state;
-final_boundary:read.query receives only the final visible query-byte pre-core state.

No candidate/winner gate should be inferred from pooled superiority. This is a directional diagnostic:
predeclare two contrasts:
1.final_boundary should be reported on shared_prefix2;
2.first_boundary should be reported on shared_suffix2.
Both arms must also report original two-character retention and all other triple profiles.

Use fresh matched seeds,the exact C273 paired CE training policy,and the same fixed evaluation
thresholds. The diagnostic should not change Gate F state and should not select a fusion weight.
C274 requires separate preregistration,implementation,final manifest sealing,committed-byte review
and runtime Validate. C275 NOT REGISTERED.
