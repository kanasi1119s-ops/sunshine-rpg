# 町の人（NPC）のドット絵 一覧

ゲームの町の人は、プログラム（`src/game/sprite/character-specs.ts` の `spriteSpecForNpc` と `src/game/sprite/overworld-sprite.ts`）が、その場で色や髪型を決めて描いています。
ここには、その描き方で出てくる絵を、すべて画像に書き出して置いています（2026-10-06、人間の依頼）。ゲームはこの画像を読みこみません（見る・確かめる用）。

- `all-npcs.png` — 全種類の一覧（正面、4倍、名前と町つき）
- `each/` — 1種類ごとの画像（16×32 のコマを、下・左・右・上 × 3コマで横に並べた 192×32）
- `index.json` — 画像ファイルと、NPCのID・名前・いる地図の対応
- 同じ見た目の人は1種類にまとめています（355種類）

書き出し直し: 開発用サーバー（`npx vite --port 5199`）を動かしてから、`node assets-src/npc-sprites/export-npc-sprites.mjs`（Playwright が必要）。
