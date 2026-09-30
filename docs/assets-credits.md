# 外部素材の記録（出典・規約・クレジット）

無料で商用利用できる素材を使うときの記録です（`CLAUDE.md` 1-1 の例外の運用）。素材を1つ使うごとに、下の表に1行足します。

## 記録のしかた
- 素材名・入手元（URL）・入手日・使った場所（ファイルや画面）
- 利用規約の要点（商用利用、加工・改変、クレジット、再配布、ゲームへの組み込み）。読んだ規約のURLも書く
- クレジット表記が必要か（必要なら、ゲーム内クレジットまたは README に書いたか）
- 規約が読めない・不明な素材は、使わない

## 使用中の素材

| 素材名 | 入手元 | 入手日 | 使った場所 | 規約の要点 | クレジット |
|---|---|---|---|---|---|
| ぴぽや「フィールドマップセット１」「同 追加パーツ」（`pipo-map001.zip`・`pipo-map001plus.zip`） | https://pipoya.net/sozai/assets/map-chip_tileset32/ | 2026-09-30 | 元ファイルは `assets-src/pipoya/`。2026-09-30から、マップの地形（草・道・水・森）の128×128テクスチャに使用（`tools/pixel-art/import-pipoya.mjs`で32×32チップを26色に減色・向きを変えて並べ、`src/game/art/sprite-data.generated.ts`に書き出し） | 無料素材利用規約（https://pipoya.net/sozai/terms-of-use/ ）と同梱の readme を確認。商用利用可、加工可、無償の再配布可（規約とともに）、ゲームへの組み込み・販売可。禁止は素材としての販売（転売）。要点は `assets-src/pipoya/LICENSE-pipoya.md` | 不要（お礼として README に「ぴぽや https://pipoya.net/」と記載済み（ゲーム内クレジット画面は未実装。作る際に追記する）） |

## 素材の置き場
- 元ファイル: `assets-src/`（規約の写しも一緒に置く）
- ゲームに読み込む形（色番号のRLEなど）に変換したもの: `src/game/art/`

## メモ
- 2026-09-29: 人間から「ぴぽや倉庫（https://pipoya.net/sozai/ ）の無料素材を使う、または参考にする」との指示があった。ただし、この作業環境のネットワークからはpipoya.netに接続できず、素材の取得も規約の確認もできなかった。人間が素材をダウンロードして `assets-src/pipoya/` に置いた時点で、規約（素材に付属のreadmeなど）を確認し、上の表に記録する。
- 2026-09-30: パソコンのClaude Code＋Chrome拡張で、ぴぽや倉庫の規約ページと素材ページを確認し、上の2点を取得した（ダウンロード・展開とも人間の承認済み）。
- 2026-09-30: ぴぽや素材の、生成AI・AI学習・AIが作った作品での利用についての記述を確認した。**結果: 記述なし**（禁止も制限も、許可の明記もない）。
  - 確認した範囲: (1) 素材利用規約 https://pipoya.net/sozai/terms-of-use/ の本文全体（冒頭の「素材利用規約」から末尾の「素材利用許諾者・許諾作品」の表記例まで。無料素材・有料素材・支援サイト限定素材の各規約と特殊事項を含む。約1.1万字）。(2) `assets-src/pipoya/pipo-map001/readme.txt`、`assets-src/pipoya/pipo-map001plus/readme.txt`
  - 確認の方法: Chromeで全文を読んだうえで、本文を取得して「AI」「ＡＩ」「人工知能」「生成」「学習」「機械」「データセット」「ディープ」「深層」「NFT」などの語を検索した
  - 検索に当たったのは「学習」の2か所だけで、どちらも有料素材・支援サイト限定素材の「Scratchでの利用について」にある、購入者自身の学習目的でローカル環境で使うことの話。AIとは関係ない
  - 規約には「予告なく追加変更する場合がある」とあるため、素材を追加で使うときや公開前には、あらためて確認する

## 使わないと決めた素材（2026-09-30 確認）
人間から紹介された Seliel the Shaper（Mana Seed）の素材。Chromeで価格と Mana Seed User License（https://selieltheshaper.weebly.com/user-license.html ）を確認した。

| 素材名 | URL | 価格 | 判断 |
|---|---|---|---|
| Iconic Homestead | https://seliel-the-shaper.itch.io/iconic-homestead | 有料（19.99ドル〜） | 使わない |
| Muddy Cave | https://seliel-the-shaper.itch.io/muddy-cave | 有料（19.99ドル〜） | 使わない |
| Gentle Forest | https://seliel-the-shaper.itch.io/gentle-forest | 無料（0ドル〜。払うと色違いが増える） | 使わない |

理由: 規約の「No GenAI」条項が、AIが作った絵・文章・コードなどと同じ作品で使うことを、例外なく禁じている。このゲームはAI（Claude）がコード・文章・絵を作っているため、無料・有料を問わず条件を満たせない。また Gentle Forest の無料版の色は、既存作品（聖剣伝説3）の各ステージを参考にしたと明記されており、CLAUDE.md 1-1 の点でも避ける。作者の意向を尊重し、技法の参考にもしない（人間の了承済み）。

