# 重音テトのボカロ曲25曲・第2弾（vt25）の部品（2026-11-04）。表は docs/sound/vt25-plan.md。
# 作り方は第1弾（vb25『SCARLET FREQUENCY』）と同じ。vb25_lib をそのまま使い、第2弾で足したものだけをここに書く:
#   ・finish(): BGM の版／歌の版の書き出し（teto）に、曲ごとのエフェクト（.fx）と、歌の重ね（vocalDouble）を足す
#   ・エフェクトは、人間が見せてくれた無料のエフェクト（T-Saturator・OTT・Vocal Doubler・Wider・Tape Stop）と同じ働きのものを作った。
#     合う曲だけに使う（vt25_fx.py・tools/singer/sing.py）
from vb25_lib import *
import json as _vjson, sys as _vsys


_DRUMS = ("kick", "snare", "hihat", "hat", "tom", "crash", "ride", "clap", "perc")


def _big_arc(x):
    """作曲ソフトの「人が弾いたような強弱」（src/audio/dynamics.ts の bigArc）と同じ曲線。x は曲の中の位置（0〜1）"""
    import math
    if x < 0.7: return 0.62 + 0.38 * math.sin((x / 0.7) * (math.pi / 2))
    return 1 - 0.3 * ((x - 0.7) / 0.3) ** 2


def flatten_arc(path, S):
    """2026-11-04（04・08）: 「人が弾いたような強弱」の曲全体の山（出だし 0.62 → 7割で 1.0）は、ドラムには半分しかかからない。
    そのため前半はドラム以外だけが大きく下がり、人間に「ドラム以外が極端に小さい」と言われた。強弱そのものを切ると（dynamics: false）
    音の強さの広がり（wide）もなくなり、どの楽器も強く弾かれて点数が大きく下がった（04 v4: 7.63 → 6.81）。
    → 強弱の設定は残し、曲全体の山だけを小節ごとの強さ（barGain）で打ち消す。フレーズの息づかいと拍の強弱は残る。合う曲だけに使う"""
    js = _vjson.load(open(path)); nb = S.nb
    for p in js["parts"]:
        drum = str(p.get("instrument", "")).startswith(_DRUMS)
        g = []
        for b in range(nb):
            a = _big_arc((b + 0.5) / nb)
            a = 1 - (1 - a) * 0.5 if drum else a
            old = p.get("barGain", [1] * nb)
            g.append(round(min(2.0, (old[b] if b < len(old) else 1) / a), 4))
        p["barGain"] = g
    _vjson.dump(js, open(path, "w"), ensure_ascii=False)


def finish(S, LY, V, transpose=0, fx=None, double=None, flat=False, **kw):
    """fx: [{"type": "sat"|"ott"|"width"|"tapestop", "scenes": [場面の名前] か "*", ...}]
    double: [(場面の名前, 量 0〜1), ...] … 歌の版で、その場面だけ歌を重ねる（ダブラー）"""
    teto(S, LY, V, transpose=transpose, **kw)
    path = _vsys.argv[1]
    if flat: flatten_arc(path, S)
    if fx:
        open(path + ".fx", "w").write(_vjson.dumps(fx, ensure_ascii=False))
    if double and VOCAL:
        js = _vjson.load(open(path))
        segs = []
        for name, amt in double:
            bars = S.sc(name)
            segs.append({"from": bars[0] * S.beats, "to": (bars[-1] + 1) * S.beats, "amount": amt})
        js["vocalDouble"] = segs
        _vjson.dump(js, open(path, "w"), ensure_ascii=False)
