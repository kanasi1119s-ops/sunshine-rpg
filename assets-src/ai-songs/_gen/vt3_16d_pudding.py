# 16「おやつ宣戦布告」D版（はねるファンク・ロック）。仮。
# 人間（2026-11-16）: スケッチ D・E・F を「全部」1曲に仕上げる。分析ソフト（段2）で分かった3つを直して作る:
#   ① ベース: 根音を置くだけにしない（歩く・つなぎの音）  ② コード: 根音が4度5度ばかりで動かない（となり・3度・♭II）  ③ 歌: 2小節の型をくり返さない（小節ごとにリズムを書く）
# 曲を決める表:
#   形 … ベースひとりで始まる → いくさ（A・B・サビ）×2 → 雪どけ（ドラムが休み、手びょうしと歌）→ 小さいサビ → 最後のサビ → リフの途中で、ぷつっと止まる
#   強さ … ベース 3 → 前奏 6 → A 5 → B 4（最後の1拍は全員休み）→ サビ 8 → A2 6 → B2 4 → サビ2 8.5 → 雪どけ 2 → 小さいサビ 3 → 最後のサビ 10
#   旋律の性格 … 16分で食って短く切る。句の最後だけ伸ばす。サビの山は 9小節目からの上り（ファ♯5まで。テトの音域は ラ3〜ファ♯5）
# 使い方: VB_VOCAL=1 python3 vt3_16d_pudding.py <出力.json>
from vocalo_lib import *
import random as _r

S = Song("16", "pudding-d", "おやつ宣戦布告 D（仮）", "Snack War D", 112, 4, "E", "minor", "ファンク・ロック")
S.kit = "naked-x"; S.flags = S.flags + " --bass bnb-loud --space room --space-wet 0.08"
K = Key("E", "minor"); SC = {4, 6, 7, 9, 11, 0, 2}
RIFF = ["Em7", "Em7|D"]
A_CH = ["Em7", "D", "Cmaj7", "B7", "Em7", "G", "A", "A|B7"]                      # 根音: 下へ1つずつ（ミ→レ→ド→シ）、後半は上へ（ミ→ソ→ラ→シ）
B_CH = ["C", "C|D", "Bm7", "B7"]
C_CH = ["Em7", "G", "A", "C|B7", "Em7", "G", "A", "C|B7", "Em7", "F", "C|D", "Em"]   # 10小節目の F（♭II）で景色を変える
Y_CH = ["Cmaj7", "D", "Em7", "G|F#m7", "Cmaj7", "D", "Am7", "B7"]
S.scene("ベース", 2, "intro", RIFF)
S.scene("前奏", 4, "intro", ["Em7", "Em7|D", "C", "C|B7"])
S.scene("Aメロ", 8, "verse", A_CH)
S.scene("Bメロ", 4, "pre", B_CH)
S.scene("サビ1", 12, "chorus", C_CH)
S.scene("つなぎ", 2, "break", RIFF)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 12, "chorus", C_CH)
S.scene("雪どけ", 8, "bridge", Y_CH)
S.scene("小さいサビ", 6, "chorus", C_CH[:6])
S.scene("最後のサビ", 16, "chorus", C_CH + ["Em7", "F", "C|D", "Em"])
S.scene("おわり", 2, "outro", RIFF)
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(1604)

# ================= 歌（1小節ずつ、型も言葉も書く）=================
AP = ["x-xx.x-x--x-x---", "xx-x-xx-------..", "xx.x-xx.x--x----", "x--xx---x-----..", "x-xx-xx.xx.x----", "x.x-xx-x------..", ".xx-xx.x-x-x-...", "x-x-x-xx--x---.."]      # 2小節でひと息。句の最後を伸ばす
AD = ["1 1 3 1 1 3 5", "4 4 2 4 4", "3 3 5 3 3 5 6", "5 4 2 2", "5 5 7 5 5 7 5 3", "5 7 7 5 7", "4 4 #6 4 #6 1' #6", "1' #6 1' 2' 1' 2'"]
A1 = ["さんじをさした", "れいぞうこ", "しろいとびらの", "そのおく", "きんのつきひとつ", "ねむってるよ", "せなかにけはい", "となりのおう"]
A2 = ["こぶしをにぎり", "かまえたら", "なんかいしても", "ひきわけ", "つきがぬるんでく", "いそがなきゃ", "わけあうなんて", "ありえないね"]
BP_ = ["x---x-x---x---..", "x-----x-x-----..", "x-x---x---x---..", "x-------x-----.."]
BD = ["3 5 6 6", "6 6 7", "7 5 7 2'", "1' #7"]
B1 = ["ゆずれぬ", "ひかり", "ゆらゆら", "よぶ"]
B2 = ["つるぎが", "ひかる", "にらんで", "さあ"]
Ca, Cb, Cc, Cd, Ce, Cf, Cg, Ch = "..xx.xx.x--x----", "xx.x--x-------..", "x-xx-x--x--x----", "x-x--x--x-----..", "xx.xx.xx.x--x---", "x-x-x---------..", "x--xx-x---------", "xx-xx---------.."
CP = [Ca, Cb, Cc, Cd, Ca, Ch, Ce, Cf, Cc, Cd, Ce, Cg]
CD = ["5 5 7 5 3 5", "7 7 5 7", "1' 1' 7 #6 7 1'", "1' 7 1' #7", "3 3 5 3 1 3", "5 5 3 3", "1' 1' #6 1' 1' #6 7 1'", "1' 1' 2'",
      "3 5 7 1' 2' 1'", "1' 6 4 6", "1' 1' 7 1' 2' 2' 1' 2'", "2' 1' 7 1'"]
C1 = ["さんじのかね", "なりだす", "つきはひとつ", "きんいろ", "となりのおう", "にやりと", "つるぎをぬいたら", "さいご", "ゆずれないね", "このつき", "らんせのまくあけ", "さんじだ"]
C2 = ["ぐーちょきぱー", "あいこで", "うらないまだ", "つづくよ", "かがみあわせ", "おなじて", "つきをわるなんて", "むりだ", "とろけるまえ", "きめたい", "らんせまだつづく", "さんじだ"]
C3 = ["さんじのかぜ", "やさしい", "つきはふたつ", "ならんで", "となりのおう", "わらうよ", "つるぎをおいたら", "はるだ", "おなじうたを", "うたえば", "らんせのまくおり", "またあす"]
C4 = ["あしたのつき", "さかなだ", "あたまとしっぽどっち", "さんじだ"]
YP = ["x---x---x-x---..", "x-----x-------..", "..x-x---x---x-..", "x-x-x---------..", "x---x-x-x---x-..", "x---x---------..", "..x-x-x-x---x-..", "x-x---x-------.."]
YD = ["3 5 6 5", "2 4", "3 5 7 5", "7 5 4", "3 3 5 6 1'", "7 2'", "6 6 1' 6 1'", "2' #7 2'"]
YT = ["めがみが", "きて", "ふたつめ", "おいた", "めがあえば", "ふと", "わらいだす", "ふたり"]


def put(name, pats, degs, words, o=4):
    lines, text = song_lines(list(zip(pats, degs, words))); bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ", AP, AD, A1); put("Bメロ", BP_, BD, B1); put("サビ1", CP, CD, C1)
put("Aメロ2", AP, AD, A2)
put("Bメロ2", BP_, BD, B2); put("サビ2", CP, CD, C2); put("雪どけ", YP, YD, YT)
put("小さいサビ", CP[:6], CD[:6], C3[:6]); put("最後のサビ", CP + [Ca, Cb, Ce, Cg], CD + CD[8:], C3 + C4)

# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


def strum(tracks, b, pat, **kw):
    c1, c2 = halves(b)
    if c1 == c2: gtr_strum(tracks, S, b, pat, c1, RNG, **kw)
    else: gtr_strum(tracks, S, b, pat[:8] + "." * 8, c1, RNG, **kw); gtr_strum(tracks, S, b, "." * 8 + pat[8:], c2, RNG, **kw)


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), SC))


CLEAN = dict(di="emily", stringNoise=True, amp="jpopClean", ampDrive=0.12, chorus=0, humanPitch=0, noScoop=True, powerChord=False, sustain=1.3, release=0.5)
GFX = [{"type": "filter", "kind": "highpass", "freq": 110, "q": 0.7}, {"type": "eq", "low": -1, "mid": 1.5, "midHz": 1800, "high": 1}, {"type": "room", "mix": 0.1}]
GR = [S.track(f"Rギター{i + 1}弦め（クリーン）", "distGuitar", volume=0.075, pan=0.5, fx=GFX, **CLEAN) for i in range(6)]
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.04, -0.55, drive=0.3)) for i in range(6)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.26))
STAB = [S.track(f"スーパーソウの合いの手{i + 1}", "lead", patch="kfbSupersawWide", volume=0.024, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.15, fx=rack_supersaw()) for i in range(5)]
PLK = S.track("きらきらのプラック", "lead", patch="kfbSquarePluck", volume=0.05, pan=-0.3, reverb=0.2, fx=rack_pluck())
CLAP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.075, pan=0.05, reverb=0.15, modulate=False)

# ベースの型（1小節に5〜7音。根音から歩いて、次の和音の根音へとなりの音で入る）
RIFF_B = [("x-.x..x-x-.xx-x-", "11355wd"), ("x-..x.x-x-x-x-x-", "1871l1a")]                       # 曲の顔になるリフ
WB = [("x-.x..x-x-.xx-x-", "11355wd"), ("x-..x.x-..x-x-x-", "1875wd"), ("x-x-..x-.xx-x-x-", "12355wd"), ("x-.x-.x-x-x-x-x-", "1123123"),
      ("x-..x.x-x-.xx-x-", "18755wd"), ("x-x-x-..x-.xx-x-", "12345wd"), ("x-.x..x-.xx-x-x-", "11345wa"), ("x-x-..x-x-x-x-x-", "1231234")]
VB_ = [("x--x..x-..x-x-x-", "113wda"), ("x-..x-x-..x.x-x-", "1535wd"), ("x--x..x-x-..x-x-", "11235d"), ("x-.x..x-x-x-x-x-", "1151123")]      # Aメロ: 少しすき間を空ける
FUNK = ["x-xxx-x-xxx-x-xx", "x-x-xxx-x-xxx-x-", "x-xxx-x-x-xxx-xx", "x-x-xxx-xxx-x---"]
KICKS = ["X..x...xX.x.....", "X.....x.X..x....", "X..x...xX.x.....", "X.....x.X.x....."]


def stab(b, pat, second=True):
    v = wide9(halves(b)[1 if second else 0])
    for j in range(5): STAB[j].bar(b, steps(pat, [N(v[j])]))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "ベース":                                                              # ベースひとり。2小節目にハイハットが小さく入る
        bass(b, *RIFF_B[i])
        if i == 1: D.set(b, "................", "..............xX", "x...x...x...x..."); stab(b, "............x-x-")
    elif n in ("前奏", "つなぎ", "おわり"):
        bass(b, *(RIFF_B[i % 2] if i < 2 else WB[i + 2]))
        if n == "おわり" and i == 1:                                                # リフの途中（3拍目のウラ）で全員止まる
            BASS.bar(b, walk_bass("x-.x..x-x-x.....", "11351", "Em7", "Em7", "Em7", SC)); strum(GR, b, "x-xxx-x-x-x.....", drive=False); strum(GL, b, "x-------x-x.....", strings=3)
            D.set(b, "X..x...xX.X.....", "....X.....X.....", "X.xxX.xxX.X....."); continue
        strum(GR, b, FUNK[i % 4], drive=False)
        if i % 2 == 0 or n == "前奏": strum(GL, b, "x-------x-------" if i % 2 == 0 else "x-----x---x-----", strings=3)
        if n == "前奏": stab(b, "x-----x-----x-x-" if not odd else "..........x-.x-.", second=odd)
        feel(D, b, "funk16", k=KICKS[i % 4])
        if i == 0: crash(D, b, "C2", 4)
        if n == "前奏" and last: fill_cresc(D, b, 1)
        if n == "つなぎ" and last: fill_cresc(D, b, 2)
    elif n in ("Aメロ", "Aメロ2"):
        two = n == "Aメロ2"
        stop = i == 3                                                               # 4小節目: 後ろの2拍は伴奏が休む（歌の伸ばす音とドラムだけ）
        bass(b, *(("x-.x..x-........", "115") if stop else VB_[i % 4] if not two else WB[(i + 4) % 8]))                      # 2番はベースがもっと動く
        strum(GR, b, "x-----x-........" if stop else ["x-------x-x-----", "x-----x---x-x---", "x---x-----x-----", "x-----x-x---x-x-"][i % 4], drive=False)      # 歌が細かいので、ギターは長めに置く
        if two and i >= 4: strum(GL, b, "x---------------" if not odd else "x-------x-------", strings=3)
        if two: feel(D, b, "break" if not odd else "break2")
        else: feel(D, b, "soul8", k=["X.......x.X.....", "X..x....X.......", "X.......x.X.....", "X.....x.X..x...."][i % 4])
        if i == 0: crash(D, b, "C2", 4)
        if i == 3: D.H[b] = D.H[b][:14] + "O."
        if last: fill_cresc(D, b, 1)
        if two and odd: PLK.bar(b, "R:2.5 " + arp16(halves(b)[1], "xxxxxx", (0, 1, 2, 3, 4, 5), lo="E5", hi="E7"))
    elif n in ("Bメロ", "Bメロ2"):                                                   # 半分の速さ。和音をのばす。最後の1拍は全員休み
        bass(b, ["x-----x---x-x-x-", "x-----x-x---x-x-", "x-----x---x-x-x-", "x-------x-x-...."][i], ["115wd", "11513"[:5], "135wd", "118"][i])
        strum(GR, b, "x-------x-------" if i < 3 else "x-------x---....", drive=False, lag_ms=14)
        stab(b, "x-------x-------" if i < 3 else "x-------x---....", second=False)
        if n == "Bメロ2": strum(GL, b, "x---------------" if i < 3 else "x-------x---....", strings=3)
        feel(D, b, "half", h="X...x...X...x...")
        if i == 3: D.set(b, "X.......X.X.....", "........X.xX....", "X...x...X.......")
        CLAP.bar(b, "R:2 B4:1 R:1")
    elif n in ("サビ1", "サビ2", "小さいサビ", "最後のサビ"):
        small = n == "小さいサビ"; big = n == "最後のサビ"
        if small:                                                                  # ドラムなし。クリーンのギターと、のばすベースと歌
            bass(b, "x-------x---x-x-" if not odd else "x-----x---x-x-x-", "11wd" if not odd else "135wd"); strum(GR, b, "x-----x---x-x---" if not odd else "x---x-----x-----", drive=False, lag_ms=14)
            if i >= 4: CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
            if last: D.set(b, "................", "........oxxxXXXX", "................"); stab(b, "........x-------", second=True)
            continue
        stop = i in (7, 11)                                                         # 8・12小節目: 後ろの2拍は伴奏が休む（歌の伸ばす音とドラムのフィルだけ）
        strum(GR, b, FUNK[i % 4] if not stop else "x-xxx-x-........", drive=False)
        if stop: strum(GL, b, "x-------........", strings=3)
        elif i % 4 == 0: strum(GL, b, "x-------x-------" if big else "x---------------", strings=3)
        elif big or n == "サビ2": strum(GL, b, "x-------x-------" if not odd else "x-----x---x-----", strings=3)
        if i == 9: strum(GL, b, "x---x---x-x-x---", strings=4)                        # F（♭II）の小節は、ギターも前へ出る
        bass(b, *(WB[(i + (0 if n == "サビ1" else 3)) % 8] if not stop else ("x-.x..x-........", "115")))
        if (CP + [Ca, Cb, Ce, Cg])[i] in (Cb, Ch, Cd, Cf, Cg) and not stop: stab(b, "..........x-.x-." if i % 4 != 3 else "........x-.x-.x-")       # 歌が伸ばしている後ろで合いの手
        if big and odd: PLK.bar(b, "R:2 " + arp16(halves(b)[1], "xxxxxxxx", (0, 1, 2, 3, 4, 5, 6, 7), lo="E5", hi="E7"))
        feel(D, b, "funk16", k=KICKS[i % 4], h=None if not big else "X.xxX.xxX.OxX.xO" if i % 4 == 1 else None)
        if big or n == "サビ2": CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i % 4 == 0: crash(D, b, "C2", 4)
        if i in (7, 11) or (big and i == 15): fill_cresc(D, b, 2)
        if n == "サビ1" and i == 11: fill_cresc(D, b, 1)
    elif n == "雪どけ":                                                             # ドラムは休み。手びょうしとベースと、のびる和音
        bass(b, ["x-----x---x---x-", "x-------x-x-x-x-", "x-----x---x---x-", "x---x---x---x-x-"][i % 4], ["135d", "115wd", "153d", "1313a"[:5]][i % 4])
        stab(b, "x---------------", second=False)
        if i >= 2: CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i >= 4: strum(GR, b, "x-------x-------" if not odd else "x---x---x-x-----", drive=False, lag_ms=16)
        if odd: PLK.bar(b, "R:2.5 " + arp16(halves(b)[1], "xxxxxx", (0, 1, 2, 3, 4, 5), lo="E5", hi="E7"))
        if last: D.set(b, "................", "............oxXX", "................")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の16「おやつ宣戦布告」のD版（はねるファンク・ロック・112・ホ短調）。分析ソフトで分かった弱い所"
          "（ベースが根音ばかり・コードが4度5度ばかり・歌のリズムのくり返し）を直して作った。ベースひとりで始まり、リフの途中で止まる。自作")
finish(S, LY, V, 0, level={"verse": -0.1}, special={"雪どけ": -0.6, "小さいサビ": -0.5, "最後のサビ": 0.5, "ベース": 0.3})

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=88, down=10, up=10, seed=16)
js = load(path); gtr_velocity(js, "Lギター", 3); gtr_velocity(js, "Rギター", 4); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 4, "pre": 10, "chorus": 12, "最後のサビ": 16, "bridge": 6}, scoop=0.25, slash=0.6, vib_min_beats=2.0, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ1", 8, None, K), ("サビ2", 4, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    for sgn in (-1, 1): harmony(path, S, [("最後のサビ", 0, None, K)], steps=0, vol=0.2, pan=0.6 * sgn, transpose=0.07 * sgn)
    voice_by_scene(path, S, {"雪どけ": "whisper", "小さいサビ": "cute"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
final_gain(path, {"ベース": 4.0, "Bメロ2": -0.8, "サビ2": -0.3, "雪どけ": -1.5, "最後のサビ": 0.8})   # v1: ベースだけの頭が小さかった・雪どけがサビと同じ大きさだった・最後のサビがサビ2より小さかった
