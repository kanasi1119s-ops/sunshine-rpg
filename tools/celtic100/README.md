# ケルト100曲「銀の笛と百の夜」の書き出しの流れ

1曲 = 4つの段階（クラウドでは /tmp/cel を作業場所にしていた。パソコンでは好きな場所に置きかえてよい）
1. 曲の設計図を作る: `python3 assets-src/ai-songs/_gen/c100_NNN.py <作業場所>/w/cNNN.json`（同時に cNNN.json.flags に書き出しの設定ができる。空気の設計図を書く曲は <作業場所>/w/airNNN.json も作る）
2. 音を作る: `node tools/composer/song.mjs build <作業場所>/w/cNNN.json --wav $(cat cNNN.json.flags) --out <作業場所>/out`（Playwright の Chromium を使う）
3. 空気（環境音・空間の層）を重ねる: `python3 assets-src/ai-songs/_gen/c100_air.py <out>/cNNN.wav <w>/airNNN.json <out>/cNNN.final.wav`
   - 空気の設計図の控えは assets-src/ai-songs/_gen/c100_air/airNNN.json（曲のスクリプトが自分で書く曲もある）
4. 検査: `python3 tools/celtic100/qc.py <out>/cNNN.final.wav`（音量の段差）と `python3 tools/audio-check/aes-score-lowmem.py <out>/cNNN.final.wav`（音質の点数 PQ。Audiobox Aesthetics）
   - 目標: 静の曲 PQ 7.2 以上、動の曲 7.8 以上。前奏が小さい・急に小さい所がないこと（chk.sh の表示）

点数（Audiobox Aesthetics）は、一度ダウンロードした重みを HF_HOME=/tmp/hf に置き、HF_HUB_OFFLINE=1 で読む（入れ物が替わったあと huggingface への接続が 403 で止まったため）。
run.sh / q.sh / chk.sh / next.sh はクラウド（Linux）で使っていた手順そのまま。パソコン（Windows）では、同じ流れを PowerShell か Node で書き直して使う。
同時に何曲書き出すかは CPU の数で決める（1曲あたり CPU 1〜2個・メモリ 3〜4GB が目安）。

## パソコンへの保存待ち（つながっていない間に完成した曲。SendUserFile の file_uuid）
（いまは無し。007・013 は 2026-11-01 に保存済み）
