#!/usr/bin/env python3
"""Build one source-linked, offline CGX engineering review lens. No authorisation or simulation."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

SOURCE = Path(__file__).resolve().parents[2]
PRINT = Path(__file__).resolve().parent
GROUPS = ("component", "technology", "product", "printer", "twin")
TOURS = (
    {"id": "diode-to-device", "name": "Diode → integrated devices", "steps": (
        ("component","CGA-D-001"), ("component","CGA-R-001"), ("component","CGA-C-001"),
        ("component","CGA-L-001"), ("component","CGA-IC-055"), ("component","CGA-E-008"),
        ("component","CGA-RF-041"), ("product","FW-01"), ("product","FU-01"))},
    {"id": "printceptor-first-article", "name": "PrintCeptor → Butter Bot", "steps": (
        ("printer","CGX-PC-FAM-PC0"), ("product","FO-01"), ("printer","CGX-PC-FAM-PCA"),
        ("printer","CGX-PC-FAM-EVD"), ("printer","CGX-PC-FAM-PRO"), ("printer","CGX-PC-FAM-MIC"))},
    {"id": "earth-to-intersol", "name": "Solar Hull → Mark → Luke → InterSol", "steps": (
        ("component","CGA-E-017"), ("product","FR-04"), ("twin","TWIN-SOLAR-HULL"),
        ("product","FR-01"), ("product","FR-02"), ("twin","TWIN-MARK-III"),
        ("product","FR-03"), ("product","FR-07"), ("product","FR-08"),
        ("twin","TWIN-LUKE-FAMILY"), ("twin","TWIN-INTERSOL"))},
    {"id": "circular-civil", "name": "Recovery → Eco → civil systems", "steps": (
        ("printer","CGX-PC-FAM-REC"), ("twin","TWIN-SECOND-CYCLE"),
        ("twin","TWIN-EMBEDDED-BIO-BLOCKS"), ("twin","TWIN-WATCHTOWER"),
        ("twin","TWIN-M1-ELEVATED-BYPASS"))},
)
TWINS = (
    ("solar_hull", "Solar Hull"),
    ("free_flow_batteries", "Free Flow Batteries"),
    ("free_flow_capacitors", "Free Flow Capacitors"),
    ("free_flow_solenoid_stack", "Free Flow Solenoid Stack"),
    ("rfs_emff", "RFS & EMFF Test Sandbox"),
    ("mark_1p", "Mark 1P"),
    ("mark_i", "Mark I Terrestrial Test Chamber"),
    ("mark_iii", "Mark III"),
    ("luke_family", "Luke / Luke II / Apostle"),
    ("maglev_luke_iv", "Mag-Lev / Luke IV"),
    ("embedded_bio_blocks", "Embedded / Bio-Blocks"),
    ("second_cycle", "Second Cycle"),
    ("watchtower", "WatchTower Living Twin"),
    ("intersol", "InterSol Planned Facility"),
    ("m1_elevated_bypass", "M1 Elevated Bypass"),
    ("romer_spaceport", "Römer Spaceport"),
)
def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def githead(path: Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()

def entry(kind: str, object_id: str, name: str, domain: str, description: str,
          source_path: str, source_repo: str, source_sha: str,
          evidence: str, hold: str, view: str = "", details: dict | None = None) -> dict:
    return dict(kind=kind, id=str(object_id), name=str(name), domain=str(domain),
                description=str(description)[:560], source_path=source_path,
                source_url="https://github.com/" + source_repo + "/blob/" +
                           source_sha + "/" + quote(source_path, safe="/"),
                evidence=evidence, hold=hold, view=view, details=details or {})

def compile_data(light_root: Path, print_root: Path):
    sources = {
        "atlas": light_root / "cgx/component_atlas/component_geometry_atlas_v0_1.json",
        "pt": light_root / "docs/engineering/CGX_PRINTABLE_TECH_CATALOGUE_INDEX_2026-10-07.md",
        "twins": light_root / "docs/digital-twin/DIGITAL_TWIN_ATRIUM_2026-09-11.md",
        "products": print_root / "CGX/PrintSpace/CROSS_GREX_PRODUCT_ATLAS_v0_5.json",
        "printers": print_root / "CGX/PrintSpace/PRINTCEPTOR_FAMILY_PARAMETRIC_REGISTRY_v0_1.json",
    }
    for key, path in sources.items():
        if not path.is_file(): raise FileNotFoundError(f"{key}: {path}")
    lshead, pshead = githead(light_root), githead(print_root)
    data: list[dict] = []
    atlas = json.loads(sources["atlas"].read_text(encoding="utf-8"))
    for row in atlas["records"]:
        data.append(entry("component", row["ID"], row["Component Archetype"],
            row.get("Domain", ""), row.get("Primary Function",""),
            "cgx/component_atlas/component_geometry_atlas_v0_1.json",
            "achillesromer-coder/LightSpeed", lshead,
            row.get("Evidence State", "UNKNOWN"),
            "Archetype only; exact SKU/lot/dimensions, material process and measured qualification required.",
            details={"geometry":row.get("Baseline Geometry",""),
                     "materials":row.get("Typical Material Stack",""),
                     "physics":row.get("Baseline Model / Equation",""),
                     "tests":row.get("Acceptance Tests",""),
                     "interfaces":row.get("Ports / Interfaces","")}))
    pt_lines = sources["pt"].read_text(encoding="utf-8").splitlines()
    pt_rows = []
    for line in pt_lines:
        if not line.lstrip().startswith("| PT-"): continue
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) < 9 or not re.fullmatch(r"PT-\d{3}", cells[0]): continue
        pt_rows.append(cells)
        data.append(entry("technology", cells[0], cells[2], cells[1], cells[3],
            "docs/engineering/CGX_PRINTABLE_TECH_CATALOGUE_INDEX_2026-10-07.md",
            "achillesromer-coder/LightSpeed", lshead, cells[7],
            "Technology catalogue candidate; measured instantiation / installed process availability not implied.",
            details={"compute":cells[4], "DIY":cells[5], "horizon":cells[6], "route":cells[8]}))
    products = json.loads(sources["products"].read_text(encoding="utf-8"))
    for row in products["products"]:
        data.append(entry("product", row["product_id"], row["name"],
            row.get("category_title") or row.get("category",""),
            row.get("functional_contract",""), "CGX/PrintSpace/CROSS_GREX_PRODUCT_ATLAS_v0_5.json",
            "NCNBOUWER/Raphael", pshead, "CANDIDATE_ONLY",
            "Product decomposition and process stages are proposal-only; no qualified finished article.",
            details={"grex":row.get("primary_grex",""),"contributors":row.get("contributor_grex",[])}))
    printers = json.loads(sources["printers"].read_text(encoding="utf-8"))
    for row in printers["family"]:
        data.append(entry("printer", row["id"], row["name"],
            row.get("kind",""), ", ".join(row.get("use_cases", [])),
            "CGX/PrintSpace/PRINTCEPTOR_FAMILY_PARAMETRIC_REGISTRY_v0_1.json",
            "NCNBOUWER/Raphael", pshead, row.get("characterization","CONCEPT"),
            "Illustrative mm envelope, no validated reach, process, certified chamber or actual installed machine.",
            details={"envelope_mm":row.get("outer_envelope_mm"),"inner_mm":row.get("inner_envelope_mm"),
                     "features":row.get("features_candidate",[]),"physically_qualified":False}))
    for slug, label in TWINS:
        asset = light_root / "assets/type1-svg" / slug / "T1-00.svg"
        if not asset.is_file(): raise FileNotFoundError(f"twin thumbnail missing {asset}")
        data.append(entry("twin", "TWIN-"+slug.upper().replace("_","-"), label, "System digital twin",
            "Engineering visualization with unresolved physical, material and deployment evidence.",
            "docs/digital-twin/DIGITAL_TWIN_ATRIUM_2026-09-11.md",
            "achillesromer-coder/LightSpeed", lshead, "REVIEW_PREPUBLISH",
            "SVG is design representation; not exact as-built CAD, certified simulation or validated performance.",
            view="assets/"+slug+".svg",
            details={"svg_source":"assets/type1-svg/"+slug+"/T1-00.svg","svg_sha256":sha(asset)}))
    counts = {k:sum(row["kind"]==k for row in data) for k in GROUPS}
    expect = {"component":411,"technology":81,"product":80,"printer":17,"twin":16}
    if counts != expect: raise ValueError(f"Drift/partial source import: {counts}, expected {expect}")
    keys=[(row["kind"],row["id"]) for row in data]
    if len(keys)!=len(set(keys)): raise ValueError("Duplicate within namespace")
    present = set(keys)
    for tour in TOURS:
        for kind, object_id in tour["steps"]:
            if (kind, object_id) not in present:
                raise ValueError(f"Unbound review route {tour['id']}: {kind}:{object_id}")
    meta = dict(schema="CGX-REVIEW-LENS-OFFLINE/0.1", state="READ_ONLY_DERIVED_NOT_CANON",
        created_by="cgx_review_lens_compiler.py", counts=counts,
        source_heads={"LightSpeed":lshead,"PrintSpace":pshead},
        source_sha256={key:sha(path) for key,path in sources.items()},
        claims="No source CAD changed; concept SVG does not imply physical accuracy; no owner approvals are written.",
        operator_review="Local shortlist is a draft selection only; authority and DBR acceptance require the existing CGX owner.")
    return meta,data

HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; connect-src 'none'">
<title>CGX — Engineering Object Review</title>
<style>
:root{color-scheme:dark;--bg:#091116;--ink:#eaf2f3;--quiet:#9aaeb4;--line:#2b4048;--panel:#101e25;--orange:#ff873c;--blue:#83bff0}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at top left,#20313a,#091116 47%);color:var(--ink);font:14px/1.5 Segoe UI,system-ui,sans-serif}
header{padding:25px 30px;border-bottom:1px solid var(--line);display:flex;gap:18px;justify-content:space-between;align-items:center}h1{margin:0;font-size:29px;letter-spacing:.015em}h2{font-size:18px;margin:3px 0 13px}small,.muted{color:var(--quiet)}.eyebrow{font-size:10px;letter-spacing:.19em;color:var(--orange);font-weight:800}.pill{border:1px solid var(--line);border-radius:30px;padding:5px 12px;color:var(--quiet);display:inline-block}
main{display:grid;grid-template-columns:minmax(370px,40%) 1fr;max-height:calc(100vh - 108px);min-height:600px}.catalog{padding:20px;border-right:1px solid var(--line);overflow:auto}
.row{display:flex;gap:9px;align-items:center;flex-wrap:wrap}input,select,button,textarea{font:inherit;color:var(--ink);background:#0c181f;border:1px solid var(--line);padding:11px 12px;border-radius:9px}input{flex:1;min-width:170px}button{cursor:pointer}button:hover,button:focus-visible{border-color:var(--orange)}button.active{background:#3d2c23;border-color:var(--orange)}#types{margin:12px 0 16px}.objects{display:grid;grid-template-columns:repeat(auto-fill,minmax(205px,1fr));gap:10px}.item{border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:13px;text-align:left;min-height:120px}.item.selected{border:2px solid var(--orange);padding:12px}.item strong{display:block;font-size:14px;line-height:1.26;margin:8px 0}.item .id{font:11px Consolas,monospace;color:var(--orange)}
.inspect{padding:23px 26px;overflow:auto}.inspect h2{font-size:clamp(25px,3vw,40px);line-height:1.15}.preview{background:#e5edf0;border:1px solid #49616b;border-radius:12px;min-height:290px;max-height:52vh;display:flex;align-items:center;justify-content:center;overflow:hidden;color:#22333a}.preview img{width:100%;height:auto;max-height:52vh;object-fit:contain}.blank{font-size:14px;text-align:center;max-width:340px;padding:25px}
.fields{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:9px;margin:12px 0}.field{padding:11px 13px;border:1px solid var(--line);background:var(--panel);border-radius:9px;word-break:break-word}.field b{color:var(--orange);display:block;font-size:10px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:5px}
.section{border-top:1px solid var(--line);padding-top:13px;margin-top:16px}.notice{color:#f1c18b}.link{color:var(--blue);word-break:break-word}.status{font-size:11px;color:#f0bc8c}.low{font-size:12px}textarea{width:100%;min-height:105px;display:none}.actions{display:flex;gap:8px;flex-wrap:wrap;margin:15px 0}
@media(max-width:850px){main{display:block;max-height:none}.catalog,.inspect{overflow:visible}.catalog{border-right:0;border-bottom:1px solid var(--line)}header{display:block}.objects{max-height:380px;overflow:auto}.preview{min-height:200px}}
@media print{header,.catalog,.actions{display:none}main{display:block}.inspect{padding:0}.preview{max-height:none}.preview img{max-height:none}body{background:#fff;color:#111}.field{background:#fff;color:#111}}
</style></head><body>
<header><div><div class="eyebrow">COGNIGREX / TECHNICAL REVIEW</div><h1>CGX Object & Family Atlas</h1><small>Identity → source → geometry → environment → evidence → review · Not a production authorisation</small></div><div><span class="pill" id="allCount"></span><span class="pill">Source-bound / local-only</span></div></header>
<main><section class="catalog"><div class="row"><input id="search" aria-label="Search CGX objects" placeholder="Find diode, capacitor, PrintCeptor, Mark III, Luke…" autofocus><select id="family" aria-label="Object family"><option value="">All families</option></select></div><div class="row" id="types"></div>
<div class="row"><select id="tour" aria-label="Guided source-linked review"><option value="">Guided review route…</option></select><button id="tourPrev" title="Previous verified source object">◀ Route</button><button id="tourNext" title="Next verified source object">Route ▶</button><small id="tourStep">Select a route to navigate its source records</small></div><div class="row"><small id="resultCount"></small><small id="shortlistCount"></small></div><div class="objects" id="items" aria-label="Object cards"></div></section>
<section class="inspect"><div class="eyebrow" id="cat">SOURCE-LINKED COMPONENT</div><h2 id="name">Select an object</h2><div class="row low"><span class="pill" id="key"></span><span class="pill" id="badge"></span></div><p class="muted" id="description"></p><div class="preview" id="preview"></div><div class="actions"><button id="add">Add to review shortlist</button><button id="export">Show draft shortlist</button><button id="prev">◀ Previous</button><button id="next">Next ▶</button></div><textarea id="exportBox" aria-label="Review shortlist draft"></textarea><div class="fields" id="fields"></div><div class="section"><div class="eyebrow">Evidence ceiling and release gates</div><p class="notice" id="hold"></p><p class="muted">This interface cannot approve objects, advance a DBR, claim measured geometry or command a physical printer. Use existing CGX owner/LightSpeed authority gates.</p></div><div class="section"><div class="eyebrow">Native source provenance</div><p id="source"></p><small id="hashes"></small></div></section></main>
<script id="data" type="application/json">__PAYLOAD__</script>
<script>
"use strict";
const payload=JSON.parse(document.getElementById("data").textContent),items=payload.items,routes=payload.routes||[];
const $=id=>document.getElementById(id), chosen=new Set();
let visible=items,selected=0,kind="all",activeRoute=null,routeIndex=0;
for(const route of routes){const option=document.createElement("option");option.value=route.id;option.textContent=route.name+" ("+route.steps.length+" steps)";document.getElementById("tour").appendChild(option)}
function jumpRoute(target){
 if(!activeRoute)return;
 routeIndex=(target+activeRoute.steps.length)%activeRoute.steps.length;
 const step=activeRoute.steps[routeIndex];
 kind=step.kind;document.getElementById("search").value="";document.getElementById("family").value="";
 update();
 const index=visible.findIndex(item=>item.kind===step.kind&&item.id===step.id);
 if(index<0){text("tourStep","Source unavailable — route held");return}
 selected=index;render();
 text("tourStep",(routeIndex+1)+"/"+activeRoute.steps.length+" · "+step.id+" · source review only");
}
document.getElementById("tour").addEventListener("change",event=>{
 activeRoute=routes.find(route=>route.id===event.target.value)||null;
 if(activeRoute)jumpRoute(0);else text("tourStep","Select a route to navigate its source records");
});
document.getElementById("tourPrev").addEventListener("click",()=>jumpRoute(routeIndex-1));
document.getElementById("tourNext").addEventListener("click",()=>jumpRoute(routeIndex+1));
const types=[["all","All"],["component","Components"],["technology","Technologies"],["product","Products"],["printer","PrintCeptor"],["twin","System twins"]];
for(const [id,label] of types){let b=document.createElement("button");b.textContent=label;b.onclick=()=>{kind=id;update()};b.dataset.kind=id;$("types").appendChild(b)}
$("allCount").textContent=items.length+" records · 5 namespaces";
const allDomain=[...new Set(items.map(x=>x.domain))].sort();
for(const d of allDomain){let o=document.createElement("option");o.value=d;o.textContent=d;$("family").appendChild(o)}
$("search").addEventListener("input",update);$("family").addEventListener("change",update);
function text(id,value){$(id).textContent=String(value==null?"":value)}
function render(){
 $("items").replaceChildren();
 const frag=document.createDocumentFragment();
 for(let i=0;i<visible.length;i++){const v=visible[i];const b=document.createElement("button");b.className="item"+(selected===i?" selected":"");
 const k=document.createElement("span");k.className="id";k.textContent=v.id;
 const title=document.createElement("strong");title.textContent=v.name;
 const sub=document.createElement("small");sub.textContent=v.domain;
 b.append(k,title,sub);b.onclick=()=>{selected=i;render();inspect()};frag.append(b)}
 $("items").append(frag);text("resultCount",visible.length+" matching");text("shortlistCount",chosen.size+" shortlisted");
 inspect();
}
function update(){
 const q=$("search").value.toLowerCase(),family=$("family").value;
 visible=items.filter(v=>(kind==="all"||v.kind===kind)&&(!family||v.domain===family)
   &&(v.id+" "+v.name+" "+v.domain+" "+v.description+" "+JSON.stringify(v.details)).toLowerCase().includes(q));
 selected=0;for(const b of $("types").children)b.classList.toggle("active",b.dataset.kind===kind);render();
}
function inspect(){
 const v=visible[selected];$("fields").replaceChildren();$("preview").replaceChildren();
 if(!v){text("name","No matching records");text("description","Change search or filters");text("key","");text("badge","");text("cat","");text("hold","");text("source","");return}
 text("name",v.name);text("key",v.id);text("cat",v.kind.toUpperCase()+" / "+v.domain);
 text("badge",v.evidence);text("description",v.description);text("hold",v.hold);
 $("add").textContent=chosen.has(v.kind+":"+v.id)?"Remove from shortlist":"Add to review shortlist";
 if(v.view){const img=document.createElement("img");img.src=v.view;img.alt=v.name+" — inherited technical concept SVG";$("preview").append(img)}
 else{const p=document.createElement("div");p.className="blank";p.textContent="No verified graphic is linked to this source record. Native CAD/4D view or measured instance geometry remains a source-owner gate."; $("preview").append(p)}
 const obj={Identity:v.id,Category:v.kind,Source: v.source_path,"Evidence tier":v.evidence,...v.details};
 for(const [k,value] of Object.entries(obj)){if(value===undefined||value===null||value==="")continue;
 const el=document.createElement("div"),title=document.createElement("b"),body=document.createElement("span");
 el.className="field";title.textContent=k;body.textContent=typeof value==="object"?JSON.stringify(value):String(value);el.append(title,body);$("fields").append(el)}
 $("source").replaceChildren();const a=document.createElement("a");a.textContent=v.source_path;a.href=v.source_url;a.target="_blank";a.rel="noopener noreferrer";a.className="link";$("source").append(a);
 text("hashes","Source sha256: "+(payload.meta.source_sha256[v.kind]||"See manifest.json")+" · source HEAD: "+(v.source_url.split("/")[5]||""));
}
$("add").onclick=()=>{const v=visible[selected];if(!v)return;const key=v.kind+":"+v.id;if(chosen.has(key))chosen.delete(key);else chosen.add(key);inspect();text("shortlistCount",chosen.size+" shortlisted")};
$("export").onclick=()=>{const list=items.filter(x=>chosen.has(x.kind+":"+x.id)).map(x=>({id:x.id,kind:x.kind,name:x.name,source:x.source_url,request:"REVIEW_ONLY",evidence:x.evidence,hold:x.hold}));const box=$("exportBox");box.style.display="block";box.value=JSON.stringify({schema:"CGX_REVIEW_SELECTION_DRAFT/0.1",state:"NOT_APPROVED",source_heads:payload.meta.source_heads,items:list},null,2);box.focus();box.select()};
$("prev").onclick=()=>{if(visible.length){selected=(selected-1+visible.length)%visible.length;render()}};
$("next").onclick=()=>{if(visible.length){selected=(selected+1)%visible.length;render()}};
document.addEventListener("keydown",e=>{if(e.target.tagName==="INPUT"||e.target.tagName==="TEXTAREA")return;if(e.key==="ArrowRight")$("next").click();else if(e.key==="ArrowLeft")$("prev").click()});
update();
</script></body></html>'''

def build(light_root: Path, print_root: Path, output: Path, check: bool):
    meta, rows=compile_data(light_root,print_root)
    if check:
        print(json.dumps({"status":"SOURCE_CHECK_PASS","counts":meta["counts"],"source_heads":meta["source_heads"]},indent=2))
        return
    output.mkdir(parents=True,exist_ok=True)
    assets=output/"assets";assets.mkdir(exist_ok=True)
    files={}
    for slug,_label in TWINS:
        source=light_root/"assets/type1-svg"/slug/"T1-00.svg"
        blob=source.read_text(encoding="utf-8")
        if re.search(r"<script\b|<foreignObject\b|\bonload\s*=|\bonerror\s*=|javascript:",blob,re.I):
            raise ValueError(f"Unsafe SVG source, inspect owner: {source}")
        target=assets/(slug+".svg");target.write_text(blob,encoding="utf-8");files[str(target.relative_to(output))]=sha(target)
    safe_json=json.dumps(dict(meta=meta,items=rows,routes=[{"id":t["id"],"name":t["name"],"steps":[{"kind":k,"id":i} for k,i in t["steps"]]} for t in TOURS]),ensure_ascii=False,separators=(",",":")).replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    viewer=output/"index.html";viewer.write_text(HTML.replace("__PAYLOAD__",safe_json),encoding="utf-8")
    receipt=dict(meta,artifact="OFFLINE_LOCAL_REVIEW_ONLY",item_total=len(rows),files={**files,"index.html":sha(viewer)},safety="Local file only, no served dist/public CYC upload, approval, machine or root write.",target=str(output))
    (output/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"BUILT_OFFLINE_REVIEW","counts":meta["counts"],"path":str(viewer),"assets":len(files),"receipt":str(output/"receipt.json")},indent=2))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--lightspeed-root",type=Path,required=True)
    parser.add_argument("--printspace-root",type=Path,default=SOURCE)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--check",action="store_true")
    a=parser.parse_args()
    if not a.check and a.output is None:parser.error("--output required unless --check")
    build(a.lightspeed_root,a.printspace_root,a.output,a.check)

if __name__=="__main__":main()
