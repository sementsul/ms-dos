# MBFU — загрузочная флешка MS-DOS

[![build](https://github.com/sementsul/ms-dos/actions/workflows/build.yml/badge.svg)](https://github.com/sementsul/ms-dos/actions/workflows/build.yml)
[![pages](https://github.com/sementsul/ms-dos/actions/workflows/pages.yml/badge.svg)](https://github.com/sementsul/ms-dos/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Графическая утилита для создания загрузочных USB-флешек **MS-DOS 5.00 / 6.22**.
Сайт проекта: https://ms-dos.su/

![MBFU](docs/assets/icon-64.png)

## Возможности

- Выбор USB-накопителя (модель, размер, буква) через PowerShell, без мигающих окон
- MS-DOS 6.22 / 5.00, метка тома
- Norton Commander 4.0 — опционально, галочка включена по умолчанию
- Обязательное принятие лицензий MS-DOS и Norton Commander (в установщике и в программе)
- Блокировка системного диска, тройное подтверждение перед форматированием
- Понятные ошибки вместо кодов («флешка больше 4 ГБ для FAT16» и т.д.)
- Автономный EXE: Python и установка чего-либо не нужны

## Скачать

Готовые сборки — в [Releases](https://github.com/sementsul/ms-dos/releases):
`MBFU-*-portable.zip` (распаковал и запустил) или `MBFU-*-setup.exe` (установщик Inno Setup).
Запускать от имени администратора — иначе запись MBR невозможна.

## Собрать из исходников

Нужны: Windows, Python 3.12+, [Inno Setup 6](https://jrsoftware.org/isinfo.php)
и лицензионная нагрузка из `PAYLOAD.md` (в репозитории ее нет — см. ниже).

```bat
pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --uac-admin --noupx ^
  --name MBFU_GUI --icon MBFU.ico --version-file version_info.txt ^
  --distpath MBFU_clean MBFU_clean\MBFU_GUI.py
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" MBFU.iss
```

## Важно про лицензии

- **Код MBFU** (GUI, скрипты, установщик, сайт) — [MIT](LICENSE), делайте что хотите.
- **MS-DOS 5.00/6.22** — собственность Microsoft. **Norton Commander** — собственность
  правообладателя линейки Norton. **BEN-утилиты, DOSBox, SDL, RMPARTUSB** — их авторов.
  Эти файлы в репозитории **отсутствуют сознательно**: используйте свои законные копии,
  раскладка — в [PAYLOAD.md](PAYLOAD.md). Публикация чужих файлов под MIT была бы
  нарушением — не делайте так и вы.
- Программа при первом запуске требует принять лицензии MS-DOS и NC, иначе кнопки
  заблокированы.
