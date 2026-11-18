# -*- coding: utf-8 -*-
import importlib
import re
import sys
from html.parser import HTMLParser

PATH = "seo_data_8a.py"
raw = open(PATH, "rb").read()
print("BOM:", raw[:3] == b"\xef\xbb\xbf")
text = raw.decode("utf-8")
lines = text.splitlines()
print("line1:", repr(lines[0]))
print("line2:", repr(lines[1]))

sys.path.insert(0, ".")
A = importlib.import_module("seo_data_8a").ARTICLES
print("count:", len(A))

ALLOWED_TAGS = {"p", "ul", "ol", "li", "b", "code", "pre", "table", "tr", "th", "td", "a"}
ALLOWED_LINKS = {
    "kak-sozdat-zagruzochnuyu-fleshku-ms-dos-hub", "ms-dos-622-na-fleshku",
    "ms-dos-license", "dosbox-mount", "dosbox-imgmount", "dosbox-conf",
    "dosbox-cycles", "dosbox-znakomstvo", "komanda-fdisk", "komanda-format",
    "komanda-sys", "mbfu-protiv-tolko-dosbox", "chto-takoe-ms-dos",
    "oshibki-zagruzki-dos-hub", "emm386", "himem-sys",
}
VOID = {"br", "hr", "img", "input", "meta", "link"}
QUERIES = {
    "igry-ms-dos-v-dosbox": ["ms dos игры", "игры для ms dos", "doom ms dos", "ms dos games", "запуск игры dos"],
    "emulyator-ms-dos": ["эмулятор ms dos", "эмулятор ms dos скачать", "ms dos online", "эмулятор ms dos для windows 10", "эмулятор ms dos на андроид", "ms dos emulator"],
    "ms-dos-v-virtualbox": ["ms dos virtualbox", "установка ms dos на virtualbox", "как установить ms dos на virtualbox", "скачать ms dos для virtualbox"],
}

class Check(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED_TAGS:
            self.errors.append("tag " + tag)
        if tag not in VOID:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append("mismatch </%s> stack=%s" % (tag, self.stack[-3:]))
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()

def visible(html):
    return re.sub(r"<[^>]+>", " ", html)

def words(s):
    return re.findall(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-'][A-Za-zА-Яа-яЁё0-9]+)*", s)

ok = True
for a in A:
    print("\n===", a["slug"])
    joined = " ".join([a["h1"], a["title"], a["desc"], a["lead"]]
                      + [h + " " + b for h, b in a["sections"]]
                      + [q + " " + x for q, x in a["faq"]]
                      + [n + " " + s for n, s in a.get("howto", [])])
    print("title", len(a["title"]), "desc", len(a["desc"]), "lead", len(a["lead"]))
    body = visible(joined)
    print("words", len(words(body)))
    body2 = a["lead"] + " " + " ".join(b for h, b in a["sections"]) + " " + " ".join(q + " " + x for q, x in a["faq"]) + " " + " ".join(n + " " + s for n, s in a.get("howto", []))
    print("body-only", len(words(visible(body2))), "with-heads", len(words(visible(body2 + " " + " ".join(h for h, b in a["sections"])))))

    parser = Check()
    all_html = "".join(b for _, b in a["sections"])
    parser.feed(all_html)
    parser.close()
    print("html errors:", parser.errors, "unclosed:", parser.stack)

    hrefs = re.findall(r'href="([^"]+)"', all_html)
    print("links", len(hrefs))
    for h in hrefs:
        if h not in {"https://ms-dos.su/%s.html" % s for s in ALLOWED_LINKS}:
            print("BAD LINK", h)
            ok = False

    low = joined.lower()
    missing = [q for q in QUERIES[a["slug"]] if q not in low]
    print("missing queries:", missing)

    for bad in ["Visual Studio", "Norton", "!", "тысяч", "<div", "<span", "style=", "<h1", "<h2", "<h3"]:
        if bad.lower() in joined.lower():
            print("FORBIDDEN:", bad)
            ok = False

    if '"' in body:
        print("straight double quote in visible text")
    if re.search(r"\s-\s", body):
        print("hyphen dash")

print("\nALL OK:", ok)