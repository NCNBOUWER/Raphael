#!/usr/bin/env python3
"""Raphael 173 v0.5 research construction: canonical Johnson J1..J92 and Kepler references.

IMPORTANT: Numeric Euclidean reconstruction and abstract face-incidence verification only.
No Raphael-metric, physical ToE, rights-to-mint, or identity-completeness assertion.
"""
import pathlib, contextlib, io, importlib.util, itertools, collections, json, math, hashlib
import numpy as np
from scipy.optimize import brentq
from scipy.spatial import ConvexHull
import networkx as nx
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT_DIR=ROOT/'Raphael_Packages/geometry_173/showcase'
spec=importlib.util.spec_from_file_location('geom_seed',OUT_DIR/'build_expansion.py')
g=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(g)
prior=json.loads((OUT_DIR/'analytic_reference_meshes_v03.json').read_text());source=json.loads((OUT_DIR/'showcase_data_v03.json').read_text())
meshes={str(k):v for k,v in prior['meshes'].items()};aliases={str(k):int(v) for k,v in prior['aliases'].items()}
orig=ROOT/'Raphael_Packages/geometry_173/catalogue.json'
cat=json.loads(orig.read_text())

# Ten Johnson solids arise through pentagonal-cupola operations on the independent analytic
# rhombicosidodecahedron. The convention for cap IDs is fixed by the deterministic hull order.
v=g.rich_rhombico
pent=[f for f in g.faces_info(v) if f['size']==5]
assert len(pent)==12

def gyrate_cut(rots=(),removed=()):
 p=v.copy()
 for i in rots:
  f=pent[i];axis=f['normal'];center=f['center'];q=p[f['ids']]-center
  c,s=math.cos(math.pi/5),math.sin(math.pi/5)
  p[f['ids']]=center+q*c+np.cross(axis,q)*s+np.outer(q@axis,axis)*(1-c)
 rem=set().union(*(set(pent[i]['ids']) for i in removed)) if removed else set()
 return np.delete(p,sorted(rem),axis=0)

johnson_positions={
 93:((0,),()),94:((0,3),()),95:((0,1),()),96:((0,1,6),()),
 98:((3,),(0,)),99:((1,),(0,)),100:((1,6),(0,)),103:((6,),(0,1))
}

sources={
'J72-82':'https://www.orchidpalms.com/polyhedra/johnson/johnson.html',
'J84':'https://www.qfbox.info/4d/J84','J85':'https://www.qfbox.info/4d/J85',
'J86':'https://www.qfbox.info/4d/J86','J87':'https://www.qfbox.info/4d/J87',
'J88':'https://www.qfbox.info/4d/J88','J89':'https://www.qfbox.info/4d/J89',
'J90':'https://www.qfbox.info/4d/J90','J91':'https://www.qfbox.info/4d/J91','J92':'https://www.qfbox.info/4d/J92',
'SnubDodecahedron':'https://en.wikipedia.org/wiki/Snub_dodecahedron',
'Kepler':'https://mathworld.wolfram.com/Kepler-PoinsotSolid.html'}

def add_convex(slot,verts,method,source_url):
 result,error=g.verified_convex(verts,slot)
 if not result:raise AssertionError(f'Could not validate slot {slot}: {error}')
 result['source']='original mathematical reconstruction evaluated from published algebraic or geometric relation'
 result['algorithm']=method
 result['formula_reference_url']=source_url
 result['geometry_class']='CONVEX_EUCLIDEAN'
 result['verification_scope']='numeric convex hull, planar face reconstruction, equal edges, two-face incidence, V/E/F, Euler'
 result['source_rights']='ORIGINAL_FORMULA_IMPLEMENTATION; source attributions retained; no third-party mesh file copied'
 meshes[str(slot)]=result
 return result

for slot,(rot,cut) in johnson_positions.items():
 add_convex(slot,gyrate_cut(rot,cut),f'rotate pentagonal cupola by 36 degrees, caps={rot}; remove cap vertex sets={cut}',sources['J72-82'])

# Last nine Johnson solids: algebraic coordinates evaluated numerically, never copied meshes.
A=2.458190775872486;D=.169022229424176;C=1.661955541151648
j84=np.array([[0,math.sqrt(A),s] for s in(-1,1)]+[[s*math.sqrt(C),math.sqrt(D),0] for s in(-1,1)]+[[0,-math.sqrt(D),s*math.sqrt(C)] for s in(-1,1)]+[[s,-math.sqrt(A),0] for s in(-1,1)])
add_convex(105,j84,'evaluate snub disphenoid algebraic root coordinate system',sources['J84'])
A=1.715731736910394;D=math.sqrt(1-(1-1/math.sqrt(2))*A*A);C=math.sqrt(2*(1+math.sqrt(2)*A-A*A))+D
j85=np.array([[a,b,C] for a in(-1,1) for b in(-1,1)]+[[s*math.sqrt(2)*A,0,D] for s in(-1,1)]+[[0,s*math.sqrt(2)*A,D] for s in(-1,1)]+[[a*A,b*A,-D] for a in(-1,1) for b in(-1,1)]+[[0,s*math.sqrt(2),-C] for s in(-1,1)]+[[s*math.sqrt(2),0,-C] for s in(-1,1)])
add_convex(106,j85,'evaluate snub square antiprism polynomial-root coordinate system',sources['J85'])
A=1.705453885692834;B=1.044713857367277;C=1.914399800381786;D=1.578855253321743;E=2.626590848527109
j86=np.array([[0,0,s] for s in(-1,1)]+[[s*A,B,t] for s in(-1,1) for t in(-1,1)]+[[0,C,s*D] for s in(-1,1)]+[[s,E,0] for s in(-1,1)])
add_convex(107,j86,'evaluate sphenocorona quartic-algebraic coordinate system',sources['J86'])
qf=g.faces_info(j86);square=next(i for i,f in enumerate(qf) if f['size']==4)
add_convex(108,g.augment_pyramid(j86,[square],4),'augment J86 square with regular square pyramid',sources['J87'])
A=.594633335632639;B=math.sqrt(1-A*A);C=math.sqrt(3-4*A*A);D=1-2*A*A
j88=np.array([[s,0,2*B] for s in(-1,1)]+[[s,t*2*A,0] for s in(-1,1) for t in(-1,1)]+[[s*(C+B)/B,0,D/B] for s in(-1,1)]+[[0,s,-math.sqrt(2+4*A-4*A*A)] for s in(-1,1)]+[[s*(1+C*D/B**3),0,(2*A**4-1)/B**3] for s in(-1,1)])
add_convex(109,j88,'evaluate sphenomegacorona algebraic root and symmetry orbit',sources['J88'])
A=.216844815713457;B=math.sqrt(1-A*A);C=math.sqrt(2*(1-2*A));D=math.sqrt(3-4*A*A);E=math.sqrt(1+A);F=2*(1-A)
j89=np.array([[s,t,2*B] for s in(-1,1) for t in(-1,1)]+[[s,t*(1+2*A),0] for s in(-1,1) for t in(-1,1)]+[[s*(1+C/math.sqrt(1-A)),0,-(2*A*A+A-1)/B] for s in(-1,1)]+[[0,s,-D] for s in(-1,1)]+[[s*(D*C+E)/(F*E),0,((2*A-1)*D)/F-C/(F*E)] for s in(-1,1)])
add_convex(110,j89,'evaluate hebesphenomegacorona algebraic root and symmetry orbit',sources['J89'])
A=2.208875884159868;B=1.534262227966923;C=.925895207830730;D=2.252966294157959;E=.650005951899941
j90=np.array([[s,0,A] for s in(-1,1)]+[[s,t*B,C] for s in(-1,1) for t in(-1,1)]+[[s*D,0,E] for s in(-1,1)]+[[0,s*D,-E] for s in(-1,1)]+[[s*B,t,-C] for s in(-1,1) for t in(-1,1)]+[[0,s,-A] for s in(-1,1)])
add_convex(111,j90,'evaluate disphenocingulum algebraic coordinate system',sources['J90'])
phi=(1+math.sqrt(5))/2
j91=np.array([[s,0,t*phi**2] for s in(-1,1) for t in(-1,1)]+[[s*phi,t,u] for s in(-1,1) for t in(-1,1) for u in(-1,1)]+[[0,s*phi,0] for s in(-1,1)])
add_convex(112,j91,'construct bilunabirotunda from golden-ratio coordinate orbits',sources['J91'])
j92=np.array([[0,2/math.sqrt(3),2*phi**2/math.sqrt(3)]]+[[s,-1/math.sqrt(3),2*phi**2/math.sqrt(3)] for s in(-1,1)]+[[s,phi**3/math.sqrt(3),2*phi/math.sqrt(3)] for s in(-1,1)]+[[s*phi**2,-1/(phi*math.sqrt(3)),2*phi/math.sqrt(3)] for s in(-1,1)]+[[s*phi,-(phi+2)/math.sqrt(3),2*phi/math.sqrt(3)] for s in(-1,1)]+[[s*phi**2,phi**2/math.sqrt(3),2/math.sqrt(3)] for s in(-1,1)]+[[0,-2*phi**2/math.sqrt(3),2/math.sqrt(3)]]+[[s,t*math.sqrt(3),0] for s in(-1,1) for t in(-1,1)]+[[s*2,0,0] for s in(-1,1)])
add_convex(113,j92,'construct triangular hebesphenorotunda from golden-ratio coordinate orbits',sources['J92'])

# Snub dodecahedron: rotation-group orbit of one polynomial root point; orientation preserved.
xi=float(np.real(np.roots([1,2,0,-phi**2])[np.argmin(abs(np.roots([1,2,0,-phi**2])-0.943))]))
p=np.array([phi**2-phi**2*xi,-phi**3+phi*xi+2*phi*xi**2,xi])
M1=np.array([[1/(2*phi),-phi/2,.5],[phi/2,.5,1/(2*phi)],[-.5,1/(2*phi),phi/2]])
M2=np.array([[0,0,1],[1,0,0],[0,1,0]])
orb=[p];todo=[p]
while todo:
 q=todo.pop(0)
 for M in(M1,M2):
  r=M@q
  if not any(np.linalg.norm(r-z)<1e-7 for z in orb):orb.append(r);todo.append(r)
assert len(orb)==60
add_convex(13,np.array(orb),'icosahedral rotation-group orbit of polynomial-root snub-dodecahedron seed',sources['SnubDodecahedron'])
# Catalan dual #13 of snub dodecahedron
dual_mesh, dual_error = g.verified_convex(g.polar_dual(np.array(orb)),130,uniform_edges=False)
assert dual_mesh is not None, dual_error
dual_mesh.update({'geometry_class':'CONVEX_CATALAN_DUAL_NONREGULAR_FACES', 'algorithm':'polar dual of analytically constructed snub dodecahedron', 'formula_reference_url':sources['SnubDodecahedron'], 'verification_scope':'closed convex manifold, planar congruent nonregular dual faces, V/E/F, Euler; equal edges not required', 'source_rights':'ORIGINAL_FORMULA_IMPLEMENTATION', 'Raphael_metric_admissibility':'UNTESTED'})
meshes['130']=dual_mesh
# Catalan duals have congruent nonregular faces and unequal edge length by definition.
# Above add_convex requires equal edges, so replace that slot with the admitted polar dual if needed.

# Non-convex regular Kepler-Poinsot four: face order is essential; a convex hull cannot represent them.
v=g.unit(g.m.icosa());N=len(v);D=np.linalg.norm(v[:,None,:]-v[None,:,:],axis=2)
chords=sorted(set(round(float(d),8) for d in D.flat if d>1e-6));near,far=chords[0],chords[1]
GN=nx.Graph();GF=nx.Graph();GN.add_nodes_from(range(N));GF.add_nodes_from(range(N))
for a,b in itertools.combinations(range(N),2):
 if abs(D[a,b]-near)<1e-6:GN.add_edge(a,b)
 if abs(D[a,b]-far)<1e-6:GF.add_edge(a,b)
triangles=[list(s) for s in itertools.combinations(range(N),3) if all(GF.has_edge(*edge) for edge in itertools.combinations(s,2))]
assert len(triangles)==20

def rings(i,step=1):
 vals=list(GN.neighbors(i));axis=v[i]/np.linalg.norm(v[i]);u=v[vals[0]]-(v[vals[0]]@axis)*axis;u/=np.linalg.norm(u)
 w=np.cross(axis,u)
 vals=sorted(vals,key=lambda j:math.atan2(v[j]@w,v[j]@u))
 return [vals[(k*step)%len(vals)] for k in range(len(vals))]
small_stellated=[rings(i,2) for i in range(N)]
great_dodeca=[rings(i,1) for i in range(N)]
# Great stellated dodecahedron: polar dual of great icosahedron, with faces from face-adjacency cycles.
verts_dual=[]
for f in triangles:
 pts=v[f];nrm=np.cross(pts[1]-pts[0],pts[2]-pts[0]);d=nrm@pts[0]
 assert abs(d)>1e-8
 verts_dual.append((nrm/d).tolist())
verts_dual=np.array(verts_dual);fsets=[set(f) for f in triangles]
great_stellated=[]
for i in range(N):
 adj=[j for j,f in enumerate(triangles) if i in f]
 G=nx.Graph();G.add_nodes_from(adj)
 for j,k in itertools.combinations(adj,2):
  if len(fsets[j]&fsets[k])==2:G.add_edge(j,k)
 assert len(adj)==5 and all(G.degree(j)==2 for j in adj) and nx.is_connected(G)
 seq=[adj[0]];previous=None;current=adj[0]
 while len(seq)<5:
  nextnode=next(j for j in G[current] if j!=previous)
  seq.append(nextnode);previous,current=current,nextnode
 great_stellated.append(seq)

def star_mesh(slot,verts,faces,expected,method):
 verts=np.asarray(verts,float)
 # faces must be planar star polygons, not a triangulated convex hull or fake filling.
 edges=collections.Counter(tuple(sorted((f[j],f[(j+1)%len(f)]))) for f in faces for j in range(len(f)))
 V,E,F=len(verts),len(edges),len(faces)
 assert (V,E,F)==expected,(slot,(V,E,F),expected)
 assert all(x==2 for x in edges.values())
 lengths=np.array([np.linalg.norm(verts[a]-verts[b]) for a,b in edges])
 assert (lengths.max()-lengths.min())/lengths.mean()<1e-7
 plane_error=0
 for f in faces:
  pts=verts[f];normal=np.cross(pts[1]-pts[0],pts[2]-pts[0]);normal/=np.linalg.norm(normal)
  plane_error=max(plane_error,max(abs((pts-pts[0])@normal)))
 assert plane_error<1e-7,plane_error
 m={'source':'independent analytic incidence construction from regular icosahedron vertex orbit',
   'slug':f'RAP-SLOT-{slot:03d}', 'vertices':np.round(verts,9).tolist(),'faces':[list(map(int,f)) for f in faces],
   'counts':{'V':V,'E':E,'F':F,'euler':V-E+F},'face_sizes':dict(collections.Counter(len(f) for f in faces)),
   'edge_length_relative_spread':float((lengths.max()-lengths.min())/lengths.mean()),
   'all_edges_two_faces':True,'max_face_planarity_error':float(plane_error),
   'verified_euclidean_reference':True,'geometry_class':'SELF_INTERSECTING_REGULAR_STAR',
   'algorithm':method,'formula_reference_url':sources['Kepler'],
   'verification_scope':'planar star-face ring, abstract edge degree two, regular side-length, topology V/E/F; NOT convex hull or physical field closure',
   'source_rights':'ORIGINAL_FORMULA_IMPLEMENTATION','Raphael_metric_admissibility':'UNTESTED',
   'physical_correspondence':'UNTESTED','role_slot':slot}
 meshes[str(slot)]=m
 return m
star_mesh(114,v,small_stellated,(12,30,12),'fivefold neighbor-ring star order, step two')
star_mesh(115,verts_dual,great_stellated,(20,30,12),'abstract dual of great icosahedron; fiveface dual rings')
star_mesh(116,v,great_dodeca,(12,30,12),'pentagonal nearest-neighbor rings about twelve icosahedron axes')
star_mesh(117,v,triangles,(12,30,20),'far-neighbor icosahedron graph triangular cycles')
# one canonical geometry represented by several research slots; never duplicate payload IDs.
aliases['151']=13
aliases['156']=114
aliases['157']=116

# Cross-check expected characteristic counts and polygon inventory for newly added Johnson entries.
expected={
 93:(60,120,62,{3:20,4:30,5:12}),94:(60,120,62,{3:20,4:30,5:12}),
 95:(60,120,62,{3:20,4:30,5:12}),96:(60,120,62,{3:20,4:30,5:12}),
 98:(55,105,52,{3:15,4:25,5:11,10:1}),99:(55,105,52,{3:15,4:25,5:11,10:1}),
 100:(55,105,52,{3:15,4:25,5:11,10:1}),103:(50,90,42,{3:10,4:20,5:10,10:2}),
 105:(8,18,12,{3:12}),106:(16,40,26,{3:24,4:2}),107:(10,22,14,{3:12,4:2}),
 108:(11,26,17,{3:16,4:1}),109:(12,28,18,{3:16,4:2}),110:(14,33,21,{3:18,4:3}),
 111:(16,38,24,{3:20,4:4}),112:(14,26,14,{3:8,4:2,5:4}),
 113:(18,36,20,{3:13,4:3,5:3,6:1})
}
for slot,(V,E,F,inventory) in expected.items():
 m=meshes[str(slot)];assert (m['counts']['V'],m['counts']['E'],m['counts']['F'])==(V,E,F),slot
 assert {int(k):val for k,val in m['face_sizes'].items()}==inventory,(slot,m['face_sizes'],inventory)

# Independent signature distinction for adjacent Johnson classes with equal scalar counts.
def colored_incidence(m):
 G=nx.Graph();vertices=len(m['vertices']);G.add_nodes_from(range(vertices),tag='vertex')
 for i,f in enumerate(m['faces']):
  node=vertices+i;G.add_node(node,tag='face_'+str(len(f)))
  for j in f:G.add_edge(node,j)
 return G
for a,b in ((94,95),(98,99),(99,100)):
 assert not nx.is_isomorphic(colored_incidence(meshes[str(a)]),colored_incidence(meshes[str(b)]),node_match=lambda x,y:x['tag']==y['tag']),(a,b)

# Mark all 92 Johnson positions as having numeric Euclidean reference coordinates.
for slot in range(22,114):assert str(slot) in meshes,('missing_Johnson',slot)
assert str(130) in meshes
assert str(13) in meshes

for entry in source['items']:
 slot=entry['slot'];shape=meshes.get(str(slot)) or (meshes.get(str(aliases[str(slot)])) if str(slot) in aliases else None)
 entry['mesh']=bool(shape)
 entry['mesh_reference_slot']=int(aliases[str(slot)]) if str(slot) in aliases else (slot if shape else None)
 if shape:
  entry['counts']={k:int(shape['counts'][k]) for k in('V','E','F')}
  entry['counts_grade']='ANALYTIC_EUCLIDEAN_REFERENCE' if shape.get('geometry_class')!='SELF_INTERSECTING_REGULAR_STAR' else 'NONCONVEX_STAR_INCIDENCE_REFERENCE'
  entry['evidence']='NUMERIC_COORDINATES_FACE_INCIDENCE_AND_EDGE_TESTS_EUCLIDEAN'
  entry['mesh_provenance']='ORIGINAL_FORMULA_CONSTRUCTION'
  entry['mesh_class']=shape.get('geometry_class','CONVEX_EUCLIDEAN')
 else:
  entry['counts_grade']='SOURCE_REFERENCE_OR_DRAFT_UNVERIFIED'
  entry['mesh_provenance']='NOT_ATTACHED'
  entry['mesh_class']='PROVISIONAL_MODEL_ONLY'
 entry['Raphael_common_metric']='UNDEFINED'
 entry['physical_validity']='NOT_PROVEN'
 if 93<=slot<=113 and str(slot) in meshes:
  entry['source']=meshes[str(slot)].get('formula_reference_url',entry.get('source'))
source['version']='0.5.0-research';source['exact_geometry_count']=len(meshes)
source['mesh_role_count']=sum(1 for r in source['items'] if r['mesh'])
source['metric_status']='COMMON_RAPHAEL_METRIC_NOT_DEFINED'
source['physical_status']='PHYSICAL_CORRESPONDENCE_HYPOTHESIS'
assert len(source['items'])==173 and source['items'][173-1]['slot']==173
assert cat['position_174']['state']=='INTENTIONALLY_EMPTY' and cat['position_174']['object_id'] is None

# Geometry hashes provide content-identity receipts for future dedup, not a mint/authentication signature.
for k,m in meshes.items():
 payload={'v':m['vertices'],'f':m['faces']}
 m['numerical_geometry_hash_sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()

out={'schema_version':'0.5-research','scope':'Numeric Euclidean reference geometries, star abstract incidences; NO Raphael metric embeddings',
 'mesh_count':len(meshes),'alias_count':len(aliases),'meshes':meshes,'aliases':aliases,
 'rejected':prior['rejected'],'source_conflicts':prior['source_conflicts'],
 'admission_boundary':'Research preview only, no mint or physical theory acceptance'}
(OUT_DIR/'analytic_reference_meshes_v05.json').write_text(json.dumps(out,separators=(',',':')))
(OUT_DIR/'showcase_data_v05.json').write_text(json.dumps(source,separators=(',',':')))
qa={'schema_version':'0.5-research','positions':173,'johnson_exact_euclidean_roles':92,'new_coordinate_reference_count':len(meshes)-len(prior['meshes']),
 'distinct_numeric_meshes':len(meshes),'shared_geometry_alias_roles':len(aliases),'mesh_backed_roles':source['mesh_role_count'],
 'remaining_unattached':173-source['mesh_role_count'],'kepler_star_reconstructions':4,
 'J72_75_77_79_82_graph_nonisomorphism':'PASS','position_174':'EMPTY_NOT_OBJECT',
 'common_Raphael_metric':'UNDEFINED','raphael_physical_ToE':'NOT_PROVEN','mint':'BLOCKED',
 'all_92_Johnson_Euclidean_counts_faces_edges':'PASS'}
(OUT_DIR/'showcase_qa_v05.json').write_text(json.dumps(qa,indent=2))
print(json.dumps(qa,indent=2))
