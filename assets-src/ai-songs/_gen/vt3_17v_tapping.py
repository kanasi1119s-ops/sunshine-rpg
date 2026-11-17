# 17「放課後タッピング」v4（エレクトロ・ダンスロックのボカロ曲）。仮。
# 人間（2026-11-16 23:31）:「16から17ボカロ感強めで1から作り直しましょう。4から5分の曲でお願いします。」
# 16（高速ボカロック 176・ピアノのリフ・丸サ）とは別の形のボカロ感にする:
#   中くらいの速さの4つ打ちダンスロック（132）／タッピングのギターの2小節のリフが曲を引っぱる／裏で短く切るピアノ／うねるスーパーソウ
#   サビは王道進行（IV→V→IIIm→VIm）で短3度上へ転調（ニ短調 → ヘ短調）、最後のサビは半音上（嬰ヘ短調）／歌は16分で食う・サビの頭は合いことば「タッピング」
#   歌のない「ドロップ」（リフと、歌のかけら「たっぴんぐ」）／Bメロの最後は全員止まって歌だけ／Cメロ → ギターの番 → 落ちサビ
# 曲を決める表:
#   形 … タッピングひとり → 全員 → A（1つの和音 → 丸サ）→ B → サビ → ドロップ → A2（短い）→ B2 → サビ2 → ドロップ2 → Cメロ → ギターの番 → 落ちサビ → 最後のサビ（半音上）→ リフで止まる
#   強さ … 前奏 3→7 → A 5 → B 4 → サビ 9 → ドロップ 8 → A2 6 → B2 4 → サビ2 9.5 → ドロップ2 8.5 → C 3 → ギター 7 → 落ち 2 → 最後 10
#   旋律の性格 … Aメロは16分まじりで5度を行き来。サビは同じ音を打って4度跳ぶ合いことば → 長い音はウラから
# 歌詞: 弦＝六本の川、新しい曲＝名前のない鳥、部室＝夕焼けの実験室。長さ 4分35秒ほど。
# 使い方: VB_VOCAL=1 python3 vt3_17v_tapping.py <出力.json>
from vocalo_lib import *
import random as _r, re as _re

S = Song("17", "tapping", "放課後タッピング（仮）", "After School Tapping", 132, 4, "D", "minor", "エレクトロ・ダンスロック")
S.kit = "naked-x"; S.flags = S.flags + " --bass bnb-loud --space room --space-wet 0.08"      # 16（v11）と音を変える: ドラム・エレピ・FM のベース・きらめくパッド・クリーンのギター
K = Key("D", "minor"); KF = Key("F", "minor"); KG = Key("F#", "minor"); SC = {2, 4, 5, 7, 9, 10, 0}; SCF = {5, 7, 8, 10, 0, 1, 3}; SCG = {6, 8, 9, 11, 1, 2, 4}
MARU = ["Dm7", "Bbmaj7", "Gm7", "A7"]      # 16 が丸サ進行なので、こちらは Im → ♭VI → IVm → V7（名前は MARU のまま）
A_CH = ["Dm7"] * 8 + MARU * 2
B_CH = ["Gm7", "A7", "Dm7", "D7", "Gm7", "Am7", "Bbmaj7", "C7"]
C_CH = ["Dbmaj7", "Eb", "Cm7", "Fm7"] * 3 + ["Dbmaj7", "Eb", "Fm", "Fm"]
G_CH = ["Dmaj7", "E", "C#m7", "F#m7"] * 3 + ["Dmaj7", "E", "F#m", "F#m"]
DR_CH = ["Bbmaj7", "C", "Dm7", "Dm7|C", "Bbmaj7", "C", "Dm7", "A7"]
S.scene("前奏", 8, "intro", ["Dm7"] * 8)
S.scene("Aメロ", 16, "verse", A_CH)
S.scene("Bメロ", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("ドロップ", 8, "break", DR_CH)
S.scene("Aメロ2", 8, "verse", MARU * 2)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ドロップ2", 8, "break", DR_CH)
S.scene("Cメロ", 8, "bridge", ["Bbmaj7", "C", "Am7", "Dm7", "Bbmaj7", "C", "A7", "A7"])
S.scene("ギターの番", 8, "solo", MARU * 2)
S.scene("落ちサビ", 8, "chorus", C_CH[:8])
S.scene("最後のサビ", 24, "chorus", G_CH + G_CH[8:])
S.scene("おわり", 8, "outro", ["F#m7"] * 8)
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(1704)

# ================= 歌 =================
Va, Va2, Vb, Vb2 = "x-xx-x-x.xx-x-x-", "x-x-.x--x---....", "..xx-x-xx-x-.x-x", "x--x--x-----...."
Vc, Vc2, Vd, Vd2 = "x-xx-xx-x-x-xx-x", "x---x.x---......", "..x-xx-x.x-xx-x-", "x-x-x-x.x---...."
AP = [Va, Va2, Vb, Vb2, Vc, Vc2, Vd, Vd2] * 2
AD = ["5 1' 5 1' 7 5 4 5 7", "1' 7 4 5", "4 5 7 5 4 3 4 5", "5 4 1", "1 3 4 5 5 7 5 4 5 7", "1' 7 1'", "7 1' 7 1' 7 5 7 1'", "1' 1' 7 #7 1'",
      "5 1' 5 1' 7 5 4 5 7", "1' 7 5 5", "4 5 7 5 4 3 4 5", "5 4 2", "1 3 4 5 5 7 5 4 5 7", "1' 7 1'", "7 1' 7 1' 7 5 7 1'", "1' 7 1' #7 1'"]
A1 = ["ちゃいむがなりやんではじまる", "ゆうやけのじっけんしつで", "つくえたたくゆびさきおどる", "ろくほんのかわがめをさます",
      "だれもしらないうたうまれる", "なまえのないとりがいま", "はねをひろげてまどのそとへ", "あかねいろのそらめざしてる"]
A2 = ["まちがえたおとさえわらえる", "もういちどといってわらう", "ゆびがおぼえるまではなんど", "くりかえしてゆくほうかごだ"]
BP_ = ["x---x---x-x-x---", "x-------x-----..", "x-x-x---x-x-x---", "x-----------....", "x---x---x-x-x---", "x-------x-----..", "x-xx-xx-x-xx-xx-", "x.x---.........."]
BD = ["4 4 6 5 4", "5 #7", "1' 1' 7 5 7 1'", "7", "4 4 6 5 4", "5 7", "3 3 4 5 5 6 5 4 5 6", "7 #7"]
B1 = ["まだへたくそな", "このおとだけど", "きみとならせば", "どこまでもとべるきがする"]
B2 = ["ゆうやけがもう", "しずみそうでも", "あとすこしだけ", "このままでならしていたい"]
Xa, Xa2, Xb, Xb2, Xc, Xc2, Xd, Xd2 = "x-x-xx-x--x-x-x-", ".x----x.x---....", "..x-xx-x-x-xx-x-", ".x----------....", "x-xx-x--x-xx-x--", "x--x--x-.x----..", "..x-x-xx-x-x-xx-", "x-----------...."
CP = [Xa, Xa2, Xb, Xb2, Xc, Xc2, Xd, Xd2] * 2
CD = ["5 5 1' 5 5 5 1' 5", "7 5 7", "5 5 7 5 4 5 7 5", "5", "6 6 1' 6 5 6 1' 6", "7 7 5 7", "7 5 4 5 7 5 7 1'", "1'"] * 2
C1 = ["たっぴんぐたっぴんぐひびけ", "かわをこえていけよ", "なまえのないとりはばたけ", "ゆうやけのむこうへ", "たっぴんぐたっぴんぐとどけ", "まどのそとのきみへ", "まだなまえのないこのうた", "いまここでうまれた"]
C2 = C1[:5] + ["あしたのぼくらへと", "へたくそなままのこのおと", "それでもすきなんだ"]
C3 = C1 + ["たっぴんぐたっぴんぐひびけ", "なまえをつけようか", "ほうかごのとりとよぼうか", "あしたもここでまた"]
MP = ["x---x---x-x-x---", "x-------x---....", "..x-x---x-x-x---", "x-----------...."] * 2
MD = ["3 3 5 6 5", "4 7", "5 5 7 2' 7", "1'", "6 6 5 6 1'", "2' 7", "#7 #7 2' 3' 2'", "2'"]
M1 = ["げんがきれても", "いたむゆびも", "ここがぼくらの", "じっけんしつだ"]
DP, DD = "x-.x-x-x--......", ["5 5 7 5", "5 5 7 1'"]      # ドロップの歌のかけら「たっぴんぐ」


def put(name, pats, degs, phrases, key=K, o=4, bars=None):
    lines, text = song_phrases(pats, degs, phrases); bars = bars or S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ", AP, AD, A1); put("Bメロ", BP_, BD, B1); put("サビ1", CP, CD, C1, key=KF); put("Aメロ2", AP[:8], AD[8:], A2); put("Bメロ2", BP_, BD, B2); put("サビ2", CP, CD, C2, key=KF)
put("Cメロ", MP, MD, M1); put("落ちサビ", CP[:8], CD[:8], C1[:4], key=KF); put("最後のサビ", CP + CP[8:], CD + CD[8:], C3, key=KG)
# v5（2026-11-17 人間「もっと寄せようか」＝Kawaii future bass に）: ドロップの「たっぴんぐ」は歌の行ではなく、声を切って音程をつけるチョップにした（下の chops）

# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


def scale(b): n = S.scene_of(b)[0]; return SCG if n in ("最後のサビ", "おわり") else SCF if n in ("サビ1", "サビ2", "落ちサビ") else SC


def strum(tracks, b, pat, **kw):
    kw["drive"] = False; kw.pop("strings", None); c1, c2 = halves(b)      # クリーンのギター（弦の数は毎回変える）
    if c1 == c2: gtr_strum(tracks, S, b, pat, c1, RNG, **kw)
    else: gtr_strum(tracks, S, b, pat[:8] + "." * 8, c1, RNG, **kw); gtr_strum(tracks, S, b, "." * 8 + pat[8:], c2, RNG, **kw)


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), scale(b), lo=29)); SUB.bar(b, steps("x-------x-------" if not pat.endswith("........") else "x-------........", [N(low(c1, "F1")), N(low(c2, "F1"))]))


def piano(b, pat, short=0.2, center=66):
    c1, c2 = halves(b)
    if c1 == c2: rows = relcut(PN, c1, pat, center=center, short=short)
    else: r1, r2 = relcut(PN, c1, pat[:8], center=center, short=short), relcut(PN, c2, pat[8:], center=center, short=short); rows = [a + " " + c for a, c in zip(r1, r2)]
    for t, r in zip(PN, rows): t.bar(b, r)


def saw(b, pat):
    c1, c2 = halves(b); v, v2 = wide9(c1), wide9(c2)
    for j in range(5): SAW[j].bar(b, steps(pat, [N(v[j])]) if c1 == c2 else steps(pat[:8], [N(v[j])]) + " " + steps(pat[8:], [N(v2[j])]))


def riff(b, i, ch=None):
    """タッピングの2小節のリフ（たたく→はなす→左手でたたく の3つ組。2小節目は順を変えて、最後を伸ばす）"""
    c = ch or halves(b)[0]; TAP.bar(b, tap3(c, "xxxxxxxxxxxxxxxx", order="TPH", start=0, lo="D4") if i % 2 == 0 else tap3(c, "xxxxxxxxxxxx-...", order="THP", start=1, lo="D4"))


CLEAN = dict(di="emily", stringNoise=True, amp="jpopClean", ampDrive=0.12, chorus=0, humanPitch=0, noScoop=True, powerChord=False, sustain=1.3, release=0.5)
GFX = [{"type": "filter", "kind": "highpass", "freq": 110, "q": 0.7}, {"type": "eq", "low": -1, "mid": 1.5, "midHz": 1800, "high": 1}, {"type": "room", "mix": 0.1}]
TAP = S.track("タッピングのギター（クリーン）", "distGuitar", volume=0.8, pan=-0.2, fx=GFX + [{"type": "pingpong", "beats": 0.75, "mix": 0.14, "feedback": 0.25}], legato=True, **CLEAN)
LEAD = S.track("リードギター", "distGuitar", **lead_gtr_spec(0.12, 0.15))
PN = [S.track(f"エレピ（短く切る{i + 1}）", "keys", patch="kfbGlassEp", volume=0.075, pan=0.1 + 0.15 * i, reverb=0.15, sustain=0.5) for i in range(3)]
PL = S.track("エレピ（のばす）", "keys", patch="kfbGlassEp", volume=0.11, pan=0.0, reverb=0.25, sustain=1.5)
GL = [S.track(f"Lギター{i + 1}弦め（クリーン）", "distGuitar", volume=0.07, pan=-0.6, fx=GFX, **CLEAN) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め（クリーン）", "distGuitar", volume=0.07, pan=0.6, fx=GFX, **CLEAN) for i in range(6)]
BASS = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.1, pan=0, duck=0.25, fx=rack_bass())
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.022, pan=0, duck=0.4)
SAW = [S.track(f"きらめくパッド{i + 1}", "lead", patch="kfbSparklePad", volume=0.03, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.65, fx=rack_supersaw()) for i in range(5)]
PLK = S.track("駆け上がるプラック", "lead", patch="kfbSquarePluck", volume=0.05, pan=0.3, reverb=0.25, fx=rack_pluck())
KSAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.03, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.65, fx=rack_supersaw()) for i in range(5)]      # ドロップとサビ: キックでへこむ（ポンプ）
SWELL = [S.track(f"ふくらむスーパーソウ{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.035, pan=-0.4 + 0.4 * i, reverb=0.3) for i in range(3)]                                               # Bメロ: 「ポワン」とふくらむ和音
BELL = S.track("ベル", "lead", patch="kfbGlocken", volume=0.08, pan=0.25, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
CLAP = S.track("クラップ", "guitar", patch="kawaiiFx", volume=0.07, pan=0.05, reverb=0.15, modulate=False)
KGATE = ["x-x-x-..x-x-.x-.", "x-----x-x-..x-x-", "x-.x-.x-x-.x-.x-", "x-x-..x-..x-x-x-", "x-x-x-..x-x-.x-.", "x-.x-.x-....x-x-", "x-----x-----x-x-", "x-x-x-x-........"]      # ドロップ: 和音が小節ごとに違う型で切れる


def ksaw(b, pat):
    c1, c2 = halves(b); v, v2 = wide9(c1), wide9(c2)
    for j in range(5): KSAW[j].bar(b, steps(pat, [N(v[j])]) if c1 == c2 else steps(pat[:8], [N(v[j])]) + " " + steps(pat[8:], [N(v2[j])]))


def swell(b, pat="x-------------.."):
    v = sorted(voice(halves(b)[0], 66, 3))
    for j in range(3): SWELL[j].bar(b, steps(pat, [N(v[j])]))
FXT = S.track("効果音", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.2, modulate=False)

OCT = [("x-x-x-x-x-x-x-x-", "18181858"), ("x-x-x-x-x-x-x-x-", "181815wd"), ("x-x-x-x-x-x-x-x-", "18158535"), ("x-x-x-x-x-x-x-x-", "1818wdwa"[:8])]      # 4つ打ちのベース（根音とオクターブを行き来して、終わりで歩く）
WB = [("x-.x..x-x-.xx-x-", "11355wd"), ("x-..x.x-..x-x-x-", "1875wd"), ("x-x-..x-.xx-x-x-", "12355wd"), ("x-.x-.x-x-x-x-x-", "1123123")]
OFF = ["..x...x...x...x.", "..x...x...x..x.x", "..x...x..x.x..x.", "..x.x.x...x...x."]                                                  # 裏で短く切るピアノ
GATE = ["x---x-x---x-x-x-", "x-x---x-----x-x-", "x---x-x-x-x-x---", "x-x---x---x-x---"]
G_SOLO = ["R:0.5 D5:0.5_ F5:0.5 A5:1/ G5:0.5_ F5:1", "F5:1.5/ E5:0.25_ D5:0.25 Bb4:1 R:1", "R:0.5 G4:0.5 Bb4:0.5_ D5:0.5 F5:0.5 G5:0.5_ F5:0.5 D5:0.5", "R:1 E5:0.5 G5:0.5_ A5:0.5 A5:0.5 G5:0.5_ E5:0.5",
          "D6:0.75 D6:0.75 C6:0.5_ A5:0.5 F5:1.5/", "R:0.5 F5:0.5_ A5:0.25_ Bb5:0.25 D6:1/ Bb5:0.5_ A5:0.5 F5:0.5", "G5:0.5 G5:0.5 F5:0.5_ D5:0.5 Bb4:0.5 D5:0.5_ F5:1", "R:0.5 C#5:0.5 E5:1/ A5:2~"]


def four(b, i, hat16=True):
    D.set(b, "X...X...X...X..." if i % 4 != 3 else "X...X...X...X.x.", "....X.......X..." if i % 4 != 3 else "....X.......X..x", ("x.xxx.xxx.xxx.xx" if i % 2 == 0 else "xxx.xxx.xxx.xxx.") if hat16 else "x.x.x.x.x.x.x.x.")


def chorus(b, i, n):
    big = n == "最後のサビ"; j = i % 16 if i < 16 else 8 + (i - 16); stop = j == 7 or (j == 15 and not (big and i == L_LAST))
    if stop:
        saw(b, "x-------........"); bass(b, "x-x-x-x-........", "1815"); strum(GL, b, "x-------........", strings=3); strum(GR, b, "x-------........", strings=4); piano(b, "..x...x.........")
        D.set(b, "X...X...........", "....X...........", "x.xxx.xx........"); fill_cresc(D, b, 2); return
    ksaw(b, GATE[(i + (2 if n == "サビ2" else 0)) % 4]); bass(b, *OCT[(i + (1 if n == "サビ2" else 0)) % 4]); piano(b, OFF[i % 4])
    if CP[j] in (Xb2, Xd2): FXT.bar(b, fx_bar((3, "kira", 1)))
    if j % 4 == 3: hat_roll(HATR, b, 0.5)
    strum(GL, b, "x-------x-------" if i % 2 == 0 else "x-----x---------", strings=3); strum(GR, b, "x---------------" if i % 2 == 0 else "x-----x---x-----", strings=4)
    four(b, i); CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
    if CP[j] in (Xb2, Xd2): TAP.bar(b, "R:1.5 " + tap3(halves(b)[0], "xxxxxxxxx-", order="TPH", start=(i // 4) % 3, lo="F4"))      # 歌が伸ばしている後ろで、タッピングが答える
    if j % 8 == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
    if j % 4 == 3: fill_cresc(D, b, 1)
    if big and i == L_LAST: saw(b, "x---------------"); D.set(b, "X.........X.X...", "........X...X.XX", "X.x.X.x.........")


L_LAST = 23
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "前奏":                                                                # タッピングひとり（4小節）→ 全員
        riff(b, i)
        # ドラムの入り方（この曲）: キックだけが先に4つ打ちで入る（3小節目）→ 5小節目でハイハットとベースが足される → 7小節目でスネア。フィルもクラッシュも使わない。最後の2拍はドラムが抜ける
        if i in (2, 3): D.set(b, "X...X...X...X...", "................", "................"); CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i >= 4: bass(b, *OCT[i % 4]); piano(b, OFF[i % 4])
        if i in (4, 5): D.set(b, "X...X...X...X...", "................", "x.x.x.x.x.x.x.x.")
        if i >= 6: four(b, i); strum(GL, b, "x-------x-------", strings=3); strum(GR, b, "x---------------" if not odd else "x-----x---x-----", strings=4)
        if last: D.set(b, "X...X...X.......", "....X...........", "x.xxx.xx........")
    elif n in ("ドロップ", "ドロップ2", "おわり"):                                    # 歌は「たっぴんぐ」のかけらだけ。リフが主役
        two = n == "ドロップ2"; end = n == "おわり"
        if end and last:
            TAP.bar(b, tap3(halves(b)[0], "xxxxxxxxx-......", order="TPH", start=0, lo="F#4")); bass(b, "x-x-x-x-x-......", "18181"); strum(GL, b, "x-------x-......", strings=3); strum(GR, b, "x-------x-......", strings=4)
            D.set(b, "X...X...X.......", "....X...X.......", "x.xxx.xxx......."); continue
        if end:                                                                     # おわりは、タッピングのリフと4つ打ち
            riff(b, i); saw(b, ["x-x-x---x-x-x---", "x---x-x-x---x-x-"][i % 2]); bass(b, *OCT[(i + 2) % 4]); four(b, i); CLAP.bar(b, "R:1 B4:1 R:1 B4:1"); piano(b, OFF[(i + 1) % 4])
            strum(GL, b, "x-------x-------", strings=3); strum(GR, b, "x-----x---x-----" if odd else "x---------------", strings=4); PLK.bar(b, arp16(halves(b)[0], "xxxxxxxx........" if not odd else "........xxxxxxxx", (0, 1, 2, 3, 4, 5, 6, 7), lo="D5", hi="D7"))
            if i in (0, 4): crash(D, b, "C2", 4)
            continue
        # Kawaii future bass のドロップ: 半分の速さ／スーパーソウが小節ごとに違う型で切れてポンプ／ベースも同じ型／3拍目にクラップ／偶数小節はタッピング、奇数小節は声のチョップとベル（かけ合い）／ハイハットのロール／きらきら
        g = KGATE[(i + (3 if two else 0)) % 8]; ksaw(b, g); c1, c2 = halves(b); r = low(c1, "F1"); BASS.bar(b, steps(g, [N(r + (12 if q % 5 == 4 else 0)) for q in range(onsets(g))])); SUB.bar(b, steps("x-------x-------", [N(r), N(low(c2, "F1"))]))
        if not odd: TAP.bar(b, tap3(c1, "xxxxxxxxxxxx....", order="TPH", start=(i // 2) % 3, lo="D4"))
        else: t = [N(m) for m in tones(c1, "D5", "D6")]; BELL.bar(b, steps("........x.x.x-x-", [t[0], t[1], t[2 % len(t)], t[-1]])); FXT.bar(b, fx_bar((3, "kira" if i % 4 == 1 else "pyon", 1)))
        feel(D, b, "half" if i % 4 != 3 else "halfopen"); CLAP.bar(b, "R:2 B4:1 R:1")
        if i == 0 and not two: D.set(b, "....X.....x.....", "........X.......", "....x.x.x.x.x.x."); FXT.bar(b, fx_bar((0, "impact", 2)))      # ドロップ1: 1拍目は和音とインパクトだけ。ドラムは2拍目から
        elif i == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2), (0, "sub", 2)))
        if i in (3, 7): hat_roll(HATR, b, 0.5 if i == 3 else 1)
        if last: fill_cresc(D, b, 2, toms=False) if two else D.set(b, "X.........x.....", "........X...X.X.", "X.x.X.x.........")
    elif n in ("Aメロ", "Aメロ2"):
        two = n == "Aメロ2"; first = (not two) and i < 8; stop = last
        if stop: bass(b, "x-x-x-x-........", "1815"); piano(b, "..x...x........."); D.set(b, "X...X...........", "....X...........", "x.x.x.x........."); fill_cresc(D, b, 2); continue
        if first:                                                                   # 1つの和音。ベースと、裏のピアノ。歌の句の終わりにタッピングのかけら
            bass(b, *WB[i % 4]); piano(b, OFF[i % 4]) if i >= 4 else None
            if odd: TAP.bar(b, "R:2 " + tap3("Dm7", "xxxxxx", order="TPH", start=(i // 2) % 3, lo="D4") + " R:0.5")
            D.set(b, "X.....x.X......." if not odd else "X.....x.X.x.....", "....X.......X...", "x.x.x.x.x.x.x.x.")
        else:
            bass(b, *OCT[i % 4]); piano(b, OFF[i % 4]); strum(GL, b, "x-------x-------" if not odd else "x---------------", strings=3); four(b, i, hat16=two)
            if two: strum(GR, b, "x-----x---x-----" if odd else "x---------------", strings=4); saw(b, "x---------------") if i >= 4 else None
        if i == 8 and not two: crash(D, b, "C2", 4)                                   # Aメロの頭はクラッシュなしで、そのまま入る
        if i == 7 and not last: D.H[b] = D.H[b][:12] + "x.O."                         # 8小節目はフィルのかわりに、ハイハットを開くだけ
    elif n in ("Bメロ", "Bメロ2"):                                                   # ためる。最後は全員止まって、歌だけ
        if last: saw(b, "x.x---.........."); bass(b, "x.x---..........", "11"); strum(GL, b, "x.x---..........", strings=3); strum(GR, b, "x.x---..........", strings=4); D.set(b, "X.X.............", "X.X.............", "................"); continue
        swell(b, "x-------------.." if i < 6 else "x-----x-------.."); bass(b, "x-------x---x-x-" if i < 4 else "x---x---x-x-x-x-", "115d" if i < 4 else "1135wd"); piano(b, "x.......x......." if i < 4 else "x.x.x.x.x.x.x.x.")
        if i == 5: hat_roll(HATR, b, 1)
        if i >= 4: strum(GL, b, "x---------------", strings=3); strum(GR, b, "x-------x-------", strings=4)
        D.set(b, "X.......X......." if i < 4 else "X...X...X...X...", "........X......." if i < 4 else ("....X.......X..." if i < 6 else "X...X...X.X.X.X."), "x...x...x...x..." if i < 6 else "................")
        if i == 6: FXT.bar(b, fx_bar((0, "up", 4)))
    elif n in ("サビ1", "サビ2", "最後のサビ"): chorus(b, i, n)
    elif n == "Cメロ":                                                             # ピアノとベースと歌。5小節目から小さくドラム
        c1 = halves(b)[0]; v = sorted(voice(c1, 62, 3)); PL.bar(b, steps("x---x---x---x---", [N(v[q]) for q in (0, 1, 2, 1)]))
        bass(b, "x-------x---x-x-" if not last else "x-------........", "115d" if not last else "1")
        if i >= 4 and not last: D.set(b, "X.........x.....", "........X.......", "x...x...x...x..."); saw(b, "x---------------")
        if last: D.set(b, "................", "........ooxxXXXX", "................")
    elif n == "ギターの番":                                                         # ギターが歌う（1拍に約1.6音・句は8分のウラから・しゃくりは長い音だけ・ビブラートは最後の1音）
        LEAD.bar(b, G_SOLO[i]); bass(b, *OCT[i % 4]); piano(b, OFF[i % 4]); four(b, i); saw(b, GATE[i % 4]) if i >= 4 else None
        strum(GL, b, "x-------x-------", strings=3); strum(GR, b, "x---------------" if not odd else "x-----x---x-----", strings=4)
        if i in (0, 4): crash(D, b, "C2", 4)
        if i == 3: fill_cresc(D, b, 1)
        if last: saw(b, "x-------........"); D.set(b, "X...X...X...X...", "........x.x.XXXX", "x.x.x.x........."); FXT.bar(b, fx_bar((0, "down", 4)))
    elif n == "落ちサビ":                                                           # ピアノと歌だけ。5小節目からベース
        c1, c2 = halves(b); v = sorted(voice(c1, 62, 3))
        for j in range(3): PN[j].bar(b, steps("x---------------" if not last else "x-------........", [N(v[j])]))
        PL.bar(b, steps("x-------x-------" if not last else "x-------........", [N(low(c1, "E1") + 12)] * 2))
        if i >= 4 and not last: bass(b, "x-------x-------", "15")
        if last: D.set(b, "................", "........x.x.XXXX", "................"); FXT.bar(b, fx_bar((0, "up", 4)))

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の17「放課後タッピング」v4（エレクトロ・ダンスロック・132・ニ短調 → サビはヘ短調 → 最後のサビは嬰ヘ短調）。タッピングのギターの2小節のリフ、"
          "裏で短く切るピアノ、うねるスーパーソウ、合いことば「タッピング」、歌のないドロップ、ギターの番、落ちサビ。自作")
finish(S, LY, V, 0, level={"verse": -0.1}, special={"落ちサビ": -0.5, "Cメロ": -0.4, "最後のサビ": 0.5})

from vt3x_lib import *
path = sys.argv[1]
js = load(path); gtr_velocity(js, "Lギター", 4); gtr_velocity(js, "Rギター", 4); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 16, "chorus": 26, "最後のサビ": 30, "bridge": 14}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ1", 8, None, KF), ("サビ2", 0, None, KF), ("最後のサビ", 0, None, KG)], vol=0.36)
    for sgn in (-1, 1): harmony(path, S, [("最後のサビ", 0, None, KG)], steps=0, vol=0.2, pan=0.6 * sgn, transpose=0.07 * sgn)
    cb = {}                                                                         # ドロップ: 声のチョップ「た・ぴ・ん・ぐ」（奇数小節。タッピングとかけ合う）
    for nm_ in ("ドロップ", "ドロップ2"):
        for i, b in enumerate(S.sc(nm_)):
            t = tones(S.chords[b].split("|")[0], "A4", "F5"); a, c = nm(t[0]), nm(t[-1])
            if i % 2 == 1: cb[b] = [f"{a}:0.5:た {a}:0.25:ぴ {c}:0.25:ん R:0.5 {c}:0.5:ぐ {a}:0.5:た R:1.5", "R:0.5 " + stutter_chop(c, "た", 4, 0.25) + f" {a}:0.5:ぴ {c}:0.5:ん {a}:0.5:ぐ R:1"][(i // 2) % 2]
    chops(path, S, cb, vol=0.36, pan=-0.15)
    voice_by_scene(path, S, {}, default="whisper")
    js = load(path)
    sing_ends(path, S)   # 2026-11-17 人間「歌の余韻とか音程が素人っぽく」: 句の最後の音をのばす・消え方・音程の動きを人の歌に近づける
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    for v in js.get("vocals", []): v["debreathAt"] = [[t + 0.03, 1.2] for t in [60.89, 252.1, 206.34, 249.98, 102.02, 133.61, 106.24, 21.79]]   # 息の点検が言った所だけ、追加で息の音を下げる（2026-11-17。全体の debreath は 0.5 のまま）
    save(path, js)
js = load(path); drum_punch(js); drum_center(js); save(path, js)   # drum_center: 2026-11-18 ドラムを真ん中に寄せる（次の書き出しから効く）
final_gain(path, {"ドロップ": 0.5, "ドロップ2": 1.0, "Aメロ2": -1.0, "Bメロ2": -0.8, "Cメロ": -2.0, "ギターの番": -0.5, "落ちサビ": -1.5, "最後のサビ": 1.8, "おわり": 1.0})   # v4: タッピングひとりの出だしが小さかった・Aメロ2 がサビ1 より大きかった・最後のサビを山に
