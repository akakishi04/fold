# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:explicit PowerShell7,ParseFile,tools/invoke_active_v2.ps1.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C326 ACCEPTED VALID NEGATIVE. C327 NOT REGISTERED.**
No ACTIVE during next-C authoring. Do not rerun C326 or earlier accepted experiments.
All earlier verdicts unchanged. C326 scientific FAIL is not an execution failure.

## Accepted C326 evidence

Report:docs/experiment-ledger-addendum-c326-c327.md.
Execution:dbef3dbc1566ff2c8c30405e9c8d207f5e79f460.
Publication:4b94198f36af10ee319cd00c5a908b95426d8464;parent matches execution.
Remote metadata150874bytes;SHA2561f40e1038fc5d68e44fd6aa3f48668ab81795c0ebae4b3350ca9d0ccb49abecf.
Reviewer checked phase/regression/paired/terminal receipts and re-summed all paired
counts;no independent whole-log hash,full-cell reconstruction or raw model replay.
Full5610tests/215modules PASS0failures/errors/skips;765.616seconds.
Ten complete fits/ten replays;814sources/1533inputs;all final1533rereads;
fresh envelope verification and run_execution_valid=true. Composite0/5.
Interior answers1005/1440 ->1316/1440;pairs375/720 ->611/720;all5pairs improve.
Original2..6 answers7048/7200 ->7015/7200;pairs3460/3600 ->3440/3600.
Candidate interior1/5,retention0/5;control0/5,0/5. No mechanism proof or Gate F.

Parent folder:runs/c326-mixing-bbd9cd8f43db45f18b2370f2c3337dfa/.
Primary summarySHA256:0dd7af1c69774f5d00b1ee654284c38731f4233b2b858aedcf1bf0aaa77656aa.
EnvelopeSHA256:d379e907d3d9668f47b9690cb097398005b6c0c6c349ac30082ac3590d7dc62a.
Both records/full814source/1533input union mandatory for successor.
Previous handoff:docs/handoff-history/c326-pre-acceptance.md.

## Authoring boundary

Candidate C327:fixed-final-checkpoint original4/interior4 gradient alignment,
matched TRAIN/profile/language,all10states,no training or optimizer steps.
Complete source/tests/registration/remote review/activation/launcher before issuing
the completed user response;do not stop at this design note. No C328 or new CI.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
