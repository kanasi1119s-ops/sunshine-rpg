# 町の人（モブ）の2頭身ドット絵を、画像生成AIで作るためのプロンプト

2026-10-07、人間の指示「画像生成からこれに似たドット絵を作るプロンプトをつくろうか」。
「これ」= いまゲームで使っている町の人（`assets-src/npc-sprites/`、355種類。`claude/awesome-dirac-d8uu9z` ブランチ）。
仲間6人の歩くキャラの頼み方は `prompt-field-character.md`。こちらは **名前の無い町の人・脇役** 向け。

画像生成AIは、ドットの数・外周・コマの位置を正確には守れない。**下絵（色・形・持ち物の見本）として使い**、
仕上げは型（素体）に色を当てはめて、ドット絵エディタで描く（D）。

## いまの町の人の絵の特徴（プロンプトに書く中身）

| 項目 | 特徴 |
|---|---|
| 大きさ | 1コマ 16×32。2頭身（頭が全体の半分近く）。足もとは下から4行目あたり |
| 頭 | 丸くて大きい。髪は頭の上と左右をすっぽり包む帽子のような形。前髪は横一直線か、少しはねる |
| 顔 | 目は縦2ドットの暗い点を2つ、はなして置く。口は1ドット。肌は明るい1色＋影1色 |
| 体 | 頭より少し細い。上着（チュニック・コート・エプロン・ワンピース・ローブ）に、**襟元・スカーフ・帯の目立つ1色** |
| 縁取り | 1ドットの暗い外周（真っ黒ではなく、こげ茶・紺など、その色を暗くした色） |
| 陰影 | 部位ごとに2〜3段。光は左上。グラデーション・ぼかしなし |
| 小さな飾り | 金具・ボタンの明るい1ドット、腰の袋、靴の色、持ち物（杖・かご・帽子・ランタン） |
| 色 | 1人 16〜20色。髪・肌・上着・下・目印の色・靴の6系統 |
| 向きとコマ | 下・左・右・上 × 3コマ（立ち・左足・右足）。右向きは左向きの左右反転 |
| 歩き | 体が1ドット上下し、腕を前後に1ドット振る。スカートのすそ・髪の先が1ドット揺れる |

## A. ChatGPT・Gemini などで、1人の12コマを作るとき（日本語）

```
16×32ピクセルの、2頭身のドット絵キャラクターの歩行スプライトシートを描いてください。
横に12コマを1列に並べる（左から: 正面3コマ・左向き3コマ・右向き3コマ・後ろ向き3コマ。
各向きの3コマは「立ち・左足を出す・右足を出す」）。右向きは左向きを左右反転した絵。背景は透明か単色の緑。

キャラクター（RPGの町の人）: 〈例: 港町のパン屋のおかみさん。こげ茶のまとめ髪、白いエプロンに桃色のワンピース、
襟元に黄色いスカーフ、茶色の靴、腕にパンのかご〉

絵の決まり:
- 大きな丸い頭と小さな体の2頭身。髪は頭の上と左右を包む形で、前髪はまっすぐ。
- 目は縦2ドットの暗い点を2つ、口は1ドット。顔はシンプルに。
- 1ピクセルの暗い輪郭線（真っ黒ではなく、色ごとに暗くした色）。
- 部位ごとに2〜3段のくっきりした陰影、光は左上から。グラデーション・ぼかし・アンチエイリアスは使わない。
- 襟元・スカーフ・帯に、目立つ1色を入れる。金具やボタンに明るい1ドット。
- 歩くコマでは、体が1ドット上下し、腕を小さく前後に振る。〈スカート・長い髪なら: すそや髪の先が1ドット揺れる〉
- 色は20色以内。90年代の家庭用ゲーム機のRPGの町の人のような、やさしくくっきりした作り。
- 既存のゲームや漫画のキャラクターには似せない。文字・ロゴは入れない。
```

## A'. 同じ内容を英語で（AIによっては英語のほうが守りやすい）

```
A pixel art walking sprite sheet of a chibi (2-heads-tall) RPG townsperson, each frame exactly 16x32 pixels.
12 frames in one horizontal row: 3 facing down, 3 facing left, 3 facing right, 3 facing up
(each set: standing, left foot forward, right foot forward). The right-facing frames mirror the left-facing ones.
Transparent or flat green background.
Character: 〈a baker woman from a harbor town, dark brown hair in a bun, pink dress with a white apron,
yellow scarf at the collar, brown shoes, a basket of bread on her arm〉.
Style: big round head and small body, hair wraps the top and sides of the head like a cap with straight bangs,
eyes are two small vertical 2-pixel dark dots, 1-pixel mouth, simple face,
1-pixel dark colored outline (not pure black), 2-3 tone crisp cel shading per part with light from the top-left,
one bright accent color at the collar, scarf or sash, tiny 1-pixel highlights on buttons and metal,
walking frames bob the body by one pixel and swing the arms slightly〈, skirt hem and hair tips sway one pixel〉,
under 20 colors, no gradients, no anti-aliasing, no blur, no text, no logo.
Gentle, clean look of a 1990s home console RPG village. Original design, not based on any existing game or manga character.
```

## B. 町の人を何人もまとめて考えるとき（正面だけ・デザイン案）

```
16×32ピクセル・2頭身のドット絵で、RPGの町の人を10人、正面向きで横一列に並べてください（1人1コマ、背景は単色）。
全員、同じ体つき・同じ絵の決まり（A と同じ）で、服・髪型・色・持ち物だけを変えて、ひと目で役割が分かるように。
1. 漁師（つばの広い帽子・網）  2. パン屋の女将（エプロン・かご）  3. 灯守り（ランタン）  4. 宿屋の主人（前かけ・鍵）
5. 農夫（麦わら帽子・くわ）  6. 巡礼者（フードつきの外とう・杖）  7. 書記（めがね・本）  8. 渡し守（櫂）
9. 衛兵（かぶと・槍）  10. 子ども（大きな頭・短い手足）
色は1人20色以内。既存のゲームや漫画のキャラクターには似せない。
```
→ 役割は `assets-src/npc-sprites/index.json` の名前（宿屋の主人・灯守り・渡し守・巡礼者・書記・農夫など）から選ぶとよい。

## C. うちの画像生成（Stable Diffusion 1.5・`generate.py`）で下絵を作るとき

16×32 を直接は描けないので、**大きめの1枚絵（正面）でデザインを決め、色を拾う**。

- 指示文（`make_jobs.py character` に渡す。77トークン以内）:
  `full body chibi villager, two heads tall, front view, 〈baker woman, dark brown hair bun, pink dress, white apron, yellow scarf, bread basket〉, simple flat colors, clean outline, plain white background`
- 避ける言葉: `realistic, photo, text, watermark, multiple people, cropped, cut off, blurry`
- 使い方: 下絵から6色（髪・肌・上着・下・目印・靴）を拾い、D の型に当てはめる。

## D. 仕上げ（ゲームに入る形にする）

1. 型を選ぶ: いまの町の人の素体6種（`src/game/sprite/mob-walker-data.generated.ts` の `MOB_TEMPLATES`。
   作り方は `tools/pixel-art/export_mob_walkers.py`）から、体つきが近いものを選ぶ。合わなければ型を足す。
2. 色を当てはめる: 下絵から拾った6色を、型の役割（hair・skin・top・bottom・accent・shoes）に当てはめる。
3. 見て直す: 4倍以上に拡大した12コマの一覧と、歩く動きのGIF（1→0→1→2、1コマ0.2秒）で、
   4方向とも同じ人に見えるか・持ち物の位置・20色以内かを確かめる。
4. エディタで描く: ドット絵エディタで 192×32（12コマ）を描き、「食い違い 0 マス」を確かめる。

## 書くときの注意

- 作品名・ゲーム名・作者名・既存のキャラの名前は書かない（CLAUDE.md 1-1）。「〜のような」は「年代・機種の雰囲気」までにする。
- 町の人どうしで、髪の色と目印の1色ができるだけ重ならないようにする（並んだときに見分けられるように）。
- 主要キャラ（仲間6人）とまちがえないよう、町の人には仲間と同じ髪色＋同じ目印の色の組み合わせを使わない。
