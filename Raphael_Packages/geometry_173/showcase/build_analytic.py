"""Independent coordinate construction for selected classical polyhedra.

All geometries are conventional EUCLIDEAN reference samples, not Raphael-metric
embeddings. No external shape coordinate dataset is copied.
"""
from __future__ import annotations
import itertools,math,json
from collections import Counter,defaultdict
import numpy as np
from scipy.spatial import ConvexHull

PHI=(1+math.sqrt(5))/2

def unique(points):
    r={tuple(round(float(v),12) for v in p) for p in points}
    return np.array(sorted(r),dtype=float)

def signperm(values):
    pts=[]
    for v in set(itertools.permutations(values)):
        for signs in itertools.product((-1,1),repeat=3):
            pts.append([a*s for a,s in zip(v,signs)])
    return unique(pts)

def truncate(points,fraction=1/3):
    v=unique(points); hull=ConvexHull(v);
    # hull triangles contain diagonals on coplanar faces; use min edge length
    # for known equal-edge regular input, true edges are minimal positive distances.
    dd=np.linalg.norm(v[:,None,:]-v[None,:,:],axis=2)
    positive=dd[dd>1e-6]; edge=float(np.min(positive));
    pairs=[(i,j) for i in range(len(v)) for j in range(i+1,len(v)) if abs(dd[i,j]-edge)<1e-5]
    p=[]
    for i,j in pairs:
        p.extend([v[i]*(1-fraction)+v[j]*fraction,v[j]*(1-fraction)+v[i]*fraction])
    return unique(p)

def icosa():
    return unique([(0,a,b*PHI) for a in(-1,1) for b in(-1,1)] + [(a,b*PHI,0) for a in(-1,1) for b in(-1,1)] + [(a*PHI,0,b) for a in(-1,1) for b in(-1,1)])

def rectify(points):
    v=unique(points);dd=np.linalg.norm(v[:,None,:]-v[None,:,:],axis=2);
    d=np.min(dd[dd>1e-6]);
    return unique((v[i]+v[j])/2 for i in range(len(v)) for j in range(i+1,len(v)) if abs(dd[i,j]-d)<1e-6)

def pyramid(n):
    rad=1/(2*math.sin(math.pi/n));h=math.sqrt(1-rad**2)
    return unique([[rad*math.cos(2*math.pi*j/n),rad*math.sin(2*math.pi*j/n),0] for j in range(n)]+[[0,0,h]])

def dipyramid(n):
    rad=1/(2*math.sin(math.pi/n));h=math.sqrt(1-rad**2)
    return unique([[rad*math.cos(2*math.pi*j/n),rad*math.sin(2*math.pi*j/n),0] for j in range(n)]+[[0,0,h],[0,0,-h]])

def prism(n,anti=False):
    # regular unit-edged prism/antiprism
    R=1/(2*math.sin(math.pi/n)); delta=math.pi/n if anti else 0
    h=math.sqrt(max(0,1-(2*R*math.sin(delta/2))**2)) if anti else 1
    return unique([[R*math.cos(2*math.pi*k/n+theta),R*math.sin(2*math.pi*k/n+theta),z]
            for theta,z in [(0,-h/2),(delta,h/2)] for k in range(n)])

def faces_from_hull(v):
    hull=ConvexHull(v)
    normal_groups={}
    for simp,equation in zip(hull.simplices,hull.equations):
        n=equation[:3];norm=np.linalg.norm(n);n=n/norm;d=equation[3]/norm
        key=tuple(np.round(np.r_[n,d],6));normal_groups.setdefault(key,set()).update(map(int,simp))
    faces=[]
    for key,inds in normal_groups.items():
        idx=sorted(inds)
        ctr=v[idx].mean(axis=0)
        n=np.array(key[:3]);
        horizontal=v[idx[0]]-ctr;horizontal=horizontal/np.linalg.norm(horizontal)
        vertical=np.cross(n,horizontal)
        a=[math.atan2(np.dot(v[k]-ctr,vertical),np.dot(v[k]-ctr,horizontal)) for k in idx]
        ordered=[x for _,x in sorted(zip(a,idx))]
        faces.append(ordered)
    # sort deterministic to reduce source drift
    return sorted(faces,key=lambda f:(len(f),min(f),f))

def mesh(v,expected,slug):
    v=unique(v); faces=faces_from_hull(v)
    edges=Counter(tuple(sorted((face[i],face[(i+1)%len(face)]))) for face in faces for i in range(len(face)))
    nV=len(v);nE=len(edges);nF=len(faces)
    d=np.array([np.linalg.norm(v[a]-v[b]) for a,b in edges])
    residual=(d.max()-d.min())/d.mean() if len(d) else None
    comp=(nV,nE,nF)
    sizes=Counter(map(len,faces))
    valid=(comp==tuple(expected) and all(n==2 for n in edges.values()) and nV-nE+nF==2 and (residual is not None and residual<1e-6))
    return {
        'source':'independently constructed analytic Euclidean reference; convex hull coplanar facet reconstruction',
        'slug':slug,'vertices':v.round(9).tolist(),'faces':faces,
        'counts':{'V':nV,'E':nE,'F':nF,'euler':nV-nE+nF},
        'face_sizes':dict(sizes),'edge_length_relative_spread':float(residual),
        'all_edges_two_faces':all(n==2 for n in edges.values()),
        'verified_euclidean_reference':bool(valid),
        'Raphael_metric_admissibility':'NOT_TESTED',
    }

E={
  1:(12,18,8),2:(12,24,14),3:(24,36,14),4:(24,36,14),5:(24,48,26),6:(48,72,26),
  8:(30,60,32),9:(60,90,32),10:(60,90,32),12:(120,180,62),
  15:(6,9,5),16:(10,15,7),17:(12,18,8),18:(16,24,10),19:(20,30,12),
  20:(8,16,10),21:(10,20,12),22:(5,8,5),23:(6,10,6),33:(5,9,6),34:(7,15,10)
}
# tetrahedron vertices, regular
T=unique([(1,1,1),(-1,-1,1),(-1,1,-1),(1,-1,-1)])
I=icosa()
# dodeca is polar dual of regular icosa, from convex hull outward face normals
h=ConvexHull(I)
D=unique(e[:3]/(-e[3]) for e in h.equations)
provided={
  1:truncate(T),
  2:signperm((1,1,0)),
  3:signperm((1,1,math.sqrt(2)-1)),
  4:signperm((0,1,2)),
  5:signperm((1,1,1+math.sqrt(2))),
  6:signperm((1,1+math.sqrt(2),1+2*math.sqrt(2))),
  8:rectify(I),
  9:truncate(I),
  10:truncate(D,1/(2+PHI)),
  12:truncate(rectify(I)),
  15:prism(3),16:prism(5),17:prism(6),18:prism(8),19:prism(10),
  20:prism(4,True),21:prism(5,True),
  22:pyramid(4),23:pyramid(5),33:dipyramid(3),34:dipyramid(5)
}

out={};
for slot,v in provided.items():
  try:
    x=mesh(v,E[slot],f'RAP-SLOT-{slot:03d}')
  except Exception as exc:
    print('ERROR',slot,exc);continue
  print(f'{slot:03} {x["counts"]} sizes {x["face_sizes"]} spread {x["edge_length_relative_spread"]:.3g} pass {x["verified_euclidean_reference"]}')
  if x['verified_euclidean_reference']:out[str(slot)]=x
print('verified',len(out),'of',len(provided))
with open(str(pathlib.Path(__file__).resolve().parent/'analytic_reference_meshes.json'),'w') as f:json.dump({'scope':'selected Euclidean analytic polyhedra reference meshes only; no Raphael spacetime geometry proof','meshes':out},f,separators=(',',':'))
