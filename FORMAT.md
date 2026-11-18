# Формат образа `.mbfu`

`MBFUTool 2.x` хранит образы дисков в собственном контейнере `.mbfu`. Формат
описан здесь, чтобы образы можно было читать и проверять без запуска программы.
Веб-версия той же спецификации: <https://ms-dos.su/mbfu-format.html>.

## Зачем контейнер

- **Потоковая запись.** Заголовок фиксированного размера, дальше один поток
  deflate: образ распаковывается сразу на устройство, без временной копии.
- **Целостность.** SHA-256 считается по несжатым данным и проверяется при
  распаковке и после записи на носитель.
- **Метаданные.** В заголовке — исходное имя файла и тип носителя.
- **Размер.** Образы MS-DOS сжимаются в разы: пустое пространство и повторяющиеся
  сектора убирает deflate.

## Структура файла

Заголовок — 126 байт, многобайтные числа little-endian, без выравнивания.
Формат в терминах Python `struct`: `<8sHBBHQQ32s64s`.

| Смещение | Размер | Поле | Значение |
|---:|---:|---|---|
| 0 | 8 | `magic` | `MBFUIMG\x01` |
| 8 | 2 | `version` | uint16, сейчас `1` |
| 10 | 1 | `image_type` | uint8: `0` сырой образ, `1` дискета, `2` жёсткий диск |
| 11 | 1 | `compression` | uint8: `1` — zlib (deflate) |
| 12 | 2 | `reserved` | uint16, всегда `0` |
| 14 | 8 | `raw_size` | uint64, размер несжатого образа |
| 22 | 8 | `data_size` | uint64, размер сжатого потока |
| 30 | 32 | `sha256` | SHA-256 несжатого образа |
| 62 | 64 | `name` | имя исходного файла, ASCII, дополнено нулями |

Сразу за заголовком идёт один поток zlib длиной `data_size`. Оглавлений и
выравниваний нет, поэтому файл читается последовательно без знания его размера.

## Чтение на Python

```python
import hashlib, struct, zlib

HDR = "<8sHBBHQQ32s64s"
SIZE = struct.calcsize(HDR)          # 126

def read_header(path):
    with open(path, "rb") as f:
        buf = f.read(SIZE)
    magic, ver, itype, comp, res, raw, dsize, digest, name = struct.unpack(HDR, buf)
    if magic != b"MBFUIMG\x01":
        raise ValueError("not an .mbfu image")
    return {"version": ver, "image_type": itype, "compression": comp,
            "raw_size": raw, "data_size": dsize, "sha256": digest.hex(),
            "name": name.rstrip(b"\0").decode("ascii", "replace")}

def extract(src, dst):
    info = read_header(src)
    h = hashlib.sha256()
    with open(src, "rb") as f, open(dst, "wb") as out:
        f.seek(SIZE)
        dec = zlib.decompressobj()
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            data = dec.decompress(chunk)
            if data:
                h.update(data)
                out.write(data)
        tail = dec.flush()
        if tail:
            h.update(tail)
            out.write(tail)
    if h.hexdigest() != info["sha256"]:
        raise ValueError("checksum mismatch")
    return info
```

Проверка хэша обязательна: файл, обрезанный по границе блока, распакуется без
ошибки zlib, и только SHA-256 это поймает.

## Что принимается на вход

`.mbfu`, `.img`, `.ima` (сырые образы дискет и дисков), `.vhd`, `.vfd`.
Сырые образы пишутся как есть; `.mbfu` распаковывается по ходу записи, хэш
сверяется после завершения.

## Ограничения

- образ больше 4 ГБ не открывается в DOSBox 0.72 — редактор образов ограничен
  этим размером;
- запись на флешку работает и для больших образов, но DOS-раздел ограничен FAT16
  (до 4 ГБ, на практике 2 ГБ);
- имя файла в заголовке — ASCII.

## Правовой статус

Описание формата открыто: чтение `.mbfu` можно реализовать в своём инструменте.
Сама программа `MBFUTool 2.x` — проприетарная, исходный код не публикуется;
условия — в [LICENSE](LICENSE) и на странице <https://ms-dos.su/terms.html>.

---

# The `.mbfu` image format (English)

`.mbfu` is the image container used by `MBFUTool 2.x`. A fixed 126-byte header,
zlib compression, SHA-256 over the uncompressed data. Web version:
<https://ms-dos.su/en/mbfu-format.html>.

Header layout (`<8sHBBHQQ32s64s`, little-endian): magic `MBFUIMG\x01` (8),
version uint16 = 1 (2), image_type uint8 (0 raw, 1 floppy, 2 hard disk) (1),
compression uint8 = 1 for zlib (1), reserved uint16 = 0 (2), raw_size uint64 (8),
data_size uint64 (8), sha256 32 bytes, name 64 bytes ASCII zero-padded.

A single zlib stream follows the header; its length is `data_size`. The format is
publicly documented so images can be verified without the program; the program
itself remains proprietary and its source is not published.