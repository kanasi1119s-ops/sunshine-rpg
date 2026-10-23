# ラウド26曲 26「BACHI」（仮。もとの仮題「鬼灯の撥」）。2026-10-24 素材から作り直し
# スタイル: 和の響きのラウドロック／メタルコア（都節のパワーコード・盆踊りの跳ね・櫓の太鼓）＋三味線2本＋尺八。E 都節・128 → 140・4/4
# 物語: 盆の夜。亡くなった祖母の撥の音が、迎え火の向こうから聞こえる。孫は同じ旋律を弾いて追いかけるが、いつも少し遅れる（1拍 → 半拍）。
#   踊りの輪、孫ひとりの叩き、櫓の太鼓をへて、ついに祖母に追いつき、二人の撥がぴったり重なる。送り火で祖母の音は遠ざかり、孫の音だけが残る。
# 形: 追いかけっこ（同じ旋律を、孫が 1拍遅れ → 半拍遅れ → ぴったり重なる。ずれが縮まっていくのが曲の筋）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   迎え火（0）: 祖母の三味線（遠い）と尺八だけ
#   追う・1拍遅れ（2）: バンドが入る。孫が1拍遅れで同じ旋律（輪唱のようにずれて聞こえる）
#   盆踊り（2）: 跳ねる踊りのリズム。リードが踊りの旋律、孫は裏拍で合いの手
#   叩き（1→2）: 孫ひとりの津軽の叩き。ベースとキックが強い音にだけ合わせる
#   追う・半拍遅れ（2→3）: 140 に上がる。ずれが半拍に縮む
#   櫓の太鼓（3）: タムの太鼓。尺八の長い息
#   重なる（3）: 二人の撥とリードが、ぴったり同じ旋律。この曲でいちばん大きい
#   送り火（0）: 祖母の音が2拍遅れの遠いこだまになって消え、孫の開放弦の E だけが残る
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *
from lm25_lib import _bar_pieces

BPM, BEATS = 128, 4
bar = Bars(BEATS)
R4 = bar.rest()

# 祖母の旋律（E 都節: E F A B C）
THEME = ["E5:0.5! F5:0.5 A5:1 B5:0.5 A5:0.5 F5:1", "E5:1.5 B4:0.5 C5:1 B4:1", "A4:0.5 B4:0.5 C5:0.5 E5:0.5 F5:1 E5:0.5 C5:0.5", "B4:2 E4:1 R:1",
         "B5:0.5! C6:0.5 B5:1 A5:0.5 F5:0.5 E5:1", "F5:1.5 E5:0.5 C5:1.5 B4:0.5", "C5:0.5 B4:0.5 A4:0.5 F4:0.5 E4:1 F4:0.5 A4:0.5", "B4:3 R:1"]
THEME_CH = ["E5", "E5", "Am", "E5", "Am", "F5", "Am", "E5"]


def delayed(bars_, d):
    """同じ旋律を d 拍遅らせる（小節線をまたぐ音は、小節の終わりで切る）"""
    nb = len(bars_)
    s = (f"R:{d:g} " if d else "") + " ".join(bars_)
    out = []
    for pcs in _bar_pieces(s, BEATS, nb):
        toks = [f"R:{L:g}" if (n is None or cont) else f"{n}:{L:g}{m}" for n, L, m, cont in pcs]
        out.append(bar(fix_len(merge_rests(" ".join(toks)), BEATS)))
    return out


FORM = [("welcome", 8), ("chase1", 24), ("ondo", 16), ("tataki", 12), ("chase2", 24), ("yagura", 12), ("reach", 28), ("farewell", 12)]
CH = {"welcome": THEME_CH, "chase1": THEME_CH * 3, "ondo": ["Am", "E5", "Am", "E5", "C5", "E5", "Am", "E5"] * 2, "tataki": ["E5"] * 12,
      "chase2": THEME_CH * 3, "yagura": ["E5", "F5", "E5", "F5"] * 3, "reach": THEME_CH * 3 + ["Am", "C5", "E5", "E5"], "farewell": THEME_CH + ["E5"] * 4}
song = Song("鬼灯の撥（仮）",
            "仮: ラウド26曲の26曲目（2026-10-24 素材から作り直し）。和の響きのラウドロック＋三味線2本＋尺八。E 都節・128 → 140。亡き祖母の撥の旋律を、"
            "孫が1拍遅れ → 半拍遅れで追いかけ、盆踊り・孫ひとりの叩き・櫓の太鼓をへて、最後に二人の撥がぴったり重なる。送り火で祖母の音が遠ざかる。自作",
            BPM, BEATS, FORM, CH)
song.flags = "--space hall --space-wet 0.1"
song.desc += " 物語: 盆の夜、祖母の撥を追いかける孫。ずれが縮まり、最後に二人の撥が重なる。"
song.kinds = {"welcome": "intro", "chase1": "verse", "ondo": "interlude", "tataki": "solo", "chase2": "pre", "yagura": "break", "reach": "chorus", "farewell": "outro"}
SECS, NB = song.secs, song.nb
MIYAKO = scale_pcs("E", "miyako")

CHASE1 = delayed(THEME * 3, 1)
CHASE2 = delayed(THEME * 3, 0.5)
FAREWELL = delayed(THEME + [R4] * 4, 2)
ONDO = [bar(x) for x in melody_walk(MIYAKO, "A4", "E5", [[0.75, 0.25, 0.75, 0.25, 1, -1], [-0.5, 0.75, 0.25, 0.5, 2], [0.75, 0.25, 1, 0.75, 0.25, 1]], 1, CH["ondo"],
                                     contour=(1, 1, -2, 1, -1), lo="E4", hi="C6")]
SOAR = [bar(x) for x in melody_walk(MIYAKO, "E5", "B5", [[2, 1, 1], [-1, 1, 2], [3, -1], [1.5, 0.5, 2]], 2, CH["reach"][16:24], contour=(1, 2, -1, -1), lo="B4", hi="E6")]
# 津軽の叩き: 開放弦（E4・B3）の16分の連打に、旋律の音を差しこむ。強い音（!）の位置を小節ごとに変える
TATAKI_ACC = ["1001001000100010", "1000100100100100", "1001000100010010", "1010010010010000"]
TATAKI_MEL = ["A4", "B4", "C5", "E5", "F5", "E5", "C5", "B4", "A4", "F4", "B4", "E5"]


def tataki(i):
    acc = TATAKI_ACC[i % 4]
    toks = []
    for j, c in enumerate(acc):
        if c == "1": toks.append(f"{TATAKI_MEL[(i + j) % len(TATAKI_MEL)] if j % 8 == 0 else ('B3' if j % 2 else 'E4')}:0.25!")
        else: toks.append(f"{'E4' if j % 2 == 0 else 'B3'}:0.25,")
    return bar(" ".join(toks))


LOW = {"E5": "E2", "Am": "A1", "C5": "C2", "F5": "F2"}
P = {k: [] for k in ["riff", "rhy", "lead", "sha", "gran", "shaku", "bass", "mute"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = sha = gran = shaku = mute = R4
    g = LOW[ch]; root = root_note(ch)
    drive = bar(f"{g}:0.5! {g}:0.5 R:0.5 {g}:0.25 {g}:0.25 {tr(g, 1)}:0.5! {g}:0.5 R:0.5 {tr(g, 7)}:0.5")
    if name == "welcome":
        gran = bar(THEME[i])
        shaku = bar("E4:4") if i in (2, 3) else (bar("B4:3 R:1") if i in (6, 7) else R4)
        b = R4
    elif name == "chase1":
        gran = bar(THEME[i % 8]); sha = CHASE1[i]
        riff = rhy = drive
        b = unison_low(drive, -1, "B0")
    elif name == "ondo":
        riff = rhy = bar(f"{g}:0.75! {g}:0.25 R:0.5 {tr(g, 7)}:0.5 {g}:0.75! {g}:0.25 {tr(g, 10 if ch != 'Am' else 3)}:1")
        lead = ONDO[i]
        sha = bar(" ".join(f"R:0.5 {t}:0.5" for t in (chord_tones(ch, 'E4', 'E5') * 4)[:4]))      # 裏拍の合いの手
        b = bar(f"{root}:0.75 {root}:0.25 R:0.5 {fifth_of(ch)}:0.5 {root}:0.75 {root}:0.25 {fifth_of(ch)}:1")
    elif name == "tataki":
        sha = tataki(i)
        acc = TATAKI_ACC[i % 4]
        b = bar(merge_rests(" ".join("E1:0.25!" if c == "1" and j % 4 == 0 else "R:0.25" for j, c in enumerate(acc)))) if i >= 4 else R4
        mute = bar("R:1.5 E1:0.25, R:2.25") if i >= 8 else R4
    elif name == "chase2":
        gran = bar(THEME[i % 8]); sha = CHASE2[i]
        riff = rhy = drive
        if i >= 16: lead = bar(shift_oct(strip_marks(THEME[i % 8]), -1))
        b = unison_low(drive, -1, "B0")
    elif name == "yagura":
        riff = rhy = bar(f"{g}:1.5! {g}:0.5 R:1 {g}:1!")
        shaku = bar(["B4:4", "C5:4", "B4:3 A4:1", "F4:4"][i % 4])
        b = bar(f"{root}:1.5! {root}:0.5 R:1 {root}:1!")
    elif name == "reach":
        if i < 24:
            gran = sha = bar(THEME[i % 8])
            lead = bar(shift_oct(strip_marks(THEME[i % 8]), -1)) if i < 16 else SOAR[i - 16]
        else:
            lead = bar(["A5:4", "C6:2 A5:2", "E6:4", "E6:2 R:2"][i - 24])
            gran = sha = bar(["A4:0.5! C5:0.5 E5:1 A5:2", "C5:0.5! E5:0.5 A5:1 C6:2", "E5:4!", "E5:2! R:2"][i - 24])
        riff = rhy = drive if i < 26 else (bar(f"{g}:4!") if i == 26 else bar(f"{g}:2! R:2"))
        b = unison_low(riff, -1, "B0")
    else:   # farewell
        if i < 8: sha = bar(strip_marks(THEME[i])); gran = bar(" ".join(x if x.startswith("R") else x.split(":")[0] + ":" + x.split(":")[1] + "," for x in FAREWELL[i].split()).replace(",,", ","))
        else: sha = bar(["E4:4", "B3:4", "E4:4", "R:4"][i - 8])
        b = bar(f"{root}:4,") if i in (0, 4) else R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["sha"].append(sha); P["gran"].append(gran); P["shaku"].append(shaku); P["bass"].append(b); P["mute"].append(mute)
    kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
SHA_FX = [{"type": "eq", "low": -3, "mid": 2, "midHz": 2500, "high": 1}, {"type": "room", "mix": 0.18}]
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(part("三味線（孫・近い）", "shamisen", J("sha"), volume=0.16, pan=0.22, reverb=0.25, attack=0.002, release=0.5, fx=SHA_FX))
song.add(part("三味線（祖母・遠い）", "shamisen", J("gran"), volume=0.13, pan=-0.4, reverb=0.6, attack=0.002, release=0.7,
              fx=[{"type": "eq", "low": -4, "mid": 1, "midHz": 2000, "high": -2}, {"type": "reverb", "mix": 0.35}]))
song.add(part("追加の楽器: 尺八（祖母の息）", "shakuhachi", J("shaku"), volume=0.11, pan=-0.2, reverb=0.5, attack=0.3, release=0.6))
song.add(bass_part(J("bass")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [8 + 24 + 16 + 12 + 24 + 12]     # 二人の撥が重なった瞬間に一度だけ
song.ref_tone = "wide-dark-wall"

from lm25_plans import apply_plan
apply_plan(song, "26")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-26-hozuki.json"
    song.write(out)
    check_clash(song)
