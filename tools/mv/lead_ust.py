"""歌の本線の UST を、曲の JSON と台本の歌詞（*.json.kana）から作る（歌詞の表示と口の形のため）。2026-11-22
場面ごとに声を分けた曲・ハモリ・声のチョップがある曲は、UST が何本にも分かれるので、本線だけを1本にまとめる。
  python3 lead_ust.py <曲.json> <見本の UST（頭の部分を借りる）> <出力.ust>
本線の歌詞は *.json.kana の [拍, かな]。その拍から始まる音の長さを、vocals の中から探す（見つからなければ次の歌詞までの長さ。長くても 2 拍）。"""
import sys, json
song, sample, out = sys.argv[1:4]
js = json.load(open(song)); kana = json.load(open(song + ".kana"))
starts = {}
for v in js["vocals"]:
    t = 0.0
    for tok in v["notes"].split():
        p = tok.split(":"); L = float(__import__("re").match(r"[0-9.]+", p[1]).group(0))
        if not tok.startswith("R") and len(p) >= 3: starts.setdefault(round(t, 3), L)
        t += L
notes = []; miss = 0
for i, (b, k) in enumerate(kana):
    L = starts.get(round(b, 3))
    if L is None: miss += 1; L = min(2.0, (kana[i + 1][0] - b) if i + 1 < len(kana) else 1.0)
    if i + 1 < len(kana): L = min(L, kana[i + 1][0] - b)
    if L > 1e-6: notes.append((b, L, k))
head = open(sample, "rb").read().decode("cp932").split("[#0000]")[0]
body = []; t = 0.0
for beat, L, ly in notes:
    if beat > t + 1e-6: body.append(("R", beat - t))
    elif beat < t - 1e-6: continue
    body.append((ly, L)); t = beat + L
txt = head
for i, (ly, L) in enumerate(body): txt += f"[#{i:04d}]\nLength={int(round(L * 480))}\nLyric={ly}\nNoteNum=60\n"
txt += "[#TRACKEND]\n"
open(out, "wb").write(txt.encode("cp932", errors="replace"))
print(len(kana), "音 →", len(notes), "（長さが見つからない", miss, "）")
