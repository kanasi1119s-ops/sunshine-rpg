# vt3 16「おやつ宣戦布告」Snack-Time Declaration of War（仮）— ラウドロック。150・4/4。D短調（ドロップDの低い刻み）。
# 第3弾（0時〜24時の街）の 15時。表は docs/sound/vt3-plan.md。（13「お弁当交換条約」の「次の会議はおやつの3時に」の続き）
# 物語: 3時。冷蔵庫に残ったプリンはひとつだけ。うしろには兄。目が合った ── ここは戦場だ。スプーンを構えてにらみ合い、
#   じゃんけんはあいこばかり。兄の「半分こ」は断固拒否（プリンは形が命）。そこへ母が、冷蔵庫の奥からもうひとつ。
#   ふたつのプリンを並べて、ふたりで笑い出し、同じ鼻歌を口ずさむ。次はたいやき、しっぽはわたし。（大まじめに大げさに）
# 場面と強さ: 冷蔵庫（開く音 → 無音）→ イントロ（リフ・強）→ Aメロ1（叫ぶような短い句）→ Bメロ1（ハーフ・ためる）→ サビ1（高く歌う・強）
#   → リフ（節）→ Aメロ2 → Bメロ2 → サビ2 → ブレイクダウン「いただきます」（いちばん重い）→ ギターソロ
#   → 静けさ（クリーンのギターだけ・冷蔵庫を開ける一瞬）→ 最後のサビ（いちばん強い）→ スプーンを置く「カチ」
# 旋律の性格: Aメロは16分の短い言葉の連打（A4・D5 の叫び）、サビは D5 → F5 と高く伸ばす。
# この曲だけの音: ラウドの音（TRiDENT のギター・crocell-punch のドラム）。キックはトリガーと重いキックの2種類を重ねる（人間の決まり）。
#   ブレイクダウンで「いただきます」。ベースは明るくゴリッとした指弾きで、少し大きめ（人間の好み）。
#   合いことばの節（3・5・6・5・2）は、リフの場面でギターが弾く（F長調として A・C・D・C・G）。
from vt25_lib import *

S = Song("16", "pudding", "おやつ宣戦布告（仮）", "Snack-Time Declaration of War", 150, 4, "D", "minor", "ラウドロック（ボカロ）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.55
S.drum_scale = 0.85
S.keepers = {"Aメロ2": "ride"}   # v2: サビの裏のオープンハイハットをやめる（07・08 で点が上がった）
K = Key("D", "minor")          # oct 4 で 1 = D4

RIFF_CH = ["Dm", "Dm", "Bb", "C"]
A_CH = ["Dm", "Dm", "Bb", "C", "Dm", "Dm", "Gm", "A"]
B_CH = ["Gm", "Bb", "C", "A", "Gm", "Bb", "C", "A"]
C_CH = ["Bb", "C", "Dm", "Dm", "Bb", "C", "A", "A", "Gm", "Bb", "C", "Dm", "Bb", "C", "A", "Dm"]

S.scene("冷蔵庫", 2, "intro", ["Dm", "Dm"])
S.scene("イントロ", 12, "intro", RIFF_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("リフ", 8, "break", RIFF_CH)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ブレイクダウン", 8, "break", ["Dm", "Dm", "Dm", "Eb", "Dm", "Dm", "Dm", "Eb"])
S.scene("ギターソロ", 8, "solo", ["Bb", "C", "Dm", "Dm", "Bb", "C", "A", "A"])
S.scene("静けさ", 4, "bridge", ["Dm9", "Bbmaj7", "Gm9", "A7sus4"])
S.scene("最後のサビ", 24, "chorus", C_CH + C_CH[:8])
S.scene("スプーン", 4, "outro", ["Bb", "C", "Dm", "Dm"])

V = Voice(S, vol=0.21, delay=0.5, bright=0.0, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
GL = [S.track(f"Lギター（刻み{i + 1}）", "distGuitar", **rock_gtr_spec(0.05, -0.6, drive=0.55)) for i in range(3)]
GR = [S.track(f"Rギター（刻み{i + 1}）", "distGuitar", **rock_gtr_spec(0.047, 0.6, drive=0.55)) for i in range(3)]
RIFF = S.track("ギター（リフ）", "distGuitar", **rock_gtr_spec(0.07, -0.2, drive=0.55))
LGS = S.track("リードギター（ソロ）", "leadGuitar", **lead_gtr_spec(0.13, 0.05))
CLN = S.track("クリーンのギター", "guitar", amp="crystal", volume=0.08, pan=0.3, reverb=0.35, chorus=0, sustain=1.0)
WALL = [S.track(f"厚いシンセ{i + 1}", "pad", **pad_spec("kfbSupersaw", vol=0.03, pan=-0.6 + 0.6 * i, duck=0.4, sustain=1.0)) for i in range(3)]
BASS = S.track("ベース（指弾き・ゴリッと）", "bass", **rock_bass_spec(0.27))
KT = S.track("キックのトリガー", "kickTrigger", volume=0.09, pan=0)
FRIDGE = S.track("冷蔵庫（カホン）", "cajon", volume=0.08, pan=0.2, reverb=0.2)
SPOON = S.track("スプーン（グロッケン）", "glockenspiel", volume=0.06, pan=0.25, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.07, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.25 5:0.25 5:0.5 3:0.5 R:0.5 5:0.25 5:0.25 1':0.5 R:0.5", "R:0.5 4:0.25 4:0.25 4:0.5 3:0.5 2:1 R:1",
      "R:0.5 5:0.25 5:0.25 5:0.5 3:0.5 R:0.5 5:0.25 5:0.25 2':0.5 R:0.5", "R:0.5 1':0.25 1':0.25 7:0.5 6:0.5 5:1 R:1",
      "R:0.5 5:0.25 5:0.25 5:0.5 3:0.5 R:0.5 5:0.25 5:0.25 1':0.5 R:0.5", "R:0.5 4:0.25 4:0.25 4:0.5 3:0.5 2:1 R:1",
      "R:0.5 6:0.5 6:0.5 5:0.5 6:0.5 1':0.5 2':0.5 1':0.5", "5:2 R:2"]
A1 = ("さんじがきたぞ/れいぞうこ/のこりはひとつ/ぷりんだけ/うしろにはあに/めがあったぞ/ここはせんじょうだ/"
      "すぷーんかまえ/にらみあい/とおくでははが/わらってるよ/ちいさなかっぷが/ふるえてる/いざいざかいせん")
A2 = ("じゃんけんでいく/あいこでしょ/なんかいやっても/きまらない/あにがいいだす/はんぶんこ/そんなのいやだよ/"
      "ぷりんのいのち/まるごとだ/かあさんがきて/ためいきを/れいぞうこから/もうひとつ/かくしてあったのか")
VB = ["R:1 3:1 4:1 5:1", "6:2 5:2", "R:1 4:1 5:1 6:1", "7:2 6:2", "R:1 5:1 6:1 7:1", "1':2 7:2", "R:1 6:1 7:1 1':1", "#7:3 R:1"]
B1 = "ひけないの/あにだってさ/ゆずれない/いちびょう"
B2 = "ふたつめの/ぷりんにね/ぼうぜんと/かたまった"
VC = ["R:0.5 1':0.5 3':1 2':0.5 1':0.5 7:1", "1':1.5 5:0.5 5:1 R:1", "R:0.5 7:0.5 2':1 1':0.5 7:0.5 6:1", "5:2 R:2",
      "R:0.5 1':0.5 3':1 2':0.5 1':0.5 2':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 6:0.5 7:0.5 1':0.5 2':1 1':1", "#7:2 R:2",
      "R:0.5 1':0.5 3':1 2':0.5 1':0.5 7:1", "1':1.5 5:0.5 5:1 R:1", "R:0.5 7:0.5 2':1 1':0.5 7:0.5 6:1", "5:2 R:2",
      "R:0.5 1':0.5 3':1 2':0.5 1':0.5 2':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 6:0.5 7:0.5 1':0.5 2':1 #7:1", "1':3 R:1"]
C1 = "おやつせんそうだ/ゆずれないよ/すぷーんをぬけば/かみなりなる/おやつせんそうだ/あまいぷりん/かったほうのものだ/それがおきて"
C2 = "おやつせんそうだ/あいこでしょう/なんどもふりあげ/きまらないよ/おやつせんそうだ/ぬるくなるよ/はやくきめなくちゃ/さんじまでに"
C3 = ("おやつせんそうだ/しゅうせんだよ/ふたつのぷりんを/ならべたらね/おやつせんそうだ/わらいだした/おなじはなうたを/くちずさんだ/"
      "おやつせんそうだ/またあしたね/つぎはたいやきだ/しっぽはわたし")
BD = ["R:2 5:0.5 5:0.5 5:0.5 5:0.5", "1':0.5! 5:0.5 R:3"] * 4
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA + VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("ブレイクダウン", BD, "いただきます/いただきます/いただきます/いただきます", o=3)
put("最後のサビ", VC + VC[:8], C3)

# ================= ギター =================
def chug8(b, ch, n=3, pat=None):
    """8分の刻み（ジャジャジャジャ）。左はパワーコード（D2〜）、右は C3〜B4 の中の和音"""
    pw = power(ch, "D2")
    r = low(ch, "C3"); up = [x for x in tones(ch, nm(r + 1), nm(r + 12))][:2]
    while len(up) < 2: up.append(r + 12)
    rv = [r] + up
    for j in range(n):
        if pat:
            GL[j].bar(b, pat.replace("x", nm(pw[j]))); GR[j].bar(b, pat.replace("x", nm(rv[j])))
        else:
            GL[j].bar(b, " ".join(f"{nm(pw[j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))
            GR[j].bar(b, " ".join(f"{nm(rv[j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))


def wall(b, ch):
    v = voice(ch, 62, 3)
    for j in range(3): WALL[j].bar(b, f"{nm(v[j])}:4")


RIFFS = ["D2:0.5! D2:0.25 D2:0.25 F2:0.5 D2:0.5 G2:0.5! F2:0.5 D2:0.5 C2:0.5", "D2:0.5! D2:0.25 D2:0.25 F2:0.5 D2:0.5 A2:0.5! G2:0.5 F2:0.5 E2:0.5",
         "A#1:0.5! A#1:0.25 A#1:0.25 D2:0.5 A#1:0.5 F2:0.5! D2:0.5 A#1:0.5 A#1:0.5", "C2:0.5! C2:0.25 C2:0.25 E2:0.5 C2:0.5 G2:0.5! E2:0.5 C#2:0.5 D2:0.5"]
MOTIF = ["R:1 A3:0.5 C4:0.5 D4:1 C4:0.5 G3:0.5", "F3:2 R:2"]          # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "イントロ":
        RIFF.bar(b, RIFFS[i % 4])
        if i >= 4: chug8(b, ch)
        if i >= 8: wall(b, ch)
    elif n in ("Aメロ1", "Aメロ2"):
        # v2: Aメロが 6.7〜7.2（低いリフが毎小節つづき、8分の刻みも重なって歌のまわりが埋まっていた）
        #     → リフは2小節に1回（あいだは のばすパワーコード）、刻みは2分の和音に
        RIFF.bar(b, (RIFFS[i % 4] if ch in ("Dm",) or i % 4 < 2 else RIFFS[2 + (i % 2)]) if i % 2 == 0 else f"{nm(power(ch, 'D2')[0])}:4")
        if n == "Aメロ2" or i >= 8: chug8(b, ch, 2, "x:2! x:2")
    elif n in ("Bメロ1", "Bメロ2"):
        chug8(b, ch, 3, "x:2! x:2"); wall(b, ch)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        chug8(b, ch); wall(b, ch)
    elif n == "リフ":
        RIFF.bar(b, MOTIF[i - 2] if i in (2, 3) else RIFFS[i % 4]); chug8(b, ch, 2)
    elif n == "ブレイクダウン":
        chug8(b, ch, 3, "x:0.75! x:0.25 R:0.5 x:0.5! R:1 x:0.25 x:0.25 x:0.5!")
        RIFF.bar(b, "D2:0.75! D2:0.25 R:0.5 D2:0.5! R:1 D#2:0.25 D2:0.25 D2:0.5!" if ch != "Eb" else "D#2:0.75! D#2:0.25 R:0.5 D#2:0.5! R:1 D2:0.25 D#2:0.25 D#2:0.5!")
    elif n == "ギターソロ":
        chug8(b, ch, 2); wall(b, ch)
        SOLO = ["F4:0.5 A4:0.5 D5:0.5 F5:0.5 E5:1 D5:1", "C5:1 E5:0.5 G5:0.5 F5:1.5 E5:0.5", "D5:0.5 F5:0.5 A5:1 G5:0.5 F5:0.5 E5:0.5 D5:0.5", "A4:3 R:1",
                "D5:0.5 C5:0.5 A#4:0.5 D5:0.5 F5:1 D5:1", "E5:0.5 G5:0.5 C5:0.5 E5:0.5 G5:1 A5:1", "C#5:0.5 E5:0.5 A5:0.5 E5:0.5 C#5:1 A4:1", "A4:3 R:1"]
        LGS.bar(b, SOLO[i])
    elif n == "静けさ":
        t = tones(ch, "D4", "D6"); CLN.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))
    elif n == "スプーン":
        if i < 2: chug8(b, ch); wall(b, ch)
        elif i == 2: chug8(b, ch, 3, "x:0.5! R:3.5")

FRIDGE.bar(S.sc("冷蔵庫")[0], "D3:0.5 R:0.25 D3:0.25 R:3")      # 冷蔵庫が開く「パカッ」
SPOON.bar(S.sc("スプーン")[3], "R:1 E7:0.25 R:2.75")             # スプーンを置く「カチ」

# ================= ベース（明るくゴリッと・少し大きめ）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "D1")
    if n in ("冷蔵庫", "静けさ"): continue
    if n == "イントロ" and i < 4: continue
    if n == "ブレイクダウン": BASS.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.25 R:0.5 {nm(r)}:0.5 R:1 {nm(r)}:0.25 {nm(r)}:0.25 {nm(r)}:0.5"); continue
    if n in ("Bメロ1", "Bメロ2"): BASS.bar(b, f"{nm(r)}:2 {nm(r)}:2"); continue
    if n == "スプーン":
        if i < 2: BASS.bar(b, bass_line(S, b, "root8", lo="D1"))
        elif i == 2: BASS.bar(b, f"{nm(r)}:0.5 R:3.5")
        continue
    BASS.bar(b, bass_line(S, b, "root8", lo="D1"))

for name in ("サビ1", "サビ2", "最後のサビ", "ブレイクダウン"): cym_swell(CYM, S.sc(name)[0], 2, "C4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("冷蔵庫", "静けさ"):
        if n == "静けさ" and i == 3: put_fill(D, b, "build")
        continue
    if n == "イントロ":
        if i < 4: D.set(b, "X.......X.......", "................", "x.x.x.x.x.x.x.x.")
        else: vgroove(D, b, "vrock", ghosts=0.15, seed=b)
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "tomdown")
    elif n in ("Aメロ1", "Aメロ2", "リフ"):
        vgroove(D, b, "vrock2" if n == "リフ" else "vrock", ghosts=0.2, seed=b)
        if i == 0: crash(D, b)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "half", ghosts=0.2, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "vrock2", ghosts=0.15, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "ブレイクダウン":
        D.set(b, "X..XX.....X.XX..", "........X.......", "x...x...x...x...")
        if i % 4 == 0: crash(D, b, "C2", 6)
    elif n == "ギターソロ":
        vgroove(D, b, "vrock", ghosts=0.2, seed=b)
        if i == 0: crash(D, b)
        if last: halt(D, b, 1)
    elif n == "スプーン":
        if i < 2: vgroove(D, b, "vrock2", ghosts=0.15, seed=b)
        if i == 0: crash(D, b, "C2", 6)
        if i == 2: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 8)

# キックのトリガー（キックと同じ所。人間の決まり: トリガーと重いキックの2種類）
for b in range(S.nb):
    kk = D.K[b]
    toks, t = [], 0
    for q, c in enumerate(kk):
        if c in "Xx":
            if q > t: toks.append(f"R:{(q - t) * 0.25:g}")
            toks.append(f"{'C2' if c == 'X' else 'C1'}:0.25"); t = q + 1
    if toks:
        if t < D.n: toks.append(f"R:{(D.n - t) * 0.25:g}")
        KT.bar(b, " ".join(toks))

for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の16（15時）。ラウドロック。D短調・150。最後のプリンをめぐる兄弟げんか（大まじめに大げさに）。"
          "TRiDENT のギター・crocell-punch のドラム・キックのトリガー・明るい指弾きのベース。ブレイクダウンで「いただきます」。"
          "合いことばの節はリフの場面のギター。スプーンを置く「カチ」で終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.1}, special={"静けさ": -0.6, "最後のサビ": 0.35, "ブレイクダウン": 0.2})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午後3時・冷蔵庫のプリンをめぐる戦い・ラウドロック）で直すこと:
#   ギター: 全部同じ強さの刻みをやめ、左＝強い下ろしをずらして置く（1拍目・2拍目の裏・4拍目）、右＝「ジャッ・ジャジャ」の16分まじり。4小節ごとにたたみかける。
#          刻みが終わる小節は最後を伸ばす。ブリッジミュートの短い音は使わない（人間: 聞きにくい）。クリーンのギターは DI ギターに。音色（歪み）はそのまま
#   電子の音: 厚いシンセをスーパーソー（kfbSupersaw）に
#   歌: Aメロ・Bメロはクリア、サビとブレイクダウン（いただきます）はキュート（まじめに戦うほどかわいい）、静けさはウィスパー。ハモリは サビ2 の後半と最後のサビ
from vt3x_lib import *
path = sys.argv[1]
pl = restrum(path, S, "Lギター（刻み", -0.6, lambda n, i, end, b: "D.d.d.D.d.d.D---" if end else ("D.d.D.d.D.D.DDDD" if i % 4 == 3 else "D.d.d.D.d.d.D.d."), seed=2)
pr = restrum(path, S, "Rギター（刻み", 0.6, lambda n, i, end, b: "D.ddD.d.D.d.D---" if end else ("DuDuD.ddDuDuD.D." if i % 4 == 3 else ("D.ddD.d.D.ddD.d." if i % 2 == 0 else "D.d.D.ddD.d.D.dd")), seed=9)
add_parts(path, pl + pr, drop=lambda p: p.get("role", "").startswith("Lギター（刻み") or p.get("role", "").startswith("Rギター（刻み"))
to_di(path, S, "クリーンのギター", "clean_arp", vol=0.07, seed=4)
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 8, "pre": 14, "chorus": 22, "最後のサビ": 26, "break": 0, "bridge": 6, "outro": 0}, scoop=0.35, slash=0.8, vib_min_beats=1.5, vib_start=0.5, auto=0.5, breaths=0.5)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {"verse": "clear", "pre": "clear", "chorus": "cute", "break": "cute", "bridge": "whisper"}, default="clear")
