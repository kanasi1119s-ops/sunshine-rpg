# ケルト・フルート100曲「銀の笛と百の夜」022 止まった水車 The Silent Mill — 第3版（2026-10-29: 7.03→ 回る1から弦、内声、回る2から笛の和声、床）
# イメージ: 錆びついて止まった水車小屋。最初は拍がない（時間が止まっている）。笛が水車に話しかけるように歌うと、
#   木がきしみ、輪がぎくしゃくと動きはじめる。ゆっくり→だんだん速く回りだした瞬間に3拍子が始まる。最後は勢いよく回り続ける（山）。
# 形（台帳）: 拍のない前奏→水車が回りだす瞬間に3拍子が始まり、だんだん回る。3/4・♩=40→60（回りだすところで速くなる）。D エオリア。終盤に山。
# 編曲の表:
#   静止     : 低い弦のドローンだけ。笛が拍のない語りかけ（長い音）
#   軋み     : 木のきしみ（空気の層の録音）。竪琴の低い音が1小節に1つ（輪が少し動く）
#   回りだす : テンポが40→60へ。ピチカートと竪琴が「ドン・チャ・チャ」の3拍子を刻みはじめる
#   回る1    : 笛の3拍子の旋律。チェロ
#   回る2    : ＋弦。笛の装飾
#   山       : 全員。笛は高い所で（いちばん勢いよく回る）
#   回転     : 回り続けたまま、少しずつ遠ざかる
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "022-the-silent-mill", "止まった水車", "The Silent Mill", 40, 3, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
S.tempo = [{"bar": 13, "bpm": 60, "ramp": 8}]
WC = ["Dm", "C", "Dm", "Am", "Dm", "Bb", "C", "Dm", "F", "C", "Dm", "Am", "Bb", "C", "Am", "Dm"]
S.scene("静止", 8, "intro", ["Dm"] * 8)
S.scene("軋み", 4, "break", ["Dm", "Dm", "C", "Dm"])
S.scene("回りだす", 8, "verse", ["Dm", "Dm", "C", "Dm", "Dm", "Bb", "C", "Dm"])
S.scene("回る1", 16, "verse", WC)
S.scene("回る2", 16, "verse", WC)
S.scene("山", 8, "chorus", ["Bb", "C", "Dm", "Am", "Bb", "C", "Dm", "Dm"])
S.scene("回転", 16, "outro", ["Dm", "C", "Dm", "Am", "Dm", "Bb", "C", "Dm", "Dm", "C", "Dm", "Dm", "Dm", "C", "Dm", "Dm"])
NAMES = ["静止", "軋み", "回りだす", "回る1", "回る2", "山", "回転"]

c = make(S, NAMES,
         [("静止", 0, 0.6), ("軋み", 0, 0.6), ("回りだす", 0, 0.62), ("回りだす", 7, 0.7), ("回る1", 0, 0.7), ("回る2", 0, 0.76), ("山", 0, 0.84), ("山", 5, 0.95),
          ("回転", 0, 0.8), ("回転", 15, 0.45)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="静止", passing=True, tension=False)
S.extra["rubato"] = 0.0
PIZZ = S.track("ピチカート（回る）", "strings", patch="pizzicato", volume=0.07, pan=-0.3, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.2, reverb=0.45, barGain=c.g())
DR = [S.track(f"ドローン{i + 1}", "strings", patch="slowStrings", volume=0.11, pan=[-0.4, 0.4][i], reverb=0.6, barGain=c.g()) for i in range(2)]

W1 = ["1:1 2:1 3:1", "5:2 4:1", "3:1 2:1 1:1", "7,:3", "1:1 3:1 5:1", "6:2 5:1", "4:1 3:1 2:1", "3:3",
      "5:1 6:1 7:1", "1':2 7:1", "6:1 5:1 4:1", "5:3", "4:1 3:1 2:1", "3:1 2:1 1:1", "7,:1 1:1 2:1", "1:3"]
W2 = ["3:1 4:1 5:1", "7:2 6:1", "5:1 4:1 3:1", "2:3", "3:1 5:1 7:1", "1':2 7:1", "6:1 5:1 4:1", "5:3"]
play_melody(c, "静止", ["R:3", "5:3", "4:1.5 3:1.5", "2:3", "R:3", "1:3", "7,:1.5 1:1.5", "2:3"], 4, "air", density=0.6, seed=2201)
play_melody(c, "軋み", ["3:3", "R:1.5 2:1.5", "5:3", "4:3"], 4, "air", density=0.4, seed=2207)   # 笛が水車に「起きて」と呼びかける
play_melody(c, "回りだす", ["5:3", "R:3", "3:1.5 4:1.5", "5:3", "1:1 2:1 3:1", "5:3", "4:1 3:1 2:1", "1:3"], 4, "air", density=0.4, seed=2202)
play_melody(c, "回る1", W1, 4, "air", density=0.6, seed=2203)
play_melody(c, "回る2", W1, 4, "air", density=1.0, seed=2204)
play_melody(c, "山", W2, 4, "air", density=1.0, seed=2205)
play_melody(c, "回転", W1[:8] + ["1:1 2:1 3:1", "5:2 4:1", "3:1 2:1 1:1", "1:3", "R:3", "R:3", "R:3", "R:3"], 4, "air", density=0.5, seed=2206)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D5")
    if n in ("静止", "軋み"):
        drone(DR, b, B, 50)
        CELLO.bar(b, "D2:3")
        v = voice(ch, 53, 3, spread=True)       # 止まった時間の中の、ひんやりした小屋の空気
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
        if n == "軋み": c.HARP.bar(b, f"{nm(r)}:1 R:2" if i % 2 == 0 else f"R:1 {nm(r)}:2")
        continue
    if n == "回りだす":
        drone(DR, b, B, 50)
        PIZZ.bar(b, f"{nm(r)}:1 R:2" if i < 2 else (f"{nm(r)}:1 {nm(t[1])}:1 R:1" if i < 4 else f"{nm(r)}:1 {nm(t[1])}:1 {nm(t[2])}:1"))
        c.HARP.bar(b, f"{nm(r)}:3" if i < 4 else f"{nm(r)}:1 {nm(t[2])}:1 {nm(t[3 % len(t)])}:1")
        CELLO.bar(b, f"{nm(r)}:3")
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
        continue
    PIZZ.bar(b, f"{nm(r)}:1 {nm(t[1])}:1 {nm(t[2])}:1")
    c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[0], t[2], t[4 % len(t)], t[2], t[3 % len(t)], t[2])) if n != "回転" or i < 14 else f"{nm(r)}:3")
    CELLO.bar(b, f"{nm(r)}:3")
    if n in ("回る1", "回る2", "山", "回転"):
        v = voice(ch, 57 if n != "回る1" else 54, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
rich(c, choir_scenes=["回る2", "山"], pulse_scenes=["回る1", "回る2", "山"], guitar=False, pizz=False, inner=True)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の022（第2版）。錆びて止まった水車が、笛の語りかけで回りだす。拍のない前奏（低いドローンときしみ）→回りだす瞬間に3拍子が始まり、テンポが♩=40→60へ。D エオリア。最後は勢いよく回る（山）。",
       harm_scenes=None, tail_scene="回転", fill=False, pads=True, pad_scenes=["軋み", "回りだす", "回る1", "回る2", "山", "回転"], floor=True)
# 空気：きしみ（戸棚・ドアのきしみの録音）を軋みの場面と回りだしに
sec_bar = 3 * 60 / 40
t_kishi = 8 * sec_bar
ev = [{"t": round(t_kishi + 0.3, 2), "file": "0306", "db": -22, "len": 3.5, "pan": -0.2, "seek": 0.3, "hp": 150, "lp": 6000},
      {"t": round(t_kishi + 2 * sec_bar, 2), "file": "0305", "db": -24, "len": 2.5, "pan": 0.25, "seek": 0.2, "hp": 150, "lp": 6000},
      {"t": round(t_kishi + 4 * sec_bar + 1.0, 2), "file": "0306", "db": -26, "len": 2.5, "pan": -0.1, "seek": 1.5, "hp": 150, "lp": 5000}]
air = {"pre": 1.0, "tail": 7.0, "layers": [{"file": "0864", "db": -35, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 10}],
       "events": ev,
       "fx": {"glass": {"hz": [293.7, 587.3, 880.0], "db": -28, "rt": 6.0, "start": 4}, "shimmer": {"db": -27, "rt": 8.0},
              "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5}, "haze": {"db": -27, "rt": 8.0}, "band": {"db": -37, "hz": 6500, "per": 23}}, "intro_db": 8.5}
json.dump(air, open("/tmp/cel/w/air022.json", "w"), ensure_ascii=False)
