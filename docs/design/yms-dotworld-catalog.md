# ドット絵世界（yms.main.jp）の素材カタログ（2026-09-30 調査）

人間から「ドット絵世界のドット絵でダウンロードできるものはすべてダウンロードしてプッシュして」と依頼があり、調べた記録です。

**結論: 素材の画像そのものはリポジトリに入れていない（入れられない）。** このリポジトリは**公開**されているので、元の画像を置くと、誰でもそのまま持っていける＝「そのままの素材を配る」ことになるためです。ここには、どんな素材があるか・どこから取れるか・使ってよいかの判定だけを残します。

## 規約（2026-09-30 に利用規約ページ https://yms.main.jp/page-s1/terms.html を全文確認）

| 項目 | 内容 |
|---|---|
| 編集・改変 | ○ 自由に編集してよい |
| 使用報告 | 不要（していただけると嬉しい、とのこと） |
| 二次配布 | **× 禁止**（英語版: It may not be redistributed.） |
| ツール | ツクール用の表記がある素材を除き、ウディタなど**あらゆるゲーム制作ツールで使える** |
| ツクール用の表記がある素材 | **ツクールシリーズを使ったゲーム制作でのみ使える → このゲームでは使えない** |
| サンプルマップ | **使用NG**（ツクールで作られており、ツクールの規約に触れるおそれがあるため） |
| 使用範囲 | ゲーム・アプリの制作。例外としてゲーム紹介サイト・動画制作などもOK |
| 商用利用 | ○ OK |
| 著作権表示 | Web などで不特定多数に配布するときは、スタッフロールなど1か所に表示する。表示内容: サイト名「ドット絵世界」（英語は Pixel Art World）、URL http://yms.main.jp |
| その他 | 公序良俗に反する作品での利用は不可。著作権は放棄されていない（royalty-free but not copyright free） |

### 作者さんへの問い合わせの答え（2026-09-30、旭さんが確認して伝えてくれたもの）

- **ツクールの素材以外は使ってよい。**
- 規約の「配る」（二次配布）には、**商用のゲームとして配ることは含まれない**。つまり、素材を組み込んだゲームを売ったり配ったりするのはよい。
- **ダメなのは、素材をそのままの形で配ること。**

## このゲームでの扱い方（守ること）

1. **元の画像ファイルを、このリポジトリ（公開）にそのまま置かない。** `assets-src/` にも置かない。ほかの無料素材（ぴぽや・CC0）とはここが違う。
2. 使うときは、定期タスクや作業者がそのつど作者のサイトから取得し、**ゲーム用に加工したものだけ**をゲームに入れる。加工の例: 16px 規格に縮小して描き直す、色数を減らしてゲームのパレットに合わせる、必要なタイルだけを切り出してほかの素材と1枚にまとめる。
   - 加工した絵もゲームのファイル（`dist/`、公開されるソース）に入るが、これは「ゲームに組み込んで配る」ことなので作者さんの答えの範囲内。ただし、**加工がほとんどない（元のタイルシートとほぼ同じ）形で置くのは避ける**。
   - 迷ったら、作業を止めて人間に確認する。
3. 使ったら、`docs/assets-credits.md` の「使用中の素材」に使った素材とファイル名を書き、ゲーム内クレジットと README に「ドット絵世界 http://yms.main.jp」と書く（必須）。
4. **「ツクール用」「VX素材」などツクール専用の表記がある素材、サンプルマップ（「素材サンプル」の文字入り画像）、キノコ村・カボチャ村のサンプルゲームは使わない。**
5. 実在の商品（商標）の絵は使わない。

## 大きさについての注意

ほとんどが **RPGツクールVX Ace の規格（1マス32×32px、A1〜E のタイルシート、キャラは3×4コマ）** です。このゲームは1マス16px・マップのキャラ16×32（2026-09-30に決定）なので、**半分に縮めると大きさがそろう**（キャラは32×32の1コマ→16×16になるため、キャラは縮小ではなく16×32で描き直す）。そのまま貼るのではなく、そのまま貼るのではなく、**縮小して描き直す・描き方の参考にする**使い方になります。オートタイル（A1・A2・A4）は VX Ace 形式なので、使うならこのゲームの形式に組み直す必要があります（ウディタ用に作り直された `[BASE]NobleHouse1.png` が1つだけあります）。

## ページの一覧

| ページ | 内容 |
|---|---|
| https://yms.main.jp/page-msets/worldmap1.html | ワールドマップ（通常・暗い・シンプルの3種＋部品） |
| https://yms.main.jp/page-msets/forest1.html ・ forest2.html ・ forest3.html | 森と草原（明るい森・深い森・針葉樹）、吊り橋・遺跡・テントなど |
| https://yms.main.jp/page-msets/cave1.html ・ cave1_rock.html | 土の洞窟・岩の洞窟・鉱山 |
| https://yms.main.jp/page-msets/ger1.html | 草原の集落（テント型の家） |
| https://yms.main.jp/page-msets/town_foresttown1.html ・ town_posttown1.html ・ town_castletown1.html ・ noblehouse1.html ・ village1.html | 町・村・城下町・貴族の家の外観 |
| https://yms.main.jp/page-msets/town_inside1.html ・ bath1.html | 町の内装、トイレ・浴室 |
| https://yms.main.jp/page-m1/chara_door1.html ・ chara_light1.html ・ chara_object1.html ・ chara_walk1.html | ドア、照明、宝箱・たき火・船などのオブジェクト、動物などの歩行キャラ |
| https://yms.main.jp/page-m1/looseleaf1.html | ルーズリーフ風のキャラ素材 |
| https://yms.main.jp/page-m2/materialp_park.html | 公園タイルセット（VX規格。配布は zip。ページの画像 park01〜08 はサンプル） |
| https://yms.main.jp/page-m2/materialp_mushroom.html | キノコ村とカボチャ村（ツクール VX Ace のサンプルゲーム付き。使わない） |
| https://yms.main.jp/dotartworld/index.html | 旧サイト（チップ・VX素材など。「一部RPGツクール専用の素材もあります」と書かれている） |

## ダウンロードできた素材（200点。2026-09-30）

判定: ○ 使ってよい（加工して組み込む）／△ 使う前にページでツクール用の表記がないか確認する／× 使わない。
サムネイル・バナー・アイコン・サンプルマップの画像は数に入れていない（取得できなかった2点: `sozai1/tile_outside_f1/Town-B.png`、`TownBF-PostTown-C-2.png`）。公園タイルセットの zip は未取得。

### `dotartworld/sozai/chara/`（1点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [$PManekineko01.png](https://yms.main.jp/dotartworld/sozai/chara/%24PManekineko01.png) | 288×384 | △ 旧サイト（使う前にページで表記を確認） |

### `dotartworld/sozai/chips/`（23点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Cakes01.png](https://yms.main.jp/dotartworld/sozai/chips/Cakes01.png) | 224×256 | △ 旧サイト（使う前にページで表記を確認） |
| [Eu-Easel01.png](https://yms.main.jp/dotartworld/sozai/chips/Eu-Easel01.png) | 96×96 | △ 旧サイト（使う前にページで表記を確認） |
| [Eu-FurnitureMV01.png](https://yms.main.jp/dotartworld/sozai/chips/Eu-FurnitureMV01.png) | 240×288 | △ 旧サイト（使う前にページで表記を確認） |
| [Eu-GlandPiano.png](https://yms.main.jp/dotartworld/sozai/chips/Eu-GlandPiano.png) | 224×224 | △ 旧サイト（使う前にページで表記を確認） |
| [Eu-Lace01.png](https://yms.main.jp/dotartworld/sozai/chips/Eu-Lace01.png) | 144×160 | △ 旧サイト（使う前にページで表記を確認） |
| [Eu-Pillar01.png](https://yms.main.jp/dotartworld/sozai/chips/Eu-Pillar01.png) | 192×96 | △ 旧サイト（使う前にページで表記を確認） |
| [Eu-PillarMV01.png](https://yms.main.jp/dotartworld/sozai/chips/Eu-PillarMV01.png) | 240×144 | △ 旧サイト（使う前にページで表記を確認） |
| [Eu-Sofa01.png](https://yms.main.jp/dotartworld/sozai/chips/Eu-Sofa01.png) | 720×495 | △ 旧サイト（使う前にページで表記を確認） |
| [Eu-Sofa02.png](https://yms.main.jp/dotartworld/sozai/chips/Eu-Sofa02.png) | 256×240 | △ 旧サイト（使う前にページで表記を確認） |
| [Eu-Statue01.png](https://yms.main.jp/dotartworld/sozai/chips/Eu-Statue01.png) | 192×128 | △ 旧サイト（使う前にページで表記を確認） |
| [Jukebox01.png](https://yms.main.jp/dotartworld/sozai/chips/Jukebox01.png) | 64×64 | △ 旧サイト（使う前にページで表記を確認） |
| [Millais-Ophelia01.png](https://yms.main.jp/dotartworld/sozai/chips/Millais-Ophelia01.png) | 80×64 | △ 旧サイト（使う前にページで表記を確認） |
| [Millais-Ophelia02.png](https://yms.main.jp/dotartworld/sozai/chips/Millais-Ophelia02.png) | 80×64 | △ 旧サイト（使う前にページで表記を確認） |
| [Showcase01.png](https://yms.main.jp/dotartworld/sozai/chips/Showcase01.png) | 160×208 | △ 旧サイト（使う前にページで表記を確認） |
| [Statue02.png](https://yms.main.jp/dotartworld/sozai/chips/Statue02.png) | 96×96 | △ 旧サイト（使う前にページで表記を確認） |
| [Statue02MV.png](https://yms.main.jp/dotartworld/sozai/chips/Statue02MV.png) | 144×96 | △ 旧サイト（使う前にページで表記を確認） |
| [ajisai.png](https://yms.main.jp/dotartworld/sozai/chips/ajisai.png) | 128×144 | △ 旧サイト（使う前にページで表記を確認） |
| [oshiro.png](https://yms.main.jp/dotartworld/sozai/chips/oshiro.png) | 256×128 | △ 旧サイト（使う前にページで表記を確認） |
| [oshiromv.png](https://yms.main.jp/dotartworld/sozai/chips/oshiromv.png) | 384×192 | △ 旧サイト（使う前にページで表記を確認） |
| [pot.png](https://yms.main.jp/dotartworld/sozai/chips/pot.png) | 144×160 | △ 旧サイト（使う前にページで表記を確認） |
| [tanabata.png](https://yms.main.jp/dotartworld/sozai/chips/tanabata.png) | 128×160 | △ 旧サイト（使う前にページで表記を確認） |
| [treeMV.png](https://yms.main.jp/dotartworld/sozai/chips/treeMV.png) | 96×144 | △ 旧サイト（使う前にページで表記を確認） |
| [yukiyanagi.png](https://yms.main.jp/dotartworld/sozai/chips/yukiyanagi.png) | 64×64 | △ 旧サイト（使う前にページで表記を確認） |

### `dotartworld/sozai/food/`（1点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Ozen.png](https://yms.main.jp/dotartworld/sozai/food/Ozen.png) | 160×128 | △ 旧サイト（使う前にページで表記を確認） |

### `dotartworld/sozai/vx/`（1点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Autotile-MarbleCounterMV01.png](https://yms.main.jp/dotartworld/sozai/vx/Autotile-MarbleCounterMV01.png) | 288×192 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |

### `dotartworld/sozai/vx/vx-autotile/`（1点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Autotile-MarbleCounter01.png](https://yms.main.jp/dotartworld/sozai/vx/vx-autotile/Autotile-MarbleCounter01.png) | 192×128 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |

### `dotartworld/sozai/vx/vx-chara/`（5点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [!$PClock01.png](https://yms.main.jp/dotartworld/sozai/vx/vx-chara/%21%24PClock01.png) | 96×320 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |
| [!$PEdoinu01.png](https://yms.main.jp/dotartworld/sozai/vx/vx-chara/%21%24PEdoinu01.png) | 96×128 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |
| [!$PMirror01.png](https://yms.main.jp/dotartworld/sozai/vx/vx-chara/%21%24PMirror01.png) | 288×320 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |
| [!$PMirror02.png](https://yms.main.jp/dotartworld/sozai/vx/vx-chara/%21%24PMirror02.png) | 288×320 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |
| [Edoinu.png](https://yms.main.jp/dotartworld/sozai/vx/vx-chara/Edoinu.png) | 64×32 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |

### `dotartworld/vx/sozai/`（7点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [!$Gate-Euro03.png](https://yms.main.jp/dotartworld/vx/sozai/%21%24Gate-Euro03.png) | 240×256 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |
| [Cupnoodle.png](https://yms.main.jp/dotartworld/vx/sozai/Cupnoodle.png) | 256×128 | × 実在の商品（商標）なので使わない |
| [European-StyleHouseSet.zip](https://yms.main.jp/dotartworld/vx/sozai/European-StyleHouseSet.zip) |  | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |
| [Kagamimochi.png](https://yms.main.jp/dotartworld/vx/sozai/Kagamimochi.png) | 160×64 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |
| [Wa-Season01.png](https://yms.main.jp/dotartworld/vx/sozai/Wa-Season01.png) | 128×128 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |
| [Wall-MV01.png](https://yms.main.jp/dotartworld/vx/sozai/Wall-MV01.png) | 192×240 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |
| [Wall01.png](https://yms.main.jp/dotartworld/vx/sozai/Wall01.png) | 128×128 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |

### `dotartworld/vx/sozai/psam_washitsu/`（1点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [smt_wa12.png](https://yms.main.jp/dotartworld/vx/sozai/psam_washitsu/smt_wa12.png) | 288×230 | △ ツクール専用の可能性（旧サイトVX素材。使う前に表記を確認） |

### `page-m2/`（12点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [autotile_park.png](https://yms.main.jp/page-m2/autotile_park.png) | 256×192 | ○ |
| [park01.png](https://yms.main.jp/page-m2/park01.png) | 352×272 | × サンプル（使用NG） |
| [park02.png](https://yms.main.jp/page-m2/park02.png) | 352×272 | × サンプル（使用NG） |
| [park03.png](https://yms.main.jp/page-m2/park03.png) | 352×272 | × サンプル（使用NG） |
| [park04.png](https://yms.main.jp/page-m2/park04.png) | 352×272 | × サンプル（使用NG） |
| [park05.png](https://yms.main.jp/page-m2/park05.png) | 352×272 | × サンプル（使用NG） |
| [park06.png](https://yms.main.jp/page-m2/park06.png) | 352×272 | × サンプル（使用NG） |
| [park07.png](https://yms.main.jp/page-m2/park07.png) | 352×272 | × サンプル（使用NG） |
| [park08.png](https://yms.main.jp/page-m2/park08.png) | 352×272 | × サンプル（使用NG） |
| [parkobject.png](https://yms.main.jp/page-m2/parkobject.png) | 256×288 | ○ |
| [street_tree1.png](https://yms.main.jp/page-m2/street_tree1.png) | 256×256 | ○ |
| [vending_machine1.png](https://yms.main.jp/page-m2/vending_machine1.png) | 192×192 | ○ |

### `sozai1/chara/chara_doors/`（12点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [!$Door-Balcony01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21%24Door-Balcony01.png) | 192×384 | ○ |
| [!$Door-Cafe01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21%24Door-Cafe01.png) | 96×256 | ○ |
| [!$Door-Cafe02.png](https://yms.main.jp/sozai1/chara/chara_doors/%21%24Door-Cafe02.png) | 96×256 | ○ |
| [!$Door-Fence01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21%24Door-Fence01.png) | 192×192 | ○ |
| [!$Door-GBath01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21%24Door-GBath01.png) | 192×256 | ○ |
| [!$Door-GBath02.png](https://yms.main.jp/sozai1/chara/chara_doors/%21%24Door-GBath02.png) | 96×256 | ○ |
| [!$Door-Ger01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21%24Door-Ger01.png) | 96×192 | ○ |
| [!$Door-NobleHouse01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21%24Door-NobleHouse01.png) | 288×384 | ○ |
| [!$Door-Prison01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21%24Door-Prison01.png) | 288×256 | ○ |
| [!Door-FArch01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21Door-FArch01.png) | 768×512 | ○ |
| [!Door-FTown01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21Door-FTown01.png) | 384×512 | ○ |
| [!Door-FTownInside01.png](https://yms.main.jp/sozai1/chara/chara_doors/%21Door-FTownInside01.png) | 384×512 | ○ |

### `sozai1/chara/chara_light/`（5点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [!$PW-Lantan01.png](https://yms.main.jp/sozai1/chara/chara_light/%21%24PW-Lantan01.png) | 96×128 | ○ |
| [!$PW-Lantan02.png](https://yms.main.jp/sozai1/chara/chara_light/%21%24PW-Lantan02.png) | 96×128 | ○ |
| [!$PW-LantanVIllage01.png](https://yms.main.jp/sozai1/chara/chara_light/%21%24PW-LantanVIllage01.png) | 288×320 | ○ |
| [!$PW-LantanVIllage02.png](https://yms.main.jp/sozai1/chara/chara_light/%21%24PW-LantanVIllage02.png) | 288×384 | ○ |
| [!PW-Candle01.png](https://yms.main.jp/sozai1/chara/chara_light/%21PW-Candle01.png) | 768×512 | ○ |

### `sozai1/chara/chara_object/`（22点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [!$PW-Boat01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Boat01.png) | 384×512 | ○ |
| [!$PW-Chest-Wood.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Chest-Wood.png) | 96×128 | ○ |
| [!$PW-Drumfire.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Drumfire.png) | 96×192 | ○ |
| [!$PW-Fire01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Fire01.png) | 96×128 | ○ |
| [!$PW-FireCook01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-FireCook01.png) | 96×192 | ○ |
| [!$PW-Megami01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Megami01.png) | 96×384 | ○ |
| [!$PW-Momo.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Momo.png) | 192×192 | ○ |
| [!$PW-Pointer01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Pointer01.png) | 96×128 | ○ |
| [!$PW-Rainbow01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Rainbow01.png) | 528×512 | ○ |
| [!$PW-Swirl01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Swirl01.png) | 480×640 | ○ |
| [!$PW-Town-Tower01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Town-Tower01.png) | 288×704 | ○ |
| [!$PW-Town-Tower02.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Town-Tower02.png) | 288×704 | ○ |
| [!$PW-Trolley01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-Trolley01.png) | 150×256 | ○ |
| [!$PW-UnkoB01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-UnkoB01.png) | 192×192 | ○（うんこネタ。使うかは場面次第） |
| [!$PW-UnkoS01.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-UnkoS01.png) | 96×128 | ○（うんこネタ。使うかは場面次第） |
| [!$PW-UnkoS02.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-UnkoS02.png) | 96×128 | ○（うんこネタ。使うかは場面次第） |
| [!$PW-UnkoS03.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-UnkoS03.png) | 96×128 | ○（うんこネタ。使うかは場面次第） |
| [!$PW-WallLion.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PW-WallLion.png) | 96×384 | ○ |
| [!$PWLaundry.png](https://yms.main.jp/sozai1/chara/chara_object/%21%24PWLaundry.png) | 96×128 | ○ |
| [!PW-Barricade01.png](https://yms.main.jp/sozai1/chara/chara_object/%21PW-Barricade01.png) | 96×256 | ○ |
| [!PW-Sign01.png](https://yms.main.jp/sozai1/chara/chara_object/%21PW-Sign01.png) | 384×256 | ○ |
| [!PW-Sign02.png](https://yms.main.jp/sozai1/chara/chara_object/%21PW-Sign02.png) | 384×512 | ○ |

### `sozai1/chara/chara_walk/`（13点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [!$PEdoinu01.png](https://yms.main.jp/sozai1/chara/chara_walk/%21%24PEdoinu01.png) | 96×128 | ○ |
| [$PW-Ani-Lama01.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-Ani-Lama01.png) | 144×256 | ○ |
| [$PW-DogBeagle01.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-DogBeagle01.png) | 120×160 | ○ |
| [$PW-DogOsuwari01.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-DogOsuwari01.png) | 192×192 | ○ |
| [$PW-DogOsuwari02.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-DogOsuwari02.png) | 96×128 | ○ |
| [$PW-DogRetriever01.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-DogRetriever01.png) | 192×192 | ○ |
| [$PW-DogRetriever02.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-DogRetriever02.png) | 192×192 | ○ |
| [$PW-DogSheepdog01.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-DogSheepdog01.png) | 192×192 | ○ |
| [$PW-Moai01.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-Moai01.png) | 96×320 | ○ |
| [$PW-Moai02.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-Moai02.png) | 96×320 | ○ |
| [$PW-Moai03.png](https://yms.main.jp/sozai1/chara/chara_walk/%24PW-Moai03.png) | 96×320 | ○ |
| [PW-Ani-Hose01.png](https://yms.main.jp/sozai1/chara/chara_walk/PW-Ani-Hose01.png) | 1152×640 | ○ |
| [PW-Ani-Unicorn01.png](https://yms.main.jp/sozai1/chara/chara_walk/PW-Ani-Unicorn01.png) | 960×640 | ○ |

### `sozai1/looseleaf/`（6点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [$LF-Chara-Unko01.png](https://yms.main.jp/sozai1/looseleaf/%24LF-Chara-Unko01.png) | 96×256 | ○（うんこネタ。使うかは場面次第） |
| [$LF-Chara-Unko02.png](https://yms.main.jp/sozai1/looseleaf/%24LF-Chara-Unko02.png) | 96×256 | ○（うんこネタ。使うかは場面次第） |
| [LF-Chara-Sogen01.png](https://yms.main.jp/sozai1/looseleaf/LF-Chara-Sogen01.png) | 384×512 | ○ |
| [LF-Parts-Sogen01.png](https://yms.main.jp/sozai1/looseleaf/LF-Parts-Sogen01.png) | 384×512 | ○ |
| [LF-Parts-Unkoboshi01.png](https://yms.main.jp/sozai1/looseleaf/LF-Parts-Unkoboshi01.png) | 96×256 | ○（うんこネタ。使うかは場面次第） |
| [LF-Parts-Unkoboshi02.png](https://yms.main.jp/sozai1/looseleaf/LF-Parts-Unkoboshi02.png) | 96×256 | ○（うんこネタ。使うかは場面次第） |

### `sozai1/tile_inside_f1/`（16点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Cave1-A1.png](https://yms.main.jp/sozai1/tile_inside_f1/Cave1-A1.png) | 512×384 | ○ |
| [Cave1-A2.png](https://yms.main.jp/sozai1/tile_inside_f1/Cave1-A2.png) | 512×384 | ○ |
| [Cave1-EarthA5.png](https://yms.main.jp/sozai1/tile_inside_f1/Cave1-EarthA5.png) | 256×512 | ○ |
| [Cave1-EarthB.png](https://yms.main.jp/sozai1/tile_inside_f1/Cave1-EarthB.png) | 512×512 | ○ |
| [Cave1-MineC.png](https://yms.main.jp/sozai1/tile_inside_f1/Cave1-MineC.png) | 512×512 | ○ |
| [Cave1-RockA5.png](https://yms.main.jp/sozai1/tile_inside_f1/Cave1-RockA5.png) | 256×512 | ○ |
| [Cave1-RockB.png](https://yms.main.jp/sozai1/tile_inside_f1/Cave1-RockB.png) | 512×512 | ○ |
| [Ger-InsideA5.png](https://yms.main.jp/sozai1/tile_inside_f1/Ger-InsideA5.png) | 256×512 | ○ |
| [Ger-InsideB.png](https://yms.main.jp/sozai1/tile_inside_f1/Ger-InsideB.png) | 512×512 | ○ |
| [Inside-CastleTown-B.png](https://yms.main.jp/sozai1/tile_inside_f1/Inside-CastleTown-B.png) | 512×512 | ○ |
| [Inside-CastleTown-C.png](https://yms.main.jp/sozai1/tile_inside_f1/Inside-CastleTown-C.png) | 512×512 | ○ |
| [Inside-Town-A2.png](https://yms.main.jp/sozai1/tile_inside_f1/Inside-Town-A2.png) | 512×384 | ○ |
| [Inside-Town-A4.png](https://yms.main.jp/sozai1/tile_inside_f1/Inside-Town-A4.png) | 512×480 | ○ |
| [Inside-Town-A5.png](https://yms.main.jp/sozai1/tile_inside_f1/Inside-Town-A5.png) | 256×512 | ○ |
| [Inside-Town-D.png](https://yms.main.jp/sozai1/tile_inside_f1/Inside-Town-D.png) | 512×512 | ○ |
| [Inside-Town-E.png](https://yms.main.jp/sozai1/tile_inside_f1/Inside-Town-E.png) | 512×512 | ○ |

### `sozai1/tile_inside_f1/mod_insidef1/`（3点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Pot01.png](https://yms.main.jp/sozai1/tile_inside_f1/mod_insidef1/Pot01.png) | 64×64 | ○ |
| [carpet-Stairs01.png](https://yms.main.jp/sozai1/tile_inside_f1/mod_insidef1/carpet-Stairs01.png) | 128×64 | ○ |
| [cave-parts.png](https://yms.main.jp/sozai1/tile_inside_f1/mod_insidef1/cave-parts.png) | 128×128 | ○ |

### `sozai1/tile_inside_g1/`（5点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Bath-A2.png](https://yms.main.jp/sozai1/tile_inside_g1/Bath-A2.png) | 512×384 | ○ |
| [Bath-A4.png](https://yms.main.jp/sozai1/tile_inside_g1/Bath-A4.png) | 512×480 | ○ |
| [Bath-Ie.png](https://yms.main.jp/sozai1/tile_inside_g1/Bath-Ie.png) | 512×512 | ○ |
| [Bath-Neko.png](https://yms.main.jp/sozai1/tile_inside_g1/Bath-Neko.png) | 512×512 | ○ |
| [Bath-Sento.png](https://yms.main.jp/sozai1/tile_inside_g1/Bath-Sento.png) | 512×512 | ○ |

### `sozai1/tile_inside_g1/mod_inside1/`（4点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Bath-marble.png](https://yms.main.jp/sozai1/tile_inside_g1/mod_inside1/Bath-marble.png) | 256×160 | ○ |
| [Bath-pink.png](https://yms.main.jp/sozai1/tile_inside_g1/mod_inside1/Bath-pink.png) | 192×144 | ○ |
| [Ike.png](https://yms.main.jp/sozai1/tile_inside_g1/mod_inside1/Ike.png) | 320×224 | ○ |
| [Shower-cartain.png](https://yms.main.jp/sozai1/tile_inside_g1/mod_inside1/Shower-cartain.png) | 64×128 | ○ |

### `sozai1/tile_outside1/`（9点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [WorldMap-A1.png](https://yms.main.jp/sozai1/tile_outside1/WorldMap-A1.png) | 512×384 | ○ |
| [WorldMap-A1Dark.png](https://yms.main.jp/sozai1/tile_outside1/WorldMap-A1Dark.png) | 512×384 | ○ |
| [WorldMap-A1Simple.png](https://yms.main.jp/sozai1/tile_outside1/WorldMap-A1Simple.png) | 512×384 | ○ |
| [WorldMap-A2.png](https://yms.main.jp/sozai1/tile_outside1/WorldMap-A2.png) | 512×384 | ○ |
| [WorldMap-A2Dark.png](https://yms.main.jp/sozai1/tile_outside1/WorldMap-A2Dark.png) | 512×384 | ○ |
| [WorldMap-A2Simple.png](https://yms.main.jp/sozai1/tile_outside1/WorldMap-A2Simple.png) | 512×384 | ○ |
| [WorldMap-B.png](https://yms.main.jp/sozai1/tile_outside1/WorldMap-B.png) | 512×512 | ○ |
| [WorldMap-C.png](https://yms.main.jp/sozai1/tile_outside1/WorldMap-C.png) | 512×512 | ○ |
| [WorldMap-D.png](https://yms.main.jp/sozai1/tile_outside1/WorldMap-D.png) | 512×512 | ○ |

### `sozai1/tile_outside1/mod_outside1/`（9点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Autotile-WorldMapField1.png](https://yms.main.jp/sozai1/tile_outside1/mod_outside1/Autotile-WorldMapField1.png) | 128×96 | ○ |
| [Autotile-WorldMapLava.png](https://yms.main.jp/sozai1/tile_outside1/mod_outside1/Autotile-WorldMapLava.png) | 192×96 | ○ |
| [Autotile-WorldMapMontain01.png](https://yms.main.jp/sozai1/tile_outside1/mod_outside1/Autotile-WorldMapMontain01.png) | 128×96 | ○ |
| [Autotile-WorldMapMontain02.png](https://yms.main.jp/sozai1/tile_outside1/mod_outside1/Autotile-WorldMapMontain02.png) | 128×96 | ○ |
| [Autotile-WorldMapRoad.png](https://yms.main.jp/sozai1/tile_outside1/mod_outside1/Autotile-WorldMapRoad.png) | 64×96 | ○ |
| [Autotile-WorldMapTree01.png](https://yms.main.jp/sozai1/tile_outside1/mod_outside1/Autotile-WorldMapTree01.png) | 128×96 | ○ |
| [WorldMapBridge.png](https://yms.main.jp/sozai1/tile_outside1/mod_outside1/WorldMapBridge.png) | 160×128 | ○ |
| [WorldMapRoad01.png](https://yms.main.jp/sozai1/tile_outside1/mod_outside1/WorldMapRoad01.png) | 96×160 | ○ |
| [WorldMapRoad02.png](https://yms.main.jp/sozai1/tile_outside1/mod_outside1/WorldMapRoad02.png) | 256×96 | ○ |

### `sozai1/tile_outside_f1/`（38点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Bridge1-F.png](https://yms.main.jp/sozai1/tile_outside_f1/Bridge1-F.png) | 512×512 | ○ |
| [BrightForest-A1.png](https://yms.main.jp/sozai1/tile_outside_f1/BrightForest-A1.png) | 512×384 | ○ |
| [BrightForest-A2.png](https://yms.main.jp/sozai1/tile_outside_f1/BrightForest-A2.png) | 512×384 | ○ |
| [BrightForest-A5.png](https://yms.main.jp/sozai1/tile_outside_f1/BrightForest-A5.png) | 256×512 | ○ |
| [BrightForest-B.png](https://yms.main.jp/sozai1/tile_outside_f1/BrightForest-B.png) | 512×512 | ○ |
| [CastleTown-A5-1.png](https://yms.main.jp/sozai1/tile_outside_f1/CastleTown-A5-1.png) | 256×512 | ○ |
| [CastleTown-B.png](https://yms.main.jp/sozai1/tile_outside_f1/CastleTown-B.png) | 512×512 | ○ |
| [CastleTown-C-1.png](https://yms.main.jp/sozai1/tile_outside_f1/CastleTown-C-1.png) | 512×512 | ○ |
| [CastleTownBF-A2.png](https://yms.main.jp/sozai1/tile_outside_f1/CastleTownBF-A2.png) | 512×384 | ○ |
| [ConiferForest-A1-1.png](https://yms.main.jp/sozai1/tile_outside_f1/ConiferForest-A1-1.png) | 512×385 | ○ |
| [ConiferForest-A1-2.png](https://yms.main.jp/sozai1/tile_outside_f1/ConiferForest-A1-2.png) | 512×385 | ○ |
| [ConiferForest-A5-1.png](https://yms.main.jp/sozai1/tile_outside_f1/ConiferForest-A5-1.png) | 256×512 | ○ |
| [ConiferForest-A5-2.png](https://yms.main.jp/sozai1/tile_outside_f1/ConiferForest-A5-2.png) | 256×512 | ○ |
| [ConiferForest-B-1.png](https://yms.main.jp/sozai1/tile_outside_f1/ConiferForest-B-1.png) | 512×512 | ○ |
| [ConiferForest-B-2.png](https://yms.main.jp/sozai1/tile_outside_f1/ConiferForest-B-2.png) | 512×512 | ○ |
| [DeepForest-A1.png](https://yms.main.jp/sozai1/tile_outside_f1/DeepForest-A1.png) | 512×384 | ○ |
| [DeepForest-A2.png](https://yms.main.jp/sozai1/tile_outside_f1/DeepForest-A2.png) | 512×384 | ○ |
| [DeepForest-A5.png](https://yms.main.jp/sozai1/tile_outside_f1/DeepForest-A5.png) | 256×512 | ○ |
| [DeepForest-B.png](https://yms.main.jp/sozai1/tile_outside_f1/DeepForest-B.png) | 512×512 | ○ |
| [Ger-OutsideB.png](https://yms.main.jp/sozai1/tile_outside_f1/Ger-OutsideB.png) | 512×512 | ○ |
| [Market-D.png](https://yms.main.jp/sozai1/tile_outside_f1/Market-D.png) | 512×512 | ○ |
| [NobleHouseA5.png](https://yms.main.jp/sozai1/tile_outside_f1/NobleHouseA5.png) | 256×512 | ○ |
| [NobleHouseC.png](https://yms.main.jp/sozai1/tile_outside_f1/NobleHouseC.png) | 512×512 | ○ |
| [Ruin-F.png](https://yms.main.jp/sozai1/tile_outside_f1/Ruin-F.png) | 512×512 | ○ |
| [Tent-F.png](https://yms.main.jp/sozai1/tile_outside_f1/Tent-F.png) | 512×512 | ○ |
| [Town-PostTown-C-1.png](https://yms.main.jp/sozai1/tile_outside_f1/Town-PostTown-C-1.png) | 512×512 | ○ |
| [TownBF-A2.png](https://yms.main.jp/sozai1/tile_outside_f1/TownBF-A2.png) | 512×384 | ○ |
| [TownBF-B.png](https://yms.main.jp/sozai1/tile_outside_f1/TownBF-B.png) | 512×512 | ○ |
| [TownBF-Forest-A5.png](https://yms.main.jp/sozai1/tile_outside_f1/TownBF-Forest-A5.png) | 256×512 | ○ |
| [TownBF-Forest-C.png](https://yms.main.jp/sozai1/tile_outside_f1/TownBF-Forest-C.png) | 512×512 | ○ |
| [TownBF-PostTown-A5-1.png](https://yms.main.jp/sozai1/tile_outside_f1/TownBF-PostTown-A5-1.png) | 256×512 | ○ |
| [TownBF-PostTown-A5-2.png](https://yms.main.jp/sozai1/tile_outside_f1/TownBF-PostTown-A5-2.png) | 256×512 | ○ |
| [TownDF-A2.png](https://yms.main.jp/sozai1/tile_outside_f1/TownDF-A2.png) | 512×384 | ○ |
| [TownDF-B.png](https://yms.main.jp/sozai1/tile_outside_f1/TownDF-B.png) | 512×512 | ○ |
| [Village1-A5.png](https://yms.main.jp/sozai1/tile_outside_f1/Village1-A5.png) | 256×512 | ○ |
| [Village1-C.png](https://yms.main.jp/sozai1/tile_outside_f1/Village1-C.png) | 512×513 | ○ |
| [Village1-D.png](https://yms.main.jp/sozai1/tile_outside_f1/Village1-D.png) | 512×512 | ○ |
| [WallOutside-Fantasy1-A4.png](https://yms.main.jp/sozai1/tile_outside_f1/WallOutside-Fantasy1-A4.png) | 512×480 | ○ |

### `sozai1/tile_outside_f1/mod_outside_f1/`（5点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [Autotile-Forest01.png](https://yms.main.jp/sozai1/tile_outside_f1/mod_outside_f1/Autotile-Forest01.png) | 64×96 | ○ |
| [Autotile-RuinA4.png](https://yms.main.jp/sozai1/tile_outside_f1/mod_outside_f1/Autotile-RuinA4.png) | 192×160 | ○ |
| [Field-Rise01.png](https://yms.main.jp/sozai1/tile_outside_f1/mod_outside_f1/Field-Rise01.png) | 288×128 | ○ |
| [Kakashi.png](https://yms.main.jp/sozai1/tile_outside_f1/mod_outside_f1/Kakashi.png) | 160×64 | ○ |
| [ParasolTable.png](https://yms.main.jp/sozai1/tile_outside_f1/mod_outside_f1/ParasolTable.png) | 448×256 | ○ |

### `sozai1/tile_outside_f1/woditor/`（1点）

| ファイル | 大きさ(px) | 判定 |
|---|---|---|
| [[BASE]NobleHouse1.png](https://yms.main.jp/sozai1/tile_outside_f1/woditor/[BASE]NobleHouse1.png) | 256×3520 | ○ |
