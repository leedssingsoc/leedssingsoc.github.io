# Leeds Singaporean Society website

Live at: https://waveriderjc-max.github.io/leeds-singsoc-site/

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

Separate several events with commas. The site puts each one in date order under
"Coming up", adds a countdown, and moves it to "Already happened" after the date.
Commit the change; the site updates in about a minute.

Or ask Claude: send the poster and details and say "add this event to the leeds-singsoc-site repo and push".
