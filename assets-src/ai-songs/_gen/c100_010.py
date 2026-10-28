# ケルト・フルート100曲「銀の笛と百の夜」010 出航 Setting Sail — 第2版（2026-10-28）
# イメージ: 帆を上げる朝。綱を引く人々の行進の足どり（6/8 の行進）。帆が風をはらみ、船が岸を離れる（B：上の音域へ）。
#   もう一度行進の節が戻り、全員の力で岬を越える所で、ティンパニが転がり、1拍だけ全部が息をのむ。そして目の前に広い海原。
# 形（台帳）: 行進・物語型 A–A–B–B–A′–山–コーダ。6/8・付点4分＝52。G ミクソリディア（F♮の帆の色）。
# 編曲の表:
#   静けさ : 竪琴だけ（まだ岸に結ばれた船）
#   A1     : 笛の行進の節＋竪琴＋低い弦
#   A2     : ＋ピチカートの足どり（付点4分の行進）＋チェロ
#   B1     : 帆が風をはらむ：ホルンの長い和音、笛は上の音域
#   B2     : ＋弦のうねり。ティンパニが区切りで1打
#   A3     : 行進が全員で戻る（弦のトレモロ風の刻み）
#   山     : ティンパニのロール→1拍の無音
#   海原   : 広い海：笛の長い音、弦の広い和音、グロッケンと竪琴の倍音、遠いホルン
import sys
from c100_common import *
from c100_v2 import *

BPM = 156   # 8分音符＝156（付点4分＝52）
S = Song("C100", "010-setting-sail", "出航", "Setting Sail", BPM, 6, "G", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
AC = ["G", "C", "G", "Am", "F", "Dm", "F", "G", "G", "C", "Am", "F", "G", "Dm", "F", "G"]
BC = ["C", "G", "Dm", "Am", "C", "G", "F", "G", "C", "G", "F", "Em", "G", "C", "Dm", "G"]
S.scene("静けさ", 6, "intro", ["G", "G", "F", "G", "C", "G"])
S.scene("A1", 16, "verse", AC)
S.scene("A2", 16, "verse", AC)
S.scene("B1", 16, "chorus", BC)
S.scene("B2", 16, "chorus", BC)
S.scene("A3", 16, "verse", AC)
S.scene("山", 4, "break", ["F", "C", "D", "D"])
S.scene("海原", 16, "outro", ["G", "C", "G", "F", "G", "C", "F", "G", "G", "G", "C", "G", "G", "G", "G", "G"])
NAMES = ["静けさ", "A1", "A2", "B1", "B2", "A3", "山", "海原"]

c = make(S, NAMES,
         [("静けさ", 0, 0.58), ("A1", 0, 0.62), ("A2", 0, 0.68), ("B1", 0, 0.72), ("B2", 0, 0.78), ("A3", 0, 0.82), ("A3", 15, 0.86),
          ("山", 0, 0.88), ("山", 3, 0.95), ("海原", 0, 0.8), ("海原", 8, 0.66), ("海原", 15, 0.4)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="静けさ", passing=True, tension=False)
HORN = S.track("ホルン", "brass", patch="horn", volume=0.07, pan=-0.25, reverb=0.55, breath=False, attack=0.25, release=0.8, bright=-0.5, barGain=c.g())
HORN2 = S.track("ホルン2", "brass", patch="horn", volume=0.055, pan=-0.15, reverb=0.55, breath=False, attack=0.25, release=0.8, bright=-0.5, barGain=c.g())
TIMP = S.track("ティンパニ", "strings", patch="timpani", volume=0.1, pan=0, reverb=0.4, gainDb=-4, barGain=c.g())
PIZZ = S.track("ピチカート（足どり）", "strings", patch="pizzicato", volume=0.06, pan=-0.35, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.2, reverb=0.45, barGain=c.g())
GLOCK = S.track("グロッケン", "bell", patch="glockenspiel", volume=0.028, pan=0.35, reverb=0.7, barGain=c.g())

A = ["1:2 3:1 5:2 3:1", "4:2 6:1 5:3", "3:2 5:1 1':2 7:1", "6:3 5:3", "4:2 6:1 5:2 3:1", "2:2 4:1 3:2 1:1", "7,:2 2:1 5:2 4:1", "3:3 1:3",
     "1:2 3:1 5:2 3:1", "4:2 6:1 5:3", "1':2 7:1 6:2 5:1", "4:3 6:3", "5:2 3:1 1:2 3:1", "2:2 4:1 7,:2 2:1", "1:2 5,:1 7,:2 2:1", "1:6"]
Bm = ["5:3 1':3", "7:2 6:1 5:3", "6:3 2':3", "1':2 7:1 6:3", "5:2 6:1 7:2 1':1", "2':3 1':3", "7:2 6:1 5:2 4:1", "5:6",
      "5:3 1':3", "2':2 1':1 7:3", "6:2 7:1 1':2 2':1", "3':6", "2':2 1':1 7:2 6:1", "5:2 4:1 3:3", "2:2 3:1 4:2 7,:1", "1:6"]
play_melody(c, "A1", A, 4, "jig", density=0.4, seed=1001)
play_melody(c, "A2", A, 4, "jig", density=0.7, seed=1002)
play_melody(c, "B1", Bm, 4, "air", density=0.6, seed=1003)
play_melody(c, "B2", Bm, 4, "air", density=0.9, seed=1004)
play_melody(c, "A3", A, 4, "jig", density=0.9, seed=1005)
play_melody(c, "山", ["4:6", "5:6", "6:6", "6:5 R:1"], 4, "air", density=0)
play_melody(c, "海原", ["1':6", "3':6", "2':3 1':3", "7:6", "1':6", "6:3 5:3", "4:6", "5:6", "1':6", "R:6", "5:6", "1':6", "R:6", "R:6", "R:6", "R:6"], 4, "air", density=0.6, seed=1006)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D6")
    if n == "静けさ":
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[2], t[4 % len(t)], t[2])))
        continue
    if n in ("A1", "A2", "A3"):
        c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:1 {nm(t[4 % len(t)])}:2 {nm(t[2])}:1")
        v = voice(ch, 50 if n != "A3" else 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6" if n != "A3" else " ".join(f"{nm(v[j])}:1" for _ in range(6)))
        if n != "A1": PIZZ.bar(b, f"{nm(r + 12)}:3 {nm(r + 19)}:3"); CELLO.bar(b, f"{nm(r)}:6")
    if n in ("B1", "B2"):
        h = tones(ch, "G3", "G4"); HORN.bar(b, f"{nm(h[0])}:6"); HORN2.bar(b, f"{nm(h[1])}:6")
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[5 % len(t)], t[4 % len(t)], t[2])))
        CELLO.bar(b, f"{nm(r)}:6")
        if n == "B2":
            v = voice(ch, 57, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
            if i % 8 == 7: TIMP.bar(b, f"R:3 {nm(r)}:3")
    if n == "A3" and i % 4 == 0: TIMP.bar(b, f"{nm(r)}:3 R:3")
    if n == "山":
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        h = tones(ch, "G3", "G4"); HORN.bar(b, f"{nm(h[0])}:6"); HORN2.bar(b, f"{nm(h[1])}:6")
        CELLO.bar(b, f"{nm(r)}:6")
        if i >= 2: TIMP.bar(b, " ".join("D3:0.5" for _ in range(12 if i == 2 else 10)) + (" R:1" if i == 3 else ""))
    if n == "海原":
        v = voice(ch, 60, 3, spread=True)
        if i < 14:
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
            CELLO.bar(b, f"{nm(r)}:6")
        if i < 8: h = tones(ch, "G3", "G4"); HORN.bar(b, f"{nm(h[0])}:6")
        if i % 2 == 0 and i < 12: GLOCK.bar(b, f"{nm(tones(ch, 'C6', 'C7')[i // 2 % 3])}:6")
        if i % 2 == 1 and i < 13: c.HARP2.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "G4", "G6")[:6]))
# 山の最後の1拍：全部が息をのむ
c.SIL.add(c.s0["山"] + 3, 5, 6)
rich(c, choir_scenes=["B2", "A3"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.25 --side-hpf 220",
       "ケルト・フルート100曲の010（第2版）。帆を上げて船が海へ出る。6/8 の行進（付点4分＝52）、G ミクソリディア。A–A–B–B–A′：竪琴だけの静けさ→行進の節→帆が風をはらむ（ホルン）→全員の行進→ティンパニのロールと1拍の無音→広い海原。",
       harm_scenes=None, tail_scene="海原", fill=False, pads=True, pad_scenes=["B1", "B2", "A3", "海原"])
