# Session e2953710 turn 1 (add_a1_checks.py) and turn 9 (patch_docs.py, A1 part), verbatim logic.
import openpyxl, shutil, sys
from openpyxl.styles import Font
path = sys.argv[1]
wb = openpyxl.load_workbook(path)
ws = wb["cph_route_a1_frame"]
assert ws.cell(102,1).value.startswith("Pass F1 — Københavns"), ws.cell(102,1).value
assert ws.cell(104,1).value.startswith("D-032"), ws.cell(104,1).value
ws.insert_rows(103, amount=5)
ARI="Arial"
checks = [
 ("CHECK — tier counts must sum to candidates enumerated (D-032, made mechanical)",
  '=IF(B91+B92+B93+B94+B95=B90,"PASS","FAIL — the five tier counts do not sum to the enumerated total")'),
 ("CHECK — F1 pass + F1 fail must equal candidates enumerated",
  '=IF(B102+B96=B90,"PASS","FAIL — pass and fail do not partition the candidate list")'),
 ("CHECK — the two kommune lines must equal the F1 pass count",
  '=IF(B98+B99=B102,"PASS","FAIL — kommune breakdown does not equal the F1 pass count")'),
 ("CHECK — F0 resolved + not resolved must equal candidates enumerated",
  '=IF(B100+B101=B90,"PASS","FAIL — F0 resolution states do not partition the candidate list")'),
]
for i,(lab,f) in enumerate(checks):
    r = 103+i
    ws.cell(r,1,lab).font = Font(name=ARI, bold=True, size=10)
    ws.cell(r,2,f).font   = Font(name=ARI, bold=True, size=10)
ws.cell(107,1,"CHECK ROWS ADDED 2026-08-01. Every count block in this project carries one; A1 was owed the same guard A2 and the prediction ledger already had. All four must read PASS.").font = Font(name=ARI, italic=True, size=9)
wb.save(path)
print("checks added")

wb=openpyxl.load_workbook(path); ws=wb["cph_route_a1_frame"]
FIX={73:"Gentofte Kommune",74:"Gentofte Kommune",75:"Gentofte Kommune",76:"Rudersdal Kommune"}
for r,k in FIX.items():
    assert ws.cell(r,5).value==k, (r,ws.cell(r,5).value)
    ws.cell(r,30,f"Fails F1 on the RESOLVED ADDRESS — {ws.cell(r,6).value}, which is {k}, outside Københavns + Frederiksberg. "
                 f"Note corrected 2026-08-01: it previously read 'fails F1 on the guide's city label', which cites the wrong evidence. "
                 f"21 §12.1 requires F1 to be applied to resolved addresses only, because MICHELIN's city label is not a boundary. Verdict unchanged.")
ws.cell(96,1,"Fail F1 — outside_boundary (4 on the resolved address, 11 on country: Malmö rows are unresolved)")
ws.cell(108,1,"NOTE CORRECTION 2026-08-01: rows 73-76 previously recorded the guide's city label as the basis for their F1 failure. All four have resolved addresses and resolved kommunes, so they fail on the resolved address, per 21 §12.1. Counts unaffected. See D-045.").font=Font(name="Arial",italic=True,size=9,color="B00000")
wb.save(path)
print("notes patched")
