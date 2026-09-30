# ドット絵の参考素材 1000点

描き方の参考にするためのドット絵を1000点集めたものです（2026-09-30、人間の依頼で用意）。規約上はゲームに使うこともできますが、主な目的は**見て学ぶ・部品として組み立てる**ことです。
`../pixel-library/`（500枚）・`../pixel-library-2/`（500枚）・先に取り込んだぴぽやの10枚と、画素が同じ絵は1点も入れていません（270点が重複で外れた）。**まだゲームには使っていません。**

- 1点ずつの出典・作者・規約: [`MANIFEST.md`](MANIFEST.md)・`manifest.csv`
- 縮小一覧（素材ではない）: `_preview/`
- 規約の写し: `LICENSES/`

## 分類と点数

| フォルダ | 中身 | 点数 |
|---|---|---|
| `01-characters/` | 人物。ぴぽやの現代・お仕事の人物143点（学生・先生・医師・警官・店員・会社員など）、ぴぽやの色違い、CC0の小さな人物・顔 | 242 |
| `02-monsters/` | 魔物。スライム・おばけ・骸骨・クモ・ヘビ・オオカミ・カエル・コウモリ・ゴブリンなど | 106 |
| `03-bosses/` | ボス向き（ネズミの王・大きな骸骨・オオカミの霊） | 4 |
| `04-field/` | フィールド。ウディタ形式のままのオートタイル33点、木・岩・草・畑・水辺など | 106 |
| `06-dungeon/` | ダンジョン・遺跡・溶岩のタイル | 12 |
| `07-town-indoor/` | 町の建物（MiniWorld の屋根の色違いを含む）・家 | 54 |
| `08-objects-items/` | アイテムのアイコン（1点ずつ。武器・防具・薬・食べ物・宝石・技など177点）、宝箱・盾・置物 | 224 |
| `09-effects/` | 爆発・炎・光の輪などのエフェクト | 16 |
| `10-parts/` | **キャラを組み立てる部品**（ぴぽやのグラフィック合成器用パーツ235点: 服・髪・帽子・マント・メガネ・ひげ・持ち物・体・猫にんの体と尻尾。CC0 の魔物を組み立てる部品1点） | 236 |
| 合計 | | **1000** |

配布元の内訳: ぴぽや倉庫 431点、OpenGameArt（CC0）569点（203種類の素材セットから）。

**正直なところ**: 1000点のうち、1点ずつの小さな絵（アイコン177点・組み立て用の部品235点・MiniWorld の色違い）が多く入っています。新しく見つけた OpenGameArt の配布元からの絵は約213点です。ボス向きの大きな魔物とダンジョンは、条件（CC0・ドット絵・由来がはっきり・既存作品と関係ない）を満たすものが少なく、数が少なめです。マップの見本は今回はありません（1回目・2回目の見本を見てください）。

## 参考にするときのヒント

- **`10-parts/` の部品**は、重ねると 32×32・4方向×3コマのキャラになる（同じ位置に描かれている）。体（body）→服（clothes）→髪（hair）→帽子（hat）の順に重ねる。配布素材をそのまま主人公にせず、**部品の形や陰影を参考にオリジナルのキャラを描く**のに向く。
- アイコン（`08-objects-items/oga-icon-*`）は 32×32 で、輪郭線・光の当たり方・色数の少なさの手本になる。
- ぴぽやの `pipoya-wolf-autotile-*` はウディタのオートタイルの並び（5段）。1回目の `pipoya-autotile-*`（展開したもの）と見比べると、オートタイルの仕組みが分かる。
- 描き方の要点は `docs/design/pixel-art-notes.md` と `docs/design/pixel-character-guide.md` にまとめてある。

## 規約

- **CC0（OpenGameArt）**: 商用利用・加工・再配布・ゲームへの組み込みは自由、クレジット不要。使った 199 ページすべてを 2026-09-30 に読み直し、ライセンス欄が CC0 だけであることを確かめた。
- **ぴぽや 無料素材利用規約**（https://pipoya.net/sozai/terms-of-use/ ）と各 readme（写しは `LICENSES/pipoya/`）: 商用利用可・加工可・ゲームへの組み込み可、クレジット・連絡不要。**素材そのものを素材として販売するのは禁止。** 無償の再配布は規約とともに。グラフィック合成器用パーツの readme にも同じ条件が書かれている。
- **このフォルダの絵を、素材として販売・再配布しないこと。**

## 選び方

2回目（`../pixel-library-2/README.md`）と同じ厳しさで選んだ。
1. 規約: 上のとおり。
2. 説明文の全文を読み、既存のゲームの絵・既存のゲームのために作られた（使われた）絵・既存作品に似せた絵・ゲームジャム作品の絵・由来があいまいな絵・AIや3Dや写真から作った絵を外した（例: Tuxemon・Stendhal・FLARE・Frogatto・Minecraft 用の絵、有名作品に似せたと書かれたもの、公開済みゲームの絵）。
3. ドット絵か: 色数・半透明を数え、縮小一覧を目で見て、なめらかな絵・文字入り・3D風の絵・白や単色の背景だけのものを外した。
4. 全年齢向け: ぴぽやの現代の人物のうち、下着・水着・ナイトワークの絵は外した。
5. 重複: これまでの素材と画素が同じものを外した。

## 配布元の一覧

| 配布元 | 素材 | 作者 | 規約 | 枚数 |
|---|---|---|---|---|
| ぴぽや倉庫 | [RPGキャラ基本セット（キャラチップ.zip）](https://pipoya.net/sozai/assets/charachip/character-chip-1/) | ぴぽや | ぴぽや 無料素材利用規約 | 20 |
| ぴぽや倉庫 | [ぴぽや32×32グラフィック合成器用パーツ（キャラを組み立てる部品）](https://pipoya.net/sozai/assets/charachip/character-chip-2/) | ぴぽや | ぴぽや 無料素材利用規約 | 235 |
| ぴぽや倉庫 | [ぴぽやキャラチップ32出力素材（ぴぽや32×32 出力画像＋α）](https://pipoya.net/sozai/assets/charachip/character-chip-2/) | ぴぽや | ぴぽや 無料素材利用規約 | 143 |
| ぴぽや倉庫 | [ウディタ２用マップセット（ウディタ2_32x32mapchip_20210215.zip）](https://pipoya.net/sozai/assets/map-chip_tileset32/) | ぴぽや | ぴぽや 無料素材利用規約 | 33 |
| OpenGameArt | ['SHROOMBLADE 2 SIZES](https://opengameart.org/content/shroomblade-2-sizes) | GoopyBus | CC0 1.0 | 2 |
| OpenGameArt | [1-Bit Doomcrypt Kit](https://opengameart.org/content/1-bit-doomcrypt-kit) | B77345-100 | CC0 1.0 | 6 |
| OpenGameArt | [1-Bit Doomgeon Kit](https://opengameart.org/content/1-bit-doomgeon-kit) | B77345-100 | CC0 1.0 | 10 |
| OpenGameArt | [1-Bit Doomland Kit](https://opengameart.org/content/1-bit-doomland-kit) | B77345-100 | CC0 1.0 | 9 |
| OpenGameArt | [1-Bit Graveyard Pixel Art Asset Pack](https://opengameart.org/content/1-bit-graveyard-pixel-art-asset-pack) | Fava Beans | CC0 1.0 | 2 |
| OpenGameArt | [16-bit skeleton](https://opengameart.org/content/16-bit-skeleton) | jhanson9012 | CC0 1.0 | 1 |
| OpenGameArt | [16x16 Ant Enemies](https://opengameart.org/content/16x16-ant-enemies) | ARoachIFoundOnMyPillow | CC0 1.0 | 2 |
| OpenGameArt | [16x16 Dungeon Tiles](https://opengameart.org/content/16x16-dungeon-tiles) | ETTiNGRiNDER | CC0 1.0 | 2 |
| OpenGameArt | [16x16 Flies](https://opengameart.org/content/16x16-flies) | ARoachIFoundOnMyPillow | CC0 1.0 | 1 |
| OpenGameArt | [16x16 Sprite Ninji](https://opengameart.org/content/16x16-sprite-ninji) | One To Zero | CC0 1.0 | 1 |
| OpenGameArt | [16x16 Square Block Variations](https://opengameart.org/content/16x16-square-block-variations) | etqws3 | CC0 1.0 | 1 |
| OpenGameArt | [1bit Graphics Collection](https://opengameart.org/content/1bit-graphics-collection) | Drummyfish | CC0 1.0 | 1 |
| OpenGameArt | [2D Enemy Characters Pack [20x20]](https://opengameart.org/content/2d-enemy-characters-pack-20x20) | RottingPixels | CC0 1.0 | 1 |
| OpenGameArt | [2D Female Character Animated Elfia](https://opengameart.org/content/2d-female-character-animated-elfia) | nyarlko | CC0 1.0 | 1 |
| OpenGameArt | [2D Slime Animated](https://opengameart.org/content/2d-slime-animated) | SpinachChicken | CC0 1.0 | 1 |
| OpenGameArt | [30 sprites made in 30 minutes](https://opengameart.org/content/30-sprites-made-in-30-minutes) | russpuppy | CC0 1.0 | 1 |
| OpenGameArt | [32x32 Explosion](https://opengameart.org/content/32x32-explosion) | diamonddmgirl | CC0 1.0 | 1 |
| OpenGameArt | [43 8x8 food tiles](https://opengameart.org/content/43-8x8-food-tiles) | ZakChaos | CC0 1.0 | 1 |
| OpenGameArt | [496 pixel art icons for medieval/fantasy RPG](https://opengameart.org/content/496-pixel-art-icons-for-medievalfantasy-rpg) | Henrique Lazarini (7Soul1) | CC0 1.0 | 177 |
| OpenGameArt | [8x8 8-bit Styled Grassland Tileset](https://opengameart.org/content/8x8-8-bit-styled-grassland-tileset) | ImpossibleRealms | CC0 1.0 | 1 |
| OpenGameArt | [A statue of a knight in pixel art.](https://opengameart.org/content/a-statue-of-a-knight-in-pixel-art) | Kitsune64 | CC0 1.0 | 1 |
| OpenGameArt | [Alex's fun starter pack](https://opengameart.org/content/alexs-fun-starter-pack) | Fooliery | CC0 1.0 | 1 |
| OpenGameArt | [Angel](https://opengameart.org/content/angel) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [ANGEL - Pixel Character Spritesheet](https://opengameart.org/content/angel-pixel-character-spritesheet) | ben0bi | CC0 1.0 | 1 |
| OpenGameArt | [Animated Fire](https://opengameart.org/content/animated-fire) | BenHickling | CC0 1.0 | 1 |
| OpenGameArt | [Animated Fires](https://opengameart.org/content/animated-fires) | stealthix | CC0 1.0 | 1 |
| OpenGameArt | [archer [Static] [64x64]](https://opengameart.org/content/archer-static-64x64) | LordNeo | CC0 1.0 | 1 |
| OpenGameArt | [Archer Elf](https://opengameart.org/content/archer-elf) | Ian Peter | CC0 1.0 | 1 |
| OpenGameArt | [Assorted 32x32 creatures](https://opengameart.org/content/assorted-32x32-creatures) | AndHeGames | CC0 1.0 | 1 |
| OpenGameArt | [Basic Rpg Icons](https://opengameart.org/content/basic-rpg-icons) | Pixel Archer | CC0 1.0 | 1 |
| OpenGameArt | [Beach tileset](https://opengameart.org/content/beach-tileset) | ChikenwingJJA | CC0 1.0 | 1 |
| OpenGameArt | [Bear](https://opengameart.org/content/bear-0) | Sketlux | CC0 1.0 | 1 |
| OpenGameArt | [Bear Warrior](https://opengameart.org/content/bear-warrior) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Beginner TileSet OUT NOW!](https://opengameart.org/content/beginner-tileset-out-now) | DesolateCorp | CC0 1.0 | 1 |
| OpenGameArt | [Behrs 2,500 Pixel Spears 32x32 Archive](https://opengameart.org/content/behrs-2500-pixel-spears-32x32-archive) | Behrtron | CC0 1.0 | 1 |
| OpenGameArt | [Behrs 4,500 Pixel Swords 32x32 Archive](https://opengameart.org/content/behrs-4500-pixel-swords-32x32-archive) | Behrtron | CC0 1.0 | 1 |
| OpenGameArt | [Benza](https://opengameart.org/content/benza) | megupets | CC0 1.0 | 1 |
| OpenGameArt | [Bird](https://opengameart.org/content/bird-2) | rmazanek | CC0 1.0 | 1 |
| OpenGameArt | [Bird asset](https://opengameart.org/content/bird-asset) | EclipseDaOne | CC0 1.0 | 1 |
| OpenGameArt | [Bomb Animation 24p DX](https://opengameart.org/content/bomb-animation-24p-dx) | Umplix | CC0 1.0 | 1 |
| OpenGameArt | [Boy Npc](https://opengameart.org/content/boy-npc) | Blind Harpy Gamedev | CC0 1.0 | 2 |
| OpenGameArt | [Cat sprites](https://opengameart.org/content/cat-sprites) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [CC0 Currency](https://opengameart.org/content/cc0-currency) | ZaninDevelopers | CC0 1.0 | 2 |
| OpenGameArt | [CC0 Plant Clutter](https://opengameart.org/content/cc0-plant-clutter) | ZaninDevelopers | CC0 1.0 | 1 |
| OpenGameArt | [Character Animations (Caveman)](https://opengameart.org/content/character-animations-caveman) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [Chicken Sprites](https://opengameart.org/content/chicken-sprites) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Chinese Icons](https://opengameart.org/content/chinese-icons) | Pixel Archer | CC0 1.0 | 1 |
| OpenGameArt | [Classical Ruin Tiles](https://opengameart.org/content/classical-ruin-tiles) | surt | CC0 1.0 | 1 |
| OpenGameArt | [Colony sim assets](https://opengameart.org/content/colony-sim-assets) | Buch | CC0 1.0 | 1 |
| OpenGameArt | [Cowboys vs Zombies](https://opengameart.org/content/cowboys-vs-zombies) | BananaGirl | CC0 1.0 | 2 |
| OpenGameArt | [Crops CC0](https://opengameart.org/content/crops-cc0) | SnoopethDuckDuck | CC0 1.0 | 2 |
| OpenGameArt | [Cute 16x16 Animal Icons](https://opengameart.org/content/cute-16x16-animal-icons) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [cute frog](https://opengameart.org/content/cute-frog) | kotnaszynce | CC0 1.0 | 1 |
| OpenGameArt | [Cutted tree + roots](https://opengameart.org/content/cutted-tree-roots) | MiguelOliveira3D | CC0 1.0 | 1 |
| OpenGameArt | [Dancing Seaweed](https://opengameart.org/content/dancing-seaweed-0) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Dino RPG Character](https://opengameart.org/content/dino-rpg-character) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Dog/Wolf spritesheet](https://opengameart.org/content/dogwolf-spritesheet) | Cough-E | CC0 1.0 | 1 |
| OpenGameArt | [Dutone tileset objects and character](https://opengameart.org/content/dutone-tileset-objects-and-character) | Eris | CC0 1.0 | 1 |
| OpenGameArt | [Enemy Game Character - Cute Spider](https://opengameart.org/content/enemy-game-character-cute-spider) | bevouliin.com | CC0 1.0 | 1 |
| OpenGameArt | [Enemy Sprite](https://opengameart.org/content/enemy-sprite-0) | Teapot | CC0 1.0 | 1 |
| OpenGameArt | [Explosion](https://opengameart.org/content/explosion-3) | Sogomn | CC0 1.0 | 1 |
| OpenGameArt | [Explosion](https://opengameart.org/content/explosion-7) | BenHickling | CC0 1.0 | 1 |
| OpenGameArt | [Explosion Animation](https://opengameart.org/content/explosion-animation-1) | den_yes | CC0 1.0 | 1 |
| OpenGameArt | [Faces of Surt](https://opengameart.org/content/faces-of-surt) | Ragnar Random | CC0 1.0 | 1 |
| OpenGameArt | [Fantasy Swords 16X16 pack 1.0](https://opengameart.org/content/fantasy-swords-16x16-pack-10) | IshtartPixels | CC0 1.0 | 1 |
| OpenGameArt | [Fire Circle FX](https://opengameart.org/content/fire-circle-fx) | Matriax | CC0 1.0 | 1 |
| OpenGameArt | [Fire Slime](https://opengameart.org/content/fire-slime) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [fish](https://opengameart.org/content/fish-0) | kotnaszynce | CC0 1.0 | 1 |
| OpenGameArt | [Floor is lava](https://opengameart.org/content/floor-is-lava) | Kipperfalcon | CC0 1.0 | 1 |
| OpenGameArt | [Flying Monster Frames 16x16](https://opengameart.org/content/flying-monster-frames-16x16) | awesomeduck | CC0 1.0 | 2 |
| OpenGameArt | [Flying Snake Monster Hero](https://opengameart.org/content/flying-snake-monster-hero) | marionline | CC0 1.0 | 1 |
| OpenGameArt | [Free Pixel Effects Pack](https://opengameart.org/content/free-pixel-effects-pack) | CodeManu | CC0 1.0 | 1 |
| OpenGameArt | [Frog](https://opengameart.org/content/frog) | Pixel Archer | CC0 1.0 | 1 |
| OpenGameArt | [Frog [Classic Hero]](https://opengameart.org/content/frog-classic-hero) | xxgicoxx | CC0 1.0 | 1 |
| OpenGameArt | [Froggy](https://opengameart.org/content/froggy) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [fwoggy](https://opengameart.org/content/fwoggy) | kotnaszynce | CC0 1.0 | 1 |
| OpenGameArt | [Game icons](https://opengameart.org/content/game-icons) | Kenney | CC0 1.0 | 1 |
| OpenGameArt | [German Shepherd](https://opengameart.org/content/german-shepherd-0) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Ghost](https://opengameart.org/content/ghost-3) | Robotrage | CC0 1.0 | 1 |
| OpenGameArt | [Ghost](https://opengameart.org/content/ghost-5) | StygianChrno | CC0 1.0 | 1 |
| OpenGameArt | [GOBLIN FREE PIXELART](https://opengameart.org/content/goblin-free-pixelart) | thekingphoenix | CC0 1.0 | 1 |
| OpenGameArt | [Graveyard Goon](https://opengameart.org/content/graveyard-goon) | Admurin | CC0 1.0 | 1 |
| OpenGameArt | [Green Slime](https://opengameart.org/content/green-slime-1) | Kimicharu | CC0 1.0 | 1 |
| OpenGameArt | [Green Temple Autotile Set](https://opengameart.org/content/green-temple-autotile-set) | Ultrahuntr | CC0 1.0 | 1 |
| OpenGameArt | [Grey Roguelike Tileset](https://opengameart.org/content/grey-roguelike-tileset) | Sardonic | CC0 1.0 | 1 |
| OpenGameArt | [Ground Tiles](https://opengameart.org/content/ground-tiles-2) | Raijin | CC0 1.0 | 1 |
| OpenGameArt | [Half-Human NPCs](https://opengameart.org/content/half-human-npcs) | marionline | CC0 1.0 | 1 |
| OpenGameArt | [Halloween characters](https://opengameart.org/content/halloween-characters) | Armando Rodarte | CC0 1.0 | 1 |
| OpenGameArt | [Hedge Maze and Ice Palace Tiles](https://opengameart.org/content/hedge-maze-and-ice-palace-tiles) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Hit Die Icons](https://opengameart.org/content/hit-die-icons) | OptimusGnu | CC0 1.0 | 1 |
| OpenGameArt | [Home Tile Set](https://opengameart.org/content/home-tile-set) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [Horned Skeletons](https://opengameart.org/content/horned-skeletons) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Industrial Mine Tileset](https://opengameart.org/content/industrial-mine-tileset) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Inventory filter icons](https://opengameart.org/content/inventory-filter-icons) | twiswist | CC0 1.0 | 2 |
| OpenGameArt | [Kawaii Slime sprites](https://opengameart.org/content/kawaii-slime-sprites) | Graveheartart | CC0 1.0 | 1 |
| OpenGameArt | [King Rat](https://opengameart.org/content/king-rat) | djantosh10 | CC0 1.0 | 1 |
| OpenGameArt | [Kiwi Sprites](https://opengameart.org/content/kiwi-sprites) | Shepardskin | CC0 1.0 | 1 |
| OpenGameArt | [Knight spritesheet](https://opengameart.org/content/knight-spritesheet) | marqueeplier | CC0 1.0 | 2 |
| OpenGameArt | [Kudzu leaves pixel art](https://opengameart.org/content/kudzu-leaves-pixel-art) | hatmix | CC0 1.0 | 1 |
| OpenGameArt | [Lamps Lights n Torches](https://opengameart.org/content/lamps-lights-n-torches) | Reactorcore | CC0 1.0 | 2 |
| OpenGameArt | [Lava tileset](https://opengameart.org/content/lava-tileset) | batica | CC0 1.0 | 1 |
| OpenGameArt | [little weirdos](https://opengameart.org/content/little-weirdos) | pebonius | CC0 1.0 | 3 |
| OpenGameArt | [MEDICINES](https://opengameart.org/content/medicines) | NaranjaIncógnita | CC0 1.0 | 1 |
| OpenGameArt | [MiniWorld Sprites](https://opengameart.org/content/miniworld-sprites) | Shade | CC0 1.0 | 76 |
| OpenGameArt | [Misc props](https://opengameart.org/content/misc-props) | .bee | CC0 1.0 | 1 |
| OpenGameArt | [Miscellaneous pixel art.](https://opengameart.org/content/miscellaneous-pixel-art) | darkagegames ほか: darkagegames, surt | CC0 1.0 | 1 |
| OpenGameArt | [Monster Builder Pack](https://opengameart.org/content/monster-builder-pack) | Kenney | CC0 1.0 | 1 |
| OpenGameArt | [Mountain Tileset](https://opengameart.org/content/mountain-tileset) | ImpossibleRealms | CC0 1.0 | 1 |
| OpenGameArt | [Nat's 8x8 Starter Pack](https://opengameart.org/content/nats-8x8-starter-pack) | nateonus | CC0 1.0 | 16 |
| OpenGameArt | [Nature Props Surface Forest](https://opengameart.org/content/nature-props-surface-forest) | Reactorcore | CC0 1.0 | 3 |
| OpenGameArt | [NPC Characters (20)](https://opengameart.org/content/npc-characters-20) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [Orange Fat Cat](https://opengameart.org/content/orange-fat-cat) | megupets | CC0 1.0 | 1 |
| OpenGameArt | [Orange Spider Game Character](https://opengameart.org/content/orange-spider-game-character) | bevouliin.com | CC0 1.0 | 1 |
| OpenGameArt | [Piskel cute ghost](https://opengameart.org/content/piskel-cute-ghost) | PINKCANNON | CC0 1.0 | 1 |
| OpenGameArt | [Pixel art animations and enemies from 'Gop go go' project](https://opengameart.org/content/pixel-art-animations-and-enemies-from-gop-go-go-project) | madmedicsoft | CC0 1.0 | 1 |
| OpenGameArt | [Pixel art Bomb animation](https://opengameart.org/content/pixel-art-bomb-animation) | momopey | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Art Circular Table](https://opengameart.org/content/pixel-art-circular-table) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Pixel art explosion animation](https://opengameart.org/content/pixel-art-explosion-animation-0) | floatvoid | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Art Ghosts](https://opengameart.org/content/pixel-art-ghosts) | bonzille | CC0 1.0 | 2 |
| OpenGameArt | [pixel art top down soldiers](https://opengameart.org/content/pixel-art-top-down-soldiers) | tbbk | CC0 1.0 | 1 |
| OpenGameArt | [Pixel bat sprite](https://opengameart.org/content/pixel-bat-sprite) | tbbk | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Bug](https://opengameart.org/content/pixel-bug) | Umplix | CC0 1.0 | 1 |
| OpenGameArt | [Pixel frog](https://opengameart.org/content/pixel-frog-0) | scofanogd | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Frog (16*16)](https://opengameart.org/content/pixel-frog-1616) | scriptoy | CC0 1.0 | 1 |
| OpenGameArt | [Pixel FX Pack](https://opengameart.org/content/pixel-fx-pack) | CodeManu | CC0 1.0 | 1 |
| OpenGameArt | [pixel horse](https://opengameart.org/content/pixel-horse) | alizard | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Man](https://opengameart.org/content/pixel-man) | Shawneth | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Pine Tree Assets (10 Pack)](https://opengameart.org/content/pixel-pine-tree-assets-10-pack) | pistachio | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Rabbit People](https://opengameart.org/content/pixel-rabbit-people) | diamonddmgirl | CC0 1.0 | 1 |
| OpenGameArt | [Pixel Tree Frog Sprite](https://opengameart.org/content/pixel-tree-frog-sprite) | ieppei | CC0 1.0 | 1 |
| OpenGameArt | [Pixel wizard girl](https://opengameart.org/content/pixel-wizard-girl) | mailbun | CC0 1.0 | 1 |
| OpenGameArt | [pixel wolf](https://opengameart.org/content/pixel-wolf) | alizard | CC0 1.0 | 1 |
| OpenGameArt | [Pixelated Goblin](https://opengameart.org/content/pixelated-goblin) | markoxx2 | CC0 1.0 | 1 |
| OpenGameArt | [Plant Pets](https://opengameart.org/content/plant-pets) | Aswino | CC0 1.0 | 1 |
| OpenGameArt | [Potions 32x32](https://opengameart.org/content/potions-32x32) | Leozlk | CC0 1.0 | 1 |
| OpenGameArt | [Potions Pack](https://opengameart.org/content/potions-pack) | FunnyDude | CC0 1.0 | 1 |
| OpenGameArt | [Psycho Furs!](https://opengameart.org/content/psycho-furs) | Spring Spring ほか: withthelove | CC0 1.0 | 1 |
| OpenGameArt | [Puny Characters](https://opengameart.org/content/puny-characters) | Shade | CC0 1.0 | 13 |
| OpenGameArt | [Purple Ghost Bunny Sprite](https://opengameart.org/content/purple-ghost-bunny-sprite) | cwendeku | CC0 1.0 | 1 |
| OpenGameArt | [Purple Puma pixel art spritesheet](https://opengameart.org/content/purple-puma-pixel-art-spritesheet) | nightgane | CC0 1.0 | 1 |
| OpenGameArt | [random assets](https://opengameart.org/content/random-assets) | megupets | CC0 1.0 | 1 |
| OpenGameArt | [Ranger [Animated]](https://opengameart.org/content/ranger-animated) | DezrasDragons | CC0 1.0 | 1 |
| OpenGameArt | [Rat](https://opengameart.org/content/rat) | djantosh10 | CC0 1.0 | 1 |
| OpenGameArt | [Ring Explosion](https://opengameart.org/content/ring-explosion) | BenHickling | CC0 1.0 | 1 |
| OpenGameArt | [Rose sprite](https://opengameart.org/content/rose-sprite) | Ergorius | CC0 1.0 | 1 |
| OpenGameArt | [Rough gems](https://opengameart.org/content/rough-gems) | mistergrey | CC0 1.0 | 1 |
| OpenGameArt | [round shield [64x64]](https://opengameart.org/content/round-shield-64x64) | LordNeo | CC0 1.0 | 1 |
| OpenGameArt | [RPG - Sprites - Blu Guy](https://opengameart.org/content/rpg-sprites-blu-guy) | Ulti | CC0 1.0 | 1 |
| OpenGameArt | [RPG Asset Character 'Centurion' NES](https://opengameart.org/content/rpg-asset-character-centurion-nes) | Chasersgaming | CC0 1.0 | 2 |
| OpenGameArt | [RPG Asset Character 'Zombie' NES](https://opengameart.org/content/rpg-asset-character-zombie-nes) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [RPG Character 'Knight' SMS](https://opengameart.org/content/rpg-character-knight-sms) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [RPG Character 'Ranger' SMS](https://opengameart.org/content/rpg-character-ranger-sms) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [RPG Goblin Knife Jab Animation Sprite Sheet](https://opengameart.org/content/rpg-goblin-knife-jab-animation-sprite-sheet) | Gman2099 | CC0 1.0 | 1 |
| OpenGameArt | [Rpg House](https://opengameart.org/content/rpg-house) | Angel | CC0 1.0 | 1 |
| OpenGameArt | [RPG Sprite Sheet](https://opengameart.org/content/rpg-sprite-sheet) | Healy | CC0 1.0 | 1 |
| OpenGameArt | [Scary Ghost](https://opengameart.org/content/scary-ghost) | StygianChrno | CC0 1.0 | 1 |
| OpenGameArt | [Shattering Boulder](https://opengameart.org/content/shattering-boulder) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Sideview Goblin by lucasserapiao](https://opengameart.org/content/sideview-goblin-by-lucasserapiao) | Dwapook | CC0 1.0 | 1 |
| OpenGameArt | [Simple RPG Weapons Icon (16x16)](https://opengameart.org/content/simple-rpg-weapons-icon-16x16) | CapivarAzul | CC0 1.0 | 1 |
| OpenGameArt | [Singular Direction Monsters + Battlers](https://opengameart.org/content/singular-direction-monsters-battlers) | Some Weirdo | CC0 1.0 | 4 |
| OpenGameArt | [Sinkar Birber](https://opengameart.org/content/sinkar-birber) | Spring Spring | CC0 1.0 | 1 |
| OpenGameArt | [Skeleton](https://opengameart.org/content/skeleton-4) | rehcub | CC0 1.0 | 1 |
| OpenGameArt | [Skeleton Sprite](https://opengameart.org/content/skeleton-sprite) | r0ar | CC0 1.0 | 1 |
| OpenGameArt | [Skull Game Obstacle](https://opengameart.org/content/skull-game-obstacle) | bevouliin.com | CC0 1.0 | 1 |
| OpenGameArt | [Skulls](https://opengameart.org/content/skulls) | Doodle | CC0 1.0 | 1 |
| OpenGameArt | [slime](https://opengameart.org/content/slime-5) | troler_24 | CC0 1.0 | 1 |
| OpenGameArt | [Slime](https://opengameart.org/content/slime-6) | Soloslime | CC0 1.0 | 1 |
| OpenGameArt | [Slime Emojis](https://opengameart.org/content/slime-emojis) | SCaydi | CC0 1.0 | 1 |
| OpenGameArt | [Slimes 32x32](https://opengameart.org/content/slimes-32x32) | RodHakGames | CC0 1.0 | 1 |
| OpenGameArt | [Snake](https://opengameart.org/content/snake-0) | Sketlux | CC0 1.0 | 1 |
| OpenGameArt | [Snake 2d](https://opengameart.org/content/snake-2d) | Zelta | CC0 1.0 | 1 |
| OpenGameArt | [Snake on an old stump](https://opengameart.org/content/snake-on-an-old-stump) | Angry Amish | CC0 1.0 | 1 |
| OpenGameArt | [Spider](https://opengameart.org/content/spider-3) | smark | CC0 1.0 | 1 |
| OpenGameArt | [spider set](https://opengameart.org/content/spider-set) | aman7 | CC0 1.0 | 1 |
| OpenGameArt | [Spider with cut leg](https://opengameart.org/content/spider-with-cut-leg) | KindlyFire | CC0 1.0 | 1 |
| OpenGameArt | [Spooky House](https://opengameart.org/content/spooky-house) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [Sprites And Icons Pack](https://opengameart.org/content/sprites-and-icons-pack) | PucciGames | CC0 1.0 | 1 |
| OpenGameArt | [Sprites from old project - forest objects and character](https://opengameart.org/content/sprites-from-old-project-forest-objects-and-character) | TheNess | CC0 1.0 | 2 |
| OpenGameArt | [Tile Set Pack 17](https://opengameart.org/content/tile-set-pack-17) | Chasersgaming | CC0 1.0 | 1 |
| OpenGameArt | [Tiny Slime](https://opengameart.org/content/tiny-slime) | gustavoasilveira | CC0 1.0 | 1 |
| OpenGameArt | [Toon Characters 1](https://opengameart.org/content/toon-characters-1) | Kenney | CC0 1.0 | 2 |
| OpenGameArt | [Top down 2d pixel art](https://opengameart.org/content/top-down-2d-pixel-art) | graphicBeardo | CC0 1.0 | 1 |
| OpenGameArt | [Top Down Asset Pack 1.0](https://opengameart.org/content/top-down-asset-pack-10) | IshtartPixels | CC0 1.0 | 45 |
| OpenGameArt | [Top View Crossbow man](https://opengameart.org/content/top-view-crossbow-man) | Cliipso | CC0 1.0 | 1 |
| OpenGameArt | [tree falling over](https://opengameart.org/content/tree-falling-over) | sodri | CC0 1.0 | 1 |
| OpenGameArt | [tree with small details](https://opengameart.org/content/tree-with-small-details) | Angry Amish | CC0 1.0 | 1 |
| OpenGameArt | [unreleased scraps](https://opengameart.org/content/unreleased-scraps) | pebonius | CC0 1.0 | 2 |
| OpenGameArt | [Upwards Floating Soul](https://opengameart.org/content/upwards-floating-soul) | patvanmackelberg | CC0 1.0 | 1 |
| OpenGameArt | [Walking Knight](https://opengameart.org/content/walking-knight-0) | utkdub | CC0 1.0 | 1 |
| OpenGameArt | [Warped Shooting Fx](https://opengameart.org/content/warped-shooting-fx) | ansimuz | CC0 1.0 | 1 |
| OpenGameArt | [Wasp](https://opengameart.org/content/wasp-0) | Spring Spring ほか: Puffolotti | CC0 1.0 | 1 |
| OpenGameArt | [Water Aqua Layer System](https://opengameart.org/content/water-aqua-layer-system) | Reactorcore | CC0 1.0 | 2 |
| OpenGameArt | [White wing, 32x32](https://opengameart.org/content/white-wing-32x32) | twiswist | CC0 1.0 | 1 |
| OpenGameArt | [Wizard](https://opengameart.org/content/wizard-7) | lylfDW | CC0 1.0 | 1 |
| OpenGameArt | [Wolf](https://opengameart.org/content/wolf-3) | carnageddon | CC0 1.0 | 1 |
| OpenGameArt | [Wolf](https://opengameart.org/content/wolf-4) | Sketlux | CC0 1.0 | 1 |
| OpenGameArt | [Wolf Spirit](https://opengameart.org/content/wolf-spirit) | zonked | CC0 1.0 | 2 |
| OpenGameArt | [Zombibi](https://opengameart.org/content/zombibi) | megupets | CC0 1.0 | 1 |
| OpenGameArt | [Zombie](https://opengameart.org/content/zombie-6) | NiceGraphic | CC0 1.0 | 1 |
