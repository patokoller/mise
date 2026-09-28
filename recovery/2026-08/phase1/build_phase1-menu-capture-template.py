import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

ARIAL = "Arial"
HDR_FILL = PatternFill("solid", fgColor="1F3B4D")
HDR_FONT = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
FILL_ME = PatternFill("solid", fgColor="FFF2CC")   # operator fills
DERIVED = PatternFill("solid", fgColor="E8EEF2")   # controlled vocabulary
EG_FONT = Font(name=ARIAL, size=10, italic=True, color="808080")
EG_FILL = PatternFill("solid", fgColor="F2F2F2")
BODY = Font(name=ARIAL, size=10)
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# ----------------------------------------------------------------- Menus
ws = wb.active
ws.title = "Menus"

menus_cols = [
    ("menu_id", 10, "M001, M002 — you assign, never reused"),
    ("venue_name_as_written", 28, "The venue's own spelling and case. Not the guide's"),
    ("city", 12, "Copenhagen / London / Barcelona"),
    ("source_url", 46, "The exact page the menu was on. Never a homepage"),
    ("retrieved_at", 18, "TEXT. Your clock when you loaded it: 2026-08-11 14:30"),
    ("observed_at", 14, "TEXT, date only. See observed_at_source"),
    ("observed_at_source", 20, "Where observed_at came from. Mandatory"),
    ("menu_date_stated", 22, "Verbatim, if the menu prints a date. Else blank"),
    ("menu_type", 14, "One menu per row. A venue with 3 menus gets 3 rows"),
    ("f2_state", 12, "full / price_only / none"),
    ("f2_note", 30, "How hard it was to find. Free text"),
    ("languages_published", 20, "Q7. What this page is published in"),
    ("language_primary", 16, "ISO 2-letter: da / en / es / ca"),
    ("language_secondary", 18, "Blank unless genuinely bilingual"),
    ("menu_price", 12, "Set price for a tasting menu. Blank for a la carte"),
    ("currency", 10, "DKK / GBP / EUR"),
    ("competing_prices", 16, "yes / no — flag, never resolve it yourself"),
    ("competing_prices_detail", 30, "Both figures and where each appeared"),
    ("format_service_notes", 34, "Anything notable about format or service"),
    ("capture_stored", 24, "Where the PDF or screenshot lives"),
    ("collected_by", 14, "Who looked at it"),
]

for i, (h, w, _) in enumerate(menus_cols, start=1):
    c = ws.cell(row=1, column=i, value=h)
    c.font, c.fill, c.border = HDR_FONT, HDR_FILL, BOX
    c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[1].height = 30

example_menu = [
    "M001", "Restaurant Eksempel (EXAMPLE ROW — DELETE)", "Copenhagen",
    "https://example.com/menukort", "2026-08-11 14:30", "2026-08-11", "retrieval",
    "", "tasting", "full", "Menu was a PDF two clicks from the footer",
    "da+en", "da", "en", 1450, "DKK", "no", "",
    "No a la carte. One seating. Wine pairing priced separately",
    "capture/M001.pdf", "Operator",
]
for i, v in enumerate(example_menu, start=1):
    c = ws.cell(row=2, column=i, value=v)
    c.font, c.fill, c.border = EG_FONT, EG_FILL, BOX
    c.alignment = Alignment(vertical="top", wrap_text=True)
ws.row_dimensions[2].height = 30

for r in range(3, 203):
    for i in range(1, len(menus_cols) + 1):
        c = ws.cell(row=r, column=i)
        c.font, c.border, c.fill = BODY, BOX, FILL_ME
        c.alignment = Alignment(vertical="top", wrap_text=True)

for col in ("E", "F", "H"):
    for r in range(2, 203):
        ws[f"{col}{r}"].number_format = "@"

vals = {
    "G": '"menu_artefact,page_published_date,retrieval"',
    "I": '"a_la_carte,tasting,lunch,breakfast,bar,wine,dessert,brunch,snacks"',
    "J": '"full,price_only,none"',
    "L": '"da,en,da+en,other,none_published"',
    "Q": '"yes,no"',
}
for col, formula in vals.items():
    dv = DataValidation(type="list", formula1=formula, allow_blank=True, showErrorMessage=True)
    dv.error = "Not one of the permitted values. If reality needs a new one, add it to the Legend first."
    dv.errorTitle = "Controlled vocabulary"
    ws.add_data_validation(dv)
    dv.add(f"{col}2:{col}202")
    for r in range(3, 203):
        ws[f"{col}{r}"].fill = DERIVED

ws.freeze_panes = "C2"

# ---------------------------------------------------------------- Dishes
ws2 = wb.create_sheet("Dishes")

dish_cols = [
    ("dish_id", 10, "D0001 — you assign"),
    ("menu_id", 10, "Must match a menu_id on the Menus sheet"),
    ("position", 10, "Order on the menu, 1 = first"),
    ("section_name_original", 22, "As printed: Forretter, Snacks, Til deling"),
    ("section_name_translation", 22, "Separate column, never in place of the original"),
    ("dish_name_original", 34, "EXACTLY as printed. Case, accents, ø æ å, all of it"),
    ("dish_name_translation", 34, "Separate column. May be blank"),
    ("translation_source", 20, "Who translated it. Mandatory if a translation exists"),
    ("description_original", 40, "The venue's own words under the dish"),
    ("description_translation", 40, "Separate column"),
    ("price", 12, "Number only. No currency symbol, no thousands separator"),
    ("currency", 10, "DKK / GBP / EUR"),
    ("price_note", 26, "supplement / market price / per person / half portion"),
    ("uncertain", 12, "yes if you could not read it confidently"),
    ("notes", 30, "Anything else"),
]

for i, (h, w, _) in enumerate(dish_cols, start=1):
    c = ws2.cell(row=1, column=i, value=h)
    c.font, c.fill, c.border = HDR_FONT, HDR_FILL, BOX
    c.alignment = Alignment(vertical="center", wrap_text=True)
    ws2.column_dimensions[get_column_letter(i)].width = w
ws2.row_dimensions[1].height = 30

example_dishes = [
    ["D0001", "M001", 1, "Snacks", "Snacks",
     "Stegt flæsk med persillesovs", "Fried pork belly with parsley sauce",
     "machine_unverified", "Økologisk flæsk, kartofler fra Samsø",
     "Organic pork, potatoes from Samsø", None, "DKK", "included in set menu", "no",
     "EXAMPLE ROW — DELETE"],
    ["D0002", "M001", 2, "Hovedretter", "Mains",
     "Rødspætte, brunet smør", "Plaice, brown butter",
     "machine_unverified", "", "", 285, "DKK", "", "no", "EXAMPLE ROW — DELETE"],
]
for j, row in enumerate(example_dishes, start=2):
    for i, v in enumerate(row, start=1):
        c = ws2.cell(row=j, column=i, value=v)
        c.font, c.fill, c.border = EG_FONT, EG_FILL, BOX
        c.alignment = Alignment(vertical="top", wrap_text=True)

for r in range(4, 1004):
    for i in range(1, len(dish_cols) + 1):
        c = ws2.cell(row=r, column=i)
        c.font, c.border, c.fill = BODY, BOX, FILL_ME
        c.alignment = Alignment(vertical="top", wrap_text=True)

dv2 = DataValidation(
    type="list",
    formula1='"venue_published,operator,machine_unverified,none"',
    allow_blank=True, showErrorMessage=True)
dv2.error = "Not one of the permitted values."
dv2.errorTitle = "Controlled vocabulary"
ws2.add_data_validation(dv2)
dv2.add("H2:H1003")

dv3 = DataValidation(type="list", formula1='"yes,no"', allow_blank=True, showErrorMessage=True)
ws2.add_data_validation(dv3)
dv3.add("N2:N1003")

for col in ("H", "N"):
    for r in range(4, 1004):
        ws2[f"{col}{r}"].fill = DERIVED

ws2.freeze_panes = "C2"

# ---------------------------------------------------------------- Legend
ws3 = wb.create_sheet("Legend")
ws3.column_dimensions["A"].width = 34
ws3.column_dimensions["B"].width = 104

def line(label, text, bold=False, gap=False):
    r = ws3.max_row + (2 if gap else 1)
    a = ws3.cell(row=r, column=1, value=label)
    b = ws3.cell(row=r, column=2, value=text)
    a.font = Font(name=ARIAL, size=10, bold=True)
    b.font = Font(name=ARIAL, size=10, bold=bold)
    a.alignment = Alignment(vertical="top", wrap_text=True)
    b.alignment = Alignment(vertical="top", wrap_text=True)

ws3["A1"] = "Phase 1 menu capture template"
ws3["A1"].font = Font(name=ARIAL, size=14, bold=True)
ws3["B1"] = "Created 2026-08-10. Drafted by Claude, unendorsed until the operator has filled one real row."
ws3["B1"].font = Font(name=ARIAL, size=10, italic=True)

line("WHAT THIS IS", "Two sheets. Menus = one row per menu. Dishes = one row per dish, linked by menu_id. "
                     "A venue publishing a tasting menu and an a la carte menu gets two rows on Menus.", gap=True)
line("WHAT TO EDIT", "Every yellow cell. Grey-blue cells are yellow cells with a dropdown — same thing, "
                     "fewer ways to be inconsistent. Delete the two grey italic EXAMPLE rows before you start.")
line("WHAT THIS DOES NOT DO", "It validates nothing beyond the dropdowns, joins nothing, and computes nothing. "
                              "It is not the schema — the schema is what comes out of Phase 1, not what goes in.")

line("THE THREE DATE FIELDS", "This is the part that cannot be fixed later.", bold=True, gap=True)
line("retrieved_at", "Your clock at the moment you loaded the page. Always filled. Format 2026-08-11 14:30, typed as text.")
line("observed_at", "The date the menu was in force. Take the first of: (1) a date printed on the menu itself; "
                    "(2) a published or updated date shown on the page; (3) failing both, the same as retrieved_at.")
line("observed_at_source", "Which of the three applied: menu_artefact / page_published_date / retrieval. "
                           "Mandatory. Without it, nobody can later tell a venue-dated menu from one we dated by looking at it.")
line("Never used as a date", "PDF internal metadata, HTTP Last-Modified, and anything from a sitemap. "
                             "A re-save stamp is not an observation (D-053).")
line("Never inferred", "'This looks like the winter menu' is not a date. Undated is undated.")

line("THE ORIGINAL-LANGUAGE RULE", "D-020. Unrecoverable if skipped.", bold=True, gap=True)
line("dish_name_original", "Exactly as printed. Case, accents, ø æ å, the venue's own styling. "
                           "Never overwritten by a translation, ever, for any reason.")
line("translation_source", "If a translation column has anything in it, this must say who produced it. "
                           "machine_unverified is the honest default: nobody on this project reads Danish (D-022), "
                           "so a machine translation cannot be checked by anyone and must not harden into fact.")

line("PRICES", "", bold=True, gap=True)
line("Two prices on one page", "Flag it, do not resolve it. Set competing_prices to yes, put both figures and "
                               "where each appeared in the detail column, and move on. akmē carried 1500 and 1300 DKK "
                               "and only the operator could settle it. There is no mechanical rule and none is proposed.")
line("Format", "Number only. 1450, not 1.450 kr. Currency goes in its own column.")

line("F2", "full = dish-level menu published. price_only = a price with no dish list. "
           "none = neither. Three states (D-027).", gap=True)
line("If a menu defeats you", "Say so and move on. F2 needed a human on 5 of 6 venues tested, across five different "
                              "failure modes. Record f2_state as none, write what happened in f2_note, and leave it.")

line("WHAT THIS FILE IS NOT", "A sample. These venues are operator-chosen method-development venues (D-056). "
                              "Nothing published from them carries a denominator. Not one number. Ever.", bold=True, gap=True)

line("NO FORMULAS, DELIBERATELY", "There is nothing to count yet. Count blocks get added when there is. "
                                  "When they are: recalculate before sharing — on 2026-08-01 a file shipped with six "
                                  "blank counts that were correct underneath, and that produced a wrong number downstream.", gap=True)

for r in range(1, ws3.max_row + 1):
    ws3.row_dimensions[r].height = None

# RECOVERY NOTE: original saved to /mnt/user-data/outputs/phase1-menu-capture-template.xlsx
wb.save("phase1-menu-capture-template.xlsx")
print("written")
