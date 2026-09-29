# 作曲ソフトに同梱するNAMモデル

入手元: Neural Amp Modeler Core のリポジトリ（https://github.com/sdatkinson/NeuralAmpModelerCore ）の `example_models/`
取得日: 2026-09-30（コミット 0b3d3c97b0859a3a8c92a8628c4dd89a25eb5842）

リポジトリ全体が MIT ライセンス（`LICENSE-NeuralAmpModelerCore.txt`、© 2023 Steven Atkinson）で、`example_models/` に別の規約はない。
MIT なので、商用利用・改変・再配布ができる（著作権表示と許諾文を含めること）。

| このフォルダの名前 | 元のファイル | 作曲ソフトでの名前 | 調べた特徴 |
|---|---|---|---|
| `highgain-a.nam` | `A2.nam` | ハイゲインアンプA | 強く歪む（小さな入力でも出力がほぼ一定。倍音が多い） |
| `highgain-b.nam` | `my_model.nam` | ハイゲインアンプB | 強く歪む（標準のWaveNet） |
| `bass-preamp.nam` | `wavenet.nam` | ベース用プリアンプ | 小さな入力ではきれい、大きな入力で少し歪む |

- 作曲ソフト（`tools/composer/build.mjs`）だけが埋め込む。ゲーム本体には入れない。
- モデルの中の説明（機材のメーカー名など）は、画面には出さない。
