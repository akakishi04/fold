# C298 formal acceptance — component-initialization diagnostic

C298 ACCEPTED PASS (diagnostic integrity only). C297 remains diagnostic ACCEPTED PASS.
C296 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C299 NOT REGISTERED in this commit.

## Evidence identity and validity

Scientific execution HEAD:026dc1983cbdf7c54e6bb6ba6302f04430b17a36.
Published log commit:5113666bdb581526cdc0f2707e493258accbc028.
Metadata log SHA256:52e131f27922ab2ae51c0fd3c9e7bce8f9a42224536a270c90acc60b3af2d90e;724286 bytes.
Publication changes only docs/experiment-run-logs/c298/latest.json and latest.log.
Summary:runs/c298-v5b-components-13bf02bea0764e2cb8fe8802cfa52eb7/summary.json.
Summary SHA256:a57e5f2fc3071c630b6cd083f855511b035a4d8478c91e22f86fe97c373add6e.
Manifest:e89e471d5f6e50e028136cf667b7a20f797c444f63b2638c3e29f11736c9cb62.
Authoritative log:own32/focused4525 PASS;full regression306.686s;source634/protected1161.
All9 training cells and original scoring/strict replay completed. Saved reconstruction PASS;
components_matched=True;tracked tree clean;execution HEAD preserved;run_execution_valid=True.
All three diagonal controls reproduce C297 order297101,with exact initialization/final fingerprints,
all800 CE values and schedules;reported maximum all-view logit error0.0 for every diagonal.
No C298 rerun or altered threshold is justified.

## Deciding observations

Rows=backbone297001/297002/297003;columns=reader297001/297002/297003.
Quad full gates:[[true,true,true],[false,false,false],[true,true,true]].
Two-character and three-character full gates:all9 pass. All seen-length normal TRAIN/HOLDOUT
answers are correct. The six cells using backbone297001 or297003 also answer all864 normal
quad inputs correctly and pass all original masked/full criteria.

For backbone297002,the three reader choices give quad TRAIN/HOLDOUT correct counts:
reader297001:576/576 and286/288 (2 total errors);
reader297002:566/576 and280/288 (18 total errors);
reader297003:567/576 and283/288 (14 total errors).
Thus full-gate outcomes follow the backbone factor in this grid,but reader initialization still
changes error severity. The failed diagonal is not fixed by either other reader level.

## Interpretation boundary

This is targeted evidence about the same three initialized component sets at one fixed order,
not an independent fresh-seed replication or a universal initial-state rule. It narrows the next
component investigation but does not establish that the reader is irrelevant or that the entire
backbone is faulty. All parameters train jointly;backbone encompasses multiple mechanisms.
Earlier seen-length TRAIN failures were not reproduced here. No best-cell deployment or Gate F
promotion. Normal pooled accuracy does not replace local fixed gates.

A next separately preregistered comparison can split the initialized backbone into its recurrent
core and its complement,keeping the added reader and order fixed. Preserve all three factor levels
and reproduce every same-backbone diagonal from C298,including the failed case. Do not choose
only the best donor or continue learned checkpoints. C299 requires its own review before activation.
