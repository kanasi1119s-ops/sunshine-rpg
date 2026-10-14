# Suno との差の調べと、足した音源の記録

作成: 2026-10-14（音質の調査・音源の調達の担当）。依頼は「いつまでたっても Suno みたいな品質の音が出ない。徹底的に学び、足りなければ使える音源を足す」。
この文書は、(A) 差の原因の調べ、(B) 無料で商用利用できる音源の調査、(C) 変換して作曲ソフトで使える形にした記録、の3部と、次に動く人へのお願いをまとめる。

## 読み方（確からしさの印）

| 印 | 意味 |
|---|---|
| 【実測】 | 今回、自分の曲の音声ファイルを測った、または音源を実際に変換・鳴らして確かめた数字 |
| 【一次】 | 今回、公式ページ・論文・ライセンス本文を直接取りに行って読んだ事実（URL つき） |
| 【参考値】 | 日本一フリーBGM 1000曲（Suno 製）を測った既存の統計（`docs/sound/data/nihonichi-bgm-1000-metrics.json`）。Suno 全体の代表ではない。「Suno の代理」として使うが、あくまで1000曲の測定値 |
| 【一般知識】 | ミキシング・マスタリングの定説で、今回は一次資料を取り直していないもの。数字は目安で、鵜呑みにしない |
| 【推測】 | 上の材料からの推論。まちがっている可能性がある。確かめ方を添える |
| 【耳未確認】 | 数字では確かめたが、人が耳で聴いて確かめていない |

商用曲の音声は、ダウンロードも解析もしていない（依頼どおり）。Suno について書いた内容は、公開ページ・論文の抜粋と、既存の1000曲の測定値だけに基づく。

## 0. 先に読む要約（10の発見）

1. **差の本体は「音の数値」より「ステレオの位相」と「つぶしすぎ」にある。** 【実測】ロック曲 summer-rock3 は、1k〜8k の帯域で左右の相関が -0.48、サイド成分がミッドより 2〜4 dB 大きい（中域 +2.2、プレゼンス +3.9、空気 +3.4 dB）。Suno 製1000曲の中央値は、同じ帯域でサイドがミッドより 5〜7 dB 小さい（-5.3、-6.0、-7.5 dB）。しかも1000曲のうち、プレゼンス帯でサイドがミッドより大きい曲は 8 曲（0.8%）しかない【参考値】。作曲ソフトの広げ処理（widen 2.4）が、中高域で位相をずらして「広いのに芯がない」音にしている可能性が高い【推測】。
2. **音量を上げすぎている。** 【実測】統合ラウドネス -10.2 LUFS、クレストファクター 10.6 dB。Suno 1000曲は中央値 -13.4 LUFS（大きい側の p90 でも -12.0）、クレスト中央値 14.1 dB（下位10%でも 12.6）【参考値】。自分の曲は1000曲の「大きい側10%」の境目（-12.0）よりさらに 2 dB 大きく、クレストは1000曲の下位10%の境目（12.6）よりさらに 2 dB 低い。Spotify は -14 LUFS に合わせて下げる【一次】ので、-10 に上げても得にならず、つぶれた音だけが残る。
3. **mp3 の書き出しで真のピークが 0 dB を超えている。** 【実測】summer-d-jazzclean.mp3 が TP +2.0、summer-e-gretsch-lead.mp3 が +2.3、summer-c-crunch.mp3 が +1.3 dBTP。デコードで音割れを起こし得る。Spotify は損失圧縮向けに 1 dB の余裕を残す設計【一次】。真のピークは -1 dBTP 以下にそろえる。
4. **スペクトルの傾き（暗さ）は思ったほど大きな差ではない。** 【実測】傾き -4.9〜-6.2 dB/oct は、Suno 1000曲の ロック分類 p10〜p90（-6.95〜-2.96）に入る【参考値】。スペクトル重心が 170〜265 Hz と低いのは下位10%の端（ロックの p10 は 190 Hz）。「暗いからSunoっぽくない」という前提は半分しか当たらない。
5. **クリーンな電気ギターが決定的に足りなかった。** 既存のギター音源は、ジャズボディのギターや、すでに音づくりされたものだけで、ソリッドボディの素直な直接録音（DI）がなかった。FreePats の「FSBS Electric Guitar」（CC0）の DI を SF3 にして追加した。ただし音量が既存のギターより 12〜19 dB 大きいので、統合時に音量合わせが要る【実測】。
6. **打楽器の細かい音（シェイカー、タンバリン、ボンゴなど）は録音に差し替えられる。** 既存の GeneralUser のサンプルから、VCSL（CC0）と FreePats World Percussion（CC0）の録音に差し替えたドラム SF3 を6種類作った【実測：鳴ることを確認、耳未確認】。
7. **鍵盤の選択肢が増えた。** Wurlitzer EP200、Yamaha CP80、Hohner Pianet T（Greg Sullivan、CC BY 3.0。**クレジット必須**）、アップライトピアノ、ハモンド系オルガン3種、教会オルガン、ナイロンギター、シンセパッド4種を追加（FreePats は CC0）。
8. **ベース「Growlybass」（Squier Jazz Bass、CC0）を追加した。** Karoryfer の SFZ は実音より1オクターブ上に書かれているため、`--shift -12` が必要だった。直したあと、倍音の櫛型検査で音程のずれ 0 セントを確認した【実測】。
9. **人間の演奏らしさは音源より「ばらつき」にある。** Suno の曲は、時間のゆれ・強さのゆれ・弦の擦れ・息継ぎなどが録音に最初から混ざっている。音源側ではラウンドロビン（弾くたびに別の録音）と速度層を増やすのが効く。新しい FSBS ギターは強弱を速度1〜127に細かく割り当ててあり、人間味づけ（human）が効くようにした。
10. **今回の調査の限界。** WebSearch の回数が尽き、WebFetch は出どころの制限で使えなかったため、一次資料は curl で直接取りに行った。Suno の内部構造は非公開なので、原因は「測れる範囲の推測」にとどまる。耳での確認は一切できていない。

## 1. 調べ方と使えなかった手段

### 1.1 到達できたもの・できなかったもの【実測】

| 対象 | 結果 |
|---|---|
| github.com のリリース・git clone・ls-remote | 取得できた |
| raw.githubusercontent.com | 取得できた |
| freepats.zenvoid.org | 取得できた（SF2 一式） |
| sfzinstruments.github.io | 取得できた（一覧のみ） |
| arXiv（abs / html） | 取得できた |
| Wikipedia | 取得できた |
| support.spotify.com | 取得できた |
| voxengo.com / echothief.com / mcdermottlab.mit.edu | 取得できた（規約の確認） |
| openair.hosted.york.ac.uk | 空の応答（規約を読めず） |
| GitHub の API・組織ページ | 403 |
| musical-artifacts.com / zenodo / freesound | 403 |
| WebSearch | 回数の上限に達し使えなかった |
| WebFetch | 出どころの制限で使えなかった |

### 1.2 方針

- 規約が読めない素材は使わない（CLAUDE.md の例外の条件1）。
- 候補の列挙は、sfzinstruments の一覧と FreePats の各ページ、Karoryfer / VCSL の各リポジトリの LICENSE を直接読んで行った。
- 数値の比較は、自分の曲の音声（`tools/audio-check/analyze.py` と今回の追加の測定 `ext.py`）と、既存の Suno 代理統計で行った。

## 2. パートA: 自分の曲が Suno と違って聞こえる理由

### 2.1 測った曲

| 曲 | 種類 | 備考 |
|---|---|---|
| summer-rock3.wav | ロック、WAV | 最新の作曲ソフトの出力 |
| summer-rock2.wav | ロック、WAV | 1つ前 |
| summer-d-jazzclean.mp3 | クリーンジャズ調ギター、mp3 | |
| summer-e-gretsch-lead.mp3 | グレッチのリード、mp3 | |
| summer-c-crunch.mp3 | クランチ、mp3 | |
| 04-last-summer_v9.mp3 | 過去の版（v9） | 比較用 |
| 02-bike-hill_v9.mp3 | 過去の版（v9） | 比較用 |
| prog-a-modernhigh.mp3 | プログレ A | 比較用 |
| prog-b-hardrock-warm.mp3 | プログレ B | 比較用 |

測定項目: 統合ラウドネス I（LUFS）、真のピーク TP、PLR（ピーク対ラウドネス）、LRA、クレストファクター、左右の相関 corr、スペクトル重心、傾き、6つの帯域の相対レベル、各帯域でのサイド−ミッド差（正ならサイドが大きい）。

### 2.2 比較表（ロック分類の Suno 代理統計との対応）

Suno 側は日本一フリーBGM のうちロック／パンク／メタルの分類（n=92）の中央値と、p10〜p90（下位10%〜上位10%）。【参考値】

| 指標 | summer-rock3 | summer-rock2 | Suno 代理（ロック） 中央値 [p10, p90] | 判定 |
|---|---|---|---|---|
| 統合ラウドネス I（LUFS） | -10.2 | -10.3 | -13.3 [-14.6, -12.2] | 中央値より約3 dB、p90 よりも約2 dB 大きい（範囲外） |
| クレスト（dB） | 10.63 | 10.50 | 13.68 [12.31, 15.42] | 範囲外（つぶれている） |
| PLR（dB） | 9.0 | 9.2 | 11.45 [10.5, 13.5] | 範囲外（つぶれている） |
| LRA（LU） | 3.1 | 4.7 | 3.25 [1.5, 5.77] | 範囲内 |
| 左右相関 corr | 0.729 | 0.807 | 0.78 [0.56, 0.91] | 範囲内 |
| スペクトル重心（Hz） | 170 | 265 | 534 [190, 1042] | 下端〜やや下 |
| 傾き（dB/oct） | -4.91 | -5.72 | -4.22 [-6.95, -2.96] | 範囲内 |
| 平坦度（2〜8 kHz） | 0.33 | 0.19 | 0.28 [0.10, 0.41] | 範囲内 |
| サイド−ミッド 低中域 | -0.2 | -3.8 | -5.55 [-10.2, -2.1] | rock3 は範囲外 |
| サイド−ミッド 中域 | +2.2 | -0.8 | -5.25 [-7.9, -2.2] | 範囲外（サイドが大きい） |
| サイド−ミッド プレゼンス | +3.9 | +4.4 | -6.0 [-9.9, -3.1] | 範囲外（サイドが大きい） |
| サイド−ミッド 空気 | +3.4 | +4.4 | -7.45 [-14.8, -2.9] | 範囲外（サイドが大きい） |
| 帯域 中域（dB、相対） | -16.1 | -13.9 | -10.5 [-22.0, -7.2] | 範囲内 |
| 帯域 プレゼンス（dB、相対） | -20.3 | -21.3 | -16.95 [-33.7, -13.4] | 範囲内（やや低い） |
| 帯域 空気（dB、相対） | -25.5 | -27.4 | -20.0 [-30.8, -16.1] | 範囲内（やや低い） |
| 帯域 サブ（dB、相対） | -7.1 | -5.3 | -7.95 [-12.2, -4.0] | 範囲内 |
| 帯域 低域（dB、相対） | -1.6 | -2.6 | -2.9 [-3.8, -2.0] | 範囲内 |

読み取れること【推測を含む】:

- 外れているのは、**ラウドネスとクレスト（つぶしすぎ）** と、**高域のサイド過多** の2点だけ。ほかはおおむね Suno の範囲に入っている。
- 傾きや帯域の形は大きく外れていない。つまり「EQ を足せば Suno に近づく」というやり方では、本質の差を取りこぼす。

### 2.2b 1000曲の中で、自分の曲の値はどれだけ珍しいか【参考値の再集計】

分類を問わず、日本一フリーBGM の1000曲（Suno 製）の測定値を数え直した（`docs/sound/data/nihonichi-bgm-1000-metrics.json`）。

| 条件 | 該当する曲数（1000曲中） | 自分の曲 |
|---|---|---|
| サイド−ミッド（プレゼンス）が 0 dB より大きい（サイドの方が大きい） | 8 曲（0.8%） | summer-rock3 は +3.9、rock2 は +4.4 |
| サイド−ミッド（中域）が 0 dB より大きい | 8 曲（0.8%） | rock3 は +2.2 |
| サイド−ミッドが中域・プレゼンスの両方で 0 dB より大きい | 1 曲 | rock3 は両方を満たす |
| サイド−ミッド（空気）が 0 dB より大きい | 6 曲（0.6%） | +3.4〜+4.4 |
| 統合ラウドネスが -11 LUFS より大きい（うるさい） | 13 曲 | -10.2 |
| 統合ラウドネスが -10.2 LUFS 以上 | 2 曲 | -10.2 |
| クレストが 10.7 dB 以下 | 1 曲 | 10.5〜10.6 |
| 真のピークが 0 dBTP を超える | 68 曲（6.8%） | 3 曲の mp3 が超える |
| 全体の左右相関が 0.5 未満 | 192 曲（19.2%） | rock3 は 0.73（範囲内） |
| 全体の左右相関が 0.1 未満 | 3 曲 | prog-b は 0.067 |

読み取れること:

- **「中高域でサイドがミッドより大きい」は、Suno 1000曲ではほとんどない（1% 未満）。** 自分の曲は、ここで外れている。1000曲の側は、中高域をミッド（中央）に置き、サイドは控えめにするのが普通。
- **「うるさくてつぶれている」も同様に珍しい。** -10.2 LUFS 以上は2曲だけ、クレスト 10.7 dB 以下は1曲だけ。
- 一方で、**真のピークが 0 dBTP を超える曲は 6.8% ある**。Suno 側も完璧ではない。TP の超過は、差の主因ではない。
- 全体の左右相関は、Suno でも幅が広い（0.5 未満が19%）。全体の相関が低いこと自体は珍しくない。外れているのは**帯域別の中高域**と考えられる。

分類ごとの中央値（ジャンルで目標をかえるときの参考）:

| 分類 | 曲数 | I(LUFS) | クレスト(dB) | corr | 重心(Hz) | S−M 中域 | S−M プレゼンス | S−M 空気 |
|---|---|---|---|---|---|---|---|---|
| オーケストラ/シネマ | 306 | -13.0 | 13.52 | 0.62 | 526.5 | -3.7 | -5.75 | -8.45 |
| ロック/パンク/メタル | 92 | -13.3 | 13.68 | 0.78 | 534.5 | -5.25 | -6.0 | -7.45 |
| エレクトロニック/シンセ | 120 | -13.35 | 13.43 | 0.76 | 646.0 | -4.3 | -7.45 | -10.4 |
| チップチューン/8bit | 36 | -13.4 | 13.89 | 0.86 | 726.5 | -6.1 | -7.3 | -11.0 |
| ジャズ/ファンク/ボサノバ | 44 | -13.9 | 14.8 | 0.83 | 384.5 | -6.35 | -6.8 | -7.85 |
| ピアノ独奏 | 44 | -14.3 | 16.35 | 0.42 | 350.5 | -4.2 | -2.15 | -3.55 |
| アンビエント/ドローン | 160 | -13.8 | 14.22 | 0.6 | 222.0 | -3.3 | -3.8 | -5.2 |
| アコースティック/フォーク | 53 | -13.8 | 14.75 | 0.78 | 312.0 | -7.3 | -7.5 | -9.9 |
| 和風 | 74 | -13.1 | 13.99 | 0.68 | 460.5 | -7.1 | -7.2 | -9.8 |
| バラード/子守歌 | 88 | -14.1 | 16.03 | 0.48 | 354.0 | -4.3 | -3.45 | -5.85 |
| ボス/戦闘 | 119 | -12.8 | 13.14 | 0.74 | 641.0 | -4.2 | -7.4 | -9.9 |
| ホラー/ダーク | 79 | -13.1 | 13.3 | 0.57 | 196.0 | -2.9 | -4.3 | -5.4 |
| フィールド/町/ダンジョン | 32 | -13.4 | 14.54 | 0.65 | 465.5 | -4.35 | -4.85 | -6.75 |
| （全体） | 1000 | -13.4 | 14.07 | 0.67 | 437.5 | -4.4 | -6.0 | -8.2 |

どの分類でも、S−M の中央値は中域で -3〜-7 dB、プレゼンスで -2〜-7.5 dB、空気で -3.5〜-11 dB。**どの分類でも、中高域のサイドがミッドを上回る中央値はない。**（ボス/戦闘の統合ラウドネス中央値は -12.8 が最も大きい。ここでも -10 には届かない。）

### 2.3 mp3 版・過去の版との比較

| 曲 | I | TP | PLR | クレスト | corr | 重心(Hz) | S−M 中域 | S−M プレゼンス | S−M 空気 |
|---|---|---|---|---|---|---|---|---|---|
| summer-d-jazzclean.mp3 | -10.7 | +2.0 | 12.7 | 13.8 | 0.744 | 189 | +3.1 | +4.1 | +3.6 |
| summer-e-gretsch-lead.mp3 | -10.7 | +2.3 | 13.0 | 14.33 | 0.747 | 235 | +1.9 | +4.0 | +3.6 |
| summer-c-crunch.mp3 | -10.5 | +1.3 | 11.8 | 15.07 | 0.407 | 1063 | -0.6 | +0.2 | +3.8 |
| 04-last-summer_v9.mp3 | -13.4 | -2.6 | 10.8 | 14.53 | 0.570 | 1061 | -2.6 | -6.0 | -13.2 |
| 02-bike-hill_v9.mp3 | -13.4 | -2.7 | 10.7 | 14.95 | 0.412 | 1527 | -0.8 | -2.6 | -5.3 |
| prog-a-modernhigh.mp3 | -12.7 | -3.2 | 9.5 | 14.64 | 0.527 | 1569 | -3.7 | +0.1 | -0.7 |
| prog-b-hardrock-warm.mp3 | -11.3 | -1.1 | 10.2 | 14.07 | 0.067 | 828 | +1.7 | +0.6 | +0.7 |

【実測】読み取れること:

- v9 の2曲は、ラウドネス -13.4 LUFS、クレスト 14.5〜15.0 dB で、Suno の中央値にほぼ一致する。サイド−ミッドの中高域も負（サイドが小さい）で、Suno 型の形になっている。**v9 より後の世代の作曲ソフトの出力のほうが、Suno から離れている。**
- 後の世代（summer-*）で入った変更（widen の強化、ラウドネス -10 の目標、ギターのアンプ処理など）が、離れた原因の候補。具体的な変更の特定は、`tools/composer/master.mjs` の MASTER_PRESETS（rock は -10 LUFS、widen 2.4）を見る限り、ラウドネス目標と広げ処理が最有力。
- prog-b-hardrock-warm の corr 0.067 は、中高域で左右がほぼ無相関〜逆相の混在を示す。モノラルに畳むと中高域が薄くなる。

### 2.4 拡張測定（帯域ごとの相関など）【実測】

| 曲 | corr 150–500 | corr 500–2k | corr 2k–8k | corr 8k–16k | 傾き(PSD, dB/oct) | 10–16k 対 1–4k (dB) | 16–20k 対 1–4k (dB) | 短時間クレスト中央値 | 50ms RMS の下位5%(dBFS) |
|---|---|---|---|---|---|---|---|---|---|
| summer-rock3.wav | 0.49 | -0.04 | -0.48 | -0.42 | -5.49 | -12.4 | -23.3 | 9.7 | -26.4 |
| summer-rock2.wav | 0.75 | 0.42 | -0.40 | -0.53 | -5.40 | -16.3 | -24.3 | 10.1 | -25.8 |
| summer-d-jazzclean.mp3 | 0.60 | -0.12 | -0.50 | -0.44 | -5.50 | -10.9 | -24.1 | 10.7 | -26.6 |
| summer-e-gretsch-lead.mp3 | 0.60 | -0.01 | -0.43 | -0.44 | -5.40 | -12.2 | -25.4 | 10.6 | -26.2 |
| summer-c-crunch.mp3 | 0.35 | -0.03 | 0.04 | -0.44 | -3.86 | -25.0 | -41.5 | 11.3 | -27.2 |
| 04-last-summer_v9.mp3 | 0.55 | 0.42 | 0.23 | 0.90 | -2.82 | -20.7 | -42.5 | 12.3 | -23.5 |
| 02-bike-hill_v9.mp3 | 0.68 | 0.16 | 0.14 | 0.53 | -2.53 | -19.8 | -44.4 | 12.6 | -25.3 |

読み取れること:

- 新しい4曲（rock2、rock3、jazzclean、gretsch-lead）は、2 kHz 以上で左右の相関が **約 -0.4〜-0.5**。中高域の左右が逆相に近い。モノラル再生（スマホ1本のスピーカー、Bluetooth スピーカー、会場の中央寄り再生）では、この帯域が打ち消し合って**ギターのピッキングやシンバルが消える**【推測：モノ化の影響は、モノに畳んで測れば確認できる】。
- v9 の2曲は同じ帯域で相関が正（0.14〜0.90）。Suno 型の「中高域は中央寄り」になっている。
- 10〜16 kHz の相対レベルは、新しい曲のほうが高い（-11〜-16 dB 対 v9 の -20 dB）。これは、逆相で広げた高域が余計に増えて見えている面もあり、明るくなったのではなく**位相の乱れた高域が増えた**可能性がある【推測】。
- 短時間クレスト中央値は新しい曲で 9.7〜10.7 dB、v9 で 12.3〜12.6 dB。**つぶしすぎ**を別の指標でも確認できた。

### 2.5 公開されている基準値の整理

| 基準 | 値 | 出どころ | 印 |
|---|---|---|---|
| Spotify の再生時の基準ラウドネス | -14 LUFS（ITU-R BS.1770）。大きい曲は下げる。小さい曲は上げるが、損失圧縮のために 1 dB の余裕を残す | https://support.spotify.com/us/artists/article/loudness-normalization/ | 【一次】 |
| Spotify のウェブプレーヤーと一部の外部機器 | ラウドネス調整なし | 同上 | 【一次】 |
| EBU R 128 の目標 | -23 LUFS（放送向け）。LU は1dBに相当。LRA の上限は定めていない | https://en.wikipedia.org/wiki/EBU_R_128 | 【一次】 |
| ハース効果 | 1〜5 ms（クリック）、複雑な音で最大約 40 ms までは1つに融合。5〜30 ms の単独の反射は直接音より最大 10 dB 大きくてもエコーと感じない。1 ms 以上の遅れの反射は音の広がりを増す | https://en.wikipedia.org/wiki/Haas_effect | 【一次】 |
| クレストファクター | ピーク÷RMS。dB で表すと PAPR と等しい。正弦波は 3.01 dB | https://en.wikipedia.org/wiki/Crest_factor | 【一次】 |
| ラウドネス戦争 | 圧縮とリミッターによる音量競争。音のつぶれを起こす | https://en.wikipedia.org/wiki/Loudness_war | 【一次（概要）】 |
| ピンクノイズ | 電力スペクトル密度が 1/f（-3 dB/oct）。音楽の平均スペクトルはおおむねこれに近い | https://en.wikipedia.org/wiki/Pink_noise | 【一次（概要）】 |
| Apple Sound Check の目標 | 約 -16 LUFS | 今回は取り直していない | 【一般知識】 |
| YouTube の基準 | 約 -14 LUFS | 今回は取り直していない | 【一般知識】 |
| 真のピークの上限 | -1 dBTP が一般的（損失圧縮に備える） | Spotify の「1 dB の余裕」から支持【一次】。数値そのものは | 【一般知識】 |

ここから作曲ソフトのマスタリング目標を決めるなら:

- **配信向けの書き出し: 統合 -14 LUFS 前後、TP -1 dBTP 以下、クレスト 12 dB 以上** が Suno 1000曲の分布（I 中央値 -13.4、crest 中央値 14.1）と合う【参考値＋一次】。
- ゲーム内の BGM は配信サービスのラウンドネス調整を通らない。ゲーム内の他の音（効果音、会話）との音量バランスで決める。ここでは -14 〜 -16 LUFS を目安にし、効果音が埋もれないようにする【推測】。

### 2.6 公開されている研究から分かること【一次（要旨のみ）】

| 論文 | 分かること | 今回の使い道 |
|---|---|---|
| SONICS（arXiv 2408.14080、Suno と Udio の曲を見分ける研究） | Suno・Udio のように、伴奏も歌も歌詞も全部が合成された曲は、従来の「歌声だけが偽物」を見分ける方法では見分けにくい。長い時間の流れ（繰り返し、リズム、盛り上がり）の整合が、見分ける手がかりになる | 「長い時間の整合」が人の耳に完成して聞こえる要因である可能性。ここで言う整合は、繰り返しに小さな変化を入れること、盛り上がりの設計など。音色の差だけが原因ではない【推測】 |
| Afchar ら「Detecting music deepfakes is easy but actually hard」（arXiv 2405.04181） | 自動符号化器（オートエンコーダ）で再構成した偽物は 99.8% で見分けられる。しかし生成モデルの違いや、音の加工に弱く、実用には問題が多い | 合成音の「指紋」は、符号化の周波数の痕跡にある可能性。ただし今回の差の説明には直接使えない |
| MusicGen / EnCodec（arXiv） | 生成モデルは、圧縮された離散トークンで音を作る。32 kHz などの標本化周波数と、数本の符号帳で音を再構成する | Suno の内部は非公開。同様の構造だとすれば、**とても高い周波数の細部は元から作られない**。→ Suno の曲の高域が自然に整うのは、そもそも高域の「ざらつき」が少ないからという仮説が立つ【推測】 |
| Bark（Suno の公開モデル、MIT ライセンス） | 音声・音楽を生成する自己回帰型のモデル。公開の事実はこれだけ | Suno 本体は別のモデル。Bark の性質を Suno に当てはめてはいけない【推測の注意】 |

Suno 側の公開情報【一次：https://en.wikipedia.org/wiki/Suno_AI の記述】:
- 2023年4月に Bark を公開、2024年3月に v3（4分までの曲）、2024年11月に v4、2025年5月に v4.5、2025年9月に v5 と Suno Studio（ステムを並べて MIDI や音声で書き出せるワークステーション）、2026年9月に v6 系へ置き換え。
- 2026年の流出で、YouTube Music などから学習データを集めていたことが明らかになったと書かれている（Wikipedia の記述。裏づけは未確認）。
- 日本一フリーBGM の1000曲がどの版で作られたかは不明。版が違えば数値が違うので、**参考値は「Suno 製のある時期の曲」の分布として扱う**。

### 2.7 差の原因の候補（確からしさ順）

| # | 原因の候補 | 根拠 | 印 | 確かめ方 |
|---|---|---|---|---|
| 1 | 中高域のサイドが大きく、左右が逆相に近い（widen の位相ずらし） | 2 kHz 以上の corr が -0.4〜-0.5、S−M が +2〜+4 dB。Suno は -5〜-7 dB | 【実測】【参考値】 | widen を 1.0（なし）にして同じ測定をし、差が消えるか。モノに畳んで聴き比べ |
| 2 | ラウドネスが高すぎ、リミッターでつぶれている | I -10.2、crest 10.6。Suno は I -13.4、crest 14.1 | 【実測】【参考値】 | 目標 -14 LUFS で書き出し、聴き比べ |
| 3 | mp3 の真のピークが 0 dBTP を超える | TP +1.3〜+2.3 | 【実測】 | TP を -1 dBTP 以下に抑えて書き出し |
| 4 | ギターが「素直な録音」ではなく、アンプ処理後の硬い音 | ソリッドボディの直接録音がなかった。ジャズボディ系は中域が丸い | 【実測：音源の不在】 | FSBS direct + アンプを通して聴き比べ（耳での確認が必要） |
| 5 | ドラムの細かい打楽器が合成寄りの小さなサンプル | GeneralUser の打楽器は短く、強弱が少ない | 【推測】 | 差し替えた aux 版と聴き比べ（耳での確認が必要） |
| 6 | 演奏のばらつきが足りない（時間・強さ・音の出だし） | Suno は録音そのものが人間の揺れを含む | 【一般知識】【推測】 | ラウンドロビンの数と human の設定を変えて聴き比べ |
| 7 | 曲全体の流れに小さな変化が少ない（繰り返しが機械的） | SONICS の「長い時間の整合」の手がかり | 【一次（要旨）】【推測】 | 構成の設計の話（作曲担当の領域） |
| 8 | 残響の質（部屋の自然な広がりと合成の残響の違い） | 今回は測っていない | 【未測定】 | 余韻の測定（tail_s は 1.0〜1.95 s）と、インパルス応答の導入検討（9章） |

### 2.8 「完成して聞こえる」ための数値案（ミキサー担当への提案）

これは調査の結論として渡す提案で、実装はこの文書の担当ではない（ミキサーの領域）。

1. **サイド量の上限**: 2 kHz 以上のサイド−ミッドを、ロックで -4 dB 以下（Suno 中央値 -5〜-7 dB）にする。低域（200 Hz 以下）はサイドを切る（モノ化）。参考: Suno ロックの低域 S−M は -11〜-21 dB。
2. **widen の仕方**: 全帯域に同じ広げ処理をかけず、500 Hz 以下はモノ、広げるのは主に 1 kHz 以上のリバーブ成分と、パンで振った楽器の位置で行う。位相をずらす方式（ステレオ化の遅延やコーラス）は、2〜8 kHz の相関を -0.4 まで落とすので避ける。【一般知識】
3. **ラウドネス目標**: 配信向けは -14 LUFS、TP -1 dBTP。ゲーム内用は -16 〜 -14 LUFS。
4. **クレスト**: 短時間クレストの中央値 11 dB 以上、曲全体のクレスト 12 dB 以上を目標に。
5. **モノ互換の検査を自動化**: 書き出しのたびに、(a) 2〜8 kHz の相関、(b) モノに畳んだときのラウドネス低下量（目安 2 dB 以内）、(c) 帯域ごとの S−M を測り、範囲を外れたらやり直す。`tools/audio-check/analyze.py` に追加するのが近道。【提案】
6. **合格の目安（ロック）**: I -14.6〜-12.2、crest ≥ 12.3、PLR ≥ 10.5、corr 0.56〜0.91、S−M 中域 -8〜-2、プレゼンス -10〜-3、空気 -15〜-3（Suno ロックの p10〜p90）。これは Suno に似せるための目安で、良い音の保証ではない。

### 2.9 「完成して聞こえる」要因の整理【一般知識＋推測】

数値で測れないが、聴いたときの「完成感」に関わると言われる要素。ここは一次資料を今回取り直していないので、確かめる材料として使う。

| 要素 | 説明 | 作曲ソフトでの確かめ方 |
|---|---|---|
| 録音そのものの揺れ | 本物の演奏は、弦ごとの鳴り・ピックの当たり・息遣い・部屋の鳴りが毎回違う | ラウンドロビンが2つ以上ある音源を使い、同じ音を連続で弾いて波形が違うか確かめる |
| 倍音の複雑さ | 実機のアンプとスピーカーは、非線形のひずみで倍音がなめらかにつながる | アンプモデル（NAM）の有無で比べる |
| 時間の揺れ | 人は拍の前後に数 ms〜数十 ms 揺れる。楽器によって「前のり」「後ろのり」がある | human の設定を変えて聴き比べ |
| 強さの揺れ | 同じ音型でも強さが毎回違う。特に裏拍が弱くなる | 速度のばらつきの幅を変えて聴き比べ |
| 音の出だしと終わり | 打楽器・弦の出だしの鋭さ、休符直前のミュート、弦のこすれ | 音源に余韻サンプル・ノイズサンプルがあるか |
| 楽器どうしの空間 | 同じ部屋で鳴っている感じ（共通の残響、かぶり） | 楽器ごとではなく、全体にかける共通の短い残響を試す |
| 周波数の住み分け | ギター・ベース・ドラム・鍵盤が同じ帯域で重ならない | ミキサー担当の領域 |
| 時間的な構成 | 8小節ごとの小さな変化、フィルイン、休符の使い方 | 作曲担当の領域 |
| ステレオの設計 | 低域はモノ、パンは楽器ごとに固定、広げすぎない | 2.8 の提案 |
| 最後の接着（バス圧縮、軽い飽和） | 全体を1つの楽器のようにまとめる | 軽い飽和（テープ風）を試す。やりすぎるとクレストが落ちる |

### 2.10 測定の限界（正直に）

- Suno 1000曲の統計は、日本一フリーBGM（ゲーム・映画音楽に偏る）の曲で、**ロック分類は92曲**。BGM 用途のインスト曲の分布であり、歌入りのポップスとは違う。
- 「ロック」の分類は説明タグのキーワードによる。実際にはギターの入っていない曲も混ざる可能性がある【推測】。
- 参考値の「サイド−ミッド」は帯域ごとのレベル差。位相の情報（相関）は全体の corr しかなく、帯域別の相関の参考値はない。このため、**帯域別の逆相（-0.4〜-0.5）が Suno と比べて異常かどうかは、参考値と直接比べられていない**。1000曲の mp3 は著作権の都合でリポジトリに置かず、帯域別の相関は再測定していない。
- 全体の S−M が正である点（サイドがミッドより大きい）だけは、Suno の p90 側にも出ない値（中域 p90 は -2.2、プレゼンス p90 は -3.1）なので、はっきり外れていると言える。

## 3. パートB: 無料で商用利用できる音源の調査

### 3.1 調べた範囲

- **SFZ Instruments**（https://sfzinstruments.github.io/）の全14分類、136件の一覧と、ライセンス欄を読んだ【一次】。ライセンス欄の内訳: Commercial 51（有料）、CC0 35、Custom 10、CC-BY-4.0 7、MIT 6、空欄 6、CC-BY-SA-4.0 3、Public Domain 3、CC-BY-3.0 3、そのほか。
- **FreePats**（https://freepats.zenvoid.org/）の SF2 を直接取得。各 SF2 に付いた README・ライセンス文を読んだ【一次】。
- **VCSL**（Versilian Community Sample Library）のリポジトリ全体を取得し、LICENSE を読んだ【一次】。
- Karoryfer の各リポジトリ（Emily、Growlybass、Fashionbass、Pastabass、Shinyguitar、Black and Blue Basses）と、Wilkinson Audio の Naked Drums をクローンしてファイル一覧を確認した。LICENSE の本文を読めたのは Emily と Growlybass（CC0 1.0）、Greg Sullivan E-Pianos（CC BY 3.0）。それ以外は、SFZ Instruments の一覧の記載【一次】を根拠にした（リポジトリ側の本文は未読）。
- インパルス応答（残響）のライブラリ: Voxengo、EchoThief、MIT の IR Survey、OpenAIR の規約を確かめに行った。結果は 3.4。

### 3.2 採用の条件（`docs/assets-credits.md` と CLAUDE.md 1-1 の例外）

使ってよい: CC0、パブリックドメイン、CC BY（クレジット表記を守る）、CC BY-SA（改変物を同じ条件で出す義務を明記して扱う。今回は使っていない）、独自の無料商用許諾（規約が読めるもの）。
使わない: GPL、NC（非商用）、規約が不明のもの、有料のもの、CC Sampling Plus（広告・宣伝目的の利用を禁じる条項を含むため、ゲームの扱いが不明）、既存の作品から取った音。

### 3.3 追加した音源（変換して `assets-src/soundfont/extra/` に置いたもの）

| 音源 | 作者・入手元 | 規約 | クレジット | 変換後のファイル | 印 |
|---|---|---|---|---|---|
| FSBS Electric Guitar（Fender 基本機種の直接録音）。direct 版 | FreePats（Roberto ほか）。https://freepats.zenvoid.org/ElectricGuitar/clean-electric-guitar.html | CC0 1.0（README とライセンス文を確認） | 不要 | `guitar-fsbs-direct.sf3`（2.12MB） | 【一次】規約、【実測】音程・無音 |
| 同 clean bridge small | 同上（2026-08-07 版） | CC0 1.0（README 確認） | 不要 | `guitar-fsbs-clean-small.sf3`（0.68MB） | 同上 |
| 同 jazz bridge small | 同上（2026-08-07 版） | CC0 1.0（README 確認） | 不要 | `guitar-fsbs-jazz-small.sf3`（0.56MB） | 同上 |
| 同 dist2（歪み版） | 同上 | 同じシリーズ（CC0）。**元の README の写しをこの版については保存していない** | 不要 | `guitar-fsbs-dist2.sf3`（3.55MB） | 【一次】シリーズ規約。この版の本文は未再確認。**禁止音（「みんなで」の曲の歪みギター）に注意** |
| Emilyguitar（Epiphone Emily the Strange、全ノブ最大の直接録音、フラットワウンド 11） | Karoryfer Samples / D. Smolken。https://github.com/sfzinstruments/karoryfer.emilyguitar | CC0 1.0（LICENSE 本文を確認） | 不要 | `guitar-emily.sf3`（5.6MB） | 【一次】【実測】 |
| Growlybass（Squier Jazz Bass） | Karoryfer Samples。https://github.com/sfzinstruments/karoryfer.growlybass | CC0 1.0（LICENSE 本文を確認） | 不要 | `bass-growly.sf3`（3.1MB） | 【一次】【実測】 |
| VCSL（Versilian Community Sample Library）の手持ち打楽器 | Versilian Studios。https://github.com/sgossner/VCSL | CC0 1.0（LICENSE を確認） | 不要（任意で感謝） | `drums-*-aux.sf3` に組み込み | 【一次】 |
| FreePats World Percussion（カホン、ボンゴ、コンガ、マラカス、カスタネットなど） | FreePats（Xavimart、Gonzalo、Roberto の録音）。https://freepats.zenvoid.org/ | CC0（LICENSE.txt を確認）。付属の picture.jpg だけ CC BY 4.0（使っていない） | 不要 | `drums-*-aux.sf3` に組み込み | 【一次】 |
| Wurlitzer EP200 | Greg Sullivan（マッピング: kinwie）。https://github.com/sfzinstruments/GregSullivan.E-Pianos 、作者ページ http://www.sullivang.net/ | **CC BY 3.0（LICENSE を確認）。作者の求めにより表記が必要** | **必要** | `epiano-wurlitzer-ep200.sf3`（0.70MB） | 【一次】【実測】 |
| Yamaha CP80 | 同上 | CC BY 3.0 | **必要** | `epiano-cp80.sf3`（2.55MB） | 同上 |
| Hohner Pianet T | 同上 | CC BY 3.0 | **必要** | `epiano-pianet-t.sf3`（1.10MB） | 同上 |
| Upright piano KW（Kawai アップライト、居間で録音）と bright 版 | FreePats（Gonzalo、Roberto）。http://freepats.zenvoid.org/Piano/acoustic-grand-piano.html#UprightKW | CC0（cc0.txt を確認） | 不要 | `piano-upright-kw.sf3`（0.74MB）、`piano-upright-kw-bright.sf3`（0.83MB） | 【一次】【実測】 |
| Drawbar organ emulation（setBfree の録音） | FreePats（Roberto）。http://freepats.zenvoid.org/Organ/ | CC0（README に明記） | 不要 | `organ-drawbar.sf3`（0.39MB） | 【一次】【実測】 |
| Percussive organ emulation | FreePats（Strix SoundFont Team 提供） | CC0 | 不要 | `organ-percussive.sf3`（0.74MB） | 同上 |
| Rock organ emulation | 同上 | CC0 | 不要 | `organ-rock.sf3`（1.24MB） | 同上 |
| Church organ emulation（Aeolus の録音） | FreePats（Roberto）。http://freepats.zenvoid.org/Organ/pipe-organ.html | CC0 | 不要 | `organ-church.sf3`（0.95MB） | 同上 |
| Spanish classical guitar（ナイロン弦） | FreePats（Roberto）。http://freepats.zenvoid.org/Guitar/acoustic-guitar.html | CC0（cc0.txt を確認） | 不要 | `guitar-nylon-spanish.sf3`（1.33MB） | 同上 |
| New age pad（GM 89 向け） | FreePats（Roberto。ZynAddSubFX / Yoshimi で作成） | CC0 | 不要 | `synth-pad-newage.sf3`（0.85MB） | 【一次】【実測：無音でないことのみ】 |
| Sweep pad（GM 96 向け） | 同上 | CC0 | 不要 | `synth-pad-sweep.sf3`（0.56MB） | 同上 |
| Synth pad bowed（GM 93 向け） | FreePats（Strix SoundFont Team） | CC0 | 不要 | `synth-pad-bowed.sf3`（1.70MB） | 同上 |
| Synth pad choir（GM 92 向け） | FreePats | CC0 | 不要 | `synth-pad-choir.sf3`（1.03MB） | 同上 |

追加した SF3 の合計は約 50MB。すべて作曲ソフト専用で、ゲーム本体（`dist/`、128 メガビット = 16MB の予算）には入れていない。

ライセンス文と README の写しは `assets-src/soundfont/extra/src/licenses/`（32 ファイル、約 130KB）に保存した。

#### 補足: GPL ソフトウェアで作った録音について【推測を含む】

オルガン（setBfree、Aeolus）とパッド（ZynAddSubFX、Yoshimi）は、GPL のソフトウェアで鳴らした音を録音したもの。FreePats はこれらの録音を CC0 として公開しており、**音そのもの（出力）にはソフトの GPL は及ばない**というのが一般的な理解【一般知識】。ただし、法律の最終判断は人間（旭さん）に委ねる。心配なら、オルガン4種とパッド4種だけ外しても本体の品質に影響は小さい。

### 3.4 追加しなかった音源（理由つき）

#### 規約を読んで外したもの

| 音源 | 規約 | 外した理由 |
|---|---|---|
| Voxengo の無料インパルス応答 | 「どんな目的にも無償で使ってよい。商用も可。ただし売ったり、配布で直接・間接の利益を得てはならない」と書かれている（https://www.voxengo.com/impulses/ 、2026-10-14 確認）【一次】 | ゲームに組み込んで売る可能性がある。「配布で間接的に利益を得る」に当たる恐れが排除できない。人間の判断が要る |
| EchoThief（Chris Warren） | 今回読めたページには規約の記載がなかった（https://www.echothief.com/ 、2026-10-14）【一次：記載なし】 | 規約が読めないものは使わない |
| MIT IR Survey（271 の残響） | ページに規約の記載がなかった（https://mcdermottlab.mit.edu/Reverb/IR_Survey.html 、2026-10-14）【一次：記載なし】 | 同上 |
| OpenAIR | ページが空の応答で読めなかった | 同上。OpenAIR は CC BY と CC BY-NC が混在すると記憶しているが、未確認【一般知識】 |
| Rickenbacker 4001（Project 16） | CC BY-NC-SA 3.0（SFZ 一覧）【一次】 | 非商用 |
| jRhodes3c / jRhodes3d（Rhodes） | CC BY-NC-SA 4.0 / CC BY-NC 4.0 【一次】 | 非商用。Rhodes は欲しい音だが使えない |
| Kay 5-String Banjo | GPL-3.0-or-later 【一次】 | GPL |
| MF Tin Whistle | CC BY-NC-SA 3.0（改変あり）【一次】 | 非商用 |
| Sonatina Symphonic Orchestra / G-Town Church | CC Sampling Plus 1.0 【一次】 | 広告・宣伝目的の利用を禁じる条項があり、ゲームでの扱いが不明。すでに VSCO 2 CE（CC0）がある |
| Baconwulf / Beefowulf（Karoryfer）ほか Commercial 欄の51件 | 有料 【一次】 | 有料素材は人間の承認が必要（CLAUDE.md 1-2） |
| Unreal Instruments の各種（Standard Guitar、Metal GTX、The Slapper、Koto、1912 など） | Custom 【一次】 | 独自規約の本文を今回は読めていない。読めない規約は使わない |
| Salamander Drumkit | CC BY-SA 3.0 【一次】（既存記録あり） | 改変したサンプルを同じ条件で出す義務が生じる。すでに見送りと記録済み |
| Sam's Sonor / LivingRoom Upright Micro / BJDNielPercussions | CC BY-SA 4.0 【一次】 | ShareAlike の扱いがむずかしい。別の CC0 の代替がある |
| Standard Bass / Estate Grand LE / Piano in 162 / Church Steinway / Maestro Concert Grand など | Custom または空欄 【一次】 | 規約の本文を読めていない |
| Meatbass | 一覧では CC0-1.0。ただし既存の記録（2026-10-07）は GPL 3 と書いている | **記録のくいちがい**。要確認。使っていない。人間か次の担当が、リポジトリの LICENSE を直接読んで確かめる |

#### 規約は使える（CC0 / CC BY）が、今回は変換しなかったもの（候補）

| 音源 | 規約 | 容量 | 使えそうな場面 | 見送り理由 |
|---|---|---|---|---|
| Naked Drums（Wilkinson Audio） | CC-BY-4.0 【一次（一覧）】 | 1.3GB | 10 ラウンドロビン・最大5段の強さ・複数マイク。生ドラムの質感の本命 | 容量が大きく、マイクの混ぜ方の作り込みが要る。ディスクの余裕も限られていた（約 3.7GB）。次の担当向けの最有力候補 |
| DRS Kit（DrumGizmo） | CC-BY-4.0 【一次（一覧）】 | 754MB | Muldjord とは別の部屋鳴りの生ドラム | Muldjord と同じ DrumGizmo 系で、追加の差が小さいと判断 |
| SM Drums | Public Domain 【一次（一覧）】 | 2.2GB以上 | 大きな生ドラム | 容量 |
| Swirly Drums / Unruly Drums / Frankensnare / Gogodze Phu Vol I・II | CC0 【一次（一覧）】 | 0.1〜2GB | ブラシ、スネア単体、ガーナのドラム | 用途が限られる |
| Fashionbass / Pastabass / Black and Blue Basses / Swagbass / Ergo EUB | CC0 【一次（一覧）】 | 0.1〜1GB | ベースの音色違い（ジャズベース系、ベース VI、5弦など） | Growlybass と FreePats ベースで当面足りる |
| Shinyguitar（黒いアーチトップ。アコースティックとエレキのプログラム） | CC0 【一次（一覧）】 | 352MB | ジャズ寄りのクリーンギター | 追加の差が小さい |
| Headroom Piano（Yamaha C3） | CC BY 4.0 【一次（一覧）】 | 156MB | Salamander の代わりの明るいグランド | クレジットが増える。Salamander で足りる |
| Accurate-Salamander | CC BY 【一次（一覧）】 | 1.6GB | Salamander の音程改善版 | 容量 |
| VCSL Keys | CC0 【一次（一覧）】 | 680MB | ピアノ、チェンバロ | 容量 |
| MTG Solo Sax / Bear Sax / Weresax | CC BY 4.0 / CC0 / CC0 【一次（一覧）】 | 110MB 前後 | サックス（バンドのソロ） | 時間。次の担当向け |
| War Tuba | CC0 【一次（一覧）】 | 104MB | チューバ | 優先度が低い |
| Minifreak Pads / Wavestate Pads（SHLD Music） | CC0 【一次（一覧）】 | 265MB / 160MB | 本物のシンセ由来のパッド | 容量。FreePats のパッド4種で当面足りる |
| ganjo / Etherealwinds Harp / Dim Cabasa / Ixox Flute / MSLP Vibes / Terkelsen's Marimba | CC0 / CC0 / CC BY 4.0 / CC BY 4.0 / CC BY 3.0 / 空欄 【一次（一覧）】 | 10〜200MB | 小物の楽器 | 優先度が低い。Terkelsen's Marimba は規約欄が空なので使わない |

### 3.5 容量の予算

- 追加した SF3 は約 50MB。すべて `assets-src/` に置き、`dist/` に入れていない（作曲ソフト専用）。
- ゲームの予算（128 メガビット = 16MB）は、この作業で変わらない。
- ディスクの空き: 作業開始時は約 6GB、終了時は約 5.1GB（作業用の一時ファイルを削除したあと。7 章）。

## 4. パートC: 変換と検証

### 4.1 作ったツール（`tools/soundfont/`、既存のコードは変更していない）

| ツール | 役割 | 使い方 |
|---|---|---|
| `build-fsbs.mjs` | FreePats FSBS の SF2 を、作曲ソフト用の小さな SF3 にする。先頭 N 秒だけ切り、最後に 0.8 秒のフェード、ラウンドロビンを絞る、Vorbis 圧縮。強さ1〜127を1つずつ割り当て、弱い層は 92 まで、強い層は 93 以上 | `node tools/soundfont/build-fsbs.mjs <sf2> <id> [--program 27] [--seconds 6] [--q 4] [--rr 2]` |
| `sfz-to-sf3.mjs` | 汎用の SFZ → SF3 変換。control / global / master / group / region の継承、#define、#include、default_path、ラウンドロビン、ループを扱う。SFZ の既定の音程は 60、リージョンの volume はゲインに反映、`--shift` で半音ずらし | `node tools/soundfont/sfz-to-sf3.mjs <SFZ> <name> [--program] [--seconds] [--q] [--rr] [--stereo] [--only RE] [--exclude RE] [--gain dB] [--loop] [--fade] [--release] [--shift N] [--outdir]` |
| `build-aux-percussion.mjs` | 既存のドラム SF3 に、VCSL と World Percussion の録音の小物打楽器を足す。置き換える鍵の単発ゾーンを全楽器から削除し、「AuxPerc」の楽器と全域の準備ゾーンを4つのドラムプリセット（0 / 8 / 16 / 32）に追加。元の GeneralUser の音量にそろえる | `node tools/soundfont/build-aux-percussion.mjs <drums.sf3> <out.sf3> --vcsl <dir> --wp <WorldPercussion.sf2>` |
| `sf2-to-sf3.mjs` | FreePats の小さな SF2 を、ほぼそのまま SF3 にする。`--program` で GM の番号を付けかえ、`--no-effects` で元のコーラス・リバーブの送りを 0 に | `node tools/soundfont/sf2-to-sf3.mjs <in.sf2> <out.sf3> [--program N] [--name] [--q 4] [--mono] [--no-effects]` |

作りかたは既存の `build-guitar.mjs`（Karoryfer のギター）と `lib.mjs` に倣った。

### 4.2 置き換えるプログラムの番号（作曲ソフトの overlay への登録案）

| ファイル | 置き換える GM の番号（0 始まり） | 備考 |
|---|---|---|
| guitar-fsbs-direct | 27（クリーンギター） | **アンプ（NAM）に通す前提**。単体で聴かない |
| guitar-fsbs-clean-small | 27 | 元の作者がアンプとエフェクトを通した「クリーン」 |
| guitar-fsbs-jazz-small | 26（ジャズギター） | 同「ジャズ」 |
| guitar-fsbs-dist2 | 30（ディストーション） | 禁止音に注意（「みんなで」の曲の歪みギターは使わない） |
| guitar-emily | 27 | 直接録音。ハムバッカー系で太い |
| guitar-nylon-spanish | 24（ナイロンギター） | |
| bass-growly | 33（フィンガーベース） | Jazz Bass の指弾き |
| organ-drawbar | 16 | |
| organ-percussive | 17 | |
| organ-rock | 18 | |
| organ-church | 19 | |
| piano-upright-kw / bright | 0 | 上書きすると既存のグランドと入れかわる。アップライトとして別枠で選べる登録が望ましい |
| epiano-cp80 | 2 | |
| epiano-wurlitzer-ep200 / epiano-pianet-t | 4 | 同じ番号 4 を使う。登録時はどちらか一方を選べるようにする |
| synth-pad-newage | 88 | |
| synth-pad-choir | 91 | |
| synth-pad-bowed | 92 | |
| synth-pad-sweep | 95 | |
| drums-{rock,muldjord,jpop,metal,jazz,supra}-aux | ドラムの 0 / 8 / 16 / 32 | 既存の同名のドラム SF3 の差し替え版。小物打楽器だけが録音に変わる |

組み込みの注意: SoundBankManager の priorityOrder で overlay を使うとき、プリセットは**最初に持っているバンクから取られ、鍵ごとの代替はない**。FSBS のギターは鍵 28〜96 しか持たない。範囲外の鍵はそのプリセットでは鳴らないので、範囲の外は別の音源に流れない点に注意する【実測】。

### 4.3 検証の結果【実測】

方法: 各 SF3 を spessasynth_core のオフライン描画（SpessaSynthProcessor、44.1 kHz）で鳴らし、(1) 全体の無音ではないか、(2) 音程が合っているか（倍音の櫛型検査 `combcheck.mjs`、ゴーツェル法）、(3) 音量のピークを測った。25 秒の試験フレーズ（音階と和音）を使用。

| ファイル | ピーク(dBFS) | RMS(dBFS) | 無音の半秒 | 音程の検査 |
|---|---|---|---|---|
| guitar-fsbs-direct | -8.5 | -28.6 | 4/50 | 合格 |
| guitar-fsbs-clean-small | -10.8 | -29.6 | 4/50 | 合格 |
| guitar-fsbs-jazz-small | -9.6 | -29.0 | 4/50 | 合格 |
| guitar-fsbs-dist2 | -8.9 | -26.6 | 4/50 | 合格 |
| guitar-emily | -21.2 | -45.3 | 17/50 | 合格（鍵59の無音を修正後） |
| guitar-nylon-spanish | -10.8 | -33.6 | 3/50 | 合格 |
| bass-growly | -15.7 | -38.9 | 4/50 | 合格（-12 オクターブのずれを修正後、0 セント） |
| organ-drawbar | -10.2 | -26.5 | 3/50 | 合格 |
| organ-percussive | -8.7 | -24.1 | 3/50 | 合格 |
| organ-rock | -8.8 | -25.4 | 3/50 | 合格 |
| organ-church | -9.0 | -25.0 | 1/50 | 合格 |
| piano-upright-kw | -9.3 | -32.3 | 4/50 | 合格 |
| piano-upright-kw-bright | -9.6 | -32.7 | 4/50 | 合格 |
| epiano-wurlitzer-ep200 | -13.6 | -34.1 | 5/50 | 合格 |
| epiano-cp80 | -14.6 | -32.9 | 4/50 | 合格 |
| epiano-pianet-t | -11.7 | -29.8 | 4/50 | 合格 |
| synth-pad-newage | -10.1 | -28.2 | 2/50 | 無音でないことのみ確認 |
| synth-pad-sweep | -10.8 | -26.5 | 3/50 | 同上 |
| synth-pad-bowed | -10.0 | -27.1 | 2/50 | 同上 |
| synth-pad-choir | -5.4 | -23.3 | 2/50 | 同上（ほかより 5 dB ほど大きい） |
| （参考）guitar-hofner 既存 | -16.3 | -42.0 | 4/50 | － |
| （参考）bass-jazz 既存 | -27.4 | -49.4 | 10/50 | － |
| （参考）guitar-pluck-clear 既存 | -13.9 | -34.3 | 4/50 | － |

読み取れること:

- **音量が音源ごとに大きくちがう。** FSBS のギターは RMS -27〜-30 dBFS、既存の Hofner は -42、Emily は -45。差は 12〜19 dB。バス・ドラムなどとのバランスは、統合のときに音源ごとのゲインを決めて合わせる必要がある（ミキサー担当の仕事）。
- Growlybass は既存の Jazz ベースより約 11 dB 大きい。
- Emily の「無音の半秒 17/50」は、鍵によって減衰が速い（短く切れる）か、ピーク前後の無音が長いため。実際に使うとき、音の長さを確かめる。
- ドラム aux 版は、元のキットと全体のピーク・RMS が変わらない（元の GeneralUser の音量にそろえているため）。

### 4.4 耳で確認していないこと【耳未確認】

すべての音源は、数値の検査（無音でない・音程・ピーク）だけで、**人の耳で聴いて確かめていない**。特に次を、聴いて確かめてもらう必要がある。

1. FSBS direct が、アンプ（NAM）を通して「生ギターらしい」か。直接録音はそのままではかすかで金属的に聞こえる（元の作者も「単体で使う想定ではない」と書いている）。
2. FSBS clean/jazz の「元の作者がアンプとエフェクトを通した音」が好ましいか。
3. ラウンドロビンが連続で鳴ったとき、不自然な音程のゆれや段差がないか（強さ1〜127を1つずつに割り当てたため、段差の出方は聴かないと分からない）。
4. Emily の減衰が音楽的に使える長さか（鍵ごとに 6 秒で切っている）。
5. Growlybass の音程が、全鍵域で自然か（数値は合格。ただし 21〜96 のうち高域の音色変化は聴いていない）。
6. ドラム aux 版の小物（シェイカー、タンバリン、ボンゴ、コンガなど）が、元の GeneralUser より自然か。音量の釣り合い、鍵の割り当て（GM の標準と一致するか）。
7. オルガンのループが途切れないか（ループの継ぎ目のクリック）。
8. パッド4種の継ぎ目と、長い伸ばしでのうねり。
9. Wurlitzer / CP80 / Pianet の音域の端（低い鍵、高い鍵）の音色の飛び。
10. アップライトピアノの部屋鳴りの量（居間で録音されたため、残響が元から入っている。作曲ソフトの残響と二重にならないか）。

### 4.5 作業中に見つけた問題と直し方（再現しないための記録）

| 問題 | 原因 | 直し方 |
|---|---|---|
| Emily の鍵59が無音 | SFZ に pitch_keycenter がない領域があった。SFZ の既定は 60 | `sfz-to-sf3.mjs` で SFZ の既定の音程を 60 にした。再検査で解消 |
| Growlybass が1オクターブ低く鳴った | Karoryfer のベースは実音の1オクターブ上に書かれている | `--shift -12` を追加。櫛型検査で 0 セント |
| aux 打楽器の名前が文字化け | サンプル名に日本語を使った | ASCII の名前にした |
| aux の鍵に元の音が残った | 差し替える鍵の単発ゾーンを、ドラムの他の楽器にも持っていた | 全楽器からその鍵のゾーンを消し、AuxPerc の楽器を追加 |
| ピッチ検査が誤検出する | 自己相関法は基音の弱い低音や高音で外れる | 櫛型検査（ゴーツェル法）に切り替え |
| 圧縮済みサンプルの再読み込みで「デコーダ未準備」 | SF3 のデコーダの準備待ち | ffmpeg で compressedData をデコードして検査 |
| git の blobless クローンで `git ls-tree -l` が全データを取得 | -l はサイズのために blob を取りに行く | `--name-only` を使う |

## 5. 統合メモ（作曲ソフト側を触る人へ）

この担当は `src/audio/` と `tools/composer/` を触っていない。統合は別の担当が行う前提で、必要な情報だけ渡す。

### 5.1 音量合わせの目安

目標 RMS を -34 dBFS（25 秒の試験フレーズでの RMS）に置いたときの、必要なゲイン。**LUFS ではなく簡易な RMS なので、あくまで出発点**。

| ファイル | 試験の RMS(dBFS) | 目安のゲイン(dB) |
|---|---|---|
| guitar-fsbs-direct | -28.6 | -5.4 |
| guitar-fsbs-clean-small | -29.6 | -4.4 |
| guitar-fsbs-jazz-small | -29.0 | -5.0 |
| guitar-fsbs-dist2 | -26.6 | -7.4 |
| guitar-emily | -45.3 | +11.3 |
| guitar-nylon-spanish | -33.6 | -0.4 |
| bass-growly | -38.9 | +4.9 |
| organ-drawbar | -26.5 | -7.5 |
| organ-percussive | -24.1 | -9.9 |
| organ-rock | -25.4 | -8.6 |
| organ-church | -25.0 | -9.0 |
| piano-upright-kw | -32.3 | -1.7 |
| piano-upright-kw-bright | -32.7 | -1.3 |
| epiano-wurlitzer-ep200 | -34.1 | +0.1 |
| epiano-cp80 | -32.9 | -1.1 |
| epiano-pianet-t | -29.8 | -4.2 |
| synth-pad-newage | -28.2 | -5.8 |
| synth-pad-sweep | -26.5 | -7.5 |
| synth-pad-bowed | -27.1 | -6.9 |
| synth-pad-choir | -23.3 | -10.7 |

実際の曲の中では、ほかの楽器とのバランスと、ミキサー担当の自動調整（`src/audio/auto-mix*.ts`、別の担当が編集中）が最終的な音量を決める。この表は、**音源を差しかえたとき、急に何 dB も大きく（小さく）ならないための補正の目安**。

### 5.2 登録のしかた（提案）

- 既存の登録先は、`ai-song.ts` の ORCHESTRA_PATCHES などと、overlay のスロット（bass、drums、guitar、orchestra、piano、synth）。新しい SF3 は、1 つの SF3 に 1 つのプリセット（ドラムは4つ）なので、**ギター・ベース・ピアノ・シンセのスロットに、選べる音源として並べる**のが最小の変更。
- 鍵盤とオルガンは、いまのスロットに「オルガン」「エレピ」の枠が独立していない可能性がある。番号 16〜19（オルガン）、2・4（エレピ）を使う前に、既存の曲がそれらの番号を使っていないか確かめる。**使っている曲の音が急に変わらないよう、「選んだときだけ有効」にする**。
- 複数の overlay を同時に重ねる場合は、SoundBankManager の priorityOrder で順番を決める。同じ番号を持つバンクは、先に並べたものが勝つ（鍵ごとの代替はない）。
- FSBS の direct は、アンプ（NAM）に通すのが前提。アンプ未接続の曲で選べないように、プリセットの説明に書く。

### 5.3 禁止音との関係（`docs/sound/banned-sounds.md`）

- スラップ曲の伴奏ギター、「みんなで」の曲の歪みギターは使わない。`guitar-fsbs-dist2.sf3` は歪み版なので、この2曲では選ばない。
- クリーンギターにコーラスをかけない。クランチのアンプをリードギターに使わない。FSBS direct は、**コーラスなし・クランチなしの設定で試す**。
- ミックスのバランスはミキサー担当の領域。この文書の音量の目安はその前段の補正にとどまる。

## 6. 聴き比べで確かめてほしい実験（耳での確認が必要）

数値は「悪い兆候」を示すだけで、直したら良くなったかは**聴かないと分からない**。次の順に1つずつ試し、効果がなければ戻す。

| # | 実験 | 変えるもの | 測るもの | 期待 | 失敗したときの見方 |
|---|---|---|---|---|---|
| 1 | widen をなしにして書き出し | `master.mjs` の rock の widen 2.4 → 1.0 | 2k〜8k の corr、S−M、モノ化したときの音量低下 | corr が正に、S−M が負に近づく | corr が変わらなければ、位相ずれは widen 以外（コーラス、ステレオ化したサンプル）にある |
| 2 | 低域をモノ化（200 Hz 以下のサイドを切る） | サイドのハイパス | S−M の低中域 | Suno に近づく（-5 dB 以下） | 低域の広がりが失われて物足りなくなれば、150 Hz 以下に |
| 3 | 目標ラウドネスを -14 LUFS に | master の目標値 | I、TP、クレスト、PLR | クレスト 12 dB 以上に | リミッターの設定が原因なら、リミッターの先読みと戻りを調整 |
| 4 | TP の上限を -1 dBTP に | master の真のピーク | mp3 化後の TP | 0 を超えない | mp3 のエンコーダで再び超えるなら、-1.5 まで下げる |
| 5 | FSBS direct → アンプ → 既存のギターと並べて聴く | ギター音源 | 耳 | 「生っぽさ」が増す | 金属的に聞こえるなら、アンプの前に軽い低域カット（80 Hz 以下）と、高域のなだらかな減衰 |
| 6 | ドラム aux 版と元のドラムを並べて聴く | ドラム音源 | 耳 | 小物がずっと自然に | 割り当てがずれていれば、`build-aux-percussion.mjs` の MAP を直す |
| 7 | 同じ音型を human なし／強めで書き出して聴き比べ | human の幅 | 耳、onsets_per_sec | 機械的な感じが減る | 揺れすぎでぎこちなくなれば幅を狭める |
| 8 | 共通の短い残響を全体にかける | 全体の残響 | 耳、tail_s | 「同じ部屋で鳴っている」感じ | 濁るなら、200 Hz 以下の送りを切る |

聴き比べの原則: **同じ音量にそろえて**から聴く（大きいほうが良く聞こえるため）。1 回に1つだけ変える。

## 7. 作業の後始末と現在の状態

- 作業用の一時ファイル（クローンしたリポジトリ、VCSL の展開、FreePats の SF2、試聴用の WAV、`/tmp/py7`）を削除した。ディスクの空きは約 3.7GB → 約 5.1GB。
- 検査ツールのスクリプトは、`/tmp/claude-0/keep-suno/tools/`（inspect、names、presets、pitchcheck、combcheck、audition）に残した。リポジトリには入れていない。必要なら `tools/audio-check/` に移す。
- **git のコミットはしていない**（依頼どおり）。追加されたもの: `assets-src/soundfont/extra/*.sf3`（30 ファイル）、`assets-src/soundfont/extra/src/licenses/`、`tools/soundfont/{build-fsbs,build-aux-percussion,sfz-to-sf3,sf2-to-sf3}.mjs`、この文書、`docs/assets-credits.md` の追記。
- `src/audio/` と `tools/composer/` は触っていない（別の担当が編集中）。

## 8. 人間（旭さん）にお願いしたいこと

| # | お願い | 理由 | 急ぎ度 |
|---|---|---|---|
| 1 | 追加した音源を、耳で聴いて良し悪しを教えてほしい。まず FSBS direct（アンプ経由）、ドラム aux 版、Growlybass、Wurlitzer の4つ | 数値の検査だけで、耳での確認がゼロ。ここが一番大きな不確実性 | 高 |
| 2 | Greg Sullivan のエレピ3種を**ゲームに入れる場合は**、クレジット表記を決める（CC BY 3.0）。表記の案: 「Electric piano samples by Greg Sullivan (CC BY 3.0), http://www.sullivang.net/」 | 表記が義務。作曲ソフト専用で使う間は不要 | 中 |
| 3 | オルガン・パッド（GPL ソフトで鳴らした録音を CC0 で公開したもの）を、ゲームに入れてよいか判断してほしい | 通常は問題ないとされるが、法的な最終判断は人間 | 低 |
| 4 | Voxengo、EchoThief、MIT IR Survey の残響データを使ってよいか、規約の確認（作者への問い合わせ）をしてほしい | 規約が不明・曖昧。使えれば残響の質が上がる | 低 |
| 5 | Meatbass の規約（既存記録は GPL 3、SFZ 一覧は CC0-1.0）が食いちがう。リポジトリの LICENSE を直接見て確かめてほしい | 記録のくいちがい。使うかどうかの前に解消したい | 低 |
| 6 | Naked Drums（CC BY 4.0、1.3GB）を取り込む作業を、ディスクの余裕が出てから次の担当に任せてよいか | 生ドラムの質を一段上げる最有力候補だが、容量が大きい | 中 |
| 7 | 日本一フリーBGM のほかに、Suno 以外の「完成して聞こえる」基準になる曲の測定（自作でない、権利が確かな曲。例: 自分で録音した曲、権利を持つ曲）があれば教えてほしい | 比較対象が Suno の1000曲だけで偏っている | 低 |
| 8 | WebSearch の回数の上限が回復したら、一次資料の追加調査（ミキシングの定説の数値の再確認、ラウドネスの各サービスの基準）を再開させてほしい | 今回は curl で直接取りに行ける範囲に限った。2.5 の【一般知識】の数値は再確認の余地がある | 中 |

## 9. 次の担当への提案（優先順）

1. 6 章の実験 1〜4（widen・低域モノ化・ラウドネス・TP）。音源の追加より先に効く可能性が高い【推測】。コストが低く、聴けばすぐ分かる。
2. `tools/audio-check/analyze.py` に、帯域別の相関（150–500、500–2k、2k–8k、8k–16k）、モノ化したときのラウドネス低下量、短時間クレスト中央値を追加し、書き出しごとに自動で記録する。今回の `ext.py` の計算がそのまま使える（Welch 法で 1/3 オクターブの電力、サイド−ミッドの相関）。
3. FSBS direct をアンプ（NAM）に通して聴き比べる（実験 5）。
4. ドラム aux の割り当ての聴き取り確認（実験 6）。
5. Naked Drums の取り込み（`build-drums.mjs` に倣う。マイクは近接＋オーバーヘッド＋部屋の3つ程度に絞る）。
6. 残響のインパルス応答の導入（規約が確かなものが見つかってから）。いまの残響の質は未測定。
7. サックスなど、バンドのソロ楽器の追加（MTG Solo Sax、CC BY 4.0。110MB）。

## 10. この調査の限界（正直な記録）

- **耳で確認していない。** 4.4 のとおり。
- WebSearch の回数が尽き、WebFetch は出どころの制限で使えなかった。そのため、一次資料は curl で直接取りに行った。取れたのは、Spotify、EBU R 128（Wikipedia 経由）、arXiv の要旨とHTML、Wikipedia（ピンクノイズ、ハース効果、クレストファクター、ラウドネス戦争、Suno AI など）、Voxengo、EchoThief、MIT。
- 取れなかった・読めなかった: OpenAIR の規約、Apple Sound Check の公式の基準、EBU の原本 PDF、AES の推奨値、Pestana の本などのミックスの定説の一次資料。2.5 の【一般知識】の行は、これらを根拠にしていない。
- **SONICS と Afchar の論文は、要旨と一部の本文だけ**。周波数の痕跡についての具体的な数値は取り出せなかった。「生成音は高域が自然に整う」は推測。
- Suno 1000曲の統計は、日本一フリーBGM の曲の測定値で、Suno 全体の代表ではない。曲が作られた版も不明。
- 1000曲の統計には、帯域別の左右相関がない。**帯域別の逆相が Suno と比べて異常かどうかは、直接は比べられていない**（2.10）。ただし全体の S−M が p90 の外にあることは確かめた。
- この作業で使った元の SF2・SFZ・リポジトリは、後始末で削除したため、再変換には再ダウンロードが必要。規約本文の写しは `src/licenses/` に保存した。FSBS dist2 だけは、元の README の写しを保存できていない。
- 外部サイトの記述（Wikipedia の Suno AI の項など）は、そのまま裏づけたわけではない。

## 付録A: 出どころ一覧（URL と確認日 2026-10-14）

| 項目 | URL |
|---|---|
| Spotify ラウドネス正規化 | https://support.spotify.com/us/artists/article/loudness-normalization/ |
| EBU R 128（概要） | https://en.wikipedia.org/wiki/EBU_R_128 |
| ハース効果 | https://en.wikipedia.org/wiki/Haas_effect |
| クレストファクター | https://en.wikipedia.org/wiki/Crest_factor |
| ラウドネス戦争 | https://en.wikipedia.org/wiki/Loudness_war |
| ピンクノイズ | https://en.wikipedia.org/wiki/Pink_noise |
| ダイナミックレンジ圧縮 | https://en.wikipedia.org/wiki/Dynamic_range_compression |
| マスタリング | https://en.wikipedia.org/wiki/Mastering_(audio) |
| Suno AI | https://en.wikipedia.org/wiki/Suno_AI |
| Bark（Suno の公開モデル、MIT） | https://github.com/suno-ai/bark |
| SONICS（Suno / Udio の検出） | https://arxiv.org/abs/2408.14080 （HTML: https://arxiv.org/html/2408.14080） |
| Afchar ら（音楽ディープフェイクの検出） | https://arxiv.org/abs/2405.04181 |
| SFZ Instruments の一覧 | https://sfzinstruments.github.io/ |
| FreePats | https://freepats.zenvoid.org/ |
| FSBS Electric Guitar（FreePats） | https://freepats.zenvoid.org/ElectricGuitar/clean-electric-guitar.html |
| Karoryfer Emilyguitar | https://github.com/sfzinstruments/karoryfer.emilyguitar |
| Karoryfer Growlybass | https://github.com/sfzinstruments/karoryfer.growlybass |
| Greg Sullivan E-Pianos | https://github.com/sfzinstruments/GregSullivan.E-Pianos |
| Greg Sullivan（作者のページ） | http://www.sullivang.net/ |
| VCSL | https://github.com/sgossner/VCSL |
| Voxengo の無料 IR | https://www.voxengo.com/impulses/ |
| EchoThief | https://www.echothief.com/ |
| MIT IR Survey | https://mcdermottlab.mit.edu/Reverb/IR_Survey.html |
| 日本一フリーBGM（既存の参考値の出どころ） | https://nihonichi-bgm.com/ |

## 付録B: 再現のしかた

```
# 変換（assets-src/soundfont/extra/ に出る）
node tools/soundfont/build-fsbs.mjs <FSBS の SF2> direct --program 27
node tools/soundfont/sfz-to-sf3.mjs <emily_basic.sfz> guitar-emily --program 27
node tools/soundfont/sfz-to-sf3.mjs <growlybass_clean.sfz> bass-growly --program 33 --shift -12
node tools/soundfont/sf2-to-sf3.mjs <FreePats の SF2> <出力.sf3> --program 16 --no-effects
node tools/soundfont/build-aux-percussion.mjs assets-src/soundfont/extra/drums-rock.sf3 assets-src/soundfont/extra/drums-rock-aux.sf3 --vcsl <VCSL の場所> --wp <WorldPercussion.sf2>
```

元のデータは作業後に削除したので、再現するときは付録A のリポジトリ・ページから取り直す。

## 付録C: 測定値の生データの場所

- 自分の曲の測定: 作業用の ours.json と ext_*.json（`/tmp/claude-0/.../scratchpad/suno-gap/`。セッションの終了で消える可能性がある）。この文書の 2.2〜2.4 の表に、必要な数値を転記してある。
- Suno 代理の統計: `docs/sound/data/nihonichi-bgm-1000-metrics.json`（1000曲）、`docs/sound/data/genre-targets-nihonichi.json`（分類別の p10 / 中央値 / p90）。

## 11. 追補（2026-10-14）: キーボード・シンセ系の音源の追加

人間（旭さん）の依頼「キーボード系の音源を追加して」への対応。すべて作曲ソフト専用（`tools/composer/entry.ts` の `PIANO_FONTS`）。ゲーム本体の `dist/` には入れていない。追加は 35 ファイル・約 44MB（SF3）。規約の本文・README の写しは `assets-src/soundfont/extra/src/licenses/`、素材ごとの規約の要点は `docs/assets-credits.md`。

### 11.1 追加した音源

印: 【規約】本文を読んだ／【実測】SF3 を作曲ソフトと同じ描画（spessasynth）で鳴らして、音程（倍音の検査）・無音でないこと・ループの音量の落ち込みを機械で確かめた／【耳×】耳では未確認。

| ファイル（`assets-src/soundfont/extra/`） | 中身 | GM 番号 | 規約 | 容量 |
|---|---|---|---|---|
| `piano-ydp-grand.sf3` | グランドピアノ（Disklavier Pro。Zenph/OLPC の録音を FreePats が SoundFont 化） | 0 | **CC BY 3.0（クレジット必須）** | 9.96MB |
| `piano-honkytonk.sf3` | ホンキートンクピアノ（FreePats Piano FB） | 3 | CC0 | 1.31MB |
| `epiano-fm-dx7.sf3`／`epiano-fm-bright.sf3` | FM エレピ（DX7 風）2 種 | 4 | CC0 | 2.93／1.05MB |
| `epiano-tx81z-fm.sf3`／`epiano-tx81z-piano1.sf3` | TX81Z 実機録音の FM エレピ／ピアノ風（VCSL） | 4 | CC0 | 3.07／2.52MB |
| `keys-clavi-tx81z.sf3` | クラビ風の FM 音（TX81Z Clavisynth）。**本物のクラビネットではない** | 7 | CC0 | 1.71MB |
| `harpsichord-french.sf3`／`harpsichord-italian.sf3` | チェンバロ 2 種（VCSL） | 6 | CC0 | 1.91／2.32MB |
| `chimes-vcsl.sf3`／`glass-water.sf3` | ハンドチャイム／水のグラス。**セレスタの代わり**（本物のセレスタは見つからなかった） | 8 | CC0 | 0.54／2.22MB |
| `glockenspiel-vcsl.sf3` | グロッケン | 9 | CC0 | 1.25MB |
| `vibraphone-vcsl.sf3` | ビブラフォン（ハードマレット） | 11 | CC0 | 1.51MB |
| `marimba-vcsl.sf3` | マリンバ | 12 | CC0 | 0.56MB |
| `xylophone-vcsl.sf3` | シロフォン | 13 | CC0 | 0.28MB |
| `accordion-hohner.sf3` | アコーディオン（Hohner のボタン式。ループあり） | 21 | CC0 | 0.80MB |
| `synth-lead-square.sf3` | シンセリード スクエア | 80 | CC0 | 1.06MB |
| `synth-lead-saw.sf3`／`synth-lead-supersaw.sf3`／`synth-lead-arp.sf3` | ソー／スーパーソー（7 本）／アルペジオ向けの短い音。**自作の合成** | 81 | 外部素材なし | 0.51／0.47／0.15MB |
| `synth-lead-calliope.sf3`／`synth-lead-fifths.sf3`／`synth-lead-bass.sf3` | カリオペ／5度／ベース＋リード | 82／86／87 | CC0 | 0.49／1.54／0.89MB |
| `synth-poly-analog.sf3` | ジュピター系のポリシンセ（自作の合成） | 90 | 外部素材なし | 0.40MB |
| `synth-strings-machine.sf3` | ストリングスマシン（自作の合成） | 50 | 外部素材なし | 0.58MB |
| `synth-strings-1.sf3`／`synth-strings-2.sf3` | シンセストリングス（FreePats） | 50／51 | CC0 | 0.75／0.94MB |
| `synth-brass-analog.sf3` | アナログ風シンセブラス（自作の合成） | 62 | 外部素材なし | 0.33MB |
| `synth-brass-zyn.sf3`／`synth-brass-dx7.sf3` | シンセブラス 1／DX7 風（FreePats） | 62／63 | CC0 | 0.66／0.33MB |
| `synth-bass-moog.sf3`／`synth-bass-acid.sf3` | ムーグ系／アシッド（303 風）ベース（自作の合成） | 38／39 | 外部素材なし | 0.16／0.14MB |
| `synth-bass-zyn.sf3`／`synth-bass-lately.sf3`／`synth-bass-dx7.sf3` | シンセベース 1／Lately Bass／DX7 BASS 風（FreePats） | 38／38／39 | CC0 | 0.18／0.38／0.30MB |

- 検査の結果【実測】: すべて無音ではない。音程は、サンプル単体の検査と、作曲ソフトの描画での検査（鍵盤 5〜8 点）の両方で合っている。ループの音(アコーディオンと自作シンセ)は、3 秒保持しても落ち込みがなく、つなぎ目の飛びもない。
- 低音域で基音が極端に弱い録音（チェンバロ イタリア型の最低域、ホンキートンクと YDP の最低域）は、基音の検査では判定できなかったので、倍音が基音の整数倍に乗っているかで確かめた【実測】。
- 【耳×】音色の良し悪し、音量バランス、ループの自然さ、自作シンセの出来は、耳で確かめていない。自作シンセの音量は、FreePats のシンセと実効値（RMS）が±5dB 程度におさまるよう寄せたが、ほかの音源との釣りあいは未確認。
- 音名のずれを実測で直した: VCSL の鍵盤・打楽器は、ファイル名の音名が 1 オクターブ低く（Clavisynth は 2 オクターブ低く）書かれていた。FM Piano（TX81Z）はずれなし。

### 11.2 追加できなかったもの（理由）

| 欲しかった音 | 状況 |
|---|---|
| 本物のクラビネット | CC0・CC BY の録音が見つからなかった。代わりに FM のクラビ風（TX81Z Clavisynth） |
| 本物のセレスタ | 同上。代わりにハンドチャイムと水のグラス |
| Rhodes の別の無料音源 | jRhodes3c/3d は非商用（CC BY-NC 系）で使えない。FM エレピ（DX7 風）を代わりに追加。見つかれば CC0/CC BY の Rhodes を足す |
| ハモンド系の別音色 | FreePats の 4 種（ドローバー・パーカッシブ・ロック・教会）で足りると判断。ほかに CC0/CC BY の候補は見つからなかった |
| メロトロン | Sforzatron（Plogue 配布の Taijiguy 版）は SFZ 一覧のライセンス欄が空で規約が読めない。使わない。ストリングスマシン（自作）で代用 |
| 本物のムーグ・ジュピターなどの録音 | 規約を読めた無料の録音が見つからなかった。**自作の合成**で、ソー波・ラダーフィルター・アンサンブルコーラスから作った（`tools/soundfont/build-analog-synths.mjs`）。本物の機材の録音ほどの厚みや揺らぎはない |
| 別のグランドピアノ（Kawai／Steinway B。VCSL、CC0） | 取得に 500MB 以上かかり、ディスクの空きが約 2〜3GB しかなかったので見送り。次の担当向けの候補（Salamander と YDP がすでにある） |
| Pianobook | 規約（制作への商用利用は可、ただし商用のサンプルライブラリにしない）はパックごと。SoundFont をソフトに入れて配る形が認められるか不明なので使わない |
| Surge／Vital／Helm のプリセットの録音 | 実際に録るには、そのソフトを入れて描画する必要がある。FreePats の Zyn/Hexter/Surge 由来の CC0 の録音で、リード・ベース・ブラス・ストリングスを埋めた |

### 11.3 組み込み（`tools/composer/entry.ts`）と、使うときの注意

- `PIANO_FONTS` の末尾に 35 行を追加した（`import ...?url` と `{label, url}` の 1 行）。ラベルの末尾の（ ）が GM の番号。
- **鍵盤の差し替えスロットは 1 つだけ**。同時に選べるのは 1 つ（たとえば、ビブラフォンとシンセリードを同時に差し替えることはできない）。同時に使いたいなら、スロットを増やすか、SF3 をまとめる必要がある。
- 優先順位は、ベース・ドラム・ギター・オーケストラ・ピアノ（鍵盤）・シンセの順。**オーケストラ音源（VSCO）を選ぶと、9（グロッケン）・12（マリンバ）などはそちらが優先される**。マリンバ・グロッケンの差し替えを聴くときは、オーケストラを「標準」にする。
- **曲から実際に使われる番号か**（`src/audio/gm-map.ts`・`ai-song.ts` の `SYNTH_PATCHES`）:
  - 使われる: ピアノ 0、エレピ 4（keys）、チェンバロ 6（harpsichord）、グロッケン 9（bell）、ビブラフォン 11（chime）、オルガン 16〜19、ストリングス 50・51（synthStrings1/2）、リード 80・81・82・86・87、ポリシンセ 90、ベース 38・39（synthBass1/2・sub808）、グロッケン patch 9、マリンバ patch 12。
  - **patch に名前がなく、曲から選べない**: ホンキートンク 3、クラビ 7、セレスタ 8、シロフォン 13、アコーディオン 21、シンセブラス 62・63（brass 楽器は 61 を使う）。使うには、`SYNTH_PATCHES` に `honkyTonk: 3, clavinet: 7, celesta: 8, xylophone: 13, accordion: 21, synthBrass1: 62, synthBrass2: 63` を足す必要がある（`ai-song.ts` の変更になるので、今回は触っていない）。
  - 通常の「標準」音源（`game.sf3`）は使う番号だけに切り出してあるので、上の番号は、差し替えを選ばないと無音になる可能性がある（未確認）。
- 作曲ソフトの HTML は音源を丸ごと埋め込むので、**HTML が約 44MB（Base64 で約 59MB）大きくなる**。重いと感じたら、YDP（10MB）を外すのがいちばん効く。

### 11.4 作ったツール

| ツール | 役割 |
|---|---|
| `tools/soundfont/build-analog-synths.mjs` | 自作のアナログ風シンセ 8 種を、WAV と SFZ に書き出して SF3 にする。ループの長さを整数フレームにして、全オシレーターの周期の数を整数にそろえる（つなぎ目が鳴らない）。基音のずれは SFZ の tune で打ち消す |
| `tools/soundfont/strip-unused.mjs` | `sfz-to-sf3.mjs` の出力に残る、使われていないサンプル（元のゲーム音源から写った約 95KB）を取り除く。音は変わらない |
| `tools/soundfont/sf2-to-sf3.mjs` に `--first-only` を追加 | 強さ別のプリセットが複数入った SF2 で、最初の 1 つだけ残す（ほかの GM 番号を上書きしないため） |

| `tools/soundfont/gen-vcsl-sfz.py` | VCSL の WAV 一式から SFZ を作る（音名のオクターブ補正と、層ごとの音量そろえつき）。例: `python3 -I tools/soundfont/gen-vcsl-sfz.py "<VCSL>/Idiophones/Struck Idiophones/Marimba" marimba . 'Outrigger_([A-G]#?\d)_' '_(soft|med|loud)_' soft,med,loud 1`（最後の 1 がオクターブ補正） |
| `tools/audio-check/sf3-render-check.mjs`・`sf3-pitch-check.mjs` | 検査。前者は作曲ソフトと同じ描画で鍵ごとに音量・基音・ループの落ち込み・飛びを見る。後者は SF3 のサンプルごとに基音の位置と無音を見る |
