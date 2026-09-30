# サブストーリーの実装フォーマット（roadmap 5-1）

サブストーリーは `src/game/world/side-stories.ts` の一覧（`SIDE_STORIES`）に、1本ずつデータとして書く。形式は `src/game/world/side-story.ts` の `SideStory`。

## 1本の構造
- **依頼人（giver）**: 地図・座標・色（顔グラフィックがあれば `spriteName`）。話しかけると、次の状態で会話が切り替わる。
  1. 解放前（`unlockFlags` がそろっていない）→ `locked` の会話
  2. 受注前 → `offer` の会話 → 選択肢（受ける／あとにする）
  3. 受注中 → まだ調べ終わっていなければ `hint`、すべて調べ終わっていれば `complete` の会話と「ごほうび（仮）」
  4. 完了後 → `after`
- **調べる場所（steps）**: 依頼人とは別のNPC（物・人）。受注前は何も起きず、受注後に話しかけると `commands` が流れて `side_<key>_step<番号>` が立つ。回る順番は自由。選択肢を含めてよい（例: S-013）。
- 調べる場所が0個の話（例: S-008 昔語り）は、受注の選択肢で `complete` まで進み、その場で完了する。

## フラグの名前
`side_<key>_accepted` ／ `side_<key>_step<番号>` ／ `side_<key>_done`。ほかのサブストーリーの解放条件に `side_s004_done` のように使ってよい（S-010が例）。

## 解放条件
本編のフラグ（例: `chapter1_reported_to_elder`, `chapter3_orca_joined`）を `unlockFlags` に書く。本編に影響を与える話は、別に本編側のイベントを書く（サブストーリーは本編の進行に必要な情報を持たない）。

## 報酬（仮）
灯貨・所持品・信頼度・技の解放は、まだゲームの仕組みがない。今は「ごほうび（仮）」の1行と `side_<key>_done` の記録だけを残す。仕組みができたら、`reward` の文と `done` フラグを見て付与する（`docs/decisions.md` 2026-09-30）。

## テスト
`src/game/world/side-stories.test.ts`: IDの重複なし・座標が歩ける場所で出入り口や到着地点・ほかのNPCと重ならない・すべてのサブストーリーが解放→受注→調査→報告で完了できる・解放前は受けられない。
