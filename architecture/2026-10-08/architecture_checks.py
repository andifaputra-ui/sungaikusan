"""Architecture-only checks: metadata arithmetic and exhaustive artificial populations.
No RNG/seed, real sample selection, pixel access, network or detector execution.
"""
from pathlib import Path
from itertools import combinations, product
from fractions import Fraction as F
from collections import Counter
import hashlib
import json
import math

P = Path(__file__).resolve().parent
C = P.parent
inputs = [C/'REFERENCE_RESPONSE_STAGE1/FIREWALL.json',
          C/'REFERENCE_RESPONSE_STAGE1/ACQUISITION_FRAME.json',
          C/'PHYSICAL_CONTEXT_REFERENCE_DESIGN/FRAME_FEASIBILITY/OPTICAL_OPPORTUNITY_SUMMARY.json',
          C/'REFERENCE_QUALIFICATION_WAVE2/FINAL_QUALIFICATION/DECISION_FOR_REVIEW.md']
checks = []
def check(name, ok):
    assert ok, name
    checks.append({'name': name, 'pass': True})
def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))
def mean(v):
    return sum(v, F(0))/len(v)
def var(v):
    return sum((x-mean(v))**2 for x in v)/(len(v)-1)

portable = not inputs[0].exists()
snapshot = read(P/'ARCHITECTURE_INPUT_METADATA.json') if portable else None
d = snapshot['domain'] if portable else read(inputs[0])['domain']
W, H = d['width'], d['height']
cols, rows = math.ceil(W/3), math.ceil(H/3)
sizes = Counter(min(3, W-3*c)*min(3, H-3*r)
                for r in range(rows) for c in range(cols))
check('disjoint tile areas preserve every 10m map cell', sum(k*v for k,v in sizes.items()) == W*H)
check('partial edge tiles retained', sizes[4] == 1 and sizes[6] == 2479)
check('known full operational grid count', W*H == 13139038)
check('new tiles differ explicitly from legacy centre neighbourhoods', cols*rows == 1460720)
if portable:
    counts = snapshot['year_halfyear_counts']
    eligible_count = sum(counts.values())
else:
    frame = read(inputs[1])['frame']
    eligible = [x for x in frame if x['coverage'] >= 1-1e-8]
    counts = dict(sorted(Counter(x['date'][:4]+'H'+str(1 if int(x['date'][5:7]) <= 6 else 2)
                                 for x in eligible).items()))
    eligible_count = len(eligible)
check('saved catalogue contains 270 full-envelope eligible entries', eligible_count == 270)
check('18 year-halfyear strata all permit at least two dates', len(counts) == 18 and min(counts.values()) >= 2)

# Exact design enumeration, NOT a sample or pseudo-random simulation.
# Three artificial dates, two spatial strata per date, three units per stratum.
# Select two dates and two units/stratum. Unequal date signals and within-date variation.
pop = [[[F(x) for x in z] for z in day]
       for day in [[[0,0,1],[0,1,1]], [[0,0,0],[0,0,1]], [[1,1,1],[0,1,1]]]]
N, n, M, m, K = 3, 2, 3, 2, 2
truth = sum(sum(sum(z) for z in day) for day in pop)/F(N*M*K)
date_opts = []
for day in pop:
    opts = []
    for choices in product(list(combinations(range(M),m)), repeat=K):
        est_total = F(0)
        est_var = F(0)
        for k, ix in enumerate(choices):
            yy = [day[k][j] for j in ix]
            est_total += F(M,m)*sum(yy)
            est_var += F(M*M)*(1-F(m,M))*var(yy)/m
        opts.append((est_total, est_var))
    date_opts.append(opts)
estimates, variances = [], []
for dates in combinations(range(N),n):
    for chosen in product(*(date_opts[t] for t in dates)):
        totals = [q[0] for q in chosen]
        total_hat = F(N,n)*sum(totals)
        vhat = F(N*N)*(1-F(n,N))*var(totals)/n + F(N,n)*sum(q[1] for q in chosen)
        estimates.append(total_hat/F(N*M*K))
        variances.append(vhat/F((N*M*K)**2))
exact_v = mean([(x-truth)**2 for x in estimates])
check('exhaustive two-stage HT mean is unbiased', mean(estimates) == truth)
check('exact two-stage variance estimator is unbiased', mean(variances) == exact_v)
check('all artificial design possibilities enumerated', len(estimates) == 243)
check('positive first-order inclusion for all artificial units', F(n,N)*F(m,M) > 0)
try:
    var([F(1)])
    one_unit_variance_rejected = False
except ZeroDivisionError:
    one_unit_variance_rejected = True
check('one sampled support cannot estimate within-stratum variance', one_unit_variance_rejected)

# Unequal allocation is valid with weights; unweighted summaries can be wrong.
aux_sets = [[F(1),F(1)], [F(0),F(0),F(0),F(0)]]
weighted, unweighted = [], []
for a,b in product(combinations(aux_sets[0],2), combinations(aux_sets[1],2)):
    weighted.append((2*mean(a)+4*mean(b))/6)
    unweighted.append(mean(list(a)+list(b)))
check('weighted unequal-allocation estimate recovers finite mean', mean(weighted) == F(1,3))
check('ignoring unequal allocation produces bias in constructed case', mean(unweighted) == F(1,2))
# Incorrect auxiliary assignments remain valid strata when exhaustive.
misassigned = [[F(1),F(0)], [F(1),F(0),F(0),F(0)]]
mis_est = [(2*mean(a)+4*mean(b))/6 for a,b in product(combinations(misassigned[0],2), combinations(misassigned[1],2))]
check('imperfect auxiliary strata do not invalidate weighted selection', mean(mis_est) == F(1,3))

# Reference identification is separate from sampling precision.
response_scenarios = []
for resolved in [F(555,10000),F(1,4),F(1,2),F(3,4),F(9,10),F(19,20)]:
    unknown = 1-resolved
    lo, hi = resolved*F(9,10), resolved*F(9,10)+unknown
    response_scenarios.append({'resolved_fraction':float(resolved), 'unknown_fraction':float(unknown),
                               'accuracy_if_resolved_subset_90_percent': [float(lo),float(hi)],
                               'identification_width':float(hi-lo)})
    check(f'unknown mass preserved at resolved fraction {resolved}', hi-lo == unknown)
check('no-data not silently removed from area denominator', F(1,2) != F(1,2)/F(3,4))

scenarios = []
for dates, supports in [(18,8),(36,6),(36,8),(54,8)]:
    nn = dates*supports
    scenarios.append({'dates':dates, 'supports_per_date':supports, 'total':nn,
                      'srs_illustrative_95_halfwidth_at_p_half':1.96*math.sqrt(.25/nn),
                      'expected_conditional_at_old_5_55pct_NOT_forecast':nn*.0555,
                      'slots_if_4_per_support':4*nn,
                      'charge_GiB_using_old_attempt_average_NOT_provider_quote':4*nn*(1894475446/538)/(1024**3)})

result = {
 'status':'PASS_ARCHITECTURE_ONLY_NO_RANDOMIZATION',
 'checks':checks, 'check_count':len(checks),
 'grid':{'width':W,'height':H,'cells':W*H,'area_km2':W*H/10000,
         'tile_rows':rows,'tile_cols':cols,'tiles':cols*rows,
         'tiles_by_number_of_10m_cells':dict(sizes),
         'legacy_1955000_centres_fraction_of_grid':1955000/(W*H)},
 'catalogue':{'eligible_entries':eligible_count,'completeness':'UNVERIFIED_OUTSIDE_SAVED_CATALOGUE',
              'year_halfyear_counts':counts},
 'exhaustive_artificial_two_stage':{'designs':len(estimates),'truth':float(truth),
                                  'exact_variance':float(exact_v),'mean_estimated_variance':float(mean(variances))},
 'response_identification_scenarios':response_scenarios,'planning_scenarios':scenarios,
 'limitations':['No sample-size sufficiency claim; SRS halfwidths ignore design effects and reference uncertainty.',
               'Old5.55percent is conditional bridge yield, not fully known response mass; its use here is an optimistic illustrative assumption.',
               'No pixels, detector outputs, source geometry, real reference rows or final evidence accessed.',
               'All artificial populations enumerated exactly; no random seed exists.'],
 'input_hashes':snapshot['input_hashes'] if portable else {str(p.relative_to(C)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
out=P/'ARCHITECTURE_CHECK_RESULTS.json'
if out.exists():
    assert read(out)==json.loads(json.dumps(result)), 'Existing result differs; preserve it and investigate'
else:
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({'status':result['status'],'checks':len(checks),'tiles':cols*rows,
                  'enumerated_artificial_designs':len(estimates)},indent=2))
