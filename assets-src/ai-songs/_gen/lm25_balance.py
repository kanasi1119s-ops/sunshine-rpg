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
LEAD_MAX = None      # 2026-10-23 人間が「全体的にはいい」と言った 02（BBS の音・ベース1.5倍）は、参考の音で測った比のとおり
                     #   リードがギターの約4.4倍だった。リードは測った比のまま（上限をかけない）
TECH_LEVEL = 0.75    # 速弾きのギターの合計を、ギターの 0.75 倍とリードの 0.6 倍の大きい方に
TECH_OF_LEAD = 0.6
RIFF_GAIN = 1.05
BASS_GAIN = 1.4      # 2026-10-23 人間「ベースの音小さくて聞きにくいかも」（+約3dB）
# リードの余韻（2026-10-23 人間「ギターの高音をリードで弾くときは少し余韻を残すように響かせよう」）:
#   参考の音はリードに部屋の鳴り（ルーム）しか残さないので、短めのプレートと、付点8分のうすいやまびこを足し、音の終わりを少し長く
# リードの音色（2026-10-23 人間「鋭いけど、優しい心に響く感じ」）: 輪郭（2kHz 前後）は残して鋭さを保ち、
#   耳に刺さる 4.5kHz より上を少し丸め、800Hz あたりに温かさを足す
LEAD_TONE = [{"type": "eq", "low": 0, "mid": 1.5, "midHz": 850, "high": -2.5}, {"type": "filter", "kind": "lowpass", "freq": 8500, "q": 0.6}]
# 2026-10-23 人間「歪が汚い」: アンプの前のオーバードライブを外し、コンプはごく軽く、アンプへの入力を浅く（0.5）
# 2026-10-23 聞き比べで人間が③を選んだ（PRS Archon リード1・コンプなし・いちばん浅い歪み）
# 2026-10-23 人間（01 を聞いて）「歪がちょっと濁っている」: 歪みを 0.45→0.38 に浅く、低い中域をもう少し削る。
#   ハモリ（3度上など）を同じ歪みで重ねると、2本の音がぶつかって濁りが増えるので、ハモリは歪みをさらに浅く・音量を 0.7 倍に
LEAD_CHAIN = [{"type": "filter", "kind": "highpass", "freq": 150, "q": 0.7},
              {"type": "eq", "low": 0, "mid": -3.5, "midHz": 320, "high": 0},                                    # 濁り
              {"type": "eq", "low": 0, "mid": 2.0, "midHz": 1600, "high": 0},                                    # 歌う帯域（鋭さ）
              {"type": "eq", "low": 0, "mid": -2.0, "midHz": 4200, "high": 0},                                   # 刺さる所だけ細く
              {"type": "filter", "kind": "lowpass", "freq": 11500, "q": 0.6},                                    # 空気感は残す
              {"type": "delay", "beats": 0.75, "mix": 0.16, "feedback": 0.3}]                                    # 余韻
LEAD_DRIVE = 0.38
HARM_DRIVE = 0.28
HARM_GAIN = 0.7
LEAD_AMP = "namArchonL1"   # PRS Archon（手元だけのモデル。無い環境ではマーシャル系で鳴る）
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
        # 速弾き（スウィープ・タッピング・レガート）は、ソロの楽器としてはっきり聞こえる大きさに（2026-10-23 人間「ピロピロの速弾きのギターの音が聞こえないの、小さすぎて」）。
        #   やまびこが付いているため「そのほか」に入り、重ねと一緒に小さく縮められていた
        if any(w in role for w in ("技のギター", "タッピング", "スウィープ", "レガート", "速弾き")): return "tech"
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
    L = tot("lead")
    F = sum(p.get("volume", 0) for p in ps if p.get("_feat"))
    if G > 0 and F > 0 and F < FEATURE_LEVEL * G:      # 主役の楽器は、小さすぎるときだけ上げる（参考の音で大きいならそのまま）
        k = FEATURE_LEVEL * G / F
        for p in ps:
            if p.get("_feat"): p["volume"] = round(p["volume"] * k, 5)
        log.append(f"主役の楽器 ×{k:.3f}")
    T = sum(p.get("volume", 0) for p in ps if group(p) == "tech")
    if G > 0 and T > 0:
        k = max(TECH_LEVEL * G, TECH_OF_LEAD * L) / T
        for p in ps:
            if group(p) == "tech": p["volume"] = round(p["volume"] * k, 5)
        log.append(f"速弾き ×{k:.3f}")
    if G > 0:
        for g, mx in (("other", OTHER_MAX), ("lead", LEAD_MAX)):
            if mx is None: continue
            s = tot(g)
            cap = mx * G
            if s > cap:
                k = cap / s
                for p in ps:
                    if group(p) == g and not p.get("_feat"): p["volume"] = round(p["volume"] * k, 5)
                log.append(f"{g} ×{k:.3f}")
    for p in ps:
        if group(p) == "guitar" and p.get("role", "").startswith(("看板リフ", "リズム")): p["volume"] = round(p.get("volume", 0) * RIFF_GAIN, 5)
        if group(p) == "drums": p["volume"] = round(p.get("volume", 0) * DRUM_GAIN, 5)
        if group(p) == "bass": p["volume"] = round(p.get("volume", 0) * BASS_GAIN, 5)
        if group(p) == "lead" and not p.get("_toned"):
            # リード専用の音作り（2026-10-23 人間「問題なのは高音。歪があるんだけど透き通るような伸びが欲しくて、余韻も感じたい。
            #   チョーキングしても、そのまましっかり伸び切った鋭く透き通った高い音に」）。参考の音の「歌の EQ」（2.5k・3.9k を -12dB、
            #   4.5k より上を +9dB）は、リードの抜ける帯域を削ってザラつきだけ残していたので使わない。
            p["fx"] = [dict(f) for f in LEAD_CHAIN]
            p["ampGate"] = 3                                   # 余韻を切らない
            p["ampDrive"] = LEAD_DRIVE
            # 2026-10-23 人間「この濁り、高音に近づけるときと、高音から下げて音が重なってるときに聞こえる。全曲共通かも」:
            #   sustain 2 と release 0.9 で前の音が次の音に重なり、歪みの中で2音がぶつかっていた。
            #   単音の楽器として弾き（mono: 次の音で前の音を止める）、離したあとの尾は短く。余韻は休符の前の伸び・プレート・やまびこ（アンプのあと＝濁らない）で出す
            p["sustain"] = max(p.get("sustain", 1.0), 2.0)
            p["mono"] = True
            p["release"] = 0.35
            p["reverb"] = max(p.get("reverb", 0), 0.25)
            if LEAD_AMP: p["amp"] = LEAD_AMP
            if "ハモリ" in p.get("role", ""):
                p["ampDrive"] = HARM_DRIVE
                p["pan"] = round(min(1.0, (p.get("pan") or 0) + 0.22), 2)   # 別のチャンネル＝別のアンプで鳴らす（同じアンプで3度が歪むと濁る）
                p["volume"] = round(p.get("volume", 0) * HARM_GAIN, 5)
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
