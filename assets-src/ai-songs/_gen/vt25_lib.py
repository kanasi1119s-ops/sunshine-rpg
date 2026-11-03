# 重音テトのボカロ曲25曲・第2弾（vt25）の部品（2026-11-04）。表は docs/sound/vt25-plan.md。
# 作り方は第1弾（vb25『SCARLET FREQUENCY』）と同じ。vb25_lib をそのまま使い、第2弾で足したものだけをここに書く:
#   ・finish(): BGM の版／歌の版の書き出し（teto）に、曲ごとのエフェクト（.fx）と、歌の重ね（vocalDouble）を足す
#   ・エフェクトは、人間が見せてくれた無料のエフェクト（T-Saturator・OTT・Vocal Doubler・Wider・Tape Stop）と同じ働きのものを作った。
#     合う曲だけに使う（vt25_fx.py・tools/singer/sing.py）
from vb25_lib import *
import json as _vjson, sys as _vsys


def finish(S, LY, V, transpose=0, fx=None, double=None, **kw):
    """fx: [{"type": "sat"|"ott"|"width"|"tapestop", "scenes": [場面の名前] か "*", ...}]
    double: [(場面の名前, 量 0〜1), ...] … 歌の版で、その場面だけ歌を重ねる（ダブラー）"""
    teto(S, LY, V, transpose=transpose, **kw)
    path = _vsys.argv[1]
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
