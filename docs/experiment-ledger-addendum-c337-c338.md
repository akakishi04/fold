# C337 acceptance and C338 authoring boundary

Date: 2026-10-25 Japan time.
C337 ACCEPTED PASS (DIAGNOSTIC INTEGRITY).
C335 remains ACCEPTED VALID NEGATIVE; Gate F NOT PASSED.
C338 is not registered by this acceptance commit. No ACTIVE during authoring.

## Evidence identity and validity

Execution: aae0a83742d56df9dcfe059f3b6ad81e26798505.
Console publication: 38b129ee5569b288c52539eb31caa0853381f2e5.
The publication's sole parent is the execution commit.
Publisher reports 695809 original Windows bytes and SHA256:
e36c2ef9418fca92abe343b931671cef1c5a9a410c2259296b02a63f38fe3831.
Log blob: 4ca447ba0446dafcbc66f897a6a5931c365934c4.
Metadata blob: f4b9bb10b7d25b4b1b36d05c643736f79e62a041.

6122 tests / 227 sequential isolated modules passed; failures/errors/skips 0.
Regression elapsed 1995.526 seconds, including process orchestration.
Ordered full test-ID SHA256:
3f5e74b88652cf88f37150b087d52ef6f6086138f9b05ccafc4674893d84d6ca.
Native locks, immediate-parent reconstruction, 883 source / 4827 input protection,
all 4827 final uncached rereads, saved output reconstruction and independent fresh
verification succeeded. Science/verify exited 0; run_execution_valid=true.
Persisted audit: 10 states, 51840 answers, 12960 source quads, 720 strata;
scientific inference/updates 0. Parent candidate_gate=false, eligible_seed_count=1.

Local folder: runs/c337-value-support-bca3d06eebf74f74a1b1038c5cb38627/.
Primary science/summary.json SHA256:
415784b8d7d468a6d3f102775e29ae887fcb01ebc5718abef35dc9439fd6a0b8.
Mandatory execution-envelope.json SHA256:
12df1d44c5973f9bb5ac7bd2ce766b4bf1fb5204bb3d064c44d6a9f09c7b237e.
Scientific manifest SHA256:
4233762c9dd30360f0173e22e1db6ec697c1d7cafd479fc3ce6c3bad0ca81d26.
A successor inherits all 883 sources/4827 inputs plus ALL 463 parent outputs:
4 scientific files + primary + envelope + 457 regression proofs (3+227*2).

## Deciding observations, explicitly limited to seed335002 HOLDOUT

Each row sums all 3 profiles x 2 languages = 288 answers. These are repeated
controlled variants, not independent tasks. Counts were summed independently from
the 24 published strata (log lines2767..2772,2779..2784,2839..2844,2851..2856).

|Domain|Arm|Correct|Other supplied value|Absent0..3 value|Outside catalog|Target higher within pair among absent winners|Other higher among absent winners|
|---|---|---:|---:|---:|---:|---:|---:|
|original2|native|161|9|118|0|71|47|
|original2|alternating|126|28|134|0|74|60|
|interior4|native|121|68|99|0|52|47|
|interior4|alternating|97|57|134|0|61|73|

All corresponding within-pair and support ties are 0. Every outside-pair winner in
these four aggregates is a digit0..3 absent from that problem, not outside_catalog.
Do not extrapolate this inspected subset to all720strata without a full aggregation.

Some wrong answers put the correct supplied value above its supplied alternative,
but below an absent value. Other wrong answers also reverse the supplied-value
ranking. Thus candidate restriction would not remove all errors even as an offline
oracle-assisted calculation. We did not repair predictions, deploy such a filter,
claim an accuracy gain, or establish a neural mechanism/optimization cause.
C337's PASS is integrity; C335's capability verdict is unchanged.

## Review scope

Exact-ref metadata, commit lineage, registered source contract, full-regression
completion, terminal 4827 rereads/fresh verification and deciding strata were read.
The reviewer did not independently rehash the original whole Windows console,
read all local module proof files, replay a model, or audit all720strata. Completion
of those native integrity checks is reported by the preserved executor/verifier.
Old attached C323/C324 logs are not current evidence.

## Next bounded question, not execution authorization

Consider a fresh paired fixed-budget native-readout experiment comparing ordinary
256-class cross entropy with the same loss plus a fixed supplied-value support
penalty. The support penalty is -log of the probability mass on BOTH values present
in the TRAIN example; it does not reveal which is queried and is not used in
inference. All 256 classes remain in raw evaluation. No alternating readout, extra
model parameters, old checkpoint reuse, failed-seed removal or candidate filter.
This is a hypothesis, not a demonstrated remedy; within-pair errors may persist.
Finish source/tests/preregistration, committed-byte review and activation separately
before supplying a C338 command. Do not mutate accepted sources or start paid/CI work.
