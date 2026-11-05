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
- Ticket links close by themselves (Jarryl, 26 Oct 2026): each card's ticket/sign-up buttons
  (`.ctas-left`) become "Ticket sales have closed." when the event starts. When Jarryl says sales
  closed early, add `data-closed` to that card (or `"closed": true` in the JSON event).
- Event card layout (Jarryl, 5 Nov 2026), modelled on the Paintball card so it never feels overwhelming:
  chips (date + countdown), title, ONE or two short sentences, then just three facts: When, Where, Price.
  Everything else (programme/timings, line-up, ticket tiers, dress code, meeting point, what's included)
  goes in a collapsed `<details class="more">` with a short summary like "Plan for the day", using
  `<ul|ol class="prog">` rows of `<li><b>label</b> text</li>`. Then the button with one short tiny line.
  JSON events: `"details": [["14:00", "Meet at ..."], ...]` and optional `"detailsTitle"`.
- "Where" is always `<dd class="venue"><b>Venue name</b><span class="addr">street, postcode</span><a class="dir" ...>Directions →</a></dd>`
  (Google Maps search link). JSON events: `"venue"` plus optional `"address"`; the directions link is added automatically.
- Every future event gets a live countdown (Jarryl, 5 Nov 2026): a chip with `data-cd="YYYY-MM-DD"` (and
  `data-time` if known). JSON events get one automatically.
- For things that OPEN on a date (applications, sign-ups) rather than happen on it, add `data-keep-open` to the
  card and `data-done="Applications open"` to the chip (JSON: `"keepOpen": true, "liveText": "..."`): it counts
  down ("Opens in …"), then shows the done text, and the buttons stay usable until `data-until`.
- NTU Management Associate Programme card (`#ntu-map`): counts down to 1 Jan 2027 (NTU said only "January 2027";
  move `data-cd` if they give an exact date), stays up until 28 Feb 2027 (Jarryl, unless NTU states a closing date). When NTU publishes the application link,
  add an "Apply now" button, keeping the interest form and programme website buttons.

## Ticket forms and prices (Jarryl, 27 Oct 2026)
Ticket forms (e.g. Monsta nights) are Google Forms made and managed by the treasurer (Yadira), not Jarryl.
The website only links to the form's share link (`forms.gle/...` or `.../viewform`, never `/edit`) and shows
the prices. Bank details, sort codes, account numbers and phone numbers stay in the form, never on the site.
- When Jarryl says "update the prices" (or sends a new form): run `python tools/read_form.py <share link>`
  (set `SSL_CERT_FILE=/root/.ccr/ca-bundle.crt` in the cloud). It prints every section and question of ANY
  form layout, then each line with a £ price or "sold out" and which section it sits in. It hides bank and
  phone details. Don't assume the old Halloween template: forms change.
- Put the prices on the event as `"tiers"`: `[{"name": "Early bird", "soldOut": true},
  {"name": "Second advance", "price": "£18 members · £20 non-members"}, ...]`, in the form's own stage names
  and order, plus `"priceNote": "Prices go up nearer the event. The ticket form always has the latest price."`
  (Hand-written cards: same idea in their Price/Tickets row.)
- If the form is unclear (a price with no stage name, members/non-members not marked, prices only in an image,
  two prices that disagree, or a branch you can't tell apart), DON'T guess: show Jarryl the lines the reader
  printed and ask. Use only prices the form states; never work them out or invent a stage.
- If the reader says the form is closed, add `"closed": true` (or `data-closed`) so the button shows
  "Ticket sales have closed."
- After updating, tell Jarryl in one line what changed (old → new) so he can check it against the form.

## Homepage photos
- The taped photos at the top change every day (UK date). They're picked from the `WIDE`
  (landscape, big print, plus a third print `#print-c` on laptops that fills the column under the other two)
  and `TALL` (portrait, small print) lists in the script. Phones show only the first two. When new gallery
  photos are added, add them to the matching list with a short handwritten-style caption.

## House style
- Colours come from the logo: teal ink #0E2A2F, Singapore red #D9343E. Keep it human, not "AI-looking".
- Sponsor cards: logo tile, name, "Type · Street", deal in red, conditions in one standard set of words
  (Cash only · Up to 4 people · Student ID needed · Mon–Thu · Until Mon YYYY), then "Directions →"
  and "Website →" (or "Instagram →" if there is no website; check the link is the Leeds branch).
- Plain, friendly wording. Don't invent numbers, prices or names.
- Singaporean touches stay SUBTLE (Jarryl, 5 Nov 2026): Peranakan-tile washi tape (`var(--peranakan)`, one pattern
  reused for all tape and the footer strip), the dated LEEDS ✈ SINGAPORE postmark on the big hero photo, and a
  little Singlish in small print ("Paiseh to ask?", "Copied lah!", "fuelled by kopi"). Don't pile on more flags,
  Merlions or slang; one light touch per area.
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
posts a ⏳ placeholder and runs the full check itself (and recreates the task if it was deleted, when it can). Backup of the prompt:
`routines/site-check-cloud.md` in the private repo waveriderjc-max/jobsearch.

## Visitor stats (since 27 Oct 2026)
GoatCounter (no cookies, so no cookie banner needed): https://leedssingsoc.goatcounter.com . The script block
at the end of `index.html` counts page views and sends events named `tap-…` (buttons/links, e.g.
`tap-membership-<section>`, `tap-whatsapp-<section>`, `tap-directions-<sponsor>`, `tap-ticket-<event>`),
`open-faq-…`/`open-more-…` (details opened), `play-video-…` and `see-<section>` (section scrolled into view).
Keep it when editing the page; new buttons are tracked automatically. Counts only, never who someone is.
The daily site check reads the stats with env var GOATCOUNTER_TOKEN (read-only API token).
