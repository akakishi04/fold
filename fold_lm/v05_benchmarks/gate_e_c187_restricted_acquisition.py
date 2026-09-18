"""C187: semantic necessity under independent runtime acquisition restrictions.

Diagnostic only. Unchanged C185 driver, frozen C181 checkpoints, raw decisions.
Change exactly one initial resource field in each restriction arm. No policy
repair, implicit retry, permission bypass, answer generator or new training.
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

EXPERIMENT_ID = 'C187-v5e-restricted-acquisition-necessity'
STAGE = 'V5-E-RESTRICTED-ACQUISITION-NECESSITY'
BASE = '6e59bcbcdf84a37c4bece228b8163042cc6ac06a'
PARENT_SHA = 'e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82'
SEEDS = (181001, 181002, 181003)
ARMS = ('FINAL_ONLY', 'INTERNAL_SEMANTICS')
RULES = ('MISSING_RULE', 'NEVER_QUERY')
LAYOUTS = ((0, 1, 2, 3), (3, 2, 1, 0))
SCENARIOS = ('ALLOWED_ZERO', 'ALLOWED_ONE', 'PERMISSION_DENIED',
             'PROVIDER_UNAVAILABLE', 'ACQUISITION_BUDGET_ZERO')
PARENTS = ('c186', 'c185', 'c184', 'c183', 'c182', 'c181', 'c180', 'c179',
           'c178', 'c177', 'c176', 'c174')
OWN = ('fold_lm/v05_benchmarks/gate_e_c187_restricted_acquisition.py',
       'tests_lm/test_v05_c187_restricted_acquisition.py', 'tools/run_c187.ps1',
       'docs/experiment-ledger-addendum-c187-preregistration.md')
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
OUTPUTS = {'restriction-plan.json', 'frozen-replay.json', 'episode-results.json',
           'episode-traces.jsonl.gz', 'episode-predictions.npz'} | set(SOURCES)
COUNTERS = ('failed', 'initial_error', 'missed_proposal', 'unnecessary_proposal',
            'post_error', 'false_sufficient_after_denial', 'contract_error',
            'action_attempts', 'denied_attempts', 'provider_calls', 'publications',
            'reservations', 'decision_charges', 'internal_charged')
ATOL = 1e-6
EXPECTED_TESTS = 1377


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def scenario_spec(name):
    require(name in SCENARIOS, 'Unregistered restriction')
    if name in SCENARIOS[:2]:
        return dict(bit=int(name == 'ALLOWED_ONE'), allowed=True, field=None,
                    reason='ACQUISITION_RESERVED', outcome=0)
    return dict(bit=0, allowed=False, **{
        'PERMISSION_DENIED': dict(field=67, reason='PERMISSION_DENIED', outcome=2),
        'PROVIDER_UNAVAILABLE': dict(field=64, reason='PROVIDER_UNAVAILABLE', outcome=0),
        'ACQUISITION_BUDGET_ZERO': dict(field=63, reason='BUDGET_EXHAUSTED', outcome=3),
    }[name])


def restrict_views(views, scenario):
    """Copy ONLY one execution field. No semantic label, model or provider input."""
    spec = scenario_spec(scenario)
    result = []
    for view in views:
        r = view.resources
        if scenario == 'PERMISSION_DENIED':
            r = replace(r, permitted=(False, *r.permitted[1:]))
        elif scenario == 'PROVIDER_UNAVAILABLE':
            r = replace(r, available=(False, *r.available[1:]))
        elif scenario == 'ACQUISITION_BUDGET_ZERO':
            r = replace(r, acquisitions_remaining=0)
        result.append(replace(view, resources=r))
    return result


def resource_fields(scenario, phase, attempted=True):
    spec = scenario_spec(scenario)
    x = [12,4,1,0,0,1,0,0,0,7]
    if spec['field'] is not None:
        x[spec['field']-62] = 0
    require(phase in ('initial', 'first', 'post'), 'Unknown phase')
    if phase == 'first':
        x[0], x[9] = 11, 8
    elif phase == 'post':
        require(attempted, 'No second decision after a skipped proposal')
        x[0], x[9] = (7,12) if spec['allowed'] else (9,10)
        x[1] -= int(spec['allowed'])
        x[8] = spec['outcome']
    return x


def score_episode(record, label, scenario):
    """Post-hoc only. Preserve finite policy errors; never change a decision/action."""
    require(type(label) is int and label in (0,1), 'Exact semantic label required')
    spec = scenario_spec(scenario)
    initial, final = record['initial'], record['final']
    x, f = initial['features'], final['features']
    require(len(x) == len(f) == 72, 'Complete packets required')
    missing = [i for i in range(4) if x[48+4*i] == 0]
    require(len(missing) == 1, 'One missing fact required')
    mi = missing[0]; ib, fb = initial['binding'], final['binding']
    fid = ib['fact_ids'][mi]
    phases = record['phases']; p0 = phases[0]['prediction'] if phases else -1
    post = phases[1]['prediction'] if len(phases) == 2 else -1
    attempted = p0 == 1
    a = record['acquisition']; d = a['dispatch'] if a else None
    reserved = a['action']['acquisition_reserved'] if a else 0
    calls = d['provider_calls'] if d else 0
    published = d['fact_publications'] if d else 0
    charges = record['decision_charges'] + (a['action']['internal_charged'] if a else 0) + (d['internal_charged'] if d else 0)
    changed = set(range(62,72))
    if attempted and spec['allowed']:
        changed.update(range(46+4*mi,50+4*mi))
    fields_ok = all(f[i] == x[i] for i in range(72) if i not in changed)
    binding_ok = (fb['request_id'] == ib['request_id'] and fb['scope_id'] == ib['scope_id']
        and fb['fact_ids'] == ib['fact_ids'] and all(fb['reference_ids'][i] == ib['reference_ids'][i]
                                                  for i in range(4) if i != mi))
    clocks_ok = (f[62] == x[62]-charges and f[63] == x[63]-reserved and f[71] == x[71]+charges)
    packets_ok = (list(x[62:]) == resource_fields(scenario,'initial')
        and len(phases) == 1+int(attempted) and record['decision_charges'] == 1+int(attempted))
    for j, phase in enumerate(phases):
        packets_ok = packets_ok and phase['phase'] == j and list(phase['packet']['features'][62:]) == resource_fields(scenario,'first' if j == 0 else 'post')
    packets_ok = packets_ok and list(f[62:]) == resource_fields(scenario,'post' if attempted else 'first')
    receipts = record['receipts']
    if attempted:
        io_ok = (a is not None and a['fact_id'] == fid and a['input_index'] == mi
                 and a['action']['internal_charged'] == 1
                 and a['action']['reason'] == spec['reason'])
        if spec['allowed']:
            io_ok = (io_ok and a['action']['status'] == 'PENDING' and d is not None
                and reserved == calls == published == 1 and d['internal_charged'] == 2
                and d['status'] == 'PUBLISHED' and d['reason'] == 'OBSERVATION_ADMITTED')
            evidence_ok = (len(receipts) == 1 and receipts[0]['fact_id'] == fid
                and receipts[0]['request_id'] == ib['request_id'] and receipts[0]['scope_id'] == ib['scope_id']
                and receipts[0]['action'] == 'RETRIEVE' and receipts[0]['value'] == spec['bit']
                and d is not None and d['evidence'] == receipts[0]
                and list(f[46+4*mi:50+4*mi]) == [1,2,1,spec['bit']]
                and list(fb['reference_ids'][mi]) == [receipts[0]['reference_id']])
        else:
            io_ok = io_ok and a['action']['status'] == 'DENIED' and d is None and reserved == calls == published == 0
            evidence_ok = not receipts and fb == ib and list(f[46:62]) == list(x[46:62])
    else:
        io_ok = a is None and reserved == calls == published == 0
        evidence_ok = not receipts and fb == ib and list(f[46:62]) == list(x[46:62])
    status_ok = record['status'] == ('SUFFICIENT_CLASSIFICATION' if (post if attempted else p0) == 0 else 'UNRESOLVED')
    contract_ok = (fields_ok and binding_ok and clocks_ok and packets_ok and io_ok and evidence_ok
        and status_ok and record['pending'] is None and record['runtime_terminal'] is None)
    initial_error = int(p0 != label)
    expected_post = 0 if spec['allowed'] else label
    post_error = int(attempted and post != expected_post)
    return dict(failed=int(bool(initial_error or post_error or not contract_ok)), initial_error=initial_error,
        missed_proposal=int(label == 1 and not attempted), unnecessary_proposal=int(label == 0 and attempted),
        post_error=post_error, false_sufficient_after_denial=int(attempted and not spec['allowed'] and label == 1 and post == 0),
        contract_error=int(not contract_ok), action_attempts=int(a is not None),
        denied_attempts=int(a is not None and a['action']['status'] == 'DENIED'), provider_calls=calls,
        publications=published, reservations=reserved, decision_charges=record['decision_charges'], internal_charged=charges)


def expected_order():
    return [(s,a,l,c) for s,a in [(s,a) for s in SEEDS for a in ARMS]+[(0,r) for r in RULES]
            for l in range(2) for c in SCENARIOS]


def gate(records):
    if not isinstance(records,list) or [(r.get('seed'),r.get('arm'),r.get('layout'),r.get('scenario'))
                                       for r in records] != expected_order():
        return False
    for r in records:
        if r.get('episodes') != 3712 or r.get('labels') != {'needs':768,'sufficient':2944}:
            return False
        if any(type(r.get(k)) is not int or r[k] < 0 for k in COUNTERS) or r['contract_error'] != 0:
            return False
        allowed = scenario_spec(r['scenario'])['allowed']
        attempts = r['action_attempts']
        if (r['provider_calls'] != attempts*int(allowed) or r['publications'] != r['provider_calls']
            or r['reservations'] != r['provider_calls'] or r['denied_attempts'] != attempts*int(not allowed)
            or r['decision_charges'] != 3712+attempts
            or r['internal_charged'] != 3712+attempts*(4 if allowed else 2)):
            return False
        if r['arm'] == ARMS[1] and (any(r[k] != 0 for k in COUNTERS[:7]) or attempts != 768):
            return False
        if r['arm'] == RULES[0] and (attempts != 3712 or r['unnecessary_proposal'] != 2944
            or r['initial_error'] != 2944 or r['failed'] != 2944 or r['post_error'] != 2944*int(not allowed)):
            return False
        if r['arm'] == RULES[1] and (attempts != 0 or r['missed_proposal'] != 768
            or r['failed'] != 768 or r['post_error'] != 0):
            return False
    return True


def check_initial_packet_change(actual, prior, scenario):
    """No label check. Only the declared resource coordinate may change at phase0."""
    a, p = np.asarray(actual), np.asarray(prior)
    require(a.shape == p.shape and a.shape[-1] == 72 and a.dtype == p.dtype == np.int32,
            'Initial replay packet shape/dtype')
    expected = p.copy(); field = scenario_spec(scenario)['field']
    if field is not None:
        expected[...,field] = 0
    require(np.array_equal(a,expected), 'Undeclared change to initial visible input')


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,source_head=BASE,
        seeds=SEEDS,arms=ARMS,rules=RULES,layouts=LAYOUTS,scenarios=SCENARIOS,source_files=SOURCES,
        changed='one initial runtime field: retrieve permission, availability or acquisition budget; unchanged observations',
        driver='unchanged C185.run_block;raw argmax;one proposal at most,two decisions;no context reset',
        cohort='all3712one-missing development rows;768needs/2944sufficient;visibility-only selection',
        blocks=80,episodes=296960,candidate_episodes=111360,rule_episodes=74240,
        static_replay_rows=56376,successful_replay_blocks=32,neural_initial_rows=222720,
        neural_post_rows='measured,0..222720',total_neural_rows_max=501816,
        ideal_candidate_proposals=23040,ideal_candidate_reads=9216,ideal_candidate_denials=13824,
        ideal_candidate_skips=88320,checkpoint_loads=6,training=0,fresh_seeds=0,
        teacher=0,auxiliary=0,answer=0,proof=0,network=0,core_evidence_writes=0,
        first_resources='11internal/step8;only registered permission/availability/acquisition field differs',
        post_resources='allowed7/3/step12;denied9/(4 or0)/step10;outcome2,0,3 retained',
        device='cpu',dtype='float32',threads=2,batch=1024,replay_atol=ATOL,replay_rtol=0,
        gate='all3candidates zero initial/post/contract failures;allpolicycontracts;registeredcontrols',
        outputs=sorted(OUTPUTS),limits='same development semantics;not learned policy for alternative actions, retries or full GateE')


MANIFEST_SHA = 'e6b3c94a9c36bdf9e15333320a95f81f295baf1b6cda956e11c549e1ec89262e'


def precheck(c186_summary, *args):
    from fold_lm.v05_benchmarks import gate_e_c186_nonadmission_reclassification as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args) == 12, 'Eleven prior summaries and repository root required')
    root = args[-1]; p181,p174,pins,protected = previous.precheck(*args)
    require(audit.sha(c186_summary) == PARENT_SHA,'C186 summary changed')
    parent = audit.read_json(c186_summary); previous.validate_result(parent)
    require(parent['commit_sha'] == BASE and parent['status'] == 'PASS' and parent['source_blobs'] == pins,
            'Wrong accepted C186 source')
    protected[str(Path(c186_summary).resolve())] = PARENT_SHA
    for a in parent['artifacts']:
        f = audit.safe_child(Path(c186_summary).resolve().parent,a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],
                'Changed C186 artifact:'+a['file'])
        protected[str(f.resolve())] = a['sha256']
    pins = dict(pins)
    for name in previous.OWN:
        pins[name] = audit.git(root,'rev-parse',BASE+':'+name).decode().strip()
    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root,'rev-parse','HEAD:'+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins) == 99 and len(protected) == 221,'Source/protected union drift')
    require(digest(manifest()) == MANIFEST_SHA,'Manifest drift')
    return p181,p174,pins,protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c186_nonadmission_reclassification as previous
    names = previous.regression_modules(root)
    require(len(names) == len(set(names)) == 71,'Historical module drift')
    return names+['tests_lm.test_v05_c187_restricted_acquisition']


def validate_result(p):
    require(p['experiment_id'] == EXPERIMENT_ID and p['stage'] == STAGE and p['diagnostic_execution_valid'] is True,
            'Wrong/incomplete C187')
    require(p['episodes'] == 296960 and p['replay_rows'] == 56376 and p['neural_initial_rows'] == 222720
        and 0 <= p['neural_post_rows'] <= 222720 and p['total_inference_rows'] == 56376+222720+p['neural_post_rows']
        and p['inference_cell_calls'] == 7*p['inference_batches'] and p['checkpoint_loads'] == 6,'Workload drift')
    require(len(p['replay']) == 6 and len(p['successful_replay']) == 32 and len(p['records']) == 80
        and len(p['source_blobs']) == 99 and len(p['input_sha256']) == 221
        and len(p['artifacts']) == 13 and {a['file'] for a in p['artifacts']} == OUTPUTS,'Coverage drift')
    require(all(p[k] == 0 for k in ('new_training','fresh_seeds','teacher_calls','auxiliary_forward_calls',
        'answer_generation','proof_checker_calls','core_evidence_writes','network_calls'))
        and p['production_runtime_modified'] is False and p['gate_e_candidate'] is False,'Scope drift')
    require(all(p['totals'][k] == sum(r[k] for r in p['records']) for k in COUNTERS),'Counter drift')
    require(p['actual_file_reads'] == p['totals']['provider_calls']
        and p['taskview_fact_publications'] == p['totals']['publications'],'IO drift')
    require(p['status'] == ('PASS' if gate(p['records']) else 'FAIL'),'Gate drift')


def run(*, output_dir, expected_head, **parents):
    import torch
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c186_nonadmission_reclassification as prior
    from fold_lm.v05_benchmarks.c186_c185_npz_input import load_c185_predictions
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    graph,life = frozen.graph,driver.life
    root = Path(__file__).resolve().parents[2]
    args = tuple(parents[n+'_summary'] for n in PARENTS)+(root,)
    def guard():
        require(audit.git(root,'rev-parse','HEAD').decode().strip() == expected_head,'HEAD mismatch')
        require(audit.git(root,'branch','--show-current').decode().strip() == 'feat/sft-target-loss','Branch mismatch')
        require(not audit.git(root,'status','--porcelain','--untracked-files=no').strip(),'Dirty tracked tree')
    guard(); p181,p174,pins,protected = precheck(*args)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter(); artifacts=[]; records=[]; replay=[]; successful=[]
    def record_file(name):
        f=out/name; artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,value):
        (out/name).write_bytes(blob(value)); record_file(name)
    save('restriction-plan.json',dict(manifest(),source_blobs=pins))
    try:
        print('[C187] plan fixed; frozen necessity versus independent runtime restrictions; no repair',flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data,_=audit.load_data(Path(parents['c174_summary']).resolve().parent,p174)
        ev=data['split_codes']==1; missing=(data['features'][:,48:62:4]==0).sum(1)
        mask=ev & (missing==1); indices=np.flatnonzero(mask); y=data['labels'][mask]; groups=data['groups'][mask]
        require(len(indices)==3712 and int(y.sum())==768 and len(set(groups.tolist()))==4,'Cohort drift')
        raw=torch.from_numpy(data['features'][mask].copy()); rh=graph.tensor_sha(raw)
        require(torch.equal(raw[:,62:],torch.tensor(resource_fields(SCENARIOS[0],'initial'),dtype=torch.int32).expand(len(raw),-1)),
                'Original resource context drift')
        parent_dir=Path(parents['c181_summary']).resolve().parent
        saved=audit.read_json(parent_dir/'pilot-predictions.json')
        # Exact accepted C185 schema loader, NOT generic32MiB or a C186-NPZ reader.
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
        print('[C187] 1/3 all56376 original decisions replayed; all3712 one-missing rows retained',flush=True)
        providers={}; endpoints={}; (out/'sources').mkdir()
        for bit in (0,1):
            endpoints[bit]={}
            for i,fid in enumerate(driver.FACT_IDS):
                name=f'sources/fact-{i}-completion-{bit}.json'; b=driver.fixture_bytes(i,bit)
                require(hashlib.sha256(b).hexdigest()==SOURCES[name],'Source bytes drift')
                (out/name).write_bytes(b); record_file(name)
                sb=life.SourceBinding(f'C185-fixture-{i}-{bit}',hashlib.sha256(b).hexdigest())
                pr=life.FileSnapshotProvider(out/name,sb); providers[(i,bit)]=pr
                endpoints[bit][fid]=life.Endpoint(sb,pr)
        policies=[driver.FrozenPolicy(m) for m in models]+[driver.RulePolicy(r) for r in RULES]
        dense=dict(predictions=np.full((8,2,5,3712,2),-1,dtype=np.int8),
            logits=np.zeros((8,2,5,3712,2,2),dtype=np.float32),
            logit_present=np.zeros((8,2,5,3712,2),dtype=bool),
            policy_inputs=np.zeros((8,2,5,3712,2,72),dtype=np.int32))
        post_rows=0
        with gzip.open(out/'episode-traces.jsonl.gz','wt',encoding='utf-8',newline='\n') as trace:
            for pi,((seed,arm),policy) in enumerate(zip(order,policies)):
                for li,layout in enumerate(LAYOUTS):
                    for si,scenario in enumerate(SCENARIOS):
                        base_views=driver.make_views(raw,indices,layout,f'C187-p{pi}-l{li}-s{si}')
                        views=restrict_views(base_views,scenario)
                        before_reads=sum(pr.reads for pr in providers.values())
                        observed,arrays,m=driver.run_block(views,endpoints[scenario_spec(scenario)['bit']],policy)
                        actual_reads=sum(pr.reads for pr in providers.values())-before_reads
                        for k in meter: meter[k]+=m[k]
                        if pi<6: post_rows+=m['rows']-len(views)
                        for k in dense: dense[k][pi,li,si]=arrays[k]
                        if si<2:
                            delta=prior.replay_arrays(arrays,{k:old[k][pi,li,si] for k in dense})
                            successful.append(dict(seed=seed,arm=arm,layout=li,completion=si,
                                                   decisions_equal=True,max_abs_logit_difference=delta))
                        check_initial_packet_change(arrays['policy_inputs'][:,0],old['policy_inputs'][pi,li,0,:,0],scenario)
                        scores=[score_episode(r,int(label),scenario) for r,label in zip(observed,y)]
                        totals={k:sum(s[k] for s in scores) for k in COUNTERS}
                        require(actual_reads==totals['provider_calls'],'Provider accounting discrepancy')
                        records.append(dict(seed=seed,arm=arm,layout=li,scenario=scenario,episodes=len(views),
                            labels=dict(needs=768,sufficient=2944),actual_file_reads=actual_reads,
                            initial_flips_from_unrestricted=int(np.count_nonzero(arrays['predictions'][:,0]!=old['predictions'][pi,li,0,:,0])),
                            by_group={str(g):{k:sum(scores[j][k] for j in np.flatnonzero(groups==g)) for k in COUNTERS}
                                      for g in sorted(set(groups.tolist()))},**totals))
                        for j,r in enumerate(observed):
                            trace.write(json.dumps(dict(policy_index=pi,seed=seed,arm=arm,layout=li,scenario=scenario,
                                source_row=int(indices[j]),label=int(y[j]),score=scores[j],trace=r),
                                sort_keys=True,separators=(',',':'),allow_nan=False)+'\n')
                        print(f'[C187] block={len(records)}/80 arm={arm} seed={seed} scenario={scenario} '
                              f'failed={totals["failed"]} denied={totals["denied_attempts"]} reads={actual_reads}',flush=True)
        record_file('episode-traces.jsonl.gz'); save('episode-results.json',records)
        save('frozen-replay.json',dict(static=replay,successful=successful))
        np.savez_compressed(out/'episode-predictions.npz',**dense,row_indices=indices.astype('<i4'),
            policy_seeds=np.asarray([s for s,a in order],dtype='<i4'),policy_names=np.asarray([a for s,a in order]),
            layouts=np.asarray(LAYOUTS,dtype=np.int8),scenarios=np.asarray(SCENARIOS))
        record_file('episode-predictions.npz')
        print('[C187] 2/3 all296960 episodes collected; denied requests never repaired into knowledge',flush=True)
        guard(); precheck(*args)
        require(graph.tensor_sha(raw)==rh and [graph.fingerprint(m) for m in models]==fps,'Input/model changed')
        for f,h in protected.items(): require(audit.sha(f)==h,'Protected input changed:'+f)
        for a in artifacts: require(audit.sha(out/a['file'])==a['sha256'],'Output changed:'+a['file'])
        totals={k:sum(r[k] for r in records) for k in COUNTERS}
        reads=sum(pr.reads for pr in providers.values()); readbytes=sum(pr.bytes_read for pr in providers.values())
        require(reads==totals['provider_calls'],'IO meter drift')
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status='PASS' if gate(records) else 'FAIL',diagnostic_execution_valid=True,
            C186_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            replay=replay,successful_replay=successful,records=records,totals=totals,episodes=sum(r['episodes'] for r in records),
            replay_rows=56376,neural_initial_rows=222720,neural_post_rows=post_rows,total_inference_rows=meter['rows'],
            inference_batches=meter['forward_calls'],inference_cell_calls=meter['cell_calls'],checkpoint_loads=6,
            actual_file_reads=reads,provider_bytes_read=readbytes,taskview_fact_publications=totals['publications'],
            new_training=0,fresh_seeds=0,teacher_calls=0,auxiliary_forward_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,network_calls=0,production_runtime_modified=False,gate_e_candidate=False,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device='cpu',dtype='float32',threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['initial single-field restrictions,not concurrent revocation or learned retry/alternative selection',
                'same four development groups and one unknown;handwritten target/tool/transport',
                'raw necessity classification is not an answer or permission;finite errors never corrected'])
        validate_result(result); (out/'summary.json').write_bytes(blob(result))
        print('[C187] 3/3 source/output preservation checked',flush=True)
        print('=== C187 RESULT ===',flush=True); print(blob(result).decode(),flush=True)
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
