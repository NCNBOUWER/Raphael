#!/usr/bin/env python3
"""Unsigned CGX research composite: a reference-only, never-mint preview."""
import argparse,json,pathlib,hashlib
source=pathlib.Path(__file__).resolve().parent/"showcase_data.json"
def build(slots):
 d=json.loads(source.read_text()); lookup={e["slot"]:e for e in d["items"]}
 if not slots or len(slots)>8 or any(x not in lookup for x in slots):raise ValueError("Choose 1–8 slots in range 1..173")
 selected=[lookup[j] for j in dict.fromkeys(slots)]
 return {"type":"raphael.cgx.composite.preview","version":"0.2.0","state":"UNSIGNED_NONMINTABLE",
 "roles":[{"slot":e["slot"],"role_id":e["id"],"canonical_geometry_id":e["canonical"],"physical_role":"HYPOTHESIS"} for e in selected],
 "unique_canonical_geometry_ids":list(dict.fromkeys(e["canonical"] for e in selected if e["canonical"])),
 "position_174":{"empty":True,"object_id":None},"rights":"UNASSESSED","signatures":[],"receipts":[],"minting_permitted":False}
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("slots",nargs="+",type=int);ap.add_argument("--out");args=ap.parse_args()
 s=json.dumps(build(args.slots),indent=2);pathlib.Path(args.out).write_text(s) if args.out else print(s)
