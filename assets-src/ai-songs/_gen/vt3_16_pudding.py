# vt3 16「おやつ宣戦布告」Snack-Time Declaration of War（仮）— かけぬける明るいパンク・ロック。200・4/4。F長調（IV → IVm）、最後のサビは半音上。2分48秒。
# 第3弾（0時〜24時の街）の 15時。表は docs/sound/vt3-plan.md。
#
# v7（2026-11-15）: ゼロから作り直し。30秒のスケッチ3案（sk16_pudding.py）から、人間が C を選んだ:「C良かったけど、もっとプロ仕様にして。」
#   スケッチ C から、プロの編曲に近づけるために変えたこと:
#   ① 左右のギターに別の役（L＝パワーコードの8分、R＝3・3・2 のかき鳴らし）。全員が同じ8分を弾かない
#   ② 歌が食って入る所（小節の2拍目のウラ）で、ギター・ベース・ドラムもいっしょに食う（バンドの「キメ」）
#   ③ ベースは根音の8分だけにせず、オクターブと次の和音へ近づく音を入れる。Aメロはすき間のある型
#   ④ ドラムは人が叩いたゆれ・強弱・ゴーストノートつき（vgroove）。場面ごとに型を変え、4〜8小節ごとにフィル
#   ⑤ 場面ごとに鳴らす楽器を決める（Aメロはベースとドラムと歌が中心、ギターは答えるだけ。Bメロは半分の速さでピアノ。サビで全員）
#   ⑥ 和音は3和音を中心に、sus4 → 3和音の解決、IVm、小節の途中で変わる所（Csus4|C）
#   ⑦ 伴奏が休む所: Aメロの答えのあと1拍、サビの8小節目（歌だけ残る）、サビの前の1拍、雪どけの頭（ピアノだけ）
# 人間（2026-11-15）:「歌詞が直接すぎるものが多いので重要な所は隠語にしたりして。」→ 大事な言葉を言いかえた。「プリン」「兄」「けんか」「母」「じゃんけん」とは一度も言わない:
#   プリン＝金色の月／冷蔵庫＝白いとびらの向こうの冷たい部屋／けんか＝三時の乱世・いくさ／スプーン＝銀のつるぎ／兄＝となりの王／
#   じゃんけん＝こぶしをにぎる・グー・チョキ・パーのうらない／あいこ＝かがみ合わせ／半分こ＝満月を割る／母＝女神／なかなおり＝三時の春／たいやき＝魚のかたちの月
#
# 構成（前半と後半で別の曲のように変わる＝いくさ → 雪どけ）:
#   前奏（8）→ Aメロ（16・歌とリズム隊。ギターは答えるだけ）→ Bメロ（8・半分の速さ）→ サビ1（16）→ 間奏（8・合いことばの節）
#   → Aメロ2（8・短い）→ Bメロ2（8）→ サビ2（16）→ 雪どけ（16・ピアノとクリーンのギター。別の曲のように静か）→ ギターソロ（8）
#   → 最後のサビ（24・半音上）→ おわり（4・スプーンを置く「カチ」）
#
# 物語: 3時。白いとびらの向こうに、金色の月がひとつ。背中に気配 ── となりの王と目が合った。こぶしをにぎっても、かがみ合わせで決まらない。
#   満月を割る提案は認められない。そこへ女神が、ふたつめの月を差し出す。月をふたつ並べたら、ふたりで吹き出して、同じ鼻歌。明日の月は魚のかたち、あたまをあげる。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は景色で表す: 取り合いの「乱世」が、並んで食べる「春」に変わる。
from vocalo_lib import *

S = Song("16", "pudding", "おやつ宣戦布告（仮）", "Snack-Time Declaration of War", 200, 4, "F", "major", "パンク・ロック（ボカロ）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock --piano salamander " + S.flags
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.4
S.drum_scale = 0.9
S.keepers = {}
K = Key("F", "major"); KD = Key("F#", "major")
def M(pat, degs): return mel16(pat, degs.split())


C_CH = ["F", "Am", "Bb", "Bbm", "F", "Dm", "Gm", "Csus4", "F", "Am", "Bb", "Bbm", "F", "Dm", "Gm", "Csus4|C"]
A_CH = ["F", "F", "Dm", "Dm", "Bb", "Bb", "Gm", "Csus4", "F", "F", "Dm", "Dm", "Bb", "Bbm", "Gm", "C"]
B_CH = ["Gm", "Am", "Bb", "C", "Gm", "Am", "Bb", "Csus4|C"]
up1 = lambda L: ["|".join(tr_chord(x, 1) for x in c.split("|")) for c in L]
S.scene("前奏", 8, "intro", ["F", "Am", "Bb", "Bbm"] * 2)
S.scene("Aメロ", 16, "verse", A_CH)
S.scene("Bメロ", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", ["F", "Am", "Bb", "Bbm", "F", "Am", "Bb", "C"])
S.scene("Aメロ2", 8, "verse", ["F", "F", "Dm", "Dm", "Bb", "Bbm", "Gm", "C"])
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("雪どけ", 16, "bridge", ["Bbmaj7", "C", "Am7", "Dm", "Bbmaj7", "C", "F", "F"] * 2)
S.scene("ギターソロ", 8, "solo", ["Bb", "C", "Am", "Dm", "Bb", "C", "F", "C#7"])
S.scene("最後のサビ", 24, "chorus", up1(C_CH) + up1(C_CH[:7]) + ["C#"])
S.scene("おわり", 4, "outro", ["F#", "Bm", "F#", "F#"])

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
GL = [S.track(f"Lギター（パワーコード{i + 1}）", "distGuitar", **rock_gtr_spec(0.047, -0.6, drive=0.4)) for i in range(3)]
GR = [S.track(f"Rギター（かき鳴らし{i + 1}）", "distGuitar", **rock_gtr_spec(0.044, 0.6, drive=0.35)) for i in range(3)]
LEAD = S.track("リードギター", "leadGuitar", **lead_gtr_spec(0.075, 0.05))
CLN = S.track("クリーンのギター", "guitar", amp="crystal", volume=0.075, pan=0.35, reverb=0.3, chorus=0, sustain=1.0)
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.24))
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.1, pan=-0.2 + 0.15 * i, reverb=0.25, sustain=1.4) for i in range(3)]
PLK = S.track("きらきらのプラック", "lead", patch="kfbSquarePluck", volume=0.058, pan=0.3, reverb=0.2, fx=rack_pluck())
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.02, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.5, fx=rack_supersaw()) for i in range(5)]
SPOON = S.track("スプーン（グロッケン）", "glockenspiel", volume=0.06, pan=0.25, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
N = lambda m: nm(m)

# ================= 歌（16分のマス。x＝音の頭、-＝のばす、.＝休み）=================
# サビ: 2小節でひと息。1小節目は大きく（4分・4分・8分・8分・4分）、2小節目は「短い → 2拍目のウラから食って2拍のばす」
P1 = "x---x---x-x-x---"; P2 = "x-----x-------.."
CA = ["3 3 5 3 1", "4 4 5 6 1'", "5 5 6 5 3", "6 6 5 4 2", "1' 1' 6 5 6", "6 6 1' 6 4", "5 6 1' 1' 6", "2 4 6 1' 6"]
CB = ["2 3", "6 b6", "5 6", "4 5", "6 5", "5 4", "6 1'", "5 5"]
VC = [x for a, b in zip(CA, CB) for x in (M(P1, a), M(P2, b))]
C1 = "さんじのらんせ/つきはひとつぶ/ぎんのつるぎを/ぬいたらさいご/さんじのらんせ/ゆずれぬひかり/とろけるまえに/きめてしまおう"
C2 = "さんじのらんせ/ぐーちょきぱーの/うらないはまだ/かがみあわせで/さんじのらんせ/まんげつをわる/そんなていあん/みとめられない"
C3 = ("さんじのはるだ/つきはふたつぶ/ならべてみたら/わらいがもれた/さんじのはるだ/おなじはなうた/くちずさんでる/となりのおうと/"
      "さんじのはるだ/あしたのつきは/さかなのかたち/あたまをあげる")
# Aメロ: 1小節目は8分で言葉をつめる（16分の切れ目が1つ）、2小節目は3音で、2拍目のウラから食って伸ばし、1拍休む
PA = "x-x-x-.xx-x-x-.."; PB = "x-x-..x-----...."
AA = ["1 1 2 3 3 2 1", "3 3 4 5 5 4 3", "1 1 2 3 3 5 3", "6, 6, 1 2 2 1 6,", "5 5 6 5 3 3 5", "6 6 1' 6 5 5 6", "1 1 2 3 5 5 6", "6 6 5 3 2 2 3"]
AB = ["2 3 5", "4 5 6", "2 1 2", "1 2 1", "6 5 6", "5 3 5", "1' 6 1'", "2 2 5"]
VA = [x for a, b in zip(AA, AB) for x in (M(PA, a), M(PB, b))]
A1 = ("とけいのはりが/さんじ/しろいとびらの/むこう/つめたいへやに/ひとつ/きんいろのつき/ねむる/"
      "せなかにけはい/だれだ/となりのおうが/わらう/めとめがあえば/ひばな/ひくにひけない/いくさ")
A2 = "こぶしをにぎり/かまえ/なんかいしても/おなじ/つきがぬるんで/しまう/わけあうなんて/いやだ"
VA2 = VA[0:4] + VA[12:16]
# Bメロ: 半分の速さ。2拍・1拍・1拍 → 3拍のばす
Q1 = "x-------x---x---"; Q2 = "x-----------...."
VB = [M(Q1, "2 4 5"), M(Q2, "5"), M(Q1, "4 6 1'"), M(Q2, "7"), M(Q1, "2 4 6"), M(Q2, "5"), M(Q1, "5 6 7"), M(Q2, "1'")]
B1 = "ゆずれぬ/ひかりが/ゆらゆら/よんでる"
B2 = "めがみが/あらわれ/ふたつめ/さしだす"
# 雪どけ: 4分でゆっくり → 3拍のばす（別の曲のように）
Y1 = "x---x---x---x-x-"; Y2 = "x-----------...."
YA = ["3 3 2 1 2", "5 5 3 2 3", "6 6 5 3 5", "3 2 1 2 1", "5 5 6 1' 6", "6 6 5 3 5", "1' 1' 6 5 6", "3 2 1 2 2"]
YB = ["3", "1", "5", "1", "5", "6", "5", "1"]
VY = [x for a, b in zip(YA, YB) for x in (M(Y1, a), M(Y2, b))]
YT = "つきがふたつ/ならぶつくえ/つるぎをおき/かおをみたら/ふきだしてた/おなじくせで/はなうたまで/おそろいだね"
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ", K, VA, A1)
put("Bメロ", K, VB, B1)
put("サビ1", K, VC, C1)
put("Aメロ2", K, VA2, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC, C2)
put("雪どけ", K, VY, YT)
put("最後のサビ", KD, VC + VC[:8], C3)

# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return (c[0], c[-1])


def gtr(tracks, b, pat, kind, short=None):
    """ギター3声。kind: 'pw'＝パワーコード（低い）、'mid'＝中の和音。小節の途中で和音が変わるときは、前半と後半で和音を分ける"""
    c1, c2 = halves(b); out = [[], [], []]
    for ch, pp in ((c1, pat[:8]), (c2, pat[8:])):
        if kind == "pw": v = power(ch, "F2")
        else:
            r = low(ch, "C3"); up = tones(ch, nm(r + 1), nm(r + 12))[:2]
            while len(up) < 2: up.append(r + 12)
            v = [r] + up
        for j in range(3): out[j].append(steps(pp, [N(v[j])], short=short))
    for j in range(3): tracks[j].bar(b, " ".join(out[j]))


def bassp(b, pat, kinds, short=None):
    """ベース。kinds: r＝根音・o＝オクターブ上・5＝5度・a＝次の和音へ近づく音・R＝後半の和音の根音"""
    c1, c2 = halves(b); r = low(c1, "F1"); r2 = low(c2, "F1"); nx = S.chords[b + 1].split("|")[0] if b + 1 < S.nb else c2; rn = low(nx, "F1")
    ap = r2 + 7 if rn == r2 else (rn - 1 if rn > r2 else rn + 1); mp = {"r": r, "o": r + 12, "5": r + 7, "a": ap, "R": r2}
    BASS.bar(b, steps(pat, [N(mp[c]) for c in kinds], short=short))


def pno(b, pat, c=64, short=None):
    v = sorted(voice(halves(b)[0], c, 3))
    for j in range(3): PN[j].bar(b, steps(pat, [N(v[j])], short=short))


def saw(b, pat="x-------------.."):
    v = wide9(halves(b)[0])
    for j in range(5): SAW[j].bar(b, steps(pat, [N(v[j])]))


def sparkle(b, hi=False):
    """歌が伸ばしている後ろで「ピロピロピロピーン」（和音を16分で8つ駆け上がる）"""
    PLK.bar(b, "R:2 " + arp16(halves(b)[1], "xxxxxxxx", (0, 1, 2, 3, 4, 5, 6, 7), lo="F5" if not hi else "F#5", hi="F7"))


RSTRUM = "x-.x-.x-x-.x-.x-"                    # R: 3・3・2 のかき鳴らし
RSTRUM2 = "x-.x-.x---x-.x-."                   # 歌が食う小節: 2拍目のウラでいっしょに打って伸ばす
LDRIVE = "x-x-x-x-x-x-x-x-"; LDRIVE2 = "x-x-x-x---x-x-x-"
MOTIF = ["R:1 A4:0.5 C5:0.5 D5:1 C5:0.5 G4:0.5", "F4:2.5 R:1.5"]          # 合いことばの節（3・5・6・5・2 → 1）
SOLO = ["R:0.5 C4:0.5 F4:0.5 A4:0.5 G4:1.5 F4:0.5", "E4:1 G4:0.5 C5:0.5 A4:1.5 R:0.5", "R:0.5 E4:0.5 A4:0.5 C5:0.5 A#4:0.5 A4:0.5 G4:1", "F4:2.5 R:0.5 D4:0.5 F4:0.5",
        "A#4:1 A4:0.5 G4:0.5 F4:0.5 G4:0.5 A4:1", "C5:1.5 A#4:0.5 A4:0.5 G4:0.5 E4:1", "F4:0.25 G4:0.25 A4:0.25 C5:0.25 F5:1 E5:0.5 D5:0.5 C5:1", "C#5:3 R:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1
    if n == "前奏":
        # 4小節はプラックとRギターだけ → 全員
        PLK.bar(b, arp16(S.chords[b], "x.xxx.xxx.xxx.xx", (0, 2, 4, 3, 5, 4, 6, 5, 7, 6, 4, 2), lo="F4", hi="F6", short=0.25))
        gtr(GR, b, RSTRUM, "mid")
        if i >= 4: gtr(GL, b, LDRIVE if i < 7 else "x-x-x-x-x-x-....", "pw"); bassp(b, LDRIVE if i < 7 else "x-x-x-x-x-x-....", "rrrrrr5a" if i < 7 else "rrrrrr")
    elif n in ("Aメロ", "Aメロ2"):
        two = n == "Aメロ2"
        if not odd:      # 歌が言葉をつめる小節: ベースとドラムが中心。Rギターは頭の1発だけ（2番はLギターも8分で入る）
            bassp(b, "x-....x-x-....x-", "rr5o", short=0.5)
            gtr(GR, b, "x-..............", "mid", short=0.5)
            if two: gtr(GL, b, "x-x-x-x-x-x-x-..", "pw")
        else:            # 歌が食って伸ばす小節: 全員いっしょに2拍目のウラで打ち、最後の1拍は休む
            bassp(b, "x-x-..x-----....", "rrR"); gtr(GL, b, "x-....x-----....", "pw"); gtr(GR, b, "x-.x-.x-----....", "mid")
            if i % 4 == 3 and not two: LEAD.bar(b, steps("........x-x-x-x-", [N(m) for m in tones(halves(b)[1], "C4", "C5")[-4:]]))    # 4小節ごとに、リードギターが次へつなぐ
    elif n in ("Bメロ", "Bメロ2"):
        q = i
        if q < 7:
            pno(b, "x-------x-----.." if not odd else "x-----------....", 62 + q); bassp(b, "x-------..x-x---", "r5o"); saw(b, "x-----------....")
            if n == "Bメロ2": gtr(GR, b, "x-----------....", "mid")
        else:            # 最後の小節: sus4 → 3和音。前半だけ打って、4拍目は全員休み
            pno(b, "x---x---x-x-....", 69); gtr(GL, b, "x---x---x-x-....", "pw"); gtr(GR, b, "x---x---x-x-....", "mid"); bassp(b, "x---x---x-x-....", "rrRR")
    elif n in ("サビ1", "サビ2", "最後のサビ", "ギターソロ"):
        j = i % 8; lastc = n == "最後のサビ"
        if j == 7 and n in ("サビ1", "サビ2"):      # 8小節目: 頭の1発だけで全員止まり、歌の長い音がひとり残る
            gtr(GL, b, "x-..............", "pw", short=0.5); gtr(GR, b, "x-..............", "mid", short=0.5); bassp(b, "x-..............", "r", short=0.5)
        else:
            gtr(GL, b, LDRIVE if not odd else LDRIVE2, "pw"); gtr(GR, b, RSTRUM if not odd else RSTRUM2, "mid")
            bassp(b, LDRIVE, "rrrorr5a") if not odd else bassp(b, LDRIVE2, "rrrRoRa")
            if n != "ギターソロ": saw(b)
            if odd and n != "ギターソロ" and (n != "サビ1" or j in (3, 7)): sparkle(b, lastc)      # サビ1 は4小節ごと、サビ2 からは2小節ごと
        if n == "ギターソロ": LEAD.bar(b, SOLO[i])
        if lastc and i >= 16 and not odd: LEAD.bar(b, steps("x-----------x---", [N(m) for m in tones(halves(b)[0], "A#4", "A#5")[1:3]]))   # 最後の8小節: リードギターが上で伸ばす
    elif n == "間奏":
        gtr(GL, b, LDRIVE, "pw"); gtr(GR, b, RSTRUM, "mid"); bassp(b, LDRIVE, "rrrorr5a")
        if i in (0, 1, 4, 5): LEAD.bar(b, MOTIF[i % 2])
        if i == 7: gtr(GL, b, "x-x-x-x-x-x-....", "pw"); gtr(GR, b, "x-.x-.x-x-.x....", "mid"); bassp(b, "x-x-x-x-x-x-....", "rrrrrr")
    elif n == "雪どけ":
        # 頭の4小節はピアノだけ → クリーンのギターとベースが入る → 最後の4小節でドラムが戻る
        pno(b, "x-----x---x-----" if not odd else "x---------x-----", 65)
        if i >= 4:
            t = tones(halves(b)[0], "F4", "F6"); CLN.bar(b, steps("..x-x-x-..x-x-x-", [N(t[q % len(t)]) for q in (0, 2, 1, 3, 2, 4)]))
            bassp(b, "x---------x-x---", "r5o")
        if i >= 12: saw(b, "x-----------....")
    elif n == "おわり":
        if i == 0: gtr(GL, b, "x---------------", "pw"); gtr(GR, b, "x---------------", "mid"); bassp(b, "x---------------", "r")
        if i == 1: PLK.bar(b, arp16(S.chords[b], "x.x.x.x.x.x.x-..", (7, 6, 5, 4, 3, 2, 1), lo="F#4", hi="F#6"))
        if i == 2: gtr(GL, b, "x-----------....", "pw"); gtr(GR, b, "x-----------....", "mid"); bassp(b, "x-----------....", "r")
        if i == 3: SPOON.bar(b, "R:1 F#7:0.25 R:2.75")                          # スプーンを置く「カチ」

# ================= ドラム =================
# v8（2026-11-15）人間「テンポ200だけどドラムをテンポ200に合わせて手数多く入れる必要性はないよ。そういうのも勉強してきて。」
#   プロのドラマーの演奏（Groove MIDI）を測ると、1秒あたりの打数はテンポが変わってもほぼ同じ（7〜10打）。＝速い曲ほど、1拍あたりは少なく叩く。
#   テンポ 175〜215 では、キックは1拍に 0.57（2拍に1回）、刻みは 0.9（4分）、全部で 3.1。v7 のサビはキック 1.25・刻み 1.66 で、倍ちかく叩いていた。
#   → 刻みは4分。キックは1拍目と3拍目（＋歌が食う所の1発）。スネアは2・4拍目。Aメロ・Bメロは半分の速さ（スネアは3拍目だけ）。
#     ギターは8分で走りつづけ、ドラムは大きくとる（速さはギターが出す。ドラムは広さを出す）。8分の刻みに上げるのは、最後の8小節だけ。
Q4 = "x...x...x...x..."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "前奏":
        if i >= 4:
            vgroove(D, b, "beat8", ghosts=0.0, seed=b, k="X.......X.......", s="....X.......X...", h=Q4, vary=False)
            if i == 4: crash(D, b, "C2", 4)
            if last: put_fill(D, b, "small")
    elif n in ("Aメロ", "Aメロ2"):
        # 半分の速さ: スネアは3拍目だけ。歌が食う小節は、2拍目のウラの1発でいっしょに打って、あとは休む
        if not odd: vgroove(D, b, "beat8", ghosts=0.1, seed=b, k="X.........X....." if n == "Aメロ" else "X.....X...X.....", s="........X.......", h=Q4, vary=False)
        else: D.set(b, "X.....X.........", "......X.........", "x...x...........")
        if i == 0: crash(D, b, "C2", 4)
    elif n in ("Bメロ", "Bメロ2"):
        if i < 6: vgroove(D, b, "beat8", ghosts=0.1, seed=b, k="X.........X....." if not odd else "X...............", s="........X.......", h=Q4, vary=False)
        elif i == 6: D.set(b, "X.......X.......", "........X...X.X.", Q4)
        else: D.set(b, "X...X...X.X.....", "X...X...X.X.....", "................")
    elif n in ("サビ1", "サビ2", "最後のサビ", "ギターソロ", "間奏"):
        j = i % 8
        if j == 7 and n in ("サビ1", "サビ2"): D.set(b, "X...............", "X...............", "................")
        else:
            hh = Q4 if not (n == "最後のサビ" and i >= 16) else "x.x.x.x.x.x.x.x."
            if not odd: vgroove(D, b, "beat8", ghosts=0.0, seed=b, k="X.......X.......", s="....X.......X...", h=hh, vary=False)
            else: vgroove(D, b, "beat8", ghosts=0.0, seed=b, k="X.....X...X.....", s="....X.......X...", h=hh, vary=False)      # 2拍目のウラで、キックも食う
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if last and n in ("間奏", "ギターソロ", "サビ2"): put_fill(D, b, "small")
        if last and n == "最後のサビ": D.set(b, *KIME_END)
    elif n == "雪どけ":
        if i >= 12:
            D.set(b, "X.........X.....", "........X.......", Q4)
            if last: put_fill(D, b, "build")
    elif n == "おわり":
        if i in (0, 2): D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)

for name in ("サビ1", "サビ2", "最後のサビ"): cym_swell(CYM, S.sc(name)[0], 2, "C4")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の16（15時）。かけぬける明るいパンク・ロック・200。F長調（IV → IVm）、最後のサビは半音上。"
          "30秒のスケッチ3案から人間が選んだ方向。左右で役のちがうギター、歌といっしょに食うキメ、動くベース、前半（いくさ）と後半（雪どけ）で別の曲のように変わる。2分48秒。自作")
finish(S, LY, V, 0, level={"verse": -0.15}, special={"雪どけ": -0.5, "最後のサビ": 0.5})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "Rギター", mid=84, down=12, up=10, seed=3); humanize(path, "Lギター", mid=86, down=8, up=8, seed=4); humanize(path, "ベース", mid=86, down=10, up=8, seed=5)
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 4, "pre": 12, "chorus": 18, "最後のサビ": 22, "bridge": 8}, scoop=0.25, slash=0.6, vib_min_beats=2.0, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ1", 8, None, K), ("サビ2", 0, None, K), ("雪どけ", 8, None, K), ("最後のサビ", 0, None, KD)], vol=0.36)
    harmony(path, S, [("最後のサビ", 0, None, KD)], steps=7, vol=0.2, lowest=50)
    for sgn in (-1, 1): harmony(path, S, [("最後のサビ", 0, None, KD)], steps=0, vol=0.2, pan=0.6 * sgn, transpose=0.07 * sgn)     # ダブリング
    voice_by_scene(path, S, {"雪どけ": "cute"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
final_gain(path, {"前奏": 2.2, "ギターソロ": -2.6, "サビ2": 0.4, "最後のサビ": 1.0})   # v7: ソロが最後のサビより大きく飛び出していた・前奏が小さかったのを直す
