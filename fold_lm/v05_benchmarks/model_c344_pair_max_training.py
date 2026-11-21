"""C344: maximum full-class CE within each TRAIN query pair at fixed mixed45 budget."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C344-v5b-pair-max-training'
STAGE = 'V5-B-PAIR-MAX-TRAINING'
SEEDS = tuple(range(344001,344006))
ORDERS = tuple(range(344101,344106))
ARMS = ('mean_ce','pair_max')
PROFILES = ('repeat','shared_prefix','shared_suffix')
CYCLE, STEPS, FIT_RNG = 1200, 2400, 612000
RATES = (.005,.0005)
TRAIN_TOKENS = {arm:3168000 for arm in ARMS}
SPLITS = ('TRAIN','HOLDOUT')
LOSS_TOL = 1e-12
DOMAINS = tuple('original'+str(n) for n in range(2,7))+('interior4',)
OWN = ('fold_lm/v05_benchmarks/model_c344_pair_max_training.py',
       'tools/c344_execution.py','tests_lm/test_v05_c344_pair_max_training.py',
       'tests_lm/test_v05_c344_execution.py','tools/run_c344.ps1',
       'tools/invoke_c344.ps1','docs/experiment-ledger-addendum-c344-preregistration.md')
OUTPUTS = ('experiment-plan.json','training-traces.json','trained-models.pt',
           'evaluations.pt','measurements.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 72, 6514, 239
SOURCE_COUNT, INPUT_COUNT = 930, 8183
WORK = dict(training_models=10,evaluation_models=10,checkpoint_states=10,
    optimizer_creations=10,train_steps=24000,gradient_calls=24000,optimizer_steps=24000,
    training_rows=1152000,model_forward_calls=27420,row_presentations=1480320,
    core_forward_calls=109680,query_projection_calls=54840,model_state_loads=20,
    checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA = 'a663ebb0b09671c6d277b5abec6d09604a49a194d5d61409a1a5bf5018785ad8'


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
    return importlib.import_module('fold_lm.v05_benchmarks.model_c342_mixed_length45_training')


def support():
    return reference().support()


def identities():
    return list(itertools.product(SEEDS,ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base='345830ca6cd256abfb33d2d220db06e8f83e2859',
        parent_execution='1effc2138967715e9e9319e1da19c3653e4fd9ac',
        parent_summary='883c1c0142173f038bec25f65589643af9ba40ef2442e7c376b845a61f1477ce',
        parent_envelope='275ac041de4a858ca5a7f50aabb16898e85befebb2ee3ba6159a06198a7c993a',
        question='does maximum full256 CE within every TRAIN query pair improve interior fitting and held-value binding while retaining all domains versus ordinary mean CE on identical mixed45 inputs',
        seeds=list(SEEDS),orders=list(ORDERS),arms=list(ARMS),cycle=CYCLE,steps=STEPS,fit_rng=FIT_RNG,
        changed='loss reduction only:mean48full256CE versus mean24maximum(CEqueryA,CEqueryB);no auxiliary term or coefficient search',
        objective_identity='pairmax = ordinary meanCE + .5*mean absolute within-pair CE difference;torch.maximum splits exact ties symmetrically',
        pair_semantics='before optimizer creation and before every forward,validate canonical TRAIN row identities,shared language/entities/values/fact order,two distinct queries and counterpart targets',
        held='paired fresh weights,identical mixed45 token/target streams,192TRAIN rows,1200events repeated twice,family/length masks,48rows24completepairs,native readout,optimizer,rates,capacity,scorers',
        input_policy='immutable C342 mixed45 balanced length mask on fresh C344 order seeds;canonical C342 banks/select_tokens;no global-constant mutation or fallback',
        actual_per_row_exposure=dict(original2=200,original3=200,original4=50,original5=50,original6=0,interior4=100),
        per_cycle_exposure=dict(original2=100,original3=100,original4=25,original5=25,original6=0,interior4=50),
        exposure_unit='per canonical logical TRAIN row across all profiles;HOLDOUT and masked views never fitted;original6 never fitted',
        nonpadding_training_tokens_per_model=dict(TRAIN_TOKENS),
        compute_boundary='same2400updates/115200rows/3168000nonpaddingtokens per model;both reductions computed in both arms;no extra model forward,backward,parameters or input rows',
        input_proof='identical paired canonical-bank/event/family/length/actual-int64le-token-and-target-stream fingerprints;literal pair metadata separately bound',
        optimizer='core_slow AdamW noncore.005/core.0005 betas.9/.999 eps1e-8 decay0/globalclip1;one continuous optimizer,no LR compensation',
        histories='every preupdate ordinaryCE,pairmax,selectedloss and global preclip norm;both reductions measured in both arms',
        gate='all5candidate full original2..6+interior4;EACHseed EACH6domain EACHsplit TRAIN/HOLDOUT nonnegative normal answer AND query-pair gains;strict aggregate interior TRAIN and HOLDOUT answer AND pair gains',
        contrasts=60,strict_endpoints=['interior_TRAIN_answers','interior_TRAIN_query_pairs','interior_HOLDOUT_answers','interior_HOLDOUT_query_pairs'],
        saturation='any strict-endpoint tie or perfect-control ceiling remains valid negative;no seed/subgroup exclusion or relaxed gate',
        history='C268 margin and C288 softplus assignment auxiliaries were valid negatives;this full-class CE reduction is not a renamed assignment loss',
        limits='adaptive within-pair gradient weights and nonsmooth switching can neglect the easier query temporarily;maxCE need not select the incorrect answer;family exposure is unchanged;no loss-dilution or causal-mechanism proof',
        support_counts='all120state/domain/split normal support/collapse/pair summaries and60paired contrasts emitted,including TRAIN;no supplied-value inference filter',
        thresholds=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,both_order=.80),
        parameters=14256,core_parameters=3328,slots=64,precision='cpu float64',threads=2,
        evaluation_policy='native_before;all10fits finish before full114views/state evaluation and replay;exactargmax and1e-9 replay;all256classes',
        preflight='all5 schedules/pairs/allocations/identical input streams;discarded native model,botharms/bothcycles/original+interior/English+Japanese complete pairs;16forwards64rows8backwards0updates',
        source_count=SOURCE_COUNT,input_count=INPUT_COUNT,parent_files=483,parent_test_proof_files=477,
        own_tests=OWN_TESTS,full_tests=FULL_TESTS,modules=MODULES,outputs=list(OUTPUTS),
        raw_logit_payload_bytes=672399360,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA,'C344 manifest seal')


def prepared(data, old, new, cx):
    """Unchanged C340 canonical banks; TRAIN fitting chooses between them explicitly."""
    return reference().prepared(data,old,new,cx)


def make_model(seed, x):
    require(type(seed) is int and seed in SEEDS,'fresh C344 seed')
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


def length_mask(events, family):
    return reference().length_mask(events,family,'mixed45')


def actual_exposure(events, family, selected):
    return reference().actual_exposure(events,family,selected,'mixed45')


def select_tokens(tables, event, family, selected):
    return reference().select_tokens(tables,event,family,selected)


def training_fingerprint(tables, y, events, family, selected):
    return reference().training_fingerprint(tables,y,events,family,selected)


def stream_update(value, tokens, y, ids):
    value.update(tokens.contiguous().numpy().astype('<i8',copy=False).tobytes())
    value.update(y[ids].contiguous().numpy().astype('<i8',copy=False).tobytes())


def input_accounting(tables, y, events, family, selected):
    value = hashlib.sha256(b'C344 TRAIN int64le tokens then targets per update\n'); count = 0
    for step in range(STEPS):
        tokens,ids = select_tokens(tables,events[step%CYCLE],family[step%CYCLE],selected[step])
        count += int((tokens != 256).sum()); stream_update(value,tokens,y,ids)
    return count,value.hexdigest()


def validate_batch_pairs(rows, targets, ids):
    require(isinstance(ids,torch.Tensor) and ids.dtype == torch.int64 and ids.device.type == 'cpu'
            and ids.ndim == 1 and len(ids) > 0 and len(ids)%2 == 0 and len(set(ids.tolist())) == len(ids)
            and bool(((ids >= 0)&(ids < len(rows))).all()),'distinct complete TRAIN pair indices')
    indices = ids.tolist()
    for a,b in zip(indices[::2],indices[1::2],strict=True):
        left,right = rows[a],rows[b]
        require(all(left[k] == right[k] for k in ('language','entities','values','permutation'))
                and left['id'] != right['id'] and left['query'] != right['query']
                and {left['query'],right['query']} == set(left['entities']), 'adjacent canonical query-pair identity')
        values = dict(zip(left['entities'],left['values'],strict=True))
        expected = [48+values[row['query']] for row in (left,right)]
        require(expected[0] != expected[1] and [left['target'],right['target']] == expected
                and [int(targets[a]),int(targets[b])] == expected, 'query-pair target/counterpart alignment')


def validate_training_pairs(rows, targets, events, x):
    require(type(rows) is list and rows == x.c.p267.dataset()['TRAIN'], 'canonical TRAIN pair metadata')
    require(isinstance(targets,torch.Tensor) and targets.shape == (192,) and targets.dtype == torch.int64
            and targets.device.type == 'cpu' and targets.tolist() == [r['target'] for r in rows], 'canonical TRAIN targets')
    previous().source().curriculum().validate_schedule(events)
    require(events.shape == (CYCLE,24,4) and events.dtype == torch.int64 and events.device.type == 'cpu', 'pair schedule frame')
    for event in events:
        validate_batch_pairs(rows,targets,event[:,2:].reshape(-1))


def objective(logits, targets, arm):
    """Only the TRAIN loss reduction changes; retain the exact ordinary CE call."""
    require(arm in ARMS and isinstance(logits,torch.Tensor) and logits.ndim == 2 and logits.shape[1] == 256
            and len(logits) > 0 and len(logits)%2 == 0 and logits.dtype == torch.float64
            and logits.device.type == 'cpu' and bool(torch.isfinite(logits).all()), 'finite paired full256 TRAIN logits')
    require(isinstance(targets,torch.Tensor) and targets.shape == (len(logits),) and targets.dtype == torch.int64
            and targets.device.type == 'cpu' and bool(((targets >= 0)&(targets < 256)).all())
            and bool((targets[::2] != targets[1::2]).all()), 'distinct paired TRAIN targets')
    ce = F.cross_entropy(logits,targets)
    per_query = F.cross_entropy(logits,targets,reduction='none').reshape(-1,2)
    pair_max = torch.maximum(per_query[:,0],per_query[:,1]).mean()
    selected = ce if arm == 'mean_ce' else pair_max
    require(all(bool(torch.isfinite(v)) and float(v.detach()) >= 0 for v in (ce,pair_max,selected)), 'finite nonnegative objectives')
    tolerance = LOSS_TOL*max(1.,float(ce.detach()))
    require(float(ce.detach())-tolerance <= float(pair_max.detach()) <= 2*float(ce.detach())+tolerance, 'pairmax CE bounds')
    return selected,ce,pair_max


def optimize(model, arm, tables, y, events, family, selected, rows, x):
    require(arm in ARMS and len(events) == len(family) == CYCLE and len(selected) == STEPS == 2*CYCLE, 'registered cycles')
    # This entire metadata check precedes optimizer creation, not merely the first update.
    validate_training_pairs(rows,y,events,x)
    p = previous(); torch.manual_seed(FIT_RNG)
    opt = x.policy.optimizer_for(model,'core_slow'); opt_id = id(opt)
    initial = p.state_hash(model.state_dict()); core_initial = p.state_hash(model.backbone.core.state_dict())
    losses,rates,counts,indices,norms = [],[],[],[],[]; union = {}; boundary = None; continuation = None
    stream = hashlib.sha256(b'C344 TRAIN int64le tokens then targets per update\n'); nonpadding = 0; checked_pairs = 0
    model.train()
    with torch.enable_grad(),p.readouts().readout(model,x.wide,'native_before') as stats:
        for step in range(STEPS):
            if step == CYCLE:
                continuation = dict(weights=p.state_hash(model.state_dict()),optimizer=p.state_hash(opt.state_dict()))
                require(continuation == boundary, 'optimizer/weight reset')
            require(id(opt) == opt_id, 'optimizer replaced'); x.policy.verify_optimizer(opt,model,'core_slow')
            rate = [g['lr'] for g in opt.param_groups]; require(rate == list(RATES), 'fixed rates'); rates.append(rate)
            index = step%CYCLE; indices.append(index); opt.zero_grad(set_to_none=True)
            tokens,ids = select_tokens(tables,events[index],family[index],selected[step])
            require(len(ids) == 48 and torch.equal(ids,events[index,:,2:].reshape(-1)), 'actual paired TRAIN row order')
            validate_batch_pairs(rows,y,ids); checked_pairs += len(ids)//2
            nonpadding += int((tokens != 256).sum()); stream_update(stream,tokens,y,ids)
            logits = model(tokens,torch.zeros(len(ids),dtype=torch.int64)); x.c.p267.check_logits(logits,len(ids))
            loss,ce,pair_max = objective(logits,y[ids],arm)
            losses.append(dict(mean_ce=float(ce.detach()),pair_max=float(pair_max.detach()),selected=float(loss.detach())))
            loss.backward()
            got = {name:v.numel() for name,v in model.named_parameters() if v.grad is not None}
            require(got, 'missing gradients'); counts.append(sum(got.values())); union.update(got)
            norm = torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True)
            norms.append(float(norm)); opt.step()
            if step+1 == CYCLE: boundary = dict(weights=p.state_hash(model.state_dict()),optimizer=p.state_hash(opt.state_dict()))
            if (step+1)%200 == 0:
                print(f'[C344] arm={arm} step={step+1}/{STEPS} ce={losses[-1]["mean_ce"]:.6f} pairmax={losses[-1]["pair_max"]:.6f} selected={losses[-1]["selected"]:.6f}',flush=True)
    model.eval(); require(boundary is not None and boundary == continuation, 'continuous optimizer')
    require(stats == dict(calls=STEPS,query_calls=2*STEPS,rows=48*STEPS,grad_calls=STEPS)
            and checked_pairs == 24*STEPS, 'TRAIN pair/forward receipt')
    state = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    require(p.state_hash(state) == p.state_hash(model.state_dict()) and all(v.numel() == 0 or state[k].data_ptr() != v.data_ptr()
            for k,v in model.state_dict().items()), 'deep checkpoint')
    return dict(arm=arm,readout_mode='native_before',length_policy='mixed45',steps=STEPS,
        initial_sha256=initial,final_sha256=p.state_hash(state),core_initial_sha256=core_initial,
        core_final_sha256=p.state_hash(model.backbone.core.state_dict()),loss_history=losses,preclip_norm_history=norms,
        optimizer_group_lrs=rates,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())),
        event_indices=indices,policy_receipt=dict(stats),boundary=boundary,continuation=continuation,
        optimizer_creations=1,intermediate_evaluations=0,checked_training_pairs=checked_pairs,
        pair_metadata_sha256=digest(rows),nonpadding_token_presentations=nonpadding,
        actual_training_stream_sha256=stream.hexdigest()),state


def train_one(seed, arm, model, tables, y, rows, cx, root, pins):
    p = previous(); x = cx[-1]; p.source().base().check_dependencies(root,pins,cx,model)
    events,family = schedule(seed,rows,x); selected = length_mask(events,family)
    before = training_fingerprint(tables,y,events,family,selected); exposure = actual_exposure(events,family,selected)
    print(f'[C344] seed={seed} arm={arm} phase=training',flush=True)
    with x.c.p267.counted(model,x.c.core) as (calls,cores):
        trace,state = optimize(model,arm,tables,y,events,family,selected,rows,x)
    require(calls == [2400,115200] and cores[0] == 9600, 'measured TRAIN work')
    require(training_fingerprint(tables,y,events,family,selected) == before, 'TRAIN input mutation')
    count,stream = input_accounting(tables,y,events,family,selected)
    require(trace['nonpadding_token_presentations'] == count == TRAIN_TOKENS[arm]
            and trace['actual_training_stream_sha256'] == stream, 'measured TRAIN token stream')
    trace.update(seed=seed,training_input_sha256=before,
        logical_training_sha256=p.state_hash(dict(targets=y,events=events,mask=family)),
        schedule_sha256=digest(events.tolist()),mask_sha256=digest(family.tolist()),length_mask_sha256=digest(selected.tolist()),
        family_exposure_per_cycle=p.source().curriculum().exposure(events,family),actual_exposure_per_cycle=exposure)
    return trace,state


def check_trace(t, rows, x, tables, y):
    p = previous(); require(type(t['seed']) is int and t['seed'] in SEEDS and t['arm'] in ARMS, 'trace identity')
    events,family = schedule(t['seed'],rows,x); selected = length_mask(events,family)
    validate_training_pairs(rows,y,events,x)
    require(t['readout_mode'] == 'native_before' and t['length_policy'] == 'mixed45', 'trace token/readout policy')
    require(type(t['steps']) is int and t['steps'] == STEPS and t['event_indices'] == list(range(CYCLE))*2
            and all(type(v) is int for v in t['event_indices']), 'event budget/order')
    require(t['schedule_sha256'] == digest(events.tolist()) and t['mask_sha256'] == digest(family.tolist())
            and t['length_mask_sha256'] == digest(selected.tolist())
            and t['family_exposure_per_cycle'] == p.source().curriculum().exposure(events,family)
            and t['actual_exposure_per_cycle'] == actual_exposure(events,family,selected), 'actual exposure reconstruction')
    count,stream = input_accounting(tables,y,events,family,selected)
    require(type(t['nonpadding_token_presentations']) is int and t['nonpadding_token_presentations'] == count == TRAIN_TOKENS[t['arm']]
            and t['actual_training_stream_sha256'] == stream, 'reconstructed token stream')
    require(t['training_input_sha256'] == training_fingerprint(tables,y,events,family,selected)
            and t['logical_training_sha256'] == p.state_hash(dict(targets=y,events=events,mask=family))
            and t['pair_metadata_sha256'] == digest(rows) and type(t['checked_training_pairs']) is int
            and t['checked_training_pairs'] == 24*STEPS, 'TRAIN recipe/pair fingerprint')
    require(t['optimizer_group_lrs'] == [list(RATES)]*STEPS and len(t['loss_history']) == len(t['preclip_norm_history']) == STEPS, 'rates/loss history length')
    for row in t['loss_history']:
        require(set(row) == {'mean_ce','pair_max','selected'} and all(type(v) is float and math.isfinite(v) and v >= 0 for v in row.values()), 'finite saved losses')
        tol = LOSS_TOL*max(1.,row['mean_ce'])
        require(row['mean_ce']-tol <= row['pair_max'] <= 2*row['mean_ce']+tol and row['selected'] == row[t['arm']], 'registered reduction arithmetic')
    require(all(type(v) is float and math.isfinite(v) and v >= 0 for v in t['preclip_norm_history']), 'preclip gradient norms')
    union,counts = t['gradient_union'],t['gradient_parameter_counts']
    require(union and all(type(k) is str and type(v) is int and v > 0 for k,v in union.items()) and 0 < sum(union.values()) <= 14256
            and len(counts) == STEPS and all(type(v) is int and 0 < v <= sum(union.values()) for v in counts), 'gradient inventory')
    for key in ('initial_sha256','final_sha256','core_initial_sha256','core_final_sha256','training_input_sha256',
                'logical_training_sha256','actual_training_stream_sha256','length_mask_sha256','pair_metadata_sha256'):
        require(type(t[key]) is str and re.fullmatch('[0-9a-f]{64}',t[key]), 'state/input fingerprint')
    require(t['initial_sha256'] != t['final_sha256'] and t['core_initial_sha256'] != t['core_final_sha256'], 'trained state')
    require(t['boundary'] == t['continuation'] and set(t['boundary']) == {'weights','optimizer'}
            and all(type(v) is str and re.fullmatch('[0-9a-f]{64}',v) for v in t['boundary'].values()), 'continued state')
    require(type(t['optimizer_creations']) is int and t['optimizer_creations'] == 1 and type(t['intermediate_evaluations']) is int
            and t['intermediate_evaluations'] == 0 and t['policy_receipt'] == dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400), 'no restart/selection')


def normal_report(raw, data):
    base = previous().source().base(); audit = support().audit(); result = {}
    exposures = manifest()['actual_per_row_exposure']
    for domain in DOMAINS:
        result[domain] = {}; tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
        for split in SPLITS:
            rows = data[split]; pairs = base.query_pairs(rows); targets = [r['target'] for r in rows]
            others = [48+r['values'][1-r['entities'].index(r['query'])] for r in rows]
            kinds = dict.fromkeys(audit.KINDS,0); both = collapsed = 0
            for profile in audit.parent().profiles(domain):
                items = audit.audit_logits(tree[split][profile]['normal'],targets,others)
                for item in items: kinds[item['kind']] += 1
                for i,j in pairs:
                    both += items[i]['kind'] == items[j]['kind'] == 'correct'
                    collapsed += items[i]['prediction'] == items[j]['prediction']
            total_pairs = 3*len(pairs); one = kinds['correct']-2*both
            result[domain][split] = dict(answers=3*len(rows),query_pairs=total_pairs,both_query_correct=both,
                one_correct_pairs=one,zero_correct_pairs=total_pairs-both-one,collapsed_pairs=collapsed,**kinds,
                normal_prompt_seen_in_training=split == 'TRAIN' and exposures[domain] > 0,
                domain_presentations_per_logical_row=exposures[domain] if split == 'TRAIN' else 0)
    return result


def compare_normal(control, candidate, data):
    base = previous().source().base(); kinds = support().audit().parent(); result = {}
    for domain in DOMAINS:
        result[domain] = {}
        trees = [raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]] for raw in (control,candidate)]
        for split in SPLITS:
            # C324's helper accepts arbitrary canonical rows; its historical name
            # does not restrict it to HOLDOUT. Preserve its three-profile ABI.
            adapted = [{ip:tree[split][op] for ip,op in zip(kinds.profiles('interior4'),kinds.profiles(domain),strict=True)} for tree in trees]
            result[domain][split] = base.heldout_contrast(*adapted,data[split])
    return result


def contrast_check(row, split):
    keys = ('answers','query_pairs','control_correct','candidate_correct','control_both_correct','candidate_both_correct',
            'rescued','regressed','pair_rescued','pair_regressed','answer_gain','query_pair_gain')
    n = 576 if split == 'TRAIN' else 288; m = n//2
    require(set(row) == set(keys) and all(type(row[k]) is int for k in keys)
            and row['answers'] == n and row['query_pairs'] == m, 'complete split contrast')
    for key in keys[2:-2]:
        maximum = m if key in ('control_both_correct','candidate_both_correct','pair_rescued','pair_regressed') else n
        require(0 <= row[key] <= maximum, 'contrast count range')
    require(row['candidate_correct']-row['control_correct'] == row['answer_gain'] == row['rescued']-row['regressed']
            and row['candidate_both_correct']-row['control_both_correct'] == row['query_pair_gain'] == row['pair_rescued']-row['pair_regressed'], 'contrast conservation')
    require(row['rescued'] <= n-row['control_correct'] and row['regressed'] <= row['control_correct']
            and row['pair_rescued'] <= m-row['control_both_correct'] and row['pair_regressed'] <= row['control_both_correct'], 'contrast feasible transitions')


def fixed_gate(pairs):
    require([r['seed'] for r in pairs] == list(SEEDS) and all(type(r['seed']) is int for r in pairs), 'all paired seeds')
    eligible = []
    for row in pairs:
        require(type(row['candidate_full_pass']) is bool and set(row['normal_by_domain']) == set(DOMAINS), 'full candidate/domain gate')
        gains = []
        for domain in DOMAINS:
            require(set(row['normal_by_domain'][domain]) == set(SPLITS), 'both comparison splits')
            for split in SPLITS:
                z = row['normal_by_domain'][domain][split]; contrast_check(z,split)
                gains.extend(z[k] for k in ('answer_gain','query_pair_gain'))
        eligible.append(row['candidate_full_pass'] and all(g >= 0 for g in gains))
    strict = {split:{key:sum(r['normal_by_domain']['interior4'][split][key] for r in pairs)
                     for key in ('answer_gain','query_pair_gain')} for split in SPLITS}
    return all(eligible) and all(g > 0 for z in strict.values() for g in z.values()),eligible,strict


def check_normal_report(value, domain, split):
    kinds = support().audit().KINDS; n = 576 if split == 'TRAIN' else 288; m = n//2
    counts = ('answers','query_pairs','both_query_correct','one_correct_pairs','zero_correct_pairs','collapsed_pairs',*kinds)
    require(set(value) == {*counts,'normal_prompt_seen_in_training','domain_presentations_per_logical_row'}
            and all(type(value[k]) is int for k in counts) and value['answers'] == n and value['query_pairs'] == m, 'normal result schema/denominators')
    require(all(0 <= value[k] <= n for k in kinds) and sum(value[k] for k in kinds) == n
            and all(0 <= value[k] <= m for k in counts[2:6]), 'normal kind/pair ranges')
    both,one,zero = [value[k] for k in ('both_query_correct','one_correct_pairs','zero_correct_pairs')]
    require(both+one+zero == m and 2*both+one == value['correct'] and value['collapsed_pairs'] <= m-both, 'normal pair arithmetic')
    presentations = manifest()['actual_per_row_exposure'][domain] if split == 'TRAIN' else 0
    require(type(value['normal_prompt_seen_in_training']) is bool and value['normal_prompt_seen_in_training'] is (presentations > 0)
            and type(value['domain_presentations_per_logical_row']) is int and value['domain_presentations_per_logical_row'] == presentations, 'normal actual fitting exposure')


def check_summary(value):
    require(set(value) == {*WORK,'candidate_gate','eligible_seed_count','strict_interior_gains','paired_conditions_valid',
        'all_replays','evaluation_policy','seed_results','paired_comparisons'}, 'summary writer schema')
    require(all(type(value[k]) is int and value[k] == n for k,n in WORK.items()) and value['paired_conditions_valid'] is True
            and value['all_replays'] is True and value['evaluation_policy'] == 'native_before', 'work/integrity')
    require([(r['seed'],r['arm']) for r in value['seed_results']] == identities() and len(value['paired_comparisons']) == 5, 'complete cohort')
    state_keys = {'seed','arm','original_pass','interior_pass','retention_pass','failures','support','normal_by_domain','training_nonpadding_tokens'}
    for state in value['seed_results']:
        require(set(state) == state_keys and set(state['original_pass']) == set(map(str,range(2,7)))
                and all(type(flag) is bool for flag in state['original_pass'].values()) and type(state['interior_pass']) is bool
                and state['retention_pass'] is all(state['original_pass'].values()), 'state gate fields')
        require(type(state['training_nonpadding_tokens']) is int and state['training_nonpadding_tokens'] == TRAIN_TOKENS[state['arm']]
                and set(state['normal_by_domain']) == set(state['support']) == set(state['failures']) == set(DOMAINS), 'state accounting domains')
        for domain in DOMAINS:
            require(set(state['normal_by_domain'][domain]) == set(SPLITS), 'state split coverage')
            for split in SPLITS: check_normal_report(state['normal_by_domain'][domain][split],domain,split)
            require(state['support'][domain] == {k:state['normal_by_domain'][domain]['HOLDOUT'][k] for k in ('answers',*support().audit().KINDS)}, 'legacy HOLDOUT support binding')
            failures = state['failures'][domain]
            require(set(failures) == {'local','order'} and all(type(failures[k]) is int and 0 <= failures[k] <= limit
                    for k,limit in (('local',72),('order',36))), 'state failure counts')
            passed = state['interior_pass'] if domain == 'interior4' else state['original_pass'][domain[-1]]
            require(passed is (failures == dict(local=0,order=0)), 'state failure/pass binding')
    gain_keys = ('interior_train_answer_gain','interior_train_pair_gain','interior_holdout_answer_gain','interior_holdout_pair_gain')
    for i,row in enumerate(value['paired_comparisons']):
        require(set(row) == {'seed','control_full_pass','candidate_full_pass','normal_by_domain',*gain_keys}, 'paired writer schema')
        for offset,name in ((0,'control_full_pass'),(1,'candidate_full_pass')):
            state = value['seed_results'][2*i+offset]
            require(type(row[name]) is bool and row[name] is (state['retention_pass'] and state['interior_pass']), 'paired full flags')
        require(set(row['normal_by_domain']) == set(DOMAINS), 'paired domain coverage')
        for domain in DOMAINS:
            require(set(row['normal_by_domain'][domain]) == set(SPLITS), 'paired split coverage')
            for split in SPLITS:
                contrast = row['normal_by_domain'][domain][split]; contrast_check(contrast,split)
                left,right = [r['normal_by_domain'][domain][split] for r in value['seed_results'][2*i:2*i+2]]
                require([contrast[k] for k in ('control_correct','candidate_correct','control_both_correct','candidate_both_correct')] ==
                        [left['correct'],right['correct'],left['both_query_correct'],right['both_query_correct']], 'normal/paired count binding')
        expected = [row['normal_by_domain']['interior4'][split][key] for split in SPLITS for key in ('answer_gain','query_pair_gain')]
        require(all(type(row[k]) is int for k in gain_keys) and [row[k] for k in gain_keys] == expected, 'four interior endpoints')
    gate,eligible,strict = fixed_gate(value['paired_comparisons'])
    require(value['candidate_gate'] is gate and type(value['eligible_seed_count']) is int and value['eligible_seed_count'] == sum(eligible)
            and blob(value['strict_interior_gains']) == blob(strict), 'fixed gate and strict endpoint sums')


def analyze(traces, records, states, data, cx, tables, y):
    p = previous(); q = p.readouts(); reference().reference().validate_tables(tables,y)
    require([(t['seed'],t['arm']) for t in traces] == [(r['seed'],r['arm']) for r in records] == identities()
            and len(states) == 10, 'complete trained cohort')
    metrics,flags = [],[]
    for trace,record,state in zip(traces,records,states,strict=True):
        check_trace(trace,data['TRAIN'],cx[-1],tables,y)
        require(set(record) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and record['state_sha256'] == trace['final_sha256'] == p.state_hash(state) and record['evaluation_policy'] == 'native_before'
                and set(record['raw']) == set(record['receipts']) == {'evaluation','replay'}, 'state binding')
        for mode in ('evaluation','replay'):
            p.source().base().validate_raw(record['raw'][mode],data,cx)
            require(blob(record['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)), 'evaluation receipt')
        require(p.source().base().replay_error(record['raw']['evaluation'],record['raw']['replay'],data,cx) <= 1e-9, 'saved replay')
        score,f = q.summarize_mode(record['raw']['evaluation'],data,cx); normal = normal_report(record['raw']['evaluation'],data)
        metrics.append(dict(seed=trace['seed'],arm=trace['arm'],score=score))
        legacy = {domain:{k:normal[domain]['HOLDOUT'][k] for k in ('answers',*support().audit().KINDS)} for domain in DOMAINS}
        flags.append(dict(seed=trace['seed'],arm=trace['arm'],training_nonpadding_tokens=trace['nonpadding_token_presentations'],
            support=legacy,normal_by_domain=normal,**f))
    pairs = []
    equal_keys = ('initial_sha256','core_initial_sha256','logical_training_sha256','schedule_sha256','mask_sha256',
                  'family_exposure_per_cycle','actual_exposure_per_cycle','event_indices','optimizer_group_lrs',
                  'training_input_sha256','actual_training_stream_sha256','length_mask_sha256','pair_metadata_sha256','nonpadding_token_presentations')
    for i,seed in enumerate(SEEDS):
        a,b = traces[2*i:2*i+2]; require(all(a[k] == b[k] for k in equal_keys), 'paired identical conditions/input stream')
        normal = compare_normal(records[2*i]['raw']['evaluation'],records[2*i+1]['raw']['evaluation'],data)
        inside = normal['interior4']
        pairs.append(dict(seed=seed,control_full_pass=flags[2*i]['retention_pass'] and flags[2*i]['interior_pass'],
            candidate_full_pass=flags[2*i+1]['retention_pass'] and flags[2*i+1]['interior_pass'],normal_by_domain=normal,
            interior_train_answer_gain=inside['TRAIN']['answer_gain'],interior_train_pair_gain=inside['TRAIN']['query_pair_gain'],
            interior_holdout_answer_gain=inside['HOLDOUT']['answer_gain'],interior_holdout_pair_gain=inside['HOLDOUT']['query_pair_gain']))
    gate,eligible,strict = fixed_gate(pairs)
    value = dict(candidate_gate=gate,eligible_seed_count=sum(eligible),strict_interior_gains=strict,paired_conditions_valid=True,
        all_replays=True,evaluation_policy='native_before',seed_results=flags,paired_comparisons=pairs,**WORK)
    check_summary(value)
    return metrics,value


def report_results(value, emit):
    check_summary(value)
    for row in value['seed_results']:
        emit('C344 seed result',{k:v for k,v in row.items() if k != 'normal_by_domain'})
        for domain,split in itertools.product(DOMAINS,SPLITS):
            emit('C344 normal result',dict(seed=row['seed'],arm=row['arm'],domain=domain,split=split,**row['normal_by_domain'][domain][split]))
    for row in value['paired_comparisons']:
        emit('C344 paired comparison',{k:v for k,v in row.items() if k != 'normal_by_domain'})
        for domain,split in itertools.product(DOMAINS,SPLITS):
            emit('C344 normal contrast',dict(seed=row['seed'],domain=domain,split=split,**row['normal_by_domain'][domain][split]))
    emit('C344 strict interior gains',value['strict_interior_gains'])




def load_states(path):
    value = torch.load(path,map_location='cpu',weights_only=True)
    require(set(value) == {'schema','identities','states'} and value['schema'] == 'fold-c344-trained-models-v1'
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
        torch.save(dict(schema='fold-c344-trained-models-v1',identities=[list(z) for z in identities()],states=states),stream)
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
        print(f'[C344] seed={seed} arm={arm} native_saved_evaluation_and_replay=COMPLETE',flush=True)
    metrics,value = analyze(traces,records,saved,data,cx,tables,y)
    require(digest((data,old,new)) == before,'data/prompt mutation')
    with (out/'evaluations.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c344-evaluations-v1',records=records),stream)
    for name,item in (('experiment-plan.json',manifest()),('training-traces.json',traces),('measurements.json',metrics),('validation-summary.json',value)):
        with (out/name).open('xb') as stream: stream.write(blob(item))
    return value


def semantic_recheck(out, data_out, cx, read):
    data,old,new = previous().load_data(data_out,read); tables,y = prepared(data,old,new,cx)
    archive = torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c344-evaluations-v1','evaluation schema')
    metrics,value = analyze(read(out/'training-traces.json'),archive['records'],load_states(out/'trained-models.pt'),data,cx,tables,y)
    for name,item in (('experiment-plan.json',manifest()),('measurements.json',metrics),('validation-summary.json',value)):
        require(blob(read(out/name)) == blob(item),'saved training reconstruction:'+name)
    return value


def native_preflight(data_out, cx, root, pins, read):
    p = previous(); x = cx[-1]; data,old,new = p.load_data(data_out,read); tables,y = prepared(data,old,new,cx)
    for seed in SEEDS:
        events,family = schedule(seed,data['TRAIN'],x); validate_training_pairs(data['TRAIN'],y,events,x)
        chosen = length_mask(events,family); actual_exposure(events,family,chosen)
        require(input_accounting(tables,y,events,family,chosen)[0] == 3168000, 'preflight identical mixed45 tokens')
    events,family = schedule(SEEDS[0],data['TRAIN'],x); selected = length_mask(events,family)
    model = make_model(SEEDS[0],x); p.source().base().check_dependencies(root,pins,cx,model)
    with torch.no_grad():
        w = model.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
    initial = p.state_hash(model.state_dict())
    for arm,cycle,kind in itertools.product(ARMS,range(2),('original','interior4')):
        chosen_tokens = []; chosen_ids = []
        for language in ('en','ja'):
            found = None
            for i,event in enumerate(events):
                if int(event[0,0]) != 4: continue
                tokens,ids = select_tokens(tables,event,family[i],selected[cycle*CYCLE+i])
                for j in range(24):
                    a,b = ids[2*j:2*j+2].tolist()
                    if data['TRAIN'][a]['language'] == language and bool(family[i,j]) == (kind == 'interior4'):
                        found = tokens[2*j:2*j+2],(a,b); break
                if found is not None: break
            require(found is not None, 'native preflight language/family pair coverage')
            chosen_tokens.append(found[0]); chosen_ids.extend(found[1])
        tokens = torch.cat(chosen_tokens); ids = torch.tensor(chosen_ids,dtype=torch.int64)
        validate_batch_pairs(data['TRAIN'],y,ids); target = y[ids]
        require(tokens.shape == (4,64), 'native complete-pair frame'); tasks = torch.zeros(4,dtype=torch.int64); model.train()
        with torch.no_grad(): expected = model(tokens,tasks)
        model.zero_grad(set_to_none=True)
        with torch.enable_grad(),p.readouts().readout(model,x.wide,'native_before') as stats:
            logits = model(tokens,tasks); p.readouts().same(expected,logits.detach())
            loss,ce,pair_max = objective(logits,target,arm)
            require(float(ce.detach()) > 0 and float(pair_max.detach()) > 0, 'nontrivial native objectives'); loss.backward()
        require(stats == dict(calls=1,query_calls=2,rows=4,grad_calls=1) and model.read.query.weight.grad is not None
                and bool((model.read.query.weight.grad != 0).any())
                and all(v.grad is None or bool(torch.isfinite(v.grad).all()) for v in model.parameters()), 'native pair-max/mean backward')
    require(p.state_hash(model.state_dict()) == initial, 'preflight changed weights')
    print('C344_native_preflight=PASS;schedules=5;forwards=16;rows=64;backward=8;updates=0',flush=True)
    return identities()
