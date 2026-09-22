# -*- coding: utf-8 -*-
"""Генератор SEO-раздела ms-dos.su: 100 статей + каталог + sitemap + robots."""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
SITE = 'https://ms-dos.su'

from seo_data_1 import COMMANDS
from seo_data_2 import VENDORS, ERRORS, FILESYSTEMS
from seo_data_3 import NC, QBASIC, DOSBOX, MEMORY
from seo_data_4 import VERSIONS, COMPARE, GUIDES
from seo_data_faq import VENDOR_FAQ, ERROR_FAQ

HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ms-dos.su — MBFU">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}/{slug}.html">
<meta property="og:image" content="{site}/assets/icon-64.png">
<meta property="og:locale" content="ru_RU">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="dns-prefetch" href="https://github.com">
{jsonld}
<meta name="yandex-verification" content="bb775f01a3383d99">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Y8PG2P181B"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-Y8PG2P181B');
</script>
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=106570050', 'ym');
    ym(106570050, 'init', {{ssr:true, webvisor:true, clickmap:true, accurateTrackBounce:true, trackLinks:true}});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/106570050" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<link rel="stylesheet" href="style.css">
<link rel="icon" type="image/png" href="assets/icon-64.png">
</head>
<body>
<nav class="crumbs"><a href="./">MBFU</a> / <a href="stati.html">Статьи</a></nav>
<main>
<article>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{sections}
{faq}
</article>
<aside>
<h2>Читайте также</h2>
<ul>
{related}
</ul>
<div class="cta-box">
<p><b>Нужна загрузочная флешка MS-DOS?</b></p>
<p>MBFU сделает ее за пару кликов: MS-DOS 5.00/6.22 + Norton Commander.</p>
<p><a class="btn" href="https://github.com/sementsul/ms-dos/releases">Скачать MBFU</a></p>
</div>
</aside>
</main>
<footer>
<p><a href="../">MBFU</a> · (c) 2025 Sementsul Maxim · MIT · MS-DOS (c) Microsoft</p>
</footer>
</body>
</html>
"""


def esc(s):
    return html.escape(s, quote=True)


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


import json as _json


def jsonld(p):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p['h1'],
        "description": p['desc'],
        "inLanguage": "ru",
        "author": {"@type": "Organization", "name": "MBFU"},
        "publisher": {"@type": "Organization", "name": "MBFU"},
        "mainEntityOfPage": SITE + '/' + p['slug'] + '.html',
        "datePublished": "2026-09-22",
        "dateModified": "2026-09-22",
    }
    if p['faq']:
        data["mainEntity"] = [{
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        } for q, a in p['faq']]
    return ('<script type="application/ld+json">\n%s\n</script>' %
            _json.dumps(data, ensure_ascii=False))


def render(p, related):
    secs = ''.join('<h2>%s</h2>\n%s\n' % (h, b) for h, b in p['sections'])
    faq = ''
    if p['faq']:
        faq = '<h2>Вопросы и ответы</h2>\n' + ''.join(
            '<p><b>%s</b><br>%s</p>\n' % (q, a) for q, a in p['faq'])
    rel = '\n'.join('<li><a href="%s.html">%s</a></li>' % (r['slug'], esc(r['h1']))
                    for r in related)
    return HEAD.format(site=SITE, slug=p['slug'], title=esc(p['title']),
                       desc=esc(p['desc']), h1=esc(p['h1']),
                       lead=p['lead'], sections=secs, faq=faq, related=rel,
                       jsonld=jsonld(p))


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
    # каталог
    cats = ''.join(
        '<h2>%s</h2>\n<ul>\n%s\n</ul>\n' % (c, '\n'.join(
            '<li><a href="%s.html">%s</a></li>' % (p['slug'], esc(p['h1']))
            for p in lst)) for c, lst in bycat.items())
    with open(os.path.join(DOCS, 'stati.html'), 'w', encoding='utf-8') as f:
        f.write(HEAD.format(
            site=SITE, slug='stati', title='Статьи про MS-DOS, DOS и загрузочные флешки | ms-dos.su',
            desc='100 статей: команды DOS, версии MS-DOS, Secure Boot, Norton Commander, ошибки и гайды.',
            h1='Статьи', lead='Вся база знаний: от первой команды DIR до мультизагрузки.',
            sections=cats, faq='', related='',
            jsonld=jsonld({'slug': 'stati', 'h1': 'Статьи про MS-DOS',
                           'desc': 'Каталог из 100 статей про MS-DOS.', 'faq': []})))
    # sitemap
    urls = ([SITE + '/', SITE + '/stati.html', SITE + '/dos-test.html'] +
            [SITE + '/%s.html' % p['slug'] for p in pages])
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          ''.join('<url><loc>%s</loc></url>\n' % u for u in urls) + '</urlset>\n')
    with open(os.path.join(ROOT, 'docs', 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sm)
    with open(os.path.join(ROOT, 'docs', 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE)
    print('OK: %d страниц + каталог + sitemap' % len(pages))


if __name__ == '__main__':
    main()
