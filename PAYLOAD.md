# Лицензионная нагрузка (в репозитории отсутствует)

Полная сборка (установщик/portable) кроме кода из репозитория требует файлы,
которые нельзя публиковать под MIT. Положите их локально — структура ниже.
Релизы на GitHub собирает мейнтейнер из этих файлов своими руками.

## Куда класть (относительно корня репозитория)

| Файл | Откуда взять |
|---|---|
| `MBFU_clean/MSDOSBOOT.exe` + `.manifest` | RMPARTUSB-бэкенд из вашей сборки |
| `MBFU_clean/dosbox.exe`, `SDL.dll`, `SDL_net.dll` | Официальный DOSBox (dosbox.com), версии должны совпадать с `cfg.conf` |
| `MBFU_clean/DOS/sourcr/MSDOS5/*` | Ваша лицензионная копия MS-DOS 5.00 |
| `MBFU_clean/DOS/sourcr/MSDOS6/*` | Ваша лицензионная копия MS-DOS 6.22 |
| `MBFU_clean/DOS/sourcr/NC/*` | Ваша лицензионная копия Norton Commander |
| `MBFU_clean/DOS/BEN*.EXE`, `BEN*.HLP`, `MDESIGN.EXE`, `!BEN*.EXE` | BEN-утилиты из вашей сборки |
| `MBFU_clean/DOS/VENDOR.TXT`, `WHATSNEW.TXT` | Документация BEN |

`MBFU_clean/dosbox.conf` и `temp.txt` создавать не нужно — генерируются при работе.

## Проверка перед релизом

1. `MBFU_clean\MBFU_GUI.exe` запускается, список дисков виден, лицензии принимаются.
2. Тест на **ненужной** флешке до 4 ГБ: `MSDOSBOOT.bat /MSD6 E:`.
3. Компиляция `MBFU.iss` в Inno Setup — без ошибок о missing Source.
4. Тег `git tag v1.x && git push origin v1.x` — CI соберет EXE и выложит Release-черновик.
