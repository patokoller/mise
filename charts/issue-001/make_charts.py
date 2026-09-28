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
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openpyxl

OUT = "charts/issue-001/"
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


# ---------------------------------------------------------------- Chart 2: the Copenhagen frame by guide
def chart_frame():
    ws = openpyxl.load_workbook("data/cphrouteaframeunion.xlsx", data_only=True)["cph_route_a_frame_union"]
    hdr_row = next(r for r in range(1, 15) if "google_place_id" in [c.value for c in ws[r]])
    hdr = [c.value for c in ws[hdr_row]]
    rows = [dict(zip(hdr, [c.value for c in row])) for row in ws.iter_rows(min_row=hdr_row + 1)]
    rows = [r for r in rows if isinstance(r["google_place_id"], str) and r["google_place_id"].startswith("ChIJ")]
    by_route = Counter(r["route_provenance"] for r in rows)
    total = len(rows)
    assert total == 132 and sum(by_route.values()) == total, by_route

    # Closed per source on 2026-09-28 (Phase 1 collection), matched by name to the frame.
    menus = list(csv.DictReader(open("data/phase1/phase1-menus-2026-09-28.csv", encoding="utf-8")))
    closed_names = {m["venue_query_name"] for m in menus if m["trading_status"] == "closed_per_source"}
    closed = Counter(r["route_provenance"] for r in rows if r["display_name_provisional"] in closed_names)
    assert sum(closed.values()) == len(closed_names), (closed, closed_names)

    order = [("A1-only", "MICHELIN only"), ("both", "Both guides"), ("A2-only", "White Guide only")]
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    colour = CITY["Copenhagen"][0]
    for i, (key, label) in enumerate(order):
        n, k = by_route[key], closed[key]
        ax.barh(i, n, color=colour, alpha=0.85)
        if k:
            ax.barh(i, k, left=n - k, color="white", edgecolor=INK, hatch="////", linewidth=0.8)
        ax.text(n + 1, i, f"{n} of {total}" + (f"  (incl. {k} found closed)" if k else ""), va="center", fontsize=9)
    ax.set_yticks(range(3), [l for _, l in order])
    ax.invert_yaxis()
    ax.set_xlim(0, total * 0.75)
    ax.set_xlabel(f"Restaurants on our Copenhagen list (n = {total})")
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color="#dddddd", linewidth=0.5)
    fig.suptitle("Where Copenhagen's list comes from, and where the closures sit", x=0.01, ha="left",
                 fontsize=11, fontweight="bold")
    footnote(fig, f"List: MICHELIN Guide Nordic Countries 2026 and White Guide Denmark, snapshot for 28 July 2026, inside "
                  f"Københavns and Frederiksberg kommuner ({total} restaurants).\nHatched: closed per the source named in the issue, found 2026-09-28 "
                  "among the few on the list we checked by hand. Most of the list has not yet been checked for closures.\n"
                  "Restaurants no guide lists are not on the list. The Next Table.")
    fig.tight_layout(rect=(0, 0.19, 1, 0.92))
    fig.savefig(OUT + "chart2-copenhagen-list-closures.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- Chart 3: menu languages, Copenhagen, named
def chart_languages():
    menus = list(csv.DictReader(open("data/phase1/phase1-menus-2026-09-28.csv", encoding="utf-8")))
    cph = [m for m in menus if m["city"] == "Copenhagen" and m["trading_status"] != "closed_per_source"]
    langs = {}
    for m in cph:
        langs.setdefault(m["venue_query_name"], set()).update(m["languages_published"].split("+"))
    names = sorted(langs, key=lambda v: (("da" in langs[v]) + 2 * ("en" in langs[v] and "da" not in langs[v]), v.lower()))
    cols = [("en", "English"), ("da", "Danish"), ("it", "Italian")]
    fig, ax = plt.subplots(figsize=(6.2, 0.32 * len(names) + 1.6))
    colour = CITY["Copenhagen"][0]
    for y, v in enumerate(names):
        for x, (code, _) in enumerate(cols):
            if code in langs[v]:
                ax.scatter(x, y, s=70, color=colour)
            else:
                ax.scatter(x, y, s=70, facecolors="none", edgecolors="#bbbbbb")
    ax.set_xticks(range(len(cols)), [c for _, c in cols])
    ax.set_yticks(range(len(names)), names, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(-0.6, len(cols) - 0.4)
    ax.xaxis.tick_top()
    ax.grid(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)
    fig.suptitle("Which languages Copenhagen restaurants publish their menu in", x=0.01, ha="left",
                 fontsize=11, fontweight="bold")
    footnote(fig, f"{len(names)} trading Copenhagen restaurants we chose by hand — not a sample; no shares should be read "
                  "from this.\nFilled dot = the venue's own site publishes its menu or price page in that language. Checked 2026-09-28. The Next Table.")
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    fig.savefig(OUT + "chart3-copenhagen-menu-languages.png", dpi=200)
    plt.close(fig)
    return names, langs


if __name__ == "__main__":
    chart_prices()
    chart_frame()
    names, langs = chart_languages()
    print("chart 3 venues:", {v: "+".join(sorted(langs[v])) for v in names})
    print("done")
