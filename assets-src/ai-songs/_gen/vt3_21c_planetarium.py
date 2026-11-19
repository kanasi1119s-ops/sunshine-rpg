# vt3 21「屋上プラネタリウム」Rooftop Planetarium（仮）— エレクトロロック（4分の4・146）。ロ短調。転調なし。
# 第3弾（0時〜24時の街）の 20時。
#
# v7（2026-11-19）: 人間「ギターってそんな単純な弾き方でいいの？」「アルペジオとかではなく、和音をそんな単純にジャン、、、ジャンみたいな弾き方普通しないでしょ」「全体の音チェックして、小さかったり大きかったりして違和感感じるよ」
#   → かき鳴らしの型を作り直した（手を止めない）。場面とパートの大きさを測り直してそろえた。
# v6（2026-11-19）: 人間「21の歌、一音一音はっきりと聞こえるようにした方がいいな。あと、ギター和音で弾いてないよね？弾くとしたら今までの和音の弾き方を忘れて、一から作り直して欲しい」
#   → ギターは gtr2_lib（新しい部品）で弾く。歌は子音をはっきり。
# v5（2026-11-19）: 物語の出来事に合わせて音が変わるように、形から作り直した。
#   人間の言葉: 「音は悪くない。前奏が今までの曲と変わりがなく、曲調は単調」
#     「前奏の始まり方って曲によって違うと思うし、曲の中にストーリーがあってそれに音が変化してメロディを作り上げていくと思うんだよね。その変化が少なすぎて単調になってる」
#     「曲名をそのまま歌詞に使うのが良くないかな。場景を分かりやすくする分すごくカッコ悪くなる感じがする」
#   v3・v4（vt3_21b_planetarium.py）は、歌詞では Aメロ1 で明かりが消えるのに、音が消えるのは3分すぎだった（物語と音の時間が合っていない）。
#   音はそのまま: リンキン・パーク寄り（参考の音 bright-nu-wall・ギター nu-metal-wall。人間「音源リンキン・パークも入れて欲しいな」）。
#
# 物語の出来事 → その時の音（この表を見せて「良い」をもらってから作った）:
#   明るすぎる街        → 始まりからバンドとシンセが全部鳴る。すき間がない（まぶしい街・ねむらない窓）
#   明かりが消える      → 歌詞の「いきをとめたまち」で、電気の音がぜんぶ止まる（曲が始まって 26 秒）
#   まっ暗な部屋        → 声とナイロン弦のギター1本だけ。旋律は低く、せまく、短く切れる（まっくら）
#   階段をのぼる        → ベースが1小節に1段ずつ上がる。足音のキック。旋律も1行ごとに上がる（階段）
#   扉を開ける          → 旋律がはじめて高い音（5'）にとどく。星の音（高い分散和音）がいっぱいに鳴る（サビ1。電気の音はまだない＝ギターは生、ドラムとベースとピアノ）
#   星をかぞえる        → 星の音が1小節に1つずつ増える。ピアノの旋律（星をかぞえる）
#   となりの屋根にも人  → 手拍子・ドラム・ピアノ・ハモリが、4小節ごとに1つずつ増える（となりの屋根・手拍子・サビ2）
#   電気がもどる        → 歪んだギターとシンセがもどる。でも星の音は消えずに鳴りつづける（電気がもどる・最後のサビ）
#   終わり              → 星の音が1つだけ残る
# 歌詞: 曲名は歌わない。「停電」「屋上」「星」という言葉も使わず、場面が浮かぶ言い方にする。
# 声: クリア 1 種類。
from vocalo_lib import *
import random as _r, re as _re

S = Song("21", "planetarium", "屋上プラネタリウム（仮）", "Rooftop Planetarium", 146, 4, "B", "minor", "エレクトロロック（ボカロ）")
S.kit = "naked-x"; S.flags = "--bass bnb-loud --ref-tone bright-nu-wall --piano salamander " + S.flags
K = Key("B", "minor"); SC = {11, 1, 2, 4, 6, 7, 9}
R_CH = ["Bm", "Bm", "G", "G", "Em7", "Em7", "A", "A"]
A_CH = ["Bm", "Bm", "D", "D", "G", "G", "F#m", "F#m", "Em7", "Em7", "G", "G", "Bm", "A", "G", "A"]
B_CH = ["Em7", "Em7", "G", "G", "Asus4", "A", "Asus4", "A"]
C_CH = ["D", "F#m", "Bm", "G", "D", "F#m", "Em7", "A", "D", "F#m", "Bm", "G", "Em7", "G|A", "Bm", "Bm"]
C_END = C_CH[:14] + ["D", "D"]
S.scene("まぶしい街", 8, "intro", R_CH)
S.scene("ねむらない窓", 8, "verse", R_CH)
S.scene("まっくら", 8, "verse", ["Bm", "Bm", "Em7", "Em7", "G", "G", "F#m", "F#m"])
S.scene("階段", 8, "pre", ["Bm", "D", "Em7", "F#m", "G", "A", "Bm", "A"])
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("星をかぞえる", 8, "break", ["G", "G", "D", "D", "Em7", "Em7", "A", "A"])
S.scene("となりの屋根", 16, "verse", A_CH)
S.scene("手拍子", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("電気がもどる", 16, "break", R_CH + R_CH)
S.scene("最後のサビ", 32, "chorus", C_CH + C_END)
S.scene("おわり", 8, "outro", ["Bm", "Bm", "G", "G", "Bm", "Bm", "Bm", "Bm"])
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(2121)

# ================= 歌（ロ短調の度数。oct=3 で 1 = B3）=================
P1, P2 = "x-x-x-x---x-x---", "x---x-------...."
Q1, Q2 = "..x-x-x-x-x-x---", "x-x---------...."
R1, R2 = "x---x-x-x---x-x-", "x---x-------...."
# ねむらない窓（明るすぎる街。バンドが全部鳴る中で、まん中の高さ）
NP = [P1, P2, Q1, Q2, R1, R2, Q1, Q2]
ND = ["3 3 2 3 5 4", "3 2", "2 3 4 3 2 3", "4 3", "4 4 5 6 5 4", "3 4", "4 5 4 2 4 5", "4 2"]
N1 = ["ねむらないまどが", "そらをぬりつぶす", "まぶしさのなかで", "いきをとめたまち"]
# まっくら（低く・せまく・短く切れる）
D1, D2, D3 = "x-x-x-----......", "x-x-x-------....", "x-x-x-x---......"
MP = [D1, D2, D3, D2, D3, D2, D3, D2]
MD = ["3 3 2", "3 2 3", "4 4 3 4", "3 2 4", "3 3 2 3", "3 4 3", "2 2 3 2", "2 4 5"]
M1 = ["しずか", "すぎて", "てさぐり", "かべを", "たどれば", "ひやり", "じぶんの", "こきゅう"]      # 1小節ごとに切れる、短い言葉
# 階段（1行ごとに上がる）
KP = [P1, P2, P1, P2, R1, R2, R1, R2]
KD = ["3 3 4 3 4 5", "5 5", "4 4 5 4 5 6", "7 5", "6 6 7 6 7 1'", "7 7", "1' 1' 7 1' 2' 1'", "2' 2'"]
K1 = ["ひとつずつのぼる", "あしおとをかぞえ", "てすりがとぎれて", "とびらをおしたら"]
# となりの屋根（つめて歌う行 W と、おくれて入る行 Z）
W1, W2 = "x-x-x-x-x-x-x---", "x-----------...."
Z1, Z2 = "....x-x-x-x-x-x-", "x---x-------...."
AP2 = [W1, W2, Z1, Z2, W1, W2, Z1, Z2, R1, R2, Q1, Q2, W1, W2, Z1, Z2]
AD2 = ["5 5 5 7 5 3 5", "5", "7 7 5 7 1' 7", "5 3", "6 6 6 1' 7 6 5", "3", "7 7 5 4 5 7", "5 2",
       "4 4 6 6 5 4", "3 4", "6 5 3 5 6 7", "7 6", "1' 1' 7 5 7 1' 7", "7", "6 6 7 6 7 1'", "2' 2'"]
A2 = ["となりのやねにも", "だれかがてをふる", "なまえもしらない", "おなじほうをみる", "あかるすぎたから", "みえずにいたもの", "くらやみのおくで", "まちつづけていた"]
B1p, B2p = "x---x---x-x-x---", "x-------x---...."
BP_ = [B1p, B2p] * 4
BD = ["4 4 6 5 4", "3 4", "6 6 1' 7 6", "5 6", "7 7 1' 7 5", "7 7", "7 7 1' 2' 1'", "2' 2'"]
B2 = ["てをたたくおと", "やねからやねへ", "ひとつふたつと", "こえがふえてく"]
# サビ（扉を開けた所で、はじめて 5' にとどく。行ごとにリズムを変える）
E1, E2 = "x---x-x-x-x-x---", "x-x-x-x-x---...."
F1, F2 = "x---x---x-x-x---", "x-x-x-x-----...."
G1, G2 = "x---x---x-x-x---", "x-x-x-------...."
X1, X2 = "..x-x-x-x---x-x-", "x---x-x-x-x-...."
Y1, Y2 = "x-----x-x-x-x-x-", "x---x---x-x-x-.."
CP = [E1, E2, X1, X2, Y1, Y2, F1, F2, E1, E2, X1, X2, Y1, Y2, G1, G2]
CD = ["7 7 3' 3' 5' 4'", "3' 3' 2' 1' 2'", "1' 1' 3' 3' 4' 3'", "3' 3' 1' 7 1'", "5 5 7 7 3' 4'", "5' 4' 2' 1' 2'", "4' 4' 3' 1' 3'", "2' 2' 4' 4'",
      "7 7 3' 3' 5' 4'", "3' 3' 2' 1' 2'", "1' 1' 3' 3' 4' 5'", "4' 3' 1' 7 1'", "4' 4' 3' 3' 1' 3'", "3' 3' 2' 2' 4'", "3' 3' 2' 1' 2'", "1' 7 1'"]
CDE = CD[:15] + ["2' 3' 3'"]
C1 = ["てんじょうがきえたへやで", "まちがまぶたをとじたら", "かくれてたひかりたちが", "いまふりそそいでる",
      "てんじょうがきえたへやで", "ひとりぶんのちいさなひ", "ゆびでむすんだらかたち", "なまえはまだない"]
C2 = [C1[0], "あかりがねむるあいだに", "とおくのうたがとどいた", "だれもがみあげてる"] + C1[4:]


def put(name, pats, degs, phrases):
    lines, text = song_phrases(pats, degs, phrases); bars = S.sc(name); mel = [K.mel(x, oct=3) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("ねむらない窓", NP, ND, N1); put("まっくら", MP, MD, M1); put("階段", KP, KD, K1); put("サビ1", CP, CD, C1)
put("となりの屋根", AP2, AD2, A2); put("手拍子", BP_, BD, B2); put("サビ2", CP, CD, C2); put("最後のサビ", CP + CP, CD + CDE, C1 + C2)

# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


def strum(tracks, b, pat, **kw):
    c1, c2 = halves(b)
    if c1 == c2: gtr_strum(tracks, S, b, pat, c1, RNG, **kw)
    else: gtr_strum(tracks, S, b, pat[:8] + "." * 8, c1, RNG, **kw); gtr_strum(tracks, S, b, "." * 8 + pat[8:], c2, RNG, **kw)


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), SC, lo=28))


def saw(b, pat="x---------------"):
    c1, c2 = halves(b); v, v2 = sorted(voice(c1, 62, 3)), sorted(voice(c2, 62, 3))
    for j in range(3): SAW[j].bar(b, steps(pat, [N(v[j])]) if c1 == c2 else steps("x-------x-------", [N(v[j]), N(v2[j])]))


def sub(b):
    c1, c2 = halves(b); SUB.bar(b, f"{N(low(c1, 'E1'))}:4" if c1 == c2 else f"{N(low(c1, 'E1'))}:2 {N(low(c2, 'E1'))}:2")


def arp(b, pat="x-x-x-x-x-x-x-x-", order=(0, 2, 1, 3, 2, 4, 3, 1), lo="D5", hi="C7"):
    ARP.bar(b, arp16(halves(b)[0], pat, order, lo=lo, hi=hi))


GL = [S.track(f"Lギター{i + 1}弦め（ニューメタルの壁）", "distGuitar", **rock_gtr_spec(0.16, -0.6, tone="nu-metal-wall")) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め（ニューメタルの壁）", "distGuitar", **rock_gtr_spec(0.15, 0.6, tone="nu-metal-wall")) for i in range(6)]
LG = S.track("リードギター（フック・合いの手）", "leadGuitar", **lead_gtr_spec(0.055, -0.08))
AG = [S.track(f"アコースティックギター{i + 1}弦め", "guitar", patch="nylonGuitar", amp="clean", volume=0.2, pan=0.0, reverb=0.25, chorus=0) for i in range(6)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.25))
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.02, pan=0, duck=0.4)
PNO = S.track("ピアノ（フック）", "piano", volume=0.2, pan=-0.1, reverb=0.3, sustain=0.9, fx=[{"type": "eq", "low": -3, "mid": -1.5, "midHz": 400, "high": 1}])
# ★ v3 の大きなまちがい: パートの設定（pan など）がちがうと MIDI のチャンネルを1つずつ使い、16 をこえた分は「前のパートの楽器の音」で鳴る。
#   v3 では ピアノ・パッド3本・プラック・アコースティックギター3本 が同じチャンネルに入り、パッドもプラックもピアノの音で鳴っていた（だからシンセの音量を変えても変わらなかった）。
#   build の「MIDI のチャンネルが足りません」という注意を見落としていた。v4 では pan をそろえてチャンネルを 15 以内に収めた（広がりは widen でつける）
# 作る前の確認で、16 と音色の重なりが 64%（目安 60% 未満）と出た → スーパーソウと矩形波のプラックをやめ、暗いシンセのパッドと別のプラックにした（リンキン・パーク寄りの音の組み合わせ＝vb25 09 と同じパッド）
SAW = [S.track(f"暗いシンセのパッド{i + 1}", "pad", patch="surgePadNewtonWasEvil", volume=0.12, pan=0.0, reverb=0.3, sustain=2.0, duck=0.4,
               fx=[{"type": "filter", "kind": "highpass", "freq": 200, "q": 0.7}, {"type": "widen", "amount": 1.4}]) for i in range(3)]
ARP = S.track("分散和音（街の明かり・星）", "lead", patch="surgeNicePluck", volume=0.12, pan=0.25, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
HATR = S.track("電子のハイハット", "guitar", patch="kawaiiFx", volume=0.045, pan=-0.2, reverb=0.08, modulate=False)
CLAP = S.track("クラップ・手拍子", "guitar", patch="kawaiiFx", volume=0.07, pan=0.05, reverb=0.2, modulate=False)
FXT = S.track("効果音", "guitar", patch="kawaiiFx", volume=0.07, pan=0.05, reverb=0.2, modulate=False)

# ピアノのフック（2小節ひと組。和音ごとに形を移す）
HOOK = ["F#5:0.75 D5:0.75 B4:0.5 C#5:0.5 D5:0.5 F#5:1", "E5:0.75 D5:0.75 B4:2.5", "G5:0.75 D5:0.75 B4:0.5 C#5:0.5 D5:0.5 G5:1", "F#5:0.75 D5:0.75 B4:2.5",
        "G5:0.75 E5:0.75 B4:0.5 D5:0.5 E5:0.5 G5:1", "F#5:0.75 E5:0.75 B4:2.5", "A5:0.75 E5:0.75 C#5:0.5 D5:0.5 E5:0.5 A5:1", "G5:0.75 E5:0.75 C#5:1 E5:1.5"]


def shift(s, n): return " ".join(x if x.startswith("R") else _re.sub(r"^[A-G][#b]?\d", lambda m: nm(midi(m.group(0)) + n), x) for x in s.split())


def hook(b, i, lead=True, pno=True):
    if pno: PNO.bar(b, HOOK[i % 8])
    if lead: LG.bar(b, shift(HOOK[i % 8], -12))


BV = [("x-x-x-x-x-x-x-x-", "11118151"), ("x-----x-x---x-x-", "1185d"), ("x---x-x---x-x-x-", "11585a"), ("x-x---x-x-x---x-", "115351")]      # ベースの型（リフ・Aメロ）
BC = [("x-----x-x-------", "118"), ("x-----x-x---x-x-", "1185d"), ("x---------x-x-x-", "15wd"), ("x-----x-----x-x-", "115a")]                # サビ（半分の速さ）
EH = ["C#5:0.5 C#5:0.25 C#5:0.25 " * 4, "C#5:0.5 C#5:0.25 C#5:0.25 " * 3 + "C#5:0.5 D5:0.5"]                                                 # 電子のハイハット
STAR = ["x...............", "x.......x.......", "x.....x.....x...", "x...x...x...x...", "x.x.x...x.x.x...", "x.x.x.x.x.x.x...", "x-x-x-x-x-x-x-x-", "x-x-x-x-x-x-x-x-"]
LGS = ["R:0.5 B4:0.5 D5:0.5 E5:0.5 F#5:1 E5:0.5 D5:0.5", "R:0.5 D5:0.5 E5:0.5 G5:1 F#5:0.5 D5:0.5 B4:0.5", "R:0.5 E5:0.5 G5:0.5 B5:1 A5:0.5 G5:0.5 E5:0.5", "R:0.5 A5:0.5 G5:0.5 E5:0.5 C#5:0.5 E5:0.5 A5:1"]      # かけ合いのリードギター
LANS = {7: "R:3 E5:0.5 F#5:0.5", 15: "R:1.5 B4:0.5 D5:0.5 F#5:0.5 E5:1"}      # サビの歌の休みに、リードギター


# ===== v6: ギターの和音の弾き方を一から作り直した（gtr2_lib）。人間「ギター和音で弾いてないよね？弾くとしたら今までの和音の弾き方を忘れて、一から作り直して欲しい」 =====
#   今まで: 左は 根音・5度・オクターブ の3本だけ（3度なし）。試しに書き出して測ると、8つの和音のうち和音どおりに聞こえたのは 3つ、3度の強さは 0.39
#   新しい弾き方: 左＝いちばん下が根音で、1オクターブ上の3度まで入る4本。右＝まん中の弦の三和音（前の形にいちばん近い転回形へ動く）。弦ごとに鳴りつづける。ダウンとアップは手の向きどおり
#   同じ試しで: 8つとも和音どおりに聞こえ、3度の強さは 0.71
# ★ 音量のしくみを測って分かった事（2026-11-19。tools/vt3/volume_test.py）: パートの volume は 0.2 で頭打ち（0.2 → 0.4 にしても 0.3dB しか変わらない）。
#   それより大きくしたい時は fx の boost（録音の音は効く。歪んだギターは、アンプの前に入るので大きくならない）。歪んだギターは volume 0.05 → 0.2 で 11dB 変わる。
#   v6 までの 左右のギター（0.085・0.08）は小さく、ナイロン弦のギター（0.32 → 0.5）は何も変わっていなかった。
import gtr2_lib as G2
SL, SR, SA = G2.Strummer(GL, S, 11), G2.Strummer(GR, S, 12), G2.Strummer(AG, S, 13); TRI = [None]


PUSH = [False]


def gL(b, pat, feel="down"):
    c1, c2 = halves(b); SL.bar(b, pat, G2.low_shape(c1), G2.low_shape(c2) if c2 != c1 else None, feel=feel)


def gR(b, pat, feel=8, push=False):
    """右のギター（三和音）。push: 次の小節の和音を、8分早く弾いて次の頭までのばす（食い）"""
    c1, c2 = halves(b); a = TRI[0] if PUSH[0] and TRI[0] else G2.triad(c1, TRI[0]); TRI[0] = a; z = None; sw = 8
    if PUSH[0]: pat = "-" + pat[1:]; PUSH[0] = False              # 前の小節で先に弾いてあるので、頭は弾かずにのばす
    if c2 != c1: z = TRI[0] = G2.triad(c2, a)
    elif push and b + 1 < S.nb and nxt(b) != c1: z = TRI[0] = G2.triad(nxt(b), a); sw = 14; PUSH[0] = True
    SR.bar(b, pat, a, z, feel=feel, switch=sw)


def gA(b, pat, feel=8):
    c1, c2 = halves(b); SA.bar(b, pat, G2.open_shape(c1), G2.open_shape(c2) if c2 != c1 else None, feel=feel)


# かき鳴らしの型（16分のマス。D d＝ダウン、U u＝アップ、-＝空振り（鳴らしたまま）、.＝止める）
# v7: 人間「和音をそんな単純にジャン、、、ジャンみたいな弾き方普通しないでしょ」→ まばらに置く型をやめた。手は止めず、小節のほとんどの8分を弾いて、強弱と空振りでノリを作る
#   左（歪み・低い形）: 8分をぜんぶダウン。強い所を 3・3・2 や 2・3・3 に置く
#   右（歪み・三和音）: 8分で下・上に振る。空振りを1〜2か所
#   生のギター: 8分で下・上に振る
EL = ("D-d-d-D-d-d-D-d-", "D-d-D-d-d-D-d-d-", "D-d-d-D-d-D-d-d-", "D-D-d-d-D-d-d-D-")           # 左: 1小節に8回
EL_SOFT = ("D-d-d-d-D-d-d-d-", "D-d-d-d-d-d-D-d-")                                                 # 歌の後ろ: 1・3拍めだけ強く
ER = ("D-U-D-U---U-D-U-", "D---D-U-D-U-D-U-", "D-U---U-D-U-D-U-", "D-U-D-U-D-U---U-")           # 右: 1小節に7回
ER16 = ("D-dUdUD-dUdUD-dU", "D-dU-UdUD-dUdUdU")                                                    # まぶしい街の右だけ16分（すき間なく）
HIT = "D---............"; LONG = "D---------------"                                                 # キメ（全員で止まる所）と、曲の終わりだけ
AC = ("D---D-U---U-D-U-", "D-U-D-U---U-D-U-", "D---D-U-D-U-D-U-", "D-U-D-U-D-U---U-")           # 生: 1小節に6〜7回
AC_SOFT = ("D---d-U---U-d-U-", "D-U-d-U---U-d-U-"); AC_FULL = "D-U-D-U-D-U-D-U-"
for _p in EL + EL_SOFT + ER + ER16 + AC + AC_SOFT + (AC_FULL,): assert G2.strokes(_p) >= 6, _p        # まばらな型が入っていないこと

COUNT = ["B5:2 G5:1 D5:1", "B5:1.5 A5:0.5 G5:2", "A5:2 F#5:1 D5:1", "A5:1.5 G5:0.5 F#5:2", "G5:2 E5:1 B4:1", "G5:1.5 F#5:0.5 E5:2", "E5:1 A5:1 C#6:2", "C#6:1 B5:1 A5:2"]      # 星をかぞえるピアノ


AGP = S.track("ナイロン弦のギター（1本の指で）", "guitar", patch="nylonGuitar", amp="clean", volume=0.2, pan=0.0, reverb=0.3, chorus=0, fx=[{"type": "boost", "gain": 6}])      # 1 回め: かき鳴らす用の音量（0.09）のままだと −37dB で、歌より 7dB 小さかった


def pick(b, fast=False):
    """ナイロン弦のギターを1本の指で（和音をばらして）"""
    v = sorted(voice(halves(b)[0], 62, 3))
    AGP.bar(b, " ".join(f"{N(x)}:0.5" for x in (v[0], v[1], v[2], v[1], v[2], v[1], v[0], v[1])) if fast else f"{N(v[0])}:1 {N(v[1])}:1 {N(v[2])}:1 {N(v[1])}:1")




def electric(b, i, hookon=True, busy=True, riff=False):
    """電気の音がぜんぶ鳴る（歪んだギター・シンセ・サブベース）"""
    odd = i % 2 == 1
    if hookon: hook(b, i)
    bass(b, *BV[i % 4]); sub(b); saw(b); gL(b, (EL if busy or riff else EL_SOFT)[i % (4 if busy or riff else 2)]); gR(b, ER16[odd], feel=16) if busy else gR(b, ER[i % 4], push=riff and odd)
    feel(D, b, "rock8" if not odd else "rock8b"); HATR.bar(b, EH[i % 2]); arp(b, "xxxxxxxxxxxxxxxx" if busy else "x-x-x-x-x-x-x-x-", order=(0, 2, 1, 3, 2, 4, 3, 1) * 2 if busy else (0, 2, 1, 3, 2, 4, 3, 1))


def chorus(b, i, n):
    lv = {"サビ1": 1, "サビ2": 2, "最後のサビ": 3}[n]; j = i % 16; fast = lv == 3 and i >= 16; end = lv == 3 and i == 31
    sub(b) if lv == 3 else None; bass(b, *(BC[i % 4] if not fast else BV[i % 4]))
    gA(b, AC[i % 4])                                   # 生のギターは、どのサビでも鳴る（屋上にいる人）
    arp(b, "x-x-x-x-x-x-x-x-" if lv == 1 else "xxxxxxxxxxxxxxxx", order=(0, 2, 1, 3, 2, 4, 3, 1) * 2)       # 星の音
    feel(D, b, ("half" if i % 2 == 0 else "halfopen") if not fast else "four")
    if lv >= 2: CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
    if lv <= 2 and j % 2 == 1: PNO.bar(b, "R:2 " + ["F#5:0.5 D5:0.5 B4:1", "E5:0.5 D5:0.5 B4:1", "G5:0.5 E5:0.5 B4:1", "E5:0.5 C#5:0.5 A4:1"][(j // 2) % 4])
    if lv == 3:                                                                                           # 電気がもどったあと: 歪んだギターの壁とシンセ
        saw(b)
        if not end: gL(b, EL[i % 4]); gR(b, ER[(i + 1) % 4], push=i % 4 == 1)
        if j in LANS and not end: LG.bar(b, LANS[j])
        elif fast and not end: t = sorted(voice(halves(b)[0], 74, 3))[-1]; LG.bar(b, f"{N(t)}:4" if i % 2 == 0 else f"R:2 {N(t)}:1 {N(t + 2)}:1")
    if j % 8 == 0: crash(D, b, "C2", 4)
    if j == 0 and lv == 3: FXT.bar(b, fx_bar((0, "impact", 2)))
    if j % 8 == 7 and not end: fill_cresc(D, b, 1 if j == 7 else 2)
    if end: D.set(b, "X.........X.....", "........X.......", "X.x.X.x........."); gL(b, LONG); gR(b, LONG)


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "まぶしい街":                                               # 明るすぎる街: 1拍めから全部鳴る。すき間がない
        electric(b, i); CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i in (0, 4): crash(D, b, "C2", 4)
        if last: fill_cresc(D, b, 1, toms=False)
    elif n == "ねむらない窓":                                           # 歌が入る。まだ全部鳴っている。最後の小節「まち」で、電気の音がぜんぶ止まる
        if not last:
            electric(b, i, hookon=False, busy=False)
            if odd: PNO.bar(b, "R:2 " + ["F#5:0.5 D5:0.5 B4:1", "G5:0.5 D5:0.5 B4:1", "G5:0.5 E5:0.5 B4:1"][(i // 2) % 3])
            if i == 0: crash(D, b, "C2", 4)
        else:
            D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4); gL(b, HIT); gR(b, HIT)
            BASS.bar(b, f"{N(low(halves(b)[0], 'E1'))}:1 R:3"); FXT.bar(b, fx_bar((0, "down", 3)))
    elif n == "まっくら":                                               # 声とナイロン弦のギター1本だけ
        pick(b)
    elif n == "階段":                                                   # ベースが1小節に1段ずつ上がる。足音のキック。ギターは細かくなる
        pick(b, fast=True); BASS.bar(b, f"{N(low(halves(b)[0], 'B1'))}:3.5 R:0.5"); D.set(b, "X.......X.......", "................" if i < 6 else ("....x.......x.x." if i == 6 else "x.x.x.x.xxxxXXXX"), "................")
    elif n in ("サビ1", "サビ2", "最後のサビ"): chorus(b, i, n)
    elif n == "星をかぞえる":                                           # 星の音が1小節に1つずつ増える。ピアノが星をかぞえる
        pick(b, fast=i >= 4); BASS.bar(b, f"{N(low(halves(b)[0], 'E1'))}:4"); arp(b, STAR[i], order=(4, 2, 3, 1, 4, 2, 5, 3)); PNO.bar(b, COUNT[i])
        if i >= 4: D.set(b, "X.......X.......", "................", "................")
    elif n == "となりの屋根":                                           # 人が増える: 4小節ごとに 手拍子 → ドラム → ピアノ → 星の音
        gA(b, AC_SOFT[odd] if i < 8 else AC[i % 4]); bass(b, *BV[(i + 1) % 4])
        if i < 4: D.set(b, "X.......X.......", "................", "................"); CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        else: feel(D, b, "break" if not odd else "break2")
        if i >= 8 and odd: PNO.bar(b, "R:2 " + ["F#5:0.5 D5:0.5 B4:1", "E5:0.5 D5:0.5 B4:1", "G5:0.5 E5:0.5 B4:1", "E5:0.5 C#5:0.5 A4:1"][(i // 2) % 4])
        if i >= 12: arp(b, "x.......x.......", order=(4, 2))
        if i == 4: crash(D, b, "C2", 4)
        if last: fill_cresc(D, b, 1)
    elif n == "手拍子":                                                 # 屋根から屋根へ手拍子がひろがる（4分 → 8分）。星の音が増える
        gA(b, AC_FULL if i >= 4 else AC[i % 4]); bass(b, "x-------x---x-x-" if i < 4 else "x---x---x-x-x-x-", "115d" if i < 4 else "115w5d")
        CLAP.bar(b, "R:1 B4:1 R:1 B4:1" if i < 4 else "B4:0.5 B4:0.5 " * 4); arp(b, STAR[i], order=(4, 2, 3, 1, 4, 2, 5, 3))
        D.set(b, "X...X...X...X...", "................" if i < 6 else ("x.x.x.x.x.x.x.x." if i == 6 else "x.x.x.x.xxxxXXXX"), "................")
    elif n == "電気がもどる":                                           # 歪んだギターとシンセがもどる。星の音は消えない。後半はリードギターとプラックのかけ合い
        if i < 8:
            electric(b, i, busy=False, riff=True)
            if i == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
        else:
            j = i - 8
            if j % 2 == 0:
                LG.bar(b, LGS[j // 2]); D.set(b, "X...............", "................", "X...x...x...x..."); gL(b, HIT); gR(b, HIT)
                BASS.bar(b, f"{N(low(halves(b)[0], 'E1'))}:1 R:3"); crash(D, b, "C2", 4); arp(b, "x---x---x---x---")
            else:
                feel(D, b, "break" if j % 4 == 1 else "break2"); bass(b, *BV[(j // 2) % 4]); sub(b); saw(b); gL(b, EL[(j // 2) % 4]); gR(b, ER[(j // 2 + 2) % 4])
                arp(b, "xxxxxxxxxxxxxxxx", order=(0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 3) if j % 4 == 1 else (5, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4))
            if last: fill_cresc(D, b, 2)
    elif n == "おわり":                                                 # 電気の音が先に消えて、星の音が1つだけ残る
        if i < 4:
            hook(b, i, lead=i < 2); bass(b, *BV[i % 4]); gL(b, EL[i % 4] if i < 3 else LONG); gR(b, ER[i % 4] if i < 3 else LONG)
            feel(D, b, "rock8" if not odd else "rock8b"); arp(b)
            if i == 0: crash(D, b, "C2", 4)
            if i == 3: D.set(b, "X.......X.......", "....X...........", "X.x.X.x.........")
        elif i < 7: arp(b, STAR[(7 - i) * 2 - 1 if i < 6 else 1], order=(4, 2, 3, 1, 4, 2, 5, 3))
        else: ARP.bar(b, "F#6:4")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の21（20時）。エレクトロロック（146）。ロ短調。明るすぎる街の明かりが消えて、空が見える夜の話。物語の出来事に合わせて音が変わる: "
          "全部鳴る → 電気の音が止まる → 声とギター1本 → 階段 → 星の音がいっぱいのサビ → 人が増える → 電気がもどっても星の音は残る。参考の音 bright-nu-wall。自作")
SL.end(S.nb); SR.end(S.nb); SA.end(S.nb)
finish(S, LY, V, 0)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=88, down=10, up=10, seed=21); humanize(path, "ピアノ", mid=86, down=10, up=8, seed=5)
js = load(path); print("  ギターの強さ（新しい弾き方）:", SL.velocity(js) + SR.velocity(js) + SA.velocity(js), "音  左", SL.count, "右", SR.count, "生", SA.count); save(path, js)
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 8, "pre": 14, "chorus": 24, "最後のサビ": 28}, scoop=0.1, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {}, default="clear")       # 1 曲 1 種類の声（2026-11-17 人間）
    sing_ends(path, S, human=0.5)
    js = load(path)
    # v6: 人間「21の歌、一音一音はっきりと聞こえるようにした方がいいな」→ 子音をやわらげる設定（softCons 0.3）を外し、子音を少し強く、音程の移りを速く、しゃくりを小さくした
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0; v["consonant"] = 1.25; v["glide"] = 0.75
    for v in js.get("vocals", []): v["debreathAt"] = [[t + 0.02, 1.2] for t in [61.82, 154.08, 149.57, 202.17, 29.74, 187.78, 193.33, 42.92, 115.66, 39.39, 229.49, 150.58]]      # 子音をはっきりさせたら、音の途中の息の音が 8か所で大きくなった → そこだけ下げる
    js["vocalLevel"] = 0.66      # 決まりの 0.6 より 0.8dB だけ大きく（歪んだギターの中で言葉が聞こえるように）
    save(path, js)
js = load(path); drum_punch(js); drum_center(js); save(path, js)
# v7: 曲の大きさを2小節ごとに測った（tools/vt3/level_curve.py。LUFS）。直す前: まぶしい街 −16.9・ねむらない窓 −15.6・まっくら −22.3・階段 −19.7・サビ1 −14.9・星をかぞえる −21.0・となりの屋根 −15.2・サビ2 −13.6・電気がもどる −12.3・最後のサビ −10.8
#   ・同じバンドなのに、始まり（−16.9）が 電気がもどる（−12.3）より 4.6dB 小さい ・静かな場面が小さすぎる（サビ1 → 星をかぞえる で −10.6dB）・歌が まっくら −28.6 〜 最後のサビ −21.7 と 7dB 動く
#   → 静かな場面を持ち上げ、始まりを上げ、最後のサビの持ち上げをやめた。下がる変わり目（階段→サビ1、星をかぞえる→となりの屋根 の −2dB）は、どちらも楽器が入れかわる所で、歌の大きさはむしろそろう
final_gain(path, {"まぶしい街": 1.5, "ねむらない窓": 1.5, "まっくら": 4.0, "階段": 4.0, "サビ1": 1.0, "星をかぞえる": 3.0, "となりの屋根": 1.0, "手拍子": 0.5, "サビ2": 0.5})
