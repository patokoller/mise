# Restaurant price indices: sources

Retrieved on 2026-09-28 (UTC, from `date -u`). Every value in `restaurant_cpi.csv` was read from the raw machine-readable response of the URL given in its `source_url` column. No value was estimated, interpolated or computed. Coverage is monthly, 2023-01 to 2026-08, for all three countries. August 2026 is the latest month each source had published on the retrieval date.

## United Kingdom (ONS, CPI)
- **Restaurants:** series CDID **D7JA**, dataset MM23, titled "CPI ANNUAL RATE 11.1.1 : RESTAURANTS & CAFES 2015=100", unit %.
- **All items:** CDID **D7G7**, MM23, titled "CPI ANNUAL RATE 00: ALL ITEMS 2015=100".
- **Fetched:** the ONS CSV generator:
  - https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/d7ja/mm23
  - https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/d7g7/mm23
- **Release:** both files carry the header "Release date 16-09-2026, Next release 21 October 2026".
- **Coverage:** 2023-01 to 2026-08, with no gaps.
- **Annual averages:** the same files also give them (D7JA: 2023 9.2, 2024 5.4, 2025 4.2; D7G7: 2023 7.3, 2024 2.5, 2025 3.4). They are not in the CSV, which holds monthly values only.
- **Definition:** this is the national CPI, which follows HICP methodology. It is not CPIH (CPIH, which includes owner-occupiers' housing costs, was not fetched). The UK is not in Eurostat after 2020, so there is no Eurostat cross-check.

## Denmark (Danmarks Statistik, CPI)
- **Table:** statbank table **PRIS01**, the current national CPI table on the ECOICOP ver. 2 classification. Its last period is 2026M08.
- **Restaurants:** VAREGR **1111**, "11.1.1 Restaurants, cafés and the like".
- **All items:** VAREGR **000000**, "00 Consumer price index, total".
- **Unit:** ENHED **300**, "Percentage change compared to same month the year before (per cent)".
- **Fetched:** the Statbank API:
  - https://api.statbank.dk/v1/data/PRIS01/CSV?lang=en&VAREGR=000000,1111&ENHED=300&Tid=>=2023M01
  - The all-items series was fetched a second time on its own to confirm the values.
- **Coverage:** 2023-01 to 2026-08, with no gaps.
- **Older table, not used:** PRIS111 (the old-classification table, which the tableinfo response describes as replaced by PRIS01) was also read up to 2025M12. Several of its months differ by 0.1 point from PRIS01 (for example 2023M02 restaurants: 10.0 in PRIS111, 10.1 in PRIS01). That looks like a revision from the reclassification. I used only PRIS01.
- **Annual averages:** not fetched.
- **Cross-check against Eurostat HICP:** the Eurostat restaurants series (CP1111) has exactly the same monthly values as PRIS01 for every month. Danish all-items HICP differs from Danish national all-items CPI (for example 2023-01: CPI 7.7, HICP 8.4). Both are included in the CSV under different `measure` labels.

## Spain (INE, IPC base 2025)
- **Restaurants:** series **IPC291378**, "Nacional. Restaurantes, cafés, establecimientos de comida rápida y similares. Variación anual." This is subclass 11.1.1 under ECOICOP ver. 2 (INE table 76127, "Índices nacionales de clases ECOICOP ver.2"). The series metadata shows classification "Base 2025 (IPC, IPCA)" and latest publication "Índice de Precios de Consumo. Agosto 2026".
- **All items:** series **IPC290750**, "Nacional. Índice general. Variación anual." (table 76125).
- **Fetched:** the INE Tempus3 JSON API:
  - https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC291378?date=20230101:20261231
  - https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC290750?date=20230101:20261231
  - https://servicios.ine.es/wstempus/js/ES/SERIE/IPC291378?det=2 (metadata)
- **Coverage:** 2023-01 to 2026-08, with no gaps.
- **Label:** INE's current label is "Restaurantes, cafés, establecimientos de comida rápida y similares". The older label "Restaurantes, bares, cafeterías y similares" does not appear in the base-2025 tables. It is the same COICOP code (11.1.1).
- **Annual averages:** not fetched.
- **Cross-check against Eurostat HICP (CP1111):** it differs from INE's national IPC by 0.1 point in a few months (for example 2023-01: IPC 7.8, HICP 7.9). All-items HICP also differs from IPC (for example 2026-08: IPC 4.3, HICP 4.6). Both are in the CSV.

## Eurostat (HICP; cross-check for Denmark and Spain)
- **Dataset:** **prc_hicp_minr**, the current ECOICOP ver. 2 dataset (last updated 2026-09-17, latest period 2026-08).
- **Series:** unit RCH_A (annual rate of change); coicop18 **CP1111** "Restaurants, cafés and the like" and **TOTAL**; geo DK and ES.
- **URL:** https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_minr?format=JSON&geo=DK&geo=ES&coicop18=CP1111&coicop18=TOTAL&sinceTimePeriod=2023-01
- **Dataset suggested in the brief, not used:** prc_hicp_manr is marked "discontinued and replaced by dataset prc_hicp_minr" and stops at 2025-12. I fetched it but did not use its values. Some of its months differ by 0.1 point from minr.
- **Flags:** none of the RCH_A values used carry a status flag. The only "low reliability" flags in the response are on the moving-average unit, which was not used.
- **In the CSV:** these rows are labelled `restaurants_hicp` and `all_items_hicp`.

## Definitional notes
- **UK and national-CPI rows:** the UK (ONS CPI), Denmark (national CPI) and Spain (national IPC) rows are each country's national index. These are not strictly identical in method: they use different weights, and treat owner-occupied housing and some taxes and services differently.
- **Like-for-like comparison of Denmark and Spain:** use the Eurostat HICP rows.
- **UK coverage:** only the UK national CPI is available. It is HICP-methodology but not published by Eurostat after 2020.
- **Classification:** all restaurant series are COICOP 11.1.1. Denmark and Spain are now on ECOICOP ver. 2 (COICOP 2018). The ONS series is labelled with the older COICOP 11.1.1 "Restaurants & cafes". ONS has not been checked for any reclassification.
