# ギターの試聴セット（2026-10-21 人間「ギターの音はありとあらゆるものに対応できるようにしたい」「実際聞かないとわからない」）
#   どの音色でも、同じ6つのフレーズ（自作）を鳴らす曲を作る。音色を変えて聞き比べ、良いものを音色（guitar-tones.ts）として残すための物差し。
#   1. パワーコード（伸ばす → 8分の刻み → ブリッジミュート）  2. オープンコードのストローク（8分）  3. アルペジオ（単音を伸ばして重ねる）
#   4. 単音のリフ（16分を含む）  5. リード（チョーキング・レガート。揺れは付けない）  6. 16分のカッティング
#   各フレーズは4小節、間に1小節の休み。bpm 100。ドラムなし（ギターだけを聞く）。
# 使い方:
#   python3 guitar_audition.py <出力.json> --tone loud-mid            … 保存した音色（guitarTone）で
#   python3 guitar_audition.py <出力.json> --part '{"amp":"namDD",...}' … パートの設定を直接
#   [--di emily|fsbs]（歪ませる前の録音。既定 emily） [--drop]（ドロップDの低い音で刻む）
import argparse, json

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--tone")
ap.add_argument("--part", default="{}")
ap.add_argument("--di", default="emily")
ap.add_argument("--drop", action="store_true")
ap.add_argument("--title", default=None)
a = ap.parse_args()
rig = json.loads(a.part)
if a.tone:
    rig = {"guitarTone": a.tone, **rig}

R = "R:4"
def bars(n): return " ".join([R] * n)
low = "D2" if a.drop else "E2"
# 1. パワーコード（根音だけ書く。distGuitar は 5度とオクターブを自動で重ねる）
power = f"{low}:4! A2:2! G2:2! {low}:0.5! {low}:0.5 {low}:0.5 {low}:0.5 G2:0.5! G2:0.5 A2:1! " + \
        f"{low}:0.5! {low}:0.5, {low}:0.5, {low}:0.5 {low}:0.5! {low}:0.5, C3:0.5! B2:0.5! A2:4!"
power_pm = bars(2) + f" {low}:0.5! {low}:0.5, {low}:0.5, {low}:0.5 {low}:0.5! {low}:0.5, R:1 " + bars(1)
# 3. アルペジオ（Em → C → G → D の分散。伸ばして重ねる）
arp = "E3:0.5 B3:0.5 E4:0.5 G4:0.5 B4:0.5 G4:0.5 E4:0.5 B3:0.5 C3:0.5 G3:0.5 C4:0.5 E4:0.5 G4:0.5 E4:0.5 C4:0.5 G3:0.5 " + \
      "G2:0.5 D3:0.5 G3:0.5 B3:0.5 D4:0.5 B3:0.5 G3:0.5 D3:0.5 D3:0.5 A3:0.5 D4:0.5 F#4:0.5 A4:2"
# 4. 単音のリフ（16分を含む）
riff = f"{low}:0.25! {low}:0.25 G2:0.5! {low}:0.25! {low}:0.25 A2:0.5! {low}:0.25! {low}:0.25 A#2:0.25 A2:0.25 G2:0.5 {low}:0.5 " + \
       f"{low}:0.25! {low}:0.25 G2:0.5! {low}:0.25! {low}:0.25 A2:0.5! C3:0.5! B2:0.5 A2:0.5 G2:0.5 " + \
       f"{low}:0.25! {low}:0.25 G2:0.5! {low}:0.25! {low}:0.25 A2:0.5! {low}:0.25! {low}:0.25 A#2:0.25 A2:0.25 G2:0.5 {low}:0.5 E3:2! D3:2"
# 5. リード（チョーキング ^、レガート _。ビブラート ~ は付けない）
lead = "B4:1! D5:0.5 E5:0.5_ G5:1 E5:1 D5:1.5 B4:0.5 A4:2^ G4:1 A4:0.5 B4:0.5_ D5:2 E5:4^"

# パートごとに、自分のフレーズの区間だけ鳴らす（6つの区間＋休み）
SEC = [("intro", 5), ("verse", 5), ("pre", 5), ("chorus", 5), ("bridge", 5), ("outro", 5)]
order = [k for k, _ in SEC]
def only(kind): return {k: (1 if k == kind else 0) for k in order}
def pad(notes, kind):
    # 自分の区間の前は休み、区間の中は4小節＋1小節の休み、うしろも休み
    i = order.index(kind)
    return " ".join([bars(5 * i), notes, R, bars(5 * (len(order) - i - 1))]).strip()

base = {"volume": 0.12, "pan": 0, **rig}
parts = [
    {"instrument": "distGuitar", "role": "1 パワーコード", **base, "notes": pad(power, "intro")},
    {"instrument": "distGuitar", "role": "1 パワーコード（ブリッジミュート）", **base, "palmMute": True, "notes": pad(power_pm, "intro")},
    {"instrument": "guitar", "role": "2 オープンコードのストローク", **base, "notes": "", "strum": {"chords": "G D Em C", "bars": 1, "pattern": "pop"}, "sections": only("verse")},
    {"instrument": "guitar", "role": "3 アルペジオ", **base, "sustain": 1.6, "notes": pad(arp, "pre")},
    {"instrument": "distGuitar", "role": "4 単音のリフ", **base, "powerChord": False, "notes": pad(riff, "chorus")},
    {"instrument": "leadGuitar", "role": "5 リード", **{k: v for k, v in base.items() if k != "double"}, "noRestrike": True, "notes": pad(lead, "bridge")},
    {"instrument": "guitar", "role": "6 カッティング", **base, "notes": "", "strum": {"chords": "Em7 A7 Em7 A7", "bars": 1, "pattern": "funk-cut"}, "sections": only("outro")},
]
song = {
    "title": a.title or f"ギターの試聴セット（{a.tone or 'パートの設定'}）",
    "description": "仮: ギターの音色の聞き比べ用（6つのフレーズ。自作）",
    "bpm": 100, "beats": 4, "chords": "Em C G D", "barsPerChord": 1, "repeats": 30 // 4 * 1 + 2,
    "autoAccompaniment": False, "tone": "rock", "human": 0.3,
    "diGuitar": a.di, "autoScoop": False, "guitarWobble": False,
    "sections": [{"kind": k, "bars": b} for k, b in SEC],
    "parts": parts,
}
song["repeats"] = 30 // 4 + (1 if 30 % 4 else 0)
json.dump(song, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(a.out, "30 小節", round(30 * 4 * 60 / 100, 1), "秒")
