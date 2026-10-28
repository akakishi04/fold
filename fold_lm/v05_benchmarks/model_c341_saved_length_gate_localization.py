"""C341: localize all saved C340 gates with arm-correct training-exposure metadata."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json

EXPERIMENT_ID = 'C341-v5b-saved-length-gate-localization'
STAGE = 'V5-B-SAVED-LENGTH-GATE-LOCALIZATION'
SEEDS = tuple(range(340001, 340006))
ARMS = ('original4', 'original5')
DOMAINS = ('original2', 'original3', 'original4', 'original5', 'original6', 'interior4')
STATE_KEYS = ('seed','arm','original_pass','interior_pass','retention_pass','failures')
OWN = ('fold_lm/v05_benchmarks/model_c341_saved_length_gate_localization.py',
       'tools/c341_execution.py', 'tests_lm/test_v05_c341_saved_length_gate_localization.py',
       'tests_lm/test_v05_c341_execution.py', 'tools/run_c341.ps1', 'tools/invoke_c341.ps1',
       'docs/experiment-ledger-addendum-c341-preregistration.md')
OUTPUTS = ('diagnostic-plan.json','localization.json','transitions.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 56, 6314, 233
SOURCE_COUNT, INPUT_COUNT = 909, 6723
WORK = dict(checkpoint_records=10,domain_records=60,local_cells=4320,order_cells=2160,
    local_transitions=2160,order_transitions=1080,train_steps=0,model_forward_calls=0,
    gradient_calls=0,optimizer_steps=0,model_state_loads=0,new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = '453b701fcf597a7ea8d38eb7b9457ee97693575f1349fa4903beebe5a1f6a647'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c340_length5_training')


def localizer():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c330_saved_gate_localization')


def identities():
    return list(itertools.product(SEEDS,ARMS))


def training_exposure(arm, domain, split):
    require(arm in ARMS and domain in DOMAINS and split in ('TRAIN','HOLDOUT'), 'exposure coordinate')
    seen = domain in ('original2','original3','interior4',arm)
    values_seen = split == 'TRAIN'
    return dict(name_family_seen_in_training=seen,value_combination_seen_in_training=values_seen,
        normal_prompt_seen_in_training=seen and values_seen,masked_views_seen_in_training=False)


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,
        acceptance_base='20478759b35b930170ac0e723f71da8788349e73',
        parent_execution='15f88d08071ac0b36551fb2f61b3e10dbd0c6445',
        parent_summary='263902957881a2a6a9bff426f540b7e05e8b43be46c1ce6e546e235cf0db7b7e',
        parent_envelope='a4b32eebbff72a6e6637bed1ef23e881dee77e9747b467d80349095909613c9a',
        question='which saved local binding,masked-dependence and both-order conditions improve,regress or persist after original4-to5 TRAIN-token replacement',
        seeds=list(SEEDS),arms=list(ARMS),domains=list(DOMAINS),
        source_schema='C340 measurement rows seed/arm/score;score original/interior;explicit C340 seed-result projection retains support and training token counts in full parent summary',
        parent_state_keys=[*STATE_KEYS,'support','training_nonpadding_tokens'],
        matching='exact seed/domain/split/scorer-profile/language/entity-set/fact-order;all successes and failures',
        scorer='unchanged C330 numeric adapted_score/counts/transition;child overwrites copied exposure metadata with actual C340 arm semantics',
        exposure='original4 sees original2/3/4+interior4;original5 sees original2/3/5+interior4;original6 untrained in both;TRAIN denotes value partition,normal prompt fitted only if its domain was exposed',
        masks='normal-only fitting in C340;masked views were never trained even for TRAIN-value rows in a seen name domain',
        thresholds=dict(accuracy=.90,query_pair_accuracy=.80,evidence_drop=.35,query_drop=.35,both_order=.80),
        deficits='max(0,unchanged threshold-value),descriptive distance only;no tolerance,new threshold or causal score',
        changed='saved measurement analysis only;no fitting,forward,state loading,new prompts,filter,checkpoint selection or gate change',
        gate='diagnostic integrity only;reconcile every C340 state flag/failure count and HOLDOUT correct/pair count;keep parent candidatefalse/eligible2',
        nonclaims='gate-cell rescue differs from answer rescue;masked failure does not establish shortcut causation;no seed exclusion or production adoption',
        parent_output_files=473,parent_test_proof_files=465,source_count=SOURCE_COUNT,input_count=INPUT_COUNT,
        own_tests=OWN_TESTS,full_tests=FULL_TESTS,modules=MODULES,outputs=list(OUTPUTS),
        console='all failed local and both-order cells from both arms with coordinates,values,thresholds,deficits and arm-correct exposure',
        parent_semantics='unchanged immediate C340 saved logits/trace/token reconstruction under no_neural;older bytes/proofs retained without ancestor science reruns',
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C341 manifest seal')


def parent_projection(saved):
    """Project known C340 writer fields, validating rather than discarding its extras."""
    p = parent(); p.check_summary(saved)
    require(type(saved) is dict and set(saved) == {*p.WORK,'candidate_gate','eligible_seed_count',
        'paired_conditions_valid','all_replays','evaluation_policy','seed_results','paired_comparisons'}, 'C340 summary writer keys')
    require(saved['candidate_gate'] is False and type(saved['eligible_seed_count']) is int
            and saved['eligible_seed_count'] == 2, 'preserve accepted C340 negative/eligible2')
    result = []
    for row in saved['seed_results']:
        require(type(row) is dict and set(row) == {*STATE_KEYS,'support','training_nonpadding_tokens'}, 'C340 seed writer keys')
        require(set(row['failures']) == set(DOMAINS), 'parent failure domains')
        for counts in row['failures'].values():
            require(set(counts) == {'local','order'}, 'parent failure count keys')
            localizer().integer(counts['local'],0,72,'parent local failures')
            localizer().integer(counts['order'],0,36,'parent order failures')
        result.append({key:row[key] for key in STATE_KEYS})
    return result


def adapted_score(score, arm, domain):
    """Keep accepted numeric gates; replace only copied C329-era exposure annotations."""
    q = localizer(); cells,orders,passed = q.adapted_score(score,domain)
    result = []
    for is_order,rows in ((False,cells),(True,orders)):
        output = []
        for row in rows:
            copy = dict(row)
            copy.update(training_exposure(arm,domain,row['split']))
            if is_order:
                copy.update(threshold=.80,deficit=max(0.,.80-row['accuracy']),
                    fact_orders=[row['entities'],list(reversed(row['entities']))])
            else:
                thresholds = dict(zip(q.CRITERIA,q.THRESHOLDS,strict=True))
                copy.update(thresholds=thresholds,deficits={k:max(0.,thresholds[k]-row[k]) for k in q.CRITERIA})
            output.append(copy)
        result.append(output)
    return *result,passed


def decode_record(record):
    require(type(record) is dict and set(record) == {'seed','arm','score'}
            and type(record['seed']) is int and record['seed'] in SEEDS and record['arm'] in ARMS, 'C340 measurements record')
    scores = record['score']
    require(type(scores) is dict and set(scores) == {'original','interior'}
            and set(scores['original']) == set(map(str,range(2,7))), 'C340 score wrapper')
    cells,orders,flags,failures = [],[],{},{}
    for domain in DOMAINS:
        value = scores['interior'] if domain == 'interior4' else scores['original'][domain[-1]]
        cc,oo,passed = adapted_score(value,record['arm'],domain)
        tags = dict(seed=record['seed'],arm=record['arm'],domain=domain)
        cells.extend(dict(r,**tags) for r in cc); orders.extend(dict(r,**tags) for r in oo)
        flags[domain] = passed
        failures[domain] = dict(local=sum(not r['passed'] for r in cc),order=sum(not r['passed'] for r in oo))
    state = dict(seed=record['seed'],arm=record['arm'],original_pass={str(n):flags['original'+str(n)] for n in range(2,7)},
        interior_pass=flags['interior4'],retention_pass=all(flags[d] for d in DOMAINS[:-1]),failures=failures)
    return cells,orders,state


def reconcile_counts(cells, states, saved):
    require(blob(states) == blob(parent_projection(saved)), 'all parent flags/failure counts')
    for pair in saved['paired_comparisons']:
        for domain in DOMAINS:
            totals = [localizer().counts([r for r in cells if (r['seed'],r['arm'],r['domain'],r['split']) ==
                (pair['seed'],arm,domain,'HOLDOUT')],[]) for arm in ARMS]
            ref = pair['interior'] if domain == 'interior4' else pair['original_by_length'][domain[-1]]
            a,b = totals
            require(a['rows'] == b['rows'] == ref['answers'] == 288
                    and a['query_pairs'] == b['query_pairs'] == ref['query_pairs'] == 144, 'HOLDOUT denominators')
            require([a['correct'],b['correct'],a['both_query_correct'],b['both_query_correct']] ==
                [ref[k] for k in ('control_correct','candidate_correct','control_both_correct','candidate_both_correct')], 'parent HOLDOUT counts')
            require(b['correct']-a['correct'] == ref['answer_gain'] and
                    b['both_query_correct']-a['both_query_correct'] == ref['query_pair_gain'], 'parent HOLDOUT gains')
    # Individual-answer rescues/regressions stay in the complete raw-verified parent
    # summary. Aggregate gate cells cannot reconstruct those answer identities.


def matched_transition(control, candidate, order=False):
    q = localizer(); value = q.transition(control,candidate,order)
    criteria = ('both_order',) if order else q.CRITERIA
    values = {}
    for key in criteria:
        name = 'accuracy' if order else key
        threshold = .80 if order else q.THRESHOLDS[q.CRITERIA.index(key)]
        values[key] = dict(control=control[name],candidate=candidate[name],threshold=threshold,
            control_deficit=max(0.,threshold-control[name]),candidate_deficit=max(0.,threshold-candidate[name]))
    exposure_keys = tuple(training_exposure(ARMS[0],DOMAINS[0],'TRAIN'))
    return dict(**value,criterion_values=values,
        control_exposure={k:control[k] for k in exposure_keys},candidate_exposure={k:candidate[k] for k in exposure_keys})


def analyze(metrics, saved):
    q = localizer(); parent_projection(saved)
    require(type(metrics) is list and [(r['seed'],r['arm']) for r in metrics] == identities(), 'all ten trained states')
    cells,orders,states = [],[],[]
    for record in metrics:
        cc,oo,state = decode_record(record); cells.extend(cc); orders.extend(oo); states.append(state)
    reconcile_counts(cells,states,saved)
    indices = [{(r['seed'],r['arm'],r['domain'],*q.identity(r,order)):r for r in rows}
               for order,rows in ((False,cells),(True,orders))]
    require([len(i) for i in indices] == [WORK['local_cells'],WORK['order_cells']], 'complete unique coordinates')
    transitions = [[],[]]
    for seed,domain in itertools.product(SEEDS,DOMAINS):
        for order in (False,True):
            for coordinate in q.expected_keys(order):
                a,b = [indices[int(order)][(seed,arm,domain,*coordinate)] for arm in ARMS]
                tags = {k:a[k] for k in ('seed','domain','split','profile','input_profile','language','entities')}
                if not order: tags['permutation'] = a['permutation']
                else: tags['fact_orders'] = a['fact_orders']
                transitions[int(order)].append(dict(**tags,**matched_transition(a,b,order)))
    strata = []
    fields = ('arm','domain','split','profile','language')
    for key in itertools.product(ARMS,DOMAINS,q.SPLITS,q.SCORER_PROFILES,q.LANGUAGES):
        cc,oo = [[r for r in rows if tuple(r[k] for k in fields) == key] for rows in (cells,orders)]
        strata.append(dict(zip(fields,key,strict=True),input_profile=cc[0]['input_profile'],
            **training_exposure(key[0],key[1],key[2]),
            failed_seeds=sorted({r['seed'] for r in cc+oo if not r['passed']}),**q.counts(cc,oo)))
    changes = []
    for domain,criterion in itertools.product(DOMAINS,(*q.CRITERIA,'both_order')):
        rows = [r for r in transitions[int(criterion=='both_order')] if r['domain']==domain]
        counts = {k:sum(criterion in r[k] for r in rows) for k in ('rescued','regressed','persistent','stable_pass')}
        changes.append(dict(domain=domain,criterion=criterion,pairs=len(rows),**counts))
    result = dict(diagnostic_complete=True,parent_validation_summary=saved,seed_results=states,strata=strata,
        transition_summary=changes,failure_inventory=dict(local=sum(not r['passed'] for r in cells),
        two_order=sum(not r['passed'] for r in orders)),**WORK)
    check_summary(result)
    return dict(cells=cells,two_order=orders),dict(local=transitions[0],two_order=transitions[1]),result


def check_summary(v):
    q = localizer(); projected = parent_projection(v['parent_validation_summary'])
    require(v['diagnostic_complete'] is True and blob(v['seed_results']) == blob(projected)
            and all(type(v[k]) is int and v[k] == n for k,n in WORK.items()), 'diagnostic work/parent state')
    fields = ('arm','domain','split','profile','language')
    require([tuple(r[k] for k in fields) for r in v['strata']] ==
        list(itertools.product(ARMS,DOMAINS,q.SPLITS,q.SCORER_PROFILES,q.LANGUAGES)), 'all strata')
    for r in v['strata']:
        require(type(r['cells']) is int and r['cells'] == 30 and type(r['order_cells']) is int and r['order_cells'] == 15, 'stratum size')
        require(set(r['patterns']) == set(q.PATTERNS) and set(r['criteria']) == set(q.CRITERIA), 'all criteria/patterns')
        for value in [r['failed_cells'],*r['patterns'].values(),*r['criteria'].values()]: q.integer(value,0,30,'cell count')
        q.integer(r['failed_order_cells'],0,15,'order count')
        require(sum(r['patterns'].values()) == 30 and r['failed_cells'] == 30-r['patterns']['pass'], 'exclusive pattern counts')
        n = 16 if r['split'] == 'TRAIN' else 8
        require(type(r['rows']) is int and r['rows'] == 30*n and type(r['query_pairs']) is int and r['query_pairs'] == 15*n, 'stratum denominators')
        q.integer(r['correct'],0,r['rows'],'correct'); q.integer(r['both_query_correct'],0,r['query_pairs'],'both correct')
        profiles = q.INTERIOR_PROFILES if r['domain'] == 'interior4' else q.ORIGINAL_PROFILES
        require(r['input_profile'] == profiles[q.SCORER_PROFILES.index(r['profile'])]
                and r['failed_seeds'] == sorted(set(r['failed_seeds']))
                and all(type(seed) is int and seed in SEEDS for seed in r['failed_seeds']), 'profile/seed semantics')
        expected = training_exposure(r['arm'],r['domain'],r['split'])
        require(all(type(r[k]) is bool and r[k] is expected[k] for k in expected), 'arm-specific training exposure')
    require([(r['domain'],r['criterion']) for r in v['transition_summary']] ==
        list(itertools.product(DOMAINS,(*q.CRITERIA,'both_order'))), 'transition inventory')
    for r in v['transition_summary']:
        n = 180 if r['criterion'] == 'both_order' else 360
        require(type(r['pairs']) is int and r['pairs'] == n, 'matched gate denominator')
        values = [q.integer(r[k],0,n,'transition count') for k in ('rescued','regressed','persistent','stable_pass')]
        require(sum(values) == n, 'transition conservation')
        failed = [sum(z['failed_order_cells'] if r['criterion']=='both_order' else z['criteria'][r['criterion']]
            for z in v['strata'] if z['arm']==arm and z['domain']==r['domain']) for arm in ARMS]
        require(failed == [r['rescued']+r['persistent'],r['regressed']+r['persistent']], 'transition/stratum reconciliation')
    for arm,domain in itertools.product(ARMS,DOMAINS):
        group = [r for r in v['strata'] if r['arm']==arm and r['domain']==domain]
        source = [r['failures'][domain] for r in projected if r['arm']==arm]
        require(sum(r['failed_cells'] for r in group) == sum(r['local'] for r in source)
                and sum(r['failed_order_cells'] for r in group) == sum(r['order'] for r in source), 'parent/stratum failure reconciliation')
    inventory = dict(local=sum(r['failed_cells'] for r in v['strata']),two_order=sum(r['failed_order_cells'] for r in v['strata']))
    require(set(v['failure_inventory']) == set(inventory) and all(type(v['failure_inventory'][k]) is int
            and v['failure_inventory'][k] == inventory[k] for k in inventory), 'failure inventory')


def load_parent_measurements(folder, read):
    return read(folder/'measurements.json'),read(folder/'validation-summary.json')


def run_diagnostic(out, parent_out, read):
    inputs = load_parent_measurements(parent_out,read); before = digest(inputs)
    localization,transitions,result = analyze(*inputs)
    require(digest(inputs) == before, 'source JSON mutation')
    for name,value in zip(OUTPUTS,(manifest(),localization,transitions,result),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(value))
    return result


def semantic_recheck(out, parent_out, read):
    localization,transitions,result = analyze(*load_parent_measurements(parent_out,read))
    for name,value in zip(OUTPUTS,(manifest(),localization,transitions,result),strict=True):
        require(blob(read(out/name)) == blob(value), 'saved diagnostic reconstruction:'+name)
    return result


def report_failures(out, read, emit):
    """Emit every failure only after persisted outputs have passed reconstruction."""
    value = read(out/'validation-summary.json'); check_summary(value)
    rows = read(out/'localization.json'); inventory = {}; groups = []
    for key,label,size in (('cells','C341 failed local',WORK['local_cells']),('two_order','C341 failed both_order',WORK['order_cells'])):
        require(type(rows[key]) is list and len(rows[key]) == size, 'report coordinate coverage')
        failed = [row for row in rows[key] if not row['passed']]
        inventory['local' if key == 'cells' else 'two_order'] = len(failed)
        groups.append((label,failed))
    require(inventory == value['failure_inventory'], 'complete failure publication')
    for label,failed in groups:
        for row in failed: emit(label,row)
    emit('C341 failure inventory',inventory)
    return inventory
