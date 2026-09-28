# Ingredient forecast research: notes
Retrieved 2026-09-28. Every row in forecasts.csv comes from a page opened in this session (WebFetch or Firecrawl basic proxy). Quotes are kept short; everything else is paraphrased.

## Part B (Google Trends): not done
Google Trends could not be retrieved:
- WebFetch on trends.google.com/trends/explore was refused (the site's robots.txt disallows it).
- Firecrawl scrape (basic proxy) of the DK/koji and GB/miso explore URLs returned HTTP 429 "Too Many Requests", with no chart data.
Following the brief, I stopped part B and wrote no search_interest.csv. I have no search-interest direction for any term or country. I did not try the stealth proxy, pytrends or third-party Trends mirrors.

## Sources opened (23 pages)
Restaurant/foodservice scope:
- Baum + Whiteman 2026 report (PDF, dated 2025-11-03). I opened the PDF through Firecrawl and extracted it with a query, so I did not read the full text myself.
- McCormick for Chefs Flavor Forecast 2026 (foodservice page; mccormickforchefs.com redirects there). The page shows no date; I used the 2025-12-09 date of the McCormick press release.
- Datassential 2026 trends report page (2025-11-06) and "10 Flavors to Know" (2026-02-02).
- Technomic 2026 Global Foodservice Trend Predictions. The page shows no publication date.
- Restaurant Business roundup, 2025-12-19. It is a secondary source quoting Technomic, Datassential, Monin, AF&Co.+Carbonate, Yelp, Kimpton, US Foods and B+W.
- James Beard Foundation (2026-01-05), MICHELIN Guide inspectors (2026-01-08).
- UK: Great British Chefs (2026-01-08), Restaurant Industry Magazine (2025-12-03), Morning Advertiser (2026-01-15), Lumina Intelligence (2026-01-22), Bidfood (2026-05-18), Tastewise UK menu trends (2026-06-02).
- Spain: InfoHoreca on Madrid Fusion 2026 (2026-01-27) and Canariasgourmet on San Sebastian Gastronomika 2025 (2025-10-04). Both are thematic and name almost no trend ingredients.
Retail scope: Waitrose Food & Drink Report 2025-26 press release (2025-12-03), Whole Foods Market 2026 (2025-10-08), McCormick consumer Flavor of the Year press release (2025-12-09), Sanchez Romero (Spanish gourmet grocer, 2025-12-29).
Home scope: Madison.dk (Danish lifestyle magazine, 2026-04-27), Fine Dining Lovers ES (2026-01-26), Pinterest Predicts 2026 (2025-12-10).

## Couldn't open, or skipped
- Waitrose full report microsite (waitrose-foodanddrinkreport.com/report2025/): the content sits in an iframe, so I used the John Lewis Partnership press release instead.
- Tastewise 2026 global forecast: the page is a landing page and the report is gated. Only the UK menu-trends blog was usable.
- Nation's Restaurant News 2026 trends: only the headline themes were visible, so it is not in the CSV.
- gastronomistas.com: fetch timed out.
- Kalsec: I found no 2026 ingredient forecast (search returned only a beer piece), so I skipped it.
- Food Organisation of Denmark: I found no 2026 trends publication and skipped it. The only Danish source with ingredients is Madison.dk, a consumer and home-cooking magazine and a weak source. restaurant.dk (2025-12-14) names no ingredients, only operational trends.
- Monocle and Eater: I found no 2026 trends piece in search and did not look further.
- Michelin Spain page (guide.michelin.com/es/es/...tendencias-2026...): not opened. It looks like the Spanish version of the inspectors' article.

## Caveats
- The sources skew heavily to the US: Whole Foods, Datassential, Technomic, B+W, McCormick, JBF and Monin. None of them is about Copenhagen or Barcelona.
- Michelin is the only source that places ingredient trends in the three cities. It gives London (Plates London) as an example of bitterness/depth and Copenhagen (Sushi Anaba) as an example of "time is an ingredient" (koji, lacto-fermentation).
- Tastewise figures are proprietary "growth" metrics with no stated denominator. I left the numbers out of the CSV for that reason.
- Some sources are not independent. Tim Dela Cruz appears in both Restaurant Industry Magazine and the Morning Advertiser. Sanchez Romero's black currant echoes McCormick. The Restaurant Business rows restate other forecasters.

## Conflicts between forecasters
- Dubai chocolate: Waitrose lists it as declining. Bidfood and Rob Allcock (Morning Advertiser) list it as rising or elevated.
- Cauliflower: Waitrose lists it as declining. Rob Allcock calls it the vegetable of 2026.
- Chili crisp/crunch: B+W says the heat is being toned down, not that it is rising or falling. No other source names it.
- Hot honey: Great British Chefs, Bidfood and Monin see it continuing. B+W presents fermented honey as its more complex successor.
- Hojicha vs matcha: Technomic and Tastewise call hojicha the "next matcha", while Waitrose, Whole Foods and Bidfood still list matcha as rising.

## Ingredients named by more than one independent forecaster
The Restaurant Business attributions are counted under the forecaster it quotes.
- miso: MICHELIN Guide; Technomic (via RB); Monin (via RB); Bidfood; Madison.dk; Fine Dining Lovers ES
- kimchi: Baum + Whiteman; Technomic (swicy pairing); Bidfood; Madison.dk; Fine Dining Lovers ES
- matcha: Waitrose; Whole Foods; Bidfood; Tastewise; Booker (Karen Poole, via Morning Advertiser)
- pistachio: Bidfood; Tastewise; Sanchez Romero; Booker (via Morning Advertiser)
- hojicha: Technomic; Tastewise; Madison.dk
- fruit / flavoured vinegars: Whole Foods; James Beard Foundation chefs; Madison.dk; Sanchez Romero
- yuzu: Whole Foods; Bidfood; Sanchez Romero
- fermentation / lacto-fermentation (as a technique): James Beard Foundation chefs; MICHELIN Guide; Madison.dk; San Sebastian Gastronomika (theme)
- seaweed / sea greens: James Beard Foundation chefs; MICHELIN Guide; Madison.dk
- koji: James Beard Foundation chefs (in cocktails); MICHELIN Guide
- beef tallow / beef fat: Whole Foods; Baum + Whiteman. Madison.dk is broader, naming animal fats in general.
- cardamom: Baum + Whiteman; McCormick for Chefs
- hot honey: Great British Chefs; Bidfood; Monin (via RB)
- gochujang: Waitrose (gochujang hot honey product); Technomic (swicy pairing)
- ube: Datassential; Tim Dela Cruz (chef); Booker (via Morning Advertiser)
- tamarind: Tim Dela Cruz (chef); Bidfood
- pickles: Lumina Intelligence; Pinterest
- chipotle: Technomic; Sanchez Romero
- bitter leaves and bitterness: MICHELIN Guide. Waitrose is related (bitter aperitifs/flavours).
- Single-forecaster only, despite repeat mentions: black currant (McCormick, echoed by others), stracciatella / fermented black beans / huacatay (Datassential, in two of its own pieces).

## Candidate terms no forecaster named as a trend
None of the pages I opened named any of these as trend ingredients: garum, fish sauce, buckwheat, verjus, sea buckthorn, brown butter, cultured butter, pine, birch.
- Garum appears only as one experimental Madrid Fusion dish.
- Butter appears only generically: Waitrose names flavoured butter and Madison names quality butter.
