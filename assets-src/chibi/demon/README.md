# 紅髪の悪魔（2頭身・16×32・4方向×3コマ）

2026-10-07、人間の指示「なんか4人作って。モンスターでもいいから」で作った2頭身ドット絵。**ゲームには入れていない。**

- 種類: 悪魔／性別: 女性／設定: 契約を持ちかける悪魔
- イメージ画像: `ref.png`（Stable Diffusion 1.5、CreativeML OpenRAIL-M。人の形の下書き tall から img2img・強さ0.9、QUALITY=real、乱数の種 6174）
  - 指示文: full body shot of a female demon, long crimson hair, small black horns, black leather dress, bat wings, thin tail, highly detailed realistic dark fantasy character, intricate textures, cinematic lighting, dark fantasy concept art, plain white background
- ドット絵: 体は仲間の2頭身の型（女性はアヤメ、男性はレトの体）。**髪は仲間の髪型を使わず、`../heads.py` で1から描いた**
  （2026-10-07、人間の指示「髪の毛の感じが既存のドット絵に近いから気をつけて」）。羽・角・光輪・しっぽ・マントは `../chibi_parts.py`。
  作り方は `../make_four.py`。
- ドット絵エディタで 48×128（12コマ）を描き、食い違い 0 マスを確かめた（`sheet-editor.png`）。
- ファイル: `demon.walker.json`（ゲームの形式）、`sheet.txt`・`sheet.json`（エディタ用）、`sheet.png`・`sheet_x8.png`（縦: 下・上・左・右、横: 3コマ）、`walk.gif`
- 2026-10-07、人間の指示「悪魔と、エルフも、魔王と同じ手の動きにしてほしい」で、前・後ろ向きの両手を交互に上下させた（もとの型は片手が下がるだけだったので、反対の手を1ドット上げる。`../chibi_parts.py` の `swing_arms_ayame`）。
