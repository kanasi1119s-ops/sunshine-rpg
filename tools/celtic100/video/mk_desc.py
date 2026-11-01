# 「銀の笛と百の夜」全100曲の動画の説明文を作る（ケルト異世界ファンタジー・カフェジャズの説明文と同じ項目をすべて入れる）
#   タイトル行（英語を頭に）・日本語の紹介・英語の紹介・曲目（タイムスタンプ「和名 - English」）・楽器・クレジット・ハッシュタグ・タグ欄
#   使っている音源（VSCO 2 CE・FreePats・VCSL など CC0、FluidR3 は MIT）は表記の義務がないので書かない（2026-10-20 人間「入れなきゃいけない物だけ」）
# 使い方: python3 mk_desc.py <starts.txt（1行1曲の開始秒）> <全体の秒> <出力.txt>
import sys, os
starts_file, total_s, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
songs = [l.split("|") for l in open(os.path.join(HERE, "songs.txt"), encoding="utf-8").read().strip().splitlines()]
st = [float(x) for x in open(starts_file, encoding="utf-8").read().split()]
assert len(st) == len(songs) == 100
def ts(s):
    s = int(s); return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}"
h, m = int(total_s // 3600), int(total_s // 60 % 60)
total_ja = f"約{h}時間{m}分"
title = f"Silver Flute – A Hundred Nights of Celtic Fantasy Flute | 銀の笛と百の夜 ケルト幻想の笛 全100曲・{total_ja} | 作業用BGM・睡眠・読書"
ja = ("雲の海に浮かぶ島々。崖の上の古い鐘のそばで、ひとりの少女が銀の笛を吹く――。\n"
      "灯台の島を旅立った笛吹きの少女エイラが、百の夜をめぐって、止まった鐘を目覚めさせるまでの物語を、笛を主役にしたケルト音楽100曲でつづりました。\n"
      "ジグ・リール・ホーンパイプ・スロー・エアー・子守歌まで、1曲ずつ形も楽器も変えています。静かな曲から踊りたくなる曲まで、長く流しても飽きにくいので、作業や勉強、読書、眠る前のひとときにどうぞ。")
en = ("Islands floating on a sea of clouds. Beside an old bell on a cliff, a girl plays a silver flute.\n"
      "One hundred all-original Celtic fantasy tracks with the flute always in the lead, following Eira, a young flute player from a lighthouse island, "
      "across a hundred nights on her journey to wake a silent bell. Jigs, reels, hornpipes, slow airs and lullabies — every track has its own form and instruments. "
      "Gentle to lively, for working, studying, reading and drifting off to sleep.")
inst = ("フルート（全曲の主役）・竪琴・ナイロン弦ギター・フィドル・ビオラ・チェロ・コントラバス・アコーディオン・ティン・ホイッスル・ボーラン・ホルン・マリンバ・木琴・グロッケン・リードオルガン ほか\n"
        "Flute (lead on every track), harp, nylon guitar, fiddle, viola, cello, double bass, accordion, tin whistle, bodhrán, horn, marimba, xylophone, glockenspiel, reed organ and more")
txt = f"""{title}

{ja}
{en}

■ 曲目 / Tracklist
""" + "\n".join(f"{ts(t)} {n} {j} - {e}" for t, (n, j, e) in zip(st, songs)) + f"""

■ 楽器 / Instruments
{inst}

■ クレジット / Credits
作曲・編曲・映像: Sunshine Pixel Sound
Music, arrangement & animation: Sunshine Pixel Sound
すべてオリジナル曲です。 / All tracks are original compositions.

#ケルト音楽 #作業用BGM #フルート

■ タグ（YouTubeのタグ欄に貼る）
ケルト音楽, ケルト, ファンタジー, 異世界, フルート, 笛, 作業用BGM, 勉強用BGM, 読書用BGM, 睡眠用BGM, 集中, リラックス, 癒し, 竪琴, フィドル, アコーディオン, ジグ, リール, RPG, ゲーム音楽風, オリジナル曲, {h}時間, Celtic music, Celtic fantasy, fantasy music, flute music, Irish flute, study music, sleep music, reading music, relaxing music, harp, fiddle, RPG music, background music, BGM, Sunshine Pixel Sound
"""
open(out, "w", encoding="utf-8").write(txt)
print(txt[:600]); print("…文字数", len(txt))
