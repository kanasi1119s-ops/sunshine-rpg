# パソコン（Windows）で、作曲ソフトのすべての曲を作れるようにする準備

2026-10-29 人間の指示「ケルト曲に限らず、全ての曲に対処できる様にして欲しい」。クラウドの作業場所（CPU 2個）より速く、同時に何曲も書き出すため。
ジャンル（ケルト・ジャズ・ラウド・J-POP・歌入り・ゲームの曲）を問わず、クラウドでできることをパソコンでもできるようにする。

## 1. リポジトリ
- https://github.com/kanasi1119s-ops/sunshine-rpg のブランチ `feat/composer-mixer`（作曲ソフトの最新はここ）
- 楽器の音源（`assets-src/soundfont/` の SF2/SF3・`assets-src/ir/` の残響・`assets-src/nam-models/` のアンプ）・環境音（`assets-src/ambience/`）はリポジトリに入っている

## 2. 入れるもの
| もの | 使い道 | 入れ方の例 |
|---|---|---|
| Git | リポジトリ | winget install Git.Git |
| Node.js 22 以上 | 作曲ソフト（tools/composer）・検査（*.mjs） | winget install OpenJS.NodeJS.LTS → リポジトリで `npm install` |
| Playwright の Chromium | 作曲ソフトが曲の音を作る（WAV 書き出し） | `npx playwright install chromium` |
| Python 3.11 | 曲の生成スクリプト（assets-src/ai-songs/_gen）・空気・検査・歌声 | winget install Python.Python.3.11 |
| Python の部品 | 下の一覧 | `py -3.11 -m pip install ...` |
| ffmpeg | mp3・動画・音の変換、検査 | winget install Gyan.FFmpeg |
| Audiobox Aesthetics のモデル | 音質の点数（PQ・CE・CU・PC） | はじめて動かしたときに自動でダウンロード（約1GB。HF_HOME の場所に置かれる） |

Python の部品: `numpy scipy soundfile librosa pyworld pyyaml onnxruntime torch torchaudio audiobox_aesthetics matplotlib`（torch は CPU 版でよい。GPU があれば CUDA 版）。パートに分ける道具（demucs）を使うときは `demucs`。

## 3. リポジトリに入っていないもの（規約で再配布できない。各自が公式から入手）
| もの | 置き場所 | 入手元 |
|---|---|---|
| 重音テト UTAU 音源（通常・弱・滑らか） | `assets-src/voicebanks/teto/重音テト音声ライブラリー/`（または環境変数 SUNSHINE_VOICEBANKS） | https://kasaneteto.jp/utau/ |
| 欲音ルコ DiffSinger Ver.2.00 | `assets-src/voicebanks/ds/ruko/` | https://long-sleeper.net/ |
| BigVGAN v2（44kHz・128band・512x） | `assets-src/voicebanks/ds/_vocoders/bigvgan-v2-44k/` | https://huggingface.co/nvidia/bigvgan_v2_44khz_128band_512x |
規約は docs/assets-credits.md。音源そのものは、リポジトリにもゲーム本体にも入れない。

## 4. 書き出しのしかた
- 作曲ソフト: `node tools/composer/song.mjs build <曲.json> --wav [音源・仕上げの設定] --out <出力>`（使い方は `node tools/composer/song.mjs guide`）
- 歌入り: 曲の JSON の "vocals" を、書き出しのときに `tools/singer/sing.py` が混ぜる
- 音質の点数: `python tools/audio-check/aes-score-lowmem.py <曲.wav>`
- ケルト100曲の流れ: tools/celtic100/README.md
- スクリプトの中の `/tmp/...` や `/home/claude/...` のような Linux の場所は、パソコンの作業場所（例 `C:\Users\<名前>\composer-work`）に置きかえる。bash のスクリプトは PowerShell か Node で書き直すか、Git Bash で動かす

## 5. 同時に何曲書き出すか
- 1曲あたり CPU 2個・メモリ 4GB が目安（Chromium が1つ、点数つけの AI が 2〜3GB）
- 論理プロセッサ数とメモリから同時の数を決める。点数つけは重いので、点数つけだけは同時に1〜2つまで

## 6. 動作の確認（クラウドの値と比べる）
- ケルト: 019（c100_019.py）→ PQ 7.35 前後
- 歌入りやバンドの曲も、それぞれ1曲書き出して、クラウドの点数と近いかを見る
