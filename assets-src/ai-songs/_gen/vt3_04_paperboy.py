# vt3 04「新聞配達スプリンター」Newspaper Sprinter（仮）— ホーン隊のスカ（ギターなし）。176・4/4。B♭長調 → 最後のサビは C。
# 第3弾（0時〜24時の街）の 3時。表は docs/sound/vt3-plan.md。
#
# v4（2026-11-13）: ゼロから作り直し（人間「全ての曲を1みたいにこだわって作って」「このレベル（02 v7）まで詰めて曲作って」）。
#   v1〜v3 はスカパンク（ギターの裏打ち＋ひずんだギターの8分）。ギターの音は 02 で「ポコポコ」と言われた（ギターに聞こえない音は使わない）ので、
#   この曲はギターを使わない。裏打ちはピアノとオルガン、主役はホーン隊（トランペット・テナーサックス・トロンボーン）と自転車のベル。
#
# 物語: 午前3時。まだ真っ暗な町を、かごいっぱいの新聞をのせた自転車で走る「わたし」。だれも知らない、町でいちばんの早起き。
#   角の家では番犬がほえ、信号は黄色だけが点めつしている。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: 2番で、同じ暗い道が舞台に、黄色い点めつがライトに、白い息がきらきらに、
#   ほえる犬が応援団に見えてくる。どこかの窓から聞こえた鼻歌（1時のラジオの節 3・5・6・5・2）に、ベルで「ちりん」と答える。
#
# 曲を決める表（書く前に similar_check.py --plan で確かめた: いちばん近い曲でも近さ 20%）:
#   形: 自転車のベルだけ（サビの節のリズム）→ ホーン隊のテーマ → Aメロ1（前半はピアノの裏打ちとベースだけ → 後半オルガンとホーンの合いの手）
#       → Bメロ（のぼって止まる。止まった所でベルが「ちりん」）→ サビ1（「ちりんちりん」と歌うとベルが答える）→ 間奏（ホーンのテーマ）
#       → Aメロ2（前半はオルガンとベースとリムだけ。窓からの鼻歌にベルが答える）→ Bメロ2 → サビ2（ホーンの合いの手が増える）
#       → トロンボーンのソロ → Cメロ（信号待ち・半分の速さ。東の空がうす青い）→ 最後のサビ（C に上がる・いちばん強い）→ テーマで終わり、最後にベル
#   旋律: Aメロ＝裏拍から入る、同じ高さを刻む話し方（スカの裏打ちに乗る）。Bメロ＝長い音で1段ずつのぼる。
#         サビ＝「ちりん・ちりん」を同じ形で呼び（2回目は上の高さ）、その返事を次の小節で歌う（呼びかけと返事）
#   和音: Aメロ I・IV・vi・ii・V。Bメロは IV → #IVdim → I/V → VI7 → ii → V（昔のジャズの回り方）。サビは I → III7 → vi → I7 → IV → iv6（明るい中に1か所だけ切ない色）
#   ベース: 歩くベース（4分で和音の音をのぼって、次の小節でおりる）。サビは8分ではねる。丸くて短い音（「ドン」と鳴って伸びない）
#   この曲だけ: ①自転車のベルが曲の中の楽器（サビの「ちりんちりん」のすき間に必ず答える）②ギターなしのスカ ③歌とホーンの呼びかけと返事
#
# スカの作り方（2026-11-13 に調べた。melodigging.com の ska / ska-punk、violetrecording.com の reggae の作り方、musical-u.com の ska）:
#   裏拍の短い和音（スカンク）はギターかピアノ、オルガンが重ねる「バブル」。ベースは歩くか、はねる。ドラムは2・4拍のスネアとまっすぐなハイハット。
#   ホーン（トランペット・トロンボーン・サックス）は、そろった節か3声の短い和音で、歌との呼びかけと返事に使い、鳴らしっぱなしの壁にしない。
#   ベースは伸びる明るい音ではなく「ドン」という丸い音。サビは短く、みんなで歌える形に。
from vt25_lib import *

S = Song("04", "paperboy", "新聞配達スプリンター（仮）", "Newspaper Sprinter", 176, 4, "Bb", "major", "ホーン隊のスカ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.5
S.keepers = {}
K = Key("Bb", "major")          # oct 3 で 1 = B♭3
KC = Key("C", "major")          # 最後のサビ（+2）

TH = ["Bb", "Bb", "Eb", "Eb", "Bb", "Gm", "Cm7", "F7"]
A_CH = TH
B_CH = ["Eb", "Edim", "Bb/F", "G7", "Cm7", "Cm7", "F7", "F7"]
C_CH = ["Bb", "D7", "Gm", "Bb7", "Eb", "Ebm6", "Bb", "F7", "Bb", "D7", "Gm", "Bb7", "Eb", "F7", "Bb", "Bb"]
LAST = [tr_chord(c, 2) for c in C_CH]

S.scene("ベル", 4, "intro", ["Bb", "Bb", "Bb", "F7"])
S.scene("テーマ", 8, "intro", TH)
S.scene("Aメロ1", 16, "verse", A_CH + A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", TH)
S.scene("Aメロ2", 16, "verse", A_CH + A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("かけあい", 8, "break", ["Bb", "Bb", "Gm", "Gm", "Eb", "Eb", "F7", "F7"])
S.scene("トロンボーンのソロ", 8, "solo", TH)
S.scene("トランペットのソロ", 8, "solo", TH)
S.scene("Cメロ", 16, "bridge", ["Gm", "Gm", "Eb", "Eb", "Bb", "Bb", "F", "F", "Gm", "Gm", "Eb", "Eb", "Cm7", "Cm7", "G7", "G7"])     # 最後の G7 は C への入り口
S.scene("最後のサビ", 32, "chorus", LAST + LAST)
S.scene("おわり", 8, "outro", ["C", "C", "F", "F", "C", "C", "F", "C"])

V = Voice(S, vol=0.2, delay=0.4, bright=0.0, patch="kfbSineLead" if VOCAL else "altoSax", low=False)   # BGM の旋律はアルトサックス（v4 のリードオルガンは、場面ごとの採点で歌の版より 0.7〜0.9 低かった）
PN = [S.track(f"ピアノ（裏打ち{i + 1}）", "piano", volume=0.085, pan=-0.3, reverb=0.14, sustain=0.3,
              fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 1200, "high": 1}]) for i in range(3)]
PLG = [S.track(f"ピアノ（のばす和音{i + 1}）", "piano", volume=0.08, pan=-0.2, reverb=0.25, sustain=1.4) for i in range(3)]
ORG = [S.track(f"オルガン{i + 1}", "drawbarOrgan", volume=0.036, pan=0.35, reverb=0.2, sustain=0.35) for i in range(3)]
ORL = [S.track(f"オルガン（のばす{i + 1}）", "drawbarOrgan", volume=0.026, pan=0.3, reverb=0.25, sustain=1.2) for i in range(3)]
TP = S.track("トランペット", "brass", patch="trumpet", volume=0.085, pan=0.2, reverb=0.25)
SX = S.track("テナーサックス", "brass", patch="tenorSax", volume=0.08, pan=0.0, reverb=0.25)
TB = S.track("トロンボーン", "brass", patch="trombone", volume=0.085, pan=-0.2, reverb=0.25)
BASS = S.track("ベース（指弾き・丸い音）", "bass", sustain=0.75, **dict(finger_bass_spec(vol=0.215), fx=[{"type": "eq", "low": 1, "mid": 1, "midHz": 700, "high": -3}, {"type": "filter", "kind": "lowpass", "freq": 1400, "q": 0.6}]))
BELL = S.track("自転車のベル", "lead", patch="tubeGlock", volume=0.075, pan=0.3, reverb=0.3)
HUMT = S.track("窓からの鼻歌", "lead", patch="kfbSineLead", volume=0.06, pan=-0.45, reverb=0.45)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
# Aメロ: 裏拍から入って、同じ高さを刻む（スカの裏打ちに乗って話す）。2小節で1つの文
VA = ["R:0.5 3:0.5 3:0.5 3:0.5 5:0.5 3:0.5 3:0.5 1:0.5", "R:0.5 1:0.5 2:0.5 3:0.5 5:1.5 R:0.5",
      "R:0.5 6:0.5 6:0.5 4:0.5 6:0.5 1':0.5 6:0.5 6:0.5", "R:0.5 4:0.5 5:0.5 6:0.5 5:1.5 R:0.5",
      "R:0.5 5:0.5 5:0.5 5:0.5 1':0.5 5:0.5 3:0.5 3:0.5", "R:0.5 3:0.5 5:0.5 6:0.5 1':1.5 R:0.5",
      "1':0.5 1':0.5 6:0.5 4:0.5 6:0.5 1':0.5 R:1", "2':0.5 2':0.5 1':0.5 7:0.5 5:1.5 R:0.5"]
VA2 = VA[:4] + ["R:0.5 5:0.5 5:0.5 1':0.5 3':0.5 1':0.5 5:0.5 5:0.5", "R:0.5 5:0.5 6:0.5 1':0.5 2':1.5 R:0.5",
                "2':0.5 2':0.5 1':0.5 6:0.5 1':0.5 2':0.5 R:1", "2':0.5 2':0.5 2':0.5 1':0.5 2':1.5 R:0.5"]
A1 = ("ごぜんさんじの/まちかど/かごにやまもり/しんぶん/ねむるまどべを/すりぬけ/ぺだるをふむ/しろいいき/"
      "かどのいえには/ばんけん/さかをのぼれば/ぽすとだ/しんごうはまだ/きいろで/ちかちかして/ねむそうだ")
# 2番（景色が書きかわる）: 同じ道が舞台に、黄色い点めつがライトに、白い息がきらきらに、ほえる犬が歌に
A2 = ("だれもしらない/はやおき/けれどこのみち/すてーじ/きいろのあかり/らいとで/はくいきまで/きらきらだ/"
      "どこかのまどで/はなうた/きいたことある/あのふし/べるでこたえる/ちりんと/いぬもほえて/うたになる")
# Bメロ: 長い音で1段ずつのぼる。最後は高い音をのばして、全員止まる
VB = ["4:1.5 6:0.5 1':1.5 R:0.5", "6:1 1':1 6:0.5 1':1 R:0.5", "5:1.5 1':0.5 3':1.5 R:0.5", "2':0.5 3':0.5 3':1 6:0.5 3':1 R:0.5",
      "4':1 4':0.5 2':0.5 1':1 2':0.5 R:0.5", "R:0.5 6:0.5 1':0.5 2':0.5 4':1.5 R:0.5", "2':0.5 2':0.5 2':0.5 2':0.5 3':0.5 3':0.5 4':1", "5':2 R:2"]
B1 = "だれも/みてない/けれど/まちはまつ/あたらしい/いちにち/とどけにいくよー"
B2 = "やみも/さむさも/ぜんぶ/みかたにし/このまちの/あさへと/ぺだるをふむよー"
# サビ: 「ちりん・ちりん」（呼びかけ）→ 次の小節で返事。2回目の「ちりんちりん」は上の高さ。後半は長めの音で風になる
HOOK_A = "3:0.5 5:0.5 5:0.5 R:0.5 3:0.5 5:0.5 1':1"
HOOK_B = "6:0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':0.5 3':1"
HOOK_C = "5:0.5 3':0.5 3':0.5 R:0.5 5:0.5 2':0.5 1':1"
VC = [HOOK_A, "R:0.5 6:0.25 6:0.25 7:0.5 7:0.5 2':0.5 2':0.5 7:0.5 R:0.5",
      HOOK_B, "R:0.5 3':0.5 2':0.5 1':0.5 1':0.25 6:0.25 5:0.25 6:0.25 5:0.5 R:0.5",
      "4:0.75 6:0.75 1':0.5 1':1 6:0.5 R:0.5", "R:0.5 4:0.5 1':0.5 2':0.5 1':1.5 R:0.5",
      "5:0.5 5:0.5 3:0.5 5:0.5 1':0.5 1':0.5 3':0.5 R:0.5", "2':0.5 2':0.5 1':0.5 7:0.5 1':0.5 2':1 R:0.5",
      HOOK_A, "R:0.5 6:0.25 6:0.25 7:0.5 7:0.5 2':0.5 2':0.5 7:0.5 R:0.5",
      HOOK_B, "R:0.5 3':0.5 2':0.5 1':0.5 1':0.25 6:0.25 5:0.25 6:0.25 5:0.5 R:0.5",
      "6:0.75 1':0.75 3':0.5 3':1 1':0.5 R:0.5", "R:0.5 2':0.5 3':0.5 4':0.5 4':1.5 R:0.5",
      HOOK_C, "R:4"]
C1 = ("ちりんちりん/あさをくばるよ/ちりんちりん/まちじゅうのまどへ/かぜになる/よあけへ/だれもしらない/いちばんのり/"
      "ちりんちりん/さかをくだるよ/ちりんちりん/しんごうはきいろ/ぺだるふむ/ちからで/ちりんちりん")
C2 = ("ちりんちりん/まちがおきだす/ちりんちりん/てんめつのきいろ/らいとだね/わたしの/ほえるいぬまで/おうえんだん/"
      "ちりんちりん/よるをぬりかえ/ちりんちりん/ひがしのそらまで/あおくなる/もうすぐ/ちりんちりん")
C3 = ("ちりんちりん/あさがおいつく/ちりんちりん/さいごのいっけんへ/かぜになる/ひかりへ/からっぽのかごに/あさひがのる/"
      "ちりんちりん/よるがあけるよ/ちりんちりん/はなうたもつれて/あさがくる/ここまで/ちりんちりん/"
      "ちりんちりん/あしたもくるよ/ちりんちりん/しらなくていいよ/かぜになる/わたしが/このまちのあさ/はこんでいる/"
      "ちりんちりん/おはようくばる/ちりんちりん/まちじゅうのまどへ/ぺだるふむ/ちからで/ちりんちりん")
# かけあい: 歌が「ちりんちりん」と呼ぶと、次の小節でホーンが答える
VCALL = [HOOK_A, "R:4", HOOK_B, "R:4", "4:0.5 6:0.5 6:0.5 R:0.5 4:0.5 6:0.5 1':1", "R:4", "5:0.5 7:0.5 7:0.5 R:0.5 5:0.5 2':0.5 2':1", "R:4"]
CALL = "ちりんちりん/ちりんちりん/ちりんちりん/ちりんちりん"
ANS = ["R:0.5 D5:0.5 C5:0.5 Bb4:0.5 G4:0.5 F4:0.5 R:1", "R:0.5 D5:0.5 Bb4:0.5 G4:0.5 Bb4:1 R:1", "R:0.5 Eb5:0.5 D5:0.5 C5:0.5 Bb4:0.5 G4:0.5 R:1", "A4:0.5 C5:0.5 Eb5:0.5 F5:0.5 F5:1 R:1"]
# Cメロ（信号待ち）: 半分の速さ。4分の長い音でのぼる
VBR = ["R:1 6:1 1':1 3':1", "2':2 1':1 R:1", "R:1 4:1 6:1 1':1", "2':1.5 1':1.5 R:1",
       "R:1 3':1 2':1 1':1", "6:2 1':1 R:1", "R:1 5:1 7:1 2':1", "2':3 R:1",
       "R:1 6:1 1':1 3':1", "2':2 1':1 R:1", "R:1 6:1 1':1 4':1", "3':1.5 1':1.5 R:1",
       "R:1 4:1 6:1 1':1", "2':2 4':1 R:1", "R:1 6:1 #1':1 3':1", "5':3 R:1"]
CB = "とまるあし/ひとやすみ/ひがしがわ/うすあお/かじかむて/いきをかけ/とりがなく/もうすぐ"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA2, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC, C1)
put("Aメロ2", K, VA + VA2, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC, C2)
put("Cメロ", K, VBR, CB)
put("かけあい", K, VCALL, CALL)
put("最後のサビ", KC, VC + VC, C3, o=4)

# ================= 和音の楽器 =================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]


def chd(tracks, b, pat, c=62):
    v = voice(root(b), c, 3)
    for j in range(3): tracks[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


SKANK = "R:0.5 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5"            # 裏拍の短い和音
SKANK2 = "R:0.5 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5 R:0.5 x:0.25 x:0.25"   # 4小節目だけ、最後を2回
BUBBLE = "R:0.5 x:0.25 x:0.25 R:0.5 x:0.5 R:0.5 x:0.25 x:0.25 R:0.5 x:0.5"   # オルガンの「バブル」（裏拍を2回・1回で交代）


def horn3(b, pat, c=65):
    """ホーン3本の短い和音（上からトランペット・サックス・トロンボーン）"""
    v = sorted(voice(root(b), c, 3))
    for tr, m in zip((TB, SX, TP), v): tr.bar(b, " ".join(t.replace("x", nm(m)) for t in pat.split()))


def under(line, ch, gap=3):
    """節の下に、和音の音でハモる線（gap 半音より下の、いちばん近い和音の音）"""
    out = []
    for t in line.split():
        n_, L = t.split(":")
        if n_ == "R": out.append(t); continue
        m = midi(n_); cs = [x for x in tones(ch, nm(m - 12), nm(m - gap))]
        out.append(f"{nm(cs[-1] if cs else m - 12)}:{L}")
    return " ".join(out)


def tr_line(line, semi):
    return " ".join(t if t.startswith("R") else f"{nm(midi(t.split(':')[0]) + semi)}:{t.split(':')[1]}" for t in line.split())


# ホーン隊のテーマ（サビの「ちりんちりん」と同じリズムで始まる）
THEME = ["F4:0.5 Bb4:0.5 Bb4:0.5 R:0.5 F4:0.5 Bb4:0.5 D5:1", "R:0.5 D5:0.5 C5:0.5 Bb4:0.5 G4:0.5 F4:0.5 R:1",
         "G4:0.5 Bb4:0.5 Bb4:0.5 R:0.5 G4:0.5 Bb4:0.5 Eb5:1", "R:0.5 Eb5:0.5 D5:0.5 C5:0.5 Bb4:0.5 G4:0.5 R:1",
         "F4:0.5 Bb4:0.5 D5:0.5 R:0.5 D5:0.5 F5:0.5 D5:1", "R:0.5 D5:0.5 Bb4:0.5 G4:0.5 Bb4:1 R:1",
         "C5:1 Eb5:0.5 C5:0.5 G4:1 Bb4:1", "A4:0.5 C5:0.5 Eb5:0.5 F5:0.5 F5:1 R:1"]
# トロンボーンのソロ（低い所で歌う。長い音とすべりこむ8分）
TBSOLO = ["Bb3:1.5 D4:0.5 F4:1.5 R:0.5", "R:0.5 F4:0.5 G4:0.5 F4:0.5 D4:1 Bb3:1", "Eb4:1.5 G4:0.5 Bb4:1.5 R:0.5", "R:0.5 Bb4:0.5 G4:0.5 Eb4:0.5 G4:1.5 R:0.5",
          "D4:0.5 F4:0.5 Bb4:1 R:0.5 Bb4:0.5 A4:0.5 Bb4:0.5", "D5:1.5 Bb4:0.5 G4:1.5 R:0.5", "R:0.5 Eb4:0.5 G4:0.5 Bb4:0.5 C5:1 Bb4:0.5 G4:0.5", "A4:1 C5:1 F4:1 R:1"]


TPSOLO = ["R:0.5 F4:0.5 Bb4:0.5 D5:0.5 F5:1 D5:0.5 Bb4:0.5", "C5:0.5 D5:0.5 C5:0.5 Bb4:0.5 G4:1 R:1", "R:0.5 G4:0.5 Bb4:0.5 Eb5:0.5 G5:1 Eb5:0.5 D5:0.5", "Eb5:0.5 D5:0.5 C5:0.5 Bb4:0.5 C5:1.5 R:0.5",
          "D5:0.25 Eb5:0.25 F5:0.5 D5:0.5 Bb4:0.5 F5:0.5 D5:0.5 Bb4:0.5 F4:0.5", "G4:0.5 Bb4:0.5 D5:0.5 G5:1.5 R:1", "G5:0.5 Eb5:0.5 C5:0.5 Eb5:0.5 G5:0.5 Eb5:0.5 C5:0.5 Bb4:0.5", "A4:0.5 C5:0.5 Eb5:0.5 F5:0.5 A5:1 R:1"]


def theme(b, i, semi=0, full=True):
    ch = tr_chord(TH[i], semi) if semi else TH[i]
    ln = tr_line(THEME[i], semi)
    TP.bar(b, ln)
    if full:
        SX.bar(b, under(ln, ch)); TB.bar(b, tr_line(ln, -12))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ベル":
        if i >= 1: chd(PN, b, SKANK)
    elif n in ("テーマ", "間奏"):
        chd(PN, b, SKANK2 if i % 4 == 3 else SKANK); chd(ORG, b, BUBBLE, 67)
        theme(b, i, full=(n == "間奏" or i >= 4))               # はじめのテーマは、前半トランペットだけ → 後半3本
    elif n == "Aメロ1":
        chd(PN, b, SKANK2 if i % 4 == 3 else SKANK)             # 前半はピアノの裏打ちとベースだけ
        if i >= 8:
            chd(ORG, b, BUBBLE, 67)
            if i % 2 == 1: horn3(b, "R:3 x:0.25 R:0.25 x:0.5" if i % 4 == 1 else "R:2.5 x:0.5 R:0.5 x:0.5")     # 歌の文の終わりにホーンが答える
    elif n == "Aメロ2":
        chd(ORG, b, BUBBLE, 67)                                 # 2番の前半はオルガンとベースとリムだけ（ピアノは休み）
        if i >= 8:
            chd(PN, b, SKANK2 if i % 4 == 3 else SKANK)
            if i >= 12 and i % 2 == 1: horn3(b, "R:3 x:0.25 R:0.25 x:0.5")
        elif i % 2 == 1:
            TB.bar(b, f"R:2.5 {nm(tones(root(b), 'F3', 'F4')[0])}:0.5 {nm(tones(root(b), 'F3', 'F4')[1])}:0.5 {nm(tones(root(b), 'F3', 'F4')[2])}:0.5")   # トロンボーンだけが低い所でつぶやく
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6:
            chd(PLG, b, "x:4", 63 + i); chd(ORL, b, "x:4", 67 + i)
            chd(PN, b, SKANK)
        elif i == 6:
            chd(PN, b, "x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5", 67); chd(ORL, b, "x:4", 72)
        else:
            chd(PN, b, "x:1 R:3", 69); chd(ORL, b, "x:2 R:2", 74)
        # ホーンは1本ずつ増えて、長い音でのぼる（2番はサックスも最初から）
        hs = sorted(voice(root(b), 62 + i, 3))
        if i < 7:
            TB.bar(b, f"{nm(hs[0])}:3.5 R:0.5")
            if i >= 2 or n == "Bメロ2": SX.bar(b, f"{nm(hs[1])}:3.5 R:0.5")
            if i >= 4: TP.bar(b, f"{nm(hs[2])}:3.5 R:0.5")
        else:
            for tr, m in zip((TB, SX, TP), hs): tr.bar(b, f"{nm(m)}:0.5 R:0.5 {nm(m)}:1 R:2")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        key2 = n == "最後のサビ"
        j = i % 16                                              # 最後のサビは2回り（1回り目は少し薄く、2回り目がいちばん厚い）
        chd(PN, b, SKANK2 if i % 4 == 3 else SKANK, 64)
        if not (key2 and i < 8): chd(ORL, b, "x:4", 67)
        if (n == "サビ1" and i >= 8) or n == "サビ2" or (key2 and i >= 8): chd(ORG, b, BUBBLE, 69)
        # ホーン: 歌が休む所で答える。サビ1 は文の終わりだけ、サビ2 は返事の小節の頭にも、最後のサビは「ちりんちりん」をいっしょに吹く
        hook = j in (0, 2, 8, 10, 14)
        if hook and key2:
            ln = KC.mel(VC[j], oct=4); TP.bar(b, ln); TB.bar(b, tr_line(ln, -12))
            if i >= 16: SX.bar(b, under(ln, S.chords[b]))
        elif hook and n == "サビ2":
            horn3(b, "R:3 x:0.5 x:0.5", 67)
        elif j in (5, 7):
            horn3(b, "R:2.5 x:0.5 R:0.5 x:0.5" if n == "サビ1" else "R:2 x:0.25 R:0.25 x:0.5 R:0.5 x:0.5", 67)
        elif j in (4, 12) and n != "サビ1":
            hs = sorted(voice(root(b), 65, 3))
            for tr, m in zip((TB, SX, TP), hs): tr.bar(b, f"{nm(m)}:3.5 R:0.5")
        elif j == 15:                                           # サビの終わり: テーマの1小節目でしめる
            tl = tr_line(THEME[0], 2 if key2 else 0); TP.bar(b, tl); SX.bar(b, under(tl, S.chords[b])); TB.bar(b, tr_line(tl, -12))
    elif n == "かけあい":                                        # 歌の「ちりんちりん」→ ホーン3本が答える
        chd(PN, b, SKANK); 
        if i >= 4: chd(ORG, b, BUBBLE, 67)
        if i % 2 == 1:
            ln = ANS[i // 2]; TP.bar(b, ln); SX.bar(b, under(ln, S.chords[b])); TB.bar(b, tr_line(ln, -12))
    elif n == "トロンボーンのソロ":
        chd(PN, b, SKANK2 if i % 4 == 3 else SKANK); chd(ORG, b, BUBBLE, 67)
        TB.bar(b, TBSOLO[i])
        if i >= 4 and i % 2 == 1:                               # 後半はトランペットとサックスが合いの手
            hs = sorted(voice(root(b), 67, 3)); TP.bar(b, f"R:3 {nm(hs[2])}:0.5 {nm(hs[2])}:0.5"); SX.bar(b, f"R:3 {nm(hs[1])}:0.5 {nm(hs[1])}:0.5")
    elif n == "トランペットのソロ":                                # トランペットが高い所で吹き、トロンボーンとサックスは裏拍の和音
        chd(PN, b, SKANK2 if i % 4 == 3 else SKANK); chd(ORG, b, BUBBLE, 67)
        TP.bar(b, TPSOLO[i])
        hs = sorted(voice(root(b), 60, 3))
        if i % 2 == 1 or i >= 6: TB.bar(b, f"R:2.5 {nm(hs[0])}:0.5 R:0.5 {nm(hs[0])}:0.5"); SX.bar(b, f"R:2.5 {nm(hs[1])}:0.5 R:0.5 {nm(hs[1])}:0.5")
    elif n == "Cメロ":                                          # 信号待ち: ピアノの長い和音とオルガン。黄色い点めつ＝ベルが2拍ごと
        chd(PLG, b, "x:4", 62); chd(ORL, b, "x:4", 67)
        if i >= 8:
            hs = sorted(voice(root(b), 58 + i // 2, 3)); TB.bar(b, f"{nm(hs[0])}:4"); SX.bar(b, f"{nm(hs[1])}:4")
            if i >= 12: TP.bar(b, f"{nm(hs[2])}:4" if i < 15 else f"{nm(hs[2])}:3 R:1")
    elif n == "おわり":
        if i < 6:
            chd(PN, b, SKANK, 64); chd(ORG, b, BUBBLE, 69); theme(b, i if i < 4 else i - 4, 2)
        elif i == 6:
            horn3(b, "x:0.5 R:0.5 x:0.5 R:0.5 x:1 R:1", 69); chd(PN, b, "x:0.5 R:0.5 x:0.5 R:0.5 x:1 R:1", 65)
        else:
            horn3(b, "x:1 R:3", 72); chd(PN, b, "x:1 R:3", 67)

# 自転車のベル: 「ちりんちりん」のすき間（2拍目）と小節の終わりに答える。出だしはベルだけで、サビのリズムを先に聞かせる
S_BELL = "F6:0.25 F6:0.25"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ベル" and i in (0, 2): BELL.bar(b, "F6:0.5 Bb6:0.5 Bb6:0.5 R:0.5 F6:0.5 Bb6:0.5 Bb6:1")
    elif n == "かけあい" and i % 2 == 0: BELL.bar(b, "R:1.5 F6:0.25 F6:0.25 R:2")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        j = i % 16
        top_ = "G6" if n == "最後のサビ" else "F6"
        if j in (0, 2, 8, 10, 14): BELL.bar(b, f"R:1.5 {top_}:0.25 {top_}:0.25 R:2")
        if j == 15: BELL.bar(b, f"R:3 {top_}:0.25 {top_}:0.75")
    elif n == "Aメロ2" and i == 11:                                # 「あのふし」→ 窓からの鼻歌（合いことばの節 3・5・6・5・2）
        HUMT.bar(b, "R:2.5 D5:0.5 F5:0.5 G5:0.5"); HUMT.bar(b + 1, "F5:0.5 C5:1 R:2.5")
    elif n == "Aメロ2" and i == 13: BELL.bar(b, "R:3 F6:0.25 F6:0.75")     # 「ちりんと」
    elif n == "Cメロ" and i < 14: BELL.bar(b, "R:1 D6:1 R:1 D6:1" if i < 12 else "R:1 D6:1 R:2")       # 黄色い点めつ
    elif n == "おわり" and i == 7: BELL.bar(b, "R:2 G6:0.25 G6:1.75")

# ================= ベース（この曲のために書く。共通の部品 bass_line は使わない）=================
def bl(b, style):
    ch = S.chords[b]; r = low(ch, "F1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "F1")
    up = tones(root(b), nm(r + 1), nm(r + 12))
    t3 = next((m for m in up if (m - r) in (3, 4)), r + 4); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); t6 = next((m for m in up if (m - r) in (9, 10)), r + 9)
    o = r + 12; ap = (rn - 1 if rn > r else rn + 1) if rn != r else t5
    N = nm
    return {"walk_up": f"{N(r)}:1 {N(t3)}:1 {N(t5)}:1 {N(t6)}:1",                              # 歩く: のぼる
            "walk_dn": f"{N(o)}:1 {N(t6)}:1 {N(t5)}:1 {N(ap)}:1",                             # 歩く: おりて、次の和音の半音となりへ
            "walk_mid": f"{N(r)}:1 {N(t5)}:1 {N(t3)}:1 {N(ap)}:1",
            "two": f"{N(r)}:1.5 R:0.5 {N(t5)}:1.5 R:0.5",                                     # 1拍目と3拍目だけ（静かな所）
            "bounce_a": f"{N(r)}:1 {N(t5)}:0.5 {N(r)}:0.5 {N(o)}:1 {N(t5)}:0.5 {N(ap)}:0.5",          # サビ: 8分ではねる
            "bounce_b": f"{N(r)}:0.5 {N(r)}:0.5 {N(t3)}:0.5 {N(t5)}:0.5 {N(t6)}:1 {N(t5)}:0.5 {N(ap)}:0.5",
            "push": f"{N(r)}:0.5 {N(r)}:0.5 {N(r)}:0.5 {N(r)}:0.5 {N(t3)}:0.5 {N(t3)}:0.5 {N(t5)}:0.5 {N(ap)}:0.5",   # 最後のサビ: 8分で押す
            "pedal": f"{N(r)}:1 {N(r)}:1 {N(r)}:1 {N(r)}:0.5 {N(ap)}:0.5",
            "climb": f"{N(r)}:0.5 {N(t3)}:0.5 {N(t5)}:0.5 {N(t6)}:0.5 {N(o)}:0.5 {N(t6)}:0.5 {N(t5)}:0.5 {N(t3)}:0.5",
            "stop": f"{N(r)}:1 R:3", "hit2": f"{N(r)}:0.5 R:0.5 {N(r)}:1 R:2",
            "long": f"{N(r)}:3.5 R:0.5", "end": f"{N(r)}:0.5 R:0.5 {N(r)}:0.5 R:0.5 {N(o)}:1 R:1"}[style]


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ベル" and i >= 2: BASS.bar(b, bl(b, "two") if i == 2 else "F2:1 R:1 F2:0.5 G2:0.5 A2:0.5 A2:0.5")
    elif n == "かけあい": BASS.bar(b, bl(b, "climb" if i == 7 else ("bounce_a" if i % 2 == 0 else "walk_dn")))
    elif n in ("テーマ", "間奏", "トロンボーンのソロ", "トランペットのソロ"): BASS.bar(b, bl(b, "climb" if i == 7 else ("walk_up" if i % 2 == 0 else "walk_dn")))
    elif n == "Aメロ1": BASS.bar(b, bl(b, ("walk_up" if i % 2 == 0 else "walk_mid") if i < 8 else ("climb" if i == 15 else ("walk_up" if i % 2 == 0 else "walk_dn"))))
    elif n == "Aメロ2": BASS.bar(b, bl(b, "two" if i < 4 else (("walk_mid" if i % 2 == 0 else "walk_dn") if i < 15 else "climb")))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bl(b, "pedal" if i < 6 else ("push" if i == 6 else "hit2")))
    elif n == "サビ1": BASS.bar(b, bl(b, "climb" if i % 8 == 7 else ("bounce_a" if i % 2 == 0 else "walk_dn")))
    elif n == "サビ2": BASS.bar(b, bl(b, "climb" if i % 8 == 7 else ("bounce_a" if i % 2 == 0 else "bounce_b")))
    elif n == "最後のサビ": BASS.bar(b, bl(b, "climb" if i % 8 == 7 else (("push" if i % 2 == 0 else "bounce_b") if i < 16 else ("bounce_a" if i % 2 == 0 else "bounce_b"))))
    elif n == "Cメロ": BASS.bar(b, bl(b, "long" if i < 12 else ("two" if i < 14 else ("pedal" if i == 14 else "climb"))))
    elif n == "おわり": BASS.bar(b, bl(b, ("walk_up", "walk_dn", "walk_up", "walk_dn", "walk_up", "climb", "end", "stop")[i]))

# ================= ドラム（スカ: 2・4拍のスネア、裏拍のハイハット）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ベル":
        if i in (1, 2): D.set(b, "................" if i == 1 else "X.......X.......", "................", "..x...x...x...x.")
        if i == 3: D.set(b, "X.......X.......", "........x.x.X.XX", "..x...x.........")       # スネアの呼びこみ
    elif n == "かけあい":                                            # キックの4つ打ちと2・4拍のスネア。歌とホーンを前に出す
        D.set(b, "X...X...X...X...", "....X.......X...", "..x...x...x...x." if i < 4 else "x.X.x.X.x.X.x.X.")
        if last: put_fill(D, b, "snare16")
    elif n in ("テーマ", "間奏", "トロンボーンのソロ", "トランペットのソロ"):
        vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X.......X.....x." if i % 2 == 0 else "X.......X.......", s="....X.......X...", h="x.X.x.X.x.X.x.X.", vary=False)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "snare16" if n != "トロンボーンのソロ" else "small")
        if n == "トランペットのソロ" and last: halt(D, b, 3)
    elif n == "Aメロ1":
        if i < 8: D.set(b, "X.......X.......", "....x.......x...", "..x...x...x...x.")                       # 前半: リムと裏拍のハイハットだけ
        else: D.set(b, "X.......X.....x." if i % 2 == 0 else "X.......X.......", "....X.......X...", "x.X.x.X.x.X.x.X.")
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n == "Aメロ2":
        if i < 8: D.set(b, "X.........x....." if i % 2 == 0 else "X.......x.......", "....x.......x...", "..x...x...x...x." if i >= 4 else "................")   # ワンドロップ風に軽く
        else: D.set(b, "X.......X.....x." if i % 2 == 0 else "X.......X.......", "....X.......X...", "x.X.x.X.x.X.x.X.")
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):                                  # タムと4つ打ちでのぼって、8小節目の頭で止まる
        if i < 4: D.set(b, "X...X...X...X...", "................", "..x...x...x...x.")
        elif i < 6: D.set(b, "X...X...X...X...", "....X.......X...", "x.x.x.x.x.x.x.x.")
        elif i == 6: D.set(b, "X...X...X...X...", "X.X.X.X.X.X.XXXX", "................")
        else: halt(D, b, 2); D.S[b] = "X...X..........."; D.K[b] = "X...X..........."
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        kp = "X...X...X...X..." if n != "サビ1" or i >= 8 else ("X.......X.....x." if i % 2 == 0 else "X.....x.X.......")   # サビ1 の前半はまだ4つ打ちにしない
        hh = "x.X.x.X.x.X.x.X." if n != "最後のサビ" or i < 16 else "x.Xxx.Xxx.Xxx.Xx"            # v4b: 裏拍のオープンハイハットをやめた（場面ごとに採点すると、オープンにした サビ2・最後のサビ・おわり だけ 6.1〜6.5 に落ちていた）。閉じたハイハットの裏拍を強く、最後の2回り目だけ16分を足す
        vgroove(D, b, "beat8", ghosts=0.2 if n != "最後のサビ" else 0.3, seed=b, k=kp, s="....X.......X..." if i % 4 != 3 else "....X.......X.X.", h=hh, vary=False)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small" if n == "サビ1" else "tomtrip")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "Cメロ":                                              # 半分の速さ
        if i < 12: D.set(b, "X..............." if i % 2 == 0 else "X.........x.....", "........x.......", "x...x...x...x..." if i >= 4 else "................")
        elif i < 15: D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.x.x.")
        else: D.set(b, "X...X...X.X.X.X.", "X.X.X.X.XXXXXXXX", "................")
    elif n == "おわり":
        if i < 6:
            vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X...X...X...X...", s="....X.......X...", h="x.X.x.X.x.X.x.X.", vary=False)
            if i == 0: crash(D, b)
            if i == 5: put_fill(D, b, "snare16")
        elif i == 6: D.set(b, "X...X...X.......", "X...X...X.......", "................")
        else: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)

cym_swell(CYM, S.sc("サビ2")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# 止め: Bメロ の8小節目は、頭の2拍のあと全員休み（そこでベルが「ちりん」と鳴って、サビに入る）
for nme in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(nme)[-1], 2, 4)
SIL.apply()
for nme in ("Bメロ1", "Bメロ2"): BELL.bar(S.sc(nme)[-1], "R:3 F6:0.25 F6:0.75")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の04（3時）。ホーン隊のスカ（ギターなし）。B♭→C・176。まだ暗い町を自転車で新聞を配る。"
          "サビの「ちりんちりん」に自転車のベルが答える。ピアノとオルガンの裏打ち・トランペット・テナーサックス・トロンボーン・歩くベース。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"Cメロ": -0.5, "かけあい": -0.1, "最後のサビ": 0.4})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ピアノ（裏打ち"); humanize(path, "オルガン", mid=80, down=8, up=8, seed=4)
# 測ると サビ1 −17.7・サビ2 −16.7・最後のサビ −17.0 → 最後をいちばん大きくする（山は最後）
final_gain(path, {"サビ2": 0.3, "最後のサビ": 1.5, "おわり": 1.0})
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    # 息つぎの音は入れない。ウィスパーも使わない（docs/sound/composer-preferences.md「歌声で今後必ずやらないこと」）
    vocal_polish(path, S, {"verse": 6, "pre": 16, "chorus": 20, "最後のサビ": 24, "bridge": 10}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 16, None, KC)], vol=0.36)
    voice_by_scene(path, S, {}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.5   # softCons: 息の子音だけ 約 −6dB。 この曲は「ち」（ちりんちりん）が多く、0.5 だと「ち」の出だしが母音と 2〜3dB 差で 51 か所あった
    save(path, js)
