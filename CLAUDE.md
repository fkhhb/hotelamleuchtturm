# CLAUDE.md – Hotel am Leuchtturm concept site

Handover for the next session. The human-facing overview is [README.md](./README.md); this file holds what a session needs to carry on without the earlier conversation.

## What this is

A clickable **concept** for a new website for Hotel am Leuchtturm, Warnemünde (Rostock) – *not* Lübeck, an early mix-up. Built by Fritz Bremer (mndst.co, Berlin, info@mndst.co) to pitch the hotel on more direct bookings, better booking UX (every step has its own URL) and visibility in Google and AI assistants.

- Live: https://hotelamleuchtturm.mndst.co (Vercel project `mndstprojects/hotelamleuchtturm`, CNAME at GoDaddy → `cname.vercel-dns.com`)
- Real hotel site: https://www.hotel-am-leuchtturm.de/DE/home.html · booking engine DIRS21: `https://reservation.one.dirs21.de/hotel-am-leuchtturmde?range=YYYY-MM-DD,YYYY-MM-DD&sets=[{"occupancy":{"adultCount":2,"children":[]}}]&culture=de-DE&show_results=true`
- Hotel: R. Kossow & Levermann Hotelbetriebs GmbH, managing directors Friedemann Kunz and Fredrich Kunz, info@hotel-am-leuchtturm.de, 0381 54370, Am Leuchtturm 16, 18119 Rostock-Warnemünde

## Workflow (agreed with the user)

- **Push straight to `main`** – the user asked for that; every push deploys on Vercel. No PRs for this repo.
- After a push, confirm the change is actually live (`curl` the page and grep for the new text); deploys take ~10–60 s.
- **Never hand-edit generated HTML.** Edit `quelle/build_site.py` (pages, German first, English after `# Englische Version`), then `python3 quelle/build_site.py`. `assets/site.css` and `assets/site.js` are edited directly.
- Test before every push:
  ```bash
  python3 -m http.server 8772
  ```
  ```bash
  node quelle/tests/test_site.js
  ```
  Expect `BAD: []` and `ERRORS: none` (38 pages, 44 links as of 31 Oct 2026). Playwright is preinstalled in cloud sessions.
- Gotcha: don't put `pkill -f "http.server 8772"` in the same shell command as other steps – the pattern matches that shell's own command line and kills it (exit 144). Run it on its own.
- Keep the site **noindex** (`robots.txt`, `X-Robots-Tag` in `vercel.json`, meta robots) so demo prices never reach Google or AI answers about the real hotel. `quelle/`, `README.md` and this file are excluded from deploys via `.vercelignore`.

## Content rules

- Only real data from the hotel's site, or values clearly labelled Demo/Vorschlag. Don't invent reviews, prices or facts. Present opinions as proposals.
- Yellow numbered notes (`<div class="note" data-n="…">`) explain each recommendation to the hotel. They stay German on English pages too.
- Real: rooms, sizes, floors, beds, 2026 season prices, extra bed 75 €, 14-day cancellation (apartments four weeks), payment EC/cash/bank transfer, check-in 15:00 / out 11:00, parking Tiefgarage Kurhaus 14 €/24 h, minimum stays (low-season weekend 2, mid 4, high 6, Easter/Ascension/Whitsun/New Year's Eve 5), winter package from 105 €, review score 91 % from 1,563 reviews (hotel's own Customer Alliance widget, Oct 2026), Hanse Sail 2027 = 5–8 Aug (city event calendar).
- Demo: availability (`freeNight`/`nextFree` in site.js), breakfast 20 € (only published figure, from the outdated English price list), Kurtaxe 3 €, saver rate −10 %, late check-out, Sekt, voucher online purchase.

## Decisions already made (don't re-litigate)

- Header photo: aerial from the lighthouse (`img/hero-promenade.jpg`, user's photo IMG_3058) full width, headline in a navy band below. Headline **„Direkt am Strand“** / "Right by the beach"; the lighthouse is named in the line below.
- Dune video band (AI-animated from a hotel photo, labelled as such) sits after the room cards.
- Fonts: Marcellus (headings), Source Sans 3 (text and numbers – the old number font looked italic).
- No "copy share link" box – the URL itself carries the booking state.
- Hotel branding kept: navy `#00284b`, sea `#376f8d`, aqua `#a6d9e2`, their logo.

## Findings (checked 30 Oct 2026)

The full list is the **Prüfbericht** on `/vorschlag/#pruefbericht`, generated from `PRUEF` in `quelle/build_site.py` – update it there. Headlines:
- DIRS21 ≠ website: other room names (no „Komfort-Doppelzimmer“), lower off-season prices, minimum stays not enforced, Panorama-Terrassen-Doppelzimmer never offered in 8 tested ranges.
- English site outdated (2023/24 prices, four-week cancellation, claims public parking at the hotel).
- German site: Einzelzimmer "Queensize 100 cm" for 1–2 adults, max 2 adults vs. extra bed, 2023 apartment prices, 1850 vs. 1851, typos.
- Cookies: booking works after declining, but DIRS21 shows a second cookie banner. (An earlier claim that declining blocks booking was wrong by the afternoon of 30 Oct and was corrected everywhere.)
- Server: PHP 5.4/5.6, OpenSSL 1.0.2 (no security updates). Site was down for hours on 30 Oct (HTTP 500), back since.

Re-check against the live site with:
```bash
node quelle/tests/dirs21_check.js 2026-11-17:2026-11-19 2027-07-12:2027-07-18
```
```bash
node quelle/tests/live_booking_check.js
```

## Emails (Gmail drafts in info@mndst.co – not sent by Claude)

- `r-8827152305921281286` – formal, to info@hotel-am-leuchtturm.de, „Sehr geehrte Herren Kunz“, subject „Wie besprochen: Vorschlag für Ihre neue Website …“. PHP outage note at the bottom. Open wording question: the outage is described as caused by PHP – likely, not proven.
- `r8840212369577244993` – casual „du“ version for a friend who works at the hotel; recipient and `[Name]` still empty.

## Open items

- Impressum: street and postcode still `[Straße und Hausnummer]` / `[PLZ]` in `imprint()`.
- Photo rights for the header photo and the dune-video source photo.
- Real review quotes once the hotel agrees which ones may be used.
- Questions for the hotel: is the Panorama-Terrassen-DZ bookable online? Single-night exception for cruise guests? Single-room bed width?
- The user wants improvements to keep coming: good next candidates are the apartments booking flow, a voucher checkout mock, and an English Prüfbericht.
