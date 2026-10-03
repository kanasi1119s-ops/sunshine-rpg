# モンスター（戦闘の敵・ボス）の作り方

目標: 大きくて陰影の重い、スーファミ後期の戦闘画面のような敵（特定の作品の敵には似せない）。質の要素は `docs/design/heavy-enemy-workflow.md` 第1節。

## 1. 何を描くか決める（指示文の中身）

英語で「種類＋色＋体の特徴＋持ち物・光る差し色」を1文で書く。名前だけ（"a salamander" など）にしない。

| よい例 | なぜよいか |
|---|---|
| `an ancient stone golem covered in moss with glowing blue runes` | 素材（石・苔）と差し色（青い紋様）が決まっている |
| `a giant armored crab monster with huge orange claws and barnacles` | 色と特徴的な部位がある |
| `a floating hooded specter in tattered blue robes holding a lantern` | 形（フード・ぼろの衣）と光（ランタン）がある |
| `an evil sorcerer in purple and gold robes with a skull staff, casting fire` | ボス向き。色の組み合わせと持ち物がある |
| `a huge horned war beast with shaggy dark mane and long ivory tusks` | 大きさと角・牙で迫力が出る |

- 章の舞台・属性に合わせる（`docs/story/` と `docs/design/` の敵の表を見る）。同じ地域の敵は、色の系統をそろえると群れに見える。
- 避ける: 作品名・ゲーム名・作者名、既存のモンスターの名前（"slime" など）、"cute"・"chibi"（重厚さが消える）。

## 2. 下絵を描く

```sh
cd <作業フォルダ>
python3 tools/pixel-art/ai-gen/make_jobs.py monster jobs.json \
  "golem:an ancient stone golem covered in moss with glowing blue runes" \
  "crab:a giant armored crab monster with huge orange claws and barnacles" --seeds 2
MODEL=stable-diffusion-v1-5/stable-diffusion-v1-5 VARIANT=fp16 STYLE=painterly \
  python3 tools/pixel-art/ai-gen/generate.py jobs.json      # → raw/golem_0.png ...
```
- ボスは `make_jobs.py boss ...`（128×128 用の指示文）。
- 1体につき2枚以上。使える形になるのは半分ほど。体が切れた・別の物になった・2体描かれた絵は捨てる。

## 3. ドット絵にする

```sh
python3 tools/pixel-art/ai-gen/sfcize.py raw/golem_0.png out/golem 96 20     # ボスは 128 24
```
出力: `golem.png`（確認用）・`golem.txt`（エディタ用の文字グリッド）・`golem.json`（パレット）。
（ブラウザで行うなら、ドット絵エディタの「画像から作る（重厚な敵）」が同じ処理。）

## 4. 見て、手直しする（ここで質が決まる）

4倍に拡大した画像を見て、`edits.py` で直す（`{"palette": {...}, "pixels": [[行, 列, "記号"]], "rects": [...], "erase": [[行0,列0,行1,列1,"消す記号"]]}`）。
1. **目**: 2ドットの光る目（中心に明るい1ドット）＋上に暗い眉の線。顔が分からない敵は、まずここ。
2. **口・牙**: 暗い横線＋明るい牙2本。
3. **背景の取り残し**: 足のあいだ・脇の下の背景色を消す（`erase`）。
4. **強すぎる色**: 鮮やかすぎる赤紫などは、彩度を3割落として少し暗く。
5. **差し色**: 光る紋様・宝石・炎を2〜5ドット足す。
6. 外周に黒一色の線が残っていないか（縁取りは「その部分の色を暗くした色」）。孤立した1ドットが無いか。
7. **似ていないかの確認**（SKILL.md の1）。似ていたら捨てる。

## 5. エディタで描いて確かめる

```sh
EDITOR=<保存したエディタのindex.html> node tools/pixel-practice/editor-draw.mjs out/golem_fix.txt out/golem_fix.json out/golem-editor.png --zoom 6
```
「食い違い 0 マス」を確かめる。並べて見る（暗い背景に、同じ地域の敵2〜3体と並べた見本を作る）。

## 6. 記録・ゲームへ

SKILL.md の4・5。ゲームの敵データへの組み込みは、`src/game/monster/` と `tools/pixel-art/export-game-data.mjs` の形（色番号の文字列＋パレット）に合わせる。
