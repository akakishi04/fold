"""C185: frozen learned necessity -> one real acquisition -> live reclassification.

Diagnostic-only. Target selection (the sole unknown), RETRIEVE and file transport
are explicit hand-written scaffolding. No answer/proof generator, training, hidden
value in a policy input, retry, semantic fallback, or reset of live resource fields.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
import gzip
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import torch
from fold_lm.v05 import structured_task_input as task
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_acquisition_lifecycle as life

EXPERIMENT_ID = 'C185-v5e-learned-single-missing-acquisition'
STAGE = 'V5-E-LEARNED-SINGLE-MISSING-ACQUISITION'
BASE = '4d07e9e5190487fdcc9cb68f7204381e5ea5ab67'
PARENT_SHA = '7817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04'
SEEDS = (181001, 181002, 181003)
ARMS = ('FINAL_ONLY', 'INTERNAL_SEMANTICS')
RULES = ('MISSING_RULE', 'NEVER_QUERY')
LAYOUTS = ((0, 1, 2, 3), (3, 2, 1, 0))
PARENTS = ('c184', 'c183', 'c182', 'c181', 'c180', 'c179', 'c178', 'c177', 'c176', 'c174')
FACT_IDS = tuple('external-fact:' + hashlib.sha256(f'C185|{i}'.encode()).hexdigest()[:16] for i in range(4))
OWN = ('fold_lm/v05_benchmarks/gate_e_c185_single_missing_acquisition.py',
       'tests_lm/test_v05_c185_single_missing_acquisition.py', 'tools/run_c185.ps1',
       'docs/experiment-ledger-addendum-c185-preregistration.md')
OUTPUTS = {'acquisition-plan.json', 'frozen-replay.json', 'episode-results.json',
           'episode-traces.jsonl.gz', 'episode-predictions.npz'} | {
           f'sources/fact-{i}-completion-{v}.json' for i in range(4) for v in (0, 1)}
BATCH = 1024


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


@dataclass(frozen=True)
class BoundInput:
    packet: task.PolicyInput
    canonical_to_input: tuple[int, ...]
    source_sha256: str


def bind_views(views):
    """C184 numeric normalization PLUS matching C170 opaque binding relocation.

    External fact IDs/references are moved, never renamed. No truth or provider
    argument exists. Decode and inverse reconstruction guard the entire packet.
    """
    from fold_lm.v05_benchmarks import gate_e_c184_canonical_fact_indices as canon
    require(len(views) > 0, 'Nonempty current views required')
    packets = [task.encode(v) for v in views]
    require(all(task.decode(p) == v for p, v in zip(packets, views)), 'Invalid current view')
    raw = torch.tensor([p.features for p in packets], dtype=torch.int32)
    normalized, maps = canon.canonicalize(raw)
    require(torch.equal(canon.restore_input(normalized, maps), raw), 'Numeric inverse mismatch')
    result = []
    for v, p, row, mapping in zip(views, packets, normalized.tolist(), maps.tolist()):
        b = p.binding
        nb = task.Binding(b.request_id, b.scope_id,
            tuple(b.fact_ids[i] for i in mapping), tuple(b.reference_ids[i] for i in mapping))
        packet = task.PolicyInput(task.SCHEMA, tuple(row), nb)
        nv = task.decode(packet)
        inverse = [mapping.index(i) for i in range(4)]
        restored_binding = task.Binding(nb.request_id, nb.scope_id,
            tuple(nb.fact_ids[i] for i in inverse), tuple(nb.reference_ids[i] for i in inverse))
        require(restored_binding == b, 'Opaque binding inverse mismatch')
        require(nv.resources == v.resources and (nv.evidence_time, nv.revision) ==
                (v.evidence_time, v.revision), 'Live context changed')
        for old, new in zip(v.nodes, nv.nodes):
            if old.kind == 'FACT':
                require(v.facts[old.fact] == nv.facts[new.fact], 'External fact/reference association lost')
        result.append(BoundInput(packet, tuple(mapping), digest(asdict(v))))
    return normalized, result


def unique_target(view, bound):
    """Select the ONLY unknown, not the most informative fact. Never inspect an answer."""
    require(type(bound) is BoundInput and bound.source_sha256 == digest(asdict(view)),
            'Stale binding: rebuild from current state')
    mapping = bound.canonical_to_input
    require(len(mapping) == 4 and all(type(i) is int for i in mapping)
            and sorted(mapping) == list(range(4)), 'Invalid inverse map')
    nv = task.decode(bound.packet)
    require((nv.request_id, nv.scope_id) == (view.request_id, view.scope_id), 'Binding scope mismatch')
    indices = [i for i, f in enumerate(nv.facts) if f.status == 'UNOBSERVED']
    require(len(indices) == 1 and all(f.status in ('OBSERVED', 'UNOBSERVED') for f in nv.facts),
            'Exactly one unobserved fact required for target selection')
    ci = indices[0]; oi = mapping[ci]
    require(view.facts[oi] == nv.facts[ci] and view.facts[oi].status == 'UNOBSERVED',
            'Canonical target does not identify the current external fact')
    return ci, oi, view.facts[oi].fact_id


def charge_decision(owner):
    """Trusted scheduler debit, BEFORE encoding. Not a learned action or CPU-time unit."""
    s = owner.state; v = s.view; r = v.resources
    if (s.terminal is not None or s.pending is not None or r.internal_remaining < 1
            or r.internal_step >= task.MAX_INTEGER or s.transition >= task.MAX_INTEGER):
        return False
    owner.refresh(replace(v, resources=replace(r, internal_remaining=r.internal_remaining-1,
                                              internal_step=r.internal_step+1)))
    return True


def acquire_once(owner, bound):
    """Map back to original external identity; C172/C173 recheck authority and admission."""
    ci, oi, fid = unique_target(owner.state.view, bound)
    transition = owner.apply(action.propose(owner.state, 'RETRIEVE', fact_index=oi))
    dispatched = None
    if transition.result.status == 'PENDING':
        dispatched = owner.dispatch(transition.result.intent.intent_id)
    return dict(canonical_index=ci, input_index=oi, fact_id=fid,
                action=asdict(transition.result), dispatch=asdict(dispatched) if dispatched else None)


class RulePolicy:
    def __init__(self, name):
        require(name in RULES, 'Unregistered rule control')
        self.name = name

    def __call__(self, raw):
        p = ((raw[:, 48:62:4] == 0).any(1).to(torch.int64).numpy()
             if self.name == RULES[0] else np.zeros(len(raw), dtype=np.int64))
        return p, None, dict(rows=0, forward_calls=0, cell_calls=0)


class FrozenPolicy:
    def __init__(self, model):
        self.model = model

    def __call__(self, raw):
        from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
        from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
        p, z, meter = graph.predict(self.model, binding.prepare_pair(raw)[1], batch=BATCH)
        return p.numpy(), z.numpy(), meter


def checked_predictions(policy, raw):
    before = raw.clone(); p, z, meter = policy(raw)
    p = np.asarray(p)
    require(p.shape == (len(raw),) and p.dtype.kind in 'iu' and set(np.unique(p)) <= {0, 1},
            'Finite raw binary policy decisions required')
    if z is None:
        require(type(policy) is RulePolicy, 'Only explicit rules may omit neural logits')
    else:
        z = np.asarray(z)
        require(z.shape == (len(raw), 2) and z.dtype == np.float32 and np.isfinite(z).all()
                and np.array_equal(p, z.argmax(1)), 'Invalid logits or repaired decisions')
    require(torch.equal(before, raw), 'Policy changed its input')
    require(all(type(meter[k]) is int and meter[k] >= 0 for k in ('rows', 'forward_calls', 'cell_calls')),
            'Invalid inference accounting')
    return p.astype(np.int8), z, meter


def run_block(views, endpoints, policy):
    """One independent episode per view; at most two decisions and ONE acquisition attempt.

    No expected-label, hidden completion, solver or fallback parameter. The model
    callback sees numeric current inputs ONLY. All actual states/bindings are retained.
    A final SUFFICIENT_CLASSIFICATION is not an ANSWER or a verified conclusion.
    """
    require(views and all(sum(f.status == 'UNOBSERVED' for f in v.facts) == 1 for v in views),
            'Initial cohort must have exactly one unobserved fact per view')
    bind_views(views)  # Validate before any IO or model call.
    owners = [life.AcquisitionOwner(action.RuntimeState(v),
        {'RETRIEVE': endpoints[next(f.fact_id for f in v.facts if f.status == 'UNOBSERVED')]},
        max_dispatches=1) for v in views]
    n = len(views); pred = np.full((n, 2), -1, dtype=np.int8)
    logits = np.zeros((n, 2, 2), dtype=np.float32); logit_present = np.zeros((n, 2), dtype=bool)
    inputs = np.zeros((n, 2, 72), dtype=np.int32); records = []
    meter = dict(rows=0, forward_calls=0, cell_calls=0)
    for v in views:
        records.append(dict(initial=asdict(task.encode(v)), phases=[], acquisition=None,
                            decision_charges=0, status='UNRESOLVED'))

    def decide(ids, phase):
        active = [i for i in ids if charge_decision(owners[i])]
        if not active:
            return [], []
        raw, bound = bind_views([owners[i].state.view for i in active])
        p, z, m = checked_predictions(policy, raw)
        for k in meter: meter[k] += m[k]
        for j, i in enumerate(active):
            pred[i, phase] = p[j]; inputs[i, phase] = raw[j].numpy()
            if z is not None:
                logits[i, phase] = z[j]; logit_present[i, phase] = True
            records[i]['decision_charges'] += 1
            records[i]['phases'].append(dict(phase=phase, packet=asdict(bound[j].packet),
                canonical_to_input=bound[j].canonical_to_input,
                source_sha256=bound[j].source_sha256, prediction=int(p[j])))
        return active, bound

    ids, bound = decide(list(range(n)), 0)
    post = []
    for i, b in zip(ids, bound):
        if pred[i, 0] == 0:
            records[i]['status'] = 'SUFFICIENT_CLASSIFICATION'
        else:
            records[i]['acquisition'] = acquire_once(owners[i], b)
            post.append(i)
    ids, _ = decide(post, 1)
    for i in ids:
        records[i]['status'] = 'SUFFICIENT_CLASSIFICATION' if pred[i, 1] == 0 else 'UNRESOLVED'
    for i, owner in enumerate(owners):
        records[i]['final'] = asdict(task.encode(owner.state.view))
        records[i]['receipts'] = [asdict(r) for r in owner.receipts]
        records[i]['pending'] = asdict(owner.state.pending) if owner.state.pending else None
        # Returning ends this diagnostic. No ANSWERED state or derived value is fabricated.
        records[i]['runtime_terminal'] = owner.state.terminal
    return records, dict(predictions=pred, logits=logits, logit_present=logit_present,
                         policy_inputs=inputs), meter


def assess(record, label, completion):
    """Scoring ONLY, after decisions. Does not repair actions or invoke a provider."""
    require(type(label) is int and label in (0, 1) and type(completion) is int and completion in (0, 1),
            'Exact scoring labels required')
    initial, final = record['initial'], record['final']
    x, f = initial['features'], final['features']
    missing = [i for i in range(4) if x[48+4*i] == 0]
    require(len(missing) == 1, 'Scoring initial domain changed')
    mi = missing[0]; fid = initial['binding']['fact_ids'][mi]
    phases = record['phases']; p0 = phases[0]['prediction'] if phases else -1
    post = phases[1]['prediction'] if len(phases) == 2 else -1
    a = record['acquisition']; d = a['dispatch'] if a else None
    reserved = a['action']['acquisition_reserved'] if a else 0
    calls = d['provider_calls'] if d else 0
    publications = d['fact_publications'] if d else 0
    charges = record['decision_charges'] + (a['action']['internal_charged'] if a else 0) + (d['internal_charged'] if d else 0)
    unchanged = all(f[i] == x[i] for i in range(72) if not (46+4*mi <= i < 50+4*mi or i >= 62))
    bindings = (final['binding']['request_id'] == initial['binding']['request_id']
        and final['binding']['scope_id'] == initial['binding']['scope_id']
        and final['binding']['fact_ids'] == initial['binding']['fact_ids']
        and all(final['binding']['reference_ids'][i] == initial['binding']['reference_ids'][i]
                for i in range(4) if i != mi))
    accounting = (f[62] == x[62]-charges and f[63] == x[63]-reserved and f[71] == x[71]+charges
                  and list(f[64:70]) == list(x[64:70]))
    receipts = record['receipts']
    receipt_ok = True
    if publications:
        receipt_ok = (len(receipts) == 1 and a['fact_id'] == fid and a['input_index'] == mi
            and receipts[0]['fact_id'] == fid and receipts[0]['request_id'] == initial['binding']['request_id']
            and receipts[0]['scope_id'] == initial['binding']['scope_id'] and receipts[0]['action'] == 'RETRIEVE'
            and receipts[0]['value'] == completion and list(f[46+4*mi:50+4*mi]) == [1,2,1,completion]
            and list(final['binding']['reference_ids'][mi]) == [receipts[0]['reference_id']])
    else:
        receipt_ok = not receipts and list(f[46:62]) == list(x[46:62]) and final['binding'] == initial['binding']
    needed_ok = (p0 == label and ((not a and not calls and not publications) if label == 0
        else (a is not None and reserved == calls == publications == 1 and post == 0
              and d['status'] == 'PUBLISHED')))
    structural_ok = unchanged and bindings and accounting and receipt_ok and record['pending'] is None
    return dict(failed=int(not (needed_ok and structural_ok)), initial_error=int(p0 != label),
        missed_acquisition=int(label == 1 and not publications),
        unnecessary_acquisition=int(label == 0 and calls > 0),
        post_error=int(publications > 0 and post != 0), contract_error=int(not structural_ok),
        action_attempts=int(a is not None), reservations=reserved, provider_calls=calls,
        publications=publications, decision_charges=record['decision_charges'], internal_charged=charges)


def gate(records):
    expected = [(s, a, li, bit) for s, a in [(s,a) for s in SEEDS for a in ARMS]+[(0,r) for r in RULES]
                for li in range(2) for bit in (0,1)]
    if [(r.get('seed'),r.get('arm'),r.get('layout'),r.get('completion')) for r in records] != expected:
        return False
    for r in records:
        if r.get('episodes') != 3712 or r.get('labels') != {'sufficient':2944,'needs':768}:
            return False
        if r.get('contract_error') != 0:
            return False
        if r['arm'] == ARMS[1] and any(r.get(k) != 0 for k in
                ('failed','initial_error','missed_acquisition','unnecessary_acquisition','post_error')):
            return False
        if r['arm'] == RULES[0] and (r.get('provider_calls') != 3712 or r.get('unnecessary_acquisition') != 2944):
            return False
        if r['arm'] == RULES[1] and (r.get('provider_calls') != 0 or r.get('missed_acquisition') != 768):
            return False
    return True


def fixture_bytes(fact_index, bit):
    require(type(fact_index) is int and 0 <= fact_index < 4 and type(bit) is int and bit in (0,1), 'Fixture identity')
    return blob(dict(schema=life.SOURCE_SCHEMA, provider_id=f'C185-fixture-{fact_index}-{bit}',
        evidence_time=1, revision=1, records=[dict(fact_id=FACT_IDS[fact_index], value=bit)]))


def make_views(raw, row_indices, layout, block_id):
    """Wrap supplied visible rows with opaque external bindings; no hidden completion."""
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    require(layout in LAYOUTS and len(raw) == len(row_indices), 'Registered aligned layout required')
    changed = frozen.rename_raw(raw, layout)
    ids = [None]*4
    for old, new in enumerate(layout): ids[new] = FACT_IDS[old]
    views = []
    for row, source_row in zip(changed.tolist(), row_indices):
        scope = f'C185-{block_id}-{int(source_row)}'
        refs = tuple((f'initial:{scope}:{ids[i]}',) if row[48+4*i] else () for i in range(4))
        packet = task.PolicyInput(task.SCHEMA, tuple(row), task.Binding(scope+'|query', scope, tuple(ids), refs))
        views.append(task.decode(packet))
    return views


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, parent_sha256=PARENT_SHA,
        source_execution_head=BASE, seeds=SEEDS, arms=ARMS, controls=RULES, layouts=LAYOUTS,
        changed='frozen necessity is now the sole acquisition trigger; real external-ID mapping, C172/C173 and live resources',
        cohort='all3712PILOT rows with exactly one unknown;768needs/2944sufficient;no label-based selection',
        completions=(0,1), policies=8, blocks=32, episodes=118784, model_episodes=89088,
        candidate_episodes=44544, baseline_episodes=29696, original_replay_rows=56376,
        checkpoint_loads=6, inference_batch=1024, max_decisions_per_episode=2, max_acquisition_attempts_per_episode=1,
        neural_initial_rows=89088, neural_post_rows='observed,0..89088', total_neural_rows_max=234552,
        ideal_candidate_acquisitions=9216, ideal_candidate_no_acquisitions=35328,
        initial_resources='unchanged C17412internal,4acquisitions,step7;decision debit1 BEFORE every input',
        normal_first_input='11internal,4acquisitions,step8', normal_post_input='7internal,3acquisitions,step12',
        source_files={f'sources/fact-{i}-completion-{v}.json':hashlib.sha256(fixture_bytes(i,v)).hexdigest()
                      for i in range(4) for v in (0,1)},
        target='handwritten sole unknown; inverse map to unchanged external fact_id', tool='RETRIEVE only',
        outputs=sorted(OUTPUTS), training=0, fresh_seeds=0, teacher_calls=0, auxiliary_calls=0,
        answer_generation=0, proof_calls=0, core_evidence_writes=0, network_calls=0,
        numeric='CPUfloat32,2threads,deterministic algorithms;raw argmax,no calibration',
        gate='all3candidates correct necessity/IO/redecision in all14848episodes each;all policies retain state/authority contracts',
        limits='reused development semantics;new live resource contexts;not independent generalization or full Gate E')


MANIFEST_SHA = '61563a16d40883db8f2f651e440ae4704d5ef8f36115aca28f9bade64d3d6385'


def precheck(c184_summary, c183_summary, c182_summary, c181_summary, c180_summary, c179_summary,
             c178_summary, c177_summary, c176_summary, c174_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c184_canonical_fact_indices as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    p181,p174,pins,protected = previous.precheck(c183_summary,c182_summary,c181_summary,c180_summary,
        c179_summary,c178_summary,c177_summary,c176_summary,c174_summary,root)
    require(audit.sha(c184_summary) == PARENT_SHA, 'Wrong C184 summary bytes')
    parent = audit.read_json(c184_summary); previous.validate_result(parent)
    require(parent['commit_sha'] == BASE and parent['status'] == 'PASS' and parent['source_blobs'] == pins,
            'Wrong accepted C184 source')
    protected[str(Path(c184_summary).resolve())] = PARENT_SHA
    for a in parent['artifacts']:
        f = audit.safe_child(Path(c184_summary).resolve().parent,a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],
                'Changed C184 artifact:'+a['file'])
        protected[str(f.resolve())] = a['sha256']
    pins = dict(pins)
    for name in previous.OWN: pins[name] = audit.git(root,'rev-parse',BASE+':'+name).decode().strip()
    allpins = dict(pins)
    for name in OWN: allpins[name] = audit.git(root,'rev-parse','HEAD:'+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins) == 88 and len(protected) == 182, 'Source/input union drift')
    require(digest(manifest()) == MANIFEST_SHA, 'Manifest drift')
    return p181,p174,pins,protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c184_canonical_fact_indices as previous
    names = previous.regression_modules(root)
    require(len(names) == len(set(names)) == 68, 'Historical regression list drift')
    return names+['tests_lm.test_v05_c185_single_missing_acquisition']


def validate_result(p):
    require(p['experiment_id'] == EXPERIMENT_ID and p['stage'] == STAGE
        and p['diagnostic_execution_valid'] is True and p['episodes'] == 118784
        and p['replay_rows'] == 56376 and p['neural_initial_rows'] == 89088
        and 0 <= p['neural_post_rows'] <= 89088
        and p['total_inference_rows'] == 56376+89088+p['neural_post_rows'], 'Identity/workload drift')
    require(p['inference_cell_calls'] == 7*p['inference_batches'] and p['checkpoint_loads'] == 6
        and len(p['source_blobs']) == 88 and len(p['input_sha256']) == 182
        and len(p['replay']) == 6 and len(p['artifacts']) == 13
        and {a['file'] for a in p['artifacts']} == OUTPUTS, 'Coverage/protection drift')
    require(all(p[k] == 0 for k in ('new_training','fresh_seeds','teacher_calls','auxiliary_forward_calls',
        'proof_checker_calls','answer_generation','core_evidence_writes','network_calls'))
        and p['production_runtime_modified'] is False and p['gate_e_candidate'] is False,'Scope drift')
    require(p['status'] == ('PASS' if gate(p['records']) else 'FAIL'), 'Fixed gate disagreement')


def run(*, output_dir, expected_head, **parents):
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    graph = frozen.graph; root = Path(__file__).resolve().parents[2]
    args = tuple(parents[n+'_summary'] for n in PARENTS)+(root,)
    def guard():
        require(audit.git(root,'rev-parse','HEAD').decode().strip() == expected_head, 'HEAD mismatch')
        require(audit.git(root,'branch','--show-current').decode().strip() == 'feat/sft-target-loss', 'Branch mismatch')
        require(not audit.git(root,'status','--porcelain','--untracked-files=no').strip(), 'Tracked tree dirty')
    guard(); p181,p174,pins,protected = precheck(*args)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    started = time.perf_counter(); artifacts=[]; records=[]; replay=[]
    def record(name):
        f = out/name; artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,value):
        (out/name).write_bytes(blob(value)); record(name)
    save('acquisition-plan.json',dict(manifest(),source_blobs=pins))
    try:
        print('[C185] plan fixed; frozen decisions drive real bounded RETRIEVE; no answer generator',flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data,_ = audit.load_data(Path(parents['c174_summary']).resolve().parent,p174)
        ev = data['split_codes'] == 1; pilot_indices = np.flatnonzero(ev)
        raw_ev = torch.from_numpy(data['features'][ev].copy())
        missing = (data['features'][:,48:62:4] == 0).sum(1)
        selected = ev & (missing == 1); indices = np.flatnonzero(selected)
        y = data['labels'][selected]; groups = data['groups'][selected]
        require(len(indices) == 3712 and int(y.sum()) == 768 and len(set(groups.tolist())) == 4, 'Cohort drift')
        raw = torch.from_numpy(data['features'][selected].copy()); rh = graph.tensor_sha(raw)
        require(torch.equal(raw[:,62:],torch.tensor([12,4,1,0,0,1,0,0,0,7],dtype=torch.int32).expand(len(raw),-1)),
                'Original C174 resource context drift')
        old = audit.read_json(Path(parents['c181_summary']).resolve().parent/'pilot-predictions.json')
        model_order = [(s,a) for s in SEEDS for a in ARMS]
        models=[]; identities=[]; fps=[]; meter=dict(rows=0,forward_calls=0,cell_calls=0)
        require(len(old) == 6 and len(p181['fit_records']) == 6, 'Checkpoint coverage drift')
        for i,(seed,arm) in enumerate(model_order):
            fit = p181['fit_records'][i]; saved=old[i]
            require((fit['seed'],fit['arm']) == (seed,arm) == (saved['seed'],saved['arm'])
                and np.array_equal(saved['row_indices'],pilot_indices), 'Frozen model/row identity drift')
            model = frozen.restore_bare(Path(parents['c181_summary']).resolve().parent/f'probe-{seed}-{arm}.pt',
                                       seed,arm,fit['final_sha256'])
            p,z,m = graph.predict(model,binding.prepare_pair(raw_ev)[1],batch=BATCH)
            replay.append(dict(seed=seed,arm=arm,**frozen.replay_check(p.numpy(),z.numpy(),saved['predictions'],saved['logits'])))
            for k in meter: meter[k] += m[k]
            models.append(model); fps.append(graph.fingerprint(model)); identities.append(p.numpy()[missing[ev] == 1])
        save('frozen-replay.json',replay)
        print('[C185] 1/3 all56376 original decisions replayed; 3712 one-missing source rows fixed',flush=True)
        providers = {}; endpoints = {}; (out/'sources').mkdir()
        for bit in (0,1):
            endpoints[bit] = {}
            for i,fid in enumerate(FACT_IDS):
                name = f'sources/fact-{i}-completion-{bit}.json'; b = fixture_bytes(i,bit)
                (out/name).write_bytes(b); record(name)
                sb = life.SourceBinding(f'C185-fixture-{i}-{bit}',hashlib.sha256(b).hexdigest())
                provider = life.FileSnapshotProvider(out/name,sb); providers[(i,bit)] = provider
                endpoints[bit][fid] = life.Endpoint(sb,provider)
        policies = [FrozenPolicy(m) for m in models]+[RulePolicy(r) for r in RULES]
        order = model_order+[(0,r) for r in RULES]
        dense = dict(predictions=np.full((8,2,2,3712,2),-1,dtype=np.int8),
            logits=np.zeros((8,2,2,3712,2,2),dtype=np.float32),
            logit_present=np.zeros((8,2,2,3712,2),dtype=bool),
            policy_inputs=np.zeros((8,2,2,3712,2,72),dtype=np.int32))
        episode_count=0; post_rows=0
        with gzip.open(out/'episode-traces.jsonl.gz','wt',encoding='utf-8',newline='\n') as trace:
            for pi,((seed,arm),policy) in enumerate(zip(order,policies)):
                for li,layout in enumerate(LAYOUTS):
                    for bit in (0,1):
                        views = make_views(raw,indices,layout,f'p{pi}-l{li}-c{bit}')
                        observed, arrays, m = run_block(views,endpoints[bit],policy)
                        for k in meter: meter[k] += m[k]
                        if pi < 6: post_rows += m['rows']-len(views)
                        for k in dense: dense[k][pi,li,bit] = arrays[k]
                        scores = [assess(r,int(label),bit) for r,label in zip(observed,y)]
                        totals = {k:sum(s[k] for s in scores) for k in scores[0]}
                        changes = int((arrays['predictions'][:,0] != identities[pi]).sum()) if pi < 6 else None
                        rec = dict(seed=seed,arm=arm,layout=li,completion=bit,episodes=len(views),
                            labels=dict(sufficient=2944,needs=768), initial_flips_from_original=changes,
                            by_group={str(g):{k:sum(scores[i][k] for i in np.flatnonzero(groups == g))
                                for k in scores[0]} for g in sorted(set(groups.tolist()))},**totals)
                        records.append(rec)
                        for j,r in enumerate(observed):
                            trace.write(json.dumps(dict(policy_index=pi,seed=seed,arm=arm,layout=li,completion=bit,
                                source_row=int(indices[j]),label=int(y[j]),score=scores[j],trace=r),
                                sort_keys=True,separators=(',',':'),allow_nan=False)+'\n')
                        episode_count += len(views)
                        print(f'[C185] block={len(records)}/32 arm={arm} seed={seed} layout={li} completion={bit} '
                              f'failed={totals["failed"]} provider_calls={totals["provider_calls"]}',flush=True)
        record('episode-traces.jsonl.gz')
        np.savez_compressed(out/'episode-predictions.npz',**dense,row_indices=indices.astype('<i4'),
            policy_seeds=np.asarray([s for s,a in order],dtype='<i4'),
            policy_names=np.asarray([a for s,a in order]),layouts=np.asarray(LAYOUTS,dtype=np.int8))
        record('episode-predictions.npz'); save('episode-results.json',records)
        print('[C185] 2/3 all118784 bounded episodes collected; no output or resource reset',flush=True)
        guard(); precheck(*args)
        require(graph.tensor_sha(raw) == rh and [graph.fingerprint(m) for m in models] == fps,'Frozen input/model changed')
        for f,h in protected.items(): require(audit.sha(f) == h,'Protected input changed:'+f)
        for a in artifacts: require(audit.sha(out/a['file']) == a['sha256'],'Output changed:'+a['file'])
        totals = {k:sum(r[k] for r in records) for k in scores[0]}
        provider_reads=sum(p.reads for p in providers.values()); provider_bytes=sum(p.bytes_read for p in providers.values())
        require(provider_reads == totals['provider_calls'], 'Provider call/read accounting discrepancy')
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status='PASS' if gate(records) else 'FAIL',diagnostic_execution_valid=True,
            C184_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            records=records,replay=replay,episodes=episode_count,replay_rows=56376,neural_initial_rows=89088,
            neural_post_rows=post_rows,total_inference_rows=meter['rows'],inference_batches=meter['forward_calls'],
            inference_cell_calls=meter['cell_calls'],checkpoint_loads=6,totals=totals,
            actual_acquisitions=totals['provider_calls'],actual_file_reads=provider_reads,
            provider_bytes_read=provider_bytes,taskview_fact_publications=totals['publications'],
            new_training=0,fresh_seeds=0,teacher_calls=0,auxiliary_forward_calls=0,
            answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,network_calls=0,
            production_runtime_modified=False,gate_e_candidate=False,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device='cpu',dtype='float32',threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['reused four development semantic groups;one unknown only',
                'target/tool/transport and numeric normalization are handwritten',
                'model is a necessity classifier,not answer/proof generator or production FOLD core',
                'live consumed resources are new inputs;no calibration or reset to training constants',
                'batched independent episodes;single-owner synchronous reference,not concurrent durability'])
        validate_result(result); (out/'summary.json').write_bytes(blob(result))
        print('[C185] 3/3 source/output preservation checked',flush=True)
        print('=== C185 RESULT ===',flush=True); print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status='INVALID',
            diagnostic_execution_valid=False,error=str(exc),completed_records=records,completed_replay=replay)))
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in PARENTS: p.add_argument('--'+n+'-summary',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--expected-head',required=True)
    run(**vars(p.parse_args()))


if __name__ == '__main__':
    main()
