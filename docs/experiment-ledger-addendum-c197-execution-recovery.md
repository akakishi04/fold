# C197 execution recovery

## First invalid attempt — malformed generated Python newline

- execution HEAD: `675af144558c9528a8cde9e79d20a0c447736b72`
- published log commit: `938b316cad79fdbcf0ccb63738387a5a0acd0a63`
- log SHA256: `c4c3eeff5c2557bc102ec6ba47ddf0f83a274688e15a1e243b07f69da8a4710b`
- disposition: **INVALID EXECUTION / RETRY SAME C197**

Observed failure:

```text
SyntaxError: unexpected character after line continuation character
```

Two generated Python call sites contained the literal characters `\n` rather than a real
newline. Import failed during source/artifact precheck. Focused regression, model inference,
provider calls and episode blocks did not start.

Recovery:
- replace exactly those two literal `\n` call-site sequences with actual newlines;
- add `python -m py_compile` for the C197 benchmark and test module before precheck.

Unchanged scientific conditions:
- experiment ID/stage;
- accepted C196 parent and C194 allowed reference;
- ALLOWED and PROVIDER_FAILURE_AFTER_RESERVATION arms;
- budget13/cohort/9 frozen C181xC188 selectors/16 coherent worlds;
- provider-failure semantics and expected resource accounting;
- gate/workload/interpretation;
- manifest `7f7121c336e68dc58578e35f75b7c459986f5adbd2329344fc08514e468d58d2`.

C198 remains unregistered until C197 is formally judged.
