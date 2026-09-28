# Session f00a0b22 turn 45 — adds legend_and_provenance sheet to the A2 frame (verbatim logic).
import sys
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
p=sys.argv[1]
wb=load_workbook(p)
lg=wb.create_sheet("legend_and_provenance")
lg.column_dimensions["A"].width=32; lg.column_dimensions["B"].width=104
lg["A1"]="How to read this file"; lg["A1"].font=Font(name="Arial",size=13,bold=True)
B=Font(name="Arial",size=10,bold=True); N=Font(name="Arial",size=10)
rows=[
("What this is","Route A2 for Copenhagen: the complete White Guide Denmark listing with F1 applied. One row per venue."),
("WHAT IT IS NOT — read this first","**This is not the frame and not a frame size.** Route A1 (MICHELIN) is a separate file and the two have NOT been unioned. "
 "They share an unknown number of venues. DO NOT add this file's count to A1's. F2, price, ownership, opened_on and Route B are all absent."),
("Source","whiteguide.com search, query=&type=restaurant&execute=true. Retrieved 2026-07-30 via Firecrawl, proxy=basic. "
 "No robots.txt exists on the domain (404); pages carry index,follow. Recorded in 06 §4."),
("Vintage (D-033)","White Guide publishes no dated edition — it updates weekly. Per D-033 the stored snapshot IS the edition, and "
 "retrieved_at 2026-07-30 is the vintage. frame_date remains 2026-07-28; for a rolling source the two dates are different objects."),
("Completeness (D-037)","The source states no result total, so D-032's stated-total check could not be used. Instead the five classification "
 "tiers were enumerated separately and reconciled to the full list: 28+67+81+21+3 = 203 rendered rows = the unfiltered listing exactly, "
 "with every entry carrying exactly one classification. LIMITATION: this proves the list is internally complete, NOT that the publisher's "
 "database is fully exposed. If White Guide's search silently omits a category, this method would not reveal it."),
("Tier scope (D-036)","All five tiers are kept. Recommended is 3 venues nationally — the Repsol swamping argument does not transfer."),
("THE 75 EXCLUSIONS ARE WEAKER THAN A1'S","Venues the guide placed outside the Copenhagen region were excluded on the guide's own locality "
 "string, NOT on a resolved address. Resolving 75 obviously-out-of-region venues was not judged worth the lookups. If any single one matters "
 "later, it is one lookup. A1's exclusions all rest on resolved addresses; these do not. Do not present them as equivalent."),
("Why the guide's locality is unsafe","White Guide uses 'København' as a REGION prefix. 'København / Hellerup', 'København / Gentofte' and "
 "'København / Klampenborg' are all OUTSIDE the boundary while containing the word København. ESSE is filed under 'Sjælland og øer / Köpenhamn'. "
 "Thirteen entries carry no locality at all. F1 was applied to resolved addresses only."),
("F0 unresolved (15 rows)","Carry no F1 verdict and are kept visible rather than dropped. Two are refusals worth knowing: "
 "Kiin Kiin Tok Tok (guide: Vesterbrogade 55; Places returned 'Kiin Kiin Bao Bao' at Vesterbrogade 96) and Toto (guide: Amagerbrogade 145; "
 "Places returned 'Il Gambero Rosso' at 166-168). Both are near-matches a fuzzy matcher would have accepted. Neither was."),
("Shared addresses are NOT duplicates","Bæst, Mirabelle and Brus all trade at Guldbergsgade 29. Grim and Tèrra both at Ryesgade 65. "
 "Esmée and Goldfinch both at Kongens Nytorv 8. Brasserie Barner and Donda SOLÈNE both at Århusgade 1. An address-based auto-merge would "
 "destroy all of these. Per 01, a visible duplicate beats an invisible bad merge."),
("Operator decisions in this file","D-035 Kappo Ando = Aotori = one venue (White Guide, MICHELIN slug and MICHELIN display name are three "
 "labels for it). D-038 Anarki recorded at Masters; the source rendered it at both Very Fine and Masters, and the superseded row is not carried. "
 "D-039 'Propaganda – next door' is one venue with Propaganda."),
("Known matcher hazard","Danish ø does not decompose under NFKD and was initially being deleted rather than folded to 'o', so "
 "'Kadeau København' failed to match A1's 'Kadeau Copenhagen'. Fixed for ø, æ, å. Any future cross-guide matching needs the same handling — "
 "this bug class produces a silent duplicate venue."),
("Blank cells","Not looked at. Never 'no'."),
("in_cohort","FALSE on every row. No cohort has been drawn; seed 20260728 is unused."),
]
r=3
for a,b in rows:
    lg.cell(row=r,column=1,value=a).font=B
    c=lg.cell(row=r,column=2,value=b); c.font=N
    c.alignment=Alignment(wrap_text=True,vertical="top"); lg.row_dimensions[r].height=46
    r+=1
wb.save(p)
print("legend added:", load_workbook(p).sheetnames)
