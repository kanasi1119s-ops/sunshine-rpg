# ギターの聞きくらべ（B のサビの和音・テンポ 144）。5通り × 4小節、あいだに1小節の休み
from vocalo_lib import *
import gtr2_lib as G2
S = Song("96", "gtrab", "ギターの聞きくらべ", "guitar ab", 144, 4, "E", "major", "見本")
S.kit = "crocell-punch"; S.flags = S.flags + " --space room --space-wet 0.08"
CH = ["E", "F#/E", "Amaj7", "Am6"]
for k in range(4): S.scene(f"{k + 1}", 5, "break", CH + ["E"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}
V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False); D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)
SUB = S.track("シンセの低いベース", "bass", patch="kfbSub", volume=0.066, pan=0, duck=0.12)
def mk(name, spec_l, spec_r, inst="distGuitar"):
    return (G2.Strummer([S.track(f"{name}L{i}", inst, **spec_l) for i in range(6)], S, 1), G2.Strummer([S.track(f"{name}R{i}", inst, **spec_r) for i in range(6)], S, 2))
import re as _re
def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "dim" if ("m7b5" in rest or "dim" in rest) else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")
L1 = lambda: {**rock_gtr_spec(0.40, -0.6, tone="marshall-mid", drive=0.18), "sustain": 3.0, "release": 0.8}; R1 = lambda: {**rock_gtr_spec(0.38, 0.6, tone="marshall-mid", drive=0.15), "sustain": 3.0, "release": 0.8}
A1 = mk("1", L1(), R1()); A2 = mk("2", {**L1(), "release": 0.9}, {**R1(), "release": 0.9})
A3 = mk("3", rock_gtr_spec(0.21, -0.6, tone="glossy-jrock"), rock_gtr_spec(0.20, 0.6, tone="glossy-jrock")); A4 = mk("4", {**rock_gtr_spec(0.21, -0.6, tone="glossy-jrock"), "release": 0.9}, {**rock_gtr_spec(0.20, 0.6, tone="glossy-jrock"), "release": 0.9})
for a_ in (A2, A4):
    for st in a_: st.gap = 0.0
A5 = A4
tri = None
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    ch = S.chords[b]
    if i == 4:
        a = (A1, A2, A3, A4)[int(n) - 1]; a[0].bar(b, "." * 16, G2.low_shape(ch), feel=16); a[1].bar(b, "." * 16, G2.triad(ch, None), feel=16); continue; r = low(ch, "E1"); SUB.bar(b, f"{N(r)}:1.5 R:1 {N(r)}:1.5"); D.set(b, "X.....X...X.....", "....X.......X...", "x.x.x.x.x.x.x.x.")
    tri = G2.triad(ch, tri); lo = G2.low_shape(ch); op = G2.open_shape(ch); pl, pr = ("D-d-d-D-d-d-D-d-", "D-d-D-d-d-D-d-d-")[i % 2], ("D-U-D-U---U-D-U-", "D---D-U-D-U-D-U-")[i % 2]
    lo2 = G2.low_shape(simple(ch), with_third=False); tri2 = G2.triad(simple(ch), globals().get("_p2"), top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5))); globals()["_p2"] = tri2
    if n == "1": A1[0].bar(b, "D-----d---d-----", lo, feel=16); A1[1].bar(b, "D-----d---d-----", tri, feel=16)
    elif n == "2": A2[0].bar(b, "D-----d---d-----", lo2, feel=16); A2[1].bar(b, "D-----d---d-----", tri2, feel=16)
    elif n == "3": A3[0].bar(b, pl, lo, feel="down"); A3[1].bar(b, pr, tri)
    elif n == "4": A4[0].bar(b, pl, lo2, feel="down"); A4[1].bar(b, pr, tri2)
for a in (A1, A2, A3, A4):
    for st in a: st.end(S.nb)
S.fade_out = 0; S.desc = "見本"
finish(S, LY, V, 0, flat=True)
