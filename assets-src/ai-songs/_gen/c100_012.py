# ケルト・フルート100曲「銀の笛と百の夜」012 羊飼いの朝 Shepherd's Morning — 第2版の作り方の最初の試作（2026-10-28）
# 物語: 朝霧の丘。鳥の声で目を覚まし、羊を集めて歩き出す（ジグ1）。丘の上で一息ついて（ドローンだけのつなぎ）、
#       足どりが軽くなり、調が4度上がって2つ目のジグへ（ジグ2）。最後は最初のジグの節が上の調で戻り、全員で「ジャン・ジャン」と止まる。
# 形: 「ゆっくり→速い」ではなく「ジグ2曲のセット＋キー・リフト」（docs/sound/celtic-study の C・D）。6/8。付点4分＝80（明るく、走らない）。
# 編曲の表（場面ごとに鳴る楽器。全部を鳴らしっぱなしにしない）:
#   鳥        : 小さな鳥の笛と本物の鳥。最後の2小節でボーランが小さく入る
#   ジグ1-1回目: 笛＋ボーラン（小）＋ギター（Aは5度だけの軽い打ち、Bで開放和音のストローク）
#   ジグ1-2回目: ＋竪琴（ローヴィング・サム）＋ピチカート。Bでは鳥の笛が3度下でハモる。笛の装飾が増える
#   つなぎ     : ドローン（弦の主音と5度）だけ＋笛の弱起
#   ジグ2-1回目: 4度上（G→C）。竪琴の3音オスティナート＋ギター＋チェロの低音。Bから持続の弦
#   ジグ2-2回目: 全員。Bは和声の笛。グロッケンが要所を光らせる
#   帰り道     : ジグ1のAが上の調で戻る。最初の4小節はストップタイム（全員は1拍目だけ、あとは笛ひとり）→全員
#   結び       : 「付点4分・付点4分」の一斉の止め×2 → 鳥の笛がひと声
import sys
from c100_common import *
from c100_v2 import *

BPM = 240   # 8分音符＝240（付点4分＝80）
S = Song("C100", "012-shepherds-morning", "羊飼いの朝", "Shepherd's Morning", BPM, 6, "G", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
J1A = ["G", "G", "C", "D", "G", "G", "C", "G"]          # ジグ1 A（8小節）
J1B = ["C", "C", "F", "G", "C", "G", "C", "G"]          # ジグ1 B（F＝♭VII の色）
J2A = ["C", "C", "F", "C", "C", "F", "G", "C"]          # ジグ2 A（C）
J2B = ["F", "G", "Am", "C", "F", "G", "G", "C"]         # ジグ2 B
S.scene("鳥", 4, "intro", ["G", "G", "C", "G"])
S.scene("ジグ1-1", 32, "verse", J1A * 2 + J1B * 2)
S.scene("ジグ1-2", 32, "verse", J1A * 2 + J1B * 2)
S.scene("つなぎ", 2, "break", ["G", "G"])
S.scene("ジグ2-1", 32, "chorus", J2A * 2 + J2B * 2)
S.scene("ジグ2-2", 32, "chorus", J2A * 2 + J2B * 2)
S.scene("帰り道", 16, "chorus", ["C", "C", "F", "G", "C", "C", "F", "C"] * 2)
S.scene("結び", 4, "outro", ["C", "C", "C", "C"])
NAMES = ["鳥", "ジグ1-1", "ジグ1-2", "つなぎ", "ジグ2-1", "ジグ2-2", "帰り道", "結び"]

c = make(S, NAMES,
         [("鳥", 0, 0.6), ("ジグ1-1", 0, 0.66), ("ジグ1-1", 31, 0.7), ("ジグ1-2", 0, 0.74), ("ジグ1-2", 31, 0.78), ("つなぎ", 0, 0.6),
          ("ジグ2-1", 0, 0.78), ("ジグ2-1", 31, 0.84), ("ジグ2-2", 0, 0.86), ("ジグ2-2", 31, 0.9), ("帰り道", 0, 0.8), ("帰り道", 15, 0.92),
          ("結び", 0, 0.9), ("結び", 3, 0.5)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="鳥", passing=True, tension=False)
BIRD = S.track("鳥の笛", "panflute", patch="flute", volume=0.4, bright=-0.7, pan=0.45, reverb=0.7, breath=False, mono=True, barGain=c.g())
DRUM = S.track("ボーラン", "guitar", patch="frameDrum", volume=0.075, pan=-0.15, reverb=0.3, modulate=False, barGain=c.g())
GTR = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.05, pan=0.35 + 0.04 * i, reverb=0.35, barGain=c.g()) for i in range(5)]
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.06, pan=-0.4, reverb=0.35, barGain=c.g())
GLOCK = S.track("グロッケン", "bell", patch="glockenspiel", volume=0.028, pan=0.3, reverb=0.6, barGain=c.g())
DR = [S.track(f"ドローン{i + 1}", "strings", patch="slowStrings", volume=0.09, pan=[-0.3, 0.3][i], reverb=0.6) for i in range(2)]

# ---------- 旋律（度数・8分＝1） ----------
# ジグ1：動機 a＝「下から駆け上がって3度で止まる」(5, 1 2 3)。前半4小節は2度で開いて終わり、後半は主音で閉じる
J1_A = ["5,:1 1:1 2:1 3:2 1:1", "2:1 3:1 4:1 5:3",
        "6:1 5:1 3:1 4:1 3:1 2:1", "1:1 2:1 3:1 2:3",
        "5,:1 1:1 2:1 3:2 1:1", "2:1 3:1 4:1 5:2 6:1",
        "1':2 6:1 5:1 3:1 2:1", "1:3 1:2 5,:1"]
# B（ターン）：上の音域で始め、最高音は5小節目、最後の2小節は A の結び
J1_B = ["5:1 6:1 1':1 2':2 1':1", "6:1 1':1 6:1 5:3",
        "4:1 5:1 6:1 1':2 6:1", "5:1 3:1 2:1 3:3",
        "5:1 6:1 1':1 2':1 3':1 2':1", "1':2 6:1 5:3",
        "1':2 6:1 5:1 3:1 2:1", "1:3 1:2 5,:1"]
# ジグ2（C）：動機 b＝「分散和音で跳ね上がって、同じ音を叩いて下りる」
J2_A = ["1:1 3:1 5:1 1':2 5:1", "6:1 5:1 3:1 5:3",
        "4:1 6:1 1':1 6:1 4:1 6:1", "5:1 3:1 1:1 2:3",
        "1:1 3:1 5:1 1':2 5:1", "6:1 1':1 6:1 5:1 3:1 5:1",
        "4:1 3:1 2:1 5,:1 7,:1 2:1", "1:3 1:2 5,:1"]
J2_B = ["3:1 4:1 5:1 6:2 5:1", "4:1 5:1 6:1 7:3",
        "1':2 7:1 6:1 5:1 4:1", "3:1 5:1 3:1 2:3",
        "3:1 4:1 5:1 6:2 1':1", "7:1 6:1 5:1 6:3",
        "4:1 3:1 2:1 5,:1 7,:1 2:1", "1:3 1:2 5,:1"]
END = ["1:3 1:3", "5,:3 1:3"]

play_melody(c, "ジグ1-1", J1_A + J1_A + J1_B + J1_B, 4, "jig", density=0.6, seed=11)
play_melody(c, "ジグ1-2", J1_A + J1_A + J1_B + J1_B, 4, "jig", density=1.0, seed=12)
play_melody(c, "つなぎ", ["R:6", "R:3 5,:1 6,:1 7,:1"], 4, "jig", density=0)
K2 = S.key.up(5)   # G→C（4度上）
play_melody(c, "ジグ2-1", J2_A + J2_A + J2_B + J2_B, 4, "jig", key=K2, density=0.7, seed=21)
play_melody(c, "ジグ2-2", J2_A + J2_A + J2_B + J2_B, 4, "jig", key=K2, density=1.0, seed=22)
play_melody(c, "帰り道", J1_A + J1_A[:7] + ["1:3 1:3"], 4, "jig", key=K2, density=1.0, seed=31)
play_melody(c, "結び", ["1:3 1:3", "1:6", "R:6", "R:6"], 4, "jig", key=K2, density=0)
# 鳥の笛：始まりの呼び合いと、ジグ1-2のBでの3度下のハモり、結びのひと声
for idx, s in [(0, "R:1 2':0.5 3':1.5 1':2 R:1"), (1, "R:3 7:0.5 1':1 2':1.5"), (2, "R:1 1':0.5 2':1.5 6:2 R:1"), (3, "5:1 6:0.5 1':1.5 R:3")]:
    BIRD.bar(c.s0["鳥"] + idx, S.key.mel(s, oct=4))
harm = [s for s in J1_B + J1_B]
for t, L, m in section_events(c, "ジグ1-2", J1_A * 2 + J1_B * 2, 4):
    bar = int(t // 6) - c.s0["ジグ1-2"]
    if bar >= 16 and L >= 1:
        h = [x for x in range(m - 5, m - 2) if x % 12 in chord_pcs(S.chords[int(t // 6)])]
        if h: BIRD.at(round(t + 0.03, 3), f"{nm(h[-1])}:{L}")
BIRD.bar(c.s0["つなぎ"], S.key.mel("R:1 2':0.5 3':1.5 1':3", oct=4))
BIRD.bar(c.s0["結び"] + 2, K2.mel("R:2 2':0.5 3':1.5 1':2", oct=4))

# ---------- 伴奏（編曲の表どおりに出し入れ） ----------
B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    root = [x for x in range(36, 48) if x % 12 == PC[ch.rstrip("m")[:2] if len(ch) > 1 and ch[1] in "#b" else ch[0]]][0]
    if n == "鳥":
        bodhran(DRUM, b, B, "slow", var=i % 2, soft=True)
        drone(DR, b, B, 55)
        if i >= 1: roving_thumb(c.HARP, b, B, ch, up=(i % 2 == 1))
    elif n == "ジグ1-1":
        bodhran(DRUM, b, B, "jig", var=1 if i % 8 == 7 else 0, soft=True)
        if i < 16: GTR[0].bar(b, f"{nm(root + 12)}:3, {nm(root + 19)}:3,"); GTR[1].bar(b, f"R:3 {nm(root + 24)}:3,")
        else: strum(GTR, b, B, ch, JIG_STRUM)
    elif n == "ジグ1-2":
        bodhran(DRUM, b, B, "jig", var=1 if i % 4 == 3 else 0)
        strum(GTR, b, B, ch, JIG_STRUM)
        roving_thumb(c.HARP, b, B, ch, up=(i % 2 == 0))
        if i % 2 == 0: PIZZ.bar(b, f"{nm(root + 12)}:3 {nm(root + 19)}:3")
    elif n == "つなぎ":
        drone(DR, b, B, 55)
        strum(GTR, b, B, ch, [(0, 6, "d", ",")] if i == 0 else [(0, 3, "d", ","), (3, 3, "d", ",")])
        c.LOW.bar(b, "G2:6")
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (43, 50, 55, 59, 62, 67)) if i == 0 else "G4:6")
        DRUM.bar(b, "D3:3, R:3" if i == 0 else "R:3 D3:3,")
    elif n in ("ジグ2-1", "ジグ2-2"):
        full = n == "ジグ2-2" or i >= 16
        bodhran(DRUM, b, B, "jig", var=1 if i % 4 == 3 else 0)
        strum(GTR, b, B, ch, JIG_STRUM)
        t3 = tones(ch, "G4", "G5")[:3]
        harp_ostinato(c.HARP, b, B, t3)
        c.LOW.bar(b, f"{nm(root + 12)}:3 {nm(root + 19)}:3")
        if full:
            v = voice(ch, 57, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        if n == "ジグ2-2":
            PIZZ.bar(b, f"{nm(root + 12)}:1 R:2 {nm(root + 19)}:1 R:2")
            if i % 4 == 0: GLOCK.bar(b, f"{nm(tones(ch, 'C6', 'C7')[0])}:3 R:3")
    elif n == "帰り道":
        if i < 4:   # ストップタイム：全員は1拍目だけ
            strum(GTR, b, B, ch, [(0, 1, "d", "!")])
            DRUM.bar(b, "D3:1! R:5"); c.LOW.bar(b, f"{nm(root + 12)}:1 R:5")
        else:
            bodhran(DRUM, b, B, "jig", var=1 if i % 4 == 3 else 0)
            strum(GTR, b, B, ch, JIG_STRUM)
            harp_ostinato(c.HARP, b, B, tones(ch, "G4", "G5")[:3])
            c.LOW.bar(b, f"{nm(root + 12)}:3 {nm(root + 19)}:3")
            v = voice(ch, 57, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
            if i % 4 == 0: GLOCK.bar(b, f"{nm(tones(ch, 'C6', 'C7')[0])}:3 R:3")
    elif n == "結び":
        if i == 0:   # 「ジャン・ジャン」と一斉に止める
            strum(GTR, b, B, ch, [(0, 2.5, "d", "!"), (3, 3, "d", "!")])
            DRUM.bar(b, "D3:3! D3:3!"); c.LOW.bar(b, f"{nm(root + 12)}:3 {nm(root + 12)}:3")
            v = voice(ch, 57, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3 {nm(v[j])}:3")
        if i >= 1:   # 止めのあとは、弦と竪琴の響きが残って、ゆっくり消える
            v = voice(ch, 57, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
            drone(DR, b, B, 48)
            if i == 1: c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, 'C4', 'C6')[:6]))
            if i == 2: c.HARP.bar(b, f"{nm(tones(ch, 'C5', 'C6')[0])}:6")

# 笛の和声（ジグ2-2のBだけ）
rich(c, choir_scenes=["ジグ2-2"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.25 --master -15 --widen 1.0",
       "ケルト・フルート100曲の012（第2版の試作）。朝霧の丘で羊を集めて歩き出す。G→C・6/8 のジグ2曲のセット（付点4分＝80）。笛の装飾（カット・タップ・ロール）とジグのはずみ。楽器は場面ごとに出入りし、最後は上の調で最初の節が戻って一斉に止まる。",
       harm_scenes=None, tail_scene="結び", fill=False, pads=False)
