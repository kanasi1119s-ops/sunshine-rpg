# エディタで描いている様子を、自分のパソコンで見る

ドット絵エディタ（`../editor.html`）を実際のブラウザで開き、マウスの動きで絵が描かれていく様子をそのまま見られます。

## 手順（Windows / Mac 共通。Google Chrome が入っていること）
1. リポジトリを取得して、この場所に移動する: `cd tools/pixel-art/v2`
2. 一度だけ: `npm install playwright-core`
3. 実行: `HEADED=1 PACE=8 node live.mjs`
   - Windows のコマンドプロンプトでは `set HEADED=1 && set PACE=8 && node live.mjs`
   - Chrome の場所が違うときは `CHROME_PATH="Chromeのパス"` を足す
4. Chrome が開き、パレット設定 → 面積の大きい色から順に、マウスでなぞって描く様子が見られる（256×256は数十分かかる）
   - `PACE` は1筆ごとの待ち（ミリ秒）。大きいほどゆっくり。0で最速
5. 終わると `live-out/` に完成画面（`final-canvas.png`）と書き出しテキスト（`export.txt`）が残る

## 別の絵を描く
`node live.mjs ../editor.html ./別の部品.mjs ./出力フォルダ`（部品は `PIECES` を export するモジュール）
