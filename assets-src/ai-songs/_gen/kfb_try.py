# Kawaii future bass の試作（4方向。各30秒ほど）。仮。
# 人間（2026-11-15）:「Kawaii_future_bassも色々試してみて」「もうちょいドラムの感じ勉強してみて。色々アクセントとかも勉強して。」
# 使い方: KT=1|2|3|4 VB_VOCAL=1 python3 kfb_try.py <出力.json>
# docs/sound/kawaii-future-bass-100.md の番号から、方向ごとにちがう組み合わせを選ぶ（かっこの数字）。ドラムの感じ（FEEL）とアクセントも方向ごとに変える。
#   1「王道のドロップ」150・F長調 … 半分の速さ(31)・クラップ重ね(32)・半音ずつ下がる和音(4)・ポンプ(11)・小節ごとに変わる刻み(13,14)・ベースも同じ型(25)・声とリードのかけ合い(47)・ハイハットのロール(34)・上がる音とインパクト(71,73)
#   2「カワイイ・ハウス」128・A長調 … 4つ打ち(39)・ウラのハイハット・3・3・2 のリリースカット(18,19)・ベル主役(43)・ウラ打ちのベース・歌の休みにアルペジオ(51,54)・sus4 の解決(3)・指パッチン(40)
#   3「かわいくない音でかわいい曲」170・D短調 … ひずませたブレイクビート(38)・オルゴール(43)・サブを長く(21)・すき間の多い和音(100)・テープストップ(77)・サブドロップ(29)
#   4「ドラムなしのポンプ」140・C リディア … 音量を拍で刻む(12,13)・リディアの♯4(7)・キックなし・クラップと指パッチンだけ(35,40)・すべるサブ(24)・きらきら(75)・全員1小節休み(80)
# 歌詞は同じ（大事な言葉は言いかえ: 夢＝星ひとつぶ）: ほしをひとつぶ／てのひらにのせ／あしたのそらへ／なげてみようか
from vocalo_lib import *
KT = os.environ.get("KT", "1")
def M(pat, degs): return mel16(pat, degs.split())


TXT = "ほしをひとつぶ/てのひらにのせ/あしたのそらへ/なげてみようか"
SPEC = {"1": ("王道のドロップ", 150, "F", "major", ["Bbmaj7", "C", "Am7", "Dm7", "Gm7", "F#m7", "Fm7", "Csus4|C"]),
        "2": ("カワイイ・ハウス", 128, "A", "major", ["Dmaj7", "E", "C#m7", "F#m7", "Dmaj7", "E", "Asus4|A", "A"]),
        "3": ("かわいくない音でかわいい曲", 170, "D", "minor", ["Bbmaj7", "C", "Dm7", "Dm7", "Gm7", "Asus4", "Dm7", "Dm7"]),
        "4": ("ドラムなしのポンプ", 140, "C", "major", ["Cmaj7", "D", "Em7", "Bm7", "Cmaj7", "D", "G", "G"])}
NAME, BPM, TONIC, MODE, CH = SPEC[KT]
S = Song(f"9{KT}", f"try{KT}", f"Kawaii future bass の試作{KT}「{NAME}」（仮）", f"KFB try {KT}", BPM, 4, TONIC, MODE, "Kawaii future bass（試作）")
S.kit = "naked-x"; S.flags = S.flags + " --piano salamander --space room --space-wet 0.1"
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}
K = Key(TONIC, MODE)
S.scene("歌", 8, "verse", CH); S.scene("ドロップ", 8, "chorus", CH); S.scene("おわり", 1, "outro", [CH[0]])

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.03, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.65 if KT != "4" else 0,
               fx=rack_supersaw() if KT != "4" else rack_supersaw()[:3] + [{"type": "transgate", "ms": round(60000 / BPM / 4), "pattern": "x.xxx.x.x.xx.x.x", "depth": 0.85}, {"type": "widen", "mix": 0.35}, {"type": "plate", "mix": 0.16}]) for i in range(5)]
FMB = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.09, pan=0, duck=0.25, fx=rack_bass())
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.04, pan=0, duck=0.4)
BELL = S.track("ベル", "lead", patch={"1": "kfbGlocken", "2": "kfbBrightBells", "3": "kfbMusicBox", "4": "kfbGlocken"}[KT], volume=0.085, pan=0.25, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
LEAD = S.track("リード", "lead", patch="kfbSquareLead" if KT in "13" else "kfbSineLead", volume=0.07, pan=-0.15, reverb=0.25, fx=rack_lead())
PLK = S.track("プラック", "lead", patch="kfbSquarePluck", volume=0.058, pan=0.3, reverb=0.2, fx=rack_pluck())
PAD = [S.track(f"きらめくパッド{i + 1}", "lead", patch="kfbSparklePad", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.4) for i in range(3)]
KFXT = S.track("クラップ・指パッチン", "guitar", patch="kawaiiFx", volume=0.07, pan=0.05, reverb=0.15, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
FXT = S.track("効果音", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.2, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ---- 歌（8小節。方向ごとにリズムの形を変える）----
if KT == "1":
    P1 = "x---x---x-x-x---"; P2 = "x-----x-------.."
    VC = [M(P1, "3 3 5 3 1"), M(P2, "2 3"), M(P1, "5 5 6 5 3"), M(P2, "5 6"), M(P1, "4 4 5 6 5"), M(P2, "4 3"), M(P1, "5 5 b3 1 b3"), M(P2, "5 5")]
elif KT == "2":
    PA = "x-x-x-.xx-x-x-.."
    VC = [M(PA, "3 3 4 3 1 1 3"), "R:4", M(PA, "5 5 6 5 3 2 3"), "R:4", M(PA, "6 6 5 6 4 3 4"), "R:4", M(PA, "5 5 4 3 2 2 1"), "R:4"]
elif KT == "3":
    Q1 = "x---x---x-------"; Q2 = "x-x-x---x-----.."
    VC = [M(Q1, "3 5 6"), M(Q2, "5 7 1' 2'"), M(Q1, "3' 2' 1'"), M(Q2, "7 1' 7 5"), M(Q1, "4 6 1'"), M(Q2, "2' 1' 7 1'"), M(Q1, "5 4 3"), M(Q2, "2 3 2 1")]
else:
    R1 = "..x-x-x-x---x---"; R2 = "x---x---------.."
    VC = [M(R1, "3 5 #4 3 2"), M(R2, "3 #4"), M(R1, "5 7 5 3 2"), M(R2, "3 2"), M(R1, "5 1' 7 5 #4"), M(R2, "5 6"), M(R1, "5 5 3 2 3"), M(R2, "2 2")]
bars = S.sc("歌"); mel = [K.mel(x, oct=4) if x != "R:4" else x for x in VC]
for b, m in zip(bars, mel): V.bar(b, m)
LY.flow(bars, mel, TXT, "歌")


def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def saw(b, pat, short=None):
    v = wide9(halves(b)[0])
    for j in range(5): SAW[j].bar(b, steps(pat, [N(v[j])], short=short))


def pad(b):
    v = sorted(voice(halves(b)[0], 67, 3))
    for j in range(3): PAD[j].bar(b, steps("x-------------..", [N(v[j])]))


def bs(b, pat, kinds, short=None, sub=None):
    c1, c2 = halves(b); r = low(c1, "F1"); nx = S.chords[b + 1].split("|")[0] if b + 1 < S.nb else c2; rn = low(nx, "F1")
    mp = {"r": r, "o": r + 12, "5": r + 7, "a": rn - 1 if rn > r else rn + 1}
    FMB.bar(b, steps(pat, [N(mp[c]) for c in kinds], short=short))
    if sub: SUB.bar(b, steps(sub, [N(r)]))


def top(b, k=0):
    """和音のいちばん上あたりの音（ベルやリードの旋律の材料）"""
    t = tones(halves(b)[0], "C5", "C6"); return [N(t[(q + k) % len(t)]) for q in range(len(t))]


GATES = ["x-x-x-..x-x-.x-.", "x-----x-x-..x-x-", "x-.x-.x-x-.x-.x-", "x-x-..x-..x-x-x-", "x-x-x-..x-x-.x-.", "x-.x-.x-....x-x-", "x-----x-----x-x-", "x-x-x-x-........"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; t = top(b)
    if n == "おわり":
        BELL.bar(b, steps("x-x-x-----------", [t[0], t[1], t[-1]])); pad(b); continue
    if KT == "1":
        if n == "歌":      # ベル・パッド・サブと、指パッチン。ドラムは半分の速さで軽く
            pad(b); bs(b, "x-------..x-x---", "r5o", sub="x-----------....")
            if odd: BELL.bar(b, steps("........x.x.x-x-", [t[0], t[1], t[2 % len(t)], t[-1]]))            # 歌が伸ばす後ろで、ベルが答える
            feel(D, b, "half", s="........X.......", h="X...x...X...x..."); KFXT.bar(b, "R:2 B4:1 R:1")
            if i == 7: FXT.bar(b, fx_bar((0, "up", 3))); D.set(b, "X...............", "........X.x.XX..", "X...x..........."); hat_roll(HATR, b, 1)       # 最後の1拍は、ロールだけ
        else:              # ドロップ: 和音が小節ごとにちがう型でポンプ。ベースも同じ型。リードと声がかけ合う
            saw(b, GATES[i]); bs(b, GATES[i], "rrrrrorr5a"[:onsets(GATES[i])], sub="x-------x-------" if i < 7 else "x-------........")
            if not odd: LEAD.bar(b, steps("x-x-x---........", [t[-1], t[1], t[0]]))
            feel(D, b, "half" if i % 4 != 3 else "halfopen"); KFXT.bar(b, "R:2 B4:1 R:1")
            if i == 0: FXT.bar(b, fx_bar((0, "impact", 2))); crash(D, b, "C2", 4)
            if i in (3, 7): hat_roll(HATR, b, 0.5)
            if i == 7: fill_cresc(D, b, 2)
    elif KT == "2":
        house = "..x-..x-..x-..x-"
        if n == "歌":
            saw(b, "x-.x-.x-........" if not odd else "..x-..x-..x-....", short=0.5) if i >= 2 else None
            bs(b, house, "rrrr" if not odd else "rr5o", short=0.5, sub="x---............")
            if odd: PLK.bar(b, arp16(halves(b)[1], "x.xxx.xxxxxxx-..", (0, 2, 1, 3, 2, 4, 3, 4, 5, 6, 7), lo="A4", hi="A6", short=0.25))      # 歌の休みにアルペジオ
            feel(D, b, "four", s="................", h="x.X.x.X.x.X.x.X." if i >= 4 else "................"); KFXT.bar(b, "R:1 C5:1 R:1 C5:1")
            if i == 7: fill_cresc(D, b, 1, toms=False); FXT.bar(b, fx_bar((0, "rev", 3)))
        else:
            saw(b, ["x-.x-.x-x-.x-.x-", "x-.x-.x-....x-x-"][i % 2], short=0.5); bs(b, house, "rorR"[:3] + "o" if not odd else "ro5a", short=0.5, sub="x---....x---....")
            BELL.bar(b, steps(["x-x-x-.xx---....", "..x-x-x---......", "x-x-x-.xx-x-x---", "x-----x---......"][i % 4], [t[0], t[1], t[-1], t[1], t[0], t[-1], t[1]]))      # ベルが主役
            feel(D, b, "four"); KFXT.bar(b, "R:1 B4:1 R:1 B4:1")
            if i == 0: FXT.bar(b, fx_bar((0, "impact", 2))); crash(D, b, "C2", 4)
            if i == 7: fill_cresc(D, b, 1, toms=False)
    elif KT == "3":
        if n == "歌":
            BELL.bar(b, steps("x-..x-..x-x-....", [t[0], t[-1], t[1], t[0]]) if not odd else steps("....x-x-x-------", [t[1], t[0], t[-1]]))
            bs(b, "x-------------..", "r", sub="x-------------..")
            if i >= 4: feel(D, b, "break" if not odd else "break2")
            else: feel(D, b, "space")
            if i == 7: FXT.bar(b, fx_bar((2, "down", 2))); FMB.bar(b, steps("x-------", [N(low(halves(b)[0], "F1"))]) + " " + tape_stop(N(low(halves(b)[0], "F1") + 12), 2)); D.set(b, "X...............", "....X...........", "X.x.X.x.........")
        else:
            if i % 4 in (0, 3): saw(b, "x---........x---" if i % 4 == 0 else "x-x-x-x-........", short=1.0)       # 和音は、すき間を大きく空けて打つ
            bs(b, "x-..x-....x-x-..", "rr5o", short=0.5, sub="x-------x-------")
            LEAD.bar(b, steps(["x-x-x---x-x-x---", "x-----..x-x-x-x-", "x-x-x---x-----..", "xxxxx-x-x-------"][i % 4], [t[-1], t[1], t[0], t[1], t[-1], t[0], t[1], t[-1]]))
            feel(D, b, "break" if not odd else "break2")
            if i == 0: FXT.bar(b, fx_bar((0, "impact", 2), (0, "sub", 2))); crash(D, b, "C2", 4)
            if i == 7: fill_cresc(D, b, 2)
    else:
        saw(b, "x-------------.." if not (n == "ドロップ" and i == 7) else "x---............")      # のばした和音を、エフェクター（transgate）が拍で刻む
        r0 = low(halves(b)[0], "F1"); r1 = low(S.chords[b + 1].split("|")[0], "F1") if b + 1 < S.nb else r0
        SUB.bar(b, steps("x---............", [N(r0)]) if (n == "ドロップ" and i == 7) else (f"{N(r0)}:3>{N(r1)} R:1" if r1 != r0 else f"{N(r0)}:3 R:1"))
        if n == "歌":
            if odd: BELL.bar(b, steps("........x.x.x-x-", [t[0], t[1], t[2 % len(t)], t[-1]])); FXT.bar(b, fx_bar((3, "kira", 1)))
            KFXT.bar(b, "R:2 C5:1 R:1" if i < 4 else "R:2 B4:1 C5:0.5 R:0.5")
        else:
            if i == 7: FXT.bar(b, fx_bar((1, "down", 3)))       # 最後の小節: 頭の1拍だけ鳴らして、あとは全員休み
            else:
                BELL.bar(b, steps(["x-..x-x-..x-x---", "..x-x-..x-------"][i % 2], [t[-1], t[0], t[1], t[-1], t[0]])); KFXT.bar(b, "R:2 B4:1 C5:0.5 C5:0.5")
                if i == 0: FXT.bar(b, fx_bar((0, "impact", 2)))

S.fade_out = 0
S.desc = f"仮: Kawaii future bass の試作{KT}「{NAME}」。{BPM}・{TONIC}{'長調' if MODE == 'major' else '短調'}。自作"
finish(S, LY, V, 0)

from vt3x_lib import *
path = sys.argv[1]
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("verse",)))
    vocal_polish(path, S, {"verse": 12}, scoop=0.25, slash=0.6, vib_min_beats=2.0, vib_start=0.5, auto=0.6, breaths=0.0)
    # ドロップ: 声のチョップ（歌詞の「ほ」「し」を切って、和音の音で）。リードやベルが休む所で答える
    cb = {}; db = S.sc("ドロップ")
    for i, b in enumerate(db):
        t = tones(S.chords[b].split("|")[0], "A4", "E5"); a, c = nm(t[0]), nm(t[-1])
        if KT == "1" and i % 2 == 1: cb[b] = f"{a}:0.5:ほ {a}:0.25:し {c}:0.25:ほ R:0.5 {c}:0.5:し {a}:0.5:ほ"
        if KT == "2" and i % 4 == 3: cb[b] = "R:2 " + stutter_chop(c, "ほ", 4, 0.25) + f" {a}:0.5:し"
        if KT == "3" and i % 4 == 1: cb[b] = f"R:3 {c}:0.25:ほ {c}:0.25:し {a}:0.5:ほ"[:0] + f"R:2.5 {c}:0.25:ほ {c}:0.25:し {a}:0.5:ほ"
        if KT == "4" and i < 7: cb[b] = (f"{c}:1:ほ R:1 {a}:0.5:し {c}:0.5:ほ" if i % 2 == 0 else f"R:1 {a}:0.5:ほ {a}:0.5:し {c}:1:ほ")
    chops(path, S, cb, vol=0.36, pan=-0.15)
    voice_by_scene(path, S, {}, default="cute" if KT in "24" else "clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path)
if KT == "3":      # ドラムをひずませる（かわいくない音）: ビットを落として、軽く歪ませる
    for p in js["parts"]:
        if p.get("instrument") in ("kick", "snare", "hihat"): p["fx"] = [{"type": "bitcrusher", "bits": 9, "mix": 0.4}, {"type": "tubescreamer", "gain": 0.35, "level": 0.8, "mix": 0.5}]
else: drum_punch(js)
save(path, js)
