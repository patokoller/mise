# Commodity price sources: what was fetched, 2026-09-28

Files in this folder:
- `prices.csv`: one row per commodity × series × month. Columns: commodity, series_name, source, unit, month, value, source_url, retrieved_on, note. I added the `note` column myself. It flags annual-only values, computed values, partial months and suspect values.
- `eu_weekly.csv`: the raw weekly EU quotes, exactly as the EC API published them. The EC monthly values in prices.csv are calculated from these.
- `raw/`: the source files as retrieved. WB and IMF xlsx files were converted to markdown by Firecrawl, the EC API responses are saved as JSON, and the NASS PDF was converted to markdown. Keep these for auditing.

Retrieval method: the shell has no internet access. Everything was fetched with Firecrawl scrape (basic proxy) or WebFetch/WebSearch. No value was estimated, interpolated or recalled from memory. Values were parsed by script from the fetched files, except the Spices Board figures. Those were copied into the build script by hand from the Firecrawl markdown of the PDFs (see caveats).

---

## 1. World Bank Pink Sheet (monthly)
- **Fetched:** `https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx`, sheet "Monthly Prices". The file says "Updated on September 02, 2026". The link came from worldbank.org/en/research/commodity-markets.
- **Series (column headers exactly as in the file):** Cocoa ($/kg), Coffee, Arabica ($/kg), Coffee, Robusta ($/kg), Sugar, world ($/kg), Beef ** ($/kg), Orange ($/kg), Palm oil ($/mt).
- **Range:** 2020-01 to 2026-08 for all seven series, with no gaps (80 months each).
- **Definition notes from the file's Description sheet. These matter for charts:**
  - Beef: from Jan 2024 the series is New Zealand 90% chemical lean, c.i.f. U.S. From Sep 2021 to Dec 2023 it is Australia cow forequarters 85% CL. Before Aug 2021 it is Aus/NZ mixed trimmings 85%. **So the series spliced twice inside 2020–2026.**
  - Palm oil: from Feb 2025 it is Crude, DAP. Nov 2024 to Jan 2025 it is 5% bulk CIF NW Europe. Jan 2021 to Oct 2024 it is RBD FOB Malaysia. Up to Dec 2020 it is RBD CIF Rotterdam. **Three definition changes inside the chart window.**
  - "Orange" means fresh navel oranges (EU indicative import price, c.i.f. Paris). **It is not orange juice.** The Pink Sheet has no orange juice series.
  - Sugar, world = ISA daily price, raw, f.o.b. Caribbean.
- The latest Pink Sheet PDF (September 2026) was identified but not needed, because the xlsx read cleanly.

## 2. IMF Primary Commodity Prices (monthly)
- **Fetched:** `https://www.imf.org/-/media/files/research/commodityprices/monthly/external-data.xlsx`, linked from imf.org/en/Research/commodity-prices.
- **Series:** POLVOIL (olive oil, extra virgin <1% FFA, ex-tanker U.K., US$/metric ton), PCOCO (US$/mt), PCOFFOTM (Other Mild Arabicas, US cents/lb), PCOFFROB (Robusta, US cents/lb).
- **Range:** 2020-01 to 2026-08, no gaps (80 months each).
- **Unit caveat:** the file labels every series "USD" in its Data Type row. The actual units are in each series description, and I used those. For POLVOIL the description says "US$ per metric ton".
- **Cross-check against WB:** IMF cocoa is $/mt and WB cocoa is $/kg. The Aug 2026 values are 5950.99 and 5.95. The coffee series use different units (c/lb vs $/kg) and different market definitions (IMF uses the New York cash price, WB uses the NY+EU average), so they will not match exactly.
- The file also contains PORANG, an orange juice futures series (generic 1st 'JO' future, USD/lb). It was not extracted because the brief listed orange juice under WB only. It is available if wanted.

## 3. European Commission Agri-food Data Portal (weekly, converted to monthly by us)
- **Fetched (JSON API):**
  - Olive oil: `https://ec.europa.eu/agrifood/api/oliveOil/prices?memberStateCodes=ES&beginDate=01/01/2020&endDate=28/09/2026` (11,513 records)
  - Dairy: `https://ec.europa.eu/agrifood/api/dairy/prices?memberStateCodes=EU&beginDate=01/01/2020&endDate=28/09/2026` (3,397 records)
  - Eggs: `https://ec.europa.eu/agrifood/api/poultry/egg/prices?memberStateCodes=EU&beginDate=01/01/2020&endDate=28/09/2026` (984 records)
- **Series kept:**
  - Extra virgin olive oil (up to 0.8%), market "Jaén (ES616)", €/100kg: weekly, from the week starting 06/01/2020 to the week starting 14/09/2026.
  - The same product, market "Average national price" (Spain), also kept.
  - BUTTER, EU, €/100kg: weekly, 06/01/2020 to 14/09/2026.
  - SMP, EU, €/100kg: weekly, 06/01/2020 to 14/09/2026.
  - Eggs, EU average, €/100kg, for the Barn, Free range and Cage farming methods: **weekly from 03/01/2022 only**. The Organic series is also in the raw JSON.
- **Important:** the EC publishes these as weekly prices. The monthly values in prices.csv are **my own arithmetic means of the weekly quotes whose week begins in that month**. They are not an official EC monthly figure, and each row says so in `note`. The raw weekly numbers are in eu_weekly.csv. **2026-09 is a partial month** (2 weeks) and is flagged.
- **Gap:** EU-aggregate egg prices for 2020–2021. A direct query for 01/01/2020–31/12/2021 returned HTTP 404, "No results found for the selected parameter(s)." Member-state egg series were not tried.
- Not tried: EU average olive oil across member states (Italian and Greek markets), and other dairy products. Cheddar, Gouda, Emmental, Edam, WMP, whey powder, cream and drinking milk are all in raw/eu_dairy.json if needed.

## 4. Spices Board India (monthly)
- **Fetched (PDF):**
  - `https://www.indianspices.com/admin/international_weekly_price/upload/monthly%20domestic%20average%20price%20upto%20FEB%202026.pdf`. This is the file currently linked from indianspices.com/monthly-price-domestic.html. It covers FY2021-22 to Feb 2026.
  - `https://www.indianspices.com/admin/international_weekly_price/upload/monthly%20domestic%20average%20price%20upto%20September%202024.pdf`. Used only for 2020 and 2021 months that the newer file no longer contains.
  - Also read for cross-checking: the "upto may 2024" PDF.
- **Series:**
  - BLACK PEPPER (MG-1) COCHIN, Rs/kg, on a fiscal year Apr–Mar. **Range: 2020-01 to 2026-02, complete (74 months).**
  - CARDAMOM (SMALL) UNGRADED ALL INDIA AUCTION PRICE, Rs/kg, on a season Aug–Jul. **Range: 2020-01 to 2026-02, 73 months. 2020-04 is missing and printed as "-" in the source**, the Covid auction suspension.
  - SAFFRON (DELHI), Rs/kg: see section 6.
- **Latest available is Feb 2026.** No newer monthly PDF was found. The site also publishes daily small-cardamom auction results (daily-price-small.html), which run to 25-Sep-2026. I did not turn these into monthly averages, because that would be our calculation, not Spices Board's.
- **Caveats:**
  - The PDFs are exports from Excel. Firecrawl's text conversion garbled one cardamom row label in the Feb-2026 file ("LL) GRAPHAMED ALL INDIA AUCTION PRICE"), and it printed a duplicated, corrupted 2022-23 row ("070.40 | … | 045.24"). **I used the clean 2022-23 row, which matches the Sep-2024 file.**
  - The two files differ slightly for some months, because the newer file revised them. Cardamom 2023-10: 1653.36 (Feb-2026 file) vs 1653.50 (Sep-2024 file). 2024-07: 2208.54 vs 2208.57. 2024-08/09: 2204.43/2286.41 vs 2204.40/2289.13. **I used the newer Feb-2026 values wherever both exist.**
  - **Recommend a manual eyeball check of these rows against the PDF before publishing**, because values were copied from converted text.
  - The Spices Board attributes the underlying prices to trade bodies: the Indian Pepper and Spice Trade Association (pepper) and the Cardamom Merchant's Chamber and auctioneers (cardamom). It is official publication of market-reported prices.

## 5. USDA tree nuts (annual only)
- **No official monthly price series was found** for pistachios or hazelnuts. USDA AMS and FAS were not exhaustively searched. ERS Fruit and Tree Nut Yearbook tables were not fetched.
- **Fetched:** USDA NASS *Noncitrus Fruits and Nuts* annual summaries:
  - 2025 Summary (May 2026): `https://release.nass.usda.gov/reports/ncit0526.pdf`. Gives 2023–2025.
  - 2022 Summary (May 2023): `https://esmis.nal.usda.gov/sites/default/release-files/zs25x846c/zk51wx21m/k356bk214/ncit0523.pdf`. Gives 2020–2022.
- **Series (annual crop-year grower price):**
  - Pistachio (California), $/lb: 2020 2.510, 2021 2.160, 2022 2.110, 2023 1.870, 2024 2.250, 2025 2.480.
  - Hazelnut (Oregon), $/ton, in-shell: 2020 2100, 2021 2160, 2022 1300, 2023 1350.00, 2024 1680.00, 2025 2800.00.
- **Check:** every year was verified as production × price = the published value of production. In the 2022 file's summary table, the pistachio figure was mis-rendered as "2,510". The state table has it as 2.510, and that is the one used.
- In prices.csv, `month` holds the crop year only (e.g. "2025"), and each row is flagged ANNUAL.

## 6. Vanilla and saffron
- **Vanilla: nothing official found.** A search for official Madagascar export unit values (INSTAT, Banky Foiben'i Madagasikara, the Ministry of Commerce) returned only trade press and commercial sites: Tridge, Cooks Vanilla, Le Vanillier, exportready.africa, tradingeconomics. None were used. Two possible official routes were not reached: UN Comtrade (HS 0905 export value ÷ quantity) and Madagascar's regulated minimum export price announcements. **No vanilla data in prices.csv.**
- **Saffron:** the Spices Board PDFs include "SAFFRON (DELHI)", Rs/kg, sourced from Vyapara Kiranamandi, New Delhi. It is included as the only official-publication series found, with these caveats:
  - Coverage is 2020-01 to 2026-02 with **gaps**: 2020-04, 2020-05, 2021-10 to 2021-12, and **all of FY2022-23 (Apr 2022 to Mar 2023)**, which is absent from both PDFs. That gives 57 months.
  - **2021-06 is printed as 675000 in both PDFs**, against neighbouring months of 65000 and 75000. It is almost certainly a typo in the source. It is recorded as printed and flagged SUSPECT. Do not chart it without deciding how to handle it.
  - This is a Delhi wholesale market quote, not an international price. No official international saffron price series (e.g. from Iran) was found.
