import re, unicodedata
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from resolution_map import RES as A1RES
from a2_res import A2RES, UNRESOLVED

A="Arial"
HDR=Font(name=A,bold=True,color="FFFFFF",size=10); HF=PatternFill("solid",fgColor="333333")
BODY=Font(name=A,size=10); BOLD=Font(name=A,size=10,bold=True)
RED=Font(name=A,size=10,color="C00000",bold=True); GREY=Font(name=A,size=10,color="808080",italic=True)
TITLE=Font(name=A,size=13,bold=True); YELL=PatternFill("solid",fgColor="FFF2CC")
THIN=Border(bottom=Side(style="thin",color="D9D9D9"))

def norm(s):
    s=unicodedata.normalize('NFKD',s.lower())
    s=''.join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r'^(restaurant|restaurang)\s+','',s)
    return re.sub(r'[^a-z0-9]','',s)

# manual A1<->A2 name bridges (near-misses the normaliser cannot safely catch)
BRIDGE={"kadeaukobenhavn":"Kadeau Copenhagen","akme":"akmē","aoc":"a|o|c","no2":"no.2",
        "restaurantaoc":"a|o|c","restaurantlevi":"Levi","restaurantvie":"Restaurant VIE",
        "restaurantmark":"Mark","kodbyensfiskebar":"Kødbyens Fiskebar","aterre":"à terre",
        "kiinkiin":"Kiin Kiin","sanktannae":"Sankt Annæ","paesano":"Paesàno"}
a1n={norm(k):k for k in A1RES}

src=load_workbook('/mnt/user-data/outputs/cph-route-a2-candidates.xlsx')['wg_a2_candidates']
rows=[]
for r in range(5,205):
    n=src.cell(r,1).value
    if n: rows.append((n,src.cell(r,2).value,src.cell(r,3).value,src.cell(r,4).value,src.cell(r,16).value))

def kommune(addr):
    m=re.search(r"\b(\d{4})\s+(\S+)",addr)
    if not m: return "UNRESOLVED",False
    town=m.group(2)
    if town.startswith("Frederiksberg"): return "Frederiksberg Kommune",True
    if town.startswith("København"): return "Københavns Kommune",True
    return f"UNMAPPED {town}",False

out=[]
for name,addr_raw,tier,flag,note in rows:
    resolved=pid=""; kom="not resolved"; inside=False; f0=note or ""
    if flag=="likely IN — resolve":
        key=norm(name)
        if name in A2RES:
            resolved,pid,n2=A2RES[name]; f0=n2 or f0
        elif key in a1n:
            resolved,pid=A1RES[a1n[key]]
        elif key in BRIDGE and BRIDGE[key] in A1RES:
            resolved,pid=A1RES[BRIDGE[key]]
            f0=(f0+" Name bridged to A1 entry '%s' — guides use different spellings for one venue."%BRIDGE[key]).strip()
        elif name in UNRESOLVED:
            f0=UNRESOLVED[name]
        if resolved: kom,inside=kommune(resolved)
    else:
        kom="outside — see provisional_area" if flag=="likely OUTSIDE" else "not resolved"
        if name in UNRESOLVED: f0=UNRESOLVED[name]
    excl="" if inside else ("outside_boundary" if flag=="likely OUTSIDE" else ("unresolved" if not resolved else ""))
    out.append(dict(n=name,raw=addr_raw,t=tier,fl=flag,res=resolved,pid=pid,kom=kom,ex=excl,note=f0))

need=[d for d in out if d["fl"]=="likely IN — resolve" and not d["res"]]
print("provisionally IN unresolved:",len(need))
for d in need: print("   -",d["n"])

wb=Workbook(); ws=wb.active; ws.title="cph_route_a2_frame"
ws["A1"]="COPENHAGEN — ROUTE A2 FRAME (White Guide Denmark)"; ws["A1"].font=TITLE
ws["A2"]=("Route A2 only. F1 applied to RESOLVED ADDRESSES for every candidate the guide placed in the Copenhagen region. "
          "Venues the guide placed elsewhere were not resolved — they are excluded on the guide's own locality, which is weaker evidence.")
ws["A2"].font=GREY
COLS=[("venue_name",28),("route_a2_tier",15),("kommune",22),("address_resolved",40),("google_place_id",30),
      ("address_at_source",42),("route_a1",9),("in_cohort",10),("excluded_reason",17),
      ("frame_date",11),("source_url",46),("observed_at",12),("retrieved_at",12),("added_by",10),("f0_notes",64)]
r=4
for i,(n,w) in enumerate(COLS,start=1):
    c=ws.cell(row=r,column=i,value=n); c.font=HDR; c.fill=HF
    c.alignment=Alignment(vertical="center",wrap_text=True); ws.column_dimensions[get_column_letter(i)].width=w
ws.row_dimensions[r].height=30; ws.freeze_panes="B5"
SRC="https://whiteguide.com/dk/da/search?query=&type=restaurant&execute=true"
r=5
for d in out:
    vals=[d["n"],d["t"],d["kom"],d["res"],d["pid"],d["raw"],"","FALSE",d["ex"],
          "2026-07-28",SRC,"2026-07-30","2026-07-30","claude",d["note"]]
    for i,v in enumerate(vals,start=1):
        c=ws.cell(row=r,column=i,value=v); c.font=BODY; c.border=THIN
        c.alignment=Alignment(vertical="top",wrap_text=(i in (6,11,15)))
    if d["ex"]=="unresolved": ws.cell(row=r,column=9).font=RED; ws.cell(row=r,column=15).font=RED
    elif d["ex"]: ws.cell(row=r,column=9).font=GREY
    if "CONFLICT" in d["note"] or "MISMATCH" in d["note"]: ws.cell(row=r,column=15).font=RED
    r+=1
last=r-1
r+=1
ws.cell(row=r,column=1,value="COUNTS — every one states its denominator").font=BOLD; r+=1
S=[("A2 listing rows (Anarki appears twice)",f'=COUNTA(A5:A{last})'),
   ("Unique venues",f'=COUNTA(A5:A{last})-1'),
   ("PASS F1 — resolved into Københavns or Frederiksberg Kommune",f'=COUNTIF(I5:I{last},"")'),
   ("  of which Københavns Kommune",f'=COUNTIF(C5:C{last},"Københavns Kommune")'),
   ("  of which Frederiksberg Kommune",f'=COUNTIF(C5:C{last},"Frederiksberg Kommune")'),
   ("Excluded — outside boundary on the guide's own locality",f'=COUNTIF(I5:I{last},"outside_boundary")'),
   ("F0 UNRESOLVED — no verdict, kept visible",f'=COUNTIF(I5:I{last},"unresolved")')]
for lab,f in S:
    ws.cell(row=r,column=1,value=lab).font=BODY
    c=ws.cell(row=r,column=2,value=f); c.font=BOLD; c.fill=YELL
    r+=1
wb.save('/mnt/user-data/outputs/cph-route-a2-frame.xlsx')
print("saved")
