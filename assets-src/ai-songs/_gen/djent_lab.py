# ジェント／プログレッシブ・メタル風の試験曲（「メシュガーのような音」の音の質感を確かめる用。リフ・リズムは自作。既存曲はまねない）
#   2026-10-20 人間「メシュガーみたいなギターの音も再現してほしい」
#   8弦の半音下げ（いちばん低い F1）の単音の刻み。7つ（16分×7）のまとまりが小節線をまたいで回り、キックがギターと同じ位置を打つ。
#   スネアは3拍目だけ（重く遅く感じる）、ライドとハイハットは4分で拍を保つ。
#   ギター: 歪ませる前の録音（DI）→ 高域の共振を戻す EQ（低く下げた録音のこもりを補う）→ ゲート（検出 500Hz）→ ブースト（200Hz から下を削る）→ 学習式アンプ → 4x12 のIR
# 使い方: python3 djent_lab.py <出力.json>
import json, sys
out = sys.argv[1]
BPM = 118; BARS = 24
STEP = 0.25
# 7つのまとまり（16分）: 強い開放 → ミュート2つ → 休み → ミュート → 開放 → 休み（自作の型）
CELL = [("F1", "!", 1), ("F1", ",", 1), ("F1", ",", 1), (None, "", 1), ("F1", ",", 1), ("F#1", "!", 1), (None, "", 1)]
CELL_B = [("F1", "!", 1), ("F1", ",", 1), (None, "", 1), ("G#1", "!", 2), ("F1", ",", 1), ("A1", "!", 1)]
def seq(cells, bars, start=0):
    total = bars * 16; out = []; pos = 0; i = 0
    while pos < total:
        n, m, d = cells[i % len(cells)]
        d = min(d, total - pos)
        out.append((n, m, d, pos)); pos += d; i += 1
    return out
secs = [("A", 8), ("B", 8), ("A2", 8)]
gtr, kick = [], []
for name, bars in secs:
    cells = CELL if name != "B" else CELL_B
    for n, m, d, pos in seq(cells, bars):
        gtr.append(f"{n}:{d*STEP}{m}" if n else f"R:{d*STEP}")
        kick.append("X" if (n and m == "!") else ("x" if n else ".") )
        kick += ["."] * (d - 1)
# サビ代わりの B では、伸ばす不協和の音を重ねる（2本目のギター。5度を重ねない単音）
lead = []
for name, bars in secs:
    if name == "B":
        lead += ["C4:4_ C#4:4 B3:4_ A#3:4", "C4:4 D#4:4 C#4:8"]
    else:
        lead += ["R:4"] * bars
gtr_notes = " ".join(gtr)
bass_notes = gtr_notes  # ベースもギターと同じ音域（このジャンルの作り。ベースの音源は B0 まで出る）
ride = " ".join(["D2:1"] * (BARS * 4))
snare = "g:" + "........X......." * BARS
hat = "g:" + "x...x...x...x..." * BARS
rig = {"amp": "namDD", "ampDrive": 1.4, "ampGate": 50, "ampGateHz": 500, "ampTight": 1, "ampTightHz": 200,
       "ampCabIr": "jd-brutal-4x12-01+jd-greenback-4x12-02", "double": {"irR": "jd-brutal-4x12-06+jd-brutal-4x12-12"},
       "powerChord": False, "fx": [{"type": "eq", "low": 0, "mid": 4, "midHz": 3000, "high": 0, "pre": True}]}
song = {
    "title": "ジェントの試験曲", "description": "仮: 8弦の低い刻みの音づくりを確かめる試験曲（F1・bpm118・自作のリフ）",
    "bpm": BPM, "beats": 4, "chords": "Fm", "barsPerChord": 1, "repeats": BARS, "autoAccompaniment": False,
    "feel": "rock", "tone": "metal", "dynamics": True, "human": 0.25, "diGuitar": "emily", "autoScoop": False, "guitarWobble": False,
    "sections": [{"kind": "verse", "bars": 8}, {"kind": "chorus", "bars": 8}, {"kind": "verse", "bars": 8}],
    "parts": [
        {"instrument": "distGuitar", "role": "刻み（8弦）", "volume": 0.11, "pan": 0, **rig, "notes": gtr_notes},
        {"instrument": "leadGuitar", "role": "伸ばす不協和の音", "volume": 0.07, "pan": 0.3, "amp": "namDD", "ampDrive": 0.5, "ampCabIr": "dd-v30-2x12-cap-2in",
         "reverb": 0.35, "fx": [{"type": "delay", "beats": 0.75, "mix": 0.18, "feedback": 0.3}], "noRestrike": True, "notes": " ".join(lead)},
        {"instrument": "bass", "role": "ベース（ギターと同じ動き）", "volume": 0.16, "pan": 0, "amp": "bassSplit", "ampDrive": 0.5, "notes": bass_notes},
        {"instrument": "kick", "role": "キック（ギターと同じ位置）", "volume": 0.2, "pan": 0, "amp": "auto", "notes": "g:" + "".join(kick)},
        {"instrument": "snare", "role": "スネア（3拍目）", "volume": 0.17, "pan": 0, "amp": "auto", "notes": snare},
        {"instrument": "crash", "role": "ライド", "volume": 0.05, "pan": 0, "amp": "auto", "notes": ride},
    ],
}
json.dump(song, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, BARS, "小節", round(BARS * 4 * 60 / BPM, 1), "秒")
