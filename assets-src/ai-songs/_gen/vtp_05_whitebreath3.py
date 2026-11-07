# vtp 05「白い息のリテイク」第3版（仮）— 重音テト・ボカロック（冬）。150・4/4。Bm／D長調 → 最後のサビは +1（E♭長調）。
# 2026-11-07 人間「テトの曲作りましょう」「和音も単音も上手く使って。あとコード進行を変えて」
#   前の版（vtp_01・02）は「曲がつまらない」「音・弾き方が素人」。前夜祭は「和音になったけど曲として成立してない」。
# この版で変えたこと:
#   ・ドラム＝人の演奏データ（Groove MIDI）。場面ごとに、その場面に合う所（フィルの位置）を選んでつなぐ
#   ・ギター＝弾く場所は曲に合わせて型で決め、本物のギタリストの揺れ方（GuitarSet）だけを借りる（strum_groove.py）
#       左＝低い押さえ方の和音のかき鳴らし（全編）／右＝単音の分散和音（Aメロ・Cメロ・落ちサビ）→ 単音の旋律（Bメロ）→ 高い和音の16分（サビ）
#       リード＝単音のリフ（前奏・間奏）・合いの手・ソロ
#   ・コード進行: 王道進行（Ⅳ→Ⅴ→Ⅲm→Ⅵm）は使わない。
#       Aメロ＝Bm の下降（Bm→Bm/A#→Bm/A→G#m7♭5）／サビ＝Ⅲ（F#/A#）・同主調のⅣm（Gm）・Ⅱ（E）・Ⅵ7（B7）・Ⅳm6（Gm6）
#       「ごめんね」は F#sus4 のまま解決しない／Cメロ＝♭Ⅵ・♭Ⅶ（B♭・C）／落ちサビの最後は B♭7 で E♭ へ
import sys, os, json, copy, re, random
from vt25_lib import *
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools/composer'))
from strum_groove import Groove, Lanes
from gmd_to_parts import parts_from_gmd

S = Song("05", "whitebreath3", "白い息のリテイク（仮）", "White Breath Retake", 150, 4, "D", "major", "ボカロック（冬）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
S.keep_old_synth = True
S.no_depth = True
K = Key("D", "major")
KL = Key("Eb", "major")

RIFF = ["Bm", "D/A", "Gmaj7", "F#7"]
VCH = ["Bm", "Bm/A#", "Bm/A", "G#m7b5", "Gmaj7", "Em7", "F#sus4", "F#"]
BCH = ["Em7", "F#m7", "Gmaj7", "A", "Em7", "F#m7", "Gmaj7", "A7sus4"]
CH = ["D", "F#/A#", "Bm", "D/A", "G", "Gm", "D/F#", "E", "Em7", "A/G", "F#m7", "B7", "Em7", "Gm6", "A", "A"]
CHSAD = CH[:12] + ["Em7", "Gm6", "F#sus4", "F#sus4"]
CMCH = ["Bbmaj7", "C", "Dm7", "Dm7/C", "Bbmaj7", "C", "Bb", "C"]
OCH = ["D", "F#/A#", "Bm", "D/A", "G", "Gm", "Gm6", "Bb7"]
LASTCH = [tr_chord(c, 1) for c in CH + ["D", "F#/A#", "Bm", "D/A", "G", "Gm6", "A", "D"]]

S.scene("前奏", 10, "intro", ["Bm", "Bm"] + RIFF + RIFF)
S.scene("Aメロ1", 16, "verse", VCH + VCH)
S.scene("Bメロ1", 8, "pre", BCH)
S.scene("サビ1", 16, "chorus", CHSAD)
S.scene("間奏1", 4, "solo", RIFF)
S.scene("Aメロ2", 16, "verse", VCH + VCH)
S.scene("Bメロ2", 8, "pre", BCH)
S.scene("サビ2", 16, "chorus", CH)
S.scene("ソロ", 8, "solo", RIFF + RIFF)
S.scene("Cメロ", 8, "bridge", CMCH)
S.scene("落ちサビ", 8, "bridge", OCH)
S.scene("最後のサビ", 24, "chorus", LASTCH)
S.scene("白い息", 4, "outro", ["Ebmaj7"] * 4)

V = Voice(S, vol=0.2, delay=0.5, bright=0.2, patch="brightLead", low=False)
LEAD = S.track("リードギター（単音）", "leadGuitar", guitarTone="warm-lead-a", volume=0.075, pan=0.1)
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.23))
LY = Lyrics(S)

# ================= 歌（D長調・oct 4: 1＝D4、5,＝A3、3'＝F#5） =================
VA = ["6,:0.5 6,:0.25 1:0.25 3:0.5 3:0.5 2:0.5 1:0.5 2:1", "1:0.5 6,:1 R:2.5",
      "R:0.5 3:0.5 3:0.25 4:0.25 5:0.5 5:0.5 4:0.5 3:0.5 4:0.5", "3:0.5 2:1.5 R:2",
      "6,:0.5 1:0.5 2:0.5 3:1 5:1 3:0.5", "3:0.5 2:0.5 1:0.5 7,:0.5 1:1 R:1",
      "R:1 3:0.5 3:0.5 3:1 2:1", "#5:2 3:1 R:1"]
VA2 = ["6,:0.5 6,:0.25 1:0.25 3:0.5 3:0.5 2:0.5 1:0.5 2:1", "1:0.5 3:1 R:2.5",
       "R:0.5 3:0.5 3:0.25 4:0.25 5:0.5 5:0.5 4:0.5 3:0.5 4:0.5", "3:0.5 2:1.5 R:2",
       "6,:0.5 1:0.5 2:0.5 3:1 6:1 5:0.5", "3:0.5 2:0.5 1:0.5 7,:0.5 1:1 R:1",
       "R:1 3:0.5 4:0.5 5:1 6:1", "#5:1.5 7:0.5 R:2"]
VB = ["R:1 2:0.5 3:0.5 4:1 5:1", "6:3 R:1", "R:1 3:0.5 4:0.5 5:1 6:1", "7:3 R:1",
      "R:1 3:0.5 4:0.5 5:1 6:1", "5:3 R:1", "R:0.5 5:0.5 6:0.5 7:0.5 1':1 2':1", "2':1 R:3"]
CA = ["3':1.5 2':0.5 1':0.5 2':0.5 3':1", "7:0.5 #5:0.25 7:0.25 3':0.5 3':0.5 3':1 R:1"]
CB = ["R:0.5 2':0.5 2':0.5 1':0.5 6:0.5 1':0.5 2':1", "1':0.5 5:0.5 6:0.5 1':0.5 1':1 R:1"]
CC = ["1':1.5 6:0.5 5:0.5 6:0.5 1':1", "b6:0.5 b6:0.5 5:0.5 4:0.5 5:1 R:1"]
CD = ["3:0.5 5:0.5 1':1 7:0.5 1':0.5 2':1", "6:1 #4:0.5 6:0.5 2':1 R:1"]
CE = ["2':1.5 1':0.5 6:0.5 1':0.5 2':1", "7:0.5 5:0.25 7:0.25 2':0.5 2':0.5 2':1 R:1"]
CF = ["R:0.5 3':0.5 3':0.5 2':0.5 7:0.5 2':0.5 3':1", "#1':0.5 6:0.5 #1':0.5 3':0.5 3':1 R:1"]
CG = ["1':1 2':1 3':1 2':0.5 1':0.5", "2':0.5 2':0.5 b6:0.5 5:0.5 4:1 R:1"]
CHh = ["5:0.5 6:0.5 7:0.5 2':0.5 3':2", "2':1 1':0.5 7:0.5 6:0.5 5:0.5 R:1"]
SAD = ["R:1 3':1 2':1 1':1", "6:3 R:1"]
CEND = ["5:0.5 6:0.5 7:0.5 2':0.5 3':2", "3':0.5 2':0.5 2':0.5 1':0.5 1':2"]
CHORUS = CA + CB + CC + CD + CE + CF + CG
PIV = ["2':0.5 2':0.5 b6:0.5 5:0.5 4:1 R:1", "4:0.5 4:0.5 5:0.5 b6:0.5 1':1 R:1"]
VCM = ["R:1 5:1 1':1 b7:1", "2':3 R:1", "R:1 b3':1 2':1 1':1", "5:3 R:1",
       "R:1 5:0.5 b7:0.5 1':1 b3':1", "2':3 R:1", "R:1 1':1 2':1 b3':1", "2':3 R:1"]

A1 = ("えきのまえのひかりに/かぜがほほをさしてく/てぶくろのなかでにぎった/ことばのたね/"
      "なんどもれんしゅうした/さいしょのひとことだけ/きみがふりむくまえにね/いきをすうの")
B1 = "ほしのした/きみがくる/あとすこし/いまいわなきゃ"
C1 = ("ふゆのよるにきみをよぶ/こごえたこえがこぼれた/すきといえたはじめて/しろいいきがきえてく/"
      "ふゆのよるにきみはいう/やさしいめでうつむいて/ありがとうでもいまは/ごめんね")
A2 = ("はるにかみをきってみた/なつのあさははしるの/にがてなこともいちから/やりなおした/"
      "あきのそらはたかくて/かがみのなかのわたし/すこしだけかおをあげた/まえをむいた")
B2 = "ふゆがくる/またおなじ/あのみちへ/こんどこそね"
C2 = ("ふゆがくるまでにかわる/きのうのわたしをこえる/だれのためでもなくて/わたしのためにはしる/"
      "ふゆがくるまでにかわる/ころんだかずだけつよく/なりたいからかおあげ/つぎのふゆまではしれ")
CMT = "ひととせ/このみち/しろいいき/きみのせ"
OC = "ふゆのよるにまたきたよ/いちねんぶんのことばを/こわいけれどいわせて/しろいいきにのせるよ"
C3 = ("ふゆのよるにまたここで/こごえないこえでいうよ/すきだよともういちど/しろいいきがかがやく/"
      "ふゆのよるにきみがいう/こたえはまだいらないよ/いまはただとどけたい/ことしのわたしのこえ/"
      "ふゆのよるにきみをよぶ/こごえたこえはもうない/すきだよともういちど/しろいいきのむこうへ")


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA2, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, CHORUS + SAD, C1)
put("Aメロ2", K, VA + VA2, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, CHORUS + CHh, C2)
put("Cメロ", K, VCM, CMT)
put("落ちサビ", K, CA + CB + CC + PIV, OC)
put("最後のサビ", KL, CHORUS + CHh + CA + CB + CC + CEND, C3)

# ================= リード（単音） =================
RF = ["B4:0.75 B4:0.25 D5:0.5 B4:0.5 E5:1^^@0.3 D5:0.5 B4:0.5", "A4:0.75 A4:0.25 D5:0.5 A4:0.5 F#5:1 E5:0.5 D5:0.5",
      "G4:0.75 G4:0.25 B4:0.5 D5:0.5 F#5:1.5 E5:0.5", "E5:0.5 D5:0.5 C#5:0.5 A#4:0.5 C#5:2~."]
RF8 = "F#5:0.5 E5:0.5 C#5:0.5 A#4:0.5 F#4:2"
SOLO = ["F#4:0.5 B4:0.5 C#5:0.5 D5:0.5 F#5:1.5 E5:0.5", "D5:0.5 C#5:0.5 A4:1 D5:0.5 E5:0.5 F#5:1",
        "E5:2^^@0.3 D5:1 B4:1", "C#5:0.25_ D5:0.25_ E5:0.5 F#5:0.5 E5:0.5 C#5:0.5 A#4:0.5 C#5:1",
        "B5:2!~. A5:0.5 F#5:0.5 D5:1", "F#5:0.5 E5:0.5 D5:0.5 A4:0.5 D5:0.5 E5:0.5 F#5:1",
        "G5:1 F#5:0.5 E5:0.5 D5:0.5 B4:0.5 D5:1", "F#5:4~."]
OBB = "R:3 D5:0.25_ E5:0.25 F#5:0.5"
for name in ("前奏", "間奏1", "ソロ"):
    for i, b in enumerate(S.sc(name)):
        if name == "前奏" and i < 2: continue
        k = i - (2 if name == "前奏" else 0)
        if name == "ソロ": LEAD.bar(b, SOLO[k]); continue
        LEAD.bar(b, RF8 if (name == "前奏" and k == 7) else RF[k % 4])
for name in ("サビ2", "最後のサビ"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 1: LEAD.bar(b, OBB if name == "サビ2" else "R:3 D#5:0.25_ F5:0.25 G5:0.5")

# ================= ベース（指弾き・分数コードの低い音に沿う） =================
def bass_root(ch):
    bs = ch.split("/")[1] if "/" in ch else re.match(r"[A-G][#b]?", ch).group(0)
    return low(bs, "E1")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]; r = bass_root(ch)
    if n == "白い息": BASS.bar(b, f"{nm(r)}:4" if i == 0 else "R:4"); continue
    if n == "前奏": BASS.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.75 {nm(r)}:0.5 R:0.5 {nm(r)}:0.5 {nm(r + 12)}:1"); continue
    if n in ("間奏1", "ソロ"): BASS.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.75 {nm(r)}:0.5 R:0.5 {nm(r)}:0.5 {nm(r + 12)}:1"); continue
    if n in ("Aメロ1", "Aメロ2"):
        BASS.bar(b, f"{nm(r)}:2 {nm(r)}:1.5 {nm(r + 7)}:0.5" if (n == "Aメロ1" and i < 8) else f"{nm(r)}:1.5 {nm(r)}:0.5 R:0.5 {nm(r)}:1 {nm(r + 12)}:0.5"); continue
    if n in ("Bメロ1", "Bメロ2"):
        BASS.bar(b, f"{nm(r)}:0.5 R:3.5" if i == 7 else (f"{nm(r)}:2 {nm(r)}:2" if i < 4 else " ".join([f"{nm(r)}:0.5"] * 8))); continue
    if n == "サビ1" and i >= 14: BASS.bar(b, f"{nm(r)}:4" if i == 14 else "R:4"); continue
    if n == "Cメロ": BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2"); continue
    if n == "落ちサビ": BASS.bar(b, "R:4" if i < 4 else f"{nm(r)}:4"); continue
    BASS.bar(b, " ".join([f"{nm(r)}:0.5"] * 7) + (f" {nm(r + 12)}:0.5" if i % 2 else f" {nm(r)}:0.5"))

S.fade_out = 0
S.desc = ("仮: プロ仕様のボカロ曲（重音テト）05＝白い息のリテイクの第3版。冬のボカロック。Bm／D・150、最後のサビは +1（E♭）。"
          "ドラムは人の演奏データ、ギターは曲に合わせた型に本物のギタリストの揺れ方。左＝和音のかき鳴らし、右＝単音の分散和音→高い和音、リード＝単音のリフ。"
          "王道進行を使わず、Bm の下降・Ⅲ・同主調のⅣm・Ⅵ7・解決しない「ごめんね」。自作")
finish(S, LY, V, 0, hi=80, level={"verse": -0.2}, special={"最後のサビ": 0.4, "サビ1": 0.2})

# ================= 書き出したあとで、ギター（左右）とドラムを足す =================
path = sys.argv[1]
js = json.load(open(path))
NB = S.nb; TOTAL = NB * 4; BPM = 150

# --- 押さえ方（低い弦から。None＝鳴らさない）
VO = {"Bm": [None, "B2", "F#3", "B3", "D4", "F#4"], "Bm/A#": [None, "A#2", "F#3", "B3", "D4", "F#4"], "Bm/A": [None, "A2", "F#3", "B3", "D4", "F#4"],
      "G#m7b5": ["G#2", None, "F#3", "B3", "D4", None], "Gmaj7": ["G2", "B2", "D3", "G3", "B3", "F#4"], "Em7": ["E2", "B2", "D3", "G3", "B3", "E4"],
      "F#sus4": ["F#2", "C#3", "F#3", "B3", "C#4", "F#4"], "F#": ["F#2", "C#3", "F#3", "A#3", "C#4", "F#4"], "F#7": ["F#2", "C#3", "E3", "A#3", "C#4", "F#4"],
      "F#m7": ["F#2", "C#3", "E3", "A3", "C#4", "E4"], "A": [None, "A2", "E3", "A3", "C#4", "E4"], "A7sus4": [None, "A2", "E3", "G3", "D4", "E4"],
      "D": [None, "A2", "D3", "A3", "D4", "F#4"], "F#/A#": [None, "A#2", "F#3", "A#3", "C#4", "F#4"], "D/A": [None, "A2", "D3", "A3", "D4", "F#4"],
      "G": ["G2", "B2", "D3", "G3", "B3", "G4"], "Gm": ["G2", "D3", "G3", "A#3", "D4", "G4"], "D/F#": ["F#2", None, "D3", "A3", "D4", "F#4"],
      "E": ["E2", "B2", "E3", "G#3", "B3", "E4"], "A/G": ["G2", None, "E3", "A3", "C#4", "E4"], "B7": [None, "B2", "D#3", "A3", "B3", "F#4"],
      "Gm6": ["G2", None, "E3", "A#3", "D4", None], "Bbmaj7": [None, "A#2", "F3", "A3", "D4", None], "C": [None, "C3", "E3", "G3", "C4", "E4"],
      "Dm7": [None, None, "D3", "A3", "C4", "F4"], "Dm7/C": [None, "C3", "D3", "A3", "C4", "F4"], "Bb": [None, "A#2", "F3", "A#3", "D4", "F4"],
      "Bb7": [None, "A#2", "F3", "G#3", "D4", "F4"]}
NN = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def mi(n): g = re.match(r"([A-G]#?)(-?\d)", n); return NN.index(g[1]) + (int(g[2]) + 1) * 12
def up1(v): return [None if x is None else (lambda m: f"{NN[m % 12]}{m // 12 - 1}")(mi(x) + 1) for x in v]
for c in list(VO):  # 最後のサビ（+1）は、同じ形を1フレット上で
    VO[tr_chord(c, 1)] = up1(VO[c])
VO["Ebmaj7"] = [None, "A#2", "D#3", "G3", "A#3", "D4"]
HI4 = lambda v: [None, None] + [x for x in v if x is not None][-4:]   # 右の高い押さえ方（上の4本）
def vo(b): return VO[S.chords[b]]
def vo_next(b): return VO[S.chords[min(NB - 1, b + 1)]]

gL, gR = Groove(seed=5), Groove(seed=8, takes=["00_Rock3-148-C_comp", "03_Rock3-148-C_comp", "02_Rock3-117-Bb_comp"])
LL, RR = Lanes(), Lanes()
# 型（16分×16）。曲の場面と句に合わせて決める
P = {
    "intro_hit": "D--D--D-D-d-D-dU",          # 前奏のリフの土台（3・3・2のアクセント＝リードのリフと同じ所）
    "intro_end": "D--D--D-D---P---",          # 4小節目の終わりは先取り
    "verse_a": "D-------x-----u-",            # Aメロ前半: 1回鳴らしてのばす＋3拍目のチャッ（歌の邪魔をしない）
    "verse_b": "D-d-x-u-d-u-x-u-",            # Aメロ後半: 軽いジャカジャカ（ミュート混じり）
    "verse_end": "D-d-x-u-D---.---",          # 句の切れ目で止める
    "pre_hold": "D-------D-------",           # Bメロ前半: 2拍ずつのばす
    "pre_drive": "D-d-D-d-D-d-D-dU",          # Bメロ後半: ダウンを詰める
    "pre_stop": "D---............",           # Bメロの最後: 1打で全員止まる
    "ch_l": "D-d-dUd-D-d-dUdU",               # サビ（左）
    "ch_l_push": "D-d-dUd-D-d-dUP-",          # 4小節目: 次の小節を先取り
    "ch_r": "D-dUDUdUD-dUDUdU",               # サビ（右・高い押さえ方の16分）
    "ring": "D---------------",               # 1回鳴らしてのばす
    "solo_l": "D--D--D-D-d-D-dU",
    "c_ring": "D-------d-------",
}
# 右の単音（分散和音）: 弦の順番。1音ずつ、その弦が次に鳴るまで響かせる
ARP = [2, 4, 3, 5, 4, 3, 5, 4]
def arp_bar(lanes, b, order=ARP, vel=88, step=0.5, rnd=random.Random(3)):
    v6 = HI4(vo(b)); strs = [k for k in range(6) if v6[k] is not None]
    for q, s in enumerate(order):
        st = strs[min(len(strs) - 1, s - 2)]
        t = b * 4 + q * step + rnd.gauss(0, 0.012)
        lanes.ev[st].append([max(0, t), 0.0, v6[st], int(vel * (1.1 if q % 4 == 0 else 0.9 if q % 2 else 1.0) + rnd.gauss(0, 4))])
def line_bar(lanes, b, notes, vel=95, rnd=random.Random(4)):
    """右の単音の旋律（Bメロ）。notes: [(拍, 長さ, 音名)]"""
    for t, d, n in notes:
        lanes.ev[3].append([b * 4 + t + rnd.gauss(0, 0.01), d - 0.02, n, int(vel + rnd.gauss(0, 4))])
RA = Lanes()   # 右の単音（分散和音・旋律）
BLINE = {0: [(0, 1, "B3"), (1, 1, "D4"), (2, 2, "E4")], 1: [(0, 1, "C#4"), (1, 1, "E4"), (2, 2, "F#4")],
         2: [(0, 1, "D4"), (1, 1, "F#4"), (2, 2, "G4")], 3: [(0, 1, "E4"), (1, 1, "A4"), (2, 2, "C#5")],
         4: [(0, 1, "B3"), (1, 1, "D4"), (2, 2, "E4")], 5: [(0, 1, "C#4"), (1, 1, "E4"), (2, 2, "A4")],
         6: [(0, 1, "D4"), (1, 1, "F#4"), (2, 2, "B4")], 7: [(0, 0.5, "E4")]}
for b in range(NB):
    n, i, L, k = S.scene_of(b)
    if n == "前奏":
        if i >= 2:
            LL.add(gL.bar(b, P["intro_end"] if i % 4 == 1 else P["intro_hit"], vo(b), vo_next(b), BPM, 1.05))
            if i >= 6: RR.add(gR.bar(b, P["intro_end"] if i % 4 == 1 else P["intro_hit"], HI4(vo(b)), HI4(vo_next(b)), BPM, 1.0))
    elif n in ("間奏1", "ソロ"):
        LL.add(gL.bar(b, P["intro_end"] if i % 4 == 3 else P["solo_l"], vo(b), vo_next(b), BPM, 1.05))
        if n == "ソロ": RR.add(gR.bar(b, P["ch_r"], HI4(vo(b)), HI4(vo_next(b)), BPM, 0.85))
    elif n in ("Aメロ1", "Aメロ2"):
        pat = P["verse_a"] if (n == "Aメロ1" and i < 8) else (P["verse_end"] if i % 8 == 7 else P["verse_b"])
        LL.add(gL.bar(b, pat, vo(b), vo_next(b), BPM, 0.82))
        if n == "Aメロ2" or i >= 8: arp_bar(RA, b, vel=80 if i < 8 else 86)
    elif n in ("Bメロ1", "Bメロ2"):
        pat = P["pre_stop"] if i == 7 else (P["pre_hold"] if i < 4 else P["pre_drive"])
        LL.add(gL.bar(b, pat, vo(b), vo_next(b), BPM, 0.9 + 0.03 * i))
        if i == 7: LL.stop_at(b * 4 + 1.0)
        line_bar(RA, b, BLINE[i], vel=92)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        sad = n == "サビ1" and i >= 14
        if sad:
            if i == 14: LL.add(gL.bar(b, P["ring"], vo(b), vo(b), BPM, 0.95)); RR.stop_at(b * 4)
            continue
        last = n == "最後のサビ" and i == L - 1
        vv = 1.1 if n == "最後のサビ" else 1.0
        LL.add(gL.bar(b, P["ring"] if last else (P["ch_l_push"] if i % 4 == 3 else P["ch_l"]), vo(b), vo_next(b), BPM, vv))
        if not last: RR.add(gR.bar(b, P["ch_r"], HI4(vo(b)), HI4(vo_next(b)), BPM, vv * 0.92))
        else: RR.stop_at(b * 4)
    elif n == "Cメロ":
        arp_bar(RA, b, vel=84)
        if i >= 4: LL.add(gL.bar(b, P["c_ring"], vo(b), vo_next(b), BPM, 0.8))
    elif n == "落ちサビ":
        arp_bar(RA, b, vel=78 if i < 4 else 84)
        if i >= 4: LL.add(gL.bar(b, P["ring"], vo(b), vo(b), BPM, 0.78))
    elif n == "白い息":
        if i == 0: LL.add(gL.bar(b, P["ring"], vo(b), vo(b), BPM, 0.9)); RR.stop_at(b * 4)
LL.stop_at(TOTAL); RR.stop_at(TOTAL)

src = json.load(open('/tmp/ab/i1_nodr.json'))
gt = [p for p in src['parts'] if p['instrument'] == 'distGuitar'][0]
gtmpl = {k: v for k, v in gt.items() if k not in ('notes', 'role', 'pan', 'volume', 'double')}
gtmpl.update(double=False, powerChord=False, humanTiming=0)
add = []
for side, lanes, pan, vol, over in (("L", LL, -0.8, 0.045, {}), ("R", RR, 0.8, 0.045, {"ampCabIr": "jd-greenback-4x12-01"})):
    for st, n_ in enumerate(lanes.notes(TOTAL)):
        if not n_: continue
        p = copy.deepcopy(gtmpl); p.update(role=f"{side}ギター（和音）・弦{st + 1}", pan=pan, volume=vol, notes=n_, **over); add.append(p)
for st, n_ in enumerate(RA.notes(TOTAL)):
    if not n_: continue
    p = copy.deepcopy(gtmpl); p.update(role=f"Rギター（単音）・弦{st + 1}", pan=0.75, volume=0.075, notes=n_, ampDrive=0.14, release=0.4, sustain=1.6,
                                     ampCabIr="jd-greenback-4x12-01", fx=gtmpl["fx"] + [{"type": "room", "mix": 0.12}])
    add.append(p)

# --- ドラム（人の演奏データ）
G = '/tmp/gmd/groove/'
R14 = G + 'drummer5/session2/14_rock_140_beat_4-4.mid'; R13 = G + 'drummer5/session2/13_rock_140_beat_4-4.mid'
PK = G + 'drummer1/session2/32_punk_140_beat_4-4.mid'; HT = G + 'drummer1/session1/202_rock-halftime_140_beat_4-4.mid'
dn = {k: [] for k in ('kick', 'snare', 'hihat', 'tom', 'crash')}
def dseg(f, b0, n):
    r = parts_from_gmd(f, b0, n)
    for k in dn: dn[k].append(r.get(k) or f'R:{n * 4}')
def dcus(n, **kw):
    for k in dn: dn[k].append(kw.get(k, f'R:{n * 4}'))
dseg(R14, 0, 10)                                   # 前奏
dseg(HT, 1, 8); dseg(R13, 16, 8)                   # Aメロ1（前半は半分の速さのノリ）
dseg(PK, 4, 7); dcus(1, kick='x:1%120 R:3', crash='C2:4%120')          # Bメロ1（最後は1打で止まる）
dseg(R14, 40, 8); dseg(R14, 32, 6); dcus(2, crash='C2:8%115', kick='x:8%110')   # サビ1（「ごめんね」で止まる）
dseg(R14, 20, 4)                                   # 間奏1
dseg(R13, 0, 16)                                   # Aメロ2
dseg(PK, 12, 7); dcus(1, kick='x:1%120 R:3', crash='C2:4%120')         # Bメロ2
dseg(R14, 24, 8); dseg(R14, 40, 8)                 # サビ2
dseg(PK, 53, 8)                                    # ソロ（ライド）
dseg(HT, 9, 8)                                     # Cメロ（半分の速さ）
dcus(4); dseg(HT, 1, 4)                            # 落ちサビ（前半は声と単音のギターだけ）
dseg(R14, 32, 8); dseg(R14, 40, 8); dseg(R14, 24, 7); dcus(1, kick='x:1%125 R:3', crash='C2:4%128', snare='x:1%120 R:3')   # 最後のサビ
dcus(4, crash='C2:16%110')                         # 白い息（シンバルの余韻だけ）
ref = {p['instrument']: p for p in json.load(open('/tmp/ab/gd.json'))['parts'] if p['instrument'] in dn}
for k, lst in dn.items():
    p = copy.deepcopy(ref[k]); p['notes'] = ' '.join(lst); add.append(p)
tot = {k: sum(float(re.match(r'[\d.]+', t.split(':', 1)[1]).group()) for t in ' '.join(v).split()) for k, v in dn.items()}
assert all(abs(x - TOTAL) < 0.05 for x in tot.values()), (tot, TOTAL)

js["parts"] = [p for p in js["parts"] if p["instrument"] not in ("kick", "snare", "hihat", "tom", "crash", "ride")] + add
json.dump(js, open(path, "w"), ensure_ascii=False)
flatten_arc(path, S)   # 曲全体の山（出だしを小さく）だけを打ち消す。足したパートにも効かせるため、足したあとで
print("ギター・ドラムを足した:", len(add), "パート")
