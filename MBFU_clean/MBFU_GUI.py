# -*- coding: utf-8 -*-
"""MBFU GUI 1.1.0 — графический интерфейс создания загрузочных флешек MS-DOS.

Только стандартная библиотека (tkinter) — без зависимостей, чтобы не
триггерить антивирусы лишними DLL/упаковщиками.
Бэкенд: MSDOSBOOT.bat + MSDOSBOOT.exe (RMPARTUSB) + DOSBox.
Без принятия LICENSE-MS-DOS-RU.txt создание флешки заблокировано.
"""
import ctypes
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

APP_VERSION = "1.3.0"
LICENSE_FILE = "LICENSE-MS-DOS-RU.txt"
# Метка версии — строго ASCII: файл принятия пишет и Inno-установщик
# (SaveStringToFile сохраняет в ANSI системной кодовой страницы),
# кириллица там превращается в крякозябры и проверка вечно False.
LICENSE_VERSION = "1.0-2026-09-22"
NC_LICENSE_FILE = "LICENSE-NC-RU.txt"
NC_LICENSE_VERSION = "1.0-2026-09-22"
MS_ACCEPT_NAME = "license_accepted.json"
NC_ACCEPT_NAME = "nc_license_accepted.json"

if getattr(sys, "frozen", False):
    # автономный EXE (PyInstaller onefile): файлы лежат рядом с EXE
    APP_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_BAT = os.path.join(APP_DIR, "MSDOSBOOT.bat")


def _store_dirs():
    """Папки хранения факта принятия: личная + общая.

    Общая (%ProgramData%) нужна, чтобы принятие лицензии на экране
    установщика (Inno, LicenseFile) подхватывалось программой:
    установщик работает с правами админа и пишет именно туда.
    """
    dirs = []
    try:
        d = os.path.join(os.environ.get("APPDATA") or os.path.expanduser("~"), "MBFU")
        os.makedirs(d, exist_ok=True)
        dirs.append(d)
    except OSError:
        pass
    try:
        pd = os.environ.get("PROGRAMDATA") or r"C:\ProgramData"
        d2 = os.path.join(pd, "MBFU")
        os.makedirs(d2, exist_ok=True)
        dirs.append(d2)
    except OSError:
        pass
    return dirs


def _accepted_in(path, version):
    # Файл может быть записан GUI (UTF-8) или Inno-установщиком (ANSI),
    # поэтому перебираем кодировки вместо жесткого UTF-8.
    for enc in ("utf-8-sig", "utf-8", "cp1251", "cp866"):
        try:
            with open(path, "r", encoding=enc) as f:
                data = json.load(f)
            return data.get("license_version") == version and data.get("accepted") is True
        except (OSError, ValueError, UnicodeError):
            continue
    return False


def acceptance_files(name=MS_ACCEPT_NAME):
    return [os.path.join(d, name) for d in _store_dirs()]


def _save_acceptance(name, version):
    payload = {
        "accepted": True,
        "license_version": version,
        "app_version": APP_VERSION,
        "date": datetime.now().isoformat(timespec="seconds"),
    }
    for p in acceptance_files(name):
        try:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except OSError:
            continue


def _reset_acceptance(name):
    for p in acceptance_files(name):
        try:
            os.remove(p)
        except OSError:
            pass


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def load_acceptance():
    return any(_accepted_in(p, LICENSE_VERSION) for p in acceptance_files(MS_ACCEPT_NAME))


def save_acceptance():
    _save_acceptance(MS_ACCEPT_NAME, LICENSE_VERSION)


def load_nc_acceptance():
    return any(_accepted_in(p, NC_LICENSE_VERSION) for p in acceptance_files(NC_ACCEPT_NAME))


def save_nc_acceptance():
    _save_acceptance(NC_ACCEPT_NAME, NC_LICENSE_VERSION)


def reset_nc_acceptance():
    _reset_acceptance(NC_ACCEPT_NAME)


def ps_json(cmd):
    """Run powershell and return parsed JSON (list-normalized).

    Русские метки томов в консоли идут в CP866, а locale Python —
    CP1251, поэтому байты декодируем вручную с перебором кодировок.
    """
    full = ["powershell", "-NoProfile", "-NonInteractive", "-Command",
            "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; " + cmd]
    # CREATE_NO_WINDOW: без этого каждый опрос дисков мигает черным окном;
    # весь вывод и так идет во встроенный журнал GUI
    out = subprocess.run(full, capture_output=True, timeout=30,
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    raw = out.stdout or b""
    txt = ""
    for enc in ("utf-8", "cp866", "cp1251"):
        try:
            txt = raw.decode(enc)
            break
        except Exception:
            continue
    txt = txt.strip()
    if not txt:
        return []
    try:
        data = json.loads(txt)
    except Exception:
        return []
    if isinstance(data, dict):
        return [data]
    return data or []


def list_usb_drives():
    """Return list of dicts: number, model, size_gb, bus, letters, label, is_system."""
    disks, parts, vols = [], [], []
    try:
        disks = ps_json(
            "Get-Disk | Select-Object Number,FriendlyName,Model,Size,BusType,MediaType,"
            "PartitionStyle,IsSystem,IsBoot | ConvertTo-Json -Compress")
        parts = ps_json(
            "Get-Partition | Select-Object DiskNumber,DriveLetter,Size,Type | ConvertTo-Json -Compress")
        vols = ps_json(
            "Get-Volume | Select-Object DriveLetter,FileSystemLabel,FileSystem,DriveType | ConvertTo-Json -Compress")
    except Exception:
        pass
    vol_by_letter = {}
    for v in vols:
        dl = str(v.get("DriveLetter") or "").upper()
        if dl:
            vol_by_letter[dl] = v
    parts_by_disk = {}
    for p in parts:
        try:
            dn = int(p.get("DiskNumber"))
        except (TypeError, ValueError):
            continue
        dl = str(p.get("DriveLetter") or "").upper()
        if dl:
            parts_by_disk.setdefault(dn, []).append(dl)
    result = []
    for d in disks:
        try:
            num = int(d.get("Number"))
        except (TypeError, ValueError):
            continue
        size = d.get("Size") or 0
        try:
            size_gb = round(float(size) / (1024 ** 3), 1)
        except Exception:
            size_gb = 0
        letters = parts_by_disk.get(num, [])
        labels = []
        for l in letters:
            v = vol_by_letter.get(l, {})
            if v.get("FileSystemLabel"):
                labels.append(str(v["FileSystemLabel"]))
        result.append({
            "number": num,
            "model": str(d.get("FriendlyName") or d.get("Model") or "Диск %d" % num),
            "size_gb": size_gb,
            "bus": str(d.get("BusType") or d.get("MediaType") or ""),
            "letters": letters,
            "labels": labels,
            "is_system": bool(d.get("IsSystem") or d.get("IsBoot")),
            "style": str(d.get("PartitionStyle") or ""),
        })
    # Fallback: если Get-Disk пуст (старая ОС) — хотя бы буквы через Win32_LogicalDisk
    if not result:
        try:
            lds = ps_json(
                "Get-CimInstance Win32_LogicalDisk | Select-Object DeviceID,VolumeName,Size,DriveType | ConvertTo-Json -Compress")
            for ld in lds:
                dev = str(ld.get("DeviceID") or "").upper().rstrip(":")
                if not dev:
                    continue
                try:
                    sz = round(float(ld.get("Size") or 0) / (1024 ** 3), 1)
                except Exception:
                    sz = 0
                result.append({"number": -1, "model": "Том %s:" % dev,
                               "size_gb": sz, "bus": "", "letters": [dev],
                               "labels": [str(ld.get("VolumeName") or "")],
                               "is_system": dev == "C", "style": ""})
        except Exception:
            pass
    return sorted(result, key=lambda r: r["number"])


# Коды возврата RMPARTUSB (из встроенной справки /?):
# 0 OK, 1 плохие параметры, 2 отмена пользователем, 3 не найден,
# 4 не USB-устройство, 5 неизвестно, 6 ошибка диска/операции, 7 ошибка записи.
RMPARTUSB_ERRORS = {
    1: 'Плохие параметры бэкенда.',
    2: 'Операция отменена.',
    3: 'Диск не найден.',
    4: 'Это не USB-устройство.',
    6: 'Ошибка диска или операции.',
    7: 'Ошибка записи на диск.',
}


def decide_size_param(size_gb):
    """Больше 4 ГБ — режем раздел SIZE=4000 (МБ), иначе штатно целиком."""
    try:
        big = float(size_gb) > 4.0
    except (TypeError, ValueError):
        big = False
    return 'SIZE=4000' if big else ''


# Соответствие "сырой вывод бэкенда" -> понятная ошибка.
# Порядок важен: первые совпадения приоритетнее.
# Каждый элемент: (подстрока для поиска в нижнем регистре, заголовок, текст).
BACKEND_ERRORS = [
    ("cannot exceed 4gb",
     "Ошибка диска",
     "Флешка слишком большая для FAT16 (лимит — 4 ГБ), "
     "а MS-DOS загружается только с FAT16.\n\n"
     "Возьмите флешку до 4 ГБ и повторите."),
    ("refusing to write to system",
     "Ошибка диска",
     "Запись на системный диск заблокирована.\n\n"
     "Выберите USB-флешку, а не диск с Windows."),
    ("cannot map",
     "Ошибка диска",
     "Не удалось сопоставить букву флешки с физическим диском.\n\n"
     "Проверьте, что флешка вставлена и видна в проводнике, "
     "затем нажмите «Обновить диски»."),
    ("disk write test failed",
     "Ошибка диска",
     "Тест записи на флешку не прошел.\n\n"
     "Возможно, флешка неисправна, защищена от записи "
     "или буква указана неверно."),
    ("cannot write to",
     "Ошибка диска",
     "Нет доступа на запись к выбранной букве.\n\n"
     "Проверьте букву флешки и запуск от имени администратора."),
    ("write protect",
     "Ошибка диска",
     "Флешка защищена от записи (переключатель Lock или сбой).\n\n"
     "Снимите защиту и повторите."),
    ("access is denied",
     "Ошибка диска",
     "Доступ запрещен: диск занят другой программой или нет прав.\n\n"
     "Закройте проводник/антивирус, проверьте запуск от администратора."),
    ("device is not ready",
     "Ошибка диска",
     "Устройство не готово.\n\n"
     "Выньте и вставьте флешку, дождитесь ее появления в проводнике."),
    ("msdosboot.exe failed",
     "Ошибка диска",
     "Не удалось разметить диск и записать MBR (бэкенд RMPARTUSB).\n\n"
     "Чаще всего: флешка больше 4 ГБ (нужна до 4 ГБ), неисправна "
     "или защищена от записи. Подробности — в журнале выше."),
    ("dosbox file-copy stage failed",
     "Ошибка копирования",
     "Разметка прошла, но не скопировались файлы MS-DOS.\n\n"
     "Проверьте папку DOS рядом с программой и повторите."),
]


def explain_backend_error(code, output):
    """Подобрать понятное объяснение по коду возврата и выводу бэкенда."""
    low = output.lower()
    for needle, title, text in BACKEND_ERRORS:
        if needle in low:
            return title, text
    if code in RMPARTUSB_ERRORS:
        return ('Ошибка диска',
                '%s\n\nПодробности — в журнале выше.' % RMPARTUSB_ERRORS[code])
    return ("Ошибка",
            "Создание флешки не удалось (код %d).\n\n"
            "Смотрите журнал выше — там строка с причиной." % code)


class LicenseDialog(tk.Toplevel):
    """Модальное принятие лицензии.

    title  — заголовок окна; license_text — текст документа;
    checks — список текстов чекбоксов (все обязательны);
    on_accept — callback, сохраняющий факт принятия.
    """
    def __init__(self, parent, title, license_text, checks, on_accept,
                 decline="Отклонить и выйти"):
        super().__init__(parent)
        self.title(title)
        self.geometry("640x560")
        self.resizable(True, True)
        self.result = False
        self._on_accept = on_accept
        self.transient(parent)
        self.grab_set()

        ttk.Label(self, text="Перед использованием необходимо принять условия.",
                  font=("", 10, "bold")).pack(padx=12, pady=(10, 4), anchor="w")
        txt = tk.Text(self, wrap="word", height=22)
        txt.pack(fill="both", expand=True, padx=12, pady=4)
        txt.insert("1.0", license_text)
        txt.config(state="disabled")
        sb = ttk.Scrollbar(self, command=txt.yview)
        txt.config(yscrollcommand=sb.set)

        self._vars = []
        for c in checks:
            v = tk.BooleanVar(value=False)
            v.trace_add("write", self._upd)
            self._vars.append(v)
            ttk.Checkbutton(self, variable=v, wraplength=600,
                            text=c).pack(padx=12, pady=2, anchor="w")

        btns = ttk.Frame(self)
        btns.pack(fill="x", padx=12, pady=10)
        self.btn_ok = ttk.Button(btns, text="Принимаю", command=self._ok, state="disabled")
        self.btn_ok.pack(side="right", padx=4)
        ttk.Button(btns, text=decline, command=self._cancel).pack(side="right", padx=4)
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _upd(self, *a):
        self.btn_ok.config(state="normal" if all(v.get() for v in self._vars) else "disabled")

    def _ok(self):
        self.result = True
        try:
            self._on_accept()
        except OSError:
            pass
        self.destroy()

    def _cancel(self):
        self.result = False
        self.destroy()


MS_CHECKS = [
    "Я подтверждаю: MS-DOS принадлежит Microsoft, "
    "у меня есть законное право его использовать, "
    "претензии — только ко мне.",
    "Я понимаю: ВСЕ данные на выбранной флешке будут "
    "УНИЧТОЖЕНЫ (форматирование + MBR).",
]
NC_CHECKS = [
    "Я подтверждаю: Norton Commander — чужая собственность, "
    "у меня есть законное право его использовать, "
    "претензии — только ко мне.",
]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MBFU %s — загрузочная флешка MS-DOS" % APP_VERSION)
        self.geometry("760x680")
        # Иконка окна и панели задач (у EXE-файла своя, вшита при сборке)
        try:
            self.iconbitmap(os.path.join(APP_DIR, "MBFU.ico"))
        except Exception:
            pass
        self.drives = []
        self.selected = None  # dict
        self.proc = None
        self.msg_q = queue.Queue()

        # --- верх: статус ---
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=6)
        self.lbl_admin = ttk.Label(top, text="")
        self.lbl_admin.pack(side="left")
        self.lbl_license = ttk.Label(top, text="")
        self.lbl_license.pack(side="right")
        self._refresh_status()

        # --- лицензия ---
        lic = ttk.Frame(self)
        lic.pack(fill="x", padx=10, pady=2)
        ttk.Button(lic, text="Лицензия MS-DOS",
                   command=self.show_license).pack(side="left")
        ttk.Button(lic, text="Лицензия Norton Commander",
                   command=self.show_nc_license).pack(side="left", padx=6)
        ttk.Button(lic, text="Сбросить принятия",
                   command=self.reset_license).pack(side="left")

        # --- диски ---
        ttk.Label(self, text="1. Выберите USB-накопитель:",
                  font=("", 10, "bold")).pack(padx=10, pady=(6, 0), anchor="w")
        df = ttk.Frame(self)
        df.pack(fill="both", expand=False, padx=10, pady=4)
        cols = ("num", "letters", "model", "size", "bus", "sys")
        self.tree = ttk.Treeview(df, columns=cols, show="headings", height=6)
        for c, t, w in [("num", "Диск", 60), ("letters", "Буквы", 90),
                        ("model", "Модель", 280), ("size", "ГБ", 70),
                        ("bus", "Шина", 90), ("sys", "Сист.", 60)]:
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="center" if c != "model" else "w")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        ttk.Button(df, text="Обновить\nдиски", command=self.refresh_drives).pack(side="right", padx=6)

        # --- параметры ---
        ttk.Label(self, text="2. Параметры установки:",
                  font=("", 10, "bold")).pack(padx=10, pady=(6, 0), anchor="w")
        pf = ttk.LabelFrame(self, text="MS-DOS и опции")
        pf.pack(fill="x", padx=10, pady=4)
        self.var_ver = tk.StringVar(value="6.22")
        ttk.Radiobutton(pf, text="MS-DOS 6.22 (рекомендуется)", variable=self.var_ver,
                        value="6.22").grid(row=0, column=0, sticky="w", padx=8, pady=2)
        ttk.Radiobutton(pf, text="MS-DOS 5.00", variable=self.var_ver,
                        value="5.00").grid(row=0, column=1, sticky="w", padx=8, pady=2)
        self.var_nc = tk.BooleanVar(value=True)
        ttk.Checkbutton(pf, text="Norton Commander 4.0 (нужна его лицензия)",
                        variable=self.var_nc,
                        command=self.on_nc_toggle).grid(row=1, column=0, columnspan=2,
                                                        sticky="w", padx=8, pady=2)
        ttk.Label(pf, text="Метка тома:").grid(row=2, column=0, sticky="e", padx=8, pady=2)
        self.var_label = tk.StringVar(value="dos")
        ttk.Entry(pf, textvariable=self.var_label, width=14).grid(row=2, column=1, sticky="w", pady=2)
        ttk.Label(pf, text="(латиница, до 11 символов)").grid(row=2, column=2, sticky="w")

        # --- подтверждение ---
        ttk.Label(self, text="3. Подтверждение (защита от ошибки):",
                  font=("", 10, "bold")).pack(padx=10, pady=(6, 0), anchor="w")
        cf = ttk.Frame(self)
        cf.pack(fill="x", padx=10, pady=4)
        ttk.Label(cf, text="Введите букву выбранной флешки (напр. E:):").pack(side="left")
        self.var_confirm = tk.StringVar()
        self.ent_confirm = ttk.Entry(cf, textvariable=self.var_confirm, width=8)
        self.ent_confirm.pack(side="left", padx=6)
        self.var_confirm.trace_add("write", lambda *a: self._update_run())
        self.var_dataloss = tk.BooleanVar(value=False)
        ttk.Checkbutton(cf, text="Данные будут уничтожены — подтверждаю",
                        variable=self.var_dataloss,
                        command=self._update_run).pack(side="left", padx=6)

        # --- запуск ---
        rf = ttk.Frame(self)
        rf.pack(fill="x", padx=10, pady=4)
        self.btn_run = ttk.Button(rf, text="СОЗДАТЬ загрузочную флешку",
                                  command=self.run_backend, state="disabled")
        self.btn_run.pack(side="left", padx=2)
        ttk.Button(rf, text="Только проверить флешку",
                   command=self.verify_only).pack(side="left", padx=6)
        ttk.Button(rf, text="Остановить", command=self.stop_backend).pack(side="right")

        # --- лог ---
        ttk.Label(self, text="Журнал:", font=("", 10, "bold")).pack(padx=10, anchor="w")
        self.log = tk.Text(self, wrap="word", height=12, state="disabled")
        self.log.pack(fill="both", expand=True, padx=10, pady=4)
        self.after(150, self._pump_log)

        self.refresh_drives()
        if not load_acceptance():
            self.after(300, self.ask_license_first)
        self._update_run()

    # ----- helpers -----
    def _refresh_status(self):
        admin = is_admin()
        self.lbl_admin.config(
            text=("Права: АДМИНИСТРАТОР ✓" if admin else "Права: НЕТ админа! Запустите от имени администратора"),
            foreground=("green" if admin else "red"))
        ms, nc = load_acceptance(), load_nc_acceptance()
        self.lbl_license.config(
            text=("MS-DOS ✓  |  NC ✓" if (ms and nc) else
                  "MS-DOS ✓  |  NC: не принят" if ms else
                  "MS-DOS: НЕ принят  |  NC ✓" if nc else
                  "Лицензии: НЕ приняты!"),
            foreground=("green" if ms else "red"))

    def log_line(self, s):
        self.log.config(state="normal")
        self.log.insert("end", "[%s] %s\n" % (datetime.now().strftime("%H:%M:%S"), s))
        self.log.see("end")
        self.log.config(state="disabled")

    def _pump_log(self):
        try:
            while True:
                self.msg_q.get_nowait()
                # сообщения уже залогированы отправителем; просто обновляем кнопки
                self._update_run()
        except queue.Empty:
            pass
        self.after(150, self._pump_log)

    def _read_doc(self, name):
        p = os.path.join(APP_DIR, name)
        try:
            with open(p, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return "Не найден %s: %s" % (name, e)

    def license_text(self):
        return self._read_doc(LICENSE_FILE)

    def nc_license_text(self):
        return self._read_doc(NC_LICENSE_FILE)

    def ask_license_first(self):
        d = LicenseDialog(self, "Лицензия MS-DOS — обязательное принятие",
                          self.license_text(), MS_CHECKS, save_acceptance)
        self.wait_window(d)
        if d.result or load_acceptance():
            # MS-DOS принята — если выбран NC, сразу предлагаем и его лицензию
            if self.var_nc.get() and not load_nc_acceptance():
                if not self.show_nc_license():
                    self.var_nc.set(False)
        self._refresh_status()
        self._update_run()
        if not load_acceptance():
            messagebox.showwarning(
                "Без лицензии — никак",
                "Вы не приняли лицензию MS-DOS. Создание флешки заблокировано.\n"
                "Можно только смотреть список дисков.")
            self.log_line("Лицензия MS-DOS отклонена — действия заблокированы.")

    def show_license(self):
        d = LicenseDialog(self, "Лицензия MS-DOS",
                          self.license_text(), MS_CHECKS, save_acceptance,
                          decline="Закрыть")
        self.wait_window(d)
        self._refresh_status()
        self._update_run()

    def show_nc_license(self):
        d = LicenseDialog(self, "Лицензия Norton Commander",
                          self.nc_license_text(), NC_CHECKS, save_nc_acceptance,
                          decline="Закрыть")
        self.wait_window(d)
        self._refresh_status()
        self._update_run()
        return d.result or load_nc_acceptance()

    def on_nc_toggle(self):
        # галочку NC можно оставить только с принятой NC-лицензией
        if self.var_nc.get() and not load_nc_acceptance():
            if not self.show_nc_license():
                self.var_nc.set(False)
                self.log_line("NC-лицензия не принята — Norton Commander отключен.")
            else:
                self.log_line("NC-лицензия принята.")
        self._update_run()

    def reset_license(self):
        _reset_acceptance(MS_ACCEPT_NAME)
        _reset_acceptance(NC_ACCEPT_NAME)
        if self.var_nc.get():
            self.var_nc.set(False)
        self._refresh_status()
        self._update_run()
        self.log_line("Принятия лицензий сброшены.")

    # ----- drives -----
    def refresh_drives(self):
        self.log_line("Опрос дисков через PowerShell (Get-Disk)...")
        try:
            self.drives = list_usb_drives()
        except Exception as e:
            messagebox.showerror("Ошибка опроса дисков", str(e))
            self.drives = []
        for i in self.tree.get_children():
            self.tree.delete(i)
        for d in self.drives:
            letters = " ".join(l + ":" for l in d["letters"]) or "—"
            sys_mark = "ДА!" if d["is_system"] else ""
            self.tree.insert("", "end", iid=str(d["number"]), values=(
                "Disk %d" % d["number"] if d["number"] >= 0 else "?",
                letters, d["model"], d["size_gb"], d["bus"], sys_mark))
        self.log_line("Найдено дисков/томов: %d" % len(self.drives))
        self.selected = None
        self._update_run()

    def on_select(self, *a):
        sel = self.tree.selection()
        if not sel:
            self.selected = None
        else:
            try:
                num = int(sel[0])
            except ValueError:
                num = -1
            self.selected = next((d for d in self.drives if d["number"] == num), None)
        if self.selected:
            ls = ", ".join(l + ":" for l in self.selected["letters"]) or "(без буквы)"
            self.log_line("Выбран: Disk %s [%s] %s" % (self.selected["number"], ls, self.selected["model"]))
        self._update_run()

    def target_letter(self):
        if not self.selected or not self.selected["letters"]:
            return ""
        # если у диска несколько букв — берем первую, остальные покажем в предупреждении
        return (self.selected["letters"][0] + ":").upper()

    def _update_run(self):
        ok = True
        reason = ""
        if not load_acceptance():
            ok, reason = False, "примите лицензию MS-DOS"
        elif self.var_nc.get() and not load_nc_acceptance():
            ok, reason = False, "примите лицензию NC"
        elif not self.selected:
            ok, reason = False, "выберите диск"
        elif self.selected.get("is_system"):
            ok, reason = False, "это системный диск!"
        elif not self.selected.get("letters"):
            ok, reason = False, "у диска нет буквы тома"
        elif self.var_confirm.get().strip().upper() != self.target_letter().upper():
            ok, reason = False, "введите букву %s" % (self.target_letter() or "флешки")
        elif not self.var_dataloss.get():
            ok, reason = False, "подтвердите уничтожение данных"
        elif self.proc and self.proc.poll() is None:
            ok, reason = False, "процесс уже идет"
        self.btn_run.config(state="normal" if ok else "disabled")
        if reason:
            self.btn_run.config(text="СОЗДАТЬ загрузочную флешку (%s)" % reason)
        else:
            self.btn_run.config(text="СОЗДАТЬ загрузочную флешку")

    # ----- backend -----
    def run_backend(self):
        if not os.path.isfile(BACKEND_BAT):
            messagebox.showerror("Нет бэкенда", "Не найден MSDOSBOOT.bat рядом с GUI.")
            return
        letter = self.target_letter()
        mode = "/MSD6" if self.var_ver.get() == "6.22" else "/MSD5"
        label = "".join(c for c in self.var_label.get().strip() if c.isalnum())[:11] or "dos"
        if len(self.selected["letters"]) > 1:
            if not messagebox.askyesno(
                    "Несколько разделов",
                    "На диске несколько томов: %s.\nПродолжить с %s?" % (
                        ", ".join(l + ":" for l in self.selected["letters"]), letter)):
                return
        if not messagebox.askyesno(
                "Последнее предупреждение",
                "Сейчас будет ОТФОРМАТИРОВАН диск %s (%s, %s ГБ)!\n"
                "Все данные будут УНИЧТОЖЕНЫ.\n\nПродолжить?" % (
                    letter, self.selected["model"], self.selected["size_gb"])):
            return
        ncflag = "1" if self.var_nc.get() else "0"
        nc_txt = " + Norton Commander" if self.var_nc.get() else " (без Norton Commander)"
        self.log_line("Старт: %s %s %s, метка=%s%s" % (BACKEND_BAT, mode, letter, label, nc_txt))
        self.log_line("ВАЖНО: не вынимайте флешку до надписи Done.")
        t = threading.Thread(target=self._run_thread, args=(mode, letter, label, ncflag), daemon=True)
        t.start()

    def _run_thread(self, mode, letter, label, ncflag):
        try:
            # бэкенд принимает: MSDOSBOOT.bat /MSD6 E: [метка] [NC: 1 ставить / 0 пропустить]
            # CREATE_NO_WINDOW: весь вывод бэкенда построчно идет в журнал GUI
            self.proc = subprocess.Popen(
                ["cmd", "/c", BACKEND_BAT, mode, letter, label, ncflag],
                cwd=APP_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, errors="replace", bufsize=1,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            tail = []
            for line in self.proc.stdout:
                s = line.rstrip()
                tail.append(s)
                if len(tail) > 60:
                    del tail[0]
                self.log.config(state="normal")
                self.log.insert("end", s + "\n")
                self.log.see("end")
                self.log.config(state="disabled")
            code = self.proc.wait()
            if code == 0:
                self.log_line("Готово.")
                self.after(0, lambda: messagebox.showinfo(
                    "Готово", "Флешка %s готова (MS-DOS %s)." % (letter, self.var_ver.get())))
            else:
                title, text = explain_backend_error(code, "\n".join(tail))
                self.log_line("%s: %s" % (title, text.split("\n\n")[0]))
                self.after(0, lambda t=title, x=text: messagebox.showerror(t, x))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Ошибка запуска", str(e)))
        finally:
            self.proc = None
            self.msg_q.put("done")

    def verify_only(self):
        letter = self.target_letter()
        if not letter:
            messagebox.showinfo("Проверка", "Сначала выберите диск с буквой.")
            return
        test = os.path.join(letter + "\\", "tdd_gui_test.txt")
        try:
            with open(test, "w") as f:
                f.write("Test GUI %s" % datetime.now().isoformat())
            with open(test) as f:
                ok = "Test" in f.read()
            os.remove(test)
            msg = "Флешка %s доступна для записи ✓" % letter if ok else "Запись есть, чтение не сошлось!"
            (messagebox.showinfo if ok else messagebox.showerror)("Проверка", msg)
            self.log_line(msg)
        except Exception as e:
            messagebox.showerror("Проверка", "Нет доступа к %s: %s" % (letter, e))
            self.log_line("Проверка %s failed: %s" % (letter, e))

    def stop_backend(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            self.log_line("Остановка запрошена (terminate).")
        else:
            self.log_line("Активного процесса нет.")


# ==================== SETUP-режим (--setup) ====================
# Маленькое окно -> сканирование -> скрытый хелпер + весь интерфейс в DOSBox.
# Связь с DOS-сессией — через файлы DOS\IPC\: хелпер пишет DRIVES/STATUS/OK/ERR,
# DOS-меню (SETUP.BAT) пишет REQUEST. Ожидания в DOS — циклами SLEEP (свой SLEEP.COM,
# т.к. CHOICE /T в DOSBox не работает).

IPC_DIRNAME = "IPC"
SETUP_BAT = "SETUP.BAT"


def ipc_sanitize(s):
    """ASCII для DOS-экрана: без кириллицы и мусора."""
    return ''.join(c if 32 <= ord(c) < 127 else '?' for c in str(s))[:40]


def build_drives_txt(drives):
    """drives: список list_usb_drives() -> (текст DRIVES.TXT, {idx: строка}, empty).
    Только флешки С БУКВАМИ, максимум 4: строго 1:1 с файлами D1-D4.TXT,
    по которым DOS-меню предлагает выбор."""
    usb = [d for d in drives
           if (d.get('bus') or '').upper() == 'USB' and d.get('letters')][:4]
    lines = []
    per = {}
    for i, d in enumerate(usb, 1):
        letters = ','.join(l + ':' for l in d['letters'])
        label = ipc_sanitize((d.get('labels') or [''])[0])
        model = ipc_sanitize(d.get('model', ''))
        line = '%d. %s %s %sGB %s' % (i, letters, label, d.get('size_gb', '?'), model)
        lines.append(line.strip())
        per[i] = line.strip()
    return '\n'.join(lines) + ('\n' if lines else ''), per, (len(usb) == 0)


def parse_request(text):
    parts = (text or '').strip().split()
    if not parts:
        return '', ''
    cmd = parts[0].upper()
    return cmd, (parts[1] if len(parts) > 1 else '')


def setup_map_letter(letter, ipc_dir):
    """Буква тома -> номер PHYSICALDRIVE через Get-UsbDrive.ps1. Только чтение."""
    ps1 = os.path.join(APP_DIR, 'Get-UsbDrive.ps1')
    tmp = os.path.join(ipc_dir, 'tmpmap.txt')
    want = (letter or '').strip().upper().rstrip(':')
    for n in range(1, 31):
        try:
            subprocess.run(
                ['powershell', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
                 '-File', ps1, '-DiskNumber', str(n), '-OutFile', tmp],
                capture_output=True, timeout=30,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            if os.path.isfile(tmp):
                with open(tmp, encoding='utf-8', errors='replace') as f:
                    got = f.read().upper()
                if want and want in re.split(r'[^A-Z]+', got):
                    return n
        except Exception:
            continue
    return 0


def setup_format(letter, size_gb=0):
    """Форматирование для SETUP-режима. Возвращает (ok, текст, номер_диска).
    Диски больше 4 ГБ режутся ключом SIZE=4000 (см. RMPARTUSB /?)."""
    exe = os.path.join(APP_DIR, 'MSDOSBOOT.exe')
    if not os.path.isfile(exe):
        return False, 'Нет MSDOSBOOT.exe рядом с программой.', 0
    n = setup_map_letter(letter, os.path.join(APP_DIR, IPC_DIRNAME))
    if not n:
        return False, 'Не сопоставлена буква %s с физическим диском.' % letter, 0
    args = [exe, 'DRIVE=%d' % n, 'MSDOS', 'CHS']
    sizep = decide_size_param(size_gb)
    if sizep:
        args.append(sizep)
    args += ['VOLUME', 'dos']  # VOLUME обязано быть последним
    try:
        p = subprocess.run(
            args, cwd=APP_DIR, capture_output=True, text=True, errors='replace',
            timeout=600,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        out = (p.stdout or '') + '\n' + (p.stderr or '')
        if p.returncode == 0:
            return True, '', n
        title, text = explain_backend_error(p.returncode, out)
        return False, '%s: %s' % (title, text.split('\n\n')[0]), n
    except Exception as e:
        return False, 'Не запустился бэкенд: %s' % e, n


def setup_disk_letter(n):
    """Буква первого тома диска N (после переразметки буква могла смениться)."""
    try:
        out = subprocess.run(
            ['powershell', '-NoProfile', '-NonInteractive', '-Command',
             "(@(Get-Partition -DiskNumber %d | Where-Object {$_.DriveLetter}) | "
             "Select-Object -First 1).DriveLetter" % n],
            capture_output=True, text=True, timeout=30,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        letter = (out.stdout or '').strip().upper()
        if len(letter) == 1 and letter != 'C':
            return letter + ':'
    except Exception:
        pass
    return ''


def _ipc_wipe(ipc):
    """Чистит все IPC-файлы, включая USE_<буква>.TXT."""
    names = ['REQUEST.TXT', 'OK.TXT', 'ERR.TXT', 'STATUS.TXT', 'DRIVES.TXT',
             'EMPTY.TXT', 'tmpmap.txt', 'D1.TXT', 'D2.TXT', 'D3.TXT', 'D4.TXT']
    names += ['USE_%s.TXT' % c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    for f in names:
        try:
            os.remove(os.path.join(ipc, f))
        except OSError:
            pass


def supervise_decision(back, cmd, fmt_started, fmt_done):
    """Чистое решение supervisor по состоянию маркеров.
    Возвращает: 'stage1' | 'stage2' | 'bye'.
    Воркер формата нельзя бросать на полпути: если он стартовал —
    всегда дожимаем до конца и идем в STAGE2."""
    if back:
        return 'stage1'
    if cmd == 'QUIT':
        return 'bye'
    if cmd == 'SCAN':
        return 'stage1'
    if cmd == 'FORMAT' or fmt_started or fmt_done:
        return 'stage2'
    return 'bye'


def _trace(ipc, msg):
    import datetime as _dt
    try:
        with open(os.path.join(ipc, 'TRACE.LOG'), 'a', encoding='utf-8') as _f:
            _f.write('%s %s\n' % (_dt.datetime.now().strftime('%H:%M:%S'), msg))
    except OSError:
        pass


def run_setup():
    ipc = os.path.join(APP_DIR, IPC_DIRNAME)
    os.makedirs(ipc, exist_ok=True)
    _ipc_wipe(ipc)
    _trace(ipc, 'start')

    dosbox = os.path.join(APP_DIR, 'dosbox.exe')
    if not os.path.isfile(dosbox):
        messagebox.showerror('MS-DOS SETUP FOR USB SEMENTSUL MAXIM 2026', 'Не найден dosbox.exe рядом с программой.')
        return

    root = tk.Tk()
    root.title('MS-DOS SETUP FOR USB SEMENTSUL MAXIM 2026')
    root.geometry('340x150')
    root.resizable(False, False)
    status = tk.StringVar(value='Сканирование дисков…')
    ttk.Label(root, textvariable=status, wraplength=320).pack(padx=12, pady=10)
    bar = ttk.Progressbar(root, mode='indeterminate')
    bar.pack(fill='x', padx=12)
    bar.start(20)
    cancelled = {'v': False}

    def cancel():
        cancelled['v'] = True
        q.put(('status', 'Отмена… ждем фоновые операции.'))
        if fmt['started'] and not fmt['done']:
            q.put(('status', 'Идет форматирование — дождитесь окончания.'))
            t = 0
            while not fmt['done'] and t < 900:
                time.sleep(1)
                t += 1
        try:
            p = proc['p']
            if p is not None and p.poll() is None:
                p.terminate()
        except Exception:
            pass
        try:
            root.destroy()
        except Exception:
            pass

    ttk.Button(root, text='Отмена', command=cancel).pack(pady=8)

    def write_scan():
        try:
            drives = list_usb_drives()
        except Exception:
            drives = []
        # скрытые системные не предлагаем, но и не прячем C: от проверки формата
        txt, per, empty = build_drives_txt(drives)
        with open(os.path.join(ipc, 'DRIVES.TXT'), 'w', encoding='ascii') as f:
            f.write(txt)
        for i in range(1, 5):
            p = os.path.join(ipc, 'D%d.TXT' % i)
            try:
                os.remove(p)
            except OSError:
                pass
            if i in per:
                with open(p, 'w', encoding='ascii') as f:
                    f.write(per[i] + '\n')
        if empty:
            open(os.path.join(ipc, 'EMPTY.TXT'), 'w').close()
        else:
            try:
                os.remove(os.path.join(ipc, 'EMPTY.TXT'))
            except OSError:
                pass
        with open(os.path.join(ipc, 'STATUS.TXT'), 'w', encoding='ascii') as f:
            f.write('READY\n')
        return drives

    def set_status(s):
        try:
            status.set(s)
        except Exception:
            pass

    proc = {'p': None}
    fmt = {'started': False, 'done': False}
    stage = {'name': 'STAGE1.BAT'}

    def launch_stage(batname, label):
        """Запуск (перезапуск) DOSBox с нужным батом. Возвращает процесс."""
        try:
            with open(os.path.join(APP_DIR, 'cfg.conf'), encoding='utf-8', errors='replace') as f:
                conf = f.read()
        except Exception:
            conf = ''
        with open(os.path.join(APP_DIR, 'dosbox.conf'), 'w', encoding='utf-8') as f:
            f.write(conf)
            if not conf.endswith('\n'):
                f.write('\n')
            f.write('mount e "%s"\n' % ipc)
        p = subprocess.Popen(
            [dosbox, '-conf', os.path.join(APP_DIR, 'dosbox.conf'),
             os.path.join('DOS', batname)],
            cwd=APP_DIR)
        proc['p'] = p
        stage['name'] = batname
        _trace(ipc, 'dosbox launched ' + batname)
        q.put(('status', label))
        return p

    def peek_request():
        try:
            if os.path.isfile(os.path.join(ipc, 'REQUEST.TXT')):
                with open(os.path.join(ipc, 'REQUEST.TXT'), encoding='utf-8', errors='replace') as f:
                    return parse_request(f.read())
        except OSError:
            pass
        return '', ''

    def del_request():
        try:
            os.remove(os.path.join(ipc, 'REQUEST.TXT'))
        except OSError:
            pass

    def format_worker(idx):
        try:
            _do_format(idx)
        finally:
            fmt['done'] = True
            _trace(ipc, 'worker done')
            p = proc['p']  # сразу гасим DOS-сессию — дальше STAGE2 с новым кэшем
            try:
                if p is not None and p.poll() is None:
                    p.terminate()
            except Exception:
                pass

    def poll():
        """Пока DOSBox жив: ранний старт форматирования. Остальное решает supervisor."""
        while True:
            if cancelled['v']:
                break
            p = proc['p']
            if p is not None and p.poll() is not None:
                break
            try:
                cmd, arg = peek_request()
                if cmd == 'FORMAT' and not fmt['started']:
                    fmt['started'] = True
                    del_request()
                    threading.Thread(
                        target=format_worker,
                        args=(int(arg) if arg.isdigit() else 0,),
                        daemon=True).start()
            except Exception:
                pass
            time.sleep(0.5)

    def rescan_relaunch(batname, label):
        del_request()
        try:
            os.remove(os.path.join(ipc, 'BACK.TXT'))
        except OSError:
            pass
        q.put(('status', 'Сканирование дисков…'))
        write_scan()
        time.sleep(1)
        launch_stage(batname, label)

    def ensure_format(idx):
        """Дожать форматирование до конца (если воркер еще не стартовал — стартуем)."""
        if not fmt['started']:
            fmt['started'] = True
            del_request()
            threading.Thread(target=format_worker, args=(idx,),
                             daemon=True).start()
        t = 0
        while not fmt['done'] and t < 900:
            time.sleep(1)
            t += 1
        fmt['started'] = fmt['done'] = False

    def supervise():
        """Ждем закрытия DOSBox и решаем, что дальше. Цикл до cleanup."""
        while not cancelled['v']:
            p = proc['p']
            if p is None:
                break
            while p.poll() is None and not cancelled['v']:
                time.sleep(0.5)
            if cancelled['v']:
                break
            _trace(ipc, 'dosbox exited, supervise')
            back = os.path.isfile(os.path.join(ipc, 'BACK.TXT'))
            cmd, arg = peek_request()
            action = supervise_decision(back, cmd, fmt['started'], fmt['done'])
            _trace(ipc, 'decision=%s back=%s cmd=%s fmt=%s/%s' % (
                action, back, cmd, fmt['started'], fmt['done']))
            if back:
                try:
                    os.remove(os.path.join(ipc, 'BACK.TXT'))
                except OSError:
                    pass
                rescan_relaunch('STAGE1.BAT', 'DOSBox запущен. Работайте в DOS-окне.')
                continue
            if action == 'bye':
                if cmd:
                    del_request()
                _trace(ipc, 'bye')
                break
            if action == 'stage1':
                _trace(ipc, 'go STAGE1')
                rescan_relaunch('STAGE1.BAT', 'DOSBox запущен. Работайте в DOS-окне.')
                continue
            # stage2
            del_request()
            ensure_format(int(arg) if arg.isdigit() else 0)
            _trace(ipc, 'go STAGE2')
            fmt['started'] = fmt['done'] = False
            launch_stage('STAGE2.BAT', 'Этап 2: установка системы в DOS-окне.')
            continue
        try:
            root.after(0, root.destroy)
        except Exception:
            pass

    def _do_format(idx):
        # индекс -> буква из свежего скана (тот же отбор, что в DRIVES.TXT)
        try:
            drives = list_usb_drives()
        except Exception:
            drives = []
        txt, per, empty = build_drives_txt(drives)
        usb = [d for d in drives
               if (d.get('bus') or '').upper() == 'USB' and d.get('letters')][:4]
        if idx < 1 or idx > len(usb):
            write_file('ERR.TXT', 'Нет такой флешки. Обновите список (R).')
            return
        letter = (usb[idx - 1]['letters'][0] + ':').upper()
        size_gb = usb[idx - 1].get('size_gb', 0)
        if letter == 'C:':
            write_file('ERR.TXT', 'Системный диск заблокирован.')
            return
        # маркер USE_<буква> запишем после формата (буква может смениться)
        for f in ('OK.TXT', 'ERR.TXT'):
            try:
                os.remove(os.path.join(ipc, f))
            except OSError:
                pass
        write_file('STATUS.TXT', 'FORMATTING ' + letter + '\n')
        q.put(('status', 'Форматирование %s… Не вынимайте флешку.' % letter))
        _trace(ipc, 'format start ' + letter)
        ok, msg, disk_n = setup_format(letter, size_gb)
        _trace(ipc, 'format end ok=%s' % ok)
        if ok:
            # после переразметки буква могла смениться — перечитываем по номеру диска
            new_letter = setup_disk_letter(disk_n) if disk_n else ''
            if new_letter:
                letter = new_letter
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                try:
                    os.remove(os.path.join(ipc, 'USE_%s.TXT' % c))
                except OSError:
                    pass
            write_file('USE_%s.TXT' % letter[0], letter + '\n')
            _trace(ipc, 'use letter ' + letter)
        write_file('STATUS.TXT', 'READY\n')
        q.put(('status', 'DOSBox запущен. Работайте в DOS-окне.'))
        write_file('OK.TXT' if ok else 'ERR.TXT', 'OK\n' if ok else msg + '\n')

    def write_file(name, text):
        with open(os.path.join(ipc, name), 'w', encoding='utf-8', errors='replace') as f:
            f.write(text)

    q = queue.Queue()

    def pump():
        try:
            while True:
                kind, val = q.get_nowait()
                if kind == 'status':
                    set_status(val)
        except Exception:
            pass
        try:
            root.after(200, pump)
        except Exception:
            pass

    # стартовый скан + запуск DOSBox (этап 1)
    try:
        write_scan()
    except Exception as e:
        messagebox.showerror('MS-DOS SETUP FOR USB SEMENTSUL MAXIM 2026', 'Не опросить диски: %s' % e)
        root.destroy()
        return
    try:
        launch_stage('STAGE1.BAT', 'Этап 1: выбор флешки в DOS-окне.')
    except Exception as e:
        messagebox.showerror('MS-DOS SETUP FOR USB SEMENTSUL MAXIM 2026', 'Не запустился DOSBox: %s' % e)
        root.destroy()
        return
    bar.stop()
    root.withdraw()  # окно прячется — дальше только DOSBox + скрытый опрос
    threading.Thread(target=poll, daemon=True).start()
    threading.Thread(target=supervise, daemon=True).start()
    root.after(200, pump)
    root.mainloop()
    # уборка IPC
    _ipc_wipe(ipc)


if __name__ == "__main__":
    import sys as _sys
    if '--setup' in _sys.argv:
        run_setup()
    else:
        App().mainloop()
