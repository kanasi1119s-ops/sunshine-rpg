# ケルト・フルート100曲「銀の笛と百の夜」024 川辺の蛙たち The Frogs at Dusk — 第2版（2026-10-28）
# イメージ: 夕方の水辺。一匹の蛙が鳴きはじめると、あちこちから仲間が加わり、いつのまにか大合唱。
#   笛も蛙に調子を合わせて、同じ節を、1本・2本・3本と、4小節ずつ遅れて歌い出す（輪唱）。夜になると、笛は一本ずつ帰っていき、蛙の声が残る。
# 形（台帳）: 輪唱（蛙の合唱に、3本の笛が加わる）。4/4・♩=58。G ドリア（i と ♭VII が2小節ずつ）。始め：蛙の声／終わり：蛙の声。山なし。
# 編曲の表:
#   蛙     : 蛙の声（録音）＋チェロのピチカート（蛙の拍）
#   一匹   : 笛1（中央）が節を歌う
#   二匹   : 笛2（右）が4小節遅れて加わる
#   合唱   : 笛3（左・低め）が加わり、3本の輪唱。竪琴
#   もっと : 弦がうすく、ピチカートが細かく
#   夜へ   : 笛が1本ずつ抜け、蛙の声が残る
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 58
S = Song("C100", "024-the-frogs-at-dusk", "川辺の蛙たち", "The Frogs at Dusk", BPM, 4, "G", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
CC = ["Gm", "Gm", "F", "F"]
S.scene("蛙", 4, "intro", CC)
S.scene("一匹", 8, "verse", CC * 2)
S.scene("二匹", 8, "verse", CC * 2)
S.scene("合唱", 16, "verse", CC * 4)
S.scene("もっと", 16, "chorus", CC * 4)
S.scene("夜へ", 8, "outro", CC * 2)
NAMES = ["蛙", "一匹", "二匹", "合唱", "もっと", "夜へ"]

c = make(S, NAMES,
         [("蛙", 0, 0.6), ("一匹", 0, 0.62), ("二匹", 0, 0.64), ("合唱", 0, 0.68), ("もっと", 0, 0.74), ("夜へ", 0, 0.64), ("夜へ", 7, 0.4)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="蛙", passing=True, tension=False)
F2 = S.track("笛2", "panflute", patch="flute", volume=0.32, bright=-0.6, pan=0.4, reverb=0.55, breath=True, noRestrike=True, mono=True, sustain=1.1, phrase=16, gainDb=2, barGain=c.g())
F3 = S.track("笛3", "panflute", patch="flute", volume=0.3, bright=-0.75, pan=-0.4, reverb=0.6, breath=True, noRestrike=True, mono=True, sustain=1.1, phrase=16, gainDb=2, barGain=c.g())
PZ = S.track("チェロのピチカート（蛙の拍）", "strings", patch="pizzicato", volume=0.08, pan=0.1, reverb=0.35, barGain=c.g())

K = ["1:1 R:0.5 3:0.5 5:1 3:1", "4:1.5 3:0.5 2:2", "3:1 5:1 7:1 5:1", "6:2 5:2",
     "4:1 R:0.5 5:0.5 6:1 4:1", "5:1.5 4:0.5 3:2", "2:1 3:1 4:1 2:1", "1:4"]
END = c.s0["夜へ"]
def canon(track, start, oct_, stop, key=None, orn=0.6, seed=1):
    key = key or S.key; B = S.beats; b = start; j = 0; ev = []
    while b < stop:
        ev += mel_events(key, K[j % 8], oct_, b * B); b += 1; j += 1
    notes = ornament(ev, key, S.bpm, "air", B, density=orn, seed=seed)
    for t, L, m, mk in notes: track.at(round(t, 4), f"{nm(m)}:{round(L, 4)}{mk}")
a = c.s0["一匹"]
canon(c.FLUTE, a, 4, END + 6, orn=0.8, seed=2401)          # 笛1：夜への6小節目まで
canon(F2, a + 8, 4, END + 4, orn=0.6, seed=2402)            # 笛2：4小節目まで
canon(F3, a + 12, 4, END + 2, orn=0.5, seed=2403)           # 笛3（左・やわらかい音色）：2小節目まで（笛の低音は鳴りにくいので同じ高さ）

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D5")
    PZ.bar(b, f"{nm(r)}:1 R:1 {nm(r + 7)}:1 R:1" if n != "もっと" else f"{nm(r)}:0.5 R:0.5 {nm(r + 7)}:0.5 {nm(r + 12)}:0.5 R:1 {nm(r + 7)}:1")
    if n in ("合唱", "もっと") or (n == "夜へ" and i < 6): c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2")
    if n in ("もっと",) or (n == "夜へ" and i < 7):
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の024（第2版）。夕方の水辺の蛙の大合唱。4/4・♩=58、G ドリア。蛙の声（録音）とチェロのピチカートの拍に、3本の笛が4小節ずつ遅れて加わる輪唱。夜になると笛が1本ずつ帰り、蛙の声が残る。",
       harm_scenes=None, tail_scene="夜へ", fill=False, pads=True, pad_scenes=["合唱", "もっと"], double=False)
BEAT = 60 / BPM
ev = [{"t": round((b * 4 + q) * BEAT + 0.05, 2), "file": "0819", "db": -24 - (3 if q else 0), "len": 0.6, "pan": [-0.3, 0.35][(b + q) % 2], "seek": 0.0, "hp": 200, "lp": 7000}
      for b in range(0, 6) for q in (0, 2)]
air = {"pre": 2.5, "tail": 9.0, "layers": [{"file": "0997", "db": -29, "hp": 150, "lp": 7000, "wide": 0.014, "duck": 0.25, "fade": 6}],
       "events": ev,
       "fx": {"glass": {"hz": [392.0, 784.0, 1174.7], "db": -29, "rt": 6.0, "start": 4}, "shimmer": {"db": -28, "rt": 8.0},
              "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5}, "haze": {"db": -27, "rt": 8.0}, "band": {"db": -38, "hz": 6500, "per": 23}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air024.json", "w"), ensure_ascii=False)
