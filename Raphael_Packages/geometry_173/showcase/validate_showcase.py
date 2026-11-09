#!/usr/bin/env python3
"""Read-only integrity audit for 173-slot offline UI and analytic seeds."""
import json,pathlib,re,math,collections,hashlib,sys
from collections import Counter
ROOT=pathlib.Path(__file__).resolve().parent
D=json.loads((ROOT/'showcase_data.json').read_text())
M=json.loads((ROOT/'analytic_reference_meshes.json').read_text())['meshes']
O=json.loads((ROOT.parent/'catalogue.json').read_text())
R=json.loads((ROOT.parent/'relations.json').read_text())
S=(ROOT/'showcase_template.html').read_text()
assert len(D['items'])==173
assert [r['slot'] for r in D['items']]==list(range(1,174))
assert len({r['id'] for r in D['items']})==173
assert D['sentinel_174']['empty'] and not D['sentinel_174']['mintable']
assert D['origin_relationship_count']==699==len(R['edges'])
assert D['origin_source_sha256']==hashlib.sha256((ROOT.parent/'catalogue.json').read_bytes()).hexdigest()
assert all(r['golden_exponent']==r['slot']-1 for r in D['items'])
assert D['items'][13]['canonical']==D['items'][57]['canonical']=='J37'
assert all(D['items'][j+21]['canonical']==f'J{j+1}' for j in range(92))
assert all(D['items'][j+137]['canonical']==f'U{j+16}' for j in range(35))
assert D['items'][172]['counts']=={'V':60,'E':240,'F':124}
assert all(r['physical']=='HYPOTHESIS' and r['metric']=='NOT_TESTED' for r in D['items'])
assert all(r['mesh']==(str(r['slot']) in M) for r in D['items'])
assert '<script id="seed" type="application/json">__DATA__</script>' in S
assert 'minting_permitted:false' in S
mesh_checks={}
for sk,m in M.items():
    verts=m['vertices'];faces=m['faces']
    edges=Counter(tuple(sorted((f[i],f[(i+1)%len(f)]))) for f in faces for i in range(len(f)))
    counts=m['counts']
    assert all(len(v)==3 for v in verts)
    assert len(verts)==counts['V'] and len(edges)==counts['E'] and len(faces)==counts['F']
    assert all(v==2 for v in edges.values())
    assert counts['V']-counts['E']+counts['F']==2
    assert m['edge_length_relative_spread']<1e-6
    assert m['verified_euclidean_reference']
    assert m['Raphael_metric_admissibility']=='NOT_TESTED'
    orig=D['items'][int(sk)-1]
    if orig['counts']:
        assert {k:counts[k] for k in ('V','E','F')}==orig['counts'],(sk,counts,orig['counts'])
    mesh_checks[int(sk)]=counts
html=pathlib.Path(str(ROOT/'showcase.html')).read_text()
assert '__DATA__' not in html and '__MESHES__' not in html
assert 'position_174' not in [r['id'] for r in D['items']]
assert html.count('<script')==3 and html.count('</script>')==3
report={'schema':'0.2.0','items':len(D['items']),'source_relationships':len(R['edges']),
 'exact_euclidean_meshes':len(M),'mesh_slots':sorted(mesh_checks),'abstract_topology_checks':'PASS',
 'source_reference_sets':sum(r['counts'] is not None for r in D['items']),
 'metric_tests':'see metric_test_results.json (illustrative only)',
 'model_status':'PROVISIONAL_NONCANONICAL','asset_signing':'NOT_DONE','mint':'BLOCKED',
 'position_174':'EMPTY',
 'physical_validation':'NOT_PROVEN','UI_self_contained':True,'runtime_smoke_test':'run test_browser.py'}
(ROOT/'showcase_qa.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
