"""Quietly take an event off the website (e.g. a trip cancelled for low sign-ups), with no "cancelled" notice.

Removes the event card (<article id="...">) and its "Already happened" row, so the event simply disappears:
no sign-up button, no countdown, and it never shows up in the past list. Its poster file is left in place.

Usage: python tools/remove_event.py york-xmas            (shows what it would remove)
       python tools/remove_event.py york-xmas --apply    (removes it from index.html)
"""
import re
import sys


def main(card_id, apply):
    path = "index.html"
    s = open(path, encoding="utf-8").read()
    m = re.search(r'\n[ \t]*<article\b[^>]*\bid="%s"[^>]*>.*?</article>[ \t]*\n' % re.escape(card_id), s, re.S)
    if not m:
        sys.exit(f"No event card with id=\"{card_id}\" found.")
    card = m.group(0)
    title = re.search(r'<h3 class="ftitle">(.*?)</h3>', card, re.S).group(1).strip()
    until = re.search(r'data-until="([\d-]+)"', card).group(1)
    s2 = s[:m.start()] + "\n" + s[m.end():]
    s2 = re.sub(r'\n\n\n+', "\n\n", s2)
    row = re.search(r'\n[ \t]*<div class="row" data-after="%s"[^\n]*<h4>%s</h4>[^\n]*' % (until, re.escape(title)), s2)
    if row:
        s2 = s2[:row.start()] + s2[row.end():]
    links = re.findall(r'data-tickets-for="%s"' % re.escape(card_id), s2) + re.findall(r'href="#%s"' % re.escape(card_id), s2)
    print(f"Event: {title} ({until})\n- card: {card.count(chr(10))} lines\n- past row: {'yes' if row else 'none found'}")
    if links:
        print(f"! {len(links)} other link(s) still point to #{card_id}: remove them by hand")
    if apply:
        open(path, "w", encoding="utf-8").write(s2)
        print("Removed from index.html. Test, commit and push to main.")
    else:
        print("Dry run: nothing changed. Add --apply to remove it.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], "--apply" in sys.argv[2:])
