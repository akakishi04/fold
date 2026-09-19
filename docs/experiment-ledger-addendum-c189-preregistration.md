# C189 preregistration — live learned multi-missing target acquisition

V5-E; repository `akakishi04/fold`; branch `feat/sft-target-loss`.

Registered only after C188 acceptance commit
`2edadff6f8fab1c3c26da46adee630d12e433be8`.

**C188 ACCEPTED PASS. C189 ACTIVE / NOT YET JUDGED. C190 NOT REGISTERED.**
Gate E remains **NOT PASSED**. Earlier judgments and checkpoints remain fixed.

## One scientific question

Can the accepted frozen C181 necessity representation plus a frozen accepted C188 target
selector, sharing one initial neural forward, choose an influential fact in a multi-missing
state, drive exactly one real C172/C173 `RETRIEVE` of that learned selected external fact,
and then correctly reclassify the actual updated state?

C188 proved only offline WHICH-fact selection. C189 changes only the boundary from
offline selection to one real bounded acquisition and one post-acquisition necessity
decision. It does not introduce new training, retry, tool choice, answer generation or
proof generation.

## Fixed candidate set

Reuse all nine accepted C188 combinations:

Base seeds:
`181001`, `181002`, `181003`

Target-head seeds:
`188001`, `188002`, `188003`

Base arm:
`INTERNAL_SEMANTICS`

No C181 or C188 weights are updated. No new seed is introduced.

Parent C188:
- execution HEAD `683d795b12d4f0aada4850dcac2a010e699882ad`
- summary SHA256 `2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153`

## Cohort

Use the same C174 PILOT development family and all **1768 NEEDS rows with 2 or 3
unobserved facts**:

- missing2: 1152
- missing3: 616

The original C188 discriminating target-choice subset of **528 rows** remains separately
reported and is still required to have zero target errors.

This is the same repeatedly inspected four-group development split. It is not an
independent confirmation set.

## Initial learned decision

Each episode starts from the original C174 local fact layout. C189 deliberately does
**not** add another fact-renaming intervention; C184/C185 already tested that engineering
boundary and another rename would confound first live target integration.

The trusted scheduler charges one internal decision before encoding:

`12 internal / 4 acquisitions / step7`
→ `11 internal / 4 acquisitions / step8`.

One frozen C181 TREE_LINKS forward is executed. From that same forward:

1. the original C181 readout emits `SUFFICIENT` vs `NEEDS`;
2. all seven shared-cell hidden states are captured;
3. the paired frozen C188 target head scores the four local fact candidates;
4. already observed facts are masked using observable presence only;
5. raw argmax selects the target.

Thus target selection does **not** pay for or invoke a duplicate C181 base forward.

The C188 target feature path is resource-independent by construction: it uses the seven
cell states plus leaf-position one-hot, while runtime resource fields enter the separate
C181 final readout context. C189 nevertheless requires the live target logits to replay
the accepted C188 target logits within `atol=1e-6` and requires exact target argmax equality.

## Trusted endpoint binding

Before target selection every episode owns the exact current `RuntimeState` but no
RETRIEVE endpoint is bound.

After the learned local target is produced, trusted runtime scaffolding binds only the
matching external fact endpoint. Rebinding must preserve the exact `RuntimeState`;
it does not inspect a target teacher, expected label or hidden completion.

The source files are the same bounded C185-format single-fact fixtures, one per external
fact and bit value. There are exactly eight registered sources.

The learned selected target is passed unchanged to C172:
`action.propose(..., "RETRIEVE", fact_index=<raw learned target>)`.

C172 reserves at most one acquisition; C173 performs at most one actual file read and
may publish only that selected fact. The other still-missing facts and their opaque
bindings must remain unchanged.

## Completion bits

Cross every selector with both selected-fact values:

`0` and `1`.

The source bit is not a policy feature. It is observed only if the real registered
provider path succeeds.

Total formal live episodes:

`9 selectors × 2 bits × 1768 rows = 31824 episodes`

Formal blocks: **18**.

## Post-acquisition decision

After one successful admission, the trusted scheduler charges one further necessity
decision. With the normal C172/C173 charges, the expected post input is:

`7 internal / 3 acquisitions / step12`.

The frozen C181 base performs one necessity-only decision on the actual current TaskView.

If the post state is still `NEEDS`, the diagnostic stops unresolved.
**No second target is executed and no second acquisition is permitted in C189.**

If the post state is `SUFFICIENT`, that is only a classification. C189 does not emit
an answer or proof.

## Scoring teachers

Two programmed teachers are scoring-only:

1. **initial target teacher** — the exact C188 influential-target set;
2. **post necessity teacher** — C174 logical necessity computed from the actual final
   visible facts after admission.

Neither teacher is passed to the policy, target head, C172 proposal, endpoint selection
or provider.

## Parent replay

Before live execution C189 must restore the 3 accepted C181 bases and 9 accepted C188
heads and replay the accepted C188 full-multi-missing target predictions:

- rows: `9 × 1768 = 15912`
- exact target argmax equality
- max absolute finite unknown-target logit delta `<= 1e-6`

Failure is execution invalidity, not a scientific negative.

## Fixed deciding gate

For **each of all 18 selector × source-bit blocks**:

- episodes = 1768
- discriminating target rows = 528
- initial C181 necessity errors = 0
- target errors over all1768 = 0
- target errors over discriminating528 = 0
- target replay errors vs accepted C188 = 0
- selected observed facts = 0
- initial target logit delta vs C188 <= `1e-6`
- missed acquisitions = 0
- post necessity errors = 0
- acquisition/runtime contract errors = 0
- reservations = provider calls = publications = 1768
- decision charges = 3536
- total internal charged = 8840
- post SUFFICIENT + post NEEDS = 1768

All 18 blocks must pass. No averaging, head selection, rescue or teacher override.

A finite completed failure is **ACCEPTED VALID NEGATIVE**.
Source/hash/schema/parent replay/nonfinite/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C189**.

## Workload

Preregistered:

- C181 checkpoint loads: 3
- C188 target-head loads: 9
- new training: 0
- fresh seeds: 0
- static target replay rows: 15912
- static base feature rows: 5304
- static base forwards/cell calls: 6/42
- live initial base rows: 31824
- live target rows: 31824
- live post base rows: measured 0..31824
- total base rows maximum: 68952
- ideal actual file reads/publications: 31824
- max acquisitions/episode: 1
- network calls: 0
- core EvidenceState writes: 0
- answer generation: 0
- proof checker calls: 0
- production runtime modified: False
- Gate E candidate: False

## Registered sources / outputs

Eight single-fact source hashes are frozen in the benchmark manifest. C189 writes exactly
13 artifacts excluding `summary.json`:

- `live-target-plan.json`
- `selector-replay.json`
- `episode-results.json`
- `episode-traces.jsonl.gz`
- `episode-predictions.npz`
- `sources/fact-0-completion-0.json`
- `sources/fact-1-completion-0.json`
- `sources/fact-2-completion-0.json`
- `sources/fact-3-completion-0.json`
- `sources/fact-0-completion-1.json`
- `sources/fact-1-completion-1.json`
- `sources/fact-2-completion-1.json`
- `sources/fact-3-completion-1.json`

Historical source pins expected: **107**.
Protected paths expected: **258**.

Scientific manifest SHA256:
`e1ba8c1b84dc016410e91432eadfc53e28a46dd49cb91bf015d3336f37e8402e`.

## Interpretation boundary

PASS supports only:

> In the registered four-fact development family, the accepted learned necessity/target
> components can be connected to the actual bounded C172/C173 acquisition path so that
> the raw learned selected fact is really read and admitted once, and the frozen
> necessity model correctly classifies the resulting actual state.

PASS does not establish:
- iterative multi-step acquisition planning;
- learned retry/stopping;
- learned tool/provider choice;
- target optimality beyond C188's influential-fact definition;
- fact renaming invariance in this C number;
- natural language, repeated variables or larger expressions;
- answers/proofs;
- independent final confirmation;
- production adoption or Gate E completion.

## Implementation validation before formal run

The exact new benchmark and test sources are syntax-compiled by the reviewer.
Pure manifest/gate replay checks were executed locally. The environment available to the
reviewer does not contain a complete repository checkout or GitHub DNS, so C172/C173
integration tests and the full historical regression cannot be run independently here.

Formal expected regression:
**1449 = 1413 existing + 36 new; 74 modules.**

Run only `tools/run_c189.ps1` with C188/C187/C186/C185/C184/C183/C182/C181/C180/C179/
C178/C177/C176/C174 summaries and the exact registered HEAD.

Do not register or execute C190 until C189 is judged and ledger/handoff is updated.


## Execution-recovery note

The first two C189 attempts were execution-invalid before regression/model work.
The second attempt showed that the valid UTF-8 source's scientific manifest serializes to
SHA256 `e1ba8c1b84dc016410e91432eadfc53e28a46dd49cb91bf015d3336f37e8402e`.
The previously written manifest hash was a transcription/serialization error. The manifest
object, seeds, checkpoints, cohort, workload, gate, thresholds and interpretation are unchanged.
This SHA correction is execution-recovery metadata only and does not alter the preregistered
scientific conditions.
