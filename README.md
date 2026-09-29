# sunshine-rpg（仮題）

サンシャインソフトウェアが制作中の、ブラウザで遊べるオリジナル長編RPGです。

- 王道のコマンド選択式RPGの遊び心地に、章をまたいで真相に近づくミステリーを組み合わせた物語
- メインストーリーは48時間以内にクリアできる長さ（目標30〜40時間）、サブストーリーとクリア後の裏ボスあり
- オリジナルのファミコン〜スーファミ風BGM

> 現在制作中です。進み具合は [`docs/progress.md`](docs/progress.md) をご覧ください。

## 遊び方

まだ画面表示だけの土台段階です（歩行や戦闘はこれから作ります）。

```bash
npm install
npm run dev
```

- `npm run build` — 本番用ビルド
- `npm test` — 自動テスト

操作方法や遊び方の詳細は [`docs/manual.md`](docs/manual.md) を参照してください。

## Claude Code で作り進める

このリポジトリは Claude Code で作り進める前提で設定されています。

| やりたいこと | Claude Code で入力するもの |
|---|---|
| 工程表に沿って作業を1回分進める | `/rpg-cycle` |
| 今どこまでできているかを知る | `/rpg-status` |

- プロジェクトの決まりごと: [`CLAUDE.md`](CLAUDE.md)
- 作業1回分の手順: [`.claude/skills/rpg-cycle/SKILL.md`](.claude/skills/rpg-cycle/SKILL.md)
- 定期タスクの設定方法: [`docs/scheduled-task.md`](docs/scheduled-task.md)

## 使用している外部素材（クレジット）

- 地形のタイル絵の一部に、ぴぽや「フィールドマップセット１」（https://pipoya.net/ ）の無料素材を加工して使っています。規約と記録は [`docs/assets-credits.md`](docs/assets-credits.md) を参照してください。

- BGMの録音音源に、Fluid (R3) GM SoundFont（© 2000-2002 Frank Wen、Mono版 © 2014-2017 Michael Cowgill、MITライセンス）から、ゲームで使う楽器だけを切り出して使っています。再生には spessasynth（Apache-2.0）を使っています。ライセンス文は `public/licenses/` にあります。
