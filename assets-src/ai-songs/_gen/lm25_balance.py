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
BASS_GAIN = 1.9      # 2026-10-23 人間「ベースの音小さくて聞きにくいかも」（1.4）。2026-10-24 重低音の棚を +9→+3dB にして約4dB下がった分を戻す（1.9）
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
              {"type": "eq", "low": 0, "mid": 2.0, "midHz": 3000, "high": 0},                                    # 粒（2026-10-24 人間「リードの高音の部分がもう少し粒が立って透き通るように」）
              {"type": "eq", "low": 0, "mid": -1.0, "midHz": 4600, "high": 0},                                   # 刺さる所だけ、ほんの少し（-2→-1）
              {"type": "filter", "kind": "lowpass", "freq": 13500, "q": 0.6},                                    # 透き通る空気感（11.5k→13.5k）
              {"type": "delay", "beats": 0.75, "mix": 0.16, "feedback": 0.3}]                                    # 余韻
LEAD_DRIVE = 0.38
HARM_DRIVE = 0.28
HARM_GAIN = 0.7
LEAD_AMP = "namArchonL1"   # PRS Archon（手元だけのモデル。無い環境ではマーシャル系で鳴る）
LEAD_TAIL = [{"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.22}, {"type": "plate", "mix": 0.2}]
# ベースの音作り（2026-10-24 人間「点数低い曲ベースが埋もれてないかな」）: 測ると、点の低い曲ほど 100〜250Hz が全体の大半（-1〜-2dB）で、
#   600〜1500Hz（ベースの「ゴリッ」と指の粒が聞こえる帯域）が -14〜-17dB しかなかった。参考の音の EQ がベースの 730・810・1850Hz を
#   それぞれ -9dB 削っていたため、低い音の量はあるのに、ベースの輪郭が聞こえず埋もれていた。中域の削りは外し、ゴリッと指の粒を足す
BASS_MID_KEEP = (500, 2600)    # この帯域の削りは外す
# 2026-10-24 16 をパートごとに書き出して測った結果: ベースはいちばん大きいパート（ギターより約6dB大きい）だが、その大半が 40〜100Hz の
#   重低音（-3dB）で、600〜1500Hz は -26dB、1500〜3000Hz は -43dB しかなかった。「低い唸りはあるのに、音の動きが聞こえない」＝埋もれて聞こえる。
#   参考の音の EQ の低い棚（+9dB）を +3dB までにし、ゴリッと指の粒を大きく足す
BASS_LOW_SHELF_MAX = 3.0
BASS_GROWL = [{"type": "eq", "low": 0, "mid": 8.0, "midHz": 900, "high": 0},     # ゴリッ
              {"type": "eq", "low": 0, "mid": 6.0, "midHz": 1900, "high": 0},    # 指の粒
              {"type": "eq", "low": 0, "mid": -2.0, "midHz": 200, "high": 0}]    # こもり（100〜250Hz の出すぎ）
SAX_PATCHES = {"altoSax", "tenorSax", "bariSax", "sopranoSax"}
SAX_DB = 5.0           # 2026-10-24 人間「サックスの音かなり小さいからそれも大きくして」: 参考の音の EQ が 2.5k・5.4k・高い方を -3dB 削っていた分も戻す
SHAMISEN_DB = 4.0      # 2026-10-24 人間「三味線もっと音大きくていいよ」（はじく楽器の +6dB に、さらに）
DRUM_GAIN = 0.9
# 2026-10-23 人間「ピロピロ大きくなってないな…原因調べて」→ 原因は2つ:
#   (1) 作曲ソフトはパートの volume を 0.5 で頭打ちにする（ai-song.ts）。リード 1.03・速弾き 1.22・シタール 2.54 などは、すべて 0.5 で鳴っていた
#       （速弾きを何倍にしても、リードと同じ 0.5 のまま。和楽器が負けていたのも同じ理由）
#   (2) 速弾きのギターに、参考の音の「そのほかの楽器」の EQ（参考の曲のシンセ用。533Hz・2kHz・5.9kHz を -10〜-15dB、高い方を -11dB）が
#       掛かり、ギターの抜ける帯域がほとんど削られていた
#   直し: 速弾きは専用の音作り（TECH_CHAIN）にし、0.5 を超えた分は、パートの gainDb（チャンネルの音量。-12〜+18dB）で鳴らす。
#   ただしリードなどは、人間が今の大きさ（0.5 で頭打ちの音）を聞いて判断しているので、今のまま（0.5）にする
VOL_MAX = 0.5
TECH_DB = 3.0          # 速弾き: リードより 3dB 前に
FEATURE_DB_MAX = 6.0   # 主役の楽器（和楽器・サックスなど）: 0.5 を超えた分を最大 +6dB まで
# はじく楽器（三味線・琴など）は、鳴った瞬間だけ大きくすぐ消えるので、伸び続ける歪みギターと同じ「音量の数値」では、
#   耳ではずっと小さく聞こえる（2026-10-24 人間「和楽器の音小さい原因は何だ？」）。数値をそろえたうえで、さらに前へ出す
PLUCK = {"shamisen", "koto", "biwa", "harp", "xylophone", "marimba", "harpsichord", "musicBox"}
PLUCK_DB = 6.0         # はじく主役の楽器: 減衰のぶんを足す
PLUCK_BITE_HZ = (1500, 5500)   # 撥・爪の当たる帯域。参考の音の EQ で削らない（ここで抜ける）
TECH_CHAIN = [{"type": "filter", "kind": "highpass", "freq": 110, "q": 0.7},
              {"type": "eq", "low": 0, "mid": -2.5, "midHz": 320, "high": 0},
              {"type": "eq", "low": 0, "mid": 2.5, "midHz": 1800, "high": 0},
              {"type": "eq", "low": 0, "mid": -1.5, "midHz": 4500, "high": 0},
              {"type": "filter", "kind": "lowpass", "freq": 11000, "q": 0.6},
              {"type": "delay", "beats": 0.5, "mix": 0.12, "feedback": 0.2},
              {"type": "room", "mix": 0.1}]
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
        if group(p) == "bass":
            p["volume"] = round(p.get("volume", 0) * BASS_GAIN, 5)
            if p.get("instrument") == "bass" and not p.get("_bassed"):
                fx, free = [], []
                for f in p.get("fx", []):
                    f = dict(f)
                    if f.get("type") == "eq" and f.get("low", 0) > BASS_LOW_SHELF_MAX: f["low"] = BASS_LOW_SHELF_MAX
                    if f.get("type") == "eq" and BASS_MID_KEEP[0] <= f.get("midHz", 0) <= BASS_MID_KEEP[1] and f.get("mid", 0) < 0:
                        if not f.get("low") and not f.get("high"): free.append(len(fx))     # 削りだけの EQ は、ゴリッの EQ に置きかえる
                        f["mid"] = 0.0
                    fx.append(f)
                rest = []
                for g in BASS_GROWL:
                    if free: fx[free.pop(0)] = dict(g)
                    else: rest.append(dict(g))
                k = next((j for j, f in enumerate(fx) if f.get("type") == "filter" and f.get("kind") == "lowpass"), len(fx))
                p["fx"] = fx[:k] + rest + fx[k:]
                p["_bassed"] = True
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
            # リードの左右の別テイク（double）もやめる: 1本のリードを2本で重ねると、わずかなずれが歪みの中で揺れて濁り、チャンネルも2つ使う
            if p.get("double"): p["double"] = False
            p["release"] = 0.35
            p["reverb"] = max(p.get("reverb", 0), 0.25)
            if LEAD_AMP: p["amp"] = LEAD_AMP
            if "ハモリ" in p.get("role", ""):
                p["ampDrive"] = HARM_DRIVE
                p["pan"] = round(min(1.0, (p.get("pan") or 0) + 0.22), 2)   # 別のチャンネル＝別のアンプで鳴らす（同じアンプで3度が歪むと濁る）
                p["volume"] = round(p.get("volume", 0) * HARM_GAIN, 5)
            p["_toned"] = True
    for p in ps:
        p.pop("_feat", None); p.pop("_toned", None); p.pop("_bassed", None)
        fit_fx(p)
    return log


def chan_key(p):
    return tuple(p.get(k) for k in ("instrument", "patch", "pan", "reverb", "chorus", "bright", "duck", "detune", "attack", "release"))


def headroom(song):
    """速弾きの音作りを差しかえ、主役の楽器の深い削り（参考の曲のシンセ用の EQ）を浅くし、0.5 を超えた分を gainDb に移す"""
    import math
    log = []
    ps = song["parts"]
    for p in ps:
        if group(p) == "tech":
            p["fx"] = [dict(f) for f in TECH_CHAIN]; p["ampGate"] = min(p.get("ampGate", 10), 6)
        elif featured(p):
            pluck = p.get("instrument") in PLUCK
            fx = []
            for f in p.get("fx", []):
                if f.get("type") == "eq":
                    f = dict(f)
                    if f.get("mid", 0) < -6: f["mid"] = -3.0
                    if f.get("high", 0) < -6: f["high"] = -3.0
                    # 主役の楽器の「抜ける帯域」（1.5〜5.5kHz）と高い方は、参考の音の EQ で削らない（はじく楽器も、サックスも、ここで聞こえる）
                    if PLUCK_BITE_HZ[0] <= f.get("midHz", 0) <= PLUCK_BITE_HZ[1] and f.get("mid", 0) < 0: f["mid"] = 0.0
                    if f.get("high", 0) < 0: f["high"] = 0.0
                fx.append(f)
            if p.get("patch") in SAX_PATCHES:
                p["gainDb"] = round((p.get("gainDb") or 0) + SAX_DB, 2)
                log.append(f"{p.get('role')}（サックス）+{SAX_DB:.0f}dB・抜ける帯域を削らない")
            if pluck:
                fx.insert(1, {"type": "eq", "low": 0, "mid": 2.5, "midHz": 2800, "high": 0})     # 撥の当たりを前へ
                p["gainDb"] = round((p.get("gainDb") or 0) + PLUCK_DB + (SHAMISEN_DB if p.get("instrument") == "shamisen" else 0), 2)
                log.append(f"{p.get('role')}（はじく主役の楽器）+{PLUCK_DB:.0f}dB・撥の帯域を削らない")
            p["fx"] = fx
    # リードの組（旋律・ハモリ・オクターブ）は、組ごとまとめて 0.5 に収める。チャンネルごとに頭打ちにすると、
    #   ハモリ（0.45）が旋律（1.03→0.5）とほぼ同じ大きさになり、2本の重なりが前に出て濁っていた
    L = [p for p in ps if group(p) == "lead"]
    top = max([p.get("volume", 0) for p in L] or [0])
    if top > VOL_MAX:
        for p in L: p["volume"] = round(max(0.02, p["volume"] * VOL_MAX / top), 5)
        log.append(f"リードの組 ×{VOL_MAX / top:.3f}（比はそのまま）")
    # チャンネルごとに、いちばん大きいパートで gainDb を決め、同じチャンネルのパートは同じ gainDb・音量の比はそのまま
    chans = {}
    for p in ps:
        if p.get("instrument") in DRUMS: continue
        chans.setdefault(chan_key(p), []).append(p)
    for k, grp in chans.items():
        top = max(p.get("volume", 0) for p in grp)
        if top <= VOL_MAX: continue
        if any(group(p) == "tech" for p in grp): add = TECH_DB
        elif any(featured(p) for p in grp): add = min(FEATURE_DB_MAX, 20 * math.log10(top / VOL_MAX))
        else: add = 0.0
        scale = VOL_MAX / top
        for p in grp:
            p["volume"] = round(max(0.02, p.get("volume", 0) * scale), 5)
            if add: p["gainDb"] = round((p.get("gainDb") or 0) + add, 2)
        if add: log.append(f"{grp[0].get('role')} +{add:.1f}dB")
    return log


if __name__ == "__main__":
    path = sys.argv[1]
    song = json.load(open(path))
    # 曲ごとの音量の好み（<曲.json>.gains。例 {"drums": 0.97}。人間「16ドラムの音3落とそう」）
    import os
    gp = sys.argv[2] if len(sys.argv) > 2 else path + ".gains"
    gains_ = json.load(open(gp)) if os.path.exists(gp) else {}
    gtr_delay = gains_.pop("_guitar_delay", None)
    log = balance(song)
    log += headroom(song)
    # 曲ごとの音量の好みは、0.5 の頭打ちのあとに掛ける（前に掛けると、0.5 を超えているパートでは効かなかった。01 のリード -15% など）
    for g_, k_ in gains_.items():
        for p in song["parts"]:
            if group(p) == g_: p["volume"] = round(p.get("volume", 0) * k_, 5)
    # 曲ごとのリフのやまびこ（<曲.json>.gains の "_guitar_delay": 混ぜる量）。2026-10-23 人間（01）「ギターにほんの少しディレイ入れよう」「リフ」
    #   看板リフ（と透明感の層）だけに、付点8分のうすいやまびこを、アンプのあとに足す。やまびこはチャンネルごとなので、
    #   リズムのギターと同じチャンネルにならないよう、看板リフの残響をわずかに変えて別のチャンネルにする
    #   ただしチャンネルが足りない曲（01）では、別のチャンネルを増やすとハモリがリードのアンプに戻されて濁るので、
    #   看板リフと同じ旋律を重ねる「透明感の層」（もとから別のチャンネル）があれば、そこにだけ少し多め（1.4倍）に掛ける
    if gtr_delay:
        layer = [p for p in song["parts"] if p.get("instrument") in GUITARS and p.get("role", "").startswith("看板リフ（透明感")]
        for p in song["parts"]:
            if p.get("instrument") in GUITARS and p.get("role", "").startswith("看板リフ") and (not layer or p in layer):
                if p.get("role") == "看板リフ": p["reverb"] = round((p.get("reverb") or 0) + 0.01, 3)
                fx = p.setdefault("fx", [])
                if not any(f.get("type") in ("delay", "pingpong") for f in fx):
                    fx.append({"type": "delay", "beats": 0.75, "mix": round(gtr_delay * (1.4 if layer else 1.0), 3), "feedback": 0.22})
                    fit_fx(p)
        log.append(f"リフのやまびこ {gtr_delay}")
    json.dump(song, open(path, "w"), ensure_ascii=False)
    print("組の大きさを直しました:", ", ".join(log) or "（上限の内側）")
