# ギターだけの試し書き出し: old（今までの部品）/ newA（左=根音・5度・オクターブ、右=三和音）/ newB（左=10度入り、右=三和音）
import sys, os
sys.path.insert(0, "/home/claude/wt-mix/assets-src/ai-songs/_gen")
mode = os.environ["GT"]; out = sys.argv[1]
sys.argv = [sys.argv[0], out]
from vocalo_lib import *
import gtr2_lib as G2, random as _r
CH = ["Bm", "G", "D", "A", "Em7", "F#m", "Asus4", "D"]
S = Song("99", "gtest", "ギターの試し", "gtest", 146, 4, "B", "minor", "試し")
S.kit = "naked-x"; S.flags = "--bass bnb-loud --ref-tone bright-nu-wall " + S.flags
S.scene("試し", 8, "break", CH); S.keep_old_synth = True; S.no_depth = True; S.keepers = {}
V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False); D = S.drumkit(); LY = Lyrics(S); RNG = _r.Random(1)
drv = float(os.environ.get("DRV", "0")) or None
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.085, -0.6, tone="nu-metal-wall")) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.08, 0.6, tone="nu-metal-wall", drive=drv)) for i in range(6)]
if mode == "old":
    for b in range(8): gtr_strum(GL, S, b, "x-----x-----x---", CH[b], RNG, strings=3); gtr_strum(GR, S, b, "x---------x-----" if b % 2 == 0 else "x-----x---x-----", CH[b], RNG, strings=4)
else:
    L, R = G2.Strummer(GL, S, 1), G2.Strummer(GR, S, 2); prev = None
    for b in range(8):
        prev = G2.triad(CH[b], prev)
        L.bar(b, "D-----d-D---d---", G2.low_shape(CH[b], with_third=(mode == "newB")))
        R.bar(b, "D-dU-UD-D-dU-Ud-" if b % 2 == 0 else "D--U-Ud-D-d-dU--", prev)
        print(CH[b], "低:", [nm(m) for _, m in G2.low_shape(CH[b], with_third=(mode == "newB"))], "三和音:", [(s, nm(m)) for s, m in prev], "生:", [nm(m) for _, m in G2.open_shape(CH[b])])
    L.end(8); R.end(8)
S.desc = "試し"; finish(S, LY, V, 0)
from vt3x_lib import *
js = load(out)
if mode == "old": gtr_velocity(js, "Lギター", 3); gtr_velocity(js, "Rギター", 4)
else: print("強さを付けた:", L.velocity(js) + R.velocity(js), "音  ストローク:", L.count, R.count)
save(out, js)
