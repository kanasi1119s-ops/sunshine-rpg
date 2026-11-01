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
- 026_小さな滝の祈り.mp3 → ffb6a648-13bd-4094-95e8-79830a881c17（2026-11-01 パソコンのつながりが切れていた）
- 027_鴨の親子.mp3 → f40161b8-9ca5-440a-9851-a52b580a9135
- 024_川辺の蛙たち.mp3 → 39f5fcc5-690d-4b13-ba41-f3d17b3856a7
- 023_水面の光.mp3 → d5479b65-ed7d-4663-8bcc-14e512d0b4a3
- 029_水が教える道.mp3 → 575b7c32-3dbe-458d-ac00-33cb5d121063
- 028_夕もやの川.mp3 → 563b2fed-215f-4511-8b86-324a3aaedd7b
- 030_水車の夜明け.mp3 → db773f04-3138-416b-bd63-37587605d0e7
- 032_木漏れ日.mp3 → 903c7e9b-6863-4d61-975e-4fbe705cb160
- 031_森の入口.mp3 → 62c679b8-bea1-4229-a9fd-026ac96d6317
