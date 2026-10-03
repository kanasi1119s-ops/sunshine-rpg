# 野ねずみの影（enc-touri-outskirts-2）

AIの下絵から作った絵（2026-10-04）。手順: AIの下絵 → ドット絵化（sfcize.py 96×96・20色） → 手直し（edits.py） → ドット絵エディタで描く（食い違い0マス）。

- 下絵: `draft.png`（Stable Diffusion 1.5、CreativeML OpenRAIL-M。置き場所の下書き layouts.py の `ground` から img2img、強さ0.9、QUALITY=real：DPM++ 24歩・cfg 7）
- 乱数の種: 2000
- 指示文: full body shot of a large wild field rat beast with shaggy dark brown fur, long tail, glowing amber eyes, small stone growths on its back, facing right, highly detailed realistic fantasy creature, intricate skin and fur texture, cinematic lighting, dark fantasy concept art, plain white background
- 避ける言葉: cartoon, clipart, flat colors, vector art, anime, chibi, cute, toy, plush, cropped, cut off, close-up, portrait, text, watermark, signature, frame, border, multiple creatures, blurry, deformed, extra heads
- 全身チェック（fullbody.py）: 全身OK
- 手直し: 光る琥珀色の目（2×2＋暗い眉）を足した。背中の白すぎる縁を薄い茶色に。
- 仕上げ: `final.txt`・`final.json`（ゲームの `enemy:enc-touri-outskirts-2`）、エディタで描いた画面 `final-editor.png`
