# vt3 17「放課後タッピング」After-School Tapping（仮）— マスロック。138・4/4（5つ割りのフレーズが小節をはみ出す）。A長調（転調なし）。
# 第3弾（0時〜24時の街）の 16時。表は docs/sound/vt3-plan.md。
# 物語: 放課後の空き教室。軽音部の4人が新しい曲をつくる。だれかが弦を指でたたいて（タッピング）、けさ聞いたあの節を試す。
#   ベースがのり、ドラムがくる。ずれたリズムに笑い合い、5回目でやっとかみ合う。窓の外では運動部の「ファイトー」の声。
#   その声ものせて、名前のない曲ができあがる。チャイムが鳴るまでもう一回。教室のかぎを閉めて帰る。
# 場面と強さ: タッピング（ギター1本・弱）→ イントロ（全員のユニゾン・強）→ Aメロ1（細かく動く・中）→ Bメロ1 → サビ1（強）
#   → 間奏（5つ割りのリフ・節）→ Aメロ2 → Bメロ2 → サビ2 → 間奏2（ドラムとベースの手数）→ 窓の外（ハーモニクスだけ・弱）
#   → 最後のサビ（いちばん強い）→ ユニゾン（全員で切る）
# 旋律の性格: Aメロは16分で細かく動く（C#4〜B4）、サビは5度上から入ってなめらかに伸ばす（A4〜F#5）。
# この曲だけの音: 5つ割り（16分5つ）でくり返すタッピングとキックが、4拍子の小節線をまたいでずれていく（マスロックの「拍子のはみだし」）。
#   合いことばの節（3・5・6・5・2＝C#・E・F#・E・B）は、最初のタッピングと間奏のタッピング。
from vt25_lib import *

S = Song("17", "tapping", "放課後タッピング（仮）", "After-School Tapping", 138, 4, "A", "major", "マスロック（ボカロ）")
S.kit = "naked-x"
S.flags = "--bass bnb-loud " + S.flags + " --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.5
S.keepers = {"Aメロ2": "ride", "サビ2": "open", "最後のサビ": "open"}
K = Key("A", "major")          # oct 3 で 1 = A3

A_CH = ["Aadd9", "C#m7", "Dmaj7#11", "Esus4"]
B_CH = ["Bm7", "C#m7", "Dmaj7", "E", "Bm7", "C#m7", "Dmaj7", "Esus4"]
C_CH = ["Dmaj7", "E", "C#m7", "F#m7", "Bm7", "E", "Aadd9", "Aadd9", "Dmaj7", "E", "C#m7", "F#m7", "Bm7", "E", "Dmaj7", "Aadd9"]

S.scene("タッピング", 4, "intro", A_CH)
S.scene("イントロ", 8, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("間奏2", 8, "solo", A_CH)
S.scene("窓の外", 8, "bridge", ["Dmaj7", "C#m7", "Bm7", "Aadd9", "Dmaj7", "C#m7", "Bm7", "Esus4"])
S.scene("最後のサビ", 24, "chorus", C_CH + C_CH[:8])
S.scene("ユニゾン", 6, "outro", ["Dmaj7", "E", "C#m7", "F#m7", "Aadd9", "Aadd9"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
TAP = S.track("タッピングのギター", "guitar", amp="crystal", volume=0.075, pan=-0.35, reverb=0.25, chorus=0, sustain=0.5)
GC = [S.track(f"ギター（和音{i + 1}）", "guitar", amp="jpopClean", volume=0.05, pan=0.45, reverb=0.2, chorus=0, sustain=0.6) for i in range(3)]
GD = [S.track(f"歪みのギター{i + 1}", "distGuitar", **rock_gtr_spec(0.04, 0.6 if i % 2 else -0.6, drive=0.45)) for i in range(3)]
HARM = S.track("ハーモニクス", "guitar", patch="guitarFx", amp="crystal", volume=0.07, pan=0.2, reverb=0.45, chorus=0, sustain=1.5)
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.24))
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 3:0.25 5:0.25 6:0.5 5:0.5 3:0.25 2:0.25 1:0.5 R:1", "R:0.5 2:0.25 3:0.25 5:0.5 3:0.5 2:1 R:1",
      "R:0.5 3:0.25 5:0.25 6:0.5 1':0.5 7:0.25 6:0.25 5:0.5 R:1", "R:0.5 6:0.25 5:0.25 3:0.5 2:0.5 3:1 R:1",
      "R:0.5 3:0.25 5:0.25 6:0.5 5:0.5 3:0.25 2:0.25 1:0.5 R:1", "R:0.5 2:0.25 3:0.25 5:0.5 3:0.5 2:1 R:1",
      "R:0.5 4:0.5 5:0.5 6:0.5 1':0.5 2':0.5 1':0.5 7:0.5", "6:2 R:2"]
A1 = ("あきのきょうしつ/よじちょうど/あんぷのすいっち/ぱちっといれ/げんをたたいて/きらきらだ/あのふしためそう/"
      "べーすがのったら/どらむきた/ずれたりずむも/わらいごえ/ごかいめでやっと/かみあったよ/これだってゆびさす")
A2 = "まどのそとでは/うんどうぶ/かけごえひびく/ふぁいとーと/そのこえものせ/かきたして/あたらしいきょくが"
VB = ["R:1 6:0.5 1':0.5 2':1 1':1", "6:1 5:1 R:2", "R:1 5:0.5 6:0.5 1':1 6:1", "5:1 3:1 R:2",
      "R:1 6:0.5 1':0.5 3':1 2':1", "1':1 6:1 R:2", "R:0.5 2':0.5 3':0.5 2':0.5 1':0.5 6:0.5 5:1", "R:4"]
B1 = "なまえはまだ/ないままでも/よにんのおと/それでいいね"
B2 = "なんかいめか/まちがえても/やりなおせば/ちかづいてく"
VC = ["R:0.5 5:0.5 1':1 2':1 3':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 6:0.5 1':1 2':1 1':1", "6:2 5:1 R:1",
      "R:0.5 5:0.5 1':1 2':1 3':1", "5':1.5 4':0.5 3':1 R:1", "R:0.5 3':0.5 2':0.5 1':0.5 2':1 1':1", "1':3 R:1",
      "R:0.5 3':0.5 5':1 4':1 3':1", "2':1.5 1':0.5 6:1 R:1", "R:0.5 6:0.5 1':1 3':1 2':1", "1':2 R:2",
      "R:0.5 3':0.5 5':1 6':1 5':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 2':0.5 3':0.5 2':0.5 1':0.5 7:0.5 6:0.5 7:0.5", "1':3 R:1"]
HOOK = "ほうかごのたっぷ"
C1 = f"{HOOK}/ゆびがおどる/はみだすりずむ/それもいいね/{HOOK}/ゆうやけに/ひびくこのおと/わすれないでいて"
C2 = f"{HOOK}/まちがいさえ/かざりになるの/おもしろいね/{HOOK}/じかんまで/もういっかいひく/ちゃいむがなるまで"
C3 = (f"{HOOK}/できたよほら/よにんのきょくだ/なまえはねえ/{HOOK}/それでいい/そのままがいい/あしたもここでね/"
      f"{HOOK}/またあしたね/きょうしつのかぎ/しめてかえる")
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("最後のサビ", VC + VC[:8], C3)

# ================= 5つ割りのタッピング（小節線をまたいで続く）=================
def tap_section(name, lo="A4", hi="A6", motif_bars=()):
    bars = S.sc(name); q = 0
    for i, b in enumerate(bars):
        if i in motif_bars: continue
        t = tones(S.chords[b], lo, hi)
        cyc = [t[0], t[2 % len(t)], t[1], t[3 % len(t)], t[2 % len(t)]]       # 5つで1回り
        TAP.bar(b, " ".join(f"{nm(cyc[(q + s) % 5])}:0.25{'!' if (q + s) % 5 == 0 else ''}" for s in range(16)))
        q = (q + 16) % 5


def chords(b, ch, pat):
    v = voice(ch, 64, 3)
    for j in range(3): GC[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def dist8(b, ch):
    pw = power(ch, "E2")
    for j in range(3): GD[j].bar(b, " ".join(f"{nm(pw[j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))


MOTIF = ["R:1 C#5:0.5 E5:0.5 F#5:1 E5:0.5 B4:0.5", "A4:3 R:1"]      # 合いことばの節（3・5・6・5・2）
for i, b in enumerate(S.sc("タッピング")):
    TAP.bar(b, MOTIF[i] if i < 2 else "R:4")
tap_section("タッピング", motif_bars=(0, 1)) if False else None
for i, b in enumerate(S.sc("タッピング")[2:]):
    t = tones(S.chords[b], "A4", "A6"); cyc = [t[0], t[2 % len(t)], t[1], t[3 % len(t)], t[2 % len(t)]]
    TAP.bar(b, " ".join(f"{nm(cyc[(i * 16 + s) % 5])}:0.25" for s in range(16)))
for name in ("イントロ", "Aメロ2", "サビ1", "サビ2", "最後のサビ"): tap_section(name)
tap_section("Aメロ1", "E4", "E6"); tap_section("間奏", motif_bars=(4, 5)); tap_section("間奏2", "E4", "E6")
for k, b in enumerate(S.sc("間奏")[4:6]): TAP.bar(b, MOTIF[k])

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "イントロ":
        dist8(b, ch); chords(b, ch, "x:0.75! x:0.75 x:0.5 R:0.5 x:0.75 x:0.75")
    elif n in ("Aメロ1", "Aメロ2"):
        if n == "Aメロ2" or i >= 8: chords(b, ch, "x:0.75 R:0.75 x:0.5 R:0.5 x:0.75 R:0.75")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 7: chords(b, ch, "x:1 x:1 x:1 x:1"); dist8(b, ch) if i >= 4 else None
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏2"):
        dist8(b, ch); chords(b, ch, "x:0.75! x:0.75 x:0.5 R:0.5 x:0.75 x:0.75")
    elif n == "間奏":
        dist8(b, ch)
    elif n == "窓の外":
        HARM.bar(b, f"{nm(tones(ch, 'E5', 'E6')[0])}:2 {nm(tones(ch, 'E5', 'E6')[-1])}:2")
        if i >= 4: chords(b, ch, "x:4")
    elif n == "ユニゾン":
        if i < 4: dist8(b, ch); chords(b, ch, "x:0.75! x:0.75 x:0.5 R:0.5 x:0.75 x:0.75")
        elif i == 4: dist8(b, ch); chords(b, ch, "x:0.5! R:0.25 x:0.25! R:0.5 x:0.5! R:0.25 x:0.25! R:0.5 x:1!")
        else:
            for j in range(3): GD[j].bar(b, f"{nm(power(ch, 'E2')[j])}:0.5! R:3.5")

# ================= ベース（指弾き・手数）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "タッピング": continue
    if n == "窓の外": BASS.bar(b, f"{nm(r)}:4" if i >= 4 else "R:4"); continue
    if n == "Aメロ1" and i < 4: continue
    if n == "ユニゾン":
        if i < 5: BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
        else: BASS.bar(b, f"{nm(r)}:0.5 R:3.5")
        continue
    if n == "間奏2":
        BASS.bar(b, f"{nm(r)}:0.25 {nm(r + 12)}:0.25 {nm(r + 7)}:0.25 {nm(r)}:0.25 {nm(r + 10)}:0.25 {nm(r)}:0.25 {nm(r + 12)}:0.25 {nm(r + 7)}:0.25 "
                    f"{nm(r)}:0.5 {nm(r + 7)}:0.25 {nm(r + 12)}:0.25 {nm(r + 10)}:0.5 {nm(r + 7)}:0.5"); continue
    BASS.bar(b, bass_line(S, b, "root8" if n in ("サビ1", "サビ2", "最後のサビ", "イントロ") else "push", lo="E1"))

# ================= ドラム（キックも5つ割り）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("タッピング",) or (n == "Aメロ1" and i < 4): continue
    if n == "窓の外":
        if i == 7: put_fill(D, b, "build")
        continue
    if n == "ユニゾン":
        if i < 4: vgroove(D, b, "vrock", ghosts=0.2, seed=b)
        elif i == 4: D.set(b, "X..X..X.X..X..X.", "X..X..X.X..X..XX", "................"); crash(D, b)
        else: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 8)
        continue
    # 5つ割りのキック（小節ごとに位置がずれていく）
    off = (b * 16) % 5
    kick = "".join("X" if (s + off) % 5 == 0 else "." for s in range(16))
    if n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "half", ghosts=0.25, seed=b)
        if i == 6: put_fill(D, b, "build")
        continue
    vgroove(D, b, "beat8", ghosts=0.4, seed=b, k=kick, s="....X.......X...", h="x.x.x.x.x.x.x.x.")
    if n in ("サビ1", "サビ2", "最後のサビ", "イントロ") and i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
    if n == "間奏2": D.set(b, None, "..x.X..x.xX.x.X.", None)
    if i % 8 == 7 and not last: put_fill(D, b, "tomtrip" if n == "間奏2" else "small")
    if last and n not in ("最後のサビ",): put_fill(D, b, "snare16")

for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 0, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の17（16時）。マスロック。A長調・138。放課後の空き教室で、軽音部が新しい曲をつくる。"
          "16分5つでくり返すタッピングとキックが、4拍子の小節線をまたいでずれていく。合いことばの節は最初と間奏のタッピング。全員のユニゾンで切って終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.15}, special={"窓の外": -0.6, "最後のサビ": 0.35})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午後4時・放課後の机のタッピング・マスロック）で直すこと:
#   ギター: タッピングの線を DI ギター（明るいクリーン・粒をそろえる）に。和音のギターは、のばすだけでなく「下ろし・上げ」のまじったかき鳴らしに（小節ごとに型をずらす＝マスロックのずれ）。
#          歪みのギターも、左右でちがう型のかき鳴らしに
#   歌: Aメロはウィスパー（ひとりで机をたたく）、Bメロとサビはクリア、窓の外（ブリッジ）はウィスパー。最後のサビだけキュート（みんなでユニゾン）。ハモリは最後のサビ
from vt3x_lib import *
path = sys.argv[1]
to_di(path, S, "タッピングのギター", "bright_line", vol=0.07, seed=6)
MP = ["D..d.u.dD.u.d.u.", "D.u..d.uD..d.u.d", "D..d.uD..d.u.D.u", "D.u.d..D.u.d.DuD"]
pc = restrum(path, S, "ギター（和音", 0.45, lambda n, i, end, b: "D..d.u.dD.D-----" if end else MP[i % 4], seed=5, lag=0.014)
pd = restrum(path, S, "歪みのギター", 0.0, lambda n, i, end, b: "D.d.D.d.D.D-----" if end else ("D.d.d.D.d.d.D.d." if i % 2 == 0 else "D.ddD.d.D.d.D.dd"), seed=8)
add_parts(path, pc + pd, drop=lambda p: p.get("role", "").startswith("ギター（和音") or p.get("role", "").startswith("歪みのギター"))
final_gain(path, {"タッピング": 5, "最後のサビ": 1.6})
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 20, "最後のサビ": 24, "bridge": 0, "outro": 0}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.5, breaths=0.6)
    harmony(path, S, [("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {"verse": "whisper", "pre": "clear", "chorus": "clear", "bridge": "whisper", "最後のサビ": "cute"}, default="clear")
