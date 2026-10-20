"""C336: classify saved four-response patterns, without model inference or fitting."""
from __future__ import annotations
from collections import defaultdict
import hashlib
import importlib
import itertools
import json
import re
import torch

EXPERIMENT_ID = 'C336-v5b-saved-query-order-patterns'
STAGE = 'V5-B-SAVED-QUERY-ORDER-PATTERNS'
SEEDS = tuple(range(335001, 335006))
ARMS = ('native', 'alternating')
SPLITS = ('TRAIN', 'HOLDOUT')
LANGUAGES = ('en', 'ja')
DOMAINS = tuple('original'+str(n) for n in range(2, 7))+('interior4',)
CATEGORIES = ('query_correct', 'query_swapped', 'first_fact', 'last_fact',
              'value_lock', 'other_class', 'mixed')
OWN = ('fold_lm/v05_benchmarks/model_c336_saved_query_order_patterns.py',
       'tools/c336_execution.py', 'tests_lm/test_v05_c336_saved_query_order_patterns.py',
       'tools/run_c336.ps1', 'tools/invoke_c336.ps1',
       'docs/experiment-ledger-addendum-c336-preregistration.md')
OUTPUTS = ('audit-plan.json', 'query-order-quads.json', 'transitions.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 32, 6090, 226
SOURCE_COUNT, INPUT_COUNT = 877, 4360
WORK = dict(saved_states=10, normal_answers=51840, query_pairs=25920, order_quads=12960,
            paired_quads=6480, reporting_groups=720, train_steps=0, model_forward_calls=0,
            gradient_calls=0, optimizer_steps=0, model_state_loads=0, new_checkpoint_writes=0,
            network_calls=0)
MANIFEST_SHA = 'e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def previous():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c335_alternating_readout_training')


def identities():
    return list(itertools.product(SEEDS, ARMS))


def profiles(domain):
    require(domain in DOMAINS, 'registered domain')
    return ('u_dominant', 'balanced', 'v_dominant') if domain == 'interior4' else ('repeat', 'shared_prefix', 'shared_suffix')


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='8984740dcc538cf785ca2fdc96db735b9ff8a4a1',
        parent_execution='3b185a97ef86ab911d425620b4e6645fbd0c9f9e',
        parent_summary='6624fc176f349f7688af45da55ac5855951e7094c824201b16fe127b92aa25c4',
        parent_envelope='70f5102a454db4370533f8da2f765d2e4eac6ab29d0bb93f5f4cbe976b9b5ab0',
        question='which query/fact-order behavioral patterns account for C335 errors and paired changes, including broad failure in BOTH arms of335002',
        seeds=list(SEEDS), arms=list(ARMS), domains=list(DOMAINS), splits=list(SPLITS), languages=list(LANGUAGES),
        profiles={d:list(profiles(d)) for d in DOMAINS}, categories=list(CATEGORIES),
        unit='queries A,B in canonical entity order,under fact permutations AB,BA:four saved normal argmax responses',
        categories_rule='exclusive:query_correct,query_swapped,first_fact,last_fact,value_lock;any out-of-two-values=other_class;remaining=mixed',
        labels='ground truth used only for offline scoring;predictions are unchanged torch.argmax,not forced binary or repaired',
        held='all10C335states;both logical splits/languages;all18domain/profile combinations;no seed/policy selection or inference',
        reconciliation='all30parent HOLDOUT contrasts including correct/both-correct/rescued/regressed and gains;full native gates retained unchanged',
        boundary='behavioral taxonomy,not internal mechanism,optimization cause or proof of training-data acquisition;TRAIN includes multiple evaluated name variants',
        outputs=list(OUTPUTS), own_tests=OWN_TESTS, full_tests=FULL_TESTS, modules=MODULES,
        source_count=SOURCE_COUNT, input_count=INPUT_COUNT, parent_files=461,
        gate='diagnostic integrity only;C335 remains valid negative irrespective of pattern counts',
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C336 manifest seal')


def logical_groups(data):
    """Index the unchanged dataset, preserving row positions into saved tensors."""
    require(type(data) is dict and set(data) == set(SPLITS), 'logical split inventory')
    result = {}
    for split, count in zip(SPLITS, (192, 96), strict=True):
        rows = data[split]; require(type(rows) is list and len(rows) == count, 'logical row count')
        groups = defaultdict(dict); seen = set()
        for index, row in enumerate(rows):
            entities, values, order = tuple(row['entities']), tuple(row['values']), tuple(row['permutation'])
            require(row['id'] not in seen, 'duplicate row ID'); seen.add(row['id'])
            require(len(entities) == len(values) == 2 and len(set(entities)) == 2
                    and all(type(v) is int for v in values) and set(values) == {0, 1}
                    and order in (entities, entities[::-1]) and row['query'] in entities
                    and row['language'] in LANGUAGES, 'logical row semantics')
            query = entities.index(row['query']); perm = int(order != entities)
            require(type(row['target']) is int and row['target'] == 48+values[query], 'source target')
            key = (row['language'], entities, values); slot = (perm, query)
            require(slot not in groups[key], 'duplicate query/order slot'); groups[key][slot] = index
        ordered = []
        for key in sorted(groups):
            slots = groups[key]; require(set(slots) == {(0,0),(0,1),(1,0),(1,1)}, 'complete two-query/two-order group')
            ordered.append(dict(language=key[0], entities=list(key[1]), values=list(key[2]),
                                indices=[slots[slot] for slot in ((0,0),(0,1),(1,0),(1,1))]))
        require(len(ordered) == count//4 and all(sum(g['language'] == lang for g in ordered) == count//8
                                                for lang in LANGUAGES), 'balanced language groups')
        result[split] = ordered
    return result


def classify(predictions, targets):
    require(type(predictions) in (list, tuple) and len(predictions) == 4
            and all(type(v) is int and 0 <= v < 256 for v in predictions), 'four byte predictions')
    require(type(targets) in (list, tuple) and len(targets) == 2
            and all(type(v) is int for v in targets) and set(targets) == {48,49}, 'two distinct target values')
    a,b = targets; pred = tuple(predictions); expected = (a,b,a,b)
    patterns = {'query_correct':expected, 'query_swapped':(b,a,b,a),
                'first_fact':(a,a,b,b), 'last_fact':(b,b,a,a)}
    category = next((k for k,v in patterns.items() if pred == v), None)
    if category is None:
        category = ('other_class' if any(v not in (a,b) for v in pred) else
                    'value_lock' if len(set(pred)) == 1 else 'mixed')
    correct = tuple(x == y for x,y in zip(pred,expected,strict=True))
    return dict(category=category, correct=sum(correct), both_correct=int(all(correct[:2]))+int(all(correct[2:])),
        four_correct=int(all(correct)), collapsed_orders=int(pred[0] == pred[1])+int(pred[2] == pred[3]),
        order_stable_queries=int(pred[0] == pred[2])+int(pred[1] == pred[3]),
        other_answers=sum(v not in (a,b) for v in pred))


def transition(a, b):
    require(a['targets'] == b['targets'], 'matched target identities')
    target = a['targets']*2
    old = [v == t for v,t in zip(a['predictions'], target, strict=True)]
    new = [v == t for v,t in zip(b['predictions'], target, strict=True)]
    op = [all(old[:2]),all(old[2:])]; np = [all(new[:2]),all(new[2:])]
    return dict(before=a['category'], after=b['category'], answers=4, query_pairs=2,
        control_correct=sum(old), candidate_correct=sum(new),
        control_both_correct=sum(op), candidate_both_correct=sum(np),
        rescued=sum(not x and y for x,y in zip(old,new)), regressed=sum(x and not y for x,y in zip(old,new)),
        pair_rescued=sum(not x and y for x,y in zip(op,np)), pair_regressed=sum(x and not y for x,y in zip(op,np)),
        answer_gain=sum(new)-sum(old), query_pair_gain=sum(np)-sum(op))


def normal_predictions(raw, domain, split, profile, count):
    block = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
    logits = block[split][profile]['normal']
    require(isinstance(logits,torch.Tensor) and logits.shape == (count,256)
            and logits.dtype == torch.float64 and logits.device.type == 'cpu'
            and bool(torch.isfinite(logits).all()), 'saved normal logits')
    return logits.argmax(-1).tolist()


def aggregate(rows):
    require(rows, 'nonempty stratum')
    result = dict(quads=len(rows), answers=4*len(rows), query_pairs=2*len(rows),
                  categories={k:sum(r['category'] == k for r in rows) for k in CATEGORIES})
    for key in ('correct','both_correct','four_correct','collapsed_orders','order_stable_queries','other_answers'):
        result[key] = sum(r[key] for r in rows)
    return result


def analyze(data, archive, parent, cx):
    p = previous(); p.check_summary(parent)
    require(parent['candidate_gate'] is False and parent['evaluation_policy'] == 'native_before', 'accepted negative parent')
    require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c335-evaluations-v1', 'parent archive schema')
    records = archive['records']; require([(r['seed'],r['arm']) for r in records] == identities(), 'all10saved states')
    index = logical_groups(data); details = []
    for record in records:
        require(set(record) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and re.fullmatch('[0-9a-f]{64}',record['state_sha256']) and record['evaluation_policy'] == 'native_before'
                and set(record['raw']) == set(record['receipts']) == {'evaluation','replay'}, 'parent state record')
        for mode in ('evaluation','replay'):
            p.previous().source().base().validate_raw(record['raw'][mode],data,cx)
            require(blob(record['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)), 'parent forward receipts')
        p.crossed().same_tree(record['raw']['evaluation'],record['raw']['replay'])
        raw = record['raw']['evaluation']
        for domain, split in itertools.product(DOMAINS,SPLITS):
            for profile in profiles(domain):
                pred = normal_predictions(raw,domain,split,profile,len(data[split]))
                for g in index[split]:
                    values = [pred[i] for i in g['indices']]; targets = [48+v for v in g['values']]
                    details.append(dict(seed=record['seed'],arm=record['arm'],domain=domain,split=split,profile=profile,
                        language=g['language'],entities=g['entities'],values=g['values'],
                        row_ids=[data[split][i]['id'] for i in g['indices']],predictions=values,targets=targets,
                        **classify(values,targets)))
    require(len(details) == WORK['order_quads'], 'full quad inventory')
    bykey = {}; strata = defaultdict(list)
    keyfields = ('seed','domain','split','profile','language')
    for row in details:
        key = tuple(row[k] for k in keyfields)+(tuple(row['entities']),tuple(row['values']))
        require((row['arm'],key) not in bykey, 'duplicate quad'); bykey[row['arm'],key] = row
        strata[(row['seed'],row['arm'],row['domain'],row['split'],row['profile'],row['language'])].append(row)
    transitions = []
    for arm,key in sorted(bykey):
        if arm != 'native':
            continue
        a,b = bykey[arm,key],bykey['alternating',key]
        transitions.append(dict(**dict(zip(keyfields,key[:5],strict=True)),entities=list(key[5]),values=list(key[6]),
                                **transition(a,b)))
    require(len(transitions) == WORK['paired_quads'], 'full paired quad inventory')
    reconciled = []
    for pair in parent['paired_comparisons']:
        for domain in DOMAINS:
            rows = [r for r in transitions if r['seed'] == pair['seed'] and r['domain'] == domain and r['split'] == 'HOLDOUT']
            expected = pair['interior'] if domain == 'interior4' else pair['original_by_length'][domain[-1]]
            actual = {k:sum(r[k] for r in rows) for k in expected}
            require(blob(actual) == blob(expected), 'parent HOLDOUT answer/pair/rescue reconciliation')
            reconciled.append(dict(seed=pair['seed'],domain=domain,**actual))
    reports = [dict(seed=k[0],arm=k[1],domain=k[2],split=k[3],profile=k[4],language=k[5],**aggregate(rows))
               for k,rows in sorted(strata.items())]
    value = dict(diagnostic_complete=True,parent_validation_summary=parent,strata=reports,
                 holdout_reconciliation=reconciled,**WORK)
    check_summary(value)
    return details,transitions,value


def check_summary(value):
    require(value['diagnostic_complete'] is True and all(type(value[k]) is int and value[k] == n for k,n in WORK.items()), 'diagnostic work')
    previous().check_summary(value['parent_validation_summary'])
    require(value['parent_validation_summary']['candidate_gate'] is False, 'negative parent preserved')
    expected = {(seed,arm,d,sp,pr,lang) for seed,arm,d,sp,lang in itertools.product(SEEDS,ARMS,DOMAINS,SPLITS,LANGUAGES)
                for pr in profiles(d)}
    rows = value['strata']; keys = [(r['seed'],r['arm'],r['domain'],r['split'],r['profile'],r['language']) for r in rows]
    require(len(rows) == len(set(keys)) == WORK['reporting_groups'] and set(keys) == expected, 'complete strata')
    for r in rows:
        q = 24 if r['split'] == 'TRAIN' else 12
        require(all(type(r[k]) is int for k in ('quads','answers','query_pairs','correct','both_correct','four_correct',
                'collapsed_orders','order_stable_queries','other_answers')), 'integer counts')
        require(r['quads'] == q and r['answers'] == 4*q and r['query_pairs'] == 2*q
                and set(r['categories']) == set(CATEGORIES) and all(type(n) is int and n >= 0 for n in r['categories'].values())
                and sum(r['categories'].values()) == q, 'category partition')
        require(0 <= r['correct'] <= 4*q and 0 <= r['both_correct'] <= 2*q
                and r['four_correct'] == r['categories']['query_correct'] and 0 <= r['collapsed_orders'] <= 2*q
                and 0 <= r['order_stable_queries'] <= 2*q and 0 <= r['other_answers'] <= 4*q, 'outcome bounds')
    require(len(value['holdout_reconciliation']) == 30, 'all30parent contrasts')
    require(sum(r['answers'] for r in rows) == WORK['normal_answers'], 'answer conservation')


def load_and_analyze(source_out, data_out, parent, cx, read):
    data = read(data_out/'dataset.json')
    archive = torch.load(source_out/'evaluations.pt',map_location='cpu',weights_only=True)
    return analyze(data,archive,parent,cx)


def run_diagnostic(out, source_out, data_out, parent, cx, read):
    details,changes,value = load_and_analyze(source_out,data_out,parent,cx,read)
    for name,item in zip(OUTPUTS,(manifest(),details,changes,value),strict=True):
        with (out/name).open('xb') as stream:
            stream.write(blob(item))
    return value


def semantic_recheck(out, source_out, data_out, parent, cx, read):
    details,changes,value = load_and_analyze(source_out,data_out,parent,cx,read)
    for name,item in zip(OUTPUTS,(manifest(),details,changes,value),strict=True):
        require(blob(read(out/name)) == blob(item), 'saved diagnostic reconstruction:'+name)
    return value
