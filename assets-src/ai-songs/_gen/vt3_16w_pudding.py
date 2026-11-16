# 16「おやつ宣戦布告」v10（西部の決闘 → なかなおり）。仮。
# 人間（2026-11-16 22:30）:「16.17もう一度作り直そう」→ 方向は「まったく新しい方向で」。D（ファンク・ロック）・E（ポンプするロック）・F（バラード）・v9（パンク）のどれとも違う曲調にする。
# 曲を決める表:
#   形 … 前半と後半で別の曲のように変わる（工程表の決まり）。前半＝砂ぼこりの町の決闘（ホ短調・馬が走るリズム・トランペット）。にらみ合いで全員が止まり、女神の声。後半＝なかなおり（ホ長調・半分の速さ・みんなで「ラララ」）
#   強さ … ファンファーレ 5 → 前奏 7 → A 3（にらみ合い。すき間が主役）→ サビ 8 → A2 4 → サビ2 9 → にらみあい 1 → なかなおりA 4 → ラララ 6 → トランペット 7 → ラララ2 10 → おわり 6
#   旋律の性格 … 前半は短く言い切って、すぐ黙る（西部劇のせりふ）。サビは8分で進んで最後を伸ばす。後半は長い音でゆったり
#   その曲だけの音 … トランペットのファンファーレ（最後に長調でもう一度）、ティンパニの心臓の音、全員が止まる「にらみ合い」
# お手本167曲とくらべて直す所: 歌の休みを多く（Aメロは半分以上休む）／同じリズムの小節をつづけない／ビブラートを深く（サビ 26セント）／ベースは根音だけにしない（走るリズムの中で5度・となりの音）
# 使い方: VB_VOCAL=1 python3 vt3_16w_pudding.py <出力.json>
from vocalo_lib import *
import random as _r

S = Song("16", "pudding", "おやつ宣戦布告（仮）", "Snack War", 152, 4, "E", "minor", "西部の決闘ロック")
S.kit = "naked-x"; S.flags = S.flags + " --bass bnb-loud --space hall --space-wet 0.12"
K = Key("E", "minor"); KE = Key("E", "major"); SC = {4, 6, 7, 9, 11, 0, 2}; SCE = {4, 6, 8, 9, 11, 1, 3}
A_CH = ["Em", "D", "C", "B7", "Em", "D", "C", "B7"]                                   # 根音が下へ1つずつ（ミ→レ→ド→シ）
C_CH = ["Em", "G", "D", "B7", "Em", "G", "A", "B7", "C", "D", "Em", "Em"]
E_CH = ["E", "C#m", "A", "B", "E", "G#m", "A", "B"]
L_CH = ["E", "D", "A", "E", "E", "D", "A", "B"]                                       # 長調の中の D（♭VII）で、西部の空の広さ
S.scene("ファンファーレ", 4, "intro", ["Em", "Em", "C", "B7"])
S.scene("前奏", 4, "intro", A_CH[:4])
S.scene("Aメロ", 8, "verse", A_CH)
S.scene("サビ1", 12, "chorus", C_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("サビ2", 12, "chorus", C_CH)
S.scene("にらみあい", 4, "bridge", ["C", "C", "B7", "B7"])
S.scene("なかなおり", 8, "verse", E_CH)
S.scene("ラララ", 8, "chorus", L_CH)
S.scene("トランペット", 8, "break", E_CH)
S.scene("ラララ2", 12, "chorus", L_CH + ["A", "B", "E", "E"])
S.scene("おわり", 3, "outro", ["E", "D", "E"])
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(1610)

# ================= 歌 =================
AP = ["x.x.x-xx-x--....", "x---x-------....", "..x.x-x.xx-x-...", "x-x-x-------....", "x-xx-x-x-x--....", ".x----x-----....", "x.x-xx.x-x-x-...", "x--x--------...."]      # 短く言って、黙る
AD = ["1 1 3 1 3 5", "4 2", "3 3 5 3 5 6", "5 4 2", "5 5 7 5 7 1'", "7 4", "6 6 5 6 1' 6 5", "#7 2'"]
A1 = ["さんじのかね", "なる", "すなぼこりの", "まちで", "きんのつきが", "よぶ", "となりのおうが", "きた"]
A2 = ["こぶしにぎり", "さあ", "なんどやっても", "あいこ", "つきがぬるむ", "もう", "ゆずれないのさ", "まだ"]
CP = ["x-.x-x-.x-x--x--", ".x------x-----..", "x-x.x-.x--x.x-x-", ".x----------....", "..x.x-x--x--x-x-", "x--x--.x------..", "x-.x.x-xx-x-----", ".x----------....",      # 16分で食う・短く切る・長い音はウラから
      "x-x-x-x-........", "x-x-x-x-........", "x---x---x---x---", "x-----------...."]
CD = ["5 5 7 1' 7 5", "5 7", "2' 2' 1' 7 1' 2' 1'", "#7", "3 5 7 1' 2' 1'", "7 5 7", "1' 1' #6 1' 2' 1'", "2'", "1' 1' 6 5", "7 7 4 7", "5 7 1' 2'", "1'"]
C1 = ["さんじのけっとうだ", "つきはひとつだけ", "ぎんのつるぎをぬけ", "ゆずれぬいくさ", "いちにの", "さんだよ", "ふりむけば"]
C2 = ["さんじのけっとうだ", "あいこがつづくよ", "まんげつわるなんて", "できないふたり", "いちにの", "さんだよ", "またあいこ"]
NP, ND, NT = ["x---x---x---x---", "x---x-------....", "x-x-x-x-x-x-x---", "x-------........"], ["3 3 5 6", "5 3", "2 2 4 5 4 2 4", "5"], ["めがみがきた", "もうひとつあるよ"]
EP = ["x.x---x.x--x----", "x-------x---....", "..x-x---x-x-x---", ".x----------....", "x--x.x---x-x----", "x---x---x---....", "x-x-x---x-x---x-", "x-----------...."]
ED = ["3 3 5 5 6", "5 3", "6 6 1' 6 5", "5", "5 5 1' 1' 2'", "2' 7 5", "6 6 1' 1' 2' 1'", "2'"]
E1 = ["つるぎをおけば", "はるのかぜだ", "つきがふたつある", "わらうふたりだ"]
LP = ["x--x--x-.x-x----", ".x------x-----..", "x--x--x-.x-x----", ".x----------...."] * 2      # 3＋3＋2 のはずみ
LD = ["5 5 6 5 3", "4 2'", "1' 1' 6 1' 6", "5", "5 5 6 5 1'", "2' 4", "6 6 1' 2' 1'", "2'"]
L1 = ["ららららららら", "らららららら", "あすはさかなだ", "またけっとうだ"]
L2 = ["ららららららら", "らららららら", "あすはさかなだ", "またけっとうだ", "ららららららら", "またあした"]
TP_, TD_ = ["x---x---x-x-x---", "x-------x-----..", "x---x---x---x---", "x-----------...."], ["6 6 1' 6 5", "7 2'", "1' 2' 1' 7", "1'"]


def put(name, pats, degs, phrases, key=K, o=4):
    lines, text = song_phrases(pats, degs, phrases); bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ", AP, AD, A1); put("サビ1", CP, CD, C1); put("Aメロ2", AP, AD, A2); put("サビ2", CP, CD, C2); put("にらみあい", NP, ND, NT)
put("なかなおり", EP, ED, E1, key=KE); put("ラララ", LP, LD, L1, key=KE); put("ラララ2", LP + TP_, LD + TD_, L2, key=KE)

# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


def strum(tracks, b, pat, **kw):
    c1, c2 = halves(b)
    if c1 == c2: gtr_strum(tracks, S, b, pat, c1, RNG, **kw)
    else: gtr_strum(tracks, S, b, pat[:8] + "." * 8, c1, RNG, **kw); gtr_strum(tracks, S, b, "." * 8 + pat[8:], c2, RNG, **kw)


def bass(b, pat, kinds, major=False):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), SCE if major else SC))


CLEAN = dict(di="emily", stringNoise=True, amp="jpopClean", ampDrive=0.12, chorus=0, humanPitch=0, noScoop=True, powerChord=False, sustain=1.4, release=0.6)
GFX = [{"type": "filter", "kind": "highpass", "freq": 100, "q": 0.7}, {"type": "eq", "low": -1, "mid": 1, "midHz": 1600, "high": 1}, {"type": "room", "mix": 0.14}]
GR = [S.track(f"Rギター{i + 1}弦め（クリーン）", "distGuitar", volume=0.08, pan=0.5, fx=GFX, **CLEAN) for i in range(6)]
GL = [S.track(f"Lギター{i + 1}弦め（クリーン）", "distGuitar", volume=0.075, pan=-0.5, fx=GFX, **CLEAN) for i in range(6)]
TW = S.track("低いトゥワンギター", "distGuitar", volume=0.13, pan=-0.15, fx=GFX + [{"type": "reverb", "mix": 0.22}], **CLEAN)
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.25))
TP = S.track("トランペット", "brass", patch="trumpet", volume=0.12, pan=0.12, reverb=0.3)
TP2 = S.track("トランペット（下）", "brass", patch="trumpet", volume=0.07, pan=0.3, reverb=0.3)
TIMP = S.track("ティンパニ", "lead", patch="timpani", volume=0.12, pan=-0.2, reverb=0.4)
CLAP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.075, pan=0.05, reverb=0.2, modulate=False)
# 馬が走るリズム（タン・タタ）。キックとフロアは「タン・タタ」、刻みは4分だけ（テンポ152 なので、手数をふやしすぎない）
GAL_K = ["X..xx...X..xx...", "X..xx...X..xx.x.", "X..xx...X..xx...", "X..xx..xX..xx..."]
GAL_B = [("x--xx---x--xx-x-", "1151158"[:7]), ("x--xx---x--xx-x-", "11511wd"), ("x--xx---x--xx-x-", "1153135"), ("x--xx---x-x-x-x-", "1151wda"[:7])]
FAN = ["E4:1.5 G4:0.5 B4:1 E5:1", "D5:0.5 E5:0.5 D5:0.5 B4:0.5 G4:2", "C5:1.5 E5:0.5 G5:1 E5:1", "F#5:3 R:1"]              # ファンファーレ（短調）
FAN2 = ["E4:1.5 G#4:0.5 B4:1 E5:1", "F#5:0.5 E5:0.5 D5:0.5 A4:0.5 F#4:2", "E5:3 R:1"]                                       # 最後（長調）
TP_ANS = {1: "R:2 B4:0.5 D5:0.5 G5:1", 3: "R:1.5 F#5:0.5 D#5:0.5 B4:0.5 F#4:1", 5: "R:2.5 D5:0.5 B4:0.5 D5:0.5", 7: "R:1 B4:0.5 D#5:0.5 F#5:2"}      # サビ: 歌が伸ばしている小節で答える
SOLO = ["E5:1.5 G#5:0.5 B5:1 G#5:1", "G#5:0.5 E5:0.5 C#5:1 E5:2", "C#5:0.5 E5:0.5 A5:1 G#5:0.5 F#5:0.5 E5:1", "F#5:2 D#5:1 R:1",
        "R:0.5 B4:0.5 E5:0.5 G#5:0.5 B5:1.5 G#5:0.5", "B5:1 G#5:0.5 D#5:0.5 B4:2", "A5:0.5 G#5:0.5 F#5:0.5 E5:0.5 C#5:1 E5:1", "F#5:3 R:1"]      # 後半の歌（なかなおり）を、長調で歌い直す


def gallop(b, i, full=True, stop=False):
    if stop:
        bass(b, "x--xx---........", "115"); strum(GR, b, "x---x-x-........", drive=False); strum(GL, b, "x-------........", drive=False); D.set(b, "X..xx...........", "....X...........", "X...x..........."); return
    bass(b, *GAL_B[i % 4]); strum(GR, b, ["x---x-x-x---x-x-", "x---x-x-x-x-x---", "x---x-x-x---x-x-", "x-x-x---x---x-x-"][i % 4], drive=False)
    if full: strum(GL, b, "x-------x-------" if i % 2 == 0 else "x-----x---x-----", drive=False)
    D.set(b, GAL_K[i % 4], "....X.......X..." if i % 4 != 3 else "....X.......X.xx", "X...x...X...x...")


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; r = N(low(halves(b)[0], "E2"))
    if n == "ファンファーレ":                                                       # トランペットひとり → ティンパニのロール → 全員で1発
        TP.bar(b, FAN[i])
        if i >= 2: TIMP.bar(b, "E2:0.5 E2:0.5 E2:0.5 E2:0.5 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25" if i == 2 else "B1:1 R:1 B1:0.5 B1:0.5 B1:0.25 B1:0.25 B1:0.25 B1:0.25")
        if i == 3: strum(GR, b, "x-----------....", drive=False, lag_ms=16); strum(GL, b, "x-----------....", drive=False, lag_ms=16); bass(b, "x-----------....", "1"); D.set(b, "X...............", "X...........xXXX", "................"); crash(D, b, "C2", 6)
    elif n == "前奏":
        gallop(b, i); TW.bar(b, ["E3:1.5 G3:0.5 B3:2", "D3:1.5 F#3:0.5 A3:2", "C3:1.5 E3:0.5 G3:1 E3:1", "B2:2 D#3:1 F#3:1"][i])
        if i == 0: crash(D, b, "C2", 4)
        if last: fill_cresc(D, b, 1)
    elif n in ("Aメロ", "Aメロ2"):                                                   # にらみ合い: ベースと手びょうしと、ときどきギター。歌が黙ると、低いギターが1音だけ答える
        two = n == "Aメロ2"
        if last: bass(b, "x---x---........", "15"); D.set(b, "X.......X.......", "............xXXX" if True else "", "................"); strum(GR, b, "x-------........", drive=False, lag_ms=16); continue
        bass(b, ["x-------x---x-x-", "x-----x-x-------", "x-------x---x-x-", "x---x---x-x-x-x-"][i % 4], ["115d", "115", "113d", "1351wd"][i % 4])
        if not odd: strum(GR, b, "x---------------", drive=False, lag_ms=16)
        else: TW.bar(b, "R:2 " + ["A2:0.5 F#2:0.5 D3:1", "B2:0.5 D#3:0.5 F#3:1", "A2:0.5 D3:0.5 F#3:1", "R:2"][(i // 2) % 4] if i != 7 else "R:4")
        CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if two: D.set(b, "X.......x.X.....", "................", "x...x...x...x..."); strum(GL, b, "x-------x-------" if not odd else "x---------------", drive=False) if i >= 4 else None
        else: D.set(b, "X...............", "................", "....x.......x...")
    elif n in ("サビ1", "サビ2"):
        tag = i >= 8; stop = i == 7                                                 # 8小節目の後ろ2拍は伴奏が休む
        if i in (8, 9):                                                             # 「いち・にの」「さんだよ」: 全員で頭だけ打って、あとは歌だけ
            strum(GR, b, "x---x---........", drive=False); strum(GL, b, "x---x---........", drive=False); bass(b, "x---x---........", "11"); D.set(b, "X...X...........", "X...X...........", "................"); TIMP.bar(b, f"{'C2' if i == 8 else 'D2'}:1 {'C2' if i == 8 else 'D2'}:1 R:2"); continue
        gallop(b, i, stop=stop)
        if i in TP_ANS and not stop: TP.bar(b, TP_ANS[i])
        if i == 7: TP.bar(b, "R:2 B4:0.5 D#5:0.5 F#5:1")
        if n == "サビ2" and not stop: CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i in (0, 4, 10): crash(D, b, "C2", 4)
        if i == 7: fill_cresc(D, b, 2)
        if i == 10: TP.bar(b, "E5:1 D5:0.5 B4:0.5 G4:1 B4:1"); TP2.bar(b, "B4:1 B4:0.5 G4:0.5 E4:1 G4:1")
        if last: TP.bar(b, "E5:3 R:1"); TP2.bar(b, "B4:3 R:1"); D.set(b, GAL_K[0], "....X.......XXXX", "X...x...X...x...") if n == "サビ1" else D.set(b, "X..xx...X.......", "....X...X.......", "X...x...X.......")
    elif n == "にらみあい":                                                         # 全員が止まる。ティンパニの心臓の音と、ささやく歌だけ
        TIMP.bar(b, "E2:1 R:1 E2:0.5 E2:0.5 R:1" if i < 2 else ("B1:1 R:1 B1:0.5 B1:0.5 R:1" if i == 2 else "B1:1 R:3"))
        if i == 0: strum(GR, b, "x---------------", drive=False, lag_ms=20)
        if i == 2: strum(GL, b, "x---------------", drive=False, lag_ms=20)
    elif n == "なかなおり":                                                         # 半分の速さ。長調。ベースが歩き、ギターはのばす
        bass(b, ["x-------x---x-x-", "x---x---x-----x-", "x-------x-x-x-x-", "x---x---x---x-x-"][i % 4], ["115d", "1353", "11wda"[:5], "1351d"][i % 4], major=True)
        strum(GR, b, "x-------x---x---" if not odd else "x-----x---------", drive=False, lag_ms=14); strum(GL, b, "x---------------", drive=False, lag_ms=14) if i >= 4 else None
        D.set(b, "X.........x.....", "........X.......", "x...x...x...x..." if i < 4 else "x.x.x.x.x.x.x.x.")
        if i == 0: crash(D, b, "C2", 6)
        if last: fill_cresc(D, b, 2)
    elif n in ("ラララ", "ラララ2", "トランペット"):
        big = n == "ラララ2"; tp = n == "トランペット"; stop = (n == "ラララ" and last) or (big and i == 7)
        if stop: bass(b, "x---x---........", "13", major=True); strum(GR, b, "x-------........", drive=False); strum(GL, b, "x-------........", drive=False); D.set(b, "X.......X.......", "........X.......", "x.x.x.x........."); fill_cresc(D, b, 2); continue
        bass(b, *[("x-----x-x---x-x-", "1135d"), ("x---x---x-x-x-x-", "1351wd"), ("x-----x-x-x---x-", "1123d"), ("x---x-x-x---x-x-", "11875a"[:6])][i % 4], major=True)
        strum(GR, b, ["x---x-x-x---x-x-", "x---x-x-x-x-x---"][i % 2], drive=False); strum(GL, b, "x-------x-------" if not odd else "x-----x---x-----", drive=False)
        D.set(b, "X.....x...x....." if not odd else "X.........x..x..", "........X.......", "X.x.X.x.X.x.X.x." if not big else "X.x.X.xxX.x.X.x."); CLAP.bar(b, "R:2 B4:1 R:1" if not big else "R:1 B4:1 R:1 B4:1")
        if tp: TP.bar(b, SOLO[i])
        if tp and i >= 4: TP2.bar(b, ["R:0.5 G#4:0.5 B4:0.5 E5:0.5 G#5:1.5 E5:0.5", "G#5:1 E5:0.5 B4:0.5 G#4:2", "C#5:0.5 B4:0.5 A4:0.5 A4:0.5 A4:1 C#5:1", "D#5:3 R:1"][i - 4])
        if big and (LP + TP_)[i] in ("x-------x-----..", "x-----------....") and i < 11: TP.bar(b, ["R:2 B4:0.5 E5:0.5 G#5:1", "R:1.5 F#5:0.5 A5:1 F#5:1", "R:2 E5:0.5 G#5:0.5 B5:1", "R:1 F#5:1 D#5:1 B4:1"][(i // 2) % 4])
        if i % 4 == 0: crash(D, b, "C2", 6)
        if i % 4 == 3 and not last: fill_cresc(D, b, 1)
        if big and last: D.set(b, "X...............", "X...............", "................"); bass(b, "x---------------", "1", major=True)
    elif n == "おわり":                                                            # ファンファーレを、長調でもう一度。最後は全員で1発
        TP.bar(b, FAN2[i]); TP2.bar(b, ["R:4", "D5:0.5 B4:0.5 A4:0.5 F#4:0.5 D4:2", "B4:3 R:1"][i])
        if i == 1: TIMP.bar(b, "D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.25 D2:0.25 D2:0.25 D2:0.25 D2:0.25 D2:0.25 D2:0.25 D2:0.25"); strum(GR, b, "x---------------", drive=False, lag_ms=16)
        if i == 2: strum(GR, b, "x-----------....", drive=False, lag_ms=18); strum(GL, b, "x-----------....", drive=False, lag_ms=18); bass(b, "x-----------....", "1", major=True); TIMP.bar(b, "E2:3 R:1"); D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の16「おやつ宣戦布告」v10（西部の決闘ロック・152・ホ短調 → 後半はホ長調で半分の速さ）。プリンの取り合いを、砂ぼこりの町の決闘に見立てる。"
          "トランペットのファンファーレ、馬が走るリズム、全員が止まるにらみ合い、最後はみんなでラララ。自作")
finish(S, LY, V, 0, level={"verse": -0.1}, special={"にらみあい": -0.6, "ラララ2": 0.5, "ファンファーレ": 0.2})

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=88, down=10, up=10, seed=16)
js = load(path); gtr_velocity(js, "Lギター", 3); gtr_velocity(js, "Rギター", 4); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 10, "chorus": 26, "ラララ2": 28, "bridge": 6}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K), ("ラララ", 4, None, KE), ("ラララ2", 0, None, KE)], vol=0.36)
    for sgn in (-1, 1): harmony(path, S, [("ラララ2", 0, None, KE)], steps=0, vol=0.2, pan=0.6 * sgn, transpose=0.07 * sgn)
    voice_by_scene(path, S, {"にらみあい": "whisper", "なかなおり": "cute"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
final_gain(path, {"ファンファーレ": 7.0, "Aメロ2": -0.8, "なかなおり": -1.5, "ラララ": -0.4, "ラララ2": 1.8, "おわり": 6.0})   # v10: トランペットひとりの出だしと終わりが小さかった・なかなおりの入りが大きすぎた・最後のラララが1回目より小さかった
