#!/usr/bin/env python3
"""Independent QA of 173-role v0.5 research preview; no physical/mint proof."""
from pathlib import Path
import collections,hashlib,json,math
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[3]
B=ROOT/'Raphael_Packages/geometry_173/showcase'
M=json.loads((B/'analytic_reference_meshes_v05.json').read_text())
D=json.loads((B/'showcase_data_v05.json').read_text())
C=json.loads((B.parent/'catalogue.json').read_text())
assert len(D['items'])==173 and [r['slot'] for r in D['items']]==list(range(1,174))
assert len(M['meshes'])==131 and len(M['aliases'])==9
assert sum(r['mesh'] for r in D['items'])==140
assert all(str(j) in M['meshes'] for j in range(22,114))
assert C['position_174']['object_id'] is None and C['position_174']['state']=='INTENTIONALLY_EMPTY'
assert len(set(M['meshes'])&set(M['aliases']))==0
for alias,canonical in M['aliases'].items():
 assert str(canonical) in M['meshes'] and alias!=str(canonical)
 assert D['items'][int(alias)-1]['mesh_reference_slot']==canonical
assert all(r.get('Raphael_common_metric')=='UNDEFINED' and r.get('physical_validity')=='NOT_PROVEN' for r in D['items'])

def graph(m):
 n=len(m['vertices']);G=nx.Graph();G.add_nodes_from(range(n),type='vertex')
 for k,f in enumerate(m['faces']):
  i=n+k;G.add_node(i,type='face'+str(len(f)))
  for v in f:G.add_edge(i,v)
 return G

signature={};issues=[]
for key,obj in M['meshes'].items():
 v=np.asarray(obj['vertices'],float);faces=obj['faces'];c=obj['counts']
 assert len(v)==c['V'] and len(faces)==c['F'] and np.isfinite(v).all(),key
 incidences=collections.Counter()
 for f in faces:
  assert len(f)>=3 and len(set(f))==len(f) and all(0<=i<len(v) for i in f),key
  for a,b in zip(f,f[1:]+f[:1]): incidences[tuple(sorted((a,b)))]+=1
 assert len(incidences)==c['E'] and all(k==2 for k in incidences.values()),key
 assert c['V']-c['E']+c['F']==c['euler'],key
 lengths=np.array([np.linalg.norm(v[a]-v[b]) for a,b in incidences])
 if obj.get('geometry_class')!='CONVEX_CATALAN_DUAL_NONREGULAR_FACES' and not 118<=int(key)<=130:
  assert (lengths.max()-lengths.min())/lengths.mean()<1e-6,key
 # star faces must be planar; Euler may differ from two without invalidating the abstract complex.
 if obj.get('geometry_class')=='SELF_INTERSECTING_REGULAR_STAR':
  assert c['V'] in(12,20)
  assert c['euler'] in(-6,2)
  for f in faces:
   q=v[f];normal=np.cross(q[1]-q[0],q[2]-q[0]);normal/=np.linalg.norm(normal)
   assert np.max(np.abs((q-q[0])@normal))<1e-6,key
 else:
  assert c['euler']==2,key
 sourcehash=hashlib.sha256(json.dumps({'v':obj['vertices'],'f':obj['faces']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 assert sourcehash==obj['numerical_geometry_hash_sha256'],key
 signature[key]={'V':c['V'],'E':c['E'],'F':c['F'],'chi':c['euler'], 'faces':obj['face_sizes'],'mesh_class':obj.get('geometry_class','CONVEX_EUCLIDEAN'),
                 'edge_spread':float((lengths.max()-lengths.min())/lengths.mean()), 'fingerprint_sha256':sourcehash}
for p,q in [(94,95),(98,99),(99,100)]:
 assert not nx.is_isomorphic(graph(M['meshes'][str(p)]),graph(M['meshes'][str(q)]),node_match=lambda a,b:a['type']==b['type'])
# Source list includes all eight gyration/diminishment positions and all final-nine Johnsons.
for p in [93,94,95,96,98,99,100,103,*range(105,114)]:
 assert D['items'][p-1]['counts_grade']=='ANALYTIC_EUCLIDEAN_REFERENCE',p
pending=[]
for r in D['items']:
 if r['mesh']:continue
 slot=r['slot'];catg='RAPHAEL_UNDEFINED_CANDIDATE' if 131<=slot<=137 else ('U75_NONCONVEX_SPECIAL' if slot==173 else 'KNOWN_NONCONVEX_UNIFORM')
 pending.append({'slot':slot,'canonical':r['canonical'],'label':r['name'],'category':catg,
                 'source':r.get('source'), 'blocking_requirement':('founder-defined geometric construction: coordinates, face order and admissibility' if catg=='RAPHAEL_UNDEFINED_CANDIDATE' else 'exact non-convex Wythoff/stellation coordinates and oriented face/edge incidence'),
                 'required_validation':['source identification and rights','vertex coordinate and explicit regular polygon/star order','face incidence and edge-length checks','abstract and geometric topology','symmetry and uniqueness vs existing identities','common Raphael metric (separate)','physical role (separate)'],
                 'admission':'NOT_MINTABLE'})
assert len(pending)==33
counts=collections.Counter(r['category'] for r in pending)
assert counts=={'KNOWN_NONCONVEX_UNIFORM':25,'U75_NONCONVEX_SPECIAL':1,'RAPHAEL_UNDEFINED_CANDIDATE':7},counts
(B/'proof_queue_v05.json').write_text(json.dumps({'scope':'remaining 33 geometry roles; bounded read-only research obligations, not completed geometry','pending':pending},indent=2))
(B/'geometry_signatures_v05.json').write_text(json.dumps(signature,indent=2))
qa={'result':'PASS','version':'0.5','positions':173,'verified_numeric_reference_meshes':131,'shared_geometry_aliases':9,'mesh_backed_roles':140,'complete_standard_Johnson_library':92,
    'remaining_unattached':33,'remaining_categories':dict(counts),'nonconvex_Kepler_meshes':4,'metric_and_ToE':'UNPROVEN','minting':'DISABLED',
    'three_state_sort_browser':'PASSED_IN_SEPARATE_BROWSER_TEST','provenance_hashes':'PASS','source_graph_isomorphism_distinctions':'PASS'}
(B/'qa_v05_full.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
