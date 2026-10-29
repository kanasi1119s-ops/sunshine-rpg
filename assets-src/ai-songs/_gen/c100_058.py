# ケルト・フルート100曲「銀の笛と百の夜」058 霧が晴れる前 Before the Mist Lifts（2026-10-29。第6章 霧の湖）
# イメージ: 夜明け前。湖はまだ白い霧の中。舟を止めて、エイラは待つ。霧は少しずつうすくなり、輪郭がひとつ、またひとつ見えてくる。
#   最後に、霧が晴れきる直前の、すんだ空気だけが残る。
# 形: ギター → 待つ1 → 待つ2（中盤の山）→ 白む → 澄む。4/4・♩=50・F リディア。長い音がゆるく上がっていく旋律。
# ただひとつ: 弦の和音に、となりあう音（にごり＝霧）を混ぜておき、場面が進むたびに一つずつ外していく
#   （ギター・待つ1＝3つ、待つ2＝2つ、白む＝1つ、澄む＝0）。最後は、3度もなくなり、5度とオクターブだけの澄んだ響きになる。
# 編曲の表:
#   ギター: ナイロンギターのゆっくりした分散和音と、にごった弦（霧）
#   待つ1 : 笛の長い音。ピアノの左手、にごりの弦
#   待つ2 : ピアノの右手も。弦3声・内声。山（中盤）
#   白む  : 笛が高い音域へ。にごりは1つだけ。竪琴の高い音が光りはじめる
#   澄む  : 弦は5度とオクターブだけ。笛は長い C で止まる
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 50
S = Song("C100", "058-before-the-mist-lifts", "霧が晴れる前", "Before the Mist Lifts", BPM, 4, "F", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.22})
P = ["F", "G", "Am", "F", "Dm", "C", "G", "F", "F", "G", "Em", "Am", "Dm", "G", "C", "F"]
S.scene("ギター", 4, "intro", ["F", "G", "F", "G"])
S.scene("待つ1", 16, "verse", P)
S.scene("待つ2", 16, "chorus", P)
S.scene("白む", 12, "verse", ["F", "G", "F", "G", "Dm", "Am", "G", "C", "F", "G", "F", "F"])
S.scene("澄む", 4, "outro", ["F", "F", "F", "F"])
NAMES = ["ギター", "待つ1", "待つ2", "白む", "澄む"]

c = make(S, NAMES,
         [("ギター", 0, 0.6), ("待つ1", 0, 0.64), ("待つ2", 0, 0.72), ("待つ2", 8, 0.84), ("待つ2", 15, 0.72), ("白む", 0, 0.7), ("白む", 11, 0.72),
          ("澄む", 0, 0.66), ("澄む", 3, 0.52)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="ギター", passing=True, tension=False)
GTR = S.track("ナイロンギター", "guitar", patch="nylonGuitar", volume=0.075, pan=0.3, reverb=0.45, barGain=c.g())
PL = S.track("ピアノ（左手）", "piano", volume=0.85, pan=-0.2, reverb=0.5, barGain=c.g())
PR = S.track("ピアノ（右手）", "piano", volume=0.7, pan=-0.1, reverb=0.5, barGain=c.g())
FOG = [S.track(f"霧のにごり（弦）{i + 1}", "strings", patch="slowStrings", volume=0.022, pan=[-0.5, 0.5, 0.1][i], reverb=0.7, barGain=c.g()) for i in range(3)]
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.12, reverb=0.5, barGain=c.g())

M = ["3:3 5:1", "4:4", "3:2 5:2", "1':4", "6:3 5:1", "5:2 3:2", "2:2 4:2", "3:4",
     "5:3 6:1", "7:2 6:2", "7:4", "5:2 7:2", "1':3 2':1", "2':4", "3':2 2':2", "1':4"]
W = ["3':4", "4':4", "3':2 2':2", "2':4", "1':3 6:1", "1':2 3':2", "2':4", "3':2 5:2", "1':4", "2':2 4':2", "3':4", "3':4"]
play_melody(c, "待つ1", M, 4, "air", density=0.4, seed=5801)
play_melody(c, "待つ2", M, 4, "air", density=0.6, seed=5802)
play_melody(c, "白む", W, 4, "air", density=0.45, seed=5803)
play_melody(c, "澄む", ["5:4", "5:4", "R:4", "R:4"], 4, "air", density=0.0)

B = S.beats
FOGN = {"ギター": 3, "待つ1": 3, "待つ2": 2, "白む": 1, "澄む": 0}
SC = [(S.key.t + x) % 12 for x in S.key.steps]
def neighbors(ch, lo):
    """和音の音のすぐ上の音階の音（にごり）。2度でぶつかる音を、和音の中ほどの音域に"""
    pcs = chord_pcs(ch); out = []
    for m in range(lo, lo + 14):
        if m % 12 in SC and m % 12 not in pcs and (m - 1) % 12 in pcs or (m - 2) % 12 in pcs and m % 12 in SC and m % 12 not in pcs:
            out.append(m)
    return out
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "F3", "F5")
    CELLO.bar(b, f"{nm(r)}:4")
    if n == "澄む":   # 5度とオクターブだけ
        for j, m in enumerate((53, 60, 65)): c.STR[j].bar(b, f"{nm(m)}:4")
        GTR.bar(b, f"{nm(41)}:2 {nm(48)}:2" if i < 3 else f"{nm(53)}:4")
        if i < 3: c.HARP2.bar(b, f"{nm(72)}:2 {nm(77)}:2")
        continue
    nv = 3 if n in ("待つ2", "白む") else 2
    v = voice(ch, 55, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:4")
    nb = neighbors(ch, 57)[:FOGN[n]]
    for j, m in enumerate(nb): FOG[j].bar(b, f"{nm(m)}:4")
    GTR.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 2)) if n == "ギター" else " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 5, 4, 2, 3, 2)))
    if n != "ギター": PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
    if n in ("待つ2", "白む"):
        hi = tones(ch, "A4", "A5"); PR.bar(b, f"{nm(hi[0])}:2 {nm(hi[1])}:2")
    if n == "白む" and i >= 4:
        hh = tones(ch, "C6", "C7"); c.HARP2.bar(b, f"{nm(hh[0])}:1 {nm(hh[1])}:1 {nm(hh[2 % len(hh)])}:2")
rich(c, choir_scenes=["待つ2"], pulse_scenes=["待つ2", "白む"], guitar=False, pizz=False, inner=True)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の058。夜明け前、湖の霧が少しずつうすくなる。4/4・♩=50、F リディア。弦の和音に混ぜた「となりあう音（にごり＝霧）」が、場面ごとに一つずつ外れていき、最後は5度とオクターブだけの澄んだ響きになる。笛は長い音でゆるく上がっていく。",
       harm_scenes=None, tail_scene="澄む", fill=False, pads=True, pad_scenes=["待つ1", "待つ2", "白む"], floor=True)
air = {"pre": 0.8, "tail": 8.0, "layers": [{"file": "0621", "db": -39, "hp": 150, "lp": 5000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -28, "rt": 8.0}, "far": {"db": -25, "delay": 0.3, "lp": 2800, "rt": 5.0}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air058.json", "w"), ensure_ascii=False)
