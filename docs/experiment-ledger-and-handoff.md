# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:explicit PowerShell7,ParseFile,tools/invoke_active_v2.ps1.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C325 ACCEPTED VALID NEGATIVE. C326 NOT REGISTERED.**
No ACTIVE experiment during next-C authoring. Do not rerun C325 or accepted C324.
All earlier verdicts unchanged. No source/tests/logs/gates were changed for acceptance.

## Latest accepted evidence

Report:docs/experiment-ledger-addendum-c325-c326.md.
Execution:f95895313da81634976d0ff2761efdd793888c2b.
Publication:c030498473daf1155bc5cba6e358f944ec8fce1a;parent matches execution.
Remote metadata:149964bytes;logSHA256 c54a2ec2d20bd94990fa0eac79dc14e98a5db83dc53a06299c809757fa72dfa5.
No independent whole-log rehash or local tensor replay claimed by reviewer.
All5546 tests PASS,0failures/errors/skips;10models/10replays;808sources/1517inputs;
final1517rereads;fresh envelope verification;all exits0;run_execution_valid=true.
Scientific FAIL;candidate gate0/5. Mixed interior0/5,retention1/5;control2/5,0/5.
Interior pooled answers1064/1440 ->827/1440,pairs472/720 ->288/720.
Original2..6 pooled answers5573/7200 ->6312/7200,pairs2439/3600 ->2920/3600.
No causal-mechanism/unseen-template/general-language/production claim.

Parent folder:runs/c325-mixed-name-26478978a92c42d2980095d76d6e4339/.
Primary summarySHA256:e3e9808fea616ecc27e2644f808553f16fb6a11203284bdea5c2cf63b32006e8.
EnvelopeSHA256:e40a7e93159cdf33b94b11e8ee8df197da66949d121dd52eb8c6036db99440b9.
Both records and all808source/1517input protections must be inherited.
Previous complete handoff:docs/handoff-history/c325-pre-acceptance.md.

## Next authoring boundary

C326 candidate:temporal mixing granularity with exactly matched per-pair/per-profile
family exposure. Fix whole-epoch control versus within-update mixed candidate,
logical order/labels/optimizer/architecture/budget;fresh paired seeds.
Complete implementation,additive tests,registration and committed-byte review BEFORE
activation/user command. Do not stop at this authoring-state handoff as a completed
user response. No C327,no CI,no package reinstall,no artifact deletion.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
