# r20-props — マップの飾り33点（町・ダンジョン／遺跡）

すべて一から自作（既存作品の絵・名前は使っていない）。`r17-polish/townprops.py` と同じ道具立て（1文字=1色の文字グリッド＋`pal-*.json`）で、`python3 build.py` で全部作り直せる（生成の元は `town.py` `town2.py` `dungeon.py` `dungeon2.py`、共通の道具は `lib.py`）。確認画像は `preview.png`（4倍拡大。上が町＝緑の地、下がダンジョン＝紫の地）。

## 作り方の約束（守った規則）
- 光は左上。**ハイライト（照り）は使わない**。影と地の2〜3段＋素材ごとの暗い縁取り。影の色は地より少し暗く彩度を少し上げた。
- 足元に濃い楕円の影（キー **`S`** に固定。町は `#26382a`、ダンジョンは `#14121c`。砂地・雪地に置くときは本体側で `S` を差し替えるとなじむ）。
- 色は1点あたり最大16色（実際は4〜16色）。`build.py` が色数・文字の抜けを自動で確かめる。
- 例外（光る物）: 水晶・きのこ・炎・灯りの祠・光の玉・金貨は、光って見せるため明るい色を1〜2段足している（照りではなく「光源の色」）。
- 灯りの祠・垂れ幕・墓石・棺の輪の模様は、`docs/story/bible.md` の「灯の環」「環信仰」にそろえた自作の意匠。
- 絵のサイズは**そのまま**（1ドット=1画面ドット）。`tileWidth` が16なので、48は3マス、16は1マス。「足元」は絵の**最下行**（そのすぐ上に影が入っている）。横は中央をタイルの中央にそろえる（`prop-renderer.ts` のとおり）。

## 一覧
サイズは 幅×高さ(px)。当たり判定の「足元」はマス数（左・右・上）で、`PROP_FOOTPRINT` の値の案。

### 町（緑の地の上に置く想定）
| 名前（ファイル） | 大きさ | 当たり判定の案 | 使う場所の提案 |
|---|---|---|---|
| fountain（噴水） | 48×47 | 通れない 左1・右1・上1 | 町の広場の中央。水が噴き上がる |
| stall（市場の屋台） | 48×45 | 通れない 左1・右1・上0 | 市場のある町の通り沿い。縞の日よけ・台・果物の籠 |
| haystack（干し草の山） | 32×28 | 通れない 左0・右0・上0 | 村はずれ・畑・厩の脇 |
| cart（荷車・荷つき） | 48×32 | 通れない 左1・右1・上0 | 街道、港、市場の裏 |
| laundry（洗濯物） | 48×30 | 通れない 左1・右1・上0（下をくぐれる扱いにはしない） | 民家の裏庭、貧しい町 |
| fence（柵・中） | 16×17 | 通れない 0・0・0 | 畑・牧場の囲い。横に並べてつなぐ（横木は左右いっぱいまで） |
| fence-end（柵の端） | 16×18 | 通れない 0・0・0 | 柵の右端。左端は左右反転して使う |
| bench（ベンチ） | 32×20 | 通れない 左1・右0・上0 | 広場・噴水のそば・港 |
| statue-traveler（旅人像） | 24×41 | 通れない 0・0・0 | 町の入口・広場。つば広の帽子と杖の無名の像 |
| grave-cross（十字の墓石） | 16×22 | 通れない 0・0・0 | 墓地・丘の上 |
| grave-round（丸い墓石） | 16×19 | 通れない 0・0・0 | 墓地。小さな環の彫り |
| noticeboard（立て札・掲示板） | 32×37 | 通れない 左0・右1・上0 | 町の入口・広場（依頼やうわさの掲示に） |
| brazier（かがり火台） | 24×32 | 通れない 0・0・0 | 夜の広場・砦・祭り。炎は明るい（光源） |
| shrine（灯りの祠） | 24×33 | 通れない 0・0・0 | 各町の片すみ（環信仰の小さな祠。灯の環の金の輪と灯り。お参りイベントの対象にできる） |

### ダンジョン・遺跡（紫の地の上に置く想定）
| 名前（ファイル） | 大きさ | 当たり判定の案 | 使う場所の提案 |
|---|---|---|---|
| pillar（立つ石柱） | 20×48 | 通れない 0・0・0 | 神殿・遺跡の広間（左右対に並べる） |
| pillar-broken（折れた柱） | 26×29 | 通れない 0・0・0（右の欠片まで含めるなら右1） | 崩れた遺跡 |
| statue-soldier（兵士の像） | 26×46 | 通れない 0・0・0 | 城・砦跡。盾と槍 |
| statue-winged（翼ある像） | 36×46 | 通れない 左0・右1・上0 | 神殿の奥・仕掛けの間。胸の光の玉が光る |
| banner-purple（垂れ幕・紫） | 22×42 | **通れる**（壁の飾り） | 城・神殿の壁。金の輪の紋 |
| banner-red（垂れ幕・赤） | 22×42 | **通れる**（壁の飾り） | 同上（敵の城など） |
| bones（骨と頭蓋骨の山） | 34×17 | 通れる（足元の飾り） | 洞窟・牢・墓所 |
| cobweb（くも巣） | 26×26 | **通れる**（部屋の左上の角用。右上は左右反転） | 古い塔・墓所・地下 |
| candelabra（燭台・床置き） | 20×36 | 通れない 0・0・0 | 城・墓所・神殿。炎は光源 |
| coffin（棺） | 44×24 | 通れない 左1・右1・上0 | 墓所・地下聖堂 |
| barrel-broken（壊れた樽） | 36×21 | 通れる（低い残骸）か 左1・右1 | 牢・倉庫跡・襲われた村 |
| box-broken（壊れた箱） | 32×24 | 通れない 左1・右0・上0 | 同上 |
| crystal-blue（水晶・青） | 34×36 | 通れない 左1・右1・上0 | 洞窟。光る（灯り石の洞窟に） |
| crystal-red（水晶・赤） | 34×36 | 通れない 左1・右1・上0 | 火山・危険な洞窟。光る |
| mushrooms（光るきのこ群） | 32×25 | 通れる（足元の飾り） | 洞窟・地下湖のほとり。光る |
| chest-closed（宝箱・閉） | 26×22 | 通れない 0・0・0 | 既存の宝箱の代わり／色違いの箱として |
| chest-open（宝箱・開） | 26×30 | 通れない 0・0・0 | 開けたあとの絵（金貨の山つき。中身が空なら金貨を消した版を別に作る） |
| chains（鎖と手かせ） | 22×44 | **通れる**（壁・天井の飾り） | 牢・拷問部屋。手かせ2本 |
| jail-bars（牢の柵・扉つき） | 34×50 | 通れない 左1・右0・上0（横2マス。つなげるなら端の石柱を共有） | 牢・砦の地下。間は透ける |

## 出来の自己評価（正直に）
- **よい**: fountain、cart、shrine、brazier、candelabra、banner 2種、chest 2種、crystal 2色、mushrooms、pillar、statue-soldier、statue-winged、jail-bars、chains、noticeboard、bench、haystack。
- **弱い（作り直し候補）**:
  - **bones**: 頭蓋骨は読めるが、骨のかたまりが平たい板のように見える。
  - **box-broken / barrel-broken**: 小さく、色が茶色で単調。「壊れている」は分かるが、何の残骸かは近くで見ないと分からない。
  - **cobweb**: 糸が細く、暗い床の上でしか読めない。隅の飾りとしての最小限。
  - **coffin**: ふたの形が少し丸く、棺というより箱に見える。頭側の肩の形をもう少し出したい。
  - **statue-traveler**: 帽子が魔法使いのようにも見える。顔の彫りが粗い。
  - **stall**: 果物の籠が暗い背景に溶けやすい。
  - **fence / fence-end**: 低くて目立たない。つなげたときの見た目は未確認（実マップで確認が必要）。
  - **laundry**: 布の形が単純。
- 実際のマップに置いたときの見え方・当たり判定・前後の重なりは**まだ確かめていない**（ゲームには組み込んでいない）。

## ゲームに組み込むために本体側で必要な変更（まだやっていない）
名前（種類）は `prop:<種類>` にする案。種類名＝上の表のファイル名（ハイフンつき）。

### 1. `tools/pixel-art/props.mjs`
- `piece()` の `frame` が正方形（48/64/80）で、絵を下そろえ・中央で透明の余白を足している。本体の描画（`prop-renderer.ts`）は**絵の大きさそのまま**で足元にそろえるので、**自然な大きさで出す**ために `frame = 0`（余白なし）を許す。`frame ? ... : w` と `oy = frame ? frame - h : 0`、`g` のサイズを `w×h` にする。
- ディレクトリ `r20-props` から33点を `PIECES` に足す。例: `piece("P16-噴水", "r20-props", "fountain.txt", "pal-fountain.json", {}, 0)`。番号は P16〜P48。
- `fence-end` の左向き用に、`flipX` オプション（行を反転）を足して `fence-end-l` を作る（またはプレビュー用の反転版 txt を足す）。同様に `cobweb` の右上用 `cobweb-r`。
- 影（キー `S`）は `recolor: { S: "#..." }` で地面ごとに差し替えられる（雪・砂など）。

### 2. `tools/pixel-art/export-game-data.mjs`
- 41行目付近の `props: [1, { ... }]` の対応表に `"P16-噴水": "prop:fountain"` … と33点（＋`fence-end-l`・`cobweb-r`）を足す。ほかは変えない（`sprite-data.generated.ts` は再生成）。

### 3. `src/game/map/types.ts`
- `MapPropKind` に種類を足す:
  `"fountain" | "stall" | "haystack" | "cart" | "laundry" | "fence" | "fence-end" | "fence-end-l" | "bench" | "statue-traveler" | "grave-cross" | "grave-round" | "noticeboard" | "brazier" | "shrine" | "pillar" | "pillar-broken" | "statue-soldier" | "statue-winged" | "banner-purple" | "banner-red" | "bones" | "cobweb" | "cobweb-r" | "candelabra" | "coffin" | "barrel-broken" | "box-broken" | "crystal-blue" | "crystal-red" | "mushrooms" | "chest-closed" | "chest-open" | "chains" | "jail-bars"`

### 4. `src/game/map/map-props.ts`
- `PROP_FOOTPRINT` に上の表の「当たり判定の案」を足す（`Record<MapProp["kind"], ...>` なので全種類の記入が必須）。
- **通れる飾り**（banner・bones・cobweb・mushrooms・chains・barrel-broken）のために、`{ left, right, up }` に `passable?: boolean` を足し、`propFootprintTiles` は `passable` のとき `[]` を返す。
- `PROP_HEIGHT` に絵の高さ（表の「高さ」）を足す。`propOverhangTiles` の確認用。
- 壁の飾り（banner・chains・cobweb）は足元＝壁の下端のマスで書くと、高さが3マス前後で上へはみ出す。`map-props.test.ts` の「NPC・出入り口と重ならない」確認に引っかかるときは、`PROP_HEIGHT` を実寸のままにして、重なりの確認から壁の飾りを除く。
- `isHouse` は変えない。`MAP_PROPS` に置く例（町の広場）: `{ kind: "fountain", tileX: 11, tileY: 8 }`、`{ kind: "shrine", ... }`。

### 5. 描画の前後
- `renderProps` は足元のyで前後を決める。垂れ幕・くも巣・鎖は常にプレイヤーより奥（背景側）に描くのが自然なので、`filter` の「奥」の側に入れる。
- 光る物（水晶・きのこ・炎・祠）に夜の光のにじみを足すのは別の作業（今回は絵のみ）。

## 同じ素材の作り直し方
```
cd assets-src/pixel-practice/r20-props
python3 build.py        # 全部作り直し＋色数チェック＋preview.png
python3 preview.py 名前…  # 一部だけ6倍で preview-tmp.png に出す（確認用。コミットしない）
```

## 家の中の家具（2026-10-04 追加）
`interior.py` で作った4点（一から自作）: bookshelf（本棚 28×36）、bed（ベッド 34×32）、tansu（箪笥 26×30）、table（丸テーブルとポット・ろうそく 32×28）。光は左上、ハイライトなし、影と地の2〜3段＋暗い縁取り。`python3 interior.py` で作り直し、`node tools/pixel-art/export-game-data.mjs` でゲームの絵（`prop:*`）に書き出す。家の中の部屋は `src/game/world/house-interiors.ts`。
