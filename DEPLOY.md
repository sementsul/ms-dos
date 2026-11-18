# Публикация сайта ms-dos.su

Сайт — статические файлы в `docs/`, раздаются GitHub Pages с домена `ms-dos.su`
(файл `docs/CNAME`). Никакого серверного кода нет: только HTML, CSS, JS,
картинки и ZIP с пробной версией.

## 1. Сборка

Нужен Python 3.11+ (в этой среде — встроенный интерпретатор DSH) и файлы
пробной сборки в `../mbfu-work/trial/out/` (ZIP и `SHA256SUMS.txt`).

```powershell
cd tools
python gen_site.py      # 17 страниц × 2 языка: главная, правовые, покупка, тест DOS
python gen_seo.py       # 124 статьи, 8 EN-гайдов, каталоги /stati.html и /en/stati.html
python gen_sitemap.py   # sitemap-main.xml, sitemap-articles.xml, robots.txt
python check_site.py    # битые ссылки, JSON-LD, alt, незаменённые токены

# после публикации — сообщить поисковикам об изменениях
python tools/indexnow.py --dry    # что будет отправлено
python tools/indexnow.py          # отправка в IndexNow (Bing, Yandex, Seznam)
```

Перед сборкой положите свежий архив Trial в `docs/downloads/`:

```powershell
Copy-Item ..\mbfu-work\trial\out\MBFUTool_2.0_Trial_Portable.zip docs\downloads\ -Force
```

`gen_site.py` подставит в главную страницу SHA-256 и размер из
`mbfu-work/trial/out/SHA256SUMS.txt` и напечатает список блокеров, если не
заполнены реквизиты продавца.

## 2. Что нужно заполнить один раз

`tools/site_config.py`:

| Поле | Значение |
|---|---|
| `SELLER["name"]` | Семенцул Максим Геннадиевич |
| `SELLER["inn"]` | 381616884622 |
| `SELLER["address"]` | пусто → «предоставляется по запросу»; впишите адрес, если готовы его публиковать |
| `SELLER["email"]` | `sementsul.maksim@yandex.ru` — поддержка |
| `SELLER["email_legal"]` | `sementsul.maksim@yandex.ru` — юридические вопросы |

ФИО, ИНН и e-mail уже заполнены. Если адрес остаётся пустым, на страницах
контактов и в оферте выводится «предоставляется по запросу на e-mail»;
`seller_address()` подставляет формулировку по языку страницы.

`BUY_URL` уже указывает на <https://boosty.to/mbfu>. Если поменяется цена или
формат покупки — правьте текст в `content/*/index.html` и `terms.html`, а не
только ссылку.

## 3. Публикация

### Вариант А. Репозиторий уже клонирован

```powershell
cd C:\path\to\ms-dos
# скопируйте содержимое docs/ из этой папки поверх docs/ в репозитории
git add docs
git commit -m "site: MBFUTool 2.0 landing, 100 articles, RU/EN legal pages"
git push origin main
```

GitHub Pages обновится через 1–2 минуты. Проверьте:

- <https://ms-dos.su/> — главная;
- <https://ms-dos.su/en/> — английская версия;
- <https://ms-dos.su/sitemap.xml> — индекс карт сайта;
- <https://ms-dos.su/downloads/MBFUTool_2.0_Trial_Portable.zip> — скачивание Trial.

### Вариант Б. Пуш из другой среды

В песочнице DSH сеть до GitHub не работает: `schannel: AcquireCredentialsHandle
failed`. Пуш делайте из обычного терминала Windows или через GitHub Desktop.
Если git ругается на TLS, попробуйте OpenSSL-бэкенд:

```powershell
git -c http.sslBackend=openssl push origin main
```

Токен не храните в скриптах: используйте Git Credential Manager или
`GITHUB_TOKEN` в переменной окружения на один сеанс.

## 4. Настройки репозитория (один раз)

1. Settings → Pages → Source: `Deploy from a branch`, ветка `main`, папка `/docs`.
2. Custom domain: `ms-dos.su`, включите `Enforce HTTPS`.
3. Убедитесь, что `docs/CNAME` содержит `ms-dos.su` без пробелов и перевода строки.
4. DNS: `A` на IP GitHub Pages (185.199.108.153, .109, .110, .111) и `CNAME`
   `www` → `sementsul.github.io`.

## 5. Проверка после публикации

- [ ] `https://ms-dos.su/` открывается по HTTPS, без редиректов на `/docs/`.
- [ ] В исходном коде страницы нет `googletagmanager` и `mc.yandex` до нажатия
      «Принять аналитику» (проверяется в DevTools → Network).
- [ ] Кнопка «Только необходимые» не загружает счётчики и не ставит cookie.
- [ ] Ссылка «Настройки cookie» в футере открывает диалог, `Esc` закрывает.
- [ ] `/en/` и переключатель языка работают на всех страницах.
- [ ] ZIP скачивается, SHA-256 совпадает с указанным на главной.
- [ ] `/404.html` отдаётся для несуществующих адресов.
- [ ] В Яндекс.Вебмастере и Google Search Console добавлены `sitemap.xml`.
- [ ] Реквизиты продавца видны на `/contacts.html` и в футере.
- [ ] Открываются новые страницы: `/buy.html`, `/trial-vs-full.html`, `/verify.html`,
      `/about.html`, `/changelog.html`, `/mbfu-format.html` и их `/en/`-версии.
- [ ] `https://ms-dos.su/<ключ>.txt` отдаёт ключ IndexNow из `tools/indexnow_key.txt`.
- [ ] `https://ms-dos.su/FORMAT.md` и `sitemap-articles.xml` содержат все новые URL
      (`grep -c "<loc>" sitemap-articles.xml` = числу статей плюс EN-гайды).

## 6. Внешние материалы

Черновики публикаций (Habr, VOGONS, DOSBox forum, Reddit, zx-pk.ru,
phantom.sannata.org, AlternativeTo, Softportal, Telegram, YouTube) лежат в
`../mbfu-work/marketing/`. Ничего из этого не публикуется автоматически: нужны
аккаунты и соблюдение правил каждой площадки. Там же `README.md` со списком
ручных действий.

## 7. Обновление Trial

1. `tools/build_trial.py` — собирает onedir и ZIP, пишет `SHA256SUMS.txt`.
2. Скопируйте ZIP в `docs/downloads/`.
3. Пересоберите сайт (`gen_site.py`, `gen_seo.py`, `gen_sitemap.py`).
4. Закоммитьте `docs/` — SHA-256 на главной обновится автоматически.