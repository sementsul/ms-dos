# -*- coding: utf-8 -*-
"""Ping IndexNow (Bing, Yandex, Seznam) with every URL from the sitemaps.

Usage:  python tools/indexnow.py          # send the whole site
        python tools/indexnow.py --dry    # print what would be sent

The key file lives in tools/indexnow_key.txt and is published as
docs/<key>.txt, which is how the search engines verify ownership.
"""
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://ms-dos.su"
ENDPOINT = "https://api.indexnow.org/indexnow"


def key():
    with open(os.path.join(ROOT, "tools", "indexnow_key.txt"), encoding="utf-8") as f:
        return f.read().strip()


def urls():
    out = []
    for name in ("sitemap-main.xml", "sitemap-articles.xml"):
        path = os.path.join(ROOT, "docs", name)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("<loc>"):
                    out.append(line[5:-6])
    return out


def main():
    k = key()
    batch = urls()
    if "--dry" in sys.argv:
        print("key: %s (%d urls)" % (k, len(batch)))
        for u in batch:
            print("  ", u)
        return
    payload = json.dumps({
        "host": "ms-dos.su",
        "key": k,
        "keyLocation": SITE + "/" + k + ".txt",
        "urlList": batch,
    }).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=120) as r:
        print("HTTP %s, %d urls submitted" % (r.status, len(batch)))


if __name__ == "__main__":
    main()
