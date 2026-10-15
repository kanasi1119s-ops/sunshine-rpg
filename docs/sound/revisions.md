# 曲の直しの記録

形式: `- 日付 曲ID: 直す前の数字 → 直した点（1つ）→ 直した後の数字 → 耳の印象`
追記は `node tools/composer/song.mjs log <曲ID> --before ... --change ... --after ... --ear ...`。直しは1回に1点。同じ失敗が3回出たら、ai-composition-workflow.md か AI_SONG_GUIDE に決まりとして追記する。

- 2026-10-15 scarlet-chapter-modern-long: 空間版・6分（チョーキングの代わりに半音の並び・32分のタッピング・スラップのソロ） → 現代版に作り変え: 旋律ピアノ＋リードギター warm-lead-b（ビブラート・チョーキングなし、サビは1オクターブ下でベルを重ねる）・タッピング→ピアノソロ・スラップ→指弾きベース・左右の歪みギターと弦・サビの厚いシンセ・セクションごとのドラムの型。--edition modern --drums jpop --bass pick --piano salamander --orchestra vsco --guitar emily --master-preset jpop-band → PQ 8.15（60秒ずつの平均。ドラム -3dB で 8.19 だが +0.04 なので採らず）・I -13.5 / TP -1.3 → 未（人間の感想待ち）
- 2026-10-15 helter-skelter-rb: 新曲 → R&B×ロック・BPM138シャッフル・イ長調ブルース→ロ長調。--drums muldjord --bass finger --piano salamander --orchestra vsco --guitar emily --master-preset rock-clean → PQ 8.39（60秒ずつの平均）・I -13.5 → 未（人間の感想待ち）
