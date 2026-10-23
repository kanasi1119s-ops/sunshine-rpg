# ラウド25曲（第2シリーズ）15「月の裏で眠る」（仮）。イメージ: ドラッグ×空（眠りの中で月の裏へ）。C♯ 短調・82・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: 鉄琴（グロッケン。夢のきらめき、サビの旋律の重ね、最後に一人で残る）
# 物語: 眠りの中で月の裏へ漂う。夢が悪夢に変わり押しつぶされ、目が覚めかけ、もう一度だけ大きな夢（サビ）を見て、鉄琴だけが残る。
# 形（ほかの曲と変える）: 三部形式。静かな夢（クリーン・鉄琴・ベースの旋律）→ 悪夢（重いリフ・ハーフタイム・5つずつのかたまり）→ 目覚めかけ（無音に近い）
#   → 夢がもどる → サビは最後に1回だけ（12小節）→ 鉄琴だけ。ブレイクダウンもソロもない
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 82, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 4), ("dream", 8), ("dream2", 8), ("fall", 4), ("riff", 8), ("night", 8), ("night2", 8), ("wake", 4), ("dream3", 8), ("chorus", 12), ("outro", 4)]
DREAM = ["C#madd9", "Amaj7", "Emaj7/G#", "F#m7", "C#m9", "Amaj7", "Bsus4", "B"]
CH = {"intro": ["C#m9"] * 4, "dream": DREAM, "dream2": ["Amaj7", "G#m7", "F#m9", "E", "Amaj7", "G#m7", "F#m7", "G#7sus4"],
      "fall": ["Dmaj7", "Dmaj7", "G#7sus4", "G#7"], "riff": ["C#m", "C#m", "D", "C#m", "C#m", "C#m", "D", "G#7"],
      "night": ["C#m", "D", "C#m", "G#7", "C#m", "D", "Bm", "G#7"], "night2": ["F#m", "G#7", "A", "G#7", "F#m", "G#7", "Dmaj7", "G#7"],
      "wake": ["C#m9"] * 4, "dream3": DREAM, "chorus": ["A", "E/G#", "F#m", "C#m/E", "D", "A/C#", "Bsus4", "B", "A", "E/G#", "F#m7", "G#7sus4"],
      "outro": ["C#m9"] * 4}
song = Song("月の裏で眠る（仮）",
            "仮: ラウド25曲（第2シリーズ）の15曲目。イメージはドラッグ×空（眠りの中で月の裏へ）。C♯ 短調・82。三部形式: 静かな夢（クリーンの分散和音・鉄琴・ベースの旋律）→ "
            "悪夢（重いリフ・ハーフタイム・5つずつのかたまり）→ 夢がもどり、最後に1回だけの大きなサビ（♭Ⅱ の D で光）→ 鉄琴だけが残る。別の楽器は鉄琴。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 眠りの中で月の裏へ漂い、夢が悪夢に変わり、目覚めかけ、最後に一度だけ大きな夢を見る。"
song.flags = "--space hall --space-wet 0.15"
song.kinds = {"dream": "verse", "dream2": "pre", "fall": "bridge", "riff": "interlude", "night": "verse", "night2": "solo", "wake": "break", "dream3": "verse"}
SECS, NB = song.secs, song.nb
song.pickups = ['V4', 'V3']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

RIFF = {"C#m": [bar("C#2:1.5! C#2:0.5 D2:1 C#2:0.5 G#2:0.5"), bar("C#2:1.5! C#2:0.5 E2:0.5 D2:0.5 C#2:1")],
        "D": [bar("D2:1.5! D2:0.5 A2:1 G#2:0.5 D2:0.5")] * 2, "G#7": [bar("G#1:1.5! G#1:0.5 C2:1 D#2:0.5 F#2:0.5")] * 2}

# 2026-10-24 旋律を作り直し（人間「似た曲を作らない」。前の旋律は「4分4分2分」など、シリーズの多くの曲と同じリズムだった）:
#   夢の中で拍がほどける感じに、4分の3連（2拍に3つ）を小節線にまたがって使う（3対4のずれ）。小節の終わりは休むか、動いている
CSM = scale_pcs("C#", "aeolian")
DRM = [[-0.5, 0.6667, 0.6667, 0.6666, 1, -0.5], [1, 0.6667, 0.6667, 0.6666, -1], [-1, 1.3333, 0.6667, -1], [0.6667, 0.6667, 0.6666, 0.5, 0.5, -1]]
NGT = [[-0.75, 0.25, 0.6667, 0.6667, 0.6666, -1], [0.25, 0.25, 0.5, -0.5, 1.3333, 0.6667, -0.5], [-0.5, 0.25, 0.25, 0.6667, 0.6667, 0.6666, -1]]
CHR = [[0.6667] * 5 + [0.6665], [1.3333, 1.3333, 1.3334], [-0.5, 0.5, 0.6667, 0.6667, 0.6666, 1], [0.6667, 0.6667, 0.6666, -2]]
W = lambda st, en, rh, seed, chs, ct, lo="G#3", hi="F#5": [bar(x) for x in melody_walk(CSM, st, en, rh, seed, chs, contour=ct, lo=lo, hi=hi)]
DREAM_MEL = W("G#4", "C#5", DRM, 1, CH["dream"], (1, 1, -2, 1, 2, -1))
DREAM2_MEL = W("C#5", "E5", DRM, 2, CH["dream2"], (-1, 2, 1, -2, 1))
DREAM3_MEL = W("E5", "G#4", DRM, 3, CH["dream3"], (1, -1, -1, 2, -2))
NIGHT_MEL = W("C#4", "G#4", NGT, 4, CH["night"], (0, 1, 2, -1, -2, 1), lo="G#3", hi="E5")
NIGHT2_MEL = W("F#4", "C#5", NGT, 5, CH["night2"], (1, 1, -1, 2, -2), lo="A3", hi="F#5")
CHORUS_MEL = W("C#5", "E5", CHR, 6, CH["chorus"], (1, 2, -1, 1, -2, 2, -1))


def glock_spark(ch):
    """鉄琴のきらめき（和音の高い音を2分と4分で、すき間を残して）"""
    t = chord_tones(ch.split("/")[0], "G#5", "E7")
    return bar(f"{t[-1]}:1.5 {t[len(t) // 2]}:0.5 R:1 {t[1]}:1")


def clean_arp(ch):
    t = chord_tones(ch.split("/")[0], "C#3", "E5")
    pat = [0, 2, 4, 3, 5, 3, 4, 2]
    return bar(" ".join(f"{t[j % len(t)]}:0.5" for j in pat))


DREAM_BASS = [bar("C#2:2 G#2:1 B2:1"), bar("A1:2 E2:1>G#2 G#2:1"), bar("G#1:2 B1:1 E2:1"), bar("F#1:2 C#2:1 E2:1"),
              bar("C#2:1.5 E2:0.5 G#2:1>B2 B2:1"), bar("A1:2 C#2:1 E2:1"), bar("B1:2 E2:1 F#2:1"), bar("B1:2 D#2:1 F#2:1")]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "dlead", "harm8", "clean", "glock", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R4
    if name == "riff":
        rf = RIFF[base_ch if base_ch in RIFF else "C#m"][i % 2]
    elif name == "fall" and i == 3:
        rf = bar("G#1:4!")
    P["riff"].append(rf)

    s = si = R4
    if name in ("night", "night2"):
        s = bar(f"{groot}:4") if not last else bar(f"{groot}:2! R:2")
        si = s if name == "night2" else R4
    elif name == "chorus":
        s = bar(f"{groot}:4!") if i % 4 == 0 else bar(f"{groot}:2 {groot}:2")
        si = s
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = dlead = harm8 = clean = glock = R4
    if name == "dream": dlead = DREAM_MEL[i]
    elif name == "dream2": dlead = DREAM2_MEL[i]
    elif name == "dream3": dlead = DREAM3_MEL[i]
    elif name in ("night", "night2"): lead = NIGHT_MEL[i] if name == "night" else NIGHT2_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    if name in ("intro", "dream", "dream2", "wake", "dream3"):
        clean = clean_arp(ch)
    if name in ("intro", "dream", "dream3", "wake"):
        glock = glock_spark(ch)
    elif name == "chorus":
        glock = shift_oct(strip_marks(CHORUS_MEL[i]), 1) if i >= 4 else glock_spark(ch)
    elif name == "outro":
        t = chord_tones("C#m9", "G#5", "E7")
        glock = [bar(f"{t[-1]}:1 {t[-2]}:1 {t[-3]}:1 {t[-4]}:1"), bar(f"{t[-3]}:1.5 {t[-4]}:1.5 {t[-5]}:1"), bar(f"{t[-4]}:2 {t[-6]}:2"), bar(f"{t[-6]}:4")][i]
    P["lead"].append(lead); P["dlead"].append(dlead); P["harm8"].append(harm8); P["clean"].append(clean); P["glock"].append(glock)

    if name in ("dream", "dream3"): b = DREAM_BASS[i]
    elif name == "dream2": b = bar(f"{root}:2 {fifth_of(base_ch)}:1 {up(root, 1)}:1")
    elif name == "intro": b = bar("C#2:4") if i >= 2 else R4
    elif name == "fall": b = bar(f"{root}:4") if i < 3 else bar("G#1:4!")
    elif name == "riff": b = unison_low(P["riff"][-1], -1, "B0")
    elif name in ("night", "night2"): b = bass_root8(ch, BEATS, nxt) if not last else bar(f"{root}:1! {root}:1 R:2")
    elif name == "chorus": b = bar(f"{root}:3! {root}:1") if i % 4 != 3 else bass_root8(ch, BEATS, nxt)
    elif name == "wake": b = R4
    else: b = R4
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name in ("dream", "dream2", "dream3"):
        # 夢: キックは弱く2拍ずつ、ライドは小さく、スネアはクロスのように薄く
        k = "o.......o......." ; s = "........o......." if name != "dream" else None
        cym = f"{RIDE}:1, {RIDE}:1, {RIDE}:1, {RIDE}:1," if name != "dream" or i >= 4 else None
        if name == "dream3" and i >= 4: k = "X.......X..x...."; s = "........X......."
        if last and name == "dream3": tom = "R:2 " + tom_16_down(2); s = None
    elif name == "fall":
        tom = " ".join(f"A2:0.25{',' if j < 8 else ''}" for j in range(16)) if i < 3 else None
        if i == 3: k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
    elif name == "riff":
        k = "X.....X.X......." if i % 2 == 0 else "X.....X.X..x...."
        s = "........X......."
        cym = f"{CHINA}:1! {RIDE}:1 {CHINA}:1! {RIDE}:1"
        if i == 0: cym = f"{CR}:2! {CHINA}:1! {RIDE}:1"
        if last: k = "X.....X........."; s = "........"; s += "X.X.XXXX"; cym = f"{CHINA}:1! {RIDE}:1 R:2"
    elif name == "night":
        k = ["X..x....X.......", "X.....x...X.....", "X..x....X..x....", "X.....x.X......."][i % 4]
        s = "........X......."
        cym = f"{RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1"
        if i == 0: cym = f"{CR2}:2! {RIDE}:1! {BELL}:1"
        if last: k = "X..x............"; s = "........X.X.XXXX"; cym = f"{RIDE}:1! {BELL}:1 R:2"
    elif name == "night2":
        # 悪夢の頂点: 5つずつのかたまり（16分5つ）が小節線をまたぐ
        off = i * 16
        k = "".join("X" if (off + j) % 5 == 0 else "." for j in range(16))
        s = "".join("X" if (off + j) % 5 == 3 else "." for j in range(16))
        cym = f"{CHINA}:1.25! {RIDE}:1.25 {CHINA}:1.25! {RIDE}:0.25" if i % 2 == 0 else f"{RIDE}:1.25 {CHINA}:1.25! {RIDE}:1.5"
        if last: k = "X..............."; s = "................"; cym = f"{CR}:1! R:3"
    elif name == "wake":
        cym = f"{BELL}:4," if i == 0 else None
    elif name == "chorus":
        # 1回だけの大きなサビ: ハーフタイムの大きなノリ、クラッシュは2小節ごと
        k = "X.......X.x....." if i % 2 == 0 else "X..x....X......."
        s = "........X......."
        cym = f"{RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1"
        if i % 2 == 0: cym = (f"{CR}:2! " if i % 4 == 0 else f"{CR2}:2! ") + f"{RIDE}:1! {BELL}:1"
        if i in (7,): k = "X..x....X.x.X.x."; s = "........X..X.XXX"; cym = f"{RIDE}:1! {BELL}:1 R:2"
        if last: k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if name == "intro" and i == 2: FX.append(bar("E4:4"))                     # 夢へ入るスウェル
    elif name == "fall" and i == 1: FX.append(bar("E4:4"))
    elif name == "dream3" and i == 6: FX.append(bar("E4:4"))
    elif name == "dream3" and i == 7: FX.append(bar("R:2 C4:2"))
    elif name == "dream2" and i == 4: FX.append(bar("E4:4"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("dlead"), vol=0.11, drive=0.3, role="夢の旋律（浅い歪み）", delay_beats=1.5))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(clean_part(J("clean"), vol=0.09, pan=0.25, role="クリーンの分散和音"))
song.add(part("鉄琴", "glockenspiel", J("glock"), volume=0.1, pan=-0.3, reverb=0.55, attack=0.002, release=1.5,
              fx=[{"type": "eq", "low": 0, "mid": 0, "midHz": 2000, "high": -1}, {"type": "delay", "beats": 0.75, "mix": 0.2, "feedback": 0.35}, {"type": "reverb", "mix": 0.3}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "bright-pop-rock"
add_layer(song, "piano", "月の裏側で、ひとりで弾くピアノ。")

# 展開の型（2026-10-23 人間「展開が全曲同じ」「4分から5分」）。lm25_plans.py
from lm25_plans import apply_plan
apply_plan(song, "15")
song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False    # 2026-10-24: 型は使わない

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-15-tsukinoura.json"
    song.write(out)
    check_clash(song)
