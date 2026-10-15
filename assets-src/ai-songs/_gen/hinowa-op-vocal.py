# 『ひのわのそらへ』（仮）の歌（重音テト用。オリジナルの歌詞と旋律）。リングライト・クロニクルのオープニング曲。
# 2026-10-16 改訂（人間の指摘「ケルト感ないかな。ケルトちょっと勉強してきて」）: アイルランドの踊りの曲「ジグ」の拍子（6/8＝1拍を3つに分ける）に書き直した。
#   作曲ソフトでは 4/4・BPM120 の1拍を3連符（1/3拍）に分けて書く（12/8 と同じ。付点4分音符＝1拍＝0.5秒）。1小節＝2秒。
# 旋律は「4分＋8分（2:1）」と「8分3つ」のジグの型を中心に、ミクソリディアン（C の音）の色を少し入れる。音域 D4〜E5。
# 1音＝1文字（拗音は1音）。小さい「っ」は使わない。「を」は「お」、助詞の「へ」は「え」と書く。
# 並び（44小節・88秒）: 前奏4 → 笛とフィドルの曲（ジグの A）8 → Aメロ8 → Bメロ4 → サビ16 → 後奏（ジグの B）4

def tri(s):
    """「音名:8分の数」（3連の8分＝1）を「音名:拍」に。R も同じ。"""
    out = []
    for t in s.split():
        n, k = t.rsplit(":", 1)
        out.append((n, int(k)))
    assert sum(k for _, k in out) == 12, s
    return out

MV = ["R:1 A4:1 B4:1 D5:2 A4:1 F#4:2 E4:1 D4:3", "R:1 G4:1 A4:1 C5:2 B4:1 A4:2 G4:1 E4:3",
      "R:1 B4:1 C5:1 D5:2 B4:1 G4:2 A4:1 B4:3", "A4:2 F#4:1 D4:3 R:6",
      "R:1 A4:1 B4:1 D5:2 E5:1 D5:2 B4:1 A4:3", "R:1 G4:1 A4:1 C5:2 D5:1 E5:2 D5:1 C5:3",
      "B4:2 C#5:1 D5:2 C#5:1 B4:2 A4:1 E4:3", "A4:3 A4:3 R:6"]
MP = ["E4:1 G4:1 B4:1 E5:3 D5:3 B4:3", "G4:1 B4:1 D5:1 E5:3 D5:2 B4:1 D5:3",
      "C#5:2 D5:1 E5:3 C#5:2 A4:1 E5:3", "E5:6 R:6"]
C1 = ["A4:1 D5:2 D5:1 E5:2 D5:1 A4:2 F#4:1 A4:2", "G4:1 C5:2 C5:1 D5:2 C5:1 G4:2 E4:1 G4:2",
      "B4:1 D5:2 D5:1 E5:2 D5:1 B4:2 G4:1 B4:2", "A4:2 F#4:1 A4:3 R:6",
      "R:1 B4:1 C#5:1 D5:2 B4:1 F#4:2 B4:1 D5:3", "R:1 G4:1 A4:1 B4:2 D5:1 E5:3 D5:3",
      "C#5:2 B4:1 A4:2 C#5:1 E5:3 C#5:3", "A4:6 R:6"]
C2 = C1[:3] + ["D5:3 A4:3 R:6", "B4:2 C5:1 D5:3 E5:2 D5:1 B4:3", "C#5:2 D5:1 E5:3 C#5:3 R:3", "D5:12", "R:12"]

# 2026-10-16 改訂（人間の指示「歌詞幻想的な感じも入れようか」）: 星降る港・霧の向こうの歌・精霊・魔法の空・古の歌など、幻想的なことばを入れた。旋律は同じ（1小節の文字数を合わせた）。
L = {
    "V": ["ほ し ふ る み な と", "き り の む こ う で", "だ れ か が う た う", "と お く",
          "ゆ め の ち ず に は", "ほ し の し る し が", "あ し た え ま ね く", "さ あ"],
    "P": ["め ざ め の か ね", "せ い れ い の こ え", "ま ほ う の そ ら", "え"],
    "C1": ["さ あ か け だ そ う よ", "ほ し く ず の う み お", "ひ の わ の そ ら ま で", "ゆ こ う",
           "い に し え の う た", "つ ば さ に の せ", "は こ ん で い く", "よ"],
    "C2": ["ど こ ま で も ゆ こ う", "ゆ め の そ の さ き え", "こ の て に か が や く", "ほ ら",
           "り ん ぐ ら い と", "く ろ に く", "る", ""],
}
MEL = {"V": MV, "P": MP, "C1": C1, "C2": C2}

def fmt(x): return ("%.6f" % x).rstrip("0").rstrip(".")
def make(key):
    out = []
    for mel, lyr in zip(MEL[key], L[key]):
        kana = lyr.split(); toks = []; j = 0
        for n, k in tri(mel):
            d = fmt(k / 3)
            if n == "R": toks.append(f"R:{d}"); continue
            toks.append(f"{kana[j]}:{n}:{d}"); j += 1
        assert j == len(kana), (key, mel, lyr)
        out.append(" ".join(toks))
    return out
V = {k: make(k) for k in L}
REST = "R:4"
LAYOUT = [None] * 4 + [None] * 8 + V["V"] + V["P"] + V["C1"] + V["C2"] + [None] * 4   # 44小節
# 表情のためのセクション（utau-render が 8小節ごとに見る）: 0-7 前奏, 8-15 Aメロ, 16-23 Bメロ, 24-31 サビ, 32-39 サビ, 40- 後奏
ORDER = [None, "A", "B", "C", "C", None]

def bars():
    return [REST if b is None else b for b in LAYOUT]

def notes():
    res = []; t = 0.0
    for i, bar in enumerate(bars()):
        s = 0.0
        for tok in bar.split():
            if tok.startswith("R:"): d = float(tok[2:])
            else:
                kana, pitch, d = tok.split(":"); d = float(d); res.append((t + s, d, pitch, kana))
            s += d
        assert abs(s - 4) < 1e-4, (i + 1, s, bar)
        t += 4
    return res

if __name__ == "__main__":
    ns = notes(); print(len(bars()), "bars", len(ns), "notes", "".join(n[3] for n in ns))
