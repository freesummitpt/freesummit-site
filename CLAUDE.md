# Free Summit website — project notes for Claude

Free Summit is Lourenço's guided outdoor activities business near Lisbon (rock climbing, via ferrata, hiking).
Slogan: **go beyond.** Instagram: @freesummitpt. Contact email: admin@freesummitpt.com.
This repo IS the website. It is plain static HTML/CSS/JS hosted on **GitHub Pages** at **freesummitpt.com**
(domain at Squarespace Domains, email on Google Workspace). No framework, no build step for the site itself.

## Structure
```
index.html                 Homepage: activities grouped by type, "from €xx" per location, booking form
guia/                      Activity page: rock climbing at Guia, Cascais          (generated)
via-ferrata/               Activity page: Via Ferrata dos Pinheirinhos, Sesimbra   (generated)
caminhada-arrabida/        Activity page: hiking in Serra da Arrábida              (generated)
assets/site.css            ONE stylesheet for every page (design tokens at the top)
assets/main.js             Shared JS: PT/EN toggle, contour hero, booking form
assets/config.js           Site settings (form endpoint, contact email). Only file edited by hand.
assets/*.png               Logo (olive / cream), favicon, apple-touch-icon, og-image (share image)
tools/build_pages.py       Generates the activity pages from data. Run: python3 tools/build_pages.py
tools/booking-form-apps-script.gs   Google Apps Script that receives the form (copy, not deployed from here)
CNAME                      freesummitpt.com — do not delete
```
Activity pages are generated: edit `tools/build_pages.py` (PAGES data + template), re-run it, never hand-edit `guia/index.html` etc.
The homepage `index.html` is hand-written.

## Design system (approved by Lourenço — keep it)
- **Two colours only:** cream `#ECEEBF` (background) and dark olive `#31351A` (text, rules, solid blocks). No blue, no third colour.
  The earlier cobalt blue `#0022CC` was tried and rejected.
- **Font:** Archivo (Google Fonts, variable `wdth,wght@100..125,400..900`). Headings: width 125%, weight 900, UPPERCASE (`.xb`), matching the logo wordmark.
  Slogan "go beyond." is lowercase, width 112%, weight 700. Body: Archivo normal width.
- Hero has generated topographic contour lines (`<svg id="topo">`, drawn by main.js) echoing the logo.
- Booking section: olive background, cream text, cream fields. Footer: cream logo on an olive square (`.badge`).
- Bilingual: English in the markup, Portuguese in `data-pt="..."` attributes (also `data-pt-placeholder`, `data-label-pt`).
  Every new visible text needs a `data-pt`. The slogan "go beyond." is NOT translated (it is part of the logo).

## Booking form → Google Sheet
- Form posts (no-cors) to the Apps Script web app URL in `assets/config.js` (`window.FS_CONFIG.formEndpoint`).
  If empty, the form falls back to opening an email draft.
- The script appends a row to the "Pedidos" table in the Google Sheet **Booking Requests** (owner admin@freesummitpt.com)
  and emails admin@freesummitpt.com. Columns: Received, Name, Email, Phone, Activity, Date, People, Type, Transfer,
  Message, Language, Page, Status (dropdown: New/Replied/Booked/Done/Cancelled).
- `Page` = `<body data-page="...">` of the page that sent it (home, guia, via-ferrata, caminhada-arrabida). Keep this for ad tracking.
- Activity pages pre-select their activity via `<form data-activity="...">`. Links with `data-select="<activity>"` pre-select too.
- Activity `<option value>`s are what land in the sheet — keep them stable.
- To update the script: Apps Script → Deploy → Manage deployments → Edit → New version (keeps the same /exec URL).

## Source content
Activity details and prices come from Lourenço's Google Drive: folder **Actividades** (one subfolder per location, one Google Doc per activity)
and the sheet **Free Summit – Activity Pricing**. Brand guide in Drive folder **Branding** (note: its colours are the OLD forest-green palette; the site now uses cream + olive).
The Arrábida hiking page content (route ~8 km, €35 / €20 children / €70 solo, age 8+) was drafted by Claude without a source doc — needs Lourenço's confirmation.

## Next planned work
1. Lourenço is finalising which activities he will advertise.
2. **"Know more" pages** — one per activity/location, each with a **space for a photograph of the place** (Lourenço will supply photos).
   They carry the pricing details that were removed from the homepage. Fenda da Arrábida and Forte do Cavalo have Drive docs but no pages yet
   (their homepage buttons currently jump to the form). The Sesimbra full-day combo (€110) has no page either.
3. **Final version of the homepage** once the activity list is settled.
Photos: store under `assets/photos/`, compress to ~1600 px wide JPG/WebP (< 300 KB), always with descriptive `alt` text.

## Open items
- RNAAT registration number is blank in every footer (`<span id="rnaat">`) — required before advertising.
- Group sizes and cancellation policy are still "to confirm" in the Drive docs.
- Logo source is only 584 px; ask for an SVG or larger PNG for big uses.

## Publishing
Commit and push to the `main` branch; GitHub Pages publishes in about a minute. Hard refresh to see changes.
DNS (Squarespace): 4 A records for @ → 185.199.108.153 / .109.153 / .110.153 / .111.153, CNAME www → <github user>.github.io, MX records for Google Workspace untouched.

## Working with Lourenço
He is not a developer: explain steps plainly, say clearly when a change touches `assets/main.js` or `assets/config.js`,
and never overwrite `assets/config.js` values he has filled in.
