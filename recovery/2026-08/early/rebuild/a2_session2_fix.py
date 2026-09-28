# Session 1d9082f0 turn 5 — fix_a2.py plus the in-turn COUNTIFS patch (verbatim logic). Usage: python a2_session2_fix.py IN OUT
import sys, openpyxl
from copy import copy
SRC, OUT = sys.argv[1], sys.argv[2]
wb=openpyxl.load_workbook(SRC)
ws=wb['cph_route_a2_frame']
def rowof(name):
    for r in range(5,205):
        if ws.cell(r,1).value==name: return r
    raise SystemExit('not found: '+name)
r=rowof('Kiin Kiin Tok Tok')
ws.cell(r,3).value='Københavns Kommune'
ws.cell(r,4).value='Vesterbrogade 55, 1620 København'
ws.cell(r,9).value='not_trading'
ws.cell(r,15).value=(
 "F0 RESOLVED 2026-08-01 by operator (Google Maps): venue confirmed at the guide's stated address, "
 "Vesterbrogade 55, 1620 København. The earlier Places match ('Kiin Kiin Bao Bao', Vesterbrogade 96) "
 "was correctly rejected. F1 PASS on that address. F4 FAIL — the listing shows PERMANENTLY CLOSED. "
 "DATING CAVEAT: the closure was observed 2026-08-01, four days AFTER frame date 2026-07-28, and Google "
 "publishes no closure date — so the frame-date verdict is an INFERENCE, not an observation. It is not "
 "backfilled to the frame date. NO google_place_id: the Places API does not return permanently closed "
 "venues; re-tested 2026-08-01 and it returned the same wrong venue. Reclassified unresolved -> "
 "not_trading per D-040/D-041. Note: the columns observed_at/retrieved_at on this row date the WHITE "
 "GUIDE observation (2026-07-30), not this closure — one row cannot carry two observation dates, which "
 "is what venue_facts.valid_from exists for."
)
r=rowof('Toto')
ws.cell(r,15).value=(
 "Operator check 2026-08-01: venue no longer exists and its website is unreachable. No Google listing "
 "could be confirmed, so the guide's Amagerbrogade 145 remains UNVERIFIED — no address, no place_id, and "
 "therefore no F1 verdict is possible. The earlier Places match ('Restaurant Il Gambero Rosso', "
 "Amagerbrogade 166-168) was correctly rejected; re-tested 2026-08-01, Places still returns nothing at "
 "145. STAYS UNRESOLVED: closure is likely but unevidenced, and an unverified address cannot carry a "
 "boundary verdict. Contrast Kiin Kiin Tok Tok, where the operator confirmed the address (D-041)."
)
def style_from(src,dst):
    dst.font=copy(src.font); dst.alignment=copy(src.alignment); dst.fill=copy(src.fill)
ws.cell(207,1).value='No exclusion recorded — passes F1; F2/F4/F5 not yet applied'
ws.cell(211,1).value='F0 UNRESOLVED — no verdict, kept visible'
rows=[
 (212,'Excluded — not_trading (F4): passes F1, closed at frame date','=COUNTIF(I5:I203,"not_trading")'),
 (213,'CHECK — the four categories must equal the venue count above','=B207+B210+B211+B212'),
 (214,'Memo: venues passing F1, including any failing a later filter','=B207+B212'),
]
donor_lbl=ws.cell(211,1); donor_val=ws.cell(211,2)
for rr,label,formula in rows:
    c1=ws.cell(rr,1); c2=ws.cell(rr,2)
    c1.value=label; c2.value=formula
    style_from(donor_lbl,c1); style_from(donor_val,c2)
ws.cell(216,1).value=(
 "COUNT BLOCK REPAIR 2026-08-01: this file was previously saved without recalculating, so every formula "
 "above displayed blank. The formulas were correct — 199/109/101/8/75/15 — but because no number was "
 "visible, 12-decision-log.md recorded '110 of 199 pass F1 (101 Københavns, 9 Frederiksberg)' from "
 "memory. 110 was wrong: 110+75+15 = 200, one more venue than the file holds. Corrected to 109/8. "
 "Row 213 now fails loudly if the categories ever stop reconciling."
)
style_from(ws.cell(205,1), ws.cell(216,1))
lg=wb['legend_and_provenance']
for r in range(1,lg.max_row+1):
    if lg.cell(r,1).value=='F0 unresolved (15 rows)':
        lg.cell(r,1).value='F0 unresolved (14 rows, was 15)'
        lg.cell(r,2).value=(
          "Carry no F1 verdict and are kept visible rather than dropped. ONE HAS SINCE BEEN RESOLVED: "
          "Kiin Kiin Tok Tok was confirmed by the operator on 2026-08-01 at the guide's stated address, "
          "permanently closed, and reclassified not_trading (D-041). Toto stays unresolved — no listing "
          "could be confirmed at all. SYSTEMATIC HAZARD (D-040): Google Places does not return "
          "permanently closed venues, so a venue that shut before enumeration presents as a WRONG-VENUE "
          "match, never as a closure. 'unresolved' is therefore a mixture of genuine ambiguity and "
          "unrecognised closure, in every city, until each row is checked by hand. Both Copenhagen rows "
          "checked so far turned out to be closures — 2 of 2."
        )
        break
r=lg.max_row+2
lg.cell(r,1).value='Recalculation'
lg.cell(r,2).value=('This file must be recalculated before it is shared. openpyxl writes formulas without cached '
                    'values, so an un-recalculated copy shows an empty count block and invites exactly the '
                    'transcription error corrected on 2026-08-01.')
style_from(lg.cell(3,1),lg.cell(r,1)); style_from(lg.cell(3,2),lg.cell(r,2))
# in-turn patch after first recalc
ws.cell(208,2).value='=COUNTIFS(C5:C203,"Københavns Kommune",I5:I203,"")'
ws.cell(209,2).value='=COUNTIFS(C5:C203,"Frederiksberg Kommune",I5:I203,"")'
ws.cell(215,1).value='CHECK — the two kommune lines must equal the F1 pass count above'
ws.cell(215,2).value='=B208+B209'
for c,src in ((1,ws.cell(213,1)),(2,ws.cell(213,2))):
    d=ws.cell(215,c); d.font=copy(src.font); d.alignment=copy(src.alignment); d.fill=copy(src.fill)
wb.save(OUT); print('saved', OUT)
