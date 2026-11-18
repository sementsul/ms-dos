# -*- coding: utf-8 -*-
"""Build the ms-dos.su pages that are not SEO articles.

Content lives in content/<lang>/<slug>.html as an HTML fragment (no <html>,
no header/footer).  This script wraps it with the shared shell, substitutes
site tokens, and writes docs/<slug>.html (ru) or docs/en/<slug>.html (en).

Run:  python tools/gen_site.py
"""
import glob
import hashlib
import os
import re
import sys

import layout
import site_config as cfg

ROOT = cfg.repo_root()
DOCS = cfg.docs_dir()
CONTENT = os.path.join(ROOT, "content")

# slug -> (ru title, ru description, en title, en description, jsonld kind)
PAGES = {
    "index": (
        "MBFUTool 2.0 — образы MS-DOS: создать, открыть, записать на USB",
        "MBFUTool 2.0 для Windows: запись образов MS-DOS на USB, создание .mbfu, "
        "клонирование носителей и редактирование в DOSBox. Trial — 30 дней без "
        "ограничений функций, полная версия на Boosty.",
        "MBFUTool 2.0 — create, edit and write MS-DOS images to USB",
        "MBFUTool 2.0 for Windows: write MS-DOS images to USB, create .mbfu "
        "images, clone media and edit images in DOSBox. 30-day trial with all "
        "features, full version on Boosty.",
        "software",
    ),
    "dos-test": (
        "Онлайн-тест MS-DOS 5.00 и 6.22 в браузере — ms-dos.su",
        "Загрузите свой загрузочный образ MS-DOS 5.00/6.22 и запустите его в "
        "браузере: эмулятор v86, файлы не отправляются на сервер.",
        "Test MS-DOS 5.00 and 6.22 online in your browser — ms-dos.su",
        "Load your own MS-DOS 5.00/6.22 boot floppy image and run it in the "
        "browser with the v86 emulator. Files never leave your computer.",
        "webpage",
    ),
    "privacy": (
        "Политика обработки персональных данных — ms-dos.su",
        "Какие данные собирает ms-dos.su, зачем, сколько хранит и как их удалить. "
        "Права по 152-ФЗ, GDPR и CCPA.",
        "Privacy Policy — ms-dos.su",
        "What data ms-dos.su collects, why, how long it is stored and how to "
        "delete it. Rights under the GDPR, CCPA and Russian law 152-FZ.",
        "webpage",
    ),
    "terms": (
        "Условия использования и лицензионное соглашение — ms-dos.su",
        "Лицензия на MBFUTool 2.0, правила использования, ответственность "
        "сторон, права потребителей РФ, ЕС и США.",
        "Terms of Use and Licence Agreement — ms-dos.su",
        "Licence for MBFUTool 2.0, acceptable use, liability, and consumer "
        "rights in the EU, the US and Russia.",
        "webpage",
    ),
    "cookies": (
        "Файлы cookie и аналитика — ms-dos.su",
        "Какие cookie ставит ms-dos.su, зачем, на какой срок и как отказаться. "
        "Аналитика включается только с согласия.",
        "Cookies and analytics — ms-dos.su",
        "Which cookies ms-dos.su sets, why, for how long and how to refuse. "
        "Analytics runs only with consent.",
        "webpage",
    ),
    "refund": (
        "Оплата, доставка и возврат — ms-dos.su",
        "Как проходит оплата через Boosty, что приходит после покупки, как "
        "запросить возврат по закону РФ, ЕС и США.",
        "Payment, delivery and refunds — ms-dos.su",
        "How payment through Boosty works, what you receive after purchase and "
        "how to request a refund under EU, US and Russian law.",
        "webpage",
    ),
    "contacts": (
        "Контакты и реквизиты продавца — ms-dos.su",
        "Реквизиты лицензиара, поддержка, сроки ответа и адрес для юридически "
        "значимых сообщений.",
        "Contacts and seller details — ms-dos.su",
        "Licensor details, support contacts, response times and the address for "
        "legal notices.",
        "webpage",
    ),
    "licenses": (
        "Сторонние лицензии: DOSBox, SDL, MS-DOS — ms-dos.su",
        "Что входит в поставку MBFUTool, под какими лицензиями распространяются "
        "DOSBox и SDL, где взять их исходный код и права на MS-DOS.",
        "Third-party licences: DOSBox, SDL, MS-DOS — ms-dos.su",
        "What ships with MBFUTool, the licences of DOSBox and SDL, where to get "
        "their source code, and the MS-DOS trademark.",
        "webpage",
    ),
    "trademarks": (
        "Товарные знаки и отсутствие связи с Microsoft — ms-dos.su",
        "MS-DOS и Windows — товарные знаки Microsoft Corporation. Сайт и программа "
        "не связаны с Microsoft, не спонсируются и не одобрены ею.",
        "Trademarks and non-affiliation — ms-dos.su",
        "MS-DOS and Windows are trademarks of Microsoft Corporation. This site and "
        "the program are not affiliated with, sponsored or endorsed by Microsoft.",
        "webpage",
    ),
    "buy": (
        "Купить MBFUTool 2.0 и получить файлы — ms-dos.su",
        "Что входит в покупку, как проходит оплата через Boosty, что приходит после "
        "неё, как получить чек по НПД и что делать, если доступ не открылся.",
        "Buy MBFUTool 2.0 and get the files — ms-dos.su",
        "What the purchase includes, how payment through Boosty works, what arrives "
        "afterwards, the tax receipt and what to do if access did not unlock.",
        "webpage",
    ),
    "trial-vs-full": (
        "Trial и полная версия: в чём разница — ms-dos.su",
        "Сравнение пробной и полной версии MBFUTool 2.0: срок, функции, ключ, "
        "обновления, поддержка и порядок перехода.",
        "Trial vs the full version — ms-dos.su",
        "Trial and full MBFUTool 2.0 compared: time limit, features, key, updates, "
        "support and how to switch.",
        "webpage",
    ),
    "verify": (
        "Как проверить сборку MBFUTool по SHA-256 — ms-dos.su",
        "Как сверить SHA-256 архива и установщика, что делать с предупреждением "
        "антивируса и какие файлы программа пишет на диск.",
        "How to verify the MBFUTool build — ms-dos.su",
        "How to compare the SHA-256 of the archive and installer, what to do with an "
        "antivirus warning, and what the program writes to disk.",
        "webpage",
    ),
    "about": (
        "Об авторе и проекте MBFUTool — ms-dos.su",
        "Кто делает и продаёт MBFUTool, почему версия 2.0 закрытая, что осталось "
        "открытым и как работает поддержка.",
        "About the author and the MBFUTool project — ms-dos.su",
        "Who builds and sells MBFUTool, why 2.0 is closed source, what stays open and "
        "how support works.",
        "webpage",
    ),
    "changelog": (
        "История версий MBFUTool и политика обновлений — ms-dos.su",
        "Что вошло в 2.0.0, как выходят обновления 2.x, что стало с линией 1.x "
        "и как сообщить об ошибке.",
        "MBFUTool version history and update policy — ms-dos.su",
        "What 2.0.0 includes, how 2.x updates ship, what happened to the 1.x line and "
        "how to report a bug.",
        "webpage",
    ),
    "mbfu-format": (
        "Формат образа .mbfu: спецификация — ms-dos.su",
        "Структура контейнера .mbfu: заголовок, сжатие zlib, SHA-256, пример "
        "чтения образа на Python и ограничения формата.",
        "The .mbfu image format: specification — ms-dos.su",
        "The .mbfu container: header layout, zlib compression, SHA-256, a Python "
        "reading example and format limits.",
        "webpage",
    ),
    "ms-dos-license": (
        "Где взять лицензионную копию MS-DOS — ms-dos.su",
        "Законные способы получить MS-DOS 5.00/6.22: каталог подписки Visual Studio "
        "my.visualstudio.com, ранее купленный экземпляр и образ со своих носителей.",
        "Where to get a licensed MS-DOS copy — ms-dos.su",
        "Lawful ways to obtain MS-DOS 5.00/6.22: the Visual Studio subscription "
        "catalogue at my.visualstudio.com, a copy you already own, and imaging your "
        "own media.",
        "webpage",
    ),
    "dmca": (
        "Правообладателям: уведомления и удаление — ms-dos.su",
        "Куда направить уведомление о нарушении авторских прав (DMCA и ст. 1253.1 "
        "ГК РФ) и как рассматриваются обращения.",
        "For rights holders: notices and takedown — ms-dos.su",
        "Where to send a copyright notice (DMCA and Russian Civil Code art. "
        "1253.1) and how claims are handled.",
        "webpage",
    ),
    "accessibility": (
        "Доступность сайта — ms-dos.su",
        "Насколько ms-dos.su соответствует WCAG 2.1 AA и European Accessibility "
        "Act, что уже сделано и как сообщить о проблеме.",
        "Accessibility statement — ms-dos.su",
        "How ms-dos.su meets WCAG 2.1 AA and the European Accessibility Act, "
        "what is done and how to report a barrier.",
        "webpage",
    ),
}


def load_sums():
    """Read the trial archive checksum produced by the build."""
    candidates = [
        os.path.join(ROOT, "mbfu-work", "trial", "out", "SHA256SUMS.txt"),
        os.path.join(os.path.dirname(ROOT), "mbfu-work", "trial", "out", "SHA256SUMS.txt"),
    ]
    path = next((p for p in candidates if os.path.isfile(p)), None)
    data = {"sha": "", "mb": 0.0, "setup_sha": "", "setup_mb": 0.0}
    if not path:
        return data
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2 and parts[1].endswith("_Portable.zip"):
                data["sha"] = parts[0]
            if len(parts) == 2 and parts[1].endswith("_Trial_Setup.exe"):
                data["setup_sha"] = parts[0]
    zip_path = os.path.join(DOCS, "downloads", "MBFUTool_2.0_Trial_Portable.zip")
    if os.path.isfile(zip_path):
        data["mb"] = os.path.getsize(zip_path) / 1024 / 1024
    setup_path = os.path.join(DOCS, "downloads", "MBFUTool_2.0_Trial_Setup.exe")
    if os.path.isfile(setup_path):
        data["setup_mb"] = os.path.getsize(setup_path) / 1024 / 1024
        if not data["setup_sha"]:
            h = hashlib.sha256()
            with open(setup_path, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            data["setup_sha"] = h.hexdigest()
    return data


def tokens(lang, sums):
    side = "ru" if lang == "ru" else "en"
    status = cfg.SELLER["status_ru"] if lang == "ru" else cfg.SELLER["status_en"]
    values = {
        "SITE": cfg.SITE,
        "BRAND": cfg.BRAND,
        "PRODUCT": cfg.PRODUCT,
        "AUTHOR": cfg.AUTHOR,
        "BUY_URL": cfg.BUY_URL,
        "BUY_LABEL": cfg.BUY_LABEL,
        "GITHUB": cfg.GITHUB,
        "RELEASES": cfg.RELEASES,
        "TRIAL_ZIP": "/" + cfg.TRIAL_ZIP,
        "TRIAL_SHA": sums["sha"] or "—",
        "TRIAL_SIZE": ("%.1f МБ" % sums["mb"]).replace(".", ",") if lang == "ru" else ("%.1f MB" % sums["mb"]),
        "SETUP_SIZE": ("%.1f МБ" % sums["setup_mb"]).replace(".", ",") if lang == "ru" else ("%.1f MB" % sums["setup_mb"]),
        "SETUP_SHA": sums["setup_sha"] or "—",
        "TRIAL_DAYS": str(cfg.TRIAL_DAYS),
        "VERSION": cfg.LATEST_VERSION,
        "EMAIL": cfg.SELLER["email"],
        "EMAIL_LEGAL": cfg.SELLER["email_legal"],
        "SELLER_NAME": cfg.SELLER["name"],
        "SELLER_STATUS": status,
        "SELLER_INN": cfg.SELLER["inn"],
        "SELLER_ADDRESS": cfg.seller_address(lang),
        "YEAR": cfg.COPYRIGHT,
        "LANG": side,
    }
    return values


TOKEN_RE = re.compile(r"\{\{([A-Z_]+)\}\}")


def render_body(text, values):
    def repl(match):
        key = match.group(1)
        if key not in values:
            raise SystemExit("unknown token {{%s}}" % key)
        return values[key]
    return TOKEN_RE.sub(repl, text)


def jsonld_for(kind, lang, slug, title, desc):
    if kind == "software":
        name = "MBFUTool 2.0" if lang == "ru" else "MBFUTool 2.0"
        data = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": name,
            "applicationCategory": "UtilitiesApplication",
            "operatingSystem": "Windows 10, Windows 11 (x64)",
            "softwareVersion": "2.0.0",
            "inLanguage": ["ru", "en"],
            "description": desc,
            "url": layout.url_for(lang, slug),
            "downloadUrl": cfg.SITE + "/" + cfg.TRIAL_ZIP,
            "author": {"@type": "Person", "name": cfg.AUTHOR},
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": ("Пробная версия (Trial): 30 дней, все функции. "
                                "Полная версия — на Boosty." if lang == "ru" else
                                "Trial: 30 days, all features. Full version on Boosty."),
                "url": cfg.BUY_URL,
            },
        }
        return data
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "inLanguage": "ru" if lang == "ru" else "en",
        "url": layout.url_for(lang, slug),
        "isPartOf": {"@type": "WebSite", "name": cfg.BRAND, "url": cfg.SITE},
    }


def build_page(lang, slug, sums):
    src = os.path.join(CONTENT, lang, slug + ".html")
    if not os.path.isfile(src):
        return False
    with open(src, encoding="utf-8") as f:
        body = render_body(f.read(), tokens(lang, sums))
    ru_title, ru_desc, en_title, en_desc, kind = PAGES[slug]
    title, desc = (ru_title, ru_desc) if lang == "ru" else (en_title, en_desc)
    html = (layout.head(lang, slug, title, desc,
                        jsonld=jsonld_for(kind, lang, slug, title, desc))
            + body
            + layout.footer(lang, slug))
    out_dir = DOCS if lang == "ru" else os.path.join(DOCS, "en")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, slug + ".html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def write_404():
    """404 page reuses the shared shell with a short body."""
    for lang, slug in (("ru", "404"), ("en", "404")):
        title = ("Страница не найдена — ms-dos.su" if lang == "ru"
                 else "Page not found — ms-dos.su")
        desc = ("Такой страницы нет. Начните с главной или базы знаний."
                if lang == "ru" else
                "This page does not exist. Start from the home page or the guides.")
        body = """
<section class="block"><div class="wrap">
  <h2>404</h2>
  <p class="intro">{msg}</p>
  <p><a class="btn" href="{home}">{home_label}</a>
     <a class="btn ghost" href="{docs}">{docs_label}</a></p>
</div></section>
""".format(msg="Такой страницы нет. Возможно, она переехала." if lang == "ru"
           else "This page does not exist. It may have moved.",
           home="/en/" if lang == "en" else "/",
           home_label="На главную" if lang == "ru" else "Home",
           docs="/en/stati.html" if lang == "en" else "/stati.html",
           docs_label="База знаний" if lang == "ru" else "Guides")
        html = (layout.head(lang, "404" if lang == "ru" else "404", title, desc,
                            has_en=True)
                + body + layout.footer(lang, "index"))
        path = (os.path.join(DOCS, "404.html") if lang == "ru"
                else os.path.join(DOCS, "en", "404.html"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)


def main():
    sums = load_sums()
    built = []
    for slug in PAGES:
        for lang in ("ru", "en"):
            if build_page(lang, slug, sums):
                built.append(lang + "/" + slug)
    write_404()
    print("built %d pages" % len(built))
    missing = []
    for slug in PAGES:
        for lang in ("ru", "en"):
            if lang + "/" + slug not in built:
                missing.append("content/%s/%s.html" % (lang, slug))
    if missing:
        print("missing content:" if not missing else "MISSING:")
        for m in missing:
            print("  " + m)
    blockers = cfg.blockers()
    if blockers:
        print("\nBLOCKERS before publishing (fill tools/site_config.py):")
        for b in blockers:
            print("  - " + b)


if __name__ == "__main__":
    main()