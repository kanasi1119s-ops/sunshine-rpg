# ラウド26曲 12「Ceasefire at 5AM」（仮。もとの仮題「塹壕の朝」）。2026-10-24 素材から作り直し
# スタイル: メロディックデスメタル（2本のギターが3度で重なる速い旋律のリフ）＋金管。D フリジアン・124 → 76・4/4
# 物語: 夜明け前の塹壕。ラッパが鳴り、総攻撃。砲撃。停戦の合図。そして、誰も撃たない朝。
# 形: 前の半分が戦い（最大）、後ろの3分の1以上は静かな朝。盛り上がりが曲の前半にあり、後半はずっと静か。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   夜（0）: 遠い砲声（低いタム）と、金管のかすかな和音
#   ラッパ（1）: トランペットの合図（4度・5度）
#   総攻撃（3）: 速い。旋律は歌わず、2本のギターが3度で重なる速いリフが旋律の役
#   砲撃（3）: 重いハーフタイム。金管の短い強打
#   停戦の合図（1）: 全員が止まり、トランペットだけ
#   朝（0→1）: 76 に落ちる。クリーンのギターが静かに歌い、ベースと、ブラシのようなドラム
#   朝の光（0）: 金管の静かな聖歌とクリーンだけ。フェードアウト
# 旋律の性格: 合図は4度・5度の付点の跳ね。戦いは旋律なし（速いリフが旋律）。朝は順に進むやさしい歌（クリーン）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 124, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("night", 6), ("bugle", 4), ("assault", 32), ("barrage", 16), ("signal", 4), ("morning", 32), ("light", 6)]
ASS = ["Dm", "Eb", "Dm", "C", "Dm", "Eb", "Bb", "C"]
CH = {"night": ["Dm"] * 6, "bugle": ["D5"] * 4, "assault": ASS * 4, "barrage": ["Dm", "Dm", "Eb", "Eb", "Gm", "Gm", "A", "A"] * 2,
      "signal": ["D5"] * 4, "morning": ["Dm", "Bb", "F", "C", "Dm", "Bb", "Gm", "A"] * 4, "light": ["Bb", "F", "Gm", "Dm", "Bb", "D"]}
song = Song("塹壕の朝（仮）",
            "仮: ラウド26曲の12曲目（2026-10-24 素材から作り直し）。メロディックデスメタル＋金管。D フリジアン。夜、ラッパ、総攻撃、砲撃（124）、停戦の合図、"
            "誰も撃たない朝（76・クリーンの歌）。盛り上がりは前半だけで、後ろの3分の1以上は静か。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 夜明け前の塹壕。ラッパ、総攻撃、砲撃、停戦の合図、そして誰も撃たない朝。"
song.kinds = {"night": "intro", "bugle": "interlude", "assault": "chorus", "barrage": "break", "signal": "interlude", "morning": "verse", "light": "outro"}
SECS, NB = song.secs, song.nb

LOW = {"Dm": "D2", "Eb": "D#2", "C": "C2", "Bb": "A#1", "Gm": "G1", "A": "A1", "D5": "D2", "F": "F2", "D": "D2"}


def twin(ch, i):
    """速い旋律のリフ（16分）。2本目は3度上（透明感の層に3度上を弾かせる）"""
    r = up(LOW[ch], 1)   # 1オクターブ上の高さで旋律を弾く
    s = [0, 1, 3, 1, 5, 3, 1, 0, 7, 5, 3, 1, 3, 5, 7, 8] if i % 2 == 0 else [0, 3, 5, 7, 5, 3, 1, 3, 0, 1, 3, 5, 7, 5, 3, 1]
    pcs = scale_pcs("D", "phrygian")
    sc = [m for m in range(midi(r) - 2, midi(r) + 24) if m % 12 in pcs]
    base = min(range(len(sc)), key=lambda j: abs(sc[j] - midi(r)))
    lo = " ".join(f"{nm(sc[min(base + x, len(sc) - 1)])}:0.25{'!' if j % 4 == 0 else ''}" for j, x in enumerate(s))
    hi = " ".join(f"{nm(sc[min(base + x + 2, len(sc) - 1)])}:0.25" for j, x in enumerate(s))
    return bar(lo), bar(hi)


BUGLE = [bar("D4:0.75 D4:0.25 A4:1 R:0.5 D5:1.5"), bar("A4:0.75 A4:0.25 D5:1 R:0.5 A4:1 R:0.5"),
         bar("D4:0.75 G4:0.25 A4:1 R:0.5 D5:0.75 C5:0.25 A4:0.5"), bar("D5:2 R:2")]
SIGNAL = [bar("A4:1.5 D5:0.5 R:2"), bar("A4:1.5 D4:0.5 R:2"), bar("D5:3 R:1"), R4]
MORNING = [bar("R:1 A4:0.5 F4:0.5 D4:1 E4:0.5 F4:0.5"), bar("D4:1.5 R:0.5 F4:0.5 A#4:0.5 A4:1"),
           bar("R:0.5 C5:0.5 A4:0.5 F4:0.5 G4:1 A4:0.5 R:0.5"), bar("G4:1.5 E4:0.5 C4:1 R:1"),
           bar("R:1 A4:0.5 D5:0.5 C5:1 A4:0.5 F4:0.5"), bar("D4:1 F4:0.5 A#4:0.5 D5:1 R:1"),
           bar("R:0.5 D5:0.5 C5:0.5 A#4:0.5 G4:1 A#4:0.5 R:0.5"), bar("A4:1.5 C#5:0.5 E5:1 R:1")]
MORNING_BASS = [bar(x) for x in melody_walk(scale_pcs("D", "aeolian"), "A2", "D2", [[1.5, 0.5, 2], [1, 1, 1, 1], [2, 1, 1], [3, 1]], 5,
                                             (["Dm", "Bb", "F", "C", "Dm", "Bb", "Gm", "A"] * 2)[4:16], contour=(-1, -1, 2, -1, 1), lo="C2", hi="D3")]
CHORALE = {"Bb": ["D5", "A#4", "F4"], "F": ["C5", "A4", "F4"], "Gm": ["D5", "A#4", "G4"], "Dm": ["D5", "A4", "F4"], "D": ["D5", "A4", "F#4"],
           "Eb": ["D#5", "A#4", "G4"], "A": ["C#5", "A4", "E4"], "C": ["C5", "G4", "E4"]}

P = {k: [] for k in ["riff", "riff2", "rhy", "lead", "clean", "tp", "b0", "b1", "b2", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = riff2 = rhy = lead = clean = tp = R4; br = [R4] * 3
    g = LOW[ch]; root = root_note(ch if ch != "D5" else "Dm")
    if name == "night":
        br = [bar(f"{x}:4,") for x in CHORALE["Dm"]] if i >= 2 else br
        b = R4
    elif name == "bugle":
        tp = BUGLE[i]; b = R4
    elif name == "assault":
        if 16 <= i < 20:     # 塹壕の中で息をつく4小節: 刻みだけ
            riff = rhy = bar(f"{g}:0.5! {g}:0.25 {g}:0.25 R:0.5 {g}:0.5! {g}:0.25 {g}:0.25 R:0.5 {g}:0.5! R:0.5")
        else:
            riff, riff2 = twin(ch, i)
            rhy = bar(" ".join(f"{g}:0.25{'!' if j % 4 == 0 else ''}" for j in range(16)))
        b = bar(" ".join(f"{root}:0.5{'!' if j % 2 == 0 else ''}" for j in range(8)))
    elif name == "barrage":
        riff = rhy = bar(f"{g}:1.5! {g}:0.5 R:0.5 {g}:0.5! {tr(g, 1)}:1")
        if i % 2 == 0: br = [bar(f"{x}:0.5! R:1.5 {x}:0.5! R:1.5") for x in CHORALE.get(ch, CHORALE["Dm"])]
        b = unison_low(riff, -1, "B0")
    elif name == "signal":
        tp = SIGNAL[i]; b = R4
    elif name == "morning":
        # 2026-10-24 人間「ベースでメロディ作るのもありかも」: 朝の歌を、途中からベースが受けつぐ（生き残った兵士の低い声）。
        #   12〜19小節目はベースが朝の歌（2オクターブ下）、クリーンは和音に回る。20小節目からは金管の聖歌の下で、ベースが動く対旋律
        if 12 <= i < 20:
            b = bar(shift_oct(strip_marks(MORNING[i % 8]), -2))
            tones = (chord_tones(ch, "D4", "D5") * 2)[:4]
            clean = bar(" ".join(f"{t}:1" for t in tones))
        else:
            clean = MORNING[i % 8] if i >= 4 else R4
            b = MORNING_BASS[i - 20] if i >= 20 else (bar(f"{root}:2 {fifth_of(ch)}:2") if i >= 8 else (bar(f"{root}:4,") if i >= 2 else R4))
        if i >= 20: br = [bar(f"{x}:4,") if i % 2 == 0 else R4 for x in CHORALE.get(ch, CHORALE["Dm"])]
    else:   # light
        br = [bar(f"{x}:4,") for x in CHORALE[ch]]
        clean = bar(" ".join(f"{t}:1" for t in (chord_tones(ch, 'D4', 'D5') * 2)[:4])) if i < 5 else bar("D4:4")
        b = R4
    P["riff"].append(riff); P["riff2"].append(riff2); P["rhy"].append(rhy); P["lead"].append(lead); P["clean"].append(clean); P["tp"].append(tp)
    for j in range(3): P[f"b{j}"].append(br[j])
    P["bass"].append(b)
    tom = "R:3 A1:0.5, G1:0.5," if name == "night" and i % 2 == 1 else None
    kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.", tom)

J = lambda k: " ".join(P[k])
BR = dict(reverb=0.45, attack=0.05, release=0.5, fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 1500, "high": 0}, {"type": "reverb", "mix": 0.25}])
song.add(riff_parts(J("riff"), clear=False))
song.add(part("看板リフ（3度上の2本目）", "distGuitar", J("riff2"), **{**LEAD_BASE, "volume": 0.08, "pan": 0.3, "ampDrive": 0.4, "phrase": None, "sustain": 1.0, "release": 0.3,
              "fx": [{"type": "filter", "kind": "highpass", "freq": 140, "q": 0.7}, {"type": "eq", "low": -2, "mid": 1.5, "midHz": 1500, "high": 1}, {"type": "room", "mix": 0.1}]}))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(clean_part(J("clean"), vol=0.12, pan=-0.1, role="クリーンの歌（朝）"))
song.add(part("トランペット（合図）", "brass", J("tp"), patch="trumpet", volume=0.13, pan=0.15, phrase=4, **BR))
song.add([part(f"金管（{['上', '中', '下'][j]}）", "brass", J(f"b{j}"), patch="brassSection" if j < 2 else "horn", volume=0.1, pan=[-0.2, 0.2, 0][j], **BR) for j in range(3)])
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "wide-dark-wall"

from lm25_plans import apply_plan
apply_plan(song, "12")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-12-zangou.json"
    song.write(out)
    check_clash(song)
