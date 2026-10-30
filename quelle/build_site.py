#!/usr/bin/env python3
"""Baut den Konzeptentwurf Hotel am Leuchtturm (statische Seiten) in die Repo-Wurzel.

Aufruf: python3 quelle/build_site.py
assets/site.css, assets/site.js und img/ werden nicht erzeugt, sondern direkt bearbeitet."""
import json, os, html
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Repo-Wurzel = Website
REAL = "https://www.hotel-am-leuchtturm.de"
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
      special="Ideal für Alleinreisende: individuell geschnitten mit leichter Dachschräge und Queensize-Bett.", banner=None),
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

def page(path, title, desc, body, active="", schema=None, mbar=True):
    depth = path.count("/")
    R = "../" * depth
    nav = "".join(f'<li><a href="{R}{h}"{" aria-current=page" if h==active else ""}>{t}</a></li>' for h,t in MENU)
    sch = ld(schema) if schema else ""
    mb = f'<div class="mbar"><span id="mbar-txt"><b>Ab 139 € pro Nacht</b>Bestpreis bei Direktbuchung</span><a class="btn btn-navy" href="{R}buchen.html">Buchen</a></div>' if mbar else ""
    doc = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="{R}img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/site.css">
{sch}
</head>
<body class="notes" data-root="{R}">
<div class="concept" role="note"><span><b>Konzeptentwurf</b> für eine neue Website des Hotel am Leuchtturm – keine offizielle Seite. Verfügbarkeiten und markierte Werte sind Demo. Echte Buchung: <a href="{REAL}/DE/home.html">hotel-am-leuchtturm.de</a></span><button type="button" id="toggleNotes">Hinweise ausblenden</button></div>
<header class="top"><div class="wrap bar">
  <a class="brand" href="{R}index.html" aria-label="Hotel am Leuchtturm – Startseite"><img src="{R}img/logo-header.jpg" alt="Hotel am Leuchtturm – seit 1850 in Warnemünde" width="248" height="100"></a>
  <ul class="menu" id="menu">{nav}</ul>
  <a class="lang" href="#" data-toast="Die englische Version folgt demselben Aufbau unter /en/ – inklusive englischer Buchungsstrecke."><b>DE</b> | EN</a>
  <a class="btn btn-navy" href="{R}buchen.html">Jetzt buchen</a>
  <button class="burger" type="button" aria-label="Menü" aria-controls="menu" aria-expanded="false"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
  <div class="fcols">
    <div><div class="fbrand">Hotel am Leuchtturm<small>Seit 1850 in Warnemünde</small></div>
      <p style="margin-top:18px">Am Leuchtturm 16<br>18119 Rostock-Warnemünde<br>Tel. <a href="tel:{TEL_HREF}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div><h4>Hotel</h4><p><a href="{R}zimmer/index.html">Zimmer &amp; Preise</a><br><a href="{R}apartments.html">Apartmenthaus</a><br><a href="{R}angebote/index.html">Angebote</a><br><a href="{R}galerie.html">Galerie</a><br><a href="#" data-toast="Gutscheine: online kaufen, als PDF erhalten und per Code in der Buchung einlösen.">Gutscheine</a></p></div>
    <div><h4>Service</h4><p><a href="{R}lage-anfahrt.html">Lage &amp; Anfahrt</a><br><a href="{R}index.html#fragen">Häufige Fragen</a><br><a href="{R}geschichte.html">Geschichte</a><br><a href="{R}buchen.html">Online buchen</a></p></div>
    <div><h4>Rechtliches</h4><p><a href="{REAL}/DE/ueber-uns/impressum1.html">Impressum des Hotels</a><br><a href="{REAL}/DE/ueber-uns/datenschutz.html">Datenschutz</a><br><a href="{REAL}/DE/ueber-uns/agbs.html">AGB</a></p></div>
  </div>
  <div class="fnote">Konzeptentwurf zur Neugestaltung von hotel-am-leuchtturm.de · Inhalte, Zimmerdaten und Preise 2026 von der aktuellen Website des Hotels; Verfügbarkeiten, Frühstückspreis, Kurtaxe und als „Vorschlag“ markierte Leistungen sind Beispiele. Fotos © Hotel am Leuchtturm. · <a href="{R}vorschlag/index.html">Technik-Paket (Sitemap, robots.txt, llms.txt, Weiterleitungen)</a> · <a href="{R}impressum.html">Impressum dieses Entwurfs</a></div>
</div></footer>
{mb}
<div class="lightbox" id="lightbox" role="dialog" aria-label="Foto"><img alt=""></div>
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
  <picture><source media="(max-width:640px)" srcset="img/aussen-37.jpg"><img class="hero-img" src="img/stage-6.jpg" alt="Das Hotel am Leuchtturm an der Strandpromenade von Warnemünde mit Blick auf die Ostsee"></picture>
  <div class="hero-copy"><div class="wrap">
    <div class="eyebrow">Seit 1850 an der Promenade von Warnemünde</div>
    <h1 class="caps">Direkt am Leuchtturm</h1>
    <p>Inhabergeführtes Boutique-Hotel mit 30 Zimmern, Frühstückslounge mit Blick auf die Promenade und Lobby mit Kamin – nur wenige Schritte vom feinen weißen Sand der Ostsee.</p>
  </div></div>
</section>
<div class="search"><div class="wrap">
  {searchbox(R)}
  <div class="perkline"><span>Bestpreis direkt beim Hotel</span><span>Kostenfrei stornierbar bis 14 Tage vor Anreise</span><span>Parkticket direkt mitbuchen</span></div>
  <div class="note" data-n="1" style="margin-left:auto;margin-right:auto"><b>Maßnahme 1 – teilbare Buchungs-URL:</b> Heute öffnet die Buchung als Fenster über der Seite, die Adresse ändert sich nie. Hier führt jede Suche auf eine eigene Adresse mit Daten, Gästen und Zimmer – teilbar per Link, lesbar für KI-Assistenten.</div>
</div></div>

<section style="padding-top:64px"><div class="wrap">
  <div class="facts4">
    <div><b>8,9 / 10</b><span>aus 881 verifizierten Bewertungen (Kayak, Okt. 2026)</span></div>
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
    <article class="tile"><img src="img/stage-6.jpg" alt="Strand und Leuchtturm" loading="lazy" style="object-position:85% 50%"><div class="bd"><div class="when">August <span class="demo">Vorschlag</span></div><h3>Hanse Sail</h3><p>Großsegler laufen direkt vor dem Hotel in den Hafen ein – ein Zimmer mit Blick auf die Hafeneinfahrt ist der beste Platz.</p><a class="btn btn-line" href="#" data-toast="Vorschlag: eigene Seite zur Hanse Sail mit den offiziellen Terminen und vorausgefüllter Buchung.">Seite folgt</a></div></article>
    <article class="tile"><img src="img/aussen-39.jpg" alt="Hotel am Leuchtturm von außen" loading="lazy"><div class="bd"><div class="when">Ganzjährig <span class="demo">Vorschlag</span></div><h3>Vor oder nach der Kreuzfahrt</h3><p>Eine Nacht am Meer vor dem Ablegen in Warnemünde – mit Gepäckaufbewahrung und spätem Check-out, auf Deutsch und Englisch.</p><a class="btn btn-line" href="#" data-toast="Vorschlag: eigene (auch englische) Seite für Kreuzfahrtgäste mit Ein-Klick-Buchung.">Seite folgt</a></div></article>
  </div>
</div></section>

<section class="reviews"><div class="wrap">
  <div class="score"><div class="big">8,9</div><div><h2 class="caps" style="font-size:34px">„Sehr gut“</h2><div style="opacity:.8">aus 881 verifizierten Bewertungen auf Kayak · Stand Oktober 2026</div></div></div>
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
  <p>1850 eröffnete H. F. Ohlerich hier das „Hotel Pavillon“ – als Warnemünde gerade zum Badeort wurde. 1897 entstand direkt davor der Leuchtturm. Heute führt ein inhabergeführtes Haus die Geschichte fort.</p>
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
      <div class="table-wrap"><table style="min-width:520px">
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
    <p style="margin-top:22px;font-size:18px">Preis pro Person und Nacht im Doppelzimmer <b style="font-family:var(--serif);font-size:34px;color:var(--navy)">ab 105 €</b></p>
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
    <article class="tile"><img src="../img/stage-4.jpg" alt="Dachterrasse" loading="lazy"><div class="bd"><div class="when">August <span class="demo">Vorschlag</span></div><h3>Hanse Sail vom Zimmer aus</h3><p>Eigene Seite mit den offiziellen Terminen und Zimmern mit Blick auf die Hafeneinfahrt.</p><a class="btn btn-line" href="#" data-toast="Vorschlag für eine neue Angebotsseite.">Seite folgt</a></div></article>
    <article class="tile"><img src="../img/aussen-37.jpg" alt="Hotel am Leuchtturm" loading="lazy"><div class="bd"><div class="when">Ganzjährig <span class="demo">Vorschlag</span></div><h3>Vor oder nach der Kreuzfahrt</h3><p>Englischsprachige Seite für Kreuzfahrtgäste mit Gepäckaufbewahrung und spätem Check-out.</p><a class="btn btn-line" href="#" data-toast="Vorschlag für eine neue Angebotsseite.">Seite folgt</a></div></article>
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
  <div class="share"><span>Teilbarer Link zu genau diesem Stand:</span><code class="js-url"></code><button type="button" data-copy>Link kopieren</button></div>
</div></section>
"""
    page("buchen.html", "Online buchen – Hotel am Leuchtturm Warnemünde", "Zimmer im Hotel am Leuchtturm direkt beim Hotel buchen – mit Gesamtpreis, Extras und teilbarem Buchungslink.", body, mbar=True)

# ---------------- Impressum des Entwurfs ----------------
def imprint():
    body = """
<section><div class="wrap narrow"><div class="eyebrow">Konzeptentwurf</div><h1 class="caps" style="font-size:40px">Impressum dieses Entwurfs</h1><div class="rule"></div>
<p>Diese Seiten sind ein unverbindlicher <b>Konzeptentwurf</b> für eine mögliche Neugestaltung der Website des Hotel am Leuchtturm. Sie sind keine offizielle Website des Hotels; es werden keine Buchungen angenommen und keine personenbezogenen Daten erhoben.</p>
<p><b>Verantwortlich für diesen Entwurf:</b><br>[Name / Firma]<br>[Anschrift]<br>[E-Mail]</p>
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

def tech():
    V = os.path.join(OUT, "vorschlag"); os.makedirs(V, exist_ok=True)
    # sitemap.xml
    urls = []
    for new, _, prio, freq in NEW:
        if new == "/buchen/": continue
        en = "/en" + new
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

## Weitere Seiten

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
    <article class="tile"><div class="bd"><div class="when">Buchungssystem</div><h3>DIRS21 als Link statt Fenster</h3><p>Heute öffnet <code>d21_api.ibe.open()</code> die Buchung als Overlay – die Adresse ändert sich nie. Dabei funktioniert ein direkter Link bereits (getestet 30.10.2026):</p><p><code style="font-size:12.5px;overflow-wrap:anywhere">reservation.one.dirs21.de/hotel-am-leuchtturmde?range=2027-05-14,2027-05-17&amp;culture=de-DE&amp;show_results=true</code></p><p>Die Buchungs-Buttons sollten auf diesen Link führen (neues Fenster oder eigene Seite /buchen/) – dann funktioniert die Buchung auch ohne Cookie-Zustimmung.</p><a class="btn btn-line" href="https://reservation.one.dirs21.de/hotel-am-leuchtturmde?range=2027-05-14,2027-05-17&amp;culture=de-DE&amp;show_results=true" target="_blank" rel="noopener">Link testen ↗</a></div></article>
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
    <li><b>Wer Cookies ablehnt, kann nicht buchen:</b> Das DIRS21-Skript lädt erst nach Zustimmung; ohne Zustimmung passiert beim Klick auf „Buchen“ nichts (Fehler <code>d21_api is not defined</code>). Getestet am 30.10.2026.</li>
    <li>Server meldet PHP 5.6.40 / 5.4.45 und OpenSSL 1.0.2 – alles ohne Sicherheitsupdates (5.6.40 ist die letzte PHP-5-Version, 2019). Die Seite war am 30.10.2026 mehrere Stunden komplett ausgefallen (Fehler 500); danach waren die PHP-Versionen andere als vorher.</li>
    <li>Nicht vorhandene Seiten leiten per 302 auf die Startseite um statt „404 nicht gefunden“ zu melden – Suchmaschinen und KI-Agenten sehen tote Links als gültig.</li>
    <li>Keine robots.txt, keine sitemap.xml, keine llms.txt.</li>
    <li>Buchung als Overlay (DIRS21) ohne eigene Adresse – nicht teilbar, nicht verlinkbar.</li>
    <li>Apartment-Seite zeigt Preise von 2023; Reinigung einmal „4-Tages-“, einmal „3-Tages-Rhythmus“.</li>
    <li>Zimmerseiten: „max. 2 Erwachsene“ – Preisliste: „Aufbettung 3. Person“.</li>
    <li>Geschichte: „1850“ – Anfahrt: „1851 errichtet“.</li>
    <li>Seitentitel „Preie &amp; Konditionen“ (Tippfehler) erscheint so in Google.</li>
    <li>Bewertungen nur als Grafik-Link, Fotos ohne Beschreibung und mit technischen Dateinamen.</li>
  </ul>
</div></section>
"""
    page("vorschlag/index.html", "Technik-Paket – Konzeptentwurf Hotel am Leuchtturm", "Sitemap, robots.txt, llms.txt, strukturierte Daten und 301-Weiterleitungen für hotel-am-leuchtturm.de.", body, mbar=False)

# ---------------- Hosting-Dateien für den Entwurf ----------------
def hosting():
    open(os.path.join(OUT,"robots.txt"),"w").write("# Konzeptentwurf – bitte nicht indexieren.\nUser-agent: *\nDisallow: /\n")
    open(os.path.join(OUT,"vercel.json"),"w").write(json.dumps({
        "cleanUrls": True,
        "headers": [{"source":"/(.*)","headers":[{"key":"X-Robots-Tag","value":"noindex, nofollow, noarchive"}]}]
    }, indent=2))

if __name__ == "__main__":
    home(); rooms_index(); [room_page(r) for r in ROOMS]; apartments(); offers(); history(); location(); gallery(); booking(); imprint(); tech(); hosting()
    print("ok")
