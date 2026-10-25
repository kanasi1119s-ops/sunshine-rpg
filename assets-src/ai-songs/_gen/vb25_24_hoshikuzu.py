# vb25 24「星屑コンビニエンス」Stardust Convenience（仮）— テクノポップ（エレクトロスウィング）。G 短調・152・4/4。転調なし
# 物語: 夜中のコンビニに、流れ星が買い物に来る。棚の前で迷い、レジを鳴らし、自動ドアが閉まって、星屑だけが残る。
# 場面と強さ: 自動ドア（チャイムとドアの音）→ 入店（ブラスのスウィング・中）→ 夜中の棚（Aメロ・3連の早口・シャッフル）→ 何を買う？（Bメロ・溜め・止め）
#   → レジが鳴る（サビ・強・シャッフル）→ 店内放送（ブラスの間奏）→ 星のダンス（2番。ここからストレートに切りかわる。前半はピアノが歌を受け取る）
#   → 何を買う？2（止め）→ レジが鳴る2（ストレートの4つ打ち）→ 1拍の完全な無音（自動ドアが閉まる）→ 閉まったドアの前（Half feel・弱）
#   → 星屑のソロ（ブラス）→ 最後のレジ（最大）→ ありがとうございました（シャッフルに戻って、和音で終わる）
# 旋律の性格: Aメロ1 は3連の細かい音（シャッフルの早口）、Aメロ2 は16分の早口。どちらも F#・C# の半音の飾りを入れる。サビは G5 の3連打の「ピッ・ピッ・ピッ」のフック
# 定番以外の和音: E♭7→D7（属7の半音の連鎖）、サビの A♭7（♭II の属7＝D7 の裏）、F7→B♭maj7（副属和音）
from vb25_lib import *

S = Song("24", "hoshikuzu", "星屑コンビニエンス（仮）", "Stardust Convenience", 152, 4, "G", "minor", "テクノポップ（エレクトロスウィング）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key   # G 短調（oct=4 で 1＝G4）


def chk(lines, beats=4):
    for l in lines: assert abs(total(K.mel(l, oct=4)) - beats) < 2e-3, ("拍の数", l, total(K.mel(l, oct=4)))


_DUR = re.compile(r"^([0-9.]+)(.*)$")


def warp(t):
    """シャッフルの時間の曲げ方: 拍の前半（0〜0.5）を 0〜2/3 に、後半（0.5〜1）を 2/3〜1 に"""
    b = math.floor(t + 1e-9); f = t - b
    return b + (f * 4 / 3 if f <= 0.5 + 1e-9 else 2 / 3 + (f - 0.5) * 2 / 3)


def swing(s):
    """ストレートで書いた並び（1小節）を、3連の跳ねる長さに直す（8分の裏を3連の3つ目へ）"""
    out, t = [], 0.0
    for x in s.split():
        n, v = x.split(":", 1)
        m = _DUR.match(v); L = float(m.group(1)); mk = m.group(2)
        a, z = warp(t), warp(t + L)
        out.append(f"{n}:{z - a:.4f}{mk}"); t += L
    return " ".join(out)


A_CH = ["Gm", "Gm/F", "Eb7", "D7", "Gm", "Cm7", "Am7b5", "D7"]
B_CH = ["Cm7", "F7", "Bbmaj7", "Ebmaj7", "Am7b5", "D7", "Gm", "D7"]
C_CH = ["Eb", "F", "Dm7", "Gm", "Cm7", "F7", "Bbmaj7", "D7", "Eb", "F", "Dm7", "Gm", "Cm7", "Ab7", "D7sus4", "D7"]
CM_CH = ["Cm7", "Cm7/Bb", "Am7b5", "D7", "Gm", "Gm/F", "Eb7", "D7"]
LAST_CH = C_CH + ["Eb", "F", "Dm7", "Gm", "Cm7", "Ab7", "D7", "Gm6"]

S.scene("自動ドア", 2, "intro", ["Gm", "Gm"])
S.scene("入店", 8, "intro", A_CH)
S.scene("夜中の棚", 16, "verse", A_CH)
S.scene("何を買う？", 8, "pre", B_CH)
S.scene("レジが鳴る", 16, "chorus", C_CH)
S.scene("店内放送", 8, "interlude", A_CH)
S.scene("星のダンス", 16, "verse", A_CH)
S.scene("何を買う？2", 8, "pre", B_CH)
S.scene("レジが鳴る2", 16, "chorus", C_CH)
S.scene("閉まったドアの前", 16, "bridge", CM_CH)
S.scene("星屑のソロ", 16, "solo", A_CH)
S.scene("最後のレジ", 24, "chorus", LAST_CH)
S.scene("ありがとうございました", 8, "outro", ["Cm7", "D7", "Gm", "Eb7", "Cm7", "D7", "Gm6", "Gm6"])
SHUF = set(S.sc("入店") + S.sc("夜中の棚") + S.sc("何を買う？") + S.sc("レジが鳴る") + S.sc("店内放送") + S.sc("閉まったドアの前") + S.sc("ありがとうございました"))

V = Voice(S, vol=0.22, delay=0.75, patch="picoLeadRound")   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.13, pan=0.25, reverb=0.22, gainDb=3, phrase=4,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 0.5}]) for i in range(3)]
BRM = S.track("ブラス（リフ・ソロ）", "brass", patch="brassSection", volume=0.2, pan=0.25, reverb=0.22, gainDb=3, phrase=4,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 0.5}])
PIANO_FX = [{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}]
PN = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.1, pan=-0.25, reverb=0.22, fx=PIANO_FX) for i in range(3)]
PNL = S.track("ピアノ（左手）", "piano", volume=0.12, pan=-0.25, reverb=0.22, fx=PIANO_FX)
PNM = S.track("ピアノ（歌の受け渡し）", "piano", volume=0.18, pan=-0.25, reverb=0.22, fx=PIANO_FX)
BASS = S.track("ウッドベース風", "bass", patch="acousticBass", volume=0.24, pan=0, duck=0.15,
               fx=[{"type": "filter", "kind": "highpass", "freq": 40, "q": 0.7}, {"type": "eq", "low": -2, "mid": 3, "midHz": 900, "high": 0},
                   {"type": "eq", "low": 0, "mid": 2.5, "midHz": 2200, "high": 1}])
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.05, pan=0.0, duck=0.25)) for i in range(3)]
PLK = S.track("プラック（星屑）", "pad", **pluck_spec("pluckSynth", vol=0.075, pan=0.45, delay=0.75, sustain=0.5))
BELL = S.track("レジとチャイムの電子音", "fmBell", volume=0.1, pan=-0.3, reverb=0.3, sustain=0.9, gainDb=1)
FX = S.track("効果音（自動ドア・ライザー）", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
_dspec = lambda k: {kk: vv for kk, vv in NAKED[k].items() if kk != "human"}
HATS = S.track("ハイハット（シャッフル）", "hihat", **_dspec("hihat"))
SNG = S.track("スネア（シャッフルのゴースト）", "snare", **_dspec("snare"))
RIDE = S.track("ライド", "crash", **_dspec("crash"))
D = S.drumkit()
SIL = Silence(S)


def put(tr_, b, s):
    """シャッフルの小節なら跳ねる長さに直して置く"""
    tr_.bar(b, swing(s) if b in SHUF else s)


# ================= 旋律 =================
T3 = "0.3333"
# Aメロ1（シャッフル）: 3連の細かい音の早口。F#4・C#5 の半音の飾り
A1 = ["R:0.6667 5,:0.3333 1:0.3333 1:0.3333 1:0.3334 #7,:0.3333 1:0.3333 3:0.3334 1:0.6667 R:0.3333",
      "R:0.6667 1:0.3333 3:0.3333 3:0.3333 3:0.3334 4:0.3333 3:0.3333 2:0.3334 1:0.6667 5,:0.3333",
      "R:0.6667 3:0.3333 6:0.3333 6:0.3333 6:0.3334 5:0.3333 b5:0.3333 4:0.3334 3:0.6667 1:0.3333",
      "#7,:0.6667 2:0.3333 4:0.6667 5:0.3333 #7,:1 R:1",
      "R:0.6667 5:0.3333 5:0.3333 5:0.3333 5:0.3334 4:0.3333 #4:0.3333 5:0.3334 3:0.6667 1:0.3333",
      "R:0.6667 6:0.3333 6:0.3333 6:0.3333 5:0.3334 4:0.3333 3:0.3333 4:0.3334 6:1",
      "R:0.6667 4:0.3333 2:0.3333 4:0.3333 6:0.3334 1':0.6667 6:0.3333 4:0.6667 2:0.3333",
      "#7:0.6667 5:0.3333 4:0.6667 2:0.3333 #7,:2",
      "1:0.3333 3:0.3333 5:0.3334 1':0.3333 5:0.3333 3:0.3334 R:0.6667 1:0.3333 3:0.6667 1:0.3333",
      "7,:0.3333 2:0.3333 4:0.3334 7:0.3333 4:0.3333 2:0.3334 R:0.6667 7,:0.3333 2:0.6667 7,:0.3333",
      "6,:0.3333 1:0.3333 3:0.3334 b5:0.3333 3:0.3333 1:0.3334 R:0.6667 6,:0.3333 1:0.6667 6,:0.3333",
      "5,:0.3333 #7,:0.3333 2:0.3334 4:0.3333 2:0.3333 #7,:0.3334 5,:2",
      "R:0.6667 5:0.3333 #4:0.3333 5:0.3333 6:0.3334 5:0.3333 #4:0.3333 5:0.3334 3:1",
      "R:0.6667 6:0.3333 5:0.3333 6:0.3333 1':0.3334 6:0.3333 5:0.3333 4:0.3334 3:1",
      "R:0.6667 4:0.3333 4:0.3333 6:0.3333 1':0.3334 2':0.6667 1':0.3333 6:0.6667 4:0.3333",
      "#7:1 2':0.6667 1':0.3333 #7:2"]
# Aメロ2（ストレート）: 16分の早口
A2 = ["R:0.25 5,:0.25 1:0.25 1:0.25 1:0.25 #7,:0.25 1:0.25 3:0.25 R:0.25 1:0.25 3:0.25 5:0.25 4:0.5 3:0.5",
      "R:0.25 2:0.25 2:0.25 2:0.25 4:0.25 2:0.25 7,:0.25 2:0.25 R:0.25 4:0.25 7:0.25 4:0.25 2:1",
      "R:0.25 3:0.25 3:0.25 3:0.25 b5:0.25 3:0.25 1:0.25 3:0.25 R:0.25 6:0.25 5:0.25 b5:0.25 4:1",
      "#7,:0.25 2:0.25 4:0.25 #7:0.25 R:0.5 4:0.25 2:0.25 #7,:2",
      "R:0.25 1':0.25 1':0.25 1':0.25 7:0.25 5:0.25 #4:0.25 5:0.25 R:0.25 3:0.25 4:0.25 5:0.25 3:1",
      "R:0.25 6:0.25 6:0.25 6:0.25 5:0.25 4:0.25 3:0.25 4:0.25 6:0.5 1':0.5 6:1",
      "R:0.25 4:0.25 2:0.25 4:0.25 6:0.25 4:0.25 6:0.25 1':0.25 2':0.5 1':0.5 6:1",
      "#7:0.75 6:0.25 5:0.5 4:0.5 #7,:1 R:1",
      "1:0.25 1:0.25 R:0.25 3:0.25 5:0.25 R:0.25 1':0.25 5:0.25 3:0.25 1:0.25 R:0.25 #7,:0.25 1:1",
      "7,:0.25 7,:0.25 R:0.25 2:0.25 4:0.25 R:0.25 7:0.25 4:0.25 2:0.25 7,:0.25 R:0.25 2:0.25 4:1",
      "6,:0.25 6,:0.25 R:0.25 1:0.25 3:0.25 R:0.25 b5:0.25 3:0.25 1:0.25 6,:0.25 R:0.25 1:0.25 3:1",
      "#7,:0.25 2:0.25 4:0.25 5:0.25 #7:0.5 5:0.5 4:2",
      "R:0.25 5:0.25 #4:0.25 5:0.25 6:0.25 5:0.25 #4:0.25 5:0.25 R:0.25 3:0.25 4:0.25 5:0.25 3:1",
      "R:0.25 6:0.25 5:0.25 6:0.25 1':0.25 6:0.25 5:0.25 4:0.25 R:0.25 3:0.25 4:0.25 6:0.25 5:1",
      "R:0.25 4:0.25 6:0.25 1':0.25 2':0.25 1':0.25 6:0.25 4:0.25 6:0.25 1':0.25 2':0.25 1':0.25 6:1",
      "#7:1 2':0.5 1':0.5 #7:2"]
BM = ["4:0.5 6:0.5 1':1 6:0.5 4:0.5 3:1", "3:0.5 4:0.5 7:1 6:0.5 4:0.5 2:1", "3:1 5:0.5 7:0.5 2':1 7:1", "1':1.5 6:0.5 5:2",
      "4:0.5 6:0.5 1':1 2':0.5 1':0.5 6:1", "#7:1 2':0.5 4':0.5 2':1 #7:1", "1':1.5 5:0.5 3:1 1:1", "#7,:1 2:1 R:2"]
CH = ["3:0.5 1':0.5 1':0.5 1':0.5 3':1 1':1", "2':1.5 1':0.5 7:1 2:1", "R:0.5 7:0.5 7:0.5 7:0.5 2':1 7:1", "1':2 3:1 5:1",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':1 4:1", "6:0.5 7:0.5 2':0.5 4':0.5 2':1 7:1", "2':1 1':0.5 7:0.5 5:2", "#7:1 2:1 4:2",
      "3:0.5 1':0.5 1':0.5 1':0.5 3':1 1':1", "2':1.5 1':0.5 7:1 2:1", "R:0.5 7:0.5 7:0.5 7:0.5 2':1 7:1", "5:0.5 1':0.5 3':1 1':2",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':1 4:1", "b2':1.5 6:0.5 4:1 6:1", "5:1 1':1 2':1 1':1", "#7:2 R:2"]
LAST_X = ["3':0.5 3':0.5 3':0.5 R:0.5 4':1 3':1", "2':1.5 1':0.5 7:1 2:1", "R:0.5 7:0.5 7:0.5 7:0.5 2':1 4':1", "3':2 1':2",
          "R:0.5 6:0.5 6:0.5 6:0.5 1':1 3':1", "b2':1 6:1 4:1 6:1", "#7:1 2':1 4':1 2':1", "1':4"]
CM = ["R:4"] * 4 + ["5:2 3:1 1:1", "7,:2 2:2", "3:1.5 b5:0.5 6:2", "4:1 2:1 #7,:2",
                    "6:2 1':1 6:1", "5:3 R:1", "4:1 6:1 1':1 2':1", "#7:3 R:1",
                    "1':2 3':2", "2':3 R:1", "1':1 6:1 b5:1 3:1", "#7,:1 2:1 4:1 R:1"]
chk(A1); chk(A2); chk(BM); chk(CH); chk(LAST_X); chk(CM)

for i, b in enumerate(S.sc("夜中の棚")): V.bar(b, K.mel(A1[i], oct=4))
for i, b in enumerate(S.sc("星のダンス")):
    if i < 8: PNM.bar(b, K.mel(A2[i], oct=5) if i % 4 != 3 else K.mel(A2[i], oct=4))     # ピアノが歌を受け取る
    else: V.bar(b, K.mel(A2[i], oct=4))
for name in ("何を買う？", "何を買う？2"):
    for i, b in enumerate(S.sc(name)):
        s_ = K.mel(BM[i], oct=4); V.bar(b, swing(s_) if b in SHUF else s_)
for name in ("レジが鳴る", "レジが鳴る2"):
    for i, b in enumerate(S.sc(name)):
        s_ = K.mel(CH[i], oct=4); V.bar(b, swing(s_) if b in SHUF else s_)
for i, b in enumerate(S.sc("閉まったドアの前")):
    s_ = K.mel(CM[i], oct=4); V.bar(b, swing(s_), low=i >= 8)
for i, b in enumerate(S.sc("最後のレジ")): V.bar(b, K.mel((CH + LAST_X)[i], oct=4))

# ================= ブラス（リフ・ソロ・合いの手） =================
RIFF = ["1:0.5 3:0.5 5:0.5 #4:0.25 5:0.25 1':1 R:1", "7,:0.5 2:0.5 4:0.5 7:0.5 6:1 R:1",
        "6,:0.5 1:0.5 3:0.5 b5:0.5 4:0.5 3:0.5 1:1", "#7,:0.5 2:0.5 4:0.5 2:0.5 #7,:2"]
SOLO = ["1':0.5 5:0.5 3:0.5 5:0.5 1':1 2':0.5 3':0.5", "2':1 7:0.5 4:0.5 2:1 4:1", "6:0.5 b5:0.5 3:0.5 1:0.5 3:0.5 6:0.5 1':1", "#7:1.5 6:0.25 5:0.25 4:1 R:1",
        "5:0.25 #4:0.25 5:0.25 6:0.25 5:0.5 3:0.5 1:1 3:1", "6:0.25 5:0.25 6:0.25 1':0.25 6:0.5 4:0.5 3:1 4:1",
        "1':0.5 6:0.5 4:0.5 2:0.5 4:0.5 6:0.5 1':0.5 2':0.5", "#7:2 R:2",
        "1':0.25 2':0.25 3':0.25 2':0.25 1':0.5 5:0.5 3:1 5:1", "7:0.25 1':0.25 2':0.25 1':0.25 7:0.5 4:0.5 2:1 4:1",
        "6:0.25 7:0.25 1':0.25 7:0.25 6:0.5 b5:0.5 3:1 1:1", "#7,:0.5 2:0.5 4:0.5 #7:0.5 2':1 R:1",
        "5:0.25 #4:0.25 5:0.25 6:0.25 5:0.5 3:0.5 1:1 3:1", "6:0.25 5:0.25 6:0.25 1':0.25 6:0.5 4:0.5 3:1 4:1",
        "4:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "#7:3 R:1"]
chk(RIFF); chk(SOLO)
for name in ("入店", "店内放送"):
    for i, b in enumerate(S.sc(name)): put(BRM, b, K.mel(RIFF[i % 4], oct=4 if (name == "入店" or i < 4) else 3))
for i, b in enumerate(S.sc("星屑のソロ")): BRM.bar(b, K.mel(SOLO[i], oct=4))
for name in ("レジが鳴る", "レジが鳴る2", "最後のレジ"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3:
            vv = voice(S.chords[b], 64, 3)
            for j in range(3): put(BR[j], b, f"R:2 {nm(vv[j])}:0.5' R:0.5 {nm(vv[j])}:1")

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "自動ドア" or (n == "ありがとうございました" and i >= 6): continue
    r = low(ch, "E1")
    vv = voice(ch, 64, 3)
    # ピアノ: シャッフルは左手が1・3拍、右手が2・4拍（ブンチャッ）。ストレートは和音の刻みと16分の分散和音
    if b in SHUF and n not in ("閉まったドアの前",):
        PNL.bar(b, f"{nm(r + 12)}:1 R:1 {nm(r + 19)}:1 R:1")
        for j in range(3): PN[j].bar(b, f"R:1 {nm(vv[j])}:0.6667' R:0.3333 R:1 {nm(vv[j])}:0.6667' R:0.3333")
    elif n == "閉まったドアの前":
        PNL.bar(b, f"{nm(r + 12)}:4")
        for j in range(3): PN[j].bar(b, f"R:{0.6667 * j} {nm(vv[j])}:{4 - 0.6667 * j:.4f}")
    elif n in ("星のダンス", "星屑のソロ") or n.startswith("何を買う") or n.startswith("レジ") or n == "最後のレジ":
        PNL.bar(b, piano_left8(ch, "C2"))
        if n.startswith("レジ") or n == "最後のレジ":
            for j in range(3): PN[j].bar(b, f"{nm(vv[j])}:0.75 {nm(vv[j])}:0.75 {nm(vv[j])}:0.5 R:0.5 {nm(vv[j])}:0.5 {nm(vv[j])}:1")
        else:
            for j in range(3): PN[j].bar(b, f"R:0.5 {nm(vv[j])}:0.5 R:0.5 {nm(vv[j])}:0.5 R:0.5 {nm(vv[j])}:0.5 R:0.5 {nm(vv[j])}:0.5")
    # ウッドベース風（シャッフルは4分のウォーキング、ストレートは8分のオクターブ）
    if b in SHUF:
        if n == "入店" and i < 4: BASS.bar(b, f"{nm(r)}:1 R:3" if i == 0 else bass_line(S, b, "walk"))
        elif n == "閉まったドアの前": BASS.bar(b, bass_line(S, b, "half") if i >= 4 else f"{nm(r)}:4")
        elif n == "ありがとうございました": BASS.bar(b, bass_line(S, b, "walk") if i < 6 else (f"{nm(r)}:8" if i == 6 else ""))
        elif n.startswith("何を買う") and i == L - 1: BASS.bar(b, f"{nm(r)}:2 R:2")
        else: BASS.bar(b, bass_line(S, b, "walk"))
    else:
        if n.startswith("何を買う") and i == L - 1: BASS.bar(b, f"{nm(r)}:2 R:2")
        else: BASS.bar(b, bass_line(S, b, "oct8" if (n.startswith("レジ") or n == "最後のレジ" or n == "星屑のソロ") else "root8"))
    # パッド
    if n in ("閉まったドアの前",) or n.startswith("何を買う") or n.startswith("レジ") or n == "最後のレジ":
        pv = voice(ch, 58, 3)
        for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4")
    # プラック（星屑。ストレートの所は16分、シャッフルは3連）
    t = tones(ch, "D4", "C6")
    if n in ("星のダンス",) and i >= 8 or n == "レジが鳴る2" or n == "最後のレジ":
        PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 6, 4, 3, 1)))
    elif n == "夜中の棚" and i >= 8 or n == "レジが鳴る":
        PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:{T3}" for q in (0, 2, 4, 1, 3, 5, 2, 4, 6, 3, 1, 4)))

# 自動ドア（チャイムのピン・ポーン、ドアのシュッ）と、レジの電子音（ピッ）
BELL.bar(0, "B5:1 G5:3"); FX.bar(1, "A4:2 R:2")
for name in ("レジが鳴る", "レジが鳴る2", "最後のレジ"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 1: put(BELL, b, "R:3 G6:0.25 R:0.25 G6:0.25 R:0.25")
FX.bar(S.sc("閉まったドアの前")[0], "A4:2 R:2")
BELL.bar(S.sc("閉まったドアの前")[0], "R:2 B5:0.5 G5:1.5")
riser(FX, S.sc("レジが鳴る")[0], 4, "C4"); riser(FX, S.sc("最後のレジ")[0], 8, "D4")
cym_swell(CYM, S.sc("星のダンス")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のレジ")[0], 2, "C4")
# ありがとうございました: 最後はブラスと歌の役とピアノで Gm6 の和音をのばす
bx = S.sc("ありがとうございました")[6]
gv = voice("Gm6", 64, 3)
for j in range(3): BR[j].bar(bx, f"{nm(gv[j])}:8")
V.bar(bx, K.mel("5:8", oct=4))
for j in range(3): PN[j].bar(bx, f"R:{0.25 * j} {nm(voice('Gm6', 70, 3)[j])}:{8 - 0.25 * j}")
PNL.bar(bx, "G2:8"); BASS.bar(bx, "G1:8")
for i, b in enumerate(S.sc("ありがとうございました")):
    if i < 6: V.bar(b, swing(K.mel(["5:1 4:0.5 3:0.5 4:2", "#7,:1 2:1 4:2", "3:1 2:0.5 1:0.5 5,:2", "6,:1 1:1 b5:2", "6:1 5:0.5 4:0.5 6:2", "#7:2 2':2"][i], oct=4)), low=False)

# ================= ドラム =================
def hats_cut(b, a, z):
    """シャッフルのハイハットとゴーストを、クラッシュやフィルの所だけ抜く（両手がふさがるので）"""
    for t in (HATS, SNG):
        t.ev = [e for e in t.ev if not (b * 4 + a - 1e-6 <= e[0] < b * 4 + z - 1e-6)]


SWING_HAT = swing("x:0.5 x:0.5 X:0.5 x:0.5 x:0.5 x:0.5 X:0.5 x:0.5")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "自動ドア": continue
    if b in SHUF:
        # シャッフル: キックは4つ打ち、スネアは2・4拍、ハイハットとゴーストは3連の跳ね（別のパート）
        if n == "閉まったドアの前":
            if i < 4: continue
            D.set(b, "X.........X.....", "........X.......", "." * 16)
            RIDE.bar(b, swing("D2:1! D2:0.5 D2:0.5 D2:1 D2:0.5 D2:0.5"))
            SNG.bar(b, swing("R:1.5 o:0.5 R:2"))
            if i == 4: crash(D, b); RIDE.ev = [e for e in RIDE.ev if not (abs(e[0] - b * 4) < 1e-6)]
            if last: put_fill(D, b, "tomtrip"); RIDE.ev = [e for e in RIDE.ev if not (b * 4 + 2 - 1e-6 <= e[0] < b * 4 + 4)]; SNG.ev = [e for e in SNG.ev if not (b * 4 <= e[0] < b * 4 + 4)]
            continue
        if n == "入店" and i < 4:
            D.set(b, "X...X...X...X...", "." * 16, "." * 16); HATS.bar(b, SWING_HAT if i >= 2 else "R:4")
            continue
        D.set(b, "X...X...X...X...", "....X.......X...", "." * 16)
        HATS.bar(b, SWING_HAT)
        SNG.bar(b, swing("R:1.5 o:0.5 R:1.5 o:0.5") if i % 2 else swing("R:0.5 o:0.5 R:2.5 o:0.5"))
        if i == 0 or (n.startswith("レジ") and i % 8 == 0) or (n == "入店" and i == 4):
            crash(D, b, "C2" if i % 16 == 0 else "G2"); hats_cut(b, 0, 0.5)
        if i % 8 == 7 and not last: put_fill(D, b, "small"); hats_cut(b, 3, 4)
        if last and n not in ("ありがとうございました",):
            if n.startswith("何を買う"): halt(D, b, 2); hats_cut(b, 2, 4)
            else: put_fill(D, b, "tomtrip"); hats_cut(b, 2, 4)
        if n == "ありがとうございました":
            if i == 6: D.set(b, "X" + "." * 15, "." * 16, "." * 16); crash(D, b, "C2", 8); HATS.ev = [e for e in HATS.ev if not (b * 4 <= e[0] < b * 4 + 8)]
            if i == 7: D.set(b, "." * 16, "." * 16, "." * 16); HATS.ev = [e for e in HATS.ev if not (b * 4 <= e[0] < b * 4 + 4)]
        continue
    # ストレート
    if n == "星のダンス":
        vgroove(D, b, "four16" if i < 8 else "vrock2", ghosts=0.4, seed=b)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomdown")
    elif n.startswith("何を買う"):
        vgroove(D, b, "half" if i < 4 else "four", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)
    elif n.startswith("レジ") or n == "最後のレジ":
        vgroove(D, b, "four16", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last: put_fill(D, b, "tomdown")
    elif n == "星屑のソロ":
        vgroove(D, b, "disco", ghosts=0.4, seed=b)
        if i >= 8: D.H[b] = "." * 16; RIDE.bar(b, " ".join(("D2:0.5!" if q % 2 == 0 else "D2:0.5") for q in range(8)))
        if i % 8 == 0: crash(D, b, "B2" if i else "C2")
        if i % 4 == 3 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "build")

# 止め（Bメロの最後 ×2）・1拍の完全な無音（自動ドアが閉まる直前）
for name in ("何を買う？", "何を買う？2"): SIL.add(S.sc(name)[-1], 2, 4)
SIL.add(S.sc("レジが鳴る2")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の24。テクノポップ（エレクトロスウィング）。G 短調・152・転調なし。夜中のコンビニに、流れ星が買い物に来る。"
          "自動ドアのチャイムから、ブラスのスウィング、3連の早口の Aメロ（シャッフル）、G5 の3連打のサビ。2番から16分のストレートに切りかわり、"
          "1拍の無音で自動ドアが閉まって Half feel、ブラスのソロ、最後のサビ、シャッフルに戻って Gm6 の和音で終わる。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
