import sys, os
sys.path.insert(0, "/home/claude/wt-mix/assets-src/ai-songs/_gen")
out = sys.argv[1]; vol = float(os.environ["VOL"]); kind = os.environ.get("KIND", "nylon"); sys.argv = [sys.argv[0], out]
from vocalo_lib import *
S = Song("98", "vtest", "音量の試し", "vtest", 120, 4, "C", "major", "試し"); S.kit = "naked-x"
S.scene("試し", 4, "break", ["C"] * 4); S.keep_old_synth = True; S.no_depth = True; S.keepers = {}
V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False); D = S.drumkit(); LY = Lyrics(S)
REF = [S.track(f"基準のピアノ{i}", "piano", volume=0.3, pan=0.0, reverb=0) for i in range(4)]
if kind == "nylon": T = S.track("試すパート", "guitar", patch="nylonGuitar", amp="clean", volume=vol, pan=1.0, reverb=0, chorus=0)
elif kind == "dist": T = S.track("試すパート", "distGuitar", **{**rock_gtr_spec(vol, 1.0, tone="nu-metal-wall")})
elif kind == "pluck": T = S.track("試すパート", "lead", patch="surgeNicePluck", volume=vol, pan=1.0, reverb=0)
elif kind == "trumpet": T = S.track("試すパート", "brass", patch="trumpet", volume=vol, pan=1.0, reverb=0)
g = float(os.environ.get("BOOST", "0"))
if g: T.spec["fx"] = list(T.spec.get("fx", [])) + [{"type": "boost", "gain": g}]
if os.environ.get("GDB"): T.spec["ampLevel"] = float(os.environ["GDB"])
for b in range(4):
    for i, n in enumerate(("C2", "C3", "G3", "E4")): REF[i].bar(b, f"{n}:1 {n}:1 {n}:1 {n}:1")
    T.bar(b, "E3:1 G3:1 C4:1 G3:1")
S.desc = "試し"; finish(S, LY, V, 0)
