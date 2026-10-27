# BARジャズ50曲の動画の説明文（SCARLETと同じ形: 題名・紹介（和・英）・曲目と時間（和名 - 英名）・クレジット・ハッシュタグ・タグ）
# 使い方: python3 tools/mv/yt_description_barjazz.py <mp3のフォルダ> <出力txt>   （曲は「NN 曲名.mp3」。曲名と英名は bar_songs.py から）
import sys, glob, os, subprocess
sys.path.insert(0, "/home/claude/wt-mix/assets-src/ai-songs/_gen")
from bar_songs import SONGS
d, out_path = sys.argv[1], sys.argv[2]
files = sorted(glob.glob(os.path.join(d, "*.mp3")))
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def ts(t):
    t = int(t); h, m, s = t // 3600, t // 60 % 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
PAD = float(os.environ.get("PAD", "0"))   # つないだ動画では1曲ごとに映像と音の長いほうに合わせるので、少しずつ長くなる（BARジャズでは1曲あたり約0.103秒）
tl, acc = [], 0
for p in files:
    n = int(os.path.basename(p)[:2]); s = SONGS[n - 1]
    tl.append(f"{ts(acc)} {s['title']} - {s['en']}"); acc += dur(p) + PAD
h, m = int(acc // 3600), int(acc % 3600 // 60); N = len(files)
out = f"""【作業用BGM】琥珀色のバー・ジャズ 全{N}曲・約{h}時間{m}分 | 本物の楽器の録音音源 | Amber Bar Jazz - {N} Original Songs, {h}h {m}min

夜のバーのカウンターで、グラスの氷とウイスキーの香りとともに流れる、全{N}曲のオリジナル・ジャズです。
スウィング、バラード、ボサ・ノヴァ、ワルツ、タンゴ、ブルース、モードまで、曲ごとにちがう物語と編成でお届けします。
ピアノ、ウッドベース、ドラム、サックス、トランペット、ギター、ビブラフォンなど、実際の楽器の録音音源だけで演奏しています。作業・読書・おやすみ前のBGMにどうぞ。
{N} original jazz songs for a quiet night at the bar - swing, ballads, bossa nova, waltz, tango, blues and modal. Every track has its own story and lineup, played only with real recorded instruments: piano, upright bass, drums, saxophone, trumpet, guitar and vibraphone. Perfect for work, study, reading, or winding down.

■ 曲目 / Tracklist
""" + "\n".join(tl) + """

■ クレジット / Credits
作曲・編曲・演奏・映像: Sunshine Pixel Sound
すべてオリジナル曲です。 / All songs are original compositions.
音源 / Sound sources: Salamander Grand Piano（Alexander Holm、CC BY 3.0）、Naked Drums（CC BY 4.0）、Rubner Upright Bass sampled by D. Smolken（CC0）、Karoryfer Samples のギター・サックス（Weresax・Bear Sax）、VSCO 2 Community Edition（Versilian Studios）ほか
フォント: DotGothic16・Orbitron（SIL Open Font License）

#ジャズ #作業用BGM #BARジャズ #JazzBGM #BarJazz #SunshinePixelSound

■ タグ（YouTubeのタグ欄に貼る）
ジャズ, jazz, バー ジャズ, bar jazz, 作業用BGM, 作業用 ジャズ, BGM, 睡眠用BGM, 読書BGM, 勉強用BGM, オリジナル曲, ジャズ BGM, jazz bgm, relaxing jazz, smooth jazz, late night jazz, jazz piano, ウッドベース, サックス, スウィング, ボサノバ, ジャズバラード, ラウンジ, 大人の音楽, 全50曲, 4時間, 約4時間, Sunshine Pixel Sound
"""
open(out_path, "w", encoding="utf-8").write(out); print(out)
