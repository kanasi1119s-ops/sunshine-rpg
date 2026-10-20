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

## 追加: Kay 703（ビンテージの真空管アンプ。2026-10-12）

入手元: TONE3000「Kay 703 NAM Profiles」by @aazuspan（https://www.tone3000.com/tones/kay-703-6302 ）
ライセンス: **CC0**（ページの表記は「cco」、説明文は CC0 の「with no conditions」。パブリックドメインへの献呈で、商用利用・改変・再配布・組み込みに条件なし）。クレジットは不要だが、敬意として記録する。
中身: 1960年代のKay 703（真空管）をSM57で近接録音。ゲイン3・5・7・10（トレブル5）。A2-Full版を使用（NAMの新形式 `SlimmableContainer`。同梱のWASMで読み込める）。

| このフォルダの名前 | 作曲ソフトでの名前 | AIソングの amp 名 | 測った特徴（440Hzでなく196Hzのサイン波、入力0.4） |
|---|---|---|---|
| `kay703-g3.nam` | ビンテージ真空管 ゲイン3 | `namKay3` | ほぼクリーン（ひずみ成分 16%） |
| `kay703-g5.nam` | ゲイン5 | `namKay5` | クランチ（12%） |
| `kay703-g7.nam` | ゲイン7 | `namKay7` | 深いクランチ（49%） |
| `kay703-g10.nam` | ゲイン10 | `namKay10` | ひずみ（54%） |

入力を小さくするとさらに浅くなる（`ampDrive`）。ハイゲインA・B（常に約27%）と違い、**弾く強さと入力でひずみが変わる**。軽い曲・クリアな曲向け。

## 追加: Dark Days のハイゲイン（2026-10-20）
`darkdays-ss-highgain-di.nam`（amp `namDD`）。入手元 https://darkdays.net 。CC BY 4.0（`LICENSE-darkdays-CC-BY-4.0.txt`）。クレジット必要: 「Amp capture by Dark Days — https://darkdays.net (CC BY 4.0)」。アンプだけ（キャビネットIRを通す）。

## 追加: マーシャルの中くらいの歪み（2026-10-21、試用中）
`marshall-jvm-g4.nam`（amp `namJVM`）。Marshall JVM 410H Dataset（CC BY 4.0、doi:10.5281/zenodo.7970723）の OD1・ゲイン4 から、この作曲ソフトで学習（neural-amp-modeler 0.13、WaveNet、ESR 0.050）。クレジットと注意点は `docs/assets-credits.md`。

## 外したもの
Kay 703（`kay703-g3〜g10.nam`）は、入手元 TONE3000 の利用規約が再配布・商用配布を禁止しているため、2026-10-20 に外した（docs/decisions.md）。
