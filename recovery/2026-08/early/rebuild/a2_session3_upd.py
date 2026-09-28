# Session e2953710 turn 9 — upd_a2.py (verbatim logic). Usage: python a2_session3_upd.py IN OUT
import sys, openpyxl, shutil
from openpyxl.styles import Font
shutil.copy(sys.argv[1], sys.argv[2])
wb=openpyxl.load_workbook(sys.argv[2]); ws=wb["cph_route_a2_frame"]
ARI="Arial"
OP=("OPERATOR RESOLUTION 2026-08-01 (Google Maps, by hand). Venue confirmed TRADING at the address below, "
    "OUTSIDE the F1 boundary (Københavns + Frederiksberg Kommune). Reclassified unresolved -> outside_boundary. "
    "F0 now resolves to exactly one venue; no google_place_id was captured, because an exclusion row does not need one (D-040). "
    "Why it was unresolved: White Guide's address string for this row is TRUNCATED — street and number only, no locality — "
    "so F1 could not be applied on the guide's own text, and Places resolution returned a wrong Copenhagen match that was correctly rejected.")
UPD = {
 19 :("Annebergparken 50, 4500 Moseby, Denmark","outside — Denmark, not Capital Region",None),
 24 :("Gødstrupvej 62, 7400 Gødstrup, Denmark","outside — Denmark, not Capital Region",
      "ADDRESS DISCREPANCY: White Guide states Gødstrupvej 60; the operator found the venue at Gødstrupvej 62. Does not affect F1 — outside the boundary on either. Recorded because 75 A2 exclusions rest on the guide's own address text."),
 25 :("Vesterhavsvej 5a, 7770 Agger, Denmark","outside — Denmark, not Capital Region",None),
 30 :("Nørre Havnegade 25, 6400 Sønderborg, Denmark","outside — Denmark, not Capital Region",
      "ADDRESS DISCREPANCY: White Guide states Nørre Havnegade 23; the operator found the venue at Nørre Havnegade 25. Does not affect F1."),
 60 :("Lars Larsens Vej 1, 9640 Farsø, Denmark","outside — Denmark, not Capital Region",None),
 79 :("5 Gongin, Tórshavn 100, Faroe Islands","outside — FAROE ISLANDS",None),
 124:("3 Áarvegur, Tórshavn 100, Faroe Islands","outside — FAROE ISLANDS",
      "ADDRESS DISCREPANCY: White Guide states Heiðavegur 35; the operator found the venue at Áarvegur 3. A different street, so this is a possible relocation rather than a typo. Does not affect F1."),
 125:("12 Úti á Bakka, Sandavágur 360, Faroe Islands","outside — FAROE ISLANDS",None),
 133:("2 Oknarvegur, Tórshavn 100, Faroe Islands","outside — FAROE ISLANDS",None),
 157:("Midtskovvejen 1, 4871 Horbelev, Denmark","outside — Denmark, not Capital Region",None),
 165:("Toldbodvej 55, 4581 Rørvig, Denmark","outside — Denmark, not Capital Region",None),
 190:("6 Bringsnagøta, Tórshavn 100, Faroe Islands","outside — FAROE ISLANDS",None),
}
for r,(addr,kom,extra) in UPD.items():
    assert ws.cell(r,9).value=="unresolved", (r, ws.cell(r,9).value)
    ws.cell(r,3,kom); ws.cell(r,4,addr); ws.cell(r,9,"outside_boundary")
    ws.cell(r,15, OP + ((" " + extra) if extra else ""))
CLOSED=("OPERATOR CHECK 2026-08-01: the venue NO LONGER EXISTS. Reclassified unresolved -> not_trading. "
        "NO F1 VERDICT IS POSSIBLE: the address was never independently confirmed, and an unverified address cannot carry a boundary verdict "
        "— the same distinction drawn in D-041. So this row is excluded on F4 and is NOT counted in any F1 line. "
        "No google_place_id: Places does not return permanently closed venues (D-040). "
        "DATING CAVEAT: closure observed 2026-08-01, four days AFTER frame date 2026-07-28, and Google publishes no closure date, "
        "so the frame-date verdict is an INFERENCE, not an observation, and is not backfilled.")
for r,name in [(96,"VesterVenner - Strandgården Badehotel"),(174,"Toto")]:
    assert ws.cell(r,9).value=="unresolved"
    ws.cell(r,9,"not_trading")
    prev = ws.cell(r,15).value
    ws.cell(r,15, CLOSED + (" SUPERSEDES the earlier note: " + prev if prev else ""))
for r in range(205,217):
    for c in range(1,5): ws.cell(r,c).value=None
B=[("COUNTS — every one states its denominator",None,None,True),
 ("A2 unique venues (one row per venue)",'=COUNTA(A5:A203)',"the denominator for every line below",True),
 ("No exclusion recorded — passes F1; F2/F4/F5 not yet applied",'=COUNTIF(I5:I203,"")',"of the venue count above",False),
 ("  of which Københavns Kommune",'=COUNTIFS(C5:C203,"Københavns Kommune",I5:I203,"")',"of the F1 pass count above",False),
 ("  of which Frederiksberg Kommune",'=COUNTIFS(C5:C203,"Frederiksberg Kommune",I5:I203,"")',"of the F1 pass count above",False),
 ("Excluded — outside_boundary",'=COUNTIF(I5:I203,"outside_boundary")',"of the venue count above",False),
 ("  of which resolved by the operator by hand, 2026-08-01",'=COUNTIF(O5:O203,"OPERATOR RESOLUTION 2026-08-01*")',"of the outside_boundary count above",False),
 ("  of which in the FAROE ISLANDS",'=COUNTIF(C5:C203,"outside — FAROE ISLANDS")',"of the outside_boundary count above",False),
 ("Excluded — not_trading (F4)",'=COUNTIF(I5:I203,"not_trading")',"of the venue count above",False),
 ("  of which carrying a confirmed F1 pass (Kiin Kiin Tok Tok)",'=COUNTIFS(I5:I203,"not_trading",C5:C203,"Københavns Kommune")',"of the not_trading count above",False),
 ("  of which carrying NO F1 verdict (address never confirmed)",'=COUNTIF(I5:I203,"not_trading")-COUNTIFS(I5:I203,"not_trading",C5:C203,"Københavns Kommune")',"of the not_trading count above",False),
 ("F0 UNRESOLVED — no verdict",'=COUNTIF(I5:I203,"unresolved")',"of the venue count above — all 14 adjudicated 2026-08-01; this is now ZERO",False),
 ("CHECK — the four categories must equal the venue count",'=IF(B207+B210+B213+B216=B206,"PASS","FAIL — the exclusion categories do not partition the venue list")',None,True),
 ("CHECK — the two kommune lines must equal the F1 pass count",'=IF(B208+B209=B207,"PASS","FAIL — kommune breakdown does not equal the F1 pass count")',None,True),
 ("CHECK — operator-resolved + Faroese must not exceed outside_boundary",'=IF(B211<=B210,"PASS","FAIL — sub-breakdown exceeds its parent")',None,True),
 ("Memo: venues carrying an F1 PASS, including any failing a later filter",'=B207+B214',"of the venue count above",False),
]
r=205
for lab,f,den,bold in B:
    ws.cell(r,1,lab).font=Font(name=ARI,bold=bold,size=10)
    if f: ws.cell(r,2,f).font=Font(name=ARI,bold=bold,size=10)
    if den: ws.cell(r,3,den).font=Font(name=ARI,italic=True,size=9)
    r+=1
ws.cell(r+1,1,"UPDATED 2026-08-01: all 14 F0 unresolved rows adjudicated by the operator by hand. 12 are trading venues OUTSIDE the boundary (5 of them in the Faroe Islands); 2 no longer exist. "
              "Unresolved is now ZERO and the A2 contribution to the frame is unchanged at 109. See D-044.").font=Font(name=ARI,italic=True,size=9,color="B00000")
wb.save(sys.argv[2])
print("saved")
