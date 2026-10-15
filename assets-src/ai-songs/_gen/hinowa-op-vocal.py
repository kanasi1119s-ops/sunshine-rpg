# 『ひのわのそらへ』（仮）の歌（重音テト用。オリジナルの歌詞と旋律）。リングライト・クロニクルのオープニング曲。
# 2026-10-16、人間の指示「オープニング曲は、既存のとは別で、冒険に出るのがワクワクで楽しみなケルト感あるやつで」。
# BPM160・ニ長調・4/4・56小節（1分24秒）。サビの最後でタイトル「リングライト・クロニクル」を歌う。
# 1音＝1文字（ひらがな。拗音は1音）。小さい「っ」は使わない。「を」は「お」、助詞の「へ」は「え」と書く。音域 D4〜E5。
# 並び: 前奏（バグパイプと笛）8 → リフ8（歌なし）→ Aメロ8 → Bメロ8 → サビ16 → 後奏8（タイトル）

MV = ["R:0.5 A4:0.5 A4:0.5 B4:0.5 A4:0.5 F#4:0.5 D4:1", "G4:0.5 G4:0.5 A4:0.5 B4:0.5 D5:1 B4:1",
      "R:0.5 A4:0.5 A4:0.5 D5:0.5 C#5:0.5 B4:0.5 A4:1", "E4:0.5 F#4:0.5 G4:0.5 A4:0.5 E4:2",
      "R:0.5 F#4:0.5 F#4:0.5 B4:0.5 A4:0.5 F#4:0.5 D4:1", "G4:0.5 A4:0.5 B4:0.5 D5:0.5 E5:1 D5:1",
      "C#5:0.5 B4:0.5 A4:0.5 G4:0.5 A4:1 E4:1", "A4:2 R:2"]
MP = ["G4:1 G4:0.5 A4:0.5 B4:2", "D5:1 B4:0.5 A4:0.5 G4:2", "A4:1 A4:0.5 B4:0.5 C#5:2", "D5:1.5 A4:0.5 F#4:2",
      "G4:1 B4:0.5 D5:0.5 E5:2", "D5:1 B4:0.5 G4:0.5 B4:2", "C#5:1 D5:0.5 E5:0.5 C#5:2", "E5:1 E5:1 R:2"]
MC = ["A4:0.5 D5:1 D5:0.5 E5:1 D5:1", "C#5:1 A4:0.5 C#5:0.5 E5:2", "D5:1 C#5:0.5 B4:0.5 F#4:1 A4:1", "B4:3 R:1",
      "A4:0.5 D5:1 D5:0.5 E5:1 D5:1", "C#5:1 A4:0.5 C#5:0.5 E5:2", "B4:1 D5:0.5 B4:0.5 G4:1 B4:1", "A4:3 R:1"]
MC2 = ["A4:0.5 D5:1 D5:0.5 E5:1 D5:1", "C#5:1 A4:0.5 C#5:0.5 E5:2", "D5:1 C#5:0.5 B4:0.5 F#4:1 B4:1", "D5:3 R:1",
       "E5:1 D5:0.5 B4:0.5 G4:0.5 A4:0.5 B4:1", "C#5:1 D5:0.5 C#5:0.5 E5:2", "D5:4", "R:4"]

L = {
    "A1": ["あ さ の み な と", "か ぜ が よ ん だ", "ち ず の む こ う", "と お い そ ら",
           "か ば ん ひ と つ", "む ね が お ど る", "あ し た え い こ", "う"],
    "B1": ["ひ か り の", "わ お お え", "め ざ め た", "い し が", "み ち び く", "そ の さ き", "ま だ み ぬ", "あ す"],
    "C1": ["か け だ そ う", "か ぜ よ り", "ひ の わ の そ", "ら", "め ぐ り あ う", "な か ま と", "つ む い で く", "よ"],
    "C2": ["ど こ ま で も", "と お く え", "ひ か り の さ", "き", "り ん ぐ ら い と", "く ろ に く", "る", ""],
}
MEL = {"A1": MV, "B1": MP, "C1": MC, "C2": MC2}

def make(key):
    out = []
    for mel, lyr in zip(MEL[key], L[key]):
        assert abs(sum(float(t.split(":")[1]) for t in mel.split()) - 4) < 1e-9, (key, mel)
        kana = lyr.split(); toks = []; j = 0
        for t in mel.split():
            if t.startswith("R:"): toks.append(t); continue
            p, d = t.split(":"); toks.append(f"{kana[j]}:{p}:{d}"); j += 1
        assert j == len(kana), (key, mel, lyr)
        out.append(" ".join(toks))
    return out
V = {k: make(k) for k in L}
ORDER = [None, None, "A1", "B1", "C1", "C2", None]

def bars():
    out = []
    for key in ORDER: out += ["R:4"] * 8 if key is None else V[key]
    return out

def notes():
    res = []; t = 0.0
    for i, bar in enumerate(bars()):
        s = 0.0
        for tok in bar.split():
            if tok.startswith("R:"): d = float(tok[2:])
            else:
                kana, pitch, d = tok.split(":"); d = float(d); res.append((t + s, d, pitch, kana))
            s += d
        assert abs(s - 4) < 1e-9, (i + 1, s, bar)
        t += 4
    return res

if __name__ == "__main__":
    ns = notes(); print(len(bars()), "bars", len(ns), "notes", "".join(n[3] for n in ns))
