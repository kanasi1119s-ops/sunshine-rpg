# 21「屋上プラネタリウム」の前奏のギターの弾き方 聞きくらべ（2026-11-20。人間「前奏のギターの弾き方違うかなー」）。案ごとに8小節。和音は前奏と同じ
# 使い方: python3 tools/vt3/intro21_demo.py <出力.json> → node tools/composer/song.mjs build <出力.json> --wav $(cat <出力.json>.flags)
import sys, re, random as _r
sys.path.insert(0, "/home/claude/wt-mix/assets-src/ai-songs/_gen")
from vocalo_lib import *
import gtr2_lib as G2
CH = ["Bm", "Bm", "G", "G", "Em7", "Em7", "A", "A"]
HOOK = ["F#5:0.75 D5:0.75 B4:0.5 C#5:0.5 D5:0.5 F#5:1", "E5:0.75 D5:0.75 B4:2.5", "G5:0.75 D5:0.75 B4:0.5 C#5:0.5 D5:0.5 G5:1", "F#5:0.75 D5:0.75 B4:2.5",
        "G5:0.75 E5:0.75 B4:0.5 D5:0.5 E5:0.5 G5:1", "F#5:0.75 E5:0.75 B4:2.5", "A5:0.75 E5:0.75 C#5:0.5 D5:0.5 E5:0.5 A5:1", "G5:0.75 E5:0.75 C#5:1 E5:1.5"]
def shift(s, n): return " ".join(x if x.startswith("R") else re.sub(r"^[A-G][#b]?\d", lambda m: nm(midi(m.group(0)) + n), x) for x in s.split())
STYLES = ["A 左右で和音をかき鳴らす", "B 和音のキメ（食いこみ）", "C 左は和音・右はオクターブの旋律"]
S = Song("96", "intro21", "21 前奏のギター 聞きくらべ", "intro guitar demo", 146, 4, "B", "minor", "見本")
S.kit = "naked-x"; S.flags = "--bass bnb-loud --ref-tone bright-nu-wall " + S.flags
for n in STYLES: S.scene(n, 8, "break", CH)
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}
V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False); D = S.drumkit(); LY = Lyrics(S); RNG = _r.Random(5)
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.16, -0.6, tone="nu-metal-wall")) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.15, 0.6, tone="nu-metal-wall")) for i in range(6)]
BASS = S.track("ベース", "bass", **rock_bass_spec(0.2))
SL, SR = G2.Strummer(GL, S, 1), G2.Strummer(GR, S, 2); tri = None
N = nm
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); ch = CH[i]; tri = G2.triad(ch, tri); low_ = G2.low_shape(ch); r = low(ch, "E1"); odd = i % 2
    s = n[0]
    if s == "B":      # 全員で同じ食いこみ（3・3・2）を打ち、すき間は裏の空ピッキングとブラッシングでつなぐ
        BASS.bar(b, f"{N(r)}:1.5 {N(r)}:1.5 {N(r)}:1" if not odd else f"{N(r)}:1.5 {N(r)}:1 {N(r)}:0.5 {N(r)}:0.5 {N(r)}:0.5")
        D.set(b, "X.....X.....X..." if not odd else "X.....X...X.X...", "....X.......X...", "X.x.X.x.X.x.X.x.")
        SL.bar(b, ("D--x-xD--x-xD-x-", "D--x-xD---D-D-d-")[odd], low_, feel="down")
        SR.bar(b, ("D-xUxUD-xUxUD-dU", "D-xUxUD-xUD-D-dU")[odd], tri, feel=16)
    else:
        BASS.bar(b, " ".join(f"{N(r)}:0.5" for _ in range(8))); feel(D, b, "rock8" if not odd else "rock8b")
        if s == "A":  # 左＝低い和音を8分でぜんぶダウン、右＝16分で下・上（手は止めない）。2小節ごとの終わりに食いこみ
            SL.bar(b, ("D-d-d-D-d-d-D-d-", "D-d-D-d-d-D-d-D-")[odd], low_, feel="down")
            SR.bar(b, ("D-dUdUD-dUdUD-dU", "D-dU-UdUD-dUdUdU")[odd], tri, feel=16)
        else:         # 左＝低い和音を8分、右＝フックの旋律をオクターブ奏法で
            SL.bar(b, ("D-d-d-D-d-d-D-d-", "D-d-D-d-d-D-d-d-")[odd], low_, feel="down")
            G2.octaves(SR, 2, 4, S, b, shift(HOOK[i], -24))
    if i == 0: crash(D, b, "C2", 4)
for st in (SL, SR): st.end(S.nb)
S.desc = "21 前奏のギターの弾き方 聞きくらべ（案ごとに8小節）"; finish(S, LY, V, 0)
from vt3x_lib import *
out = sys.argv[1]; js = load(out); n = sum(st.velocity(js) for st in (SL, SR)); save(out, js)
print("強さを付けた:", n)
