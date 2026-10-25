# 現代的なシンセの音の作り方（学習）と、作曲ソフトの新しいシンセ10種

2026-10-25 記録。人間「電子音をもっと現代的に。なんかボカロっぽいシンセじゃない。シンセの音も勉強してきて」。
調べたこと（Serum・Vital のレシピ、DTM 解説）をもとに、`tools/soundfont/build-modern-synths.py` で10種を合成した（自作・CC0 扱い。外部の録音は使っていない）。
数値の多くは画面写真にしか載っていないため、本文に数値があった資料（Syntorial・Cymatics・Native Instruments・FaderPro・Attack Magazine など）を優先し、ないものは定石としてまとめた。

## 調べた作り方（要点）
- リード（[Syntorial](https://www.syntorial.com/ja/preset-recipe/league-of-legends-rise-worlds-2018-ft-glitch-mob-and-mako-lead)）: ソー6本のユニゾン（音程が揺れない程度のにじみ）＋1オクターブ下を小さく。チューブ風の歪み → ローパス 24dB。歌わせるときはビブラート 5〜6Hz・±15〜30cent を 0.25〜0.4 秒遅らせ、しゃくりは −50〜−100cent から 40〜80ms。
- スーパーソウ（[FaderPro](https://blog.faderpro.com/techniques/supersaw-how-make-iconic-sound/)・[Loopmasters](https://www.loopmasters.com/articles/4372-How-To-Make-A-Future-Bass-Drop-A-Future-Bass-Production-Tutorial)）: 7〜16本、デチューンは控えめ（Vital で 20% 前後。50% を超えると濁る）、1オクターブ下に3本の層、ハイパス。外側ほど大きくずらす（JP-8000 の分析）。
- フューチャーベースの和音（[Syntorial](https://www.syntorial.com/preset-recipe/embrz-higher-chords/)・[Sleep Freaks](https://sleepfreaks-dtm.com/en/softsynth/xfer-lfo-tool)）: ユニゾン8・広がり100%、ハイパス 270Hz、音量のうねり（4分・8分。遅れて立ち上がる形）はサイドチェインで。7th・9th の和音。
- プラック（[Cymatics](https://cymatics.fm/blogs/production/creating-plucks-xfer-serum)）: 鳴り始めに約 20ms のピッチの下り、オシレーターのずらしは 30cent まで、フィルターエンベロープ D 150〜250ms・S 0。
- ベル: FM で整数でない比（1:3.5 など）、変調の深さを時間で下げる（[Cycling '74](https://docs.cycling74.com/max8/tutorials/06_synthesischapter05)）。
- ベース: リースは ±15〜30cent・ローパス 650Hz（[Native Instruments](https://blog.native-instruments.com/reese-bass/)）。808 はポルタメント 300ms（[Attack Magazine](https://www.attackmagazine.com/technique/synth-secrets/808-bass-with-saturation/)）。
- ボーカルチョップ風: 女性の「あ」の響きの山 850/1220/2810Hz（[CCRMA](https://ccrma.stanford.edu/~kglee/m220c/formant.html)）。
- 作り手: DECO*27 はハードスタイル・エレクトロスウィング・ベースハウス・ダブステップを混ぜる（[Real Sound](https://realsound.jp/2024/12/post-1863289_2.html)）。ピノキオピーは打ち込みならではの勢いと切り貼り（[Real Sound](https://realsound.jp/2026/10/post-2552765.html)）。TAKU INOUE は後ろから包まれる音場（[Real Sound](https://realsound.jp/2021/07/post-815201.html)）。Kawaii Future Bass はおもちゃのようなベル・矩形波（[Bandcamp](https://daily.bandcamp.com/2018/03/23/kawaii-japanese-electronic-feature)）。

## 作曲ソフトの新しいシンセ（patch 名 → GM の空き番号）
| patch | 中身 | 使う所 |
|---|---|---|
| `modernLead`（1） | ソー6本 ±12cent・広がり 0.4＋1オクターブ下のソー −12dB、tanh 2.5倍 → ローパス 24dB（5.5kHz へ下がる）、2.5kHz +2dB | 歌の役 |
| `brightLead`（112） | ソー7本 ±22cent＋1オクターブ上を小さく、ローパス 9kHz、軽い歪み | サビ・ソロ |
| `modernSupersaw`（5） | ソー9本 ±28cent（外側ほど大きく）・左右いっぱい＋1オクターブ下3本、基音でハイパス | サビの和音の壁 |
| `fbChord`（10） | ソー8本 ±12cent・広がり100%＋1オクターブ上の矩形、ローパスが開く、ハイパス 220Hz | フューチャーベースの和音（duck でうねり） |
| `modernPad`（74） | ソー7本 ±18＋三角、ローパス 2.6kHz、ハイパス 220Hz、アタック 0.6 秒 | 広がるパッド |
| `modernPluck`（23） | ソー3本＋矩形、ピッチ +12半音から 12ms で戻る、フィルター 10kHz → 900Hz（0.12 秒） | Aメロの刻み・アルペジオ |
| `kawaiiArp`（76） | 矩形 25%＋三角、フィルター 7kHz → 2.5kHz、0.22 秒で減衰 | かわいいアルペジオ |
| `popBell`（31） | FM 1:3.5（深さが 0.4 秒で減る）＋オクターブ上の FM | キラキラ |
| `vocalChop`（69） | ソー＋矩形＋息のノイズを、女性の「あ」の響きの山（850/1220/2810/3900Hz）に通す。0.18 秒で切れる | ボーカルチョップ風の合いの手（声ではない） |
| `modernBass`（44） | ソー2本 ±8＋サブのサイン、フィルター 3kHz → 1.1kHz、歪み、800Hz・2kHz を上げてゴリッと | シンセベース |

- 伸ばす音（リード・スーパーソウ・和音・パッド・ベース）はループ。つなぎ目の差は 0.5% 以下（全オシレーターの周期の数を整数にそろえた）。
- 試聴: 10種を8秒ずつ鳴らした mp3 を人間に送った（2026-10-25）。最後は耳で判断する。
