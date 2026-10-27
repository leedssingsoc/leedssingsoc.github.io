# Leeds Singaporean Society website

Live at: https://leedssingsoc.github.io/

Everything is in `index.html`, with images and videos alongside it.

## Add an event (quick way)

Upload the poster (optional) with **Add file → Upload files**, then edit `index.html`,
find `<script type="application/json" id="extra-events">` near the bottom and add an entry:

```json
[
  {
    "title": "Mooncake Night",
    "date": "2026-11-20",
    "time": "7pm – 10pm",
    "venue": "Leeds University Union",
    "price": "Free for members · £3 non-members",
    "desc": "One or two sentences about the event.",
    "link": "https://engage.luu.org.uk/...",
    "linkLabel": "Get tickets",
    "poster": "mooncake-poster.jpg"
  }
]
```

For events with ticket stages, use `"tiers"` instead of `"price"`, e.g.
`"tiers": [{"name": "Early bird", "soldOut": true}, {"name": "Advance", "price": "£18 members · £20 non-members"}]`,
and optionally `"priceNote": "..."` (shown next to the ticket button). To read the prices off a Google Form,
run `python tools/read_form.py <form share link>`.

Separate several events with commas. The site puts each one in date order under
"Coming up", adds a countdown, and moves it to "Already happened" after the date.
Ticket buttons switch to "Ticket sales have closed." when the event starts. To close
sales earlier, add `"closed": true` to the event (or `data-closed` to a hand-written card).
Commit the change; the site updates in about a minute.

Or ask Claude: send the poster and details and say "add this event to the leedssingsoc.github.io repo and push".
