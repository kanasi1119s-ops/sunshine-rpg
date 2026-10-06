# 金翼の天使（2頭身・16×32・4方向×3コマ）

2026-10-07、人間の指示「なんか4人作って。モンスターでもいいから」で作った2頭身ドット絵。**ゲームには入れていない。**

- 種類: 天使／性別: 男性／設定: 天の門で祈りを運ぶ天使
- イメージ画像: `ref.png`（Stable Diffusion 1.5、CreativeML OpenRAIL-M。人の形の下書き tall から img2img・強さ0.9、QUALITY=real、乱数の種 6137）
  - 指示文: full body shot of a male angel, short golden hair, white and gold robe, large white feathered wings, thin halo, highly detailed realistic dark fantasy character, intricate textures, cinematic lighting, dark fantasy concept art, plain white background
- ドット絵: 体は仲間の2頭身の型（女性はアヤメ、男性はレトの体）。**髪は仲間の髪型を使わず、`../heads.py` で1から描いた**
  （2026-10-07、人間の指示「髪の毛の感じが既存のドット絵に近いから気をつけて」）。羽・角・光輪・しっぽ・マントは `../chibi_parts.py`。
  作り方は `../make_four.py`。
- ドット絵エディタで 48×128（12コマ）を描き、食い違い 0 マスを確かめた（`sheet-editor.png`）。
- ファイル: `angel.walker.json`（ゲームの形式）、`sheet.txt`・`sheet.json`（エディタ用）、`sheet.png`・`sheet_x8.png`（縦: 下・上・左・右、横: 3コマ）、`walk.gif`
- 2026-10-07、人間の指示「天使と魔王手が動いてないんだよね」「最初のでいいや…右手の動きを左手と同じに」で、もとの型のまま、前・後ろ向きで止まっていたほうの手も、動いている手と同じ1ドットの上下で、左右反対（交互）に振るようにした（人間の指示「振り方は左右反対に」）（`../chibi_parts.py` の `swing_arms`）。横向きはもとの型のまま。
