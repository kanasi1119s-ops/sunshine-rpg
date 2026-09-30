# RPG用のドット絵2000枚の学習記録（2026-09-30）

人間の依頼「RPG用のドット絵を2000枚ほど学習してきて」で行った学習の記録です。200枚（`pixel-art-study-200.md`）と同じ物差しで、10倍の枚数を測り、200枚で分かったことが本当に一般的かを確かめました。学んだ技法は `docs/design/pixel-art-notes.md` の「2000枚で確かめ直したこと」に書いています。

## 守ったこと
- **利用条件がはっきりした無料素材だけ**: OpenGameArt の CC0（権利放棄）の作品、Kenney（CC0）、ぴぽやの無料素材（規約は `docs/assets-credits.md`）。161の配布元すべてについて、ライセンス欄が CC0 だけであることを確かめた（ぴぽやは確認済みの無料素材規約）
- **外したもの**: 説明文で既存ゲームの名前や「〜風」「〜のような」を名乗る作品（25件以上）、既存ゲームのための素材や他人の絵の改変、有料素材、説明文や同梱の文書で AI に触れている作品（「AIツールは使っていない」と明記した作者の作品を含め、念のため5件）
- **絵そのものはリポジトリに入れていない**。作業用の一時フォルダで分析し、ここには数値と出典だけを書く。今回の絵をゲームにそのまま使うことはしない

## やり方
1. OpenGameArt で CC0 に絞って約1,100件を検索し、上の条件で1件ずつ確かめ、RPG に関係するもの（横スクロール用・乗り物・SFなどを除く）を選んだ。前回までの素材と合わせて223の配布元から、重複を除いた候補を14,498枚切り出した
2. **ドット絵でないもの・学習に向かないものを外した**（計5,820枚）:
   - 配布元ごと: ベクター画・塗り絵・写真のようなもの（Animal Pack Redux、Bevouliin 系、2D Game Character Pack、塗り絵風の草原タイル、public-domain-pack、generic-items など）、RPG と関係の薄いもの（横スクロールの格闘、回る地球）… 2,496枚
   - 背景色（マゼンタ）が抜けていない切れ端・枠 … 1,021枚
   - キャラクター等のシートの塗りつぶし部分 … 615枚
   - にじんだ・塗り絵のような小片（面積のわりに色が多すぎるもの。ぴぽやの1.25倍に拡大された版を含む）… 501枚
   - 文字・見出し … 147枚
3. 残りから、**キャラ450・モンスター339・地形611・小物と建物450・混在126・顔24、計2000枚**を選んだ。1つの配布元から取るのは40枚まで（全体の2%）にして、161の配布元に散らした。顔の絵は、条件に合うものが24枚しか見つからなかった
4. 2000枚すべてを数値にした（200枚のときと同じ物差し）
5. 2000枚を200枚ずつの一覧画像10枚にして、**全体を目で見た**。混ざり物を見つけては外す作業を4回くり返した。1枚ずつ拡大して見たわけではなく、目で見たのは縮小した一覧（1枚あたり約50ドット四方）。最後の一覧でも、見出し文字など学習に向かないものが1%ほど残っている
6. 種類（キャラ・モンスターなど）は、配布元の名前でおおよそ分けた。地形タイルの中に混ざっているキャラ・敵・小物は「混在」にした。種類分けは完全ではない

## 測った数値（中央値。かっこ内は25%〜75%）

| 物差し | キャラ(450) | モンスター(339) | 地形(611) | 小物・建物(450) | 混在(126) | 顔(24) | 全体(2000) |
|---|---|---|---|---|---|---|---|
| 幅（ドット） | 16（13〜20） | 23（14〜40） | 16（16〜16） | 14（10〜20） | 16（12〜41） | 32（32〜61） | 16（12〜21） |
| 高さ（ドット） | 22（15〜40） | 24（16〜34） | 16（16〜16） | 15（12〜21） | 16（14〜41） | 31（30〜77） | 16（14〜28） |
| 色数 | 9（4〜16） | 7（5〜10） | 5（3〜7） | 6（4〜10） | 5（4〜8） | 8（6〜9） | 6（4〜10） |
| 明暗の幅 | 0.89（0.68〜1.00） | 0.83（0.60〜0.92） | 0.49（0.36〜0.67） | 0.61（0.42〜0.77） | 0.50（0.33〜0.68） | 0.82（0.82〜1.00） | 0.66（0.43〜0.87） |
| 彩度の最大 | 0.91（0.79〜1.00） | 0.88（0.72〜1.00） | 0.62（0.44〜0.84） | 0.79（0.59〜0.96） | 0.65（0.52〜0.86） | 0.73（0.73〜0.73） | 0.79（0.58〜1.00） |
| 外周の明るさ÷内側 | 0.13（0.00〜0.57） | 0.58（0.28〜0.90） | - | 0.62（0.40〜0.82） | 0.81（0.58〜0.98） | 0.64（0.61〜0.66） | 0.53（0.14〜0.80） |
| 外周のうち黒に近い割合 | 0.96（0.10〜1.00） | 0.00（0.00〜0.84） | - | 0.00（0.00〜0.21） | 0.00（0.00〜0.00） | 0.00（0.00〜0.00） | 0.00（0.00〜0.97） |
| 左上−右下の明るさ | 0.04（-0.02〜0.11） | 0.04（-0.02〜0.12） | 0.00（-0.05〜0.08） | 0.05（-0.03〜0.15） | 0.02（-0.02〜0.10） | 0.16（0.10〜0.22） | 0.03（-0.03〜0.11） |
| 孤立ドットの割合 | 0.044（0.011〜0.098） | 0.045（0.016〜0.094） | 0.027（0.004〜0.062） | 0.080（0.018〜0.190） | 0.029（0.000〜0.059） | 0.052（0.031〜0.081） | 0.040（0.010〜0.099） |
| 市松ディザの割合 | 0.005（0.000〜0.019） | 0.006（0.000〜0.016） | 0.000（0.000〜0.022） | 0.005（0.000〜0.027） | 0.000（0.000〜0.023） | 0.020（0.015〜0.025） | 0.005（0.000〜0.021） |
| いちばん暗い色の明るさ | 0.00（0.00〜0.07） | 0.08（0.03〜0.19） | 0.23（0.09〜0.42） | 0.13（0.11〜0.26） | 0.19（0.13〜0.35） | 0.18（0.18〜0.18） | 0.13（0.00〜0.28） |

- 色数の帯（全体）: 2〜4色 671枚・5〜8色 709枚・9〜16色 393枚・17色以上 227枚。**地形の半分近く（611枚中284枚）は2〜4色**で作られている
- 縁取りの型:
  - キャラ: 黒に近い 66%・色つきの暗い縁 8%・はっきりしない 26%
  - モンスター: 黒に近い 27%・色つきの暗い縁 16%・はっきりしない 58%
  - 小物・建物: 黒に近い 15%・色つきの暗い縁 24%・はっきりしない 61%
- 色相シフト（影を青・紫側、光を黄側へずらす）: 9色以上の絵に限っても、キャラ 61%・小物 50%・モンスター 45%・地形 35%。明るさだけを変えるランプも多い（地形の53%、モンスターの48%はほぼずれなし）
- 高さの帯: キャラは16以下143・17〜24は108・25〜32は43・33以上156。モンスターは16以下123・17〜24は55・25〜32は74・33以上87

## 200枚のときとの違い（2000枚で確かめ直したこと）

| 項目 | 200枚 | 2000枚 | 結論 |
|---|---|---|---|
| キャラの外周の黒い縁取り | 81% | 66% | 多数派だが、決まりではない |
| 地形の明暗の幅 | 0.48 | 0.49 | **同じ。地形は控えめ、はっきり確かめられた** |
| キャラの明暗の幅 | 0.90 | 0.89 | **同じ。キャラは最大、はっきり確かめられた** |
| 小物の縁取り | 黒は0% | 黒に近い15%・色つき24%・はっきりしない61% | 「黒ではなく物の色の暗い版」か「縁を取らない」。黒は少数 |
| 色相シフト（寒色の影） | 6〜8割 | 3.5〜6割 | **決まりではない。** 解説は勧めるが、明るさだけのランプも普通に使われている。色数が多いキャラ・小物ほど使われる |
| 孤立ドット（地形） | 3% | 2.7% | 同じ。地形は2〜4ドットの粒で質感を出す |
| ディザ | 1% | 0.5% | ほとんど使われない |

## 学習した素材（161の配布元。すべて無料。絵はリポジトリに入れていない）

| 作品名 | 作者 | 入手元 | ライセンス | 枚数 | 種類 |
|---|---|---|---|---|---|
| 32x32 colorful slimes! | AndHeGames | https://opengameart.org/content/32x32-colorful-slimes | CC0 | 40 | モンスター40 |
| NPC and Enemies | Refo | https://opengameart.org/content/npc-and-enemies-0 | CC0 | 40 | モンスター40 |
| Simple unarmed wraith (Failed experiment) | Puffolotti | https://opengameart.org/content/simple-unarmed-wraith-failed-experiment | CC0 | 40 | モンスター40 |
| bushes | SpiderDave | https://opengameart.org/content/bushes-2 | CC0 | 37 | 小物・建物37 |
| LPC Simple staff | Dr. Jamgo | https://opengameart.org/content/lpc-simple-staff | CC0 | 37 | 小物・建物37 |
| Farming crops 16x16 | josehzz | https://opengameart.org/content/farming-crops-16x16 | CC0 | 37 | 小物・建物37 |
| Hero spritesheets (Ars Notoria) | Balmer | https://opengameart.org/content/hero-spritesheets-ars-notoria | CC0 | 37 | 小物・建物37 |
| Weapons for a roguelike | Master484 | https://opengameart.org/content/weapons-for-a-roguelike | CC0 | 37 | 小物・建物37 |
| Medieval RTS (120+) | Kenney | https://opengameart.org/content/medieval-rts-120 | CC0 | 36 | 小物・建物36 |
| RPG item set | Jetrel | https://opengameart.org/content/rpg-item-set | CC0 | 36 | 小物・建物36 |
| 2D Slime Animated (12 Different Colors) Unity Ready Prefab | nyarlko | https://opengameart.org/content/2d-slime-animated-12-different-colors-unity-ready-prefab | CC0 | 35 | モンスター35 |
| Flame creature | takeshi | https://opengameart.org/content/flame-creature | CC0 | 35 | モンスター35 |
| Gnomes | AntumDeluge | https://opengameart.org/content/gnomes | CC0 | 34 | キャラ34 |
| Roguelike Characters | Kenney | https://kenney.nl/assets/roguelike-characters | CC0 | 34 | キャラ34 |
| Pixel People | TokyoGeisha | https://opengameart.org/content/pixel-people | CC0 | 34 | キャラ34 |
| Puny Characters | Shade | https://opengameart.org/content/puny-characters | CC0 | 34 | キャラ34 |
| RPG Character 'Knight' (NES) | Chasersgaming | https://opengameart.org/content/rpg-character-knight-nes | CC0 | 34 | キャラ34 |
| RPG Character 'Ranger' (NES) | Chasersgaming | https://opengameart.org/content/rpg-character-ranger-nes | CC0 | 34 | キャラ34 |
| Various Walkcycle (8 characters) | Skab | https://opengameart.org/content/various-walkcycle-8-characters | CC0 | 34 | キャラ34 |
| Classic hero and baddies pack | GrafxKid | https://opengameart.org/content/classic-hero-and-baddies-pack | CC0 | 29 | モンスター29 |
| Animated Wild Animals | ScratchIO | https://opengameart.org/content/animated-wild-animals | CC0 | 27 | モンスター27 |
| Pixel farm and shack | pixel32 | https://opengameart.org/content/pixel-farm-and-shack | CC0 | 27 | 小物・建物27 |
| 16 x 16 Monster Items | ARoachIFoundOnMyPillow | https://opengameart.org/content/16-x-16-monster-items | CC0 | 26 | 小物・建物26 |
| Misc. Dark Fantasy Scenery Sprites | ETTiNGRiNDER | https://opengameart.org/content/misc-dark-fantasy-scenery-sprites | CC0 | 26 | 小物・建物26 |
| Home Objects | Jannax | https://opengameart.org/content/home-objects | CC0 | 26 | 小物・建物26 |
| 8-bit JRPG tilesets | Hollyhart1 | https://opengameart.org/content/8-bit-jrpg-tilesets | CC0 | 25 | 地形23・混在2 |
| Pixel Characters | PIxelPeon | https://opengameart.org/content/pixel-characters-0 | CC0 | 25 | キャラ25 |
| Walking Character Set | ATMANAN | https://opengameart.org/content/walking-character-set | CC0 | 25 | キャラ25 |
| Tiny Characters Set | Fleurman | https://opengameart.org/content/tiny-characters-set | CC0 | 23 | キャラ23 |
| Sideview Fantasy Patreon Collection | ansimuz | https://opengameart.org/content/sideview-fantasy-patreon-collection | CC0 | 22 | 地形20・混在2 |
| Monochrome Rpg | Kenney | https://kenney.nl/assets/monochrome-rpg | CC0 | 21 | 地形19・混在2 |
| Overworld - Grass Biome | Beast | https://opengameart.org/content/overworld-grass-biome | CC0 | 21 | 地形19・混在2 |
| Roguelike/RPG pack (1,700+ tiles) | Kenney | https://opengameart.org/content/roguelikerpg-pack-1700-tiles | CC0 | 21 | 地形19・混在2 |
| Top Down Adventure Assets | ansimuz | https://opengameart.org/content/top-down-adventure-assets | CC0 | 21 | 地形19・混在2 |
| RPG Asset Tile Set 'Cemetery' NES | Chasersgaming | https://opengameart.org/content/rpg-asset-tile-set-cemetery-nes | CC0 | 21 | 地形19・混在2 |
| RPG Tiles — Forest / Meadows / Outdoor | Andrew J Hamilton | https://opengameart.org/content/rpg-tiles-%E2%80%94-forest-meadows-outdoor | CC0 | 21 | 地形19・混在2 |
| Village of Chaffton | Spring Spring | https://opengameart.org/content/village-of-chaffton | CC0 | 21 | 地形19・混在2 |
| 4 Colour Interior Tileset | stealthix | https://opengameart.org/content/4-colour-interior-tileset | CC0 | 20 | 地形18・混在2 |
| Chipsets from NeoWolf | alv90 | https://opengameart.org/content/chipsets-from-neowolf | CC0 | 20 | 地形18・混在2 |
| Micro Roguelike | Kenney | https://kenney.nl/assets/micro-roguelike | CC0 | 20 | 地形20 |
| Pico 8 City | Kenney | https://kenney.nl/assets/pico-8-city | CC0 | 20 | 地形18・混在2 |
| Roguelike Caves Dungeons | Kenney | https://kenney.nl/assets/roguelike-caves-dungeons | CC0 | 20 | 地形18・混在2 |
| Roguelike Rpg Pack | Kenney | https://kenney.nl/assets/roguelike-rpg-pack | CC0 | 20 | 地形18・混在2 |
| Rpg Urban Pack | Kenney | https://kenney.nl/assets/rpg-urban-pack | CC0 | 20 | 地形18・混在2 |
| Tiny Dungeon | Kenney | https://kenney.nl/assets/tiny-dungeon | CC0 | 20 | 地形18・混在2 |
| Tiny Town | Kenney | https://kenney.nl/assets/tiny-town | CC0 | 20 | 地形18・混在2 |
| Micro World: Old tileset | SurrealEmber | https://opengameart.org/content/micro-world-old-tileset | CC0 | 20 | 地形18・混在2 |
| Nat's 8x8 Starter Pack | nateonus | https://opengameart.org/content/nats-8x8-starter-pack | CC0 | 20 | 地形18・混在2 |
| Bushly and Princess Sera | GrafxKid | https://opengameart.org/content/bushly-and-princess-sera | CC0 | 20 | キャラ20 |
| Roguelike Caves & Dungeons pack | Kenney | https://opengameart.org/content/roguelike-caves-dungeons-pack | CC0 | 20 | 地形18・混在2 |
| Simple broad-purpose tileset | surt | https://opengameart.org/content/simple-broad-purpose-tileset | CC0 | 20 | 地形20 |
| The Field of the Floating Islands | Buch | https://opengameart.org/content/the-field-of-the-floating-islands | CC0 | 20 | 地形18・混在2 |
| Roguelike Modern City pack | Kenney | https://opengameart.org/content/roguelike-modern-city-pack | CC0 | 20 | 地形18・混在2 |
| School Girl | diamonddmgirl | https://opengameart.org/content/school-girl | CC0 | 20 | キャラ20 |
| Ground tiles | SpiderDave | https://opengameart.org/content/ground-tiles-0 | CC0 | 18 | 地形18 |
| Tiny Battle | Kenney | https://kenney.nl/assets/tiny-battle | CC0 | 18 | 地形16・混在2 |
| RPG portraits | Buch | https://opengameart.org/content/rpg-portraits | CC0 | 18 | 顔18 |
| Town Tiles | surt | https://opengameart.org/content/town-tiles | CC0 | 18 | 地形18 |
| Sideview terrain and vilage tileset | scrybapp | https://opengameart.org/content/sideview-terrain-and-vilage-tileset | CC0 | 18 | 地形18 |
| Roguelike Indoors | Kenney | https://kenney.nl/assets/roguelike-indoors | CC0 | 17 | 地形15・混在2 |
| Crimelike - Furniture | extradave | https://opengameart.org/content/crimelike-furniture | CC0 | 16 | 小物・建物16 |
| Classic Hero | GrafxKid | https://opengameart.org/content/classic-hero | CC0 | 16 | キャラ16 |
| RPG character sprites | GrafxKid | https://opengameart.org/content/rpg-character-sprites | CC0 | 16 | キャラ16 |
| 16x16 base sprites | Unnamed | https://opengameart.org/content/16x16-base-sprites | CC0 | 14 | キャラ14 |
| 16x16 8-bit RPG character set | devurandom | https://opengameart.org/content/16x16-8-bit-rpg-character-set | CC0 | 14 | キャラ14 |
| Happyland tileset | Buch | https://opengameart.org/content/happyland-tileset | CC0 | 14 | 地形12・混在2 |
| Ghost monster | ImogiaGames | https://opengameart.org/content/ghost-monster | CC0 | 13 | モンスター13 |
| City Mega Pack | GrafxKid | https://opengameart.org/content/city-mega-pack | CC0 | 12 | 地形10・混在2 |
| RPG pack: base set | Kenney | https://opengameart.org/content/rpg-pack-base-set | CC0 | 12 | 地形10・混在2 |
| Pixel art animated Slime | rvros | https://opengameart.org/content/pixel-art-animated-slime | CC0 | 12 | モンスター12 |
| 2D Retro Baddie Sprites | Monster Logix Studio | https://opengameart.org/content/2d-retro-baddie-sprites | CC0 | 11 | モンスター11 |
| Items and elements | GrafxKid | https://opengameart.org/content/items-and-elements | CC0 | 11 | 小物・建物11 |
| Flowers | SpiderDave | https://opengameart.org/content/flowers | CC0 | 10 | 小物・建物10 |
| Zombies & Skeletons | artisticdude | https://opengameart.org/content/zombies-skeletons | CC0 | 10 | モンスター10 |
| Various Creatures | GrafxKid | https://opengameart.org/content/various-creatures | CC0 | 10 | モンスター10 |
| Misc household items and more! >:) | NaRNeRZz | https://opengameart.org/content/misc-household-items-and-more | CC0 | 8 | 小物・建物8 |
| Tiny RPG - Forest | ansimuz | https://opengameart.org/content/tiny-rpg-forest | CC0 | 8 | 地形6・混在2 |
| Slime - Sprite Sheet | Garakh | https://opengameart.org/content/slime-sprite-sheet | CC0 | 8 | モンスター8 |
| 8x8 8-bit Styled Desert Tileset | ImpossibleRealms | https://opengameart.org/content/8x8-8-bit-styled-desert-tileset | CC0 | 7 | 地形7 |
| Barrels (Mage City Arcanos remix) | AntumDeluge | https://opengameart.org/content/barrels-mage-city-arcanos-remix | CC0 | 7 | 小物・建物7 |
| Map pack (180 assets) | Kenney | https://opengameart.org/content/map-pack-180-assets | CC0 | 7 | 地形5・混在2 |
| Pixel Art Character | acasas | https://opengameart.org/content/pixel-art-character | CC0 | 7 | キャラ7 |
| RPG Items | Buch | https://opengameart.org/content/rpg-items | CC0 | 7 | 小物・建物7 |
| Treasure chests, 32x32 and 16x16 | Blarumyrran | https://opengameart.org/content/treasure-chests-32x32-and-16x16 | CC0 | 7 | 小物・建物7 |
| Tiny Ski | Kenney | https://kenney.nl/assets/tiny-ski | CC0 | 6 | 地形4・混在2 |
| Faceset 2-bit | Blarumyrran | https://opengameart.org/content/faceset-2-bit | CC0 | 6 | 顔6 |
| Steam monster | Blarumyrran | https://opengameart.org/content/steam-monster | CC0 | 6 | モンスター6 |
| Roguelike Indoor pack | Kenney | https://opengameart.org/content/roguelike-indoor-pack | CC0 | 6 | 地形4・混在2 |
| 8bit rpg hero | danbu | https://opengameart.org/content/8bit-rpg-hero | CC0 | 5 | キャラ5 |
| 8x8 Character and Sprite Sheet | Glacialan | https://opengameart.org/content/8x8-character-and-sprite-sheet | CC0 | 5 | キャラ5 |
| Character sprite + walk animation | Belohlavek | https://opengameart.org/content/character-sprite-walk-animation | CC0 | 5 | キャラ5 |
| Desert tileset | CDmir | https://opengameart.org/content/desert-tileset-1 | CC0 | 5 | 地形5 |
| Dungeon Tileset | HorusKDI | https://opengameart.org/content/dungeon-tileset-4 | CC0 | 5 | 地形5 |
| Pixel Platformer | Kenney | https://kenney.nl/assets/pixel-platformer | CC0 | 5 | 地形3・混在2 |
| Pixel chest and coin | hippo | https://opengameart.org/content/pixel-chest-and-coin | CC0 | 5 | 小物・建物5 |
| Top down player sprite sheet (Julia) | ArlanTR | https://opengameart.org/content/top-down-player-sprite-sheet-julia | CC0 | 5 | キャラ5 |
| Mini Knight | Master484 | https://opengameart.org/content/mini-knight | CC0 | 4 | キャラ4 |
| RPG boss brown mummy | skoam | https://opengameart.org/content/rpg-boss-brown-mummy | CC0 | 4 | モンスター4 |
| Characters - The Woods | TinyWorlds | https://opengameart.org/content/characters-the-woods | CC0 | 3 | キャラ3 |
| Desert Forest | LLGD | https://opengameart.org/content/desert-forest | CC0 | 3 | 地形3 |
| Floating Eyeball | OwlishMedia | https://opengameart.org/content/floating-eyeball-0 | CC0 | 3 | モンスター3 |
| Forest Tiles | surt | https://opengameart.org/content/forest-tiles | CC0 | 3 | 混在2・地形1 |
| Furniture for nobles tileset (MV/MZ) | NettySvit | https://opengameart.org/content/furniture-for-nobles-tileset-mvmz | CC0 | 3 | 小物・建物3 |
| Haunted Forest Trees | ETTiNGRiNDER | https://opengameart.org/content/haunted-forest-trees | CC0 | 3 | 小物・建物3 |
| "Modern Houses" Tileset TopDown. | Ritpop | https://opengameart.org/content/modern-houses-tileset-topdown | CC0 | 3 | 小物・建物3 |
| Dragons | Blarumyrran | https://opengameart.org/content/dragons | CC0 | 3 | モンスター3 |
| RPG Art Pack | russpuppy | https://opengameart.org/content/rpg-art-pack | CC0 | 3 | 混在2・地形1 |
| Stalagmite Monster | Some Weirdo | https://opengameart.org/content/stalagmite-monster | CC0 | 3 | モンスター3 |
| 16x16 minimalistic rpg sprites+some tiles | Joyeuse | https://opengameart.org/content/16x16-minimalistic-rpg-spritessome-tiles | CC0 | 2 | 混在2 |
| 32x32 Water and land Map Tilesets | Lemmi | https://opengameart.org/content/32x32-water-and-land-map-tilesets | CC0 | 2 | 混在2 |
| Bountiful Bits 10x10 Top-Down RPG Tiles | VEXED | https://opengameart.org/content/bountiful-bits-10x10-top-down-rpg-tiles | CC0 | 2 | 混在2 |
| City Pixel Tileset | software_atelier | https://opengameart.org/content/city-pixel-tileset | CC0 | 2 | 混在2 |
| Clouds | Igor Gundarev | https://opengameart.org/content/clouds | CC0 | 2 | 混在2 |
| Desert village | Skab | https://opengameart.org/content/desert-village | CC0 | 2 | 混在2 |
| Forest Pass | Blackwolfdave | https://opengameart.org/content/forest-pass | CC0 | 2 | 混在2 |
| Gem Heart(Animated) | AliHamieh | https://opengameart.org/content/gem-heartanimated | CC0 | 2 | 小物・建物2 |
| modern city extension | rubberduck | https://opengameart.org/content/modern-city-extension | CC0 | 2 | 混在2 |
| Mushroom Village tileset | NettySvit | https://opengameart.org/content/mushroom-village-tileset | CC0 | 2 | 混在2 |
| 16x16 Puny World Tileset | Shade | https://opengameart.org/content/16x16-puny-world-tileset | CC0 | 2 | 混在2 |
| 4 Colour Overworld Tileset | stealthix | https://opengameart.org/content/4-colour-overworld-tileset | CC0 | 2 | 混在2 |
| DB32 Cave tileset | Buch | https://opengameart.org/content/db32-cave-tileset | CC0 | 2 | 混在2 |
| Goblin Caves | Hyptosis | https://opengameart.org/content/goblin-caves | CC0 | 2 | 混在2 |
| Mage City Arcanos | Hyptosis | https://opengameart.org/content/mage-city-arcanos | CC0 | 2 | 混在2 |
| Outside tileset | Buch | https://opengameart.org/content/outside-tileset | CC0 | 2 | 混在2 |
| pastoral overworld | pebonius | https://opengameart.org/content/pastoral-overworld | CC0 | 2 | 混在2 |
| Simple duotone tileset | Eris | https://opengameart.org/content/simple-duotone-tileset | CC0 | 2 | 混在2 |
| Unfinished dungeon tileset | Buch | https://opengameart.org/content/unfinished-dungeon-tileset | CC0 | 2 | 混在2 |
| pixel art castle tileset | rubberduck | https://opengameart.org/content/pixel-art-castle-tileset | CC0 | 2 | 混在2 |
| Pixel Raven | tbbk | https://opengameart.org/content/pixel-raven | CC0 | 2 | モンスター2 |
| Primitive Village | Vomdrache | https://opengameart.org/content/primitive-village | CC0 | 2 | 混在2 |
| RogueDB32 | SpiderDave | https://opengameart.org/content/roguedb32 | CC0 | 2 | 混在2 |
| RogueDB32 Plus - add on tiles | dannorder | https://opengameart.org/content/roguedb32-plus-add-on-tiles | CC0 | 2 | 混在2 |
| RPG 'Mansion' Tile Set (NES) | Chasersgaming | https://opengameart.org/content/rpg-mansion-tile-set-nes | CC0 | 2 | 混在2 |
| RPG Tileset | russpuppy | https://opengameart.org/content/rpg-tileset | CC0 | 2 | 混在2 |
| Undead Pirate Roguelike | AmberFallStudio | https://opengameart.org/content/undead-pirate-roguelike | CC0 | 2 | 混在2 |
| Woman RPG Character | josepharaoh99 | https://opengameart.org/content/woman-rpg-character | CC0 | 2 | キャラ2 |
| 1-Bit Pack | Kenney | https://opengameart.org/content/1-bit-pack | CC0 | 1 | 混在1 |
| 16x16 Animated Critters | patvanmackelberg | https://opengameart.org/content/16x16-animated-critters | CC0 | 1 | モンスター1 |
| 2D Spider Animated | SpinachChicken | https://opengameart.org/content/2d-spider-animated | CC0 | 1 | モンスター1 |
| a many-eyed monster | ArVexi1050 | https://opengameart.org/content/a-many-eyed-monster | CC0 | 1 | モンスター1 |
| Cool School tileset | NettySvit | https://opengameart.org/content/cool-school-tileset | CC0 | 1 | 混在1 |
| Diamond Axe (with degradation progress) | ScratchIO | https://opengameart.org/content/diamond-axe-with-degradation-progress | CC0 | 1 | 小物・建物1 |
| Filthy Ectoplasm | Winternaut | https://opengameart.org/content/filthy-ectoplasm | CC0 | 1 | モンスター1 |
| Flash Mage | Some Weirdo | https://opengameart.org/content/flash-mage | CC0 | 1 | 混在1 |
| Free Health and Mana Potions | bevouliin.com | https://opengameart.org/content/free-health-and-mana-potions | CC0 | 1 | 小物・建物1 |
| 1 Bit Pack | Kenney | https://kenney.nl/assets/1-bit-pack | CC0 | 1 | 混在1 |
| Mini Roguelike 8x8 Tiles | morgan3d | https://opengameart.org/content/mini-roguelike-8x8-tiles | CC0 | 1 | 混在1 |
| Modern RPG Guy | OVFudj | https://opengameart.org/content/modern-rpg-guy | CC0 | 1 | キャラ1 |
| Modified 32x32 Treasure chest | Blarumyrran | https://opengameart.org/content/modified-32x32-treasure-chest | CC0 | 1 | 小物・建物1 |
| monster plant | ArVexi1050 | https://opengameart.org/content/monster-plant | CC0 | 1 | モンスター1 |
| Fumiko Complete Charset | skoam | https://opengameart.org/content/fumiko-complete-charset | CC0 | 1 | キャラ1 |
| Nora World View Sprites | Pixel Scuba | https://opengameart.org/content/nora-world-view-sprites | CC0 | 1 | キャラ1 |
| Overworld Map | keith karnage | https://opengameart.org/content/overworld-map | CC0 | 1 | 混在1 |
| Pixel Art Brick Tiles | SpinachChicken | https://opengameart.org/content/pixel-art-brick-tiles | CC0 | 1 | 混在1 |
| Pixel Art Dungeon Items | SpinachChicken | https://opengameart.org/content/pixel-art-dungeon-items | CC0 | 1 | 小物・建物1 |
| pixel art skeleton | tbbk | https://opengameart.org/content/pixel-art-skeleton | CC0 | 1 | モンスター1 |
| Pixel Art Wood Tiles | SpinachChicken | https://opengameart.org/content/pixel-art-wood-tiles | CC0 | 1 | 混在1 |
| Pixel Potion Set 16x16 | yafarida | https://opengameart.org/content/pixel-potion-set-16x16 | CC0 | 1 | 小物・建物1 |
| Resouces Pack #1 | saint11 | https://opengameart.org/content/resouces-pack-1 | CC0 | 1 | 小物・建物1 |
| Slime | ArVexi1050 | https://opengameart.org/content/slime-7 | CC0 | 1 | モンスター1 |
| Winter Birds | Refuzzle | https://opengameart.org/content/winter-birds | CC0 | 1 | モンスター1 |
