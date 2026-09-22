# -*- coding: utf-8 -*-
"""Сборка демо-образа HDD «как на флешке» для dos-test.html.

Берет ЗАГРУЗОЧНЫЕ СЕКТОРЫ (MBR + VBR) с реальной флешки, созданной MBFU,
и укладывает рядом файлы DOS из sourcr/ в свежую компактную FAT16.
Сами образы НЕ коммитятся (.gitignore): секторы и файлы DOS — чужие.

Использование (от администратора, флешка уже создана через MBFU!):
  python tools/make_demo_img.py --drive E --dos DOS/sourcr/MSDOS6 --out docs/assets/demo/msdos6.img
  python tools/make_demo_img.py --drive F --dos DOS/sourcr/MSDOS5 --out docs/assets/demo/msdos5.img
--drive: буква флешки (узнаем ее PHYSICALDRIVE сами).
"""
import argparse, os, struct, sys

SECTOR = 512


def read_drive(letter):
    import subprocess
    # номер PHYSICALDRIVE по букве через CIM
    ps = ("$l='%s:'; $d=Get-CimInstance Win32_LogicalDiskToPartition | "
          "Where-Object { $_.Dependent.DeviceID -eq ($l) } | Select-Object -First 1; "
          "if (-not $d) { exit 3 }; $p=$d.Antecedent.DeviceID; "
          "$dd=Get-CimInstance Win32_DiskDriveToDiskPartition | "
          "Where-Object { $_.Dependent.DeviceID -eq $p } | Select-Object -First 1; "
          "if (-not $dd) { exit 4 }; $dd.Antecedent.DeviceID" % letter)
    out = subprocess.run(['powershell', '-NoProfile', '-NonInteractive',
                          '-Command', ps],
                         capture_output=True, timeout=60,
                         creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    dev = out.stdout.decode('utf-8', errors='replace').strip().splitlines()
    dev = dev[-1].strip() if dev else ''
    if out.returncode != 0 or not dev.startswith('\\\\.\\PHYSICALDRIVE'):
        sys.exit('Не нашел PHYSICALDRIVE для %s: (код %d)' % (letter, out.returncode))
    num = int(dev.rsplit('PHYSICALDRIVE', 1)[1])
    h = open(r'\\.\PHYSICALDRIVE%d' % num, 'rb')
    mbr = h.read(SECTOR)
    if len(mbr) != SECTOR or mbr[510:512] != b'\x55\xaa':
        sys.exit('LBA0 не похож на MBR')
    part = None
    for i in range(4):
        e = mbr[446 + i * 16: 446 + (i + 1) * 16]
        boot, ptype, start, total = e[0], e[4], struct.unpack('<I', e[8:12])[0], struct.unpack('<I', e[12:16])[0]
        if boot == 0x80 and ptype in (0x04, 0x06, 0x0E):
            part = (ptype, start, total)
            break
    if not part:
        sys.exit('Активный FAT-раздел не найден')
    h.seek(part[1] * SECTOR)
    vbr = h.read(SECTOR)
    h.close()
    if vbr[510:512] != b'\x55\xaa' or vbr[11:13] != b'\x00\x02':
        sys.exit('VBR раздела не похож на FAT')
    return part, mbr, vbr


def pick_spc(part_sectors):
    for spc in (2, 4, 8, 16, 32, 64):
        cl = part_sectors // spc
        if 4085 <= cl <= 65525:
            return spc
    sys.exit('Не подобрать кластер под размер')


def build(part, mbr_src, vbr_src, dos_dir, out, size_mb, label, nc_dir=None):
    ptype, _, _ = part
    total = size_mb * 2048
    start = 2048
    psec = total - start
    spc = pick_spc(psec)
    clusters = psec // spc
    fat_sz = (clusters * 2 + SECTOR - 1) // SECTOR
    reserved = struct.unpack('<H', vbr_src[14:16])[0] or 8
    fats = vbr_src[16] or 2
    root_ent = 512
    media = vbr_src[21]

    img = bytearray(total * SECTOR)
    # MBR: код RMPARTUSB + наша таблица
    img[0:446] = mbr_src[0:446]
    img[440:444] = mbr_src[440:444]
    img[446:462] = struct.pack('<B3sB3sII', 0x80, b'\x00\x00\x00', ptype,
                               b'\x00\x00\x00', start, psec)
    img[510:512] = b'\x55\xaa'
    # VBR: код RMPARTUSB + пересчитанный BPB
    vbr = bytearray(vbr_src)
    struct.pack_into('<H', vbr, 11, SECTOR)
    vbr[13] = spc
    struct.pack_into('<H', vbr, 14, reserved)
    vbr[16] = fats
    struct.pack_into('<H', vbr, 17, root_ent)
    if psec <= 0xFFFF:
        struct.pack_into('<H', vbr, 19, psec)
        struct.pack_into('<I', vbr, 32, 0)
    else:
        struct.pack_into('<H', vbr, 19, 0)
        struct.pack_into('<I', vbr, 32, psec)
    vbr[21] = media
    struct.pack_into('<H', vbr, 22, fat_sz)
    img[start * SECTOR:(start + 1) * SECTOR] = vbr

    fat_off = (start + reserved) * SECTOR
    root_off = fat_off + fats * fat_sz * SECTOR
    data_off = root_off + (root_ent * 32 + SECTOR - 1) // SECTOR * SECTOR

    def fat():
        return img[fat_off:fat_off + fat_sz * SECTOR]

    def set16(n, v):
        img[fat_off + n * 2:fat_off + n * 2 + 2] = struct.pack('<H', v)

    # FAT0: media + FFFF
    set16(0, 0xFF00 | media)
    set16(1, 0xFFFF)

    def nclust(size):
        return (size + spc * SECTOR - 1) // (spc * SECTOR) if size else 0

    next_cl = [2]

    def put(data):
        ncl = nclust(len(data))
        if ncl == 0:
            return 0
        first = next_cl[0]
        for i in range(ncl):
            c = first + i
            set16(c, 0xFFFF if i == ncl - 1 else c + 1)
            off = data_off + (c - 2) * spc * SECTOR
            chunk = data[i * spc * SECTOR:(i + 1) * spc * SECTOR]
            img[off:off + len(chunk)] = chunk
        next_cl[0] = first + ncl
        return first

    def entry(raw11, attr, cl, size):
        assert len(raw11) == 11
        return raw11.encode('ascii') + bytes([attr, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) + \
            struct.pack('<HHHI', 0, 0, cl, size)

    def e83(base, ext):
        return (base.upper().ljust(8)[:8] + ext.upper().ljust(3)[:3])

    # порядок важен: IO.SYS первым и непрерывным с кластера 2
    dos_files = sorted(os.listdir(dos_dir))
    must = ['IO.SYS', 'MSDOS.SYS', 'COMMAND.COM']
    for m in must:
        if m not in dos_files:
            sys.exit('Нет %s в %s' % (m, dos_dir))
    order = must + [f for f in dos_files if f not in must]
    root = bytearray()
    root += entry(label.upper().ljust(11)[:11], 0x08, 0, 0)  # метка тома
    for f in order:
        p = os.path.join(dos_dir, f)
        if not os.path.isfile(p):
            continue
        data = open(p, 'rb').read()
        cl = put(data)
        base, dot, ext = f.partition('.')
        root += entry(e83(base, ext), 0x20, cl, len(data))
    # сгенерированные CONFIG.SYS / AUTOEXEC.BAT
    cfg = b'FILES=40\r\nBUFFERS=30\r\nDEVICE=HIMEM.SYS\r\nDOS=HIGH\r\n'
    bat = (b'@ECHO OFF\r\nPROMPT $P$G\r\nPATH C:\\;C:\\DOS\r\n'
           b'ECHO Dobro pozhalovat v MS-DOS (demo MBFU)!\r\n')
    root += entry(e83('CONFIG', 'SYS'), 0x20, put(cfg), len(cfg))
    root += entry(e83('AUTOEXEC', 'BAT'), 0x20, put(bat), len(bat))
    if nc_dir and os.path.isdir(nc_dir):
        ncfiles = [f for f in sorted(os.listdir(nc_dir))
                   if os.path.isfile(os.path.join(nc_dir, f))]
        # 1-й проход: резервируем кластеры каталога
        dirsize = (2 + len(ncfiles)) * 32
        nc_cl = put(bytes(dirsize))
        # 2-й проход: файлы данных
        ents = [entry('.          ', 0x10, nc_cl, 0),
                entry('..         ', 0x10, 0, 0)]
        for f in ncfiles:
            data = open(os.path.join(nc_dir, f), 'rb').read()
            base, dot, ext = f.partition('.')
            ents.append(entry(e83(base, ext), 0x20, put(data), len(data)))
        ncroot = b''.join(ents)
        off = data_off + (nc_cl - 2) * spc * SECTOR
        img[off:off + len(ncroot)] = ncroot
        root += entry(e83('NC', ''), 0x10, nc_cl, 0)
    img[root_off:root_off + len(root)] = root

    # --- проверка ---
    assert img[510:512] == b'\x55\xaa', 'MBR signature'
    assert img[(start) * SECTOR + 510:(start) * SECTOR + 512] == b'\x55\xaa', 'VBR signature'
    # IO.SYS: первая запись после метки, кластер 2, цепочка непрерывна
    first = root[32:64]
    assert first[0:11] == b'IO      SYS', 'IO.SYS не первый: %r' % first[0:11]
    cl = struct.unpack('<H', first[26:28])[0]
    assert cl == 2, 'IO.SYS не с кластера 2'
    size = struct.unpack('<I', first[28:32])[0]
    ncl = (size + spc * SECTOR - 1) // (spc * SECTOR)
    for i in range(ncl):
        v = struct.unpack('<H', fat()[ (2 + i) * 2:(3 + i) * 2])[0]
        want = 0xFFFF if i == ncl - 1 else 2 + i + 1
        assert v == want, 'цепочка IO.SYS бита'
    open(out, 'wb').write(img)
    print('OK: %s (%d МБ, FAT16, кластер %d, система %s первым, NC=%s)' %
          (out, size_mb, spc, 'IO.SYS', 'да' if nc_dir else 'нет'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--drive', required=True, help='Буква флешки MBFU, напр. E')
    ap.add_argument('--dos', required=True, help='Каталог sourcr/MSDOS5|6')
    ap.add_argument('--out', required=True)
    ap.add_argument('--size-mb', type=int, default=32)
    ap.add_argument('--label', default='MSDOS')
    ap.add_argument('--nc', default=None, help='Каталог sourcr/NC (опционально)')
    a = ap.parse_args()
    part, mbr, vbr = read_drive(a.drive.strip().rstrip(':').upper())
    print('Раздел: тип %02X, старт LBA %d' % (part[0], part[1]))
    build(part, mbr, vbr, a.dos, a.out, a.size_mb, a.label, a.nc)


if __name__ == '__main__':
    main()
