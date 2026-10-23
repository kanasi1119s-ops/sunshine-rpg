# ラウド26曲 03「EYEWALL」（仮。もとの仮題「嵐の背骨」）。2026-10-24 素材から作り直し
# スタイル: 前半はスラッシュ（速い16分の刻みとギャロップ）、後半はドゥーム／スラッジ（遅く重い）。D 自然的短音階・138 → 72（目）→ 100（背後の壁）・4/4。チェロ
# 物語: 台風の通過。外側の暴風の壁 → 台風の目（完全な静けさ、青空がのぞく）→ 反対側の暴風（前半より重く遅い）→ 突然、切れる。
# 形: 通過（暴風・目・暴風の3部。サビは後半の頂点に1回だけ）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   近づく嵐（0→1）: チェロの低いトレモロと、遠いタムのうなり
#   外側の壁（2→3）: 速い刻み。旋律は叫ぶような2音の短い連打（長く歌わない）。チェロは低いうなりで刻みに重なる
#   目（0）: 72 に落ちる。クリーンの分散和音とチェロの長い息の旋律だけ。ドラムはほぼなし
#   背後の壁（3）: 100 のハーフタイムで、前半より低く重い。頂点の16小節だけ、リードとチェロがこの曲で一度だけのサビを歌う
#   終わり: 拍の頭で全員が切れて、無音
# 旋律の性格: 前半は2音の叫び（短い・強い・休みが多い）、目は長い息（ここだけはわざと伸ばす）、サビは4分の3連符で拍とずれて歌う
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 138, 4
bar = Bars(BEATS)
R4 = bar.rest()

WALL = ["Dm", "Dm", "Bb", "C", "Dm", "Dm", "Gm", "A"]
FORM = [("approach", 8), ("wall1", 32), ("eye", 24), ("wall2", 40)]
CH = {"approach": ["Dm"] * 8, "wall1": WALL * 4,
      "eye": ["Dm9", "Bbmaj7", "Fmaj7", "C", "Dm9", "Bbmaj7", "Gm9", "A7sus4"] * 3,
      "wall2": ["Dm", "Dm", "Bb", "Bb", "Gm", "Gm", "A", "A"] * 2 + ["Bb", "C", "Dm", "Bb", "Bb", "C", "A", "A"] * 2 + ["Dm", "Eb", "Dm", "Eb", "Dm", "Eb", "Dm", "Dm"]}
song = Song("嵐の背骨（仮）",
            "仮: ラウド26曲の3曲目（2026-10-24 素材から作り直し）。前半スラッシュ（138）、台風の目（72）、後半ドゥーム（100）。D 自然的短音階。"
            "旋律は前半が2音の叫び、目はチェロの長い息、サビは後半の頂点に1回だけ。最後は拍の頭で切れる。別の楽器はチェロ。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 台風の通過。外側の暴風、目の中の青空、反対側のもっと重い暴風、そして突然の静けさ。"
song.kinds = {"approach": "intro", "wall1": "chorus", "eye": "bridge", "wall2": "break"}
SECS, NB = song.secs, song.nb

LOWR = {"Dm": "D2", "Bb": "A#1", "C": "C2", "Gm": "G1", "A": "A1", "Eb": "D#2"}


def thrash(ch, var):
    """16分の速い刻み（開放弦のペダルに、半音で下りる線とギャロップ）"""
    r = LOWR[ch]; o = up(r, 1); m3 = tr(r, 3); f4 = tr(r, 5); b2 = tr(r, 1)
    pats = [f"{r}:0.25! {r}:0.25 {r}:0.25 {r}:0.25 {m3}:0.25! {r}:0.25 {r}:0.25 {b2}:0.25 {r}:0.25! {r}:0.25 {tr(r, 7)}:0.25 {tr(r, 6)}:0.25 {f4}:0.25 {m3}:0.25 {tr(r, 2)}:0.25 {r}:0.25",
            f"{r}:0.5! {r}:0.25 {r}:0.25 {r}:0.5! {r}:0.25 {r}:0.25 {o}:0.25! {tr(r, 10)}:0.25 {tr(r, 7)}:0.25 {f4}:0.25 {r}:0.5! {b2}:0.5",
            f"{r}:0.25! {r}:0.25 {f4}:0.25 {r}:0.25 {r}:0.25! {r}:0.25 {tr(r, 6)}:0.25 {r}:0.25 {r}:0.25! {r}:0.25 {f4}:0.25 {r}:0.25 {m3}:0.5! {b2}:0.5"]
    return bar(pats[var % 3])


def sludge(ch, var):
    """背後の壁: 遅く重い（伸ばしと半音のずり下がり）"""
    r = LOWR[ch]
    pats = [f"{r}:1.5! {r}:0.5 {tr(r, 3)}:1 {tr(r, 2)}:0.5 {tr(r, 1)}:0.5", f"{r}:0.75! {r}:0.75 {r}:0.5 R:0.5 {tr(r, 7)}:0.5! {tr(r, 6)}:0.5 {r}:0.5",
            f"{r}:2! R:0.5 {r}:0.25 {r}:0.25 {tr(r, 1)}:0.5! {r}:0.5"]
    return bar(pats[var % 3])


# 外側の壁の旋律: 2音の叫び（9〜32小節）
SHOUT = [bar("R:0.5 A4:0.25 F4:0.75! R:1 A4:0.25 F4:0.75! R:0.5"), bar("R:0.5 A4:0.25 D5:0.75! R:2.5"),
         bar("R:0.5 F4:0.25 D4:0.75! R:1 F4:0.25 A#4:0.75! R:0.5"), bar("R:1 C5:0.25 G4:0.75! R:0.5 E4:0.25 G4:0.25 R:1"),
         bar("R:0.5 D5:0.25 A4:0.75! R:1 D5:0.25 F5:0.75! R:0.5"), bar("R:0.25 E5:0.25 D5:0.5 A4:0.5! R:2.5"),
         bar("R:0.5 D5:0.25 A#4:0.75! R:1 G4:0.25 A#4:0.75! R:0.5"), bar("R:0.5 C#5:0.25 A4:0.75! R:0.5 C#5:0.25 E5:0.25 R:1.5")]
SHOUT2 = [bar("A4:0.25 F4:0.25 R:0.5 A4:0.25 F4:0.25 R:0.5 D5:1! R:1"), bar("R:2 D5:0.25 E5:0.25 F5:0.5! R:1"),
          bar("A#4:0.25 F4:0.25 R:0.5 A#4:0.25 F4:0.25 R:0.5 D5:1! R:1"), bar("R:2 C5:0.25 D5:0.25 E5:0.5! R:1"),
          bar("F5:0.25 D5:0.25 R:0.5 F5:0.25 D5:0.25 R:0.5 A4:1! R:1"), bar("R:0.5 F5:0.25 E5:0.25 D5:0.5 A4:0.5 R:2"),
          bar("D5:0.25 A#4:0.25 R:0.5 D5:0.25 A#4:0.25 R:0.5 G4:1! R:1"), bar("R:1 E5:0.5 C#5:0.5! A4:0.5 R:1.5")]
# 目: チェロの長い息（わざと伸ばす。息つぎの休みを置く）
EYE_CELLO = [bar("R:1 A3:3"), bar("D4:2 C4:1 A#3:1"), bar("A3:4"), bar("R:1 G3:1 A3:1 C4:1"),
             bar("D4:3 E4:1"), bar("F4:2 D4:2"), bar("D4:1 C4:1 A#3:2"), bar("A3:2 R:2"),
             bar("R:1 F4:1 E4:1 D4:1"), bar("C4:3 A3:1"), bar("A3:2 C4:2"), bar("E4:2 R:2"),
             bar("D4:2 F4:2"), bar("A4:3 G4:1"), bar("F4:2 D4:2"), bar("E4:4"),
             bar("R:1 A4:2 G4:1"), bar("F4:2 E4:1 D4:1"), bar("C4:4"), bar("R:2 C4:1 D4:1"),
             bar("D4:4"), bar("D4:2 R:2"), bar("R:4"), bar("R:4")]
# 背後の壁の頂点（17〜32小節）: この曲で一度だけのサビ。4分の3連符で拍とずれて歌う
CHORUS = [bar("R:0.5 A4:0.5 D5:0.667 E5:0.667 F5:0.666 E5:0.5 D5:0.5"), bar("C5:0.667 D5:0.667 E5:0.666 C5:1 R:1"),
          bar("R:0.5 F4:0.5 A4:0.667 C5:0.667 D5:0.666 C5:0.5 A4:0.5"), bar("A#4:2 R:0.5 G4:0.5 A4:0.5 C5:0.5"),
          bar("D5:0.667 F5:0.667 E5:0.666 D5:0.5 C5:0.5 A4:1"), bar("R:0.5 A#4:0.5 D5:0.667 C5:0.667 A#4:0.666 A4:1"),
          bar("R:0.5 E4:0.5 A4:0.667 C#5:0.667 E5:0.666 D5:0.5 C#5:0.5"), bar("A4:1.5 R:2.5"),
          bar("R:0.5 D5:0.5 F5:0.667 E5:0.667 D5:0.666 E5:0.5 F5:0.5"), bar("E5:0.667 D5:0.667 C5:0.666 G4:1 R:1"),
          bar("R:0.5 A4:0.5 D5:0.667 E5:0.667 F5:0.666 D5:1"), bar("R:0.5 F5:0.5 E5:0.667 D5:0.667 C5:0.666 D5:1"),
          bar("A#4:0.667 D5:0.667 F5:0.666 E5:0.5 D5:0.5 A#4:1"), bar("C5:0.667 E5:0.667 G4:0.666 C5:1 R:1"),
          bar("R:0.5 C#5:0.5 E5:0.667 D5:0.667 C#5:0.666 A4:1"), bar("A4:1 R:3")]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "cello", "clean", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]; last = i == n - 1
    riff = rhy = lead = cello = clean = R4
    root = root_note(ch)
    if name == "approach":
        # 2026-10-24: 前奏が小さすぎないように（人間「前奏が小さすぎる曲があるから、作るときチェックして」）。チェロのうなりは1小節目から
        cello = bar(" ".join(["D2:0.25" + ("!" if j % 4 == 0 else "") for j in range(16)]))
        b = bar("D1:4,") if i < 4 else bar("D1:4")
        tom = ("R:3 A1:0.25, A1:0.25, G1:0.25, G1:0.25," if i % 2 else "R:4") if i >= 2 else "R:4"
        kit.add(None, None, None, tom, (f"C2:4" if last else None))
    elif name == "wall1":
        riff = thrash(ch, i // 2)
        rhy = riff if i >= 8 else R4
        lead = (SHOUT if i < 16 else SHOUT2)[i % 8] if i >= 8 else R4
        cello = bar(" ".join([f"{up(LOWR[ch], 1)}:0.25,"] * 16)) if i >= 16 else R4
        b = unison_low(riff, -1, "B0")
        kit.add("X.X.X.X.X.X.X.X.", "....X.......X...", "x.x.x.x.x.x.x.x.")
    elif name == "eye":
        tones = chord_tones(ch, "D3", "D5")
        arp = [tones[j % len(tones)] for j in (0, 2, 1, 3, 2, 4, 3, 1)]
        clean = bar(" ".join(f"{t}:0.5" for t in arp)) if i < 22 else (bar(f"{tones[0]}:4") if i == 22 else R4)
        cello = EYE_CELLO[i]
        b = bar(f"{root}:4,") if i % 2 == 0 and i < 22 else R4
        kit.add(None, None, None, None, ("D2:4," if i % 4 == 0 and i < 20 else None))
    else:   # wall2
        if i < 16:
            riff = rhy = sludge(ch, i)
            cello = bar(f"{up(LOWR[ch], 1)}:4") if i % 2 == 0 else R4
        elif i < 32:
            riff = rhy = sludge(ch, i + 1)
            lead = CHORUS[i - 16]; cello = shift_oct(strip_marks(lead), -1)
        elif i < n - 1:
            riff = rhy = bar(f"{LOWR[ch]}:0.75! {LOWR[ch]}:0.75! {LOWR[ch]}:0.5! R:0.5 {tr(LOWR[ch], 1)}:0.5! R:1")
        else:
            riff = rhy = bar("D2:0.5! R:3.5")                     # 最後: 拍の頭の一撃で切れる
        b = unison_low(riff, -1, "B0")
        kit.add("X.......X.......", "........X.......", "x...x...x...x...")
    P["riff"].append(riff); P["rhy"].append(rhy); P["rhy_in"].append(rhy); P["lead"].append(lead); P["cello"].append(cello)
    P["clean"].append(clean); P["bass"].append(b)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(clean_part(J("clean"), vol=0.08, pan=0.25, role="クリーンの分散和音（目）"))
song.add(part("チェロ", "strings", J("cello"), patch="cello", volume=0.18, pan=-0.2, reverb=0.45, attack=0.1, release=0.6, phrase=8,
              fx=[{"type": "eq", "low": 1, "mid": -1.5, "midHz": 2500, "high": 0}, {"type": "reverb", "mix": 0.2}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [8 + 32 + 24 + 31]          # サビの最後（頂点の終わり）に一度だけ
song.ref_tone = "wide-dark-wall"

from lm25_plans import apply_plan
apply_plan(song, "03")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-03-arashi.json"
    song.write(out)
    check_clash(song)
