# C181 preregistration — proper-subexpression supervision

V5-E. Registered AFTER C180 acceptance01253f5fd548c69f3db3e1b1c4fbc56b4017160a.
Repository akakishi04/fold; branch feat/sft-target-loss; use final registration HEAD.
**C181 ACTIVE / NOT YET JUDGED. C182 NOT REGISTERED. Gate E NOT PASSED.**
C180/C179/C178/C176 remain ACCEPTED VALID NEGATIVE. Other judgments stay unchanged.

## One scientific question

Does TRAIN-only supervision of proper internal subtree semantics improve necessity
classification over final-label-only training with the SAME neural inference path?

C180 masking of the final raw-fact bypass failed the fixed joint gate. Most decisions
were unchanged and score-order changes were small/nonuniform. The bypass alone is not
an established dominant explanation. Intermediate supervision remains a HYPOTHESIS,
not a conclusion from that negative. Do not claim capacity/update sufficiency:those
variables have not been isolated. Seven cell calls are not seven ancestors per tree path.

## Common substrate and one changed variable

Both new conditions use the original C179 SharedGraphProbe TREE_LINKS, original cell,
original DIRECT raw-fact readout, and original C178 bound-visible72 input. Neither the
negative C179tree/C178binding nor C180no-direct result is adopted as a proven improvement.
The C180 mask is NOT carried into either condition. No old weights are fine-tuned.

Attach the SAME Linear64->3 auxiliary head to both models. A temporary training-only
forward hook observes outputs from the seven ORIGINAL shared-cell applications, selects
exactly TWO proper internal binary nodes, and reads those learned hidden states.
No extra cell application, teacher forcing, state replacement or recomputed root occurs.
The main logits are numerically unchanged under fixed base weights. Inference calls
only the original base.forward; it NEVER calls the teacher or auxiliary head.

Changed variable:alpha in the TRAIN loss:

    mean main binary CE + alpha * mean proper-node three-class CE
    FINAL_ONLY:alpha=0
    INTERNAL_SEMANTICS:alpha=1

Auxiliary CE is averaged over the two nodes and the batch, not summed over nodes.
Ordinary unweighted class losses; no missing-count weighting, threshold fitting,
selection of checkpoints/seeds, wider base model or extra updates.
Both arms compute the same auxiliary forward/loss. At alpha0 its gradients are zero,
so its195parameters are not effectively trained; nominal parity is not effective parity.
The zero-alpha base update is tested against original graph.fit on a synthetic two-step
fixture. This check is not a replay of any historical trained checkpoint.

## Teacher boundary: three semantic classes, TRAIN only

Class0 KNOWN_ZERO:the proper subexpression is0 under every completion of missing facts.
Class1 KNOWN_ONE:it is1 under every such completion.
Class2 UNRESOLVED:both results remain possible from the current visible facts.

These are derived training targets, NOT newly observed facts or hidden payloads.
Use the unchanged C174 read-once family:four distinct facts each occur once;seven
connected postorder nodes;AND/OR and leaf-only negation. Observed0 stays distinct from
missing. All four fact-table statuses must be OBSERVED or UNOBSERVED. Reject repeated
facts, unsupported statuses, malformed links and nonzero hidden-value placeholders.
Read-once validation matters:independent three-valued propagation is not in general
complete for correlated repetitions such as A OR NOT A. No wider completeness claim.

The generator evaluates the SIX nonroot nodes from visible facts. Only the TWO proper
internal binary-node outputs become auxiliary labels. Leaves are used to compute these
labels but are NOT supervised targets. The root is NOT evaluated by this generator and
its label is not duplicated or reweighted. Changing only the root operator does not
change these proper-node targets. No additional target for which missing fact to acquire.

A single Boolean 'needs observation' bit is not the full intermediate target:known0
and known1 have different effects on a parent AND/OR. The three classes preserve that
semantic distinction while leaving the64dimensional learned state otherwise unconstrained.

Generate targets ONCE from the42444 TRAIN raw rows only, producing84888targets. No
PILOT subtree teachers or labels are generated. Freeze and hash target rows, node indices
and class order before training. Verify target node indices against the model's supplied
syntax. Teacher input has no main-label or hidden-assignment argument.
The handwritten teacher is acknowledged training supervision, not autonomous reasoning.

## Fixed data, training and work

Reuse original C174 NPZ and metadata, not newly regenerated training or pilot rows:
TRAIN36groups/524templates/42444rows;PILOT4groups/116templates/9396rows.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
The repeatedly inspected four pilot groups remain DEVELOPMENT, not an independent test.
Main training labels and auxiliary labels are restricted to TRAIN. A new seed is not a
new independent data split.

Seeds181001/181002/181003;two fresh paired models/seed,six total. Paired full initial
weights and row schedules.2000updates/model,batch256,uniform sampling with replacement,
private CPU RNG=seed+1000000. Adam lr.001,betas(.9,.999),eps1e-8,weight_decay0,
amsgradFalse,foreachFalse;CPUfloat32,two threads,deterministic algorithms.
No early stopping, adaptive alpha, additional warmup/curriculum or score-dependent choice.
All six FINAL checkpoints saved/restored BEFORE any main TRAIN or PILOT score.
Training progress logs sampled-batch main/auxiliary losses, not full-dataset convergence.

New schema c181-proper-internal-semantics-v1. Checkpoints bind seed,condition,alpha,
class order,proper-only/root-exclusion,representation,steps and weight fingerprint.
Base parameters25726 plus auxiliary195 =25921 stored independent parameters in EACH arm.
Inference evaluates25726base parameters; retained checkpoint still includes the195head
parameters. No claim that merely bypassing the head reduces serialized model size.

|Work|Registered total|
|---|---:|
|Fresh seeds / models|3 / 6|
|TRAIN teacher rows / proper-node targets|42444 / 84888|
|Teacher nonroot node evaluations|254664|
|Pilot / root / leaf supervision targets|0 / 0 / 0|
|Main training forwards / updates|12000|
|Training batch-cell calls|84000|
|Sampled main training rows|3072000|
|Auxiliary training forward calls|12000|
|Auxiliary target uses across both arms|6144000|
|Nonzero-alpha auxiliary target uses|3072000|
|Pilot / TRAIN main predictions|56376 / 254664|
|Inference batches / batch-cell calls|312 / 2184|
|Inference auxiliary / teacher calls|0 / 0|
|New / historical checkpoint loads|6 / 0|
|Acquisition / proof / evidence / network calls|0 / 0 / 0 / 0|

Dense forward MACs/row:main177596 in both arms;training auxiliary adds2*64*3=384,
so training forward177980 in both. Seven cell applications/row remain unchanged.
Forward-MAC accounting excludes backward,optimizer,teacher generation,hooks,gathers,
validation,nonlinearities and I/O. Actual fit/inference/end-to-end time is recorded;
no speed or memory benefit is claimed. Additional TRAIN supervision and its cost are real.

## Fixed deciding gate and interpretation

Same joint-gate form as C176/C178/C179/C180,now INTERNAL_SEMANTICS vs paired FINAL_ONLY.
For EACH seed,require ALL on main raw argmax outputs in reused PILOT_EVAL:
1. Equal mean BA within missing counts1,2,3 strictly improves.
2. Original four-semantic-group macro BA does not decline.
3. Count1 NEEDS recall strictly improves.
4. Count3 SUFFICIENT recall strictly improves.
5. Both aggregate class recalls strictly exceed0.5.

Ties fail1/3/4;only2allows equality. Allseeds;no seed-average rescue. Auxiliary loss is
not a substitute gate. Its lower TRAIN loss cannot compensate for weak main predictions.

PASS:supports the fixed added-supervision intervention,not a unique causal diagnosis of
credit assignment. Extra supervision can also alter representation/regularization/
optimization. It does not prove explicit internal symbolic semantics or general reasoning.
VALID NEGATIVE:valid finite complete execution misses ANY condition;preserve all models
and results. Do not change alpha/teacher/seed/checkpoint/steps/cases/thresholds under C181.
INVALID:source/hash/schema/nonfinite/missing-work/unpaired/protection/exception issue;
restore validity of the SAME C181 without altering scientific conditions. Preserve
invalid.json and completed fits;finite scientific FAIL exits0.
Neither outcome rewrites C180 or passes Gate E. No production runtime is modified.

## Same-batch diagnostics and protection

Save both splits' MAIN logits/predictions,by-group/by-count confusion,recalls,ordinary
accuracy,within-count and matched-visible AUC,and paired rescued/regressed errors.
Do not generate pilot auxiliary teachers just to add a diagnostic. Preserve raw main
outputs without solver correction. Pure count0/4 absent-class BA/AUC stay null.
Overlapping score pairs are not independent statistical samples.

Reuse C180.precheck across C179/C178/C177/C176/C174,then add the accepted C180 summary
and all ten artifacts. Those historical checkpoints are HASHED,never deserialized.
C180 summary9ad6eb52054388abda89d2eb8254b2ce278bfc983ae2a6375ab7d8327f91adf2;
execution snapshot074419e41b38ad756b2c29a50ea070d5ca60f2d3.
72historical source pins plus4own currentHEADfiles;135unique protected input paths.
Protected C37/composition fixture retain additional outer hashes. Standalone paths only.
Output in fresh UUIDdirectory:internal-semantics-plan.json,teacher-audit.json,
teacher-targets.npz,six checkpoints,pilot-predictions.json,training-predictions.npz,
complete summary.json. Eleven artifacts excluding summary. No historical file mutation.
Manifest SHA2561f1baf3f40018ab84eb69d1812cf0c04d9fae624ee50e705d3bc780e35d6d3f4.

## Review and execution limits

36/36 new helper tests passed with actual new module and locally transcribed fetched
C179 model/fit/predict definitions,NOT a full Git-blob-identical parent checkout.
Local network could not resolve github.com;no full checkout or private artifacts were
available. No full-dependency integration claim is made. The historical regression-list
unit test mocks its predecessor;the formal runner resolves the REAL full list.
Helper environment PyTorch2.10.0CPU/NumPy2.3.5. Synthetic fixtures only;fits2rows/2updates.
Independent completion enumeration checks teacher semantics across648synthetic visible
assignments,including both tree shapes and four negation patterns. Checks include proper
node/root exclusion,hidden-payload rejection,main-forward and zero-alpha-update parity,
auxiliary gradient routing,teacher/head absence at inference,hook cleanup,checkpoint
binding and strict gate. Original C174 data or any formal six-model scores were not run.
New Python module/tests compiled;three embedded runner Python blocks parsed.
Full1153tests,WindowsPowerShell,complete source/artifactchain and formal6fits UNEXECUTED.

**1153expected=1117+36,65modules**,one regression then one CPU paired batch.
Run tools/run_c181.ps1 -C180Summary ... -C179Summary ... -C178Summary ... -C177Summary ...
-C176Summary ... -C174Summary ... -ExpectedHead ... . Progress:precheck,regression,plan,
seed/arm500steps(main_loss/aux_loss),three pairedBA lines,RESULT/POSTCHECK.
Judge C181 -> ledger/handoff -> next design. **No C182 before judgment.**
