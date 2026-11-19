# vt3 21「屋上プラネタリウム」Rooftop Planetarium（仮）— エレクトロロック（4分の4・146）。ロ短調（サビはニ長調に聞こえる明るい側）。転調なし。
# 第3弾（0時〜24時の街）の 20時。表は docs/sound/vt3-plan.md。
#
# v4（2026-11-19）: 人間「音は悪くない。前奏が今までの曲と変わりがなく、曲調は単調」→ 歌から始まる形にし、Aメロの和音・Aメロ2 の旋律・サビの行ごとのリズム・リフ2・Bメロの終わり方を作り変えた。
# v3（2026-11-19）: ゼロから作り直し。v1・v2 は電子のドラムのポップス。
#   人間の指示: 「18からは1曲ずつコンセプトとかジャンルをしっかり決めて作って行こうか。つまり作り直そう」「エレクトロロックの曲に変えよう」（21 のこと）「音源リンキン・パークも入れて欲しいな」
#   「トライデントの音源と一緒に作ったよ」＝ 2026-10-23 に参考録音を測って作った音（参考の音 bright-nu-wall・ギター nu-metal-wall。vb25 09 で使った組み合わせ）。表を見せて「良い」をもらってから作った。
#
# コンセプト: 街が停電した夜。まっ暗で困るはずの夜を、屋上で星が見える夜に書きかえる。
# ジャンル: エレクトロロック（バンドの演奏に、シンセを同じ重さで重ねる）。作る前に調べた決まりごと:
#   ・シンセとギターは、それぞれ鳴る場所（高さ）を分ける。厚いシンセはドラムで凹ませて、ドラムが前に出る場所を作る
#   ・ベースの下にサブベースを重ねる。ドラムは大きく
#   音の作り（リンキン・パーク寄り。曲そのものはまねない）: 重い歪みの壁＋ピアノのフック＋静かな Aメロと大きいサビ＋ Aメロは電子のビート
# 音の地図の場所: バンドと電子のまん中で、重い側（16・17 より強い歪み）。
#
# 曲を決める表:
#   形（v4）: サビ頭（歌から始まる。4小節は声とピアノとシンセ → バンドが入る）→ リフ（バンドが入る。ピアノとリードギターのフック）→ Aメロ（電子のビート → 生のドラム）→ Bメロ（半分の速さ）
#       → サビ（半分の速さで大きく）→ リフ → Aメロ2 → Bメロ2 → サビ2 → 停電（アコースティックギターと声と手拍子だけ）→ 星が出る（分散和音が1音ずつ増える）
#       → 最後のサビ（後半は倍の速さ）→ おわり（リフ → 分散和音が減って、1音だけ残る）
#   場面と強さ: 前奏 中 → リフ 強 → Aメロ 中弱 → Bメロ 中 → サビ1 強 → Aメロ2 中 → サビ2 強＋ → 停電 弱（いちばん静か）→ 星が出る 弱→中 → 最後のサビ 最強 → おわり 強 → 1音
#   旋律: Aメロは低め（2〜7）で言葉を置く。サビは長くのばす高い音。いちばん高い音（5'）はサビの3行めだけ。
#   和音: Bm・G・Em7・A（Aメロ）／ Em7・G・Asus4・A（Bメロ）／ D・F#m・Bm・G・Em7・A（サビ）
#   ベース: 指弾き。根音と5度・オクターブ。サビはのばして、下にサブベース。
#   ドラム: 入り方は「キックだけ先に入る → リフで全員（フィルなし・クラッシュ）」。Aメロ1 は電子のビート（キックとクラップと16分のハイハット）、サビは半分の速さ、最後のサビの後半だけ4つ打ち。
#   ギター: 和音をかき鳴らす（弦は3〜4本）。曲の出だしに刻みは置かない。リードはフックをピアノと重ねるのと、サビの歌の休みだけ。
#   この曲だけ: 停電の場面で電気の音（シンセと歪んだギター）がぜんぶ消え、アコースティックギターと声と手拍子だけになる。電気がもどる所で最後のサビ。
#   声: クリア 1 種類で最後まで。
#   ほかの曲とのちがい: 16（176・4つ打ちの速いロック・ピアノのリフ・転調2回）とは、テンポ・サビの速さ（半分）・音（ニューメタルの壁）・転調なし、がちがう。
from vocalo_lib import *
import random as _r, re as _re

S = Song("21", "planetarium", "屋上プラネタリウム（仮）", "Rooftop Planetarium", 146, 4, "B", "minor", "エレクトロロック（ボカロ）")
S.kit = "naked-x"; S.flags = "--bass bnb-loud --ref-tone bright-nu-wall --piano salamander " + S.flags
K = Key("B", "minor"); SC = {11, 1, 2, 4, 6, 7, 9}
R_CH = ["Bm", "Bm", "G", "G", "Em7", "Em7", "A", "A"]
A_CH = ["Bm", "Bm", "D", "D", "G", "G", "F#m", "F#m", "Em7", "Em7", "G", "G", "Bm", "A", "G", "A"]      # v4: リフ（Bm・G・Em7・A）と同じ和音が40小節つづいていたので、Aメロは別の進行に
B_CH = ["Em7", "Em7", "G", "G", "Asus4", "A", "Asus4", "A"]
C_CH = ["D", "F#m", "Bm", "G", "D", "F#m", "Em7", "A", "D", "F#m", "Bm", "G", "Em7", "G|A", "Bm", "Bm"]
C_END = C_CH[:14] + ["D", "D"]
T_CH = ["D", "A", "Bm", "G", "D", "A", "G", "G"]
S.scene("サビ頭", 8, "intro", C_CH[:8])
S.scene("リフ", 8, "break", R_CH)
S.scene("Aメロ", 16, "verse", A_CH)
S.scene("Bメロ", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("かけ合い", 8, "break", R_CH)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("停電", 8, "bridge", T_CH)
S.scene("星が出る", 8, "bridge", ["G", "G", "A", "A", "G", "G", "Asus4", "A"])
S.scene("最後のサビ", 32, "chorus", C_CH + C_END)
S.scene("おわり", 8, "outro", ["Bm", "Bm", "G", "G", "Bm", "Bm", "Bm", "Bm"])
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(2119)

# ================= 歌（ロ短調の度数。oct=3 で 1 = B3）=================
P1, P2 = "x-x-x-x---x-x---", "x---x-------...."
Q1, Q2 = "..x-x-x-x-x-x---", "x-x---------...."
R1, R2 = "x---x-x-x---x-x-", "x---x-------...."
AP = AP1 = [P1, P2, Q1, Q2, R1, R2, Q1, Q2] * 2
AD = ["3 3 2 3 5 4", "5 3", "3 4 5 4 3 4", "5 3", "6 6 5 3 5 6", "5 3", "5 4 5 7 5 4", "5 2",
      "4 4 6 6 5 4", "3 4", "6 5 3 5 6 7", "7 6", "5 5 7 5 3 5", "4 4", "6 6 7 6 5 6", "7 7"]
# v4: Aメロ2 は、リズムの形も高さも Aメロ1 と変える（つめて歌う行 W と、おくれて入る行 Z）
W1, W2 = "x-x-x-x-x-x-x---", "x-----------...."
Z1, Z2 = "....x-x-x-x-x-x-", "x---x-------...."
AP2 = [W1, W2, Z1, Z2, W1, W2, Z1, Z2, R1, R2, Q1, Q2, W1, W2, Z1, Z2]
AD2 = ["5 5 5 7 5 3 5", "5", "7 7 5 7 1' 7", "5 3", "6 6 6 1' 7 6 5", "3", "7 7 5 4 5 7", "5 2",
       "4 4 6 6 5 4", "3 4", "6 5 3 5 6 7", "7 6", "1' 1' 7 5 7 1' 7", "7", "6 6 7 6 7 1'", "2' 2'"]
A1 = ["まちじゅうのあかり", "いちどにきえたよ", "れいぞうこもねた", "しずかすぎるよる", "かいだんをのぼる", "てさぐりのままで", "おくじょうのどあを", "おしたらそこには"]
A2 = ["となりのやねにも", "だれかがてをふる", "なまえもしらない", "おなじそらみてる", "あかるすぎたから", "みえずにいたもの", "くらやみのおくで", "まちつづけていた"]
B1p, B2p = "x---x---x-x-x---", "x-------x---...."
BP_ = [B1p, B2p] * 4
BD = ["4 4 6 5 4", "3 4", "6 6 1' 7 6", "5 6", "7 7 1' 7 5", "7 7", "7 7 1' 2' 1'", "2' 2'"]
B1 = ["みあげてごらん", "てんじょうがない", "ひとつふたつと", "ともりはじめる"]
B2 = ["みあげてごらん", "かぞえきれない", "ひとつふたつと", "こえがふえてく"]
E1, E2 = "x---x-x-x-x-x---", "x-x-x-x-x---...."
F1, F2 = "x---x---x-x-x---", "x-x-x-x-----...."
G1, G2 = "x---x---x-x-x---", "x-x-x-------...."
X1, X2 = "..x-x-x-x---x-x-", "x---x-x-x-x-...."          # v4: サビは行ごとにリズムを変える（頭から・おくれて・長くのばしてから）
Y1, Y2 = "x-----x-x-x-x-x-", "x---x---x-x-x-.."
CP = [E1, E2, X1, X2, Y1, Y2, F1, F2, E1, E2, X1, X2, Y1, Y2, G1, G2]
CD = ["5 5 7 7 3' 2'", "2' 2' 1' 7 2'", "1' 1' 3' 3' 4' 3'", "3' 3' 1' 7 1'", "5 5 7 7 3' 4'", "5' 4' 2' 1' 2'", "4' 4' 3' 1' 3'", "2' 2' 4' 4'",
      "5 5 7 7 3' 2'", "2' 2' 1' 7 2'", "1' 1' 3' 3' 4' 5'", "4' 3' 1' 7 1'", "4' 4' 3' 3' 1' 3'", "3' 3' 2' 2' 4'", "3' 3' 2' 1' 2'", "1' 7 1'"]
CDE = CD[:15] + ["2' 3' 3'"]                                                      # 最後だけ、上（レ）で終わる
C1 = ["おくじょうぷらねたりうむ", "ていでんのよるのまほう", "くらやみがくれたそらを", "みんなでみあげてる",
      "おくじょうぷらねたりうむ", "ひとりぶんのひかりたち", "つないだらせいざになる", "きみもそのひとつ"]
C2 = [C1[0], "あかりがねむるあいだに", "ほしがうたいだしたんだ", "だれもがきいている"] + C1[4:]
H1, H2 = "x---x-x---x-x---", "x-x-x-------...."
TP_ = [H1, H2] * 4
TD = ["5 5 7 5 3", "4 5 4", "3 3 5 7 5", "6 5 3", "5 5 7 1' 7", "7 1' 2'", "3' 3' 1' 7 6", "7 1' 1'"]
T1 = ["あかりがなくても", "うたはきこえるよ", "てをたたくおとが", "ほしをよんでいる"]


def put(name, pats, degs, phrases):
    lines, text = song_phrases(pats, degs, phrases); bars = S.sc(name); mel = [K.mel(x, oct=3) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("サビ頭", CP[:8], CD[:8], C1[:4]); put("Aメロ", AP, AD, A1); put("Bメロ", BP_, BD, B1); put("サビ1", CP, CD, C1); put("Aメロ2", AP2, AD2, A2); put("Bメロ2", BP_, BD, B2); put("サビ2", CP, CD, C2)
put("停電", TP_, TD, T1); put("最後のサビ", CP + CP, CD + CDE, C1 + C2)

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


GL = [S.track(f"Lギター{i + 1}弦め（ニューメタルの壁）", "distGuitar", **rock_gtr_spec(0.085, -0.6, tone="nu-metal-wall")) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め（ニューメタルの壁）", "distGuitar", **rock_gtr_spec(0.08, 0.6, tone="nu-metal-wall")) for i in range(6)]
LG = S.track("リードギター（フック・合いの手）", "leadGuitar", **lead_gtr_spec(0.055, -0.08))
AG = [S.track(f"アコースティックギター{i + 1}弦め", "guitar", patch="nylonGuitar", amp="clean", volume=0.09, pan=0.0, reverb=0.25, chorus=0) for i in range(6)]
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


def chorus(b, i, n):
    lv = {"サビ1": 1, "サビ2": 2, "最後のサビ": 3}[n]; j = i % 16; fast = lv == 3 and i >= 16; end = lv == 3 and i == 31
    saw(b); sub(b); bass(b, *(BC[i % 4] if not fast else BV[i % 4]))
    strum(GL, b, "x-------x-------" if i % 2 == 0 else "x-----x---x-----", strings=3); strum(GR, b, "x-----x---x-----" if i % 2 == 0 else "x-------x-------", strings=4)
    feel(D, b, ("half" if i % 2 == 0 else "halfopen") if not fast else "four")
    if lv >= 2: CLAP.bar(b, "R:2 B4:1 R:1" if not fast else "R:1 B4:1 R:1 B4:1")
    if lv >= 2 or j >= 8: arp(b, "x-x-x-x-x-x-x-x-" if j % 2 == 1 or fast else "x---x---x---x---")
    if j in LANS and not end: LG.bar(b, LANS[j])
    elif fast and not end: t = sorted(voice(halves(b)[0], 74, 3))[-1]; LG.bar(b, f"{N(t)}:4" if i % 2 == 0 else f"R:2 {N(t)}:1 {N(t + 2)}:1")       # v4: 後半は、リードギターが上で長い音を重ねる
    if j % 8 == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
    if j % 8 == 7 and not end: fill_cresc(D, b, 1 if j == 7 else 2)
    if end: D.set(b, "X.........X.....", "........X.......", "X.x.X.x........."); strum(GL, b, "x---------------", strings=3); strum(GR, b, "x---------------", strings=4)


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "サビ頭":                                                  # v4: 歌から始まる（今までの曲は「1つの音から始めてだんだん増やす」ばかりだった）。4小節は声とピアノとシンセ、5小節めにバンドが入る
        saw(b); sub(b); arp(b, "x---x---x---x---"); r = low(halves(b)[0], "E2"); PNO.bar(b, " ".join(f"{N(r + d)}:0.5" for d in (0, 7, 12, 7, 16, 12, 7, 12)))
        if i >= 4:
            feel(D, b, "half" if not odd else "halfopen"); bass(b, *BC[i % 4]); strum(GL, b, "x-------x-------", strings=3); strum(GR, b, "x-----x---x-----", strings=4)
            if i == 4: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
        if last: fill_cresc(D, b, 2)
    elif n == "リフ":                                                   # ピアノとリードギターのフック
        hook(b, i); bass(b, *BV[i % 4]); sub(b); strum(GL, b, "x-----x-----x---", strings=3); strum(GR, b, "x---------x-----" if not odd else "x-----x---x-----", strings=4)
        feel(D, b, "rock8" if not odd else "rock8b"); arp(b, "x---x---x---x---")
        if i in (0, 4): crash(D, b, "C2", 4)
        if last: fill_cresc(D, b, 1, toms=False)
    elif n == "かけ合い":                                               # v4: リフのくり返しをやめた。リードギターの1小節（バンドは頭の1発で止まる）→ プラックの速い返事とバンド、を交互に
        if not odd:
            LG.bar(b, LGS[i // 2]); D.set(b, "X...............", "................", "X...x...x...x..."); strum(GL, b, "x---............", strings=3); strum(GR, b, "x---............", strings=4)
            BASS.bar(b, f"{N(low(halves(b)[0], 'E1'))}:1 R:3"); crash(D, b, "C2", 4)
        else:
            feel(D, b, "break" if i % 4 == 1 else "break2"); bass(b, *BV[(i // 2) % 4]); sub(b); strum(GL, b, "x-----x-----x---", strings=3); strum(GR, b, "x-----x---x-----", strings=4)
            arp(b, "xxxxxxxxxxxxxxxx", order=(0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 3) if i % 4 == 1 else (5, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4))
        if last: fill_cresc(D, b, 2)
    elif n in ("Aメロ", "Aメロ2"):
        two = n == "Aメロ2"; first = i < 8; AP = AP2 if two else AP1
        if first and not two:                                          # Aメロ1 の前半: 電子のビート（キックとクラップと16分のハイハット）。ギターなし
            D.set(b, "X.....x.X.......", "................", "................"); CLAP.bar(b, "R:1 B4:1 R:1 B4:1"); HATR.bar(b, EH[i % 2]); bass(b, "x-x-x-x-x-x-x-x-", "11111111"); sub(b)
            if i % 2 == 1: PNO.bar(b, "R:2 " + ["F#5:0.5 D5:0.5 B4:1", "E5:0.5 D5:0.5 B4:1", "G5:0.5 E5:0.5 B4:1", "E5:0.5 C#5:0.5 A4:1"][(i // 2) % 4])      # 句の終わりに、フックのかけら
        else:                                                          # 生のドラムとギター
            feel(D, b, ("rock8" if not odd else "rock8b") if not two or not first else ("break" if not odd else "break2")); bass(b, *BV[(i + (2 if two else 0)) % 4])
            strum(GR, b, "x---------------" if not odd else "x-----x---------", strings=3)
            if two: HATR.bar(b, EH[i % 2]) if first else strum(GL, b, "x-------x-------", strings=3)
            if two and i % 2 == 1 and first: PNO.bar(b, "R:2 " + ["F#5:0.5 D5:0.5 B4:1", "E5:0.5 D5:0.5 B4:1", "G5:0.5 E5:0.5 B4:1", "E5:0.5 C#5:0.5 A4:1"][(i // 2) % 4])
            if i == 8: crash(D, b, "C2", 4)
        if i == 7: fill_cresc(D, b, 1, toms=False)
        if last: fill_cresc(D, b, 1)
    elif n in ("Bメロ", "Bメロ2"):                                      # 半分の速さ。v4: 1回めは最後の小節で全員が止まって声だけ、2回めはタムとギターの4分で押す
        two = n == "Bメロ2"; stop = last and not two
        if stop:
            for j, v in enumerate(sorted(voice(halves(b)[0], 62, 3))): SAW[j].bar(b, f"{N(v)}:1.5 R:2.5")
            BASS.bar(b, f"{N(low(halves(b)[0], 'E1'))}:1.5 R:2.5"); strum(GL, b, "x-----..........", strings=3); strum(GR, b, "x-----..........", strings=4); D.set(b, "X.....X.........", "......X.........", "X...............")
        else:
            saw(b); sub(b); bass(b, "x-------x---x-x-" if i < 4 else "x---x---x-x-x-x-", "115d" if i < 4 else "115w5d")
            if two: strum(GL, b, "x---x---x---x---", strings=3); strum(GR, b, "x-------x-------", strings=4)
            elif i >= 4: strum(GL, b, "x---------------", strings=3); strum(GR, b, "x-------x-------", strings=4)
            if two: D.set(b, "X..X..X...X.X..." if i < 6 else "X...X...X...X...", "........X......." if i < 6 else ("x.x.x.x.x.x.x.x." if i == 6 else "x.x.x.x.xxxxXXXX"), "................" if i < 6 else "................")
            else: D.set(b, "X.......X.......", "........X.......", "X...x...X...x...")
            arp(b, "x---x---x---x---")
        if i == 6: FXT.bar(b, fx_bar((0, "up", 4)))
    elif n in ("サビ1", "サビ2", "最後のサビ"): chorus(b, i, n)
    elif n == "停電":                                                   # 電気の音がぜんぶ消える。アコースティックギターと声。後半から手拍子
        c1, c2 = halves(b); gtr_strum(AG, S, b, "x---x-x-x---x-x-" if not odd else "x---x-x-x-x-x-x-", c1, RNG, drive=False)
        if i == 0: FXT.bar(b, fx_bar((0, "down", 2)))
        if i >= 4: CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
    elif n == "星が出る":                                               # 星が1つずつ: 分散和音の音が、小節ごとに増える。5小節めからキックとサブベース
        c1, c2 = halves(b); gtr_strum(AG, S, b, "x---x-x-x---x-x-" if not odd else "x---x-x-x-x-x-x-", c1, RNG, drive=False); CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        arp(b, STAR[i], order=(4, 2, 3, 1, 4, 2, 5, 3))
        if i >= 4: sub(b); D.set(b, "X...X...X...X...", "................" if i < 6 else ("x.x.x.x.x.x.x.x." if i == 6 else "x.x.x.x.xxxxXXXX"), "................")
        if i >= 6: saw(b)
        if i == 6: FXT.bar(b, fx_bar((0, "up", 4)))
        if last: strum(GL, b, "x---------------", strings=3); strum(GR, b, "x---------------", strings=4)
    elif n == "おわり":                                                 # リフを4小節 → 分散和音が1小節ごとに減って、1音だけ残る
        if i < 4:
            hook(b, i); bass(b, *BV[i % 4]); sub(b); strum(GL, b, "x-----x-----x---" if i < 3 else "x---------------", strings=3); strum(GR, b, "x---------x-----" if i < 3 else "x---------------", strings=4)
            feel(D, b, "rock8" if not odd else "rock8b"); arp(b)
            if i == 0: crash(D, b, "C2", 4)
            if i == 3: D.set(b, "X.......X.......", "....X...........", "X.x.X.x.........")
        elif i < 7: arp(b, STAR[(7 - i) * 2 - 1 if i < 6 else 1], order=(4, 2, 3, 1, 4, 2, 5, 3))
        else: ARP.bar(b, "F#6:4")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の21（20時）。エレクトロロック（146）。ロ短調。街が停電した夜、屋上で星が見える。重い歪みのギターの壁とシンセ、ピアノのフック。"
          "停電の場面で電気の音がぜんぶ消え、アコースティックギターと声と手拍子だけになる。参考の音 bright-nu-wall。自作")
finish(S, LY, V, 0)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=88, down=10, up=10, seed=21); humanize(path, "ピアノ", mid=86, down=10, up=8, seed=5)
js = load(path); gtr_velocity(js, "Lギター", 3); gtr_velocity(js, "Rギター", 4); gtr_velocity(js, "アコースティックギター", 6); save(path, js)
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 8, "pre": 14, "chorus": 24, "最後のサビ": 28, "bridge": 12}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {}, default="clear")       # 1 曲 1 種類の声（2026-11-17 人間）
    sing_ends(path, S)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.3
    save(path, js)
js = load(path); drum_punch(js); drum_center(js); save(path, js)
# 1 回めを曲から分けて測った: シンセ（パッドと分散和音）が −45dB でほとんど聞こえない／リフ（−16〜−18）がサビ（−17〜−18）より大きい／停電のアコースティックギターが歌より 11dB 大きい／前奏が −25.5
#   → シンセを上げ、フックのリードギターとアコースティックギターを下げ、左右のギターを少し上げた。前奏にパッドを足した
#   2 回め: シンセはまだ −33〜−42dB・前奏 −23.1（リフ −18.9）。前奏を仕上げで 1.5dB 上げたら、リフに入る所で分散和音が 2.7dB 下がった（やってはいけない形）
#   → 前奏の持ち上げはやめ、シンセそのものの音量を上げた（分散和音 boost 12・パッド boost 9）
final_gain(path, {"サビ2": 0.5, "最後のサビ": 1.5})
