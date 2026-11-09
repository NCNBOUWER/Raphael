#!/usr/bin/env python3
"""Add formula-derived convex Euclidean reference meshes to Raphael 173.

No externally copied mesh-coordinate data. Outputs checked numeric embeddings of
analytic constructions, and explicitly preserves gaps for nonconvex and proposed slots.
"""
import contextlib, io, importlib.util, json, math, pathlib, itertools
from collections import Counter
import numpy as np
from scipy.spatial import ConvexHull
ROOT=pathlib.Path(__file__).resolve().parents[3]
B=ROOT/'Raphael_Packages/geometry_173/showcase'

def load_original():
 spec=importlib.util.spec_from_file_location('analytical_seeds',B/'build_analytic.py')
 obj=importlib.util.module_from_spec(spec)
 obj.pathlib=pathlib
 with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(obj)
 return obj
m=load_original()

def unique_tol(v,eps=2e-8):
 arr=np.asarray(v,float);out=[]
 for pt in arr:
  if not any(np.linalg.norm(pt-q)<eps for q in out):out.append(pt)
 return np.asarray(out)

def cupola(n):
 rt=1/(2*math.sin(math.pi/n));rb=1/(2*math.sin(math.pi/(2*n)))
 dz=rb*math.cos(math.pi/(2*n))-rt*math.cos(math.pi/n)
 h=math.sqrt(1-dz*dz)
 base=np.array([[rb*math.cos(k*math.pi/n),rb*math.sin(k*math.pi/n),0] for k in range(2*n)])
 top=np.array([[rt*math.cos((2*k-.5)*math.pi/n),rt*math.sin((2*k-.5)*math.pi/n),h] for k in range(n)])
 return np.r_[base,top],h

def rotunda():
 I=m.rectify(m.icosa());axis=m.icosa()[0]/np.linalg.norm(m.icosa()[0]);z=np.array([0.,0.,1.]); proj=I@axis; v=I[proj>=-1e-6]
 cross=np.cross(axis,z);s=np.linalg.norm(cross);c=axis@z
 if s<1e-10:rot=np.eye(3)
 else:
  x,y,z0=cross/s; K=np.array([[0,-z0,y],[z0,0,-x],[-y,x,0]]);rot=np.eye(3)+K*s+K@K*(1-c)
 v=v@rot.T;base=v[abs(v[:,2])<1e-7];a=math.atan2(base[0,1],base[0,0]);v=v@np.array([[math.cos(-a),math.sin(-a),0],[-math.sin(-a),math.cos(-a),0],[0,0,1]]).T
 d=np.linalg.norm(v[:,None,:]-v[None,:,:],axis=2);v/=d[d>1e-8].min();v[:,2]-=v[np.argmin(abs(v[:,2])),2]
 return unique_tol(v)

def transf(v,z=0,mirror=False,rotate=0):
 a=np.array(v,float,copy=True);a[:,2]*=-1 if mirror else 1
 if rotate:
  c,s=math.cos(rotate),math.sin(rotate);a[:,:2]=a[:,:2]@np.array([[c,s],[-s,c]])
 a[:,2]+=z;return a

def prism_lower(n,anti=False,top=0):
 R=1/(2*math.sin(math.pi/n));d=math.pi/n if anti else 0
 h=math.sqrt(max(0,1-(2*R*math.sin(d/2))**2)) if anti else 1
 return np.array([[R*math.cos(2*k*math.pi/n+ang),R*math.sin(2*k*math.pi/n+ang),zz] for zz,ang in [(top,0),(top-h,-d)] for k in range(n)]),h

def stack(kind,n,extension=None,other=None,gyro=False):
 upper=cupola(n)[0] if kind=='cup' else rotunda();size=2*n if kind=='cup' else 10
 if extension:
  _,h=prism_lower(size,extension=='anti')
  lower,_=prism_lower(size,extension=='anti',h if other else 0)
  if other is None:return unique_tol(np.r_[upper,lower]);
  upper=transf(upper,z=h,rotate=math.pi/n if gyro else 0)
  bottom=transf(cupola(n)[0] if other=='cup' else rotunda(),mirror=True,rotate=-math.pi/size if extension=='anti' else 0)
  return unique_tol(np.r_[upper,lower,bottom])
 bottom=transf(cupola(n)[0] if other=='cup' else rotunda(),mirror=True,rotate=math.pi/n if gyro else 0)
 return unique_tol(np.r_[upper,bottom])

def pyramid_join(n,anti=False,both=False):
 R=1/(2*math.sin(math.pi/n));a=math.sqrt(1-R*R)
 b,h=prism_lower(n,anti,0)
 v=np.r_[b,[[0,0,a]]]
 if both:v=np.r_[v,[[0,0,-h-a]]]
 return unique_tol(v)

def augmented_prism(n,faces):
 R=1/(2*math.sin(math.pi/n));v=np.asarray(m.prism(n),float).tolist();h=math.sqrt(.5)
 for k in faces:
  angle=(2*k+1)*math.pi/n;nrm=np.array([math.cos(angle),math.sin(angle),0]);p=R*math.cos(math.pi/n)*nrm+h*nrm;v.append(p)
 return unique_tol(v)

def unit(v):
 v=np.asarray(v,float);d=np.linalg.norm(v[:,None,:]-v[None,:,:],axis=2);return v/d[d>1e-8].min()

def faces_info(v):
 ff=m.faces_from_hull(v);center=v.mean(axis=0);out=[]
 for f in ff:
  pp=v[f];ctr=pp.mean(axis=0);n=np.cross(pp[1]-pp[0],pp[2]-pp[1]);n/=np.linalg.norm(n)
  if (ctr-center)@n<0:n=-n
  out.append({'ids':f,'center':ctr,'normal':n,'size':len(f)})
 return out

def augment_pyramid(v,indices,n):
 v=unit(v);ff=faces_info(v);height=math.sqrt(1-(1/(2*math.sin(math.pi/n)))**2)
 return unique_tol(np.r_[v,[ff[i]['center']+ff[i]['normal']*height for i in indices]])

def augment_cup(v,indices,n,phase_bits=None):
 v=unit(v);ff=faces_info(v);rt=1/(2*math.sin(math.pi/n));rb=1/(2*math.sin(math.pi/(2*n)))
 d=rb*math.cos(math.pi/(2*n))-rt*math.cos(math.pi/n);h=math.sqrt(1-d*d);coords=[]
 for ix,j in enumerate(indices):
  f=ff[j];assert f['size']==2*n
  u=v[f['ids'][0]]-f['center'];u/=np.linalg.norm(u);normal=f['normal'];w=np.cross(normal,u)
  for k in range(n):
   phase=.5 if phase_bits and phase_bits[ix] else -.5
   a=(2*k+phase)*math.pi/n;coords.append(f['center']+rt*(math.cos(a)*u+math.sin(a)*w)+h*normal)
 return unique_tol(np.r_[v,coords])

def polar_dual(v):
 v=np.asarray(v,float);v-=v.mean(axis=0)
 h=ConvexHull(v);return unique_tol([x[:3]/(-x[3]) for x in h.equations])

def verified_convex(v,slot,uniform_edges=True):
 v=unique_tol(v)
 try:r=m.mesh(v,(-1,-1,-1),f'RAP-SLOT-{slot:03d}')
 except Exception as e:return None,f'geometry solver failed: {e}'
 E=r['counts'];good=E['euler']==2 and r['all_edges_two_faces'] and r['counts']['V']==len(v)
 if uniform_edges:good=good and r['edge_length_relative_spread']<1e-6
 if not good:return None, 'convex closure/equal-edge test failed'
 r['verified_euclidean_reference']=True
 r['algorithm']='analytic construction, SciPy convex-hull facet reconstruction; coordinate precision 9 digits'
 r['original_source']='Raphael formula-based generator, not 3rd party mesh data'
 return r,None

# Published coordinate *formulas* evaluated independently (not copying a mesh archive).
def cyclic_sign_orbit(triples):
 pts=[]
 for base in triples:
  x,y,z=base
  for perm in [(x,y,z),(z,x,y),(y,z,x)]:
   for signs in itertools.product((-1,1),repeat=3):pts.append([a*b for a,b in zip(perm,signs)])
 return unique_tol(pts)

def snub_cube_coordinates():
 t=1.8392867552141611326; base=(1,1/t,t);pts=[]
 for perm in itertools.permutations(range(3)):
  inv=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2
  for signs in itertools.product([-1,1],repeat=3):
   plus=sum(x==1 for x in signs)
   if plus%2==inv:pts.append([base[perm[k]]*signs[k] for k in range(3)])
 return unique_tol(pts)

PHI=(1+math.sqrt(5))/2
rich_rhombico=cyclic_sign_orbit([(1,1,PHI**3),(PHI**2,PHI,2*PHI),(2+PHI,0,PHI**2)])
trunc_icosidodeca=cyclic_sign_orbit([(1/PHI,1/PHI,3+PHI),(2/PHI,PHI,1+2*PHI),(1/PHI,PHI**2,-1+3*PHI),(2*PHI-1,2,2+PHI),(PHI,3,2*PHI)])
# Build exact Euclidean candidate vertices according to standard named constructions.
candidates={}
candidates[7]=snub_cube_coordinates()
candidates[11]=rich_rhombico
candidates[12]=trunc_icosidodeca
# 20 vetted prior sources are reused; remove slot 12 (invalid equal-edge test).
orig=json.loads((B/'analytic_reference_meshes.json').read_text())['meshes']
mesh_by_slot={int(k):v for k,v in orig.items() if v.get('verified_euclidean_reference')}
for n,j in [(3,3),(4,4),(5,5)]:candidates[j+21]=cupola(n)[0]
candidates[27]=rotunda()
for n,j in [(3,7),(4,8),(5,9),(4,10),(5,11)]:candidates[j+21]=pyramid_join(n,anti=j>=10)
for n,j in [(3,14),(4,15),(5,16),(4,17)]:candidates[j+21]=pyramid_join(n,anti=j==17,both=True)
for n,j in [(3,18),(4,19),(5,20)]:candidates[j+21]=stack('cup',n,extension='prism')
candidates[42]=stack('rotunda',5,extension='prism')
for n,j in [(3,22),(4,23),(5,24)]:candidates[j+21]=stack('cup',n,extension='anti')
candidates[46]=stack('rotunda',5,extension='anti')
s=.5;h=math.sqrt(3)/2
candidates[47]=unique_tol([[x,y,0] for x in[-s,s] for y in[-s,s]]+[[0,y,h] for y in[-s,s]]+[[x,0,-h] for x in[-s,s]])
for n,j in [(3,27),(4,28),(4,29),(5,30),(5,31)]:candidates[j+21]=stack('cup',n,other='cup',gyro=j in (29,31))
for j in (32,33):candidates[j+21]=stack('cup',5,other='rotunda',gyro=j==33)
candidates[55]=stack('rotunda',5,other='rotunda')
for n,j in [(3,35),(3,36),(4,37),(5,38),(5,39),(5,40),(5,41),(5,42),(5,43)]:
 a,b=('cup','rotunda') if j in (40,41) else ('rotunda','rotunda') if j in (42,43) else ('cup','cup')
 candidates[j+21]=stack(a,n,extension='prism',other=b,gyro=j in (36,37,39,41,43))
for n,j in [(3,44),(4,45),(5,46),(5,47),(5,48)]:
 a,b=('cup','rotunda') if j==47 else ('rotunda','rotunda') if j==48 else ('cup','cup')
 candidates[j+21]=stack(a,n,extension='anti',other=b)
for j,n,faces in [(49,3,[0]),(50,3,[0,1]),(51,3,[0,1,2]),(52,5,[0]),(53,5,[0,2]),(54,6,[0]),(55,6,[0,3]),(56,6,[0,2]),(57,6,[0,2,4])]:candidates[j+21]=augmented_prism(n,faces)
# dodecahedron pentagonal-pyramid augmentation (J58–J61)
dodeca=unit(m.D);ff=faces_info(dodeca);i=0
sims=sorted((float(ff[i]['normal']@ff[j]['normal']),j) for j in range(len(ff)) if j!=i)
for j,faces in [(58,[i]),(59,[i,sims[0][1]]),(60,[i,sims[1][1]]),(61,[i,sims[2][1],sims[4][1]])]:candidates[j+21]=augment_pyramid(dodeca,faces,5)
# J62–J64: icosahedral vertex removal and a compatible regular tetrahedral augmentation.
# The selections were compared against published Johnson V/E/F and face inventories.
candidates[62+21]=np.delete(m.I,[0,5],axis=0)  # J62: 10V, 20E, 12F; 10 triangles + 2 pentagons
tri_diminished=np.delete(m.I,[0,5,9],axis=0)
candidates[63+21]=tri_diminished  # J63: 9V, 15E, 8F; 5 triangles + 3 pentagons
candidates[64+21]=augment_pyramid(tri_diminished,[0],3)  # J64: 10V, 18E, 10F
# J76, J80, J81, J83: remove pentagonal cupolas from analytic rhombicosidodecahedron.
# Each cap removal deletes its five top-pentagon vertices. "para" uses opposite
# fivefold axes; "meta" uses non-opposite axes; J83 chooses three pairwise
# separated cap axes. All are compared with published Johnson fingerprints.
_rhombi_faces=[f for f in faces_info(rich_rhombico) if f['size']==5]
def diminish_rhombico(face_numbers):
 excluded=set().union(*(set(_rhombi_faces[k]['ids']) for k in face_numbers))
 return np.delete(rich_rhombico,sorted(excluded),axis=0)
for j,faces in [(76,(0,)),(80,(0,3)),(81,(0,1)),(83,(0,1,6))]:
 candidates[j+21]=diminish_rhombico(faces)
# truncated-solid cupola augmentation, J65-71. Nonadjacent selection, independently check face inventory.
for j,shape,n,faces in [(65,1,3,[4]),(66,3,4,[8]),(67,3,4,[8,13]),(68,10,5,[20]),(69,10,5,[20,24]),(70,10,5,[20,26]),(71,10,5,[20,24,29])]:candidates[j+21]=augment_cup(m.provided[shape],faces,n,phase_bits=([1] if j==65 else [0,1] if j==67 else None))

rejections={};added=[]
for slot,v in sorted(candidates.items()):
 if slot in mesh_by_slot:continue
 result,why=verified_convex(v,slot)
 if result:
  mesh_by_slot[slot]=result;added.append(slot)
 else:rejections[str(slot)]=why
# Derive exact Catalan convex duals for the eight analytic Archimedean references available.
for slot in list(range(1,14)):
 if (slot not in m.provided and slot not in candidates) or slot not in mesh_by_slot:continue
 dual_slot=117+slot
 dual,why=verified_convex(polar_dual(m.provided[slot] if slot in m.provided else candidates[slot]),dual_slot,uniform_edges=False)
 if dual:
  dual['algorithm']='polar dual of analytic Archimedean Euclidean construction'
  mesh_by_slot[dual_slot]=dual
 else:rejections[str(dual_slot)]=why
# Reference Platonic and permitted uniform alias roles. No duplicate geometry payloads.
refmesh={}
for slot,geom in [(144, m.icosa()),(145,m.D)]:
 x,why=verified_convex(geom,slot)
 if x:mesh_by_slot[slot]=x
 else:rejections[str(slot)]=why
for k,refslot in [(146,8),(147,9),(148,10),(149,11),(150,12),(151,13)]:
 if refslot in mesh_by_slot:refmesh[str(k)]=refslot
# slot14 duplicates J37 at slot58, which is now formula-generated
if 58 in mesh_by_slot:refmesh['14']=58

# Check formula-derived shapes against independently published source counts when available.
cat=json.loads((ROOT/'Raphael_Packages/geometry_173/catalogue.json').read_text())
countmismatches={}
for slot,o in mesh_by_slot.items():
 ref=cat['entries'][slot-1].get('reference_counts')
 if ref is not None:
  d=o['counts'];ref3={k:int(ref[k]) for k in ('V','E','F')}
  if ref3!={k:d[k] for k in ('V','E','F')}:countmismatches[str(slot)]={'source_ref':ref3,'generated':{k:d[k] for k in ('V','E','F')}}
# Published Johnson topological fingerprints (OrchidPalms / Johnson catalogue).
# This independent comparison matters: a closed regular-faced convex hull alone
# does not prove the chosen Johnson label. A J65 and J67 phase correction was
# required to obtain the *actual* expected face inventories.
published_johnson = {
 62:((10,20,12),{3:10,5:2}),63:((9,15,8),{3:5,5:3}),64:((10,18,10),{3:7,5:3}),
 65:((15,27,14),{3:8,4:3,6:3}),66:((28,48,22),{3:12,4:5,8:5}),
 67:((32,60,30),{3:16,4:10,8:4}),
 68:((65,105,42),{3:25,4:5,5:1,10:11}),
 69:((70,120,52),{3:30,4:10,5:2,10:10}),
 70:((70,120,52),{3:30,4:10,5:2,10:10}),
 71:((75,135,62),{3:35,4:15,5:3,10:9}),
 76:((55,105,52),{3:15,4:25,5:11,10:1}),
 80:((50,90,42),{3:10,4:20,5:10,10:2}),
 81:((50,90,42),{3:10,4:20,5:10,10:2}),
 83:((45,75,32),{3:5,4:15,5:9,10:3}),
}
for j,(counts,sizes) in published_johnson.items():
 slot=j+21; obj=mesh_by_slot.get(slot)
 if obj is None:continue
 c=obj['counts']; vef=tuple(c[k] for k in ('V','E','F'))
 actual_sizes={int(k):v for k,v in obj['face_sizes'].items()}
 if vef!=counts or actual_sizes!=sizes:
  countmismatches[str(slot)]={'published_J':j,'published_VEF':counts,'published_faces':sizes,'computed_VEF':vef,'computed_faces':actual_sizes}
# For mismatches, do not claim source-verified identity; keep as construction candidates separately.
for slot in list(countmismatches):
 rejections[slot]='Reference count disagreement: manual review required; withheld mesh'
 mesh_by_slot.pop(int(slot),None)
for slot in list(refmesh):
 if refmesh[slot] not in mesh_by_slot:refmesh.pop(slot)

# Ensure every vertex and every face is finite, nondegenerate and valid.
for slot,o in mesh_by_slot.items():
 verts=np.asarray(o['vertices']);assert np.all(np.isfinite(verts))
 assert all(len(f)>=3 and len(f)==len(set(f)) and max(f)<len(verts) for f in o['faces'])
 o['independent_geometry_status']='ANALYTIC_EUCLIDEAN_CONSTRUCTION_VALIDATED'
 o['Raphael_metric_admissibility']='UNTESTED'
 o['physical_correspondence']='UNTESTED'
 o['source_rights']='ORIGINAL_FORMULA_GENERATOR'
 o['role_slot']=slot
assert len(set(mesh_by_slot)|set(map(int,refmesh)))<=173
out={'schema_version':'0.3-research','scope':'Exact formula-based Euclidean geometric references, not 173 Raphael metric embeddings','mesh_count':len(mesh_by_slot),'alias_count':len(refmesh),'meshes':{str(k):v for k,v in sorted(mesh_by_slot.items())},'aliases':refmesh,'rejected':rejections,'source_conflicts':countmismatches}
(B/'analytic_reference_meshes_v03.json').write_text(json.dumps(out,separators=(',',':')))
print(json.dumps({'mesh_count':len(mesh_by_slot),'alias_count':len(refmesh),'role_coverage':len(mesh_by_slot)+len(refmesh),'rejected':rejections,'mismatches':countmismatches},indent=2))
