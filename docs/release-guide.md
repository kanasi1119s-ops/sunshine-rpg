# 公開の手順（人間が行う作業）

このリポジトリには GitHub Pages 用のワークフロー（`.github/workflows/deploy-pages.yml`）がすでに置いてあります。ただし、**実際に公開される状態にする操作は人間が行います**（`CLAUDE.md` 1-2、1-3）。Claude Code はこの手順を実行しません。

## Pages を有効にする手順

1. GitHub のリポジトリ画面で **Settings → Pages** を開く
2. **Source** を「GitHub Actions」にする
3. **Settings → Secrets and variables → Actions → Variables** で、新しい変数を追加する
   - 名前: `ENABLE_PAGES_DEPLOY`
   - 値: `true`
4. `main` ブランチに何かをプッシュする（もしくは Actions タブから `Deploy Pages` を手動実行する）と、公開される

## 今の動き

- `main` への push・プルリクエスト・手動実行のたびに、依存関係のインストール→テスト→ビルドは必ず行われる（`build` ジョブ）
- 実際に公開する `deploy` ジョブは、`main` ブランチへのpushで、かつ変数 `ENABLE_PAGES_DEPLOY` が `true` のときだけ動く
- つまり、上の手順を行うまでは、ビルドとテストの確認だけが行われ、何も公開されない

## 公開を止めたいとき

- **Settings → Secrets and variables → Actions → Variables** で `ENABLE_PAGES_DEPLOY` を `false` にするか、削除する
- すでに公開されているページ自体を止めたい場合は、**Settings → Pages** の Source を「None」に戻す
