# 定期タスクの設定方法

## 定期タスク（クラウドで自動実行）

claude.ai の Claude Code で新しい定期タスクを作り、次のように設定します。

| 項目 | 設定 |
|---|---|
| 名前 | 長編RPG作成 |
| リポジトリ | `kanasi1119s-ops/sunshine-rpg` |
| 実行時刻 | 毎日 1:20・5:20・9:20・13:20・17:20・21:20（日本時間）<br>cron で書く場合: `CRON_TZ=Asia/Tokyo 20 1,5,9,13,17,21 * * *` |
| プロンプト | 下の枠の文章をそのまま貼る |

```
リポジトリ kanasi1119s-ops/sunshine-rpg で /rpg-cycle を実行し、長編RPGを前回の続きから1回分作り進めてください。
スキルが読み込めない場合は、リポジトリの .claude/skills/rpg-cycle/SKILL.md を読み、その手順どおりに作業してください。
CLAUDE.md の「大前提」は必ず守ってください。報告は日本語でお願いします。
```

長い指示はすべてリポジトリの中（`CLAUDE.md` と `.claude/skills/`）にあるので、プロンプトは短いままで大丈夫です。指示を変えたいときは、定期タスクではなくリポジトリのファイルを直します。

## 自分のPCの Claude Code で作業する

```bash
git clone https://github.com/kanasi1119s-ops/sunshine-rpg.git
cd sunshine-rpg
claude
```

Claude Code が起動したら、次のどちらかを入力します。

- `/rpg-cycle` … 工程表に沿って作業を1回分進める
- `/rpg-status` … 今どこまでできているかを見る

個別の依頼（「この曲をもっと明るくして」「第2章のボスを弱くして」など）も、そのまま話しかければ `CLAUDE.md` の決まりごとに沿って作業します。

**注意:** 定期タスクと同じ時間帯に自分のPCで `/rpg-cycle` を動かすと、作業がぶつかることがあります。`docs/progress.md` の「作業中」欄が空のときに始めてください。
