# イベントスクリプトの書式

会話・フラグ管理・マップ移動などをデータとして書くための書式です。
実装は `src/game/event/types.ts`（型定義）と `src/game/event/event-runner.ts`（実行エンジン）にあります。

## 基本の形

イベントは `EventCommand` の配列（台本）です。上から順番に実行されます。

```ts
const commands: EventCommand[] = [
  { type: "message", text: "やあ、旅の人。", speaker: "村人" },
  { type: "message", text: "この先には気をつけてね。" },
];
```

## コマンド一覧

### message — メッセージを表示する
```ts
{ type: "message", text: "本文", speaker: "話者名（省略可）" }
```
画面下のメッセージウィンドウに、文字送りしながら表示する。プレイヤーが決定ボタンを押すと次へ進む。

### choice — 選択肢を出す
```ts
{
  type: "choice",
  text: "どうする？",
  options: [
    { label: "はい", commands: [ /* 選んだ後に実行するコマンド */ ] },
    { label: "いいえ", commands: [ /* ... */ ] },
  ],
}
```
選んだ選択肢の `commands` だけが実行され、終わったら選択肢の外側の続きに戻る。

### setFlag — フラグを立てる／消す
```ts
{ type: "setFlag", flag: "met_villager", value: true }
```
フラグは章をまたいで持ち越される想定（後日セーブデータに含める）。フラグ名は分かりやすい英語のスネークケースにする。

### if — フラグで分岐する
```ts
{
  type: "if",
  flag: "met_villager",
  equals: true,
  then: [ /* フラグがtrueのとき */ ],
  else: [ /* フラグがfalseのとき（省略可） */ ],
}
```

### warp — 別マップへ移動する
```ts
{ type: "warp", mapId: "town-a", tileX: 5, tileY: 10 }
```
会話ウィンドウを閉じずに、そのまま次のコマンドへ進む（暗転などの演出は今後追加予定）。

## 注意点（ミステリー構成担当・シナリオライター向け）

- **フェアプレイの原則**（`CLAUDE.md` 2-2）: 推理パートで使う手がかりは、必ずそれより前の `setFlag` で記録できるようにする
- 伏線・手がかりに関わる `setFlag` を追加したら、`docs/story/clue-ledger.md`（今後作成）を必ず更新する
- 町の人のセリフを章ごとに変えるときは、`if` で章の進行フラグを見て分岐する
