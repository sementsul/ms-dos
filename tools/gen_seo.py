# -*- coding: utf-8 -*-
"""Генератор SEO-раздела ms-dos.su: 100 статей + каталог.

Шапка, подвал и баннер согласия берутся из layout.py, чтобы статьи выглядели
так же, как остальные страницы сайта.
"""
import html
import json
import os

import layout
import site_config as cfg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SITE = cfg.SITE

from seo_data_1 import COMMANDS
from seo_data_2 import VENDORS, ERRORS, FILESYSTEMS
from seo_data_3 import NC, QBASIC, DOSBOX, MEMORY
from seo_data_4 import VERSIONS, COMPARE, GUIDES
from seo_data_faq import VENDOR_FAQ, ERROR_FAQ


def esc(s):
    return html.escape(str(s), quote=True)


def build_pages():
    pages = []
    for slug, cmd, syntax, purpose, params, examples, pitfalls, faq in COMMANDS:
        secs = [('Синтаксис', '<pre>%s</pre>' % esc(syntax))]
        if params:
            rows = ''.join('<tr><td><code>%s</code></td><td>%s</td></tr>' % (esc(k), v)
                           for k, v in params)
            secs.append(('Все параметры',
                         '<table><tr><th>Ключ</th><th>Что делает</th></tr>%s</table>' % rows))
        if examples:
            secs.append(('Примеры',
                         ''.join('<pre>%s</pre>\n<p>%s</p>\n' % (esc(c), cm)
                                 for c, cm in examples)))
        if pitfalls:
            secs.append(('Типичные ошибки',
                         '<ul>%s</ul>' % ''.join('<li>%s</li>' % p for p in pitfalls)))
        pages.append(dict(
            slug=slug, cat='Команды MS-DOS',
            title='Команда %s MS-DOS: все параметры и примеры | ms-dos.su' % cmd,
            desc='Команда %s: полный синтаксис, все ключи (%d), примеры и типичные ошибки.' % (cmd, len(params)),
            h1='Команда %s' % cmd,
            lead=purpose,
            sections=secs, faq=faq))
    for slug, vendor, lead, steps, note in VENDORS:
        pages.append(dict(
            slug=slug, cat='Secure Boot',
            title='Отключить Secure Boot на %s для загрузки DOS | ms-dos.su' % vendor,
            desc='Как отключить Secure Boot на %s и загрузиться с DOS-флешки: пошаговая инструкция.' % vendor,
            h1='Secure Boot на %s' % vendor,
            lead=lead,
            sections=[('Пошагово', '<ol>%s</ol>' % ''.join('<li>%s</li>' % s for s in steps)),
                      ('Нюанс', '<p>%s</p>' % note)],
            faq=VENDOR_FAQ[slug]))
    for slug, err, lead, causes, fixes in ERRORS:
        pages.append(dict(
            slug=slug, cat='Ошибки',
            title='%s — причины и решение | ms-dos.su' % err,
            desc='%s: почему возникает и как исправить.' % err,
            h1=err, lead=lead,
            sections=[('Причины', '<ul>%s</ul>' % ''.join('<li>%s</li>' % c for c in causes)),
                      ('Решение', '<ol>%s</ol>' % ''.join('<li>%s</li>' % f for f in fixes))],
            faq=ERROR_FAQ[slug]))
    for slug, h1, lead, facts, note in FILESYSTEMS:
        pages.append(dict(
            slug=slug, cat='Файловые системы',
            title='%s | ms-dos.su' % h1,
            desc='%s: лимиты и совместимость с DOS.' % h1.split(':')[0],
            h1=h1, lead=lead,
            sections=[('Факты', '<ul>%s</ul>' % ''.join('<li>%s</li>' % f for f in facts)),
                      ('Вывод', '<p>%s</p>' % note)],
            faq=[]))
    for data, cat in [(NC, 'Norton Commander'), (QBASIC, 'QBASIC'),
                      (DOSBOX, 'DOSBox'), (MEMORY, 'Память и железо'),
                      (VERSIONS, 'Версии MS-DOS'), (COMPARE, 'Сравнение'),
                      (GUIDES, 'Гайды')]:
        for row in data:
            slug, h1, lead = row[0], row[1], row[2]
            rest = row[3:]
            sections = []
            for i, block in enumerate(rest):
                if isinstance(block, list):
                    sections.append(('Детали' if i == 0 else 'Еще',
                                     '<ul>%s</ul>' % ''.join('<li>%s</li>' % b for b in block)))
                else:
                    sections.append(('Итог', '<p>%s</p>' % block))
            pages.append(dict(
                slug=slug, cat=cat,
                title='%s | ms-dos.su' % h1,
                desc=lead[:150],
                h1=h1, lead=lead, sections=sections, faq=[]))
    return pages


def jsonld(p, lang="ru"):
    url = SITE + ("/" + p['slug'] + ".html" if lang == "ru"
                  else "/en/" + p['slug'] + ".html")
    data = {
        "@context": "https://schema.org",
        "@type": "TechArticle" if p['cat'] in ('Команды MS-DOS', 'DOSBox') else "Article",
        "headline": p['h1'],
        "description": p['desc'],
        "inLanguage": lang,
        "author": {"@type": "Person", "name": cfg.AUTHOR},
        "publisher": {"@type": "Organization", "name": cfg.BRAND},
        "mainEntityOfPage": url,
        "datePublished": "2026-09-22",
        "dateModified": "2026-11-17",
        "isPartOf": {"@type": "WebSite", "name": cfg.BRAND, "url": SITE},
    }
    if p['faq']:
        data["mainEntity"] = [{
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        } for q, a in p['faq']]
    return data


def related_block(items):
    """Cross-links plus the trial / full-version call to action."""
    rel = '\n'.join('<li><a href="%s.html">%s</a></li>' % (r['slug'], esc(r['h1']))
                    for r in items)
    return """<aside>
<h2>Читайте также</h2>
<ul>
%s
</ul>
<div class="cta-box">
<p><b>Нужна загрузочная флешка MS-DOS?</b></p>
<p>Trial MBFUTool 2.0 — все функции на %d дней, без ключа активации.</p>
<p><a class="btn" href="/%s" download>Скачать Trial</a>
   <a class="btn ghost" href="%s" rel="noopener">Полная версия</a></p>
</div>
</aside>""" % (rel, cfg.TRIAL_DAYS, cfg.TRIAL_ZIP,
               cfg.BUY_URL)


def render(p, related):
    secs = ''.join('<h2>%s</h2>\n%s\n' % (h, b) for h, b in p['sections'])
    faq = ''
    if p['faq']:
        faq = ('<h2>Вопросы и ответы</h2>\n'
               + ''.join('<p><b>%s</b><br>%s</p>\n' % (q, a) for q, a in p['faq']))

    body = """<nav class="crumbs" aria-label="Хлебные крошки">
<a href="/">MBFU</a> / <a href="/stati.html">Статьи</a> / %s
</nav>

<section class="block">
  <div class="wrap">
    <article>
      <h1>%s</h1>
      <p class="lead">%s</p>
%s
%s
    </article>
%s
  </div>
</section>
""" % (esc(p['cat']), esc(p['h1']), p['lead'], secs, faq, related_block(related))

    head = layout.head("ru", p['slug'], esc(p['title']), esc(p['desc']),
                       jsonld=jsonld(p), has_en=False)
    return head + body + layout.footer("ru", p['slug'], has_en=False)


def main():
    pages = build_pages()
    assert len(pages) == 100, 'страниц: %d, надо 100' % len(pages)
    assert len({p['slug'] for p in pages}) == 100, 'дубли слагов!'
    os.makedirs(DOCS, exist_ok=True)
    bycat = {}
    for p in pages:
        bycat.setdefault(p['cat'], []).append(p)
    for p in pages:
        rel = [r for r in bycat[p['cat']] if r['slug'] != p['slug']][:6]
        with open(os.path.join(DOCS, p['slug'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(render(p, rel))

    cats = ''.join(
        '<h2>%s</h2>\n<ul class="mega">\n%s\n</ul>\n' % (c, '\n'.join(
            '<li><a href="%s.html">%s</a><br><small>%s</small></li>' % (p['slug'], esc(p['h1']), esc(p['desc']))
            for p in lst)) for c, lst in bycat.items())

    catalog = """<nav class="crumbs" aria-label="Хлебные крошки">
<a href="/">MBFU</a> / Статьи
</nav>

<section class="block">
  <div class="wrap">
    <h2>Статьи</h2>
    <p class="intro">Вся база знаний: от первой команды DIR до мультизагрузки.
    Сто статей про MS-DOS 5.00/6.22, DOSBox, Secure Boot и типичные ошибки.</p>
%s
    <div class="cta-box">
      <p><b>Нужна загрузочная флешка MS-DOS?</b></p>
      <p>Trial MBFUTool 2.0 — все функции на %d дней.</p>
      <p><a class="btn" href="/%s" download>Скачать Trial</a>
         <a class="btn ghost" href="%s" rel="noopener">Полная версия</a></p>
    </div>
  </div>
</section>
""" % (cats, cfg.TRIAL_DAYS, cfg.TRIAL_ZIP, cfg.BUY_URL)

    catalog_head = layout.head(
        "ru", "stati", "Статьи про MS-DOS, DOS и загрузочные флешки | ms-dos.su",
        "100 статей: команды DOS, версии MS-DOS, Secure Boot, Norton Commander, "
        "ошибки и гайды.", jsonld=jsonld({'slug': 'stati', 'cat': '', 'h1': 'База знаний MS-DOS',
                                          'desc': 'Каталог из 100 статей про MS-DOS.',
                                          'faq': []}), has_en=True)
    with open(os.path.join(DOCS, 'stati.html'), 'w', encoding='utf-8') as f:
        f.write(catalog_head + catalog + layout.footer("ru", "stati"))

    write_en_catalog(pages, bycat)
    print('OK: %d статей + каталог' % len(pages))


def write_en_catalog(pages, bycat):
    """English index of the knowledge base.

    The 100 reference articles are written in Russian; the English catalogue
    explains that and points to them instead of shipping machine translation.
    """
    rows = ''.join(
        '<tr><td>%s</td><td>%d</td></tr>' % (esc(cat), len(items))
        for cat, items in bycat.items())
    body = """<nav class="crumbs" aria-label="Breadcrumb">
<a href="/en/">MBFU</a> / Guides
</nav>

<section class="block">
  <div class="wrap">
    <h1>MS-DOS guides and reference</h1>
    <p class="lead">The knowledge base has 100 articles: DOS commands, MS-DOS 5.00 and
    6.22 internals, DOSBox, Secure Boot and typical errors. They are written in
    Russian — the language of the DOS documentation this project grew from — and are
    listed below by topic.</p>

    <table>
      <tr><th>Topic</th><th>Articles</th></tr>
      %s
      <tr><td><b>Total</b></td><td><b>%d</b></td></tr>
    </table>

    <p><a class="btn" href="/stati.html" hreflang="ru" lang="ru">Open the catalogue (RU)</a>
       <a class="btn ghost" href="/en/dos-test.html">Try MS-DOS in the browser</a></p>

    <h2>What is covered</h2>
    <ul>
      <li>every internal and external DOS command with all switches and examples;</li>
      <li>MS-DOS 5.00 vs 6.22, memory management, Himem.sys, Emm386, MemMaker;</li>
      <li>FAT12/FAT16 limits, 4 GB partitions on large USB drives, cluster size;</li>
      <li>Secure Boot and CSM on ASUS, MSI, Gigabyte, ASRock, Lenovo, Dell, HP;</li>
      <li>DOSBox configuration, mounting images, keyboard and mouse quirks;</li>
      <li>“No bootable device”, “Non-system disk”, “Bad command or file name” and
          other errors with fixes.</li>
    </ul>

    <div class="cta-box">
      <p><b>Need a bootable MS-DOS USB drive?</b></p>
      <p>The MBFUTool 2.0 trial gives you every feature for {{TRIAL_DAYS}} days, no key
      required.</p>
      <p><a class="btn" href="/{{TRIAL_ZIP}}" download>Download the trial</a>
         <a class="btn ghost" href="{{BUY_URL}}" rel="noopener">Full version</a></p>
    </div>
  </div>
</section>
""" % (rows, len(pages))

    body = render_body(body)
    head = layout.head(
        "en", "stati", "MS-DOS guides and reference | ms-dos.su",
        "100 articles on DOS commands, MS-DOS 5.00/6.22, DOSBox, Secure Boot and "
        "typical errors. Written in Russian.",
        jsonld=jsonld({'slug': 'stati', 'cat': '', 'h1': 'MS-DOS guides',
                       'desc': 'Knowledge base index', 'faq': []}, lang="en"),
        has_en=True)
    path = os.path.join(DOCS, "en", "stati.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + body + layout.footer("en", "stati"))


def render_body(text):
    """Substitute the tokens that the catalogue uses."""
    values = {
        "TRIAL_DAYS": str(cfg.TRIAL_DAYS),
        "TRIAL_ZIP": cfg.TRIAL_ZIP,
        "BUY_URL": cfg.BUY_URL,
    }
    for key, value in values.items():
        text = text.replace("{{%s}}" % key, value)
    return text


if __name__ == '__main__':
    main()