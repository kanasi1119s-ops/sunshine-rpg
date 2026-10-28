# ケルト・フルート100曲「銀の笛と百の夜」014 迷い羊 The Lost Lamb — 第2版（2026-10-28）
# イメージ: 霧の丘で、はぐれた子羊を探す。少し歩いては立ち止まり、笛で呼んで、じっと耳をすます。
#   遠くで、かすかな鳴き声。歩くたびに、その声が近くなる（本物の録音を、呼ぶたびに大きく明るく）。見つけた所で小さな山、最後は安心の長い音。
# 形（台帳）: ストップタイムのある歌。4小節ごとに「歩く2小節 → 呼ぶ（全員が1拍目だけ鳴らして止まる）→ 耳をすます」。4/4・♩=62。A ドリア。
# 編曲の表:
#   霧     : ピチカートの足どりだけ
#   探す1  : 歩く＝笛の歩く節＋ピチカート＋竪琴＋低い弦／呼ぶ＝全員1拍目だけ、笛が上へ呼ぶ／耳をすます＝弦のごく弱い持続と鳴き声
#   探す2  : 呼ぶ声が高くなる。鳴き声が近づく
#   探す3  : 足どりが速まる（8分）
#   見つけた: 全員。竪琴の分散和音・弦・チェロ（小さな山）
#   安堵   : 笛の長い音、竪琴の根音、弦
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 62
S = Song("C100", "014-the-lost-lamb", "迷い羊", "The Lost Lamb", BPM, 4, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
U = ["Am", "D", "Am", "Am"]
S.scene("霧", 4, "intro", ["Am", "Am", "D", "Am"])
S.scene("探す1", 16, "verse", U + ["G", "D", "Am", "Am"] + U + ["C", "G", "Am", "Am"])
S.scene("探す2", 16, "verse", U + ["G", "D", "Am", "Am"] + U + ["C", "G", "Am", "Am"])
S.scene("探す3", 8, "verse", ["Am", "D", "Am", "Am", "C", "G", "D", "D"])
S.scene("見つけた", 12, "chorus", ["C", "D", "G", "Em", "C", "D", "Em", "Am", "C", "D", "G", "Am"])
S.scene("安堵", 12, "outro", ["Am", "D", "Am", "C", "G", "D", "Am", "Am", "Am", "Am", "Am", "Am"])
NAMES = ["霧", "探す1", "探す2", "探す3", "見つけた", "安堵"]

c = make(S, NAMES,
         [("霧", 0, 0.6), ("探す1", 0, 0.62), ("探す2", 0, 0.66), ("探す3", 0, 0.72), ("見つけた", 0, 0.82), ("見つけた", 5, 0.9), ("見つけた", 11, 0.74),
          ("安堵", 0, 0.66), ("安堵", 11, 0.38)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="霧", passing=True, tension=False)
PIZZ = S.track("ピチカート（足どり）", "strings", patch="pizzicato", volume=0.075, pan=-0.25, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.2, reverb=0.45, barGain=c.g())

W = [("1:1 2:1 3:1 5:1", "4:1 3:1 2:2"), ("3:1 4:1 5:1 3:1", "2:1 1:1 7,:2"), ("5:1 4:1 3:1 4:1", "5:1 6:1 5:2"), ("6:1 5:1 4:1 2:1", "3:1 2:1 1:2")]
CALL = ["R:1 5:1 1':2", "R:1 6:1 2':2", "R:1 1':1 3':2", "R:1 7:1 2':2", "R:1 1':1 3':2", "R:1 2':0.5 3':1.5 1':1"]
def unitbars(k, call):
    w = W[k % 4]; return [w[0], w[1], call, "R:4"]
s1 = sum([unitbars(k, CALL[min(k, 5)]) for k in range(4)], [])
s2 = sum([unitbars(k + 1, CALL[min(k + 2, 5)]) for k in range(4)], [])
play_melody(c, "探す1", s1, 4, "air", density=0.6, seed=1401)
play_melody(c, "探す2", s2, 4, "air", density=0.7, seed=1402)
play_melody(c, "探す3", ["1:0.5 2:0.5 3:0.5 5:0.5 4:1 3:1", "2:0.5 3:0.5 4:0.5 5:0.5 6:2", "R:1 1':1 3':2", "R:4",
                         "5:0.5 6:0.5 7:0.5 1':0.5 2':1 1':1", "7:0.5 6:0.5 5:0.5 4:0.5 5:2", "R:1 2':0.5 3':1.5 1':1", "R:4"], 4, "air", density=0.6, seed=1403)
play_melody(c, "見つけた", ["1':1 2':1 3':2", "2':1 1':1 6:2", "7:1 2':1 1':1 7:1", "6:4", "5:1 6:1 1':2", "2':1 1':1 5:2", "6:1 7:1 6:1 5:1", "3:4",
                            "5:1 6:1 1':1 3':1", "2':2 1':1 7:1", "1':1 2':1 7:1 5:1", "6:4"], 4, "air", density=1.0, seed=1404)
play_melody(c, "安堵", ["5:4", "6:2 4:2", "5:4", "3:4", "2:2 3:2", "4:4", "1:4", "1:4", "R:4", "R:4", "R:4", "R:4"], 4, "air", density=0.5, seed=1405)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "E3", "E5"); pz = tones(ch, "A3", "A4")
    if n == "霧":
        PIZZ.bar(b, f"{nm(pz[0])}:1 {nm(pz[1])}:1 R:2" if i % 2 == 0 else f"{nm(pz[2])}:1 R:1 {nm(pz[1])}:1 R:1")
        continue
    if n in ("探す1", "探す2", "探す3"):
        ph = i % 4
        if ph in (0, 1):     # 歩く
            PIZZ.bar(b, " ".join(f"{nm(pz[x % len(pz)])}:{0.5 if n == '探す3' else 1}" for x in ((0, 1, 2, 1, 0, 2, 1, 2) if n == "探す3" else (0, 1, 2, 1))))
            c.HARP.bar(b, f"{nm(r)}:2 {nm(t[2])}:2")
            v = voice(ch, 52, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
            CELLO.bar(b, f"{nm(r)}:4")
        elif ph == 2:        # 呼ぶ：全員が1拍目だけ
            PIZZ.bar(b, f"{nm(pz[0])}:1 R:3"); c.HARP.bar(b, f"{nm(r)}:1 R:3"); CELLO.bar(b, f"{nm(r)}:1 R:3")
            v = voice(ch, 52, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:1 R:3" if j else f"{nm(v[j])}:4")
        else:                # 耳をすます：弦のごく弱い持続だけ
            v = voice(ch, 57, 2, spread=True)
            for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n == "見つけた":
        c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[0], t[2], t[4 % len(t)], t[2]) * 2))
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        CELLO.bar(b, f"{nm(r)}:4"); PIZZ.bar(b, f"{nm(pz[0])}:1 R:1 {nm(pz[2])}:1 R:1")
    if n == "安堵":
        if i < 10:
            v = voice(ch, 55, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if i % 2 == 0 and i < 10: c.HARP.bar(b, f"{nm(r)}:4")
        if i < 8: CELLO.bar(b, f"{nm(r)}:4")
rich(c, choir_scenes=["見つけた"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.25 --side-hpf 220",
       "ケルト・フルート100曲の014（第2版）。霧の丘ではぐれた子羊を探す。4/4・♩=62、A ドリア。ストップタイム：歩く2小節→全員が1拍目だけ鳴らして止まり笛が呼ぶ→耳をすます。呼ぶたびに本物の鳴き声が近づき、見つけた所で小さな山。",
       harm_scenes=None, tail_scene="安堵", fill=False, pads=True, pad_scenes=["探す2", "探す3", "見つけた", "安堵"])

# ---------- 空気：耳をすます小節に、遠くの鳴き声（呼ぶたびに近づく） ----------
BAR = 4 * 60 / BPM
SEEK = [4.3, 12.0, 40.4, 61.0, 20.4, 42.1, 5.3, 14.3, 43.2, 61.2]
ev = []; k = 0
for n in ("探す1", "探す2", "探す3"):
    for p in range(3, c.sc_len[n], 4):
        b = c.s0[n] + p; near = k / 9
        ev.append({"t": round(b * BAR + 0.4, 2), "file": "0821", "db": round(-36 + 12 * near, 1), "len": 3.0, "pan": round(0.55 - 0.45 * near, 2),
                   "seek": SEEK[k % len(SEEK)], "hp": 300, "lp": int(2500 + 5000 * near)})
        k += 1
ev.append({"t": round((c.s0["見つけた"] + 1) * BAR, 2), "file": "0821", "db": -22, "len": 3.0, "pan": 0.05, "seek": 40.4, "hp": 250, "lp": 8000})
air = {"pre": 1.5, "tail": 6.0, "layers": [{"file": "0908", "db": -35, "hp": 150, "lp": 5000, "lfo": [40, 0.4], "wide": 0.014, "duck": 0.35, "fade": 10},
                                           {"file": "0904", "db": -40, "hp": 100, "lp": 3000, "lfo": [53, 0.3], "phase": 1.0, "wide": 0.012, "duck": 0.35, "fade": 10}],
       "events": ev,
       "fx": {"glass": {"hz": [440.0, 880.0, 1318.5], "db": -28, "rt": 6.0, "start": 4}, "shimmer": {"db": -27, "rt": 8.0},
              "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5}, "haze": {"db": -27, "rt": 8.0}, "band": {"db": -37, "hz": 6500, "per": 23}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air014.json", "w"), ensure_ascii=False)
print("鳴き声:", len(ev))
