# ケルト・フルート100曲「銀の笛と百の夜」059 睡蓮 Water Lilies（2026-10-29。第6章 霧の湖）
# イメージ: 霧がうすれ、湖の入り江が見えてくる。白みはじめた水の上に、睡蓮がいくつも浮かんでいる。
#   風がないので、水面は鏡のよう。花と、さかさまに映った花が、上と下で同じようにゆれている。
# 形: 池 → 浮かぶ → 映る → 開く（終盤の山）→ 閉じる（和音のロール）。12/8（付点4分×4 のゆれる子守歌）・8分＝150・E♭ イオニア。
# ただひとつ: 「映る」から、ピアノの高い音が、笛の旋律を上下さかさまにした形（鏡の旋律。B♭ を軸に、上がる所は下がり、下がる所は上がる）で
#   同時に弾く。花と水に映った花が、いっしょにゆれる。
# 編曲の表:
#   池    : 竪琴の低い音のゆれと、うすい弦とチェロ
#   浮かぶ: 笛。ピアノの左手（付点4分のゆれ）、竪琴
#   映る  : ＋ピアノの鏡の旋律（高い音）。弦3声
#   開く  : 笛の2つ目の節（上の音域）＋鏡。笛の和声。内声の動き。山
#   閉じる: 竪琴の和音のロールで閉じる
import sys, json
from c100_common import *
from c100_v2 import *
from c100_common import _dia

BPM = 150   # 8分音符＝150（付点4分＝50）
S = Song("C100", "059-water-lilies", "睡蓮", "Water Lilies", BPM, 12, "Eb", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
P = ["Eb", "Ab", "Cm", "Bb", "Eb", "Ab", "Fm", "Bb", "Cm", "Ab", "Bb", "Eb", "Ab", "Gm", "Fm", "Eb"]
S.scene("池", 4, "intro", ["Eb", "Ab", "Eb", "Bb"])
S.scene("浮かぶ", 16, "verse", P)
S.scene("映る", 16, "verse", P)
S.scene("開く", 12, "chorus", ["Ab", "Bb", "Gm", "Cm", "Ab", "Bb", "Eb", "Eb", "Ab", "Fm", "Bb", "Eb"])
S.scene("閉じる", 4, "outro", ["Ab", "Eb", "Eb", "Eb"])
NAMES = ["池", "浮かぶ", "映る", "開く", "閉じる"]

c = make(S, NAMES,
         [("池", 0, 0.6), ("浮かぶ", 0, 0.64), ("映る", 0, 0.68), ("開く", 0, 0.74), ("開く", 8, 0.86), ("開く", 11, 0.76),
          ("閉じる", 0, 0.66), ("閉じる", 3, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="池", passing=True, tension=False)
MIR = S.track("ピアノ（水に映る旋律）", "piano", volume=0.55, pan=0.3, reverb=0.65, barGain=c.g())
PL = S.track("ピアノ（左手）", "piano", volume=0.85, pan=-0.2, reverb=0.5, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.12, reverb=0.5, barGain=c.g())

M = ["3:3 2:2 1:1 5:6", "6:3 5:2 4:1 3:6", "5:3 6:2 5:1 3:3 1:3", "2:6 4:3 5:3",
     "3:3 2:2 1:1 5:6", "1':3 7:2 6:1 5:6", "4:3 5:2 6:1 1':6", "7:6 2':6",
     "1':3 7:2 6:1 5:6", "6:3 5:2 4:1 3:6", "2:3 3:2 4:1 5:6", "1:12",
     "6:6 1':6", "7:3 6:2 5:1 2':6", "1':3 7:2 6:1 4:6", "5:12"]
O = ["1':3 2':2 3':1 1':6", "2':6 4':6", "5':12", "3':3 2':2 1':1 5:6",
     "6:3 1':2 3':1 1':6", "2':3 1':2 7:1 5:6", "3':6 2':3 1':3", "5:6 3:6",
     "1':3 2':2 3':1 4':6", "3':3 2':2 1':1 6:6", "2':6 5:6", "1:12"]
play_melody(c, "浮かぶ", M, 4, "air", density=0.45, seed=5901)
a = play_melody(c, "映る", M, 4, "air", density=0.55, seed=5902)
a += play_melody(c, "開く", O, 4, "air", density=0.6, seed=5903)
play_melody(c, "閉じる", ["3:6 2:6", "1:12", "R:12", "R:12"], 4, "air", density=0.2, seed=5904)

# ---------- 鏡の旋律（B♭4 を軸に、音階の上で上下をさかさまに。1オクターブ上で） ----------
B = S.beats
SC = [(S.key.t + x) % 12 for x in S.key.steps]
AX = 70
def steps(a_, m):
    k = 0; x = a_; s = 1 if m > a_ else -1
    while x != m:
        x += s
        if x % 12 in SC: k += s
    return k
for t, L, m, mk in a:
    if L < 0.9: continue
    k = steps(AX, m)
    q = (_dia(S, AX, -k) if k else AX) + 12
    pcs = chord_pcs(S.chords[int(t // B)].split("|")[0])
    if L >= 3 and q % 12 not in pcs:   # 長い音は和音の音に寄せる
        q = min((x for x in range(q - 2, q + 3) if x % 12 in pcs), key=lambda x: abs(x - q), default=q)
    while q > 89: q -= 12
    MIR.at(round(t, 3), f"{nm(q)}:{round(L, 3)}{mk or ','}")

for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "Eb3", "Eb5")
    CELLO.bar(b, f"{nm(r)}:12")
    if n == "閉じる":
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:12")
        if i == 1: c.HARP.bar(b, " ".join(f"{nm(x)}:0.25" for x in tones(ch, "Eb3", "Eb6")[:10]) + " R:9.5")
        if i >= 2: c.HARP2.bar(b, f"{nm(tones(ch, 'G5', 'G6')[i - 2])}:12")
        continue
    nv = 2 if n in ("池", "浮かぶ") else 3
    v = voice(ch, 52 if nv == 2 else 56, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:12")
    if n == "池": c.HARP.bar(b, f"{nm(t[0])}:6 {nm(t[2])}:6")
    else:
        c.HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 2, 4, 5, 4, 2, 4, 2, 1, 2)))
        PL.bar(b, f"{nm(r)}:3 {nm(r + 7)}:3 {nm(r + 12)}:3 {nm(r + 7)}:3")
rich(c, choir_scenes=["開く"], pulse_scenes=["映る", "開く"], guitar=False, pizz=False, inner=True)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の059。白みはじめた入り江に浮かぶ睡蓮。12/8・8分＝150、E♭ イオニア。「映る」から、ピアノの高い音が笛の旋律を上下さかさまにした鏡の旋律を同時に弾き、花と水に映った花がいっしょにゆれる。最後は竪琴の和音のロールで閉じる。",
       harm_scenes=None, tail_scene="閉じる", fill=False, pads=True, pad_scenes=["浮かぶ", "映る", "開く", "閉じる"], floor=True)
air = {"pre": 0.6, "tail": 7.0, "layers": [{"file": "0691", "db": -39, "hp": 150, "lp": 5000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -28, "rt": 8.0}, "far": {"db": -25, "delay": 0.28, "lp": 2800, "rt": 4.8}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air059.json", "w"), ensure_ascii=False)
