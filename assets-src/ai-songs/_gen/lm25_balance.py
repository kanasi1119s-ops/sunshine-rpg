# 参考の音を当てたあとの、楽器の組どうしの大きさの直し（2026-10-23）。使い方: python3 lm25_balance.py <曲.json>（上書き）
# 参考の音の「そのほかの楽器 +9〜18dB」は、1つの組（参考の曲のシンセなど）に対する値なのに、パートごとに掛けていたため、
# 追加の楽器・ピアノ（5パート）・空気の層が多い曲では、そのほかの組の合計がギターの10倍近くになり、作曲ソフトが全体を縮めて
# ベースとドラムまで小さくなっていた（人間「サーって流れてる音のせいで、音のバランスかなり悪くなってる」「聴きにくい」）。
# 組の合計で上限をかける: そのほか ≦ ギター（リフ・リズム・分散和音・クリーン）の OTHER_MAX 倍、リード ≦ LEAD_MAX 倍。
# 人間の好み: リフ（看板リフ・リズム）を 5% 上げ、ドラムを 10% 下げる（「リフが弱い。5ぐらい上げて」「ドラムの音を10下げよう」＝割合）。
import json, sys

OTHER_MAX = 0.7
LEAD_MAX = 0.9
RIFF_GAIN = 1.05
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


def balance(song):
    ps = song["parts"]
    tot = lambda g: sum(p.get("volume", 0) for p in ps if group(p) == g)
    G = tot("guitar")
    log = []
    if G > 0:
        for g, mx in (("other", OTHER_MAX), ("lead", LEAD_MAX)):
            s = tot(g)
            if s > mx * G:
                k = mx * G / s
                for p in ps:
                    if group(p) == g: p["volume"] = round(p["volume"] * k, 5)
                log.append(f"{g} ×{k:.3f}")
    for p in ps:
        if group(p) == "guitar" and p.get("role", "").startswith(("看板リフ", "リズム")): p["volume"] = round(p.get("volume", 0) * RIFF_GAIN, 5)
        if group(p) == "drums": p["volume"] = round(p.get("volume", 0) * DRUM_GAIN, 5)
    return log


if __name__ == "__main__":
    path = sys.argv[1]
    song = json.load(open(path))
    log = balance(song)
    json.dump(song, open(path, "w"), ensure_ascii=False)
    print("組の大きさを直しました:", ", ".join(log) or "（上限の内側）")
