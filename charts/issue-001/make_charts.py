"""Charts for The Next Table, issue #1 (2026-09-28).

Every number drawn here is read from a file in this repository at run time; nothing is typed in.
Run from the repository root:  python3 charts/issue-001/make_charts.py
Outputs PNGs at 2x into charts/issue-001/.

House style (19-data-visualisation.md §3, colours fixed by D-066):
  Copenhagen / Denmark  #0072B2  solid
  Barcelona  / Spain    #D55E00  dashed
  London     / UK       #009E73  dotted
"""
import csv
import os
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import openpyxl

OUT = "charts/issue-001/"
HELD = "charts/held-for-later/"  # panel charts kept for a future issue (D-069)
CITY = {  # D-066: fixed forever
    "Copenhagen": ("#0072B2", "-"),
    "Barcelona": ("#D55E00", "--"),
    "London": ("#009E73", ":"),
}
GREY = "#8a8a8a"
INK = "#222222"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": "#dddddd", "grid.linewidth": 0.5,
})


def footnote(fig, text):
    fig.text(0.01, 0.01, text, fontsize=7.5, color="#555555", ha="left", va="bottom", wrap=True)


# ---------------------------------------------------------------- Chart 1: restaurant prices
def chart_prices():
    rows = list(csv.DictReader(open("data/external/restaurant_cpi_2023-01_2026-08.csv", encoding="utf-8")))
    panels = [("DK", "Denmark", "Copenhagen"), ("ES", "Spain", "Barcelona"), ("UK", "United Kingdom", "London")]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.9), sharey=True)
    for ax, (code, label, city) in zip(axes, panels):
        colour, style = CITY[city]
        for measure, c, ls, name in [("restaurants", colour, style, "Restaurants & cafés"),
                                     ("all_items", GREY, "-", "All items")]:
            s = sorted((r["month"], float(r["annual_rate_pct"])) for r in rows
                       if r["country"] == code and r["measure"] == measure)
            months = [m for m, _ in s]
            assert months[0] == "2023-01" and months[-1] == "2026-08" and len(months) == 44, (code, measure, len(months))
            x = list(range(len(s)))
            ax.plot(x, [v for _, v in s], color=c, linestyle=ls, linewidth=1.8 if measure == "restaurants" else 1.2,
                    label=name)
            dy = 5 if measure == "restaurants" else -5  # keep the two end labels apart when values are close
            ax.annotate(f"{s[-1][1]:.1f}", (x[-1], s[-1][1]), xytext=(4, dy), textcoords="offset points",
                        fontsize=8, color=c, va="center")
        ax.set_title(f"{label}\n(national data; our city: {city})", fontsize=9.5, loc="left")
        ax.set_xticks([0, 12, 24, 36, 43], ["Jan 23", "Jan 24", "Jan 25", "Jan 26", "Aug 26"], fontsize=8)
        ax.set_ylim(0, 12)
        ax.legend(fontsize=7.5, frameon=False, loc="upper right")
    axes[0].set_ylabel("% change on a year earlier")
    fig.suptitle("Restaurant prices vs all consumer prices, annual rate of change, Jan 2023 – Aug 2026",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    footnote(fig, "Source: ONS CPI D7JA / D7G7 (UK); Danmarks Statistik PRIS01, 11.1.1 / total (DK); INE IPC291378 / IPC290750 (ES). "
                  "National CPIs; methods differ slightly by country. Monthly, 44 months per series. Retrieved 2026-09-28.\n"
                  "Covers all restaurants and cafés nationally — context for our cities, not a measurement of them. The Next Table.")
    fig.tight_layout(rect=(0, 0.11, 1, 0.93))
    fig.savefig(OUT + "chart1-restaurant-prices.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- shared: ingredient outputs (analysis/ingredients)
import json
ING = json.load(open("analysis/ingredients/out/ingredient_presence.json", encoding="utf-8"))
FCB = json.load(open("analysis/ingredients/out/forecasters_by_term.json", encoding="utf-8"))
TERMS = {t["term"]: t for t in ING["terms"]}
N_PANEL = ING["denominators"]["panel_size"]
N_PUB = FCB["publishers_counted"]
PANEL_NOTE = (f"Panel: the same {N_PANEL} kitchens (Copenhagen {ING['denominators']['panel_by_city']['Copenhagen']}, "
              f"Barcelona {ING['denominators']['panel_by_city']['Barcelona']}, London {ING['denominators']['panel_by_city']['London']}) "
              "whose menus we could read both years: 2025 from Internet Archive captures dated 2025-08-09 to 2025-11-11, 2026 read on 2026-09-28. "
              "Chosen by us, not a sample; below our signal threshold.")
DOT25, DOT26 = "#9a9a9a", "#222222"


# ---------------------------------------------------------------- Chart 2: forecasts vs kitchens
def chart_forecasts():
    not_ingredients = {"fermented", "dashi / broth", "pork / iberico", "caramelised / burnt", "raw / cured", "smoked"}  # techniques / generic
    rows = [(t, len(p)) for t, p in FCB["by_term"].items() if len(p) >= 2 and t in TERMS and t not in not_ingredients]
    rows.sort(key=lambda r: (-r[1], r[0]))
    labels = {"chilli": "heat (chilli, kosho, kimchi…)", "fermented": "fermented (technique)", "honey": "honey (incl. hot honey)",
              "vinegar": "vinegar (incl. fruit vinegars)", "chocolate": "chocolate (incl. Dubai)"}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 0.36 * len(rows) + 2.3), sharey=True,
                                 gridspec_kw={"width_ratios": [1, 1.25]})
    y = list(range(len(rows)))
    a1.barh(y, [n for _, n in rows], color="#6b6b6b")
    for yi, (_, n) in zip(y, rows):
        a1.text(n + 0.15, yi, str(n), va="center", fontsize=8)
    a1.set_yticks(y, [labels.get(t, t) for t, _ in rows], fontsize=9)
    a1.invert_yaxis()
    a1.set_xlim(0, max(n for _, n in rows) + 1.5)
    a1.set_title(f"Named as a 2026 trend by … of the {N_PUB}\nforecasters we read", fontsize=9.5, loc="left")
    a1.grid(axis="y", visible=False); a1.grid(axis="x", color="#dddddd", linewidth=0.5)
    for yi, (t, _) in zip(y, rows):
        p25, p26 = TERMS[t]["panel_2025"], TERMS[t]["panel_2026"]
        a2.plot([p25, p26], [yi, yi], color="#cccccc", linewidth=1, zorder=1)
        a2.scatter(p25, yi, s=40, facecolors="white", edgecolors=DOT25, zorder=2)
        a2.scatter(p26, yi, s=40, color=DOT26, zorder=3)
    a2.set_xlim(-0.5, N_PANEL + 0.5)
    a2.set_xticks(range(0, N_PANEL + 1, 2))
    a2.set_title(f"On the menus of … of our {N_PANEL} panel kitchens\n○ Sept 2025   ● Sept 2026", fontsize=9.5, loc="left")
    a2.grid(axis="y", visible=False); a2.grid(axis="x", color="#dddddd", linewidth=0.5)
    fig.suptitle("What the 2026 forecasts name, and whether serious kitchens were already serving it",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    footnote(fig, f"Forecasters: {N_PUB} publishers of 2026 food-trend forecasts (Oct 2025 – Jun 2026), mostly US and UK; each counted once. "
                  "Ingredients named by at least 2.\n" + PANEL_NOTE + " Ingredients matched in code on menu text. The Next Table.")
    fig.tight_layout(rect=(0, 0.13, 1, 0.93))
    fig.savefig(HELD + "panel-forecasts-vs-kitchens.png", dpi=200)
    plt.close(fig)
    return rows


# ---------------------------------------------------------------- Chart 3: panel movers
def chart_movers():
    skip = {"citrus", "caramelised / burnt", "raw / cured", "dashi / broth", "sourdough / bread"}  # methods and generic words
    mv = [(t, d["panel_2025"], d["panel_2026"]) for t, d in TERMS.items()
          if t not in skip and abs(d["panel_2026"] - d["panel_2025"]) >= 3]
    mv.sort(key=lambda r: (r[2] - r[1]), reverse=True)
    fig, ax = plt.subplots(figsize=(7.5, 0.42 * len(mv) + 2.2))
    for yi, (t, a, b) in enumerate(mv):
        col = "#0b6e4f" if b > a else "#a23b2a"
        ax.annotate("", xy=(b, yi), xytext=(a, yi), arrowprops=dict(arrowstyle="->", color=col, lw=1.4))
        ax.scatter(a, yi, s=40, facecolors="white", edgecolors=DOT25, zorder=3)
        ax.scatter(b, yi, s=40, color=col, zorder=3)
        ax.text(max(a, b) + 0.4, yi, f"{a} → {b}", va="center", fontsize=8.5)
    ax.set_yticks(range(len(mv)), [t for t, _, _ in mv], fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlim(-0.5, N_PANEL + 0.5)
    ax.set_xticks(range(0, N_PANEL + 1, 2))
    ax.set_xlabel(f"Panel kitchens with it on the menu, of {N_PANEL}  (○ Sept 2025  ● Sept 2026)")
    ax.grid(axis="y", visible=False); ax.grid(axis="x", color="#dddddd", linewidth=0.5)
    fig.suptitle("Same kitchens, a year apart: the ingredients that moved most",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    footnote(fig, PANEL_NOTE + f" Shown: moves of 3 or more kitchens. Menus were shorter this year "
                  f"({ING['denominators']['panel_dish_lines']['2025']} dish lines in 2025, {ING['denominators']['panel_dish_lines']['2026']} in 2026), "
                  "which favours falls. Watch list, not a trend. The Next Table.")
    fig.tight_layout(rect=(0, 0.16, 1, 0.93))
    fig.savefig(HELD + "panel-movers.png", dpi=200)
    plt.close(fig)
    return mv



# ---------------------------------------------------------------- Chart 2: kitchen staples, indexed
COM = "data/external/commodity_prices_2020-2026.csv"


def load_series(pred):
    rows = [r for r in csv.DictReader(open(COM, encoding="utf-8")) if pred(r) and r["value"] not in ("",)]
    return {r["month"]: float(r["value"]) for r in rows}


def chart_staples():
    series = [
        ("Cocoa (World Bank)", lambda r: r["commodity"] == "cocoa" and r["source"].startswith("World Bank"), "#E69F00", "-"),
        ("Arabica coffee (World Bank)", lambda r: r["commodity"] == "coffee_arabica" and r["source"].startswith("World Bank"), "#56B4E9", "--"),
        ("Extra virgin olive oil, Spain (EU Commission)", lambda r: r["series_name"].startswith("EC: Extra virgin olive oil (up to 0.8%), Spain average"), "#CC79A7", "-."),
        ("Butter, EU average (EU Commission)", lambda r: r["commodity"] == "butter", "#333333", ":"),
    ]
    months = [f"{y}-{m:02d}" for y in range(2020, 2027) for m in range(1, 13) if f"{y}-{m:02d}" <= "2026-08"]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    for name, pred, col, ls in series:
        s = load_series(pred)
        base = [s[m] for m in months if m.startswith("2020")]
        assert len(base) == 12, (name, len(base))
        b = sum(base) / 12
        xs = [i for i, m in enumerate(months) if m in s]
        ys = [100 * s[m] / b for m in months if m in s]
        assert len(xs) == len(months), (name, "missing months")
        ax.plot(xs, ys, color=col, linestyle=ls, linewidth=1.8, label=name)
        dy = {"#E69F00": 6, "#56B4E9": -6}.get(col, 0)  # cocoa and coffee end close together
        ax.annotate(f"{ys[-1]:.0f}", (xs[-1], ys[-1]), xytext=(4, dy), textcoords="offset points", fontsize=8, color=col, va="center")
    ax.axhline(100, color="#999999", linewidth=0.7)
    ax.set_ylim(0, None)
    ax.set_xticks([0, 12, 24, 36, 48, 60, 72, len(months) - 1], ["Jan 20", "Jan 21", "Jan 22", "Jan 23", "Jan 24", "Jan 25", "Jan 26", "Aug 26"], fontsize=8.5)
    ax.set_ylabel("Price index, 2020 average = 100")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    fig.suptitle("Four staples of the pastry section and the café, monthly prices, Jan 2020 – Aug 2026",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    footnote(fig, "Sources: World Bank Commodity Price Data (Pink Sheet), monthly, updated 2 Sept 2026 — cocoa and arabica in $/kg; "
                  "European Commission agri-food data portal — weekly quotes (EUR/100 kg), averaged to months by us.\n"
                  "Wholesale and world-market prices, not what a restaurant pays. Each series divided by its own 2020 average. Retrieved 2026-09-28. The Next Table.")
    fig.tight_layout(rect=(0, 0.1, 1, 0.93))
    fig.savefig(OUT + "chart2-staples-prices.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- Chart 3: spices, Indian wholesale markets
def chart_spices():
    panels = [("Small cardamom", "cardamom_small", "all-India auction average"), ("Black pepper", "black_pepper", "Kochi market"),
              ("Saffron", "saffron", "Delhi wholesale market")]
    months = [f"{y}-{m:02d}" for y in range(2020, 2027) for m in range(1, 13) if f"{y}-{m:02d}" <= "2026-02"]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.9))
    for ax, (title, com, where) in zip(axes, panels):
        rows = [r for r in csv.DictReader(open(COM, encoding="utf-8")) if r["commodity"] == com and r["value"]]
        s = {r["month"]: float(r["value"]) for r in rows if "SUSPECT" not in (r.get("note") or "").upper()}
        ys = [s.get(m) for m in months]  # None = gap in the source; drawn as a break
        ax.plot(range(len(months)), [float("nan") if y is None else y for y in ys], color="#8a5a00", linewidth=1.6)
        last = max(m for m in s if m <= "2026-02")
        ax.annotate(f"{s[last]:,.0f}", (months.index(last), s[last]), xytext=(4, 0), textcoords="offset points", fontsize=8, va="center")
        ax.set_title(f"{title}\n({where}, Rs/kg)", fontsize=9.5, loc="left")
        ax.set_ylim(0, None)
        ax.set_xticks([0, 24, 48, len(months) - 1], ["Jan 20", "Jan 22", "Jan 24", "Feb 26"], fontsize=8)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    fig.suptitle("Spice prices in India's wholesale markets, monthly averages, Jan 2020 – Feb 2026",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    footnote(fig, "Source: Spices Board India, monthly average domestic prices (latest file: Feb 2026); figures reported to it by trade bodies and auctioneers. "
                  "Gaps are months the source leaves blank.\nSaffron: June 2021 omitted — printed as 675,000 between 65,000 and 75,000, almost certainly a typo in the source. "
                  "Retrieved 2026-09-28. The Next Table.")
    fig.tight_layout(rect=(0, 0.12, 1, 0.9))
    fig.savefig(OUT + "chart3-spice-prices.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    chart_prices()
    os.makedirs(HELD, exist_ok=True)
    chart_forecasts(); chart_movers()   # held for a later issue
    chart_staples()
    chart_spices()
    print("done")
