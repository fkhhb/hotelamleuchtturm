#!/usr/bin/env python3
"""Baut den Konzeptentwurf Hotel am Leuchtturm (statische Seiten) in die Repo-Wurzel.

Aufruf: python3 quelle/build_site.py
assets/site.css, assets/site.js und img/ werden nicht erzeugt, sondern direkt bearbeitet."""
import json, os, html
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Repo-Wurzel = Website
REAL = "https://www.hotel-am-leuchtturm.de"
LIVE = "https://hotelamleuchtturm.mndst.co"  # Adresse dieses Entwurfs
TODAY = "2026-10-30"
TEL, TEL_HREF, MAIL = "0381 5 43 70", "+4938154370", "info@hotel-am-leuchtturm.de"
e = html.escape

ROOMS = [
 dict(slug="panorama-terrassen-doppelzimmer", old="hotel-zimmer/panorama-terrassen-dz.html", name="Panorama-Terrassen-Doppelzimmer",
      tag="Direkter Ostseeblick und 40 m² Dachterrasse", view="Direkter Ostseeblick", floor="1. Etage", size="20 m² (ohne Bad)",
      bed="Doppelbett 180 × 200 cm, Komforthöhe, elektrisch verstellbarer Lattenrost", occ="max. 2 Erwachsene",
      bath="Dusche oder Dusche und Badewanne", prices=(269,309,339), imgs=["ptdz-5","ptdz-2","ptdz-3","ptdz-1"],
      special="Das Highlight: die 40 m² große Dachterrasse – in der Sommersaison mit Strandkorb, zwei Liegen und weiteren Sitzmöglichkeiten – und der direkte Blick auf die Ostsee.",
      banner="stage-4"),
 dict(slug="panorama-doppelzimmer", old="hotel-zimmer/panorama-dz.html", name="Panorama-Doppelzimmer",
      tag="Direkter Ostseeblick aus der 2. und 3. Etage", view="Direkter Ostseeblick", floor="2. und 3. Etage", size="20 m² (ohne Bad)",
      bed="Doppelbett 180 × 200 cm, Komforthöhe, elektrisch verstellbarer Lattenrost", occ="max. 2 Erwachsene",
      bath="Dusche oder Dusche und Badewanne", prices=(259,289,319), imgs=["pdz-4","pdz-1","pdz-2","pdz-3"],
      special="Lichtdurchflutet, mit direktem Blick auf Strand und Ostsee – bei Sonnenuntergang einer der schönsten Ausblicke Warnemündes.", banner=None),
 dict(slug="terrassen-doppelzimmer", old="hotel-zimmer/terrassen-dz.html", name="Terrassen-Doppelzimmer",
      tag="Eigene 12 m² Dachterrasse", view="Seitlicher Ostseeblick oder Blick auf Leuchtturm mit Hafeneinfahrt", floor="1. Etage", size="17–20 m² (ohne Bad)",
      bed="Doppelbett 180 × 200 cm, Komforthöhe", occ="max. 2 Erwachsene", bath="Dusche", prices=(219,259,299), imgs=["tdz-1","tdz-3","tdz-4","tdz-2"],
      special="Das Besondere: die 12 m² Dachterrasse, in der Sommersaison mit einer Liege und Sitzmöglichkeiten möbliert.", banner=None),
 dict(slug="komfort-doppelzimmer", old="hotel-zimmer/dz-mit-ostseeblick.html", name="Komfort-Doppelzimmer",
      tag="Seitlicher Ostseeblick oder Leuchtturmblick", view="Seitlicher Ostseeblick oder Blick auf Leuchtturm mit Hafeneinfahrt", floor="1., 2. und 3. Etage", size="17–20 m² (ohne Bad)",
      bed="Doppelbett 180 × 200 cm, Komforthöhe, teilweise extra lang (2,10 m)", occ="max. 2 Erwachsene", bath="Dusche", prices=(209,239,279), imgs=["kdz-2","kdz-1","kdz-3"],
      special="Viel Platz im klassisch-modernen Boutiquestil – mit Blick zur Ostsee oder auf das Wahrzeichen Warnemündes.", banner=None),
 dict(slug="doppelzimmer", old="hotel-zimmer/doppelzimmer2.html", name="Doppelzimmer",
      tag="Gemütlich unter dem Dach", view="Dachgeschoss mit elektrisch verstellbaren Dachfenstern", floor="3. Etage", size="15–18 m² (ohne Bad)",
      bed="Doppelbett 180 × 200 cm, Komforthöhe", occ="max. 2 Erwachsene", bath="Dusche", prices=(179,209,229), imgs=["dz-4","dz-5","dz-3"],
      special="Individuell geschnittene Zimmer mit leichter Dachschräge – behaglich, ruhig und mitten in Warnemünde.", banner=None),
 dict(slug="einzelzimmer", old="hotel-zimmer/einzelzimmer.html", name="Einzelzimmer",
      tag="Queensize-Bett unter dem Dach", view="Dachgeschoss mit elektrisch verstellbaren Dachfenstern", floor="3. Etage", size="15–18 m² (ohne Bad)",
      bed="Queensize-Bett 100 × 200 cm, Komforthöhe", occ="1–2 Erwachsene", bath="Dusche", prices=(139,159,199), imgs=["ez-1","ez-2","ez-4","ez-3"],
      special="Ideal für Alleinreisende: individuell geschnitten mit leichter Dachschräge und Queensize-Bett.", banner=None,
      warn="Bitte prüfen: Die heutige Zimmerseite nennt ein „Queensize-Bett (100 × 200 cm)“ und „1–2 Erwachsene“. 100 cm ist ein Einzelbett, ein Queensize-Bett hat 140–160 cm. Bettbreite und Belegung klären – die Angaben hier sind 1 : 1 übernommen."),
]
COMMON = ["Schwenkbarer HD-Flatscreen-Sat-TV mit Radio", "USB-Steckdosen an Nachttisch und Schreibtisch", "Großer Schreibtisch", "2 Sessel mit Beistelltischchen",
          "Großer beleuchteter Kleiderschrank", "Zimmersafe", "Beheizter Handtuchhalter, Kosmetikspiegel, Föhn, Pflegeprodukte", "Kostenloses WLAN",
          "24-Stunden-Rezeption und Weckruf"]

MENU = [("zimmer/index.html","Zimmer"),("apartments.html","Apartments"),("angebote/index.html","Angebote"),("lage-anfahrt.html","Lage"),("geschichte.html","Geschichte")]

HOTEL_LD = {
 "@context":"https://schema.org","@type":"Hotel","name":"Hotel am Leuchtturm","url":REAL+"/",
 "description":"Inhabergeführtes Boutique-Hotel an der Strandpromenade von Warnemünde, direkt am Leuchtturm. 30 Zimmer, Frühstückslounge mit Promenadenblick, Lobby mit Kamin.",
 "address":{"@type":"PostalAddress","streetAddress":"Am Leuchtturm 16","postalCode":"18119","addressLocality":"Rostock-Warnemünde","addressCountry":"DE"},
 "telephone":"+49 381 54370","email":MAIL,"checkinTime":"15:00","checkoutTime":"11:00","numberOfRooms":30,"petsAllowed":False,
 "foundingDate":"1850","priceRange":"139–339 € pro Zimmer und Nacht (ohne Frühstück)",
 "amenityFeature":[{"@type":"LocationFeatureSpecification","name":n,"value":True} for n in ["Kostenloses WLAN","24-Stunden-Rezeption","Frühstückslounge","Lobby mit Kamin","Zimmer mit Dachterrasse"]],
}

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

# ---------- Sprachen ----------
EN_SLUG = {"panorama-terrassen-doppelzimmer":"panorama-terrace-double-room","panorama-doppelzimmer":"panorama-double-room",
           "terrassen-doppelzimmer":"terrace-double-room","komfort-doppelzimmer":"comfort-double-room",
           "doppelzimmer":"double-room","einzelzimmer":"single-room"}
PAIRS = {"index.html":"en/index.html","zimmer/index.html":"en/rooms/index.html","apartments.html":"en/apartments.html",
         "angebote/index.html":"en/offers/index.html","angebote/wintertage-in-warnemuende.html":"en/offers/winter-days-in-warnemuende.html",
         "geschichte.html":"en/history.html","lage-anfahrt.html":"en/location.html","galerie.html":"en/gallery.html","buchen.html":"en/book.html"}
PAIRS.update({f"zimmer/{de}.html": f"en/rooms/{en}.html" for de,en in EN_SLUG.items()})
PAIRS.update({"angebote/hanse-sail.html":"en/offers/hanse-sail.html","angebote/kreuzfahrt.html":"en/offers/cruise.html","gutscheine.html":"en/vouchers.html"})
PAIRS_INV = {v:k for k,v in PAIRS.items()}

def ui(lang, R):
    if lang == "en":
        return dict(
          menu=[("en/rooms/index.html","Rooms"),("en/apartments.html","Apartments"),("en/offers/index.html","Offers"),("en/location.html","Location"),("en/history.html","History")],
          concept=f'<b>Concept draft</b> for a new website of Hotel am Leuchtturm – not the hotel\'s official site. Availability and marked values are demo. Real booking: <a href="{REAL}/EN/home.html">hotel-am-leuchtturm.de</a>',
          notes="Hide notes", home="Hotel am Leuchtturm – home", logo_alt="Hotel am Leuchtturm – since 1850 in Warnemünde", menu_label="Menu",
          book=("en/book.html","Book now"), mbar=("From €139 per night","Best rate when booking direct","Book","Continue"),
          f_since="Since 1850 in Warnemünde", f_tel="Phone",
          f_hotel=("Hotel", [("en/rooms/index.html","Rooms &amp; rates"),("en/apartments.html","Apartment house"),("en/offers/index.html","Offers"),("en/vouchers.html","Gift vouchers"),("en/gallery.html","Gallery")]),
          f_service=("Service", [("en/location.html","Location &amp; directions"),("en/index.html#faq","FAQ"),("en/history.html","History"),("en/book.html","Book online")]),
          f_legal=("Legal", [(f"{REAL}/DE/ueber-uns/impressum1.html","Hotel imprint"),(f"{REAL}/DE/ueber-uns/datenschutz.html","Privacy"),(f"{REAL}/DE/ueber-uns/agbs.html","Terms")]),
          fnote=f'Concept draft for a redesign of hotel-am-leuchtturm.de · Content, room data and 2026 rates from the hotel\'s current website; availability, breakfast price, visitor\'s tax and items marked "proposal" are examples. Photos © Hotel am Leuchtturm. · <a href="{R}impressum.html">Imprint of this draft</a>',
          photo="Photo", og="en_GB")
    return dict(
      menu=[("zimmer/index.html","Zimmer"),("apartments.html","Apartments"),("angebote/index.html","Angebote"),("lage-anfahrt.html","Lage"),("geschichte.html","Geschichte")],
      concept=f'<b>Konzeptentwurf</b> für eine neue Website des Hotel am Leuchtturm – keine offizielle Seite. Verfügbarkeiten und markierte Werte sind Demo. Echte Buchung: <a href="{REAL}/DE/home.html">hotel-am-leuchtturm.de</a>',
      notes="Hinweise ausblenden", home="Hotel am Leuchtturm – Startseite", logo_alt="Hotel am Leuchtturm – seit 1850 in Warnemünde", menu_label="Menü",
      book=("buchen.html","Jetzt buchen"), mbar=("Ab 139 € pro Nacht","Bestpreis bei Direktbuchung","Buchen","Weiter"),
      f_since="Seit 1850 in Warnemünde", f_tel="Tel.",
      f_hotel=("Hotel", [("zimmer/index.html","Zimmer &amp; Preise"),("apartments.html","Apartmenthaus"),("angebote/index.html","Angebote"),("gutscheine.html","Gutscheine"),("galerie.html","Galerie")]),
      f_service=("Service", [("lage-anfahrt.html","Lage &amp; Anfahrt"),("index.html#fragen","Häufige Fragen"),("geschichte.html","Geschichte"),("buchen.html","Online buchen")]),
      f_legal=("Rechtliches", [(f"{REAL}/DE/ueber-uns/impressum1.html","Impressum des Hotels"),(f"{REAL}/DE/ueber-uns/datenschutz.html","Datenschutz"),(f"{REAL}/DE/ueber-uns/agbs.html","AGB")]),
      fnote=f'Konzeptentwurf zur Neugestaltung von hotel-am-leuchtturm.de · Inhalte, Zimmerdaten und Preise 2026 von der aktuellen Website des Hotels; Verfügbarkeiten, Frühstückspreis, Kurtaxe und als „Vorschlag“ markierte Leistungen sind Beispiele. Fotos © Hotel am Leuchtturm. · <a href="{R}vorschlag/index.html">Technik-Paket (Sitemap, robots.txt, llms.txt, Weiterleitungen)</a> · <a href="{R}impressum.html">Impressum dieses Entwurfs</a>',
      photo="Foto", og="de_DE")

def page(path, title, desc, body, active="", schema=None, mbar=True, mbar_href=None, lang="de"):
    depth = path.count("/")
    R = "../" * depth
    U = ui(lang, R)
    link = lambda h: h if h.startswith("http") else R + h
    nav = "".join(f'<li><a href="{R}{h}"{" aria-current=page" if h==active else ""}>{t}</a></li>' for h,t in U["menu"])
    sch = ld(schema) if schema else ""
    de_path = path if lang == "de" else PAIRS_INV.get(path)
    en_path = PAIRS.get(path) if lang == "de" else path
    if lang == "en" and not de_path: de_path = "index.html"
    if lang == "de" and not en_path: en_path = "en/index.html"
    alts = (f'<link rel="alternate" hreflang="de" href="{LIVE}/{de_path}">\n<link rel="alternate" hreflang="en" href="{LIVE}/{en_path}">\n<link rel="alternate" hreflang="x-default" href="{LIVE}/{de_path}">') if (path in PAIRS or path in PAIRS_INV) else ""
    langsw = (f'<span class="lang"><a href="{R}{de_path}" hreflang="de" lang="de"{" aria-current=true" if lang=="de" else ""}>DE</a> | '
              f'<a href="{R}{en_path}" hreflang="en" lang="en"{" aria-current=true" if lang=="en" else ""}>EN</a></span>')
    m = U["mbar"]
    mb = f'<div class="mbar"><span id="mbar-txt"><b>{m[0]}</b>{m[1]}</span><a class="btn btn-navy" href="{mbar_href or R + U["book"][0]}">{m[3] if mbar_href else m[2]}</a></div>' if mbar else ""
    fcol = lambda c: f'<div><h4>{c[0]}</h4><p>' + "<br>".join(f'<a href="{link(h)}">{t}</a>' for h,t in c[1]) + '</p></div>'
    doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
{alts}
<meta property="og:type" content="website">
<meta property="og:locale" content="{U['og']}">
<meta property="og:site_name" content="Hotel am Leuchtturm – Konzeptentwurf">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{LIVE}/img/hero-promenade-960.jpg">
<meta property="og:image:width" content="960"><meta property="og:image:height" content="576">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#00284b">
<link rel="icon" href="{R}img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/site.css">
{sch}
</head>
<body class="notes" data-root="{R}">
<div class="concept" role="note"><span>{U['concept']}</span><button type="button" id="toggleNotes">{U['notes']}</button></div>
<header class="top"><div class="wrap bar">
  <a class="brand" href="{R}{'en/index.html' if lang=='en' else 'index.html'}" aria-label="{U['home']}"><img src="{R}img/logo-header.jpg" alt="{U['logo_alt']}" width="248" height="100"></a>
  <ul class="menu" id="menu">{nav}</ul>
  {langsw}
  <a class="btn btn-navy" href="{R}{U['book'][0]}">{U['book'][1]}</a>
  <button class="burger" type="button" aria-label="{U['menu_label']}" aria-controls="menu" aria-expanded="false"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
  <div class="fcols">
    <div><div class="fbrand">Hotel am Leuchtturm<small>{U['f_since']}</small></div>
      <p style="margin-top:18px">Am Leuchtturm 16<br>18119 Rostock-Warnemünde{'<br>Germany' if lang=='en' else ''}<br>{U['f_tel']} <a href="tel:{TEL_HREF}">{TEL if lang=='de' else '+49 381 54370'}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    {fcol(U['f_hotel'])}
    {fcol(U['f_service'])}
    {fcol(U['f_legal'])}
  </div>
  <div class="fnote">{U['fnote']}</div>
</div></footer>
{mb}
<div class="lightbox" id="lightbox" role="dialog" aria-label="{U['photo']}"><img alt=""></div>
<div class="toast" id="toast" role="status"></div>
<script src="{R}assets/site.js"></script>
</body>
</html>
"""
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(doc)

def searchbox(R, prefill_room=""):
    opts = "".join(f'<option value="{r["slug"]}"{" selected" if r["slug"]==prefill_room else ""}>{r["name"]}</option>' for r in ROOMS)
    return f"""<form class="searchbox" id="search" autocomplete="off">
  <div class="field"><label for="s-arr">Anreise</label><input type="date" id="s-arr" required></div>
  <div class="field"><label for="s-dep">Abreise</label><input type="date" id="s-dep" required></div>
  <div class="field"><label for="s-ad">Gäste</label><select id="s-ad"><option value="1">1 Erwachsener</option><option value="2" selected>2 Erwachsene</option></select></div>
  <div class="field"><label for="s-room">Zimmer</label><select id="s-room"><option value="">Alle Zimmer</option>{opts}</select></div>
  <button class="btn btn-navy" type="submit">Verfügbarkeit prüfen</button>
</form>"""

def card(r, R):
    p = r["prices"]
    return f"""<article class="card">
  <a class="ph" href="{R}zimmer/{r['slug']}.html"><img src="{R}img/{r['imgs'][0]}.jpg" alt="{e(r['name'])}" loading="lazy"></a>
  <div class="bd">
    <h3><a href="{R}zimmer/{r['slug']}.html">{e(r['name'])}</a></h3>
    <ul class="chips"><li>{e(r['view'].split(' mit Hafen')[0])}</li><li>{e(r['size'].replace(' (ohne Bad)',''))}</li>{'<li>40 m² Dachterrasse</li>' if 'panorama-terrassen' in r['slug'] else '<li>12 m² Dachterrasse</li>' if r['slug']=='terrassen-doppelzimmer' else ''}</ul>
    <div class="from">ab <b>{p[0]} €</b> pro Nacht · ohne Frühstück</div>
    <div><div class="slots-h">Nächste freie Termine <span class="demo">Demo</span></div><div class="slots" data-slots="{r['slug']}"></div></div>
    <div class="acts"><a class="btn btn-line" href="{R}zimmer/{r['slug']}.html">Details</a><a class="btn btn-navy" href="{R}buchen.html?room={r['slug']}&amp;step=1">Buchen</a></div>
  </div>
</article>"""

FAQ = [
 ("Wann kann ich einchecken und auschecken?", "Ihr Zimmer steht am Anreisetag ab 15 Uhr bereit und am Abreisetag bis 11 Uhr. Die Rezeption ist rund um die Uhr besetzt."),
 ("Ist das Frühstück im Zimmerpreis enthalten?", "Die Zimmerpreise gelten ohne Frühstück. Das Frühstücksbuffet in der Frühstückslounge mit Blick auf die Promenade können Sie bei der Buchung hinzufügen."),
 ("Wo kann ich parken?", "Die Straße Am Leuchtturm ist Fußgängerzone; zum Be- und Entladen können Sie bis ans Hotel fahren. Parken Sie danach in der Tiefgarage Kurhaus (ca. 400 m) zum Vorzugspreis von 14 € pro 24 Stunden – das Ticket gibt es an der Rezeption."),
 ("Bis wann kann ich kostenfrei stornieren?", "Hotelreservierungen sind bis 14 Tage vor Anreise kostenfrei stornierbar, Apartments bis vier Wochen vor Anreise."),
 ("Gibt es einen Mindestaufenthalt?", "Ja, je nach Saison: am Wochenende in der Nebensaison 2 Nächte, in der Zwischensaison 4, in der Hauptsaison 6 Nächte, über Ostern, Pfingsten, Himmelfahrt und Silvester 5 Nächte. Kürzere Aufenthalte sind kurzfristig bei Verfügbarkeit buchbar."),
 ("Sind Haustiere erlaubt?", "Mit Rücksicht auf alle Gäste bitten wir Sie, Ihre Haustiere nicht mitzubringen."),
 ("Wie komme ich mit der Bahn zum Hotel?", "Mit der S-Bahn ab Rostock Hbf bis Warnemünde. Vom Bahnhof sind es zu Fuß über die Bahnhofsbrücke und am Alten Strom entlang ca. 500 Meter."),
 ("Welche Zimmer haben Meerblick?", "Panorama-Doppelzimmer und Panorama-Terrassen-Doppelzimmer haben direkten Ostseeblick, das Panorama-Terrassen-Doppelzimmer zusätzlich eine 40 m² große Dachterrasse. Terrassen- und Komfort-Doppelzimmer bieten seitlichen Ostseeblick oder Blick auf den Leuchtturm mit Hafeneinfahrt."),
]
FAQ_LD = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}

# ---------------- Startseite ----------------
def home():
    R = ""
    cards = "".join(card(r, R) for r in ROOMS)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q,a in FAQ)
    body = f"""
<section class="hero" style="padding:0">
  <picture><source media="(max-width:640px)" srcset="img/hero-promenade-960.jpg"><img class="hero-img" src="img/hero-promenade.jpg" alt="Blick vom Leuchtturm auf das Hotel am Leuchtturm, die Strandpromenade und den Strand von Warnemünde" fetchpriority="high"></picture>
  <span class="hero-credit">Blick vom Leuchtturm auf Hotel, Promenade und Strand</span>
  <div class="hero-copy"><div class="wrap">
    <div class="eyebrow">Der Blick vom Leuchtturm auf unser Haus · seit 1850</div>
    <h1 class="caps">Direkt am Strand</h1>
    <p>Inhabergeführtes Boutique-Hotel an der Strandpromenade, direkt gegenüber dem Leuchtturm: 30 Zimmer, Frühstückslounge mit Blick auf die Promenade und Lobby mit Kamin – nur wenige Schritte vom feinen weißen Sand der Ostsee.</p>
  </div></div>
</section>
<div class="search"><div class="wrap">
  {searchbox(R)}
  <div class="perkline"><span>Bestpreis direkt beim Hotel</span><span>Kostenfrei stornierbar bis 14 Tage vor Anreise</span><span>Parkticket direkt mitbuchen</span></div>
  <div class="note" data-n="1" style="margin-left:auto;margin-right:auto"><b>Maßnahme 1 – teilbare Buchungs-URL:</b> Heute öffnet die Buchung als Fenster über der Seite, die Adresse ändert sich nie. Hier führt jede Suche auf eine eigene Adresse mit Daten, Gästen und Zimmer – teilbar per Link, lesbar für KI-Assistenten.</div>
</div></div>

<section style="padding-top:64px"><div class="wrap">
  <div class="facts4">
    <div><b>91 %</b><span>„Sehr zufrieden“ – 1.563 Bewertungen (Okt. 2026)</span></div>
    <div><b>30 Zimmer</b><span>sechs Kategorien, dazu 4 Apartments</span></div>
    <div><b>Seit 1850</b><span>auf historischen Grundmauern, 2017 saniert</span></div>
    <div><b>24 Stunden</b><span>Rezeption für Sie da</span></div>
  </div>
</div></section>

<section class="alt" id="zimmer"><div class="wrap">
  <div class="center"><div class="eyebrow">Zimmer &amp; Preise</div><h2 class="caps">Ihr Zimmer am Meer</h2><div class="rule"></div>
  <p class="lead">Klassisch-modern im Boutiquestil, mit Betten in Komforthöhe und Bädern in Marmoroptik. Wählen Sie Ihren Blick – und buchen Sie direkt den nächsten freien Termin.</p>
  <div class="note" data-n="2"><b>Maßnahme 2 – direkt vom Zimmer buchen:</b> Jede Karte zeigt die nächsten freien Termine. Ein Klick öffnet die Buchung bereits mit diesem Zimmer und diesen Daten.</div></div>
  <div class="cards">{cards}</div>
  <p class="center" style="margin-top:30px"><a class="btn btn-line" href="zimmer/index.html#preise">Alle Preise &amp; Konditionen</a></p>
</div></section>

<div class="strip strip-video"><video class="strip-vid" autoplay muted loop playsinline preload="metadata" poster="img/duenen-zoom-poster.jpg" aria-label="Langsame Kamerafahrt durch die Dünen auf das Hotel am Leuchtturm zu"><source media="(max-width:640px)" src="img/duenen-zoom-960.mp4" type="video/mp4"><source src="img/duenen-zoom.mp4" type="video/mp4"></video>
  <div class="vcap"><div class="wrap"><div><div class="eyebrow">Hinter den Dünen</div><h2 class="caps">Vom Strand direkt ins Hotel</h2><p>Zwischen Ihrem Zimmer und der Ostsee liegen nur die Promenade und ein paar Schritte durch die Dünen.</p><p class="vnote">Kurzer Film, per KI aus einem Foto des Hotels animiert.</p></div><a class="btn btn-white" href="buchen.html">Verfügbarkeit prüfen</a></div></div></div>

<section><div class="wrap split">
  <div class="pic2"><img class="tall" src="img/fruehstueck-1.jpg" alt="Frühstückslounge mit Blick auf die Strandpromenade" loading="lazy" data-zoom><img src="img/buffet.jpg" alt="Frühstücksbuffet" loading="lazy" data-zoom><img src="img/fruehstueck-3.jpg" alt="Gedeckter Frühstückstisch" loading="lazy" data-zoom></div>
  <div><div class="eyebrow">Frühstückslounge</div><h2 class="caps">Frühstück mit Blick auf die Promenade</h2><div class="rule"></div>
  <p>Die Frühstückslounge ist nur für Hotelgäste da: bodentiefe Fenster, maritime Note und der Blick auf das Treiben an der Strandpromenade. Das Buffet fügen Sie einfach bei der Buchung hinzu.</p>
  <ul class="ticks"><li>Reichhaltiges Frühstücksbuffet</li><li>Bodentiefe Verglasung im Verandaanbau von 2017</li><li>Nur für Hotelgäste</li></ul></div>
</div></section>

<section class="alt"><div class="wrap split rev">
  <div class="pic"><img src="img/lobby-2.jpg" alt="Lobby mit gläsernem Kamin" loading="lazy" data-zoom></div>
  <div><div class="eyebrow">Lobby &amp; Bibliothek</div><h2 class="caps">Ankommen am Kamin</h2><div class="rule"></div>
  <p>In der neuen Lobby laden individuelle Sitzplätze, ein gläserner Kamin und eine kleine Bibliothek zum Verweilen ein – im Sommer nach dem Strand, im Winter nach dem Spaziergang an der rauen Ostsee.</p>
  <p><a class="btn btn-line" href="galerie.html">Zur Galerie</a></p></div>
</div></section>

<div class="strip"><img src="img/stage-4.jpg" alt="Dachterrasse mit Strandkorb und Blick auf den Leuchtturm" loading="lazy">
  <div class="ov"><div class="wrap"><div class="eyebrow" style="color:var(--aqua)">Panorama-Terrassen-Doppelzimmer</div><h2 class="caps">40 m² Dachterrasse mit Strandkorb</h2><p>Ihr privater Logenplatz über der Promenade – mit direktem Blick auf Ostsee und Leuchtturm.</p><p><a class="btn btn-white" href="zimmer/panorama-terrassen-doppelzimmer.html">Zimmer ansehen</a></p></div></div></div>

<section><div class="wrap">
  <div class="center"><div class="eyebrow">Angebote &amp; Anlässe</div><h2 class="caps">Für diese Tage früh buchen</h2><div class="rule"></div>
  <div class="note" data-n="3"><b>Eigene Seiten für Anlässe und Zielgruppen</b> – jede mit vorausgefüllter Buchung. Genau solche Seiten beantworten Fragen, die Gäste Google und ChatGPT stellen („Hotel zur Hanse Sail“, „Hotel vor der Kreuzfahrt“).</div></div>
  <div class="tiles">
    <article class="tile"><img src="img/lobby.jpg" alt="Lobby mit Kamin" loading="lazy"><div class="bd"><div class="when">28. Oktober – 20. Dezember 2026</div><h3>Wintertage in Warnemünde</h3><p>Heißgetränk am Kamin, Komfort- oder Terrassen-Doppelzimmer, Frühstück, Kurtaxe und Parken inklusive – ab 105 € pro Person und Nacht.</p><a class="btn btn-line" href="angebote/wintertage-in-warnemuende.html">Zum Angebot</a></div></article>
    <article class="tile"><img src="img/stage-6.jpg" alt="Strand und Leuchtturm" loading="lazy" style="object-position:85% 50%"><div class="bd"><div class="when">5.–8. August 2027</div><h3>Hanse Sail</h3><p>Großsegler laufen direkt vor dem Hotel in den Hafen ein – ein Zimmer mit Blick auf die Hafeneinfahrt ist der beste Platz.</p><a class="btn btn-line" href="angebote/hanse-sail.html">Zur Hanse Sail</a></div></article>
    <article class="tile"><img src="img/aussen-39.jpg" alt="Hotel am Leuchtturm von außen" loading="lazy"><div class="bd"><div class="when">Ganzjährig</div><h3>Vor oder nach der Kreuzfahrt</h3><p>Eine Nacht am Meer vor dem Ablegen in Warnemünde – das Cruise Center ist zu Fuß erreichbar.</p><a class="btn btn-line" href="angebote/kreuzfahrt.html">Mehr erfahren</a></div></article>
  </div>
</div></section>

<section class="reviews"><div class="wrap">
  <div class="score"><div class="big">91 %</div><div><h2 class="caps" style="font-size:34px">„Sehr zufrieden“</h2><div style="opacity:.8">aus 1.563 Bewertungen auf 10 Portalen (Customer Alliance) · Stand Oktober 2026</div></div></div>
  <div class="quotes">
    <div class="quote">Platz für ein echtes Gästezitat von Google oder HolidayCheck – am besten eines, das Zimmer und Ausblick konkret beschreibt.<small>Name · Quelle · Datum</small></div>
    <div class="quote">Platz für ein echtes Gästezitat zur Frühstückslounge mit Blick auf die Promenade.<small>Name · Quelle · Datum</small></div>
    <div class="quote">Platz für ein echtes Gästezitat zum Team und zur Lage am Leuchtturm.<small>Name · Quelle · Datum</small></div>
  </div>
  <div class="note center" data-n="4" style="margin-top:26px"><b>Bewertungen als Text mit Quelle</b> – nicht als Bild. Die heutige Startseite zeigt Bewertungen nur als Grafik-Link; Suchmaschinen und KI können sie so nicht lesen.</div>
</div></section>

<section><div class="wrap split">
  <div><div class="eyebrow">Apartmenthaus am Leuchtturm</div><h2 class="caps">Mehr Platz, gleiche Lage</h2><div class="rule"></div>
  <p>Im denkmalgeschützten Apartmenthaus gegenüber dem Hotel liegen auf zwei Etagen je ein 1-Zimmer-Apartment (40 m²) und ein 2-Zimmer-Apartment (60 m²) – mit großer Panoramaverglasung und Blick auf Ostsee, Strand und Leuchtturm.</p>
  <ul class="ticks"><li>Kochnische bzw. Küche, ideal für längere Aufenthalte</li><li>Reinigung bei Direktbuchung inklusive</li><li>Nichtraucher-Apartments</li></ul>
  <p style="margin-top:22px"><a class="btn btn-navy" href="apartments.html">Apartments ansehen</a></p></div>
  <div class="pic"><img src="img/apt-2.jpg" alt="Wohnbereich im 2-Zimmer-Apartment" loading="lazy" data-zoom></div>
</div></section>

<section class="alt"><div class="wrap split rev">
  <div class="pic"><img src="img/geschichte-1905.jpg" alt="Historische Postkarte: Strand von Warnemünde mit Leuchtturm um 1905" loading="lazy" data-zoom></div>
  <div><div class="eyebrow">Seit 1850</div><h2 class="caps">Das erste Hotel am Platze</h2><div class="rule"></div>
  <p>1850 errichtete H. F. Ohlerich hier das „Hotel Pavillon“ – als Warnemünde gerade zum Badeort wurde. 1897 entstand direkt davor der Leuchtturm. Heute führt ein inhabergeführtes Haus die Geschichte fort.</p>
  <p><a class="btn btn-line" href="geschichte.html">Die ganze Geschichte</a></p></div>
</div></section>

<section id="fragen"><div class="wrap narrow">
  <div class="eyebrow">Gut zu wissen</div><h2 class="caps">Häufige Fragen</h2><div class="rule"></div>
  <div class="note" data-n="5"><b>Antworten als Text:</b> Alle Angaben stehen heute schon auf der Website – verteilt über Preis-, Anfahrts- und Zimmerseiten. Gebündelt als FAQ übernehmen Google und KI-Assistenten sie direkt in ihre Antworten.</div>
  {faq}
</div></section>
"""
    page("index.html", "Hotel am Leuchtturm – Boutique-Hotel direkt am Strand von Warnemünde",
         "Inhabergeführtes Boutique-Hotel seit 1850 an der Strandpromenade von Warnemünde, direkt am Leuchtturm. 30 Zimmer mit Ostsee- oder Leuchtturmblick, teils mit Dachterrasse.",
         body, schema=[HOTEL_LD, FAQ_LD])

# ---------------- Zimmerübersicht ----------------
def rooms_index():
    R = "../"
    rows = "".join(f'<tr><td><a href="{r["slug"]}.html">{e(r["name"])}</a><br><small style="color:var(--muted)">{e(r["view"])}</small></td>' + "".join(f'<td class="num">ab {p} €</td>' for p in r["prices"]) + "</tr>" for r in ROOMS)
    cards = "".join(card(r, R) for r in ROOMS)
    body = f"""
<div class="wrap crumbs"><a href="../index.html">Startseite</a> › Zimmer &amp; Preise</div>
<section style="padding-top:28px"><div class="wrap">
  <div class="eyebrow">Zimmer &amp; Preise</div><h1 class="caps" style="font-size:clamp(34px,4.6vw,54px)">Sechs Kategorien, ein Blick aufs Meer</h1><div class="rule"></div>
  <p class="lead">Das Hotel präsentiert sich nach der Totalsanierung 2017 im klassisch-modernen Boutiquestil: lichtdurchflutete Zimmer mit und ohne Terrasse, Betten in Komforthöhe und Bäder mit modernster Ausstattung.</p>
  <div class="cards">{cards}</div>
</div></section>
<section class="alt" id="preise"><div class="wrap">
  <div class="eyebrow">Preise 2026</div><h2 class="caps">Preise &amp; Konditionen</h2><div class="rule"></div>
  <p>Tagespreise in Euro pro Zimmer und Nacht inkl. MwSt., ohne Frühstück. Gültig bis zum Erscheinen einer neuen Preisliste.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Zimmerkategorie</th><th class="num">Nebensaison<small>05.01.–31.03. · 01.11.–23.12.</small></th><th class="num">Zwischensaison<small>01.04.–12.05. · 04.10.–31.10.</small></th><th class="num">Hauptsaison<small>13.05.–03.10. · 24.12.–04.01.27</small></th></tr></thead>
    <tbody>{rows}<tr><td>Aufbettung 3. Person</td><td class="num">75 €</td><td class="num">75 €</td><td class="num">75 €</td></tr></tbody>
  </table></div>
  <div class="split" style="margin-top:40px;align-items:start;gap:40px">
    <div><h3>Gut zu wissen</h3><ul class="ticks">
      <li>Anreise ab 15 Uhr, Abreise bis 11 Uhr</li>
      <li>Kostenfrei stornierbar bis 14 Tage vor Anreise</li>
      <li>Zahlung per EC-Karte, bar oder Bankvorauszahlung</li>
      <li>Haustiere sind nicht erlaubt</li>
      <li>Fahrräder nur nach vorheriger Absprache</li></ul></div>
    <div><h3>Mindestaufenthalt</h3><ul class="ticks">
      <li>Wochenende in der Nebensaison: 2 Nächte</li>
      <li>Zwischensaison: 4 Nächte</li>
      <li>Hauptsaison: 6 Nächte</li>
      <li>Ostern, Pfingsten, Himmelfahrt, Silvester: 5 Nächte</li>
      <li>Kürzere Aufenthalte kurzfristig bei Verfügbarkeit</li></ul></div>
  </div>
  <div class="note" data-n="6"><b>Widerspruch auflösen:</b> Die Zimmerseiten nennen „max. 2 Erwachsene“, die Preisliste eine „Aufbettung 3. Person“. Auf der neuen Seite muss klar stehen, in welchen Zimmern eine dritte Person möglich ist.</div>
</div></section>
"""
    page("zimmer/index.html", "Zimmer & Preise – Hotel am Leuchtturm Warnemünde",
         "Sechs Zimmerkategorien mit Ostsee- oder Leuchtturmblick, teils mit Dachterrasse. Preise 2026 ab 139 € pro Nacht, kostenfrei stornierbar bis 14 Tage vor Anreise.",
         body, active="zimmer/index.html", schema=HOTEL_LD)

# ---------------- Zimmerseiten ----------------
def room_page(r):
    R = "../"
    gal = "".join(f'<img src="{R}img/{k}.jpg" alt="{e(r["name"])} – Foto {i+1}" loading="{"eager" if i==0 else "lazy"}" data-zoom>' for i,k in enumerate(r["imgs"]))
    other_links = " · ".join(f'<a href="{o["slug"]}.html">{e(o["name"])}</a>' for o in ROOMS if o["slug"] != r["slug"])
    feats = "".join(f"<li>{e(x)}</li>" for x in [r["bed"]] + COMMON)
    banner = f'<div class="strip" style="margin-top:56px"><img src="{R}img/{r["banner"]}.jpg" alt="Dachterrasse mit Strandkorb" loading="lazy"><div class="ov"><div class="wrap"><h2 class="caps">Ihre Dachterrasse</h2><p>40 m², Strandkorb, zwei Liegen – und die Ostsee direkt vor Ihnen.</p></div></div></div>' if r["banner"] else ""
    p = r["prices"]
    room_ld = {"@context":"https://schema.org","@type":"HotelRoom","name":r["name"],"description":r["special"],
               "floorSize":{"@type":"QuantitativeValue","value":r["size"].split(" ")[0].replace("–","-"),"unitCode":"MTK"},
               "occupancy":{"@type":"QuantitativeValue","maxValue":2},"bed":r["bed"],
               "containedInPlace":{"@type":"Hotel","name":"Hotel am Leuchtturm","url":REAL+"/"},
               "offers":{"@type":"Offer","priceCurrency":"EUR","price":p[0],"description":"ab-Preis pro Nacht in der Nebensaison 2026, ohne Frühstück","url":REAL+f"/buchen/?room={r['slug']}"}}
    body = f"""
<div class="wrap crumbs"><a href="../index.html">Startseite</a> › <a href="index.html">Zimmer &amp; Preise</a> › {e(r['name'])}</div>
<section style="padding-top:22px"><div class="wrap">
  <div class="eyebrow">{e(r['tag'])}</div>
  <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">{e(r['name'])}</h1>
  <div class="room-top">
    <div>
      <div class="gallery">{gal}</div>
      <p style="margin-top:26px;font-size:18px">{e(r['special'])}</p>
      <p>Großzügig und komfortabel im klassisch-modernen Design, eingerichtet im Boutiquestil mit hochwertigen Materialien in hellen und warmen Farbtönen. Das schwarz-weiße Bad in Marmoroptik hat {e(r['bath'])} und Kosmetikspiegel.</p>
      <ul class="spec">
        <li><b>Ausblick</b>{e(r['view'])}</li><li><b>Größe</b>{e(r['size'])}</li>
        <li><b>Etage</b>{e(r['floor'])}</li><li><b>Belegung</b>{e(r['occ'])}</li>
        <li><b>Bad</b>{e(r['bath'])}</li><li><b>Preis</b>ab {p[0]} € · {p[1]} € · {p[2]} € pro Nacht (Neben-/Zwischen-/Hauptsaison), ohne Frühstück</li>
      </ul>
      <h3 style="margin-top:34px">Ausstattung</h3>
      <ul class="kv">{feats}</ul>
      <div class="note" data-n="2"><b>Fakten als Text:</b> Größe, Etage, Ausblick und Preis stehen oben in einer Übersicht – nicht nur im Fließtext. Genau diese Angaben vergleichen Gäste und KI-Assistenten. Die Adresse ist sprechend: /zimmer/{r['slug']} statt /{r['old'].split('/')[-1]}.</div>
      {('<div class="note" data-n="3"><b>Widerspruch:</b> ' + e(r['warn'][len('Bitte prüfen: '):]) + '</div>') if r.get('warn') else ''}
    </div>
    <aside class="bookcard" data-bookcard="{r['slug']}">
      <div class="eyebrow" style="margin:0">Direkt beim Hotel buchen</div>
      <h3>Wann möchten Sie kommen?</h3>
      <div class="grid2">
        <div class="field"><label for="b-arr">Anreise</label><input type="date" id="b-arr"></div>
        <div class="field"><label for="b-dep">Abreise</label><input type="date" id="b-dep"></div>
      </div>
      <div class="field" style="margin-top:10px"><label for="b-ad">Gäste</label><select id="b-ad"><option value="1">1 Erwachsener</option><option value="2" selected>2 Erwachsene</option></select></div>
      <div class="sum" id="b-sum"></div>
      <a class="btn btn-navy" id="b-go" href="../buchen.html" style="width:100%;margin-top:14px">Dieses Zimmer buchen</a>
      <div class="slots-h" style="margin-top:14px">Nächste freie Termine <span class="demo">Demo</span></div>
      <div class="slots" data-slots="{r['slug']}"></div>
      <p class="slots-h" style="margin-top:12px">Kostenfrei stornierbar bis 14 Tage vor Anreise · Fragen? <a href="tel:{TEL_HREF}">{TEL}</a></p>
    </aside>
  </div>
</div></section>
{banner}
<section class="alt" style="padding:48px 0"><div class="wrap"><p style="margin:0"><b style="color:var(--navy)">Weitere Zimmer:</b> {other_links}</p></div></section>
"""
    page(f"zimmer/{r['slug']}.html", f"{r['name']} – Hotel am Leuchtturm Warnemünde",
         f"{r['name']} im Hotel am Leuchtturm: {r['view']}, {r['size'].replace(' (ohne Bad)','')}, {r['floor']}. Ab {p[0]} € pro Nacht. Direkt buchen.",
         body, active="zimmer/index.html", schema=room_ld)

# ---------------- Apartments ----------------
def apartments():
    body = """
<div class="wrap crumbs"><a href="index.html">Startseite</a> › Apartmenthaus</div>
<section style="padding-top:22px"><div class="wrap">
  <div class="eyebrow">Gegenüber dem Hotel · denkmalgeschützt</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Apartmenthaus am Leuchtturm</h1><div class="rule"></div>
  <div class="split" style="align-items:start">
    <div>
      <p class="lead">Auf zwei Etagen erwarten Sie jeweils ein 1-Zimmer- und ein 2-Zimmer-Nichtraucher-Apartment – komfortabel eingerichtet für einen längeren Aufenthalt, mit großer Panoramaverglasung und Blick auf Ostsee, Strand und Promenade mit Leuchtturm.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Apartment</th><th class="num">Nebensaison</th><th class="num">Zwischensaison</th><th class="num">Hauptsaison</th></tr></thead>
        <tbody><tr><td><b>1-Zimmer-Apartment</b><br><small>40 m², Ostseeblick</small></td><td class="num">125 €</td><td class="num">ab 155 €</td><td class="num">ab 175 €</td></tr>
        <tr><td><b>2-Zimmer-Apartment</b><br><small>60 m², Ostseeblick</small></td><td class="num">ab 155 €</td><td class="num">ab 185 €</td><td class="num">ab 215 €</td></tr>
        <tr><td>Aufbettung 3. Person</td><td class="num">50 €</td><td class="num">50 €</td><td class="num">50 €</td></tr></tbody></table></div>
      <p class="slots-h" style="margin-top:8px">Preise pro Apartment und Nacht bei 2 Personen, ohne Frühstück. <b>Laut heutiger Website Stand 2023</b> – bitte aktualisieren.</p>
      <div class="note" data-n="7"><b>Veraltete Preise und ein Widerspruch:</b> Die Apartment-Seite zeigt heute noch die Preise von 2023 und nennt die Reinigung einmal im 4-Tages-, einmal im 3-Tages-Rhythmus. Solche Widersprüche übernehmen KI-Assistenten ungefiltert.</div>
      <h3 style="margin-top:28px">1-Zimmer-Apartment · 40 m²</h3>
      <p>Kombinierter Schlaf- und Wohnbereich mit Kochnische (2-Zonen-Cerankochfeld, Mikrowelle, Kühlschrank mit Frostfach); Bad mit Badewanne und Duschabtrennung.</p>
      <h3>2-Zimmer-Apartment · 60 m²</h3>
      <p>Separates Schlafzimmer, Wohnbereich mit großem Essplatz direkt am Panoramafenster, innenliegende Küche (4-Zonen-Cerankochfeld, Spülmaschine, Mikrowelle, Kühlschrank) und Bad mit Dusche.</p>
      <ul class="ticks"><li>Reinigung nur bei Direktbuchung über das Hotel inklusive</li><li>Mindestaufenthalt in der Nebensaison 3 Nächte, sonst länger</li><li>Kostenfrei stornierbar bis vier Wochen vor Anreise</li><li>Keine Haustiere</li></ul>
      <p style="margin-top:22px"><a class="btn btn-navy" href="#" data-toast="Im Entwurf: Apartments laufen über dieselbe Buchungsstrecke wie die Hotelzimmer – kein separates Anfrageformular mehr.">Apartment anfragen &amp; buchen</a></p>
    </div>
    <div class="gallery"><img src="img/apt-haus.jpg" alt="Apartmenthaus am Leuchtturm von außen" data-zoom><img src="img/apt-1.jpg" alt="1-Zimmer-Apartment" loading="lazy" data-zoom><img src="img/apt-2.jpg" alt="2-Zimmer-Apartment Wohnbereich" loading="lazy" data-zoom><img src="img/apt-3.jpg" alt="Küche im Apartment" loading="lazy" data-zoom></div>
  </div>
</div></section>
"""
    page("apartments.html", "Apartmenthaus am Leuchtturm – Ferienapartments mit Ostseeblick in Warnemünde",
         "Vier Nichtraucher-Apartments (40 und 60 m²) im denkmalgeschützten Haus gegenüber dem Hotel am Leuchtturm, mit Panoramablick auf Ostsee und Leuchtturm.",
         body, active="apartments.html", schema=HOTEL_LD)

# ---------------- Angebote ----------------
def offers():
    offer_ld = {"@context":"https://schema.org","@type":"Offer","name":"Wintertage in Warnemünde","price":105,"priceCurrency":"EUR",
                "description":"Pro Person und Nacht im Doppelzimmer: Heißgetränk am Kamin, Übernachtung im Komfort- oder Terrassen-Doppelzimmer, Frühstück, Kurtaxe und freies Parken.",
                "validFrom":"2026-10-28","validThrough":"2026-12-20","offeredBy":{"@type":"Hotel","name":"Hotel am Leuchtturm"}}
    body = """
<div class="wrap crumbs"><a href="../index.html">Startseite</a> › <a href="index.html">Angebote</a> › Wintertage in Warnemünde</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div>
    <div class="eyebrow">Arrangement · 28. Oktober bis 20. Dezember 2026</div>
    <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Wintertage in Warnemünde</h1><div class="rule"></div>
    <p class="lead">Lernen Sie den besonderen Reiz der Ostsee im Winter kennen – der Kontrast zwischen rauer, tosender Ostsee und ruhiger, behaglicher Wohlfühlatmosphäre in unserem Haus.</p>
    <h3>Im Arrangement enthalten</h3>
    <ul class="ticks"><li>Zur Begrüßung ein Heißgetränk an unserem Kamin</li><li>Übernachtung im Komfort- oder Terrassen-Doppelzimmer</li><li>Reichhaltiges Frühstück</li><li>Die ortsübliche Kurtaxe</li><li>Freies Parken in der Tiefgarage Kurhaus</li></ul>
    <p style="margin-top:22px;font-size:18px">Preis pro Person und Nacht im Doppelzimmer <b class="fig" style="font-size:32px;color:var(--navy)">ab 105 €</b></p>
    <p><a class="btn btn-navy" href="../buchen.html?offer=wintertage&amp;room=komfort-doppelzimmer&amp;arrival=2026-11-20&amp;departure=2026-11-22&amp;adults=2&amp;step=2">Arrangement buchen</a></p>
    <p class="slots-h">Buchbar bei Verfügbarkeit. Heute steht hier „auf Anfrage“ – im Entwurf führt der Button direkt in die Buchung mit passenden Daten.</p>
    <div class="note" data-n="3"><b>Angebote mit festem Link:</b> Heute führt „jetzt Buchen“ nur in die allgemeine Buchungsmaske. Hier öffnet der Button die Buchung mit Zimmer, Daten und Arrangement – ideal für Newsletter, Anzeigen und KI-Assistenten.</div>
  </div>
  <div class="pic2"><img class="tall" src="../img/lobby-2.jpg" alt="Lobby mit Kamin" data-zoom><img src="../img/kdz-1.jpg" alt="Komfort-Doppelzimmer" loading="lazy" data-zoom><img src="../img/fruehstueck-2.jpg" alt="Frühstückslounge" loading="lazy" data-zoom></div>
</div></section>
"""
    page("angebote/wintertage-in-warnemuende.html", "Wintertage in Warnemünde – Arrangement im Hotel am Leuchtturm",
         "Arrangement Wintertage in Warnemünde: Heißgetränk am Kamin, Doppelzimmer, Frühstück, Kurtaxe und Parken inklusive, ab 105 € pro Person und Nacht.",
         body, active="angebote/index.html", schema=offer_ld)
    body2 = """
<div class="wrap crumbs"><a href="../index.html">Startseite</a> › Angebote</div>
<section style="padding-top:22px"><div class="wrap">
  <div class="eyebrow">Arrangements &amp; Anlässe</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Angebote</h1><div class="rule"></div>
  <div class="tiles">
    <article class="tile"><img src="../img/lobby.jpg" alt="Lobby mit Kamin" loading="lazy"><div class="bd"><div class="when">28.10. – 20.12.2026</div><h3>Wintertage in Warnemünde</h3><p>Heißgetränk am Kamin, Frühstück, Kurtaxe und Parken inklusive – ab 105 € p. P./Nacht.</p><a class="btn btn-navy" href="wintertage-in-warnemuende.html">Zum Angebot</a></div></article>
    <article class="tile"><img src="../img/stage-4.jpg" alt="Dachterrasse" loading="lazy"><div class="bd"><div class="when">5.–8. August 2027</div><h3>Hanse Sail vom Zimmer aus</h3><p>Großsegler in der Hafeneinfahrt – und Zimmer mit Blick darauf, früh buchbar.</p><a class="btn btn-navy" href="hanse-sail.html">Zur Hanse Sail</a></div></article>
    <article class="tile"><img src="../img/aussen-37.jpg" alt="Hotel am Leuchtturm" loading="lazy"><div class="bd"><div class="when">Ganzjährig</div><h3>Vor oder nach der Kreuzfahrt</h3><p>Eine Nacht am Meer, das Cruise Center zu Fuß erreichbar – auch auf Englisch.</p><a class="btn btn-navy" href="kreuzfahrt.html">Mehr erfahren</a></div></article>
  </div>
</div></section>
"""
    page("angebote/index.html", "Angebote & Arrangements – Hotel am Leuchtturm Warnemünde",
         "Arrangements im Hotel am Leuchtturm Warnemünde, z. B. Wintertage in Warnemünde ab 105 € pro Person und Nacht.",
         body2, active="angebote/index.html", schema=HOTEL_LD)

# ---------------- Geschichte ----------------
def history():
    steps = [("1850","H. F. Ohlerich errichtet das „Hotel Pavillon“, einstöckig – Warnemünde beginnt, sich zum Badeort zu entwickeln. Es ist das erste Hotel am Platze."),
             ("~1880","Knapp 30 Jahre später wird das Haus zum dreistöckigen Bau erweitert."),
             ("1897","Direkt vor dem Hotel entsteht der Leuchtturm – das Wahrzeichen Warnemündes."),
             ("bis 1920","Vor dem Hotel liegt der Kurgarten, beliebtes Ausflugsziel. Im Erdgeschoss wird Gastwirtschaft betrieben, die Stranddiele ist ein beliebtes Tanzlokal."),
             ("1950","Die letzte Besitzerin, Elisabeth Colas, wird durch die „Aktion Rose“ enteignet. Das Haus heißt nun „Meer des Friedens“."),
             ("nach 1989","Rückübertragung an Frau Colas, die das Hotel einer Kirchengemeinde vererbt."),
             ("1996","Erweiterung von 20 auf 30 Zimmer, der erste Stock erhält eine umlaufende Dachterrasse."),
             ("2013","Letzter Eigentümerwechsel – der Name „Hotel am Leuchtturm“ wird fortgeführt."),
             ("2017","Totalsanierung und Verandaanbau mit neuer Rezeption, Lobby mit Kamin und Frühstückslounge mit Promenadenblick.")]
    tl = "".join(f"<li><b>{y}</b><p style='margin:0'>{e(t)}</p></li>" for y,t in steps)
    body = f"""
<div class="wrap crumbs"><a href="index.html">Startseite</a> › Geschichte</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div><div class="eyebrow">Hotel seit 1850</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Wie alles begann</h1><div class="rule"></div>
  <p class="lead">Das heutige Hotel am Leuchtturm steht auf den Grundmauern aus dem Jahr 1850 – und hat mehr als 170 Jahre Warnemünder Geschichte erlebt.</p>
  <ol class="timeline">{tl}</ol>
  <div class="note" data-n="8"><b>Kleiner Widerspruch:</b> Die Geschichtsseite nennt 1850, die Anfahrtsseite „1851 errichtet“. Eine Jahreszahl wählen und überall verwenden.</div></div>
  <div><div class="pic"><img src="../img/geschichte-1905.jpg" alt="Strandleben in Warnemünde um 1900" data-zoom></div><p class="slots-h" style="margin-top:8px">Strandleben um 1900 – historische Postkarte</p>
  <div class="pic" style="margin-top:22px"><img src="img/aussen-37.jpg" alt="Das Hotel heute" loading="lazy" data-zoom></div><p class="slots-h" style="margin-top:8px">Das Hotel heute, nach der Sanierung 2017</p></div>
</div></section>
""".replace('src="../img/geschichte','src="img/geschichte')
    page("geschichte.html", "Geschichte seit 1850 – Hotel am Leuchtturm Warnemünde",
         "Vom Hotel Pavillon 1850 über das Meer des Friedens zum Hotel am Leuchtturm: die Geschichte des ersten Hotels am Platze in Warnemünde.",
         body, active="geschichte.html", schema=HOTEL_LD)

# ---------------- Lage & Anfahrt ----------------
def location():
    body = """
<div class="wrap crumbs"><a href="index.html">Startseite</a> › Lage &amp; Anfahrt</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div><div class="eyebrow">Am Leuchtturm 16 · 18119 Rostock-Warnemünde</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Lage &amp; Anfahrt</h1><div class="rule"></div>
  <p class="lead">Direkt auf der Strandpromenade, gegenüber dem Leuchtturm – Strand, Alter Strom und Bahnhof sind zu Fuß erreichbar.</p>
  <h3 style="margin-top:26px">Mit dem Zug</h3>
  <p>IC bis Rostock Hbf, dort in die S-Bahn nach Warnemünde. Zu Fuß über die Bahnhofsbrücke und rechts am Alten Strom entlang: ca. 500 m bis zum Hotel.</p>
  <h3>Mit dem Auto</h3>
  <p><b>Aus Richtung Berlin:</b> A19 bis zum Ende, durch den mautpflichtigen Warnowtunnel nach Lütten Klein, dann über die B 103 nach Warnemünde.<br><b>Aus Richtung Hamburg:</b> A1 bis Kreuz Lübeck, A20 Richtung Rostock, Ausfahrt Rostock-West, B 103 nach Warnemünde.</p>
  <h3>Parken</h3>
  <p>Die Straße Am Leuchtturm ist seit 2018 Fußgängerzone und Spielstraße. Zum Be- und Entladen dürfen Sie bis ans Hotel fahren. Danach parken Sie in der <b>Tiefgarage Kurhaus</b> (ca. 400 m, an der Promenade) zum Vorzugspreis von <b>14 € pro 24 Stunden</b>.</p>
  <div class="note" data-n="3"><b>Parkticket online:</b> Heute muss das Ticket vor der Einfahrt an der Rezeption gekauft werden. In der neuen Buchung wird es gleich mitgebucht.</div>
  <h3>Mit dem Flugzeug</h3>
  <p>Flughafen Rostock-Laage. Für einen Shuttle zum Hotel melden Sie sich gern bei uns: <a href="tel:+4938154370">0381 5 43 70</a>.</p></div>
  <div><iframe title="Karte: Hotel am Leuchtturm, Warnemünde" style="width:100%;aspect-ratio:4/5;border:0;border-radius:10px;box-shadow:var(--shadow)" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=12.0760%2C54.1770%2C12.0950%2C54.1850&amp;layer=mapnik&amp;marker=54.1814%2C12.0862"></iframe>
  <p class="slots-h" style="margin-top:8px">Karte © OpenStreetMap-Mitwirkende · Markierung ungefähr</p></div>
</div></section>
"""
    page("lage-anfahrt.html", "Lage & Anfahrt – Hotel am Leuchtturm Warnemünde",
         "Anfahrt zum Hotel am Leuchtturm in Warnemünde mit Bahn, Auto und Flugzeug. Parken in der Tiefgarage Kurhaus für 14 € pro 24 Stunden.",
         body, active="lage-anfahrt.html", schema=HOTEL_LD)

# ---------------- Galerie ----------------
def gallery():
    keys = ["aussen-37","ptdz-5","fruehstueck-1","lobby-2","pdz-4","tdz-3","buffet","kdz-1","bad","stage-4","pdz-1","fruehstueck-2","collage-3","kdz-2","dz-4","ez-1","lobby","fruehstueck-3","collage-1","tdz-1","apt-2","ptdz-2","collage-2","aussen-39"]
    imgs = "".join(f'<img src="img/{k}.jpg" alt="Hotel am Leuchtturm – Foto" loading="lazy" data-zoom>' for k in keys)
    body = f"""
<div class="wrap crumbs"><a href="index.html">Startseite</a> › Galerie</div>
<section style="padding-top:22px"><div class="wrap"><div class="eyebrow">Fotogalerie</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Eindrücke</h1><div class="rule"></div>
<div class="note" data-n="9"><b>Bildtexte ergänzen:</b> Heute heißen die Fotos „Zi205(Panorama-Doppelzimmer)(4).jpg“ und haben keine Beschreibung. Sprechende Dateinamen und Alt-Texte machen sie für Google-Bildersuche und Barrierefreiheit nutzbar.</div>
<div class="masonry">{imgs}</div></div></section>
"""
    page("galerie.html", "Galerie – Hotel am Leuchtturm Warnemünde", "Fotos vom Hotel am Leuchtturm: Zimmer, Frühstückslounge, Lobby mit Kamin, Dachterrasse und Ausblick auf Ostsee und Leuchtturm.", body, schema=HOTEL_LD)

# ---------------- Buchen ----------------
def booking():
    body = """
<div class="wrap crumbs"><a href="index.html">Startseite</a> › Online buchen</div>
<section style="padding-top:22px" id="booking"><div class="wrap">
  <div class="eyebrow">Direkt beim Hotel · Bestpreis</div><h1 class="caps" style="font-size:clamp(30px,4vw,46px)">Online buchen</h1>
  <form class="searchbox" id="k-form" style="margin-top:22px;box-shadow:none;border:1px solid var(--line)">
    <div class="field"><label for="k-arr">Anreise</label><input type="date" id="k-arr"></div>
    <div class="field"><label for="k-dep">Abreise</label><input type="date" id="k-dep"></div>
    <div class="field"><label for="k-ad">Gäste</label><select id="k-ad"><option value="1">1 Erwachsener</option><option value="2">2 Erwachsene</option></select></div>
    <div></div>
    <button class="btn btn-line" type="submit">Daten ändern</button>
  </form>
  <nav class="stepper" id="stepper" aria-label="Buchungsschritte"><a href="#">1 · Zimmer</a><a href="#">2 · Rate</a><a href="#">3 · Extras</a><a href="#">4 · Übersicht</a></nav>
  <div class="bk"><div id="step"></div><aside class="summary" id="summary"></aside></div>
</div></section>
"""
    page("buchen.html", "Online buchen – Hotel am Leuchtturm Warnemünde", "Zimmer im Hotel am Leuchtturm direkt beim Hotel buchen – mit Gesamtpreis, Extras und teilbarem Buchungslink.", body, mbar=True, mbar_href="#step")

# ---------------- Impressum des Entwurfs ----------------
def imprint():
    body = """
<section><div class="wrap narrow"><div class="eyebrow">Konzeptentwurf</div><h1 class="caps" style="font-size:40px">Impressum dieses Entwurfs</h1><div class="rule"></div>
<p>Diese Seiten sind ein unverbindlicher <b>Konzeptentwurf</b> für eine mögliche Neugestaltung der Website des Hotel am Leuchtturm. Sie sind keine offizielle Website des Hotels; es werden keine Buchungen angenommen und keine personenbezogenen Daten erhoben.</p>
<p><b>Verantwortlich für diesen Entwurf:</b><br>Fritz Bremer · mndst.co<br>[Straße und Hausnummer]<br>[PLZ] Berlin<br>E-Mail: <a href="mailto:info@mndst.co">info@mndst.co</a></p>
<p>Texte, Zimmerangaben, Preise und Fotos stammen von der Website des Hotel am Leuchtturm (Am Leuchtturm 16, 18119 Rostock-Warnemünde) und dienen ausschließlich der Präsentation dieses Entwurfs. Fotos © Hotel am Leuchtturm.</p>
<p>Zur offiziellen Website: <a href="https://www.hotel-am-leuchtturm.de/DE/home.html">hotel-am-leuchtturm.de</a></p></div></section>
"""
    page("impressum.html", "Impressum des Entwurfs", "Impressum des Konzeptentwurfs.", body, mbar=False)

# ---------------- Technik-Paket ----------------
NEW = [  # (neuer Pfad, alte Pfade, Priorität, changefreq)
 ("/", ["/DE/home.html", "/"], "1.0", "weekly"),
 ("/zimmer/", ["/DE/hotel-zimmer.html", "/DE/hotel-zimmer/preise-konditionen.html"], "0.9", "monthly"),
] + [(f"/zimmer/{r['slug']}/", [f"/DE/{r['old']}"], "0.9", "monthly") for r in ROOMS] + [
 ("/apartments/", ["/DE/apartmenthaus-am-leuchtturm1.html", "/DE/apartmenthaus-am-leuchtturm1/apartmenthaus-am-leuchtturm.html"], "0.8", "monthly"),
 ("/angebote/", ["/DE/arrangements.html"], "0.8", "weekly"),
 ("/angebote/wintertage-in-warnemuende/", ["/DE/arrangements,arrangement-8-wintertage-in-warnemuende.html"], "0.7", "monthly"),
 ("/angebote/hanse-sail/", [], "0.7", "monthly"),
 ("/angebote/kreuzfahrt/", [], "0.7", "monthly"),
 ("/buchen/", [], "0.8", "weekly"),
 ("/galerie/", ["/DE/hotel-zimmer/fotogalerie.html"], "0.5", "yearly"),
 ("/gutscheine/", ["/DE/hotel-zimmer/gutscheine.html"], "0.5", "yearly"),
 ("/geschichte/", ["/DE/hotel-zimmer/geschichte.html"], "0.5", "yearly"),
 ("/lage-anfahrt/", ["/DE/ueber-uns/lage--anfahrt.html", "/DE/lageanfahrt.html"], "0.7", "yearly"),
 ("/kontakt/", ["/DE/ueber-uns.html", "/DE/ueber-uns/kontakt1.html", "/DE/kontakt.html"], "0.6", "yearly"),
 ("/partner/", ["/DE/ueber-uns/partnerseiten1.html", "/DE/partnerseiten.html"], "0.3", "yearly"),
 ("/impressum/", ["/DE/ueber-uns/impressum1.html", "/DE/impressum.html"], "0.1", "yearly"),
 ("/datenschutz/", ["/DE/ueber-uns/datenschutz.html", "/DE/datenschutz1.html"], "0.1", "yearly"),
 ("/agb/", ["/DE/ueber-uns/agbs.html"], "0.1", "yearly"),
]

EN_URL = {"/":"/en/","/zimmer/":"/en/rooms/","/apartments/":"/en/apartments/","/angebote/":"/en/offers/",
          "/angebote/wintertage-in-warnemuende/":"/en/offers/winter-days-in-warnemuende/","/angebote/hanse-sail/":"/en/offers/hanse-sail/","/angebote/kreuzfahrt/":"/en/offers/cruise/","/buchen/":"/en/book/","/galerie/":"/en/gallery/",
          "/gutscheine/":"/en/vouchers/","/geschichte/":"/en/history/","/lage-anfahrt/":"/en/location/","/kontakt/":"/en/contact/",
          "/partner/":"/en/partners/","/impressum/":"/en/imprint/","/datenschutz/":"/en/privacy/","/agb/":"/en/terms/"}
def en_url(new):
    if new.startswith("/zimmer/") and new != "/zimmer/": return "/en/rooms/" + EN_SLUG[new.split("/")[2]] + "/"
    return EN_URL[new]

# ---------------- Prüfbericht: Widersprüche auf der heutigen Website ----------------
# (Thema, Stelle A, Stelle B, Empfehlung, Stand im Entwurf) – geprüft am 30.10.2026
PRUEF = [
 ("Website ↔ Buchungssystem DIRS21", [
  ("Zimmernamen", "Website: 6 Kategorien, u. a. „Komfort-Doppelzimmer“", "DIRS21: 8 Zimmertypen, kein „Komfort“, dafür „Doppelzimmer, Blick auf Leuchtturm“ und „Doppelzimmer, mit seitlichem Ostseeblick“; Terrassen-DZ in zwei Typen geteilt; Apartments heißen „Einraum/Zweiraum“", "Überall dieselben Namen verwenden – Gäste und KI-Assistenten müssen das gebuchte Zimmer wiedererkennen", "Entwurf nutzt die Namen der Website"),
  ("Panorama-Terrassen-Doppelzimmer", "Website: das Aushängeschild (40 m² Dachterrasse)", "DIRS21: in keinem von 8 getesteten Zeiträumen (Nov. 2026 – Sep. 2027) angeboten", "Klären: nicht online buchbar oder immer ausgebucht? Falls nur telefonisch: auf der Zimmerseite so sagen", "offen"),
  ("Preise", "Preisliste 2026: Doppelzimmer ab 179 €, Einzelzimmer ab 139 € (Nebensaison)", "DIRS21 10.–12.11.2026: Doppelzimmer 165 €, Einzelzimmer 115 €; April 2027 Nebensaison-Preise, obwohl die Preisliste April als Zwischensaison führt. Hauptsaison Juli 2027 stimmt überein", "Preisliste und Buchungssystem abgleichen; „ab“-Preise sollten der niedrigste buchbare Preis sein", "offen"),
  ("Mindestaufenthalt", "Preisliste: Hauptsaison 6 Nächte, Ostern/Pfingsten 5 Nächte", "DIRS21 bietet 12.–14.07.2027 (2 Nächte) und Ostern 26.–28.03.2027 (2 Nächte) an", "Entweder Regel im Buchungssystem hinterlegen oder auf der Website streichen", "Entwurf zeigt die Regel der Preisliste als Hinweis"),
  ("Minibar", "Deutsche Website: keine Minibar erwähnt", "DIRS21 (und englische Website): Minibar bei allen Zimmern", "Klären und einheitlich angeben", "offen"),
 ]),
 ("Deutsche ↔ englische Website", [
  ("Preise", "Deutsch: Preisliste 2026 (z. B. Einzelzimmer ab 139 €, Aufbettung 75 €)", "Englisch: alte Liste mit Saisons bis „06.01.24“ (Einzelzimmer ab 135 €, Aufbettung 50 €)", "Englische Preisseite ersetzen", "Entwurf: beide Sprachen mit Preisen 2026"),
  ("Stornierung", "Deutsch: bis 14 Tage vor Anreise kostenfrei", "Englisch: bis vier Wochen vor Anreise", "Eine Frist für beide Sprachen", "Entwurf: 14 Tage (Hotel), vier Wochen (Apartments)"),
  ("Mindestaufenthalt", "Deutsch: Wochenende Nebensaison 2, Zwischensaison 4, Hauptsaison 6, Feiertage 5 Nächte", "Englisch: Wochenende 2, Ostern/Pfingsten/Himmelfahrt 3, Silvester 5, Hanse Sail 7 Nächte", "Eine Regel für beide Sprachen", "Entwurf: deutsche Regel in beiden Sprachen"),
  ("Parken", "Deutsch: seit 2018 Fußgängerzone, keine Stellplätze am Hotel", "Englisch: „public parking places at the hotel are available“", "Englischen Text korrigieren – Gäste fahren sonst ins Leere", "Entwurf: deutsche Angabe in beiden Sprachen"),
  ("Kinder und Frühstück", "Deutsch: keine Kinderpreise, kein Frühstückspreis", "Englisch: Kinder bis 4 Jahre frei, bis 14 Jahre 17,50 €; Frühstück 20 € p. P.", "Gültige Werte bestätigen und in beiden Sprachen nennen", "Entwurf: Frühstück 20 € als Demo-Wert"),
  ("Ausstattung", "Deutsch: keine Minibar, kein Wäscheservice", "Englisch: Minibar, Wäscheservice, Kissenmenü, Bademäntel", "Klären und angleichen", "offen"),
  ("Apartments", "Deutsch: Reinigung alle 3 bzw. 4 Tage, ohne Frühstück, Mindestaufenthalt 3 Nächte", "Englisch: Reinigung alle 2 Tage, Frühstück bei Direktbuchung inklusive, Mindestaufenthalt 2 Nächte", "Eine Fassung für beide Sprachen", "Entwurf: „Reinigung bei Direktbuchung inklusive“ ohne Rhythmus"),
 ]),
 ("Innerhalb der deutschen Website", [
  ("Gründungsjahr", "Geschichte: „Grundmauern aus dem Jahr 1850“, „mehr als 150-jährige Geschichte“", "Lage & Anfahrt: „1851 errichtet“", "Eine Jahreszahl wählen; „mehr als 175 Jahre“", "Entwurf: 1850, „mehr als 170 Jahre“"),
  ("Einzelzimmer", "„Queensize-Bett“", "„(100 cm × 200 cm)“ – das ist ein Einzelbett – und „Belegung 1–2 Erwachsene“", "Bettbreite und Belegung klären", "im Entwurf markiert"),
  ("Dritte Person", "Zimmerseiten: „Belegung max. 2 Erwachsene“", "Preisliste: „Aufbettung 3. Person 75 €“", "Sagen, in welchen Zimmern eine Aufbettung möglich ist", "im Entwurf markiert"),
  ("Apartments", "Preise „2023“, Hauptsaison bis „06.01.25“; Reinigung „4-Tages-Rhythmus“", "Reinigung „3-Tages-Rhythmus“ im selben Text; DIRS21: 2-Raum-Apartment Hauptsaison 205 € statt 215 €", "Preise 2026/27 veröffentlichen, eine Reinigungsangabe", "im Entwurf markiert"),
  ("Tiefgarage", "Lage & Anfahrt: „Tiefgarage Kurhaus“", "Winter-Arrangement: „Tiefgarage Kurhausgarten“", "Einen Namen verwenden", "Entwurf: „Tiefgarage Kurhaus“"),
  ("Leere Seite", "Menü: „Partnerseiten“", "Die Seite hat keinen Inhalt", "Füllen oder aus dem Menü nehmen", "Entwurf: entfällt"),
  ("Tippfehler", "„Preie &amp; Konditionen“ (Seitentitel in Google), „Onlinebuchnung“, „Frühstücklounge“", "„Intension“, „wiederspiegelt“ (Hotel &amp; Zimmer)", "Korrigieren", "Entwurf: korrigiert"),
 ]),
]

def pruefbericht():
    blocks = ""
    for title, rows in PRUEF:
        tr = "".join(f'<tr><td><b>{t}</b></td><td data-l="Hier steht">{a}</td><td data-l="Dort steht">{b}</td><td data-l="Empfehlung">{r}</td><td data-l="Im Entwurf">{st}</td></tr>' for t,a,b,r,st in rows)
        blocks += f'<h3 style="margin-top:30px">{title}</h3><div class="table-wrap"><table class="pruef"><thead><tr><th>Thema</th><th>Hier steht</th><th>Dort steht</th><th>Empfehlung</th><th>Im Entwurf</th></tr></thead><tbody>{tr}</tbody></table></div>'
    return f"""<section class="alt" id="pruefbericht"><div class="wrap">
  <h2 class="caps">Prüfbericht: Widersprüche</h2><div class="rule"></div>
  <p class="lead">Abgleich der deutschen und englischen Website mit dem Buchungssystem DIRS21 am 30.10.2026. Jeder Punkt ist eine Frage, die Gäste, Google und KI-Assistenten heute unterschiedlich beantwortet bekommen.</p>
  {blocks}
  <p class="slots-h" style="margin-top:16px">DIRS21 abgefragt für 2 Erwachsene (Einzelzimmer: 1 Erwachsener) in den Zeiträumen 10.–12.11. und 13.–15.11.2026, 26.–28.03., 12.–16.04., 07.–14.06., 12.–14.07., 12.–18.07. und 06.–13.09.2027. Preise pro Nacht laut Ergebnisliste.</p>
</div></section>"""

def tech():
    V = os.path.join(OUT, "vorschlag"); os.makedirs(V, exist_ok=True)
    # sitemap.xml
    urls = []
    for new, _, prio, freq in NEW:
        if new == "/buchen/": continue
        en = en_url(new)
        urls.append(f"""  <url>
    <loc>{REAL}{new}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
    <xhtml:link rel="alternate" hreflang="de" href="{REAL}{new}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{REAL}{en}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{REAL}{new}"/>
  </url>""")
    open(os.path.join(V,"sitemap.xml"),"w",encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    # robots.txt
    open(os.path.join(V,"robots.txt"),"w",encoding="utf-8").write(f"""# robots.txt für {REAL}
# Grundsatz: Suchmaschinen und KI-Assistenten dürfen alles lesen, was Gäste sehen.
User-agent: *
Allow: /
# Buchungsschritte mit Parametern nicht crawlen (die Seite /buchen/ selbst bleibt erlaubt)
Disallow: /buchen/?*

# Optional: Nutzung für KI-Training ausschließen, ohne die Sichtbarkeit in KI-Suchen zu verlieren.
# Nur aktivieren, wenn das bewusst so entschieden wird:
# User-agent: GPTBot
# Disallow: /
# User-agent: ClaudeBot
# Disallow: /
# User-agent: Google-Extended
# Disallow: /

Sitemap: {REAL}/sitemap.xml
""")
    # llms.txt
    rooms_md = "\n".join(f"- [{r['name']}]({REAL}/zimmer/{r['slug']}/): {r['view']}; {r['size']}; {r['floor']}; {r['bed']}; {r['occ']}; ab {r['prices'][0]} € (Nebensaison) / {r['prices'][1]} € (Zwischensaison) / {r['prices'][2]} € (Hauptsaison) pro Nacht, ohne Frühstück." for r in ROOMS)
    open(os.path.join(V,"llms.txt"),"w",encoding="utf-8").write(f"""# Hotel am Leuchtturm, Warnemünde

> Inhabergeführtes Boutique-Hotel seit 1850 direkt an der Strandpromenade von Warnemünde (Rostock), gegenüber dem Leuchtturm. 30 Zimmer in sechs Kategorien plus vier Ferienapartments im Apartmenthaus gegenüber. Frühstückslounge mit Promenadenblick, Lobby mit Kamin, 24-Stunden-Rezeption.

Adresse: Am Leuchtturm 16, 18119 Rostock-Warnemünde, Deutschland
Telefon: +49 381 54370 · E-Mail: {MAIL}
Check-in ab 15:00 Uhr, Check-out bis 11:00 Uhr. Haustiere nicht erlaubt.
Hotelzimmer kostenfrei stornierbar bis 14 Tage vor Anreise; Apartments bis vier Wochen vor Anreise.
Zahlung im Hotel: EC-Karte, bar oder Bankvorauszahlung.
Parken: keine Parkplätze am Haus (Fußgängerzone); Tiefgarage Kurhaus ca. 400 m entfernt, Vorzugspreis 14 € pro 24 Stunden.
Bahn: S-Bahn bis Warnemünde, ca. 500 m Fußweg.

## Online buchen

- Direkt buchen (Buchungssystem DIRS21, Reisedaten im Link): https://reservation.one.dirs21.de/hotel-am-leuchtturmde?range=JJJJ-MM-TT,JJJJ-MM-TT&culture=de-DE&show_results=true
- Geplant nach dem Relaunch: {REAL}/buchen/?arrival=JJJJ-MM-TT&departure=JJJJ-MM-TT&adults=2&room=<zimmer-slug>
- Zimmer-Slugs: {", ".join(r['slug'] for r in ROOMS)}

## Zimmer und Preise 2026 (pro Zimmer und Nacht inkl. MwSt., ohne Frühstück)

Saisons: Nebensaison 05.01.–31.03. und 01.11.–23.12.; Zwischensaison 01.04.–12.05. und 04.10.–31.10.; Hauptsaison 13.05.–03.10. und 24.12.–04.01.
Mindestaufenthalt: Wochenende Nebensaison 2 Nächte, Zwischensaison 4, Hauptsaison 6, Ostern/Pfingsten/Himmelfahrt/Silvester 5; kürzere Aufenthalte kurzfristig bei Verfügbarkeit.

{rooms_md}

## Apartments

- [Apartmenthaus am Leuchtturm]({REAL}/apartments/): 1-Zimmer-Apartment 40 m² und 2-Zimmer-Apartment 60 m², Panoramablick auf Ostsee und Leuchtturm, Küche/Kochnische, Reinigung bei Direktbuchung inklusive.

## Angebote

- [Wintertage in Warnemünde]({REAL}/angebote/wintertage-in-warnemuende/): 28.10.–20.12.2026, ab 105 € pro Person und Nacht im Doppelzimmer inkl. Frühstück, Kurtaxe, Parken und Heißgetränk am Kamin.
- [Hanse Sail]({REAL}/angebote/hanse-sail/): Hanse Sail 2027 vom 5. bis 8. August; Zimmer mit Blick auf Leuchtturm und Hafeneinfahrt, durch die die Großsegler einlaufen. Hauptsaison: Mindestaufenthalt 6 Nächte.
- [Vor oder nach der Kreuzfahrt]({REAL}/angebote/kreuzfahrt/): Das Warnemünde Cruise Center am Bahnhof Warnemünde ist zu Fuß erreichbar.
- [Gutscheine]({REAL}/gutscheine/): Wertgutscheine für Übernachtungen, Betrag frei wählbar.

## Weitere Seiten

- [English version]({REAL}/en/)

- [Lage & Anfahrt]({REAL}/lage-anfahrt/)
- [Geschichte seit 1850]({REAL}/geschichte/)
- [Kontakt]({REAL}/kontakt/)
""")
    # Schema
    full_ld = dict(HOTEL_LD)
    full_ld["containsPlace"] = [{"@type":"HotelRoom","name":r["name"],"url":f"{REAL}/zimmer/{r['slug']}/","bed":r["bed"],"occupancy":{"@type":"QuantitativeValue","maxValue":2}} for r in ROOMS]
    full_ld["makesOffer"] = [{"@type":"Offer","name":r["name"],"price":r["prices"][0],"priceCurrency":"EUR","description":"ab-Preis pro Nacht, Nebensaison 2026, ohne Frühstück"} for r in ROOMS]
    open(os.path.join(V,"schema-hotel.json"),"w",encoding="utf-8").write(json.dumps(full_ld, ensure_ascii=False, indent=2))
    # Weiterleitungen
    lines = ["# 301-Weiterleitungen alt -> neu (Apache .htaccess, mod_alias)", "# Die Website läuft auf Apache – diese Zeilen kommen in die .htaccess im Hauptverzeichnis."]
    csv = ["alte_url;neue_url"]
    for new, olds, _, _ in NEW:
        for o in olds:
            if o == "/": continue
            lines.append(f"Redirect 301 {o} {new}")
            csv.append(f"{REAL}{o};{REAL}{new}")
    lines += ["", "# Englische Seiten nach demselben Muster: /EN/... -> /en/...", "RedirectMatch 301 ^/EN/home\\.html$ /en/"]
    open(os.path.join(V,"weiterleitungen.htaccess.txt"),"w",encoding="utf-8").write("\n".join(lines)+"\n")
    open(os.path.join(V,"weiterleitungen.csv"),"w",encoding="utf-8").write("\n".join(csv)+"\n")
    rows = "".join(f"<tr><td>{'<br>'.join(e(o) for o in olds if o!='/') or '–'}</td><td><b>{e(new)}</b></td></tr>" for new, olds, _, _ in NEW)
    body = f"""
<div class="wrap crumbs"><a href="../index.html">Startseite</a> › Technik-Paket</div>
<section style="padding-top:22px"><div class="wrap">
  <div class="eyebrow">Für Ihre Webagentur</div><h1 class="caps" style="font-size:clamp(30px,4vw,46px)">Technik-Paket</h1><div class="rule"></div>
  <p class="lead">Diese Dateien sind für die echte Domain hotel-am-leuchtturm.de geschrieben. Sie enthalten nur echte Angaben von der heutigen Website – keine Demo-Werte.</p>
  <div class="tiles">
    <article class="tile"><div class="bd"><div class="when">Neu · fehlt heute (404)</div><h3>sitemap.xml</h3><p>Alle neuen Adressen mit deutscher und englischer Version (hreflang).</p><a class="btn btn-line" href="sitemap.xml">Ansehen</a></div></article>
    <article class="tile"><div class="bd"><div class="when">Neu · fehlt heute (404)</div><h3>robots.txt</h3><p>Lässt Suchmaschinen und KI-Assistenten alles lesen, verweist auf die Sitemap. Optionaler Ausschluss von KI-Training ist vorbereitet.</p><a class="btn btn-line" href="robots.txt">Ansehen</a></div></article>
    <article class="tile"><div class="bd"><div class="when">Neu · fehlt heute (404)</div><h3>llms.txt</h3><p>Kurzporträt für KI-Assistenten: Zimmer, Preise 2026, Konditionen, Anfahrt und Buchungslink-Format.</p><a class="btn btn-line" href="llms.txt">Ansehen</a></div></article>
    <article class="tile"><div class="bd"><div class="when">Strukturierte Daten</div><h3>schema-hotel.json</h3><p>schema.org „Hotel“ mit Adresse, Zeiten, Ausstattung, Zimmern und ab-Preisen – als JSON-LD in die Startseite einbauen.</p><a class="btn btn-line" href="schema-hotel.json">Ansehen</a></div></article>
    <article class="tile"><div class="bd"><div class="when">Umzug ohne Ranking-Verlust</div><h3>301-Weiterleitungen</h3><p>Alle alten Adressen auf die neuen – als .htaccess-Zeilen (der Server läuft auf Apache) und als Tabelle.</p><a class="btn btn-line" href="weiterleitungen.htaccess.txt">.htaccess</a> <a class="btn btn-line" href="weiterleitungen.csv" style="margin-top:8px">CSV</a></div></article>
    <article class="tile"><div class="bd"><div class="when">Buchungssystem</div><h3>DIRS21 als Link statt Fenster</h3><p>Heute öffnet <code>d21_api.ibe.open()</code> die Buchung als Overlay – die Adresse ändert sich nie. Dabei funktioniert ein direkter Link bereits (getestet 30.10.2026):</p><p><code style="font-size:12.5px;overflow-wrap:anywhere">reservation.one.dirs21.de/hotel-am-leuchtturmde?range=2027-05-14,2027-05-17&amp;culture=de-DE&amp;show_results=true</code></p><p>Die Buchungs-Buttons sollten auf diesen Link führen (neues Fenster oder eigene Seite /buchen/) – dann ist jede Suche teilbar und verlinkbar.</p><a class="btn btn-line" href="https://reservation.one.dirs21.de/hotel-am-leuchtturmde?range=2027-05-14,2027-05-17&amp;culture=de-DE&amp;show_results=true" target="_blank" rel="noopener">Link testen ↗</a></div></article>
  </div>
</div></section>
<section class="alt"><div class="wrap">
  <h2 class="caps">Neue Seitenstruktur</h2><div class="rule"></div>
  <p>Sprechende, kurze Adressen ohne Sprachkürzel in Großbuchstaben, ohne „1“ und „2“ im Namen. Doppelte Seiten (Kontakt, Impressum, Datenschutz und Anfahrt existieren heute je zweimal) werden zusammengeführt.</p>
  <div class="table-wrap"><table><thead><tr><th>Alte Adresse(n)</th><th>Neue Adresse</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="slots-h" style="margin-top:10px">Englisch nach demselben Muster unter /en/ (z. B. /en/rooms/panorama-terrace-double-room/).</p>
</div></section>
<section><div class="wrap narrow">
  <h2 class="caps">Gefunden auf der heutigen Website</h2><div class="rule"></div>
  <ul class="ticks">
    <li><b>Zwei Cookie-Abfragen hintereinander:</b> Nach der Abfrage der Website fragt das Buchungsfenster (DIRS21) ein zweites Mal. Die Buchung funktioniert mit beiden Antworten (getestet 30.10.2026 nachmittags), jede Abfrage ist aber ein möglicher Abbruchpunkt.</li>
    <li>Server meldet PHP 5.6.40 / 5.4.45 und OpenSSL 1.0.2 – alles ohne Sicherheitsupdates (5.6.40 ist die letzte PHP-5-Version, 2019). Die Seite war am 30.10.2026 mehrere Stunden komplett ausgefallen (Fehler 500); danach waren die PHP-Versionen andere als vorher.</li>
    <li>Nicht vorhandene Seiten leiten per 302 auf die Startseite um statt „404 nicht gefunden“ zu melden – Suchmaschinen und KI-Agenten sehen tote Links als gültig.</li>
    <li>Keine robots.txt, keine sitemap.xml, keine llms.txt.</li>
    <li>Buchung als Overlay (DIRS21) ohne eigene Adresse – nicht teilbar, nicht verlinkbar.</li>
    <li>Inhaltliche Widersprüche: siehe <a href="#pruefbericht">Prüfbericht</a> unten.</li>
    <li>Bewertungen nur als Grafik-Link, Fotos ohne Beschreibung und mit technischen Dateinamen.</li>
  </ul>
</div></section>
""" + pruefbericht() + """
"""
    page("vorschlag/index.html", "Technik-Paket – Konzeptentwurf Hotel am Leuchtturm", "Sitemap, robots.txt, llms.txt, strukturierte Daten und 301-Weiterleitungen für hotel-am-leuchtturm.de.", body, mbar=False)

# ---------------- Hosting-Dateien für den Entwurf ----------------
def hosting():
    open(os.path.join(OUT,"robots.txt"),"w").write("# Konzeptentwurf – bitte nicht indexieren.\nUser-agent: *\nDisallow: /\n")
    open(os.path.join(OUT,"vercel.json"),"w").write(json.dumps({
        "cleanUrls": True,
        "headers": [{"source":"/(.*)","headers":[{"key":"X-Robots-Tag","value":"noindex, nofollow, noarchive"}]}]
    }, indent=2))



# =====================================================================
# Englische Version (/en/) – gleiche Fakten wie die deutsche Seite
# =====================================================================
ROOMS_EN = {
 "panorama-terrassen-doppelzimmer": dict(name="Panorama Terrace Double Room", tag="Direct sea view and a 40 m² roof terrace", view="Direct sea view", floor="1st floor", size="20 m² (excl. bathroom)",
    bed="Double bed 180 × 200 cm, comfort height, electrically adjustable slatted frame", occ="max. 2 adults", bath="shower or shower and bathtub",
    special="The highlight: the 40 m² roof terrace – furnished in summer with a beach chair, two loungers and more seating – and the direct view of the Baltic Sea.", chip="40 m² roof terrace"),
 "panorama-doppelzimmer": dict(name="Panorama Double Room", tag="Direct sea view from the 2nd and 3rd floor", view="Direct sea view", floor="2nd and 3rd floor", size="20 m² (excl. bathroom)",
    bed="Double bed 180 × 200 cm, comfort height, electrically adjustable slatted frame", occ="max. 2 adults", bath="shower or shower and bathtub",
    special="Full of light, with a direct view of the beach and the Baltic Sea – at sunset one of the finest views in Warnemünde.", chip=""),
 "terrassen-doppelzimmer": dict(name="Terrace Double Room", tag="Private 12 m² roof terrace", view="Side sea view or view of the lighthouse and harbour entrance", floor="1st floor", size="17–20 m² (excl. bathroom)",
    bed="Double bed 180 × 200 cm, comfort height", occ="max. 2 adults", bath="shower",
    special="The special feature: a 12 m² roof terrace, furnished in summer with a lounger and seating.", chip="12 m² roof terrace"),
 "komfort-doppelzimmer": dict(name="Comfort Double Room", tag="Side sea view or lighthouse view", view="Side sea view or view of the lighthouse and harbour entrance", floor="1st, 2nd and 3rd floor", size="17–20 m² (excl. bathroom)",
    bed="Double bed 180 × 200 cm, comfort height, some extra long (2.10 m)", occ="max. 2 adults", bath="shower",
    special="Plenty of space in classic-modern boutique style – with a view of the Baltic Sea or of Warnemünde's landmark.", chip=""),
 "doppelzimmer": dict(name="Double Room", tag="Cosy under the roof", view="Top floor with electrically adjustable roof windows", floor="3rd floor", size="15–18 m² (excl. bathroom)",
    bed="Double bed 180 × 200 cm, comfort height", occ="max. 2 adults", bath="shower",
    special="Individually shaped rooms with a gently sloping ceiling – snug, quiet and in the heart of Warnemünde.", chip=""),
 "einzelzimmer": dict(name="Single Room", tag="Queen-size bed under the roof", view="Top floor with electrically adjustable roof windows", floor="3rd floor", size="15–18 m² (excl. bathroom)",
    bed="Queen-size bed 100 × 200 cm, comfort height", occ="1–2 adults", bath="shower",
    special="Ideal for solo travellers: individually shaped with a gently sloping ceiling and a queen-size bed.", chip=""),
}
COMMON_EN = ["Swivelling HD flat-screen satellite TV with radio", "USB sockets at bedside and desk", "Large desk", "2 armchairs with side tables",
             "Large illuminated wardrobe", "In-room safe", "Heated towel rail, cosmetic mirror, hairdryer, toiletries", "Free Wi-Fi", "24-hour reception and wake-up call"]
FAQ_EN = [
 ("What are the check-in and check-out times?", "Your room is ready from 3 pm on the day of arrival and available until 11 am on the day of departure. The reception is staffed around the clock."),
 ("Is breakfast included in the room rate?", "Room rates are without breakfast. You can add the breakfast buffet in our breakfast lounge, overlooking the promenade, when you book."),
 ("Where can I park?", "Am Leuchtturm is a pedestrian zone; you may drive up to the hotel to load and unload. Afterwards, park in the Kurhaus underground garage (approx. 400 m) at the hotel guest rate of €14 per 24 hours – tickets are available at reception."),
 ("Until when can I cancel free of charge?", "Hotel bookings can be cancelled free of charge up to 14 days before arrival, apartments up to four weeks before arrival."),
 ("Is there a minimum stay?", "Yes, depending on the season: 2 nights at weekends in low season, 4 nights in mid season, 6 nights in high season and 5 nights over Easter, Whitsun, Ascension Day and New Year's Eve. Shorter stays can be booked at short notice, subject to availability."),
 ("Are pets allowed?", "Out of consideration for all guests, we kindly ask you not to bring pets."),
 ("Can I stay before or after a cruise?", "Yes. The cruise terminal in Warnemünde is within walking distance. Ask us about luggage storage and a late check-out, subject to availability."),
 ("How do I get here by train?", "Take the S-Bahn from Rostock Hbf to Warnemünde. From the station it is about 500 metres on foot, across the station bridge and along the Alter Strom."),
]
FAQ_EN_LD = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ_EN]}

def en_room_href(R, slug): return f"{R}en/rooms/{EN_SLUG[slug]}.html"
def en_book(R, q=""): return f"{R}en/book.html" + (("?" + q) if q else "")

def searchbox_en(R):
    opts = "".join(f'<option value="{r["slug"]}">{ROOMS_EN[r["slug"]]["name"]}</option>' for r in ROOMS)
    return f"""<form class="searchbox" id="search" autocomplete="off">
  <div class="field"><label for="s-arr">Arrival</label><input type="date" id="s-arr" required></div>
  <div class="field"><label for="s-dep">Departure</label><input type="date" id="s-dep" required></div>
  <div class="field"><label for="s-ad">Guests</label><select id="s-ad"><option value="1">1 adult</option><option value="2" selected>2 adults</option></select></div>
  <div class="field"><label for="s-room">Room</label><select id="s-room"><option value="">All rooms</option>{opts}</select></div>
  <button class="btn btn-navy" type="submit">Check availability</button>
</form>"""

def card_en(r, R):
    x = ROOMS_EN[r["slug"]]; p = r["prices"]
    chips = f'<li>{e(x["view"].split(" or view of")[0])}</li><li>{e(x["size"].replace(" (excl. bathroom)",""))}</li>' + (f'<li>{e(x["chip"])}</li>' if x["chip"] else "")
    return f"""<article class="card">
  <a class="ph" href="{en_room_href(R, r['slug'])}"><img src="{R}img/{r['imgs'][0]}.jpg" alt="{e(x['name'])}" loading="lazy"></a>
  <div class="bd">
    <h3><a href="{en_room_href(R, r['slug'])}">{e(x['name'])}</a></h3>
    <ul class="chips">{chips}</ul>
    <div class="from">from <b>€{p[0]}</b> per night · excl. breakfast</div>
    <div><div class="slots-h">Next available dates <span class="demo">Demo</span></div><div class="slots" data-slots="{r['slug']}"></div></div>
    <div class="acts"><a class="btn btn-line" href="{en_room_href(R, r['slug'])}">Details</a><a class="btn btn-navy" href="{en_book(R, 'room=' + r['slug'] + '&amp;step=1')}">Book</a></div>
  </div>
</article>"""

HOTEL_LD_EN = dict(HOTEL_LD, url=REAL+"/en/", description="Owner-run boutique hotel on the beach promenade of Warnemünde, right by the lighthouse. 30 rooms, breakfast lounge overlooking the promenade, lobby with fireplace.",
                   priceRange="€139–339 per room and night (excl. breakfast)")

def home_en():
    R = "../"
    cards = "".join(card_en(r, R) for r in ROOMS)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q,a in FAQ_EN)
    body = f"""
<section class="hero" style="padding:0">
  <picture><source media="(max-width:640px)" srcset="../img/hero-promenade-960.jpg"><img class="hero-img" src="../img/hero-promenade.jpg" alt="View from the lighthouse onto Hotel am Leuchtturm, the beach promenade and the beach of Warnemünde" fetchpriority="high"></picture>
  <span class="hero-credit">The view from the lighthouse: hotel, promenade and beach</span>
  <div class="hero-copy"><div class="wrap">
    <div class="eyebrow">The view from the lighthouse onto our hotel · since 1850</div>
    <h1 class="caps">Right by the beach</h1>
    <p>Owner-run boutique hotel on the beach promenade, right opposite the lighthouse: 30 rooms, a breakfast lounge overlooking the promenade and a lobby with fireplace – just steps from the fine white sand of the Baltic Sea.</p>
  </div></div>
</section>
<div class="search"><div class="wrap">
  {searchbox_en(R)}
  <div class="perkline"><span>Best rate directly with the hotel</span><span>Free cancellation up to 14 days before arrival</span><span>Add parking when you book</span></div>
  <div class="note" data-n="EN" style="margin-left:auto;margin-right:auto"><b>Englische Version:</b> gleiche Struktur unter /en/ mit eigenen, englischen Adressen, per hreflang mit der deutschen Seite verknüpft – für Kreuzfahrt- und internationale Gäste. Der Sprachumschalter oben springt auf die passende Seite; auf der Buchungsseite bleibt die Auswahl erhalten. Die Buchung über DIRS21 öffnet sich auf Englisch.</div>
</div></div>

<section style="padding-top:64px"><div class="wrap">
  <div class="facts4">
    <div><b>91 %</b><span>"Very satisfied" – 1,563 reviews (Oct 2026)</span></div>
    <div><b>30 rooms</b><span>six categories, plus 4 apartments</span></div>
    <div><b>Since 1850</b><span>on historic foundations, renovated 2017</span></div>
    <div><b>24 hours</b><span>reception at your service</span></div>
  </div>
</div></section>

<section class="alt" id="rooms"><div class="wrap">
  <div class="center"><div class="eyebrow">Rooms &amp; rates</div><h2 class="caps">Your room by the sea</h2><div class="rule"></div>
  <p class="lead">Classic-modern boutique style, beds at comfort height and marble-look bathrooms. Choose your view – and book the next available date directly.</p></div>
  <div class="cards">{cards}</div>
  <p class="center" style="margin-top:30px"><a class="btn btn-line" href="rooms/index.html#rates">All rates &amp; conditions</a></p>
</div></section>

<div class="strip strip-video"><video class="strip-vid" autoplay muted loop playsinline preload="metadata" poster="../img/duenen-zoom-poster.jpg" aria-label="Slow camera move through the dunes towards Hotel am Leuchtturm"><source media="(max-width:640px)" src="../img/duenen-zoom-960.mp4" type="video/mp4"><source src="../img/duenen-zoom.mp4" type="video/mp4"></video>
  <div class="vcap"><div class="wrap"><div><div class="eyebrow">Behind the dunes</div><h2 class="caps">From the beach straight to the hotel</h2><p>Only the promenade and a few steps through the dunes lie between your room and the Baltic Sea.</p><p class="vnote">Short clip, animated with AI from a photo of the hotel.</p></div><a class="btn btn-white" href="book.html">Check availability</a></div></div></div>

<section><div class="wrap split">
  <div class="pic2"><img class="tall" src="../img/fruehstueck-1.jpg" alt="Breakfast lounge overlooking the beach promenade" loading="lazy" data-zoom><img src="../img/buffet.jpg" alt="Breakfast buffet" loading="lazy" data-zoom><img src="../img/fruehstueck-3.jpg" alt="Breakfast table" loading="lazy" data-zoom></div>
  <div><div class="eyebrow">Breakfast lounge</div><h2 class="caps">Breakfast with a view of the promenade</h2><div class="rule"></div>
  <p>The breakfast lounge is reserved for hotel guests: floor-to-ceiling windows, a maritime touch and a view of the bustle on the beach promenade. Simply add the buffet when you book.</p>
  <ul class="ticks"><li>Generous breakfast buffet</li><li>Floor-to-ceiling glazing in the 2017 veranda extension</li><li>For hotel guests only</li></ul></div>
</div></section>

<section class="alt"><div class="wrap split rev">
  <div class="pic"><img src="../img/lobby-2.jpg" alt="Lobby with glass fireplace" loading="lazy" data-zoom></div>
  <div><div class="eyebrow">Lobby &amp; library</div><h2 class="caps">Arrive by the fireplace</h2><div class="rule"></div>
  <p>Individual seating, a glass fireplace and a small library invite you to linger – after the beach in summer, after a walk along the wild Baltic in winter.</p>
  <p><a class="btn btn-line" href="gallery.html">View gallery</a></p></div>
</div></section>

<div class="strip"><img src="../img/stage-4.jpg" alt="Roof terrace with beach chair and lighthouse view" loading="lazy">
  <div class="ov"><div class="wrap"><div class="eyebrow" style="color:var(--aqua)">Panorama Terrace Double Room</div><h2 class="caps">40 m² roof terrace with beach chair</h2><p>Your private box seat above the promenade – with a direct view of the Baltic Sea and the lighthouse.</p><p><a class="btn btn-white" href="{en_room_href(R,'panorama-terrassen-doppelzimmer')}">View room</a></p></div></div></div>

<section><div class="wrap">
  <div class="center"><div class="eyebrow">Offers &amp; occasions</div><h2 class="caps">Book these dates early</h2><div class="rule"></div></div>
  <div class="tiles">
    <article class="tile"><img src="../img/aussen-39.jpg" alt="Hotel am Leuchtturm" loading="lazy"><div class="bd"><div class="when">All year</div><h3>Before or after your cruise</h3><p>A night by the sea before you sail from Warnemünde – the cruise centre is within walking distance.</p><a class="btn btn-line" href="offers/cruise.html">Learn more</a></div></article>
    <article class="tile"><img src="../img/lobby.jpg" alt="Lobby with fireplace" loading="lazy"><div class="bd"><div class="when">28 Oct – 20 Dec 2026</div><h3>Winter days in Warnemünde</h3><p>Hot drink by the fireplace, Comfort or Terrace Double Room, breakfast, visitor's tax and parking included – from €105 per person and night.</p><a class="btn btn-line" href="offers/winter-days-in-warnemuende.html">View offer</a></div></article>
    <article class="tile"><img src="../img/stage-6.jpg" alt="Beach and lighthouse" loading="lazy" style="object-position:85% 50%"><div class="bd"><div class="when">5–8 August 2027</div><h3>Hanse Sail</h3><p>Tall ships sail into the harbour right in front of the hotel – a room facing the harbour entrance is the best seat in town.</p><a class="btn btn-line" href="offers/hanse-sail.html">Hanse Sail stays</a></div></article>
  </div>
</div></section>

<section class="reviews"><div class="wrap">
  <div class="score"><div class="big">91 %</div><div><h2 class="caps" style="font-size:34px">"Very satisfied"</h2><div style="opacity:.8">from 1,563 reviews on 10 portals (Customer Alliance) · as of October 2026</div></div></div>
  <div class="quotes">
    <div class="quote">Space for a real guest review from Google or Tripadvisor – ideally one that describes the room and the view.<small>Name · source · date</small></div>
    <div class="quote">Space for a real guest review about the breakfast lounge overlooking the promenade.<small>Name · source · date</small></div>
    <div class="quote">Space for a real guest review about the team and the location by the lighthouse.<small>Name · source · date</small></div>
  </div>
</div></section>

<section><div class="wrap split">
  <div><div class="eyebrow">Apartment house by the lighthouse</div><h2 class="caps">More space, same location</h2><div class="rule"></div>
  <p>In the listed apartment house opposite the hotel, each of the two floors has a one-room apartment (40 m²) and a two-room apartment (60 m²) – with large panoramic windows overlooking the Baltic Sea, the beach and the lighthouse.</p>
  <ul class="ticks"><li>Kitchenette or kitchen, ideal for longer stays</li><li>Cleaning included when booking directly</li><li>Non-smoking apartments</li></ul>
  <p style="margin-top:22px"><a class="btn btn-navy" href="apartments.html">View apartments</a></p></div>
  <div class="pic"><img src="../img/apt-2.jpg" alt="Living area of the two-room apartment" loading="lazy" data-zoom></div>
</div></section>

<section class="alt"><div class="wrap split rev">
  <div class="pic"><img src="../img/geschichte-1905.jpg" alt="Historic postcard: Warnemünde beach and lighthouse around 1905" loading="lazy" data-zoom></div>
  <div><div class="eyebrow">Since 1850</div><h2 class="caps">The first hotel in town</h2><div class="rule"></div>
  <p>In 1850 H. F. Ohlerich built the "Hotel Pavillon" here – just as Warnemünde was becoming a seaside resort. In 1897 the lighthouse was built right in front of it. Today an owner-run hotel continues the story.</p>
  <p><a class="btn btn-line" href="history.html">The full story</a></p></div>
</div></section>

<section id="faq"><div class="wrap narrow">
  <div class="eyebrow">Good to know</div><h2 class="caps">Frequently asked questions</h2><div class="rule"></div>
  {faq}
</div></section>
"""
    page("en/index.html", "Hotel am Leuchtturm – boutique hotel on the beach in Warnemünde, Germany",
         "Owner-run boutique hotel since 1850 on the beach promenade of Warnemünde, right by the lighthouse. 30 rooms with sea or lighthouse views, some with roof terrace. Close to the cruise terminal.",
         body, lang="en", schema=[HOTEL_LD_EN, FAQ_EN_LD])

def rooms_index_en():
    R = "../../"
    rows = "".join(f'<tr><td><a href="{EN_SLUG[r["slug"]]}.html">{e(ROOMS_EN[r["slug"]]["name"])}</a><br><small style="color:var(--muted)">{e(ROOMS_EN[r["slug"]]["view"])}</small></td>' + "".join(f'<td class="num">from €{p}</td>' for p in r["prices"]) + "</tr>" for r in ROOMS)
    cards = "".join(card_en(r, R) for r in ROOMS)
    body = f"""
<div class="wrap crumbs"><a href="../index.html">Home</a> › Rooms &amp; rates</div>
<section style="padding-top:28px"><div class="wrap">
  <div class="eyebrow">Rooms &amp; rates</div><h1 class="caps" style="font-size:clamp(34px,4.6vw,54px)">Six categories, one view of the sea</h1><div class="rule"></div>
  <p class="lead">After its complete renovation in 2017, the hotel welcomes you in classic-modern boutique style: light-filled rooms with and without terrace, beds at comfort height and bathrooms with the latest fittings.</p>
  <div class="cards">{cards}</div>
</div></section>
<section class="alt" id="rates"><div class="wrap">
  <div class="eyebrow">Rates 2026</div><h2 class="caps">Rates &amp; conditions</h2><div class="rule"></div>
  <p>Daily rates in euros per room and night incl. VAT, without breakfast. Valid until a new price list is published.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Room category</th><th class="num">Low season<small>5 Jan–31 Mar · 1 Nov–23 Dec</small></th><th class="num">Mid season<small>1 Apr–12 May · 4 Oct–31 Oct</small></th><th class="num">High season<small>13 May–3 Oct · 24 Dec–4 Jan</small></th></tr></thead>
    <tbody>{rows}<tr><td>Extra bed, 3rd person</td><td class="num">€75</td><td class="num">€75</td><td class="num">€75</td></tr></tbody>
  </table></div>
  <div class="split" style="margin-top:40px;align-items:start;gap:40px">
    <div><h3>Good to know</h3><ul class="ticks">
      <li>Check-in from 3 pm, check-out until 11 am</li>
      <li>Free cancellation up to 14 days before arrival</li>
      <li>Payment by debit card (EC), cash or bank transfer in advance</li>
      <li>No pets</li>
      <li>Bicycles only by prior arrangement</li></ul></div>
    <div><h3>Minimum stay</h3><ul class="ticks">
      <li>Weekends in low season: 2 nights</li>
      <li>Mid season: 4 nights</li>
      <li>High season: 6 nights</li>
      <li>Easter, Whitsun, Ascension Day, New Year's Eve: 5 nights</li>
      <li>Shorter stays at short notice, subject to availability</li></ul></div>
  </div>
</div></section>
"""
    page("en/rooms/index.html", "Rooms & rates – Hotel am Leuchtturm, Warnemünde",
         "Six room categories with sea or lighthouse views, some with roof terrace. 2026 rates from €139 per night, free cancellation up to 14 days before arrival.",
         body, active="en/rooms/index.html", lang="en", schema=HOTEL_LD_EN)

def room_page_en(r):
    R = "../../"; x = ROOMS_EN[r["slug"]]; p = r["prices"]; slug_en = EN_SLUG[r["slug"]]
    gal = "".join(f'<img src="{R}img/{k}.jpg" alt="{e(x["name"])} – photo {i+1}" loading="{"eager" if i==0 else "lazy"}" data-zoom>' for i,k in enumerate(r["imgs"]))
    other = " · ".join(f'<a href="{EN_SLUG[o["slug"]]}.html">{e(ROOMS_EN[o["slug"]]["name"])}</a>' for o in ROOMS if o["slug"] != r["slug"])
    feats = "".join(f"<li>{e(f)}</li>" for f in [x["bed"]] + COMMON_EN)
    banner = f'<div class="strip" style="margin-top:56px"><img src="{R}img/{r["banner"]}.jpg" alt="Roof terrace with beach chair" loading="lazy"><div class="ov"><div class="wrap"><h2 class="caps">Your roof terrace</h2><p>40 m², a beach chair, two loungers – and the Baltic Sea right in front of you.</p></div></div></div>' if r["banner"] else ""
    room_ld = {"@context":"https://schema.org","@type":"HotelRoom","name":x["name"],"description":x["special"],"bed":x["bed"],"occupancy":{"@type":"QuantitativeValue","maxValue":2},
               "containedInPlace":{"@type":"Hotel","name":"Hotel am Leuchtturm","url":REAL+"/en/"},
               "offers":{"@type":"Offer","priceCurrency":"EUR","price":p[0],"description":"From-rate per night, low season 2026, excl. breakfast"}}
    body = f"""
<div class="wrap crumbs"><a href="../index.html">Home</a> › <a href="index.html">Rooms &amp; rates</a> › {e(x['name'])}</div>
<section style="padding-top:22px"><div class="wrap">
  <div class="eyebrow">{e(x['tag'])}</div>
  <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">{e(x['name'])}</h1>
  <div class="room-top">
    <div>
      <div class="gallery">{gal}</div>
      <p style="margin-top:26px;font-size:18px">{e(x['special'])}</p>
      <p>Spacious and comfortable in classic-modern design, furnished in boutique style with high-quality materials in light, warm tones. The elegant black-and-white marble-look bathroom has a {e(x['bath'])} and a cosmetic mirror.</p>
      <ul class="spec">
        <li><b>View</b>{e(x['view'])}</li><li><b>Size</b>{e(x['size'])}</li>
        <li><b>Floor</b>{e(x['floor'])}</li><li><b>Occupancy</b>{e(x['occ'])}</li>
        <li><b>Bathroom</b>{e(x['bath'].capitalize())}</li><li><b>Rate</b>from €{p[0]} · €{p[1]} · €{p[2]} per night (low / mid / high season), excl. breakfast</li>
      </ul>
      <h3 style="margin-top:34px">Room features</h3>
      <ul class="kv">{feats}</ul>
      {('<div class="note" data-n="3"><b>Widerspruch:</b> ' + e(r['warn'][len('Bitte prüfen: '):]) + '</div>') if r.get('warn') else ''}
    </div>
    <aside class="bookcard" data-bookcard="{r['slug']}">
      <div class="eyebrow" style="margin:0">Book directly with the hotel</div>
      <h3>When would you like to come?</h3>
      <div class="grid2">
        <div class="field"><label for="b-arr">Arrival</label><input type="date" id="b-arr"></div>
        <div class="field"><label for="b-dep">Departure</label><input type="date" id="b-dep"></div>
      </div>
      <div class="field" style="margin-top:10px"><label for="b-ad">Guests</label><select id="b-ad"><option value="1">1 adult</option><option value="2" selected>2 adults</option></select></div>
      <div class="sum" id="b-sum"></div>
      <a class="btn btn-navy" id="b-go" href="../book.html" style="width:100%;margin-top:14px">Book this room</a>
      <div class="slots-h" style="margin-top:14px">Next available dates <span class="demo">Demo</span></div>
      <div class="slots" data-slots="{r['slug']}"></div>
      <p class="slots-h" style="margin-top:12px">Free cancellation up to 14 days before arrival · Questions? <a href="tel:{TEL_HREF}">+49 381 54370</a></p>
    </aside>
  </div>
</div></section>
{banner}
<section class="alt" style="padding:48px 0"><div class="wrap"><p style="margin:0"><b style="color:var(--navy)">Other rooms:</b> {other}</p></div></section>
"""
    page(f"en/rooms/{slug_en}.html", f"{x['name']} – Hotel am Leuchtturm, Warnemünde",
         f"{x['name']} at Hotel am Leuchtturm: {x['view']}, {x['size'].replace(' (excl. bathroom)','')}, {x['floor']}. From €{p[0]} per night. Book direct.",
         body, active="en/rooms/index.html", lang="en", schema=room_ld)

def apartments_en():
    body = """
<div class="wrap crumbs"><a href="index.html">Home</a> › Apartment house</div>
<section style="padding-top:22px"><div class="wrap">
  <div class="eyebrow">Opposite the hotel · listed building</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Apartment house by the lighthouse</h1><div class="rule"></div>
  <div class="split" style="align-items:start">
    <div>
      <p class="lead">On each of the two floors there is a one-room and a two-room non-smoking apartment – comfortably furnished for longer stays, with large panoramic windows overlooking the Baltic Sea, the beach and the promenade with the lighthouse.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Apartment</th><th class="num">Low season</th><th class="num">Mid season</th><th class="num">High season</th></tr></thead>
        <tbody><tr><td><b>One-room apartment</b><br><small>40 m², sea view</small></td><td class="num">€125</td><td class="num">from €155</td><td class="num">from €175</td></tr>
        <tr><td><b>Two-room apartment</b><br><small>60 m², sea view</small></td><td class="num">from €155</td><td class="num">from €185</td><td class="num">from €215</td></tr>
        <tr><td>Extra bed, 3rd person</td><td class="num">€50</td><td class="num">€50</td><td class="num">€50</td></tr></tbody></table></div>
      <p class="slots-h" style="margin-top:8px">Rates per apartment and night for 2 people, excl. breakfast. <b>As currently published (2023 price list).</b></p>
      <h3 style="margin-top:28px">One-room apartment · 40 m²</h3>
      <p>Combined sleeping and living area with kitchenette (2-zone ceramic hob, microwave, fridge with freezer compartment); bathroom with bathtub and shower screen.</p>
      <h3>Two-room apartment · 60 m²</h3>
      <p>Separate bedroom, living area with a large dining table right by the panoramic window, kitchen (4-zone ceramic hob, dishwasher, microwave, fridge) and bathroom with shower.</p>
      <ul class="ticks"><li>Cleaning included only when booking directly with the hotel</li><li>Minimum stay 3 nights in low season, longer otherwise</li><li>Free cancellation up to four weeks before arrival</li><li>No pets</li></ul>
      <p style="margin-top:22px"><a class="btn btn-navy" href="#" data-toast="In this concept, apartments run through the same booking flow as the hotel rooms.">Enquire &amp; book</a></p>
    </div>
    <div class="gallery"><img src="../img/apt-haus.jpg" alt="Apartment house by the lighthouse" data-zoom><img src="../img/apt-1.jpg" alt="One-room apartment" loading="lazy" data-zoom><img src="../img/apt-2.jpg" alt="Two-room apartment living area" loading="lazy" data-zoom><img src="../img/apt-3.jpg" alt="Apartment kitchen" loading="lazy" data-zoom></div>
  </div>
</div></section>
"""
    page("en/apartments.html", "Apartment house by the lighthouse – holiday apartments with sea view, Warnemünde",
         "Four non-smoking apartments (40 and 60 m²) in the listed house opposite Hotel am Leuchtturm, with panoramic views of the Baltic Sea and the lighthouse.",
         body, active="en/apartments.html", lang="en", schema=HOTEL_LD_EN)

def offers_en():
    offer_ld = {"@context":"https://schema.org","@type":"Offer","name":"Winter days in Warnemünde","price":105,"priceCurrency":"EUR",
                "description":"Per person and night in a double room: hot drink by the fireplace, Comfort or Terrace Double Room, breakfast, visitor's tax and free parking.",
                "validFrom":"2026-10-28","validThrough":"2026-12-20","offeredBy":{"@type":"Hotel","name":"Hotel am Leuchtturm"}}
    body = f"""
<div class="wrap crumbs"><a href="../index.html">Home</a> › <a href="index.html">Offers</a> › Winter days in Warnemünde</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div>
    <div class="eyebrow">Package · 28 October to 20 December 2026</div>
    <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Winter days in Warnemünde</h1><div class="rule"></div>
    <p class="lead">Discover the special charm of the Baltic Sea in winter – the contrast between the rough, roaring sea and the calm, cosy atmosphere of our hotel.</p>
    <h3>Included in the package</h3>
    <ul class="ticks"><li>A hot drink by our fireplace on arrival</li><li>Overnight stay in a Comfort or Terrace Double Room</li><li>Generous breakfast</li><li>Local visitor's tax</li><li>Free parking in the Kurhaus garage</li></ul>
    <p style="margin-top:22px;font-size:18px">Per person and night in a double room <b class="fig" style="font-size:32px;color:var(--navy)">from €105</b></p>
    <p><a class="btn btn-navy" href="{en_book('../../', 'offer=wintertage&amp;room=komfort-doppelzimmer&amp;arrival=2026-11-20&amp;departure=2026-11-22&amp;adults=2&amp;step=2')}">Book this package</a></p>
    <p class="slots-h">Subject to availability.</p>
  </div>
  <div class="pic2"><img class="tall" src="../../img/lobby-2.jpg" alt="Lobby with fireplace" data-zoom><img src="../../img/kdz-1.jpg" alt="Comfort Double Room" loading="lazy" data-zoom><img src="../../img/fruehstueck-2.jpg" alt="Breakfast lounge" loading="lazy" data-zoom></div>
</div></section>
"""
    page("en/offers/winter-days-in-warnemuende.html", "Winter days in Warnemünde – package at Hotel am Leuchtturm",
         "Winter package: hot drink by the fireplace, double room, breakfast, visitor's tax and parking included, from €105 per person and night.",
         body, active="en/offers/index.html", lang="en", schema=offer_ld)
    body2 = f"""
<div class="wrap crumbs"><a href="../index.html">Home</a> › Offers</div>
<section style="padding-top:22px"><div class="wrap">
  <div class="eyebrow">Packages &amp; occasions</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Offers</h1><div class="rule"></div>
  <div class="tiles">
    <article class="tile"><img src="../../img/lobby.jpg" alt="Lobby with fireplace" loading="lazy"><div class="bd"><div class="when">28 Oct – 20 Dec 2026</div><h3>Winter days in Warnemünde</h3><p>Hot drink by the fireplace, breakfast, visitor's tax and parking included – from €105 per person/night.</p><a class="btn btn-navy" href="winter-days-in-warnemuende.html">View offer</a></div></article>
    <article class="tile"><img src="../../img/aussen-37.jpg" alt="Hotel am Leuchtturm" loading="lazy"><div class="bd"><div class="when">All year</div><h3>Before or after your cruise</h3><p>A night by the sea, a short walk from the cruise centre.</p><a class="btn btn-navy" href="cruise.html">Learn more</a></div></article>
    <article class="tile"><img src="../../img/stage-4.jpg" alt="Roof terrace" loading="lazy"><div class="bd"><div class="when">5–8 August 2027</div><h3>Hanse Sail from your room</h3><p>Tall ships in the harbour entrance – and rooms that look onto it, bookable early.</p><a class="btn btn-navy" href="hanse-sail.html">Hanse Sail stays</a></div></article>
  </div>
</div></section>
"""
    page("en/offers/index.html", "Offers & packages – Hotel am Leuchtturm, Warnemünde",
         "Packages at Hotel am Leuchtturm in Warnemünde, e.g. Winter days in Warnemünde from €105 per person and night.",
         body2, active="en/offers/index.html", lang="en", schema=HOTEL_LD_EN)

def history_en():
    steps = [("1850","H. F. Ohlerich builds the single-storey \"Hotel Pavillon\" as Warnemünde begins to develop into a seaside resort – the first hotel in town."),
             ("~1880","Almost 30 years later the building is extended to three storeys."),
             ("1897","The lighthouse – Warnemünde's landmark – is built right in front of the hotel."),
             ("until 1920","The spa garden lies in front of the hotel, a popular destination. The ground floor houses a restaurant, and the beach hall is a popular dance venue."),
             ("1950","The last owner, Elisabeth Colas, is expropriated in \"Aktion Rose\". The hotel is renamed \"Meer des Friedens\" (Sea of Peace)."),
             ("after 1989","The hotel is returned to Ms Colas, who leaves it to a parish."),
             ("1996","Extension from 20 to 30 rooms; the first floor gets a wraparound roof terrace."),
             ("2013","Last change of ownership – the name \"Hotel am Leuchtturm\" is kept."),
             ("2017","Complete renovation and veranda extension with new reception, lobby with fireplace and a breakfast lounge overlooking the promenade.")]
    tl = "".join(f"<li><b>{y}</b><p style='margin:0'>{e(t)}</p></li>" for y,t in steps)
    body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> › History</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div><div class="eyebrow">A hotel since 1850</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">How it all began</h1><div class="rule"></div>
  <p class="lead">Today's Hotel am Leuchtturm stands on foundations from 1850 – and has witnessed more than 170 years of Warnemünde history.</p>
  <ol class="timeline">{tl}</ol></div>
  <div><div class="pic"><img src="../img/geschichte-1905.jpg" alt="Beach life in Warnemünde around 1900" data-zoom></div><p class="slots-h" style="margin-top:8px">Beach life around 1900 – historic postcard</p>
  <div class="pic" style="margin-top:22px"><img src="../img/aussen-37.jpg" alt="The hotel today" loading="lazy" data-zoom></div><p class="slots-h" style="margin-top:8px">The hotel today, after the 2017 renovation</p></div>
</div></section>
"""
    page("en/history.html", "History since 1850 – Hotel am Leuchtturm, Warnemünde",
         "From Hotel Pavillon in 1850 to Hotel am Leuchtturm: the story of the first hotel in Warnemünde.", body, active="en/history.html", lang="en", schema=HOTEL_LD_EN)

def location_en():
    body = """
<div class="wrap crumbs"><a href="index.html">Home</a> › Location &amp; directions</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div><div class="eyebrow">Am Leuchtturm 16 · 18119 Rostock-Warnemünde · Germany</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Location &amp; directions</h1><div class="rule"></div>
  <p class="lead">Right on the beach promenade, opposite the lighthouse – the beach, the Alter Strom and the station are all within walking distance.</p>
  <h3 style="margin-top:26px">By train</h3>
  <p>Take an intercity train to Rostock Hbf, then the S-Bahn to Warnemünde. From the station, cross the station bridge and walk along the Alter Strom: about 500 m to the hotel.</p>
  <h3>By cruise ship</h3>
  <p>The Warnemünde cruise terminal is within walking distance along the Alter Strom. We are happy to store your luggage.</p>
  <h3>By car</h3>
  <p><b>From Berlin:</b> A19 to the end, through the Warnow tunnel (toll) to Lütten Klein, then B 103 to Warnemünde.<br><b>From Hamburg:</b> A1 to the Lübeck junction, A20 towards Rostock, exit Rostock-West, B 103 to Warnemünde.</p>
  <h3>Parking</h3>
  <p>Since 2018 Am Leuchtturm has been a pedestrian zone. You may drive up to the hotel to load and unload. Afterwards, park in the <b>Kurhaus underground garage</b> (approx. 400 m, on the promenade) at the hotel guest rate of <b>€14 per 24 hours</b>.</p>
  <h3>By plane</h3>
  <p>Rostock-Laage airport. For a shuttle to the hotel, please contact us: <a href="tel:+4938154370">+49 381 54370</a>.</p></div>
  <div><iframe title="Map: Hotel am Leuchtturm, Warnemünde" style="width:100%;aspect-ratio:4/5;border:0;border-radius:10px;box-shadow:var(--shadow)" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=12.0760%2C54.1770%2C12.0950%2C54.1850&amp;layer=mapnik&amp;marker=54.1814%2C12.0862"></iframe>
  <p class="slots-h" style="margin-top:8px">Map © OpenStreetMap contributors · marker approximate</p></div>
</div></section>
"""
    page("en/location.html", "Location & directions – Hotel am Leuchtturm, Warnemünde",
         "Directions to Hotel am Leuchtturm in Warnemünde by train, cruise ship, car and plane. Parking in the Kurhaus garage for €14 per 24 hours.",
         body, active="en/location.html", lang="en", schema=HOTEL_LD_EN)

def gallery_en():
    keys = ["aussen-37","ptdz-5","fruehstueck-1","lobby-2","pdz-4","tdz-3","buffet","kdz-1","bad","stage-4","pdz-1","fruehstueck-2","collage-3","kdz-2","dz-4","ez-1","lobby","fruehstueck-3","collage-1","tdz-1","apt-2","ptdz-2","collage-2","aussen-39"]
    imgs = "".join(f'<img src="../img/{k}.jpg" alt="Hotel am Leuchtturm – photo" loading="lazy" data-zoom>' for k in keys)
    body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> › Gallery</div>
<section style="padding-top:22px"><div class="wrap"><div class="eyebrow">Photo gallery</div><h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Impressions</h1><div class="rule"></div>
<div class="masonry">{imgs}</div></div></section>
"""
    page("en/gallery.html", "Gallery – Hotel am Leuchtturm, Warnemünde", "Photos of Hotel am Leuchtturm: rooms, breakfast lounge, lobby with fireplace, roof terrace and views of the Baltic Sea and the lighthouse.", body, lang="en", schema=HOTEL_LD_EN)

def booking_en():
    body = """
<div class="wrap crumbs"><a href="index.html">Home</a> › Book online</div>
<section style="padding-top:22px" id="booking"><div class="wrap">
  <div class="eyebrow">Directly with the hotel · best rate</div><h1 class="caps" style="font-size:clamp(30px,4vw,46px)">Book online</h1>
  <form class="searchbox" id="k-form" style="margin-top:22px;box-shadow:none;border:1px solid var(--line)">
    <div class="field"><label for="k-arr">Arrival</label><input type="date" id="k-arr"></div>
    <div class="field"><label for="k-dep">Departure</label><input type="date" id="k-dep"></div>
    <div class="field"><label for="k-ad">Guests</label><select id="k-ad"><option value="1">1 adult</option><option value="2">2 adults</option></select></div>
    <div></div>
    <button class="btn btn-line" type="submit">Change dates</button>
  </form>
  <nav class="stepper" id="stepper" aria-label="Booking steps"><a href="#">1 · Room</a><a href="#">2 · Rate</a><a href="#">3 · Extras</a><a href="#">4 · Summary</a></nav>
  <div class="bk"><div id="step"></div><aside class="summary" id="summary"></aside></div>
</div></section>
"""
    page("en/book.html", "Book online – Hotel am Leuchtturm, Warnemünde", "Book a room at Hotel am Leuchtturm directly with the hotel – with total price, extras and a shareable booking link.", body, mbar=True, mbar_href="#step", lang="en")

def build_en():
    home_en(); rooms_index_en(); [room_page_en(r) for r in ROOMS]; apartments_en(); offers_en(); history_en(); location_en(); gallery_en(); booking_en()


# =====================================================================
# Anlass-Seiten und Gutscheine (DE + EN)
# =====================================================================
HANSE_LD = {"@context":"https://schema.org","@type":"Event","name":"Hanse Sail 2027","startDate":"2027-08-05","endDate":"2027-08-08",
            "location":{"@type":"Place","name":"Rostock und Warnemünde","address":"Rostock, Deutschland"}}

def hanse_sail():
    body = """
<div class="wrap crumbs"><a href="../index.html">Startseite</a> › <a href="index.html">Angebote</a> › Hanse Sail</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div>
    <div class="eyebrow">Hanse Sail 2027 · 5. bis 8. August</div>
    <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Hanse Sail vom Hotel aus</h1><div class="rule"></div>
    <p class="lead">Zur Hanse Sail laufen Großsegler und Traditionsschiffe durch die Hafeneinfahrt von Warnemünde ein – direkt am Leuchtturm, direkt vor dem Hotel.</p>
    <h3>Die besten Zimmer dafür</h3>
    <ul class="ticks">
      <li><a href="../zimmer/terrassen-doppelzimmer.html">Terrassen-Doppelzimmer</a> – je nach Zimmer Blick auf Leuchtturm und Hafeneinfahrt, eigene 12 m² Dachterrasse</li>
      <li><a href="../zimmer/komfort-doppelzimmer.html">Komfort-Doppelzimmer</a> – seitlicher Ostseeblick oder Blick auf Leuchtturm mit Hafeneinfahrt</li>
      <li><a href="../zimmer/panorama-terrassen-doppelzimmer.html">Panorama-Terrassen-Doppelzimmer</a> – direkter Ostseeblick, 40 m² Dachterrasse mit Strandkorb</li>
    </ul>
    <h3 style="margin-top:26px">Gut zu wissen</h3>
    <ul class="ticks">
      <li>Die Hanse Sail fällt in die Hauptsaison: Mindestaufenthalt 6 Nächte, kürzere Aufenthalte kurzfristig bei Verfügbarkeit.</li>
      <li>Preise 2027 stehen noch nicht fest. Zur Orientierung Hauptsaison 2026: ab 229 € bis ab 339 € pro Zimmer und Nacht, ohne Frühstück.</li>
      <li>Kostenfrei stornierbar bis 14 Tage vor Anreise.</li>
    </ul>
    <p style="margin-top:24px"><a class="btn btn-navy" href="../buchen.html?arrival=2027-08-04&amp;departure=2027-08-10&amp;adults=2&amp;room=terrassen-doppelzimmer&amp;step=2">Zur Hanse Sail buchen</a></p>
    <p class="slots-h">Termin laut Veranstaltungskalender der Stadt; bitte vor Veröffentlichung mit dem offiziellen Programm abgleichen.</p>
    <div class="note" data-n="6"><b>Event-Seite mit vorausgefüllter Buchung:</b> Der Button öffnet die Buchung schon mit Zimmer und Reisedaten rund um die Hanse Sail. Solche Seiten beantworten genau die Suche „Hotel Hanse Sail Warnemünde“ – bei Google und bei ChatGPT.</div>
  </div>
  <div><div class="pic"><img src="../img/tdz-3.jpg" alt="Terrassen-Doppelzimmer" data-zoom></div>
  <div class="pic" style="margin-top:16px"><img src="../img/stage-6.jpg" alt="Strand, Leuchtturm und Hafeneinfahrt von Warnemünde" style="aspect-ratio:3/1" loading="lazy" data-zoom></div></div>
</div></section>
"""
    page("angebote/hanse-sail.html", "Hanse Sail 2027 – Hotel am Leuchtturm direkt an der Hafeneinfahrt Warnemünde",
         "Hanse Sail 2027 (5.–8. August) vom Hotel am Leuchtturm aus: Zimmer mit Blick auf Leuchtturm und Hafeneinfahrt, früh buchbar.",
         body, active="angebote/index.html", schema=HANSE_LD)

def hanse_sail_en():
    body = """
<div class="wrap crumbs"><a href="../index.html">Home</a> › <a href="index.html">Offers</a> › Hanse Sail</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div>
    <div class="eyebrow">Hanse Sail 2027 · 5 to 8 August</div>
    <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Hanse Sail from the hotel</h1><div class="rule"></div>
    <p class="lead">During Hanse Sail, tall ships and traditional sailing vessels enter the harbour of Warnemünde – right by the lighthouse, right in front of the hotel.</p>
    <h3>The best rooms for it</h3>
    <ul class="ticks">
      <li><a href="../rooms/terrace-double-room.html">Terrace Double Room</a> – depending on the room, a view of the lighthouse and harbour entrance, private 12 m² roof terrace</li>
      <li><a href="../rooms/comfort-double-room.html">Comfort Double Room</a> – side sea view or view of the lighthouse and harbour entrance</li>
      <li><a href="../rooms/panorama-terrace-double-room.html">Panorama Terrace Double Room</a> – direct sea view, 40 m² roof terrace with beach chair</li>
    </ul>
    <h3 style="margin-top:26px">Good to know</h3>
    <ul class="ticks">
      <li>Hanse Sail falls in the high season: minimum stay 6 nights, shorter stays at short notice, subject to availability.</li>
      <li>2027 rates are not yet published. For orientation, high season 2026: from €229 to from €339 per room and night, excl. breakfast.</li>
      <li>Free cancellation up to 14 days before arrival.</li>
    </ul>
    <p style="margin-top:24px"><a class="btn btn-navy" href="../book.html?arrival=2027-08-04&amp;departure=2027-08-10&amp;adults=2&amp;room=terrassen-doppelzimmer&amp;step=2">Book for Hanse Sail</a></p>
    <p class="slots-h">Dates as listed in the city's event calendar.</p>
  </div>
  <div><div class="pic"><img src="../../img/tdz-3.jpg" alt="Terrace Double Room" data-zoom></div>
  <div class="pic" style="margin-top:16px"><img src="../../img/stage-6.jpg" alt="Beach, lighthouse and harbour entrance of Warnemünde" style="aspect-ratio:3/1" loading="lazy" data-zoom></div></div>
</div></section>
"""
    page("en/offers/hanse-sail.html", "Hanse Sail 2027 – Hotel am Leuchtturm at the harbour entrance of Warnemünde",
         "Hanse Sail 2027 (5–8 August) from Hotel am Leuchtturm: rooms overlooking the lighthouse and harbour entrance, bookable early.",
         body, active="en/offers/index.html", lang="en", schema=HANSE_LD)

def cruise():
    body = """
<div class="wrap crumbs"><a href="../index.html">Startseite</a> › <a href="index.html">Angebote</a> › Kreuzfahrt</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div>
    <div class="eyebrow">Ganzjährig · Warnemünde Cruise Center</div>
    <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Vor oder nach der Kreuzfahrt</h1><div class="rule"></div>
    <p class="lead">Warnemünde ist einer der großen Kreuzfahrthäfen an der Ostsee. Das Cruise Center liegt am Bahnhof Warnemünde – vom Hotel zu Fuß über die Bahnhofsbrücke erreichbar (ca. 500 m bis zum Bahnhof).</p>
    <h3>Ihre Nacht am Meer</h3>
    <ul class="ticks">
      <li>Anreise mit dem Zug: IC bis Rostock Hbf, S-Bahn bis Warnemünde</li>
      <li>Zimmer ab 15 Uhr, Abreise bis 11 Uhr – Rezeption rund um die Uhr</li>
      <li>Abends an den Strand, morgens Frühstück mit Blick auf die Promenade</li>
      <li>Gepäckaufbewahrung und später Check-out am Abreisetag <span class="demo">Vorschlag</span></li>
    </ul>
    <p class="slots-h" style="margin-top:12px">Hinweis: Laut Preisliste gilt ein Mindestaufenthalt (Nebensaison am Wochenende 2, Zwischensaison 4, Hauptsaison 6 Nächte); einzelne Nächte sind kurzfristig bei Verfügbarkeit buchbar.</p>
    <div class="note" data-n="4"><b>Entscheidung nötig:</b> Eine Seite für Kreuzfahrtgäste lohnt sich nur, wenn eine einzelne Nacht auch buchbar ist. Vorschlag: Kreuzfahrt-Nächte vom Mindestaufenthalt ausnehmen – oder die Seite weglassen.</div>
    <p style="margin-top:22px"><a class="btn btn-navy" href="../buchen.html?room=panorama-doppelzimmer&amp;step=1">Nacht vor der Kreuzfahrt buchen</a> <a class="btn btn-line" href="../en/offers/cruise.html" lang="en">English</a></p>
    <div class="note" data-n="3"><b>Zielgruppe mit eigener Seite:</b> Viele Kreuzfahrtgäste kommen aus dem Ausland und suchen auf Englisch („hotel near Warnemünde cruise terminal“). Diese Seite gibt es deshalb in beiden Sprachen.</div>
  </div>
  <div class="pic2"><img class="tall" src="../img/aussen-39.jpg" alt="Hotel am Leuchtturm" data-zoom><img src="../img/pdz-4.jpg" alt="Panorama-Doppelzimmer mit Blick auf die Ostsee" loading="lazy" data-zoom><img src="../img/fruehstueck-1.jpg" alt="Frühstückslounge" loading="lazy" data-zoom></div>
</div></section>
"""
    page("angebote/kreuzfahrt.html", "Hotel vor oder nach der Kreuzfahrt in Warnemünde – Hotel am Leuchtturm",
         "Übernachten vor oder nach der Kreuzfahrt: Das Hotel am Leuchtturm liegt an der Strandpromenade, das Cruise Center am Bahnhof Warnemünde ist zu Fuß erreichbar.",
         body, active="angebote/index.html", schema=HOTEL_LD)

def cruise_en():
    body = """
<div class="wrap crumbs"><a href="../index.html">Home</a> › <a href="index.html">Offers</a> › Cruise</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div>
    <div class="eyebrow">All year · Warnemünde Cruise Center</div>
    <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Before or after your cruise</h1><div class="rule"></div>
    <p class="lead">Warnemünde is one of the major cruise ports on the Baltic Sea. The cruise centre is next to Warnemünde station – within walking distance of the hotel across the station bridge (about 500 m to the station).</p>
    <h3>Your night by the sea</h3>
    <ul class="ticks">
      <li>By train: intercity to Rostock Hbf, then the S-Bahn to Warnemünde</li>
      <li>Rooms from 3 pm, check-out until 11 am – reception open around the clock</li>
      <li>Evening walk on the beach, breakfast overlooking the promenade</li>
      <li>Luggage storage and late check-out on departure day <span class="demo">Proposal</span></li>
    </ul>
    <p class="slots-h" style="margin-top:12px">Please note: per the price list a minimum stay applies (low-season weekends 2, mid season 4, high season 6 nights); single nights can be booked at short notice, subject to availability.</p>
    <p style="margin-top:22px"><a class="btn btn-navy" href="../book.html?room=panorama-doppelzimmer&amp;step=1">Book a night before your cruise</a></p>
  </div>
  <div class="pic2"><img class="tall" src="../../img/aussen-39.jpg" alt="Hotel am Leuchtturm" data-zoom><img src="../../img/pdz-4.jpg" alt="Panorama Double Room with sea view" loading="lazy" data-zoom><img src="../../img/fruehstueck-1.jpg" alt="Breakfast lounge" loading="lazy" data-zoom></div>
</div></section>
"""
    page("en/offers/cruise.html", "Hotel before or after your cruise in Warnemünde – Hotel am Leuchtturm",
         "Stay before or after your Baltic cruise: Hotel am Leuchtturm is on the beach promenade, and the Warnemünde Cruise Center next to the station is within walking distance.",
         body, active="en/offers/index.html", lang="en", schema=HOTEL_LD_EN)

def vouchers():
    chips = "".join(f'<a class="slot" href="#" data-toast="Im Entwurf: Betrag wählen, online bezahlen, Gutschein sofort als PDF erhalten.">{v} €</a>' for v in (100, 200, 300, 500))
    body = f"""
<div class="wrap crumbs"><a href="index.html">Startseite</a> › Gutscheine</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div>
    <div class="eyebrow">Zum Verschenken</div>
    <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Gutscheine</h1><div class="rule"></div>
    <p class="lead">Verschenken Sie Tage am Meer: Wertgutscheine für Übernachtungen im Hotel am Leuchtturm, Betrag frei wählbar.</p>
    <div class="bookcard" style="position:static;margin-top:24px">
      <h3>Betrag wählen</h3>
      <div class="slots" style="margin-top:12px">{chips}</div>
      <p class="slots-h" style="margin-top:10px">oder Wunschbetrag eingeben</p>
      <ul class="ticks" style="margin-top:14px"><li>Online bezahlen mit Karte oder PayPal <span class="demo">Vorschlag</span></li><li>Gutschein sofort als PDF zum Ausdrucken <span class="demo">Vorschlag</span></li><li>Einlösen per Code direkt in der Online-Buchung <span class="demo">Vorschlag</span></li></ul>
      <a class="btn btn-navy" href="#" data-toast="Im Entwurf endet der Ablauf hier." style="width:100%;margin-top:16px">Gutschein kaufen</a>
    </div>
    <div class="note" data-n="5"><b>Gutscheine, die sich selbst verkaufen:</b> Heute bestellt man über ein Formular mit Rechnungsanschrift und Sicherheitscode und zahlt per Überweisung nach Rechnung – der Gutschein kommt erst nach Zahlungseingang. Mit Online-Zahlung und sofortigem PDF verkauft die Seite auch am 23. Dezember noch, ohne Arbeit an der Rezeption.</div>
  </div>
  <div class="pic2"><img class="tall" src="img/ptdz-5.jpg" alt="Panorama-Terrassen-Doppelzimmer" data-zoom><img src="img/fruehstueck-3.jpg" alt="Frühstück" loading="lazy" data-zoom><img src="img/lobby-2.jpg" alt="Lobby mit Kamin" loading="lazy" data-zoom></div>
</div></section>
"""
    page("gutscheine.html", "Gutscheine – Hotel am Leuchtturm Warnemünde", "Wertgutscheine für Übernachtungen im Hotel am Leuchtturm in Warnemünde – Betrag frei wählbar.", body)

def vouchers_en():
    chips = "".join(f'<a class="slot" href="#" data-toast="In this concept: choose an amount, pay online, receive the voucher instantly as a PDF.">€{v}</a>' for v in (100, 200, 300, 500))
    body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> › Gift vouchers</div>
<section style="padding-top:22px"><div class="wrap split" style="align-items:start">
  <div>
    <div class="eyebrow">A gift of days by the sea</div>
    <h1 class="caps" style="font-size:clamp(32px,4.4vw,52px)">Gift vouchers</h1><div class="rule"></div>
    <p class="lead">Give days by the sea: gift vouchers for stays at Hotel am Leuchtturm, for any amount you choose.</p>
    <div class="bookcard" style="position:static;margin-top:24px">
      <h3>Choose an amount</h3>
      <div class="slots" style="margin-top:12px">{chips}</div>
      <p class="slots-h" style="margin-top:10px">or enter any amount</p>
      <ul class="ticks" style="margin-top:14px"><li>Pay online by card or PayPal <span class="demo">Proposal</span></li><li>Instant PDF voucher to print <span class="demo">Proposal</span></li><li>Redeem with a code in the online booking <span class="demo">Proposal</span></li></ul>
      <a class="btn btn-navy" href="#" data-toast="In this concept the flow ends here." style="width:100%;margin-top:16px">Buy a voucher</a>
    </div>
  </div>
  <div class="pic2"><img class="tall" src="../img/ptdz-5.jpg" alt="Panorama Terrace Double Room" data-zoom><img src="../img/fruehstueck-3.jpg" alt="Breakfast" loading="lazy" data-zoom><img src="../img/lobby-2.jpg" alt="Lobby with fireplace" loading="lazy" data-zoom></div>
</div></section>
"""
    page("en/vouchers.html", "Gift vouchers – Hotel am Leuchtturm, Warnemünde", "Gift vouchers for stays at Hotel am Leuchtturm in Warnemünde – any amount.", body, lang="en")

def build_extra():
    hanse_sail(); hanse_sail_en(); cruise(); cruise_en(); vouchers(); vouchers_en()


if __name__ == "__main__":
    home(); rooms_index(); [room_page(r) for r in ROOMS]; apartments(); offers(); history(); location(); gallery(); booking(); imprint(); tech(); hosting()
    build_en()
    build_extra()
    print("ok")
