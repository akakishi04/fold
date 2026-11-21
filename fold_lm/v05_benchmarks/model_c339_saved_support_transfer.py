"""C339: paired saved support/binding diagnostics; never repairs model answers."""
from __future__ import annotations
from collections import defaultdict
import hashlib
import importlib
import itertools
import json
import math
import re
import torch

EXPERIMENT_ID = 'C339-v5b-saved-support-transfer'
STAGE = 'V5-B-SAVED-SUPPORT-TRANSFER'
SEEDS = tuple(range(338001, 338006))
ARMS = ('native', 'support_loss')
SPLITS = ('TRAIN', 'HOLDOUT')
LANGUAGES = ('en', 'ja')
DOMAINS = tuple('original'+str(n) for n in range(2,7))+('interior4',)
KINDS = ('correct','wrong_observed','absent_digit','outside_catalog')
KEYS = ('seed','arm','domain','split','profile','language')
PAIR_KEYS = ('seed','domain','split','profile','language')
OWN = ('fold_lm/v05_benchmarks/model_c339_saved_support_transfer.py',
       'tools/c339_execution.py','tests_lm/test_v05_c339_saved_support_transfer.py',
       'tools/run_c339.ps1','tools/invoke_c339.ps1',
       'docs/experiment-ledger-addendum-c339-preregistration.md')
OUTPUTS = ('audit-plan.json','answer-components.json','paired-transitions.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 32, 6202, 229
SOURCE_COUNT, INPUT_COUNT = 895, 5769
DATA_SHA = '1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1'
WORK = dict(saved_states=10,normal_answers=51840,paired_answers=25920,
    reporting_groups=720,paired_groups=360,parent_contrasts=30,parent_partitions=60,
    train_steps=0,model_forward_calls=0,gradient_calls=0,optimizer_steps=0,
    model_state_loads=0,new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = '3f3380eac1a0e5d0c076825081c10edfa86bed75e02b2c1b5ee23ebf21dc42f1'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c338_value_support_training')


def auditor():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c337_saved_value_support')


def profiles(domain):
    require(domain in DOMAINS,'registered domain')
    return ('u_dominant','balanced','v_dominant') if domain == 'interior4' else ('repeat','shared_prefix','shared_suffix')


def identities():
    return list(itertools.product(SEEDS,ARMS))


def expected_keys(paired=False):
    if paired:
        return [(s,d,sp,p,l) for s,d,sp in itertools.product(SEEDS,DOMAINS,SPLITS) for p,l in itertools.product(profiles(d),LANGUAGES)]
    return [(s,a,d,sp,p,l) for s,a,d,sp in itertools.product(SEEDS,ARMS,DOMAINS,SPLITS) for p,l in itertools.product(profiles(d),LANGUAGES)]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,
        acceptance_base='928bc539f83a22584e71e99adac7f5031bd480d0',
        parent_execution='f81a49e383e78ff503a4e4c6fe1156e7a8b75849',
        parent_summary='67e369808641a781dd144084a4e1a77d8347a07675740b8c3c694eaedbdf3137',
        parent_envelope='11977e359dbb65236803fb7eaa1d085728a72d27a582dcc2d76d01906e3329e5',
        question='where does support-loss training improve or degrade supplied-value support versus within-pair binding across splits and name domains',
        seeds=list(SEEDS),arms=list(ARMS),domains=list(DOMAINS),splits=list(SPLITS),languages=list(LANGUAGES),
        dataset_sha256=DATA_SHA,changed='saved-logit diagnosis only;all original2..6/interior4 normal views',
        held='all10C338states,allrows/languages/profiles,raw256argmax,exactties,parentgates;no fit/forward/filter/selection',
        components='supportNLL=softplus(logsumexp(254outside)-logsumexp(two supplied));withinNLL=softplus(other-target)',
        ranks='unchanged C337.audit_logits;4x4 answer-kind and3x3 sign transitions;candidate minus native',
        reconciliation='all60HOLDOUTsupportpartitions andall30completepairedcontrasts including rescues/regressions/querypairs',
        boundary='NLLs are retrospective label-assisted measurements,not corrected accuracy or independent samples;no internal causal claim',
        parent_files=467,source_count=SOURCE_COUNT,input_count=INPUT_COUNT,
        own_tests=OWN_TESTS,full_tests=FULL_TESTS,modules=MODULES,outputs=list(OUTPUTS),
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA,'C339 manifest seal')


def components(logits, targets, others):
    items = auditor().audit_logits(logits,targets,others)
    rows = torch.arange(len(items)); t = torch.tensor(targets); o = torch.tensor(others)
    selected = torch.stack((logits[rows,t],logits[rows,o]),dim=1)
    outside = logits.clone(); outside[rows,t] = -torch.inf; outside[rows,o] = -torch.inf
    gap = torch.logsumexp(outside,1)-torch.logsumexp(selected,1)
    require(bool(torch.isfinite(gap).all()),'finite support logmass gap')
    snll = torch.logaddexp(torch.zeros_like(gap),gap)
    within_gap = logits[rows,o]-logits[rows,t]
    wnll = torch.logaddexp(torch.zeros_like(within_gap),within_gap)
    require(bool(torch.isfinite(snll).all()) and bool(torch.isfinite(wnll).all()),'finite NLL components')
    for item,sn,wn in zip(items,snll.tolist(),wnll.tolist(),strict=True):
        require(sn >= 0 and wn >= 0 and math.isfinite(sn+wn),'nonnegative finite components')
        item.update(support_nll=sn,within_nll=wn)
    return items


def aggregate(items):
    result = auditor().aggregate(items)
    result.update(mean_support_nll=math.fsum(v['support_nll']/len(items) for v in items),
                  mean_within_nll=math.fsum(v['within_nll']/len(items) for v in items))
    return result


def sign(value):
    require(type(value) in (int,float) and math.isfinite(value),'finite sign')
    return 'positive' if value > 0 else 'negative' if value < 0 else 'zero'


def transitions(left, right):
    require(len(left) == len(right) and left,'paired stratum')
    require([r['row_id'] for r in left] == [r['row_id'] for r in right]
            and all((a['target'],a['other']) == (b['target'],b['other']) for a,b in zip(left,right,strict=True)),'paired row identities')
    kinds = {a:{b:0 for b in KINDS} for a in KINDS}; signs = ('positive','zero','negative')
    matrices = {field:{a:{b:0 for b in signs} for a in signs} for field in ('pair_margin','support_margin')}
    for a,b in zip(left,right,strict=True):
        kinds[a['kind']][b['kind']] += 1
        for field,matrix in matrices.items(): matrix[sign(a[field])][sign(b[field])] += 1
    means = {}
    for field in ('support_nll','within_nll','pair_margin','support_margin'):
        deltas = [b[field]-a[field] for a,b in zip(left,right,strict=True)]
        require(all(math.isfinite(v) for v in deltas),'finite paired differences')
        means[field] = math.fsum(v/len(deltas) for v in deltas)
    return dict(answers=len(left),kind_matrix=kinds,sign_matrices=matrices,
                mean_delta=means,rescued=sum(kinds[k]['correct'] for k in KINDS[1:]),
                regressed=sum(kinds['correct'][k] for k in KINDS[1:]))


def query_pairs(rows):
    groups = {}
    for i,r in enumerate(rows):
        key = (r['language'],tuple(r['entities']),tuple(r['values']),tuple(r['permutation']))
        group = groups.setdefault(key,{})
        require(r['query'] not in group,'duplicate query'); group[r['query']] = i
    result = []
    for (_,entities,_,_),group in groups.items():
        require(set(group) == set(entities),'incomplete query pair'); result.append(tuple(group[e] for e in entities))
    require(2*len(result) == len(rows),'query pair inventory'); return result


def contrast(left, right, rows):
    require(len(left) == len(right) == 3,'three profiles')
    pairs = query_pairs(rows); answers = [[],[]]; pair_values = [[],[]]; outside = [0,0]
    for arm,trees in enumerate((left,right)):
        for items in trees:
            correct = [r['kind'] == 'correct' for r in items]
            require(len(correct) == len(rows),'all contrast rows')
            answers[arm].extend(correct); pair_values[arm].extend(correct[i] and correct[j] for i,j in pairs)
            outside[arm] += sum(r['kind'] in KINDS[2:] for r in items)
    a,b = answers; pa,pb = pair_values
    return dict(answers=len(a),query_pairs=len(pa),control_correct=sum(a),candidate_correct=sum(b),
        control_both_correct=sum(pa),candidate_both_correct=sum(pb),answer_gain=sum(b)-sum(a),query_pair_gain=sum(pb)-sum(pa),
        rescued=sum(not x and y for x,y in zip(a,b,strict=True)),regressed=sum(x and not y for x,y in zip(a,b,strict=True)),
        pair_rescued=sum(not x and y for x,y in zip(pa,pb,strict=True)),pair_regressed=sum(x and not y for x,y in zip(pa,pb,strict=True)),
        outside_gain=outside[1]-outside[0])


def analyze(data, archive, prior):
    p = parent(); p.check_summary(prior)
    require(prior['candidate_gate'] is False and prior['eligible_seed_count'] == 0,'accepted C338negative')
    require(digest(data) == DATA_SHA,'canonical dataset')
    require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c338-evaluations-v1','C338archive schema')
    records = archive['records']
    require([(r['seed'],r['arm']) for r in records] == identities(),'full ordered cohort')
    details = []; strata = defaultdict(list); indexed = {}
    for record in records:
        require(set(record) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and type(record['state_sha256']) is str and re.fullmatch('[0-9a-f]{64}',record['state_sha256']) and record['evaluation_policy'] == 'native_before'
                and set(record['raw']) == set(record['receipts']) == {'evaluation','replay'},'source record contract')
        for mode in ('evaluation','replay'):
            require(blob(record['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)),'source work receipt')
        for domain,split in itertools.product(DOMAINS,SPLITS):
            rows = data[split]; targets = [r['target'] for r in rows]
            others = [48+r['values'][1-r['entities'].index(r['query'])] for r in rows]
            for profile in profiles(domain):
                def view(mode):
                    raw = record['raw'][mode]
                    tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
                    return tree[split][profile]['normal']
                z,replay = view('evaluation'),view('replay')
                items = components(z,targets,others)
                require(replay.shape == z.shape and replay.dtype == z.dtype and replay.device == z.device
                        and bool(torch.isfinite(replay).all()) and float((z-replay).abs().max()) <= 1e-9
                        and torch.equal(z.argmax(1),replay.argmax(1)),'normal saved replay')
                indexed[record['seed'],record['arm'],domain,split,profile] = items
                for row,item in zip(rows,items,strict=True):
                    key = (record['seed'],record['arm'],domain,split,profile,row['language'])
                    value = dict(zip(KEYS,key,strict=True),row_id=row['id'],**item)
                    details.append(value); strata[key].append(value)
    require(set(strata) == set(expected_keys()) and len(details) == WORK['normal_answers'],'complete answer scope')
    flags = {(r['seed'],r['arm']):r for r in prior['seed_results']}; comparisons = {r['seed']:r for r in prior['paired_comparisons']}
    require(set(flags) == set(identities()) and set(comparisons) == set(SEEDS),'parent cohort')
    reconciled = []
    for seed,domain in itertools.product(SEEDS,DOMAINS):
        arms = []
        for arm in ARMS:
            tree = [indexed[seed,arm,domain,'HOLDOUT',pr] for pr in profiles(domain)]; arms.append(tree)
            items = [r for group in tree for r in group]
            counts = dict(answers=len(items),**{k:sum(v['kind'] == k for v in items) for k in KINDS})
            require(blob(counts) == blob(flags[seed,arm]['support'][domain]),'parent support partition')
        actual = contrast(*arms,data['HOLDOUT'])
        require(blob(actual) == blob(comparisons[seed]['domains'][domain]),'complete parent contrast')
        reconciled.append(dict(seed=seed,domain=domain,**actual))
    reports = [dict(zip(KEYS,k,strict=True),**aggregate(strata[k])) for k in sorted(strata)]
    paired = []
    for seed,domain,split,profile,lang in sorted(expected_keys(True)):
        key = (seed,domain,split,profile,lang)
        paired.append(dict(zip(PAIR_KEYS,key,strict=True),**transitions(
            strata[seed,ARMS[0],domain,split,profile,lang],strata[seed,ARMS[1],domain,split,profile,lang])))
    value = dict(diagnostic_complete=True,parent_counts_preserved=True,parent_candidate_gate=False,parent_eligible_seed_count=0,
                 strata=reports,paired_strata=paired,reconciled_contrasts=reconciled,**WORK)
    check_summary(value); return details,paired,value


def check_summary(v):
    require(set(v) == set(WORK)|{'diagnostic_complete','parent_counts_preserved','parent_candidate_gate',
            'parent_eligible_seed_count','strata','paired_strata','reconciled_contrasts'},'summary schema')
    require(all(type(v[k]) is int and v[k] == n for k,n in WORK.items()) and v['diagnostic_complete'] is True
            and v['parent_counts_preserved'] is True and v['parent_candidate_gate'] is False
            and type(v['parent_eligible_seed_count']) is int and v['parent_eligible_seed_count'] == 0,'work/parent flags')
    reports = {tuple(r[k] for k in KEYS):r for r in v['strata']}
    require(len(v['strata']) == len(reports) == 720 and set(reports) == set(expected_keys()),'all720strata')
    for key,r in reports.items():
        n = 96 if r['split'] == 'TRAIN' else 48
        require(type(r['answers']) is int and r['answers'] == n and set(r['kinds']) == set(KINDS)
                and all(type(x) is int and x >= 0 for x in r['kinds'].values()) and sum(r['kinds'].values()) == n,'answer partition')
        require(set(r['within_pair']) == set(KINDS) and set(r['support_rank']) == {'inside_higher','tie','outside_higher'},'rank keys')
        for kind,row in r['within_pair'].items():
            require(set(row) == {'target_higher','tie','other_higher'} and all(type(x) is int and x >= 0 for x in row.values())
                    and sum(row.values()) == r['kinds'][kind],'joint rank counts')
        require(all(type(x) is int and x >= 0 for x in r['support_rank'].values()) and sum(r['support_rank'].values()) == n,'support ranks')
        for f in ('mean_pair_margin','mean_support_margin','mean_support_nll','mean_within_nll'):
            require(type(r[f]) is float and math.isfinite(r[f]) and ('nll' not in f or r[f] >= 0),'finite means')
    require(len(v['paired_strata']) == 360 and [tuple(r[k] for k in PAIR_KEYS) for r in v['paired_strata']] == sorted(expected_keys(True)),'all360pairedstrata')
    for r in v['paired_strata']:
        s,d,sp,p,l = (r[k] for k in PAIR_KEYS); n = 96 if sp == 'TRAIN' else 48
        a,b = [reports[s,arm,d,sp,p,l] for arm in ARMS]; m = r['kind_matrix']
        require(type(r['answers']) is int and r['answers'] == n and set(m) == set(KINDS),'transition fields')
        for k,row in m.items():
            require(set(row) == set(KINDS) and all(type(x) is int and x >= 0 for x in row.values())
                    and sum(row.values()) == a['kinds'][k],'transition row marginal')
        require(all(sum(m[k][j] for k in KINDS) == b['kinds'][j] for j in KINDS),'transition column marginal')
        require(type(r['rescued']) is int and type(r['regressed']) is int and r['rescued'] == sum(m[k]['correct'] for k in KINDS[1:])
                and r['regressed'] == sum(m['correct'][k] for k in KINDS[1:]),'rescue accounting')
        require(set(r['sign_matrices']) == {'pair_margin','support_margin'},'sign matrices')
        for field,matrix in r['sign_matrices'].items():
            signs = {'positive','zero','negative'}
            require(set(matrix) == signs and all(set(row) == signs and all(type(x) is int and x >= 0 for x in row.values())
                    for row in matrix.values()) and sum(sum(row.values()) for row in matrix.values()) == n,'sign transition partition')
            def margins(report):
                if field == 'support_margin':
                    return dict(positive=report['support_rank']['inside_higher'],zero=report['support_rank']['tie'],negative=report['support_rank']['outside_higher'])
                return {k:sum(report['within_pair'][kind][order] for kind in KINDS)
                        for k,order in (('positive','target_higher'),('zero','tie'),('negative','other_higher'))}
            left,right = margins(a),margins(b)
            require(all(sum(matrix[k].values()) == left[k] and sum(matrix[j][k] for j in signs) == right[k]
                        for k in signs),'sign transition marginals')
        require(set(r['mean_delta']) == {'support_nll','within_nll','pair_margin','support_margin'}
                and all(type(x) is float and math.isfinite(x) for x in r['mean_delta'].values()),'finite differences')
    require(len(v['reconciled_contrasts']) == 30 and [(r['seed'],r['domain']) for r in v['reconciled_contrasts']]
            == list(itertools.product(SEEDS,DOMAINS)),'all30parent contrasts')
    for r in v['reconciled_contrasts']:
        parent().previous().contrast_check({k:x for k,x in r.items() if k not in ('seed','domain','outside_gain')})
        require(type(r['outside_gain']) is int,'outside count type')
        selected = [[reports[r['seed'],arm,r['domain'],'HOLDOUT',p,l] for p,l in itertools.product(profiles(r['domain']),LANGUAGES)] for arm in ARMS]
        totals = [{k:sum(v['kinds'][k] for v in group) for k in KINDS} for group in selected]
        require((r['control_correct'],r['candidate_correct']) == (totals[0]['correct'],totals[1]['correct'])
                and r['outside_gain'] == sum(totals[1][k]-totals[0][k] for k in KINDS[2:]),'contrast stratum reconciliation')
        paired = [x for x in v['paired_strata'] if x['seed'] == r['seed'] and x['domain'] == r['domain'] and x['split'] == 'HOLDOUT']
        require(r['rescued'] == sum(x['rescued'] for x in paired) and r['regressed'] == sum(x['regressed'] for x in paired),'paired rescue reconciliation')


def load_source(source_out, data_out, read):
    data = read(data_out/'dataset.json')
    archive = torch.load(source_out/'evaluations.pt',map_location='cpu',weights_only=True)
    return data,archive


def run_audit(out, source_out, data_out, prior, read):
    data,archive = load_source(source_out,data_out,read)
    details,paired,value = analyze(data,archive,prior)
    for name,item in zip(OUTPUTS,(manifest(),details,paired,value),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(item))
    return value


def semantic_recheck(out, source_out, data_out, prior, read):
    data,archive = load_source(source_out,data_out,read)
    details,paired,value = analyze(data,archive,prior)
    for name,item in zip(OUTPUTS,(manifest(),details,paired,value),strict=True):
        require(blob(read(out/name)) == blob(item),'saved reconstruction:'+name)
    return value
