# 顔のアイコン（512×512・128×128）を作るためのプロンプト

仲間6人（ユーリ・レト・ミナ・コハク・オルカ・アヤメ）の顔アイコンと同じ作り（顔に寄せた構図、頭は切らない、ドット絵エディタで描く）で、新しい人物のアイコンを作るときの頼み方。
`〈 〉` のところを書きかえて使う。手順の中身は `character.md` の「5-2. 顔のアイコン」。

## A. Claude（定期作業・Claude Code）に頼むとき

```
/make-art 〈名前〉の顔アイコンを作ってください。

イメージ画像: 〈置き場所。例: assets-src/ref/〈名前〉.jpg（顔のアップの枠があれば、その枠から）〉
（イメージ画像がないとき: 〈髪の色と形・目の色・肌・服の襟元の色・頭の飾り（はちまき・リボン・兜・額の飾りなど）・表情〉を英語の1文にして、
 make_jobs.py character で胸から上の下絵を描いてから使う）

作り方（仲間6人の顔アイコンとそろえる）:
- 大きさは 512×512（32色）と 128×128（24色）の2つ。どちらも同じ構図にする。
- 構図（全員で顔の大きさをそろえる）: icon_frame.py で、元の絵の両目の中心・あご先・顔の幅（目の高さでのほおの外側）を指定する。
  √(目〜あご × 顔の幅) = 138px（512のとき）、目の高さは上から55%、両目の真ん中が画面の真ん中になる。
  頭のてっぺん（髪の先・帽子・リボン・ゴーグル・額の飾りまで）は必ず入れる。入らないときは、その人物だけ少し小さくして、理由を書く。
  横に流れる長い髪やリボンの端は、枠で切れてもよい。元の絵に足りない所（首から下・頭の上・横）は icon_frame.py が描き足す（元の絵の部分は変えない）。
  描き足した服の色が元の絵と違ったら、--desc に色をはっきり書いて作り直す。
- 背景は rembg の isnet-anime で切り抜き、いちばん大きなかたまりだけ残す。街灯・建物などの取り残しは消す。
- icon512.py で、正方形の構図のまま減色する（icon_frame.py で構図を決めたあとなので --crop はいらない）。輪郭は真っ黒にせず、その部分を暗くした色。胸の下の切れ目には輪郭をつけない。
- うちのドット絵エディタで描いて「食い違い 0 マス」を確かめる（512 は --import --wide --zoom 4、128 は --import --zoom 6）。
- 有名な作品のキャラに似ていないかを確かめる。

できたら、2つの大きさを並べた見本と、エディタ用のファイル（文字グリッド・色）を見せてください。ゲームへの組み込みは、見せてから決めます。
```

## B. 画像生成AI（ChatGPT・Gemini など）で下絵を作るとき

画像AIの絵は**下絵**として使い、仕上げ（切り抜き・減色・エディタで描く）は A の手順で行う。

```
RPGの会話ウインドウに出す、キャラクターの顔のアップのイラストを1枚描いてください。正方形。
構図: 胸から上。顔を大きく、頭のてっぺん（髪の先・帽子・髪飾りまで）とあごが必ず画面に入り、頭の上に少し余白を残す。顔は少し斜め、目線はこちら。
キャラクター: 〈例: 港町の見張りの青年。黒に近い紺の少しはねた短髪、灰色の目、日焼けした肌、紺の上着に赤いマフラー、落ち着いた笑み〉
絵の決まり: くっきりした輪郭線とアニメ調の塗り分け（影は2〜3段）、光は左上から。背景は無地の明るい色（あとで切り抜くため）。
文字・枠・ほかの人物は入れない。既存のゲームや漫画のキャラクターには似せない。
```

英語で頼むとき:

```
A square close-up portrait of an RPG character for a dialogue window, chest up.
The face is large; the whole head including the top of the hair, hat or hair ornament and the chin must be inside the frame, with a little space above the head.
Three-quarter view, looking at the viewer.
Character: 〈a young harbor lookout, short slightly messy navy-black hair, gray eyes, tanned skin, navy jacket and red scarf, calm smile〉.
Clean line art, anime-style cel shading with 2-3 tones, light from the top-left, plain light background for easy cutout.
No text, no frame, no other people. Original design, not based on any existing game or manga character.
```

## 書くときの注意

- 作品名・ゲーム名・作者名・既存のキャラの名前は書かない（CLAUDE.md 1-1）。
- 写真をもとにしたアニメ風の画像は使わない（人間の指示）。
- 髪の色・目の色・目印の1色は、全身の絵（256×256）と歩くキャラ（16×32）と同じ色にする。
