# 苔岩の子竜（2頭身のモンスター・32×32・右向き・待機3コマ）

2026-10-07、人間の指示「モンスターも1体作ってみて」で作った2頭身ドット絵。**ゲームには入れていない。**

- 種類: モンスター（龍）／性別: なし／設定: 苔むした岩場にすむ、小さな竜の子ども。頭と背中に石のとげが育つ
- イメージ画像: `ref.png`（Stable Diffusion 1.5、CreativeML OpenRAIL-M。地面の下絵 ground から img2img・強さ0.9、QUALITY=real、乱数の種 7300）
  - 指示文: full body shot of a small young rock dragon, stubby legs, big head, mossy grey stone scales, green moss on its back, small leathery wings, glowing amber gem on its forehead, facing right, highly detailed realistic fantasy creature, intricate skin texture, dark fantasy concept art, plain white background
  - 描けた絵には額の宝石は出なかったので、ドット絵にも入れていない（イメージ画像どおり）
- 2頭身で残した特ちょう: 苔の緑の体と模様／頭の上の灰色の石のとげ（冠のように並ぶ）／黒いアーモンド形の大きな目と石のまゆ／後ろへのびる灰色の羽（とげ3本）／長いしっぽと灰色の爪
- 大きさ: 32×32（人間の指示「64は細かすぎる」に合わせて、キャラと同じ高さにした）。14色
- コマ: 0 ふつう／1 体が1ドット下がる（足はそのまま）／2 羽が上がる。`idle.gif` は 0→1→0→2
- 作り方: `make.py`（部品をしっぽ・後ろ足・羽・体・前足・頭の順に置き、縁取りと陰影をつけてから、目・口・石のとげ・爪を1ドットずつ置く）
- ドット絵エディタで 96×32（3コマ）を描き、食い違い 0 マスを確かめた（`sheet-editor.png`）。
