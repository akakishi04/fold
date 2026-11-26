"""C347: exhaustive saved loss/correctness transitions on accepted C346 logits."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch

EXPERIMENT_ID = 'C347-v5b-saved-loss-transition'
STAGE = 'V5-B-SAVED-LOSS-TRANSITION'
SEEDS = tuple(range(346001,346006))
ARMS = ('mean_ce','pair_max','pair_max_half_rate')
CONTROLS = ('pair_max','mean_ce')
CANDIDATE = 'pair_max_half_rate'
DOMAINS = tuple('original'+str(n) for n in range(2,7))+('interior4',)
SPLITS = ('TRAIN','HOLDOUT')
TRANSITIONS = ('CC','CW','WC','WW')
COLLAPSE_TRANSITIONS = ('distinct_to_distinct','distinct_to_same','same_to_distinct','same_to_same')
OWN = ('fold_lm/v05_benchmarks/model_c347_saved_loss_transition.py',
       'tools/c347_execution.py','tests_lm/test_v05_c347_saved_loss_transition.py',
       'tests_lm/test_v05_c347_execution.py','tools/run_c347.ps1',
       'tools/invoke_c347.ps1','docs/experiment-ledger-addendum-c347-preregistration.md')
OUTPUTS = ('audit-plan.json','normal-pair-observations.json','loss-transition-decomposition.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 72, 6724, 245
SOURCE_COUNT, INPUT_COUNT = 951, 9681
WORK = dict(checkpoint_records=15,normal_answers=77760,query_pairs=38880,
    terminal_summaries=180,terminal_contrast_count=120,matched_answers=51840,matched_pairs=25920,
    comparison_groups=120,answer_transition_groups=480,pair_transition_groups=480,collapse_transition_groups=480,
    evaluation_bundle_loads=1,training_trace_loads=1,
    train_steps=0,model_forward_calls=0,gradient_calls=0,optimizer_steps=0,
    model_state_loads=0,new_checkpoint_writes=0,network_calls=0)
ACCEPTANCE_BASE = 'c0597bbc24ca3db2761763b65cfe8521af7d1b2e'
MANIFEST_SHA = '8e85821c7d4e69c49cd0695ccb5126a7dbb8b5cc0f5b9ca77f5fb0cd98a0aee3'
METRIC_FIELDS = ('control_sum','candidate_sum','delta_sum','control_mean','candidate_mean','delta_mean','delta_min','delta_max','delta_contribution')
PAIR_METADATA = ('seed','domain','split','profile','row_ids','targets','language','entities','values','permutation')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c346_pair_max_rate')


def diagnostic():
    return parent().parent()


def identities():
    return list(itertools.product(SEEDS,ARMS))


def coordinates():
    return list(itertools.product(SEEDS,CONTROLS,DOMAINS,SPLITS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=ACCEPTANCE_BASE,
        parent_execution='622e623faa0c3c698a18033eb8b4bca554088918',
        parent_summary='d06fa2a06287696424ac58e3d56e7262282caca81b028f61709f609ab728e816',
        parent_envelope='b8b57583363d61aca10d947c891de0d8b3d8b2319e659652cacf101a334e3c3d',
        question='which exhaustive matched answer/pair correctness transitions account for lower aggregate loss with fewer correct answers in C346 half-rate pair-max versus its controls',
        seeds=list(SEEDS),arms=list(ARMS),controls=list(CONTROLS),candidate=CANDIDATE,domains=list(DOMAINS),splits=list(SPLITS),
        changed='saved-logit arithmetic only;no fitting,model calls,state loading,prompt change,prediction repair,rate selection or new cohort',
        observations='all15saved states;full256 CPU float64 cross entropy and first-index argmax;all3profiles/bothlanguages;canonical metadata query pairs',
        pairing='language/entities/values/factorder and distinct counterpart queries/targets;match exact seed/domain/split/profile/row IDs across candidate and each control',
        correctness='first letter is control and second candidate;C means correct answer or both-query-correct pair;pair W means not-both-correct,including one-correct pairs',
        transitions=list(TRANSITIONS),collapse_transitions=list(COLLAPSE_TRANSITIONS),
        collapse='same means both query argmax predictions coincide;distinct does not imply correct;allfour collapse transitions are descriptive secondary strata',
        loss='per-answer CE and per-pair meanCE/pairmax;pairmax delta is max(candidate query CEs)-max(control query CEs),not max of per-query deltas',
        reduction='math.fsum;each stratum records count,control/candidate sums and means,delta sum/mean/min/max,signed delta contribution divided by the FULL comparison answer/pair count',
        empty='count0;all sums/contributions0;unobserved means and delta extrema null;no arbitrary filtering,tail subset,margin or new threshold',
        conservation='every partition separately exhausts its full comparison;counts recover exact parent rescue/regression/collapse;contributions recover parent loss deltas',
        numeric_tolerance='loss conservation uses1e-12*max(1,absolute compared values,underlying control/candidate sums or means for cancellation);identities,counts,and parent terminal/contrast bytes remain exact',
        weighting='equal answer/query-pair weighting inside each domain/split;not training-exposure weighting;the three partitions overlap and their contributions are never added across partition families',
        provenance='one evaluation archive and one training-trace JSON load;trace final_sha256 binds each saved record;no loss/norm trajectory analysis',
        nonclaims='correctness transition does not force CE delta sign in256classes;no causal mechanism,convergence,undertraining,calibration,capability gain,independent-sample or optimal-rate claim',
        gate='diagnostic integrity only;bind all180parent terminal summaries and120contrasts;preserve complete C346 candidatefalse/eligible0 result;no desired-sign gate',
        native_validation='Validate must pass before formal execution log capture/publication;failure is SKIPPED without publication',
        regression_execution='complete registered regression runs once in Validate;Execute independently verifies and reuses the bound receipt/proofs',
        validation_binding='canonical unique run folder,HEAD,manifest,exact source/input maps,regression proof hashes,cleanup,compile/import inventory and closed log bytes;495validation/proof files leased separately from9681inputs through fresh verification',
        validation_outputs=['validation-receipt.json','validation.log'],regression_proof_files=493,
        validation_retained_files=495,retained_output_files=501,
        retained_scope='hash-bound contract output inventory;auxiliary regression/science/verify process transcripts and outer console log are excluded',
        parent_output_files=497,parent_test_proof_files=489,source_count=SOURCE_COUNT,input_count=INPUT_COUNT,
        own_tests=OWN_TESTS,full_tests=FULL_TESTS,modules=MODULES,outputs=list(OUTPUTS),
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA,'C347 manifest seal')


def close(a, b, message, scale=0.):
    require(all(math.isfinite(v) for v in (a,b,scale)),message)
    tolerance = 1e-12*max(1.,abs(a),abs(b),abs(scale))
    require(math.isclose(a,b,rel_tol=0.,abs_tol=tolerance),message)


def finite(value, nonnegative=False):
    require(type(value) is float and math.isfinite(value) and (not nonnegative or value >= 0),'finite loss arithmetic')
    return value


def parent_summary(saved):
    parent().check_summary(saved)
    require(saved['candidate_gate'] is False and type(saved['eligible_seed_count']) is int
            and saved['eligible_seed_count'] == 0,'accepted C346 negative/zero eligible')
    return saved


def check_archive(archive, traces, data, saved, cx):
    p = parent(); base = p.previous().source().base(); cx[-1].c.p267.validate_data(data)
    parent_summary(saved)
    require(type(archive) is dict and set(archive) == {'schema','records'}
            and archive['schema'] == 'fold-c346-evaluations-v1','C346 evaluation schema')
    records = archive['records']
    require(type(records) is list and type(traces) is list
            and [(r['seed'],r['arm']) for r in records] == identities()
            and [(r['seed'],r['arm']) for r in traces] == identities(),'complete saved three-arm cohort')
    for record,trace,state in zip(records,traces,saved['seed_results'],strict=True):
        require(type(record) is dict and set(record) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and type(record['seed']) is int and type(trace['seed']) is int
                and type(record['state_sha256']) is str and re.fullmatch('[0-9a-f]{64}',record['state_sha256'])
                and record['state_sha256'] == trace['final_sha256'] and record['evaluation_policy'] == 'native_before'
                and set(record['raw']) == set(record['receipts']) == {'evaluation','replay'},'saved state/trace identity')
        for mode in ('evaluation','replay'):
            require(blob(record['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)),'parent evaluation receipt')
            base.validate_raw(record['raw'][mode],data,cx)
        require(base.replay_error(record['raw']['evaluation'],record['raw']['replay'],data,cx) <= 1e-9,'saved evaluation replay')
        require(blob(p.normal_report(record['raw']['evaluation'],data)) == blob(state['normal_by_domain']),'all180parent normal bindings')
    return records


def normal_observations(records, data, saved):
    observations,terminal = [],[]; helper = diagnostic()
    for record,state in zip(records,saved['seed_results'],strict=True):
        raw = record['raw']['evaluation']
        for domain,split in itertools.product(DOMAINS,SPLITS):
            tags = dict(seed=record['seed'],arm=record['arm'],domain=domain,split=split)
            tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
            group = []
            for profile in helper.profiles(domain):
                for pair in helper.terminal_view(tree[split][profile]['normal'],data[split]):
                    group.append(dict(**tags,profile=profile,**pair,collapsed=pair['predictions'][0] == pair['predictions'][1]))
            normal = state['normal_by_domain'][domain][split]
            require(len(group) == normal['query_pairs'] and sum(r['correct_answers'] for r in group) == normal['correct']
                    and sum(r['both_correct'] for r in group) == normal['both_query_correct']
                    and sum(r['collapsed'] for r in group) == normal['collapsed_pairs'],'terminal normal/count binding')
            observations.extend(group)
            terminal.append(dict(**tags,normal=normal,mean_ce=helper.statistics([r['mean_ce'] for r in group]),
                pair_max=helper.statistics([r['pair_max'] for r in group])))
    require(len(observations) == WORK['query_pairs'] and 2*len(observations) == WORK['normal_answers'],'all saved normal answers/pairs')
    require(blob(terminal) == blob(saved['terminal']),'exact180parent terminal binding')
    return dict(pairs=observations),terminal


def transition(control, candidate):
    require(type(control) is bool and type(candidate) is bool,'boolean correctness transition')
    return ('C' if control else 'W')+('C' if candidate else 'W')


def collapse_transition(control, candidate):
    require(type(control) is bool and type(candidate) is bool,'boolean collapse transition')
    return ('same' if control else 'distinct')+'_to_'+('same' if candidate else 'distinct')


def matched_pair(control, candidate):
    require(all(control[k] == candidate[k] for k in PAIR_METADATA)
            and control['arm'] in CONTROLS and candidate['arm'] == CANDIDATE
            and type(control['seed']) is int and control['seed'] in SEEDS
            and control['domain'] in DOMAINS and control['split'] in SPLITS
            and control['profile'] in diagnostic().profiles(control['domain']),'exact matched pair metadata/cohort')
    for row in (control,candidate):
        require(len(row['row_ids']) == len(set(row['row_ids'])) == len(row['targets']) == len(set(row['targets'])) == 2
                and len(row['predictions']) == len(row['per_query_ce']) == 2
                and all(type(v) is int and 0 <= v < 256 for v in [*row['targets'],*row['predictions']]),'matched pair answers')
        for value in row['per_query_ce']: finite(value,True)
        require(row['mean_ce'] == math.fsum(row['per_query_ce'])/2 and row['pair_max'] == max(row['per_query_ce'])
                and type(row['correct_answers']) is int and row['correct_answers'] == sum(a == b for a,b in zip(row['predictions'],row['targets'],strict=True))
                and type(row['both_correct']) is bool and row['both_correct'] is (row['predictions'] == row['targets'])
                and type(row['collapsed']) is bool and row['collapsed'] is (row['predictions'][0] == row['predictions'][1]),'matched pair arithmetic')
    answer_transitions = [transition(a == wanted,b == wanted) for a,b,wanted
                          in zip(control['predictions'],candidate['predictions'],control['targets'],strict=True)]
    return dict(**{k:control[k] for k in PAIR_METADATA},control_arm=control['arm'],candidate_arm=CANDIDATE,
        control_predictions=control['predictions'],candidate_predictions=candidate['predictions'],
        control_per_query_ce=control['per_query_ce'],candidate_per_query_ce=candidate['per_query_ce'],
        query_transitions=answer_transitions,query_ce_deltas=[b-a for a,b in zip(control['per_query_ce'],candidate['per_query_ce'],strict=True)],
        pair_transition=transition(control['both_correct'],candidate['both_correct']),
        collapse_transition=collapse_transition(control['collapsed'],candidate['collapsed']),
        control_mean_ce=control['mean_ce'],candidate_mean_ce=candidate['mean_ce'],mean_ce_delta=candidate['mean_ce']-control['mean_ce'],
        control_pair_max=control['pair_max'],candidate_pair_max=candidate['pair_max'],pair_max_delta=candidate['pair_max']-control['pair_max'],
        control_correct_answers=control['correct_answers'],candidate_correct_answers=candidate['correct_answers'],
        control_both_correct=control['both_correct'],candidate_both_correct=candidate['both_correct'],
        control_collapsed=control['collapsed'],candidate_collapsed=candidate['collapsed'])


def loss_statistics(control, candidate, denominator):
    require(type(control) is list and type(candidate) is list and len(control) == len(candidate)
            and type(denominator) is int and denominator > 0 and len(control) <= denominator,'stratum observations/full denominator')
    for value in control+candidate: finite(value,True)
    n = len(control); a = math.fsum(control); b = math.fsum(candidate)
    differences = [y-x for x,y in zip(control,candidate,strict=True)]; delta = math.fsum(differences)
    result = dict(control_sum=a,candidate_sum=b,delta_sum=delta,control_mean=a/n if n else None,
        candidate_mean=b/n if n else None,delta_mean=delta/n if n else None,
        delta_min=min(differences) if n else None,delta_max=max(differences) if n else None,delta_contribution=delta/denominator)
    check_loss_statistics(result,n,denominator)
    return result


def check_loss_statistics(value, count, denominator):
    require(type(value) is dict and set(value) == set(METRIC_FIELDS)
            and type(count) is int and type(denominator) is int and 0 <= count <= denominator and denominator > 0,'loss statistic schema/count')
    for key in ('control_sum','candidate_sum','delta_sum','delta_contribution'): finite(value[key],key in ('control_sum','candidate_sum'))
    close(value['delta_sum'],value['candidate_sum']-value['control_sum'],'stratum sum difference',max(value['control_sum'],value['candidate_sum']))
    close(value['delta_contribution'],value['delta_sum']/denominator,'full denominator signed contribution')
    if count == 0:
        require(all(value[k] == 0. for k in ('control_sum','candidate_sum','delta_sum','delta_contribution'))
                and all(value[k] is None for k in ('control_mean','candidate_mean','delta_mean','delta_min','delta_max')),'empty stratum zero sums/null means/extrema')
    else:
        for name in ('control','candidate','delta'):
            finite(value[name+'_mean'],name != 'delta')
            close(value[name+'_mean'],value[name+'_sum']/count,'stratum mean arithmetic')
        minimum,maximum = finite(value['delta_min']),finite(value['delta_max'])
        tolerance = 1e-12*max(1.,abs(minimum),abs(maximum))
        require(minimum <= maximum and minimum-tolerance <= value['delta_mean'] <= maximum+tolerance,'stratum delta extrema/bounds')
        if count == 1: require(minimum == maximum == value['delta_sum'],'single observation delta extrema')


def decompose_group(rows, terminal_contrast):
    require(type(rows) is list and rows,'nonempty full matched comparison')
    fields = ('seed','control_arm','candidate_arm','domain','split'); tags = {k:rows[0][k] for k in fields}
    require(all(all(r[k] == tags[k] for k in fields) for r in rows)
            and all(terminal_contrast[k] == tags[k] for k in fields),'comparison coordinate binding')
    answers = [(r['query_transitions'][i],r['control_per_query_ce'][i],r['candidate_per_query_ce'][i]) for r in rows for i in range(2)]
    answer_groups = []
    for label in TRANSITIONS:
        chosen = [(a,b) for transition_name,a,b in answers if transition_name == label]
        answer_groups.append(dict(transition=label,count=len(chosen),ce=loss_statistics([r[0] for r in chosen],[r[1] for r in chosen],len(answers))))
    def partition(field, labels):
        result = []
        for label in labels:
            chosen = [r for r in rows if r[field] == label]
            result.append(dict(transition=label,count=len(chosen),**{metric:loss_statistics(
                [r['control_'+metric] for r in chosen],[r['candidate_'+metric] for r in chosen],len(rows)) for metric in ('mean_ce','pair_max')}))
        return result
    return dict(**terminal_contrast,answer_transitions=answer_groups,
        pair_transitions=partition('pair_transition',TRANSITIONS),collapse_transitions=partition('collapse_transition',COLLAPSE_TRANSITIONS))


def decomposition(observations, saved):
    states = {key:[] for key in itertools.product(SEEDS,ARMS,DOMAINS,SPLITS)}
    seen = set()
    for row in observations['pairs']:
        key = (row['seed'],row['arm'],row['domain'],row['split'])
        identity = (*key,row['profile'],*row['row_ids'])
        require(key in states and identity not in seen,'complete unique observation identity')
        seen.add(identity); states[key].append(row)
    matched,comparisons = [],[]
    for coordinate,terminal_contrast in zip(coordinates(),saved['terminal_contrasts'],strict=True):
        seed,control,domain,split = coordinate
        left,right = [states[seed,arm,domain,split] for arm in (control,CANDIDATE)]
        expected = 288 if split == 'TRAIN' else 144
        require(len(left) == len(right) == expected,'complete matched domain/split pairs')
        rows = [matched_pair(a,b) for a,b in zip(left,right,strict=True)]
        matched.extend(rows); comparisons.append(decompose_group(rows,terminal_contrast))
    require(len(matched) == WORK['matched_pairs'] and 2*len(matched) == WORK['matched_answers'],'complete matched comparison observations')
    return dict(pairs=matched,comparisons=comparisons)


def check_partition(groups, labels, metrics, total, left, right):
    require(type(groups) is list and [g['transition'] for g in groups] == list(labels),'fixed exhaustive transition labels/order')
    for row in groups:
        require(type(row) is dict and set(row) == {'transition','count',*metrics}
                and type(row['count']) is int and 0 <= row['count'] <= total,'transition group schema/count')
        for metric in metrics: check_loss_statistics(row[metric],row['count'],total)
    require(sum(r['count'] for r in groups) == total,'transition partition count conservation')
    for metric in metrics:
        terminal_metric = 'mean_ce' if metric == 'ce' else metric
        a,b = left[terminal_metric]['mean'],right[terminal_metric]['mean']
        for name,wanted in (('control_sum',a),('candidate_sum',b)):
            close(math.fsum(r[metric][name] for r in groups)/total,wanted,'partition full parent loss mean')
        close(math.fsum(r[metric]['delta_contribution'] for r in groups),b-a,'partition full parent loss delta',max(abs(a),abs(b)))
    return {r['transition']:r['count'] for r in groups}


def check_summary(value):
    hashes = ('source_trace_sha256','source_parent_summary_sha256','observations_sha256','decomposition_sha256')
    require(type(value) is dict and set(value) == {*WORK,'diagnostic_complete','parent_validation_summary',
        'terminal','terminal_contrasts','comparisons',*hashes},'diagnostic summary schema')
    require(value['diagnostic_complete'] is True and all(type(value[k]) is int and value[k] == n for k,n in WORK.items()),'diagnostic work')
    saved = parent_summary(value['parent_validation_summary'])
    require(all(type(value[k]) is str and re.fullmatch('[0-9a-f]{64}',value[k]) for k in hashes),'diagnostic provenance hashes')
    require(value['source_parent_summary_sha256'] == digest(saved),'complete parent summary fingerprint')
    require(blob(value['terminal']) == blob(saved['terminal']) and blob(value['terminal_contrasts']) == blob(saved['terminal_contrasts']),
            'exact full parent terminal/contrast binding')
    terminal = {(r['seed'],r['arm'],r['domain'],r['split']):r for r in value['terminal']}
    rows = value['comparisons']; fields = ('seed','control_arm','domain','split')
    require(type(rows) is list and [tuple(r[k] for k in fields) for r in rows] == coordinates(),'all120comparison coordinates')
    for row,parent_row in zip(rows,saved['terminal_contrasts'],strict=True):
        partitions = ('answer_transitions','pair_transitions','collapse_transitions')
        require(set(row) == {*parent_row,*partitions} and type(row['seed']) is int
                and blob({k:row[k] for k in parent_row}) == blob(parent_row),'exact parent comparison fields')
        a,b = [terminal[row['seed'],arm,row['domain'],row['split']] for arm in (row['control_arm'],CANDIDATE)]
        normal = row['normal_contrast']; n,m = normal['answers'],normal['query_pairs']
        answer = check_partition(row['answer_transitions'],TRANSITIONS,('ce',),n,a,b)
        pair = check_partition(row['pair_transitions'],TRANSITIONS,('mean_ce','pair_max'),m,a,b)
        collapse = check_partition(row['collapse_transitions'],COLLAPSE_TRANSITIONS,('mean_ce','pair_max'),m,a,b)
        require(answer['CW'] == normal['regressed'] and answer['WC'] == normal['rescued']
                and answer['CC']+answer['CW'] == normal['control_correct']
                and answer['CC']+answer['WC'] == normal['candidate_correct'],'exact answer transition conservation')
        require(pair['CW'] == normal['pair_regressed'] and pair['WC'] == normal['pair_rescued']
                and pair['CC']+pair['CW'] == normal['control_both_correct']
                and pair['CC']+pair['WC'] == normal['candidate_both_correct'],'exact both-query transition conservation')
        require(collapse['same_to_distinct']+collapse['same_to_same'] == a['normal']['collapsed_pairs']
                and collapse['distinct_to_same']+collapse['same_to_same'] == b['normal']['collapsed_pairs'],'exact collapse transition conservation')
    require(len(value['terminal']) == WORK['terminal_summaries'] and len(value['terminal_contrasts']) == WORK['terminal_contrast_count']
            and len(rows) == WORK['comparison_groups']
            and all(sum(len(r[key]) for r in rows) == WORK[count] for key,count in (
                ('answer_transitions','answer_transition_groups'),('pair_transitions','pair_transition_groups'),
                ('collapse_transitions','collapse_transition_groups'))),'complete diagnostic inventories')


def analyze(traces, archive, saved, data, cx):
    records = check_archive(archive,traces,data,saved,cx)
    observations,terminal = normal_observations(records,data,saved)
    decomposed = decomposition(observations,saved)
    value = dict(diagnostic_complete=True,parent_validation_summary=saved,terminal=terminal,
        terminal_contrasts=saved['terminal_contrasts'],comparisons=decomposed['comparisons'],source_trace_sha256=digest(traces),
        source_parent_summary_sha256=digest(saved),observations_sha256=digest(observations),decomposition_sha256=digest(decomposed),**WORK)
    check_summary(value)
    return observations,decomposed,value


def load_inputs(parent_out, data_out, cx, read):
    previous = parent().previous(); base = previous.source().base()
    data,old,new = previous.load_data(data_out,read)
    require(base.digest(data) == base.DATA_SHA and base.digest(old) == base.PROMPTS_SHA
            and base.digest(new) == base.digest(cx[2].new_prompts(data)),'canonical diagnostic input bytes')
    cx[-1].c.p267.validate_data(data); cx[2].check_prompts(data,old,new,cx[3],cx[-1])
    archive = torch.load(parent_out/'evaluations.pt',map_location='cpu',weights_only=True)
    return read(parent_out/'training-traces.json'),archive,read(parent_out/'validation-summary.json'),data


def reconstructed(parent_out, data_out, cx, read):
    traces,archive,saved,data = load_inputs(parent_out,data_out,cx,read)
    previous = parent().previous()
    before = previous.state_hash((traces,archive,saved,data))
    result = analyze(traces,archive,saved,data,cx)
    require(previous.state_hash((traces,archive,saved,data)) == before,'source trace/logit/data mutation')
    return result


def run_diagnostic(out, parent_out, data_out, cx, read):
    observations,decomposed,value = reconstructed(parent_out,data_out,cx,read)
    for name,item in zip(OUTPUTS,(manifest(),observations,decomposed,value),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(item))
    return value


def semantic_recheck(out, parent_out, data_out, cx, read):
    observations,decomposed,value = reconstructed(parent_out,data_out,cx,read)
    for name,item in zip(OUTPUTS,(manifest(),observations,decomposed,value),strict=True):
        require(blob(read(out/name)) == blob(item),'saved transition reconstruction:'+name)
    return value


def report_results(value, emit):
    check_summary(value)
    for key,label in (('terminal','C347 parent terminal objective'),('terminal_contrasts','C347 parent terminal contrast'),
                      ('comparisons','C347 loss transition decomposition')):
        for row in value[key]: emit(label,row)
    emit('C347 source provenance',{k:value[k] for k in ('source_trace_sha256','source_parent_summary_sha256','observations_sha256','decomposition_sha256')})
    emit('C347 preserved parent result',dict(candidate_gate=value['parent_validation_summary']['candidate_gate'],
        eligible_seed_count=value['parent_validation_summary']['eligible_seed_count']))
    emit('C347 diagnostic inventory',dict(WORK))
    return dict(WORK)
