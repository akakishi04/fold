# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C287 ACCEPTED PASS (diagnostic integrity only). C288 NOT REGISTERED. C289 NOT REGISTERED.**
C287 scientific execution:037e8e3b214af97c5bfb3ad32a202b7cd7ee1d28.
C287 published log:621ecbf4f43f72b75f4915e3095cc0dd3044fe9b.
C286 remains ACCEPTED VALID NEGATIVE. No C287 rerun or seed filtering.
The user completed the run;previous chat claims of execution pending were erroneous.

## Latest accepted science — C287

Acceptance:docs/experiment-ledger-addendum-c287-c288.md.
Summary:runs/c287-v5b-fit-partition-fb83191e6dd74d3f840c59f9a5282069/summary.json.
Summary SHA256:69fb8b4f8eb4affe1ff340a7b3faf2b301389cc648afed7becf486dab6fce54d.
Manifest SHA256:98e5768640301fd36d00706305809bd5b4707eb10458bee5abfaef478b1bf430.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;capability_gate_applicable=False.
Own32/focused4117 PASS;source568/protected1016;all scientific neural/training/state-load/write counts0.

First direct failures:fitted_train4,seen_length_holdout0,quad1,none5.
Both arms286002/286003 already fail optimized normal TRAIN and also fail HOLDOUT/quad.
constant_lr286005 passes both seen-length splits and fails only quad;other5 states pass direct gates.
Cosine tail286002 reduces two/TRAIN correct515->399 and triple/TRAIN515->397 out of576 each.
All seeds stay in scope. Normal TRAIN fitting errors are observed;their causal mechanism is not proven.

## Next question pending preregistration

A supervised query-pair assignment loss at fixed constant LR,mixed coverage,architecture and800
updates is proposed to target fitted-query collapse without extra examples/forwards. It must be
separately preregistered and independently reviewed before an execution command is issued.
C288 has no scientific result and is not yet ACTIVE in this acceptance commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Later lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoffs are preserved under docs/handoff-history/c280-pre-acceptance.md through
c287-pre-acceptance.md. The latest preserves Git blob759e7820e365de915f8cc903e7f9b24b70c61668.
Only this Formal state is authoritative;old ACTIVE instructions are historical.
Accepted source/tests,preregistrations,logs and protected dispatchers remain unchanged.
