# 坩堝の顎（鬼神）（god-3、8神のボス）

AIの下絵から作った絵（2026-10-04、人間の指示「神を作って」）。手順: AIの下絵 → ドット絵化（sfcize.py 256×256・40色。2026-10-04 に128×128から作り直し） → 手直し → ドット絵エディタで描く（食い違い0マス）。ゲームでもそのまま256×256（輪と目の2色を足して42色）（`boss:god-3`）。

- 下絵: `draft.png`（Stable Diffusion 1.5、CreativeML OpenRAIL-M。置き場所の下書き layouts.py の `big` から img2img、強さ0.9、QUALITY=real：DPM++ 24歩・cfg 7）
- 乱数の種: 2000
- 指示文: full body shot of a towering horned forge god of molten iron, a huge furnace jaw, heavy chains, a cracked glowing ring set in its chest, facing right, huge imposing, highly detailed realistic dark fantasy boss, intricate textures, dramatic rim lighting, epic concept art, plain white background
- 避ける言葉: cartoon, clipart, flat colors, vector art, anime, chibi, cute, toy, plush, cropped, cut off, close-up, portrait, text, watermark, signature, frame, border, multiple creatures, blurry, deformed, extra heads
- 全身チェック（fullbody.py）: 全身OK
- 手直し: 8神の共通の印として、頭の後ろに「欠けた光の輪」（砕けた灯の環の欠片を表す。金色の輪に2か所の欠けと小さな破片）を、体の後ろ（透明な所）にだけ描いた。
- 前の絵（手描きの図形の絵、`tools/pixel-art/guardians.mjs`）より重厚でリアルになったので置きかえた（`docs/decisions.md` 2026-10-04）。
