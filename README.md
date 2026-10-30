# Hotel am Leuchtturm – concept website

A clickable concept for a new website for [Hotel am Leuchtturm](https://www.hotel-am-leuchtturm.de/DE/home.html), Warnemünde. It shows how the site could look and how booking could work: every step has its own URL, room pages show the next free dates, and AI assistants and search engines can read the facts.

**Live:** https://hotelamleuchtturm.mndst.co (blocked for search engines and AI crawlers, see below)

> **Concept, not the hotel's official website.** Texts, room data, 2026 prices and photos come from the hotel's current website. Free dates, breakfast price, Kurtaxe and anything labelled „Vorschlag" or „Demo" are examples. No bookings are taken and no personal data is collected.

## What's in it

| Page | File | What it shows |
| --- | --- | --- |
| Homepage | `index.html` | Header photo from the lighthouse (hotel, promenade, beach) with the headline in a navy band below it, search box → booking with dates in the URL, room cards with next free dates, dune video band (5 s, AI-animated from a photo of the hotel, labelled as such), breakfast lounge, lobby, offers, reviews (placeholders for real quotes), FAQ |
| Rooms & prices | `zimmer/index.html` | All six categories, the real 2026 price table, conditions, minimum stays |
| Room pages | `zimmer/*.html` | Gallery, facts as text (size, floor, view, bed), sticky booking box with total price and next free dates |
| Booking | `buchen.html` | 4 steps (room → rate → extras → summary). Every step is in the URL and survives reload/sharing. Step 4 links to the hotel's real DIRS21 booking with the same dates |
| Apartments | `apartments.html` | Apartment house incl. the (outdated) 2023 prices, flagged |
| Offers | `angebote/` | Real winter package; Hanse Sail 2027 (5–8 Aug, per the city event calendar) with rooms facing the harbour entrance; before/after your cruise. Each button opens the booking pre-filled |
| Gift vouchers | `gutscheine.html` | Amount chips and the proposed online purchase (pay online, instant PDF, redeem by code) |
| History, location, gallery | `geschichte.html`, `lage-anfahrt.html`, `galerie.html` | Timeline since 1850, directions and parking, photo gallery with lightbox |
| English version | `en/` | All guest-facing pages in English with English URLs (e.g. `/en/rooms/panorama-terrace-double-room`), hreflang-linked to the German pages. The DE / EN switch jumps to the matching page and keeps the booking selection. DIRS21 hand-off opens in English |
| Tech package | `vorschlag/` | For the hotel's web agency: `sitemap.xml`, `robots.txt`, `llms.txt`, `schema-hotel.json`, 301 redirects (`.htaccess` + CSV), list of issues found |

Yellow numbered notes explain which recommendation each element demonstrates. They are addressed to the hotel and stay German, also on the English pages. Visitors can hide them with the button in the top banner.

## Key findings from the live site (30 Oct 2026)

- **Guests who decline cookies cannot book.** The DIRS21 script only loads after consent; without it the booking button does nothing (`d21_api is not defined`).
- **Booking has no URL.** DIRS21 opens as an overlay. A direct link already works and should be used instead:
  `https://reservation.one.dirs21.de/hotel-am-leuchtturmde?range=2027-05-14,2027-05-17&culture=de-DE&show_results=true`
- **Server runs end-of-life PHP 5.x / OpenSSL 1.0.2.** The site was down for several hours on 30 Oct 2026 (HTTP 500 on every page).
- No `robots.txt`, `sitemap.xml` or `llms.txt`. Unknown pages redirect to the homepage instead of returning 404.
- Contradictions: 2023 apartment prices, cleaning every 3 vs. 4 days, "max. 2 adults" vs. "extra bed for 3rd person", founded 1850 vs. 1851, page title typo „Preie & Konditionen".

## Real data vs. demo

| Real (from hotel-am-leuchtturm.de) | Demo / proposal |
| --- | --- |
| Room facts, floors, sizes, beds, equipment | Availability and "next free dates" (simulated) |
| 2026 seasonal prices, extra bed 75 € | Breakfast price (22 € p.p./night) |
| 14-day free cancellation, payment methods, check-in/out | Kurtaxe (3 € p.p./night) |
| Parking at Kurhaus garage, 14 € / 24 h | Non-refundable saver rate −10 %, late check-out, Sekt |
| History, directions, winter offer (ab 105 €), Hanse Sail 2027 dates (city event calendar) | Hanse Sail and cruise package contents and prices, voucher online purchase |
| Kayak score 8.9 from 881 reviews (Oct 2026) | Review quotes (empty placeholders) |

Demo values live at the top of `assets/site.js` (`BREAKFAST`, `KURTAXE`, `SAVER`, `EXTRAS`) and in the availability functions `freeNight` / `nextFree`.

## Structure

```
index.html, buchen.html, …   generated pages (do not edit by hand)
zimmer/, angebote/, vorschlag/
assets/site.css               styles (hotel colours: navy #00284b, sea #376f8d, aqua #a6d9e2)
assets/site.js                room data, prices, booking logic, URL state, DE/EN texts
img/                          photos © Hotel am Leuchtturm, logo, favicon
quelle/build_site.py          page generator (not deployed)
vercel.json                   clean URLs + X-Robots-Tag: noindex
robots.txt                    Disallow: / (concept must not be indexed)
```

## Editing

Pages are generated, German and English. Change texts, rooms or the tech package in `quelle/build_site.py` (English pages: the section after `# Englische Version`), then rebuild:

```bash
python3 quelle/build_site.py
```

Styles and behaviour are edited directly in `assets/site.css` and `assets/site.js`. To swap a photo, replace the file in `img/` with the same name.

Preview locally:

```bash
python3 -m http.server 8000
```

## Deployment

Vercel project in the mndst team, connected to this repo. Every push to `main` deploys. Domain `hotelamleuchtturm.mndst.co` (CNAME to `cname.vercel-dns.com` at GoDaddy). No build step: static files from the repo root; `quelle/` and this README are excluded via `.vercelignore`.

**Indexing is deliberately blocked** (`robots.txt`, `X-Robots-Tag`, `<meta name="robots">`), so demo prices never show up in Google or AI answers about the real hotel. The `robots.txt`, `sitemap.xml` and `llms.txt` meant for the hotel's own domain live in `vorschlag/`.

## Before sharing publicly

- [x] Publisher name, company and email in `impressum.html` (Fritz Bremer · mndst.co, Berlin, info@mndst.co)
- [ ] Add the street address and postcode in `imprint()` in `quelle/build_site.py` – placeholders `[Straße und Hausnummer]` and `[PLZ]` are still on the page
- [ ] Confirm usage rights for the header photo (`img/hero-promenade.jpg`, aerial from the lighthouse) and the dune video source photo
- [ ] Replace the review placeholders with real quotes (name, source, date) once the hotel agrees which ones may be used
