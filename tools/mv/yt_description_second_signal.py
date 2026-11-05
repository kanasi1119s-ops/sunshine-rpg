# 説明文（前の動画と同じ形: 題名・紹介文（和・英）・曲目と時間（和名 - 英名）・クレジット・ハッシュタグ）
import subprocess, sys
rows = [l.rstrip("\n").split("\t") for l in open("/tmp/yt2/songs.tsv", encoding="utf-8")]
durs = [float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout) for p in sys.argv[1:]]
def ts(t):
    t = int(t); h, m, s = t // 3600, t // 60 % 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
PAD = float(__import__("os").environ.get("PAD", "0"))   # つないだ動画では1曲ごとに映像と音の長いほうに合わせるので、少しずつ長くなる
tot = sum(durs) + PAD * len(durs); acc = 0; tl = []
for (no, jp, en, gj, ge), d in zip(rows, durs):
    tl.append(f"{ts(acc)} {jp} - {en}"); acc += d + PAD
h, m = int(tot // 3600), int(tot % 3600 // 60)
out = f"""SECOND SIGNAL 全25曲・約{h}時間{m}分 | 歌：重音テト・歌詞つき（日本語・英語） | 25 Songs feat. Kasane Teto (JP/EN Lyrics)

重音テトの第2弾アルバム。ふたたび舞台に立ったテトが、歌詞ボードといっしょに歌う全25曲。
ノイズの中で君の声をさがす歌から、シャボン玉、深夜のメロンソーダ、最後の大合唱まで。25の新しい物語を、日本語の歌詞と英訳つきでどうぞ。
The second album by Kasane Teto: 25 brand-new original songs, each with its own story, shown with Japanese lyrics and English translations.

■ 曲目 / Tracklist
""" + "\n".join(tl) + f"""

■ クレジット / Credits
作詞・作曲・編曲・映像: Sunshine Pixel Sound
歌: 重音テト（UTAU） / Vocal: Kasane Teto (UTAU)
すべてオリジナル曲です。 / All songs are original compositions.
フォント: DotGothic16・Orbitron（SIL Open Font License）

#重音テト #KasaneTeto #UTAU

■ タグ（YouTubeのタグ欄に貼る）
重音テト, テト, Kasane Teto, Teto, UTAU, UTAUオリジナル曲, 合成音声, 歌声合成, オリジナル曲, 歌詞付き, 英訳付き, 歌詞 英語, 全25曲, 1時間44分, 第2弾, メドレー, 作業用BGM, 歌入り, SECOND SIGNAL, セカンド・シグナル, original song, lyrics, English lyrics, English subtitles, vocal synth, Japanese song, 25 songs, Sunshine Pixel Sound
"""
open("/tmp/yt2/SECOND SIGNAL 説明文.txt", "w", encoding="utf-8").write(out)
print(out)
