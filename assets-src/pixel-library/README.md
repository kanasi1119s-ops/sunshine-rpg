# ドット絵ライブラリ（500枚・素材置き場）

RPGを作るときに使える・参考にできるドット絵を500枚集めたものです（2026-09-30、人間の依頼で用意）。
**まだゲームには1枚も使っていません。** ゲームに入れるときは、下の「ゲームに入れるとき」を守ってください。

- 1枚ずつの出典・作者・規約: [`MANIFEST.md`](MANIFEST.md)（表）と `manifest.csv`（同じ内容の表計算用）
- 縮小一覧（どんな絵かを一目で見る用。素材ではない）: `_preview/`
- 規約の写し: `LICENSES/`（ぴぽやの readme、Kenney の License.txt）
- 2回目に選んだ別の500枚: `../pixel-library-2/`
- この一覧に入れていない、先に取り込んだぴぽやの10枚: `../pipoya/charachip/`・`../pipoya/simpleenemy/`（同じ絵を2つ置かないため、こちらには入れていない）

## 分類と枚数

| フォルダ | 中身 | 枚数 |
|---|---|---|
| `01-characters/` | 主人公・仲間・町の人・王族・兵士・動物・顔グラフィック | 159 |
| `02-monsters/` | ふつうの敵（スライム・ゴブリン・おばけ・骸骨・ゾンビ・悪魔など） | 101 |
| `03-bosses/` | ボス向き（魔王・骸骨王・竜・ゴーレム・大魔導士など） | 37 |
| `04-field/` | フィールドのタイル（草・土・水・森・花・崖・ワールドマップ用） | 68 |
| `05-maps/` | 組み上がったマップ（ワールドマップ・町・ダンジョン・屋内の見本） | 20 |
| `06-dungeon/` | ダンジョン・洞窟・城・墓地のタイルと仕掛け | 34 |
| `07-town-indoor/` | 町の建物・壁・屋根・屋内の家具 | 33 |
| `08-objects-items/` | 宝箱・光・炎・影・乗り物（飛空艇・船）・アイテム・武器 | 48 |
| 合計 | | **500** |

配布元の内訳: ぴぽや倉庫 235枚、OpenGameArt（CC0）250枚、Kenney（CC0）15枚。

## 規約（すべて無料・商用利用可・ゲームへの組み込み可）

- **CC0（OpenGameArt・Kenney）**: 著作権を放棄したパブリックドメインの扱い。商用利用・加工・再配布・ゲームへの組み込みは自由で、クレジットも不要（お礼として書くのはよい）。
- **ぴぽや 無料素材利用規約**（https://pipoya.net/sozai/terms-of-use/ 、2026-09-30 に原文を確認。生成AI・AI学習についての記述はなし）: 営利・非営利を問わず利用可、加工可、ゲームに組み込んでの配布・販売可、クレジット・連絡は不要。**禁止: 素材そのもの（加工したものも含む）を素材として販売すること。** 無償で再配布するときは規約とともに配る（そのため `LICENSES/pipoya/` に同梱の readme を置き、`../pipoya/LICENSE-pipoya.md` に要点を書いている）。
- 「ぴぽやキャラチップ32出力素材」には readme が入っていないため、サイトの無料素材利用規約と、素材ページの説明（「そのまま直ぐに使用可能」）で確認した。
- **このフォルダの絵を、素材として販売・再配布しないこと。**

## 選び方（何を確かめたか）

1. 規約: OpenGameArt は各ページを 2026-09-30 に読み直し、ライセンス欄が CC0 だけのものに限った。Kenney は各パックの License.txt（CC0）を確認。ぴぽやは規約ページと同梱の readme を確認。
2. 既存作品のまね（`CLAUDE.md` 1-1）: 説明文の全文を読み、既存のゲーム名・「〜風」「〜にインスパイア」などを検索した。**次のものは外した**: 既存作品に寄せたと書かれたもの（有名RPGに影響を受けたタイルなど）、**作者の公開済みゲームで使われた絵**（1-1 を厳しめに解釈）、既存のTRPGの魔物を元にしたもの、ツクールの標準素材を含むもの、有名ゲームの画像そのもの（Dungeon Crawl の画像など）。
3. AI: 説明文に生成AI・画像変換AI（例: DeepStyle）を使ったとあるものは外した。
4. ドット絵か: 色数・半透明の割合を数え、縮小一覧を目で見て、なめらかな絵（3D風・絵の具風）、透かし文字・ロゴ・説明の文字が入ったもの、単色だけの帯を外した。
5. 2026-09-30 の見直し（2回目の500枚を選ぶときに説明文を読み直した）: 既存のゲーム（Stendhal）のために作られた絵（ノーム2枚・たる1枚）と、既存のゲームの品物の名前をもじった絵（Eye of Sender）の計4枚と、元の作者でない人が上げた絵（大きなスライム。由来があいまい）1枚を外し、ぴぽや2枚・OpenGameArt 3枚に差し替えた。
6. 重複: 同じ中身のファイルは1つにした（既存の `assets-src/` とも比べた）。色違いが多いセット（ぴぽやの魔物・シンボルエネミー・オートタイルなど）は間引いた。

## 手を加えたもの（ほかはすべて配布元のファイルのまま、名前だけ変えた）

- `pipoya-basechip-*`（`pipoya-basechip-all` 以外）: ぴぽやの基本マップチップ（8列×249段）を、場面ごと（フィールド・町の外・壁と屋根・屋内・ダンジョン・壊れた町・雪の町）に横長のまま切り分けた。
- `05-maps/pipoya-worldmap-sample-a/b`: ぴぽや「フィールドマップセット１」のタイルとオートタイルを、このプロジェクトで並べて組み立てたワールドマップの見本（素材の加工。規約で認められている）。
- `05-maps/kenney-*-sample`・`oga-grass-biome-map2`・`oga-tiny-forest-map`: 配布元に入っている Tiled のマップデータを、1倍の大きさで絵に描き出した（見本画像に入っているロゴや説明の文字を避けるため）。
- `oga-mummy-boss`・`oga-pixel-dragon`: 背景の単色（マゼンタ）を透明にし、余白を切った。

## ゲームに入れるとき（必ず守る）

- ゲームに使う絵を決めたら、`docs/assets-credits.md` の「使用中の素材」に、どの絵をどこで使ったかを書き足す。
- **絵柄をそろえる。** 配布元ごとに大きさ（8・16・24・32ドット）、色数、影のつけ方がばらばら。1つの画面に混ぜると浮くので、作品全体でどの系統に合わせるかを先に決める（`docs/design/pixel-art-notes.md` のチェックリストも見る）。
- ぴぽやの絵は、やわらかい影のために半透明の画素や多くの色を使っている。今のゲームは1枚26色までのデータ形式なので、地形と同じように色を減らしてから取り込む（`tools/pixel-art/import-pipoya.mjs` が手本）。
- マップを歩くキャラクターの大きさは、まだ人間が決めていない（案A 16×24／案B 16×32／案C 16×16。`docs/design/pixel-character-guide.md` の第7節）。32×32のキャラチップをそのまま使うかどうかも、その判断に合わせる。
- 主人公や仲間など物語の中心の人物は、配布素材をそのまま使わず、オリジナルのデザインにするのがおすすめ（使う場合は人間に確かめる）。
- 容量: この置き場はゲームの `dist/` には入らない。ゲームに入れる分だけを変換して取り込み、`npm run build` の容量チェック（128メガビット）を確かめる。

## 配布元の一覧

| 配布元 | 素材 | 作者 | 規約 | 枚数 |
|---|---|---|---|---|
| ぴぽや倉庫 | [RPGキャラ基本セット（キャラチップ.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 51 |
| ぴぽや倉庫 | [その他キャラチップ（キャラチップ＋.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 12 |
| ぴぽや倉庫 | [ぴぽやキャラチップ32出力素材（ぴぽや32×32 出力画像＋α）](https://pipoya.net/sozai/assets/charachip/character-chip-2/) | ぴぽや | ぴぽや 無料素材利用規約 | 101 |
| ぴぽや倉庫 | [ウディタ２用マップセット（ウディタ2_32x32mapchip_20210215.zip）](https://pipoya.net/sozai/assets/map-chip_tileset32/) | ぴぽや | ぴぽや 無料素材利用規約 | 38 |
| ぴぽや倉庫 | [シンプルエネミーシンボル32×32キャラチップ（pipo-simpleenemy01.zip の「４方向」）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 5 |
| ぴぽや倉庫 | [ハロウィン向け32×32キャラチップ26種セット（halloweenchara2016.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 24 |
| ぴぽや倉庫 | [フィールドマップセット１・同 追加パーツ（元ファイルは assets-src/pipoya/）](https://pipoya.net/sozai/assets/map-chip_tileset32/) | ぴぽや | ぴぽや 無料素材利用規約 | 2 |
| ぴぽや倉庫 | [飛空艇２種（pipo-airship01.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 2 |
| Kenney | [1-Bit Pack](https://kenney.nl/assets/1-bit-pack) | Kenney | CC0 1.0 | 2 |
| Kenney | [Micro Roguelike](https://kenney.nl/assets/micro-roguelike) | Kenney | CC0 1.0 | 1 |
| Kenney | [Monochrome RPG](https://kenney.nl/assets/monochrome-rpg) | Kenney | CC0 1.0 | 1 |
| Kenney | [Roguelike Caves & Dungeons](https://kenney.nl/assets/roguelike-caves-dungeons) | Kenney | CC0 1.0 | 1 |
| Kenney | [Roguelike Characters](https://kenney.nl/assets/roguelike-characters) | Kenney | CC0 1.0 | 1 |
| Kenney | [Roguelike Indoors](https://kenney.nl/assets/roguelike-indoors) | Kenney | CC0 1.0 | 1 |
| Kenney | [Roguelike RPG Pack](https://kenney.nl/assets/roguelike-rpg-pack) | Kenney | CC0 1.0 | 3 |
| Kenney | [Tiny Battle](https://kenney.nl/assets/tiny-battle) | Kenney | CC0 1.0 | 1 |
| Kenney | [Tiny Dungeon](https://kenney.nl/assets/tiny-dungeon) | Kenney | CC0 1.0 | 2 |
| Kenney | [Tiny Ski](https://kenney.nl/assets/tiny-ski) | Kenney | CC0 1.0 | 1 |
| Kenney | [Tiny Town](https://kenney.nl/assets/tiny-town) | Kenney | CC0 1.0 | 1 |
| OpenGameArt | [1-Bit Doomgeon Kit](https://opengameart.org/content/1-bit-doomgeon-kit) | B77345-100 | CC0 1.0 | 5 |
| OpenGameArt | [1-Bit Doomsphere Charset](https://opengameart.org/content/1-bit-doomsphere-charset) | B77345-100 | CC0 1.0 | 1 |
| OpenGameArt | [16 x 16 Monster Items](https://opengameart.org/content/16-x-16-monster-items) | ARoachIFoundOnMyPillow | CC0 1.0 | 4 |
| OpenGameArt | [16x16 8-bit RPG character set](https://opengameart.org/content/16x16-8-bit-rpg-character-set) | devurandom | CC0 1.0 | 1 |
| OpenGameArt | [16x16 base sprites](https://opengameart.org/content/16x16-base-sprites) | Unnamed | CC0 1.0 | 2 |
| OpenGameArt | [16x16 Puny World Tileset](https://opengameart.org/content/16x16-puny-world-tileset) | Shade | CC0 1.0 | 1 |
| OpenGameArt | [16x16 tileset: water, grass and sand](https://opengameart.org/content/16x16-tileset-water-grass-and-sand) | Demetrius | CC0 1.0 | 1 |
| OpenGameArt | [2D Spider Animated](https://opengameart.org/content/2d-spider-animated) | SpinachChicken | CC0 1.0 | 1 |
| OpenGameArt | [32x32 colorful slimes!](https://opengameart.org/content/32x32-colorful-slimes) | AndHeGames | CC0 1.0 | 1 |
| OpenGameArt | [32x32 pixel art creatures volume 3](https://opengameart.org/content/32x32-pixel-art-creatures-volume-3) | AndHeGames | CC0 1.0 | 1 |
| OpenGameArt | [4 Colour Interior Tileset](https://opengameart.org/content/4-colour-interior-tileset) | stealthix | CC0 1.0 | 1 |
| OpenGameArt | [4 Colour Overworld Tileset](https://opengameart.org/content/4-colour-overworld-tileset) | stealthix | CC0 1.0 | 1 |
| OpenGameArt | [8-bit JRPG tilesets](https://opengameart.org/content/8-bit-jrpg-tilesets) | Hollyhart1 | CC0 1.0 | 2 |
| OpenGameArt | [8bit rpg hero](https://opengameart.org/content/8bit-rpg-hero) | danbu | CC0 1.0 | 1 |
| OpenGameArt | [8x8 8-bit Styled Desert Tileset](https://opengameart.org/content/8x8-8-bit-styled-desert-tileset) | ImpossibleRealms | CC0 1.0 | 1 |
| OpenGameArt | [8x8 Critter Pack](https://opengameart.org/content/8x8-critter-pack) | patvanmackelberg | CC0 1.0 | 1 |
| OpenGameArt | [a many-eyed monster](https://opengameart.org/content/a-many-eyed-monster) | ArVexi1050 | CC0 1.0 | 1 |
| OpenGameArt | [Bountiful Bits 10x10 Top-Down RPG Tiles](https://opengameart.org/content/bountiful-bits-10x10-top-down-rpg-tiles) | VEXED | CC0 1.0 | 1 |
| OpenGameArt | [bushes](https://opengameart.org/content/bushes-2) | SpiderDave | CC0 1.0 | 1 |
| OpenGameArt | [Bushly and Princess Sera](https://opengameart.org/content/bushly-and-princess-sera) | GrafxKid | CC0 1.0 | 1 |
| OpenGameArt | [Cave tile map image](https://opengameart.org/content/cave-tile-map-image) | mieki256 | CC0 1.0 | 1 |
| OpenGameArt | [Chinese Green Dragon](https://opengameart.org/content/chinese-green-dragon) | Pixel Archer | CC0 1.0 | 1 |
| OpenGameArt | [Chipsets from NeoWolf](https://opengameart.org/content/chipsets-from-neowolf) | alv90 | CC0 1.0 | 4 |
| OpenGameArt | [Classic Hero](https://opengameart.org/content/classic-hero) | GrafxKid | CC0 1.0 | 1 |
| OpenGameArt | [Classic hero and baddies pack](https://opengameart.org/content/classic-hero-and-baddies-pack) | GrafxKid | CC0 1.0 | 1 |
| OpenGameArt | [Clouds](https://opengameart.org/content/clouds) | Igor Gundarev | CC0 1.0 | 1 |
| OpenGameArt | [Dawngeon](https://opengameart.org/content/dawngeon) | pebonius | CC0 1.0 | 1 |
| OpenGameArt | [DB32 Cave tileset](https://opengameart.org/content/db32-cave-tileset) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Demonic chest](https://opengameart.org/content/demonic-chest-0) | carnageddon | CC0 1.0 | 1 |
| OpenGameArt | [Desert Forest](https://opengameart.org/content/desert-forest) | LLGD | CC0 1.0 | 1 |
| OpenGameArt | [Desert village](https://opengameart.org/content/desert-village) | Skab | CC0 1.0 | 1 |
| OpenGameArt | [Devolution Topdown tilesets and sprites](https://opengameart.org/content/devolution-topdown-tilesets-and-sprites) | Brosnya | CC0 1.0 | 1 |
| OpenGameArt | [Diamond Axe (with degradation progress)](https://opengameart.org/content/diamond-axe-with-degradation-progress) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Dragon 1 (M484)](https://opengameart.org/content/dragon-1-m484) | Master484 | CC0 1.0 | 1 |
| OpenGameArt | [Dragon character](https://opengameart.org/content/dragon-character) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Dragons](https://opengameart.org/content/dragons) | Blarumyrran | CC0 1.0 | 3 |
| OpenGameArt | [dregbin](https://opengameart.org/content/dregbin) | surt | CC0 1.0 | 1 |
| OpenGameArt | [Dungeon Tileset](https://opengameart.org/content/dungeon-tileset-4) | HorusKDI | CC0 1.0 | 1 |
| OpenGameArt | [Filthy Ectoplasm](https://opengameart.org/content/filthy-ectoplasm) | Winternaut | CC0 1.0 | 1 |
| OpenGameArt | [Fire Golem](https://opengameart.org/content/fire-golem) | teasloth | CC0 1.0 | 1 |
| OpenGameArt | [Flame creature](https://opengameart.org/content/flame-creature) | takeshi | CC0 1.0 | 1 |
| OpenGameArt | [Flash Mage](https://opengameart.org/content/flash-mage) | Some Weirdo | CC0 1.0 | 1 |
| OpenGameArt | [Floating Eyeball](https://opengameart.org/content/floating-eyeball-0) | OwlishMedia | CC0 1.0 | 1 |
| OpenGameArt | [Flowers](https://opengameart.org/content/flowers) | SpiderDave | CC0 1.0 | 1 |
| OpenGameArt | [Forest Tiles](https://opengameart.org/content/forest-tiles) | surt | CC0 1.0 | 1 |
| OpenGameArt | [Forestredling](https://opengameart.org/content/forestredling) | marionline | CC0 1.0 | 1 |
| OpenGameArt | [Free CC0 Top Down Tileset Template Pixel Art](https://opengameart.org/content/free-cc0-top-down-tileset-template-pixel-art) | rgsdev | CC0 1.0 | 4 |
| OpenGameArt | [gb mini pixel world](https://opengameart.org/content/gb-mini-pixel-world) | pebonius | CC0 1.0 | 2 |
| OpenGameArt | [Gem Heart(Animated)](https://opengameart.org/content/gem-heartanimated) | AliHamieh | CC0 1.0 | 1 |
| OpenGameArt | [Ghost monster](https://opengameart.org/content/ghost-monster) | ImogiaGames | CC0 1.0 | 1 |
| OpenGameArt | [Goblin Caves](https://opengameart.org/content/goblin-caves) | Hyptosis | CC0 1.0 | 2 |
| OpenGameArt | [Golems](https://opengameart.org/content/golems) | zwonky ほか: Ragewortt | CC0 1.0 | 2 |
| OpenGameArt | [Green Drake](https://opengameart.org/content/green-drake) | teasloth | CC0 1.0 | 1 |
| OpenGameArt | [Happyland tileset](https://opengameart.org/content/happyland-tileset) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Home Objects](https://opengameart.org/content/home-objects) | Jannax | CC0 1.0 | 1 |
| OpenGameArt | [Human RPG Character](https://opengameart.org/content/human-rpg-character) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Items and elements](https://opengameart.org/content/items-and-elements) | GrafxKid | CC0 1.0 | 1 |
| OpenGameArt | [Komodo](https://opengameart.org/content/komodo) | teasloth | CC0 1.0 | 1 |
| OpenGameArt | [Mage City Arcanos](https://opengameart.org/content/mage-city-arcanos) | Hyptosis | CC0 1.0 | 1 |
| OpenGameArt | [Micro World: Old tileset](https://opengameart.org/content/micro-world-old-tileset) | SurrealEmber | CC0 1.0 | 1 |
| OpenGameArt | [Mini Fantasy Sprites](https://opengameart.org/content/mini-fantasy-sprites) | GrafxKid | CC0 1.0 | 1 |
| OpenGameArt | [Mini Roguelike 8x8 Tiles](https://opengameart.org/content/mini-roguelike-8x8-tiles) | morgan3d ほか: Kenney | CC0 1.0 | 1 |
| OpenGameArt | [MiniWorld Sprites](https://opengameart.org/content/miniworld-sprites) | Shade | CC0 1.0 | 81 |
| OpenGameArt | [Misc household items and more! >:)](https://opengameart.org/content/misc-household-items-and-more) | NaRNeRZz | CC0 1.0 | 1 |
| OpenGameArt | [Misc. Dark Fantasy Scenery Sprites](https://opengameart.org/content/misc-dark-fantasy-scenery-sprites) | ETTiNGRiNDER | CC0 1.0 | 1 |
| OpenGameArt | [Modified 32x32 Treasure chest](https://opengameart.org/content/modified-32x32-treasure-chest) | Blarumyrran | CC0 1.0 | 1 |
| OpenGameArt | [Monochromatic Cemetery Undead Ghosts Simple Pixel Art](https://opengameart.org/content/monochromatic-cemetery-undead-ghosts-simple-pixel-art) | Eduardo Martinelli | CC0 1.0 | 1 |
| OpenGameArt | [monster plant](https://opengameart.org/content/monster-plant) | ArVexi1050 | CC0 1.0 | 1 |
| OpenGameArt | [Mushroom Village tileset](https://opengameart.org/content/mushroom-village-tileset) | NettySvit | CC0 1.0 | 1 |
| OpenGameArt | [Nat's 8x8 Starter Pack](https://opengameart.org/content/nats-8x8-starter-pack) | nateonus | CC0 1.0 | 1 |
| OpenGameArt | [Nestor tileset](https://opengameart.org/content/nestor-tileset) | Demetrius | CC0 1.0 | 1 |
| OpenGameArt | [NPC and Enemies](https://opengameart.org/content/npc-and-enemies-0) | Refo | CC0 1.0 | 1 |
| OpenGameArt | [Outside tileset](https://opengameart.org/content/outside-tileset) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Overworld - Grass Biome](https://opengameart.org/content/overworld-grass-biome) | Beast | CC0 1.0 | 3 |
| OpenGameArt | [Overworld - Monastery](https://opengameart.org/content/overworld-monastery) | knekko | CC0 1.0 | 1 |
| OpenGameArt | [Overworld Grass Extention](https://opengameart.org/content/overworld-grass-extention) | knekko | CC0 1.0 | 1 |
| OpenGameArt | [Overworld Map](https://opengameart.org/content/overworld-map) | keith karnage | CC0 1.0 | 1 |
| OpenGameArt | [pastoral overworld](https://opengameart.org/content/pastoral-overworld) | pebonius | CC0 1.0 | 1 |
| OpenGameArt | [Pixel art animated Slime](https://opengameart.org/content/pixel-art-animated-slime) | rvros | CC0 1.0 | 1 |
| OpenGameArt | [pixel art castle tileset](https://opengameart.org/content/pixel-art-castle-tileset) | rubberduck | CC0 1.0 | 2 |
| OpenGameArt | [Pixel Art Dungeon Items](https://opengameart.org/content/pixel-art-dungeon-items) | SpinachChicken | CC0 1.0 | 1 |
| OpenGameArt | [pixel art skeleton](https://opengameart.org/content/pixel-art-skeleton) | tbbk | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Bosses. Yes!](https://opengameart.org/content/pixel-bosses-yes) | Monster Logix Studio | CC0 1.0 | 1 |
| OpenGameArt | [Pixel chest and coin](https://opengameart.org/content/pixel-chest-and-coin) | hippo | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Dragon](https://opengameart.org/content/pixel-dragon) | AnvilHouse | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Potion Set 16x16](https://opengameart.org/content/pixel-potion-set-16x16) | yafarida | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Raven](https://opengameart.org/content/pixel-raven) | tbbk | CC0 1.0 | 1 |
| OpenGameArt | [Plagueking [48x48]](https://opengameart.org/content/plagueking-48x48) | One Man Army | CC0 1.0 | 1 |
| OpenGameArt | [Plant and Mushroom Enemies charset and battlers](https://opengameart.org/content/plant-and-mushroom-enemies-charset-and-battlers) | NettySvit | CC0 1.0 | 1 |
| OpenGameArt | [potion](https://opengameart.org/content/potion-1) | kotnaszynce | CC0 1.0 | 1 |
| OpenGameArt | [Puny Characters](https://opengameart.org/content/puny-characters) | Shade | CC0 1.0 | 7 |
| OpenGameArt | [RogueDB32](https://opengameart.org/content/roguedb32) | SpiderDave | CC0 1.0 | 1 |
| OpenGameArt | [RogueDB32 Plus - add on tiles](https://opengameart.org/content/roguedb32-plus-add-on-tiles) | dannorder | CC0 1.0 | 1 |
| OpenGameArt | [RPG Asset Tile Set 'Cemetery' NES](https://opengameart.org/content/rpg-asset-tile-set-cemetery-nes) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [RPG boss brown mummy](https://opengameart.org/content/rpg-boss-brown-mummy) | skoam | CC0 1.0 | 1 |
| OpenGameArt | [RPG Character 'Knight' (NES)](https://opengameart.org/content/rpg-character-knight-nes) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [RPG Character 'Ranger' (NES)](https://opengameart.org/content/rpg-character-ranger-nes) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [RPG item set](https://opengameart.org/content/rpg-item-set) | Jetrel | CC0 1.0 | 1 |
| OpenGameArt | [RPG Items](https://opengameart.org/content/rpg-items) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [RPG portraits](https://opengameart.org/content/rpg-portraits) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [RPG Tiles — Forest / Meadows / Outdoor](https://opengameart.org/content/rpg-tiles-%E2%80%94-forest-meadows-outdoor) | Andrew J Hamilton | CC0 1.0 | 1 |
| OpenGameArt | [Simple broad-purpose tileset](https://opengameart.org/content/simple-broad-purpose-tileset) | surt ほか: Sharm, vk | CC0 1.0 | 1 |
| OpenGameArt | [Simple duotone tileset](https://opengameart.org/content/simple-duotone-tileset) | Eris | CC0 1.0 | 1 |
| OpenGameArt | [Simple Overworld Tile Set](https://opengameart.org/content/simple-overworld-tile-set) | Corey Archer | CC0 1.0 | 1 |
| OpenGameArt | [Skeleton and friends (8 directional)](https://opengameart.org/content/skeleton-and-friends-8-directional) | patvanmackelberg | CC0 1.0 | 4 |
| OpenGameArt | [Slime](https://opengameart.org/content/slime-7) | ArVexi1050 | CC0 1.0 | 1 |
| OpenGameArt | [Slime - Sprite Sheet](https://opengameart.org/content/slime-sprite-sheet) | Garakh | CC0 1.0 | 1 |
| OpenGameArt | [Slimy Adventure (Unfinished)](https://opengameart.org/content/slimy-adventure-unfinished) | NaRNeRZz | CC0 1.0 | 1 |
| OpenGameArt | [Steam monster](https://opengameart.org/content/steam-monster) | Blarumyrran | CC0 1.0 | 1 |
| OpenGameArt | [Steel Golem Walking](https://opengameart.org/content/steel-golem-walking) | DanyOctrome | CC0 1.0 | 1 |
| OpenGameArt | [The Field of the Floating Islands](https://opengameart.org/content/the-field-of-the-floating-islands) | Buch ほか: devurandom, surt | CC0 1.0 | 2 |
| OpenGameArt | [The Sathan Boss](https://opengameart.org/content/the-sathan-boss) | ShawChoo | CC0 1.0 | 2 |
| OpenGameArt | [Tiny Characters Set](https://opengameart.org/content/tiny-characters-set) | Fleurman | CC0 1.0 | 1 |
| OpenGameArt | [Tiny Creatures](https://opengameart.org/content/tiny-creatures) | Clint Bellanger ほか: Kenney | CC0 1.0 | 1 |
| OpenGameArt | [Tiny Dungeon Extras - Missing Walls Addon](https://opengameart.org/content/tiny-dungeon-extras-missing-walls-addon) | trunksbomb | CC0 1.0 | 1 |
| OpenGameArt | [Tiny RPG - Forest](https://opengameart.org/content/tiny-rpg-forest) | ansimuz | CC0 1.0 | 3 |
| OpenGameArt | [Tiny RPG CC0 Characters and Portraits](https://opengameart.org/content/tiny-rpg-cc0-characters-and-portraits) | tiopalada | CC0 1.0 | 2 |
| OpenGameArt | [Town Tiles](https://opengameart.org/content/town-tiles) | surt | CC0 1.0 | 1 |
| OpenGameArt | [Trees & Bushes](https://opengameart.org/content/trees-bushes) | ansimuz | CC0 1.0 | 1 |
| OpenGameArt | [Undead King](https://opengameart.org/content/undead-king) | Reemax ほか: artisticdude | CC0 1.0 | 1 |
| OpenGameArt | [Unfinished dungeon tileset](https://opengameart.org/content/unfinished-dungeon-tileset) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Various Creatures](https://opengameart.org/content/various-creatures) | GrafxKid | CC0 1.0 | 1 |
| OpenGameArt | [Village of Chaffton](https://opengameart.org/content/village-of-chaffton) | Spring Spring | CC0 1.0 | 2 |
| OpenGameArt | [Walking Character Set](https://opengameart.org/content/walking-character-set) | ATMANAN | CC0 1.0 | 2 |
| OpenGameArt | [Weapons for a roguelike](https://opengameart.org/content/weapons-for-a-roguelike) | Master484 | CC0 1.0 | 1 |
| OpenGameArt | [Winter Birds](https://opengameart.org/content/winter-birds) | Refuzzle | CC0 1.0 | 1 |
| OpenGameArt | [Zombie RPG sprites](https://opengameart.org/content/zombie-rpg-sprites) | Curt | CC0 1.0 | 4 |
| OpenGameArt | [Zombies & Skeletons](https://opengameart.org/content/zombies-skeletons) | artisticdude | CC0 1.0 | 1 |
