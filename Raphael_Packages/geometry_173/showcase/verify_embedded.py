#!/usr/bin/env python3
"""Research-only structural validation for the standalone Raphael 173 studio."""
import pathlib,json,re,collections,math
html=(pathlib.Path(__file__).resolve().parent/"showcase.html").read_text()
def get(id):
    m=re.search(r'<script id="'+re.escape(id)+r'" type="application/json">(.*?)</script>',html,re.S)
    assert m,id
    return json.loads(m.group(1))
x=get("seed"); m=get("mesh-seed")["meshes"]; r=x["items"]
assert [y["slot"] for y in r]==list(range(1,174))
assert len({y["id"] for y in r})==173
assert len(m)==20
assert x["sentinel_174"]["empty"] and not x["sentinel_174"]["mintable"]
assert r[13]["canonical"]==r[57]["canonical"]=="J37"
assert [v["canonical"] for v in r[21:113]]==["J"+str(n) for n in range(1,93)]
assert [v["canonical"] for v in r[137:172]]==["U"+str(n) for n in range(16,51)]
assert r[172]["counts"]=={"V":60,"E":240,"F":124}
assert all(v["physical"]=="HYPOTHESIS" and v["metric"]=="NOT_TESTED" for v in r)
for key,v in m.items():
    edges=collections.Counter(tuple(sorted((f[j],f[(j+1)%len(f)]))) for f in v["faces"] for j in range(len(f)))
    c=v["counts"]
    assert (len(v["vertices"]),len(edges),len(v["faces"]))==(c["V"],c["E"],c["F"])
    assert all(n==2 for n in edges.values())
    assert c["V"]-c["E"]+c["F"]==2
    assert v["edge_length_relative_spread"]<1e-6
    assert v["verified_euclidean_reference"]
    assert v["Raphael_metric_admissibility"]=="NOT_TESTED"
phi=(1+math.sqrt(5))/2
assert math.isclose(math.log(phi),math.log(phi*phi/phi),abs_tol=1e-12)
assert math.isclose(math.pi*math.sin(math.pi/2)/(math.pi/2),2,abs_tol=1e-12)
print(json.dumps({"research_positions":173,"Euclidean_analytic_references":20,"relations_legacy":x["origin_relationship_count"],"Raphael_metric":"UNPROVED","mint":"BLOCKED","result":"PASS"},indent=2))
