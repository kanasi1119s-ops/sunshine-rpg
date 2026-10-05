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

## 2. 下絵を描く（全身が入るように）

**人間の指示（2026-10-04）: 全身が入るように。** 文字だけで頼むと、体が端で切れたアップの絵になりやすい（最初に試した神・悪魔・キメラなどは15枚中14枚が切れていた）。原因は2つ:
- 指示文はCLIPの**77トークンまで**しか効かない。後ろに書いた「全身」「白い背景」が切り捨てられていた → `make_jobs.py` は「full body shot of」を先頭に付け、77をこえたら止まる。説明は1文・20語ほどに。
- 速く描く設定（LCM、cfg 1.5）では、指示文の「全身」や避ける言葉がほとんど効かない → **置き場所の下書き**（`layouts.py`）から描く。白い背景のまん中に、ぼかした影絵（形・色・左上からの光）を置き、それを元にAIが描く（img2img、強さ0.9）。AIは影絵の位置と大きさを守るので、全身が入り、まわりに余白が残る。

ふだんは名簿の道具で行う（名簿に `prompt`・`shape`・`tone` を書いてから）:
```sh
python3 tools/pixel-art/ai-gen/monster_batch.py next 4
python3 tools/pixel-art/ai-gen/monster_batch.py draft <ID>... --seeds 3   # 生成 → 全身チェック → 見比べ用の1枚
python3 tools/pixel-art/ai-gen/monster_batch.py extend <ID> <番号>       # 形はよいのに端で切れたもの → 外側を描き足す（x<番号>）
python3 tools/pixel-art/ai-gen/monster_batch.py pick <ID> <番号> [--mirror]   # 全身OKのものだけ選べる
```
| shape（形） | 向いているもの |
|---|---|
| ground | 4本足の獣・虫（頭は右） |
| float | 霊・目玉・くらげなど宙に浮かぶもの |
| tall | 人型・鎧・悪魔・木の怪物など2本足で立つもの |
| long | 蛇・ミミズ・とかげなど低く長いもの |
| winged | 鳥・こうもり・羽虫など羽を広げたもの |
| big | ゴーレム・機械・ボスの巨体（ボスの既定） |

- `tone` は体のおおまかな色 `[r,g,b]`。暗すぎ・鮮やかすぎにしない（AIがその色をそのまま平らに塗ってしまう。中くらいの明るさ・少しくすんだ色）。
- 見比べ用の1枚には、下絵ごとに「全身OK」（緑）か「切れ:上下」「ばらばら」（赤）が出る（`fullbody.py`: 体と絵の端のあいだに2%以上の余白、体のかたまりが85%以上、額縁やポスターのような四角い絵になっていない）。`extend` は、端が白い背景なら白い余白を足すだけ、体がはみ出していればAIで外側を描き足す。**赤の下絵は使わない**（`pick` も止める）。
- 1体につき3枚ほど描いて、全身OKの中から、形がくずれていない・既存作品に似ていないものを目で選ぶ。顔が左向きなら `--mirror`。
- 手で行うとき: `make_jobs.py monster jobs.json "名前:説明"` のあと、jobs.json の各行に `"layout": {"shape": "ground", "tone": [110,100,95], "strength": 0.9}` を足して `QUALITY=real MODEL=stable-diffusion-v1-5/stable-diffusion-v1-5 VARIANT=fp16 STYLE=painterly python3 generate.py jobs.json`。
- **リアルな下絵**（人間の指示、2026-10-04「もっとリアルな下絵がいい」）: `monster_batch.py` は `QUALITY=real` で描く（速く描く設定 LCM を使わず、22〜24歩・cfg 7）。LCMでは細かさと「リアル」「避ける言葉」が効かず、クリップアートのような平らな絵になっていた。指示文の雛形も「highly detailed realistic fantasy creature, intricate ... texture, cinematic lighting」にした。
- 1枚 約5分（CPU 2コア。LCMなら2分だがリアルにならない）。生成と、全身チェック（rembg）・エディタ（ブラウザ）は同時に動かさない（`monster_batch.py` は順番に動かす）。
- 下絵がふつうの動物に寄りすぎたら、指示文を変えて描き直す。**下絵に無い目を手直しで無理に足さない**（2026-10-05、人間の指示「雑魚モンスターに無理に目をつけないで」）。

## 3. ドット絵にする

```sh
python3 tools/pixel-art/ai-gen/sfcize.py raw/golem_0.png out/golem 96 20     # ボスは 256 40（256×256で直接作る。手直しの点や輪も256の大きさで）
```
出力: `golem.png`（確認用）・`golem.txt`（エディタ用の文字グリッド）・`golem.json`（パレット）。
（ブラウザで行うなら、ドット絵エディタの「画像から作る（重厚な敵）」が同じ処理。）

## 4. 見て、手直しする（ここで質が決まる）

4倍に拡大した画像を見て、`edits.py` で直す（`{"palette": {...}, "pixels": [[行, 列, "記号"]], "rects": [...], "erase": [[行0,列0,行1,列1,"消す記号"]]}`）。
1. **目は足さない**: 下絵に描かれていない目・光る点を無理に足さない（2026-10-05、人間の指示）。顔が分からない絵は、手直しでごまかさず描き直す。
2. **口・牙**: 暗い横線＋明るい牙2本。
3. **背景の取り残し**: 足のあいだ・脇の下の背景色を消す（`erase`）。
4. **強すぎる色**: 鮮やかすぎる赤紫などは、彩度を3割落として少し暗く。
5. **差し色**: 足すのは、下絵にもともとある部分（光る紋様・炎など）をはっきりさせるときだけ。
6. 外周に黒一色の線が残っていないか（縁取りは「その部分の色を暗くした色」）。孤立した1ドットが無いか。
7. **似ていないかの確認**（SKILL.md の1）。似ていたら捨てる。

## 5. エディタで描いて確かめる

ボス（256×256）は `--zoom 6 --wide --import` で描く（1体 数十秒）。40色を超えても、エディタは62色まで扱える。ゲームの絵は27色以上だと別の書き方（`~色番号:数,...`）になり、`monster_batch.py export` が自動で選ぶ。

```sh
node tools/pixel-practice/editor-draw.mjs out/golem_fix.txt out/golem_fix.json out/golem-editor.png --zoom 6
```
「食い違い 0 マス」を確かめる。並べて見る（暗い背景に、同じ地域の敵2〜3体と並べた見本を作る）。

## 6. 記録・ゲームへ

SKILL.md の5・6。ゲームの敵データへの組み込みは、`src/game/monster/` と `tools/pixel-art/export-game-data.mjs` の形（色番号の文字列＋パレット）に合わせる。
