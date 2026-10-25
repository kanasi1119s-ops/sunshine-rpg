# vb25 21「恋するカセットデッキ」Cassette Deck in Love（仮）— K-POP（レトロポップ）。F 短調（サビは平行調の A♭）・132・4/4。最後のサビは半音上（F#m／A）
# 物語: 押し入れの奥のカセットデッキが、持ち主にもう一度聞いてほしくて、ひとりで歌い出す。
# 場面と強さ: テープを入れる（効果音だけ）→ 回り出す（ブラスのフック・中）→ ひとりごと（Aメロ・ラップのような早口・低い）
#   → 気づいてほしい（Bメロ・溜め・止め）→ 再生ボタン（サビ・強。掛け声のような短いフックのくり返し）→ 早送り（間奏）
#   → 2番（前半はブラスが歌を受け取る）→ サビ2（前半はリズムを2ステップに入れかえ）→ テープが止まる（テンポが落ちて、1拍の無音）
#   → 押し入れの暗がり（Half feel・弱）→ ダンスブレイク（掛け声のチョップ）→ 半音上の最後のサビ（最大）→ テープが止まって1音
# 旋律の性格: Aメロは C4〜F5 の低い所で16分の早口（同じ音の連打と裏の食い）、サビは A♭5 の連打を2拍の短い句でくり返す K-POP のフック。最高音 C6（最後は C#6）
# 定番以外の和音: Aメロの G♭（♭II）、サビの A♭7（IV への副属和音）、Cメロの Caug（増三和音）、最後のサビ前の E7（半音上の調の属和音へ飛ぶ）
from vb25_lib import *

S = Song("21", "cassette", "恋するカセットデッキ（仮）", "Cassette Deck in Love", 132, 4, "F", "minor", "K-POP（レトロポップ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key                    # F 短調（oct=4 で 1＝F4）
KA = Key("Ab", "major")      # サビ
KB = Key("A", "major")       # 最後のサビ（半音上）
KF2 = Key("F#", "minor")


def chk(key, lines, beats=4):
    for l in lines: assert abs(total(key.mel(l, oct=4)) - beats) < 1e-6, ("拍の数", l)


A_CH = ["Fm", "Eb", "Db", "Gb", "Fm", "Eb", "Db", "C7"]
B_CH = ["Bbm7", "Eb7", "Abmaj7", "Dbmaj7", "Gm7b5", "C7", "Fm", "C7"]
C_CH = ["Dbmaj7", "C7", "Fm7", "Ab7", "Dbmaj7", "C7", "Fm7", "Eb"]
HOOK_CH = ["Fm", "Db", "Eb", "C7"]
CM_CH = ["Dbmaj7", "Ebsus4", "Cm7", "Fm7", "Bbm7", "Eb", "Caug", "C7"]
LAST_CH = ["Dmaj7", "C#7", "F#m7", "A7", "Dmaj7", "C#7", "F#m7", "E"]

S.scene("テープを入れる", 2, "intro", ["Fm", "Fm"])
S.scene("回り出す", 8, "intro", HOOK_CH)
S.scene("ひとりごと", 16, "verse", A_CH)
S.scene("気づいてほしい", 8, "pre", B_CH)
S.scene("再生ボタン", 16, "chorus", C_CH)
S.scene("早送り", 8, "interlude", HOOK_CH)
S.scene("ひとりごと2", 16, "verse", A_CH)
S.scene("気づいてほしい2", 8, "pre", B_CH)
S.scene("再生ボタン2", 16, "chorus", C_CH)
S.scene("テープが止まる", 4, "break", ["Dbmaj7", "C7", "Fm7", "Fm7"])
S.scene("押し入れの暗がり", 16, "bridge", CM_CH)
S.scene("ダンスブレイク", 8, "interlude", ["Fm", "Fm", "Db", "Eb", "Fm", "Fm", "Db", "C7"])
S.scene("もう一度", 4, "build", ["Gbmaj7", "Ab", "Bbm7", "E7"])
S.scene("最後の再生", 16, "chorus", LAST_CH)
S.scene("テープの終わり", 6, "outro", ["F#m7", "Dmaj7", "F#m7", "Dmaj7", "E", "F#m"])
b_stop = S.sc("テープが止まる")[0]
b_end = S.sc("テープの終わり")[0]
# テープが止まる所だけ、テンポを落とす（回転が落ちる）。暗がりから元のテンポ。終わりも同じ
S.tempo = [{"bar": b_stop + 3, "bpm": 70, "ramp": 2}, {"bar": b_stop + 5, "bpm": 132},
           {"bar": b_end + 5, "bpm": 62, "ramp": 2}]

V = Voice(S, vol=0.22, delay=0.75, patch="popLeadClear")   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
EP = [S.track(f"エレピ{i + 1}", "fmEpiano", volume=0.1, pan=-0.3, reverb=0.2, sustain=0.9) for i in range(3)]
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.14, pan=0.3, reverb=0.22, gainDb=3, phrase=4,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 0.5}]) for i in range(3)]
BRM = S.track("ブラス（歌の受け渡し・フック）", "brass", patch="brassSection", volume=0.2, pan=0.3, reverb=0.22, gainDb=3, phrase=4,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 0.5}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.23, duck=0.25))
PAD = [S.track(f"レトロのパッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.055, pan=0.0, duck=0.3)) for i in range(3)]
PLK = S.track("プラック", "pad", **pluck_spec("pluckSynth", vol=0.08, pan=0.45, delay=0.75, sustain=0.5))
TAPE = S.track("テープの回転音", "pad", patch="fxRiser", volume=0.05, pan=0, reverb=0.2, modulate=False)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
KNOCK = S.track("テープを入れる音（ボディをたたく音）", "guitar", patch="guitarFx", volume=0.12, pan=0.1, amp="clean", chorus=0, reverb=0.15)
RIDE = S.track("ライド", "crash", **{k: v for k, v in NAKED["crash"].items() if k != "human"})
D = S.drumkit()
SIL = Silence(S)

# ================= 旋律 =================
# Aメロ（ラップのような早口。C4〜F5）
RAP = ["R:0.25 1:0.25 1:0.25 1:0.25 1:0.25 7,:0.25 1:0.25 3:0.25 R:0.25 1:0.25 1:0.25 7,:0.25 5,:0.5 R:0.5",
       "R:0.25 7,:0.25 7,:0.25 7,:0.25 7,:0.25 5,:0.25 7,:0.25 2:0.25 R:0.25 7,:0.25 2:0.25 4:0.25 2:0.5 7,:0.5",
       "R:0.25 6,:0.25 1:0.25 1:0.25 6,:0.25 1:0.25 3:0.25 1:0.25 R:0.25 3:0.25 4:0.25 3:0.25 1:0.5 6,:0.5",
       "b2:0.75 1:0.25 b2:0.5 4:0.5 3:1 R:1",
       "R:0.25 3:0.25 3:0.25 3:0.25 3:0.25 1:0.25 3:0.25 5:0.25 R:0.25 3:0.25 3:0.25 1:0.25 7,:0.5 1:0.5",
       "R:0.25 2:0.25 2:0.25 2:0.25 2:0.25 7,:0.25 2:0.25 4:0.25 R:0.25 4:0.25 5:0.25 4:0.25 2:1",
       "R:0.25 1:0.25 3:0.25 6:0.25 R:0.25 6:0.25 5:0.25 3:0.25 1:0.25 3:0.25 1:0.25 6,:0.25 1:1",
       "5,:0.5 #7,:0.5 2:0.5 4:0.5 #7:1 R:1",
       # 後半: 裏で切って詰める（16分の食いが続く）
       "1:0.25 1:0.25 R:0.25 1:0.25 3:0.25 1:0.25 R:0.25 7,:0.25 1:0.25 1:0.25 R:0.25 3:0.25 5:0.5 3:0.5",
       "7,:0.25 7,:0.25 R:0.25 7,:0.25 2:0.25 7,:0.25 R:0.25 5,:0.25 7,:0.25 2:0.25 R:0.25 4:0.25 5:0.5 4:0.5",
       "6,:0.25 6,:0.25 R:0.25 1:0.25 3:0.25 6:0.25 R:0.25 5:0.25 3:0.25 1:0.25 3:0.25 5:0.25 6:1",
       "b2:0.25 b2:0.25 b2:0.25 4:0.25 6:0.5 4:0.5 b2:1 R:1",
       "R:0.25 5:0.25 5:0.25 5:0.25 3:0.25 1:0.25 3:0.25 5:0.25 R:0.25 5:0.25 6:0.25 5:0.25 3:1",
       "R:0.25 4:0.25 4:0.25 4:0.25 2:0.25 7,:0.25 2:0.25 4:0.25 R:0.25 5:0.25 7:0.25 5:0.25 4:1",
       "R:0.25 3:0.25 6:0.25 1':0.25 6:0.25 3:0.25 1:0.25 3:0.25 6:0.25 5:0.25 3:0.25 1:0.25 6,:1",
       "5,:0.5 2:0.5 #7,:0.5 4:0.5 5:2"]
# 2番の後半（歌が戻る所）: 連打をさらに細かく、1拍ずつ上がる
RAP2b = ["R:0.25 3:0.25 3:0.25 R:0.25 3:0.25 3:0.25 R:0.25 5:0.25 3:0.25 1:0.25 R:0.25 7,:0.25 1:1",
         "R:0.25 2:0.25 2:0.25 R:0.25 2:0.25 2:0.25 R:0.25 4:0.25 2:0.25 7,:0.25 R:0.25 5,:0.25 7,:1",
         "R:0.25 1:0.25 3:0.25 R:0.25 3:0.25 6:0.25 R:0.25 6:0.25 1':0.5 6:0.25 5:0.25 3:1",
         "#7,:0.25 2:0.25 4:0.25 #7:0.25 R:0.5 4:0.25 2:0.25 #7,:2"] + RAP[12:]
BM = ["4:1 5:0.5 6:0.5 5:1 4:1", "5:1.5 4:0.5 2:1 7,:1", "3:1 5:0.5 7:0.5 1':1.5 7:0.5", "6:2 5:1 3:1",
      "4:1 6:0.5 1':0.5 2':1 1':1", "#7:1 1':0.5 2':0.5 4':1 #7:1", "3':1.5 2':0.5 1':2", "5:1 #7:1 R:2"]
# サビ（A♭長調）: 2拍の短い句のくり返し（A♭5 の連打）→ 6度の跳躍
CH = ["1':0.5 1':0.5 R:0.5 3:0.5 1':0.5 1':0.5 R:0.5 6:0.5", "7:0.5 7:0.5 R:0.5 #5:0.5 3':1 2':1", "1':0.5 6:0.5 R:0.5 2:0.5 6:1 5:1",
      "1':0.5 1':0.5 1':0.5 R:0.5 1:1 5:1",
      "1':0.5 1':0.5 R:0.5 3:0.5 1':0.5 1':0.5 R:0.5 6:0.5", "7:0.5 7:0.5 R:0.5 #5:0.5 7:0.5 2':0.5 3':1", "3':1 2':0.5 1':0.5 3:1 6:1", "5:1 7:1 2':2",
      "1':0.5 1':0.5 R:0.5 3:0.5 1':0.5 1':0.5 R:0.5 6:0.5", "7:0.5 7:0.5 R:0.5 #5:0.5 3':1 2':1", "1':0.5 6:0.5 R:0.5 2:0.5 6:0.5 1':0.5 3':1",
      "2':0.5 1':0.5 b7:0.5 5:0.5 1':2",
      "1':0.5 1':0.5 R:0.5 6:0.5 1':0.5 1':0.5 R:0.5 6:0.5", "3':0.5 3':0.5 R:0.5 2':0.5 7:1 #5:1", "3:1 1':1 3':1 2':1", "7:2 R:2"]
# Cメロ（押し入れの暗がり・Half feel）: のばす音で、思い出をたどる
CM = ["R:4"] * 4 + ["3:3 4:1", "5:2 4:1 2:1", "3:1.5 5:0.5 7:2", "6:3 R:1",
                    "4:1 6:1 1':1 2':1", "7:2 5:2", "3':2 #5:1 1':1", "7:2 R:2",
                    "1:0.5 1:0.5 R:0.5 6,:0.5 1:2", "7,:0.5 7,:0.5 R:0.5 #5,:0.5 3:2", "R:4", "R:4"]
chk(K, RAP); chk(K, RAP2b); chk(K, BM); chk(KA, CH); chk(KA, CM)

for i, b in enumerate(S.sc("ひとりごと")): V.bar(b, K.mel(RAP[i], oct=4))
for i, b in enumerate(S.sc("ひとりごと2")):
    if i < 8: BRM.bar(b, K.mel(RAP[i], oct=4))           # ブラスが歌を受け取る
    else: V.bar(b, K.mel(RAP2b[i - 8], oct=4))
for name in ("気づいてほしい", "気づいてほしい2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(BM[i], oct=4))
for name in ("再生ボタン", "再生ボタン2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, KA.mel(CH[i], oct=4))
# テープが止まる: フックの途中で回転が落ちて、音が下がっていく（フォール）
TS = ["1':0.5 1':0.5 R:0.5 6:0.5 1':0.5 1':0.5 R:0.5 6:0.5", "7:0.5 7:0.5 R:0.5 #5:0.5 3':1 2':1", "1':1\\ 6:1\\ 5:1\\ 3:1\\", "1:2\\ R:2"]
for i, b in enumerate(S.sc("テープが止まる")): V.bar(b, KA.mel(TS[i], oct=4))
for i, b in enumerate(S.sc("押し入れの暗がり")): V.bar(b, KA.mel(CM[i], oct=4), low=i >= 8)
# ダンスブレイク: 歌の役は掛け声のような短いチョップだけ
DB = ["1':0.25 R:0.75 1':0.25 R:1.25 6:0.25 R:0.25 1':0.5 R:0.5", "R:2 1':0.25 1':0.25 R:0.5 3':0.5 R:0.5",
      "R:4", "5:0.25 R:0.75 5:0.25 R:0.75 7:0.25 R:0.25 2':0.5 R:1"]
for i, b in enumerate(S.sc("ダンスブレイク")): V.bar(b, KA.mel(DB[i % 4], oct=4), low=False)
for i, b in enumerate(S.sc("もう一度")):
    if i == 2: V.bar(b, KA.mel("3:1 4:1 5:1 6:1", oct=4))
    if i == 3: V.bar(b, KA.mel("7:1 1':1 2':1 R:1", oct=4))
# 最後のサビ（A長調）: 半音上。終わりの4小節は C#6 へ
LAST = CH[:12] + ["1':0.5 1':0.5 R:0.5 6:0.5 1':0.5 1':0.5 R:0.5 6:0.5", "3':0.5 3':0.5 R:0.5 2':0.5 3':1 2':1", "1':1 2':1 3':2", "3':3 R:1"]
chk(KB, LAST)
for i, b in enumerate(S.sc("最後の再生")): V.bar(b, KB.mel(LAST[i], oct=4))
OUT = ["1':0.5 1':0.5 R:0.5 6:0.5 1':0.5 1':0.5 R:0.5 6:0.5", "R:4", "1':0.5 1':0.5 R:0.5 6:0.5 1':2", "R:4", "R:4", "R:4"]
for i, b in enumerate(S.sc("テープの終わり")):
    if OUT[i] != "R:4": V.bar(b, KB.mel(OUT[i], oct=4), low=False)

# ================= ブラスのフック（回り出す・早送り） =================
HOOK = ["1:0.5 1:0.25 3:0.25 R:0.25 5:0.5 3:0.25 1:0.5 7,:0.5 1:1", "6,:0.5 6,:0.25 1:0.25 R:0.25 3:0.5 1:0.25 6,:0.5 5,:0.5 6,:1",
        "7,:0.5 7,:0.25 2:0.25 R:0.25 4:0.5 2:0.25 7,:0.5 5,:0.5 7,:1", "#7,:0.5 2:0.5 4:0.5 5:0.5 #7:1 R:1"]
for name in ("回り出す", "早送り"):
    for i, b in enumerate(S.sc(name)): BRM.bar(b, K.mel(HOOK[i % 4], oct=3 if (name == "早送り" and i >= 4) else 4))
for i, b in enumerate(S.sc("ダンスブレイク")):
    BRM.bar(b, K.mel(HOOK[i % 4], oct=4))
    vv = voice(S.chords[b], 62, 3)
    for j in range(3): BR[j].bar(b, f"{nm(vv[j])}:0.25' R:1.25 {nm(vv[j])}:0.25' R:0.25 {nm(vv[j])}:0.5 R:1.5")
# 合いの手: サビの4小節目ごとにブラスの短い「パッ」
for name in ("再生ボタン", "再生ボタン2", "最後の再生"):
    kk = KB if name == "最後の再生" else KA
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3:
            vv = voice(S.chords[b], 70, 3)
            for j in range(3): BR[j].bar(b, f"R:2.5 {nm(vv[j])}:0.25' R:0.25 {nm(vv[j])}:1")

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "テープを入れる": continue
    v3 = voice(ch, 64, 3)
    # エレピ（和音の刻み。Aメロは裏、サビは付点）
    pat = None
    if n in ("回り出す", "早送り"): pat = "X:0.75 X:0.75 X:0.5 R:0.5 X:0.75 X:0.75"
    elif n.startswith("ひとりごと"): pat = "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5" if i < 8 else "X:0.5 R:0.25 X:0.25 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5"
    elif n.startswith("気づいて"): pat = "X:1 X:1 X:1 X:1" if i < L - 1 else "X:2 R:2"
    elif n.startswith("再生ボタン") or n == "最後の再生": pat = "X:0.75 X:0.75 X:0.5 X:0.75 X:0.75 X:0.5"
    elif n == "押し入れの暗がり": pat = "X:4"
    elif n == "もう一度": pat = "X:2 X:2" if i < 3 else "X:1 R:3"
    elif n == "テープが止まる": pat = "X:1 X:1 X:1 X:1" if i < 2 else ("X:4" if i == 2 else "X:2 R:2")
    elif n == "テープの終わり" and i < 5: pat = "X:2 X:2" if i < 4 else "X:4"
    if pat:
        for j in range(3):
            EP[j].bar(b, " ".join(("R:" + x.split(":")[1]) if x.startswith("R") else f"{nm(v3[j])}:{x.split(':')[1]}" for x in pat.split()))
    # シンセベース（根音。サビはオクターブ、ダンスブレイクはディスコの16分）
    if n == "回り出す": BASS.bar(b, bass_line(S, b, "push") if i >= 4 else "R:4")
    elif n.startswith("ひとりごと"): BASS.bar(b, bass_line(S, b, "push" if i < 8 else "root8"))
    elif n.startswith("気づいて"): BASS.bar(b, bass_line(S, b, "root8") if i < L - 1 else f"{nm(low(ch, 'E1'))}:2 R:2")
    elif n.startswith("再生ボタン") or n == "最後の再生": BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "早送り": BASS.bar(b, bass_line(S, b, "house"))
    elif n == "テープが止まる": BASS.bar(b, bass_line(S, b, "oct8") if i < 2 else (f"{nm(low(ch, 'E1'))}:4\\" if i == 2 else "R:4"))
    elif n == "押し入れの暗がり": BASS.bar(b, bass_line(S, b, "half") if i >= 4 else "R:4")
    elif n == "ダンスブレイク": BASS.bar(b, bass_line(S, b, "disco"))
    elif n == "もう一度": BASS.bar(b, bass_line(S, b, "long") if i < 3 else f"{nm(low(ch, 'E1'))}:1 {nm(low(ch, 'E1') + 12)}:1 {nm(low(ch, 'E1'))}:1 {nm(low(ch, 'E1') + 7)}:1")
    elif n == "テープの終わり" and i < 5: BASS.bar(b, bass_line(S, b, "half"))
    # パッド（暗がり・Bメロ・サビ）
    if n in ("押し入れの暗がり", "もう一度") or n.startswith("気づいて") or n.startswith("再生ボタン") or n == "最後の再生" or (n == "テープの終わり" and i < 5):
        vv = voice(ch, 58, 3)
        for j in range(3): PAD[j].bar(b, f"{nm(vv[j])}:4")
    # プラック（Aメロの後半・サビ）
    if (n.startswith("ひとりごと") and i >= 8) or n.startswith("再生ボタン") or n == "最後の再生":
        t = tones(ch, "C4", "C6"); PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))

# テープを入れる音（コツ、コツ）と、回転音（ホワイトノイズのシュッを長く）
KNOCK.bar(0, "G#2:1 R:0.5 G#2:0.5 R:2"); KNOCK.bar(1, "R:2 F#2:1 R:1")
TAPE.bar(1, "A4:4")
for b in S.sc("押し入れの暗がり")[:4]: TAPE.bar(b, "A4:4")
TAPE.bar(S.sc("テープが止まる")[2], "E4:8")                # ダウンリフター（回転が落ちる）
TAPE.bar(S.sc("テープの終わり")[4], "E4:8")
riser(TAPE, S.sc("再生ボタン")[0], 4, "C4"); riser(TAPE, S.sc("最後の再生")[0], 8, "D4")
cym_swell(CYM, S.sc("再生ボタン2")[0], 2, "C4"); cym_swell(CYM, S.sc("ダンスブレイク")[0], 2, "C4")
# テープが止まって1音（エレピの F#4 を長く）
EP[0].bar(S.sc("テープの終わり")[5], "F#4:4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "回り出す":
        vgroove(D, b, "four" if i >= 4 else "none", seed=b)
        if i < 4: D.set(b, "X...X...X...X...", "." * 16, "." * 16)
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n.startswith("ひとりごと"):
        vgroove(D, b, "twostep" if i < 8 else "boombap", ghosts=0.45, seed=b)
        if i == 0: crash(D, b)
        if i % 4 == 3: D.H[b] = D.H[b][:12] + "xxxx"
        if last: put_fill(D, b, "small")
    elif n.startswith("気づいて"):
        vgroove(D, b, "half" if i < 4 else "four", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)
    elif n.startswith("再生ボタン") or n == "最後の再生":
        name = "twostep" if (n == "再生ボタン2" and i < 8) else "four16"
        vgroove(D, b, name, ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last and n == "再生ボタン": put_fill(D, b, "tomdown")
        if last and n == "最後の再生": put_fill(D, b, "tomtrip")
    elif n == "早送り":
        vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "small")
    elif n == "テープが止まる":
        if i < 2: vgroove(D, b, "four16", seed=b)
        elif i == 2: D.set(b, "X.......X.......", "....X.......X...", "." * 16)
        else: D.set(b, "X" + "." * 15, "." * 16, "." * 16)
    elif n == "押し入れの暗がり":
        if i < 4: continue
        vgroove(D, b, "half", ghosts=0.5, seed=b, h="................")
        RIDE.bar(b, "D2:1! D2:1 D2:1 D2:1" if i % 2 == 0 else "D2:1! D2:1 D2:0.5 D2:0.5 D2:1")
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "tomtrip")
    elif n == "ダンスブレイク":
        vgroove(D, b, "four16", ghosts=0.4, seed=b, s="....X..o....X.oX")
        if i == 0: crash(D, b, "G2")
        if i == 3: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomdown")
    elif n == "もう一度":
        if i < 2: D.set(b, "X...X...X...X...", "." * 16, "x.x.x.x.x.x.x.x.")
        elif i == 2: put_fill(D, b, "build"); D.K[b] = "X...X...X...X..."
        else: D.set(b, "." * 16, "." * 16, "." * 16)                 # サビ直前の1小節は「ベースと歌の役だけ」
    elif n == "テープの終わり":
        if i < 4: vgroove(D, b, "half", seed=b)
        if i == 0: crash(D, b)
        if i == 4: D.set(b, "X" + "." * 15, "." * 16, "." * 16); crash(D, b, "C2", 8)

# 止め（Bメロの最後）・1拍の完全な無音（テープが止まり切る所）
for name in ("気づいてほしい", "気づいてほしい2"): SIL.add(S.sc(name)[-1], 2, 4)
SIL.add(S.sc("テープが止まる")[-1], 2, 4)
SIL.add(S.sc("もう一度")[-1], 3, 4)          # 半音上がる直前の1拍のブレイク
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の21。K-POP（レトロポップ）。F 短調・132（サビは A♭、最後のサビは半音上の A）。押し入れのカセットデッキが、"
          "持ち主にもう一度聞いてほしくて歌い出す。テープを入れる音から、ブラスのフック、ラップのような早口の Aメロ、A♭5 の連打をくり返すサビ、"
          "2番はブラスが歌を受け取り、2回目のサビは2ステップ、テープが止まる（テンポが落ちて1拍の無音）、Half feel の暗がり、ダンスブレイク、"
          "E7 から半音上の最後のサビ、テープが止まって1音。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
