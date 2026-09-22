# C227 acceptance and C228 boundary

## Formal verdict

**C227 ACCEPTED PASS (measurement audit). Gate F NOT PASSED.**

Scientific execution HEAD: `1ada3a45be61e524cf09ff9fa7c6d56efcbf29ee`.
Published log commit: `5adea153611ebe4b6788526ab71fad5b6a0027a9`.
Log SHA256: `2fdc52f6f483830d85db0b0e1908d8d157067daab94142d8c0779c5248a2a24b`.
Summary SHA256: `4e2a5282f5923b80272afd6476bf2a5ff62a672825cee6d442b0bac4325f9b75`.
Local accepted summary:
`runs/c227-v5f-factor-reuse-8abdfa3dfbd141db94ce9afd0e4c171a/summary.json`.
Validation artifact SHA: `bbb5ffefd2a0aad3c5e332ba1f50e2a87e15463267129bf657512a044c198d05`.
Measurements SHA: `68234a510756ac5d80a5a1ee770a393ad8dce656a8c395ce8ca73be80b3eac16`.

## Execution validity

Published metadata matches the registered execution HEAD. The published log records2561 focused
tests in81.680s, OK; scientific_status PASS; all_quality_parity True; parent_exports_equal True;
factor_reuse_audit_gate True; protected inputs preserved; tracked tree clean; run_execution_valid
True. Acceptance relies on published evidence and recorded local artifact checks, not a reviewer
rerun of user-local artifacts.

## Deciding measurements

All four numerical dimensions retained exact C226 candidate/symbolic export inventories. All three
arms agreed on the required values and current state/provenance. The cached comparator made no
query-time refactorizations; its preparation retained the checked Cholesky boundary.

Descriptive three-trial query medians, in milliseconds:

| Numerical dimension | H1/H2 | Checked-factor reuse | H1/H2 / reuse |
|---|---:|---:|---:|
| 2 | 0.3373 | 0.0514 | 6.5623 |
| 16 | 0.4504 | 0.0999 | 4.5085 |
| 64 | 0.4641 | 0.0921 | 5.0391 |
| 256 | 0.5179 | 0.2249 | 2.3028 |

The256 H1/H2 time is also exactly recovered as224900ns times the recorded ratio2.302801244997777.
At n256, canonical exported bytes are280561 (H1/H2) versus552365 (cached comparator).
The additional dense cache factor/rhs storage is48/2176/33280/526336 bytes at n2/16/64/256.
This additional cached tensor storage is counted, not omitted. H1/H2 is smaller than this particular
full-factor-cache comparator, but remains larger than the original uncached stateful comparator.

## Interpretation

The C226 query-time crossover against repeated dense factorization did not survive this stronger
frozen-state comparator. **No query-speed advantage for the current H1/H2 path was measured.**
The fixed-state comparison shows a time/retention trade-off, not overall FOLD superiority or a
failure of memory semantics. Constant-port algebra alone does not guarantee low wall-clock latency.

The reference candidate still performs its registered small-system safety/solve work each query;
the comparator moves its full-system factorization to preparation. This explains why operation
amortization must be considered. It does not justify disabling candidate safety checks after seeing
results, nor prove all of the difference is uniquely attributable to a single operation.

Limitations: two live factors, fixed queries/states, rank2, three-trial timings, complete shared
bridge including unused capsule in the comparator, canonical noncompressed exports and reachable
data estimates rather than process peaks. Answer memoization and matrix-specialized solvers remain
uncompared. Do not claim broad speed/storage superiority, language performance or Gate F completion.

## C228 single next question

With the same initial C227 states, what are the update-plus-query costs when12 subsequent observed
beta replacements are interleaved with1/4/16 queries each?

These replacements change bias only, not the aggregate update matrix. The full-system comparator
must therefore be allowed to retain its checked factor and refresh only the right-hand side,
after explicitly verifying unchanged matrix contribution. Forcing a new factorization on every
replacement would be an artificially weak comparator.

Keep all four dimensions, original32-event prefix, two live factors and production code fixed.
Use the next12 events of the same deterministic ledger, verify state/provenance/value parity after
every update, report preparation/update/read costs separately, and count complete retained data.
No training, production optimization or revised acceptance threshold. Measurement PASS and favorable
performance remain different claims. C228 is NOT REGISTERED by this acceptance document alone.
