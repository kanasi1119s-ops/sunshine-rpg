# メロコア曲「melocore-pluck-v2」の作り方（2026-10-12、人間が「保存」と言った版）

ギターはすべて弦モデルの `pluck-deepair`（`docs/sound/guitar-solo-guide.md`）。曲は 172BPM・164小節・約3分50秒。

## 保存したもの
| もの | 場所 |
|---|---|
| 曲の書き方（全パート） | `assets-src/ai-songs/_gen/melocore-pluck-v2.py` |
| 曲のデータ（出だしの和音つき／和音を抜いた本編） | `assets-src/ai-songs/melocore-pluck-v2.json` / `melocore-pluck-v2-main.json` |
| 出だしの和音を作る道具 | `tools/soundfont/intro-swell-synth.mjs` |
| タッピングを作る道具 | `tools/soundfont/tap-synth.mjs` |
| タッピングの音符（138音、BPM172、拍で開始・長さ） | `assets-src/ai-songs/melocore-tap-events.json` |
| 出だしを本編に重ねる道具 | `assets-src/ai-songs/_gen/melocore-splice-intro.py` |
| 目印（git タグ） | `melocore-intro-ok`（出だし）／`melocore-tapping-ok`（タッピング） |

## 出だし（最初の1回だけ弾いて、リバーブで引っ張る）
F#m を1回弾く → 頭の音は消して 1.4 秒でふくらませ、弦の減りは持ち上げて約5.5秒まで平らに → 長い残響（約7秒）と付点8分のエコー2回（減り方 0.6）→ 4小節目のスネア連打の終わりまで保つ。音量は −48dB から立ち上がり、平らな所は約 −29dB、バンドが入ると −16dB（約13dBの跳ね上がり）。

## タッピング（最後のサビ前の静かな部分、8小節）
- 和音 D → E → F#m → E を2回。A のキーで書いて 5 半音下げる。
- 1〜4小節目＝16分のアルペジオ（1拍4音）。5〜6小節目＝音域を変えた16分。7〜8小節目＝32分（1拍8音）。最後は G#（下げた後は D#）のベンド＋ビブラートの長い音でサビへ。
- 音の出し方: 8音1組の強弱（0.8, 0.62, 0.62, **1.0**, 0.62, 0.62, 0.75, 0.62）。叩く音（4音目）は明るく強く＋130Hz の「コツ」。ほかはやわらかい立ち上がり。音がつながるとき前の音は 30ms で止める。軽い残響。静かな部分は全体で約 −21dB。

## 作り直す手順
```
NOTAP=1 python3 assets-src/ai-songs/_gen/melocore-pluck-v2.py > /tmp/full.json     # タッピングを休みにした曲
# 和音のパート（role に「イントロの和音」）を抜いて本編にし、作曲ソフトで書き出す
node tools/composer/song.mjs build main.json --out out --wav --guitar pluck-deepair --bass pick --master-preset rock-clean
node --experimental-strip-types tools/soundfont/intro-swell-synth.mjs intro.wav        # 48kHz に変換して使う
python3 assets-src/ai-songs/_gen/melocore-splice-intro.py out/main.wav intro48.wav spliced.wav
node --experimental-strip-types tools/soundfont/tap-synth.mjs assets-src/ai-songs/melocore-tap-events.json tap.wav
# tap.wav を 48kHz にして、132 小節目（132×4×60/172 秒）に、全体が約 −21dB になる音量で重ねる
```

## 分かっている弱い点
- 出だしとタッピングは作曲ソフトの外で作った音で、曲データには入っていない。
- 作曲ソフトの音は、鳴ってから約0.75秒で音量が15dB落ちる（原因は未調査）。伸びが要る所は外で作る。
- 本編の継ぎ目は「要直し」。
