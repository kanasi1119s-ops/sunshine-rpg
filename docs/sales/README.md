# 販売の準備（サンシャイン作曲ソフト）

お金をかけずにできる準備は、ここまでで済ませてあります。**お金がかかること・外に公開すること・契約は、人間（旭さん）が行います**（CLAUDE.md 1-2）。

## 用意できているもの（無料）

| もの | 場所 | 状態 |
|---|---|---|
| アプリのアイコン（オリジナル） | `desktop/build/icon.svg`・`icon.png` | できた。Windows・Mac・Linux のアプリに入る |
| 利用規約（案） | `desktop/legal/terms-ja.md`（インストール時に出る版 `eula-installer-ja.txt`） | **案**。【 】を埋め、専門家に確認してもらう |
| プライバシーポリシー（案） | `desktop/legal/privacy-ja.md` | **案**。同上 |
| 特定商取引法に基づく表記（ひな形） | `docs/sales/tokushoho-template.md` | ひな形。【 】を埋める |
| 販売ページの説明文（案） | `docs/sales/store-listing.md` | 案 |
| 画面写真（1280×800） | `docs/sales/screenshots/` | 3枚 |
| 購入者向けのインストール案内 | `docs/sales/install-guide.md` | 署名なしで売るときの警告の説明つき |
| 署名の設定（証明書が来たら差し込むだけ） | `.github/workflows/desktop.yml`・`desktop/package.json`・`desktop/build/entitlements.mac.plist` | できた（Secrets がなければ署名なしで作る） |
| Microsoft Store 向けの形（appx） | `desktop/package.json` の `appx`、ワークフローの「store」 | できた（Partner Center の値を入れると作れる） |
| MP3 の書き出し（デスクトップ版） | `desktop/mp3.cjs` | できた。LAME（LGPL-3.0）を別ファイルのまま使い、表示とライセンス文を同梱 |
| ライセンス表示 | アプリの「ヘルプ」→「ライセンス」 | 使っている部品すべて（MIT・Apache-2.0・OFL・LGPL） |
| 外への通信を減らす | デスクトップ版は文字のフォントを同梱 | Google への通信なし（AI作曲のときの Anthropic だけ） |

## 人間がすること（順番の目安）

1. **屋号・連絡先を決め、規約・表記の【 】を埋める**（無料）。規約とプライバシーポリシーは、できれば専門家に見てもらう（有料のことが多い）。
2. **販売先を決める**（BOOTH・itch.io・Gumroad・Steam・Microsoft Store・Mac App Store など）。手数料や、返金の決まりは販売先ごとにちがう。
3. **署名**（有料。下の表）。署名なしでも売れるが、お客さんのパソコンで警告が出る（`install-guide.md` で案内）。
4. **インストーラーを作る**: GitHub の Actions → 「desktop」→「Run workflow」。できたファイルは、その実行の Artifacts から受け取る。
5. **販売ページを作って公開・価格を決める**（人間だけが行う）。

## 署名（証明書）の入れ方

証明書を手に入れたら、GitHub のリポジトリの Settings → Secrets and variables → Actions に、次の名前で入れる。入れたあとで「desktop」を動かすと、自動で署名される。

| 対象 | 何を用意するか（目安。申し込む前に公式サイトで確かめる） | Secrets の名前 |
|---|---|---|
| Windows | コード署名の証明書（.pfx）。認証局から買う（年に数万円〜）。または Microsoft の署名サービス（月額）※この場合は設定を足す | `WIN_CSC_LINK`（.pfx を base64 にした文字）・`WIN_CSC_KEY_PASSWORD` |
| Mac | Apple Developer Program（年会費）に入り、「Developer ID Application」の証明書（.p12）を作る。公証のために、Apple ID の「App用パスワード」とチームID | `MAC_CSC_LINK`・`MAC_CSC_KEY_PASSWORD`・`APPLE_ID`・`APPLE_APP_SPECIFIC_PASSWORD`・`APPLE_TEAM_ID` |
| Microsoft Store | Partner Center に開発者として登録（個人は無料になっている、とされる。登録時に確かめる）。アプリの名前を予約すると出る「Package/Identity/Name」と「Publisher」 | `STORE_IDENTITY_NAME`・`STORE_PUBLISHER`（ワークフローの「store」にチェックして動かす） |

- Microsoft Store で配る場合は、ストアが署名するので、Windows の証明書を買わなくても警告が出ない（店の審査はある）。
- 秘密の値（証明書・パスワード）は、リポジトリのファイルやチャットに書かない。Secrets にだけ入れる。

## 注意

- 規約・表記は案。法律の助言ではない。
- AI作曲は、お客さん自身の Anthropic APIキーで動き、料金はお客さんにかかる。販売ページにも書く（`store-listing.md` に入れてある）。
- 売る前に、使っている部品のライセンス（`docs/assets-credits.md`）をもう一度確かめる。特に、利用者が読み込むアンプ定義・IR・NAMモデルは同梱していない（同梱するなら規約を確かめる）。
