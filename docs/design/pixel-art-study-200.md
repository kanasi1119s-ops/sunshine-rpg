# 既存のドット絵200点の学習記録（2026-09-30）

人間の依頼「既存のドット絵を200点ほど学習してきて」で行った学習の記録です。学んだ技法は `docs/design/pixel-art-notes.md` の「既存のドット絵200点から学んだこと」に書き、ここには**何を・どう見たか**と**測った数値**を残します。

## 守ったこと
- **学習に使ったのは、利用条件がはっきりした無料素材だけ。** OpenGameArt の CC0（権利放棄）の作品、Kenney（CC0）、ぴぽやの無料素材（規約は `docs/assets-credits.md` で確認済み）。1件ずつ、ページのライセンス欄が CC0 だけであることを確かめた
- **市販ゲームの絵は見ていない。** 説明文で既存ゲームの名前を出したり「〜風」「〜のような」と書いたりしている作品、既存ゲームの絵の作り直し・他人の絵の改変、別のゲームのための差し替え素材は外した（CLAUDE.md 1-1。例: 「FF6風」「Zelda風」「Metroid風」「Stendhal用」）
- **AI での利用を禁じている作者の作品は使わない**（Mana Seed の件、`docs/assets-credits.md`）。今回の対象の説明文・同梱の規約に、AIについての記述は無かった
- 有料の素材は見ていない（ぴぽやのモンスター素材は有料990円だったので外した）
- ドット絵ではないもの（数千色以上、半透明が多い、写真・3Dの描き出し）は外した
- **絵そのものはリポジトリに入れていない。** 作業用の一時フォルダで分析し、ここには数値と出典だけを書く。今回の学習の絵を、ゲームにそのまま使うことはしない（使う場合は `docs/assets-credits.md` の手順を別に踏む）

## やり方
1. 上の条件で、47の配布元から素材を集めた（OpenGameArt 約40件、Kenney 2件、ぴぽや 3件）
2. シートを1点ずつの絵に切り分け（背景色を抜く→ひとかたまりずつ切り出す、タイルは格子で切る）、アニメの別コマのような似た絵を間引いて、**キャラ45・顔12・モンスター43・地形55・小物と建物45、計200点**を選んだ
3. 200点すべてを、同じ物差しで数値にした（色数、彩度、明暗の幅、色相シフト、外周の縁取り、光の向き、孤立ドット、ディザ）
4. 200点を拡大した一覧画像にして、目で見て確かめた（切り出しに失敗した十数点は、数値の傾向を見るうえでのノイズとして扱った）
5. **うちのゲームの絵15点**（地形7・ボス3・登場人物5、`src/game/art/sprite-data.generated.ts`）も同じ物差しで測って比べた。地形は、`main` でぴぽや素材から作った草・土・水・森に置き換わったあとの版で測り直した（表の「うちの地形」は、崖・岸辺＝自作と、草・土・水・森＝ぴぽや由来を分けて書いた）

## 測った数値（中央値。かっこ内は25%〜75%）

| 物差し | キャラ(45) | モンスター(43) | 地形(55) | 小物・建物(45) | **うちの地形(崖・岸辺2 / ぴぽや由来4)** | **うちの登場人物(5)** | **うちのボス(3)** |
|---|---|---|---|---|---|---|---|
| 大きさ | 14×21 | 16×23 | 16×16 | 16×18 | 128×128 | 約120×245 | 256×256 |
| 色数 | 10 (7〜14) | 9 (7〜11) | 6 (4〜9) | 8 (5〜13) | 10・16 / 23〜24 | 22〜26 | 23〜26 |
| 明暗の幅（0〜1） | 0.90 | 0.74 | **0.48** (0.25〜0.60) | 0.60 | **0.65・0.93** / 0.11〜0.27 | 0.91〜0.94 | 0.75〜0.98 |
| 彩度の最大 | 0.94 | 0.85 | **0.68** | 0.79 | 0.74・0.88 / 0.40〜0.61 | 0.84〜0.91 | 0.92〜1.00 |
| 色相シフト（暗→明で黄に近づく度合い、°） | 5.7 | 5.7 | 5.7 | 5.0 | 11〜19 / 0〜23 | 2.4〜13 | 0.6〜20 |
| 色相シフトが寒色→暖色の向きの割合 | 80% | 64% | 68% | 65% | — | — | — |
| 外周の明るさ÷内側の明るさ（小さいほど暗い縁取り） | **0.25** | 0.44 | 縁取り無し | 0.63 | 縁取り無し | 0.18〜0.30 | **0.74〜1.02** |
| 外周のうち黒に近い割合 | 81% | 33% | 0% | **0%** | — | 76〜100% | 57〜61% |
| 左上−右下の明るさの差（+は左上が明るい） | +0.07 | +0.06 | 0.00 | +0.01 | +0.06・−0.01 / — | +0.13〜+0.32 | +0.02〜+0.13 |
| 孤立ドット（上下左右が別の色）の割合 | 7% | 5% | **3%** (1〜9%) | 6% | **9%** / （近い色が並ぶため測れない） | 2〜3% | 3〜6% |
| 市松ディザの割合 | 1% | 1% | 1% | 1% | 1.3〜1.9% / 0.2〜0.5% | 0.3〜0.6% | 0.7〜1.3% |
| いちばん暗い色の明るさ | 0.05 | 0.10 | 0.17 | 0.13 | 0.07〜0.10 / — | 0.06〜0.09 | 0.02〜0.03 |

- 色相シフトの測り方: 同じ色相の仲間（30°ごと）を明るさ順に並べ、暗い色と明るい色で、黄（60°）への近さがどれだけ変わるかを見た。＋なら「影は寒色側、光は黄側」
- 参考の絵は16〜32ドットが中心で、うちの絵（128・256）とは大きさが違う。色数などは大きさで変わるので、比べるのは「割合」「幅」「向き」を中心にする

## 学習した素材（すべて無料。絵はリポジトリに入れていない）

| 種類 | 作品名 | 作者 | 入手元 | ライセンス | 点数 |
|---|---|---|---|---|---|
| キャラ | 16x16 8-bit RPG character set | devurandom | https://opengameart.org/content/16x16-8-bit-rpg-character-set | CC0 | 3 |
| キャラ | 8x8 Character Pack | patvanmackelberg | https://opengameart.org/content/8x8-character-pack | CC0 | 6 |
| キャラ | Bushly and Princess Sera | GrafxKid | https://opengameart.org/content/bushly-and-princess-sera | CC0 | 3 |
| キャラ | Classic Hero | GrafxKid | https://opengameart.org/content/classic-hero | CC0 | 6 |
| キャラ | Fumiko Complete Charset | skoam | https://opengameart.org/content/fumiko-complete-charset | CC0 | 6 |
| キャラ | Mini Knight | Master484 | https://opengameart.org/content/mini-knight | CC0 | 5 |
| キャラ | Nora World View Sprites | Pixel Scuba | https://opengameart.org/content/nora-world-view-sprites | CC0 | 4 |
| キャラ | Tiny Characters Set | Fleurman | https://opengameart.org/content/tiny-characters-set | CC0 | 4 |
| キャラ | Tiny RPG - Forest | ansimuz | https://opengameart.org/content/tiny-rpg-forest | CC0 | 3 |
| キャラ | Top Down Adventure Assets | ansimuz | https://opengameart.org/content/top-down-adventure-assets | CC0 | 5 |
| 顔 | Faceset 2-bit | Blarumyrran | https://opengameart.org/content/faceset-2-bit | CC0 | 5 |
| 顔 | RPG portraits | Buch | https://opengameart.org/content/rpg-portraits | CC0 | 7 |
| モンスター | 8x8 Critter Pack | patvanmackelberg | https://opengameart.org/content/8x8-critter-pack | CC0 | 1 |
| モンスター | Classic hero and baddies pack | GrafxKid | https://opengameart.org/content/classic-hero-and-baddies-pack | CC0 | 6 |
| モンスター | Dragons | Blarumyrran | https://opengameart.org/content/dragons | CC0 | 2 |
| モンスター | Tiny Dungeon | Kenney | https://kenney.nl/assets/tiny-dungeon | CC0 | 7 |
| モンスター | Sideview Fantasy Patreon Collection | ansimuz | https://opengameart.org/content/sideview-fantasy-patreon-collection | CC0 | 8 |
| モンスター | Steam monster | Blarumyrran | https://opengameart.org/content/steam-monster | CC0 | 6 |
| モンスター | Tiny RPG - Forest | ansimuz | https://opengameart.org/content/tiny-rpg-forest | CC0 | 7 |
| モンスター | Zombies & Skeletons | artisticdude | https://opengameart.org/content/zombies-skeletons | CC0 | 6 |
| 地形 | 8-bit JRPG tilesets | Hollyhart1 | https://opengameart.org/content/8-bit-jrpg-tilesets | CC0 | 4 |
| 地形 | DB32 Cave tileset | Buch | https://opengameart.org/content/db32-cave-tileset | CC0 | 4 |
| 地形 | The Field of the Floating Islands | Buch | https://opengameart.org/content/the-field-of-the-floating-islands | CC0 | 4 |
| 地形 | Goblin Caves | Hyptosis | https://opengameart.org/content/goblin-caves | CC0 | 4 |
| 地形 | Happyland tileset | Buch | https://opengameart.org/content/happyland-tileset | CC0 | 1 |
| 地形 | RPG pack: base set | Kenney | https://opengameart.org/content/rpg-pack-base-set | CC0 | 3 |
| 地形 | Tiny Town | Kenney | https://kenney.nl/assets/tiny-town | CC0 | 4 |
| 地形 | Mage City Arcanos | Hyptosis | https://opengameart.org/content/mage-city-arcanos | CC0 | 4 |
| 地形 | Overworld - Grass Biome | Beast | https://opengameart.org/content/overworld-grass-biome | CC0 | 2 |
| 地形 | pastoral overworld | pebonius | https://opengameart.org/content/pastoral-overworld | CC0 | 3 |
| 地形 | フィールドマップセット１（オートタイル） | ぴぽや | https://pipoya.net/sozai/assets/map-chip_tileset32/ | ぴぽや無料素材利用規約（`docs/assets-credits.md`） | 1 |
| 地形 | フィールドマップセット１ | ぴぽや | https://pipoya.net/sozai/assets/map-chip_tileset32/ | ぴぽや無料素材利用規約（`docs/assets-credits.md`） | 1 |
| 地形 | フィールドマップセット１追加パーツ | ぴぽや | https://pipoya.net/sozai/assets/map-chip_tileset32/ | ぴぽや無料素材利用規約（`docs/assets-credits.md`） | 1 |
| 地形 | 16x16 Puny World Tileset | Shade | https://opengameart.org/content/16x16-puny-world-tileset | CC0 | 4 |
| 地形 | Simple broad-purpose tileset | surt | https://opengameart.org/content/simple-broad-purpose-tileset | CC0 | 4 |
| 地形 | Tiny RPG - Forest | ansimuz | https://opengameart.org/content/tiny-rpg-forest | CC0 | 4 |
| 地形 | Town Tiles | surt | https://opengameart.org/content/town-tiles | CC0 | 3 |
| 地形 | Unfinished dungeon tileset | Buch | https://opengameart.org/content/unfinished-dungeon-tileset | CC0 | 4 |
| 小物・建物 | Hero spritesheets (Ars Notoria) | Balmer | https://opengameart.org/content/hero-spritesheets-ars-notoria | CC0 | 5 |
| 小物・建物 | Farming crops 16x16 | josehzz | https://opengameart.org/content/farming-crops-16x16 | CC0 | 7 |
| 小物・建物 | Home Objects | Jannax | https://opengameart.org/content/home-objects | CC0 | 2 |
| 小物・建物 | Medieval RTS (120+) | Kenney | https://opengameart.org/content/medieval-rts-120 | CC0 | 7 |
| 小物・建物 | Pixel farm and shack | pixel32 | https://opengameart.org/content/pixel-farm-and-shack | CC0 | 5 |
| 小物・建物 | RPG item set | Jetrel | https://opengameart.org/content/rpg-item-set | CC0 | 7 |
| 小物・建物 | Tiny RPG - Forest | ansimuz | https://opengameart.org/content/tiny-rpg-forest | CC0 | 5 |
| 小物・建物 | Top Down Adventure Assets | ansimuz | https://opengameart.org/content/top-down-adventure-assets | CC0 | 6 |
| 小物・建物 | Trees & Bushes | ansimuz | https://opengameart.org/content/trees-bushes | CC0 | 1 |


- ぴぽや由来の地形は、明るさが数%しか違わない近い色が隣り合うため、「孤立ドット」の物差しが高く出る（66〜77%）が、目で見てざわつく点ではない。この物差しは、色の差が大きい絵にだけ当てはまる
