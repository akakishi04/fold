# V5-B fixed CE training-budget comparison — C295

C294 shows both outside-support competition and within-fact ranking errors. Even oracle support
leaves33/288 quad HOLDOUT errors on C293's support_weighted seed293004. A constrained decoder alone
would not resolve those mistakes;the diagnostic also does not prove how its hidden states failed.

Rather than another auxiliary coefficient or decoder change,C295 measures a basic remaining
constraint:the repeated800-update budget. Use ordinary CE and extend to a predeclared1600 updates,
without changing model,data,optimizer state or original capability gates. This is an explicitly
higher-budget policy,not a claim of equal-cost architectural improvement or certain convergence.

A single uninterrupted trajectory provides the exact800-update counterfactual stopping state.
Copy weights at800,continue optimizer to1600,and evaluate both copies only after all training.
This avoids recomputing shared prefixes,prevents evaluation feedback into training,and preserves
all seeds and both snapshots. Persist full trajectories and independently replay saved states.

An improvement would justify investigation of fixed optimization budget as a practical limitation.
A miss would remain evidence against this particular extension policy;it would not prove a model
capacity impossibility. A mixed result must retain losses/regressions,not just rescued cases.
Oracle conditional metrics remain descriptions of stored outputs,not a new decoder or PASS gate.
