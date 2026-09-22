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
import subprocess
import sys
import threading
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


if __name__ == "__main__":
    App().mainloop()
