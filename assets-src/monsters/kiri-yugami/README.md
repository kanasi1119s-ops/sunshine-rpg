# 予言の歪み（kiri-yugami、5章のボス）

AIの下絵から作った絵（2026-10-04）。手順: AIの下絵 → ドット絵化（sfcize.py 256×256・40色） → 手直し → ドット絵エディタで描く（食い違い0マス）。

- 下絵: `draft.png`（Stable Diffusion 1.5、CreativeML OpenRAIL-M。置き場所の下書き layouts.py の `tall` から img2img、QUALITY=real）
- 指示文: full body shot of a huge broken stone monolith monster, glowing pale blue carved letters, swirling bands of paper scraps, one great eye and many small eyes, mist, facing right, ...（prompts.json の boss の雛形）
- 手直し（`touchup.json`）: 頭の空洞に、大きな光る目（青白い光と白い芯）を直線ツールで描いた。お腹に光る文字も描いたが、人間の指示「おなかの文字はいらない」で消した。
- 動き（`anim.json`、部品の決まりは `rig.json`）: `boss_rig.py` で作る。レイヤーは 胴・左腕・右腕・左肩当て・右肩当て。歩く16コマ、攻撃は3種類（腕だけ・体ごと・両手）を各14コマ。考え方は `docs/design/pixel-animation-study.md`。ゲームにはまだ入れていない（仮）。
- 動きの版（`anim-versions/`、gz圧縮）: 1 腕が切れる版（付け根がまっすぐな切り口）／2 丸い関節版（付け根に丸い玉）／3 指先なおし版（内側の指・はなれた爪も腕に入れ、細い爪の先を残す。いまの `anim.json`）。
- 古い `parts.json` は、最初の `boss_anim.py`（体ごとゆがめる版）のもの。参考に残している。
- 製作の様子の動画は `tools/pixel-practice/editor-record.mjs` で作れる（BGM: 緋色の断章）。
