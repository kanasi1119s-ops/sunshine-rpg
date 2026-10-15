# 歌声の道具（ボカロ曲づくり用。ゲームには入れない）

| 道具 | すること |
|---|---|
| `vocal-export.py` | 歌の旋律と歌詞（`_gen/*-vocal.py`）を OpenUtau のプロジェクト（.ustx）・MusicXML・歌詞カードに書き出す |
| `utau-render.py` | UTAU 音源（oto.ini つき）で実際に歌わせて WAV にする（連続音でつなぎ、歌い出しは単独音、フレーズ終わりは「a R」。WORLD で高さと長さを変える） |
| `vocal-mix.py` | 歌と伴奏を混ぜて仕上げる（ボーカルの EQ・コンプ・リバーブ・ディレイ → -13.5 LUFS） |

## 例（重音テト『なつぞら、かけだせ』）

```
VB=<音源フォルダ>/重音テト音声ライブラリー
python3 tools/vocal/utau-render.py assets-src/ai-songs/_gen/teto-natsu-vocal.py --vb "$VB/重音テト連続音" --head-vb "$VB/重音テト単独音" \
  --bpm 150 --out 歌.wav --cache <分析の置き場> --gain "8-24:0.85,24-32:0.92,56-64:0.85,64-72:0.92,88-96:0.78"
python3 tools/vocal/vocal-mix.py 伴奏.wav 歌.wav --out 完成.wav --bpm 150 --vocal-lu 2 --stems 完成
```
必要なもの: `pip install --break-system-packages pyworld pedalboard pyloudnorm`

## 確かめ方（耳の代わり）
- 音の高さ: 歌の WAV を WORLD で分析し、楽譜とのずれ（セント）を見る（初回: 中央値 2.3 セント、95% が 11 セント以内）。
- 言葉の聞き取りやすさ: faster-whisper（small）で文字起こしして歌詞と比べる。
- 音質: Audiobox Aesthetics（完成版 PQ 8.07）。

## 音源の決まり（重音テト音声ライブラリーの使用許諾条件、2011-04-01版）
- 非商用（営利目的でない同人活動を含む）なら無料。個人の楽曲投稿・同人CD・配信サイトでの有料配信・動画の広告収入は、公式ガイドラインで「商用にあたらない」とされている。
- **音源そのものの配布・販売は禁止**。だからリポジトリには入れない（作業用フォルダで使うだけ）。
- クレジットは必須ではないが、著作情報を偽らない。企業・レーベル経由の展開など商用は、事前に窓口（ピアプロ）へ問い合わせ。
- 出典: https://kasaneteto.jp/guidelines/voice.html 、音源同梱の「使用許諾条件.txt」
