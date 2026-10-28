# ケルト・フルート100曲「銀の笛と百の夜」050 石に眠る歌 The Song Asleep in Stone（2026-10-29）
# イメージ: 小部屋の奥の石壁に、古い歌が刻まれている。音符ではなく、刻みの長さと間（リズム）だけ。
#   エイラが指でその刻みを順にたたくと、石が鳴り、リズムが見えてくる。そこに音がつき、笛が歌い、眠っていた歌が目を覚ます。
#   第5章の終わり。祖父がこの歌を残した理由に、エイラは少しだけ近づく。
# 形: 石をたたく律動（音の高さのない打音）が先に旋律のリズムを刻み → 竪琴が音の高さをつけ → 笛が歌になる → 全員で目覚め（静かな山）。4/4・♩=52。G エオリア。終盤に静かな山。
# ただひとつ: 旋律のリズムを、音のない打音（枠太鼓の縁＝石をたたく音）が先に刻む。最後まで、打音が歌のリズムをなぞり続ける。
# 編曲の表:
#   刻まれた律動: 打音だけが旋律のリズムを刻む＋低い弦のドローンとチェロ（はじまりから厚く）
#   音がつく    : 竪琴が、打音と同じリズムで音の高さをつける。後半から笛が小さく重なる
#   歌1         : 笛が歌う。打音は下でなぞる。弦3声
#   目覚め      : 全員。笛の和声・ホルン・内声（静かな山）
#   歌になる    : 笛と弦。打音が最後の一打
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 52
S = Song("C100", "050-the-song-asleep-in-stone", "石に眠る歌", "The Song Asleep in Stone", BPM, 4, "G", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.15})
C8 = ["Gm", "Cm", "Bb", "Cm", "Gm", "Bb", "F", "Gm"]
S.scene("刻まれた律動", 4, "intro", C8[:4])
S.scene("音がつく", 16, "verse", C8 * 2)
S.scene("歌1", 16, "verse", C8 * 2)
S.scene("目覚め", 12, "chorus", ["Eb", "F", "Gm", "Gm", "Eb", "F", "D", "D", "Cm", "F", "Gm", "Gm"])
S.scene("歌になる", 6, "outro", ["Cm", "D", "Gm", "Gm", "Gm", "Gm"])
NAMES = ["刻まれた律動", "音がつく", "歌1", "目覚め", "歌になる"]

c = make(S, NAMES,
         [("刻まれた律動", 0, 0.64), ("音がつく", 0, 0.64), ("歌1", 0, 0.7), ("目覚め", 0, 0.8), ("目覚め", 8, 0.88), ("歌になる", 0, 0.7), ("歌になる", 5, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="刻まれた律動", passing=True, tension=False)
TAP = S.track("石をたたく音（枠太鼓の縁）", "guitar", patch="frameDrum", volume=0.11, pan=-0.2, reverb=0.55, modulate=False, barGain=c.g())
HM = S.track("竪琴（石の歌の高さ）", "harp", patch="folkHarp", volume=0.12, pan=0.25, reverb=0.5, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.12, reverb=0.45, barGain=c.g())
HORN = [S.track(f"ホルン{i + 1}", "brass", patch="horn", volume=[0.05, 0.042][i], pan=[-0.3, -0.12][i], reverb=0.6, breath=False,
                attack=0.35, release=1.0, bright=-0.5, barGain=c.g()) for i in range(2)]

M = ["1:1 1:0.5 3:0.5 5:2", "4:1 3:1 2:2", "3:1 3:0.5 5:0.5 7:2", "6:1 5:1 4:2", "5:1 5:0.5 7:0.5 1':2", "7:1 6:1 5:2", "4:1 3:1 2:1 7,:1", "1:4"]
W = ["5:2 6:1 7:1", "1':3 7:1", "1':2 2':1 1':1", "7:4", "6:2 5:1 6:1", "7:3 6:1", "5:1 4:1 #3:2", "#3:4",
     "4:1 4:0.5 6:0.5 1':2", "7:1 6:1 5:2", "4:1 3:1 2:1 7,:1", "1:4"]
def taps(bars, scene, accent_first=True):
    """旋律のリズムだけを、音の高さのない打音で（音の頭ごとに1打。長い音は1打のあと休み）"""
    b0 = c.s0[scene]; B = S.beats
    for j, s in enumerate(bars):
        t = 0.0
        for k, tok in enumerate(s.split()):
            d, L = tok.split(":"); L = float(L)
            if d != "R":
                mk = "!" if (k == 0 and accent_first) else ","
                TAP.at(round((b0 + j) * B + t, 3), f"{'A3' if L < 2 else 'D3'}:{min(L, 1)}{mk}")
            t += L
taps(M[:4], "刻まれた律動")
taps(M * 2, "音がつく"); taps(M * 2, "歌1"); taps(W, "目覚め")
taps(["4:1 4:0.5 6:0.5 1':2", "7:1 6:1 5:2", "1:4", "R:4", "R:4", "R:4"], "歌になる")
# 音がつく：竪琴が、打音と同じリズムで音の高さをつける（後半から笛も小さく重なる）
play_melody(c, "音がつく", M * 2, 4, "air", density=0.0, track=HM)
play_melody(c, "音がつく", ["R:4"] * 8 + M, 4, "air", density=0.3, seed=5001)
play_melody(c, "歌1", M * 2, 4, "air", density=0.7, seed=5002)
play_melody(c, "目覚め", W, 4, "air", density=0.9, seed=5003)
play_melody(c, "歌になる", ["4:1 4:0.5 6:0.5 1':2", "7:1 6:1 5:2", "4:1 3:1 2:1 7,:1", "1:4", "1:4", "R:4"], 4, "air", density=0.4, seed=5004)

B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "G3", "G5")
    if n == "歌になる" and i >= 5: continue
    CELLO.bar(b, f"{nm(r)}:4")
    nv = 2 if n in ("刻まれた律動", "音がつく") else 3
    v = voice(ch, 52 if nv == 2 else 57, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n == "刻まれた律動": c.HARP2.bar(b, f"R:2 {nm(t[4 % len(t)] + 12)}:2")
    if n in ("歌1", "目覚め"):
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[2])))
    if n == "目覚め":
        hv = voice(ch, 50, 2, spread=False)
        for j in range(2): HORN[j].bar(b, f"{nm(hv[j])}:4")
rich(c, choir_scenes=["目覚め"], pulse_scenes=["歌1", "目覚め"], guitar=False, pizz=False, inner=True, choir_vol=0.11)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.35 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の050（第5章の終わり）。石壁に刻まれた古い歌が目を覚ます。4/4・♩=52、G エオリア。石をたたく音（音の高さのない打音）が先に旋律のリズムを刻み、竪琴が音の高さをつけ、笛が歌になり、全員で静かな山。打音は最後まで歌のリズムをなぞる。",
       harm_scenes=None, tail_scene="歌になる", fill=False, pads=True, pad_scenes=["音がつく", "歌1", "目覚め", "歌になる"], floor=True)
air = {"pre": 0.8, "tail": 7.0, "layers": [{"file": "0595", "db": -38, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -28, "rt": 8.0}, "far": {"db": -24, "delay": 0.3, "lp": 2600, "rt": 5.0}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air050.json", "w"), ensure_ascii=False)
