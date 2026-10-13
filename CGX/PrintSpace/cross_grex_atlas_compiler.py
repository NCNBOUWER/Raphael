"""Read-only product dual-compile view. Planning records, not machine instructions."""
import argparse
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def load(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
def product(identifier, mode="both"):
    atlas=load("CROSS_GREX_PRODUCT_ATLAS_v0_5.json")
    matches=[x for x in atlas["products"] if x["product_id"]==identifier]
    if len(matches)!=1: raise ValueError("Unknown product ID")
    x=matches[0]
    if mode not in ("top","bottom","both"): raise ValueError("Invalid mode")
    ans={"id":identifier,"title":x["name"],"owner":x["primary_grex"],
         "status":"CANDIDATE_ONLY","production_approved":False}
    if mode in ("top","both"):
        ans["top_down"]={"functional_contract":x["functional_contract"],
                         "technology_ids":x["component_tech_refs"],
                         "components":x["component_functions"],
                         "hybrid_inserts":x["top_down"]["hybrid_required"],
                         "acceptance":x["top_down"]["system_acceptance_tests"],
                         "unresolved":x["top_down"]["critical_qualification_gaps"]}
    if mode in ("bottom","both"):
        ans["bottom_up"]={"material_refs":x["bottom_up"]["material_seed_refs"],
                          "opportunities":x["bottom_up"]["environment_opportunity_ids"],
                          "stages":x["bottom_up"]["stages"],
                          "physical_recipe_verified":False}
    return ans
def compare(a,b):
    x=product(a,"top")["top_down"];y=product(b,"top")["top_down"]
    p,q=set(x["technology_ids"]),set(y["technology_ids"])
    return {"a":a,"b":b,"shared":sorted(p&q),"a_only":sorted(p-q),
            "b_only":sorted(q-p),"physical_interchangeability_verified":False}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--product",default="FO-01")
    p.add_argument("--mode",choices=["top","bottom","both"],default="both")
    p.add_argument("--compare",nargs=2)
    a=p.parse_args()
    print(json.dumps(compare(*a.compare) if a.compare else product(a.product,a.mode),indent=2))
if __name__=="__main__": main()
