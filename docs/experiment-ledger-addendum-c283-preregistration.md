# C283 preregistration — frozen four-character transfer

Experiment:C283-v5b-frozen-four-character-transfer.
Stage:V5-B-FROZEN-FOUR-CHARACTER-TRANSFER.
Acceptance base:b597180933fcc464395ad62cc0e915e01c796871.
C282 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C284 NOT REGISTERED.

## One question

Do frozen C282 mixed_length states transfer better to completely untrained four-character
identifiers than their matched two_char_only states, without further training or seed selection?
This compares learned coverage regimes, not architectures. Both arms retain the actual C278
MeanFinalDualReadout, all-token support,14256 parameters and48-token context.

## Frozen provenance

C282 execution:aef5aecfc438679641e59b337d7a9eb615c619a3.
Published log:b8c0462a27246cf6ff9d9024b614dbca244be2b1.
Summary:runs/c282-v5b-mixed-length-5ad726e62dfa4eacada5a8cda8c4c27f/summary.json.
Summary SHA256:075cb7399f62d048310bdfb1c31c93ac39ab8b3dc400578d60e062ebfdacf3d1.
Direct parent source blob:fdf35a6c0c18e0c0da4b1f592cef73be156de481.
Nine ordered summaries:C282,C281,C280,C279,C278,C277,C276,C275,C274.
All nine SHA256 identities and all seven C282 artifact hashes/sizes are in the sealed manifest.
The full accepted artifact list is in docs/experiment-ledger-addendum-c282-c283.md.

C282.verify_artifacts(parent_dir,eight ancestor paths,execution_HEAD) is the exact parent loader.
Require parent FAIL,whole control0/candidate4,two_char4/4,triple0/4,all_pairs_matched and all_replays.
Read raw_two/raw_triple/final_sha256 from fold-c282-mixed-length-eval-v1;load the frozen states
through C282.load_bundle, schema fold-c282-mixed-length-models-v1. Never call C282.analyze on
C283 records. Parent reconstruction blocks neural calls,state loading and checkpoint writes.

## Dataset and unchanged scoring semantics

Retain all C282 seeds282001..282005 and arms two_char_only,mixed_length, including failed states.
The original192 TRAIN/96 HOLDOUT logical rows,targets,fact orders,English/Japanese and values remain.
TRAIN/HOLDOUT here describe value-assignment partitions inherited from C267;neither partition's
four-character prompts has ever been optimized by either arm. No new factual entity count is added.

Profiles:quadrupled (uuuu/vvvv),shared_prefix3 (uuuu/uuuv),shared_suffix3 (uuuu/vuuu).
All names have four Unicode characters. Use the same familiar byte alphabet,normal/evidence_blind/
query_blind views and punctuation. Require864 globally unique normal prompts,disjoint from original
two/three-character prompts. Maximum UTF-8 prompt length43 bytes;BOS/EOS fit within unchanged48.
No truncation,tokenizer change,position-table extension or altered model configuration is permitted.
Quad dataset SHA256:86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.

Scoring adapter maps quadrupled/shared_prefix3/shared_suffix3 to C270 scorer's
tripled/shared_prefix2/shared_suffix2 input keys,then relabels all returned cells/order cells/totals.
Only profile identifiers are adapted;logical rows,raw logits,thresholds and denominators are not.
The C270 scorer does not render names and depends only on these raw/logical records.
Runtime Validate tests its actual perfect-logit behavior and72 answer/36 order cells before science.
No target,entity,profile,split or name-length metadata enters model.forward.

## Frozen execution and fixed gate

For each of10 strict-loaded states:eval(),requires_grad_(False),verify parent fingerprint,
run original two+three task anchor,run novel four-character task,restore original two+three evaluation.
Compare anchors/restores with accepted C282 raw logits and argmax at tolerance1e-9.
All weights must remain identical. Integrity replay preserves known wrong answers;it does not require
old capability success and must not erase the failed mixed seed282001 or control seed282005.

Primary capability gate:all FIVE mixed_length states pass all four-character criteria on both
value splits/all profiles/languages/orders. Thresholds remain accuracy.90,query_pair.80,
evidence_drop.35,query_drop.35,two_order.80. Control cannot rescue or fail this candidate gate.
Report all10 per-seed gates and60 paired split/profile/language correct/collapse contrasts.
A partial improvement with fewer than5 candidate passes remains a valid negative of this gate.
Comparative benefit must be described separately;candidate PASS alone is not proof of superiority.
C282 remains ACCEPTED VALID NEGATIVE regardless of C283. Gate F remains NOT PASSED.

## Workload and artifacts

No training,optimizer steps,new checkpoint writes or network calls.
One existing ten-state checkpoint bundle load;10 strict model-state loads.
Per model:54 anchor+27 novel+54 restore=135 forwards,12960 row presentations,540 core calls.
Totals1350 forwards,129600 row presentations,5400 core calls. Novel normal rows864/model.
Raw logits payload265420800 bytes before archive overhead. This is evaluation output,not a checkpoint.
CPU float64,threads2,deterministic algorithms. Authoring/regression work is separate from science.

Outputs:transfer-plan.json,quad-dataset.json,eval-outputs.pt,measurements.json,validation-summary.json,
plus summary.json. Archive schema:fold-c283-four-character-eval-v1. Postcheck rescoring uses saved
logits with neural calls blocked;it must not perform extra hidden model evaluation.

## Protection and authoring

OWN6:source,test,runner,launcher,preregistration,design. Parent files remain immutable.
Source pins544;protected inputs964;inherited dependency-union59. Counts:538+6;950+8+6.
Child directly imports C282;all reachable C280/C278/C270/C267 and other helpers remain source-pinned
and protected through the inherited map. Own32;modules168;loaded3982;focused3981.
Sole inherited exact C204 exclusion unchanged. Build the actual suite and unique IDs at runtime.
New tests must not depend on mutable ACTIVE state;immutable preregistration seal/inventory is enough.
Manifest SHA256:e88244fe1acc677d629e3b0400dc4926be9b26560c05a782122ae1e5042213a4.

## Interpretation boundary and stop

A positive comparison supports transfer to this bounded four-character family,not arbitrary length,
arbitrary names or a general variable-length algorithm. Length diversity is confounded with larger
maximum training length and redistributed exposure;a later three-character-only control would be
needed to isolate diversity itself. Neither result proves/excludes all generalization mechanisms.

Commit all OWN6,fetch committed bytes and independently review before activation.
Validate(source/artifacts,real tokens/scorer,own32,focused3981) precedes scientific logging.
Operational failure skips science/publish;scientific integrity failure retries SAME C283.
Do not change profiles,seeds,thresholds or add training after seeing four-character results.
C284 NOT REGISTERED until C283 is judged.
