"""Ingredient tagging for The Next Table, issue #1 (2026-09-28).

Reads menu dish text (private files, D-063) and the forecast research file, and writes ONLY aggregate
outputs (ingredient x city x year presence, and forecaster counts) — no dish text — into
analysis/ingredients/out/.

Counting is done here, in code (rule 4). Matching is by a multilingual lexicon over accent-folded text.
Machine-extracted dish text is fine for DETECTING an ingredient word; it is never quoted (D-059).

Run from the repo root:  python3 analysis/ingredients/tag_ingredients.py
"""
import csv, re, unicodedata, json, os
from collections import defaultdict

PRIV = "/home/claude/private"
D26 = f"{PRIV}/phase1-2026-09-28/phase1-dishes-2026-09-28.csv"
M26 = "data/phase1/phase1-menus-2026-09-28.csv"
D25 = f"{PRIV}/wayback-2025/dishes_2025.csv"
FC = "data/external/food_trend_forecasts_2026.csv"
OUT = "analysis/ingredients/out/"


def fold(s):
    s = s.lower().replace("ø", "o").replace("æ", "ae").replace("å", "a").replace("ß", "ss")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


# canonical term -> patterns (applied to folded text). \b = word boundary; bare = substring (Danish compounds).
LEX = {
    # forecast consensus and taxonomy watchlist
    "miso": [r"\bmiso"],
    "kimchi": [r"kimchi"],
    "matcha": [r"matcha"],
    "hojicha": [r"hojicha", r"houjicha"],
    "pistachio": [r"pistach", r"pistacchi", r"pistacie", r"festuc"],
    "yuzu": [r"\byuzu"],
    "seaweed": [r"seaweed", r"\bkelp", r"kombu", r"\bnori\b", r"wakame", r"\bdulse", r"\btang\b", r"alga", r"sea lettuce", r"havsalat"],
    "koji": [r"\bkoji", r"shio koji", r"shiokoji"],
    "beef fat": [r"beef fat", r"tallow", r"oksefedt", r"sebo\b", r"dripping"],
    "cardamom": [r"cardamom", r"kardemomme", r"cardamomo"],
    "honey": [r"\bhoney", r"honning", r"\bmiel\b", r"\bmel\b", r"\bmiele\b"],
    "vinegar": [r"vinegar", r"eddike", r"vinagre", r"\bvinagr", r"aceto"],
    "gochujang": [r"gochujang"],
    "blackcurrant": [r"black ?currant", r"cassis", r"solbaer", r"grosella negra", r"groselles negres"],
    "fermented": [r"ferment"],
    "garum": [r"\bgarum"],
    "buckwheat": [r"buckwheat", r"boghvede", r"alforfon", r"fajol", r"\bsoba\b", r"grano saraceno"],
    "verjus": [r"verjus", r"verjuice", r"agraz"],
    "sea buckthorn": [r"sea ?buckthorn", r"havtorn", r"espino amarillo"],
    "brown butter": [r"brown(ed)? butter", r"beurre noisette", r"brunet smor", r"brun smor", r"mantequilla tostada", r"burro nocciola"],
    "cultured cream": [r"cultured", r"creme fraiche", r"cremefraiche", r"syrnet", r"skyr", r"kefir"],
    "pine / spruce": [r"\bpine\b", r"spruce", r"\bfyr", r"\bgran\b", r"granskud", r"\bpino\b", r"\bpi\b"],
    "fish sauce": [r"fish sauce", r"fiskesauce", r"salsa de pescado"],
    # high-end staples and produce, for "what's actually on the plate"
    "caviar": [r"caviar", r"kaviar", r"caviale"],
    "truffle": [r"truffle", r"troffel", r"trufa", r"tartufo", r"\btofon"],
    "scallop": [r"scallop", r"kammusling", r"vieira", r"capesant"],
    "langoustine": [r"langoustine", r"jomfruhummer", r"cigala", r"escamarla", r"scampi"],
    "oyster": [r"oyster(?!s? mushroom)", r"\bostr", r"osters"],
    "crab": [r"\bcrab", r"\bkrabbe", r"cangrejo", r"centollo", r"\bgranc"],
    "lobster": [r"lobster", r"\bhummer", r"bogavante", r"llamantol", r"astice"],
    "sea urchin": [r"sea urchin", r"\buni\b", r"erizo", r"garoina", r"sohest"],
    "tuna": [r"\btuna", r"\batun", r"tonno", r"\btonyina"],
    "mackerel": [r"mackerel", r"makrel", r"caballa", r"verat", r"sgombro"],
    "cod": [r"\bcod\b", r"\btorsk", r"bacalao", r"bacalla"],
    "anchovy": [r"anchov", r"ansjos", r"anchoa", r"anxov", r"boqueron", r"acciug"],
    "caviar / roe": [r"\broe\b", r"\brogn", r"\bhuevas", r"\bbottarga", r"ikura"],
    "duck": [r"\bduck", r"\band\b", r"andebryst", r"\bpato\b", r"\bpato", r"\bànec", r"\banec", r"anatra"],
    "lamb": [r"\blamb", r"\blam\b", r"lammet?", r"cordero", r"\bxai\b", r"agnello"],
    "venison / game": [r"venison", r"\bdeer", r"\bhjort", r"\bvildt", r"\bvenado", r"\bciervo", r"\bgrouse", r"\bpartridge", r"\bpigeon", r"\bdue\b", r"pichon", r"\bcolom", r"\bperdiz"],
    "wagyu / aged beef": [r"wagyu", r"dry[- ]aged", r"modnet", r"madurad"],
    "pork / iberico": [r"\bpork", r"\bgris", r"\bcerdo", r"\bporc\b", r"iberic", r"pluma", r"secreto", r"presa\b", r"\bmaiale"],
    "pumpkin / squash": [r"pumpkin", r"squash", r"graeskar", r"calabaza", r"carbassa", r"zucca"],
    "mushroom": [r"mushroom", r"\bsvamp", r"\bsvampe", r"karl johan", r"kantarel", r"chanterelle", r"\bcep", r"porcini", r"\bseta", r"\bsetas", r"\bbolet", r"rovell", r"shiitake", r"morel", r"\bfungh", r"girolle", r"trompette"],
    "celeriac": [r"celeriac", r"knoldselleri", r"selleri", r"apionabo", r"api-rave"],
    "beetroot": [r"beetroot", r"\bbeet", r"rodbede", r"remolacha", r"remolatxa", r"barbabietol"],
    "jerusalem artichoke": [r"jerusalem artichoke", r"sunchoke", r"jordskok", r"tupinambo", r"topinambur"],
    "artichoke": [r"(?<!jerusalem )artichoke", r"alcachofa", r"carxofa", r"carciof", r"artiskok"],
    "tomato": [r"tomat", r"tomaquet", r"pomodor"],
    "fig": [r"\bfig\b", r"\bfigs\b", r"\bfigen", r"\bhigo", r"\bfigue", r"\bfico\b", r"\bfichi\b"],
    "plum": [r"\bplum", r"\bblomme", r"\bciruela", r"\bpruna", r"\bsusin"],
    "quince": [r"quince", r"kvaede", r"membrillo", r"codony"],
    "apple": [r"\bapple", r"\baeble", r"manzana", r"\bpoma\b", r"\bmela\b"],
    "pear": [r"\bpear\b", r"\bpears\b", r"\bpaere", r"\bpera\b", r"\bperas\b"],
    "rhubarb": [r"rhubarb", r"rabarber", r"ruibarbo"],
    "elderflower / elderberry": [r"elder", r"hyld", r"sauco", r"sauc\b"],
    "hazelnut": [r"hazelnut", r"hasselnod", r"avellana", r"avellan", r"nocciol"],
    "walnut": [r"walnut", r"valnod", r"\bnuez", r"\bnous\b", r"\bnoci\b"],
    "chocolate": [r"chocolat", r"chokolade", r"cioccolat", r"\bcacao", r"\bcocoa"],
    "citrus": [r"\blemon", r"\bcitron", r"\blimon", r"\bllimona", r"\blime\b", r"\blimett", r"bergamot", r"\bblood orange"],
    # "chilli" = heat of any kind: chillies and chilli pastes (kosho, gochujang, kimchi, 'nduja, harissa...).
    "chilli": [r"chil+i", r"\bchile\b", r"jalape", r"chipotle", r"guindilla", r"\bnjuda", r"\bnduja", r"\baji\b", r"piment d.?espelette", r"kosho", r"sambal", r"harissa", r"sriracha", r"togarashi", r"gochu", r"kimchi", r"\bspicy\b"],
    "rye": [r"\brye\b", r"\brug\b", r"rugbrod", r"\bcenteno"],
    "sourdough / bread": [r"sourdough", r"surdej", r"masa madre"],
    "caramelised / burnt": [r"\bburnt", r"\bcharred", r"braendt", r"\bbrasa", r"\bbrasejat", r"\bgrill", r"\bgrillet", r"\bbarbecue", r"\bbbq"],
    "smoked": [r"smoked", r"\brog(et|ede)?\b", r"ahumad", r"\bfumat", r"\baffumicat"],
    "raw / cured": [r"\bcrudo", r"\bcured\b", r"\bgravad", r"\bceviche", r"\btartar", r"\bcarpaccio", r"\bsashimi"],
    "dashi / broth": [r"\bdashi", r"\bbroth", r"\bbouillon", r"\bconsomm", r"\bfond\b", r"\bcaldo", r"\bbrou\b"],
}
DANISH_VENUES = {"Abigail & Co", "Admiralgade 26", "Bistro Boheme", "Masseria", "Paula"}
DANISH_ONLY = {r"\band\b", r"\blam\b", r"\bgran\b", r"\brug\b", r"\bdue\b", r"\bgris", r"\btang\b"}  # would misfire in English


def tag(text, venue):
    t = fold(text)
    hits = set()
    for term, pats in LEX.items():
        for p in pats:
            if p in DANISH_ONLY and venue not in DANISH_VENUES:
                continue
            if re.search(p, t):
                hits.add(term)
                break
    return hits


def main():
    os.makedirs(OUT, exist_ok=True)
    menus = {r["menu_id"]: r for r in csv.DictReader(open(M26, encoding="utf-8"))}
    rows = []  # (year, city, venue, set(terms))
    for r in csv.DictReader(open(D26, encoding="utf-8")):
        m = menus[r["menu_id"]]
        rows.append((2026, m["city"], m["venue_query_name"], tag(r["dish_text_as_extracted"] + " " + r["section_as_extracted"], m["venue_query_name"])))
    for r in csv.DictReader(open(D25, encoding="utf-8")):
        rows.append((2025, r["city"], r["venue_query_name"], tag(r["dish_text_as_extracted"] + " " + r["section_as_extracted"], r["venue_query_name"])))

    venues_with_dishes = defaultdict(set)  # year -> venues
    for y, c, v, _ in rows:
        venues_with_dishes[y].add((c, v))
    # Panel = same venue, dish text in both years; Gordon Ramsay High excluded (identical document both years).
    panel = {cv for cv in venues_with_dishes[2025] & venues_with_dishes[2026] if cv[1] != "Restaurant Gordon Ramsay High"}

    pres = defaultdict(set)  # (year, term) -> set of (city, venue)
    for y, c, v, hits in rows:
        for h in hits:
            pres[(y, h)].add((c, v))

    # Composite: heat of any kind on the same dish as shellfish (oyster, scallop, langoustine, crab, lobster, sea urchin).
    SHELL = {"oyster", "scallop", "langoustine", "crab", "lobster", "sea urchin"}
    for y, c, v, hits in rows:
        if "chilli" in hits and hits & SHELL:
            pres[(y, "heat on shellfish")].add((c, v))
    LEX_KEYS = list(LEX) + ["heat on shellfish"]
    lines = {y: sum(1 for yy, c, v, _ in rows if yy == y and (c, v) in panel) for y in (2025, 2026)}

    cities = ["Copenhagen", "Barcelona", "London"]
    out = []
    for term in LEX_KEYS:
        v26 = pres[(2026, term)]
        p25 = {cv for cv in pres[(2025, term)] if cv in panel}
        p26 = {cv for cv in v26 if cv in panel}
        out.append({
            "term": term,
            "venues_2026_all": len(v26),
            **{f"in_{c.lower()}_2026": int(any(cv[0] == c for cv in v26)) for c in cities},
            "panel_2025": len(p25), "panel_2026": len(p26),
            "panel_new_2026": sorted(v for _, v in p26 - p25),
            "panel_dropped_2026": sorted(v for _, v in p25 - p26),
        })
    denom = {
        "venues_with_dish_text_2026": len(venues_with_dishes[2026]),
        "venues_with_dish_text_2026_by_city": {c: sum(1 for cc, _ in venues_with_dishes[2026] if cc == c) for c in cities},
        "panel_size": len(panel),
        "panel_by_city": {c: sum(1 for cc, _ in panel if cc == c) for c in cities},
        "panel_venues": sorted(v for _, v in panel),
        "panel_dish_lines": lines,
    }
    json.dump({"denominators": denom, "terms": out}, open(OUT + "ingredient_presence.json", "w"), ensure_ascii=False, indent=1)
    w = csv.DictWriter(open(OUT + "ingredient_presence.csv", "w", newline="", encoding="utf-8"),
                       fieldnames=[k for k in out[0] if not k.startswith("panel_new") and not k.startswith("panel_dropped")] + ["panel_new_2026", "panel_dropped_2026"])
    w.writeheader()
    for o in out:
        w.writerow({**o, "panel_new_2026": "; ".join(o["panel_new_2026"]), "panel_dropped_2026": "; ".join(o["panel_dropped_2026"])})

    # Forecasters per term: distinct publishers mentioning the term in ingredient or paraphrase fields.
    # Restaurant Business is a secondary roundup and McCormick's two pages are one publisher.
    fc = list(csv.DictReader(open(FC, encoding="utf-8")))
    pubs = defaultdict(set)
    for r in fc:
        pub = r["publisher"]
        if pub.startswith("Restaurant Business"):
            continue
        if pub.startswith("McCormick"):
            pub = "McCormick"
        # A forecaster listing an ingredient as declining is not predicting it (e.g. Waitrose on Dubai chocolate).
        if re.search(r"declin|falling|on the way out|out of favour|less popular", r["claim_paraphrase"], re.I):
            continue
        text = r["ingredient"] + " " + r["claim_paraphrase"]
        for term in tag(text, ""):
            pubs[term].add(pub)
    all_pubs = {("McCormick" if r["publisher"].startswith("McCormick") else r["publisher"]) for r in fc if not r["publisher"].startswith("Restaurant Business")}
    json.dump({"publishers_counted": len(all_pubs), "by_term": {k: sorted(v) for k, v in pubs.items()}},
              open(OUT + "forecasters_by_term.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(denom, ensure_ascii=False))
    print("publishers counted:", len(all_pubs))
    for o in sorted(out, key=lambda o: -o["venues_2026_all"]):
        print(f'{o["term"]:26s} 2026 venues {o["venues_2026_all"]:2d}  C/B/L {o["in_copenhagen_2026"]}{o["in_barcelona_2026"]}{o["in_london_2026"]}  panel {o["panel_2025"]:2d}->{o["panel_2026"]:2d}  forecasters {len(pubs.get(o["term"], []))}  new:{o["panel_new_2026"]} dropped:{o["panel_dropped_2026"]}')


if __name__ == "__main__":
    main()
