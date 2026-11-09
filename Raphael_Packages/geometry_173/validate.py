#!/usr/bin/env python3
"""Structural validation for Raphael 173 staging; does not prove physics."""
import json,math,pathlib,collections
d=pathlib.Path(__file__).resolve().parent
c=json.loads((d/"catalogue.json").read_text())
g=json.loads((d/"relations.json").read_text())
m=json.loads((d/"model.json").read_text())
a=c["entries"]
assert len(a)==173 and [x["slot"] for x in a]==list(range(1,174))
assert len({x["role_id"] for x in a})==173
assert [x["canonical_geometry_id"] for x in a[21:113]]==["J"+str(i) for i in range(1,93)]
assert [x["canonical_geometry_id"] for x in a[137:172]]==["U"+str(i) for i in range(16,51)]
assert a[13]["canonical_geometry_id"]==a[57]["canonical_geometry_id"]=="J37"
assert a[172]["reference_counts"]=={"V":60,"E":240,"F":124}
assert 40*3+60*4+24*5==2*240 and 60-240+124==-56
assert c["position_174"]["state"]=="INTENTIONALLY_EMPTY"
assert c["position_174"]["object_id"] is None
assert all(not r["verification"]["mintable"] for r in a)
assert all(r["verification"]["physical_correspondence"]=="HYPOTHESIS" for r in a)
p=(1+math.sqrt(5))/2
assert all(math.isclose(r["golden_scale"]["ratio_to_first"],p**(r["slot"]-1),rel_tol=1e-12) for r in a)
assert len(g["edges"])==g["edge_count"]
print(json.dumps({"structural_map":"PASS","slot_roles":173,"edges":len(g["edges"]),"metric_and_physical_proof":"NOT_ATTESTED"},indent=2))
