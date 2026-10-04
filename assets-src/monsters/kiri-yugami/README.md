# 予言の歪み（kiri-yugami、5章のボス）

AIの下絵から作った絵（2026-10-04）。手順: AIの下絵 → ドット絵化（sfcize.py 256×256・40色） → 手直し → ドット絵エディタで描く（食い違い0マス）。

- 下絵: `draft.png`（Stable Diffusion 1.5、CreativeML OpenRAIL-M。置き場所の下書き layouts.py の `tall` から img2img、QUALITY=real）
- 指示文: full body shot of a huge broken stone monolith monster, glowing pale blue carved letters, swirling bands of paper scraps, one great eye and many small eyes, mist, facing right, ...（prompts.json の boss の雛形）
- 手直し（`touchup.json`）: 頭の空洞に、大きな光る目（青白い光と白い芯）を直線ツールで描いた。お腹に光る文字も描いたが、人間の指示「おなかの文字はいらない」で消した。
- 動き（`anim.json`、`parts.json`）: 歩く8コマ・攻撃7コマ（`boss_anim.py`。考え方は `docs/design/pixel-animation-study.md`）。ゲームにはまだ入れていない。
- 製作の様子の動画は `tools/pixel-practice/editor-record.mjs` で作れる（BGM: 緋色の断章）。
