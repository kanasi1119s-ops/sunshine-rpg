# ケルト・フルート100曲「銀の笛と百の夜」006 夜の灯台守 The Keeper of the Night Light — 第3版（2026-10-29 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 祖父がいなくなってから、灯台の灯はエイラが守っている。日が落ちると灯をともし、夜明けまで見回る。
#   灯台守の夜の見回りは、スコットランドの「夕暮れの帰営の行進（リトリート）」のように、堂々と、ゆっくり、くり返す。
#   灯がひと回りするたびに、光は海の左から右へ、ゆっくりなでていく。
# 調べ: あいだ。形: リトリートの行進（3/4。A 8小節・B 8小節。B は A より高い）。♩=72。A ミクソリディア（G♮）。
# 主役は笛（中音域・堂々と。付点のはずみ。装飾は少しだけ）。
# 伴奏: チェロのピチカートの歩み（主役の伴奏）とコントラバスのピチカート、遠いホルン。
#   見回りから、ビオラの和音が左から右へ1音ずつ移っていく（灯の回転）。竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 灯の回転。4つのビオラを左端・左・右・右端に置き、和音の音を1拍ずつ左→右へ渡していく（和音の循環が左右にゆっくり回る）。
# 始まり: チェロのピチカートだけ（灯をともしに階段を下りる足どり）→ 終わり: ホルンの長い音（夜明け）。
# 山: 中盤（2回目の B）。最初が大きくてだんだん小さくなる形にはしない。
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "006-keeper-of-the-night-light", "夜の灯台守", "The Keeper of the Night Light", 72, 3, "A", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
CA = ["A", "A", "G", "D", "A", "E", "G", "A"]
CB = ["A", "Em", "G", "D", "Bm", "D", "E", "A"]
ROT = ["A", "G", "D", "A"]
S.scene("灯をともす", 6, "intro", ["A", "A", "G", "A", "D", "A"])
S.scene("行進A1", 16, "verse", CA + CA)
S.scene("行進B1", 16, "verse", CB + CB)
S.scene("行進A2", 16, "chorus", CA + CA)
S.scene("行進B2", 8, "chorus", CB)
S.scene("見回り", 16, "verse", ROT * 4)
S.scene("夜明けまで", 12, "verse", CA + ["A", "G", "D", "A"])
S.scene("夜明け", 6, "outro", ["A", "G", "A", "A", "A", "A"])
NAMES = ["灯をともす", "行進A1", "行進B1", "行進A2", "行進B2", "見回り", "夜明けまで", "夜明け"]
S.tempo = [{"bar": 1, "bpm": 72}, {"bar": 90, "bpm": 66, "ramp": 4}]

c = make(S, NAMES,
         [("灯をともす", 0, 0.62), ("行進A1", 0, 0.66), ("行進A1", 15, 0.7), ("行進B1", 0, 0.74), ("行進B1", 15, 0.74),
          ("行進A2", 0, 0.8), ("行進A2", 15, 0.84), ("行進B2", 0, 0.88), ("行進B2", 5, 0.92), ("行進B2", 7, 0.84),
          ("見回り", 0, 0.66), ("見回り", 15, 0.68), ("夜明けまで", 0, 0.66), ("夜明けまで", 11, 0.66), ("夜明け", 0, 0.66), ("夜明け", 5, 0.58)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="灯をともす", passing=True, tension=False)
B = S.beats
def g2(k_intro=2.2): return [round(x * (k_intro if c.scene_of_bar[b] == "灯をともす" else 1.0), 3) for b, x in enumerate(c.g())]
VC = S.track("チェロ（ピチカートの歩み）", "strings", patch="pizzicato", volume=0.12, pan=-0.2, reverb=0.4, barGain=g2())
CBS = S.track("コントラバス（ピチカート）", "strings", patch="contrabass", volume=0.08, pan=0.1, reverb=0.4, sustain=0.5, barGain=g2(1.6))
HN = S.track("遠いホルン", "brass", patch="horn", volume=0.055, pan=0.5, reverb=0.8, barGain=c.g())
VA = [S.track(f"ビオラ（灯の回転{j + 1}）", "strings", patch="viola", volume=0.035, pan=p, reverb=0.65, barGain=c.g())
      for j, p in enumerate([-0.85, -0.3, 0.3, 0.85])]

# ---------- 旋律（A ミクソリディア。1=A4） ----------
A = ["5,:1.5 1:0.5 2:1", "3:2 2:0.5 1:0.5", "7,:1.5 2:0.5 4:1", "6:2 5:1",
     "5:1.5 4:0.5 3:1", "2:1.5 3:0.5 5:1", "4:1 2:1 7,:1", "1:3"]
A2 = A[:6] + ["4:1 2:1 7,:1", "1:1.5 5,:0.5 1:1"]
Bm = ["1':1.5 7:0.5 1':1", "2':2 1':1", "7:1.5 6:0.5 5:1", "4:2 5:1",
      "6:1.5 5:0.5 6:1", "1':2 7:0.5 6:0.5", "5:1 4:1 2:1", "1:3"]
Bm2 = Bm[:6] + ["5:1 6:1 7:1", "1':3"]                       # 2回目の B は上で終わる（山）
play_melody(c, "行進A1", A + A2, 4, "march", density=0.25, seed=601)
play_melody(c, "行進B1", Bm + Bm, 4, "march", density=0.3, seed=602)
play_melody(c, "行進A2", A + A2, 4, "march", density=0.45, seed=603)
play_melody(c, "行進B2", Bm2, 4, "march", density=0.5, seed=604)
# 見回り：行進の節を、ゆっくりのばして（2倍の長さ。8小節ぶんで A の前半4小節）。2回目はホルンと交互に
LOOK = ["5,:3", "1:1.5 2:1.5", "3:3", "2:2 1:1", "7,:3", "2:1.5 4:1.5", "6:3", "5:3",
        "R:3", "R:3", "5:1.5 4:1.5", "3:3", "R:3", "R:3", "2:1.5 7,:1.5", "1:3"]
play_melody(c, "見回り", LOOK, 4, "air", density=0.15, seed=605)
play_melody(c, "夜明けまで", A + ["5:1.5 4:0.5 3:1", "2:3", "4:1 2:1 7,:1", "1:3"], 4, "march", density=0.2, seed=606)
play_melody(c, "夜明け", ["5:3", "4:1.5 2:1.5", "1:3", "R:3", "R:3", "R:3"], 4, "air", density=0.0)

# ---------- 伴奏 ----------
def root_of(ch):
    rt = re.match(r"^([A-G][#b]?)", ch).group(1)
    return 40 + (PC[rt] - 4) % 12                      # E2〜D#3
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = root_of(ch); pcs = chord_pcs(ch)
    nxt = root_of(S.chords[b + 1]) if b + 1 < c.NB else r
    fifth = r + 7
    if n == "灯をともす":                       # チェロだけ：根音と5度を2拍ずつ（階段を下りる足どり）。最後の2小節でコントラバスが加わる
        VC.bar(b, f"{nm(r + 12)}:1 {nm(fifth)}:1, {nm(r + 12)}:1,")
        if i >= 4: CBS.at(b * B, f"{nm(r)}:1")
        continue
    if n == "夜明け":
        if i < 3: VC.bar(b, f"{nm(r + 12)}:1 R:2"); CBS.at(b * B, f"{nm(r)}:2")
        if i == 1: HN.at(b * B, "E3:3")
        if i == 2: HN.at(b * B, "A3:12")                   # 終わり：ホルンの長い音（夜明け）
        continue
    if n == "見回り":                          # 歩みはゆっくり（1小節に1つ）。灯の回転は下
        VC.at(b * B, f"{nm(r + 12)}:2"); CBS.at(b * B, f"{nm(r)}:3")
        if i >= 8 and i % 4 in (0, 1): HN.at(b * B, f"{nm(max(55, min(67, r + 24)))}:3")   # 2回目：笛が休む所にホルン
        continue
    # 行進：チェロのピチカートが歩く（根音・5度・次の根音への近づき）。A2・B2 は8分の弾みが入る
    appr = nxt - 1 if nxt > r else nxt + 1
    if n in ("行進A2", "行進B2") and i % 2 == 1:
        VC.bar(b, f"{nm(r + 12)}:1 {nm(fifth)}:0.5, {nm(fifth + 2)}:0.5, {nm(appr + 12)}:1,")
    else:
        VC.bar(b, f"{nm(r + 12)}:1 {nm(fifth)}:1, {nm(appr + 12)}:1,")
    CBS.at(b * B, f"{nm(r)}:1")
    if n in ("行進B1", "行進B2", "行進A2") and i % 4 == 0:                 # 遠いホルンの長い音（B と2回目）
        HN.at(b * B, f"{nm(max(52, min(64, r + 12 + 7)))}:{B * 2}")
    if n == "夜明けまで" and i % 4 == 0:
        HN.at(b * B, f"{nm(max(52, min(64, r + 12)))}:{B * 2}")

# 灯の回転：見回りと行進A2・B2・夜明けまで。和音の音を1拍ずつ左→右へ。1つの音は3拍のびる
rot_scenes = ("見回り", "行進A2", "行進B2", "夜明けまで")
cnt = 0
for b in range(c.NB):
    n = c.scene_of_bar[b]
    if n not in rot_scenes: continue
    ch = S.chords[b]; tn = [x for x in range(57, 76) if x % 12 in chord_pcs(ch)]
    for q in range(3):
        j = cnt % 4
        VA[j].at(b * B + q, f"{nm(tn[(cnt + q) % len(tn)])}:3,")
        cnt += 1

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.28 --master -15 --widen 1.25 --side-hpf 200",
       "ケルト・フルート100曲の006（第3版）。灯台守の夜の見回り。スコットランドの夕暮れの帰営の行進（リトリート）の形、3/4・♩=72、A ミクソリディア。主役は堂々とした笛。伴奏はチェロとコントラバスのピチカートの歩みと遠いホルン。見回りから、4つのビオラが和音の音を左から右へ1拍ずつ渡し、灯がゆっくり回る。山は2回目の B、終わりはホルンの長い音（夜明け）。",
       harm_scenes=None, tail_scene="夜明け", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 7.0, "layers": [{"file": "1046", "db": -44, "hp": 110, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -28, "delay": 0.2, "lp": 2800, "rt": 2.8}}}
json.dump(air, open("/tmp/cel/w/air006.json", "w"), ensure_ascii=False)
