# Structured interface and runtime contracts — C168-C173

## Scientific subject

C168/C169 tested whether the existing interface exposed enough information for a learned necessity
decision. Their valid negatives motivated an explicit structured task interface, bounded result
contract, typed action runtime and bounded acquisition lifecycle.

## C168 — necessity-input observability
**ACCEPTED VALID NEGATIVE.**

The valid diagnostic showed an interface limitation: the existing task representation did not
provide the registered observability/readiness guarantees needed for the next learned necessity
stage. This did not invalidate C167's previously supported tasks.

## C169 — frozen interface-readiness batch
**ACCEPTED VALID NEGATIVE.**

All six diagnostic sections completed:
- 3 GAP sections
- 3 OBSERVED_BOUNDARY sections
- 0 finite-violation sections

The important result was `interface_ready=false`, not an execution fault.

## C170 — structured task input
**ACCEPTED PASS.**

Established a 72-wide structured numeric TaskView plus explicit binding identity. Key checks:
- 532 capture/consumer roundtrips
- 0 failed roundtrips
- 252 template roundtrips
- 256 distinct resource roundtrips
- malformed controls rejected

The design made task syntax, fact status and runtime resources explicit rather than relying on a
narrow legacy working-state projection.

## C171 — bounded derived-result contract
**ACCEPTED PASS.**

600 verifier calls across reference/malformed/unusable/rebound/resource/capacity/rule-scope groups
established an explicit boundary for derived/proved results. A verifier result is structured and
bounded; it is not simply a model logit treated as truth.

## C172 — typed action runtime
**ACCEPTED PASS.**

197 action-runtime cases, zero failed checks. The runtime owns internal-unit charging and
acquisition reservation. No actual provider/evidence write was needed for this boundary.

## C173 — bounded acquisition lifecycle
**ACCEPTED PASS.**

122 registered scenarios, zero failed checks. It connected typed actions to provider callbacks,
bounded reservations, source epochs and admission semantics.

## Durable conclusions

- The legacy interface was insufficient for the intended learned necessity work.
- Task semantics and runtime resources need explicit structured coordinates.
- Result verification, action authorization and acquisition lifecycle are distinct layers.
- Later learned experiments should consume this interface rather than smuggling teacher/runtime
  truth through side channels.

## Cleanup implication

C168/C169 should remain represented as **valid negatives** even if their diagnostic scripts are
archived. C170-C173 define contracts still used directly by C185+ and therefore their production
modules/tests are active dependencies, not cleanup targets.
