# -*- coding: utf-8 -*-
"""Shared HTML shell (head, navigation, footer, consent banner) for ms-dos.su."""
import json

from site_config import (SITE, BRAND, PRODUCT, AUTHOR, COPYRIGHT, BUY_URL,
                         GITHUB, TRIAL_ZIP, TRIAL_DAYS, GA_ID, METRIKA_ID,
                         YANDEX_VERIFICATION, CONSENT_VERSION, SELLER)

NAV = {
    "ru": [("Возможности", "/#features"), ("Trial", "/#trial"),
           ("Купить", "/#buy"), ("Статьи", "/stati.html"),
           ("Контакты", "/contacts.html")],
    "en": [("Features", "/en/#features"), ("Trial", "/en/#trial"),
           ("Buy", "/en/#buy"), ("Guides", "/en/stati.html"),
           ("Contact", "/en/contacts.html")],
}

FOOT = {
    "ru": [("/terms.html", "Условия и лицензия"),
           ("/privacy.html", "Конфиденциальность"),
           ("/cookies.html", "Файлы cookie"),
           ("/refund.html", "Оплата и возврат"),
           ("/contacts.html", "Контакты и реквизиты"),
           ("/licenses.html", "Сторонние лицензии"),
           ("/dmca.html", "Правообладателям"),
           ("/accessibility.html", "Доступность")],
    "en": [("/en/terms.html", "Terms and licence"),
           ("/en/privacy.html", "Privacy"),
           ("/en/cookies.html", "Cookies"),
           ("/en/refund.html", "Payment and refunds"),
           ("/en/contacts.html", "Contacts and seller details"),
           ("/en/licenses.html", "Third-party licences"),
           ("/en/dmca.html", "Rights holders"),
           ("/en/accessibility.html", "Accessibility")],
}

T = {
    "ru": {
        "skip": "Перейти к содержанию",
        "home": "Главная",
        "articles": "Статьи",
        "buy": "Полная версия на Boosty",
        "buy_note": "Trial — 30 дней бесплатно",
        "brand_tag": "Утилита для работы с образами MS-DOS",
        "legal_note": ("MS-DOS — товарный знак Microsoft Corporation. "
                       "DOSBox распространяется по GPLv2. "
                       "MBFU не связана с Microsoft и не распространяет MS-DOS."),
        "cookie_settings": "Настройки cookie",
        "consent_text": ("Мы используем файлы cookie для аналитики, чтобы "
                         "понимать, чем полезна документация. Аналитические "
                         "скрипты включаются только с вашего согласия; без него "
                         "сайт работает без cookie."),
        "consent_more": "Подробнее",
        "consent_accept": "Принять аналитику",
        "consent_reject": "Только необходимые",
        "consent_title": "Настройки cookie",
        "analytics": "Аналитика",
        "analytics_desc": ("Яндекс.Метрика и Google Analytics: обезличенная "
                           "статистика посещений. Устанавливают cookie _ym_* и _ga*."),
        "save": "Сохранить",
        "close": "Закрыть",
        "footer_docs": "Документы",
        "footer_project": "Проект",
    },
    "en": {
        "skip": "Skip to content",
        "home": "Home",
        "articles": "Guides",
        "buy": "Full version on Boosty",
        "buy_note": "Trial — 30 days free",
        "brand_tag": "MS-DOS image toolkit",
        "legal_note": ("MS-DOS is a trademark of Microsoft Corporation. "
                       "DOSBox is distributed under GPLv2. MBFU is not affiliated "
                       "with Microsoft and does not distribute MS-DOS."),
        "cookie_settings": "Cookie settings",
        "consent_text": ("We use cookies for analytics to understand which docs "
                         "are useful. Analytics scripts run only with your "
                         "consent; without it the site works without cookies."),
        "consent_more": "Details",
        "consent_accept": "Accept analytics",
        "consent_reject": "Essential only",
        "consent_title": "Cookie settings",
        "analytics": "Analytics",
        "analytics_desc": ("Yandex Metrica and Google Analytics: aggregate visit "
                           "statistics. They set _ym_* and _ga* cookies."),
        "save": "Save",
        "close": "Close",
        "footer_docs": "Documents",
        "footer_project": "Project",
    },
}


def url_for(lang, slug):
    tail = "" if slug in ("index", "") else slug + ".html"
    if lang == "en":
        return SITE + "/en/" + tail
    return SITE + "/" + tail


def _jsonld_script(data):
    if not data:
        return ""
    if isinstance(data, list):
        payload = {"@context": "https://schema.org", "@graph": data}
    else:
        payload = data
    return ('<script type="application/ld+json">\n%s\n</script>\n'
            % json.dumps(payload, ensure_ascii=False, indent=1))


def head(lang, slug, title, desc, jsonld=None, has_en=True, extra_head=""):
    canonical = url_for(lang, slug)
    alts = []
    if has_en:
        alts = [
            '<link rel="alternate" hreflang="ru" href="%s">' % url_for("ru", slug),
            '<link rel="alternate" hreflang="en" href="%s">' % url_for("en", slug),
            '<link rel="alternate" hreflang="x-default" href="%s">' % url_for("ru", slug),
        ]
    other = "en" if lang == "ru" else "ru"
    html_lang = "ru" if lang == "ru" else "en"
    return """<!DOCTYPE html>
<html lang="{hl}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{brand} — ms-dos.su">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/og.png">
<meta property="og:locale" content="{locale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0e1a">
<meta name="yandex-verification" content="{yv}">
<link rel="stylesheet" href="{css}">
<link rel="icon" type="image/png" href="{icon}">
<link rel="apple-touch-icon" href="{site}/assets/icon-64.png">
{jsonld}{extra}<script src="{assets}consent.js" defer></script>
</head>
<body>
<a class="skip" href="#main">{skip}</a>
""".format(
        hl=html_lang, title=title, desc=desc, canonical=canonical,
        alts="\n".join(alts) + ("\n" if alts else ""),
        brand=BRAND, site=SITE,
        locale="ru_RU" if lang == "ru" else "en_US",
        yv=YANDEX_VERIFICATION,
        css="/style.css",
        icon="/assets/icon-64.png",
        jsonld=_jsonld_script(jsonld),
        extra=extra_head,
        assets="/assets/",
        skip=T[lang]["skip"],
    ) + topbar(lang, slug, has_en)


def topbar(lang, slug, has_en=True):
    t = T[lang]
    other = "en" if lang == "ru" else "ru"
    tail = "" if slug in ("index", "") else slug + ".html"
    # Root-relative so the same markup works in a local preview and on the domain.
    other_url = ("/en/" if lang == "ru" else "/") + tail
    if not has_en:
        # No translated twin (the 100 reference articles): point at the
        # English section landing page instead of a missing URL.
        other_url = "/en/" if lang == "ru" else "/"
    other_label = "EN" if lang == "ru" else "RU"
    items = "\n".join('      <a href="%s">%s</a>' % (href, label)
                      for label, href in NAV[lang])
    return """<header class="topbar">
  <a class="brand" href="{home}"><img src="/assets/icon-64.png" alt="" width="28" height="28"> {brand}</a>
  <nav aria-label="{nav_label}">
{items}
  </nav>
  <span class="lang"><a href="{other_url}" hreflang="{other}" lang="{other}" aria-label="{other_label}">{other_label}</a></span>
</header>
<main id="main">
""".format(home="/en/" if lang == "en" else "/", site=SITE, brand=BRAND,
           nav_label="Основная навигация" if lang == "ru" else "Main navigation",
           items=items, other_url=other_url, other=other,
           other_label=other_label)


def footer(lang, slug, has_en=True):
    t = T[lang]
    links = "\n".join('      <a href="%s">%s</a>' % (href, label)
                      for href, label in FOOT[lang])
    articles = "/en/stati.html" if lang == "en" else "/stati.html"
    lang_href = "/" if lang == "en" else "/en/"
    if not has_en:
        lang_href = "/en/" if lang == "ru" else "/"
    if lang == "ru":
        seller_line = ('Самозанятый %s, ИНН %s · '
                       '<a href="mailto:%s">%s</a>' % (
                           SELLER["name"], SELLER["inn"],
                           SELLER["email"], SELLER["email"]))
    else:
        seller_line = ('Self-employed %s, INN %s · '
                       '<a href="mailto:%s">%s</a>' % (
                           SELLER.get("name_en") or SELLER["name"],
                           SELLER["inn"], SELLER["email"], SELLER["email"]))
    return """</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <p><b>{brand}</b> — {tag}.</p>
        <p>© {copyright} {author}</p>
        <p class="seller">{seller_line}</p>
        <p><a href="{github}" rel="noopener">{github_label}</a></p>
      </div>
      <div>
        <h2>{docs}</h2>
        <nav aria-label="{docs}">
{links}
        </nav>
      </div>
      <div>
        <h2>{project}</h2>
        <nav aria-label="{project}">
          <a href="{articles}">{articles_label}</a>
          <a href="{buy}" rel="noopener">{buy}</a>
          <a href="{lang_href}" hreflang="{lang_other}" lang="{lang_other}">{lang_label}</a>
        </nav>
        <p class="note">{buy_note}</p>
        <button type="button" class="cookie-settings" data-consent-settings>{cookie_settings}</button>
      </div>
    </div>
    <p class="legal-note">{legal_note}</p>
  </div>
</footer>
{consent}
</body>
</html>
""".format(brand=BRAND, tag=t["brand_tag"], copyright=COPYRIGHT, author=AUTHOR,
           seller_line=seller_line,
           github=GITHUB, github_label="github.com/sementsul/ms-dos",
           docs=t["footer_docs"], project=t["footer_project"], links=links,
           articles=articles, articles_label=t["articles"], buy=BUY_URL,
           buy_note=t["buy_note"], site=SITE,
           cookie_settings=t["cookie_settings"], legal_note=t["legal_note"],
           lang_href=lang_href,
           lang_other="ru" if lang == "en" else "en",
           lang_label=("Русская версия" if lang == "en" else "English version"),
           consent=consent_markup(lang))


def consent_markup(lang):
    t = T[lang]
    return """<div class="consent" id="consent" hidden lang="{lang}">
  <div class="consent-inner">
    <p>{text} <a href="{more}">{more_label}</a>.</p>
    <div class="consent-actions">
      <button type="button" id="consent-accept" class="primary">{accept}</button>
      <button type="button" id="consent-reject">{reject}</button>
      <button type="button" data-consent-settings>{settings}</button>
    </div>
  </div>
</div>
<dialog class="consent-dialog" id="consent-dialog" lang="{lang}" aria-labelledby="consent-title">
  <h2 id="consent-title">{title}</h2>
  <form method="dialog">
    <div class="row">
      <input type="checkbox" id="consent-essential" checked disabled>
      <label for="consent-essential"><b>Необходимые</b><span>Нужны для работы сайта. Всегда включены.</span></label>
    </div>
    <div class="row">
      <input type="checkbox" id="consent-analytics">
      <label for="consent-analytics"><b>{analytics}</b><span>{analytics_desc}</span></label>
    </div>
    <div class="consent-actions">
      <button type="submit" id="consent-save" class="primary" value="save">{save}</button>
      <button type="submit" value="close" formnovalidate>{close}</button>
    </div>
  </form>
</dialog>
""".format(lang=lang, text=t["consent_text"], more=("/en/cookies.html" if lang == "en" else "/cookies.html"),
           more_label=t["consent_more"], accept=t["consent_accept"],
           reject=t["consent_reject"], settings=t["cookie_settings"],
           title=t["consent_title"], analytics=t["analytics"],
           analytics_desc=t["analytics_desc"], save=t["save"], close=t["close"],
           ) if lang == "en" else """<div class="consent" id="consent" hidden lang="ru">
  <div class="consent-inner">
    <p>{text} <a href="/cookies.html">{more_label}</a>.</p>
    <div class="consent-actions">
      <button type="button" id="consent-accept" class="primary">{accept}</button>
      <button type="button" id="consent-reject">{reject}</button>
      <button type="button" data-consent-settings>{settings}</button>
    </div>
  </div>
</div>
<dialog class="consent-dialog" id="consent-dialog" lang="ru" aria-labelledby="consent-title">
  <h2 id="consent-title">{title}</h2>
  <form method="dialog">
    <div class="row">
      <input type="checkbox" id="consent-essential" checked disabled>
      <label for="consent-essential"><b>Необходимые</b><span>Нужны для работы сайта. Всегда включены.</span></label>
    </div>
    <div class="row">
      <input type="checkbox" id="consent-analytics">
      <label for="consent-analytics"><b>{analytics}</b><span>{analytics_desc}</span></label>
    </div>
    <div class="consent-actions">
      <button type="submit" id="consent-save" class="primary" value="save">{save}</button>
      <button type="submit" value="close" formnovalidate>{close}</button>
    </div>
  </form>
</dialog>
""".format(text=t["consent_text"], more_label=t["consent_more"],
             accept=t["consent_accept"], reject=t["consent_reject"],
             settings=t["cookie_settings"], title=t["consent_title"],
             analytics=t["analytics"], analytics_desc=t["analytics_desc"],
             save=t["save"], close=t["close"])