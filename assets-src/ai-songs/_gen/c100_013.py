# ケルト・フルート100曲「銀の笛と百の夜」013 丘の上の孤独 Alone on the Hill（2026-10-28）。表は docs/sound/celtic-flute-100-plan.md
# 物語: 丘の上に一人きりの羊飼い。広い空の下で、誰に聞かせるでもなく、ぽつりぽつりと独り言を笛で語る。チェロが少し離れて、低い声で相づちを打つ。
# 型: 低い声域の静かな語り。笛は E4〜G5 の低めの所だけで書ききる（始め：低い笛／終わり：同じ低い笛）。山なし。
#     笛は001と同じく一音ずつなめらかに。チェロの対旋律は2分音符で一歩ずつ動く。重ね方は「音の重ね方の勉強ノート」どおり。
import sys
from c100_common import *

S = Song("C100", "013-alone-on-the-hill", "丘の上の孤独", "Alone on the Hill", 50, 4, "E", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.scene("独り言", 4, "intro", ["Em", "Em", "C", "Em"])
S.scene("語り", 16, "verse", ["Em", "C", "G", "D", "Em", "Am", "Bm", "Em", "C", "G", "Am", "Em", "C", "D", "Em", "Em"])
S.scene("思い", 16, "verse", ["Am", "Em", "C", "G", "Am", "D", "G", "G", "C", "Bm", "Am", "Em", "Am", "Bm", "Em", "Em"])
S.scene("空", 16, "chorus", ["Cmaj7", "G", "D", "Em", "C", "D", "D", "D", "Am", "Em", "C", "G", "Am", "Bm", "Em", "Em"])
S.scene("独り言に戻る", 8, "outro", ["Em", "Am", "Em", "Em", "Em", "Em", "Em", "Em"])
NAMES = ["独り言", "語り", "思い", "空", "独り言に戻る"]

c = make(S, NAMES,
         [("独り言", 0, 0.62), ("語り", 0, 0.62), ("思い", 0, 0.66), ("空", 0, 0.7), ("空", 15, 0.66), ("独り言に戻る", 0, 0.56), ("独り言に戻る", 7, 0.3)],
         {"語り": 0.58, "思い": 0.6, "空": 0.62, "独り言に戻る": 0.55},
         flute_gain={"独り言": 1.3, "語り": 1.35, "思い": 1.3, "空": 1.25, "独り言に戻る": 1.25}, intro="独り言", passing=True, tension=True)
FA = S.track("笛の和音1", "panflute", patch="flute", volume=0.15, bright=-0.9, pan=-0.35, reverb=0.65, breath=False, mono=True, barGain=c.g())
FB = S.track("笛の和音2", "panflute", patch="flute", volume=0.13, bright=-0.9, pan=0.35, reverb=0.65, breath=False, mono=True, barGain=c.g())
CELLO = S.track("チェロ（相づち）", "strings", patch="cello", volume=0.085, pan=0.25, reverb=0.45, barGain=c.g())

# ---------- 笛（E エオリア。低めの所だけ） ----------
put_bars(c, "独り言", ["R:1 1:1 2:1 3:1", "2:3 R:1", "3:1 2:1 1:1 2:1", "1:3 R:1"], 4)
put_melody(c, "語り", [
    ["1:1 3:1 5:1 3:1", "6:1 5:1 4:1 3:1", "3:1 5:1 7:1 5:1", "4:3 R:1"],
    ["5:1 3:1 1:1 3:1", "4:1 6:1 1':1 6:1", "5:1 4:1 2:1 4:1", "3:3 R:1"],
    ["3:1 5:1 6:1 5:1", "3:1 5:1 7:1 5:1", "4:1 6:1 1':1 6:1", "5:3 R:1"],
    ["6:1 5:1 3:1 6:1", "7:1 6:1 4:1 2:1", "3:1 2:1 1:1 2:1", "1:3 R:1"]], 4)
put_melody(c, "思い", [
    ["4:1 6:1 1':1 6:1", "5:1 3:1 1:1 3:1", "3:1 5:1 6:1 5:1", "7:3 R:1"],
    ["1':1 6:1 4:1 6:1", "7:1 4:1 2:1 4:1", "3:1 5:1 7:1 5:1", "3:3 R:1"],
    ["6:1 1':1 3':1 1':1", "2':1 1':1 7:1 5:1", "6:1 4:1 1:1 4:1", "5:3 R:1"],
    ["4:1 6:1 1':1 6:1", "5:1 7:1 2':1 7:1", "1':1 7:1 5:1 3:1", "1:3 R:1"]], 4)
put_melody(c, "空", [
    ["3:1 5:1 7:1 1':1", "7:1 5:1 3:1 5:1", "4:1 6:1 7:1 6:1", "5:3 R:1"],
    ["6:1 1':1 3':1 1':1", "7:1 1':1 7:1 5:1", "4:1 6:1 2':1 6:1", "4:3 R:1"],
    ["1':1 6:1 4:1 6:1", "5:1 7:1 1':1 7:1", "6:1 5:1 3:1 5:1", "7:3 R:1"],
    ["6:1 4:1 1:1 4:1", "5:1 4:1 2:1 4:1", "3:1 2:1 1:1 2:1", "1:3 R:1"]], 4)
put_bars(c, "独り言に戻る", ["3:1 2:1 1:2", "R:4", "2:1 3:1 1:2", "R:4", "1:4", "R:4", "R:4", "R:4"], 4)

# ---------- 伴奏（チェロの相づち＝2分音符で一歩ずつ動く対旋律） ----------
prev = 52
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lo = low(ch, "C2"); t = tones(ch, "D3", "D6")
    if n == "独り言":   # 始まり：笛だけの和音（3本の笛がのばす）の上で、低い笛が独り言をはじめる
        w = voice(ch, 62, 2, spread=False)
        FA.bar(b, f"{nm(w[0])}:4"); FB.bar(b, f"{nm(w[1])}:4")
        continue
    v = voice(ch, 55, 3, spread=True)
    for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n != "独り言" and not (n == "独り言に戻る" and i >= 6):
        cand = [m for m in range(43, 60) if m % 12 in chord_pcs(ch.split("|")[0])]
        a = min(cand, key=lambda m: abs(m - prev)); z = min([m for m in cand if m != a], key=lambda m: abs(m - a))
        CELLO.bar(b, f"{nm(a)}:2 {nm(z)}:2"); prev = z
    if n in ("語り", "思い", "空"):
        c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2" if i % 2 == 0 else f"R:2 {nm(t[1])}:2")
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
    elif n == "独り言に戻る" and i in (0, 2):
        c.HARP.bar(b, f"{nm(t[0])}:4")

rich(c, choir_scenes=["思い", "空"], pulse_scenes=["思い", "空"], guitar=False)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0",
       "ケルト・フルート100曲の013。丘の上に一人きりの羊飼い。E エオリア・50。低めの所だけで語る笛に、チェロが少し離れて相づちを打つ。山なし。",
       harm_scenes=["語り", "思い", "空"], tail_scene="独り言に戻る")
