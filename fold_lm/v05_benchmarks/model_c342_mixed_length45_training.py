"""C342: restore half the original-family length-four exposure at fixed budget."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C342-v5b-mixed-length45-training'
STAGE = 'V5-B-MIXED-LENGTH45-TRAINING'
SEEDS = tuple(range(342001,342006))
ORDERS = tuple(range(342101,342106))
ARMS = ('original5','mixed45')
PROFILES = ('repeat','shared_prefix','shared_suffix')
CYCLE, STEPS, FIT_RNG = 1200, 2400, 612000
FIRST_QUOTAS = (8,8,9)
RATES = (.005,.0005)
TRAIN_TOKENS = {'original5':3225600,'mixed45':3168000}
DOMAINS = tuple('original'+str(n) for n in range(2,7))+('interior4',)
OWN = ('fold_lm/v05_benchmarks/model_c342_mixed_length45_training.py',
       'tools/c342_execution.py','tests_lm/test_v05_c342_mixed_length45_training.py',
       'tests_lm/test_v05_c342_execution.py','tools/run_c342.ps1',
       'tools/invoke_c342.ps1','docs/experiment-ledger-addendum-c342-preregistration.md')
OUTPUTS = ('experiment-plan.json','training-traces.json','trained-models.pt',
           'evaluations.pt','measurements.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 64, 6378, 235
SOURCE_COUNT, INPUT_COUNT = 916, 7205
WORK = dict(training_models=10,evaluation_models=10,checkpoint_states=10,
    optimizer_creations=10,train_steps=24000,gradient_calls=24000,optimizer_steps=24000,
    training_rows=1152000,model_forward_calls=27420,row_presentations=1480320,
    core_forward_calls=109680,query_projection_calls=54840,model_state_loads=20,
    checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA = '538150bd2b43ff286e4d5b0e0c1d665ea1e1c4d43cf8148cba1c5d1a4192734c'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def previous():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c332_trained_first_mean_query')


def reference():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c340_length5_training')


def support():
    return reference().support()


def identities():
    return list(itertools.product(SEEDS,ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base='d8ab608b482d877a3927ef48b0f03a4212451aa1',
        parent_execution='a6a052912d52f786dd8c809ed6e8e96996c74edd',
        parent_summary='ec30706ed3761c7b36c4ef215a85c53ccc79cbd1ffb271a5b387fe2049b406eb',
        parent_envelope='6cc5988f3126f0b51a2d5543755cf58471e8839354e3dcf6bc86b7ce1f30ac8e',
        question='does restoring half of original-family slot4 TRAIN exposure to canonical length4 improve original4 versus all5 while retaining every evaluated domain at equal updates',
        seeds=list(SEEDS),orders=list(ORDERS),arms=list(ARMS),cycle=CYCLE,steps=STEPS,fit_rng=FIT_RNG,
        changed='actual original-family slot4 TRAIN tokens only: all canonical5 versus fixed balanced canonical4/5;no other training row,loss or readout change',
        held='paired fresh weights,logical192TRAIN rows,targets,1200events repeated twice,batch4 family mask,original2/3 and interior4 tokens,ordinaryCE,native readout,optimizer,rates,capacity,scorers',
        allocation='immutable C326 balanced_allocation on original-only slot4 query-pair edges per profile in cycle1;exact corresponding-event complement in cycle2;both query rows stay together;no fallback',
        available_per_pair_profile_per_cycle=[16,17,17],first_cycle_length4_quotas=list(FIRST_QUOTAS),
        second_cycle_length4_quotas=[8,9,8],first_cycle_length5_quotas=[8,9,8],second_cycle_length5_quotas=list(FIRST_QUOTAS),
        actual_per_row_exposure={'original5':dict(original2=200,original3=200,original4=0,original5=100,interior4=100),
                                'mixed45':dict(original2=200,original3=200,original4=50,original5=50,interior4=100)},
        per_cycle_candidate='each logical TRAIN row:original2=100,original3=100,original4=25,original5=25,interior4=50',
        mixed_update='unchanged11..13 original query pairs plus interior;each original actual length contributes5..8pairs per slot4 update',
        never_train='original6,all HOLDOUT logical rows and all masked prompts',
        compute_boundary='equal updates,row presentations and padded64 frames;actual nonpadding tokens including BOS/EOS differ and are measured,not FLOP-equivalence',
        nonpadding_training_tokens_per_model=dict(TRAIN_TOKENS),
        input_proof='reconstruct canonical banks/events/family mask/length mask plus actual little-endian int64 token-and-target stream SHA256',
        optimizer='core_slow AdamW noncore.005/core.0005 betas.9/.999 eps1e-8 decay0/globalclip1;one optimizer,ordinary mean CE256',
        gate='all5candidate full original2..6 and interior4 gates;each seed EACH of6domains nonnegative normal HOLDOUT answer AND query-pair gains;strict aggregate original4 answer AND pair gains',
        saturation='all5-control original4 perfection or a strict-endpoint tie remains a valid negative;no threshold or cohort relaxation',
        estimand='new original4 repair comparison against freshly fitted all5;does not re-estimate C340 six-character gain against original4 or change C340 negative',
        support_counts='raw all256-argmax answer kinds descriptive only;no auxiliary loss or supplied-value inference filter',
        thresholds=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,both_order=.80),
        parameters=14256,core_parameters=3328,slots=64,precision='cpu float64',threads=2,
        evaluation_policy='native_before in both arms;full114views per state,exact argmax and1e-9 replay;all fits finish before any saved evaluation',
        preflight='all5 actual schedules/allocations/token streams;discarded native model,botharms/bothcycles/original+interior/English+Japanese;16forwards/32rows/8backwards/0updates',
        boundary='one fixed50:50 allocation,seen canonical templates/reused value split;ratio and temporal assignment are part of intervention;no optimum or causal shortcut/capacity claim',
        source_count=SOURCE_COUNT,input_count=INPUT_COUNT,parent_files=475,parent_test_proof_files=469,
        own_tests=OWN_TESTS,full_tests=FULL_TESTS,modules=MODULES,outputs=list(OUTPUTS),
        raw_logit_payload_bytes=672399360,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA,'C342 manifest seal')


def prepared(data, old, new, cx):
    """Unchanged C340 canonical banks; TRAIN fitting chooses between them explicitly."""
    return reference().prepared(data,old,new,cx)


def make_model(seed, x):
    require(type(seed) is int and seed in SEEDS,'fresh C342 seed')
    c = x.c
    ref = c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    model = x.policy.configure(x.wide.LengthReadout(ref),'core_slow')
    require(type(model) is x.wide.LengthReadout and model.backbone.config.max_tokens == 64
            and model.backbone.core.config.slots == 64,'native architecture')
    require(sum(v.numel() for v in model.parameters()) == 14256
            and sum(v.numel() for v in model.backbone.core.parameters()) == 3328,'capacity')
    require(c.base.fingerprint(model) == c.base.fingerprint(ref) and list(model.state_dict()) == list(ref.state_dict()),'native initialization')
    require(all(v.requires_grad and v.dtype == torch.float64 and v.device.type == 'cpu' for v in model.parameters()),'precision/gradient')
    x.policy.parameter_groups(model,'core_slow')
    return model


def make_pair(seed, x):
    models = {arm:make_model(seed,x) for arm in ARMS}; p = previous()
    require(p.state_hash(models[ARMS[0]].state_dict()) == p.state_hash(models[ARMS[1]].state_dict()),'paired initial weights')
    pointers = [{v.data_ptr() for v in m.parameters() if v.numel()} for m in models.values()]
    require(not pointers[0]&pointers[1],'independent paired storage')
    return models


def schedule(seed, rows, x):
    require(type(seed) is int and seed in SEEDS and len(rows) == 192,'TRAIN schedule identity')
    q = previous().source().curriculum()
    events = x.parent.plan_for_order(ORDERS[SEEDS.index(seed)],'two_to_four',rows,x.p312,x.pairs)
    q.validate_schedule(events)
    return events,q.family_mask(events,'batch4')


def length_mask(events, family, arm):
    """One bit selects canonical4; zero retains canonical5 on original slot4 only."""
    require(type(arm) is str and arm in ARMS,'registered length-mixture arm')
    q = previous().source().curriculum(); q.validate_schedule(events)
    require(isinstance(family,torch.Tensor) and family.dtype == torch.int64 and family.device.type == 'cpu'
            and torch.equal(family,q.family_mask(events,'batch4')),'unchanged family mask')
    chosen = torch.zeros((STEPS,24),dtype=torch.int64)
    if arm == 'mixed45':
        raw,mask = events.tolist(),family.tolist()
        pairs = sorted({tuple(sorted(row[2:])) for event in raw[:4] for row in event})
        index = {pair:i for i,pair in enumerate(pairs)}
        require(len(pairs) == 96,'complete query-pair inventory')
        for profile,quota in enumerate(FIRST_QUOTAS):
            steps = [i for i,event in enumerate(raw) if event[0][:2] == [4,profile]]
            neighbors = [[index[tuple(sorted(row[2:]))] for row,f in zip(raw[i],mask[i],strict=True) if f == 0] for i in steps]
            require([sum(j in row for row in neighbors) for j in range(96)] == [16 if profile == 0 else 17]*96,'available pair/profile exposure')
            allocated,_ = q.balanced_allocation(neighbors,[quota]*96)
            for i,take in zip(steps,allocated,strict=True):
                chosen[i] = torch.tensor([int(f == 0 and index[tuple(sorted(row[2:]))] in take)
                    for row,f in zip(raw[i],mask[i],strict=True)],dtype=torch.int64)
        eligible = ((events[:,:,0] == 4)&(family == 0)).to(torch.int64)
        chosen[CYCLE:] = eligible-chosen[:CYCLE]
    check_length_mask(events,family,arm,chosen)
    return chosen


def check_length_mask(events, family, arm, selected):
    require(type(arm) is str and arm in ARMS and isinstance(selected,torch.Tensor)
            and selected.shape == (STEPS,24) and selected.dtype == torch.int64 and selected.device.type == 'cpu'
            and bool(((selected == 0)|(selected == 1)).all()),'length selection contract')
    require(events.shape == (CYCLE,24,4) and family.shape == (CYCLE,24),'length selection schedule')
    eligible = ((events[:,:,0] == 4)&(family == 0)).to(torch.int64)
    require(not bool((selected > eligible.repeat(2,1)).any()),'length selection leaked outside original slot4')
    if arm == 'original5':
        require(not bool(selected.any()),'all5 control changed')
        return
    require(torch.equal(selected[:CYCLE]+selected[CYCLE:],eligible),'exact second-cycle complement')
    q = previous().source().curriculum()
    counts = q.exposure(events,selected[:CYCLE])
    for key,values in counts.items():
        n,profile,_,_ = map(int,key.split(':'))
        require(values[1] == (FIRST_QUOTAS[profile] if n == 4 else 0),'fixed first-cycle pair/profile quota')
    positions = (events[:,0,0] == 4).repeat(2)
    four = selected.sum(1)[positions]
    five = (eligible.repeat(2,1)-selected).sum(1)[positions]
    require(bool(((four >= 5)&(four <= 8)&(five >= 5)&(five <= 8)).all()),'both lengths in every mixed update')


def actual_exposure(events, family, selected, arm):
    check_length_mask(events,family,arm,selected)
    result = [{k:[0]*192 for k in DOMAINS} for _ in range(2)]
    for step,bits in enumerate(selected.tolist()):
        for row,f,short in zip(events[step%CYCLE].tolist(),family[step%CYCLE].tolist(),bits,strict=True):
            n,profile,a,b = row
            require(n in (2,3,4) and profile in (0,1,2) and f in (0,1) and (n == 4 or f == 0),'exposure domain')
            domain = 'interior4' if f else 'original'+str((4 if short else 5) if n == 4 else n)
            for i in (a,b): result[step//CYCLE][domain][i] += 1
    expected = dict(original2=100,original3=100,original4=25 if arm == 'mixed45' else 0,
                    original5=25 if arm == 'mixed45' else 50,original6=0,interior4=50)
    require(all(v[k] == [n]*192 for v in result for k,n in expected.items()),'actual per-row/per-cycle exposure')
    return result


def select_tokens(tables, event, family, selected):
    """Target labels are never available to the token selector."""
    require(selected.shape == family.shape == (24,) and selected.dtype == torch.int64
            and bool(((selected == 0)|(selected == 1)).all()),'batch length selection')
    n,p = map(int,event[0,:2])
    require(not bool((selected.bool()&((family != 0)|(n != 4))).any()),'batch substitution boundary')
    tokens,ids = previous().source().curriculum().select_tokens(tables['original5'],event,family)
    if bool(selected.any()):
        four = tables['original4']['original'][4,PROFILES[p]][ids]
        tokens = torch.where(selected.repeat_interleave(2)[:,None].bool(),four,tokens)
    return tokens,ids


def training_fingerprint(tables, y, events, family, selected):
    p = previous()
    banks = {name:p.training_fingerprint(table,y,events,family) for name,table in tables.items()}
    return p.state_hash(dict(banks=banks,length_mask=selected))


def stream_update(value, tokens, y, ids):
    value.update(tokens.contiguous().numpy().astype('<i8',copy=False).tobytes())
    value.update(y[ids].contiguous().numpy().astype('<i8',copy=False).tobytes())


def input_accounting(tables, y, events, family, selected):
    value = hashlib.sha256(b'C342 TRAIN int64le tokens then targets per update\n'); count = 0
    for step in range(STEPS):
        tokens,ids = select_tokens(tables,events[step%CYCLE],family[step%CYCLE],selected[step])
        count += int((tokens != 256).sum()); stream_update(value,tokens,y,ids)
    return count,value.hexdigest()


def optimize(model, arm, tables, y, events, family, selected, x):
    require(arm in ARMS and len(events) == len(family) == CYCLE and len(selected) == STEPS == 2*CYCLE,'registered cycles')
    p = previous(); torch.manual_seed(FIT_RNG)
    opt = x.policy.optimizer_for(model,'core_slow'); opt_id = id(opt)
    initial = p.state_hash(model.state_dict()); core_initial = p.state_hash(model.backbone.core.state_dict())
    losses,rates,counts,indices = [],[],[],[]; union = {}; boundary = None; continuation = None
    stream = hashlib.sha256(b'C342 TRAIN int64le tokens then targets per update\n'); nonpadding = 0
    model.train()
    with torch.enable_grad(),p.readouts().readout(model,x.wide,'native_before') as stats:
        for step in range(STEPS):
            if step == CYCLE:
                continuation = dict(weights=p.state_hash(model.state_dict()),optimizer=p.state_hash(opt.state_dict()))
                require(continuation == boundary,'optimizer/weight reset')
            require(id(opt) == opt_id,'optimizer replaced'); x.policy.verify_optimizer(opt,model,'core_slow')
            rate = [g['lr'] for g in opt.param_groups]; require(rate == list(RATES),'fixed rates'); rates.append(rate)
            index = step%CYCLE; indices.append(index); opt.zero_grad(set_to_none=True)
            tokens,ids = select_tokens(tables,events[index],family[index],selected[step])
            require(len(ids) == 48,'TRAIN batch'); nonpadding += int((tokens != 256).sum()); stream_update(stream,tokens,y,ids)
            logits = model(tokens,torch.zeros(len(ids),dtype=torch.int64)); x.c.p267.check_logits(logits,len(ids))
            loss = F.cross_entropy(logits,y[ids])
            require(bool(torch.isfinite(loss)) and float(loss.detach()) >= 0,'finite CE')
            losses.append(float(loss.detach())); loss.backward()
            got = {name:v.numel() for name,v in model.named_parameters() if v.grad is not None}
            require(got,'missing gradients'); counts.append(sum(got.values())); union.update(got)
            torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True); opt.step()
            if step+1 == CYCLE: boundary = dict(weights=p.state_hash(model.state_dict()),optimizer=p.state_hash(opt.state_dict()))
            if (step+1)%200 == 0: print(f'[C342] arm={arm} step={step+1}/{STEPS} ce={losses[-1]:.6f}',flush=True)
    model.eval(); require(boundary is not None and boundary == continuation,'continuous optimizer')
    require(stats == dict(calls=STEPS,query_calls=2*STEPS,rows=48*STEPS,grad_calls=STEPS),'TRAIN receipt')
    state = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    require(p.state_hash(state) == p.state_hash(model.state_dict()) and all(v.numel() == 0 or state[k].data_ptr() != v.data_ptr()
            for k,v in model.state_dict().items()),'deep checkpoint')
    return dict(arm=arm,readout_mode='native_before',length_policy=arm,steps=STEPS,
        initial_sha256=initial,final_sha256=p.state_hash(state),core_initial_sha256=core_initial,
        core_final_sha256=p.state_hash(model.backbone.core.state_dict()),ce_history=losses,
        optimizer_group_lrs=rates,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())),
        event_indices=indices,policy_receipt=dict(stats),boundary=boundary,continuation=continuation,
        optimizer_creations=1,intermediate_evaluations=0,nonpadding_token_presentations=nonpadding,
        actual_training_stream_sha256=stream.hexdigest()),state


def train_one(seed, arm, model, tables, y, rows, cx, root, pins):
    p = previous(); x = cx[-1]; p.source().base().check_dependencies(root,pins,cx,model)
    events,family = schedule(seed,rows,x); selected = length_mask(events,family,arm)
    before = training_fingerprint(tables,y,events,family,selected); exposure = actual_exposure(events,family,selected,arm)
    print(f'[C342] seed={seed} arm={arm} phase=training',flush=True)
    with x.c.p267.counted(model,x.c.core) as (calls,cores):
        trace,state = optimize(model,arm,tables,y,events,family,selected,x)
    require(calls == [2400,115200] and cores[0] == 9600,'measured TRAIN work')
    require(training_fingerprint(tables,y,events,family,selected) == before,'TRAIN input mutation')
    count,stream = input_accounting(tables,y,events,family,selected)
    require(trace['nonpadding_token_presentations'] == count == TRAIN_TOKENS[arm]
            and trace['actual_training_stream_sha256'] == stream,'measured TRAIN token stream')
    trace.update(seed=seed,training_input_sha256=before,
        logical_training_sha256=p.state_hash(dict(targets=y,events=events,mask=family)),
        schedule_sha256=digest(events.tolist()),mask_sha256=digest(family.tolist()),length_mask_sha256=digest(selected.tolist()),
        family_exposure_per_cycle=p.source().curriculum().exposure(events,family),actual_exposure_per_cycle=exposure)
    return trace,state


def check_trace(t, rows, x, tables, y):
    p = previous(); require(type(t['seed']) is int and t['seed'] in SEEDS and t['arm'] in ARMS,'trace identity')
    events,family = schedule(t['seed'],rows,x); selected = length_mask(events,family,t['arm'])
    require(t['readout_mode'] == 'native_before' and t['length_policy'] == t['arm'],'trace token/readout policy')
    require(type(t['steps']) is int and t['steps'] == STEPS and t['event_indices'] == list(range(CYCLE))*2
            and all(type(v) is int for v in t['event_indices']),'event budget/order')
    require(t['schedule_sha256'] == digest(events.tolist()) and t['mask_sha256'] == digest(family.tolist())
            and t['length_mask_sha256'] == digest(selected.tolist())
            and t['family_exposure_per_cycle'] == p.source().curriculum().exposure(events,family)
            and t['actual_exposure_per_cycle'] == actual_exposure(events,family,selected,t['arm']),'actual exposure reconstruction')
    count,stream = input_accounting(tables,y,events,family,selected)
    require(type(t['nonpadding_token_presentations']) is int and t['nonpadding_token_presentations'] == count == TRAIN_TOKENS[t['arm']]
            and t['actual_training_stream_sha256'] == stream,'reconstructed token stream')
    require(t['training_input_sha256'] == training_fingerprint(tables,y,events,family,selected)
            and t['logical_training_sha256'] == p.state_hash(dict(targets=y,events=events,mask=family)),'TRAIN input recipe fingerprint')
    require(t['optimizer_group_lrs'] == [list(RATES)]*STEPS and len(t['ce_history']) == STEPS
            and all(type(v) is float and math.isfinite(v) and v >= 0 for v in t['ce_history']),'rates/CE history')
    union,counts = t['gradient_union'],t['gradient_parameter_counts']
    require(union and all(type(k) is str and type(v) is int and v > 0 for k,v in union.items()) and 0 < sum(union.values()) <= 14256
            and len(counts) == STEPS and all(type(v) is int and 0 < v <= sum(union.values()) for v in counts),'gradient inventory')
    for key in ('initial_sha256','final_sha256','core_initial_sha256','core_final_sha256','training_input_sha256',
                'logical_training_sha256','actual_training_stream_sha256','length_mask_sha256'):
        require(type(t[key]) is str and re.fullmatch('[0-9a-f]{64}',t[key]),'state/input fingerprint')
    require(t['initial_sha256'] != t['final_sha256'] and t['core_initial_sha256'] != t['core_final_sha256'],'trained state')
    require(t['boundary'] == t['continuation'] and set(t['boundary']) == {'weights','optimizer'}
            and all(type(v) is str and re.fullmatch('[0-9a-f]{64}',v) for v in t['boundary'].values()),'continued state')
    require(type(t['optimizer_creations']) is int and t['optimizer_creations'] == 1 and type(t['intermediate_evaluations']) is int
            and t['intermediate_evaluations'] == 0 and t['policy_receipt'] == dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400),'no restart/selection')


def fixed_gate(pairs):
    require([r['seed'] for r in pairs] == list(SEEDS) and all(type(r['seed']) is int for r in pairs),'all paired seeds')
    eligible = []
    for r in pairs:
        require(type(r['candidate_full_pass']) is bool and set(r['original_by_length']) == set(map(str,range(2,7))),'full gate/domain types')
        domains = [r['original_by_length'][str(n)] for n in range(2,7)]+[r['interior']]
        gains = [z[key] for z in domains for key in ('answer_gain','query_pair_gain')]
        require(all(type(v) is int for v in gains),'per-domain gain types')
        eligible.append(r['candidate_full_pass'] and all(v >= 0 for v in gains))
    strict = all(sum(r['original_by_length']['4'][key] for r in pairs) > 0 for key in ('answer_gain','query_pair_gain'))
    return all(eligible) and strict,eligible


def check_summary(v):
    p = previous()
    require(all(type(v[k]) is int and v[k] == n for k,n in WORK.items()) and v['paired_conditions_valid'] is True
            and v['all_replays'] is True and v['evaluation_policy'] == 'native_before','work/integrity')
    require([(r['seed'],r['arm']) for r in v['seed_results']] == identities() and len(v['paired_comparisons']) == 5,'cohort')
    for i,pair in enumerate(v['paired_comparisons']):
        require(all(type(pair[key]) is int for key in ('four_answer_gain','four_pair_gain','six_answer_gain','six_pair_gain',
            'short_answer_gain','short_pair_gain','interior_answer_gain','interior_pair_gain')),'derived gain types')
        for offset,key in ((0,'control_full_pass'),(1,'candidate_full_pass')):
            f = v['seed_results'][2*i+offset]
            require(set(f['original_pass']) == set(map(str,range(2,7))) and all(type(b) is bool for b in f['original_pass'].values())
                    and type(f['interior_pass']) is bool and f['retention_pass'] is all(f['original_pass'].values())
                    and pair[key] is (f['retention_pass'] and f['interior_pass']),'full gate binding')
            require(type(f['training_nonpadding_tokens']) is int and f['training_nonpadding_tokens'] == TRAIN_TOKENS[f['arm']],'measured effective tokens')
            require(set(f['support']) == set(DOMAINS),'support domains')
            for r in f['support'].values():
                kinds = support().audit().KINDS
                require(set(r) == {'answers',*kinds} and r['answers'] == 288 and type(r['answers']) is int
                        and all(type(r[k]) is int and r[k] >= 0 for k in kinds)
                        and sum(r[k] for k in kinds) == 288,'support partition')
        old,inside = pair['original_by_length'],pair['interior']
        require(set(old) == set(map(str,range(2,7))),'all comparison domains')
        for domain,z in [('interior4',inside)]+[('original'+n,z) for n,z in old.items()]:
            p.contrast_check(z)
            require(z['control_correct'] == v['seed_results'][2*i]['support'][domain]['correct']
                    and z['candidate_correct'] == v['seed_results'][2*i+1]['support'][domain]['correct'],'support/contrast binding')
        require(pair['four_answer_gain'] == old['4']['answer_gain'] and pair['four_pair_gain'] == old['4']['query_pair_gain']
                and pair['six_answer_gain'] == old['6']['answer_gain'] and pair['six_pair_gain'] == old['6']['query_pair_gain']
                and pair['short_answer_gain'] == sum(old[str(n)]['answer_gain'] for n in (2,3,5))
                and pair['short_pair_gain'] == sum(old[str(n)]['query_pair_gain'] for n in (2,3,5))
                and pair['interior_answer_gain'] == inside['answer_gain'] and pair['interior_pair_gain'] == inside['query_pair_gain'],'gate count binding')
    gate,eligible = fixed_gate(v['paired_comparisons'])
    require(v['candidate_gate'] is gate and type(v['eligible_seed_count']) is int and v['eligible_seed_count'] == sum(eligible),'fixed gate')


def analyze(traces, records, states, data, cx, tables, y):
    p = previous(); q = p.readouts(); reference().validate_tables(tables,y)
    require([(t['seed'],t['arm']) for t in traces] == [(r['seed'],r['arm']) for r in records] == identities()
            and len(states) == 10,'complete trained cohort')
    metrics,flags = [],[]
    for t,r,state in zip(traces,records,states,strict=True):
        check_trace(t,data['TRAIN'],cx[-1],tables,y)
        require(set(r) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and r['state_sha256'] == t['final_sha256'] == p.state_hash(state) and r['evaluation_policy'] == 'native_before'
                and set(r['raw']) == set(r['receipts']) == {'evaluation','replay'},'state binding')
        for mode in ('evaluation','replay'):
            p.source().base().validate_raw(r['raw'][mode],data,cx)
            require(blob(r['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)),'evaluation receipt')
        require(p.source().base().replay_error(r['raw']['evaluation'],r['raw']['replay'],data,cx) <= 1e-9,'saved replay')
        score,f = q.summarize_mode(r['raw']['evaluation'],data,cx)
        metrics.append(dict(seed=t['seed'],arm=t['arm'],score=score))
        flags.append(dict(seed=t['seed'],arm=t['arm'],training_nonpadding_tokens=t['nonpadding_token_presentations'],
            support=support().support_report(r['raw']['evaluation'],data),**f))
    pairs = []
    for i,seed in enumerate(SEEDS):
        a,b = traces[2*i:2*i+2]
        require(all(a[k] == b[k] for k in ('initial_sha256','core_initial_sha256','logical_training_sha256',
            'schedule_sha256','mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs'))
            and all(a[k] != b[k] for k in ('training_input_sha256','actual_training_stream_sha256','length_mask_sha256')),'paired conditions/token intervention')
        compare = q.compare(records[2*i]['raw']['evaluation'],records[2*i+1]['raw']['evaluation'],data,p.source().base())
        old,inside = compare['original_by_length'],compare['interior']
        pairs.append(dict(seed=seed,control_full_pass=flags[2*i]['retention_pass'] and flags[2*i]['interior_pass'],
            candidate_full_pass=flags[2*i+1]['retention_pass'] and flags[2*i+1]['interior_pass'],
            four_answer_gain=old['4']['answer_gain'],four_pair_gain=old['4']['query_pair_gain'],
            six_answer_gain=old['6']['answer_gain'],six_pair_gain=old['6']['query_pair_gain'],
            short_answer_gain=sum(old[str(n)]['answer_gain'] for n in (2,3,5)),
            short_pair_gain=sum(old[str(n)]['query_pair_gain'] for n in (2,3,5)),
            interior_answer_gain=inside['answer_gain'],interior_pair_gain=inside['query_pair_gain'],**compare))
    gate,eligible = fixed_gate(pairs)
    value = dict(candidate_gate=gate,eligible_seed_count=sum(eligible),paired_conditions_valid=True,all_replays=True,
        evaluation_policy='native_before',seed_results=flags,paired_comparisons=pairs,**WORK)
    check_summary(value)
    return metrics,value


def load_states(path):
    value = torch.load(path,map_location='cpu',weights_only=True)
    require(set(value) == {'schema','identities','states'} and value['schema'] == 'fold-c342-trained-models-v1'
            and value['identities'] == [list(z) for z in identities()] and len(value['states']) == 10,'model bundle')
    return value['states']


def run_training(out, data_out, cx, root, pins, read):
    p = previous(); data,old,new = p.load_data(data_out,read); before = digest((data,old,new))
    tables,y = prepared(data,old,new,cx); traces,states = [],[]
    for seed in SEEDS:
        models = make_pair(seed,cx[-1])
        for arm in ARMS:
            trace,state = train_one(seed,arm,models[arm],tables,y,data['TRAIN'],cx,root,pins)
            traces.append(trace); states.append(state)
        del models
    with (out/'trained-models.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c342-trained-models-v1',identities=[list(z) for z in identities()],states=states),stream)
    saved = load_states(out/'trained-models.pt')
    require([p.state_hash(v) for v in saved] == [p.state_hash(v) for v in states],'checkpoint roundtrip')
    records = []
    for (seed,arm),state in zip(identities(),saved,strict=True):
        model = make_model(seed,cx[-1]); p.source().base().check_dependencies(root,pins,cx,model)
        model.eval(); model.requires_grad_(False); raw,receipts = {},{}
        for kind in ('evaluation','replay'):
            model.load_state_dict(state,strict=True); require(p.state_hash(model.state_dict()) == p.state_hash(state),'loaded state')
            raw[kind],receipts[kind] = p.readouts().measure(model,'native_before',data,old,new,cx)
            require(p.state_hash(model.state_dict()) == p.state_hash(state),'evaluation weight mutation')
        records.append(dict(seed=seed,arm=arm,state_sha256=p.state_hash(state),evaluation_policy='native_before',raw=raw,receipts=receipts))
        print(f'[C342] seed={seed} arm={arm} native_saved_evaluation_and_replay=COMPLETE',flush=True)
    metrics,value = analyze(traces,records,saved,data,cx,tables,y)
    require(digest((data,old,new)) == before,'data/prompt mutation')
    with (out/'evaluations.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c342-evaluations-v1',records=records),stream)
    for name,item in (('experiment-plan.json',manifest()),('training-traces.json',traces),('measurements.json',metrics),('validation-summary.json',value)):
        with (out/name).open('xb') as stream: stream.write(blob(item))
    return value


def semantic_recheck(out, data_out, cx, read):
    data,old,new = previous().load_data(data_out,read); tables,y = prepared(data,old,new,cx)
    archive = torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c342-evaluations-v1','evaluation schema')
    metrics,value = analyze(read(out/'training-traces.json'),archive['records'],load_states(out/'trained-models.pt'),data,cx,tables,y)
    for name,item in (('experiment-plan.json',manifest()),('measurements.json',metrics),('validation-summary.json',value)):
        require(blob(read(out/name)) == blob(item),'saved training reconstruction:'+name)
    return value


def native_preflight(data_out, cx, root, pins, read):
    p = previous(); x = cx[-1]; data,old,new = p.load_data(data_out,read); tables,y = prepared(data,old,new,cx)
    for seed in SEEDS:
        events,family = schedule(seed,data['TRAIN'],x)
        for arm in ARMS:
            chosen = length_mask(events,family,arm); actual_exposure(events,family,chosen,arm)
            require(input_accounting(tables,y,events,family,chosen)[0] == TRAIN_TOKENS[arm],'preflight actual tokens')
    events,family = schedule(SEEDS[0],data['TRAIN'],x)
    policies = {arm:length_mask(events,family,arm) for arm in ARMS}
    model = make_model(SEEDS[0],x); p.source().base().check_dependencies(root,pins,cx,model)
    with torch.no_grad():
        w = model.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
    initial = p.state_hash(model.state_dict())
    for arm,cycle,kind in itertools.product(ARMS,range(2),('original','interior4')):
        selected_rows = []
        for lang in ('en','ja'):
            found = None
            for i,event in enumerate(events):
                if int(event[0,0]) != 4: continue
                tokens,ids = select_tokens(tables,event,family[i],policies[arm][cycle*CYCLE+i])
                eligible = family[i].repeat_interleave(2).bool()
                for j,row_id in enumerate(ids.tolist()):
                    if data['TRAIN'][row_id]['language'] == lang and bool(eligible[j]) == (kind == 'interior4'):
                        found = tokens[j],y[row_id]; break
                if found is not None: break
            require(found is not None,'native preflight language/family coverage'); selected_rows.append(found)
        tokens = torch.stack([z[0] for z in selected_rows]); target = torch.stack([z[1] for z in selected_rows])
        tasks = torch.zeros(2,dtype=torch.int64); model.train()
        with torch.no_grad(): expected = model(tokens,tasks)
        model.zero_grad(set_to_none=True)
        with torch.enable_grad(),p.readouts().readout(model,x.wide,'native_before') as stats:
            logits = model(tokens,tasks); p.readouts().same(expected,logits.detach()); F.cross_entropy(logits,target).backward()
        require(stats == dict(calls=1,query_calls=2,rows=2,grad_calls=1) and model.read.query.weight.grad is not None
                and all(v.grad is None or bool(torch.isfinite(v.grad).all()) for v in model.parameters()),'native backward')
    require(p.state_hash(model.state_dict()) == initial,'preflight changed weights')
    print('C342_native_preflight=PASS;schedules=5;forwards=16;rows=32;backward=8;updates=0',flush=True)
