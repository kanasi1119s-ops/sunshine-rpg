# 2頭身の歩くキャラ（16×32）を作るためのプロンプト

うちの仲間6人（ユーリ・レト・ミナ・ガイド・オルカ・アヤメ）の歩くキャラと同じ作りのキャラを、新しく作るときの頼み方。
`〈 〉` のところを書きかえて使う。作り方の中身は `field-character.md`。

## A. Claude（定期作業・Claude Code）に頼むとき

```
/make-art フィールド用キャラを1人作ってください。

人物: 〈名前〉（〈役割。例: 港町の見張りの青年〉）
見た目:
- 髪: 〈色と形。例: 黒に近い紺、少しはねた短髪〉
- 目: 〈色。例: 灰色〉
- 肌: 〈例: 日焼けした肌〉
- 服: 〈上着の色と形〉／〈下の色。ズボン・スカート・ワンピースなど〉／〈靴の色〉
- 目印の1色: 〈例: 襟とマフラーの赤〉
- 持ち物・飾り: 〈例: 背中の剣、腰のランタン、腕輪〉
イメージ画像: 〈あれば置き場所。なければ「なし」〉

作り方（仲間6人の歩くキャラと同じ作りにそろえる）:
- 16×32ドット、2頭身（頭が体の半分ほどの大きさ）。4方向（下・上・左・右）×3コマ（立ち・左足・右足）。
- 1ドットの暗い外周（真っ黒ではなく、その部分を暗くした色）。部位ごとに「地・影・光」の3段、光は左上から。
- 目は縦2ドットの点。ほおに薄い赤み、口は1〜2ドット。髪に暗いすじは入れない（つやは明るい点で）。
- 歩幅は小さめ（前後に1〜2ドット）。歩くコマで、腕を前後に1ドット振り、髪の先・布の端を1ドット揺らす。物を持った手は振らない。
- 飾りは細かく: 金具の光、宝石や灯りの白い1ドット、布のしわ、靴の折り返しまで描く。
- 全体で20色以内、背景は透明。
- ドット絵エディタで描いて「食い違い 0 マス」を確かめる。
- 有名なRPGの主人公・キャラに似ていないかを確かめる（色と飾りの組み合わせ）。似ていたら色を変える。

できたら、拡大した一覧（4方向×3コマ）・歩く動きのGIF・ゲーム用データ（WalkerData の JSON）を見せてください。ゲームへの組み込みは、見せてから決めます。
```

## B. 画像生成AI（ChatGPT・Gemini など）で下絵を作るとき

画像生成AIは、ドットの数や外周を正確には守れない。**下絵（色と形の見本）として使い**、仕上げは A の手順（型に色を当てはめてエディタで描く）で行う。

```
16×32ピクセルの、2頭身のドット絵キャラクターのスプライトシートを描いてください。
横に3コマ（立ち・左足を出す・右足を出す）、縦に4方向（正面・後ろ・左向き・右向き）、全部で12コマ。背景は透明か単色。

キャラクター: 〈例: 港町の見張りの青年。黒に近い紺の、少しはねた短髪。灰色の目。紺の上着に赤いマフラー、茶色のズボンとブーツ。背中に剣〉

絵の決まり:
- 大きな頭と小さな体の2頭身。目は縦長の小さな点、ほおに薄い赤み。
- 1ピクセルの暗い輪郭線（真っ黒ではなく、色ごとに暗くした色）。
- 部位ごとに3段の陰影、光は左上から。グラデーション・ぼかし・アンチエイリアスは使わない。
- 歩幅は小さめ。歩くコマでは、腕を前後に小さく振り、髪の先とマフラーの端が少し揺れる。
- 色は20色以内。90年代後半の家庭用ゲーム機のRPGのフィールドキャラのような、くっきりした作り。
- 既存のゲームや漫画のキャラクターには似せない。
```

英語で頼むとき（AIによっては英語のほうが守りやすい）:

```
A pixel art sprite sheet of a chibi (2-heads-tall) RPG field character, each frame 16x32 pixels.
3 columns (standing, left foot forward, right foot forward) x 4 rows (facing down, up, left, right), 12 frames total, transparent background.
Character: 〈a young harbor lookout, short slightly messy navy-black hair, gray eyes, navy jacket, red scarf, brown trousers and boots, a sword on his back〉.
Style: big head and small body, small vertical-dot eyes, light blush on cheeks, 1-pixel dark colored outline (not pure black),
3-tone cel shading per part with light from the top-left, no gradients, no anti-aliasing, no blur, under 20 colors,
short steps, arms swing slightly and hair tips and scarf ends sway one pixel while walking.
Original design, not based on any existing game or manga character.
```

## 書くときの注意

- 作品名・ゲーム名・作者名・既存のキャラの名前は書かない（CLAUDE.md 1-1）。「〜のような」と書くのは「年代・機種の雰囲気」までにする。
- 髪の色と目印の1色は、仲間どうしで重ならないようにする（並んだときに見分けられるように）。
