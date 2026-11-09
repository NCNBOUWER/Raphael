#!/usr/bin/env python3
"""Patch existing Raphael PR7 v04 UI, with v05 data and explicit star-mesh fidelity."""
from pathlib import Path
import json,re
p=Path(__file__).resolve().parents[3]
B=p/'Raphael_Packages/geometry_173/showcase'
data=json.loads((B/'showcase_data_v05.json').read_text())
geom=json.loads((B/'analytic_reference_meshes_v05.json').read_text())
s=(B/'showcase_v03.html').read_text()
def seed(tag,payload):
 global s
 pat=rf'(<script id="{tag}" type="application/json">)(.*?)(</script>)'
 enc=json.dumps(payload,separators=(',',':')).replace('</','<\\/')
 s,n=re.subn(pat,lambda m:m.group(1)+enc+m.group(3),s,count=1,flags=re.S)
 assert n==1,(tag,n)
seed('seed',data)
seed('mesh-seed',{'meshes':geom['meshes'],'aliases':geom['aliases']})
s=s.replace('Raphael 173 · Sequence-Sort Geometry Studio','Raphael 173 · Verified Reference Atlas v0.5')
s=s.replace('Exact Euclidean mesh', 'Coordinate mesh')
# Correct graph horizontal ordering: must reflect sort index, not immutable Raphael slot.
a='for(const r of ordered){const x=baseX+(r.slot-1)*step,y=h/2+Math.sin(r.slot*.153)*h*.27;nodes.push([x,y]);}'
b='for(let pos=0;pos<ordered.length;pos++){const r=ordered[pos],x=baseX+pos*step,y=h/2+Math.sin(r.slot*.153)*h*.27;nodes.push([x,y]);}'
assert a in s;s=s.replace(a,b)
# Interpret self-intersecting star faces as wireframe paths only; avoid false filled exterior.
a="ctx.fillStyle=`hsla(${hue},49%,${28+Math.max(0,light)*26}%,.94)`;ctx.fill();if(state.wire){ctx.strokeStyle='rgba(169,233,239,.68)';ctx.lineWidth=1.15;ctx.stroke();}"
b="ctx.fillStyle=`hsla(${hue},49%,${28+Math.max(0,light)*26}%,.94)`;if(m.geometry_class!=='SELF_INTERSECTING_REGULAR_STAR')ctx.fill();if(state.wire||m.geometry_class==='SELF_INTERSECTING_REGULAR_STAR'){ctx.strokeStyle='rgba(169,233,239,.78)';ctx.lineWidth=1.15;ctx.stroke();}"
assert a in s;s=s.replace(a,b)
a="$('sourceBadge').textContent=m?'EXACT EUCLIDEAN MESH':'SCHEMATIC ONLY'"
b="$('sourceBadge').textContent=m?(m.geometry_class==='SELF_INTERSECTING_REGULAR_STAR'?'STAR INCIDENCE MESH':'EUCLIDEAN COORDINATE MESH'):'SCHEMATIC ONLY'"
assert a in s;s=s.replace(a,b)
a="$('sceneNote').textContent=m?'Drag to rotate · wheel to zoom':'Procedural representation — exact mesh not attached'"
b="$('sceneNote').textContent=m?(m.geometry_class==='SELF_INTERSECTING_REGULAR_STAR'?'Regular star face paths · self-intersections · wireframe only':'Drag to rotate · wheel to zoom'):'Procedural schematic — mesh unverified'"
assert a in s;s=s.replace(a,b)
a="$('euclid').textContent=m?'Analytic mesh validated':r.counts?'Reference counts only':'Identity only'"
b="$('euclid').textContent=m?(m.geometry_class==='SELF_INTERSECTING_REGULAR_STAR'?'Non-convex star incidence tested':'Analytic Euclidean mesh tested'):r.counts?'Source / draft counts':'Identity only'"
assert a in s;s=s.replace(a,b)
# Front-page coverage statement is precise about scope.
s=s.replace('20 Euclidean meshes','140 mesh-backed reference positions').replace('104 Euclidean meshes','140 mesh-backed reference positions')
s=s.replace('Source-governed geometries are research references, not verified physical ontology.','Source-governed geometries are research references, not verified physical ontology. Exactly 92 conventional Johnson slots have numeric Euclidean reference meshes.')
assert 'function sortedAll()' in s and 'star' in s.lower()
(s2:=B/'showcase_v05.html').write_text(s)
other=s2
print('HTML',other,len(s), 'has title', 'Raphael 173' in s)
