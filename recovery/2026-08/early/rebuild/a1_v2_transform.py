# Session f00a0b22 turn 27: transforms build_a1_frame.py -> build_a1_frame_v2.py (verbatim logic)
import re
src = open("build_a1_frame.py", encoding="utf-8").read()

src = src.replace("BASE = \"https://guide.michelin.com/us/en\"",
 "from resolution_map import RES, F0_NOTES\nBASE = \"https://guide.michelin.com/us/en\"")

old = '''# F1 verdict from the guide's own city label. PROVISIONAL — F0/F1 proper needs address resolution.
OUT_LABELS = {"Gentofte": "Gentofte Kommune", "Hellerup": "Gentofte Kommune",
              "Holte": "Rudersdal Kommune", "Malmo": "Malmö, Sweden"}

ROWS = []
for lst, page in ((P1, 1), (P2, 2)):
    for (n, city, tier, path) in lst:
        out = OUT_LABELS.get(city)
        ROWS.append(dict(name=n, city=city, tier=tier, url=BASE + path, page=page,
                         excl="outside_boundary" if out else "",
                         kommune=out if out else "TO RESOLVE"))'''
new = '''# F1 from the RESOLVED ADDRESS. Kommune derived from the Danish postcode, not the guide's label.
def kommune_of(addr):
    m = re.search(r"\\b(\\d{4})\\s+(\\S+)", addr)
    code, town = int(m.group(1)), m.group(2)
    if town.startswith("Frederiksberg"):
        return "Frederiksberg Kommune", True
    if town.startswith("K\\u00f8benhavn"):
        return "K\\u00f8benhavns Kommune", True
    if town in ("Gentofte", "Hellerup"):
        return "Gentofte Kommune", False
    if town.startswith("S\\u00f8ller\\u00f8d") or town == "Holte":
        return "Rudersdal Kommune", False
    return f"UNMAPPED {code} {town}", False

ROWS = []
for lst, page in ((P1, 1), (P2, 2)):
    for (n, city, tier, path) in lst:
        if city == "Malmo":
            addr, pid, kom, inside = "Malm\\u00f6, Sweden", "not resolved", "Malm\\u00f6 kommun, Sweden", False
        else:
            addr, pid = RES[n]
            kom, inside = kommune_of(addr)
        ROWS.append(dict(name=n, city=city, tier=tier, url=BASE + path, page=page,
                         excl="" if inside else "outside_boundary",
                         kommune=kom, address=addr, pid=pid))'''
assert old in src
src = src.replace(old, new)
src = "import re\n" + src

src = src.replace('''    vals = [d["name"], d["city"], "TRUE", d["tier"], d["kommune"], "TO RESOLVE", "TO RESOLVE", "",''',
                  '''    vals = [d["name"], d["city"], "TRUE", d["tier"], d["kommune"], d["address"], d["pid"], "",''')

src = src.replace('''    if d["name"] == "Marchal":
        note = "venue_type = hotel_restaurant (Hotel d'Angleterre). Qualifies on A1 in its own right per D-028."
    if d["name"] == "formel B":
        note = "Address is 1800 Frederiksberg C — Frederiksberg Kommune, in scope. Guide labels it 'Copenhagen'."''',
'''    if d["name"] in F0_NOTES:
        note = F0_NOTES[d["name"]]''')

src = src.replace('("Provisionally OUT on city label — outside_boundary"', '("Fail F1 — outside_boundary (resolved address)"')
src = src.replace('("Provisionally IN, pending address resolution"', '("Pass F1 — Københavns + Frederiksberg Kommune"')
src = src.replace('''     ("  of which Malmö, Sweden", f'=COUNTIF(B5:B{last},"Malmo")'),''',
'''     ("  of which Malmö, Sweden", f'=COUNTIF(B5:B{last},"Malmo")'),
     ("Pass F1 — of which Københavns Kommune", f'=COUNTIF(E5:E{last},"Københavns Kommune")'),
     ("Pass F1 — of which Frederiksberg Kommune", f'=COUNTIF(E5:E{last},"Frederiksberg Kommune")'),
     ("F0 resolved to exactly one venue (Danish rows)", f'=72-COUNTIF(G5:G{last},"not resolved")+COUNTIF(G5:G{last},"not resolved")-11'),''')

src = src.replace('"F1 verdicts below are PROVISIONAL, taken from the guide\'s own city label, not from a resolved address."',
                  '"F1 verdicts are taken from RESOLVED ADDRESSES (Google Places, 2026-07-30), not from the guide\'s city label."')

# second patch in the same turn: F0 formula correction
bad = '''     ("F0 resolved to exactly one venue (Danish rows)", f'=72-COUNTIF(G5:G{last},"not resolved")+COUNTIF(G5:G{last},"not resolved")-11'),'''
good = '''     ("F0 resolved to exactly one venue (address + place_id)", f'=COUNTA(G5:G{last})-COUNTIF(G5:G{last},"not resolved")'),
     ("F0 not resolved (Malmö — excluded on country, not resolved)", f'=COUNTIF(G5:G{last},"not resolved")'),'''
assert bad in src
src = src.replace(bad, good)
open("build_a1_frame_v2.py","w",encoding="utf-8").write(src)
print("written")
