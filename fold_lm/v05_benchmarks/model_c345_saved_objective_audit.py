"""C345: saved terminal objectives and complete pre-update C344 trajectories."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C345-v5b-saved-objective-audit'
STAGE = 'V5-B-SAVED-OBJECTIVE-AUDIT'
SEEDS = tuple(range(344001,344006))
ARMS = ('mean_ce','pair_max')
DOMAINS = ('original2','original3','original4','original5','original6','interior4')
SPLITS = ('TRAIN','HOLDOUT')
STEPS, CYCLE, BLOCK = 2400, 1200, 200
OWN = ('fold_lm/v05_benchmarks/model_c345_saved_objective_audit.py',
       'tools/c345_execution.py','tests_lm/test_v05_c345_saved_objective_audit.py',
       'tests_lm/test_v05_c345_execution.py','tools/run_c345.ps1',
       'tools/invoke_c345.ps1','docs/experiment-ledger-addendum-c345-preregistration.md')
OUTPUTS = ('audit-plan.json','terminal-objectives.json','training-trajectory.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 64, 6578, 241
SOURCE_COUNT, INPUT_COUNT = 937, 8679
WORK = dict(checkpoint_records=10,normal_answers=51840,query_pairs=25920,
    terminal_summaries=120,terminal_contrast_count=60,training_trace_rows=24000,
    paired_trace_rows=12000,trace_blocks=120,trace_groups=180,
    evaluation_bundle_loads=1,training_trace_loads=1,
    train_steps=0,model_forward_calls=0,gradient_calls=0,optimizer_steps=0,
    model_state_loads=0,new_checkpoint_writes=0,network_calls=0)
ACCEPTANCE_BASE = 'a7174ae51f71f001901793603ab9f7ddb26ed923'
MANIFEST_SHA = '5e69553fd6661ef46459883500fd719b474fd7cacbd17d002c957eb3fb2f1a9f'
TRACE_METRICS = ('mean_ce','pair_max','selected','pair_max_minus_mean','preclip_norm')
COMMON_METRICS = ('mean_ce','pair_max','pair_max_minus_mean','preclip_norm')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c344_pair_max_training')


def identities():
    return list(itertools.product(SEEDS,ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=ACCEPTANCE_BASE,
        parent_execution='8d1e1170cd614503deab1e09474fe82de4bba561',
        parent_summary='610398ced893ff1d1885faf9bd02ffef57779ca2bd96bfa995b6929e6d8f20d7',
        parent_envelope='c77f0fcf5fcbbf59d3961894713dbf8dcb30ae89841df0325b980a07d8913562',
        question='how do matched saved terminal meanCE/pairmax and complete preupdate loss/norm trajectories accompany C344 exact-answer deterioration',
        seeds=list(SEEDS),arms=list(ARMS),domains=list(DOMAINS),splits=list(SPLITS),
        changed='retrospective arithmetic on fixed accepted C344 artifacts only;no fitting,model calls,state loading,prompt change or prediction repair',
        terminal='full256 float64 per-answer CE;canonical metadata query pairs;mean query CE and mean pair maximum across all3profiles/bothlanguages,all120state/domain/split groups',
        pairing='canonical language/entities/values/factorder plus distinct queries/targets;never arbitrary row adjacency',
        comparison='60same-domain/split paired objective deltas alongside exact parent answer/query-pair gains;positive loss delta means worse;no desired-sign gate',
        weighting='terminal means weight every normal answer/querypair equally within its domain/split;not exposure-weighted full-training objective',
        trajectories='all24000preupdate minibatch entries and12000same-step paired differences;all12fixed200step blocks/state plus2cycles*3canonicalslots*3profiles/state',
        slot_semantics='slot2 is original2;slot3 is original3;slot4 is mixed original4/original5/interior4;batch loss cannot be attributed to a constituent family',
        trace_fields=['mean_ce','pair_max','selected','preclip_norm_history','event_indices','optimizer_group_lrs'],
        trace_reduction='math.fsum means,min,max;pairmax-minus-mean is descriptive within-pair imbalance;norm_gt1 counts threshold exceedances,not exact clipping calls',
        schedule='reconstruct every accepted event,family mask,length mask,actual perstep pair composition and metadata;retain recorded preupdate values unchanged',
        temporal_boundary='step2400 loss is before final update on one minibatch;no intermediate fullset predictions/checkpoints or learned-then-lost inference',
        nonclaims='no proof of convergence,global optimum,causal clipping,gradient starvation,internal mechanism,capability gain or independent samples',
        gate='diagnostic integrity only;all120normal summaries and60contrasts bind exact parent;preserve candidatefalse/eligible2 and every parent scientific result',
        parent_output_files=489,parent_test_proof_files=481,source_count=SOURCE_COUNT,input_count=INPUT_COUNT,
        own_tests=OWN_TESTS,full_tests=FULL_TESTS,modules=MODULES,outputs=list(OUTPUTS),
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA,'C345 manifest seal')


def finite(value, nonnegative=False):
    require(type(value) is float and math.isfinite(value) and (not nonnegative or value >= 0),'finite float')
    return value


def statistics(values):
    require(type(values) is list and values,'nonempty observations')
    values = [finite(v) for v in values]
    result = dict(count=len(values),mean=math.fsum(values)/len(values),minimum=min(values),maximum=max(values))
    for key in ('mean','minimum','maximum'): finite(result[key])
    return result


def check_statistics(value, count, nonnegative=False):
    require(type(value) is dict and set(value) == {'count','mean','minimum','maximum'}
            and type(value['count']) is int and value['count'] == count,'statistics schema/count')
    for key in ('mean','minimum','maximum'): finite(value[key],nonnegative)
    tolerance = 1e-12*max(1.,abs(value['minimum']),abs(value['maximum']))
    require(value['minimum']-tolerance <= value['mean'] <= value['maximum']+tolerance,'statistics bounds')


def parent_summary(saved):
    parent().check_summary(saved)
    require(saved['candidate_gate'] is False and type(saved['eligible_seed_count']) is int
            and saved['eligible_seed_count'] == 2,'accepted C344 negative/two eligible')
    return saved


def profiles(domain):
    require(domain in DOMAINS,'terminal domain')
    return parent().support().audit().parent().profiles(domain)


def canonical_pairs(rows):
    pairs = parent().previous().source().base().query_pairs(rows)
    require(len(pairs)*2 == len(rows) and sorted(i for pair in pairs for i in pair) == list(range(len(rows))), 'complete canonical query pairs')
    for a,b in pairs:
        left,right = rows[a],rows[b]
        require(all(left[k] == right[k] for k in ('language','entities','values','permutation'))
                and left['id'] != right['id'] and [left['query'],right['query']] == left['entities'], 'terminal pair metadata')
        targets = [48+dict(zip(row['entities'],row['values'],strict=True))[row['query']] for row in (left,right)]
        require(targets[0] != targets[1] and [left['target'],right['target']] == targets,'terminal pair targets')
    return pairs


def terminal_view(logits, rows):
    require(isinstance(logits,torch.Tensor) and logits.shape == (len(rows),256)
            and logits.dtype == torch.float64 and logits.device.type == 'cpu'
            and bool(torch.isfinite(logits).all()),'finite full256 terminal logits')
    pairs = canonical_pairs(rows)
    targets = torch.tensor([row['target'] for row in rows],dtype=torch.int64)
    with torch.no_grad():
        losses = F.cross_entropy(logits,targets,reduction='none').tolist()
        predictions = torch.argmax(logits,dim=1).tolist()
    require(all(math.isfinite(v) and v >= 0 for v in losses),'finite terminal CE')
    result = []
    for a,b in pairs:
        members = [rows[a],rows[b]]; values = [float(losses[i]) for i in (a,b)]
        actual = [predictions[i] for i in (a,b)]; wanted = [row['target'] for row in members]
        result.append(dict(row_ids=[row['id'] for row in members],targets=wanted,predictions=actual,
            language=members[0]['language'],entities=members[0]['entities'],values=members[0]['values'],
            permutation=members[0]['permutation'],per_query_ce=values,
            mean_ce=math.fsum(values)/2,pair_max=max(values),correct_answers=sum(a == b for a,b in zip(actual,wanted,strict=True)),
            both_correct=actual == wanted))
    return result


def check_archive(archive, traces, data, saved, cx):
    p = parent(); base = p.previous().source().base(); cx[-1].c.p267.validate_data(data)
    parent_summary(saved)
    require(type(archive) is dict and set(archive) == {'schema','records'}
            and archive['schema'] == 'fold-c344-evaluations-v1','C344 evaluation schema')
    records = archive['records']
    require(type(records) is list and [(r['seed'],r['arm']) for r in records] == identities()
            and type(traces) is list and [(r['seed'],r['arm']) for r in traces] == identities(),'complete saved cohort')
    for record,trace,state in zip(records,traces,saved['seed_results'],strict=True):
        require(type(record) is dict and set(record) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and type(record['state_sha256']) is str and re.fullmatch('[0-9a-f]{64}',record['state_sha256'])
                and record['state_sha256'] == trace['final_sha256'] and record['evaluation_policy'] == 'native_before'
                and set(record['raw']) == set(record['receipts']) == {'evaluation','replay'},'terminal state/trace identity')
        for mode in ('evaluation','replay'):
            require(blob(record['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)),'parent evaluation receipt')
            base.validate_raw(record['raw'][mode],data,cx)
        require(base.replay_error(record['raw']['evaluation'],record['raw']['replay'],data,cx) <= 1e-9,'terminal saved replay')
        require(blob(p.normal_report(record['raw']['evaluation'],data)) == blob(state['normal_by_domain']),'all120parent normal bindings')
    return records


def terminal_audit(records, data, saved):
    observations,summaries = [],[]
    for record,state in zip(records,saved['seed_results'],strict=True):
        raw = record['raw']['evaluation']
        for domain,split in itertools.product(DOMAINS,SPLITS):
            tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
            tags = dict(seed=record['seed'],arm=record['arm'],domain=domain,split=split)
            group = []
            for profile in profiles(domain):
                group.extend(dict(**tags,profile=profile,**row) for row in terminal_view(tree[split][profile]['normal'],data[split]))
            observations.extend(group); normal = state['normal_by_domain'][domain][split]
            require(len(group) == normal['query_pairs'] and sum(r['correct_answers'] for r in group) == normal['correct']
                    and sum(r['both_correct'] for r in group) == normal['both_query_correct'],'terminal/parent exact answers')
            summaries.append(dict(**tags,normal=normal,mean_ce=statistics([r['mean_ce'] for r in group]),
                pair_max=statistics([r['pair_max'] for r in group])))
    require(len(observations) == WORK['query_pairs'],'complete terminal observations')
    lookup = {(r['seed'],r['arm'],r['domain'],r['split']):r for r in summaries}; contrasts = []
    for pair in saved['paired_comparisons']:
        for domain,split in itertools.product(DOMAINS,SPLITS):
            a,b = [lookup[pair['seed'],arm,domain,split] for arm in ARMS]
            contrasts.append(dict(seed=pair['seed'],domain=domain,split=split,
                mean_ce_delta=b['mean_ce']['mean']-a['mean_ce']['mean'],
                pair_max_delta=b['pair_max']['mean']-a['pair_max']['mean'],
                parent_contrast=pair['normal_by_domain'][domain][split]))
    return dict(pairs=observations),summaries,contrasts


def schedule_rows(seed, data, cx):
    p = parent(); events,family = p.schedule(seed,data['TRAIN'],cx[-1]); selected = p.length_mask(events,family)
    p.validate_training_pairs(data['TRAIN'],torch.tensor([r['target'] for r in data['TRAIN']],dtype=torch.int64),events,cx[-1])
    p.actual_exposure(events,family,selected)
    result = []
    for step in range(STEPS):
        index = step%CYCLE; event = events[index].tolist(); slot,profile = event[0][:2]
        require(all(row[:2] == [slot,profile] for row in event),'homogeneous canonical event slot/profile')
        counts = dict.fromkeys(DOMAINS,0)
        for row,interior,four in zip(event,family[index].tolist(),selected[step].tolist(),strict=True):
            domain = 'interior4' if interior else 'original'+str((4 if four else 5) if slot == 4 else slot)
            counts[domain] += 1
        require(sum(counts.values()) == 24 and counts['original6'] == 0,'actual event composition')
        result.append(dict(step=step+1,event_index=index,cycle=step//CYCLE+1,block=step//BLOCK+1,
            slot=slot,profile=profile,batch_kind='mixed_original45_interior4' if slot == 4 else 'original'+str(slot),
            domain_pairs=counts))
    return result


def trace_rows(traces, data, cx, tables, targets):
    p = parent()
    require(type(traces) is list and [(t['seed'],t['arm']) for t in traces] == identities(),'all ten traces')
    schedules = {seed:schedule_rows(seed,data,cx) for seed in SEEDS}; result = []
    for trace in traces:
        p.check_trace(trace,data['TRAIN'],cx[-1],tables,targets)
        require(len(trace['loss_history']) == len(trace['preclip_norm_history']) == len(trace['event_indices']) == STEPS,'trace lengths')
        for meta,loss,norm,event in zip(schedules[trace['seed']],trace['loss_history'],trace['preclip_norm_history'],trace['event_indices'],strict=True):
            require(type(loss) is dict and set(loss) == {'mean_ce','pair_max','selected'},'writer loss fields')
            for value in loss.values(): finite(value,True)
            finite(norm,True)
            require(type(event) is int and event == meta['event_index'] and loss['selected'] == loss[trace['arm']],'preupdate objective/event binding')
            difference = loss['pair_max']-loss['mean_ce']; finite(difference)
            tolerance = 1e-12*max(1.,loss['mean_ce'])
            require(-tolerance <= difference <= loss['mean_ce']+tolerance,'pairmax reduction identity bounds')
            result.append(dict(seed=trace['seed'],arm=trace['arm'],**meta,**loss,pair_max_minus_mean=difference,
                preclip_norm=norm,norm_gt1=norm > 1.))
    for seed in SEEDS:
        left,right = [t for t in traces if t['seed'] == seed]
        for key in ('initial_sha256','core_initial_sha256','training_input_sha256','logical_training_sha256',
                    'schedule_sha256','mask_sha256','length_mask_sha256','actual_training_stream_sha256','pair_metadata_sha256'):
            require(left[key] == right[key],'paired trace input/initial identity:'+key)
        require(all(left['loss_history'][0][key] == right['loss_history'][0][key] for key in ('mean_ce','pair_max')),'paired first preupdate objectives')
    require(len(result) == WORK['training_trace_rows'],'complete preupdate observations')
    return result


def trace_group(rows, tags):
    require(rows,'nonempty trace group')
    return dict(**tags,steps=len(rows),norm_gt1=sum(r['norm_gt1'] for r in rows),
        metrics={key:statistics([r[key] for r in rows]) for key in TRACE_METRICS},
        domain_pairs={domain:sum(r['domain_pairs'][domain] for r in rows) for domain in DOMAINS})


def paired_trace_group(left, right, tags):
    require(len(left) == len(right) and all(a['step'] == b['step'] for a,b in zip(left,right,strict=True)), 'same-step paired trace group')
    metrics = {}
    for key in COMMON_METRICS:
        differences = [b[key]-a[key] for a,b in zip(left,right,strict=True)]
        metrics[key] = dict(**statistics(differences),negative=sum(v < 0 for v in differences),
            zero=sum(v == 0 for v in differences),positive=sum(v > 0 for v in differences))
    return dict(**tags,steps=len(left),metrics=metrics,
        control_norm_gt1=sum(r['norm_gt1'] for r in left),candidate_norm_gt1=sum(r['norm_gt1'] for r in right))


def trajectory_audit(rows):
    blocks,groups,paired_blocks,paired_groups = [],[],[],[]
    by_state = {(seed,arm):[r for r in rows if r['seed'] == seed and r['arm'] == arm] for seed,arm in identities()}
    for seed,arm in identities():
        source = by_state[seed,arm]
        require([r['step'] for r in source] == list(range(1,STEPS+1)),'trace step coverage')
        for block in range(1,STEPS//BLOCK+1):
            tags = dict(seed=seed,arm=arm,block=block,first_step=(block-1)*BLOCK+1,last_step=block*BLOCK)
            blocks.append(trace_group([r for r in source if r['block'] == block],tags))
        for cycle,slot,profile in itertools.product((1,2),(2,3,4),range(3)):
            tags = dict(seed=seed,arm=arm,cycle=cycle,slot=slot,profile=profile,
                batch_kind='mixed_original45_interior4' if slot == 4 else 'original'+str(slot))
            groups.append(trace_group([r for r in source if (r['cycle'],r['slot'],r['profile']) == (cycle,slot,profile)],tags))
    paired_rows = []
    for seed in SEEDS:
        left,right = [by_state[seed,arm] for arm in ARMS]
        for a,b in zip(left,right,strict=True):
            require(all(a[k] == b[k] for k in ('step','event_index','cycle','block','slot','profile','batch_kind','domain_pairs')),'paired actual batch coordinate')
            paired_rows.append(dict(seed=seed,step=a['step'],deltas={key:b[key]-a[key] for key in COMMON_METRICS}))
        for block in range(1,STEPS//BLOCK+1):
            paired_blocks.append(paired_trace_group(*[[r for r in source if r['block'] == block] for source in (left,right)],dict(seed=seed,block=block)))
        for cycle,slot,profile in itertools.product((1,2),(2,3,4),range(3)):
            paired_groups.append(paired_trace_group(*[[r for r in source if (r['cycle'],r['slot'],r['profile']) == (cycle,slot,profile)]
                for source in (left,right)],dict(seed=seed,cycle=cycle,slot=slot,profile=profile)))
    return dict(rows=rows,paired_rows=paired_rows),blocks,groups,paired_blocks,paired_groups


def check_summary(value):
    require(type(value) is dict and set(value) == {*WORK,'diagnostic_complete','parent_validation_summary','terminal',
        'terminal_contrasts','trace_blocks_summary','trace_groups_summary','paired_blocks','paired_groups','source_trace_sha256'},'diagnostic summary schema')
    require(value['diagnostic_complete'] is True and all(type(value[k]) is int and value[k] == n for k,n in WORK.items()),'diagnostic work')
    saved = parent_summary(value['parent_validation_summary'])
    require(type(value['source_trace_sha256']) is str and re.fullmatch('[0-9a-f]{64}',value['source_trace_sha256']),'bound full source traces')
    terminal = value['terminal']; fields = ('seed','arm','domain','split')
    require([tuple(r[k] for k in fields) for r in terminal] == list(itertools.product(SEEDS,ARMS,DOMAINS,SPLITS)),'all terminal coordinates')
    lookup = {}
    for row in terminal:
        require(set(row) == {*fields,'normal','mean_ce','pair_max'},'terminal summary fields')
        state = next(r for r in saved['seed_results'] if (r['seed'],r['arm']) == (row['seed'],row['arm']))
        require(blob(row['normal']) == blob(state['normal_by_domain'][row['domain']][row['split']]),'parent normal summary')
        n = row['normal']['query_pairs']
        for key in ('mean_ce','pair_max'): check_statistics(row[key],n,True)
        tolerance = 1e-12*max(1.,row['mean_ce']['mean'])
        require(row['mean_ce']['mean']-tolerance <= row['pair_max']['mean'] <= 2*row['mean_ce']['mean']+tolerance,'terminal reduction bounds')
        lookup[tuple(row[k] for k in fields)] = row
    contrasts = value['terminal_contrasts']
    require([(r['seed'],r['domain'],r['split']) for r in contrasts] == list(itertools.product(SEEDS,DOMAINS,SPLITS)),'all terminal comparisons')
    for row in contrasts:
        require(set(row) == {'seed','domain','split','mean_ce_delta','pair_max_delta','parent_contrast'},'terminal comparison fields')
        a,b = [lookup[row['seed'],arm,row['domain'],row['split']] for arm in ARMS]
        for key in ('mean_ce','pair_max'):
            finite(row[key+'_delta']); require(row[key+'_delta'] == b[key]['mean']-a[key]['mean'],'terminal delta arithmetic')
        paired = next(r for r in saved['paired_comparisons'] if r['seed'] == row['seed'])
        require(blob(row['parent_contrast']) == blob(paired['normal_by_domain'][row['domain']][row['split']]),'parent paired answers')
    for name,coordinates,keys in (
        ('trace_blocks_summary',list(itertools.product(SEEDS,ARMS,range(1,13))),('seed','arm','block')),
        ('trace_groups_summary',list(itertools.product(SEEDS,ARMS,(1,2),(2,3,4),range(3))),('seed','arm','cycle','slot','profile'))):
        rows = value[name]; require([tuple(r[k] for k in keys) for r in rows] == coordinates,'complete trajectory partition')
        require(sum(r['steps'] for r in rows) == WORK['training_trace_rows'],'partition step conservation')
        for row in rows:
            expected_fields = {*keys,'steps','norm_gt1','metrics','domain_pairs',*({'first_step','last_step'} if name == 'trace_blocks_summary' else {'batch_kind'})}
            require(set(row) == expected_fields and type(row['steps']) is int and row['steps'] > 0,'trace group fields/size')
            if name == 'trace_blocks_summary':
                require(row['steps'] == BLOCK and row['first_step'] == (row['block']-1)*BLOCK+1 and row['last_step'] == row['block']*BLOCK,'fixed block boundary')
            else:
                require(row['batch_kind'] == ('mixed_original45_interior4' if row['slot'] == 4 else 'original'+str(row['slot'])),'mixed slot meaning')
            require(type(row['norm_gt1']) is int and 0 <= row['norm_gt1'] <= row['steps'] and set(row['metrics']) == set(TRACE_METRICS),'trace metric inventory')
            for key in TRACE_METRICS: check_statistics(row['metrics'][key],row['steps'],key != 'pair_max_minus_mean')
            require(set(row['domain_pairs']) == set(DOMAINS) and all(type(v) is int and v >= 0 for v in row['domain_pairs'].values())
                    and sum(row['domain_pairs'].values()) == 24*row['steps'] and row['domain_pairs']['original6'] == 0,'trace actual composition')
            require(blob(row['metrics']['selected']) == blob(row['metrics'][row['arm']]),'selected metric identity')
    for seed,arm in identities():
        partitions = [[r for r in value[name] if (r['seed'],r['arm']) == (seed,arm)]
            for name in ('trace_blocks_summary','trace_groups_summary')]
        require(all(sum(r['steps'] for r in rows) == STEPS for rows in partitions),'complete per-state trajectory')
        for rows in partitions:
            expected = parent().manifest()['actual_per_row_exposure']
            require({d:sum(r['domain_pairs'][d] for r in rows) for d in DOMAINS} ==
                    {d:96*expected[d] for d in DOMAINS},'complete actual training exposure')
        require(sum(r['norm_gt1'] for r in partitions[0]) == sum(r['norm_gt1'] for r in partitions[1]),'norm partition conservation')
        for key in TRACE_METRICS:
            totals = [math.fsum(r['metrics'][key]['mean']*r['steps'] for r in rows)/STEPS for rows in partitions]
            require(math.isclose(*totals,rel_tol=1e-12,abs_tol=1e-12),'trace partition metric conservation')
    for name,coordinates,keys in (
        ('paired_blocks',list(itertools.product(SEEDS,range(1,13))),('seed','block')),
        ('paired_groups',list(itertools.product(SEEDS,(1,2),(2,3,4),range(3))),('seed','cycle','slot','profile'))):
        rows = value[name]; require([tuple(r[k] for k in keys) for r in rows] == coordinates,'paired partition coordinates')
        require(sum(r['steps'] for r in rows) == WORK['paired_trace_rows'],'paired step conservation')
        for row in rows:
            require(set(row) == {*keys,'steps','metrics','control_norm_gt1','candidate_norm_gt1'}
                    and type(row['steps']) is int and row['steps'] > 0 and set(row['metrics']) == set(COMMON_METRICS),'paired trace schema')
            for key in ('control_norm_gt1','candidate_norm_gt1'):
                require(type(row[key]) is int and 0 <= row[key] <= row['steps'],'paired norm exceedance')
            for metric in row['metrics'].values():
                require(set(metric) == {'count','mean','minimum','maximum','negative','zero','positive'},'signed trace delta schema')
                check_statistics({k:metric[k] for k in ('count','mean','minimum','maximum')},row['steps'])
                require(all(type(metric[k]) is int and metric[k] >= 0 for k in ('negative','zero','positive'))
                        and sum(metric[k] for k in ('negative','zero','positive')) == row['steps'],'signed delta partition')
            source = value['trace_blocks_summary' if name == 'paired_blocks' else 'trace_groups_summary']
            left,right = [next(r for r in source if r['arm'] == arm and all(r[k] == row[k] for k in keys)) for arm in ARMS]
            require(left['steps'] == right['steps'] == row['steps'] and
                    [row['control_norm_gt1'],row['candidate_norm_gt1']] == [left['norm_gt1'],right['norm_gt1']], 'paired group binding')
            for key in COMMON_METRICS:
                require(math.isclose(row['metrics'][key]['mean'],right['metrics'][key]['mean']-left['metrics'][key]['mean'],
                                    rel_tol=1e-12,abs_tol=1e-12),'paired same-metric mean difference')
    require(len(terminal) == WORK['terminal_summaries'] and len(contrasts) == WORK['terminal_contrast_count']
            and len(value['trace_blocks_summary']) == WORK['trace_blocks'] and len(value['trace_groups_summary']) == WORK['trace_groups'],'diagnostic inventories')


def analyze(traces, archive, saved, data, cx, tables, targets):
    records = check_archive(archive,traces,data,saved,cx)
    terminal,summaries,contrasts = terminal_audit(records,data,saved)
    trajectory,blocks,groups,paired_blocks,paired_groups = trajectory_audit(trace_rows(traces,data,cx,tables,targets))
    result = dict(diagnostic_complete=True,parent_validation_summary=saved,terminal=summaries,terminal_contrasts=contrasts,
        trace_blocks_summary=blocks,trace_groups_summary=groups,paired_blocks=paired_blocks,paired_groups=paired_groups,
        source_trace_sha256=digest(traces),**WORK)
    check_summary(result)
    return terminal,trajectory,result


def load_inputs(parent_out, data_out, cx, read):
    p = parent(); previous = p.previous(); base = previous.source().base()
    data,old,new = previous.load_data(data_out,read)
    require(base.digest(data) == base.DATA_SHA and base.digest(old) == base.PROMPTS_SHA
            and base.digest(new) == base.digest(cx[2].new_prompts(data)),'canonical diagnostic input bytes')
    cx[-1].c.p267.validate_data(data); cx[2].check_prompts(data,old,new,cx[3],cx[-1])
    tables,targets = p.prepared(data,old,new,cx)
    archive = torch.load(parent_out/'evaluations.pt',map_location='cpu',weights_only=True)
    return read(parent_out/'training-traces.json'),archive,read(parent_out/'validation-summary.json'),data,tables,targets


def reconstructed(parent_out, data_out, cx, read):
    traces,archive,saved,data,tables,targets = load_inputs(parent_out,data_out,cx,read)
    previous = parent().previous()
    def source_hash():
        # Accepted state_hash accepts str/int mapping keys. Token banks use
        # (slot,profile) keys, so preserve typed coordinates and even empty
        # arm/family containers in a nested, deterministically ordered sequence.
        banks = [(arm,[(family,[(slot,profile,value) for (slot,profile),value in sorted(group.items())])
                       for family,group in sorted(groups.items())]) for arm,groups in sorted(tables.items())]
        return previous.state_hash((traces,archive,saved,data,banks,targets))
    before = source_hash()
    result = analyze(traces,archive,saved,data,cx,tables,targets)
    require(source_hash() == before,'source trace/logit/data mutation')
    return result


def run_diagnostic(out, parent_out, data_out, cx, read):
    terminal,trajectory,value = reconstructed(parent_out,data_out,cx,read)
    for name,item in zip(OUTPUTS,(manifest(),terminal,trajectory,value),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(item))
    return value


def semantic_recheck(out, parent_out, data_out, cx, read):
    terminal,trajectory,value = reconstructed(parent_out,data_out,cx,read)
    for name,item in zip(OUTPUTS,(manifest(),terminal,trajectory,value),strict=True):
        require(blob(read(out/name)) == blob(item),'saved objective reconstruction:'+name)
    return value


def report_results(value, emit):
    check_summary(value)
    for key,label in (('terminal','C345 terminal objective'),('terminal_contrasts','C345 terminal contrast'),
        ('trace_blocks_summary','C345 trace block'),('trace_groups_summary','C345 trace group'),
        ('paired_blocks','C345 paired trace block'),('paired_groups','C345 paired trace group')):
        for row in value[key]: emit(label,row)
    emit('C345 diagnostic inventory',dict(WORK))
    return dict(WORK)
