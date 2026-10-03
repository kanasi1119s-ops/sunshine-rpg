# フィールド用キャラ（マップを歩く人 16×32・4方向×3コマ）の作り方

目標: 王道のコマンドRPGのフィールドキャラのような、ひと目で役割が分かる2頭身のキャラ（特定の作品のキャラには似せない）。
形式はゲームの `WalkerData`（`src/game/sprite/walker-data.generated.ts`。palette と frames の `down0`〜`right2`）。決まりは `docs/design/pixel-character-guide.md`。

## 考え方: 「AIは色の設計図、形は型」

16×32 は小さすぎて、AIの絵を縮めると形がつぶれる。そこで:
1. AIに**正面の全身デザイン画**を描かせ、髪・肌・上着・下・靴・目印の**6色だけ**を取り出す（AIを使わず、6色を自分で決めてもよい）
2. 手描きの**型**（`field_templates.py`）に当てはめる。ほお・口・肩の光・服のしわ・ボタン・腰の袋・ひざと靴先の光も型が描き込む（目は縦2ドットの点のまま。髪に暗いすじは入れない＝人間の指示 2026-10-03）。型は、2頭身・1ドットの暗い外周・目は縦2ドット・部位ごとに3段の陰影（光は左上）・小さめの歩幅の4方向×3コマ。V字の襟・袖口・金のバックル・靴の折り返しが最初からつく
3. 髪型・服・飾りを組み合わせて、役割を描き分ける

## 1. 組み合わせを決める

| 選ぶもの | 選択肢 |
|---|---|
| 髪型 `--style` | `spiky` とがった短髪・`short` ふつうの短髪・`long` 長い髪・`hood` フード |
| 服 `--outfit` | `tunic` 上着＋ズボン・`coat` ひざまでの長い上着・`dress` ワンピース（下の色）・`robe` ローブ（上着の色） |
| 飾り `--deco`（カンマ区切り） | `band` はちまき（結び目つき）・`cape` マント・`backsword` 背中の剣・`sword` 手に剣・`shield` 盾・`helmet` 兜（ヘッドランプつき）・`staff` 杖（光る玉）・`scarf` マフラー・`goggles` ゴーグル・`twintails` ふたつ結び・`ponytail` ポニーテール・`circlet` 額の飾り・`bracelet` 光る腕輪・`pickaxe` 肩にかついだつるはし・`backpick` 背中に背負ったつるはし・`lantern` ランタン・`bow` 背中の弓（正面でも肩の後ろと腰の横に先がのぞく） |
| ひげ `--beard` | 年配の人物に |

役割の例（色は自由に変える）:
| 役割 | 組み合わせ |
|---|---|
| 剣士・兵士 | `short`＋`tunic`＋`helmet,sword,shield`（隊長なら `cape` も） |
| 旅の戦士 | `short` か `spiky`＋`tunic`＋`cape,backsword` |
| 魔法使い（年配） | `hood`＋`robe`＋`--beard`＋`staff` |
| 僧侶・巫女 | `long`＋`dress`＋`cape`（白・金・水色など） |
| 村の子ども・町の人 | `short` か `spiky`＋`tunic`（飾りなし、または `band`） |

**似ないように**: 有名なRPGの主人公を思わせる組み合わせ（例: 黒いとがった髪＋赤いはちまき＋白い服、紫のマント＋白いターバン）は避ける。色を1〜2か所変えるだけでも印象は変わる。並べて見て、うちの仲間・町の人どうしが見分けられるか（髪の色と、服の目印の1色）も確かめる。

## 1-2. イメージ画像があるとき

人間がイメージ画像（全身・顔の拡大）を用意したときは、その画像から6色を拾い、飾りで持ち物（腕輪・ランタン・弓・つるはしなど）を再現する。同じ画像から、全身の絵（256×256、`sfcize.py` と同じ処理。背景の切り抜きは rembg の `isnet-anime` がアニメ調の絵に強い）と顔のアイコン（128×128）も作る。

## 2.（AIでデザインするとき）デザイン画を描く

```sh
python3 tools/pixel-art/ai-gen/make_jobs.py field jobs.json \
  "boy:a village boy with messy brown hair, white shirt, blue vest, brown trousers and boots" \
  "priestess:a young priestess with long silver hair, white and gold robe, light blue sash" --seeds 2
MODEL=stable-diffusion-v1-5/stable-diffusion-v1-5 VARIANT=fp16 STYLE=painterly \
  python3 tools/pixel-art/ai-gen/generate.py jobs.json
```
頭や足が切れた絵、横向きの絵は使わない。

## 3. 型に当てはめる

```sh
# デザイン画から色を取り出す
python3 tools/pixel-art/ai-gen/field_sprite.py raw/boy_1.png out boy --style short --outfit tunic --deco band --rembg
# 色を自分で決める（デザイン画なし）
python3 tools/pixel-art/ai-gen/field_sprite.py - out knight --style short --outfit tunic --deco helmet,sword,shield,cape \
  --set hair=#6a4a2a --set skin=#f0c4a0 --set top=#4a5a8a --set bottom=#3a3a4a --set boot=#5a3a20 --set acc=#b02a2a
```
- **取り出した色は必ず確かめる**（`out/boy.compare.png`）。フード・ひげ・白い髪・マントがあると、部位の色を取り違えやすい（肌が青、髪が肌色など）。違っていたら `--set 部位=#rrggbb` で直す。直した色は `out/boy.colors.json` に残り、`--colors out/boy.colors.json` で作り直せる。
- 肌の影がオレンジに寄りすぎないよう、肌の色は自動で控えめな影になる。真っ黒に近い髪は、光の段が赤っぽくなりやすいので、少し明るい茶・紺にすると見栄えがよい。

## 4. 見て確かめる（`out/<名前>.sheet.png`。横: コマ0〜2、縦: 下・上・左・右）

- 4方向とも同じ人物に見えるか。正面と後ろで髪型・服がつながっているか。
- 歩きのコマで、足が交互に出ているか（大股になりすぎない）。
- 飾り（盾・剣・杖）が、どの向きでも持っている位置にあるか。
- 全体で20色以内か（うちの形式の上限は26色）。
- 新しい形（髪型・服・飾り）が必要になったら、`field_templates.py` に型を足す（左半分を書いて左右反転、横向きは右向きを書いて反転）。足したら、すべての組み合わせで12コマが16×32になることを確かめる。

## 5. エディタで描いて確かめる

```sh
EDITOR=<保存したエディタのindex.html> node tools/pixel-practice/editor-draw.mjs out/boy.sheet.txt out/boy.sheet.json out/boy-editor.png --zoom 7
```
48×128（12コマ）を1枚で描く。`--zoom 7` で「食い違い 0 マス」を確かめた（5以下ではずれた）。

## 5-2. 歩きの動き（人間の指示 2026-10-03）

歩きのコマ（1・2）では、型が自動で次のように動かす。新しい型を足すときも、この動きを入れる。
- **腕**: 出した足と反対の腕が前（手が1ドット上がる）、もう一方が後ろ（手が1ドット下がる）。剣・ランタン・肩のつるはし・盾を持った手は振らない。杖は、持った手といっしょに上下に動く（人間の指示 2026-10-04）。髪で隠れた腕は動かさない。
- **髪**: 男性の人物は揺らさない（`--still-hair`。人間の指示 2026-10-04）。女性・長い髪の人物では、長い髪は、コマ1で左の房、コマ2で右の房が内側へ1ドット揺れる。横向きは後ろ髪の先が後ろへなびく。ふたつ結びは房の先が上下に、ポニーテールは先が左右に揺れる。
- **布**: はちまきの端・マフラーの端は上へはためき、マントのすそは後ろへ広がる。
動きは1ドットまで（2ドット以上動かすと、16×32 ではがたついて見える）。

## 6. ゲームへ

`out/<名前>.walker.json` が `WalkerData` の形。`src/game/sprite/walker-data.generated.ts` の `WALKERS` に人物名をキーにして加え、`character-specs.ts` の `handKey` でその人物に結びつける（`walker-data.generated.ts` は今は `assets-src/pixel-practice/r19-walkers/export_walkers.py` が書き出しているので、加え方を変えるときは `docs/decisions.md` に書く）。SKILL.md の4・5も守る。
