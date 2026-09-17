# C178 acceptance — visible leaf binding did not yield joint improvement

Judged 2026-09-18 JST. V5-E; repository akakishi04/fold; branch feat/sft-target-loss.
Read the unchanged C178 preregistration and experiment conversation handoff protocol.

## Formal verdict

**C178 ACCEPTED VALID NEGATIVE. Gate E NOT PASSED. C179 NOT REGISTERED here.**
C176 remains ACCEPTED VALID NEGATIVE. C174/C175/C177 retain their scoped PASS verdicts.
Earlier C160/C168/C169 negatives and all other accepted results remain unchanged.
No rerun, threshold adjustment, checkpoint/seed selection, extra training or reinterpretation
of a secondary endpoint may turn this C178 result into a PASS.

## Execution validity and identity

Execution HEAD e9ee578a80b63e72a33414b62ba17a0111329ddb.
Source/artifact precheck PASS; 1057/1057 focused regression tests in 24.268 seconds.
Six models; seeds178001/178002/178003; INDIRECT_FACTS and BOUND_VISIBLE_FACTS.
Initial parameter hashes and sampled row-index schedule hashes match within all three pairs.
Both arms use the same original MLP26114 and ordinary unweighted CE, 2000updates/model,
batch256, Adam0.001, CPUfloat32/two threads. Environment torch2.10.0+cu130, NumPy2.3.5.
12000updates/3072000sampled rows;56376pilot and254664TRAIN predictions;312inference batches.
51840prepared rows;207360leaf/fact lookups;414720copied fields. Six new checkpoint
roundtrip deserializations, historical checkpoint loads0. Acquisition/proof/evidence/network0.
production_runtime_modified=false;gate_e_candidate=false.
60historical source pins,90protected input paths,10output artifacts. Outer runner confirms
protected inputs preserved,tracked tree clean,execution HEAD preserved,run_execution_valid=True.
The old C145 warning appears inside a passing test and is not execution invalidity.
Benchmark wall clock78.58461839999654s is not serving latency or an isolated model speed result.

Report: runs/c178-v5e-leaf-binding-e16d745f5b3242728e9c561023938719/summary.json
Report SHA256:19bee9fbb4068d43bcd05378b18e0e87f4b4e50fc73b635b5e69f7d2d30190d8
Uploaded log387180bytes;SHA25698bfddf9d6ed487492f9b4f77898c06f43cb523b867c0082ab409b0552f6c2ef.
Canonical reconstructed summary196186bytes;hash agrees with runner report.
leaf-binding-plan.json7734bytes,3330adcc0f35875b867ab1057413e9676bbb99eed119074e4eec631f8253f574.
input-binding-audit.json524bytes,b582ddbd2636348c6eddecc4d91224f4cd966425a1f097bf275f8dad11fc03e5.
Scientific manifest4393da528c6193cd2d8762cfea081e102e02537148299578806b0f3dcb9facc0.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Parent C177 SHA25699f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4.

## Deciding metrics

BA values below are percentages. Comparisons are within new paired seeds, not against
selected old checkpoints. Primary averages missing-count1/2/3 BA equally.

|Seed|Primary indirect|Bound|Original group-macro indirect|Bound|
|---|---:|---:|---:|---:|
|178001|53.172280|52.562457|70.783067|69.946975|
|178002|56.274442|55.025598|70.943987|70.149642|
|178003|54.140143|54.611457|71.781432|72.672966|

|Seed|Count1 NEEDS recall indirect -> bound|Count3 SUFFICIENT recall indirect -> bound|
|---|---|---|
|178001|10/768 -> 0/768|16/312 -> 18/312|
|178002|132/768 -> 150/768|74/312 -> 43/312|
|178003|107/768 -> 146/768|4/312 -> 15/312|

The five preregistered conditions, in order, are:
178001:[false,false,false,true,true];178002:[false,false,true,false,true];
178003:[true,true,true,true,true]. Only the third pair meets the entire gate.
All bound aggregate recalls exceed0.5; this does not cancel the other failed conditions.
No seed averaging or exclusion is used. The registered result is VALID NEGATIVE.

## Secondary interpretation, not replacement gates

PILOT within-count mean AUC indirect -> bound:
1780010.5975481208->0.5955648533;
1780020.6032318415->0.5983654107;
1780030.6029385231->0.5951205973.
Same-visible-key AUC0.6079841983->0.5967611385,
0.6045472118->0.5928530009,0.5995276409->0.5919892239.
Both ordering summaries decline in all three pairs. TRAIN ordering also declines in all3.
The third pair's classification improvement is not evidence of improved overall ranking.

PILOT rescued/new errors:103/106,148/176,168/214.
TRAIN rescued/new errors:352/457,629/688,777/760.
It is possible for group-balanced metrics to improve while row-level accuracy falls;
these have different weighting and the third pair demonstrates that distinction.
TRAIN primary indirect->bound:0.5720832496->0.5707278832,
0.6228227898->0.6163465975,0.5769863198->0.5925707752.
TRAIN group-macro0.7289499759->0.7225348071,0.7374002207->0.7330927331,
0.7380950389->0.7466864415. Weakness is not confined to unseen groups.
Count0/4 remain perfect; their absent-class BA/AUC remain null.

## Scientific scope and confounds

Explicit copying of already-visible facts to leaves did not consistently improve the
registered classification trade-off under this flat MLP and fixed training workload.
This does NOT establish that binding is irrelevant, that longer/larger training would
or would not help, or that FOLD cannot learn necessity. It rejects this bounded claim,
not all possible structured inputs. Do not adopt the bound representation as a generally
validated improvement. The one successful seed is retained but not selected for deployment.

The transform performs handwritten lookup, not learned binding or Boolean evaluation.
No hidden values, expected necessity, truth-table outputs or proof repairs enter inference.
It activates former zero coordinates; equal parameter count does not imply identical
optimization geometry. Same four repeatedly inspected development groups; not independent
confirmation. Correlated pair combinations are not independent trials.

Existing secondary tables already answer the score-order/error-exchange questions for
this run. Another unchanged-logit audit merely seeking a favorable metric is not warranted.
A next design may test learned composition along known syntax links versus a sequential
shared-update control. That is a NEW computation-graph hypothesis, not an established
cause or an adopted FOLD-core change. Both controls and compute accounting need to be
fixed before training; avoid comparing a larger recurrent model to a smaller flat one
and attributing every gain to topology alone.

## Review scope and disposition

Reviewer independently reconstructed the complete summary/hash, recomputed312confusion
tables,72ordering tables,12exact AUC means,12stratum/group sums and36error-exchange tables,
checked their linkage to classification totals,1057test entries,fit identities,paired
initial/batch hashes,workload counts and all three five-condition gates. They agree.
Ten output artifact bytes,raw NPZ/logits/checkpoints and input-binding-audit.json were NOT
independently reread here.1057tests and six full fits were NOT rerun by reviewer.
Preserve all outputs. No C178 rerun is needed for documentation. C179 remains unregistered
at this acceptance-only boundary; any next experiment needs its own preregistration.
