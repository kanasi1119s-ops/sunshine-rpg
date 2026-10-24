# vp25 19「ぶらんこ」The Swing（仮）— J-POP（3拍子）。F長調（みんなで、で G長調）・168・3/4。主役の楽器: アコーディオン
# 物語: 夕方の公園。ぶらんこをこぎ始める。こぐたびに高くなって、いちばん高い所で手を離して跳ぶ。ふわっと浮いて、着地して、
#   みんなで笑う。夕焼けの中、ぶらんこはだんだんゆっくりになって、止まる。
# 形: 曲全体が振り子（1小節で1往復の半分）。こぐたびに振れ幅が大きくなり、いちばん高い所で手を離して跳ぶ
# 場面と強さ: 振れ幅＝強さ（だんだん大きく）／跳んでいる間＝無音の滞空（4小節）／着地＝最大／夕焼け＝ゆっくり止まる（テンポも落ちる）
# 旋律の性格: 行って戻る往復の音型。振れ幅（音の幅）が 3度→5度→オクターブ→10度と広がる
# 崩す所: J-POP を3拍子で通す
from vp25_lib import *

S = Song("19", "buranko", "ぶらんこ（仮）", "The Swing", 168, 3, "F", "major", "J-POP（3拍子）")
S.kit = "jpop"   # 2026-10-25: 切り抜きで naked 6.83 → jpop 7.07
K = S.key
P1 = ["F", "F", "Am7", "Am7", "Bbmaj7", "Bbmaj7", "C7sus4", "C7"]
P2 = ["Dm7", "Dm7", "Bbmaj7", "Bbmaj7", "Gm7", "Gm7", "C7sus4", "C7"]
P3 = ["Bbmaj7", "C/Bb", "Am7", "Dm7", "Gm7", "Gm7/F", "Ebmaj7", "C7"]
S.scene("こぎ始め", 16, "intro", P1)
S.scene("揺れる", 32, "verse", P1 + P2)
S.scene("高く", 32, "pre", P3)
S.scene("もっと高く", 32, "chorus", P1 + P3)
S.scene("手を離す", 4, "break", ["C7sus4"] * 4)
S.scene("着地", 16, "chorus", ["F", "F", "Dm7", "Dm7", "Bbmaj7", "C", "F", "D7"])
P1G = [tr_chord(c, 2) for c in P1]; P3G = [tr_chord(c, 2) for c in P3]
S.scene("みんなで", 48, "chorus", P1G + P3G + P1G[:8] + ["Cmaj7", "D/C", "Bm7", "Em7", "Am7", "Am7/G", "D7sus4", "D7"] + P1G + P3G[:8])
S.scene("夕焼け", 48, "outro", [tr_chord(c, 2) for c in P1 + P2 + P1 + P2 + P1 + P1])
S.scene("止まる", 16, "outro", ["G"] * 16)
b_slow = S.sc("夕焼け")[16]
S.tempo = [{"bar": b_slow + 1, "bpm": 168}, {"bar": b_slow + 2, "bpm": 120, "ramp": 40}]
S.extra.update({"tone": "rock", "diGuitar": "emily"})
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags   # 2026-10-25: 参考の音で 7.07 → 7.62（09 の切り抜き）
KG = K.up(2)

AC = S.track("主役: アコーディオン", "accordion", volume=0.25, pan=-0.1, reverb=0.28, gainDb=5, phrase=6, mono=True,
             fx=[{"type": "eq", "low": -4, "mid": 2, "midHz": 2000, "high": 0.5}])
AC2 = [S.track(f"アコーディオン（和音{i + 1}）", "accordion", volume=0.1, pan=[0.3, 0.4][i], reverb=0.3) for i in range(2)]
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("calliope", vol=0.18, pan=0.05, delay=1.0, extra_fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.7}]))
CL = S.track("アコースティックのギター", "guitar", **clean_gtr_spec(0.11, 0.5))
PI = [S.track(f"ピアノ{i + 1}", "piano", **piano_spec(0.11, [-0.3, -0.2, -0.4][i])) for i in range(3)]
BASS = S.track("ベース", "bass", **rock_bass_spec(0.19))
STR = [S.track(f"弦{i + 1}", "strings", patch="slowStrings", **strings_spec(0.07, [-0.55, 0.55][i])) for i in range(2)]
FX = S.track("効果音（風）", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.35)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- 振り子の旋律: 1小節で「行く」、次の小節で「戻る」。振れ幅（音の幅）が広がる ----------
SEMI = {2: 4, 4: 7, 7: 12, 9: 16}


def swing_pair(b, width, k, start_deg=None):
    """2小節ぶん（行く・戻る）。和音の音だけで、根音から width（3度・5度・オクターブ・10度）上まで行って戻る"""
    ch = S.chords[b]
    base = low(ch, "F4")
    ts = [m for m in tones(ch, "F4", "C7") if m >= base]
    top = min(ts, key=lambda m: abs(m - (base + SEMI[width])))
    mid = min([m for m in ts if base < m < top] or [top], key=lambda m: abs(m - (base + top) / 2))
    go = f"{nm(base, k.flat)}:1 {nm(mid, k.flat)}:1 {nm(top, k.flat)}:1"
    ch2 = S.chords[b + 1] if b + 1 < S.nb else ch
    ts2 = tones(ch2, "F4", "C7")
    near = lambda x: min(ts2, key=lambda m: abs(m - x))
    back = f"{nm(near(top - 1), k.flat)}:1 {nm(near(mid), k.flat)}:1 {nm(near(base), k.flat)}:1"
    return go, back


def deg_str(i):
    o, n = divmod(i, 7)
    return f"{n + 1}{chr(39) * o if o > 0 else ',' * (-o)}"


SCN = {"こぎ始め": 2, "揺れる": 4, "高く": 7, "もっと高く": 9}
for name, w in SCN.items():
    bars = S.sc(name)
    for i in range(0, len(bars), 2):
        b = bars[i]
        ch = S.chords[b]
        r = parse_chord(ch)[0]
        start = [x for x in range(7) if K.deg(deg_str(x)).rstrip("0123456789-")[:len(r)] == r] or [0]
        start = start[0] + (7 if w < 7 else 0)
        go, back = swing_pair(b, w, K, start)
        if name == "こぎ始め" and i < 4:
            AC.bar(b, go); AC.bar(b + 1, back)
        elif name in ("こぎ始め", "揺れる"):
            AC.bar(b, go); AC.bar(b + 1, back)
        else:
            LEAD.bar(b, go); LEAD.bar(b + 1, back)
# 歌の役（揺れる・高くの後半）: 振り子の上で、長い旋律
SONG = ["5:3", "6:2 5:1", "3:3", "2:2 1:1", "4:3", "5:2 6:1", "5:3", "R:3", "1':3", "7:2 6:1", "5:3", "6:2 4:1", "5:2 3:1", "2:3", "1:3", "R:3"]
for i, b in enumerate(S.sc("揺れる")):
    if i >= 16: LEAD.bar(b, K.mel(SONG[(i - 16) % 16], oct=4))
for i, b in enumerate(S.sc("高く")):
    AC.bar(b, K.mel(SONG[i % 16], oct=5) if i % 2 == 0 else "R:3")
# 手を離す: 無音の滞空（風だけ）
FX.bar(S.sc("手を離す")[0], "A4:6 R:6")
# 着地とみんなで: いちばん大きいサビ（アコーディオンとリード）
HOOK = ["1':1 3':1 5':1", "4':2 3':1", "2':1 4':1 6':1", "5':3", "4':1 6':1 1'':1", "7':2 5':1", "6':1 5':1 4':1", "3':3",
        "3':1 4':1 5':1", "6':2 5':1", "4':1 3':1 2':1", "3':3", "2':1 3':1 4':1", "5':2 7':1", "1'':3", "R:3"]
for i, b in enumerate(S.sc("着地")): AC.bar(b, K.mel(HOOK[i % 16], oct=4)); LEAD.bar(b, K.mel(HOOK[i % 16], oct=3) if i >= 8 else "R:3")
for i, b in enumerate(S.sc("みんなで")):
    LEAD.bar(b, KG.mel(HOOK[i % 16], oct=4))
    if i >= 16: AC.bar(b, KG.mel(HOOK[i % 16], oct=3 if i < 32 else 4))
# 夕焼け: 振れ幅がだんだん小さく（10度→オクターブ→5度→3度）
for i in range(0, 48, 2):
    b = S.sc("夕焼け")[i]
    w = [9, 7, 4, 2][min(3, i // 12)]
    go, back = swing_pair(b, w, KG, 7)
    AC.bar(b, go); AC.bar(b + 1, back)
for i, b in enumerate(S.sc("止まる")):
    if i in (0, 4): AC.bar(b, KG.mel("1':3", oct=4))
    if i == 8: AC.bar(b, KG.mel("5:3", oct=4))
    if i == 12: AC.bar(b, KG.mel("1':6", oct=4))

# ---------- 伴奏（ワルツ: 1拍目に低音、2・3拍目に和音） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1"); v = voice(ch, 64, 2); pv = voice(ch, 69, 3)
    if n == "手を離す": continue
    if n == "止まる" and i >= 12: continue
    if n != "こぎ始め" or i >= 8:
        BASS.bar(b, f"{nm(r)}:1! R:2" if n not in ("みんなで", "着地") else f"{nm(r)}:1! R:1 {nm(r + 7)}:1")
    if n in ("こぎ始め", "揺れる", "夕焼け", "止まる"):
        CL.bar(b, f"R:1 {nm(v[0])}:1 {nm(v[1])}:1")
    if n in ("高く", "もっと高く", "着地", "みんなで", "揺れる") and not (n == "揺れる" and i < 16):
        for j in range(2): AC2[j].bar(b, f"R:1 {nm(v[j])}:1 {nm(v[j])}:1")
    if n in ("もっと高く", "着地", "みんなで", "高く") and not (n == "高く" and i < 16):
        for j in range(3): PI[j].bar(b, f"R:1 {nm(pv[j])}:2" if n != "みんなで" else f"{nm(pv[j])}:1 {nm(pv[j])}:1 {nm(pv[j])}:1")
    if n in ("みんなで", "夕焼け") and not (n == "夕焼け" and i >= 32):
        sv = voice(ch, 72, 2)
        for j in range(2): STR[j].bar(b, f"{nm(sv[j])}:3")
cym_swell(CYM, S.sc("着地")[0], 3, "C4"); cym_swell(CYM, S.sc("みんなで")[0], 3, "C4")

# ---------- ドラム（ワルツ） ----------
W_K = "X..........."; W_S = "....x...x..."; W_H = "x...x...x..."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "こぎ始め" and i < 8: continue
    if n == "手を離す": continue
    if n == "止まる": continue
    if n in ("こぎ始め", "揺れる"):
        D.set(b, W_K, "." * 12 if n == "こぎ始め" else W_S, W_H)
    elif n in ("高く", "もっと高く"):
        D.set(b, "X.......x..." if i % 2 else W_K, "....X...x..." if n == "もっと高く" else W_S, "x.x.x.x.x.x.")
        if i % 16 == 0: D.cym(b, "C2:3")
        if i % 16 == 15: D.set(b, "X...X...X...", "....xxxxXXXX", "." * 12)
    elif n in ("着地", "みんなで"):
        D.set(b, "X.......x..." if i % 2 else "X...........", "....X...X...", "x.x.x.x.x.x.")
        if i % 8 == 0: D.cym(b, "C2:3" if i % 16 == 0 else "G2:3"); D.H[b] = "." + D.H[b][1:]
        if i % 16 == 15: D.set(b, "X...X...X...", "....xxxxXXXX", "." * 12)
    elif n == "夕焼け":
        D.set(b, W_K, W_S if i < 24 else "." * 12, W_H if i < 32 else "x...........")
D.set(S.sc("着地")[0], "X" + "." * 11, "X" + "." * 11, "." * 12)

S.desc = ("仮: ボカロ曲のインスト25曲の19。3拍子の J-POP。F長調（みんなで、で G長調）・168。主役の楽器はアコーディオン。夕方の公園のぶらんこ。"
          "1小節で行き、次の小節で戻る振り子の旋律。こぐたびに振れ幅（音の幅）が 3度→5度→オクターブ→10度と広がり、いちばん高い所で手を離して跳ぶ（4小節の無音の滞空）。"
          "着地して、みんなで笑うサビ。夕焼けの中、振れ幅もテンポもだんだん小さくなって、止まる。自作")
S.write()
