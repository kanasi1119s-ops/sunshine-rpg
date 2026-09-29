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
| ぴぽや「フィールドマップセット１」「同 追加パーツ」（`pipo-map001.zip`・`pipo-map001plus.zip`） | https://pipoya.net/sozai/assets/map-chip_tileset32/ | 2026-09-30 | 取得・規約確認済み、元ファイルは `assets-src/pipoya/`。**ゲームに反映済み（2026-09-30）**: 地形テクスチャ5点（草A・草B・土の道・水面・深い森。128×128）に、自動タイルの中央の1枚を並べ、色を24色に減らして使用（`tools/pixel-art/import-pipoya.mjs` → `pipoya-terrain.json` → `export-game-data.mjs` → `src/game/art/sprite-data.generated.ts`）。建物・城・山などの他の絵は未使用 | 無料素材利用規約（https://pipoya.net/sozai/terms-of-use/ ）と同梱の readme を確認。商用利用可、加工可、無償の再配布可（規約とともに）、ゲームへの組み込み・販売可。禁止は素材としての販売（転売）。要点は `assets-src/pipoya/LICENSE-pipoya.md` | 不要（お礼として README・ゲーム内クレジットに「ぴぽや https://pipoya.net/」と書く予定） |
| FluidR3 Mono GM サウンドフォント（`FluidR3Mono_GM.sf3`。npm `@librescore/sf3` 0.8.0 に同梱） | https://www.npmjs.com/package/@librescore/sf3 （原典: Frank Wen「Fluid (R3) GM」、Michael Cowgill による Mono 版） | 2026-09-30 | BGMの録音音源。ゲームで使う楽器（GMの17種＋ドラム6セット）だけを `tools/soundfont/trim-soundfont.mjs` で切り出し、`src/audio/soundfont/game.sf3`（約3.3MB）としてゲームに同梱。元ファイルは `assets-src/soundfont/` | MITライセンス（`assets-src/soundfont/LICENSE-FluidR3.md`）。商用利用・改変・再配布・ゲームへの組み込みは可。**著作権表示と許諾文を配布物に含める条件**あり（`public/licenses/FluidR3-GM-MIT.txt` をゲームに同梱、README にも表記）。同梱のサンプルは、パブリックドメインの素材と作者本人の録音、Ethan Winer 氏・Michael Schorsch 氏の提供分 | 必要（README・ゲーム内クレジットに「Fluid (R3) GM SoundFont © Frank Wen / Mono版 © Michael Cowgill（MIT）」と書く） |
| spessasynth_lib / spessasynth_core（サウンドフォント再生ライブラリ。npm） | https://github.com/spessasus/spessasynth_lib | 2026-09-30 | BGMの再生（`src/audio/sampled-engine.ts`） | Apache-2.0。商用利用・改変・再配布は可。ライセンス文を同梱する条件あり（`public/licenses/spessasynth-Apache-2.0.txt`） | 必要（README に表記） |
| Neural Amp Modeler Core（WASM版 `@opendaw/nam-wasm`。npm） | https://github.com/sdatkinson/NeuralAmpModelerCore （WASM版: https://www.npmjs.com/package/@opendaw/nam-wasm ） | 2026-09-30 | 作曲ソフトのアンプシミュレーター（`src/audio/nam/`）。作曲ソフト（`tools/composer/`）にだけ埋め込み、ゲーム本体には入れない | MITライセンス（© 2023 Steven Atkinson）。商用利用・改変・再配布は可。著作権表示と許諾文を含める条件あり。.namモデルは同梱していない。利用者が読み込むモデルは、モデルごとに配布元の規約（商用利用・再配布）を確認する。ゲームにはモデルを入れない | 必要（README に表記） |
| NAMの見本モデル3つ（NeuralAmpModelerCore の `example_models/` の `A2.nam`・`my_model.nam`・`wavenet.nam`） | https://github.com/sdatkinson/NeuralAmpModelerCore （コミット 0b3d3c9） | 2026-09-30 | 作曲ソフトの同梱アンプ（ハイゲインアンプA・B、ベース用プリアンプ）。元ファイルは `assets-src/nam-models/`。ゲーム本体には入れない | リポジトリ全体が MITライセンス（© 2023 Steven Atkinson）で、`example_models/` に別の規約はない。商用利用・改変・再配布は可。著作権表示と許諾文を含める（`assets-src/nam-models/LICENSE-NeuralAmpModelerCore.txt`、`public/licenses/NeuralAmpModelerCore-MIT.txt`）。モデル内の機材メーカー名は画面に出さない | 必要（README に表記） |

## 素材の置き場
- 元ファイル: `assets-src/`（規約の写しも一緒に置く）
- ゲームに読み込む形（色番号のRLEなど）に変換したもの: `src/game/art/`

## メモ
- 2026-09-30: BGMを録音音源で鳴らすため、サウンドフォントを探した。**GeneralUser GS**（ライセンスは商用利用可だが、作者自身が「サンプルの出どころは100%確認できていない」と明記）は、出どころが不明確なため使わなかった。**MuseScore General**（MIT・一部CC0/PD、出どころが明記）は40MBで大きすぎたため見送り。**FluidR3 Mono GM**（MIT、出どころの明記あり）を採用した。より高品質にしたくなったら、MuseScore General Lite（約40MB）への差し替えを検討する（容量予算は人間が拡大を許可済み）。
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

