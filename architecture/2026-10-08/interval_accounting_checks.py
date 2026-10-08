"""Exhaustive artificial area accounting; no labels/predictions from the project.
All counts are in ninths of a tile. Compare formulas against every feasible
allocation of true water to predicted W/N/A portions and every integer interval.
"""
from pathlib import Path
import json

P=Path(__file__).resolve().parent
n_cases=0
for w in range(10):
    for n in range(10-w):
        a=9-w-n
        allocations=[(x,y,z) for x in range(w+1) for y in range(n+1) for z in range(a+1)]
        for lo in range(10):
            for hi in range(lo,10):
                good=[(x,y,z) for x,y,z in allocations if lo<=x+y+z<=hi]
                assert good
                error=[w-x+y for x,y,z in good]
                predicted=(max(0,w-hi,lo-(w+a)),w+n-max(0,n-hi,lo-(n+a)))
                assert (min(error),max(error))==predicted
                fp=[w-x for x,y,z in good]
                fn=[y for x,y,z in good]
                wa=[z for x,y,z in good]
                assert (min(fp),max(fp))==(max(0,w-hi),min(w,9-lo))
                assert (min(fn),max(fn))==(max(0,lo-(w+a)),min(n,hi))
                assert (min(wa),max(wa))==(max(0,lo-(w+n)),min(a,hi))
                n_cases+=1
assert n_cases==3025
# Continuous fractions have the same piecewise-linear solution, which can be
# justified by filling predicted-W, then-A, then-N for minimum error (reverse
# for maximum). Test the salient full-assignment half/half ambiguity explicitly.
w=n=.5;a=0;lo=hi=.5
assert max(0,w-hi,lo-(w+a))==0
assert w+n-max(0,n-hi,lo-(n+a))==1
result={'status':'PASS_EXHAUSTIVE_ARTIFICIAL_INTERVAL_ACCOUNTING',
        'composition_interval_cases':n_cases,'scalar_bound_pairs_checked':4*n_cases,
        'checks':['assignederror','falsepositive','falsenegative','waterabstained'],
        'equal_half_water_fractions_pixel_error_bounds':[0,1],
        'error_lower':'max(0,w-u,l-w-a)',
        'error_upper':'w+n-max(0,n-u,l-n-a)',
        'validity':'Fraction-only constraints; spatially located reference evidence can tighten bounds. Separate extrema need not occur jointly.',
        'unknown_retained':True,'randomization':False,'research_data_read':False}
out=P/'INTERVAL_ACCOUNTING_RESULTS.json'
if out.exists():
    assert json.loads(out.read_text(encoding='utf-8'))==result
else:
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({'status':result['status'],'cases':n_cases,'bound_pairs':4*n_cases}))
