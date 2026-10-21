# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and Current response format(v2). Recovery of SAME C336.
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Runtime Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5;PowerShell7/ParseFile/active_v2.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C335 ACCEPTED VALID NEGATIVE. C336 ACTIVE / INVALID ATTEMPT RECOVERY. C337 NOT REGISTERED.**
C336 attempts01/02 INVALID EXECUTION. R2 source authored;committed-byte review PENDING.
Do not issue a retry command until review PASS. Do not rerun accepted C335.

## Latest evidence and operational skip

Attempt02 execution5029fbbad2209f462af8939c0e77f56a5a63be5e;
publication3ab32fc78d924914b07141d4a009de3c8e39fcbe;sole parent matches execution.
Archive docs/experiment-run-logs/c336/attempt-02/latest.*;attempt01 retained.
Native locks,capacity4360,parent validation,877/4360registration and6090tests/226modules
passed(1680.515s,0failures/errors/skips). Diagnosis then failed in logical_groups:
ValueError:logical row semantics. No complete diagnosis/final rereads/fresh verifier.
run_execution_valid=false. No scientific outcome;regression success is not acceptance.
User's later STALE_EXPECTED_HEAD with3b185a(C335) is a no-op,not another attempt.
Current3ab32f is a publication commit;never use it to bypass ExpectedHead.

## R2 schema repair and fixed scope

Read docs/c336-execution-recovery-r2.md and amended C336 preregistration.
Canonical inherited data use two distinct integers from0..3,not only0/1;targets48..51.
Change logical_groups/classify range guards accordingly,retain two-observed-value
categories/all256argmax and reject malformed values. Original incorrect preregistration
and R1 handoff archived under docs/handoff-history/c336-pre-r2-preregistration.md and
c336-pre-recovery-r2.md. No accepted source/data/output/gate change.
Same32IDs/6090tests/226modules/877sources/4360inputs;R1 lock fix unchanged.
Manifest e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af unchanged.
All10C335states/native+alternating,original2..6/interior4,TRAIN/HOLDOUT,en/ja,allprofiles.
12960quads/6480pairedquads/51840answers/720strata;no model forwards or training.
Full30C335contrast reconciliation,all parent proofs,locks,final rereads and fresh
reconstruction remain mandatory. New own tests use hash-exact canonical rows and
all12target pairs. Predicted logits/ancestor proof/semantic callbacks stay synthetic.

## Parent and invocation

C335folder runs/c335-alternating-training-7dd29eebabd64360b31b40985bd6fd40/.
PrimarySHA6624fc176f349f7688af45da55ac5855951e7094c824201b16fe127b92aa25c4.
EnvelopeSHA70f5102a454db4370533f8da2f765d2e4eac6ab29d0bb93f5f4cbe976b9b5ab0.
Immediate parent maps871/3893+461outputs+6own ->877/4360;no smaller-map fallback.
Standard active_v2 ->invoke_c336 ->run_c336;unchanged AST gates.
Complete requires persisted_query_order_patternsPASS,execution_envelope_verified,
run_execution_valid=true and publication. Technical failure stays SAME C336.
No automatic retry,C337,CI,paidservices,reinstall,artifact deletion or C335retraining.

## History and inherited compatibility seal

Prior R1 full handoff archived c336-pre-recovery-r2.md;both invalid attempts retained.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
