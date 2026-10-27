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

## Daily site check (since 26 Oct 2026)
A claude.ai scheduled task, `leedssingsoc-site-check`, runs every day at 08:36 UK time. It checks the live site
(new commits, broken images/links, page errors on desktop and phone, out-of-date events or sponsor deals) and
sends Jarryl ONE Telegram message a day, even when all is fine, from the website bot "SingSoc Website Check"
(@LeedsSingSocSiteBot, env var SITE_BOT_TOKEN; chat id from SITE_CHAT_ID or TELEGRAM_CHAT_ID). The day's message
is pinned; a re-run the same day edits it instead of sending another. It never uses TELEGRAM_BOT_TOKEN (the
job-search bot). It is REPORT-ONLY: Jarryl is the only one who changes the website, so the check never edits,
commits or pushes. It just tells him what to fix.
If a run crashes, the check retries failed steps and still sends the message (marking "❓ couldn't check").
A watchdog task, `leedssingsoc-site-watchdog` (09:21 daily), checks today's pinned message exists; if not, it
posts a ⏳ placeholder and re-runs the check, and recreates the task if it was deleted. Backup of the prompt:
`routines/site-check-cloud.md` in the private repo waveriderjc-max/jobsearch.
