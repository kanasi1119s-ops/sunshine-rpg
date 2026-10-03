# AIでドット絵の下絵を作る道具（試作、2026-10-03）

人間の判断（「AI生成もやってみよう」）で始めた試作です。記事「AIでドット絵を描く方法」（B4C、https://b4c.jp/making-pixelart-ai-gen/ ）の流れを、この作業環境（GPUなし・CPU 2コア・メモリ7GB）で動く形にしました。学んだことは `docs/design/pixel-art-ai-workflow-notes.md`。

## 流れ

1. **下絵を作る** `generate.py`
   - 画像生成AIで 512×512 の「ドット絵風」の画像を作る。
   - 指示文に `in pixelsprite style` を入れ、避けるもの（ぼかし・3D・グラデーション・文字など）を指定する。
2. **本物のドット絵に仕上げる** `pixelize.py`
   1. 背景を消す（四すみの色とつながった部分）
   2. 切り抜く
   3. マス目に合わせて縮める（1マスの平均。既定は長い辺48px）
   4. 減色する（既定12色）
   5. 半透明をなくす
3. **目で確かめて手で直す**
   - 既存作品に似ていないか（CLAUDE.md 1-1）
   - 色の数・欠け・形の崩れ
   - 直すのは人か Aseprite で。

```
pip install --break-system-packages torch --index-url https://download.pytorch.org/whl/cpu
pip install --break-system-packages diffusers transformers accelerate safetensors peft
MODEL=PublicPrompts/All-In-One-Pixel-Model python3 tools/pixel-art/ai-gen/generate.py tools/pixel-art/ai-gen/example-jobs.json
python3 tools/pixel-art/ai-gen/pixelize.py raw/*.png      # → px/*.png
python3 tools/pixel-art/ai-gen/pixelize.py --size 64 --colors 16 --rembg raw/*.png   # 戦闘の敵向け（64px・16色・AIで背景を切り抜く）
```

## 使っているモデルとライセンス

| モデル | ライセンス | 要点 |
|---|---|---|
| PublicPrompts/All-In-One-Pixel-Model（Stable Diffusion 1.5 を元にしたドット絵向けの追加学習） https://huggingface.co/PublicPrompts/All-In-One-Pixel-Model | CreativeML OpenRAIL-M | 生成物の商用利用は可。ライセンスの「使い方の制限」（違法・有害な用途など）を守る。**学習に使った絵の出どころは公開されていない** |
| latent-consistency/lcm-lora-sdv1-5（4〜6回の計算で絵を作る高速化） https://huggingface.co/latent-consistency/lcm-lora-sdv1-5 | openrail++ | 同上 |
| （候補）Onodofthenorth/SD_PixelArt_SpriteSheet_Generator（4方向の歩きキャラ） | Apache-2.0 | まだ試していない |

モデルの重みはリポジトリに入れていない（初回に Hugging Face から自動で取得される）。

## 注意（必ず守る）

- **既存作品に似た絵が出ることがある。**
  - 試作の8体のうち1体（キノコ）は、有名なゲームのキャラを連想させたので外した。
  - 学習に使った絵の出どころが分からないモデルなので、出てきた絵はすべて目で確かめる。
- **ゲームに入れる前に、人間の確認を受ける。** AIで作った絵であることは、`docs/assets-credits.md` と `manifest`（試作のフォルダの README）に記録する。
- 記事の筆者と同じく、**色の統一**がいちばんの課題。同じキャラの別のコマは、`pixelize.py` で同じパレットに合わせる（今後、パレットを指定できるように直す）。

## 背景の切り抜き（`--rembg`）

- 下絵に景色や地面が描かれたときは `--rembg` をつける。rembg（MITライセンス）と isnet-general-use モデル（Apache-2.0）で背景を消す。
- 入れ方: `pip install --break-system-packages rembg onnxruntime`。初回にモデル（約180MB）を GitHub から自動で取得する。
- **メモリに注意**: 7GBほどの環境では、絵の生成（generate.py）と同時に動かすとメモリ不足で止まる。生成が終わってから仕上げる。
- 減色は「見える画素」だけで色を選ぶように直した（背景の色でパレットをむだにしない）。外周に1ドットの余白を残す。
