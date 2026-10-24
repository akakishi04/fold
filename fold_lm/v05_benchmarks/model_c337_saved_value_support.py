"""C337: distinguish outside-value competition from within-pair ranking offline."""
from __future__ import annotations
from collections import Counter, defaultdict
import hashlib
import importlib
import itertools
import json
import math
import re
import torch

EXPERIMENT_ID = 'C337-v5b-saved-value-support'
STAGE = 'V5-B-SAVED-VALUE-SUPPORT'
SEEDS = tuple(range(335001, 335006))
ARMS = ('native', 'alternating')
SPLITS = ('TRAIN', 'HOLDOUT')
LANGUAGES = ('en', 'ja')
DOMAINS = tuple('original'+str(n) for n in range(2, 7))+('interior4',)
KINDS = ('correct', 'wrong_observed', 'absent_digit', 'outside_catalog')
ORDERS = ('target_higher', 'tie', 'other_higher')
KEYS = ('seed', 'arm', 'domain', 'split', 'profile', 'language')
OWN = ('fold_lm/v05_benchmarks/model_c337_saved_value_support.py',
       'tools/c337_execution.py', 'tests_lm/test_v05_c337_saved_value_support.py',
       'tools/run_c337.ps1', 'tools/invoke_c337.ps1',
       'docs/experiment-ledger-addendum-c337-preregistration.md')
OUTPUTS = ('audit-plan.json', 'answer-support.json', 'source-reconciliation.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 32, 6122, 227
SOURCE_COUNT, INPUT_COUNT = 883, 4827
DATA_SHA = '1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1'
WORK = dict(saved_states=10, normal_answers=51840, source_quads=12960, reporting_groups=720,
            train_steps=0, model_forward_calls=0, gradient_calls=0, optimizer_steps=0,
            model_state_loads=0, new_checkpoint_writes=0, network_calls=0)
MANIFEST_SHA = '4233762c9dd30360f0173e22e1db6ec697c1d7cafd479fc3ce6c3bad0ca81d26'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c336_saved_query_order_patterns')


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='5f7e434ca76132057036155c7467a15caee91b6c',
        parent_execution='274048a72eea1cbb53ece4ec57708e7de2603e6f',
        parent_summary='31ed3d3e9d45f079bbf4bc200e3a7b5aa82b197cc3f0ded176c01db2b6046b98',
        parent_envelope='39f2afcdf7107d7e070977e7b4e834694ee77bb68d00cf30a46be15c5c519dcb',
        question='do saved errors rank an outside value above both supplied values, or also fail to rank the true supplied value above its alternative',
        seeds=list(SEEDS), arms=list(ARMS), domains=list(DOMAINS), splits=list(SPLITS), languages=list(LANGUAGES),
        kinds=list(KINDS), within_pair_orders=list(ORDERS), dataset_sha256=DATA_SHA,
        raw_prediction='unchanged first-index torch.argmax over all256classes;never restrict candidates or replace outputs',
        margins='target_logit-other_supplied_logit;max(supplied_logits)-max(254outside_logits);exact ties reported',
        observed_values='two distinct digits from0..3 per problem;third digit is absent_digit,not wrong_observed',
        changed='offline per-answer decomposition only;all10states/all18domain-profile combinations/allsource rows retained',
        reconciliation='every saved C336quad and all720strata including categories/pairs/other_answers;C335negative retained',
        nonclaim='within-pair rank is label-assisted offline diagnosis,not corrected accuracy,a deployed filter,causal mechanism or new gate',
        parent_files=461, source_count=SOURCE_COUNT, input_count=INPUT_COUNT,
        own_tests=OWN_TESTS, full_tests=FULL_TESTS, modules=MODULES, outputs=list(OUTPUTS),
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C337 manifest seal')


def audit_logits(logits, targets, others):
    """Read logits without mutation, truncation, output selection or probability repair."""
    require(isinstance(logits, torch.Tensor) and logits.ndim == 2 and logits.shape[1] == 256
            and logits.dtype == torch.float64 and logits.device.type == 'cpu'
            and not logits.requires_grad and bool(torch.isfinite(logits).all()), 'finite saved logits')
    n = len(logits)
    require(n > 0 and type(targets) is list and type(others) is list and len(targets) == len(others) == n
            and all(type(t) is int and type(o) is int and 48 <= t <= 51 and 48 <= o <= 51 and t != o
                    for t, o in zip(targets, others, strict=True)), 'observed target identities')
    rows = torch.arange(n); t = torch.tensor(targets); o = torch.tensor(others)
    predictions = logits.argmax(-1).tolist()
    pair_margin = logits[rows,t]-logits[rows,o]
    outside = logits.clone(); outside[rows,t] = -torch.inf; outside[rows,o] = -torch.inf
    support_margin = torch.maximum(logits[rows,t],logits[rows,o])-outside.max(-1).values
    require(bool(torch.isfinite(pair_margin).all()) and bool(torch.isfinite(support_margin).all()), 'finite margins')
    result = []
    for pred, target, other, pm, sm in zip(predictions, targets, others, pair_margin.tolist(), support_margin.tolist(), strict=True):
        kind = ('correct' if pred == target else 'wrong_observed' if pred == other else
                'absent_digit' if 48 <= pred <= 51 else 'outside_catalog')
        order = 'target_higher' if pm > 0 else 'other_higher' if pm < 0 else 'tie'
        require(not (kind == 'correct' and pm < 0) and not (kind == 'wrong_observed' and pm > 0), 'argmax/pair rank consistency')
        require((sm >= 0 if kind in KINDS[:2] else sm <= 0), 'argmax/support rank consistency')
        result.append(dict(prediction=pred,target=target,other=other,kind=kind,within_pair_order=order,
                           pair_margin=pm,support_margin=sm))
    return result


def aggregate(rows):
    require(rows, 'nonempty stratum')
    counts = {k:sum(r['kind'] == k for r in rows) for k in KINDS}
    joint = {k:{o:sum(r['kind'] == k and r['within_pair_order'] == o for r in rows) for o in ORDERS} for k in KINDS}
    support = dict(inside_higher=sum(r['support_margin'] > 0 for r in rows),
                   tie=sum(r['support_margin'] == 0 for r in rows),
                   outside_higher=sum(r['support_margin'] < 0 for r in rows))
    return dict(answers=len(rows),kinds=counts,within_pair=joint,support_rank=support,
                mean_pair_margin=math.fsum(r['pair_margin']/len(rows) for r in rows),
                mean_support_margin=math.fsum(r['support_margin']/len(rows) for r in rows))


def quad_key(row):
    return tuple(row[k] for k in KEYS)+(tuple(row['entities']),tuple(row['values']))


def analyze(data, archive, quads, prior):
    p = parent(); p.check_summary(prior)
    require(digest(data) == DATA_SHA, 'canonical source dataset')
    groups = p.logical_groups(data)
    require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c335-evaluations-v1', 'source archive')
    records = archive['records']
    require([(r['seed'],r['arm']) for r in records] == list(itertools.product(SEEDS,ARMS)), 'all saved states')
    require(type(quads) is list and len(quads) == WORK['source_quads'], 'parent quad count')
    lookup = {quad_key(q):q for q in quads}; require(len(lookup) == len(quads), 'unique parent quads')
    seen = set(); details = []; strata = defaultdict(list); replay_counts = defaultdict(list)
    for record in records:
        require(set(record) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and type(record['state_sha256']) is str and re.fullmatch('[0-9a-f]{64}',record['state_sha256'])
                and record['evaluation_policy'] == 'native_before' and set(record['raw']) == set(record['receipts']) == {'evaluation','replay'}, 'source state record')
        for mode in ('evaluation','replay'):
            require(blob(record['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)), 'source forward receipt')
        # Full114-view and replay validation is part of the mandatory parent reconstruction.
        for domain, split in itertools.product(DOMAINS,SPLITS):
            rows = data[split]; targets = [r['target'] for r in rows]
            others = [48+r['values'][1-r['entities'].index(r['query'])] for r in rows]
            for profile in p.profiles(domain):
                tree = record['raw']['evaluation']['interior'] if domain == 'interior4' else record['raw']['evaluation']['original'][domain[-1]]
                items = audit_logits(tree[split][profile]['normal'],targets,others)
                require(len(items) == len(rows), 'all source rows')
                for row, item in zip(rows,items,strict=True):
                    key = (record['seed'],record['arm'],domain,split,profile,row['language'])
                    value = dict(zip(KEYS,key,strict=True),row_id=row['id'],**item)
                    details.append(value); strata[key].append(value)
                for g in groups[split]:
                    key = (record['seed'],record['arm'],domain,split,profile,g['language'])
                    k = key+(tuple(g['entities']),tuple(g['values']))
                    require(k in lookup and k not in seen, 'parent quad coverage'); seen.add(k)
                    pred = [items[i]['prediction'] for i in g['indices']]; target_pair = [48+v for v in g['values']]
                    reconstructed = dict(zip(KEYS,key,strict=True),entities=g['entities'],values=g['values'],
                        row_ids=[rows[i]['id'] for i in g['indices']],predictions=pred,targets=target_pair,**p.classify(pred,target_pair))
                    require(blob(reconstructed) == blob(lookup[k]), 'exact C336 quad reconstruction')
                    replay_counts[key].append(reconstructed)
    require(len(details) == WORK['normal_answers'] and seen == set(lookup), 'complete answer/quad coverage')
    source_reports = {tuple(r[k] for k in KEYS):r for r in prior['strata']}
    require(len(source_reports) == WORK['reporting_groups'] and set(source_reports) == set(strata), 'source stratum coverage')
    reports = []; reconciled = []
    for key in sorted(strata):
        actual = dict(zip(KEYS,key,strict=True),**p.aggregate(replay_counts[key]))
        require(blob(actual) == blob(source_reports[key]), 'exact C336 stratum reconstruction')
        report = dict(zip(KEYS,key,strict=True),**aggregate(strata[key]))
        require(report['kinds']['correct'] == actual['correct'] and
                report['kinds']['absent_digit']+report['kinds']['outside_catalog'] == actual['other_answers'], 'answer partition reconciliation')
        reports.append(report); reconciled.append(actual)
    gate = prior['parent_validation_summary']
    value = dict(diagnostic_complete=True,parent_counts_preserved=True,parent_candidate_gate=gate['candidate_gate'],
                 parent_eligible_seed_count=gate['eligible_seed_count'],strata=reports,**WORK)
    check_summary(value)
    return details,reconciled,value


def check_summary(value):
    require(set(value) == set(WORK)|{'diagnostic_complete','parent_counts_preserved','parent_candidate_gate','parent_eligible_seed_count','strata'}, 'summary fields')
    require(all(type(value[k]) is int and value[k] == n for k,n in WORK.items())
            and value['diagnostic_complete'] is True and value['parent_counts_preserved'] is True
            and value['parent_candidate_gate'] is False and type(value['parent_eligible_seed_count']) is int
            and value['parent_eligible_seed_count'] == 1, 'diagnostic work/parent')
    expected = {(seed,arm,d,sp,pr,lang) for seed,arm,d,sp,lang in itertools.product(SEEDS,ARMS,DOMAINS,SPLITS,LANGUAGES)
                for pr in parent().profiles(d)}
    rows = value['strata']; keys = [tuple(r[k] for k in KEYS) for r in rows]
    require(len(rows) == len(set(keys)) == WORK['reporting_groups'] and set(keys) == expected, 'complete strata')
    for row in rows:
        n = 96 if row['split'] == 'TRAIN' else 48
        require(type(row['answers']) is int and row['answers'] == n and set(row['kinds']) == set(KINDS)
                and all(type(v) is int and v >= 0 for v in row['kinds'].values()) and sum(row['kinds'].values()) == n, 'kind partition')
        require(set(row['within_pair']) == set(KINDS), 'joint kinds')
        for k in KINDS:
            counts = row['within_pair'][k]
            require(set(counts) == set(ORDERS) and all(type(v) is int and v >= 0 for v in counts.values())
                    and sum(counts.values()) == row['kinds'][k], 'joint partition')
        require(row['within_pair']['correct']['other_higher'] == row['within_pair']['wrong_observed']['target_higher'] == 0, 'impossible rank')
        support = row['support_rank']
        require(set(support) == {'inside_higher','tie','outside_higher'} and all(type(v) is int and v >= 0 for v in support.values())
                and sum(support.values()) == n, 'support partition')
        require(all(type(row[k]) is float and math.isfinite(row[k]) for k in ('mean_pair_margin','mean_support_margin')), 'finite means')
    require(sum(r['answers'] for r in rows) == WORK['normal_answers'], 'answer conservation')


def load_and_analyze(parent_out, source_out, data_out, prior, read):
    data = read(data_out/'dataset.json')
    archive = torch.load(source_out/'evaluations.pt',map_location='cpu',weights_only=True)
    quads = read(parent_out/'query-order-quads.json')
    return analyze(data,archive,quads,prior)


def run_diagnostic(out, parent_out, source_out, data_out, prior, read):
    details,reconciled,value = load_and_analyze(parent_out,source_out,data_out,prior,read)
    for name,item in zip(OUTPUTS,(manifest(),details,reconciled,value),strict=True):
        with (out/name).open('xb') as stream:
            stream.write(blob(item))
    return value


def semantic_recheck(out, parent_out, source_out, data_out, prior, read):
    details,reconciled,value = load_and_analyze(parent_out,source_out,data_out,prior,read)
    for name,item in zip(OUTPUTS,(manifest(),details,reconciled,value),strict=True):
        require(blob(read(out/name)) == blob(item), 'saved support reconstruction:'+name)
    return value
