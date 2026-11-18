# -*- coding: utf-8 -*-
"""Build sitemaps and robots.txt from what is actually on disk in docs/.

Every .html file is collected, RU/EN twins are paired, and the pairs are
emitted with xhtml:link alternates.
"""
import os
import re

import site_config as cfg

ROOT = cfg.repo_root()
DOCS = cfg.docs_dir()
SITE = cfg.SITE

PRIORITY = {
    "": "1.0", "index": "1.0", "stati": "0.9", "dos-test": "0.9",
    "privacy": "0.4", "terms": "0.4", "cookies": "0.4", "refund": "0.4",
    "contacts": "0.5", "licenses": "0.3", "dmca": "0.3",
    "ms-dos-license": "0.5", "buy": "0.8", "trial-vs-full": "0.6",
    "verify": "0.5", "about": "0.5", "changelog": "0.4", "mbfu-format": "0.4",
    "accessibility": "0.3", "trademarks": "0.4",
}
SKIP = {"404"}


def collect():
    ru, en = {}, {}
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        slug = name[:-5]
        if slug in SKIP:
            continue
        ru[slug] = SITE + ("/" if slug == "index" else "/" + name)
    en_dir = os.path.join(DOCS, "en")
    if os.path.isdir(en_dir):
        for name in sorted(os.listdir(en_dir)):
            if name.endswith(".html"):
                slug = name[:-5]
                if slug in SKIP:
                    continue
                en[slug] = SITE + "/en/" + ("" if slug == "index" else name)
    return ru, en


def url_entry(loc, slug, alt_ru=None, alt_en=None, priority="0.6"):
    lines = ["  <url>", "    <loc>%s</loc>" % loc]
    if alt_ru:
        lines.append('    <xhtml:link rel="alternate" hreflang="ru" href="%s"/>' % alt_ru)
    if alt_en:
        lines.append('    <xhtml:link rel="alternate" hreflang="en" href="%s"/>' % alt_en)
    if alt_ru:
        lines.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % alt_ru)
    lines.append("    <changefreq>monthly</changefreq>")
    lines.append("    <priority>%s</priority>" % priority)
    lines.append("  </url>")
    return "\n".join(lines)


def write_sitemap(path, entries):
    body = "\n".join(entries)
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
                '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                + body + "\n</urlset>\n")


def main():
    ru, en = collect()
    core = {"index", "stati", "dos-test", "privacy", "terms", "cookies",
            "refund", "contacts", "licenses", "ms-dos-license", "dmca",
            "accessibility", "buy", "trial-vs-full", "verify", "about",
            "changelog", "mbfu-format", "trademarks"}

    main_entries, article_entries = [], []
    for slug, loc in ru.items():
        alt_ru = loc
        alt_en = en.get(slug)
        priority = PRIORITY.get(slug, "0.6")
        entry = url_entry(loc, slug, alt_ru, alt_en, priority)
        (main_entries if slug in core else article_entries).append(entry)

    for slug, loc in en.items():
        alt_ru = ru.get(slug)
        entry = url_entry(loc, slug, alt_ru, loc, PRIORITY.get(slug, "0.6"))
        (main_entries if slug in core else article_entries).append(entry)

    write_sitemap(os.path.join(DOCS, "sitemap-main.xml"), main_entries)
    write_sitemap(os.path.join(DOCS, "sitemap-articles.xml"), article_entries)
    with open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "".join("  <sitemap><loc>%s/sitemap-%s.xml</loc></sitemap>\n" % (SITE, n)
                          for n in ("main", "articles"))
                + "</sitemapindex>\n")

    with open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)

    print("sitemap: %d main, %d article urls (%d ru, %d en)"
          % (len(main_entries), len(article_entries), len(ru), len(en)))


if __name__ == "__main__":
    main()