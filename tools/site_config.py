# -*- coding: utf-8 -*-
"""Single source of truth for the site build: seller, contacts, links, texts."""
import os

SITE = "https://ms-dos.su"
BRAND = "MBFU"
PRODUCT = "MBFUTool 2.0"
AUTHOR = "Sementsul Maxim"
COPYRIGHT = "2025–2026"
BUY_URL = "https://boosty.to/mbfu"
BUY_LABEL = "boosty.to/mbfu"
GITHUB = "https://github.com/sementsul/ms-dos"
RELEASES = GITHUB + "/releases"
TRIAL_ZIP = "downloads/MBFUTool_2.0_Trial_Setup.exe"
LATEST_VERSION = "2.0.0-trial"
TRIAL_DAYS = 30

# Analytics IDs. Both are only loaded after an explicit consent click.
GA_ID = "G-Y8PG2P181B"
METRIKA_ID = "106570050"
YANDEX_VERIFICATION = "bb775f01a3383d99"

CONSENT_VERSION = "1"

# Seller details.  Anything left as [BRACKETED] text is printed by the build
# script as a blocker and must be replaced before the site is published.
SELLER = {
    "name": "Семенцул Максим Геннадиевич",
    "name_en": "Sementsul Maxim Gennadievich",
    "status_ru": "самозанятый (налог на профессиональный доход, НПД)",
    "status_en": "self-employed individual under the Russian professional "
                 "income tax regime (NPD)",
    "inn": "381616884622",
    "ogrnip": "",  # not applicable to NPD
    "address": "",  # empty = published as "on request" (see ADDRESS_ON_REQUEST)
    "address_on_request_ru": "предоставляется по запросу на sementsul.maksim@yandex.ru",
    "address_on_request_en": "available on request at sementsul.maksim@yandex.ru",
    "country": "Российская Федерация",
    "email": "sementsul.maksim@yandex.ru",
    "email_legal": "sementsul.maksim@yandex.ru",
    "telegram": "",
}

# Placeholders that block publication.
REQUIRED_PLACEHOLDERS = ("name", "inn")


def seller_address(lang):
    """Published postal address, or the on-request wording when it is private."""
    if SELLER.get("address"):
        return SELLER["address"]
    key = "address_on_request_ru" if lang == "ru" else "address_on_request_en"
    return SELLER[key]


def seller_value(key):
    return SELLER.get(key) or ""


def blockers():
    out = []
    for key in REQUIRED_PLACEHOLDERS:
        value = seller_value(key)
        if not value or value.startswith("["):
            out.append("SELLER[" + key + "] = " + (value or "<empty>"))
    return out


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def docs_dir():
    return os.path.join(repo_root(), "docs")