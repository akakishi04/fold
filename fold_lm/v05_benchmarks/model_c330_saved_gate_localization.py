"""C330: preserve fixed C329 gates and localize their saved paired failures.

No neural call, weight loading, fitting, threshold search or new target selection.
Scorer profile names are opaque slots: expose the actual input-template mapping.
"""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math

EXPERIMENT_ID = 'C330-v5b-saved-gate-localization'
STAGE = 'V5-B-SAVED-GATE-LOCALIZATION'
SEEDS = tuple(range(329001, 329006))
ARMS = ('prefix1200', 'extended2400')
DOMAINS = ('original2', 'original3', 'original4', 'original5', 'original6', 'interior4')
SPLITS = ('TRAIN', 'HOLDOUT')
LANGUAGES = ('en', 'ja')
SUBSETS = ((0, 1), (0, 2), (1, 2))
SCORER_PROFILES = ('tripled', 'shared_prefix2', 'shared_suffix2')
ORIGINAL_PROFILES = ('repeat', 'shared_prefix', 'shared_suffix')
INTERIOR_PROFILES = ('u_dominant', 'balanced', 'v_dominant')
CRITERIA = ('accuracy', 'query_pair_accuracy', 'evidence_drop', 'query_drop')
THRESHOLDS = (.90, .80, .35, .35)
PATTERNS = ('pass', 'normal_binding_only', 'mask_only', 'mixed')
OWN = ('fold_lm/v05_benchmarks/model_c330_saved_gate_localization.py',
       'tools/c330_execution.py', 'tests_lm/test_v05_c330_saved_gate_localization.py',
       'tools/run_c330.ps1', 'tools/invoke_c330.ps1',
       'docs/experiment-ledger-addendum-c330-preregistration.md')
OUTPUTS = ('diagnostic-plan.json', 'localization.json', 'transitions.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 48, 5818, 219
SOURCE_COUNT, INPUT_COUNT = 838, 1593
WORK = dict(checkpoint_records=10, domain_records=60, local_cells=4320,
            order_cells=2160, local_transitions=2160, order_transitions=1080,
            train_steps=0, model_forward_calls=0, gradient_calls=0,
            model_state_loads=0, optimizer_steps=0, new_checkpoint_writes=0, network_calls=0)
MANIFEST_SHA = 'f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c329_fixed_budget_extension')


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='a7a36bb212656f08bd8d1c5402512ce28acb1e00',
        parent_execution='f8582ca34bd7e10c7403713e935debe94720dfde',
        parent_summary_sha256='89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a',
        parent_envelope_sha256='6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473',
        question='which unchanged local binding,masked-dependence and both-order gates remain unmet after C329 budget extension, and which matched gates improve or regress',
        seeds=list(SEEDS), arms=list(ARMS), domains=list(DOMAINS), splits=list(SPLITS),
        scorer_profiles=list(SCORER_PROFILES), original_profiles=list(ORIGINAL_PROFILES),
        interior_profiles=list(INTERIOR_PROFILES), languages=list(LANGUAGES), subsets=[list(x) for x in SUBSETS],
        thresholds=dict(zip(CRITERIA, THRESHOLDS, strict=True)), two_order_threshold=.80,
        classification='exclusive pass/normal_binding_only/mask_only/mixed from four unchanged criteria;both-order remains separate',
        matching='exact seed/domain/split/scorer-profile/language/entity-set/fact-order;not positional zip or selected failures',
        gate='integrity only;complete inventories,unchanged numeric criteria and parent flags/counts,deterministic output reconstruction',
        scope='all saved checkpoint domains,including successes;no new fit/forward/replay;parent tensor semantic verification separately scoped',
        nonclaims='failure localization is not a causal attribution;mask-only does not prove shortcut use;TRAIN labels do not make original5/6 trained name lengths',
        inherited_sources=832, inherited_inputs=1577, parent_files=10,
        source_pins=SOURCE_COUNT, protected_inputs=INPUT_COUNT, own_tests=OWN_TESTS,
        focused_tests=FULL_TESTS, modules=MODULES, outputs=list(OUTPUTS),
        historical_exclusion='sole inherited exact C204 mutable-ACTIVE test;no new exclusions/skips',
        parent_semantics='unchanged C329.semantic_recheck over five trajectory/ten checkpoint writer schema under no_neural;no older semantic recursion',
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C330 manifest seal')


def number(value, low, high, name):
    require(type(value) in (int, float) and math.isfinite(value) and low <= value <= high, name)
    return value


def integer(value, low, high, name):
    require(type(value) is int and low <= value <= high, name)
    return value


def failure_flags(values):
    require(set(values) == set(CRITERIA), 'criterion inventory')
    for k in CRITERIA:
        number(values[k], -1 if k.endswith('drop') else 0, 1, 'criterion ' + k)
    return {k: values[k] < threshold for k, threshold in zip(CRITERIA, THRESHOLDS, strict=True)}


def pattern(flags):
    require(set(flags) == set(CRITERIA) and all(type(v) is bool for v in flags.values()), 'failure flag types')
    direct = flags['accuracy'] or flags['query_pair_accuracy']
    masked = flags['evidence_drop'] or flags['query_drop']
    return 'mixed' if direct and masked else 'normal_binding_only' if direct else 'mask_only' if masked else 'pass'


def identity(row, order=False):
    fields = ('split', 'profile', 'language', 'entities') if order else ('split', 'profile', 'language', 'entities', 'permutation')
    return tuple(tuple(row[k]) if k in ('entities', 'permutation') else row[k] for k in fields)


def expected_keys(order=False):
    keys = []
    for split, profile, language, entities in itertools.product(SPLITS, SCORER_PROFILES, LANGUAGES, SUBSETS):
        if order:
            keys.append((split, profile, language, entities))
        else:
            keys.extend((split, profile, language, entities, perm) for perm in (entities, entities[::-1]))
    return keys


def index_rows(rows, order=False):
    require(type(rows) is list and len(rows) == (36 if order else 72), 'complete score coordinates')
    result = {}
    for row in rows:
        require(type(row) is dict, 'score row mapping')
        for k in ('entities',) if order else ('entities', 'permutation'):
            require(type(row[k]) is list and len(row[k]) == 2 and all(type(v) is int for v in row[k]), 'entity coordinate')
        key = identity(row, order)
        require(key not in result, 'duplicate score coordinate'); result[key] = row
    require(set(result) == set(expected_keys(order)), 'unexpected score coordinates')
    return result


def local_cell(row):
    wanted = {'split','profile','language','entities','permutation','rows','correct','accuracy',
              'query_pair_accuracy','collapsed_pairs','pairs','evidence_drop','query_drop','answer_nll','passed'}
    require(set(row) == wanted, 'C270 local writer schema')
    n = 16 if row['split'] == 'TRAIN' else 8
    require(type(row['rows']) is int and row['rows'] == n and type(row['pairs']) is int and row['pairs'] == n//2, 'cell denominators')
    correct = integer(row['correct'], 0, n, 'correct count')
    flags = failure_flags({k: row[k] for k in CRITERIA})
    require(row['accuracy'] == correct/n, 'accuracy/count mismatch')
    pair_value = row['query_pair_accuracy']*(n//2)
    require(pair_value.is_integer() if type(pair_value) is float else type(pair_value) is int, 'fractional pair count')
    both = int(pair_value)
    require(max(0, correct-n//2) <= both <= correct//2, 'both-correct constraints')
    collapse = integer(row['collapsed_pairs'], 0, n//2, 'collapsed pairs')
    require(collapse <= n//2-both, 'correct pair cannot collapse')
    masked = {}
    for name in ('evidence','query'):
        acc = row['accuracy']-row[name+'_drop']; number(acc, 0, 1, 'masked accuracy')
        count = acc*n
        require(count == int(count), 'fractional masked count'); masked[name+'_blind_correct'] = int(count)
    number(row['answer_nll'], 0, float('inf'), 'answer NLL')
    require(type(row['passed']) is bool and row['passed'] is (not any(flags.values())), 'local passed flag')
    return dict(row, both_correct=both, failures=flags, pattern=pattern(flags), **masked)


def order_cell(row, cells):
    require(set(row) == {'split','profile','language','entities','groups','both_correct','accuracy','passed'}, 'C270 order writer schema')
    n = 16 if row['split'] == 'TRAIN' else 8
    require(type(row['groups']) is int and row['groups'] == n, 'order denominator')
    count = integer(row['both_correct'], 0, n, 'order correct count')
    require(type(row['accuracy']) in (int,float) and row['accuracy'] == count/n, 'order accuracy')
    require(type(row['passed']) is bool and row['passed'] is (row['accuracy'] >= .80), 'order passed flag')
    key = identity(row, True); entity = key[-1]
    total = cells[key+(entity,)]['correct']+cells[key+(entity[::-1],)]['correct']
    require(max(0, total-n) <= count <= total//2, 'order count incompatible with normal answers')
    return dict(row, failed=not row['passed'])


def adapted_score(score, domain):
    require(domain in DOMAINS and set(score) == {'cells','two_order','totals','passed'}, 'scorer record schema')
    cells = {k:local_cell(r) for k,r in index_rows(score['cells']).items()}
    orders = {k:order_cell(r,cells) for k,r in index_rows(score['two_order'],True).items()}
    expected_totals = []
    for split, profile, language in itertools.product(SPLITS, SCORER_PROFILES, LANGUAGES):
        selected = [r for k,r in cells.items() if k[:3] == (split,profile,language)]
        expected_totals.append(dict(split=split,profile=profile,language=language,
            **{k:sum(r[k] for r in selected) for k in ('rows','correct','pairs','collapsed_pairs')}))
    require(blob(score['totals']) == blob(expected_totals), 'parent per-profile totals')
    passed = all(r['passed'] for r in (*cells.values(), *orders.values()))
    require(type(score['passed']) is bool and score['passed'] is passed, 'domain passed flag')
    names = INTERIOR_PROFILES if domain == 'interior4' else ORIGINAL_PROFILES
    for row in (*cells.values(), *orders.values()):
        row['input_profile'] = names[SCORER_PROFILES.index(row['profile'])]
        row['name_length'] = 4 if domain == 'interior4' else int(domain[-1])
        row['name_family_seen_in_training'] = domain not in ('original5','original6')
    return [cells[k] for k in expected_keys()], [orders[k] for k in expected_keys(True)], passed


def counts(local, orders):
    return dict(cells=len(local), failed_cells=sum(not r['passed'] for r in local),
        patterns={k:sum(r['pattern'] == k for r in local) for k in PATTERNS},
        criteria={k:sum(r['failures'][k] for r in local) for k in CRITERIA},
        order_cells=len(orders), failed_order_cells=sum(r['failed'] for r in orders),
        rows=sum(r['rows'] for r in local), correct=sum(r['correct'] for r in local),
        query_pairs=sum(r['pairs'] for r in local), both_query_correct=sum(r['both_correct'] for r in local))


def transition(control, candidate, order=False):
    require(identity(control,order) == identity(candidate,order), 'unmatched transition identity')
    keys = ('both_order',) if order else CRITERIA
    before = {'both_order':control['failed']} if order else control['failures']
    after = {'both_order':candidate['failed']} if order else candidate['failures']
    return dict(control_pass=control['passed'], candidate_pass=candidate['passed'],
        rescued=[k for k in keys if before[k] and not after[k]],
        regressed=[k for k in keys if not before[k] and after[k]],
        persistent=[k for k in keys if before[k] and after[k]],
        stable_pass=[k for k in keys if not before[k] and not after[k]])


def analyze(metrics, parent_summary):
    require(type(metrics) is list and [(r['seed'],r['arm']) for r in metrics] == list(itertools.product(SEEDS,ARMS)), 'complete parent checkpoint cohort')
    local, orders, state_flags = [], [], []
    for record in metrics:
        require(set(record) == {'seed','arm','original','interior','single_character'} and set(record['original']) == set(map(str,range(2,7))), 'C329 measurements writer')
        flags = {}
        for domain in DOMAINS:
            score = record['interior'] if domain == 'interior4' else record['original'][domain[-1]]
            cc, oo, passed = adapted_score(score,domain); flags[domain] = passed
            tags = dict(seed=record['seed'],arm=record['arm'],domain=domain)
            local.extend(dict(r,**tags) for r in cc); orders.extend(dict(r,**tags) for r in oo)
        state_flags.append(dict(seed=record['seed'],arm=record['arm'],original_pass={str(n):flags['original'+str(n)] for n in range(2,7)},
            interior_pass=flags['interior4'],retention_pass=all(flags[d] for d in DOMAINS[:-1])))
    require(blob(state_flags) == blob(parent_summary['seed_results']), 'reconstructed parent seed gates')
    key = lambda r,order=False:(r['seed'],r['arm'],r['domain'],*identity(r,order))
    li = {key(r):r for r in local}; oi = {key(r,True):r for r in orders}
    require(len(li) == WORK['local_cells'] and len(oi) == WORK['order_cells'], 'full diagnostic inventory')
    lt, ot = [], []
    for seed,domain in itertools.product(SEEDS,DOMAINS):
        for order,index,dest in ((False,li,lt),(True,oi,ot)):
            for coordinate in expected_keys(order):
                a,c = [index[(seed,arm,domain,*coordinate)] for arm in ARMS]
                tags = {k:a[k] for k in ('seed','domain','split','profile','input_profile','language','entities')}
                if not order: tags['permutation'] = a['permutation']
                dest.append(dict(**tags,**transition(a,c,order)))
    summaries = []
    for arm,domain,split,profile,language in itertools.product(ARMS,DOMAINS,SPLITS,SCORER_PROFILES,LANGUAGES):
        filt = lambda r:(r['arm'],r['domain'],r['split'],r['profile'],r['language']) == (arm,domain,split,profile,language)
        cc,oo = list(filter(filt,local)),list(filter(filt,orders))
        summaries.append(dict(arm=arm,domain=domain,split=split,profile=profile,input_profile=cc[0]['input_profile'],language=language,
            failed_seeds=sorted({r['seed'] for r in cc+oo if not r['passed']}),**counts(cc,oo)))
    require([r['seed'] for r in parent_summary['paired_comparisons']] == list(SEEDS), 'parent paired order')
    paired_success = []
    for i,seed in enumerate(SEEDS):
        pair = parent_summary['paired_comparisons'][i]
        for j,prefix in ((0,'control'),(1,'candidate')):
            flag = state_flags[2*i+j]
            require(pair[prefix+'_interior_pass'] is flag['interior_pass'] and pair[prefix+'_retention_pass'] is flag['retention_pass'], 'parent pair flags')
        gains = {}
        for domain in DOMAINS:
            totals = [counts([r for r in local if (r['seed'],r['arm'],r['domain'],r['split']) == (seed,arm,domain,'HOLDOUT')],[]) for arm in ARMS]
            reference = pair['interior'] if domain == 'interior4' else pair['original_by_length'][domain[-1]]
            a,c = totals
            require(a['rows'] == c['rows'] == reference['answers'] == 288 and a['query_pairs'] == c['query_pairs'] == reference['query_pairs'] == 144, 'paired denominator')
            require([a['correct'],c['correct'],a['both_query_correct'],c['both_query_correct']] ==
                [reference[k] for k in ('control_correct','candidate_correct','control_both_correct','candidate_both_correct')], 'parent deciding counts')
            gains[domain] = c['correct']-a['correct'],c['both_query_correct']-a['both_query_correct']
        inside = gains['interior4']; original = tuple(sum(gains[d][j] for d in DOMAINS[:-1]) for j in (0,1))
        require(inside == (pair['interior_answer_gain'],pair['interior_pair_gain']) and original == (pair['original_answer_gain'],pair['original_pair_gain']), 'parent deciding gains')
        passed = state_flags[2*i+1]['interior_pass'] and state_flags[2*i+1]['retention_pass'] and all(v>0 for v in inside) and all(v>=0 for v in original)
        require(pair['paired_success'] is passed, 'parent fixed composite'); paired_success.append(passed)
    require(parent_summary['candidate_gate'] is all(paired_success) and type(parent_summary['paired_success_count']) is int
            and parent_summary['paired_success_count'] == sum(paired_success), 'parent composite summary')
    transition_summary = []
    for domain in DOMAINS:
        for criterion in (*CRITERIA,'both_order'):
            selected = [r for r in (ot if criterion=='both_order' else lt) if r['domain']==domain]
            row = {k:sum(criterion in r[k] for r in selected) for k in ('rescued','regressed','persistent','stable_pass')}
            require(sum(row.values()) == len(selected), 'transition partition')
            transition_summary.append(dict(domain=domain,criterion=criterion,pairs=len(selected),**row))
    summary = dict(diagnostic_complete=True,parent_candidate_gate=all(paired_success),parent_paired_success_count=sum(paired_success),
        all_parent_gates_reconstructed=True,all_parent_counts_reconstructed=True,
        seed_results=state_flags,strata=summaries,transition_summary=transition_summary,**WORK)
    check_summary(summary)
    return dict(cells=local,two_order=orders),dict(local=lt,two_order=ot),summary


def check_summary(value):
    require(all(type(value[k]) is int and value[k] == v for k,v in WORK.items()), 'diagnostic workload')
    require(all(value[k] is True for k in ('diagnostic_complete','all_parent_gates_reconstructed','all_parent_counts_reconstructed')), 'diagnostic completion')
    require([(r['seed'],r['arm']) for r in value['seed_results']] == list(itertools.product(SEEDS,ARMS)), 'summary cohort')
    require(type(value['parent_candidate_gate']) is bool and type(value['parent_paired_success_count']) is int
            and 0 <= value['parent_paired_success_count'] <= 5
            and value['parent_candidate_gate'] is (value['parent_paired_success_count']==5), 'parent verdict binding')
    for r in value['seed_results']:
        require(set(r['original_pass'])==set(map(str,range(2,7))) and all(type(v) is bool for v in r['original_pass'].values())
                and type(r['interior_pass']) is bool and r['retention_pass'] is all(r['original_pass'].values()), 'summary seed flags')
    expected = list(itertools.product(ARMS,DOMAINS,SPLITS,SCORER_PROFILES,LANGUAGES))
    require([(r['arm'],r['domain'],r['split'],r['profile'],r['language']) for r in value['strata']] == expected, 'summary strata')
    for r in value['strata']:
        require(r['cells']==30 and r['order_cells']==15 and set(r['patterns'])==set(PATTERNS) and set(r['criteria'])==set(CRITERIA), 'stratum inventory')
        for v in [*r['patterns'].values(),*r['criteria'].values(),r['failed_cells']]: integer(v,0,30,'stratum count')
        integer(r['failed_order_cells'],0,15,'stratum order count')
        n=16 if r['split']=='TRAIN' else 8
        require(type(r['rows']) is int and r['rows']==30*n and type(r['query_pairs']) is int
                and r['query_pairs']==15*n, 'stratum row/pair denominators')
        integer(r['correct'],0,r['rows'],'stratum correct');integer(r['both_query_correct'],0,r['query_pairs'],'stratum both-correct')
        require(type(r['failed_seeds']) is list and r['failed_seeds']==sorted(set(r['failed_seeds']))
                and all(type(v) is int and v in SEEDS for v in r['failed_seeds']), 'stratum failed seed set')
        profiles=INTERIOR_PROFILES if r['domain']=='interior4' else ORIGINAL_PROFILES
        require(r['input_profile']==profiles[SCORER_PROFILES.index(r['profile'])], 'summary profile semantics')
        require(sum(r['patterns'].values())==30 and r['failed_cells']==30-r['patterns']['pass'], 'pattern partition')
    require(sum(r['cells'] for r in value['strata'])==WORK['local_cells'] and sum(r['order_cells'] for r in value['strata'])==WORK['order_cells'], 'total strata')
    require([(r['domain'],r['criterion']) for r in value['transition_summary']]==list(itertools.product(DOMAINS,(*CRITERIA,'both_order'))), 'transition summary inventory')
    for r in value['transition_summary']:
        n = 180 if r['criterion']=='both_order' else 360
        require(type(r['pairs']) is int and r['pairs']==n, 'transition denominator')
        values = [integer(r[k],0,n,'transition count') for k in ('rescued','regressed','persistent','stable_pass')]
        require(sum(values)==n,'transition conservation')
        failed=[]
        for arm in ARMS:
            rr=[z for z in value['strata'] if z['arm']==arm and z['domain']==r['domain']]
            failed.append(sum(z['failed_order_cells'] if r['criterion']=='both_order' else z['criteria'][r['criterion']] for z in rr))
        require(failed==[r['rescued']+r['persistent'],r['regressed']+r['persistent']], 'transition/strata reconciliation')


def load_parent_measurements(folder, read):
    metrics = read(folder/'measurements.json'); summary = read(folder/'validation-summary.json')
    return metrics,summary


def run_diagnostic(out, parent_out, read):
    inputs = load_parent_measurements(parent_out,read)
    before = digest(inputs); localization,transitions,summary = analyze(*inputs)
    require(digest(inputs)==before,'parent measurement mutation')
    for name,value in zip(OUTPUTS,(manifest(),localization,transitions,summary),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(value))
    return summary


def semantic_recheck(out, parent_out, read):
    localization,transitions,summary = analyze(*load_parent_measurements(parent_out,read))
    for name,value in zip(OUTPUTS,(manifest(),localization,transitions,summary),strict=True):
        require(blob(read(out/name))==blob(value),'saved diagnostic reconstruction:'+name)
    return summary
