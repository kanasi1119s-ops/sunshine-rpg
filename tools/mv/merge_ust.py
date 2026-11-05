# 2つの声の UST を1つにまとめる（歌詞の表示と口の形のため）。重なる所は1つ目の声を優先する
import sys
sys.path.insert(0, "/home/claude/wt-mix/tools/mv"); import lyric_mouth as LM
a, b, out = sys.argv[1:4]
n1 = LM.read_ust(a); n2 = LM.read_ust(b)
def over(x, lst): return any(x[0] < y[0] + y[1] - 1e-6 and y[0] < x[0] + x[1] - 1e-6 for y in lst)
notes = sorted(n1 + [x for x in n2 if not over(x, n1)])
head = open(a, "rb").read().decode("cp932").split("[#0000]")[0]
body = []; t = 0.0; i = 0
for beat, L, ly in notes:
    if beat > t + 1e-6: body.append(("R", beat - t))
    elif beat < t - 1e-6: continue
    body.append((ly, L)); t = beat + L
txt = head
for i, (ly, L) in enumerate(body):
    txt += f"[#{i:04d}]\nLength={int(round(L * 480))}\nLyric={ly}\nNoteNum=60\n"
txt += "[#TRACKEND]\n"
open(out, "wb").write(txt.encode("cp932"))
print(len(n1), len(n2), "→", len(notes))
