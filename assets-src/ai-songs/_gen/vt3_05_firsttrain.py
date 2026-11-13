# vt3 05「始発までのベンチ」Bench Before the First Train（仮）— シンセのドリームポップ（ギターなし）。92・4/4。D長調。
# 第3弾（0時〜24時の街）の 4時。表は docs/sound/vt3-plan.md。
#
# v4（2026-11-13）: ゼロから作り直し（人間「全ての曲を1みたいにこだわって作って」「このレベル（02 v7）まで詰めて曲作って」）。
#   v1〜v3 はシューゲイザー（歪ませたギターの壁）。ギターに聞こえないギターの音は使わない決まりなので、音の壁はシンセで作る。
#
# 物語: 終電をのがして、駅のベンチで朝を待つ「わたし」。ホームはしんとしていて、星がひとつだけ。時計の針は進まない。
#   東の空が少しずつ白くなり、遠くで鳥が鳴く。どこかで聞いた鼻歌（1時のラジオの節 3・5・6・5・2）を口ずさむ。始発が光をつれて来る。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: 乗りおくれた夜が、「この夜にだけひらく朝の色を見つけた」夜に変わる（最後のサビ）。
#
# 曲を決める表（書く前に similar_check.py --plan で確かめた: いちばん近い曲でも近さ 20%）:
#   形: 駅のチャイム（2つの音）→ Aメロ1（声・はじく音の分散和音・オルガンの持続音だけ）→ Bメロ → サビ1（やわらかい壁が半分・ドラムは半分の速さ）
#       → 間奏（チャイムの節）→ Aメロ2（ベースとドラムが入る）→ Bメロ2 → サビ2（壁が厚くなる）→ 間奏2（すべる音のリードが歌う）
#       → ブリッジ（鼻歌・ほぼ無音）→ 最後のサビ（始発が来る: キックとベースが「ガタン・ゴトン」のリズムになる・いちばん厚い）→ チャイムで終わる
#   旋律: Aメロ＝1拍おいてから入る、のばす音の多いつぶやき（2番は8分の弱起で少し動く）。Bメロ＝8分で上がって長い音。
#         サビ＝「あ・と・すこし」を同じ形で2回（2回目は和音に合わせて）、そのあと高い所から長くおりる
#   和音: Aメロ I △7 → iii → IV △7 → Vsus。サビは IV → V6 → I/III → vi → ii → Vsus → I（宙に浮いたまま主和音に着く）
#   ベース: 2番から。のばす音にオクターブ上をそっと足す形。最後のサビだけ「ガタン・ゴトン」（付点のリズム）
#   この曲だけ: ①駅のチャイムの2つの音（始まり・間奏・終わり）②空の明るさに合わせて厚くなるシンセの壁 ③始発が来ると電車のリズムになる
#
# ドリームポップ／シューゲイザーの作り方（2026-11-13 に調べた。melodigging.com の dream pop、beatkey の shoegaze の作り方、output.com、jackrighteous.com）:
#   テンポは 70〜110。パッドは立ち上がりが遅く余韻が長い音を重ね、リフではなく分散和音とのばす和音を使う。ドラムは目立たせず、うしろで脈を打つだけ。
#   ベースは単純で歌うような線で、低い所をふさがない。壁を厚くしても、キックとスネアの脈・ベースの根音・歌の旋律のどれかは、はっきり聞こえるように残す。
#   最初から最後まで壁を最大にしない（場面ごとに厚さを変える）。歌は深い響きの中に置く。
from vt25_lib import *

S = Song("05", "firsttrain", "始発までのベンチ（仮）", "Bench Before the First Train", 92, 4, "D", "major", "シンセのドリームポップ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space hall --space-wet 0.2"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.4
S.drum_scale = 0.8
S.keepers = {}
K = Key("D", "major")          # oct 4 で 1 = D4

A_CH = ["Dmaj7", "F#m7", "Gmaj7", "A7sus4", "Dmaj7", "F#m7", "Em7", "A7sus4"]
B_CH = ["Bm7", "F#m7", "Gmaj7", "A"]
C_CH = ["Gmaj7", "A6", "D/F#", "Bm7", "Em7", "A7sus4", "Dmaj7", "Dmaj7"]

S.scene("チャイム", 4, "intro", ["Dmaj7", "Dmaj7", "Gmaj7", "A7sus4"])
S.scene("Aメロ1", 16, "verse", A_CH + A_CH)
S.scene("Bメロ1", 4, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 4, "break", ["Dmaj7", "F#m7", "Gmaj7", "A7sus4"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("間奏2", 8, "solo", C_CH)
S.scene("ブリッジ", 8, "bridge", ["Dmaj7", "A6", "Dmaj7", "A6", "Bm7", "Gmaj7", "Em7", "A7sus4"])
S.scene("最後のサビ", 16, "chorus", C_CH + C_CH)
S.scene("おわり", 6, "outro", ["Dmaj7", "Gmaj7", "Dmaj7", "Gmaj7", "Dmaj7", "Dmaj7"])

PING = [{"type": "pingpong", "beats": 0.75, "mix": 0.22, "feedback": 0.35}]
V = Voice(S, vol=0.2, delay=0.75, bright=0.0, patch="kfbSineLead", low=False)
CHM = S.track("駅のチャイム（ビブラフォン）", "lead", patch="vibraphone", volume=0.16, pan=0.25, reverb=0.5)
ARP = S.track("はじく音の分散和音", "lead", patch="glassPluck", volume=0.11, pan=-0.3, reverb=0.4, fx=PING)
ARP2 = S.track("はじく音の分散和音（上）", "lead", patch="glassPluck", volume=0.04, pan=0.35, reverb=0.45, fx=PING)
DRN = [S.track(f"オルガンの持続音{i + 1}", "lead", patch="reedOrgan", volume=0.055, pan=-0.2 + 0.4 * i, reverb=0.45,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 2200, "q": 0.6}]) for i in range(2)]
PADA = [S.track(f"やわらかい壁{i + 1}", "lead", patch="kfbSparklePad", volume=0.03, pan=-0.45 + 0.45 * i, reverb=0.5) for i in range(3)]
PADB = [S.track(f"厚い壁{i + 1}", "pad", patch="supersawPad", volume=0.024, pan=0.5 - 0.5 * i, reverb=0.45, duck=0.4,
                fx=[{"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 5200, "q": 0.6}]) for i in range(3)]
STR = S.track("弦の高い線", "strings", patch="slowStrings", volume=0.05, pan=0.3, reverb=0.5, sustain=1.5)
LEAD = S.track("すべる音のリード", "lead", patch="kfbSineLead", volume=0.085, pan=-0.1, reverb=0.45, fx=[{"type": "pingpong", "beats": 1.5, "mix": 0.18, "feedback": 0.3}])
BASS = S.track("ベース（指弾き・丸い音）", "bass", sustain=1.3, **dict(finger_bass_spec(vol=0.19), fx=[{"type": "eq", "low": 1, "mid": 0, "midHz": 800, "high": -4}, {"type": "filter", "kind": "lowpass", "freq": 1100, "q": 0.6}]))
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.03, pan=0, duck=0.5)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.045, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
# Aメロ（1回り目）: 1拍おいて入る、のばす音のつぶやき
VA = ["R:1 3:1 5:1.5 3:0.5", "2:1.5 1:1.5 R:1", "R:1 2:1 3:1.5 2:0.5", "1:1.5 2:1.5 R:1",
      "R:1 3:1 5:1.5 6:0.5", "5:1.5 3:1.5 R:1", "R:1 2:1 4:1.5 3:0.5", "2:3 R:1"]
# Aメロ（2回り目と2番）: 8分の弱起で少し動く
VA2 = ["R:0.5 3:0.5 3:1 5:1.5 3:0.5", "2:1.5 1:1.5 R:1", "R:0.5 2:0.5 2:1 3:1.5 2:0.5", "1:1.5 2:1.5 R:1",
       "R:0.5 5:0.5 5:1 1':1.5 6:0.5", "5:1.5 3:1.5 R:1", "R:1 4:1 6:1.5 5:0.5", "5:3 R:1"]
A1 = "しゅうでんの/あかりきえ/べんちには/ひとりで/ほしはひとつ/といきはしろ/とけいのはり/ねむそう"
A2 = "ひがしのそら/すこししろく/とおくでとり/ないてる"
VB = ["R:1 1:0.5 2:0.5 3:1 5:1", "5:1.5 6:0.5 5:1 R:1", "R:1 3:0.5 5:0.5 6:1 1':1", "2':3 R:1"]
B1 = "ねむいめこすり/みあげたら"
B2 = "あのよるのふし/くちずさむ"
# サビ: 「あとすこし」を同じ形で2回 → 高い所から長くおりる → もう一度「あとすこし」
VC = ["5:1 1':1 1':0.5 7:0.5 5:0.5 R:0.5", "5:1 2':1 2':0.5 1':0.5 7:0.5 R:0.5", "3':1.5 2':0.5 1':1 6:0.5 5:0.5", "6:2 R:2",
      "4:1 6:1 6:0.5 5:0.5 4:0.5 R:0.5", "5:1 1':1 1':0.5 7:0.5 5:0.5 R:0.5", "3:1 5:1 1':1.5 7:0.5", "1':3 R:1"]
C1 = "あとすこし/あとすこし/おはようまで/もうすこし/あとすこし/よるがとけ"
C2 = "あとすこし/あとすこし/しはつのおと/まぶしくて/なきそうで/ほほえんだ"
C3 = ("あとすこし/あとすこし/ひかりつれて/くるでんしゃ/あとすこし/そらがあく/"
      "このよるに/だけひらく/あさのいろを/みつけたよ/ただいまと/かえろうか")
# ブリッジ: 鼻歌（合いことばの節 3・5・6・5・2）を2回 → 「どこかでね、聞いた節」
VBR = ["R:2 3:0.5 5:0.5 6:1", "5:0.5 2:1.5 R:2", "R:2 3:0.5 5:0.5 6:1", "5:0.5 2:1.5 R:2",
       "R:1 1:1 3:1 5:1", "6:2 5:1 R:1", "R:1 4:1 5:1 6:1", "1':1.5 2':1.5 R:1"]
CB = "ららららら/ららららら/どこかでね/きいたふし"
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA2, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA2, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("ブリッジ", VBR, CB)
put("最後のサビ", VC + VC, C3)

# ================= 和音と線 =================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]


def pad(tracks, b, c=66, L="4"):
    v = sorted(voice(root(b), c, 3))
    for j in range(len(tracks)): tracks[j].bar(b, f"{nm(v[j])}:{L}" + ("" if L == "4" else f" R:{4 - float(L):g}"))


def arp(b, order, lo="A3", hi="A5", tr=None):
    tn = tones(root(b), lo, hi)
    (tr or ARP).bar(b, " ".join(f"{nm(tn[q % len(tn)])}:0.5" for q in order))


def arp4(b):
    """4つの音だけ鳴らして、あとは余韻（すき間を多く）"""
    tn = tones(root(b), "A3", "A5"); ARP.bar(b, " ".join(f"{nm(tn[q])}:0.5" for q in (0, 2, 3, 4)) + " R:2")


UP = (0, 2, 3, 4, 5, 4, 3, 2)          # のぼっておりる
WAVE = (0, 3, 2, 4, 3, 5, 4, 2)        # 波
HIGH = (3, 5, 4, 6, 5, 7, 6, 4)        # 上の段（最後のサビ）


def drone(b):
    r = low(S.chords[b], "D3"); DRN[0].bar(b, f"{nm(r)}:4"); DRN[1].bar(b, f"{nm(tones(root(b), nm(r + 5), nm(r + 9))[0])}:4")


CHIME = "F#5:2 D5:2"                   # 駅のチャイム（2つの音）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "チャイム":
        if i in (0, 2): CHM.bar(b, CHIME if i == 0 else "G5:2 D5:2")
        drone(b); pad(PADA[:2], b, 69)                              # v5: 出だしが小さすぎた（BGM −30dB）→ 持続音にやわらかい壁を足し、チャイムを大きく
        if i >= 2: arp(b, UP)
        elif i == 1: arp4(b)
    elif n == "Aメロ1":
        drone(b)
        if i < 8:
            arp4(b); pad(PADA[:1], b, 69)   # v7: 前半は毎小節4つの音と、やわらかい壁を1本（1小節おきだと、歌のない版で出だしから 8dB 下がり、すき間が無音に近かった）
        else:
            arp(b, UP if i % 2 == 0 else WAVE)
            if i >= 12: pad(PADA[:2], b, 69)
            if i == 11: CHM.bar(b, "R:2 A5:2")
    elif n == "Aメロ2":
        drone(b); arp(b, WAVE if i % 2 == 0 else UP); pad(PADA[:2], b, 69)
        if i in (3, 7): CHM.bar(b, "R:2 E5:1 A5:1")                      # 「とおくで鳥」: チャイムの音が2つ答える
    elif n in ("Bメロ1", "Bメロ2"):
        drone(b); pad(PADA, b, 66 + 2 * i)
        arp(b, UP if i < 3 else (0, 1, 2, 3, 4, 5, 6, 7))
        if n == "Bメロ2": pad(PADB[:2], b, 62 + 2 * i)
        st = tones(root(b), "A4", "A6"); STR.bar(b, f"{nm(st[min(i + 1, len(st) - 1)])}:4")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        j = i % 8
        drone(b); pad(PADA, b, 69)
        arp(b, UP if j % 2 == 0 else WAVE)
        if n != "サビ1": pad(PADB, b, 64)                               # サビ2 から厚い壁
        if n == "サビ1" and j >= 4: pad(PADB[:1], b, 64)
        if n == "最後のサビ":
            arp(b, HIGH, tr=ARP2)
            st = tones(root(b), "D5", "D6"); STR.bar(b, f"{nm(st[-1] if i >= 8 else st[-2])}:4")
        elif n == "サビ2" and j >= 4:
            st = tones(root(b), "D5", "D6"); STR.bar(b, f"{nm(st[-2])}:4")
        if j == 3: CHM.bar(b, "R:2 F#5:1 D5:1")                          # 歌が休む所でチャイムが答える
    elif n == "間奏":
        drone(b); arp(b, UP); pad(PADA[:2], b, 69)
        CHM.bar(b, [CHIME, "R:4", "G5:2 D5:2", "R:2 E5:2"][i])
    elif n == "間奏2":                                                  # 厚い壁の上で、すべる音のリードが歌う（サビの節を高い所で、少し変えて）
        drone(b); pad(PADA, b, 69); pad(PADB, b, 64); arp(b, WAVE if i % 2 == 0 else UP)
        LEAD.bar(b, K.mel(["5:1 1':1 3':1.5 2':0.5", "2':2.5 R:0.5 1':0.5 7:0.5", "3':1.5 2':0.5 1':1 6:0.5 5:0.5", "6:3 R:1",
                           "4:1 6:1 1':1.5 2':0.5", "2':2 3':1 2':1", "3':1 5':1 3':1.5 2':0.5", "1':3 R:1"][i], oct=5))
    elif n == "ブリッジ":
        if i < 4:
            # v5: 前半をほぼ無音にしたら、場面の大きさをそろえる仕上げが後半を持ち上げて、ブリッジが曲でいちばん大きくなった（−7dB）。
            #   → 前半にも持続音とやわらかい壁を置いて、場面の中の大きさの差を小さくする（静かなままだが、無音にはしない）
            drone(b); pad(PADA[:2], b, 66)
            if i % 2 == 0: arp4(b)
            if i in (1, 3): CHM.bar(b, "R:2.5 A5:1.5")
        else:
            drone(b); pad(PADA[:2], b, 64 + i); (arp4(b) if i < 7 else arp(b, (0, 1, 2, 3, 4, 5, 6, 7)))
            if i == 7: pad(PADB, b, 66); st = tones(root(b), "A4", "A6"); STR.bar(b, f"{nm(st[-2])}:4")
    elif n == "おわり":
        if i < 4:
            drone(b); pad(PADA[:2], b, 69)
            arp(b, UP) if i < 2 else arp4(b)
        if i == 4: CHM.bar(b, CHIME); DRN[0].bar(b, "D3:4")
        if i == 5: DRN[0].bar(b, "D3:3 R:1")


# ================= ベース（この曲のために書く。共通の部品 bass_line は使わない）=================
def bl(b, style):
    ch = S.chords[b]; r = low(ch, "E1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "E1")
    up = tones(root(b), nm(r + 1), nm(r + 12))
    t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); t3 = next((m for m in up if (m - r) in (3, 4)), r + 4)
    o = r + 12; ap = t5 if rn == r else (rn + 2 if rn < r else rn - 2)
    N = nm
    return {"long": f"{N(r)}:3.5 R:0.5",
            "sway": f"{N(r)}:2.5 {N(o)}:1 {N(t5)}:0.5",                          # のばして、オクターブ上をそっと
            "sway_b": f"{N(r)}:1.5 {N(t5)}:1 {N(o)}:1 {N(ap)}:0.5",
            "pulse": f"{N(r)}:1 {N(r)}:1 {N(r)}:1 {N(t5)}:0.5 {N(ap)}:0.5",       # サビ2: 4分で脈を打つ
            "pulse_b": f"{N(r)}:1 {N(r)}:0.5 {N(t3)}:0.5 {N(t5)}:1 {N(o)}:0.5 {N(ap)}:0.5",
            "train": f"{N(r)}:0.75 {N(r)}:1.25 {N(r)}:0.75 {N(r)}:0.75 {N(t5)}:0.5",     # 最後のサビ: ガタン・ゴトン
            "train_b": f"{N(r)}:0.75 {N(r)}:1.25 {N(o)}:0.75 {N(t5)}:0.75 {N(ap)}:0.5",
            "rise": f"{N(r)}:1 {N(t3)}:1 {N(t5)}:1 {N(o)}:1"}[style]


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "Aメロ2": BASS.bar(b, bl(b, "sway" if i % 2 == 0 else "sway_b"))
    elif n == "Aメロ1" and i >= 8: BASS.bar(b, bl(b, "long"))       # v6: Aメロ1 の伴奏が小さすぎた（仕上げ前で −41〜−52dB）→ 後半からベースののばす音
    elif n == "Bメロ2": BASS.bar(b, bl(b, "long" if i < 3 else "rise"))
    elif n == "Bメロ1" and i == 3: BASS.bar(b, bl(b, "long"))
    elif n == "サビ1": BASS.bar(b, bl(b, "long" if i < 7 else "sway_b"))
    elif n == "間奏": BASS.bar(b, bl(b, "long"))
    elif n == "サビ2": BASS.bar(b, bl(b, "pulse" if i % 2 == 0 else "pulse_b"))
    elif n == "間奏2": BASS.bar(b, bl(b, "sway_b" if i % 2 == 0 else "pulse_b"))
    elif n == "ブリッジ" and i == 7: BASS.bar(b, bl(b, "rise"))       # v6: ブリッジの後半が サビ と同じ大きさ（−14dB）だった → ベースは最後の1小節だけ
    elif n == "最後のサビ": BASS.bar(b, bl(b, "train" if i % 2 == 0 else "train_b"))
    elif n == "おわり" and i < 4: BASS.bar(b, bl(b, "long"))
    if n in ("サビ2", "間奏2", "最後のサビ"): SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:3.5 R:0.5")

# ================= ドラム（うしろで脈を打つ。最後のサビだけ電車のリズム）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "Aメロ1" and i >= 12: D.set(b, "X...............", "................", "....x.......x...")
    elif n == "Bメロ1": D.set(b, "X.......X.......", "................", "....x.......x..." if i < 3 else "....x...x.x.x.x.")
    elif n == "サビ1":                                              # 半分の速さ（スネアは3拍目）
        D.set(b, "X.........x....." if i % 2 == 0 else "X.....x...x.....", "........X.......", "x...x...x...x...")
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "small")
    elif n == "間奏": D.set(b, "X...............", "........x.......", "x...x...x...x...")
    elif n == "Aメロ2":
        D.set(b, "X.....x...X....." if i % 2 == 0 else "X.........X..x..", "....x.......x...", "x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "small")
    elif n == "Bメロ2":
        D.set(b, "X...X...X...X...", "................" if i < 2 else "....X.......X...", "x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "snare16")
    elif n in ("サビ2", "間奏2"):
        vgroove(D, b, "beat8", ghosts=0.25, seed=b, k="X.....x...X....." if i % 2 == 0 else "X..x......X.....", s="....X.......X...", h="x.x.x.x.x.x.x.x.", vary=False)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "tomtrip" if n == "サビ2" else "small")
    elif n == "ブリッジ":
        if i >= 6: D.set(b, "X.......X......." if i == 6 else "X...X...X.X.X.X.", "................" if i == 6 else "....X...X.X.XXXX", "x...x...x...x..." if i == 6 else "................")
    elif n == "最後のサビ":                                          # ガタン・ゴトン（キックが付点で2回ずつ）
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X..X....X..X....", s="....X.......X..." if i % 4 != 3 else "....X.......X.X.", h="x.xxx.xxx.xxx.xx", vary=False)
        if i % 8 == 0: crash(D, b, "C2", 6)
        if i == 7: put_fill(D, b, "tomtrip")
    elif n == "おわり":
        if i == 0: crash(D, b, "C2", 6)
        if i < 2: D.set(b, "X..X....X..X....", "................", "x...x...x...x...")
        elif i < 4: D.set(b, "X.......X.......", "................", "................")

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("サビ2")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の05（4時）。シンセのドリームポップ（ギターなし）。D・92。終電をのがした駅のベンチで朝を待つ。"
          "駅のチャイムの2つの音、空の明るさに合わせて厚くなるシンセの壁、始発が来ると電車のリズムになる最後のサビ。自作")
finish(S, LY, V, 0,
       level={"verse": -0.25}, special={"ブリッジ": -0.6, "最後のサビ": 0.4})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "はじく音", mid=80, down=10, up=8, seed=3)
# v6: 仕上げ前の音を測ると、Aメロ1 −41〜−52dB・ブリッジ後半 −14dB（サビ −13.5dB）で、静かな場面と大きい場面が逆だった。
#   → 分散和音と持続音そのものを大きくし、Aメロ1 を持ち上げ、ブリッジを下げる。出だしは Aメロ1 より大きくしない
scene_gain(path, S, {"チャイム": 1.2, "Aメロ1": 1.6, "ブリッジ": 0.5})
# v6 を測ると、出だし −29（歌入り）・−36（BGM）で小さすぎ、最後のサビ（−15.3）が サビ2（−15.1）より小さかった → 仕上げで直す（出だしは Aメロ1 より大きくしない）
final_gain(path, {"チャイム": 8.0, "サビ1": 1.2, "サビ2": -0.3, "最後のサビ": 1.3, "ブリッジ": 2.0} if VOCAL else {"チャイム": 11.0, "サビ1": 1.2, "サビ2": -0.3, "最後のサビ": 1.5, "ブリッジ": 3.0})
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",), jump=7, minlen=2.0))
    vocal_polish(path, S, {"verse": 8, "pre": 14, "chorus": 22, "最後のサビ": 26, "bridge": 6}, scoop=0.3, slash=0.7, vib_min_beats=2.0, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 4, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["reverb"] = 0.26     # 歌は深めの響きの中に（ドリームポップ）。声そのものはクリアのまま
    save(path, js)
