# 16「おやつ宣戦布告」v11（高速ボカロック）。仮。
# 人間（2026-11-16 23:31）:「16から17ボカロ感強めで1から作り直しましょう。4から5分の曲でお願いします。」
# ボカロ感として入れるもの（docs/sound/vocaloid-study.md）:
#   速い4つ打ちのロック（176）／1〜2小節のリフ（ラとミの5度の行き来）が曲を引っぱる／Aメロの前半は1つの和音だけ／丸サ進行（IV△7→III7→VIm7→Vm7・I7）
#   サビで短3度上へ転調（イ短調 → ハ短調）、最後のサビはさらに半音上（嬰ハ短調）／跳ぶ旋律（5度・6度）／決めのリズム（16分＋16分休み＋4分）
#   リリースカットピアノ（短く切って刻む）／キメ（全員で同じリズム）と1拍の止め／落ちサビ／うねるスーパーソウと、駆け上がるプラック
# 曲を決める表:
#   形 … リフ（1小節目から全員）→ A（1つの和音）→ A'（丸サ）→ B（半分の速さ。最後は全員止まって「な・い」）→ サビ（転調）→ リフ → A2 → B2 → サビ2 → 間奏（リフを音色を変えて育てる）→ Cメロ（半分の速さ。女神）→ 落ちサビ（ピアノと歌）→ 最後のサビ（半音上・2回）→ リフで止まる
#   強さ … 前奏 4→8 → A 5 → A' 6 → B 4 → サビ 9 → A2 6 → B2 4 → サビ2 9.5 → 間奏 8 → C 3→5 → 落ち 2 → 最後 10 → おわり 8
#   旋律の性格 … Aメロは8分で言葉を詰め、5度で跳ぶ。句の最後は「16分＋休み＋4分」で言い切る。サビは跳んで上がり、長い音はウラから
# 長さ: 4分20秒ほど（人間の指定: 4〜5分）。
# 使い方: VB_VOCAL=1 python3 vt3_16v_pudding.py <出力.json>
from vocalo_lib import *
import random as _r, re as _re

S = Song("16", "pudding", "おやつ宣戦布告（仮）", "Snack War", 176, 4, "A", "minor", "高速ボカロック")
S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock --piano salamander " + S.flags
K = Key("A", "minor"); KC = Key("C", "minor"); KD = Key("C#", "minor"); SC = {9, 11, 0, 2, 4, 5, 7}; SCC = {0, 2, 3, 5, 7, 8, 10}; SCD = {1, 3, 4, 6, 8, 9, 11}
MARU = ["Fmaj7", "E7", "Am7", "Gm7|C7"]
A_CH = ["Am7"] * 8 + MARU * 2
B_CH = ["Dm7", "Em7", "Fmaj7", "G", "Dm7", "Em7", "Fmaj7", "G7"]
C_CH = ["Abmaj7", "G7", "Cm7", "Bbm7|Eb7"] * 3 + ["Abmaj7", "Bb", "Cm", "Cm"]
D_CH = ["Amaj7", "G#7", "C#m7", "Bm7|E7"] * 3 + ["Amaj7", "B", "C#m", "C#m"]
M_CH = ["Fmaj7", "G", "Em7", "Am7", "Fmaj7", "G", "E7", "E7"]
S.scene("前奏", 8, "intro", ["Am7"] * 8)
S.scene("Aメロ", 16, "verse", A_CH)
S.scene("Bメロ", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("リフ", 8, "break", ["Am7"] * 8)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("間奏", 16, "solo", ["Am7"] * 8 + MARU * 2)
S.scene("Cメロ", 16, "bridge", M_CH * 2)
S.scene("落ちサビ", 8, "chorus", C_CH[:8])
S.scene("最後のサビ", 32, "chorus", D_CH * 2)
S.scene("おわり", 12, "outro", ["C#m7"] * 12)
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(1611)

# ================= 歌 =================
Aa, Aa2 = "x.x-x.x-x-x.x.x-", "x-x-x-x.x---...."          # 8分で詰めて、最後は「16分＋休み＋4分」
Ab, Ab2 = "..x-x-x-x-x-x-x-", "x-x---x-----...."
Ac, Ac2 = "x-x-x-x-x-xxx-x-", "x---x---x---...."
Ad, Ad2 = "..x.x-x.x-x-x.x-", "x-x-x-x.x---...."
AP = [Aa, Aa2, Ab, Ab2, Ac, Ac2, Ad, Ad2] * 2
AD = ["1 5 1 5 4 3 1 3", "4 3 1 7, 1", "5, 1 3 5 3 1 3", "4 3 1", "1 3 5 3 5 6 5 3 1", "3 2 1", "3 5 6 5 3 1 3", "4 3 1 #7, 1",
      "1 5 1 5 4 3 1 3", "4 2 #7, 2 #7,", "5, 1 3 5 3 1 3", "4 3 2", "1 3 5 3 5 6 5 3 1", "4 2 #7,", "3 5 6 5 3 1 3", "4 3 1 b7, 1"]
A1 = ["さんじのかねなるだいどころ", "しろいとびらのおくに", "きんいろつきひとつねむる", "せなかにけはいおうがきた",
      "めとめがあえばさひばなちる", "ぎんのつるぎをぬいた", "ゆずれないゆずれぬいくさ", "とろけるまえにきめようか"]
A2 = ["こぶしにぎりしめいざしょうぶ", "ぐーちょきぱーであいこ", "なんどやってもおなじかたち", "かがみあわせのふたりだね",
      "つきがぬるんでくいそがなきゃ", "まんげつをわるなんて", "わけあうなんていやぜんぶ", "ほしいとさけぶさんじだよ"]
BP_ = ["x---x---x-x-x---", "x-------x-----..", "x---x-x-x---x---", "x-----------....", "x---x---x-x-x---", "x-------x-----..", "x-x-x-x-x-x-x-x-", "x.x---.........."]
BD = ["4 4 6 5 4", "2 5", "3 3 5 6 5", "4", "4 4 6 5 4", "2 5", "3 3 5 5 6 6 5 5", "4 6"]
B1 = ["ゆずれぬひかり", "ゆらめいてる", "だれにもこれは", "わたさないわたさない"]
B2 = ["にらみあうまま", "うごけないよ", "だれにもこれは", "わたさないわたさない"]
Ca, Ca2, Cb, Cb2, Cc, Cc2, Cd, Cd2 = "x-x-x---x-x-x---", "x-x-x-x.x---....", "..x-x-x-x---x-x-", ".x------x-----..", "x-x-x---x-x-x-x-", "x---x---x.x---..", "..x-x-x-x-x-x-x-", ".x----------...."
CP = [Ca, Ca2, Cb, Cb2, Cc, Cc2, Cd, Cd2] * 2
CD = ["5 1' 5 1' 3' 2'", "2' 2' 1' #7 2'", "3' 3' 2' 1' 7 1'", "4' 3'", "1' 3' 1' 3' 4' 3' 1'", "2' 2' #7 2'", "5 7 1' 3' 2' 1' 7", "7",
      "5 1' 5 1' 3' 2'", "2' 2' 1' #7 2'", "3' 3' 2' 1' 7 1'", "4' 3'", "1' 3' 1' 3' 4' 3' 1'", "2' 2' 7 2'", "5 7 1' 3' 2' 1' 7", "1'"]
C1 = ["いくさのかねなりひびく", "つきはひとつだけ", "ぎんのつるぎをかかげて", "ゆずれぬさんじだ", "となりのおうにらんでる", "ひくにひけないね", "とろけるまえにきめるよ", "せんせんふこくだ"]
C2 = C1[:4] + ["かがみのなかおなじかお", "わらいそうになる", "それでもつきはひとつだ", "せんせんふこくだ"]
C3 = ["やさしいかねなりひびく", "つきはふたつある", "ぎんのつるぎをおろして", "わらいあうさんじ", "となりのおうてをふるよ", "おなじはなうただ", "あしたのつきはさかなだ", "またあおうさんじ"]
C4 = C3[:7] + ["せんせんふこくだ"]
MP = ["x---x---x-x-x---", "x-------x---....", "..x-x---x-x-x---", "x-----------...."] * 4
MD = ["3 3 5 6 5", "4 2", "2 2 5 4 2", "1", "6 6 5 3 5", "4 5", "#7, #7, 2 4 2", "5"] * 2
M1 = ["そこへめがみが", "おりてきたよ", "もうひとつある", "ほほえんだよ", "つるぎをおけば", "かぜがふいた", "おなじかおして", "ふきだしたよ"]


def put(name, pats, degs, phrases, key=K, o=4):
    lines, text = song_phrases(pats, degs, phrases); bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ", AP, AD, A1); put("Bメロ", BP_, BD, B1); put("サビ1", CP, CD, C1, key=KC); put("Aメロ2", AP, AD, A2); put("Bメロ2", BP_, BD, B2); put("サビ2", CP, CD, C2, key=KC)
put("Cメロ", MP, MD, M1); put("落ちサビ", CP[:8], CD[:8], C3[:4], key=KC); put("最後のサビ", CP + CP, CD + CD, C3 + C4, key=KD)

# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


def scale(b): n = S.scene_of(b)[0]; return SCD if n in ("最後のサビ", "おわり") else SCC if n in ("サビ1", "サビ2", "落ちサビ") else SC


def strum(tracks, b, pat, **kw):
    c1, c2 = halves(b)
    if c1 == c2: gtr_strum(tracks, S, b, pat, c1, RNG, **kw)
    else: gtr_strum(tracks, S, b, pat[:8] + "." * 8, c1, RNG, **kw); gtr_strum(tracks, S, b, "." * 8 + pat[8:], c2, RNG, **kw)


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), scale(b), lo=28))


def shift(s, n): return " ".join(x if x.startswith("R") else _re.sub(r"^[A-G][#b]?\d", lambda m: nm(midi(m.group(0)) + n), x) for x in s.split())


def piano(b, pat, short=0.2, center=64):
    c1, c2 = halves(b)
    if c1 == c2: rows = relcut(PN, c1, pat, center=center, short=short)
    else: r1, r2 = relcut(PN, c1, pat[:8], center=center, short=short), relcut(PN, c2, pat[8:], center=center, short=short); rows = [a + " " + c for a, c in zip(r1, r2)]
    for t, r in zip(PN, rows): t.bar(b, r)


def saw(b, pat):
    c1, c2 = halves(b); v, v2 = wide9(c1), wide9(c2)
    for j in range(5): SAW[j].bar(b, steps(pat, [N(v[j])]) if c1 == c2 else steps(pat[:8], [N(v[j])]) + " " + steps(pat[8:], [N(v2[j])]))


PN = [S.track(f"ピアノ（短く切る{i + 1}）", "piano", volume=0.085, pan=-0.2 + 0.2 * i, reverb=0.15, sustain=0.5) for i in range(3)]
PR = S.track("ピアノ（リフ）", "piano", volume=0.15, pan=-0.1, reverb=0.2, sustain=0.9)
PR2 = S.track("ピアノ（リフの下）", "piano", volume=0.1, pan=0.1, reverb=0.2, sustain=0.9)
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.042, -0.6, drive=0.4)) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.04, 0.6, drive=0.35)) for i in range(6)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.25))
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.024, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.6, fx=rack_supersaw()) for i in range(5)]
PLK = S.track("駆け上がるプラック", "lead", patch="kfbSquarePluck", volume=0.05, pan=0.3, reverb=0.25, fx=rack_pluck())
SQ = S.track("リフのシンセ", "lead", patch="kfbSquareLead", volume=0.05, pan=0.25, reverb=0.15)
# v13（2026-11-17 人間「もっと寄せようか」＝Kawaii future bass に）: 間奏の後半を Kawaii future bass のドロップに・Bメロに「ポワン」とふくらむ和音・サビにきらきらとハイハットのロール・声のチョップ
SWELL = [S.track(f"ふくらむスーパーソウ{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.035, pan=-0.4 + 0.4 * i, reverb=0.3) for i in range(3)]
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
KGATE = ["x-----x-x-..x-x-", "x-x-x-..x-x-.x-.", "x-x-..x-..x-x-x-", "x-.x-.x-x-.x-.x-", "x-----x-----x-x-", "x-x-x-..x-x-.x-.", "x-.x-.x-....x-x-", "x-x-x-x-........"]
CLAP = S.track("クラップ", "guitar", patch="kawaiiFx", volume=0.07, pan=0.05, reverb=0.15, modulate=False)


def swell(b, pat="x-------------.."):
    v = sorted(voice(halves(b)[0], 66, 3))
    for j in range(3): SWELL[j].bar(b, steps(pat, [N(v[j])]))
FXT = S.track("効果音", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.2, modulate=False)

RIFF = ["A4:0.5 E5:0.5 A4:0.25 C5:0.25 E5:0.5 D5:0.5 C5:0.25 A4:0.25 G4:0.5 A4:0.5", "A4:0.5 E5:0.5 A4:0.25 C5:0.25 E5:0.5 G5:0.75 E5:0.25 D5:0.5 C5:0.5"]      # ラとミの5度の行き来
RIFFB = [("x-x-.xx-x-x-x-x-", "11511578"[:8]), ("x-x-.xx-x---x-x-", "1151187")]                                                    # リフの下で動くベース
WB = [("x---x-x---x-x-x-", "1155wd"), ("x-x---x-----x-x-", "1135d"), ("x---x-x-x---x-x-", "11235d"), ("x-x---x---x-x-x-", "11875a"),
      ("x---x-x---x-x-x-", "1535wd"), ("x-x---x-----x-x-", "1151d"), ("x-x-x-x---x---x-", "12345d"), ("x---x-x-x---x-x-", "1132wd")]
EIGHT = ("x-x-x-x-x-x-x-x-", "11115151")
PCUT = ["x.x.x.x.x.x.x.x.", "x.x.xx.x.x.xx.x.", "x.x.x.x.xx.x.x.x", "xx.x.x.xx.x.x.x."]                                           # 短く切るピアノの刻み
GATE = ["x---x-x---x-x-x-", "x-x---x-----x-x-", "x---x-x-x-x-x---", "x-x---x---x-x---"]


def riff(b, i, up=0, pno=True, sq=False, low=True):
    r = shift(RIFF[i % 2], up)
    if pno: PR.bar(b, r)
    if pno and low: PR2.bar(b, shift(r, -12))
    if sq: SQ.bar(b, shift(r, 12))


def chorus(b, i, n):
    big = n == "最後のサビ"; j = i % 16; stop = j == 7 or (j == 15 and not (big and i == 31))      # 8小節ごとに、後ろの2拍は伴奏が休む（歌の長い音とフィルだけ）
    if stop:
        saw(b, "x-------........"); bass(b, "x---x-x-........", "135"); strum(GL, b, "x-------........", strings=3); strum(GR, b, "x-------........", strings=4); piano(b, "x.x.x.x.........")
        D.set(b, "X...X...........", "....X...........", "x.x.x.x........."); fill_cresc(D, b, 2); return
    saw(b, GATE[(i + (2 if n == "サビ2" else 0)) % 4]); bass(b, *WB[(i + (3 if n == "サビ2" else 0)) % 8]); piano(b, PCUT[i % 4])
    strum(GL, b, "x-------x-------" if i % 2 == 0 else "x-----x---------", strings=3); strum(GR, b, "x---------------" if i % 2 == 0 else "x-----x---x-----", strings=4)
    feel(D, b, "four" if j % 4 != 3 else "upbeat8"); CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
    if CP[j] in (Cb2, Cd2): PLK.bar(b, "R:2 " + arp16(halves(b)[1], "xxxxxxxx", (0, 1, 2, 3, 4, 5, 6, 7), lo="C5", hi="C7")); FXT.bar(b, fx_bar((1, "kira", 1)))      # 歌が伸ばしている後ろで、プラックが駆け上がる
    if j % 8 == 3: hat_roll(HATR, b, 0.5)
    if j % 8 == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
    if j % 4 == 3: fill_cresc(D, b, 1)
    if big and i == 31: saw(b, "x---------------"); D.set(b, "X.........X.X...", "........X...X.XX", "X.x.X.x.........")


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "前奏":                                                                # 1小節目から全員でリフ（お手本167曲でいちばん多い始まり方: 全員いっしょに1小節目から 42%。ロックは 46%）
        # ドラムの入り方（この曲。人間 2026-11-17「ドラムの始まり方いつも同じだよなー」）: 前ぶれなしで、頭から4つ打ち。フィルもクラッシュも使わない。5小節目からシンセがリフに重なる
        riff(b, i, sq=i >= 4); bass(b, *RIFFB[i % 2]); strum(GL, b, "x-------x-------", strings=3); strum(GR, b, "x-----x---x-----" if odd else "x---------------", strings=4); feel(D, b, "four")
        if last: D.set(b, "X...X...X.X.....", "....X.....X.X...", "x.x.x.x.x......."); bass(b, "x-x-.xx-x-x-....", "115118")
    elif n in ("リフ", "おわり"):
        up = 4 if n == "おわり" else 0
        if n == "おわり" and last:                                                   # リフの途中（3拍目）で全員止まる
            PR.bar(b, shift("A4:0.5 E5:0.5 A4:0.25 C5:0.25 E5:0.5 A5:1 R:1", up)); BASS.bar(b, shift("A1:0.5 A1:0.5 E2:0.5 A2:0.5 A2:1 R:1", up)); strum(GL, b, "x-------x---....", strings=3); strum(GR, b, "x-------x---....", strings=4)
            D.set(b, "X...X...X.......", "....X...X.......", "x.x.x.x.x......."); continue
        riff(b, i, up=up, sq=True); BASS.bar(b, shift(walk_bass(RIFFB[i % 2][0], RIFFB[i % 2][1], "Am7", "Am7", "Am7", SC, lo=28), up))
        strum(GL, b, "x-------x-------", strings=3); strum(GR, b, "x-----x---x-----" if odd else "x---------------", strings=4); feel(D, b, "four"); CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i == 0 and n == "おわり": crash(D, b, "C2", 4)
        if n == "リフ" and i < 2: D.set(b, "X...X...X...X...", "................", "................")      # サビのあとのリフ: キックだけに落として、3小節目から戻る
        if n == "リフ" and last: D.set(b, "X...X...X...X...", "....X.......X...", "x.x.x.x.x.x.O...")
        if n == "おわり" and i in (3, 7): fill_cresc(D, b, 1)
        if i == 4: crash(D, b, "C2", 4)
    elif n in ("Aメロ", "Aメロ2"):
        two = n == "Aメロ2"; first = i < 8; stop = i == 15                             # 前半は1つの和音。ピアノのリフが小さく続き、ベースが動く
        if stop: bass(b, "x---x---........", "15"); piano(b, "x.x.x.x........."); strum(GL, b, "x-------........", strings=3); D.set(b, "X...X...........", "....X...........", "x.x.x.x........."); fill_cresc(D, b, 2); continue
        if first:
            bass(b, *RIFFB[i % 2]) if two else bass(b, *EIGHT)
            if AP[i] in (Aa2, Ab2, Ac2, Ad2): PR.bar(b, "R:2 " + ["E5:0.5 D5:0.5 C5:0.25 A4:0.25 G4:0.5", "A4:0.25 C5:0.25 E5:0.5 G5:0.5 E5:0.5"][(i // 2) % 2])      # 歌の句の終わりに、リフのかけらが答える
            if two: piano(b, PCUT[i % 4]); strum(GR, b, "x---------------", strings=3) if not odd else None
            feel(D, b, "quarter" if not two else "rock8", k=["X.....x.X.......", "X.....x.X.x....."][i % 2])      # テンポ176: 刻みは4分から（手数をふやしすぎない）
        else:
            bass(b, *WB[(i + (4 if two else 0)) % 8]); piano(b, PCUT[i % 4]); strum(GL, b, "x-------x-------" if not odd else "x---------------", strings=3)
            if two: strum(GR, b, "x-----x---x-----" if odd else "x---------------", strings=4)
            feel(D, b, "four" if two else "rock8b")
        if two and i < 2: D.set(b, "................", "................", "x...x...x...x..." if i == 0 else "x...x...x.x.x.xx")      # Aメロ2: ドラムは2小節おくれて入る（はじめはハイハットだけ）
        if (i == 0 and not two) or i == 8: crash(D, b, "C2", 4)
        if i == 7: fill_cresc(D, b, 1, toms=True) if two else D.set(b, D.K[b], D.S[b][:12] + "X.X.", D.H[b][:12] + "....")
    elif n in ("Bメロ", "Bメロ2"):                                                   # 半分の速さ。和音がのびる。最後は全員止まって、歌だけ「な・い」
        if last:
            saw(b, "x.x---.........."); bass(b, "x.x---..........", "11"); strum(GL, b, "x.x---..........", strings=3); strum(GR, b, "x.x---..........", strings=4); D.set(b, "X.X.............", "X.X.............", "................"); continue
        swell(b, "x-------------.." if i < 6 else "x-----x-------.."); bass(b, "x-------x---x-x-" if i < 4 else "x---x---x-x-x-x-", "115d" if i < 4 else "1135wd"); piano(b, "x.......x......." if i < 4 else "x.x.x.x.x.x.x.x.", center=67)
        if i == 5: hat_roll(HATR, b, 1)
        if i >= 4: strum(GL, b, "x---------------", strings=3); strum(GR, b, "x-------x-------", strings=4)
        D.set(b, "X.......X......." if i < 4 else "X...X...X...X...", "........X......." if i < 4 else ("....X.......X..." if i < 6 else "X...X...X.X.X.X."), "X...x...X...x..." if i < 6 else "................")
        if i == 6: FXT.bar(b, fx_bar((0, "up", 4)))
    elif n in ("サビ1", "サビ2", "最後のサビ"): chorus(b, i, n)
    elif n == "間奏":                                                              # リフを育てる: シンセ → ピアノとシンセ → 丸サの上でプラック
        if i < 8:
            riff(b, i, pno=i >= 4, sq=True); bass(b, *RIFFB[i % 2]); feel(D, b, "break" if i < 4 else "four"); strum(GL, b, "x-------x-------", strings=3) if i >= 4 else None; strum(GR, b, "x---------------", strings=4) if i >= 4 else None
            if i in (0, 4): crash(D, b, "C2", 4)
            if i == 3: fill_cresc(D, b, 1)
        else:
            # Kawaii future bass のドロップ: 半分の速さ／スーパーソウが小節ごとに違う型で切れてポンプ／ベースも同じ型／3拍目にクラップ／偶数小節はシンセのリード、奇数小節は声のチョップとプラック（かけ合い）
            q = i - 8; g = KGATE[q]; saw(b, g); c1, c2 = halves(b); r = low(c1, "E1"); BASS.bar(b, steps(g, [N(r + (12 if x % 5 == 4 else 0)) for x in range(onsets(g))]))
            t = [N(m) for m in tones(c1, "A5", "A6")]
            if not odd: SQ.bar(b, steps("x-x-x---........", [t[-1], t[1 % len(t)], t[0]]))
            else: PLK.bar(b, "R:2 " + arp16(c1, "xxxxxxxx", (0, 1, 2, 3, 4, 5, 6, 7), lo="A4", hi="A6")); FXT.bar(b, fx_bar((3, "kira" if q % 4 == 1 else "pyon", 1)))
            strum(GL, b, "x---------------", strings=3); feel(D, b, "half" if q % 4 != 3 else "halfopen"); CLAP.bar(b, "R:2 B4:1 R:1")
            if q == 0: FXT.bar(b, fx_bar((0, "impact", 2), (0, "sub", 2))); crash(D, b, "C2", 4)
            if q in (3,): hat_roll(HATR, b, 0.5)
            if last: saw(b, "x-------........"); BASS.bar(b, steps("x-------........", [N(r)])); D.set(b, "X.........x.....", "........X...x.XX", "X.x.X.x........."); hat_roll(HATR, b, 1); FXT.bar(b, fx_bar((0, "down", 4)))
    elif n == "Cメロ":                                                             # 半分の速さ。前半はピアノとベースだけ、後半でドラムと弦のかわりのスーパーソウ
        late = i >= 8; c1 = halves(b)[0]; v = sorted(voice(c1, 62, 3))
        PR.bar(b, steps(["x---x---x---x---", "x---x-x-x---x---"][i % 2], [N(v[q]) for q in ((0, 1, 2, 1) if not odd else (0, 1, 2, 1, 2))])); PR2.bar(b, steps("x-------x-------", [N(low(c1, "E1") + 12)] * 2))
        bass(b, "x-------x---x-x-" if not last else "x-------........", "115d" if not last else "1") if i >= 4 else None
        if late and not last: saw(b, "x---------------" if not odd else "x-------x-------"); D.set(b, "X.........x.....", "........X.......", "x...x...x...x...")
        if last: D.set(b, "................", "........ooxxXXXX", "................")
    elif n == "落ちサビ":                                                           # ピアノと歌だけ（短く切らず、のばす）。5小節目からベース
        c1, c2 = halves(b); v, v2 = sorted(voice(c1, 62, 3)), sorted(voice(c2, 62, 3))
        for j in range(3): PN[j].bar(b, steps("x-------x-------" if not last else "x-------........", [N(v[j]), N(v2[j])]))
        PR2.bar(b, steps("x-------x-------" if not last else "x-------........", [N(low(c1, "E1") + 12), N(low(c2, "E1") + 12)]))
        if i >= 4 and not last: bass(b, "x-------x-------", "11")
        if last: D.set(b, "................", "........x.x.XXXX", "................"); FXT.bar(b, fx_bar((0, "up", 4)))

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の16「おやつ宣戦布告」v11（高速ボカロック・176・イ短調 → サビはハ短調 → 最後のサビは嬰ハ短調）。ピアノのリフ（5度の行き来）、丸サ進行、"
          "短く切るピアノ、決めのリズム、全員が止まる「な・い」、落ちサビ、うねるスーパーソウと駆け上がるプラック。自作")
finish(S, LY, V, 0, level={"verse": -0.1}, special={"落ちサビ": -0.5, "Cメロ": -0.3, "最後のサビ": 0.5})

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=88, down=10, up=10, seed=16)
js = load(path); gtr_velocity(js, "Lギター", 3); gtr_velocity(js, "Rギター", 4); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 16, "chorus": 26, "最後のサビ": 30, "bridge": 14}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ1", 8, None, KC), ("サビ2", 0, None, KC), ("最後のサビ", 0, None, KD)], vol=0.36)
    for sgn in (-1, 1): harmony(path, S, [("最後のサビ", 0, None, KD)], steps=0, vol=0.2, pan=0.6 * sgn, transpose=0.07 * sgn)
    cb = {}                                                                         # 間奏の後半: 声のチョップ「つ・き」（奇数小節。シンセのリードとかけ合う）
    for q, b in enumerate(S.sc("間奏")[8:15]):
        t = tones(S.chords[b].split("|")[0], "A4", "F5"); a, c = nm(t[0]), nm(t[-1])
        if q % 2 == 1: cb[b] = [f"{a}:0.5:つ {a}:0.25:き {c}:0.25:つ R:0.5 {c}:0.5:き {a}:0.5:つ R:1.5", "R:0.5 " + stutter_chop(c, "つ", 4, 0.25) + f" {a}:0.5:き {c}:0.5:つ {a}:0.5:き R:1"][(q // 2) % 2]
    chops(path, S, cb, vol=0.36, pan=-0.15)
    voice_by_scene(path, S, {}, default="cute")
    js = load(path)
    sing_ends(path, S)   # 2026-11-17 人間「歌の余韻とか音程が素人っぽく」: 句の最後の音をのばす・消え方・音程の動きを人の歌に近づける
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    for v in js.get("vocals", []): v["debreathAt"] = [[t + 0.03, 1.2] for t in [188.29, 17.24, 62.19, 210.11, 177.4, 46.47, 57.35, 111.93, 11.07, 176.57]]   # 息の点検が言った所だけ、追加で息の音を下げる（2026-11-17。全体の debreath は 0.5 のまま）
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
final_gain(path, {"前奏": 4.2, "リフ": 2.0, "間奏": 1.3, "サビ1": 0.5, "サビ2": 0.8, "Cメロ": -4.5, "落ちサビ": -5.0, "最後のサビ": 2.2, "おわり": 2.5})   # v11: ピアノだけの Cメロ・落ちサビがサビより大きかった・前奏が小さかった・最後のサビを山に
