# 16「おやつ宣戦布告」E版（ポンプするロック）。仮。
# 人間（2026-11-16）: スケッチ D・E・F を「全部」1曲に仕上げる。分析ソフト（段2）で分かった3つ（ベースの歩き・コードの動き・歌のリズムのくり返し）を直して作る。
# 曲を決める表:
#   形 … サビから始まる（歌と、のびる和音だけ）→ ベルの前奏 → いくさ（A・B・サビ）×2 → 歌のないドロップ（ベルが歌う）→ 最後のサビ（長い）→ ベルひとりで終わる
#   強さ … サビ頭 4 → 前奏 5 → A 5（後半 6）→ B 4→7（最後の2拍は全員休み）→ サビ 9 → A2 6 → B2 4→7 → サビ2 9 → ドロップ 7 → 最後のサビ 10 → ベル 2
#   旋律の性格 … 半分の速さで大きく。2小節でひと息（8分で進んで、句の最後を2〜3拍のばす）。Aメロは低く言葉を多く、Bメロは長い音でためる
# 使い方: VB_VOCAL=1 python3 vt3_16e_pudding.py <出力.json>
from vocalo_lib import *
import random as _r

S = Song("16", "pudding-e", "おやつ宣戦布告 E（仮）", "Snack War E", 160, 4, "A", "major", "ポンプするロック")
S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
K = Key("A", "major"); SC = {9, 11, 1, 2, 4, 6, 8}
C_CH = ["D", "E", "C#m7", "F#m", "D", "E", "Asus4|A", "G", "D", "E", "C#m7", "F#m", "Bm7", "Dm", "A", "Esus4|E"]      # 8小節目の G（♭VII）、14小節目の Dm（IVm）
A_CH = ["A", "A", "G", "G", "F#m", "F#m", "D", "Dm", "A", "A", "G", "G", "F#m", "E", "D", "E"]                          # 根音が下へ1つずつ（ラ→ソ→ファ♯）
B_CH = ["Bm7", "C#m7", "D", "E", "Bm7", "C#m7", "D|Dm", "Esus4|E"]                                                      # 根音が上へ1つずつ
S.scene("サビ頭", 8, "chorus", C_CH[:8])
S.scene("前奏", 4, "intro", ["D", "E", "F#m", "E"])
S.scene("Aメロ", 16, "verse", A_CH)
S.scene("Bメロ", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("Aメロ2", 8, "verse", A_CH[:8])
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ドロップ", 8, "break", ["F#m", "G", "D", "E", "F#m", "G", "Bm7", "E"])
S.scene("最後のサビ", 24, "chorus", C_CH + C_CH[8:15] + ["A"])
S.scene("おわり", 4, "outro", ["D", "E", "F#m", "A"])
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(1605)

# ================= 歌 =================
E1, E2, E3, E4, E5, E6, E7, E8 = "x-x-x-x---x-x---", "x-----x-------..", "x---x-x-x-x---x-", "x-------x-----..", "..x-x-x-x---x-x-", "x---x---x-----..", "x-x---x-x---x-x-", "x-----------...."
CP = [E1, E2, E3, E4, E5, E6, E7, E8] * 2
CD = ["5, 5, 1 1 3 2", "1 2", "3 3 5 5 3 2", "1 3", "4 4 6 6 5 4", "5 4 5", "5 5 4 3 2 1", "2",
      "1 1 3 3 4 6", "6 5", "5 5 3 3 2 3", "2 1", "4 4 4 6 5 4", "b6 4 1", "1 1 3 3 5 6", "5"]
C1 = ["きんのつきひとつ", "となりのおうさま", "ゆずれぬおうかんだ", "さんじのらんせ", "ぎんのつるぎぬき", "にらみあうふたり", "とろけるまえにきめ", "いざしょうぶだよ"]
C2 = ["ぐーちょきぱーでも", "かがみあわせだね", "まんげつわるなんて", "みとめられない", "ぎんのつるぎまた", "ひかりをはなつよ", "ぬるくなるそのまえ", "きめてしまおう"]
C3 = ["めがみがふたつめ", "さしだしてくれた", "おうかんはふたつだ", "さんじのはるだ", "ぎんのつるぎおき", "わらいあうふたり", "おなじはなうたまで", "おそろいだよね"]
C4 = ["あしたのつきはね", "さかなのかたちだ", "あたまかしっぽかまた", "らんせがくるよ"]
V1, V2, V3, V4, V5, V6, V7, V8 = "x-x-x-x-x---x-x-", "x---x-------....", "..x-x-x-x-x-x---", "x-x-x-------....", "x---x-x-x-x-x-x-", "x-x---------....", "x-x-x---x-x-x---", "x---x---x---...."
AP = [V1, V2, V3, V4, V5, V6, V7, V8, V5, V6, V3, V4, V1, V2, V7, V8]
AD = ["1 1 2 3 3 2 1", "2 3", "2 2 4 2 b7, 2", "2 4 4", "3 3 1 3 3 1 6,", "1 3", "1 1 4 1 6, 1", "b6, 1 1",
      "3 3 5 3 3 5 3", "2 1", "4 4 2 4 4 5", "4 2 4", "5 5 3 5 5 3 1", "2 5", "4 4 6 4 4 6", "5 4 2"]
A1 = ["さんじのかねがなる", "しろいとびらのおく", "つめたいへやのなか", "きんのつきがねむる", "せなかにけはいあり", "となりのおうがきた", "めとめがあえばほら", "ひけないいくさだよ"]
A2 = ["こぶしをにぎりしめ", "なんかいでもおなじ", "つきがぬるんでゆく", "わけあうなんていや"]
Q1, Q2, Q3, Q5, Q6 = "x-------x---x---", "x-----------....", "x---x---x---x---", "x---x-x-x---x-x-", "x-------........"
BP_ = [Q1, Q2, Q3, Q2, Q1, Q2, Q5, Q6]
BD = ["2 2 4", "5", "4 4 1 4", "5", "4 4 6", "5", "6 6 4 b6 b6 4", "5"]
B1 = ["ゆずれぬ", "ひかりがね", "ゆらゆら", "よんでいるんだ"]
B2 = ["にらんで", "うごけない", "ぬるんで", "ゆくきんのつき"]


def put(name, pats, degs, phrases, o=4):
    lines, text = song_phrases(pats, degs, phrases); bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("サビ頭", CP[:8], CD[:8], C1[:4]); put("Aメロ", AP, AD, A1); put("Bメロ", BP_, BD, B1); put("サビ1", CP, CD, C1)
put("Aメロ2", AP[:8], AD[:8], A2); put("Bメロ2", BP_, BD, B2); put("サビ2", CP, CD, C2)
put("最後のサビ", CP + CP[8:], CD + CD[8:], C3 + C4)

# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


def strum(tracks, b, pat, **kw):
    c1, c2 = halves(b)
    if c1 == c2: gtr_strum(tracks, S, b, pat, c1, RNG, **kw)
    else: gtr_strum(tracks, S, b, pat[:8] + "." * 8, c1, RNG, **kw); gtr_strum(tracks, S, b, "." * 8 + pat[8:], c2, RNG, **kw)


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), SC, lo=29))


def saw(b, pat):
    c1, c2 = halves(b); v, v2 = wide9(c1), wide9(c2)
    for j in range(5): SAW[j].bar(b, steps(pat, [N(v[j])]) if c1 == c2 else steps(pat[:8], [N(v[j])]) + " " + steps(pat[8:], [N(v2[j])]))


GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.04, -0.6, drive=0.4)) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.038, 0.6, drive=0.35)) for i in range(6)]
BASS = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.105, pan=0, duck=0.25, fx=rack_bass())      # v2: 歩くベースが、のびるサブベースにかくれていた（分析ソフトで測ると根音 88%）ので、前へ出す
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.02, pan=0, duck=0.4)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.03, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.65, fx=rack_supersaw()) for i in range(5)]
BELL = S.track("ベル", "lead", patch="kfbGlocken", volume=0.085, pan=0.25, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
KFXT = S.track("クラップ", "guitar", patch="kawaiiFx", volume=0.07, pan=0.05, reverb=0.15, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
FXT = S.track("効果音", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.2, modulate=False)
GATES = ["x---x-x---x-x-x-", "x-x---x-----x-x-", "x---x-x-x-x-x---", "x-x---x---x-x---", "x---x-x---x-x-x-", "x-x---x-----x---", "x-x-x-x---x---x-", "x---x-x-x-------"]
# ベース（1小節に4〜6音。根音 → 3度・5度 → 次の根音へとなりの音で歩く）
WB = [("x---x-x---x-x-x-", "1155wd"), ("x-x---x-----x-x-", "1135d"), ("x---x-x-x---x-x-", "11235d"), ("x-x---x---x-x-x-", "11875a"),
      ("x---x-x---x-x-x-", "1535wd"), ("x-x---x-----x-x-", "1151d"), ("x-x-x-x---x---x-", "12345d"), ("x---x-x-x---x-x-", "1132wd")]
VBS = [("x-------x---x-x-", "115d"), ("x-----x-x---x---", "1351"), ("x-------x-x-x-x-", "11wda"), ("x---x---x---x-x-", "1535d")]      # Aメロ: 少なめ。小節の終わりで歩く
BELL_A = ["..x-..x-..x-x---", "....x-x-....x-x-", "..x-..x-x-x-....", "....x-x-..x-x---"]


def bell(b, pat, order=(0, 1, 2, 1, 0, 2), lo="C#5", hi="C#6", second=False):
    t = [N(m) for m in tones(halves(b)[1 if second else 0], lo, hi)]; BELL.bar(b, steps(pat, [t[q % len(t)] for q in order]))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; r = N(low(halves(b)[0], "F1"))
    if n == "サビ頭":                                                              # 歌と、のびる和音だけ。5小節目からサブベース、8小節目で上がる効果音
        saw(b, "x---------------" if i < 4 else "x-------x-------")
        if i >= 4: SUB.bar(b, steps("x---------------", [r])); KFXT.bar(b, "R:2 B4:1 R:1")
        if i >= 6: bell(b, "..........x-x-x-")
        if last: FXT.bar(b, fx_bar((0, "up", 4))); D.set(b, "................", "........o.x.xXXX", "................")
    elif n == "前奏":
        saw(b, GATES[i]); bell(b, ["x-x-x---x-x-x---", "x-x-x---x-------", "x-x-x---x-x-x---", "x-x-x-x-x-x-...."][i], (0, 1, 3, 1, 0, 3))
        bass(b, *WB[i]); SUB.bar(b, steps("x-------x-------", [r, r])); strum(GL, b, "x---------------", strings=3); strum(GR, b, "x---------------", strings=4)
        feel(D, b, "half" if i != 3 else "halfopen", k="X.........x....." if not odd else "X.....x...x.....")
        if i == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
        if last: fill_cresc(D, b, 1)
    elif n in ("Aメロ", "Aメロ2"):
        two = n == "Aメロ2"; late = i >= 8 or two
        stop = i == 7                                                               # 8小節目: 後ろの2拍は伴奏が休む
        bass(b, *(("x---x---........", "13") if stop else VBS[i % 4] if not late else WB[(i + 1) % 8])); SUB.bar(b, steps("x---------------" if not stop else "x-------........", [r]))
        if AP[i] in (V2, V4, V6, V8) and not stop: bell(b, BELL_A[(i // 2) % 4])       # 歌が伸ばしている小節で、ベルが答える
        if late: strum(GL, b, "x-------........" if stop else "x---------------" if not odd else "x-------x-------", strings=3)
        if two: strum(GR, b, "x-------........" if stop else "x-------x-------" if not odd else "x-----x---------", strings=4)
        feel(D, b, "half" if not late else ("break" if not odd else "break2"), h="X...x...X...x..." if not late else None)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i == 7 or last: fill_cresc(D, b, 1, toms=last)
    elif n in ("Bメロ", "Bメロ2"):                                                   # ためる。和音がのびて、スネアがだんだんふえる。最後の2拍は全員休み
        if last:
            saw(b, "x-------........"); SUB.bar(b, steps("x-------........", [r])); strum(GL, b, "x-------........", strings=3); strum(GR, b, "x-------........", strings=4)
            D.set(b, "X.......X.......", "X.x.xxXX........", "................"); continue
        saw(b, "x---------------" if i < 4 else "x-------x-------"); bass(b, "x-------x---x-x-" if i < 4 else "x---x---x-x-x-x-", "115d" if i < 4 else "1135wd"); SUB.bar(b, steps("x---------------", [r]))
        if i >= 4: strum(GL, b, "x---------------", strings=3); strum(GR, b, "x-------x-------", strings=4)
        D.set(b, "X.......X......." if i < 4 else "X...X...X...X...", "................" if i < 2 else ("........X......." if i < 4 else ("....X.......X..." if i < 6 else "X...X...X.X.X.X.")), "X...x...X...x..." if i < 6 else "................")
        if i in (3,): hat_roll(HATR, b, 1)
        if i == 6: FXT.bar(b, fx_bar((0, "up", 4)))
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        big = n == "最後のサビ"; g = GATES[(i + (3 if n == "サビ2" else 0)) % 8]; stop = i % 8 == 7 and not (big and last)      # 8小節ごとに、後ろの2拍は伴奏が休む（歌の長い音とドラムのフィルだけ）
        if stop: saw(b, "x-------........"); bass(b, "x---x-x-........", "135"); SUB.bar(b, steps("x-------........", [r])); strum(GL, b, "x-------........", strings=3); strum(GR, b, "x-------........", strings=4)
        else:
            saw(b, g); bass(b, *WB[(i + (2 if n == "サビ2" else 0)) % 8]); SUB.bar(b, steps("x-------x-------", [r, N(low(halves(b)[1], "F1"))]))
            strum(GL, b, "x-------x-------" if not odd else "x-----x---------", strings=3); strum(GR, b, "x---------------" if not odd else "x-----x---------", strings=4)
        if (CP + CP[8:])[i] in (E2, E4, E6, E8): bell(b, "..........x-x-x-" if i % 4 == 1 else "......x-x-x-x-x-", (0, 1, 2, 3, 2))
        feel(D, b, "half" if i % 4 != 3 else "halfopen", k="X.........x....." if not odd else "X.....x...x.....", h="X.x.X.x.X.x.X.x." if not big else "X.x.X.xxX.x.X.x.")
        KFXT.bar(b, "R:2 B4:1 R:1")
        if i % 8 == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
        if i % 8 == 7 and not last: fill_cresc(D, b, 2)
        if i % 8 == 3: hat_roll(HATR, b, 0.5)
        if last and n != "最後のサビ": fill_cresc(D, b, 1, toms=False)
        if last and big: saw(b, "x---------------"); D.set(b, "X.........X.X...", "........X...X.XX", "X.x.X.x.........")
    elif n == "ドロップ":                                                           # 歌は休み。ベルが歌い、和音が細かくポンプする
        saw(b, ["x-x-x---x-x-x---", "x---x-x-x---x-x-", "x-x-x---x-x-x---", "x---x-x-x-x-x-x-"][i % 4]); bass(b, *WB[(i + 4) % 8]); SUB.bar(b, steps("x-------x-------", [r, r]))
        bell(b, ["x---x-x---x-x---", "x-x---x-x-------", "x---x-x-x-x-x---", "x-x-x---x---x-x-"][i % 4], [(2, 1, 0, 1, 2), (3, 2, 1, 2), (2, 1, 0, 1, 2, 3), (3, 2, 1, 0, 1, 2)][i % 4], lo="A5", hi="A6")
        feel(D, b, "four" if i < 6 else "half"); KFXT.bar(b, "R:1 B4:1 R:1 B4:1")
        if i == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
        if i in (3,): hat_roll(HATR, b, 1)
        if last: fill_cresc(D, b, 2); FXT.bar(b, fx_bar((0, "up", 4)))
    elif n == "おわり":                                                            # ベルひとり（1小節目だけ、みんなの最後の和音がのこる）
        if i == 0: strum(GL, b, "x---------------", strings=3); strum(GR, b, "x---------------", strings=4, lag_ms=14); SUB.bar(b, steps("x---------------", [r])); D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)
        bell(b, ["x-x-x---x-x-x---", "x-x-x---x-------", "x-x-x---x-x-x---", "x-x-x-----------"][i], (0, 1, 3, 1, 0, 3))

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の16「おやつ宣戦布告」のE版（ポンプするロック・160・イ長調・半分の速さ）。分析ソフトで分かった弱い所"
          "（ベースが根音ばかり・コードが4度5度ばかり・歌のリズムのくり返し）を直して作った。サビから始まり、ベルひとりで終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.1}, special={"サビ頭": -0.2, "ドロップ": 0.2, "最後のサビ": 0.5})

from vt3x_lib import *
path = sys.argv[1]
js = load(path); gtr_velocity(js, "Lギター", 3); gtr_velocity(js, "Rギター", 4); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 4, "pre": 12, "chorus": 18, "最後のサビ": 22}, scoop=0.25, slash=0.6, vib_min_beats=2.0, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ1", 8, None, K), ("サビ2", 0, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    for sgn in (-1, 1): harmony(path, S, [("最後のサビ", 0, None, K)], steps=0, vol=0.2, pan=0.6 * sgn, transpose=0.07 * sgn)
    voice_by_scene(path, S, {"サビ頭": "cute", "Bメロ": "whisper", "Bメロ2": "whisper"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
final_gain(path, {"サビ頭": 4.0, "前奏": 3.0, "Aメロ": 0.5, "Aメロ2": -0.7, "Bメロ2": -0.7, "サビ2": -0.2, "ドロップ": 1.0, "最後のサビ": 1.6, "おわり": 4.0})   # v1: 歌い出しと前奏が小さかった・最後のサビがサビ2より小さかった
