"""Surge XT（VST3）の状態と .fxp パッチをつなぐ小道具。pedalboard の raw_state を読み書きする。"""
import re, struct
CH = ".ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+"
def jdec(s):
    size, data = s.split(".", 1); size = int(size); out = bytearray(size); bit = 0
    for c in data:
        v = CH.index(c)
        for k in range(6):
            if v >> k & 1:
                if bit // 8 < size: out[bit // 8] |= 1 << (bit % 8)
            bit += 1
    return bytes(out)
def jenc(b):
    nbits = len(b) * 8; out = []
    for i in range(0, nbits, 6):
        v = 0
        for k in range(6):
            j = i + k
            if j < nbits and b[j // 8] >> (j % 8) & 1: v |= 1 << k
        out.append(CH[v])
    return f"{len(b)}." + "".join(out)
def split(raw):
    n = struct.unpack("<I", raw[4:8])[0]; x = raw[8:8 + n].decode()
    m = re.search(r"<IComponent>([^<]+)</IComponent>", x)
    return x, m


SPACE_TYPES = {1, 2, 11, 27}   # Surge の FX の種類の番号: 1＝Delay・2＝Reverb 1・11＝Reverb 2・27＝Spring Reverb


def strip_space_xml(data):
    """パッチの中のリバーブ・ディレイの FX を「なし」にする（XML の数字を同じ長さの 0 に置きかえる＝見出しの長さはそのまま）。
    pedalboard でパラメーターを読むと、プリセットによって音が出なくなることがあるので、読みこむ前のデータで直す"""
    out = bytearray(data); n = 0
    for m in re.finditer(rb'<fx\d+_type type="0" value="(\d+)"', data):
        if int(m.group(1)) in SPACE_TYPES:
            a, b = m.span(1); out[a:b] = b"0" * (b - a); n += 1
    return bytes(out), n


def load_fxp(plugin, path, strip_space=False):
    """.fxp のパッチを Surge XT（pedalboard の VST3）に読みこむ。fxp の先頭 60 バイト（見出し）のあとが Surge の中身（sub3…）。
    strip_space=True でリバーブ・ディレイを切る。戻り値: 切った数"""
    data = open(path, "rb").read()
    assert data[:4] == b"CcnK" and data[60:64] == b"sub3", path
    cut = 0
    if strip_space: data, cut = strip_space_xml(data)
    raw = plugin.raw_state
    x, m = split(raw)
    x2 = x[:m.start(1)] + jenc(data[60:]) + x[m.end(1):]
    xb = x2.encode()
    plugin.raw_state = raw[:4] + struct.pack("<I", len(xb)) + xb + raw[8 + struct.unpack("<I", raw[4:8])[0]:]
    return cut
