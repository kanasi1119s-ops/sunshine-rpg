# ラウドロックの試験曲（作曲ソフトの「現代のロック・ラウドロック」の音づくりを確かめる用）。2026-10-20 人間「全部やって」
#   ドロップC（いちばん低い弦＝C2）・bpm 150・4/4。導入 → Aメロ（ブリッジミュートの刻み）→ Bメロ（盛り上げ）→ サビ（開いた和音・左右の壁）
#   → ブレイクダウン（ハーフタイム・キックとギターをそろえる）→ サビ。
#   RIG=old（今までの作り: 歪んだ録音のギター＋歪み系アンプ）／RIG=new（DIのギター＋学習式アンプ＋録音のキャビネット＋ダブルトラック など）
# 使い方: RIG=new python3 loud_rock_lab.py <出力.json> [bars=32|full]
import json, os, sys

RIG = os.environ.get("RIG", "new")
out = sys.argv[1]
FULL = len(sys.argv) > 2 and sys.argv[2] == "full"

# ── 構成（小節）──
if FULL:
    SEC = [("intro", 4), ("verse", 8), ("pre", 4), ("chorus", 8), ("verse", 8), ("pre", 4), ("chorus", 8), ("bridge", 8), ("breakdown", 4), ("chorus", 8), ("outro", 4)]
else:
    SEC = [("intro", 4), ("verse", 8), ("pre", 4), ("chorus", 8), ("breakdown", 4), ("chorus", 4)]
BARS = sum(b for _, b in SEC)
# 作曲ソフトの kind に直す（breakdown は bridge 扱い）
KIND = {"intro": "intro", "verse": "verse", "pre": "pre", "chorus": "chorus", "breakdown": "bridge", "bridge": "interlude", "outro": "outro"}

# コード（2小節ずつ）: Cm Ab Eb Bb → ドロップCの根音
ROOT = ["C2", "G#2", "D#2", "A#2"]   # ギターの刻みの根音（Bb は 6弦で出ないので A#2）
BROOT = ["C2", "G#1", "D#2", "A#1"]  # ベース

def bars_of(kind):
    return [k for k, b in SEC for _ in range(b)]
SECBAR = bars_of(None)

def chord_bar(i):
    return i // 2 % 4

# ── ギター（リズム）──
RIFF = [  # 導入とサビの前の「顔」のリフ（2小節）
    "C2:0.25! C2:0.25' R:0.25 C2:0.25' C2:0.5! D#2:0.5 C2:0.25 C2:0.25' R:0.25 C2:0.25' F2:0.5! F#2:0.25 G2:0.25",
    "C2:0.25! C2:0.25' R:0.25 C2:0.25' C2:0.5! D#2:0.5 G#2:1! G2:1",
]
def gtr_bar(i, sec):
    r = ROOT[chord_bar(i)]
    if sec == "intro":
        return RIFF[i % 2]
    if sec == "verse":   # ブリッジミュートの刻み（16分の「ズクズク」＋拍頭のアクセント）。根音が変わる小節は頭を開く
        return f"{r}:0.25! {r}:0.25, {r}:0.25, {r}:0.25 {r}:0.25! {r}:0.25, R:0.25 {r}:0.25 {r}:0.25! {r}:0.25, {r}:0.25, {r}:0.25 {r}:0.5! {r}:0.25, {r}:0.25"
    if sec == "pre":     # 8分で開いて、だんだん詰める
        return f"{r}:0.5! {r}:0.5 {r}:0.5 {r}:0.5 {r}:0.5! {r}:0.5 {r}:0.25 {r}:0.25 {r}:0.25 {r}:0.25"
    if sec == "chorus":  # 開いた和音（伸ばす）＋8分
        return f"{r}:1.5! {r}:0.5 {r}:1 {r}:0.5 {r}:0.5"
    if sec == "breakdown":  # ハーフタイムの刻み（キックとそろえる）
        return "C2:0.75! C2:0.75! C2:0.5! R:1 C2:0.25! C2:0.25' R:0.5" if i % 2 == 0 else "C2:0.75! C2:0.75! C2:0.5! C#2:0.5! D2:0.5! D#2:1!"
    if sec == "bridge":  # 静かに（伸ばし）
        return f"{r}:4"
    if sec == "outro":
        return "C2:4!" if i == BARS - 4 else "R:4"
    return "R:4"

def part_notes(fn, only=None):
    s = []
    for i, sec in enumerate(SECBAR):
        s.append(fn(i, sec) if only is None or sec in only else "R:4")
    return " ".join(s)

# ── ベース（ギターの根音に合わせる。刻みはキックと同じ位置）──
def bass_bar(i, sec):
    b = BROOT[chord_bar(i)]
    if sec in ("intro",):
        return RIFF[i % 2].replace("C2", "C1").replace("D#2", "D#1").replace("F2", "F1").replace("F#2", "F#1").replace("G2", "G1").replace("G#2", "G#1")
    if sec == "verse":
        return f"{b}:0.75 {b}:0.75 {b}:0.5 {b}:0.75 {b}:0.75 {b}:0.5"
    if sec == "pre":
        return f"{b}:0.5 {b}:0.5 {b}:0.5 {b}:0.5 {b}:0.5 {b}:0.5 {b}:0.5 {b}:0.5"
    if sec == "chorus":
        return f"{b}:1.5 {b}:0.5 {b}:1 {b}:0.5 {b}:0.5"
    if sec == "breakdown":
        return "C1:0.75 C1:0.75 C1:0.5 R:1 C1:0.25 C1:0.25 R:0.5" if i % 2 == 0 else "C1:0.75 C1:0.75 C1:0.5 C#1:0.5 D1:0.5 D#1:1"
    if sec == "bridge":
        return f"{b}:4"
    if sec == "outro":
        return "C1:4" if i == BARS - 4 else "R:4"
    return "R:4"

# ── ドラム（16分のグリッド。セクションの最後の小節はフィル）──
def last_of_sec(i):
    return i + 1 == BARS or SECBAR[i + 1] != SECBAR[i] or (SECBAR[i] in ("verse", "chorus") and (i + 1) % 8 == 0)
def first_of_sec(i):
    return i == 0 or SECBAR[i - 1] != SECBAR[i]

def kick_bar(i, sec):
    if sec == "intro":   return "X.X..X..X.X...X." if i % 2 == 0 else "X.X..X..X...X.X."
    if sec == "verse":   return "X..X..X.X..X..X." if i % 4 != 3 else "X..X..X.X.X.X..."
    if sec == "pre":     return "X...X...X...X..." if i % 4 < 2 else "X.X.X.X.X.X.XXXX"
    if sec == "chorus":  return "X.x.X.x.X.x.X.x." if not last_of_sec(i) else "X.x.X.x.X......."
    if sec == "breakdown": return "X..X..X.....X.X." if i % 2 == 0 else "X..X..X.X.X.X..."
    if sec == "bridge":  return "X...............X" [:16] if i % 2 == 0 else "................"
    if sec == "outro":   return "X..............." if i == BARS - 4 else "................"
    return "................"
def snare_bar(i, sec):
    fill_end = last_of_sec(i) and sec not in ("bridge", "outro", "breakdown")
    if sec == "intro":   return "....X.......X..." if not fill_end else "....X.....xxXXXX"
    if sec == "verse":   return "....X..o....X..o" if not fill_end else "....X.......xXxX"
    if sec == "pre":     return "....X.......X..." if i % 4 < 2 else ("X...X...X.X.X.X." if i % 4 == 2 else "XXXXXXXXXXXXXXXX")
    if sec == "chorus":  return "....X.......X..." if not fill_end else "....X..........."
    if sec == "breakdown": return "........X......."
    if sec == "bridge":  return "................" if i % 4 != 3 else "........x.x.xXXX"
    return "................"
def hat_bar(i, sec):
    if sec == "verse":   return "x.o.x.o.x.o.x.o."
    if sec == "pre":     return "x.x.x.x.x.x.x.x."
    if sec == "intro":   return "x.x.x.x.x.x.x.x." if i % 4 < 3 else "x.x.x.x........."
    return "................"
def tom_bar(i, sec):
    # 導入・サビの終わりのタム回し（高→低）。音名でタムの高さ
    if sec in ("chorus",) and last_of_sec(i) and i + 1 < BARS:
        return "R:2 C4:0.25! C4:0.25 A3:0.25! A3:0.25 F3:0.25! F3:0.25 D3:0.25! D3:0.25"
    return "R:4"
def cym_bar(i, sec):
    # crash パート: C2 クラッシュ／D2 ライド／B2 チャイナ／A2 スプラッシュ
    if sec == "chorus":
        head = "C2:1! " if first_of_sec(i) else "D2:1 "
        return head + "D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5" if not last_of_sec(i) else head + "D2:1 D2:1 R:1"
    if sec == "breakdown":
        return "B2:0.75! B2:0.75 B2:0.5 R:1 B2:0.5 R:0.5" if i % 2 == 0 else "B2:0.75! B2:0.75 B2:0.5 B2:1 B2:1"
    if sec in ("intro", "pre", "verse", "bridge", "outro") and first_of_sec(i):
        return "C2:4!" if sec != "bridge" else "A2:4"
    return "R:4"

def grid(fn):
    return "g:" + "".join(fn(i, sec) for i, sec in enumerate(SECBAR))

# ── リード（サビの旋律。Cマイナー）──
LEAD_CHORUS = [
    "G4:1.5! G#4:0.5 G4:1 F4:0.5 D#4:0.5", "D#4:3_ R:1",
    "C5:1.5! A#4:0.5 G#4:1 G4:0.5 F4:0.5", "G4:3~ R:1",
    "G4:1.5! G#4:0.5 A#4:1 C5:0.5 D5:0.5", "D#5:2! D5:1 C5:1",
    "A#4:1.5 C5:0.5 A#4:1 G#4:0.5 G4:0.5", "G4:3~ R:1",
]
def lead_bar(i, sec):
    if sec != "chorus":
        return "R:4"
    k = sum(1 for j in range(i) if SECBAR[j] == "chorus") % 8
    return LEAD_CHORUS[k]

PAD_CH = ["C3:2 C3:2", "C3:2 C3:2", "G#2:4", "G#2:4", "D#3:4", "D#3:4", "A#2:4", "A#2:4"]

drums_common = {"volume": 0.2, "pan": 0, "amp": "auto"}
parts = []
if RIG == "old":
    for side, pan in (("左", -0.95), ("右", 0.95)):
        parts.append({"instrument": "distGuitar", "role": f"刻み（{side}）", "volume": 0.09, "pan": pan, "amp": "modernHigh", "notes": part_notes(gtr_bar)})
else:
    # 新しい作り: 歪ませる前の録音（DI）→ ゲート → 低音を締めるブースト → 学習式アンプ（NAM）→ 録音のキャビネット2つを混ぜる
    rig = {"amp": "namDD", "ampGate": 40, "ampTight": 0.6, "ampCabIr": "dd-v30-2x12-mix-tight", "double": {"irR": "dd-v30-2x12-mix-balanced"}}
    parts.append({"instrument": "distGuitar", "role": "刻み", "volume": 0.1, "pan": 0, **rig, "notes": part_notes(gtr_bar, only=("intro", "pre", "chorus", "breakdown", "bridge", "outro"))})
    parts.append({"instrument": "distGuitar", "role": "刻み（ブリッジミュート）", "volume": 0.1, "pan": 0, **rig, "palmMute": True, "notes": part_notes(gtr_bar, only=("verse",))})
parts += [
    {"instrument": "bass", "role": "ベース", "volume": 0.18, "pan": 0, "amp": "auto" if RIG == "old" else "bassSplit", "notes": part_notes(bass_bar)},
    {"instrument": "kick", "role": "キック", "volume": 0.22, "pan": 0, "amp": "auto", "trigger": "tack", "notes": grid(kick_bar)},
    {"instrument": "snare", "role": "スネア", "volume": 0.18, "pan": 0, "amp": "auto", "push": 0.02, "notes": grid(snare_bar)},
    {"instrument": "hihat", "role": "ハイハット", "volume": 0.05, "pan": 0, "amp": "auto", "push": -0.01, "notes": grid(hat_bar)},
    {"instrument": "tom", "role": "タム", "volume": 0.16, "pan": 0, "amp": "auto", "notes": " ".join(tom_bar(i, s) for i, s in enumerate(SECBAR))},
    {"instrument": "crash", "role": "シンバル（クラッシュ・ライド・チャイナ）", "volume": 0.057, "pan": 0, "amp": "auto", "notes": " ".join(cym_bar(i, s) for i, s in enumerate(SECBAR))},
    {"instrument": "leadGuitar", "role": "リード（サビの旋律）", "volume": 0.13, "pan": 0, "amp": "lead", "noRestrike": True, "reverb": 0.25,
     "fx": [{"type": "delay", "beats": 0.75, "mix": 0.18, "feedback": 0.3}], "notes": " ".join(lead_bar(i, s) for i, s in enumerate(SECBAR))},
    {"instrument": "pad", "role": "パッド（サビの厚み）", "volume": 0.07, "pan": 0, "amp": "auto", "reverb": 0.5,
     "sections": {"intro": 0, "verse": 0, "pre": 0.5, "chorus": 1, "bridge": 0.8, "outro": 0.6},
     "notes": " ".join(PAD_CH[i % 8] for i in range(BARS))},
]
song = {
    "title": "ラウドロックの試験曲" + ("（今までの作り）" if RIG == "old" else "（新しい作り）"),
    "description": "仮: 作曲ソフトのラウドロックの音づくりを確かめるための試験曲（ドロップC・bpm150）",
    "bpm": 150, "beats": 4, "chords": "Cm Cm Ab Ab Eb Eb Bb Bb", "barsPerChord": 1, "repeats": BARS // 8,
    "autoAccompaniment": False, "feel": "rock", "tone": "metal", "dynamics": True, "human": 0.35,
    "sections": [{"kind": KIND[k], "bars": b} for k, b in SEC],
    "parts": parts,
}
if RIG != "old":
    song["diGuitar"] = "emily"
json.dump(song, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, BARS, "小節", round(BARS * 4 * 60 / 150, 1), "秒")
