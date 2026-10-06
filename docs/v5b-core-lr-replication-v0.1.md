# V5-B core-LR replication — C309

C308 met its absolute five-character5/5 gate with coreLR0.0005 and noncoreLR0.005. The frozen
control also passed5/5,while ordinary training passed4/5. This does not establish slow-core
superiority to freezing or universal reliability. C306/C307 already showed cohort variability.

Repeat all three policies prospectively on one new5-seed paired cohort,without touching model,
ratio,budget,data or gates. Keep2/3/4 training and unseen5 evaluation. Fresh initialization/order
seeds test training stability on the same task,not new task coverage or external validation.
The primary gate uses only new candidates;report frozen/full controls and old/new cohorts separately.
Do not tune the ratio after this run,discard a failed seed or keep generating cohorts until PASS.

Child uses seed-independent accepted C308 optimizer/configuration/probe functions directly;new
cohort-sensitive code has independent state and never rewrites parent module globals. Software
reference tests bind new seed inputs only in isolated namespaces. Strict old-artifact verification,
initial-state matching,all final-state replays and unchanged core-freeze invariants remain required.
