"""C343: localize saved mixed-length gates and every paired normal prediction."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import re
import torch

EXPERIMENT_ID = 'C343-v5b-saved-mixed-length-localization'
STAGE = 'V5-B-SAVED-MIXED-LENGTH-LOCALIZATION'
SEEDS = tuple(range(342001, 342006))
ARMS = ('original5', 'mixed45')
DOMAINS = ('original2', 'original3', 'original4', 'original5', 'original6', 'interior4')
STATE_KEYS = ('seed','arm','original_pass','interior_pass','retention_pass','failures')
OWN = ('fold_lm/v05_benchmarks/model_c343_saved_mixed_length_localization.py',
       'tools/c343_execution.py', 'tests_lm/test_v05_c343_saved_mixed_length_localization.py',
       'tests_lm/test_v05_c343_execution.py', 'tools/run_c343.ps1', 'tools/invoke_c343.ps1',
       'docs/experiment-ledger-addendum-c343-preregistration.md')
OUTPUTS = ('diagnostic-plan.json','localization.json','transitions.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 64, 6442, 237
SOURCE_COUNT, INPUT_COUNT = 923, 7693
WORK = dict(checkpoint_records=10,domain_records=60,local_cells=4320,order_cells=2160,
    local_transitions=2160,order_transitions=1080,normal_answers=51840,answer_transitions=25920,
    query_pair_transitions=12960,normal_support_summaries=120,normal_transition_summaries=60,
    train_steps=0,model_forward_calls=0,gradient_calls=0,optimizer_steps=0,
    model_state_loads=0,new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = '7e5de7e3040acd3d7aff1a748e8b7b97d36461badaa0c65c612b3f3a5e3c12d6'
EXPOSURES = {'original5':dict(original2=200,original3=200,original4=0,original5=100,original6=0,interior4=100),
             'mixed45':dict(original2=200,original3=200,original4=50,original5=50,original6=0,interior4=100)}
CHANGES = ('rescued','regressed','persistent_failure','stable_correct')



def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c342_mixed_length45_training')


def localizer():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c330_saved_gate_localization')


def identities():
    return list(itertools.product(SEEDS,ARMS))


def training_exposure(arm, domain, split):
    require(arm in ARMS and domain in DOMAINS and split in ('TRAIN','HOLDOUT'), 'exposure coordinate')
    presentations = EXPOSURES[arm][domain]
    seen = presentations > 0; values_seen = split == 'TRAIN'
    return dict(name_family_seen_in_training=seen,value_combination_seen_in_training=values_seen,
        normal_prompt_seen_in_training=seen and values_seen,masked_views_seen_in_training=False,
        domain_presentations_per_logical_train_row=presentations,
        domain_presentations_per_logical_row=presentations if values_seen else 0)


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base='50c277fff5242244dd82a87d392e543dc8c3594f',
        parent_execution='e379de3ff300dd01381eeb90055c017c87ead670',
        parent_summary='47862c134f7f3be25784a88694e0bc1e29041772c025006c256673dc83695775',
        parent_envelope='6d8e1ac497fd28f0c6e58fa2770526619fc0bbc47de158ab3803bcbc7559481a',
        question='where do saved mixed45 gains,regressions and failed binding/masked/both-order gates arise relative to actual arm-specific training exposure',
        seeds=list(SEEDS),arms=list(ARMS),domains=list(DOMAINS),
        source_schema='C342 measurements seed/arm/score plus fold-c342-evaluations-v1 records;explicit eight-field parent seed projection retains full support/token/paired summary',
        parent_state_keys=[*STATE_KEYS,'support','training_nonpadding_tokens'],
        matching='all seeds/domains/splits/profiles/languages/entity sets/value pairs/fact orders/queries;all successes and failures',
        scorer='immutable C330 numeric adapted_score/counts/transition;child replaces copied old exposure annotations only',
        exposures={arm:dict(value) for arm,value in EXPOSURES.items()},
        exposure_unit='domain presentations per canonical logical TRAIN row across ALL profiles,not presentations of one literal prompt;HOLDOUT values and every masked view never fitted',
        exposure='original5 sees original2/3/5+interior4;mixed45 sees original2/3/4/5+interior4;original6 untrained in both',
        thresholds=dict(accuracy=.90,query_pair_accuracy=.80,evidence_drop=.35,query_drop=.35,both_order=.80),
        deficits='max(0,unchanged threshold-value);descriptive only,no tolerance or ranking gate',
        raw_prediction='immutable C337.audit_logits,first-index all256 argmax;correct/wrong_observed/absent_digit/outside_catalog;no value filter or repaired prediction',
        transitions='25920 matched individual answers and12960 both-query pairs,TRAIN/HOLDOUT separately;four correctness transitions plus full4x4answer-kind matrices',
        summaries='120 seed/arm/domain/split support summaries and60 seed/domain/split answer/query-pair summaries;all three profiles and both languages included',
        changed='saved evaluation analysis only;no fitting,forward,state loading,new prompt,filter,checkpoint selection or threshold change',
        gate='diagnostic integrity only;all C342 flags/cell counts/normal HOLDOUT support and individual answer/pair transitions reproduced;preserve parent candidatefalse/eligible2',
        nonclaims='cell rescue is not answer rescue;net gains can hide row regressions;localization is not causal attribution or proof of value-pair shortcut',
        parent_output_files=481,parent_test_proof_files=473,source_count=SOURCE_COUNT,input_count=INPUT_COUNT,
        own_tests=OWN_TESTS,full_tests=FULL_TESTS,modules=MODULES,outputs=list(OUTPUTS),
        console='all failed gate cells from both arms plus all120normal support and60normal transition summaries',
        raw_loading='one saved evaluation bundle read per diagnostic/reconstruction pass;no model objects or checkpoint state loads;parent reconstruction and software tests separately scoped',
        parent_semantics='unchanged C342 four-argument saved logits/trace/token reconstruction under no_neural;ancestor bytes/proofs retained without ancestor science reruns',
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C343 manifest seal')


def parent_projection(saved):
    """Project known C342 writer fields, validating rather than discarding its extras."""
    p = parent(); p.check_summary(saved)
    require(type(saved) is dict and set(saved) == {*p.WORK,'candidate_gate','eligible_seed_count',
        'paired_conditions_valid','all_replays','evaluation_policy','seed_results','paired_comparisons'}, 'C342 summary writer keys')
    require(saved['candidate_gate'] is False and type(saved['eligible_seed_count']) is int
            and saved['eligible_seed_count'] == 2, 'preserve accepted C342 negative/eligible2')
    pair_keys = {'seed','control_full_pass','candidate_full_pass','four_answer_gain','four_pair_gain',
                 'six_answer_gain','six_pair_gain','short_answer_gain','short_pair_gain',
                 'interior_answer_gain','interior_pair_gain','original_by_length','interior'}
    require(all(type(pair) is dict and set(pair) == pair_keys for pair in saved['paired_comparisons']), 'C342 paired writer keys')
    result = []
    for row in saved['seed_results']:
        require(type(row) is dict and set(row) == {*STATE_KEYS,'support','training_nonpadding_tokens'}, 'C342 seed writer keys')
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
            and type(record['seed']) is int and record['seed'] in SEEDS and record['arm'] in ARMS, 'C342 measurements record')
    scores = record['score']
    require(type(scores) is dict and set(scores) == {'original','interior'}
            and set(scores['original']) == set(map(str,range(2,7))), 'C342 score wrapper')
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


def localize(metrics, saved):
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
    check_gate_summary(result)
    return dict(cells=cells,two_order=orders),dict(local=transitions[0],two_order=transitions[1]),result


def check_gate_summary(v):
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
        require(all(type(r[k]) is type(expected[k]) and r[k] == expected[k] for k in expected), 'arm-specific training exposure')
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


def audit():
    return parent().support().audit()


def profiles(domain):
    require(domain in DOMAINS, 'normal domain')
    q = localizer()
    return q.INTERIOR_PROFILES if domain == 'interior4' else q.ORIGINAL_PROFILES


def correctness_transition(control, candidate):
    require(type(control) is type(candidate) is bool, 'correctness booleans')
    return ('stable_correct' if control else 'rescued') if candidate else ('regressed' if control else 'persistent_failure')


def check_archive(archive, data, metrics, cx):
    p = parent().previous(); base = p.source().base()
    cx[-1].c.p267.validate_data(data)
    require(type(archive) is dict and set(archive) == {'schema','records'}
            and archive['schema'] == 'fold-c342-evaluations-v1', 'C342 evaluation archive')
    records = archive['records']
    require(type(records) is list and [(r['seed'],r['arm']) for r in records] == identities(), 'all saved evaluation states')
    require(type(metrics) is list and [(r['seed'],r['arm']) for r in metrics] == identities(), 'measurement/archive cohort')
    for record,measurement in zip(records,metrics,strict=True):
        require(set(record) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and type(record['state_sha256']) is str and re.fullmatch('[0-9a-f]{64}',record['state_sha256'])
                and record['evaluation_policy'] == 'native_before'
                and set(record['raw']) == set(record['receipts']) == {'evaluation','replay'}, 'saved state metadata')
        for mode in ('evaluation','replay'):
            require(blob(record['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)), 'saved evaluation receipt')
            base.validate_raw(record['raw'][mode],data,cx)
        require(base.replay_error(record['raw']['evaluation'],record['raw']['replay'],data,cx) <= 1e-9, 'saved evaluation replay')
        score,_ = p.readouts().summarize_mode(record['raw']['evaluation'],data,cx)
        require(blob(measurement) == blob(dict(seed=record['seed'],arm=record['arm'],score=score)), 'raw logits/measurements binding')
    return records


def normal_observations(records, data):
    """All normal predictions; labels classify saved outputs and never alter them."""
    base = parent().previous().source().base(); kinds = audit().KINDS
    pairs = {split:base.query_pairs(rows) for split,rows in data.items()}
    observations = {}; reports = []
    for record in records:
        seed,arm = record['seed'],record['arm']; raw = record['raw']['evaluation']
        for domain,split in itertools.product(DOMAINS,localizer().SPLITS):
            rows = data[split]; target = [r['target'] for r in rows]
            other = [48+r['values'][1-r['entities'].index(r['query'])] for r in rows]
            tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
            counts = dict.fromkeys(kinds,0); both = 0
            for profile in profiles(domain):
                items = audit().audit_logits(tree[split][profile]['normal'],target,other)
                compact = [{k:item[k] for k in ('prediction','kind','target','other')} for item in items]
                key = seed,arm,domain,split,profile
                require(key not in observations and len(compact) == len(rows), 'unique normal source block')
                observations[key] = compact
                for item in compact: counts[item['kind']] += 1
                both += sum(compact[i]['kind'] == compact[j]['kind'] == 'correct' for i,j in pairs[split])
            reports.append(dict(seed=seed,arm=arm,domain=domain,split=split,answers=3*len(rows),
                query_pairs=3*len(pairs[split]),both_query_correct=both,**counts,**training_exposure(arm,domain,split)))
    require(sum(len(rows) for rows in observations.values()) == WORK['normal_answers'], 'all normal observations')
    return observations,pairs,reports


def paired_normal(data, observations, pairs):
    kinds = audit().KINDS; answers,pair_rows,reports = [],[],[]
    for seed,domain,split in itertools.product(SEEDS,DOMAINS,localizer().SPLITS):
        rows = data[split]; answer_changes = dict.fromkeys(CHANGES,0); pair_changes = dict.fromkeys(CHANGES,0)
        matrix = {a:dict.fromkeys(kinds,0) for a in kinds}; correct = [0,0]; both = [0,0]; changed = 0
        exposure = {name:training_exposure(arm,domain,split) for name,arm in zip(('control_exposure','candidate_exposure'),ARMS,strict=True)}
        for index,profile in enumerate(profiles(domain)):
            left,right = [observations[seed,arm,domain,split,profile] for arm in ARMS]
            require(len(left) == len(right) == len(rows), 'paired source rows')
            tags = dict(seed=seed,domain=domain,split=split,profile=localizer().SCORER_PROFILES[index],input_profile=profile)
            for row,a,b in zip(rows,left,right,strict=True):
                require(a['target'] == b['target'] == row['target'] and a['other'] == b['other'], 'paired answer identities')
                flags = a['kind'] == 'correct',b['kind'] == 'correct'
                change = correctness_transition(*flags); answer_changes[change] += 1
                matrix[a['kind']][b['kind']] += 1; changed += a['prediction'] != b['prediction']
                for i,flag in enumerate(flags): correct[i] += flag
                coordinate = {k:row[k] for k in ('language','entities','values','permutation','query')}
                answers.append(dict(**tags,**coordinate,row_id=row['id'],target=a['target'],other=a['other'],
                    control={k:a[k] for k in ('prediction','kind')},candidate={k:b[k] for k in ('prediction','kind')},
                    transition=change,prediction_changed=a['prediction'] != b['prediction'],**exposure))
            for i,j in pairs[split]:
                row = rows[i]; members = [rows[i],rows[j]]
                require(all(row[k] == rows[j][k] for k in ('language','entities','values','permutation'))
                        and [r['query'] for r in members] == row['entities'], 'both-query pair identity')
                groups = [[items[i],items[j]] for items in (left,right)]
                flags = [all(item['kind'] == 'correct' for item in group) for group in groups]
                change = correctness_transition(*flags); pair_changes[change] += 1
                for k,flag in enumerate(flags): both[k] += flag
                pair_rows.append(dict(**tags,**{k:row[k] for k in ('language','entities','values','permutation')},
                    row_ids=[r['id'] for r in members],targets=[r['target'] for r in members],
                    control_predictions=[r['prediction'] for r in groups[0]],candidate_predictions=[r['prediction'] for r in groups[1]],
                    control_kinds=[r['kind'] for r in groups[0]],candidate_kinds=[r['kind'] for r in groups[1]],
                    control_both_correct=flags[0],candidate_both_correct=flags[1],transition=change,**exposure))
        reports.append(dict(seed=seed,domain=domain,split=split,answers=3*len(rows),query_pairs=3*len(pairs[split]),
            control_correct=correct[0],candidate_correct=correct[1],control_both_correct=both[0],candidate_both_correct=both[1],
            answer_gain=correct[1]-correct[0],query_pair_gain=both[1]-both[0],
            rescued=answer_changes['rescued'],regressed=answer_changes['regressed'],
            pair_rescued=pair_changes['rescued'],pair_regressed=pair_changes['regressed'],
            answer_changes=answer_changes,query_pair_changes=pair_changes,kind_transitions=matrix,
            predictions_changed=changed,**exposure))
    require((len(answers),len(pair_rows),len(reports)) ==
            (WORK['answer_transitions'],WORK['query_pair_transitions'],WORK['normal_transition_summaries']), 'complete normal transitions')
    return answers,pair_rows,reports


def check_exposure(row, expected):
    require(all(k in row and type(row[k]) is type(v) and row[k] == v for k,v in expected.items()), 'exact training exposure')


def check_normal_summary(v):
    q = localizer(); kinds = audit().KINDS; reports = v['normal_support']; changes = v['normal_transition_summary']
    support_keys = ('seed','arm','domain','split')
    require([tuple(r[k] for k in support_keys) for r in reports] == list(itertools.product(SEEDS,ARMS,DOMAINS,q.SPLITS)), 'normal support coverage')
    require([(r['seed'],r['domain'],r['split']) for r in changes] == list(itertools.product(SEEDS,DOMAINS,q.SPLITS)), 'normal transition coverage')
    source = {(r['seed'],r['arm']):r for r in v['parent_validation_summary']['seed_results']}
    support_index = {tuple(r[k] for k in support_keys):r for r in reports}
    for r in reports:
        n = 576 if r['split'] == 'TRAIN' else 288
        require(type(r['answers']) is int and r['answers'] == n and type(r['query_pairs']) is int and r['query_pairs'] == n//2, 'normal report denominator')
        q.integer(r['both_query_correct'],0,n//2,'normal report query pairs')
        require(sum(q.integer(r[k],0,n,'normal kind count') for k in kinds) == n, 'normal kind partition')
        require(2*r['both_query_correct'] <= r['correct'] <= r['query_pairs']+r['both_query_correct'], 'normal pair/answer feasibility')
        check_exposure(r,training_exposure(r['arm'],r['domain'],r['split']))
        if r['split'] == 'HOLDOUT':
            expected = source[r['seed'],r['arm']]['support'][r['domain']]
            require({k:r[k] for k in ('answers',*kinds)} == expected, 'parent normal support counts')
    for r in changes:
        a,b = [support_index[r['seed'],arm,r['domain'],r['split']] for arm in ARMS]
        n,m = a['answers'],a['query_pairs']
        for key,wanted in (('answers',n),('query_pairs',m),('control_correct',a['correct']),('candidate_correct',b['correct']),
                           ('control_both_correct',a['both_query_correct']),('candidate_both_correct',b['both_query_correct'])):
            require(type(r[key]) is int and r[key] == wanted, 'normal transition/support binding')
        for key,budget,ca,cb in (('answer_changes',n,a['correct'],b['correct']),
                                ('query_pair_changes',m,a['both_query_correct'],b['both_query_correct'])):
            z = r[key]
            require(set(z) == set(CHANGES) and sum(q.integer(z[k],0,budget,'normal change count') for k in CHANGES) == budget, 'normal transition conservation')
            require(ca == z['stable_correct']+z['regressed'] and cb == z['stable_correct']+z['rescued'], 'normal correctness transition totals')
        require(all(type(r[k]) is int for k in ('answer_gain','query_pair_gain','rescued','regressed','pair_rescued','pair_regressed')), 'normal gain types')
        require(r['answer_gain'] == b['correct']-a['correct'] == r['rescued']-r['regressed']
                and r['query_pair_gain'] == b['both_query_correct']-a['both_query_correct'] == r['pair_rescued']-r['pair_regressed']
                and [r['rescued'],r['regressed']] == [r['answer_changes'][k] for k in ('rescued','regressed')]
                and [r['pair_rescued'],r['pair_regressed']] == [r['query_pair_changes'][k] for k in ('rescued','regressed')], 'normal gains/individual transitions')
        matrix = r['kind_transitions']
        require(set(matrix) == set(kinds) and all(set(matrix[k]) == set(kinds) for k in kinds), 'all sixteen kind transitions')
        for kind in kinds:
            require(sum(q.integer(matrix[kind][k],0,n,'kind transition count') for k in kinds) == a[kind]
                    and sum(matrix[k][kind] for k in kinds) == b[kind], 'kind transition margins')
        require(matrix['correct']['correct'] == r['answer_changes']['stable_correct'], 'correct-kind transition binding')
        changed = q.integer(r['predictions_changed'],0,n,'changed predictions')
        require(changed >= r['rescued']+r['regressed'] and changed >= sum(matrix[x][y] for x in kinds for y in kinds if x != y), 'prediction/label transition bound')
        for name,arm in zip(('control_exposure','candidate_exposure'),ARMS,strict=True):
            check_exposure(r[name],training_exposure(arm,r['domain'],r['split']))
        if r['split'] == 'HOLDOUT':
            pair = next(p for p in v['parent_validation_summary']['paired_comparisons'] if p['seed'] == r['seed'])
            expected = pair['interior'] if r['domain'] == 'interior4' else pair['original_by_length'][r['domain'][-1]]
            require({k:r[k] for k in expected} == expected, 'parent individual answer/query-pair transitions')
    require((len(reports),len(changes),sum(r['answers'] for r in reports),sum(r['answers'] for r in changes),sum(r['query_pairs'] for r in changes)) ==
            (WORK['normal_support_summaries'],WORK['normal_transition_summaries'],WORK['normal_answers'],WORK['answer_transitions'],WORK['query_pair_transitions']), 'normal inventory')


def check_summary(value):
    check_gate_summary(value); check_normal_summary(value)


def analyze(metrics, saved, data, archive, cx):
    localization,transitions,value = localize(metrics,saved)
    records = check_archive(archive,data,metrics,cx)
    observations,pairs,reports = normal_observations(records,data)
    answers,pair_rows,changes = paired_normal(data,observations,pairs)
    for row in reports:
        cells = [r for r in localization['cells'] if all(r[k] == row[k] for k in ('seed','arm','domain','split'))]
        counts = localizer().counts(cells,[])
        require([counts[k] for k in ('rows','correct','query_pairs','both_query_correct')] ==
                [row[k] for k in ('answers','correct','query_pairs','both_query_correct')], 'raw normal/local gate counts')
    transitions.update(normal_answers=answers,query_pairs=pair_rows)
    value.update(normal_support=reports,normal_transition_summary=changes)
    check_summary(value)
    return localization,transitions,value


def load_inputs(parent_out, data_out, cx, read):
    p = parent().previous(); base = p.source().base()
    data,old,new = p.load_data(data_out,read)
    require(base.digest(data) == base.DATA_SHA and base.digest(old) == base.PROMPTS_SHA
            and base.digest(new) == base.digest(cx[2].new_prompts(data)), 'canonical diagnostic inputs')
    cx[-1].c.p267.validate_data(data); cx[2].check_prompts(data,old,new,cx[3],cx[-1])
    archive = torch.load(parent_out/'evaluations.pt',map_location='cpu',weights_only=True)
    return read(parent_out/'measurements.json'),read(parent_out/'validation-summary.json'),data,archive


def reconstructed(parent_out, data_out, cx, read):
    metrics,saved,data,archive = load_inputs(parent_out,data_out,cx,read)
    before = parent().previous().state_hash((metrics,saved,data,archive))
    result = analyze(metrics,saved,data,archive,cx)
    require(parent().previous().state_hash((metrics,saved,data,archive)) == before, 'source JSON/logit mutation')
    return result


def run_diagnostic(out, parent_out, data_out, cx, read):
    localization,transitions,result = reconstructed(parent_out,data_out,cx,read)
    for name,value in zip(OUTPUTS,(manifest(),localization,transitions,result),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(value))
    return result


def semantic_recheck(out, parent_out, data_out, cx, read):
    localization,transitions,result = reconstructed(parent_out,data_out,cx,read)
    for name,value in zip(OUTPUTS,(manifest(),localization,transitions,result),strict=True):
        require(blob(read(out/name)) == blob(value), 'saved diagnostic reconstruction:'+name)
    return result


def report_failures(out, read, emit):
    """Publish complete gate failures and every normal support/transition summary."""
    value = read(out/'validation-summary.json'); check_summary(value)
    rows = read(out/'localization.json'); inventory = {}; groups = []
    for key,label,size in (('cells','C343 failed local',WORK['local_cells']),('two_order','C343 failed both_order',WORK['order_cells'])):
        require(type(rows[key]) is list and len(rows[key]) == size, 'report coordinate coverage')
        failed = [row for row in rows[key] if not row['passed']]
        inventory['local' if key == 'cells' else 'two_order'] = len(failed); groups.append((label,failed))
    require(inventory == value['failure_inventory'], 'complete failure publication')
    for label,failed in groups:
        for row in failed: emit(label,row)
    emit('C343 failure inventory',inventory)
    for row in value['normal_support']: emit('C343 normal support',row)
    for row in value['normal_transition_summary']: emit('C343 normal transition',row)
    return inventory

