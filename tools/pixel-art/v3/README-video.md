# ドット絵を描く様子の「6倍速動画」を作る（インスタ用の縦動画）

`record-piece.mjs` が、ドット絵エディタ（`../editor.html`）をスマホ幅で開き、32×32の絵を1筆ずつ描く様子を録画して、6倍速の縦動画（1080×1920・H.264のMP4）にする。

```
# H.264対応のffmpegが必要（例: npm install ffmpeg-static → node_modules/ffmpeg-static/ffmpeg）
export FFMPEG=/path/to/ffmpeg
PACE=850 node record-piece.mjs yuri-front.mjs 01-yuri ./vid     # PACE=1筆ごとの待ち(ms)、SPEED=倍速(既定6)
```
- スプライトのモジュールは、`rows`（32行×32文字）と、任意で `pal`（文字→色）を export する。色は26色まで
- 録画にはマウスが映らないので、黄色い丸のカーソルを画面に重ねている
- 動画の長さは、1筆の待ち時間×筆数÷倍速。PACE=850・約250筆で、約45秒
- 作った動画をSNSに載せるのは、人間が行う（CLAUDE.md 1-2）
