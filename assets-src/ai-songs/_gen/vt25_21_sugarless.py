# vt25 21「シュガーレス・ラブコール」Sugarless Love Call（仮）— K-POP（R&B）。94・4/4。E♭長調 → 最後のサビは +1（E）。
# 物語: 甘いセリフは言えない。ハートのスタンプもうまく送れない。でも、電話をかける指は少しふるえながら、まっすぐに言う。
#   砂糖は入れないで。飾りもリボンもない、シュガーレスな声で「すき」。最後は、耳もとでささやく「すき」で終わる。
# 場面と強さ: イントロ（指パッチンとエレピ）→ Aメロ1（ささやくように）→ Bメロ1 → サビ1 → ポストサビ（「シュガーレス」の合いことば）
#   → Aメロ2 → Bメロ2 → サビ2 → ポストサビ2 → ダンスブレイク（歌なし・808 とプラック）→ Cメロ（静か・指パッチンだけ）
#   → 最後のサビ（+1・いちばん強い）→ ポストサビ3 → 終わり（耳もとの「すき」）
# 旋律の性格: Aメロは 16分で語る R&B。サビは「5, → 3 の連打」で跳ねて、2'（F5）まで。ポストサビは短い合いことば。
# ほかの曲とちがう所: 指パッチン（2・4拍）。最後に、マイクに近い、やわらかい声（teto-soft・響きなし・まん中）で「すき」とささやく。
from vt25_lib import *

S = Song("21", "sugarless", "シュガーレス・ラブコール（仮）", "Sugarless Love Call", 94, 4, "Eb", "major", "K-POP（R&B・ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.16"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.drum_scale = 0.85
K = Key("Eb", "major")          # oct 4 で 1 = E♭4（歌うのは B♭3〜F5）
KL = Key("E", "major")          # 最後のサビ（oct 4 で 1 = E4）

A_CH = ["Abmaj9", "Gm7", "Fm9", "Bb13"]
B_CH = ["Cm9", "Gm7", "Abmaj7", "Bb7"]
C_CH = ["Abmaj7", "Bb6", "Gm7", "Cm9", "Fm9", "Bb13", "Ebmaj9", "Ebmaj9"]
P_CH = ["Abmaj7", "Bb", "Ebmaj9", "Cm9"]
DB_CH = ["Cm9", "Abmaj7", "Fm9", "G7"]
X_CH = ["Fm9", "Gm7", "Abmaj7", "Bbsus4", "Fm9", "Gm7", "Abmaj7", "B7"]     # 最後の小節は E への入り口（B7）
up = lambda cs: [tr_chord(c, 1) for c in cs]

S.scene("イントロ", 4, "intro", A_CH)
S.scene("Aメロ1", 8, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("ポストサビ1", 4, "chorus", P_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("ポストサビ2", 4, "chorus", P_CH)
S.scene("ダンスブレイク", 8, "break", DB_CH)
S.scene("Cメロ", 8, "bridge", X_CH)
S.scene("最後のサビ", 16, "chorus", up(C_CH) * 2)
S.scene("ポストサビ3", 4, "chorus", up(P_CH))
S.scene("終わり", 6, "outro", ["Amaj9", "G#m7", "C#m9", "Emaj9", "Emaj9", "Emaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.6, patch="popLeadClear", low=True)
EP = [S.track(f"エレピ{i + 1}", "keys", patch="surgeKeysDxEp", volume=0.08, pan=-0.25 + 0.25 * i, reverb=0.3, sustain=0.9,
              fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": 1}]) for i in range(4)]
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("surgePadVerbPad", vol=0.04, pan=-0.35 + 0.35 * i, duck=0.35, sustain=1.6)) for i in range(3)]
B808 = S.track("808", "sub808", volume=0.17, pan=0, sustain=1.0, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7},
                                                                     {"type": "eq", "low": -1, "mid": 2.5, "midHz": 900, "high": 0}])
GT = S.track("ギター（R&B の合いの手）", "guitar", **clean_gtr_spec(0.075, 0.45))
PL = S.track("プラック（合いことば）", "pad", **pluck_spec("surgeNicePluck", vol=0.08, pan=-0.3))
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.35 + 0.35 * i, reverb=0.45, sustain=1.5) for i in range(3)]
BELL = S.track("ベル", "pad", patch="surgeFantasyBell", volume=0.045, pan=0.35, reverb=0.45, sustain=1.0)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)
SNAP = season(S, 0, "指パッチン", beats=0.5, vol=0.08, pan=0.15)
SNAP.ev = []

# ================= 歌 =================
VA = ["R:0.5 3:0.25 3:0.25 3:0.5 2:0.5 1:0.5 2:0.5 3:1", "2:0.5 3:1.5 R:2", "R:0.5 3:0.25 3:0.25 3:0.5 5:0.5 6:0.5 5:0.5 3:1", "2:1.5 R:2.5",
      "R:0.5 3:0.25 3:0.25 3:0.5 2:0.5 1:0.5 2:0.5 3:1", "2:0.5 3:1.5 R:2", "R:0.5 6:0.25 6:0.25 6:0.5 5:0.5 3:0.5 2:0.5 1:1", "2:2 R:2"]
A1 = "あまいせりふはむり/にがてなんだよね/はーとのすたんぷも/うまくおくれない"
A2 = "でんわをかけるゆび/すこしふるえてる/さとうはいれないで/まっすぐにいうから"
VB = ["R:1 5:0.5 5:0.5 6:0.5 5:0.5 3:1", "3:1 2:1 R:2", "R:1 1':0.5 1':0.5 7:0.5 6:0.5 5:1", "5:2 R:2",
      "R:1 5:0.5 5:0.5 6:0.5 5:0.5 3:1", "3:1 2:1 R:2", "R:1 1':0.5 1':0.5 2':0.5 1':0.5 7:1", "5:1 6:1 7:1 R:1"]
B1 = "きみのこえがね/あたたかいの/ふしぎなくらい/どきどきしてるの"
B2 = "ことばよりもね/このきもちを/きいてほしいの/いまからかけるよ"
VC = ["R:0.5 5,:0.5 3:0.5 3:0.5 3:0.5 2:0.5 3:1", "5:1.5 3:0.5 2:1 R:1", "R:0.5 5,:0.5 3:0.5 3:0.5 3:0.5 2:0.5 3:1", "6:1.5 5:0.5 3:1 R:1",
      "R:0.5 6:0.5 1':0.5 1':0.5 1':0.5 7:0.5 1':1", "2':1.5 1':0.5 5:1 R:1", "R:0.5 3:0.5 5:0.5 3:0.5 2:0.5 1:0.5 2:1", "1:2 R:2"]
C1 = "しゅがーれすなこえで/すきってそのままいう/かざりはなにもない/らぶこーるだよ"
C2 = "しゅがーれすなこえで/ほんとうのことだけ/あまくないけれどね/とどけにいくよ"
CL = C1 + "/しゅがーれすなこえで/ことばがへたでもね/このまっすぐなきもち/らぶこーるだよ"
VP = ["R:0.5 5:0.5 5:0.5 3:0.5 5:1 6:1", "5:1 3:1 R:2", "R:0.5 5:0.5 5:0.5 3:0.5 5:1 6:1", "5:1 3:1 1:1 R:1"]
P1 = "しゅがーれすらぶ/しゅがーれすこーる"
VX = ["R:1 3:1 2:1 1:1", "2:3 R:1", "R:1 3:1 5:1 6:1", "5:3 R:1", "R:1 6:1 5:1 3:1", "2:3 R:1", "R:1 3:1 5:1 7:1", "1':3 R:1"]
X1 = "きこえる/むねのね/さとうは/いらない"
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC, C1); put("サビ2", K, VC, C2)
put("ポストサビ1", K, VP, P1); put("ポストサビ2", K, VP, P1)
put("Cメロ", K, VX, X1)
put("最後のサビ", KL, VC + VC, CL)
put("ポストサビ3", KL, VP, P1)
if VOCAL: put("Aメロ2", K, VA, A2)
else:                                          # 歌なしの版: 2番の Aメロはギターが歌う
    for b, l in zip(S.sc("Aメロ2"), VA): GT.bar(b, K.mel(l, oct=4))
# ポストサビの合いことばを、プラックが1オクターブ上でなぞる
for name, key in (("ポストサビ1", K), ("ポストサビ2", K), ("ポストサビ3", KL)):
    for b, l in zip(S.sc(name), VP): PL.bar(b, key.mel(l, oct=5))

# ================= 伴奏 =================
EPR = ["{a}:0.75 {a}:0.75 R:0.5 {a}:1.5 R:0.5", "R:0.5 {a}:1 {a}:0.75 {a}:0.75 R:1", "{a}:1.5 R:0.5 {a}:0.75 {a}:1.25", "R:0.25 {a}:0.75 R:0.5 {a}:1.5 R:1"]
GTL = ["R:1.5 {r}:0.25 {f}:0.25 {o}:0.5 R:1.5", "R:2.5 {o}:0.25 {f}:0.25 {r}:1", "R:1 {o}:0.5 R:2.5", "R:3 {f}:0.25 {o}:0.25 {f}:0.5"]
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 64, 4, prev=prev); prev = v; pv = voice(ch, 60, 3)
    if n == "終わり":
        if i < 5:
            for j in range(4): EP[j].bar(b, f"{nm(v[j])}:4" if i < 4 else f"{nm(v[j])}:8")
            for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4" if i < 4 else f"{nm(pv[j])}:8")
        if i == 4: BELL.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C6", "C7")[:4]))
        continue
    for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4")
    if n == "Cメロ":
        for j in range(4): EP[j].bar(b, f"{nm(v[j])}:4")
        continue
    pat = EPR[(i + (1 if n.startswith(("サビ", "最後", "ポスト")) else 0)) % 4]
    for j in range(4): EP[j].bar(b, pat.format(a=nm(v[j])))
    if n.startswith(("Aメロ", "イントロ", "Bメロ")) and not (n == "Aメロ2" and not VOCAL):
        r = low(ch, "C3"); GT.bar(b, GTL[i % 4].format(r=nm(r + 12), f=nm(r + 15), o=nm(r + 19)))
    if n in ("サビ2", "最後のサビ", "ポストサビ3"):
        sv = voice(ch, 67, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
    if n.startswith(("サビ", "最後")) and i % 4 == 3:
        BELL.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C6", "C7")[:4]))
    if n == "ダンスブレイク":                        # プラックの 16分の短い型（歌のかわり）
        t = tones(ch, "C5", "C6")
        PL.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" if c == "x" else "R:0.25" for q, c in enumerate("x.x.xx.x..x.x.x." if i % 2 == 0 else "x..x.x..x.xx..x.")))

# ================= 808 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C1")
    if r < midi("D1"): r += 12
    if n == "イントロ" and i < 2: continue
    if n == "終わり":
        if i < 5: B808.bar(b, f"{nm(r)}:4" if i < 4 else f"{nm(r)}:8")
        continue
    if n == "Cメロ":
        if i % 2 == 0: B808.bar(b, f"{nm(r)}:4")
        continue
    if n == "ダンスブレイク":
        B808.bar(b, f"{nm(r)}:0.75! {nm(r)}:0.75 {nm(r + 12)}:0.5 {nm(r)}:1 {nm(r + 10)}:0.5 {nm(r + 12)}:0.5")
        continue
    B808.bar(b, f"{nm(r)}:1.5! {nm(r)}:1 R:0.5 {nm(r + 7)}:1" if i % 2 == 0 else f"{nm(r)}:2.5! {nm(r + 12)}:0.5 {nm(r + 10)}:1")

# ================= 指パッチン（2・4拍） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("イントロ", "Aメロ1", "Aメロ2", "Cメロ") or (n == "終わり" and i < 4) or n.startswith("Bメロ"):
        for st in (1, 3): SNAP.at(S.bar_beat(b) + st, "C#5:0.5")
cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

# ================= ドラム（R&B: 遅れて来るキック、2・4拍のスネア、16分の軽いハット） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "イントロ":
        if i >= 2: vgroove(D, b, "half", ghosts=0, seed=b, s="................", h="x.x.x.x.x.x.x.x.")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "half", ghosts=0.15, seed=b, k="X......X..X....." if i % 2 == 0 else "X.....X...X..X..", s="....X.......X...", h="x.x.x.xxx.x.x.x.")
        if i == 0: crash(D, b, "C2", 3)
    elif n.startswith("Bメロ"):
        vgroove(D, b, "half", ghosts=0.2, seed=b, k="X.......X.....X.", s="....X.......X...", h="x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "snare16")
    elif n.startswith(("サビ", "最後", "ポスト")):
        vgroove(D, b, "trap", ghosts=0.2, seed=b, k="X......X..X...X." if i % 2 == 0 else "X.....X...X.....", s="....X.......X...",
                h="x.x.xxx.x.x.x.xx" if i % 2 == 0 else "x.x.x.x.x.xxx.x.", vary=False)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 4 == 3 and not last: put_fill(D, b, "small")
        if last and not n.startswith("ポストサビ3"): put_fill(D, b, "snare16")
    elif n == "ダンスブレイク":
        vgroove(D, b, "trap", ghosts=0.25, seed=b, k="X..X..X...X..X..", s="....X.......X...", h="xxx.x.xxx.x.xXxX", vary=False)
        if i == 0: crash(D, b, "C2", 4)
        if last: put_fill(D, b, "build")
    elif n == "Cメロ":
        if i >= 4: vgroove(D, b, "half", ghosts=0, seed=b, k="X.......X.......", s="................", h="x...x...x...x...")
        if last: put_fill(D, b, "build")

SIL.add(S.sc("Cメロ")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の21。K-POP（R&B）。E♭長調・94、最後のサビは +1（E）。"
          "甘いセリフは言えない子が、飾りのない声でまっすぐ「すき」を伝える電話。指パッチンとエレピの R&B、16分で語る Aメロ、"
          "「シュガーレス」の合いことば（ポストサビ）、歌なしのダンスブレイク。最後は耳もとのやわらかい声で「すき」とささやいて終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.3}, special={"Cメロ": -0.45, "ダンスブレイク": -0.1, "最後のサビ": 0.5})
# 歌の版: 最後に、耳もとでささやく「すき」（やわらかい声・響きなし・まん中）
if VOCAL:
    import json as _j, sys as _s
    path = _s.argv[1]; js = _j.load(open(path))
    st = S.bar_beat(S.sc("終わり")[4]) + 1
    near = dict(js["vocals"][0]); near.update({"voice": "teto-soft", "notes": f"R:{st:g} B4:1:す G#4:2.5:き", "pan": 0.0, "volume": 0.9,
                                               "reverb": 0.04, "dynamics": [[0, -0.2]]})
    near.pop("blend", None)
    js["vocals"].append(near)
    _j.dump(js, open(path, "w"), ensure_ascii=False)
    print("  耳もとの「すき」を足した")
