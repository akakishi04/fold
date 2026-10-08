# C313 preregistration — frozen six-character transfer

Experiment:C313-v5b-frozen-six-transfer. Stage:V5-B-FROZEN-SIX-TRANSFER.
Acceptance base:0c4dfe291010f90d7b444c36fd49d3accf64158c.
C312 ACCEPTED VALID NEGATIVE remains;Gate F NOT PASSED;C314 NOT REGISTERED.

## One question and prospective primary

Do all five retained random_pairs baseline checkpoints transfer from training lengths2/3/4
to the previously untested length6 without retraining? Evaluate ALL ten C312 checkpoints,
including all five value_balanced comparators and its failed312002 state. Do not select
individual successful models,combine arms per query,or choose a primary after six results.

The prospective primary is all5 RANDOM_PAIRS states passing six-character local/masked gates.
Random is the pre-existing unchanged baseline,not the C312 registered candidate. C312's balanced
4/5 remains a negative irrespective of C313. Six is a new held-out length,not another scoring
of five to relabel C312. This choice does NOT establish random batching as universally superior.
Balanced six results are fully reported but cannot rescue a random baseline primary failure.

## Unchanged weights and model;new length only

C312 seeds312001..312005,both original arms,all14,256 stored parameters,64slots are retained.
All models trained only on normal lengths2/3/4 TRAIN,1200updates,coreLR.0005/other.005.
No new training,coefficient,optimizer,model parameter,seed search or slot extension.
Use exact C312.make_models and load_bundle then strict-load every state once and freeze it.
The original decoder uses all256 classes without restricting outputs to supplied values.
Core and reader computations remain unchanged;this is not a new architecture or speed claim.

Extend only the accepted renderer's permitted identifier length to6 in a child function.
Same repeat/shared-prefix/shared-suffix semantics,entities,fact order,values,question,language,
TRAIN/HOLDOUT value splits and normal/evidence-blind/query-blind views. The child renderer
must equal every stored C312 length2..5 prompt AND C304.render byte-for-byte before evaluation.
For length6:864 distinct normal inputs,none identical to an old normal input;new UTF-8 byte
vocabulary is contained in the old one. Japanese maximum61 bytes plus BOS/EOS=63 tokens fits
64slots. Verify every prefix byte,BOS/EOS,padding and absence of truncation. No Japanese removal.
TRAIN-value evaluation at length6 is still an untrained input length,not six-character training.

## Sequence,accounting and controls

Each state:old2..5 BEFORE -> new6 -> old2..5 AFTER. All views/profiles/splits are included.
Original before/after logits must match that same C312 state's saved raw outputs within1e-9
absolute drift and exact argmax,with original per-length full-gate flags unchanged. Exact full
state fingerprint and all hook registries remain unchanged after each pass. No new hooks are
installed by the child;the inherited reader's temporary hooks must still clean themselves up.

Per state:108+27+108=243 forwards,23328 presented rows,972 core calls. Ten states:2430 forwards,
233280 rows,9720 core calls. Ten strict state loads,one existing checkpoint-bundle read;
training0,new checkpoint writes0,network0. The new evaluation tensor archive is not a checkpoint.
Raw float64 logit payload477757440 bytes before metadata/serialization;not peak-memory accounting.
Operational probes and inherited regression/recursive checks are separate costs. Probe both arms
on one English and one Japanese old/new input;two states*three forwards=6 discarded smoke calls.
Do not infer scientific results from the smoke or choose conditions using its predictions.

## Parent contract and protected sources

C312 scientific execution:f481ae2b547bccc5cd5f43ae2654f89e8fa3140f.
Publication:16e55cffe274ac24a456cb28b650fca3140d8789.
Summary:runs/c312-v5b-value-batches-c23759c73f5c4bfbb03a7c3d9c8e8198/summary.json.
SHA256:2bb0efc9a9f128a0aeda9585dabab4ee0c672ba2e9b31f4b148cc6ba959a5ed6.
Source blob:a676b684d605424c35713ac08940e06ab16553f4.
C304 renderer/scorer blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify39 ordered summary hashes BEFORE exact C312.verify_artifacts with38 ancestors and accepted
execution HEAD. The summary seals all7 artifacts. Require acceptedFAIL,complete original ten
flags,all_pairs_matched and all_replays. Read only verified dataset.json/length-datasets.json
and fold-c312-value-batches-eval-v1 final logits. Check their original hashes and all prompt
identities. The actual parent model loader reads fold-c312-value-batches-models-v1. No checkpoint
schema guessing,weight splicing or parent record used as a newly generated model prediction.

Sole direct repository import C312;its inspected context supplies C310 no-neural,C308 policy,
C304 model/prefix/evaluator/scorer/replayer,C287 normalizer and original backend. Keep all718
inherited source pins and1343 inputs,including C312.PINNED,C304.PINNED and actual repository-local
helper/factory-language module coverage. Add OWN6+8 parent files:source724/protected1357.
No accepted code/tests/preregistrations/logs/dispatchers or historical exclusions are changed.

## Gates,reports,persistence and limits

Existing thresholds:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Reuse C304.score_length;it adapts profile names to C270,which scores logical rows independently
of identifier length. Do not call the old four-length cohort analyzer with a new six key.
Report10 six capability flags,20 split partitions,20 original-five-to-six transition groups,
10 baseline-reproduction receipts,and separate six pass counts for each arm. Transitions show
both correct,new error,recovered,both wrong and same wrong on exactly aligned logical rows.

PASS means all5 prospective random baseline models pass six after integrity checks;FAIL with
valid execution is ACCEPTED VALID NEGATIVE. An integrity failure is INVALID / RETRY SAME C313.
A positive outcome is limited to these same models,value split and three synthetic name
families. It is not a fresh-seed replication,arbitrary-length proof,or general model competence.
The five-character results were already observed;the prospective six condition is fixed here.
C312 negative,C308 bounded PASS,C309 negative and Gate F remain unchanged.

Five artifacts:evaluation-plan.json,six-dataset.json,evaluations.pt,measurements.json,
validation-summary.json plus summary.json. Archive fold-c313-six-transfer-eval-v1 stores original
before/new6/originalafter logits for every state;all arrays remain local/ignored. Hash/size and
no-neural numerical reconstruction of scores,controls,prompts and transitions are mandatory.
Own32/modules198/loaded5030/focused5029;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:f6e02599e4704457781f1ac49272a0a8d50d9c40524d66d4bcfb173e1cf86cca.
Commit/refetch/review all6 OWN before activation. Windows Validate requires39 actual parents,
724/1357 protection,render/frame checks,real frozen two-arm bilingual smoke,own32,full5029
regression and dispatcher/launcher/runner ParseFile. Validate failure skips science/publication.
C314 waits for formal C313 judgment;do not retune models,gates,cohort or length after results.
