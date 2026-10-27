"""Print the text of a public Google Form so ticket prices can be copied onto the website.

Works with any form layout: it prints the title, description, every section and question
(with answer options), then lists every line that mentions a £ price. Bank details and
phone numbers are blanked out so they never end up in the website or a chat.

Usage: python tools/read_form.py https://forms.gle/...   (the share link, not the /edit link)
"""
import html
import json
import re
import sys
import urllib.request

SECTION, TEXT_BLOCK = 8, 6
PRICE = re.compile(r"£\s?\d+(?:\.\d{2})?")
REDACT = [
    (re.compile(r"\b\d{2}[- ]\d{2}[- ]\d{2}\b"), "[sort code hidden]"),
    (re.compile(r"\b\d{8}\b"), "[account number hidden]"),
    (re.compile(r"(?:\+44\s?7\d{3}|\b07\d{3})\s?\d{3}\s?\d{3}\b"), "[phone hidden]"),
]


def redact(text):
    for pattern, label in REDACT:
        text = pattern.sub(label, text)
    return text


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.geturl(), r.read().decode("utf-8", "replace")


def load_data(page):
    m = re.search(r"FB_PUBLIC_LOAD_DATA_ = (\[.*?\]);\s*</script>", page, re.S)
    return json.loads(m.group(1)) if m else None


def main(url):
    final_url, page = fetch(url)
    if "/edit" in final_url:
        sys.exit("That is the editor link. Ask for the share link (Send > link icon), ending in /viewform or forms.gle.")
    data = load_data(page)
    if data is None:
        closed = "no longer accepting" in page.lower()
        sys.exit("The form is closed (not accepting responses)." if closed else "Couldn't read this form. Is it public?")

    form = data[1]
    title = form[8] or data[3] or "(untitled form)"
    # Each entry: (label, text, where it sits), so a price can be traced to its section.
    lines = [("TITLE", title, "title"), ("DESCRIPTION", form[0] or "", "form description")]
    where, n = "form description", 0
    for item in form[1] or []:
        kind, name, desc = item[3], item[1] or "", item[2] or ""
        if kind == SECTION:
            n += 1
            where = f"section {n} '{name.strip()}'"
        label = "SECTION" if kind == SECTION else "TEXT" if kind == TEXT_BLOCK else "QUESTION"
        lines.append((label, name + ("\n" + desc if desc else ""), where))
        if item[4] and item[4][0] and len(item[4][0]) > 1 and isinstance(item[4][0][1], list):
            for opt in item[4][0][1]:
                if opt and opt[0]:
                    lines.append(("  option", opt[0], where))

    print(f"Form: {final_url}\n")
    for label, text, _ in lines:
        text = redact(html.unescape(text)).strip()
        if text:
            print(f"[{label}] {text}\n")

    print("=== Lines with prices ===")
    seen = set()
    for _, text, where in lines:
        for line in redact(html.unescape(text)).splitlines():
            line = line.strip()
            if (PRICE.search(line) or re.search(r"sold out", line, re.I)) and (line, where) not in seen:
                seen.add((line, where))
                print(f"  {line}    <- {where}")
    if not seen:
        print("  (none found: the prices may be in an image or worded without £)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
