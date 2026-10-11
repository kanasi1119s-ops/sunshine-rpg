# サウンドセット（2026-10-11）
「この音で作る」を1つ選ぶだけで、アンプ・パートごとの音量・ミックス・ドラムの設定と、使う音源（ベース・ドラム・ギター）をまとめて切りかえる仕組み。
- 定義：`src/audio/sound-sets.ts`（`SOUND_SETS`）。音そのものは入っていない。参考にした録音・曲から測った**数値**だけ。
- 作曲ソフト：「サウンドセット」の選択欄。選ぶと、いまの曲にアンプ・音量・ミックスを当て、ベース・ドラム・ギターの音源も切りかえる（音符は変えない。もとの音量には戻せないので、先にプロジェクトを保存する）。
- 書き出し：`node tools/composer/song.mjs build 曲.json --wav --sound punk-run`。一覧は `node tools/composer/song.mjs sounds`。`--bass/--drums/--guitar` を別に書けば、そちらが優先。
- 当て方の決まり：書かれた楽器の音量は目標値に置きかえ、書かれていない楽器は 0.06 を上限に。全パートの合計が 0.9 をこえたら、同じ比率で下げる（内部のリミッターでつぶれて割れるのを避ける）。何度当てても同じ結果。
## いまあるセット
| id | 音 | 元にしたもの |
|---|---|---|
| `punk-run` | 疾走パンク。歪みギターを左右に前へ、2ビート、生ギターのクリーンのメロディ | 参考録音5曲の楽器ごとの分析の数字（見本曲は採用せず削除済み） |
| `clear-guitar-rock` | 透明感ギターロック。生ギターの自然な余韻、ナイロン弦、タム低め | 人間が「いい」と言った band-pedal-arpeggio |
確かめ：`clear-guitar-rock` を元の曲に当てると、帯域は元の音と 2dB 以内、crest は 12.8→15.8dB（つぶれにくい）。
## 新しいセットの作り方（録音を分析して）
1. 参考にする録音を `analyze.py`（帯域・左右・音量の起伏）と `analyze-rhythm.py`（テンポ・ドラムの型）で測る。
2. 同じ指標でうちの曲を測り、差が大きい帯域を、アンプ・パートの音量・ドラムの `level` で詰める。
3. 決まった値を `sound-sets.ts` に1つ足す。**名前は音の特徴にする**（バンド名にしない）。元の録音は `source` にメモだけ書く。
## できていないこと
- 楽器ごとに分けた分析（音の分離）は、このクラウド環境ではできない（AIの分離モデルが入らず、取得も許可されていない）。あなたのパソコンで動かす形が必要。
- 高域（presence・air）を録音並みに出すには、アンプ（`punk` は 6.5kHz から上を落とす）とドラムの `level` 上限（1.05）の見直しが要る。

## 追加のセット（2026-10-11、ミックスのパターン）

`docs/sound/mix-patterns.md` の M17〜M48 から、`rock-4`・`pop-lead`・`jpop-bright`・`ballad-piano-strings`・`jazz-trio`・`funk-bass`・`house-duck`・`ambient-wide`・`orchestra-depth`・`game-battle`・`game-boss`・`game-town`・`game-dungeon` を足した。`master` に `preset`（`--master-preset` と同じ）・`space`・`spaceWet` を持てる。場面から選ぶ表は `SCENE_SETS`。`node tools/composer/song.mjs sounds` で一覧。詳しくは `mix-patterns.md` §10。


## パートの音づくり（`PART_RECIPES`、2026-10-11 追記）

`src/audio/sound-sets.ts` の `PART_RECIPES` に、クリーンギターの名前付きの音づくりを足した（人間が「いい」と言った `sparkle-delay`・`crystal-wide`・`sparkle-wide-delay`、J-POP のレシピA〜E `jpop-arpeggio`・`jpop-cutting`・`jpop-stroke`・`jpop-space`・`jpop-dimension`）。サウンドセットがアンプ・音量を曲全体に当てるのに対し、こちらは **1パートに当てる**。AIソング形式では `parts[].recipe` に名前を書く（書いていない項目だけ補う）。中身と注意は `jpop-clean-guitar-guide.md` §8。
