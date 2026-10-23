# ラウド26曲 05「Seven Horns, No Halo」（仮。もとの仮題「七つの角」）。2026-10-24 素材から作り直し
# スタイル: ブラッケンド（トレモロピッキングの刻み・ブラストビート）＋三味線。E フリジアン・ドミナント（E F G♯ A B C D）・112・5/4（3+2）
# 物語: 悪魔を呼び出す儀式。三味線が呪文を唱え、バンドが答える。答えるたびに角が1本ずつ生える（旋律の音が1つずつ増える）。
#       5回目で一度すべてが消える（儀式が失敗したと思わせる罠）。6回目・7回目で七本の角がそろう。
# 形: 呪文（三味線の呼びかけ4小節＋バンドの答え8小節）×7。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ: 1回目（1）→2回目（1）→3回目（2）→4回目（2→3）→5回目（罠: 0。三味線と心拍だけ）→6回目（3）→7回目（3）
# 旋律の性格: トレモロ（同じ音を16分で刻み続ける長い音）と、増2度（F→G♯）の跳躍。回ごとに使う音が1つずつ増える
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 112, 5
bar = Bars(BEATS)
R5 = bar.rest()

HORNS = ["E4", "F4", "G#4", "A4", "B4", "C5", "D5"]
RESP = ["E", "F", "E", "F", "Am", "G#dim", "F", "E"]
FORM = [("summon", 4)] + [x for k in range(1, 8) for x in ((f"call{k}", 4), (f"answer{k}", 8))] + [("crown", 6)]
CH = {"summon": ["E"] * 4, "crown": ["E", "F", "E", "F", "E", "E"]}
for k in range(1, 8): CH[f"call{k}"] = ["E"] * 4; CH[f"answer{k}"] = RESP
song = Song("七つの角（仮）",
            "仮: ラウド26曲の5曲目（2026-10-24 素材から作り直し）。ブラッケンド＋三味線。E フリジアン・ドミナント・112・5/4（3+2）。"
            "三味線の呪文とバンドの答えを7回。答えるたびに旋律の音（角）が1つ増える。5回目は罠（全部消える）。旋律はトレモロと増2度。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 悪魔を呼び出す儀式。答えるたびに角が1本ずつ生え、5回目で失敗したかに見えて、七本の角がそろう。"
song.kinds = {"summon": "intro", "crown": "outro", **{f"call{k}": "interlude" for k in range(1, 8)}, **{f"answer{k}": ("bridge" if k == 5 else "chorus") for k in range(1, 8)}}
SECS, NB = song.secs, song.nb

LOW = {"E": "E2", "F": "F2", "Am": "A1", "G#dim": "G#1"}


def trem(note, beats):
    """トレモロ: 同じ音を16分で刻む"""
    n = int(round(beats / 0.25))
    return " ".join(f"{note}:0.25{'!' if j == 0 else ''}" for j in range(n))


def black_riff(ch, var):
    r = LOW[ch]; f5 = tr(r, 7)
    if var % 2 == 0: return bar(trem(r, 3) + " " + trem(f5, 2))
    return bar(trem(r, 1.5) + " " + trem(tr(r, 1), 1.5) + " " + trem(r, 2))


def call(k, i):
    """三味線の呪文（3+2）。回ごとに、角の音を1つ足して長くなる"""
    hs = HORNS[:min(7, k + 1)]
    seq = [hs[j % len(hs)] for j in range(8)]
    pats = [f"E4:0.5! R:0.25 E4:0.25 {seq[1]}:0.5 {seq[2]}:0.25 R:0.25 E4:0.5! R:0.5 {seq[3]}:0.25 {seq[2]}:0.25 E4:0.5 R:1",
            f"R:0.5 F4:0.25 G#4:0.25 F4:0.5 E4:0.5! R:1 {seq[4]}:0.25 {seq[5]}:0.25 {seq[4]}:0.5 E4:0.5 R:0.5",
            f"E4:0.25! E4:0.25 E4:0.25 E4:0.25 {seq[6]}:0.5 {seq[5]}:0.5 R:0.5 G#4:0.25 F4:0.25 E4:0.5! R:1.5",
            f"R:1 {seq[7]}:0.5! {seq[6]}:0.5 {seq[5]}:0.5 F4:0.25 G#4:0.25 E4:1! R:1"]
    return bar(pats[i % 4])


def answer_lead(k, i):
    """答えの旋律: その回までに生えた角の音だけで、トレモロの長い音と増2度の跳躍。小節ごとに区切り方（3+2・2+3・1+1+3…）を変える"""
    hs = HORNS[:k]
    shapes = [[3, 2], [2, 0.5, 0.5, -2], [1.5, 1.5, 2], [-0.5, 2.5, 2], [1, 1, 3], [3, -0.5, 0.5, 1], [2, 3], [4, -1]]
    sh = shapes[(i + k * 3) % 8]
    out, j = [], i * 2
    for d in sh:
        if d < 0: out.append(f"R:{-d:g}"); continue
        note = hs[j % len(hs)]; j += 1 if len(hs) < 3 else 2
        fast = k >= 6 and d >= 2 and (i % 2 == 1)
        if d <= 0.5: out.append(f"{note}:{d:g}!")
        elif fast:                                   # 6連のトレモロ（もっと速く、儀式の最後で）
            nn = int(round(d * 6)); ds = [0.1667] * nn; ds[-1] = round(d - 0.1667 * (nn - 1), 4)   # 合計がぴったり d になるように
            out.append(" ".join(f"{note}:{ds[q]:g}{'!' if q == 0 else ''}" for q in range(nn)))
        else: out.append(trem(note, d))
    return bar(fix_len(" ".join(out), 5))


P = {k: [] for k in ["riff", "rhy", "lead", "shami", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = shami = R5
    root = root_note(ch)
    if name == "summon":
        # 2026-10-24: 前奏が小さすぎた（三味線のまばらな音だけだった）→ 低いうなり（ベースの持続）と、儀式の太鼓を最初から
        shami = call(1, i)
        b = bar("E1:5")
    elif name.startswith("call"):
        k = int(name[4:])
        shami = call(k, i)
        b = bar(f"E1:3, R:2") if k >= 2 else bar("E1:5")
        if k >= 6: riff = bar(f"E2:0.5! R:2.5 E2:0.5! R:1.5")      # 角がそろうころ: 呪文の合間に一撃
    elif name.startswith("answer"):
        k = int(name[6:])
        if k == 5:
            shami = call(5, i)                                       # 罠: 三味線だけが残る
            b = R5
        else:
            riff = black_riff(ch, i + k)
            rhy = riff if k >= 2 else R5
            lead = answer_lead(k, i) if (k >= 2 or i >= 4) else R5
            if k >= 6: shami = strip_marks(answer_lead(k, i))       # 6回目から三味線も答えに加わる
            b = bar(f"{root}:3! {root}:2") if k < 4 else bar(trem(root, 3) + " " + trem(root, 2))
    else:   # crown
        riff = rhy = black_riff(ch, i) if i < 4 else (bar("E2:5!") if i == 4 else R5)
        lead = (bar(trem("E5", 3) + " " + trem("D5", 2)) if ch == "E" else bar(trem("C5", 3) + " " + trem("A4", 2))) if i < 4 else (bar("E5:5!") if i == 4 else R5)
        shami = bar("E4:0.5! R:4.5") if i == 5 else R5
        b = bar(f"{root}:5!") if i < 5 else R5
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["shami"].append(shami); P["bass"].append(b)
    kit.add("X" + "." * 19, "." * 12 + "X" + "." * 7, "".join("x" if j % 4 == 0 else "." for j in range(20)))

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(part("三味線", "shamisen", J("shami"), volume=0.17, pan=-0.22, reverb=0.3, attack=0.002, release=0.5,
              fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 1800, "high": 1}, {"type": "delay", "beats": 0.75, "mix": 0.15, "feedback": 0.25}, {"type": "plate", "mix": 0.18}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [4 + 12 * 6 + 4 + 7]            # 7回目の答えの最後（七本目の角）に一度だけ
song.ref_tone = "deep-scoop-djent"

from lm25_plans import apply_plan
apply_plan(song, "05")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-05-tsuno.json"
    song.write(out)
    check_clash(song)
