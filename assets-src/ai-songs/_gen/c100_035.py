# ケルト・フルート100曲「銀の笛と百の夜」035 光る茸 Glowing Mushrooms — 第2版（2026-10-28）
# イメージ: 森の暗がりで、小さな茸がぽっ、ぽっと光りはじめる。光るたびに、場所が右になったり左になったりする（音の左右の位置が変わる）。
#   だんだん数が増え、最後は茸の光が輪になって、ぐるりと一周する（左から右へ回る分散和音）。
# 形（台帳）: 点描（灯る音ごとに左右の位置が変わる）→最後に光の輪。4/4・♩=54。B リディア（E♯の不思議な明るさ）。始め：暗闇（低い持続）／終わり：光の輪。山なし。
# 編曲の表:
#   暗闇   : 低い弦の持続だけ
#   ひとつ : 1小節に1つ、どこかで光る（グロッケン・竪琴の倍音を、左右5か所のどれかで）。笛はまばら
#   ふえる : 1小節に2〜3つ。笛の節
#   灯り   : 1小節に4つ。笛は高い所。弦がうすく
#   光の輪 : 左から右へ回る分散和音（5か所を順に）
import sys, json, random
from c100_common import *
from c100_v2 import *

S = Song("C100", "035-glowing-mushrooms", "光る茸", "Glowing Mushrooms", 54, 4, "B", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
C4_ = ["B", "C#/B", "B", "G#m"]
S.scene("暗闇", 3, "intro", ["B", "B", "B"])
S.scene("ひとつ", 12, "verse", C4_ * 3)
S.scene("ふえる", 16, "verse", C4_ * 4)
S.scene("灯り", 16, "chorus", ["E", "C#/B", "B", "G#m", "E", "F#", "B", "B"] * 2)
S.scene("光の輪", 8, "outro", ["B", "C#/B", "B", "B", "B", "B", "B", "B"])
NAMES = ["暗闇", "ひとつ", "ふえる", "灯り", "光の輪"]

c = make(S, NAMES,
         [("暗闇", 0, 0.6), ("ひとつ", 0, 0.62), ("ふえる", 0, 0.66), ("灯り", 0, 0.7), ("光の輪", 0, 0.7), ("光の輪", 7, 0.4)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="暗闇", passing=True, tension=False)
PANS = [-0.85, -0.45, 0.0, 0.45, 0.85]
DOTS = [S.track(f"光{i + 1}", "bell" if i % 2 == 0 else "harp", patch="glockenspiel" if i % 2 == 0 else "folkHarp",
                volume=0.03 if i % 2 == 0 else 0.07, pan=PANS[i], reverb=0.75, barGain=c.g()) for i in range(5)]
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.075, pan=0.0, reverb=0.5, barGain=c.g())

play_melody(c, "ひとつ", ["R:4", "R:2 5:2", "R:4", "3:4", "R:4", "R:2 4:2", "5:4", "R:4", "R:4", "R:2 1':2", "7:4", "R:4"], 4, "air", density=0.3, seed=3501)
play_melody(c, "ふえる", ["5:2 4:1 3:1", "2:2 3:2", "4:3 5:1", "3:4", "5:2 6:1 7:1", "1':2 7:2", "6:3 5:1", "5:4",
                         "3:2 4:1 5:1", "6:2 5:2", "4:2 3:2", "2:4", "3:2 4:1 3:1", "2:2 7,:2", "1:4", "R:4"], 4, "air", density=0.6, seed=3502)
play_melody(c, "灯り", ["5:2 6:1 7:1", "1':3 7:1", "6:2 5:2", "4:4", "5:2 7:1 1':1", "2':2 1':2", "7:3 6:1", "5:4",
                       "6:2 7:1 1':1", "7:2 6:2", "5:2 4:2", "3:4", "4:2 5:1 4:1", "3:2 2:2", "1:4", "R:4"], 4, "air", density=0.8, seed=3503)

rg = random.Random(35); B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b].split("/")[0]
    v = voice(ch, 50, 3, spread=True)
    if not (n == "光の輪" and i >= 6):
        for j in range(3 if n != "暗闇" else 2): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n != "暗闇" and not (n == "光の輪" and i >= 6): CELLO.bar(b, f"{nm(low(ch, 'C2') + 12)}:4")
    hi = tones(ch, "B5", "B6") if True else []
    cnt = {"ひとつ": 1, "ふえる": 2 + (i % 2), "灯り": 4}.get(n, 0)
    if cnt:
        slots = sorted(rg.sample(range(8), cnt))      # 8分の位置
        used = {}
        for sl in slots:
            d = rg.randrange(5); used.setdefault(d, []).append(sl)
        for d, sls in used.items():
            s, t0 = [], 0
            for sl in sls:
                if sl > t0: s.append(f"R:{(sl - t0) * 0.5:g}")
                s.append(f"{nm(rg.choice(hi) - (12 if d % 2 else 0))}:0.5"); t0 = sl + 1
            if t0 < 8: s.append(f"R:{(8 - t0) * 0.5:g}")
            DOTS[d].bar(b, " ".join(s))
    if n == "光の輪" and i < 6:   # 左から右へ回る分散和音
        arp = tones(ch, "B4", "B6")
        for q in range(8):
            d = q % 5 if (i % 2 == 0) else 4 - q % 5
            DOTS[d].at(b * B + q * 0.5, f"{nm(arp[(q + i) % len(arp)] - (12 if d % 2 else 0))}:0.5")
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の035（第2版）。森の暗がりで小さな茸が光る。4/4・♩=54、B リディア。点描：灯る音ごとに左右の位置が変わり（5か所）、数がだんだん増える。最後は茸の光が輪になって、左から右へ回る分散和音。",
       harm_scenes=None, tail_scene="光の輪", fill=False, pads=True, pad_scenes=["ふえる", "灯り", "光の輪"])
json.dump({"pre": 1.0, "tail": 8.0, "layers": [{"file": "0621", "db": -34, "hp": 120, "lp": 6000, "wide": 0.014, "duck": 0.3, "fade": 6}, {"file": "0424", "db": -40, "hp": 1500, "lp": 9000, "wide": 0.012, "pan": 0.3, "duck": 0.3, "fade": 6}],
           "fx": {"glass": {"hz": [493.9, 987.8, 1480.0], "db": -27, "rt": 7.0, "start": 3}, "shimmer": {"db": -26, "rt": 9.0}, "far": {"db": -24, "delay": 0.3, "lp": 2400, "rt": 5.0},
                  "haze": {"db": -26, "rt": 9.0}, "band": {"db": -37, "hz": 7000, "per": 23}}, "intro_db": 8.5}, open("/tmp/cel/w/air035.json", "w"))
