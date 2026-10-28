# ケルト・フルート100曲「銀の笛と百の夜」013 丘の上の孤独 Alone on the Hill — 第2版の試作（ゆったりした曲）（2026-10-28）
# 物語: 丘の上に一人きりの羊飼い。最初は誰もいない所で、ドローンだけを相手に節を歌う（エア）。
#       2回目は遠くの竪琴とチェロが、少し離れて答える。空を見上げる所（B）で、3本の笛が和音になって広がり、
#       最後はまた一人に戻って、最初の節の前半だけを吹いて止める。
# 形: 「独奏のエア→合奏」（docs/sound/celtic-study の D①）。3/4・♩=56、ゆるやかなテンポのゆれ（rubato）。
#     旋律は AABA（Bで上のオクターブへ持ち上がる。Bの最後の2小節は Aの結び）。笛の装飾はエア用（すべり込み・ゆっくりした tap）。
# 編曲の表:
#   前置き  : 低いチェロの E のドローンだけ（2小節）→ 笛の弱起
#   語り1   : 笛＋チェロのドローン（E と B）だけ。AABA
#   語り2   : 竪琴（根音と、区切りでロールした和音）＋チェロの対旋律（笛と反対向きに2分音符で動く）。Bから弦が小さく
#   空      : Bを3本の笛の和音（コラール）で。最後のAは全員で、笛は1オクターブ上を少し
#   ひとりに戻る: 笛とドローンだけ。Aの前半4小節＋結び
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "013-alone-on-the-hill", "丘の上の孤独", "Alone on the Hill", 56, 3, "E", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"rubato": 0.45, "human": 0.45})
A1 = ["Em", "Em", "C", "D", "Em", "Em", "D", "Em"]
A2 = ["Em", "Em", "C", "D", "Em", "C", "D", "Em"]
BB = ["G", "G", "D", "Em", "C", "C", "D", "Em"]
S.scene("前置き", 3, "intro", ["Em", "Em", "Em"])
S.scene("語り1", 32, "verse", A1 + A2 + BB + A2)
S.scene("語り2", 32, "verse", A1 + A2 + BB + A2)
S.scene("空", 16, "chorus", BB + A2)
S.scene("ひとりに戻る", 7, "outro", ["Em", "Em", "C", "D", "Em", "Em", "Em"])
NAMES = ["前置き", "語り1", "語り2", "空", "ひとりに戻る"]

c = make(S, NAMES,
         [("前置き", 0, 0.6), ("語り1", 0, 0.62), ("語り1", 20, 0.7), ("語り1", 31, 0.62), ("語り2", 0, 0.66), ("語り2", 20, 0.76), ("語り2", 31, 0.68),
          ("空", 0, 0.78), ("空", 4, 0.9), ("空", 15, 0.72), ("ひとりに戻る", 0, 0.62), ("ひとりに戻る", 6, 0.4)],
         {}, flute_gain={n: 1.25 for n in NAMES}, intro="前置き", passing=True, tension=False)
CELLO = S.track("チェロ（ドローンと対旋律）", "strings", patch="cello", volume=0.11, pan=0.2, reverb=0.45, barGain=c.g())
CELLO2 = S.track("チェロ（5度）", "strings", patch="cello", volume=0.06, pan=-0.1, reverb=0.45, barGain=c.g())
DR = [S.track(f"ドローン（弦）{i + 1}", "strings", patch="slowStrings", volume=0.05, pan=[-0.4, 0.4][i], reverb=0.6, barGain=c.g()) for i in range(2)]
FA = S.track("笛の和音1", "panflute", patch="flute", volume=0.16, bright=-0.9, pan=-0.35, reverb=0.65, breath=False, mono=True, noRestrike=True, sustain=1.12, barGain=c.g())
FB = S.track("笛の和音2", "panflute", patch="flute", volume=0.14, bright=-0.9, pan=0.35, reverb=0.65, breath=False, mono=True, noRestrike=True, sustain=1.12, barGain=c.g())

# ---------- 旋律（E エオリア・3/4。弱起から） ----------
L_A1 = ["5,:1 1:1.5 2:0.5", "3:2 2:0.5 1:0.5", "6,:1.5 7,:0.5 1:1", "2:3",
        "5,:1 1:1.5 2:0.5", "3:1 5:1.5 4:0.5", "3:1 2:1 7,:1", "1:2 5,:1"]
L_A2 = ["5,:1 1:1.5 2:0.5", "3:2 2:0.5 1:0.5", "6,:1.5 7,:0.5 1:1", "2:3",
        "5,:1 1:1.5 2:0.5", "3:1 5:1 6:1", "5:1.5 3:0.5 2:1", "1:2 3:0.5 5:0.5"]
L_B = ["5:1 6:1 7:1", "1':2 7:0.5 6:0.5", "5:1 6:1.5 7:0.5", "2':2 1':1",
       "7:1.5 6:0.5 5:1", "6:1 4:1 2:1", "3:1 2:1 7,:1", "1:2 5,:1"]
L_A3 = L_A2[:7] + ["1:3"]
play_melody(c, "前置き", ["R:3", "R:3", "R:2 5,:1"], 4, "air", density=0)
play_melody(c, "語り1", L_A1 + L_A2 + L_B + L_A2, 4, "air", density=0.8, seed=31)
play_melody(c, "語り2", L_A1 + L_A2 + L_B + L_A2, 4, "air", density=1.0, seed=32)
play_melody(c, "空", L_B + L_A3, 4, "air", density=0.9, seed=33)
play_melody(c, "ひとりに戻る", ["5,:1 1:1.5 2:0.5", "3:2 2:0.5 1:0.5", "6,:1.5 7,:0.5 1:1", "2:1.5 3:0.5 2:1", "1:6", "R:3", "R:3"], 4, "air", density=0.6, seed=34)

# ---------- 伴奏 ----------
B = S.beats
prev = 52
LB = L_B
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    t = tones(ch, "E3", "E5")
    if n in ("前置き", "語り1", "ひとりに戻る"):
        CELLO.bar(b, "E2:3")
        if n != "前置き" or i >= 1: CELLO2.bar(b, "B2:3")
        drone(DR, b, B, 52)                         # 弦のうすいドローン（E と B）で、空間を満たす
        if n == "語り1" and i >= 16:                 # 2回目のA（B）から、遠くの竪琴が根音と5度を置く
            c.HARP.bar(b, f"{nm(t[0])}:1 R:1 {nm(t[2])}:1" if i % 4 != 3 else " ".join(f"{nm(x)}:{0.15 if j < 3 else 3 - 0.45}" for j, x in enumerate(t[:4])))
        if n == "ひとりに戻る" and i >= 4:
            c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in t[:3]) if i == 4 else f"{nm(t[0] + 12)}:3")
    elif n == "語り2":
        # 竪琴：1拍目に根音、区切り（4・8小節目）でロールした和音
        if i % 4 == 3: c.HARP.bar(b, " ".join(f"{nm(x)}:{0.15 if j < 3 else 3 - 0.45}" for j, x in enumerate(t[:4])))
        else: c.HARP.bar(b, f"{nm(t[0])}:1 R:1 {nm(t[2])}:1")
        # チェロの対旋律：笛と反対向き。2分音符＋4分
        cand = [m for m in range(40, 57) if m % 12 in chord_pcs(ch)]
        a = min(cand, key=lambda m: abs(m - prev)); z = min([m for m in cand if m != a], key=lambda m: abs(m - a))
        CELLO.bar(b, f"{nm(a)}:2 {nm(z)}:1"); prev = z
        CELLO2.bar(b, f"{nm(low(ch, 'C2') + 12 if low(ch, 'C2') < 40 else low(ch, 'C2'))}:3")
        if i >= 16:
            v = voice(ch, 55, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
    elif n == "空":
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
        CELLO2.bar(b, f"{nm(low(ch, 'C2') + 12 if low(ch, 'C2') < 40 else low(ch, 'C2'))}:3")
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)])))
        if i < 8:   # B を3本の笛の和音で（主旋律の下に3度と6度）
            w = voice(ch, 64, 2, spread=False)
            FA.bar(b, f"{nm(w[0])}:3"); FB.bar(b, f"{nm(w[1])}:3")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0",
       "ケルト・フルート100曲の013（第2版の試作）。丘の上に一人きりの羊飼い。E エオリア・3/4・♩=56、ゆるやかなテンポのゆれ。独奏のエア（AABA）→竪琴とチェロが答える→3本の笛の和音で空へ→ひとりに戻る。",
       harm_scenes=None, tail_scene="ひとりに戻る", fill=False, pads=True, pad_scenes=["語り2", "空"])
