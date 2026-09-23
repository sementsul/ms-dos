# -*- coding: utf-8 -*-
"""SLEEP.COM — задержка N секунд для DOS-сессий MBFU (где нет CHOICE /T).

Чистый собственный код (MIT): ждет через BIOS INT 1Ah (счетчик 18.2 Гц).
Собирается этим скриптом БЕЗ ассемблера — встроенный мини-ассемблер x86-16.
Использование в DOS: SLEEP 5   (без аргумента — 5 секунд)

Сборка: python tools/make_sleep.py  ->  DOS/SLEEP.COM
"""
import struct

R16 = {'AX': 0, 'CX': 1, 'DX': 2, 'BX': 3, 'SP': 4, 'BP': 5, 'SI': 6, 'DI': 7}
R8 = {'AL': 0, 'AH': 4}
JCC = {'JZ': 0x74, 'JNZ': 0x75, 'JB': 0x72, 'JAE': 0x73, 'JA': 0x77, 'JBE': 0x76}


def modrm(dst, src, reg_is_dst=False):
    # reg=приемник: 8B/8A (MOV), 03 (ADD), 1B (SBB). reg=источник: 29 (SUB), 39 (CMP)
    reg, rm = (dst, src) if reg_is_dst else (src, dst)
    return 0xC0 | (R16[reg] << 3) | R16[rm]


class Asm:
    def __init__(self):
        self.items = []  # ('label', name) | ('db', bytes) | ('ins', op, args)

    def label(self, n):
        self.items.append(('label', n))

    def emit(self, op, *args):
        self.items.append(('ins', op, args))

    def build(self, org=0x100):
        # размеры всех инструкций фиксированы -> адреса меток за один проход
        addr = {}
        pos = org
        for it in self.items:
            if it[0] == 'label':
                addr[it[1]] = pos
            elif it[0] == 'db':
                pos += len(it[1])
            else:
                pos += self._size(it[1], it[2])
        out = bytearray()
        for it in self.items:
            if it[0] == 'label':
                continue
            if it[0] == 'db':
                out += it[1]
            else:
                out += self._enc(it[1], it[2], addr, org + len(out))
        return bytes(out)

    def _size(self, op, args):
        if op in ('LODSB', 'PUSH', 'POP', 'MUL', 'INT'):
            return 1 if op in ('LODSB',) else (1 if op in ('PUSH', 'POP') else 2)
        if op == 'MOV':
            d, s = args
            if isinstance(d, str) and d in R16 and isinstance(s, int):
                return 3
            if d == 'AH' and isinstance(s, int):
                return 2
            return 2  # reg,reg
        if op in ('SUB', 'ADD', 'CMP', 'SBB'):
            d, s = args
            if d == 'AL' and isinstance(s, int):
                return 2
            if op == 'CMP' and d == 'CX' and isinstance(s, int):
                return 3
            return 2
        if op in JCC or op == 'JMP':
            return 2
        raise ValueError(op)

    def _enc(self, op, args, labels, pos):
        if op == 'LODSB':
            return b'\xAC'
        if op == 'PUSH':
            return bytes([0x50 + R16[args[0]]])
        if op == 'POP':
            return bytes([0x58 + R16[args[0]]])
        if op == 'MUL':
            return bytes([0xF7, 0xC0 | (4 << 3) | R16[args[0]]])
        if op == 'INT':
            return bytes([0xCD, args[0]])
        if op == 'MOV':
            d, s = args
            if isinstance(d, str) and d in R16 and isinstance(s, int):
                return bytes([0xB8 + R16[d]]) + struct.pack('<H', s)
            if d == 'AH':
                return bytes([0xB4, s])
            return bytes([0x8B, modrm(d, s, reg_is_dst=True)])
        if op in ('SUB', 'ADD', 'CMP', 'SBB'):
            base = {'SUB': 0x2C, 'ADD': 0x00, 'CMP': 0x3C, 'SBB': 0x18}[op]
            d, s = args
            if d == 'AL':
                return bytes([base, s])
            if op == 'CMP' and d == 'CX':
                return bytes([0x83, 0xF9, s])
            code = {'ADD': 0x03, 'SUB': 0x29, 'CMP': 0x39, 'SBB': 0x1B}[op]
            dst_in_reg = op in ('ADD', 'SBB')
            return bytes([code, modrm(d, s, reg_is_dst=dst_in_reg)])
        if op in JCC or op == 'JMP':
            opc = JCC.get(op, 0xEB)
            disp = labels[args[0]] - (pos + 2)
            assert -128 <= disp <= 127, (op, disp)
            return bytes([opc, disp & 0xFF])
        raise ValueError(op)


def build_sleep():
    a = Asm()
    E = a.emit
    E('MOV', 'SI', 0x81)
    a.label('skipsp')
    E('LODSB')
    E('CMP', 'AL', 0x20)
    E('JZ', 'skipsp')
    E('CMP', 'AL', 0x30)
    E('JB', 'default')
    E('CMP', 'AL', 0x39)
    E('JA', 'default')
    E('MOV', 'CX', 0)
    E('MOV', 'BX', 0x0A)
    a.label('digit')
    E('SUB', 'AL', 0x30)
    E('MOV', 'AH', 0)
    E('PUSH', 'AX')
    E('MOV', 'AX', 'CX')
    E('MUL', 'BX')
    E('MOV', 'CX', 'AX')
    E('POP', 'AX')
    E('ADD', 'CX', 'AX')
    E('LODSB')
    E('CMP', 'AL', 0x30)
    E('JB', 'go')
    E('CMP', 'AL', 0x39)
    E('JBE', 'digit')
    a.label('go')
    E('MOV', 'AX', 'CX')
    E('MOV', 'BX', 0x12)  # 18 тиков/сек (0x12 совпадает с десятичным!)
    E('MUL', 'BX')
    E('MOV', 'BX', 'AX')  # BX = ждать тиков
    E('MOV', 'AH', 0)
    E('INT', 0x1A)
    E('PUSH', 'CX')  # T0hi в стек: INT 1A может портить DI,
    E('PUSH', 'DX')  # поэтому T0 держим в стеке, а не в SI:DI
    a.label('poll')
    E('MOV', 'AH', 0)
    E('INT', 0x1A)  # CX:DX = сейчас
    E('POP', 'SI')  # T0lo
    E('POP', 'DI')  # T0hi (между POP и сравнением прерываний нет)
    E('PUSH', 'DI')
    E('PUSH', 'SI')
    E('SUB', 'DX', 'SI')
    E('SBB', 'CX', 'DI')
    E('CMP', 'CX', 0)
    E('JA', 'done')
    E('CMP', 'DX', 'BX')
    E('JB', 'poll')
    a.label('done')
    E('INT', 0x20)  # стек можно не чистить — выходим
    a.label('default')
    E('MOV', 'CX', 5)
    E('JMP', 'go')
    return a.build()


if __name__ == '__main__':
    import os
    blob = build_sleep()
    print('SLEEP.COM: %d байт' % len(blob))
    print(blob.hex(' '))
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'MBFU_clean', 'DOS', 'SLEEP.COM')
    open(out, 'wb').write(blob)
    print('записан:', out)
