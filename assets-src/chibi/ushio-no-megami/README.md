# 潮と月の女神（2頭身・16×32・4方向×3コマ）

2026-10-07、人間の指示（「神に変えましょうか作るの。いったんでいいので」「64は細かすぎる 32×16で」）で作った、2頭身ドット絵の試し1体目。**ゲームには入れていない。**

- 種類: 神／性別: 女性／設定: 潮の満ち引きと月の光をつかさどる女神
- イメージ画像: `ref.png`（Stable Diffusion 1.5、CreativeML OpenRAIL-M。人の形の下書き tall から img2img・強さ0.9、QUALITY=real、乱数の種 5200）
  - 指示文: full body shot of a serene colossal goddess of tides and moonlight, long silver hair, flowing deep blue robes with pearl trim, crescent halo behind her head, huge imposing, highly detailed realistic dark fantasy deity, intricate textures, epic concept art, plain white background
- ドット絵: 仲間の2頭身の体（長い髪の型）をもとに、銀の髪・深い青のローブ・真珠のふち・三日月の光輪・真珠の杖・胸の前の光る潮の玉を描いた（`make.py`）。
  - イメージ画像は、青いローブ・光輪・合わせた手が実在の宗教の聖母の絵に近かったので、手は合わせず潮の玉を持たせ、光輪は三日月にした。
- ドット絵エディタで 48×128（12コマ）を描き、食い違い 0 マスを確かめた（`sheet-editor.png`）。
- ファイル: `ushio-no-megami.walker.json`（ゲームの形式）、`sheet.txt`・`sheet.json`（エディタ用）、`sheet.png`・`sheet_x8.png`（縦: 下・上・左・右、横: 3コマ）、`walk.gif`
