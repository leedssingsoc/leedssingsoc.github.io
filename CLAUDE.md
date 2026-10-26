# Leeds Singaporean Society website — notes for Claude

Live site: https://leedssingsoc.github.io/ (repo `leedssingsoc/leedssingsoc.github.io`, moved from waveriderjc-max/leeds-singsoc-site on 26 Oct 2026; GitHub Pages, branch `main`, root).
Preview copy: https://claude.ai/artifact/TYZwBmyD5YBBXcyMdyZzgR (keep in sync when practical).

**Always make Jarryl's requested changes live (his rule, 26 Oct 2026):** after testing, push to `main` so the
public site updates; don't leave them only on a side branch.

Everything is in `index.html`; images, videos and logos sit next to it.

## Adding an event
- Easiest: add an object to the JSON in `<script type="application/json" id="extra-events">`
  (fields: title, date YYYY-MM-DD, time, venue, price, desc, link, linkLabel, poster). The page
  sorts it into "Coming up" by date, adds a countdown and moves it to "Already happened" afterwards.
- Or hand-write a `<article class="card feature" data-until="YYYY-MM-DD">` card (soonest first) plus a
  hidden `<div class="row" data-after="YYYY-MM-DD" hidden>` row for the past list, like the existing ones.
- Save posters as JPG (max ~900px wide) next to index.html.

## House style
- Colours come from the logo: teal ink #0E2A2F, Singapore red #D9343E. Keep it human, not "AI-looking".
- Sponsor cards: logo tile, name, "Type · Street", deal in red, conditions in one standard set of words
  (Cash only · Up to 4 people · Student ID needed · Mon–Thu · Until Mon YYYY), then "Directions →".
- Plain, friendly wording. Don't invent numbers, prices or names.
- Don't publish the Maki & Ramen members' e-voucher image (members only).
