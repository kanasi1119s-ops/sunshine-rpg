# 曲の直しの記録

形式: `- 日付 曲ID: 直す前の数字 → 直した点（1つ）→ 直した後の数字 → 耳の印象`
追記は `node tools/composer/song.mjs log <曲ID> --before ... --change ... --after ... --ear ...`。直しは1回に1点。同じ失敗が3回出たら、ai-composition-workflow.md か AI_SONG_GUIDE に決まりとして追記する。

- 2026-10-15 scarlet-chapter-modern-long: 空間版・6分（チョーキングの代わりに半音の並び・32分のタッピング・スラップのソロ） → 現代版に作り変え: 旋律ピアノ＋リードギター warm-lead-b（ビブラート・チョーキングなし、サビは1オクターブ下でベルを重ねる）・タッピング→ピアノソロ・スラップ→指弾きベース・左右の歪みギターと弦・サビの厚いシンセ・セクションごとのドラムの型。--edition modern --drums jpop --bass pick --piano salamander --orchestra vsco --guitar emily --master-preset jpop-band → PQ 8.15（60秒ずつの平均。ドラム -3dB で 8.19 だが +0.04 なので採らず）・I -13.5 / TP -1.3 → 未（人間の感想待ち）
- 2026-10-15 helter-skelter-rb: 新曲 → R&B×ロック・BPM138シャッフル・イ長調ブルース→ロ長調。--drums muldjord --bass finger --piano salamander --orchestra vsco --guitar emily --master-preset rock-clean → PQ 8.39（60秒ずつの平均）・I -13.5 → 未（人間の感想待ち）
- 2026-10-15 spark-floor: 新曲 → ダンス×ロック・BPM126・ト短調。標準ドラム＋edm 仕上げ（-13.5）。生ドラム＋rock-clean は 7.89、標準ドラム＋rock-clean は 8.13 → PQ 8.14（60秒ずつの平均）。--edition modern --bass pick --piano salamander --guitar emily --master-preset edm --master -13.5 → 未（人間の感想待ち）
- 2026-10-15 spark-floor-karaoke: インストのみ → 重音テトの歌を追加（spark-floor-vocal.py、歌は D4〜Eb5 に書き直し）。伴奏は歌の所の旋律楽器を外した版（KARAOKE=1）。歌 utau-render --last 104-120、vocal-mix --vocal-lu 1.5 → PQ 8.18（60秒ずつの平均）。文字起こしはほぼ歌詞どおり（サビ頭の『さあ』だけ『ら』に聞こえる） → 未（人間の感想待ち）
- 2026-10-16 celtic-epic-omen: PQ 7.52（楽器が17種類でチャンネルがあふれ、弦・チェロなどがアコーディオンの音で鳴っていた） → 同じ楽器のパートの pan・reverb・fx をそろえて15チャンネルに収め、遠いベル・インパクト・フィドル2を外し、不穏の所にアコギ、ティンパニと大太鼓を -4dB → PQ 8.01・プチッ 1か所（65秒） → 未確認（人間に聞いてもらう）
