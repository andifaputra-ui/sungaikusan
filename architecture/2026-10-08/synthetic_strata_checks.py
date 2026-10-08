"""Artificial map-strata and partial-support checks, with no research data access."""
from collections import Counter
from itertools import product
from pathlib import Path
import json

P=Path(__file__).resolve().parent
checks=[]
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'pass':True})
def stratum(codes):
    if not codes or any(x not in {'W','N','A'} for x in codes):
        raise ValueError('Invalid synthetic map code/support')
    return int('W' in codes)+2*int('A' in codes)
def allocation(counts,total=8):
    """At least2 in each available stratum (or census ifM<2); round-robin rest.
    No label/response dependent redirection. Fixed code order0,1,2,3.
    """
    n={k:min(2,v) for k,v in sorted(counts.items()) if v>0}
    target=min(total,sum(counts.values()))
    while sum(n.values())<target:
        before=sum(n.values())
        for k in sorted(n):
            if sum(n.values())==target:break
            if n[k]<counts[k]:n[k]+=1
        if sum(n.values())==before:break
    return n

hist=Counter()
for tile in product('WNA',repeat=9):
    hist[stratum(tile)]+=1
check('all3^9 artificial tile maps assigned exactlyonce',sum(hist.values())==3**9)
check('allnonwater has its ownstratum',hist[0]==1)
check('any water without abstention includes mixedW/N',hist[1]==2**9-1)
check('any abstention without water includes invalid-onlysupport',hist[2]==2**9-1)
check('waterandabstention overlap preserved',hist[3]==3**9-2*(2**9)+1)
for dims in [4,6,9]:
    check(f'partialtilewith{dims}cells cannotbe dropped',stratum(['A']*dims)==2)
bad=False
try:stratum(['W','UNRECOGNIZED'])
except ValueError:bad=True
check('unknowncode cannotbe converted tononwater',bad)
for counts in [{0:1000,1:50,2:30,3:20},{0:1000},{0:1000,1:3},
               {0:1,1:1000,2:1,3:100},{0:1,1:1,2:1,3:1},{}]:
    n=allocation(counts)
    check(f'positiveinclusion orcensus forallnonemptystrata {counts}',
          all(0<n[k]<=v for k,v in counts.items() if v>0))
    check(f'allocationtotalpreserved {counts}',sum(n.values())==min(8,sum(counts.values())))
    check(f'varianceestimabilityorfullcensus {counts}',all(v==1 or n[k]>=2 for k,v in counts.items() if v>0))
result={'status':'PASS_SYNTHETIC_ONLY','check_count':len(checks),'checks':checks,
        'all_artificial_9cell_maps_enumerated':3**9,'stratum_counts':dict(hist),
        'code_meanings':{'0':'noW_noA_allN','1':'anyW_noA','2':'noW_anyA','3':'anyW_anyA'},
        'research_data_read':False,'random_seed_generated':False,'real_sample_drawn':False}
out=P/'SYNTHETIC_STRATA_RESULTS.json'
if out.exists():
    assert json.loads(out.read_text(encoding='utf-8'))==json.loads(json.dumps(result))
else:
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({'status':result['status'],'checks':len(checks),'artificial_maps':3**9}))
