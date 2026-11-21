"""C186: frozen reclassification after admitted or deliberately non-admitted IO.

No training, answer generation, retries or policy-level failure correction.
The C185 episode driver and C170/C172/C173 runtime remain unchanged. Injection
happens after an actual reference-provider read, outside the policy input.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import gzip
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from .c186_c185_npz_input import inspect_c185_predictions, load_c185_predictions

EXPERIMENT_ID = 'C186-v5e-nonadmission-reclassification'
STAGE = 'V5-E-NONADMISSION-RECLASSIFICATION'
BASE = '36c0ab26de2334f8b54d3e0754bf408deec7f0db'
PARENT_SHA = '843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949'
SEEDS = (181001, 181002, 181003)
ARMS = ('FINAL_ONLY', 'INTERNAL_SEMANTICS')
RULES = ('MISSING_RULE', 'NEVER_QUERY')
LAYOUTS = ((0, 1, 2, 3), (3, 2, 1, 0))
SCENARIOS = ('FOUND_ZERO', 'FOUND_ONE', 'NO_DELIVERY', 'WRONG_VALUE', 'PROVIDER_FAILURE')
PARENTS = ('c185', 'c184', 'c183', 'c182', 'c181', 'c180', 'c179', 'c178', 'c177', 'c176', 'c174')
OWN = ('fold_lm/v05_benchmarks/gate_e_c186_nonadmission_reclassification.py',
       'tests_lm/test_v05_c186_nonadmission_reclassification.py', 'tools/run_c186.ps1',
       'docs/experiment-ledger-addendum-c186-preregistration.md',
       'fold_lm/v05_benchmarks/c186_c185_npz_input.py',
       'tests_lm/test_v05_c186_npz_input_recovery.py',
       'docs/experiment-ledger-addendum-c186-execution-recovery.md')
SOURCES = {
    'sources/fact-0-completion-0.json': 'd3d693b1ce3d22b31f3826feace8eb511eb3e8f5b427ba1ac2fb607af8419dc2',
    'sources/fact-1-completion-0.json': '1b6b28bab6436fb62dac757d629d4eda6da45c098f70f5f3414a6b1afc9fd292',
    'sources/fact-2-completion-0.json': 'ff89d9d08d5cf91452059f835997a2001c2c27e39a341e35294a28c564beca5b',
    'sources/fact-3-completion-0.json': '6182708e781d9f0f73cd3df20c1257a9611d8d3ed02f4499992e700545b249c2',
    'sources/fact-0-completion-1.json': 'aa684e21cc075142892e05a65d260a3967abde5da7b3996d58b924df7df8f7d6',
    'sources/fact-1-completion-1.json': '43984ace8084b91f3bb8ec74c1da6f97b3ff95a988fe62373f7a07647ceb3e56',
    'sources/fact-2-completion-1.json': 'd6fb4451badea2e3d8fe8bceb80464c891efae5f7323c1509599c9eca5e2b70c',
    'sources/fact-3-completion-1.json': '09c4b6c269cbfbf1ab3c9cf9ce22cdcd5ded0abbf2fd601d8a1e50be2a6e9ea9',
}
OUTPUTS = {'nonadmission-plan.json', 'frozen-replay.json', 'episode-results.json',
           'episode-traces.jsonl.gz', 'episode-predictions.npz'} | set(SOURCES)
COUNTERS = ('failed', 'initial_error', 'missed_attempt', 'unnecessary_attempt',
            'post_error', 'false_sufficient_after_nonadmission', 'contract_error',
            'action_attempts', 'provider_calls', 'publications', 'non_admitted_attempts',
            'reservations', 'decision_charges', 'internal_charged')
ATOL = 1e-6


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def scenario_spec(name):
    require(name in SCENARIOS, 'Unregistered delivery scenario')
    if name in SCENARIOS[:2]:
        return dict(bit=int(name == 'FOUND_ONE'), admitted=True,
                    status='PUBLISHED', reason='OBSERVATION_ADMITTED', outcome=0)
    return dict(bit=0, admitted=False, **{
        'NO_DELIVERY': dict(status='UNRESOLVED', reason='MISSING_DELIVERY', outcome=4),
        'WRONG_VALUE': dict(status='REJECTED', reason='INVALID_EVIDENCE', outcome=6),
        'PROVIDER_FAILURE': dict(status='UNRESOLVED', reason='PROVIDER_FAILURE', outcome=0),
    }[name])


class OutcomeProvider:
    """Inject AFTER the actual file provider returns. No labels or policy access.

    failure_type is the existing C173 ProviderFailure in the formal run. Synthetic
    tests may supply a separate ValueError subclass; this is not an IO timeout test.
    """
    def __init__(self, fetch, scenario, failure_type):
        scenario_spec(scenario)
        require(callable(fetch) and isinstance(failure_type, type)
                and issubclass(failure_type, ValueError), 'Trusted fetch/error type required')
        self.fetch, self.scenario, self.failure_type = fetch, scenario, failure_type
        self.calls = 0

    def __call__(self, request):
        self.calls += 1
        delivery = self.fetch(request)
        if self.scenario == 'NO_DELIVERY':
            return None
        if self.scenario == 'WRONG_VALUE':
            require(type(delivery.value) is int and delivery.value in (0, 1),
                    'Expected genuine provider bit before corruption')
            return replace(delivery, value=1-delivery.value)
        if self.scenario == 'PROVIDER_FAILURE':
            raise self.failure_type('C186_INJECTED_AFTER_REFERENCE_READ')
        return delivery


def score_episode(record, label, scenario):
    """Post-hoc scoring. Neither label nor this function reaches run_block/policy."""
    spec = scenario_spec(scenario)
    require(type(label) is int and label in (0, 1), 'Exact binary scoring label')
    initial, final = record['initial'], record['final']
    x, f = initial['features'], final['features']
    require(len(x) == len(f) == 72, 'Complete numeric packets required')
    missing = [i for i in range(4) if x[48+4*i] == 0]
    require(len(missing) == 1, 'One-missing scoring domain')
    mi = missing[0]; ib, fb = initial['binding'], final['binding']; fid = ib['fact_ids'][mi]
    phases = record['phases']; p0 = phases[0]['prediction'] if phases else -1
    post = phases[1]['prediction'] if len(phases) == 2 else -1
    a = record['acquisition']; d = a['dispatch'] if a else None
    reserved = a['action']['acquisition_reserved'] if a else 0
    calls = d['provider_calls'] if d else 0
    published = d['fact_publications'] if d else 0
    charges = record['decision_charges'] + (a['action']['internal_charged'] if a else 0) + (d['internal_charged'] if d else 0)
    # None of the three fault injections may silently publish a usable fact.
    attempted = p0 == 1
    allowed = set(range(62, 72))
    if attempted and spec['admitted']:
        allowed.update(range(46+4*mi, 50+4*mi))
    same_fields = all(f[i] == x[i] for i in range(72) if i not in allowed)
    same_binding = (fb['request_id'] == ib['request_id'] and fb['scope_id'] == ib['scope_id']
        and fb['fact_ids'] == ib['fact_ids'] and all(fb['reference_ids'][i] == ib['reference_ids'][i]
                                                  for i in range(4) if i != mi))
    bookkeeping = (f[62] == x[62]-charges and f[63] == x[63]-reserved
        and f[71] == x[71]+charges and list(f[64:70]) == list(x[64:70])
        and record['decision_charges'] == 1+int(attempted))
    current_packets = len(phases) == 1+int(attempted)
    for j, phase in enumerate(phases):
        want = [11,4,1,0,0,1,0,0,0,8] if j == 0 else [7,3,1,0,0,1,0,0,spec['outcome'],12]
        current_packets = current_packets and phase['phase'] == j and list(phase['packet']['features'][62:]) == want
    receipts = record['receipts']
    if attempted:
        io_ok = (a is not None and d is not None and a['fact_id'] == fid and a['input_index'] == mi
            and a['action']['status'] == 'PENDING' and a['action']['internal_charged'] == 1
            and reserved == calls == 1 and d['internal_charged'] == 2
            and d['status'] == spec['status'] and d['reason'] == spec['reason']
            and published == int(spec['admitted']) and f[70] == spec['outcome'])
        if spec['admitted']:
            evidence_ok = (len(receipts) == 1 and receipts[0]['fact_id'] == fid
                and receipts[0]['request_id'] == ib['request_id'] and receipts[0]['scope_id'] == ib['scope_id']
                and receipts[0]['action'] == 'RETRIEVE' and receipts[0]['value'] == spec['bit']
                and d['evidence'] == receipts[0] and list(f[46+4*mi:50+4*mi]) == [1,2,1,spec['bit']]
                and list(fb['reference_ids'][mi]) == [receipts[0]['reference_id']])
        else:
            evidence_ok = not receipts and d is not None and d['evidence'] is None and fb == ib and list(f[46:62]) == list(x[46:62])
    else:
        io_ok = a is None and reserved == calls == published == 0 and f[70] == x[70]
        evidence_ok = not receipts and fb == ib and list(f[46:62]) == list(x[46:62])
    status_ok = record['status'] == ('SUFFICIENT_CLASSIFICATION' if (post if attempted else p0) == 0 else 'UNRESOLVED')
    contract_ok = (same_fields and same_binding and bookkeeping and current_packets and io_ok
        and evidence_ok and status_ok and record['pending'] is None and record['runtime_terminal'] is None)
    expected_post = 0 if spec['admitted'] else label
    initial_error = int(p0 != label)
    post_error = int(attempted and post != expected_post)
    return dict(failed=int(bool(initial_error or post_error or not contract_ok)),
        initial_error=initial_error, missed_attempt=int(label == 1 and not attempted),
        unnecessary_attempt=int(label == 0 and attempted), post_error=post_error,
        false_sufficient_after_nonadmission=int(attempted and not spec['admitted'] and label == 1 and post == 0),
        contract_error=int(not contract_ok), action_attempts=int(a is not None), provider_calls=calls,
        publications=published, non_admitted_attempts=int(calls > 0 and published == 0),
        reservations=reserved, decision_charges=record['decision_charges'], internal_charged=charges)


def expected_order():
    return [(s,a,l,c) for s,a in [(s,a) for s in SEEDS for a in ARMS]+[(0,r) for r in RULES]
            for l in range(2) for c in SCENARIOS]


def gate(records):
    if not isinstance(records, list) or [(r.get('seed'),r.get('arm'),r.get('layout'),r.get('scenario'))
                                        for r in records] != expected_order():
        return False
    for r in records:
        if r.get('episodes') != 3712 or r.get('labels') != {'needs':768,'sufficient':2944}:
            return False
        if any(type(r.get(k)) is not int or r[k] < 0 for k in COUNTERS) or r['contract_error'] != 0:
            return False
        admitted = scenario_spec(r['scenario'])['admitted']
        if r['arm'] == ARMS[1]:
            if any(r[k] != 0 for k in COUNTERS[:7]) or r['action_attempts'] != 768 or r['provider_calls'] != 768:
                return False
            if r['publications'] != 768*int(admitted) or r['non_admitted_attempts'] != 768*int(not admitted):
                return False
        if r['arm'] == RULES[0]:
            if (r['action_attempts'] != 3712 or r['provider_calls'] != 3712 or r['unnecessary_attempt'] != 2944
                or r['initial_error'] != 2944 or r['failed'] != 2944
                or r['post_error'] != 2944*int(not admitted)):
                return False
        if r['arm'] == RULES[1] and (r['provider_calls'] != 0 or r['missed_attempt'] != 768
                                   or r['failed'] != 768 or r['post_error'] != 0):
            return False
    return True


def replay_arrays(actual, prior):
    """Same successful pipeline, not a performance comparison or a score repair."""
    for key in ('predictions', 'logit_present', 'policy_inputs'):
        require(np.array_equal(actual[key], prior[key]), 'C185 successful replay mismatch: '+key)
    a,b = np.asarray(actual['logits']), np.asarray(prior['logits'])
    require(a.shape == b.shape and a.dtype == b.dtype == np.float32 and np.isfinite(a).all() and np.isfinite(b).all(),
            'Nonfinite or wrong successful replay logits')
    delta = float(np.max(np.abs(a.astype(np.float64)-b.astype(np.float64))))
    require(delta <= ATOL, 'C185 successful replay score drift')
    return delta


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,source_head=BASE,
        seeds=SEEDS,arms=ARMS,rules=RULES,layouts=LAYOUTS,scenarios=SCENARIOS,
        changed='provider return after real read: unchanged found0/1 versus no reply, corrupt bit or ProviderFailure',
        driver='unchanged C185.run_block;raw argmax;one attempt,two decisions;no resource reset',
        cohort='all3712one-missing development rows,768NEEDS+2944SUFFICIENT',
        source_files=SOURCES,blocks=80,episodes=296960,candidate_episodes=111360,
        neural_initial_rows=222720,neural_post_rows='measured,0..222720',static_replay_rows=56376,
        successful_replay_blocks=32,total_neural_rows_upper_bound=501816,
        ideal_candidate_attempts=23040,ideal_candidate_publications=9216,
        ideal_candidate_nonadmissions=13824,ideal_candidate_skips=88320,
        snapshot_loads=6,training=0,fresh_seeds=0,teacher=0,auxiliary=0,proof=0,answer=0,
        device='cpu',dtype='float32',threads=2,batch=1024,replay_atol=ATOL,replay_rtol=0,
        gate='zero episode failures in all3candidates;allpolicycontracts;registeredrulecontrols',
        limits='injected nonadmission only;not permission denial or timeout fidelity;reused semantics;no retry policy or GateE',
        outputs=sorted(OUTPUTS))


MANIFEST_SHA = '0cbe7212e5bafd9fc52f3f315d2d4732afaca6eb11940c6fa16ac58aeb336edc'


def precheck(c185_summary, *args):
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args) == 11, 'Ten prior summaries and repository root required')
    root = args[-1]; p181,p174,pins,protected = previous.precheck(*args)
    require(audit.sha(c185_summary) == PARENT_SHA, 'C185 summary changed')
    parent = audit.read_json(c185_summary); previous.validate_result(parent)
    require(parent['commit_sha'] == BASE and parent['status'] == 'PASS' and parent['source_blobs'] == pins,
            'Wrong accepted C185 source')
    protected[str(Path(c185_summary).resolve())] = PARENT_SHA
    for a in parent['artifacts']:
        f = audit.safe_child(Path(c185_summary).resolve().parent,a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],
                'Changed C185 artifact:'+a['file'])
        protected[str(f.resolve())] = a['sha256']
    pins = dict(pins)
    for name in previous.OWN: pins[name] = audit.git(root,'rev-parse',BASE+':'+name).decode().strip()
    allpins = dict(pins)
    for name in OWN: allpins[name] = audit.git(root,'rev-parse','HEAD:'+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins) == 92 and len(protected) == 203, 'Source/protected union drift')
    require(digest(manifest()) == MANIFEST_SHA, 'Manifest drift')
    inspect_c185_predictions(Path(c185_summary).resolve().parent/'episode-predictions.npz')
    return p181,p174,pins,protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as previous
    names = previous.regression_modules(root)
    require(len(names) == len(set(names)) == 69, 'Historical module drift')
    return names+['tests_lm.test_v05_c186_nonadmission_reclassification',
                  'tests_lm.test_v05_c186_npz_input_recovery']


def validate_result(p):
    require(p['experiment_id'] == EXPERIMENT_ID and p['stage'] == STAGE and p['diagnostic_execution_valid'] is True,
            'Wrong/incomplete C186')
    require(p['episodes'] == 296960 and p['replay_rows'] == 56376 and p['neural_initial_rows'] == 222720
        and 0 <= p['neural_post_rows'] <= 222720 and p['total_inference_rows'] == 56376+222720+p['neural_post_rows']
        and p['inference_cell_calls'] == 7*p['inference_batches'] and p['checkpoint_loads'] == 6, 'Workload drift')
    require(len(p['replay']) == 6 and len(p['successful_replay']) == 32 and len(p['records']) == 80
        and len(p['source_blobs']) == 92 and len(p['input_sha256']) == 203
        and len(p['artifacts']) == 13 and {a['file'] for a in p['artifacts']} == OUTPUTS, 'Coverage drift')
    require(all(p[k] == 0 for k in ('new_training','fresh_seeds','teacher_calls','auxiliary_forward_calls',
        'answer_generation','proof_checker_calls','core_evidence_writes','network_calls'))
        and p['production_runtime_modified'] is False and p['gate_e_candidate'] is False, 'Scope drift')
    require(all(p['totals'][k] == sum(r[k] for r in p['records']) for k in COUNTERS), 'Aggregation drift')
    require(p['actual_file_reads'] == p['totals']['provider_calls']
        and p['taskview_fact_publications'] == p['totals']['publications'], 'IO drift')
    require(p['status'] == ('PASS' if gate(p['records']) else 'FAIL'), 'Gate drift')


def run(*, output_dir, expected_head, **parents):
    import torch
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as previous
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    graph,life = frozen.graph,previous.life
    root = Path(__file__).resolve().parents[2]
    args = tuple(parents[n+'_summary'] for n in PARENTS)+(root,)
    def guard():
        require(audit.git(root,'rev-parse','HEAD').decode().strip() == expected_head,'HEAD mismatch')
        require(audit.git(root,'branch','--show-current').decode().strip() == 'feat/sft-target-loss','Branch mismatch')
        require(not audit.git(root,'status','--porcelain','--untracked-files=no').strip(),'Dirty tracked tree')
    guard(); p181,p174,pins,protected = precheck(*args)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    started = time.perf_counter(); artifacts=[]; records=[]; replay=[]; successful=[]
    def record_file(name):
        f=out/name; artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,value):
        (out/name).write_bytes(blob(value)); record_file(name)
    save('nonadmission-plan.json',dict(manifest(),source_blobs=pins))
    try:
        print('[C186] plan fixed; frozen reclassification after actual IO and injected nonadmission; no retry',flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data,_=audit.load_data(Path(parents['c174_summary']).resolve().parent,p174)
        ev=data['split_codes']==1; missing=(data['features'][:,48:62:4]==0).sum(1)
        mask=ev & (missing==1); indices=np.flatnonzero(mask); y=data['labels'][mask]; groups=data['groups'][mask]
        require(len(indices)==3712 and int(y.sum())==768 and len(set(groups.tolist()))==4,'Cohort drift')
        raw=torch.from_numpy(data['features'][mask].copy()); rh=graph.tensor_sha(raw)
        require(torch.equal(raw[:,62:],torch.tensor([12,4,1,0,0,1,0,0,0,7],dtype=torch.int32).expand(len(raw),-1)),
                'Original resources drift')
        parent_dir=Path(parents['c181_summary']).resolve().parent
        saved=audit.read_json(parent_dir/'pilot-predictions.json')
        old=load_c185_predictions(Path(parents['c185_summary']).resolve().parent/'episode-predictions.npz')
        order=[(s,a) for s in SEEDS for a in ARMS]+[(0,r) for r in RULES]
        require(set(old)=={'predictions','logits','logit_present','policy_inputs','row_indices','policy_seeds','policy_names','layouts'}
            and np.array_equal(old['row_indices'],indices) and np.array_equal(old['layouts'],LAYOUTS)
            and np.array_equal(old['policy_seeds'],[s for s,a in order])
            and np.array_equal(old['policy_names'],[a for s,a in order]),'C185 saved mapping drift')
        models=[]; fps=[]; meter=dict(rows=0,forward_calls=0,cell_calls=0)
        raw_ev=torch.from_numpy(data['features'][ev].copy())
        require(len(saved)==6 and len(p181['fit_records'])==6,'Checkpoint coverage drift')
        for i,(seed,arm) in enumerate(order[:6]):
            fit=p181['fit_records'][i]; oldrow=saved[i]
            require((fit['seed'],fit['arm'])==(seed,arm)==(oldrow['seed'],oldrow['arm'])
                and np.array_equal(oldrow['row_indices'],np.flatnonzero(ev)),'Checkpoint identity drift')
            model=frozen.restore_bare(parent_dir/f'probe-{seed}-{arm}.pt',seed,arm,fit['final_sha256'])
            p,z,m=graph.predict(model,binding.prepare_pair(raw_ev)[1],batch=1024)
            replay.append(dict(seed=seed,arm=arm,**frozen.replay_check(p.numpy(),z.numpy(),oldrow['predictions'],oldrow['logits'])))
            for k in meter: meter[k]+=m[k]
            models.append(model); fps.append(graph.fingerprint(model))
        print('[C186] 1/3 all56376 static decisions replayed; entire one-missing cohort fixed',flush=True)
        providers={}; endpoints={}; wrappers=[]; (out/'sources').mkdir()
        for bit in (0,1):
            for i,fid in enumerate(previous.FACT_IDS):
                name=f'sources/fact-{i}-completion-{bit}.json'; b=previous.fixture_bytes(i,bit)
                require(hashlib.sha256(b).hexdigest()==SOURCES[name],'Source bytes drift')
                (out/name).write_bytes(b); record_file(name)
                sb=life.SourceBinding(f'C185-fixture-{i}-{bit}',hashlib.sha256(b).hexdigest())
                providers[(i,bit)]=life.FileSnapshotProvider(out/name,sb)
        for scenario in SCENARIOS:
            endpoints[scenario]={}; bit=scenario_spec(scenario)['bit']
            for i,fid in enumerate(previous.FACT_IDS):
                pr=providers[(i,bit)]; wrapper=OutcomeProvider(pr,scenario,life.ProviderFailure)
                wrappers.append(wrapper); endpoints[scenario][fid]=life.Endpoint(pr.source,wrapper)
        policies=[previous.FrozenPolicy(m) for m in models]+[previous.RulePolicy(r) for r in RULES]
        dense=dict(predictions=np.full((8,2,5,3712,2),-1,dtype=np.int8),
            logits=np.zeros((8,2,5,3712,2,2),dtype=np.float32),
            logit_present=np.zeros((8,2,5,3712,2),dtype=bool),
            policy_inputs=np.zeros((8,2,5,3712,2,72),dtype=np.int32))
        post_rows=0
        with gzip.open(out/'episode-traces.jsonl.gz','wt',encoding='utf-8',newline='\n') as trace:
            for pi,((seed,arm),policy) in enumerate(zip(order,policies)):
                for li,layout in enumerate(LAYOUTS):
                    for si,scenario in enumerate(SCENARIOS):
                        views=previous.make_views(raw,indices,layout,f'C186-p{pi}-l{li}-s{si}')
                        observed,arrays,m=previous.run_block(views,endpoints[scenario],policy)
                        for k in meter: meter[k]+=m[k]
                        if pi<6: post_rows+=m['rows']-len(views)
                        for k in dense: dense[k][pi,li,si]=arrays[k]
                        if si<2:
                            delta=replay_arrays(arrays,{k:old[k][pi,li,si] for k in dense})
                            successful.append(dict(seed=seed,arm=arm,layout=li,completion=si,
                                                   decisions_equal=True,max_abs_logit_difference=delta))
                        else:
                            # Injection occurs only AFTER the first decision, so first inputs/scores must replay.
                            replay_arrays({k:arrays[k][:,0:1] for k in dense},
                                          {k:old[k][pi,li,0][:,0:1] for k in dense})
                        scores=[score_episode(r,int(label),scenario) for r,label in zip(observed,y)]
                        totals={k:sum(s[k] for s in scores) for k in COUNTERS}
                        records.append(dict(seed=seed,arm=arm,layout=li,scenario=scenario,episodes=len(views),
                            labels=dict(needs=768,sufficient=2944),by_group={str(g):{
                                k:sum(scores[j][k] for j in np.flatnonzero(groups==g)) for k in COUNTERS}
                                for g in sorted(set(groups.tolist()))},**totals))
                        for j,r in enumerate(observed):
                            trace.write(json.dumps(dict(policy_index=pi,seed=seed,arm=arm,layout=li,scenario=scenario,
                                source_row=int(indices[j]),label=int(y[j]),score=scores[j],trace=r),
                                sort_keys=True,separators=(',',':'),allow_nan=False)+'\n')
                        print(f'[C186] block={len(records)}/80 arm={arm} seed={seed} scenario={scenario} '
                              f'failed={totals["failed"]} post_errors={totals["post_error"]} admitted={totals["publications"]}',flush=True)
        record_file('episode-traces.jsonl.gz'); save('episode-results.json',records)
        save('frozen-replay.json',dict(static=replay,successful=successful))
        np.savez_compressed(out/'episode-predictions.npz',**dense,row_indices=indices.astype('<i4'),
            policy_seeds=np.asarray([s for s,a in order],dtype='<i4'),policy_names=np.asarray([a for s,a in order]),
            layouts=np.asarray(LAYOUTS,dtype=np.int8),scenarios=np.asarray(SCENARIOS))
        record_file('episode-predictions.npz')
        print('[C186] 2/3 all296960 episodes collected; failures were not replaced by observations',flush=True)
        guard(); precheck(*args)
        require(graph.tensor_sha(raw)==rh and [graph.fingerprint(m) for m in models]==fps,'Input/model changed')
        for f,h in protected.items(): require(audit.sha(f)==h,'Protected input changed:'+f)
        for a in artifacts: require(audit.sha(out/a['file'])==a['sha256'],'Output changed:'+a['file'])
        totals={k:sum(r[k] for r in records) for k in COUNTERS}
        reads=sum(p.reads for p in providers.values()); readbytes=sum(p.bytes_read for p in providers.values())
        require(reads==sum(w.calls for w in wrappers)==totals['provider_calls'],'IO meter drift')
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status='PASS' if gate(records) else 'FAIL',diagnostic_execution_valid=True,
            C185_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            replay=replay,successful_replay=successful,records=records,totals=totals,episodes=sum(r['episodes'] for r in records),
            replay_rows=56376,neural_initial_rows=222720,neural_post_rows=post_rows,total_inference_rows=meter['rows'],
            inference_batches=meter['forward_calls'],inference_cell_calls=meter['cell_calls'],checkpoint_loads=6,
            actual_file_reads=reads,provider_bytes_read=readbytes,taskview_fact_publications=totals['publications'],
            new_training=0,fresh_seeds=0,teacher_calls=0,auxiliary_forward_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,network_calls=0,production_runtime_modified=False,gate_e_candidate=False,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device='cpu',dtype='float32',threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['injected return failures after reference read,not real outage/timeout fidelity',
                'same four development groups and one unknown;handwritten target/tool/transport',
                'no learned retry policy,answer/proof or final Gate E;finite errors never corrected'])
        validate_result(result); (out/'summary.json').write_bytes(blob(result))
        print('[C186] 3/3 source/output preservation checked',flush=True)
        print('=== C186 RESULT ===',flush=True); print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status='INVALID',
            diagnostic_execution_valid=False,error=str(exc),completed_records=records,completed_replay=replay)))
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in PARENTS: p.add_argument('--'+n+'-summary',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True); p.add_argument('--expected-head',required=True)
    run(**vars(p.parse_args()))


if __name__=='__main__':
    main()
