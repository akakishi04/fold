# V5-B core initialization grid — C299

C298 retained the same row-shaped quad gate pattern after replacing the added reader's untrained
parameters. Its failed backbone still varied from2 to18 to14 errors with the reader,so the reader
cannot be called irrelevant. The next bounded localization splits the backbone itself.

Core means the existing3328-parameter recurrent state-update module. Remaining backbone10160
includes input processing and output components. Fix the added reader768 at the first registered
seed297001,and fix order297101. Cross all three original core and remaining-backbone seeds.
The architecture is identical;this does not remove or freeze the core. All weights train anew.
Same-source diagonals must reproduce C298's fixed-reader column including its failed middle cell.

This comparison can show component-initialization-associated outcomes at these fixed levels.
It cannot establish a universal cause,core necessity,architectural superiority,or generalization
outside the tested task. A successful off-diagonal is not a deployed model. Keep every cell and
every original full/masked gate;diagnostic integrity PASS is not capability PASS.
