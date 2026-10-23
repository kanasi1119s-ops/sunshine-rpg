# 参考の音を当てたあとの、楽器の組どうしの大きさの直し（2026-10-23）。使い方: python3 lm25_balance.py <曲.json>（上書き）
# 参考の音の「そのほかの楽器 +9〜18dB」は、1つの組（参考の曲のシンセなど）に対する値なのに、パートごとに掛けていたため、
# 追加の楽器・ピアノ（5パート）・空気の層が多い曲では、そのほかの組の合計がギターの10倍近くになり、作曲ソフトが全体を縮めて
# ベースとドラムまで小さくなっていた（人間「サーって流れてる音のせいで、音のバランスかなり悪くなってる」「聴きにくい」）。
# 組の合計で上限をかける: そのほか ≦ ギター（リフ・リズム・分散和音・クリーン）の OTHER_MAX 倍、リード ≦ LEAD_MAX 倍。
# 人間の好み: リフ（看板リフ・リズム）を 5% 上げ、ドラムを 10% 下げる（「リフが弱い。5ぐらい上げて」「ドラムの音を10下げよう」＝割合）。
import json, sys

OTHER_MAX = 0.5      # 重ね（追加の楽器: ピアノ・弦・合唱など）・空気の層・ダンスの要素
FEATURE_LEVEL = 0.9  # その曲だけの楽器（サックス・シタール・三味線など）は主役: 合計をギターの 0.9 倍（リードと同じ）にそろえる
# 2026-10-23 人間「一つだけ出す楽器の音はその曲のメインになるように、音量上げていいからね」
LEAD_MAX = 0.9
RIFF_GAIN = 1.05
BASS_GAIN = 1.4      # 2026-10-23 人間「ベースの音小さくて聞きにくいかも」（+約3dB）
# リードの余韻（2026-10-23 人間「ギターの高音をリードで弾くときは少し余韻を残すように響かせよう」）:
#   参考の音はリードに部屋の鳴り（ルーム）しか残さないので、短めのプレートと、付点8分のうすいやまびこを足し、音の終わりを少し長く
# リードの音色（2026-10-23 人間「鋭いけど、優しい心に響く感じ」）: 輪郭（2kHz 前後）は残して鋭さを保ち、
#   耳に刺さる 4.5kHz より上を少し丸め、800Hz あたりに温かさを足す
LEAD_TONE = [{"type": "eq", "low": 0, "mid": 1.5, "midHz": 850, "high": -2.5}, {"type": "filter", "kind": "lowpass", "freq": 8500, "q": 0.6}]
LEAD_TAIL = [{"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.22}, {"type": "plate", "mix": 0.2}]
DRUM_GAIN = 0.9
GUITARS = {"distGuitar", "crunch", "leadGuitar", "echoGuitar", "guitar"}
DRUMS = {"kick", "snare", "hihat", "tom", "crash", "cymbal", "kickTrigger"}
BASSES = {"bass", "slap", "sub808"}


def group(p):
    ins, role = p.get("instrument", ""), p.get("role", "")
    if p.get("patch") in ("cymbalFx",): return "fx"
    if p.get("patch") in ("guitarFx",): return "fx"
    if ins in DRUMS: return "drums"
    if ins in BASSES: return "bass"
    if ins in GUITARS:
        if "空気の層" in role or any(f.get("type") in ("delay", "pingpong") for f in p.get("fx", [])) and not role.startswith(("看板リフ", "リズム", "リード")): return "other"
        if role.startswith("リード"): return "lead"
        return "guitar"
    return "other"


def fit_fx(p):
    """fx は作曲ソフトで最大8個。参考の音のローパス2段を1つにまとめ、それでも多ければ残響系を part の reverb（送り）へ移す"""
    fx = p.get("fx") or []
    if len(fx) <= 8: return
    idx = [i for i, f in enumerate(fx) if f.get("type") == "filter" and f.get("kind") == "lowpass"]
    if len(idx) >= 2:
        keep = dict(fx[idx[0]]); keep["freq"] = min(fx[i].get("freq", 20000) for i in idx)
        fx = [keep if i == idx[0] else f for i, f in enumerate(fx) if i not in idx[1:]]
    while len(fx) > 8:
        rv = next((f for f in fx if f.get("type") in ("reverb", "plate", "room", "spring")), None)
        if rv is None: fx = fx[:8]; break
        p["reverb"] = max(p.get("reverb", 0), round(rv.get("mix", 0.2), 3)); fx.remove(rv)
    p["fx"] = fx


def featured(p):
    r = p.get("role", "")
    return group(p) == "other" and p.get("instrument") not in GUITARS and not r.startswith(("追加の楽器", "ダンスの要素")) and "空気の層" not in r


def balance(song):
    ps = song["parts"]
    for p in ps:
        if featured(p): p["_feat"] = True
    tot = lambda g: sum(p.get("volume", 0) for p in ps if group(p) == g and not p.get("_feat"))
    G = tot("guitar")
    log = []
    F = sum(p.get("volume", 0) for p in ps if p.get("_feat"))
    if G > 0 and F > 0:
        k = FEATURE_LEVEL * G / F
        for p in ps:
            if p.get("_feat"): p["volume"] = round(p["volume"] * k, 5)
        log.append(f"主役の楽器 ×{k:.3f}")
    if G > 0:
        for g, mx in (("other", OTHER_MAX), ("lead", LEAD_MAX)):
            s = tot(g)
            if s > mx * G:
                k = mx * G / s
                for p in ps:
                    if group(p) == g and not p.get("_feat"): p["volume"] = round(p["volume"] * k, 5)
                log.append(f"{g} ×{k:.3f}")
    for p in ps:
        if group(p) == "guitar" and p.get("role", "").startswith(("看板リフ", "リズム")): p["volume"] = round(p.get("volume", 0) * RIFF_GAIN, 5)
        if group(p) == "drums": p["volume"] = round(p.get("volume", 0) * DRUM_GAIN, 5)
        if group(p) == "bass": p["volume"] = round(p.get("volume", 0) * BASS_GAIN, 5)
        if group(p) == "lead" and not p.get("_toned"):
            # fx は最大8個: 参考の音の EQ（ハイパス・EQ 4つ・ローパス2つ）＋ルーム。ローパスを1つにまとめ、温かさの EQ を足し、高い所の丸めは1つ目の EQ に合わせる
            fx = [dict(f) for f in (p.get("fx") or [])]
            lps = [f for f in fx if f.get("type") == "filter" and f.get("kind") == "lowpass"]
            rest = [f for f in fx if f not in lps and f.get("type") != "room"]
            eqs = [f for f in rest if f.get("type") == "eq"]
            if eqs: eqs[0]["high"] = round(eqs[0].get("high", 0) - 2.5, 2)
            lp = {"type": "filter", "kind": "lowpass", "freq": min([8500] + [f.get("freq", 20000) for f in lps]), "q": 0.6}
            new = rest + [{"type": "eq", "low": 0, "mid": 1.5, "midHz": 850, "high": 0}, lp] + [f for f in fx if f.get("type") == "room"][:1]
            p["fx"] = new[:8]
            p["reverb"] = max(p.get("reverb", 0), 0.22)      # 余韻は残響の送りで
            p["release"] = max(p.get("release", 0.3), 0.6)
            p["_toned"] = True
    for p in ps:
        p.pop("_feat", None); p.pop("_toned", None)
        fit_fx(p)
    return log


if __name__ == "__main__":
    path = sys.argv[1]
    song = json.load(open(path))
    # 曲ごとの音量の好み（<曲.json>.gains。例 {"drums": 0.97}。人間「16ドラムの音3落とそう」）
    import os
    gp = sys.argv[2] if len(sys.argv) > 2 else path + ".gains"
    if os.path.exists(gp):
        for g_, k_ in json.load(open(gp)).items():
            for p in song["parts"]:
                if group(p) == g_: p["volume"] = round(p.get("volume", 0) * k_, 5)
    log = balance(song)
    json.dump(song, open(path, "w"), ensure_ascii=False)
    print("組の大きさを直しました:", ", ".join(log) or "（上限の内側）")
