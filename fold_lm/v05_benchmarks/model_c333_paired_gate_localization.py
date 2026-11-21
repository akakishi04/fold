"""C333: localize C332's saved trained-policy tradeoffs without new neural work."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json

EXPERIMENT_ID = 'C333-v5b-paired-gate-localization'
STAGE = 'V5-B-PAIRED-GATE-LOCALIZATION'
SEEDS = tuple(range(332001, 332006))
ARMS = ('native', 'first_mean')
DOMAINS = ('original2', 'original3', 'original4', 'original5', 'original6', 'interior4')
OWN = ('fold_lm/v05_benchmarks/model_c333_paired_gate_localization.py',
       'tools/c333_execution.py', 'tests_lm/test_v05_c333_paired_gate_localization.py',
       'tools/run_c333.ps1', 'tools/invoke_c333.ps1',
       'docs/experiment-ledger-addendum-c333-preregistration.md')
OUTPUTS = ('diagnostic-plan.json', 'localization.json', 'transitions.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 32, 5978, 223
SOURCE_COUNT, INPUT_COUNT = 859, 2969
WORK = dict(checkpoint_records=10, domain_records=60, local_cells=4320, order_cells=2160,
            local_transitions=2160, order_transitions=1080, train_steps=0, model_forward_calls=0,
            gradient_calls=0, optimizer_steps=0, model_state_loads=0, new_checkpoint_writes=0, network_calls=0)
MANIFEST_SHA = '4ec2a2575956195e223e8c217086966dc95d765c644c3d3d619dd0d8dc693066'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c332_trained_first_mean_query')


def localizer():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c330_saved_gate_localization')


def identities():
    return list(itertools.product(SEEDS, ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='9614e53310b1467bd8a23b3ba938f73519165927',
        parent_execution='6a13f1e6a10cee4fad519853835fd256089456e8',
        parent_summary='478ea25268291aeec1c73c4169a0b4a5f04f45950054214ec8eec0e190f3b89d',
        parent_envelope='d6343c4ad4c7149b118183a928810d80215ffac37891b0c6a0282d6ae75f982f',
        question='where do C332 train-consistent first_mean versus native policies rescue or introduce local binding,masked and both-order gate failures',
        seeds=list(SEEDS), arms=list(ARMS), domains=list(DOMAINS),
        matching='exact seed/domain/split/scorer-profile/language/entity-set/fact-order;all successes and failures',
        source_schema='C332 measurements rows seed/arm/score;score original/interior;not C329 flat measurements',
        scorer='unchanged C330 adapted_score/counts/transition;opaque scorer slots mapped to actual input profiles',
        thresholds=dict(accuracy=.90, query_pair_accuracy=.80, evidence_drop=.35, query_drop=.35, both_order=.80),
        changed='analysis of saved measurements only;no models,data,weights,thresholds or checkpoint selection changed',
        gate='diagnostic integrity only;reconstruct every C332 seed flag,failure count and HOLDOUT answer/pair count;preserve negative primary gate',
        nonclaims='gate-cell rescue is not individual-answer rescue;no causal attribution,seed exclusion,coefficient selection or adoption',
        parent_output_files=455, parent_test_proof_files=447, source_count=SOURCE_COUNT, input_count=INPUT_COUNT,
        own_tests=OWN_TESTS, full_tests=FULL_TESTS, modules=MODULES, outputs=list(OUTPUTS),
        parent_semantics='unchanged immediate C332 saved tensor/trace reconstruction under no_neural;older bytes/proofs retained,not older science reruns',
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C333 manifest seal')


def decode_record(record):
    q = localizer()
    require(type(record) is dict and set(record) == {'seed', 'arm', 'score'}
            and type(record['seed']) is int and record['seed'] in SEEDS and record['arm'] in ARMS,
            'C332 measurements record')
    scores = record['score']
    require(type(scores) is dict and set(scores) == {'original', 'interior'}
            and set(scores['original']) == set(map(str, range(2, 7))), 'C332 score wrapper')
    cells, orders, flags, failures = [], [], {}, {}
    for domain in DOMAINS:
        value = scores['interior'] if domain == 'interior4' else scores['original'][domain[-1]]
        cc, oo, passed = q.adapted_score(value, domain)
        tags = dict(seed=record['seed'], arm=record['arm'], domain=domain)
        cells.extend(dict(r, **tags) for r in cc); orders.extend(dict(r, **tags) for r in oo)
        flags[domain] = passed
        failures[domain] = dict(local=sum(not r['passed'] for r in cc), order=sum(not r['passed'] for r in oo))
    state = dict(seed=record['seed'], arm=record['arm'], original_pass={str(n):flags['original'+str(n)] for n in range(2,7)},
                 interior_pass=flags['interior4'], retention_pass=all(flags[d] for d in DOMAINS[:-1]), failures=failures)
    return cells, orders, state


def reconcile_counts(cells, states, saved):
    p = parent(); p.check_summary(saved)
    require(blob(states) == blob(saved['seed_results']), 'all parent flags/failure counts')
    for pair in saved['paired_comparisons']:
        for domain in DOMAINS:
            totals = [localizer().counts([r for r in cells if (r['seed'], r['arm'], r['domain'], r['split']) ==
                       (pair['seed'], arm, domain, 'HOLDOUT')], []) for arm in ARMS]
            ref = pair['interior'] if domain == 'interior4' else pair['original_by_length'][domain[-1]]
            a, c = totals
            require(a['rows'] == c['rows'] == ref['answers'] == 288
                    and a['query_pairs'] == c['query_pairs'] == ref['query_pairs'] == 144, 'HOLDOUT denominators')
            require([a['correct'], c['correct'], a['both_query_correct'], c['both_query_correct']] ==
                    [ref[k] for k in ('control_correct','candidate_correct','control_both_correct','candidate_both_correct')],
                    'parent HOLDOUT counts')
            require(c['correct']-a['correct'] == ref['answer_gain'] and
                    c['both_query_correct']-a['both_query_correct'] == ref['query_pair_gain'], 'parent HOLDOUT gains')
    # Individual answer rescue/regression is retained from the raw-verified parent,
    # never reconstructed by pretending aggregate gate cells are individual answers.
    require(saved['candidate_gate'] is False, 'preserve accepted negative gate')


def analyze(metrics, saved):
    q = localizer(); parent().check_summary(saved)
    require(type(metrics) is list and [(r['seed'], r['arm']) for r in metrics] == identities(), 'all ten trained states')
    cells, orders, states = [], [], []
    for record in metrics:
        cc, oo, state = decode_record(record); cells.extend(cc); orders.extend(oo); states.append(state)
    reconcile_counts(cells, states, saved)
    indices = [{(r['seed'],r['arm'],r['domain'],*q.identity(r,order)):r for r in rows}
               for order, rows in ((False,cells),(True,orders))]
    require([len(i) for i in indices] == [WORK['local_cells'],WORK['order_cells']], 'complete unique coordinates')
    transitions = [[], []]
    for seed, domain in itertools.product(SEEDS,DOMAINS):
        for order in (False,True):
            for coordinate in q.expected_keys(order):
                a,c = [indices[int(order)][(seed,arm,domain,*coordinate)] for arm in ARMS]
                tags = {k:a[k] for k in ('seed','domain','split','profile','input_profile','language','entities')}
                if not order: tags['permutation'] = a['permutation']
                transitions[int(order)].append(dict(**tags, **q.transition(a,c,order)))
    strata = []
    for key in itertools.product(ARMS,DOMAINS,q.SPLITS,q.SCORER_PROFILES,q.LANGUAGES):
        fields = ('arm','domain','split','profile','language')
        cc,oo = [[r for r in rows if tuple(r[k] for k in fields) == key] for rows in (cells,orders)]
        strata.append(dict(zip(fields,key,strict=True), input_profile=cc[0]['input_profile'],
            failed_seeds=sorted({r['seed'] for r in cc+oo if not r['passed']}), **q.counts(cc,oo)))
    changes = []
    for domain, criterion in itertools.product(DOMAINS,(*q.CRITERIA,'both_order')):
        rows = [r for r in transitions[int(criterion=='both_order')] if r['domain']==domain]
        counts = {k:sum(criterion in r[k] for r in rows) for k in ('rescued','regressed','persistent','stable_pass')}
        changes.append(dict(domain=domain,criterion=criterion,pairs=len(rows),**counts))
    result = dict(diagnostic_complete=True, parent_validation_summary=saved, strata=strata, transition_summary=changes, **WORK)
    check_summary(result)
    return dict(cells=cells,two_order=orders), dict(local=transitions[0],two_order=transitions[1]), result


def check_summary(v):
    q = localizer(); parent().check_summary(v['parent_validation_summary'])
    require(v['diagnostic_complete'] is True and v['parent_validation_summary']['candidate_gate'] is False
            and all(type(v[k]) is int and v[k]==n for k,n in WORK.items()), 'diagnostic work/parent verdict')
    fields = ('arm','domain','split','profile','language')
    require([tuple(r[k] for k in fields) for r in v['strata']] ==
            list(itertools.product(ARMS,DOMAINS,q.SPLITS,q.SCORER_PROFILES,q.LANGUAGES)), 'all strata')
    for r in v['strata']:
        require(type(r['cells']) is int and r['cells']==30 and type(r['order_cells']) is int and r['order_cells']==15,
                'stratum size')
        require(set(r['patterns'])==set(q.PATTERNS) and set(r['criteria'])==set(q.CRITERIA), 'all criteria/patterns')
        for value in [r['failed_cells'],*r['patterns'].values(),*r['criteria'].values()]: q.integer(value,0,30,'cell count')
        q.integer(r['failed_order_cells'],0,15,'order count')
        require(sum(r['patterns'].values())==30 and r['failed_cells']==30-r['patterns']['pass'], 'exclusive pattern counts')
        n = 16 if r['split']=='TRAIN' else 8
        require(type(r['rows']) is int and r['rows']==30*n and type(r['query_pairs']) is int and r['query_pairs']==15*n,
                'stratum denominators')
        q.integer(r['correct'],0,r['rows'],'correct'); q.integer(r['both_query_correct'],0,r['query_pairs'],'both correct')
        profiles = q.INTERIOR_PROFILES if r['domain']=='interior4' else q.ORIGINAL_PROFILES
        require(r['input_profile']==profiles[q.SCORER_PROFILES.index(r['profile'])]
                and r['failed_seeds']==sorted(set(r['failed_seeds']))
                and all(type(seed) is int and seed in SEEDS for seed in r['failed_seeds']), 'profile/seed semantics')
    require([(r['domain'],r['criterion']) for r in v['transition_summary']] ==
            list(itertools.product(DOMAINS,(*q.CRITERIA,'both_order'))), 'transition inventory')
    for r in v['transition_summary']:
        n = 180 if r['criterion']=='both_order' else 360
        require(type(r['pairs']) is int and r['pairs']==n, 'matched gate denominator')
        values = [q.integer(r[k],0,n,'transition count') for k in ('rescued','regressed','persistent','stable_pass')]
        require(sum(values)==n, 'transition conservation')
        failed = [sum(z['failed_order_cells'] if r['criterion']=='both_order' else z['criteria'][r['criterion']]
                  for z in v['strata'] if z['arm']==arm and z['domain']==r['domain']) for arm in ARMS]
        require(failed==[r['rescued']+r['persistent'],r['regressed']+r['persistent']], 'transition/stratum reconciliation')


def load_parent_measurements(folder, read):
    return read(folder/'measurements.json'), read(folder/'validation-summary.json')


def run_diagnostic(out, parent_out, read):
    inputs = load_parent_measurements(parent_out,read); before = digest(inputs)
    localization,transitions,result = analyze(*inputs)
    require(digest(inputs)==before, 'source JSON mutation')
    for name,value in zip(OUTPUTS,(manifest(),localization,transitions,result),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(value))
    return result


def semantic_recheck(out, parent_out, read):
    localization,transitions,result = analyze(*load_parent_measurements(parent_out,read))
    for name,value in zip(OUTPUTS,(manifest(),localization,transitions,result),strict=True):
        require(blob(read(out/name))==blob(value), 'saved diagnostic reconstruction:'+name)
    return result
