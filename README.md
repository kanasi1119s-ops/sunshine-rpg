# sunshine-rpg（仮題）

サンシャインソフトウェアが制作中の、ブラウザで遊べるオリジナル長編RPGです。

- 王道のコマンド選択式RPGの遊び心地に、章をまたいで真相に近づくミステリーを組み合わせた物語
- メインストーリーは48時間以内にクリアできる長さ（目標30〜40時間）、サブストーリーとクリア後の裏ボスあり
- オリジナルのファミコン〜スーファミ風BGM

> 現在制作中です。進み具合は [`docs/progress.md`](docs/progress.md) をご覧ください。

## 遊び方

（ゲームの基盤ができたら、ここに起動方法と説明書 `docs/manual.md` へのリンクを書きます）

## Claude Code で作り進める

このリポジトリは Claude Code で作り進める前提で設定されています。

| やりたいこと | Claude Code で入力するもの |
|---|---|
| 工程表に沿って作業を1回分進める | `/rpg-cycle` |
| 今どこまでできているかを知る | `/rpg-status` |

- プロジェクトの決まりごと: [`CLAUDE.md`](CLAUDE.md)
- 作業1回分の手順: [`.claude/skills/rpg-cycle/SKILL.md`](.claude/skills/rpg-cycle/SKILL.md)
- 定期タスクの設定方法: [`docs/scheduled-task.md`](docs/scheduled-task.md)
