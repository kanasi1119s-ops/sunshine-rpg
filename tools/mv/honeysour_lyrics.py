"""「ハニー・サワー」の歌詞の字幕（ASS）を作る（2026-11-08 人間「歌詞は欲しいかも」）。
  python3 tools/mv/honeysour_lyrics.py <曲.json> <出力.ass>
  ・時刻は、歌の音符（曲.json.kana の「拍・ひらがな」）から取る。句ごとにひらがなをつなぎ、下の表の歌詞の行と照らし合わせる
  ・表示は漢字まじりの歌詞。歌う人で縁の色を変える（テト＝ピンク・テトの男性ボイス＝青・ふたり＝はちみつ色）
"""
import sys, json

SONG = sys.argv[1]; OUT = sys.argv[2]
BPM = 122.0; SPB = 60 / BPM
LINES = {
    "はにさわ": "ハニサワ！",
    "がらすのびんにしまったなつ": "ガラスの瓶にしまった夏", "はちみつみたいにとろけてる": "はちみつみたいにとろけてる",
    "きみのとなりはすっぱくて": "君のとなりは酸っぱくて", "ことばがのどにひっかかる": "言葉がのどに引っかかる",
    "ふるいあるばむのすみっこで": "古いアルバムのすみっこで", "わらうふたりはおなじかおで": "笑うふたりは同じ顔で",
    "いまもかわらずすきなの": "今も変わらず好きなの", "あまいだけじゃつまらない": "甘いだけじゃつまらない",
    "すこしすっぱい": "少し酸っぱい", "そのきもちごと": "その気持ちごと", "まぜてのみほして": "まぜて飲みほして", "さあいくよ": "さあ行くよ",
    "あわがはじけ": "泡がはじけ", "なつのにおいが": "夏のにおいが", "いまならいえるよ": "今なら言えるよ", "きいてよね": "聞いてよね",
    "はにはにさわ": "ハニハニサワー", "あまくてすっぱいこのこいを": "甘くて酸っぱいこの恋を", "いっきにのみほしてはじけたい": "一気に飲みほしてはじけたい",
    "はにはにはに": "ハニハニハニ", "すっぱいさわ": "酸っぱいサワー", "もっとちょうだい": "もっとちょうだい",
    "おばあちゃんのいれてくれた": "おばあちゃんの入れてくれた", "はちみつれもんのあじがする": "はちみつレモンの味がする",
    "あまいだけじゃない": "甘いだけじゃない", "それがこいでしょ": "それが恋でしょ",
}
# 2026-11-08 人間「英訳も入れましょう」: 日本語の下に小さく英語。直訳より、意味と気持ちが伝わる自然な英語に
EN = {
    "ハニサワ！": "Honey sour!", "ガラスの瓶にしまった夏": "Summer, tucked away in a glass jar", "はちみつみたいにとろけてる": "melting like honey",
    "君のとなりは酸っぱくて": "Being next to you tastes so sour", "言葉がのどに引っかかる": "my words get stuck in my throat",
    "古いアルバムのすみっこで": "In the corner of an old photo album", "笑うふたりは同じ顔で": "the two of us smile the very same way",
    "今も変わらず好きなの": "I still love you, just the same", "甘いだけじゃつまらない": "just sweet would be too boring",
    "少し酸っぱい": "A little sour", "その気持ちごと": "feelings and all", "まぜて飲みほして": "stir them in and drink it down", "さあ行くよ": "here we go!",
    "泡がはじけ": "The bubbles pop", "夏のにおいが": "and the scent of summer rises", "今なら言えるよ": "now I can say it", "聞いてよね": "so listen, okay?",
    "ハニハニサワー": "Honey honey sour", "甘くて酸っぱいこの恋を": "this sweet and sour love", "一気に飲みほしてはじけたい": "I want to gulp it down and burst",
    "ハニハニハニ": "Honey honey honey", "酸っぱいサワー": "sour, sour", "もっとちょうだい": "give me more!",
    "おばあちゃんの入れてくれた": "Just like the one Grandma made me", "はちみつレモンの味がする": "it tastes like honey lemon",
    "甘いだけじゃない": "It's not only sweet", "それが恋でしょ": "that's what love is, right?",
}
kana = json.load(open(SONG + ".kana"))
js = json.load(open(SONG))


def spans(v):
    out = []; t = 0.0
    for tok in v["notes"].split():
        L = float(tok.split(":")[1])
        if not tok.startswith("R"): out.append((t, t + L))
        t += L
    return out


def sings(sp, t):
    return any(a - 1e-6 <= t < b for a, b in sp)


teto = spans(js["vocals"][0]); man = spans(js["vocals"][2]) if len(js["vocals"]) > 2 else []
# 句を見つける: ひらがなを先頭から、表の行に合う長さでつないでいく（いちばん長く合うものから）
keys = sorted(LINES, key=len, reverse=True)
ev = []; i = 0
while i < len(kana):
    hit = None
    for k in keys:
        s = ""; j = i
        while j < len(kana) and len(s) < len(k):
            s += kana[j][1]; j += 1
        if s == k: hit = (k, j); break
    if hit is None: i += 1; continue
    k, j = hit
    b0 = kana[i][0]; b1 = kana[j - 1][0] + 0.5
    mid = (b0 + b1) / 2
    who = ("both" if sings(teto, mid) and sings(man, mid) else "man" if sings(man, mid) else "teto")
    ev.append([b0 * SPB, b1 * SPB, LINES[k], who]); i = j
# 表示の長さ: 歌い出しの 0.2秒前から、次の行の 0.05秒前まで（最大で歌い終わり＋1.2秒）
for n, e in enumerate(ev):
    nxt = ev[n + 1][0] if n + 1 < len(ev) else e[1] + 3
    e[0] = max(0.0, e[0] - 0.2); e[1] = min(e[1] + 1.2, nxt - 0.25)
COL = {"teto": "&H00A060F0&", "man": "&H00E8A040&", "both": "&H0030B8F0&"}   # ASS は BGR
def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Noto Sans CJK JP Black,54,&H00FFFFFF,&H00FFFFFF,&H00A060F0,&H64000000,0,0,0,0,100,100,1,0,1,5,3,2,40,40,170,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
rows = []
for a, b, txt, who in ev:
    fs = 54 if len(txt) <= 11 else max(38, int(54 * 11 / len(txt)))
    rows.append(f"Dialogue: 0,{ts(a)},{ts(b)},L,,0,0,0,,{{\\3c{COL[who]}\\fs{fs}\\fad(120,180)}}{txt}\\N{{\\fs28\\bord3\\shad2\\fnNoto Sans CJK JP Bold}}{EN[txt]}")
open(OUT, "w").write(head + "\n".join(rows) + "\n")
print(f"字幕 {len(ev)} 行 → {OUT}")
for e in ev[:6]: print(f"  {e[0]:6.2f}〜{e[1]:6.2f} {e[3]:4s} {e[2]}")
