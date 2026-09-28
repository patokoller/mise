import re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

A="Arial"
HDR=Font(name=A,bold=True,color="FFFFFF",size=10); HF=PatternFill("solid",fgColor="333333")
BODY=Font(name=A,size=10); BOLD=Font(name=A,size=10,bold=True)
RED=Font(name=A,size=10,color="C00000",bold=True); GREY=Font(name=A,size=10,color="808080",italic=True)
TITLE=Font(name=A,size=13,bold=True); YELL=PatternFill("solid",fgColor="FFF2CC")
THIN=Border(bottom=Side(style="thin",color="D9D9D9"))

GM="Global Masters"; MA="Masters"; VF="Very Fine"; FI="Fine"; RE="Recommended"

D=[]
def add(t,rows):
    for n,a in rows: D.append((n,a,t))

add(GM,[("Alchemist","Refshalevej 173C, København"),("Alimentum","Løkkegade 23, Aalborg"),
("Alouette","Kronprinsessegade 8, København"),("Frederikshøj","Oddervej 19-21, Aarhus"),
("Frederiksminde","Klosternakken 8, Sjælland og øer / Præstø"),("Geranium","Per Henrik Lings Alle 4, 8., København"),
("Henne Kirkeby Kro","Strandvejen 234, Henne"),("Jordnær","Gentoftegade 29, København / Gentofte"),
("KOAN","Langeliniekaj 5, København / København"),("Kadeau Bornholm","Baunevej 18, Aakirkeby"),
("Kadeau København","Wildersgade 10B, København"),("Kong Hans Kælder","Vingårdstræde 6, København"),
("LYST","Havneøen 1, Midtjylland / Vejle"),("Lille Mølle","Christianshavns Voldgade 52, København"),
("Mota","Annebergparken 50,"),("Noma","Refshalevej 96, København"),
("Okê Restaurant","Hans Ruths Vej 1, Nordjylland / Skagen"),("PAZ","Doktara Jakobsens gøta 14, Tórshavn"),
("Restaurant AOC","Dronningens Tværgade 2, København / København"),("Restaurant Domæne","Gødstrupvej 60,"),
("Restaurant TRI","Vesterhavsvej 5A,"),("Ræst","Gongin 8, Færøerne / Tórshavn"),
("Studio","Paulas Passage 5, Carlsberg Byen, København"),("Sushi Anaba","Mariehamngade 23, København"),
("Svinkløv Badehotel","Svinkløvvej 593, Fjerritslev"),("Syttende","Nørre Havnegade 23,"),
("Søllerød Kro","Søllerødvej 35, Holte"),("Ti Trin Ned","Toldkammeret 9, Fredericia")])

add(MA,[("Admiralgade 26","Admiralgade 26, København / Copenhagen"),("Akmé","Sandkaj 39, København"),
("Anarki","Vodroffsvej 47, Frederiksberg c"),("Anx","Oddervej 19-21, Aarhus"),("Aro","Østerbro 32, Odense / Odense"),
("Aure","Krudtløbsvej 8, København"),("B-Spis","Sct Peders Kirkeplads 9, Sjælland og øer / Næstved"),
("Bach & Nurup","Budolfi Plads 32, Nordjylland / Aalborg"),("Barr","Strandgade 93, København / København"),
("Bistro Boheme","Esplanaden 8, København"),("Bobe","Gråbrødretorv 11, København"),("Calma","Jægersborggade 34, København"),
("Connection","Øster Farimagsgade 18, København / Copenhagen"),("Den Røde Cottage","Strandvejen 550, København / Klampenborg"),
("Det Røde Pakhus","Snellemark 30, Rønne"),("Domestic","Mejlgade 35B, Aarhus"),
("Dragsholm Slot Gourmet","Dragsholm Allé 1, Sjælland og øer / Hørve"),("Démodé","Kronprinsessegade 64, København"),
("ESSE","Trelleborggade 13A / 13B, Sjælland og øer / Köpenhamn"),("Esmée","Kongens Nytorv 8, København / Copenhagen"),
("Falsled Kro","Assensvej 513, Millinge"),("Fasangården","Søndre Fasanvej 73, København / Copenhagen"),
("Formel B","Vesterbrogade 184, Frederiksberg"),("Fútastova","Gongin 5, Færøerne / Tórshavn"),
("Gastromé","Grenåvej 127, Aarhus"),("Grim","Ryesgade 65, Köpenhamn"),("HOS","Kongensgade 65, Odense"),
("HimmerRiget","Lars Larsens Vej 1,"),("Hærværk","Frederiks Allé 105, st. tv, Aarhus"),
("JATAK","Rantzausgade 39, København"),("Kanalen","Wilders Plads 2, København / Copenhagen"),
("Kødbyens Fiskebar","Flæsketorvet 100, København / Copenhagen"),("La Banchina","Refshalevej 141A, København / Copenhagen"),
("Lieffroy","Hesselhuset, Skræddergyden 34, Nyborg"),("Lumskebugten","Esplanaden 21, Copenhagen / Copenhagen"),
("Madeleine","Vestergade 5, Fyn og øer / Odense"),("Marchal","Hotel d'Angleterre, Kongens Nytorv 34, København"),
("Mielcke & Hurtigkarl","Frederiksberg Runddel 1, Frederiksberg"),("Miró","Marstrandsgade 2, Aarhus"),
("Molskroen","Hovedgaden 16, Midtjylland / Ebeltoft"),("Møntergade","Møntergade 19, København"),
("No. 2","Nicolai Eigtvedsgade 32, København / Copenhagen"),("Opulent","Guldsmedgade 33, Midtjylland / Aarhus c"),
("Parsley Salon","Strandvejen 203, København / Hellerup"),("Restaurant Levi","Ny Østergade 24, København"),
("Restaurant Vie","Århusgade 128E, København"),("Roks","Gongin 5,"),("Ruths Gourmet","Hans Ruths Vej 1, Skagen"),
("Scheelsminde","Scheelsmindevej 35, Aalborg"),("Schønnemann","Hauser Plads 16-18, København / Copenhagen"),
("Sdr. Bjert Kro","Gamle Bjert 16, Sønderjylland"),("Selma","Rømersgade 20, København / Copenhagen"),
("Stammershalle Badehotel","Sdr. Strandvej 128, Bådsted, Bornholm / Gudhjem"),
("Substans","Mariane Thomsens Gade 2F, 11.1, Aarhus / Aarhus"),("Sønderho Kro","Kropladsen 11, Midtjylland / Fanø"),
("The Pescatarian","Amaliegade 49, København / Copenhagen"),("The Samuel","Hellerupvej 40, København / Hellerup"),
("The Tarv","Undir Bryggjubakka 3-5, Færøerne / Tórshavn"),("Treetop","Munkebjergvej 125, Midtjylland / Vejle"),
("Trio","Jernbanegade 11, København"),("Udtryk","Teglgårdsstræde 8 A, København"),
("Vallø Slotskro","Slotsgade 1, Sjælland og øer / Køge"),("Vendia Gourmet","Markedsgade 9, Nordjylland / Hjørring"),
("VesterVenner - Strandgården Badehotel","Havnepladsen 5,"),("Villa Vest","Strandvejen 138, Lønstrup"),
("À Terre","Tordenskjoldsgade 11, København"),("ÅBEN","Slagtehusgade 15, København")])

add(VF,[("Address","Tuborg Havnepark 15, København / Hellerup"),("Alf","Gammel Kongevej 86A, Frederiksberg c"),
("Ambra","Store Kongensgade 59, København"),("Amstrup & Vigen (Dyvig Badehotel)","Dyvig Badehotel, Dyvigvej 31, Sønderjylland / Nordborg"),
("Anarki","Vodroffsvej 47, Frederiksberg c"),("Anton","Store Strandstræde 3, København"),
("Apéro","Gammel Mønt 41, København"),("Ark","Nørre Farimagsgade 63, København / Copenhagen"),
("Baka d'Busk","Rantzausgade 44, København / Copenhagen"),("Bar La Una","Oehlenschlægersgade 53A, København / Copenhagen"),
("Bar Moro","Blegdamsvej 36, København"),("Bar Piatto","Mejlgade 33, Midtjylland / Aarhus c"),
("Barabba","Store Kongensgade 34, København"),("Bavn","Helga Pedersen Gade 79, 44., Aarhus / Aarhus"),
("Bitin","Niels Finsens Gøta 12, Færøerne / Tórshavn"),("Boutique Emilia","Frederiksholms Kanal 4, København"),
("Brasserie Post","Øster Allé 1, København"),("Brus","Guldbergsgade 29F, København / Copenhagen"),
("Brøndums Hotel","Anchersvej 3, Nordjylland / Skagen"),("Café Sommersko","Palægade 2-6, København / København"),
("Christianshøjkroen","Segenvej 48, Bornholm / Aakirkeby"),("Cleo","Rantzausgade 58b, København"),
("Damindra","Holbergsgade 26, København / Copenhagen"),("Donda SOLÈNE","Århusgade 1, København"),
("Enomania","Vesterbrogade 187, Frederiksberg"),("Etika","Heiðavegur 35,"),("Fiskastykkid","12 Úti á Bakka,"),
("Fojetta","Borups Allé 112, Frederiksberg"),("Fusion","Strandvejen 4, Aalborg / Aalborg"),
("Ghrelin","Dagmar Petersens Gade 111, Aarhus c"),("Goldfinch","Kongens Nytorv 8, København"),
("Graziano","Møllegade 13, København"),("Hos Fischer","Victor Borges Plads 12, København"),
("Hummer","Nyhavn 63A, København / Copenhagen"),("Húsagardur","Oknarvegur 2,"),("JUJU","Øster Farimagsgade 8, København"),
("Kappo Ando","Øster Farimagsgade 93, København"),("Kiin Kiin","Guldbergsgade 21, København / Copenhagen"),
("Kiin Kiin Tok Tok","Vesterbrogade 55, København / Copenhagen"),("Lago","Korsgade 1, København"),
("Lamar","Gammel Kongevej 27, København"),("Le Saint Jacques","Sankt Jakobs Plads 1, Copenhagen / Copenhagen"),
("Locale 21","Ny Østergade 21, København"),("Maison","Dronningens Tværgade 43, Copenhagen / Copenhagen"),
("Margo","Vesterbrogade 38, København / København"),("Marv & Ben","Snaregade 4, København / Copenhagen"),
("Melsted Badehotel","Melstedvej 27, Gudhjem"),("Mirabelle","Guldbergsgade 29A, København"),("Moment","Ravnen 1, Rønde"),
("Mundheld","Torvegade 24, Midtjylland / Esbjerg"),("Møf","Vesterport 10, Aarhus"),("Nr. 30","Nansensgade 30, København"),
("Oberra","Skjolds Plads 2-4, København"),("Paesàno","Jægersborggade 41, København"),("Pauli","Borgbjergsvej 13, København"),
("Piola Pastificio","Thorvaldsensvej 2C, Frederiksberg"),("Pirlo Vinbar","Strandlodsvej 42a, København"),
("Pluto","Borgergade 16, København"),("Pomle Nakke","Midtskovvejen 1, Sjælland og øer"),
("Propaganda - next door","Vester Farimagsgade 2, København / København"),("Restaurant ET","Mindegade 8, Aarhus / Aarhus"),
("Restaurant Mark","Axeltorv 3, København / København"),("Resto Bar","Vesterbrogade 51, København"),
("Ribehøj","Ribevej 34, Bobøl, Føvling"),("Ripotot","Store Kongensgade 56, København"),
("Ruts Restaurant","Oyggjarvegur 45, Færøerne"),("Rørvig Kro","Toldbodvej 55,"),("SURT","Bag Elefanterne 2, København"),
("Sankt Annæ","Sankt Annæ Plads 12, Copenhagen"),("Silberbauers Bistro","Jægersborggade 40, København / Copenhagen"),
("Silo","Helsinkigade 29, København / Copenhagen"),("Skipperhuset","Skipper Allé 6, Fredensborg"),
("Sola","Havnepladsen 5, Vesterø Havn, Nordjylland"),("Strandhotellet Blokhus","Sønder i By 2, Nordjylland / Blokhus"),
("Svogerslev Kro","Svogerslev Hovedgade 45, Roskilde"),("Toto","Amagerbrogade 145, København / Copenhagen"),
("Tèrra","Ryesgade 65, København"),("Under Lindetræet","Ramsherred 2, Odense c"),
("[NAME MISSING AT SOURCE]","Västergatan 18B, Skåne / Malmö"),("Yves at Park Lane","Strandvejen 203, Hellerup"),
("Áarstova","Gongin 1, Tórshavn")])

add(FI,[("Bageri & Bistro","Kærvej 2, Midtjylland / Randers"),("Bottega Barlie","Fredericiagade 78, København"),
("Brasserie Barner","Århusgade 1, København / Copenhagen"),("Bæst","Guldbergsgade 29, København / København"),
("Delphine","Vesterbrogade 40, København"),("Donda Deli","Dybbølsgade 52, København / København"),
("Freia","Nørre Havnegade 25, Sønderjylland / Sønderborg"),("Gaarden & Gaden","Nørrebrogade 88, København / Copenhagen"),
("Gabrielle","Vestergade 3, København"),("Gammel Brydegaard","Helnæsvej 4, Fyn og øer / Haarby"),
("Katrina Christiansen","Bringsnagøta 6,"),("Le Lac","Classensgade 11A, Copenhagen / Copenhagen"),
("Ma Cuisine","Ravnsborggade 19, København"),("Noels","Sigurdsgade 39, København"),
("Noi","Niels Brocks Gade 1, København / Copenhagen"),("Odette","Kompagnistræde 18, København"),
("Râzapâz","Store Torvegade 29, Bornholm / Rønne"),("Safari","Baggesensgade 9, København / Copenhagen"),
("Seaside Toldboden","Nordre Toldbod 18-24, København / Copenhagen"),("Skeiva Pakkhús","Sigmundargøta 19, Tórshavn"),
("Told & Snaps","Toldbodgade 2, København / Copenhagen")])

add(RE,[("Masseria","Flæsketorvet 50-52, Copenhagen / Copenhagen"),("Mejerigaarden","Gl. Landevej 87, Sjælland og øer / Gedser"),
("Royal Garden","Dronningens Tværgade 30, København / Copenhagen")])

# --- D-037 reconciliation ---
counts = {}
for _,_,t in D: counts[t]=counts.get(t,0)+1
EXPECT = {GM:28, MA:67, VF:81, FI:21, RE:3}
assert counts==EXPECT, (counts, EXPECT)
assert len(D)==200, len(D)
names=[n for n,_,_ in D]
dupes=sorted({n for n in names if names.count(n)>1})
assert dupes==["Anarki"], dupes
print("D-037 reconciliation PASSED:", counts, "| rows", len(D), "| unique venues", len(set(names)))

# --- provisional area flag from the address string only ---
OUT_TOWNS = ["Hellerup","Gentofte","Klampenborg","Holte","Malmö","Skåne","Tórshavn","Færøerne",
             "Aarhus","Aalborg","Odense","Bornholm","Rønne","Skagen","Vejle","Randers","Esbjerg",
             "Fredericia","Nyborg","Millinge","Henne","Fjerritslev","Roskilde","Køge","Næstved",
             "Hørve","Præstø","Gedser","Fredensborg","Rønde","Ebeltoft","Gudhjem","Aakirkeby",
             "Fanø","Hjørring","Lønstrup","Blokhus","Sønderjylland","Nordborg","Haarby","Sønderborg",
             "Føvling","Nordjylland","Midtjylland","Fyn og øer","Vesterø"]
def flag(addr):
    if not addr.strip() or addr.strip().endswith(","): return "UNRESOLVABLE — no locality at source"
    for t in OUT_TOWNS:
        if t in addr: return "likely OUTSIDE"
    if "København" in addr or "Copenhagen" in addr or "Köpenhamn" in addr or "Frederiksberg" in addr:
        return "likely IN — resolve"
    return "UNKNOWN — resolve"

wb=Workbook(); ws=wb.active; ws.title="wg_a2_candidates"
ws["A1"]="WHITE GUIDE DENMARK — ROUTE A2 CANDIDATE LIST"; ws["A1"].font=TITLE
ws["A2"]=("Complete national list as at retrieval. NOT filtered to Copenhagen and NOT resolved to addresses. "
          "The 'provisional area' column is derived from the source's own address string and is NOT an F1 verdict.")
ws["A2"].font=GREY

COLS=[("venue_name",30),("address_raw",46),("route_a2_tier",15),("provisional_area",30),
      ("kommune",18),("address_resolved",34),("google_place_id",30),
      ("route_a1",9),("in_cohort",10),("excluded_reason",18),
      ("frame_date",11),("source_url",52),("observed_at",12),("retrieved_at",12),("added_by",10),("notes",52)]
r=4
for i,(n,w) in enumerate(COLS,start=1):
    c=ws.cell(row=r,column=i,value=n); c.font=HDR; c.fill=HF
    c.alignment=Alignment(vertical="center",wrap_text=True)
    ws.column_dimensions[get_column_letter(i)].width=w
ws.row_dimensions[r].height=30; ws.freeze_panes="B5"

SRC="https://whiteguide.com/dk/da/search?query=&type=restaurant&execute=true"
NOTE={"Anarki":"CONFLICT AT SOURCE: venue ID 9638 is classified both Very Fine and Masters. route_a2_tier undecidable — operator judgement required.",
 "[NAME MISSING AT SOURCE]":"Source renders this entry with no venue name; the address occupies the name field. F0 cannot resolve it as listed.",
 "Noma":"Listed by White Guide at Global Masters. Absent from MICHELIN's 2026 Copenhagen selection — A2 catching what A1 drops.",
 "ESSE":"Source files this under region 'Sjælland og øer / Köpenhamn' — region labels are inconsistent and unusable as a boundary.",
 "Grim":"Source gives locality as 'Köpenhamn' (Swedish spelling).",
 "Address":"Venue is literally named 'Address'. Not a parsing artefact."}
r=5
for n,a,t in D:
    fl=flag(a)
    vals=[n,a,t,fl,"TO RESOLVE","TO RESOLVE","TO RESOLVE","","FALSE","","2026-07-28",SRC,"2026-07-30","2026-07-30","claude",NOTE.get(n,"")]
    for i,v in enumerate(vals,start=1):
        c=ws.cell(row=r,column=i,value=v); c.font=BODY; c.border=THIN
        c.alignment=Alignment(vertical="top",wrap_text=(i in (2,12,16)))
    if n in ("Anarki","[NAME MISSING AT SOURCE]"): ws.cell(row=r,column=16).font=RED
    if fl.startswith("likely OUTSIDE"): ws.cell(row=r,column=4).font=GREY
    if fl.startswith("UNRESOLVABLE") or fl.startswith("UNKNOWN"): ws.cell(row=r,column=4).font=RED
    r+=1
last=r-1

r+=1
ws.cell(row=r,column=1,value="COUNTS — every one states its denominator").font=BOLD; r+=1
S=[("Rows (one per tier listing)",f'=COUNTA(A5:A{last})'),
   ("Unique venues",f'=COUNTA(A5:A{last})-1'),
   ("  Global Masters",f'=COUNTIF(C5:C{last},"Global Masters")'),
   ("  Masters",f'=COUNTIF(C5:C{last},"Masters")'),
   ("  Very Fine",f'=COUNTIF(C5:C{last},"Very Fine")'),
   ("  Fine",f'=COUNTIF(C5:C{last},"Fine")'),
   ("  Recommended",f'=COUNTIF(C5:C{last},"Recommended")'),
   ("Provisionally IN Copenhagen/Frederiksberg — needs resolution",f'=COUNTIF(D5:D{last},"likely IN — resolve")'),
   ("Provisionally outside",f'=COUNTIF(D5:D{last},"likely OUTSIDE")'),
   ("No usable locality at source",f'=COUNTIF(D5:D{last},"UNRESOLVABLE — no locality at source")+COUNTIF(D5:D{last},"UNKNOWN — resolve")')]
for lab,f in S:
    ws.cell(row=r,column=1,value=lab).font=BODY
    c=ws.cell(row=r,column=2,value=f); c.font=BOLD; c.fill=YELL
    r+=1
r+=1
ws.cell(row=r,column=1,value=("D-037 reconciliation PASSED: tier subtotals 28/67/81/21/3 sum to 200 listing rows against 199 unique venues "
                              "(Anarki is classified twice). Rendered rows were 203; three within-tier duplicate renders removed.")).font=BOLD

lg=wb.create_sheet("legend")
lg.column_dimensions["A"].width=30; lg.column_dimensions["B"].width=100
lg["A1"]="How to read this file"; lg["A1"].font=TITLE
rows=[("What this is","The complete White Guide Denmark listing, tier-labelled. Route A2 candidates before any filter."),
("What it is not","Not the Copenhagen A2 frame. No F0 resolution, no F1, no route union with A1."),
("provisional_area","Derived from the source's own address string ONLY. It is a work-sorting aid, not an F1 verdict. "
 "White Guide uses 'København' as a REGION prefix — 'København / Hellerup' and 'København / Gentofte' are outside the boundary. "
 "The same trap as Michelin's city labels, in a different form."),
("Why 200 rows, 199 venues","Anarki appears in two tiers with two classifications from one venue ID. Both rows are kept visible rather than silently merged."),
("Source","whiteguide.com search, retrieved 2026-07-30, proxy=basic. No robots.txt exists; pages are index,follow. "
 "Classification filtering is client-side, so tier views have no citable URL — the source_url column holds the unfiltered list URL for every row."),
("Vintage","Per D-033 the stored snapshot IS the edition; retrieved_at 2026-07-30 is the vintage. White Guide publishes no dated edition."),
("Assertion","Per D-037, tier subtotals reconcile to the full list. This proves internal completeness, not that the publisher's database is fully exposed."),
("Red text","Needs a human. Two rows: Anarki's conflicting tier, and one entry the source renders with no name.")]
r=2
for a,b in rows:
    lg.cell(row=r,column=1,value=a).font=BOLD
    c=lg.cell(row=r,column=2,value=b); c.font=BODY
    c.alignment=Alignment(wrap_text=True,vertical="top"); lg.row_dimensions[r].height=44
    r+=1

wb.save("/mnt/user-data/outputs/cph-route-a2-candidates.xlsx")
print("saved")
