# ドット絵ライブラリ2（500枚・素材置き場）

1回目の500枚（`../pixel-library/`）とは別に、新しく選んだRPG用のドット絵500枚です（2026-09-30、人間の依頼で用意）。1回目・先に取り込んだぴぽやの10枚と、同じ絵（画素が同じもの）は1枚も入れていません。
**まだゲームには1枚も使っていません。** ゲームに入れるときは、`../pixel-library/README.md` の「ゲームに入れるとき」を守ってください（絵柄をそろえる・色数を減らす・`docs/assets-credits.md` に記録する・キャラの大きさは人間の判断待ち）。

- 1枚ずつの出典・作者・規約: [`MANIFEST.md`](MANIFEST.md)・`manifest.csv`
- 縮小一覧（素材ではない）: `_preview/`
- 規約の写し: `LICENSES/`

## 分類と枚数

| フォルダ | 中身 | 枚数 |
|---|---|---|
| `01-characters/` | 人物（ぴぽやの色違い・合成器の見本キャラ・猫にん、小さなRPGキャラ、顔グラフィック） | 156 |
| `02-monsters/` | 魔物（正面向きの戦闘用、シンボルエネミー、ハロウィン・雪の魔物、小さな生き物） | 76 |
| `03-bosses/` | ボス向き（ヒドラ・トロル・死霊使い・吸血鬼の王・竜・大きな魔物） | 13 |
| `04-field/` | フィールドのタイル（草・水・砂・雪・森・畑・木） | 62 |
| `05-maps/` | マップの見本（ワールドマップ10枚・ダンジョン5枚） | 15 |
| `06-dungeon/` | ダンジョン・洞窟・城・遺跡・墓地のタイル | 44 |
| `07-town-indoor/` | 町の建物・家の中のタイル | 19 |
| `08-objects-items/` | 武器・防具・薬・食べ物・宝石・宝箱・本・光と魔法陣のエフェクト | 115 |
| 合計 | | **500** |

配布元の内訳: ぴぽや倉庫 168枚、OpenGameArt（CC0）329枚、Kenney（CC0）3枚。配布元の素材セットは201種類（OpenGameArt のページは186）。

1回目より少ないもの: ボス向きの大きな魔物（CC0でドット絵、かつ由来のはっきりしたものが少なかった）、町の建物。

## 規約

- **CC0（OpenGameArt・Kenney）**: 商用利用・加工・再配布・ゲームへの組み込みは自由、クレジット不要。OpenGameArt の186ページすべてを 2026-09-30 に読み直し、ライセンス欄が CC0 だけであることを確かめた。
- **ぴぽや 無料素材利用規約**（https://pipoya.net/sozai/terms-of-use/ ）と各 readme（写しは `LICENSES/pipoya/`）: 商用利用可・加工可・ゲームへの組み込み可、クレジット・連絡は不要。**素材そのものを素材として販売するのは禁止。** 無償の再配布は規約とともに。「本がめくられるキャラチップ」には readme がないため、サイトの無料素材利用規約で確認した。
- **このフォルダの絵を、素材として販売・再配布しないこと。**

## 選び方（1回目より厳しくしたところ）

1. 規約: 上のとおり。
2. **説明文の全文を読んだ**（1回目は冒頭の一部だけを機械で調べていた）。次のものを外した:
   - 既存のゲームの絵、または既存のゲームのために作られた・使われた絵（例: Monster RPG 2、Stendhal、Wesnoth、Frogatto、FLARE、作者の公開済みのゲームやゲームジャム作品）
   - 既存の作品に似せた・寄せたと書かれたもの（例: 有名RPG・Castlevania 風・Pokémon 風・Stranger Things 風、ディズニーのキャラに似ていると書かれた竜）
   - 見た目が有名な作品の生き物にそっくりなモンスター集（説明に書かれていなくても、目で見て外した）
   - 元の作者でない人が上げたもの（由来があいまい）、AIや3Dの描画から作ったもの、写真の人物を元にしたもの
3. ドット絵か: 色数・半透明を数え、縮小一覧をすべて目で見て、なめらかな絵・透かし文字・説明の文字・下書きの型紙（TEMPLATE と書かれたもの）・背景の塗りつぶしだけの絵を外した。
4. 重複: 1回目の500枚・既存の `assets-src/` と、画素が同じものを除いた（ファイルが違っても中身が同じものも除いた。10枚が当たった）。
5. 全年齢向け: 血しぶき・水着などは外した。

この見直しで、1回目の500枚からも5枚を差し替えた（Stendhal 用の絵3枚、既存のゲームの品物の名前のもじり1枚、元の作者でない人が上げた絵1枚。`../pixel-library/README.md` に記録）。

## 手を加えたもの（ほかは配布元のファイルのまま、名前だけ変えた）

- `05-maps/pipoya-worldmap-sample-c`〜`j`: ぴぽや「フィールドマップセット１」で組み立てたワールドマップの見本（素材の加工。規約で認められている）。
- 背景の単色を透明にして余白を切ったもの: `manifest.csv` の「modified」列に書いた。

## 配布元の一覧

| 配布元 | 素材 | 作者 | 規約 | 枚数 |
|---|---|---|---|---|
| ぴぽや倉庫 | [RPGキャラ基本セット（キャラチップ.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 45 |
| ぴぽや倉庫 | [ぴぽや32×32グラフィック合成器用パーツ・猫にん（同梱の見本キャラ）](https://pipoya.net/sozai/assets/charachip/character-chip-2/) | ぴぽや | ぴぽや 無料素材利用規約 | 9 |
| ぴぽや倉庫 | [ぴぽや32×32グラフィック合成器用パーツ（同梱の見本キャラ）](https://pipoya.net/sozai/assets/charachip/character-chip-2/) | ぴぽや | ぴぽや 無料素材利用規約 | 36 |
| ぴぽや倉庫 | [ぴぽやキャラチップ32出力素材（ぴぽや32×32 出力画像＋α）](https://pipoya.net/sozai/assets/charachip/character-chip-2/) | ぴぽや | ぴぽや 無料素材利用規約 | 21 |
| ぴぽや倉庫 | [ウディタ２用マップセット（ウディタ2_32x32mapchip_20210215.zip）](https://pipoya.net/sozai/assets/map-chip_tileset32/) | ぴぽや | ぴぽや 無料素材利用規約 | 8 |
| ぴぽや倉庫 | [クリスマスキャラクター（クリスマスキャラチップ.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 6 |
| ぴぽや倉庫 | [シンプルエネミーシンボル32×32キャラチップ（pipo-simpleenemy01.zip の「４方向」）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 7 |
| ぴぽや倉庫 | [ハロウィンキャラクター（ハロウィンキャラチップ.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 6 |
| ぴぽや倉庫 | [パラパラとページがめくられる本（本がめくられるキャラチップ.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 4 |
| ぴぽや倉庫 | [フィールドマップセット１・同 追加パーツ（このプロジェクトで組み立てたマップ。元のタイルは assets-src/pipoya/）](https://pipoya.net/sozai/assets/map-chip_tileset32/) | ぴぽや | ぴぽや 無料素材利用規約 | 8 |
| ぴぽや倉庫 | [光モノ16種（hikarimono_charachip16.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 16 |
| ぴぽや倉庫 | [爆弾と風船（爆弾と風船.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 2 |
| Kenney | [1-Bit Pack](https://kenney.nl/assets/1-bit-pack) | Kenney | CC0 1.0 | 1 |
| Kenney | [Tiny Battle](https://kenney.nl/assets/tiny-battle) | Kenney | CC0 1.0 | 1 |
| Kenney | [Tiny Ski](https://kenney.nl/assets/tiny-ski) | Kenney | CC0 1.0 | 1 |
| OpenGameArt | [1-Bit Doomcrypt Kit](https://opengameart.org/content/1-bit-doomcrypt-kit) | B77345-100 | CC0 1.0 | 6 |
| OpenGameArt | [1-Bit Doomland Kit](https://opengameart.org/content/1-bit-doomland-kit) | B77345-100 | CC0 1.0 | 4 |
| OpenGameArt | [16x16 Assorted RPG Icons](https://opengameart.org/content/16x16-assorted-rpg-icons) | Shade | CC0 1.0 | 1 |
| OpenGameArt | [16x16 Mage](https://opengameart.org/content/16x16-mage) | saint11 | CC0 1.0 | 1 |
| OpenGameArt | [16x16 Puny Dungeon Tileset](https://opengameart.org/content/16x16-puny-dungeon-tileset) | Shade | CC0 1.0 | 7 |
| OpenGameArt | [16x16 Simple Fantasy RPG FX](https://opengameart.org/content/16x16-simple-fantasy-rpg-fx) | Emcee Flesher | CC0 1.0 | 1 |
| OpenGameArt | [16x16 Tiles](https://opengameart.org/content/16x16-tiles) | Ogrebane | CC0 1.0 | 1 |
| OpenGameArt | [16x16 Weapon RPG Icons](https://opengameart.org/content/16x16-weapon-rpg-icons) | Shade | CC0 1.0 | 1 |
| OpenGameArt | [2D Chibi Ninja - 8 Actions](https://opengameart.org/content/2d-chibi-ninja-8-actions) | ashuuya | CC0 1.0 | 1 |
| OpenGameArt | [2D Outdoor 32x32 Tileset](https://opengameart.org/content/2d-outdoor-32x32-tileset) | aeren108 | CC0 1.0 | 1 |
| OpenGameArt | [2D Simple Grass TileSet](https://opengameart.org/content/2d-simple-grass-tileset) | Gustavo Saraiva | CC0 1.0 | 1 |
| OpenGameArt | [2D Tilesets](https://opengameart.org/content/2d-tilesets) | kddove85 | CC0 1.0 | 4 |
| OpenGameArt | [2D Vegetables](https://opengameart.org/content/2d-vegetables) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [32 x 32 Portraits](https://opengameart.org/content/32-x-32-portraits) | Seafood5040 | CC0 1.0 | 1 |
| OpenGameArt | [320 x 192 Castle Tiles Pixel Art](https://opengameart.org/content/320-x-192-castle-tiles-pixel-art) | txturs | CC0 1.0 | 1 |
| OpenGameArt | [32x32 Dungeon Tileset](https://opengameart.org/content/32x32-dungeon-tileset) | stealthix | CC0 1.0 | 1 |
| OpenGameArt | [32X32 Dungeon Tileset](https://opengameart.org/content/32x32-dungeon-tileset-0) | ThatOneRandomGameDev | CC0 1.0 | 1 |
| OpenGameArt | [32x32 Grass with water tileset](https://opengameart.org/content/32x32-grass-with-water-tileset) | GboxMikeFozzy | CC0 1.0 | 1 |
| OpenGameArt | [32x32 RPG Character Sprites](https://opengameart.org/content/32x32-rpg-character-sprites) | Eldiran | CC0 1.0 | 1 |
| OpenGameArt | [4 Colour Dungeon Tileset](https://opengameart.org/content/4-colour-dungeon-tileset) | stealthix | CC0 1.0 | 2 |
| OpenGameArt | [4-Color Dungeon Bricks (16x16)](https://opengameart.org/content/4-color-dungeon-bricks-16x16) | MoikMellah | CC0 1.0 | 1 |
| OpenGameArt | [496 pixel art icons for medieval/fantasy RPG](https://opengameart.org/content/496-pixel-art-icons-for-medievalfantasy-rpg) | Henrique Lazarini (7Soul1) | CC0 1.0 | 33 |
| OpenGameArt | [5 MORE RPG/Fantasy Weapons!](https://opengameart.org/content/5-more-rpgfantasy-weapons) | Cerbion | CC0 1.0 | 2 |
| OpenGameArt | [8x8 8-bit Styled Castle Tileset](https://opengameart.org/content/8x8-8-bit-styled-castle-tileset) | ImpossibleRealms | CC0 1.0 | 1 |
| OpenGameArt | [8x8 PICO-8 Tile Set 1](https://opengameart.org/content/8x8-pico-8-tile-set-1) | hawkbirdtree | CC0 1.0 | 1 |
| OpenGameArt | [8x8 Rogue-Like Char/Enemies/Tiles](https://opengameart.org/content/8x8-rogue-like-charenemiestiles) | Min | CC0 1.0 | 1 |
| OpenGameArt | [8x8 Starter Tile Pallet](https://opengameart.org/content/8x8-starter-tile-pallet) | EverCrazy | CC0 1.0 | 1 |
| OpenGameArt | [[Zoria] cc0 pack](https://opengameart.org/content/zoria-cc0-pack) | Baŝto | CC0 1.0 | 2 |
| OpenGameArt | [A blocky dungeon](https://opengameart.org/content/a-blocky-dungeon) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Adventure Awaits Asset Pack 1.0](https://opengameart.org/content/adventure-awaits-asset-pack-10) | IshtartPixels | CC0 1.0 | 1 |
| OpenGameArt | [Animated 2D Pixel Treasure Chest](https://opengameart.org/content/animated-2d-pixel-treasure-chest) | beddedOtaku | CC0 1.0 | 1 |
| OpenGameArt | [Animated character](https://opengameart.org/content/animated-character) | Sogomn | CC0 1.0 | 1 |
| OpenGameArt | [Animated Creepy Thing](https://opengameart.org/content/animated-creepy-thing) | Charlie | CC0 1.0 | 1 |
| OpenGameArt | [Animated Fantasy Bows](https://opengameart.org/content/animated-fantasy-bows) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Animated Filthy Ectoplasm](https://opengameart.org/content/animated-filthy-ectoplasm) | Reemax ほか: Winternaut | CC0 1.0 | 1 |
| OpenGameArt | [Animated Monsters](https://opengameart.org/content/animated-monsters) | stealthix | CC0 1.0 | 1 |
| OpenGameArt | [Animated Mushroom Monster (Pixel-Art)](https://opengameart.org/content/animated-mushroom-monster-pixel-art) | ScratchIO | CC0 1.0 | 2 |
| OpenGameArt | [Base Male Fighter](https://opengameart.org/content/base-male-fighter) | rubengc | CC0 1.0 | 1 |
| OpenGameArt | [Basic Dungeon Tileset](https://opengameart.org/content/basic-dungeon-tileset) | ShadowArtist | CC0 1.0 | 1 |
| OpenGameArt | [Behrs 2,500 Pixel Battle Axes 32x32 Archive](https://opengameart.org/content/behrs-2500-pixel-battle-axes-32x32-archive) | Behrtron | CC0 1.0 | 1 |
| OpenGameArt | [Bigleg](https://opengameart.org/content/bigleg) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Bit Bonanza 10x10 Top-Down RPG Tiles](https://opengameart.org/content/bit-bonanza-10x10-top-down-rpg-tiles) | VEXED | CC0 1.0 | 1 |
| OpenGameArt | [Blue Brick Tileset](https://opengameart.org/content/blue-brick-tileset) | Nimnon | CC0 1.0 | 1 |
| OpenGameArt | [Brightmix Icon Set](https://opengameart.org/content/brightmix-icon-set) | Brightmix | CC0 1.0 | 1 |
| OpenGameArt | [Castlecrest](https://opengameart.org/content/castlecrest) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Cave Tileset](https://opengameart.org/content/cave-tileset-2) | yewt | CC0 1.0 | 1 |
| OpenGameArt | [Cave Tileset](https://opengameart.org/content/cave-tileset-4) | GrafxKid | CC0 1.0 | 1 |
| OpenGameArt | [CC0 Award Icons](https://opengameart.org/content/cc0-award-icons) | AntumDeluge | CC0 1.0 | 1 |
| OpenGameArt | [Characters](https://opengameart.org/content/characters-2) | pondomaniac | CC0 1.0 | 1 |
| OpenGameArt | [Chest - Opening Animation 16x16](https://opengameart.org/content/chest-opening-animation-16x16) | Natural_Privateer | CC0 1.0 | 1 |
| OpenGameArt | [Chibi Base](https://opengameart.org/content/chibi-base) | thecilekli | CC0 1.0 | 1 |
| OpenGameArt | [chicken and pen](https://opengameart.org/content/chicken-and-pen) | Proyd | CC0 1.0 | 1 |
| OpenGameArt | [Classic-Knight [Animated]](https://opengameart.org/content/classic-knight-animated) | Disthron | CC0 1.0 | 1 |
| OpenGameArt | [Color RPG items](https://opengameart.org/content/color-rpg-items) | anubisky | CC0 1.0 | 1 |
| OpenGameArt | [cozy asset pack 1.0](https://opengameart.org/content/cozy-asset-pack-10) | IshtartPixels | CC0 1.0 | 3 |
| OpenGameArt | [Crates And Sacks](https://opengameart.org/content/crates-and-sacks) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Desert Level Decorations (Pixel-Art)](https://opengameart.org/content/desert-level-decorations-pixel-art) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Dog Sprites](https://opengameart.org/content/dog-sprites) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Dragon/Monster eggs](https://opengameart.org/content/dragonmonster-eggs) | Fadesta | CC0 1.0 | 1 |
| OpenGameArt | [Dungeon tileset](https://opengameart.org/content/dungeon-tileset) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Dungeon Tileset](https://opengameart.org/content/dungeon-tileset-3) | shortfoot38 | CC0 1.0 | 1 |
| OpenGameArt | [dungeon tileset with walls and floors](https://opengameart.org/content/dungeon-tileset-with-walls-and-floors) | rubberduck | CC0 1.0 | 3 |
| OpenGameArt | [Egyptian RPG](https://opengameart.org/content/egyptian-rpg) | ZomBCool | CC0 1.0 | 2 |
| OpenGameArt | [Emotes Pack](https://opengameart.org/content/emotes-pack) | Kenney | CC0 1.0 | 1 |
| OpenGameArt | [Fantasy head](https://opengameart.org/content/fantasy-head) | gamehon | CC0 1.0 | 1 |
| OpenGameArt | [Fantasy RPG Sprite Kit (32x32)](https://opengameart.org/content/fantasy-rpg-sprite-kit-32x32) | DezrasDragons | CC0 1.0 | 2 |
| OpenGameArt | [Fantasy Weapons And Shields](https://opengameart.org/content/fantasy-weapons-and-shields) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Farming crops 16x16](https://opengameart.org/content/farming-crops-16x16) | josehzz | CC0 1.0 | 1 |
| OpenGameArt | [Fever Dream Faces](https://opengameart.org/content/fever-dream-faces) | knekko | CC0 1.0 | 1 |
| OpenGameArt | [Flute Snake lite](https://opengameart.org/content/flute-snake-lite) | j0j0n4th4n | CC0 1.0 | 1 |
| OpenGameArt | [Forest / Graveyard tileset](https://opengameart.org/content/forest-graveyard-tileset) | marionline | CC0 1.0 | 1 |
| OpenGameArt | [Forest Level Decorations (Pixel-Art)](https://opengameart.org/content/forest-level-decorations-pixel-art) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Forest Tileset for 16 x 16](https://opengameart.org/content/forest-tileset-for-16-x-16) | Pav Creations | CC0 1.0 | 1 |
| OpenGameArt | [Forest troll](https://opengameart.org/content/forest-troll) | Blind Harpy Gamedev | CC0 1.0 | 1 |
| OpenGameArt | [Forest Weapons (Pixel-Art)](https://opengameart.org/content/forest-weapons-pixel-art) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Forestredling](https://opengameart.org/content/forestredling) | marionline | CC0 1.0 | 1 |
| OpenGameArt | [Forgotten Dungeon](https://opengameart.org/content/forgotten-dungeon) | Blackwolfdave | CC0 1.0 | 1 |
| OpenGameArt | [Gargoyle](https://opengameart.org/content/gargoyle-0) | dr_corchit | CC0 1.0 | 1 |
| OpenGameArt | [gb funky fauna](https://opengameart.org/content/gb-funky-fauna) | pebonius | CC0 1.0 | 3 |
| OpenGameArt | [Generic Fantasy RPG Items](https://opengameart.org/content/generic-fantasy-rpg-items) | HomoHikka | CC0 1.0 | 1 |
| OpenGameArt | [Ghost animated](https://opengameart.org/content/ghost-animated) | LetargicDev | CC0 1.0 | 1 |
| OpenGameArt | [Grass Tiles [32x32]](https://opengameart.org/content/grass-tiles-32x32-0) | CDmir | CC0 1.0 | 2 |
| OpenGameArt | [Grass&Mud 16x16 Tiles](https://opengameart.org/content/grassmud-16x16-tiles) | josehzz | CC0 1.0 | 1 |
| OpenGameArt | [Grass&Water 16x16 Tiles](https://opengameart.org/content/grasswater-16x16-tiles) | josehzz | CC0 1.0 | 1 |
| OpenGameArt | [Green Cap Character 16x18](https://opengameart.org/content/green-cap-character-16x18) | isaiah658 | CC0 1.0 | 1 |
| OpenGameArt | [Gremlin [Animated] - Classic Hero Edit](https://opengameart.org/content/gremlin-animated-classic-hero-edit) | Umz | CC0 1.0 | 2 |
| OpenGameArt | [Happyland Tileset Wang Compatible](https://opengameart.org/content/happyland-tileset-wang-compatible) | noodle ほか: Buch | CC0 1.0 | 1 |
| OpenGameArt | [helmet](https://opengameart.org/content/helmet-0) | Xevin | CC0 1.0 | 1 |
| OpenGameArt | [Helmets [64x64]](https://opengameart.org/content/helmets-64x64) | LordNeo | CC0 1.0 | 1 |
| OpenGameArt | [Horror Fantasy Assets](https://opengameart.org/content/horror-fantasy-assets) | stealthix | CC0 1.0 | 1 |
| OpenGameArt | [Icons_32x32](https://opengameart.org/content/icons32x32) | ArlanTR | CC0 1.0 | 1 |
| OpenGameArt | [Interior Mini-Tileset,"Sitting Inside Being Scared of People"](https://opengameart.org/content/interior-mini-tilesetsitting-inside-being-scared-of-people) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Just some 32x32 tiles](https://opengameart.org/content/just-some-32x32-tiles) | OwlishMedia | CC0 1.0 | 2 |
| OpenGameArt | [Land Monster Sprites](https://opengameart.org/content/land-monster-sprites) | bevouliin.com | CC0 1.0 | 1 |
| OpenGameArt | [Leaning Into The Grid (16x16 Tiles)](https://opengameart.org/content/leaning-into-the-grid-16x16-tiles) | second | CC0 1.0 | 1 |
| OpenGameArt | [Light Weapons (Pixel Art)](https://opengameart.org/content/light-weapons-pixel-art) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Lootable Mimic Asset Pack](https://opengameart.org/content/lootable-mimic-asset-pack) | Fava Beans | CC0 1.0 | 1 |
| OpenGameArt | [Maces [64 x 64]](https://opengameart.org/content/maces-64-x-64) | LordNeo | CC0 1.0 | 1 |
| OpenGameArt | [Mage Sprites (Idle and Walking)](https://opengameart.org/content/mage-sprites-idle-and-walking) | Sollision | CC0 1.0 | 1 |
| OpenGameArt | [Magical Road Pixel Art Environment](https://opengameart.org/content/magical-road-pixel-art-environment) | ansimuz | CC0 1.0 | 1 |
| OpenGameArt | [Medals](https://opengameart.org/content/medals-3) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Medieval Armor (Pixel-Art)](https://opengameart.org/content/medieval-armor-pixel-art) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Mer RPG Character](https://opengameart.org/content/mer-rpg-character) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Mercenarian](https://opengameart.org/content/mercenarian) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Mini dungeon tileset](https://opengameart.org/content/mini-dungeon-tileset) | nazaire | CC0 1.0 | 1 |
| OpenGameArt | [MiniWorld Sprites](https://opengameart.org/content/miniworld-sprites) | Shade | CC0 1.0 | 18 |
| OpenGameArt | [Mollufant](https://opengameart.org/content/mollufant) | j0j0n4th4n | CC0 1.0 | 1 |
| OpenGameArt | [More SandTileSet 16x16](https://opengameart.org/content/more-sandtileset-16x16) | GrumpyDiamond | CC0 1.0 | 1 |
| OpenGameArt | [Mr. Necromancer Man [Animated]](https://opengameart.org/content/mr-necromancer-man-animated) | Disthron | CC0 1.0 | 1 |
| OpenGameArt | [Mummy Enemies](https://opengameart.org/content/mummy-enemies) | skoam | CC0 1.0 | 1 |
| OpenGameArt | [Mythical Ruins Tileset](https://opengameart.org/content/mythical-ruins-tileset) | voec | CC0 1.0 | 1 |
| OpenGameArt | [Nat's 8x8 Starter Pack](https://opengameart.org/content/nats-8x8-starter-pack) | nateonus | CC0 1.0 | 7 |
| OpenGameArt | [Ore Tileset - Eight Ores](https://opengameart.org/content/ore-tileset-eight-ores) | DavoltC | CC0 1.0 | 1 |
| OpenGameArt | [Orthographic outdoor tiles](https://opengameart.org/content/orthographic-outdoor-tiles) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Outdoor 32x32 tileset](https://opengameart.org/content/outdoor-32x32-tileset) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Piskel Hydra enemy](https://opengameart.org/content/piskel-hydra-enemy) | PINKCANNON | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Art Character](https://opengameart.org/content/pixel-art-character) | acasas | CC0 1.0 | 1 |
| OpenGameArt | [Pixel art top down dungeon tileset and rpg character with animations](https://opengameart.org/content/pixel-art-top-down-dungeon-tileset-and-rpg-character-with-animations) | profpatonildo | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Art Wasteland](https://opengameart.org/content/pixel-art-wasteland) | CodeManu | CC0 1.0 | 2 |
| OpenGameArt | [Pixel Character 02 - James](https://opengameart.org/content/pixel-character-02-james) | ImogiaGames | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Farmer](https://opengameart.org/content/pixel-farmer) | Monster Logix Studio | CC0 1.0 | 1 |
| OpenGameArt | [Pixel RPG Sprites (Houses, Characters)](https://opengameart.org/content/pixel-rpg-sprites-houses-characters) | Keiffer | CC0 1.0 | 2 |
| OpenGameArt | [Pixel Treasure Chest and Piles of Gold](https://opengameart.org/content/pixel-treasure-chest-and-piles-of-gold) | TokyoGeisha | CC0 1.0 | 1 |
| OpenGameArt | [pixel turtle](https://opengameart.org/content/pixel-turtle) | alizard | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Weapon Icons](https://opengameart.org/content/pixel-weapon-icons) | Umplix | CC0 1.0 | 2 |
| OpenGameArt | [Pixel Weapon Sheet](https://opengameart.org/content/pixel-weapon-sheet) | Gerald Burke | CC0 1.0 | 1 |
| OpenGameArt | [Plant Tileset](https://opengameart.org/content/plant-tileset) | ARoachIFoundOnMyPillow | CC0 1.0 | 1 |
| OpenGameArt | [Pumpkin Garden tiles](https://opengameart.org/content/pumpkin-garden-tiles) | NettySvit | CC0 1.0 | 1 |
| OpenGameArt | [Purupuru Island Tileset](https://opengameart.org/content/purupuru-island-tileset) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Pyro Sprite Sheet](https://opengameart.org/content/pyro-sprite-sheet) | Bing Soy | CC0 1.0 | 1 |
| OpenGameArt | [Quick castle tileset](https://opengameart.org/content/quick-castle-tileset) | Uxorioushornet | CC0 1.0 | 1 |
| OpenGameArt | [Red head character](https://opengameart.org/content/red-head-character) | PINKCANNON | CC0 1.0 | 1 |
| OpenGameArt | [RPG Assets 'Tile Set' (NES)](https://opengameart.org/content/rpg-assets-tile-set-nes) | Chasersgaming | CC0 1.0 | 2 |
| OpenGameArt | [RPG Assets (GB)](https://opengameart.org/content/rpg-assets-gb) | Chasersgaming | CC0 1.0 | 4 |
| OpenGameArt | [RPG character sprites](https://opengameart.org/content/rpg-character-sprites) | GrafxKid | CC0 1.0 | 1 |
| OpenGameArt | [RPG Characters](https://opengameart.org/content/rpg-characters-0) | Auer | CC0 1.0 | 1 |
| OpenGameArt | [RPG Characters Pack](https://opengameart.org/content/rpg-characters-pack) | Onni | CC0 1.0 | 1 |
| OpenGameArt | [RPG DUNGEON PACKAGE](https://opengameart.org/content/rpg-dungeon-package) | Corey Archer | CC0 1.0 | 2 |
| OpenGameArt | [RPG Fantasy Icon Set](https://opengameart.org/content/rpg-fantasy-icon-set) | DezrasDragons | CC0 1.0 | 1 |
| OpenGameArt | [RPG Inventory Icons](https://opengameart.org/content/rpg-inventory-icons) | BizmasterStudios | CC0 1.0 | 1 |
| OpenGameArt | [RPG Tile Set 'Secret Service Building' NES](https://opengameart.org/content/rpg-tile-set-secret-service-building-nes) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [RPG Tile Set 'Stonelands' NES](https://opengameart.org/content/rpg-tile-set-stonelands-nes) | Chasersgaming | CC0 1.0 | 2 |
| OpenGameArt | [Sideview Fantasy Patreon Collection](https://opengameart.org/content/sideview-fantasy-patreon-collection) | ansimuz | CC0 1.0 | 6 |
| OpenGameArt | [Simple Dungeon Walls](https://opengameart.org/content/simple-dungeon-walls) | elfy_boo | CC0 1.0 | 1 |
| OpenGameArt | [Simple NES-like Village Tiles](https://opengameart.org/content/simple-nes-like-village-tiles) | surt | CC0 1.0 | 1 |
| OpenGameArt | [Singular Direction Monsters + Battlers](https://opengameart.org/content/singular-direction-monsters-battlers) | Some Weirdo | CC0 1.0 | 13 |
| OpenGameArt | [Skull Monster](https://opengameart.org/content/skull-monster) | Bombfire | CC0 1.0 | 1 |
| OpenGameArt | [Slime Animation](https://opengameart.org/content/slime-animation) | GalaxyGamingBoy | CC0 1.0 | 1 |
| OpenGameArt | [Snake RPG Character](https://opengameart.org/content/snake-rpg-character) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Some 16x16 floor tiles](https://opengameart.org/content/some-16x16-floor-tiles) | ChikenwingJJA | CC0 1.0 | 1 |
| OpenGameArt | [Spooky Castle Tileset](https://opengameart.org/content/spooky-castle-tileset) | Buch | CC0 1.0 | 2 |
| OpenGameArt | [Staff [64 x64]](https://opengameart.org/content/staff-64-x64) | LordNeo | CC0 1.0 | 1 |
| OpenGameArt | [Stone Axe (with degradation progress)](https://opengameart.org/content/stone-axe-with-degradation-progress) | ScratchIO | CC0 1.0 | 1 |
| OpenGameArt | [Stone Tile Set](https://opengameart.org/content/stone-tile-set) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [Superpowers assets characters](https://opengameart.org/content/superpowers-assets-characters) | MedicineStorm | CC0 1.0 | 2 |
| OpenGameArt | [surtizens](https://opengameart.org/content/surtizens) | pebonius | CC0 1.0 | 15 |
| OpenGameArt | [Tent "Home"](https://opengameart.org/content/tent-home) | Senmou | CC0 1.0 | 1 |
| OpenGameArt | [The Rotating Eyeball](https://opengameart.org/content/the-rotating-eyeball) | ImogiaGames | CC0 1.0 | 1 |
| OpenGameArt | [Tileset](https://opengameart.org/content/tileset-1) | Robert Ramsay | CC0 1.0 | 4 |
| OpenGameArt | [Tileset 8x8 (Rosy 42 palette)](https://opengameart.org/content/tileset-8x8-rosy-42-palette) | drakzlin | CC0 1.0 | 1 |
| OpenGameArt | [Tileset Minimal Style - 8x8 based with characters included](https://opengameart.org/content/tileset-minimal-style-8x8-based-with-characters-included) | patvanmackelberg | CC0 1.0 | 1 |
| OpenGameArt | [Tiny RPG - Forest](https://opengameart.org/content/tiny-rpg-forest) | ansimuz | CC0 1.0 | 3 |
| OpenGameArt | [Tiny Tactics - Battle Kit I](https://opengameart.org/content/tiny-tactics-battle-kit-i) | tiopalada | CC0 1.0 | 1 |
| OpenGameArt | [Tools and Ressources](https://opengameart.org/content/tools-and-ressources) | marionline | CC0 1.0 | 1 |
| OpenGameArt | [Top Down Asset Pack 1.0](https://opengameart.org/content/top-down-asset-pack-10) | IshtartPixels | CC0 1.0 | 7 |
| OpenGameArt | [Top down game assets.](https://opengameart.org/content/top-down-game-assets) | LetargicDev | CC0 1.0 | 1 |
| OpenGameArt | [Top Down Male Character Sheet](https://opengameart.org/content/top-down-male-character-sheet) | DkuCook | CC0 1.0 | 1 |
| OpenGameArt | [Top Down season/environment Tileset](https://opengameart.org/content/top-down-seasonenvironment-tileset) | marionline | CC0 1.0 | 1 |
| OpenGameArt | [Top Down Tileset](https://opengameart.org/content/top-down-tileset) | saint11 | CC0 1.0 | 1 |
| OpenGameArt | [Tower defense slime enemy](https://opengameart.org/content/tower-defense-slime-enemy) | Tisroc | CC0 1.0 | 1 |
| OpenGameArt | [Treasure Chest Sprite](https://opengameart.org/content/treasure-chest-sprite) | r0ar | CC0 1.0 | 1 |
| OpenGameArt | [Treasure hunter game assets](https://opengameart.org/content/treasure-hunter-game-assets) | hdst | CC0 1.0 | 1 |
| OpenGameArt | [Troll [Animated] - Classic Hero Edit](https://opengameart.org/content/troll-animated-classic-hero-edit) | Umz | CC0 1.0 | 1 |
| OpenGameArt | [Warped Character Pro](https://opengameart.org/content/warped-character-pro) | ansimuz | CC0 1.0 | 1 |
| OpenGameArt | [Warped Top-Down Tech Lab](https://opengameart.org/content/warped-top-down-tech-lab) | ansimuz | CC0 1.0 | 1 |
| OpenGameArt | [Warped: Super Grotto Escape Pack](https://opengameart.org/content/warped-super-grotto-escape-pack) | ansimuz | CC0 1.0 | 2 |
| OpenGameArt | [Water16x16](https://opengameart.org/content/water16x16) | GrumpyDiamond | CC0 1.0 | 1 |
| OpenGameArt | [Waterworld tileset 16x16](https://opengameart.org/content/waterworld-tileset-16x16) | coem | CC0 1.0 | 1 |
| OpenGameArt | [Weapons [64x64]](https://opengameart.org/content/weapons-64x64) | LordNeo | CC0 1.0 | 1 |
| OpenGameArt | [well 16x32 sprite](https://opengameart.org/content/well-16x32-sprite) | InThePixel | CC0 1.0 | 1 |
| OpenGameArt | [Wheatfields Tileset](https://opengameart.org/content/wheatfields-tileset) | ARoachIFoundOnMyPillow | CC0 1.0 | 1 |
| OpenGameArt | [Whip [64 x 64]](https://opengameart.org/content/whip-64-x-64) | LordNeo | CC0 1.0 | 1 |
| OpenGameArt | [Winter Story](https://opengameart.org/content/winter-story) | Brosnya | CC0 1.0 | 3 |
| OpenGameArt | [Winter Tileset [16x16]](https://opengameart.org/content/winter-tileset-16x16) | zaphgames | CC0 1.0 | 1 |
| OpenGameArt | [Woman RPG Character](https://opengameart.org/content/woman-rpg-character) | josepharaoh99 | CC0 1.0 | 1 |
| OpenGameArt | [Zombie and Skeleton 32x48](https://opengameart.org/content/zombie-and-skeleton-32x48) | Reemax ほか: artisticdude | CC0 1.0 | 1 |
