# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:explicit PowerShell7,ParseFile,tools/invoke_active_v2.ps1.
Accepted source/tests/log/contracts and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C327 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C328 NOT REGISTERED.**
No ACTIVE during authoring. C326 remains VALID NEGATIVE;earlier verdicts unchanged.
Do not rerun C327 or earlier accepted experiments.

## Latest accepted evidence

Report:docs/experiment-ledger-addendum-c327-c328.md.
Execution:847c924f50303d93ed4df7acec74b77209b7d261.
Publication:926113e7602f1ee36445cde9bbf90eab1539ace1;parent matches execution.
Published35743bytes;log SHA256
cbff015cbec04a51270a9b3410ede85391879e2bdbc2dc4ea34db2b203595cb5.
Full5658tests/216modules PASS,0failures/errors/skips;864.515seconds.
820sources/1549inputs;all10models/60pairs/240gradients;weights unchanged;
reverse/saved/final1549rereads/fresh envelope PASS;all exits0;run_execution_valid=true.
All40aggregates reviewed and counts independently summed;no whole-log rehash or
local tensor/model replay claimed. Pooled negative-dot18/25/19/16 of60 and joint
strict descent50/40/49/52 of60 for all/core/reader/other. Not finite AdamW behavior.
Parent:runs/c327-gradient-1cf048a0cd9449b6af6485a4802c46ca/.
Primary SHA256:c4a061e158a1bd617fb7638bb034b7aa3ef78da06b15062474ff986d1f347719.
Envelope SHA256:fb44749ce38e0b0909238c51c13bbb1eb95e1898369313fb34d95483a543e535.
Inherit all820source/1549input protections. Parent4outputs+summary+envelope=6files.
C326 data and checkpoint evidence remain pinned ancestor inputs.

## C328 authoring boundary

Candidate question:constant rates versus0.1rates after800updates,with fixed1200updates
and C326 batch4 exposure. Fresh paired seeds328001..328005/orders328101..328105;
identical first800weights/optimizer state;no optimizer reset or accepted global patch.
Read C308 optimizer source and C326 writer/curriculum semantics. Finish implementation,
registration,tests,committed-byte review and activation in SAME user response.
No C329,CI,package install,old artifact deletion,threshold relaxation or seed selection.

## History and compatibility

Previous full handoff:docs/handoff-history/c327-pre-acceptance.md.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
