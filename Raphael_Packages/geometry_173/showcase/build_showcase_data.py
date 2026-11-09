#!/usr/bin/env python3
"""Read-only derived UI cache from Raphael PR #7 research catalogue."""
import json,pathlib,re,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT.parent
origin=json.loads((SRC/'catalogue.json').read_text())
relations=json.loads((SRC/'relations.json').read_text())
meshes=json.loads((ROOT/'analytic_reference_meshes.json').read_text())['meshes']
zone_info={
 'core':('Foundational forms','Bound-state / material lattice model','RGS-000 · MRI4D-003'),
 'prisms_antiprisms':('Extruded symmetry','Structural / optical reference paths','CGA-* · MRI4D-003'),
 'johnson':('Local variation','Irregular geometry / candidate state transitions','RGS-000 · T1K-*'),
 'star':('Nonconvex forms','Wave interaction / topology hypothesis','MRI4D-* · RGS-*'),
 'catalan':('Dual construction','Dual geometry / boundary normal mapping','CGA-* · WIT-006'),
 'raphael_candidate':('Candidate torsion','Proposed chiral / phase interfaces','RGS-* · N³/GeoMatrices'),
 'uniform_selected':('Uniform references','Higher-order tiling / waveguide analogies','RGS-* · MRI4D-*'),
 'u75_boundary':('U75 boundary study','Outer-boundary/topological model hypothesis','T1K-* · WIT-*'),
}
ui=[]
for r in origin['entries']:
 z=r['zone']; c=r['reference_counts']; i=int(r['slot']);
 conflicts=str(r['conflict_note'] or '')
 grade='CONSTRUCTED_EUCLIDEAN_REFERENCE' if str(i) in meshes else ('REFERENCE_COUNTS_ONLY' if c else 'SOURCE_IDENTITY_ONLY')
 proposed=zone_info[z][1]
 ui.append({
  'slot':i,'id':r['role_id'],'name':r['reference_name'],'draft':r['draft_name'],
  'canonical':r['canonical_geometry_id'],'family':r['family'],'zone':z,
  'zone_name':zone_info[z][0],'candidate_function':proposed,
  'component_interface':zone_info[z][2],
  'proposed':r['proposed_interdomain_role'],'description':r['descriptive_model'],
  'counts':c,'draft_counts':r['draft_counts'],
  'face_inventory':r['reconciled_face_inventory'] or r['draft_face_inventory'],
  'evidence':grade,'rel_conflict':conflicts,
  'source':r['references'].get('geometry_source'),'viewer':r['references'].get('viewer'),
  'element':r['atomic_correspondence']['symbol'],
  'metric':'NOT_TESTED','physical':'HYPOTHESIS','golden_exponent':i-1,
  'mesh':str(i) in meshes,
  'source_fingerprint':r['references'].get('source_row_fingerprint')
 })
# crossrefs: only links to actual typed ref graph, not speculative cartesian composites
for e in ui:
 s=e['id']; connected=[x for x in relations['edges'] if x['source']==s and x['kind'] not in ('research_family','golden_scale_successor','hypothetical_atomic_correspondence')]
 e['connections']=[{'target':x['target'],'kind':x['kind']} for x in connected]
# full source references retained as original repo link, no third-party proprietary data copied
out={'version':'0.2.0-preview','origin':'NCNBOUWER/Raphael PR#7: catalogue.json and relations.json',
 'origin_source_sha256':hashlib.sha256((SRC/'catalogue.json').read_bytes()).hexdigest(),
 'origin_relationship_count':len(relations['edges']),
 'no_mint':True,'sentinel_174':{'empty':True,'mintable':False,'has_object_id':False},
 'metric_status':'NOT_FORMALISED','physical_status':'NOT_PROVEN',
 'zones':[{ 'id':k, 'label':v[0], 'domain':v[1], 'interface':v[2] } for k,v in zone_info.items()],
 'items':ui}
(ROOT/'showcase_data.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
print('items',len(ui),'meshes',len(meshes),'json chars',(ROOT/'showcase_data.json').stat().st_size)
