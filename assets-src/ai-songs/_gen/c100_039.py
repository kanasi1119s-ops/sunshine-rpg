# ケルト・フルート100曲「銀の笛と百の夜」039 妖精の輪 The Fairy Ring — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 夜明け前、森のはずれの草地に、きのこが輪になって生えている（妖精の輪）。輪のまん中の小さな塚の中から、
#   壁ごしのような、こもった音楽が聞こえてくる。大きく跳ねる、人には吹けないような節。エイラは耳で覚えて、自分の笛で吹き直す。
#   吹き直すうちに村の音楽（ギターとボーラン）が加わり、最後は妖精の音楽と人の音楽がひとつの輪になって踊る。
# 調べ: 喜び。形: 妖精の塚から聞き覚え（遠い曲 → エイラが吹き直す → 全員の輪）。ジグ（6/8）A・B 8小節ずつ。
# 拍子・速さ: 6/8・付点4分＝112（1拍＝付点4分、1小節＝2拍で書く。8分は 1/3 拍）。旋法: E ドリア → 輪で E ミクソリディア（G が G♯ に）。
# 主役は笛（遠い曲をまねる笛）。伴奏の主役: 遠い層（こもった竪琴とホイッスル。高い音を削って、塚の中から聞こえるように）
#   → 近い層（ナイロン弦ギターとボーラン）。ピアノ・弦・パッドは使わない。
# この曲だけ: 妖精の旋律は大きく跳ぶ（オクターブ・6度）。エイラが吹き直すと、同じ音のまま近いオクターブに置きかわり、なめらかになる。
# 始まり: 壁の向こうのこもった曲 → 終わり: 全員の輪（妖精の節とエイラの節が重なる）。
# 山: 終盤に1つ（輪）。
import sys, json, re
from c100_common import *
from c100_v2 import *
import c100_v2 as _v2
_oc = _v2.open_chord
_v2.open_chord = lambda ch, lo=52, hi=76: _oc(ch, lo, hi)

BPM = 112
S = Song("C100", "039-the-fairy-ring", "妖精の輪", "The Fairy Ring", BPM, 2, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
KD, KM = Key("E", "dorian", 4), Key("E", "mixolydian", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["Em", "D", "Em", "Bm", "Em", "D", "A", "Em"]
CB = ["Em", "D", "A", "Bm", "G", "D", "A", "Em"]
CAm = [x.replace("Em", "E").replace("Bm", "B") for x in CA]; CBm = [x.replace("Em", "E").replace("Bm", "B").replace("G", "E") for x in CB]
AB, ABm = CA + CA + CB + CB, CAm + CAm + CBm + CBm
SC = [("壁の向こう", 32, "intro", AB), ("聞き覚え", 32, "verse", AB), ("吹き直す", 64, "verse", AB * 2), ("輪", 64, "chorus", ABm * 2),
      ("輪のしめくくり", 32, "chorus", ABm), ("止まる", 2, "outro", ["E", "E"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("壁の向こう", 0, 0.66), ("聞き覚え", 0, 0.7), ("吹き直す", 0, 0.76), ("吹き直す", 63, 0.8), ("輪", 0, 0.86), ("輪", 63, 0.92),
          ("輪のしめくくり", 0, 0.92), ("輪のしめくくり", 31, 0.94), ("止まる", 0, 0.9)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="壁の向こう", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: こもった竪琴（0.09）は笛より約10dB 大きい → 0.035。ギター1本（0.03）も笛より大きい（5本重なる）→ 0.015。ボーランは笛と同じくらい
MUF = [{"type": "eq", "low": -2, "mid": -4, "midHz": 1800, "high": -15}]           # 塚の中：高い音を削る
FARG = [round(x * (2.0 if b < 32 else 1.0), 3) for b, x in enumerate(G)]           # 壁の向こうだけの所は大きめに（前奏が小さくならないよう）
FH = S.track("こもった竪琴（塚の中）", "harp", patch="folkHarp", volume=0.035, pan=-0.35, reverb=0.85, sustain=1.6, fx=MUF, barGain=FARG)
FW = S.track("こもったホイッスル（塚の中）", "panflute", patch="tinWhistle", volume=0.03, pan=0.35, reverb=0.85, fx=MUF, barGain=FARG)
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.015, pan=0.3 + 0.05 * i, reverb=0.3, barGain=G) for i in range(5)]
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.12 + 0.08 * j, reverb=0.3, barGain=G) for j in range(2)]

# ---------- 妖精の節（大きく跳ぶ。E ドリア。1=E4。8分＝1、1小節＝6） ----------
FA = ["1:2 5:1 1':2 5:1", "3':2 2':1 7:3", "6:2 2:1 6:2 2:1", "5:3 1:3", "1:2 1':1 7:2 3:1", "6:2 1:1 5:3", "4:2 1':1 6:2 2:1", "1:6"]
FB = ["5:2 1':1 3':2 1':1", "2':2 5:1 7:3", "1':2 4:1 6:2 2:1", "5:3 2':3", "3':2 1':1 6:2 3:1", "4:2 1':1 7:3", "6:2 2:1 5:2 7,:1", "1:6"]
FAIRY = FA + FA + FB + FB

def events(bars, key, start_bar, oct_=4):
    ev = []
    for j, s_ in enumerate(e2b(bars)):
        ev += mel_events(key, s_, oct_, (start_bar + j) * B)
    return [[round(t, 4), L, m] for t, L, m in ev]
def smooth(ev):
    """吹き直し：同じ音のまま、前の音にいちばん近いオクターブに置きかえる（大きな跳躍がなめらかになる）"""
    out = []; prev = None
    for t, L, m in ev:
        if prev is not None:
            while m - prev > 6: m -= 12
            while prev - m > 6: m += 12
            m = max(62, min(83, m))
        out.append([t, L, m]); prev = m
    return out

# 壁の向こう：妖精の節（こもった竪琴とホイッスル）
for t, L, m in events(FAIRY, KD, c.s0["壁の向こう"], 4):
    FH.at(t, f"{nm(m)}:{round(L, 4)}")
    if L >= 0.6: FW.at(round(t + 0.01, 4), f"{nm(m + 12 if m + 12 <= 93 else m)}:{round(min(L, 0.6), 4)},")
# 聞き覚え：妖精の節はつづき（小さく）、エイラが句の頭だけ追う → 後半は全部
s0 = c.s0["聞き覚え"]
for t, L, m in events(FAIRY, KD, s0, 4):
    FH.at(t, f"{nm(m)}:{round(L, 4)},")
ev = smooth(events(FAIRY, KD, s0, 4))
ev = [e for e in ev if (int(e[0] // B) - s0) % 8 < 3 or int(e[0] // B) - s0 >= 16]
play(c.FLUTE, ornament(ev, KD, BPM, "march", B, density=0.25, seed=3901))
# 吹き直す：エイラのなめらかな節（2回）。遠い層は少しずつ遠ざかる（頭の小節だけ）
s0 = c.s0["吹き直す"]
for rep in range(2):
    ev = smooth(events(FAIRY, KD, s0 + 32 * rep, 4))
    play(c.FLUTE, ornament(ev, KD, BPM, "march", B, density=0.4 + 0.1 * rep, seed=3902 + rep))
    for t, L, m in events(FAIRY, KD, s0 + 32 * rep, 4):
        if (int(t // B) - s0) % 8 == 0: FH.at(t, f"{nm(m)}:{round(L, 4)},")
# 輪：E ミクソリディア。エイラのなめらかな節と、妖精の跳ぶ節が重なる（妖精は1オクターブ下の竪琴で）
for nn in ("輪", "輪のしめくくり"):
    s0 = c.s0[nn]; reps = c.sc_len[nn] // 32
    for rep in range(reps):
        ev = smooth(events(FAIRY, KM, s0 + 32 * rep, 4))
        play(c.FLUTE, ornament(ev, KM, BPM, "march", B, density=0.55, seed=3910 + rep + len(nn)))
        for t, L, m in events(FAIRY, KM, s0 + 32 * rep, 4):
            FH.at(t, f"{nm(m - 12 if m - 12 >= 48 else m)}:{round(L, 4)}")
s0 = c.s0["止まる"]
c.FLUTE.at(s0 * B, "E5:1!"); FH.at(s0 * B, "E4:1!")

# ---------- 近い層：ギター（吹き直すから）とボーラン（輪から） ----------
JIG = [(0, 2 * T3, "d", "!"), (2 * T3, T3, "u", ","), (1, 2 * T3, "d", ""), (1 + 2 * T3, T3, "u", ",")]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    if n in ("吹き直す", "輪", "輪のしめくくり"):
        strum(GT, b, B, ch, JIG if n != "吹き直す" or i >= 16 else [(0, 2, "d", ",")])
    if n in ("輪", "輪のしめくくり"):
        tr = DR[b % 2]
        tr.bar(b, f"C3:{round(T3, 4)}! E3:{round(T3, 4)}, C3:{round(T3, 4)}, C3:{round(T3, 4)}! E3:{round(T3, 4)}, C3:{round(T3, 4)},")
    if n == "止まる" and i == 0:
        strum(GT, b, B, ch, [(0, 1, "d", "!")]); DR[0].at(b * B, "C3:1!")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の039（第3版）。森のはずれの妖精の輪。塚の中から、壁ごしのようにこもった音楽が聞こえる（竪琴とホイッスル、高い音を削って）。妖精の節は大きく跳ぶ。エイラは耳で覚え、同じ音のまま近いオクターブに置きかえて、なめらかに吹き直す。ジグ（6/8・付点4分＝112）、E ドリア。村のギターとボーランが加わり、最後は E ミクソリディアの明るい輪になって、妖精の節とエイラの節が重なる。",
       harm_scenes=None, tail_scene="止まる", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.22, "lp": 3000, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air039.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
