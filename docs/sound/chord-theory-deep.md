# コード進行の理論をジャンル別・機能別に深く学ぶ（2026-10-11 調査）

`chord-variety-guide.md`（18レシピ A〜R。「似た進行を避ける」ための手引き）の**次の段**として、「なぜその進行がそう聞こえるか」「ジャンルや場面ごとにどんな型があるか」「セクションごとにどう変えるか」をまとめた。
書いたコード名は、うちの書式で**確実に読めるものだけ**を使っている（長3・短3・`7`・`m7`・`maj7`・`sus2`・`sus4`・`dim`・`aug`）。分数コード（`G/B`）は、現状では読み込みで止まる疑いがあるため（後述）、例には ※ を付けて少数にとどめた。
注意: 実在曲の進行をそのまま使わない（CLAUDE.md 1-1）。ここに書いたのはすべて「型」で、曲名とは結びつけていない。使うときは、主音・順番・長さ・旋律を必ず変える。

---

## 1. 要点（まず読む10行）

1. **和音には3つの役割がある。** 落ち着く（T：主和音の仲間 I・vi・iii）、離れる（SD：IV・ii）、引っぱって戻す（D：V・vii°）。基本の流れは T→SD→D→T。**同じ役割の和音どうしは入れ替えられる**（IV↔ii、I↔vi など）。進行を変えるいちばん安全な方法がこれ。
2. **ジャンルは「どの和音を使うか」より「どの動きをするか」で決まる。** ロックは♭VIIとIV（解決しない広がり）、ジャズはii–V–I（5度で強く解決）、ファンクやダンスは1〜2コードの往復（解決しない）、ゲームのダンジョンは機能を弱めて足場をぐらつかせる。
3. **借用和音（同主短調から）は、1進行に1つまで。** iv は切なさ、♭VII は開放感、♭VI は壮大、♭III は不思議な明るさ。長く居座ると転調に聞こえる。
4. **副ドミナント（次のコードの5度上のドミナント7th）は、1進行に1〜2回まで。** 引力が増してサビ向き。多用すると主音がぼやける。
5. **解決を外す（偽終止）と、聞き手は「まだ続く」と感じる。** V→vi が基本、V→♭VI（A♭など）は劇的。
6. **低音を固定（ペダル）するか、内声を1音ずつ動かす（クリシェ）と、同じ和音でも別物になる。** 変な進行も、低音を固定すると筋が通って聞こえる。
7. **メロディとの関係が、聞こえ方の半分を決める。** 強拍・長い音にはコードの構成音を置き、コードの構成音の半音上の音（アヴォイド）は短く通り過ぎる。
8. **曲全体で進行を変える。** サビは「短く、はっきり、同じ形の繰り返し」、Aメロは「ぼかして長い旅」、ブリッジは「主音以外から始めて、逆の調性へ寄り道」。セクションが違えば、始まりのコードも変える。
9. **転調は1曲に1回、準備（ドミナント・全休止・フィル）を付けて、盛り上がりの頂点で。** 半音／全音上げが定番、小3度上は大きな跳躍。
10. **うちのチェッカー（`chord-variety.mjs`）には穴がある。** 進行を回して（I–V–vi–IV と vi–IV–I–V）書くと別物と判定する、転調すると度数が崩れる、分数コードの低音を見ない。対策は「9. 取り入れる提案」。

---

## 2. 機能和声の早見（差し替えの道具箱）

| 役割 | 長調（Cの例） | 短調（Amの例） | 聞こえ方 |
|---|---|---|---|
| T 主和音 | I C ／ vi Am ／ iii Em（弱い主和音） | i Am ／ ♭III C ／ ♭VI F | 落ち着く・帰る |
| SD 準備 | IV F ／ ii Dm | iv Dm ／ ii° Bdim | 出発・ふくらむ |
| D 引力 | V G ／ V7 G7 ／ vii° Bdim | V E ／ V7 E7 ／ ♭VII G（弱い） | 緊張・戻りたい |

- 入れ替えの基本: **vi は I の代わり、iii は I の弱い代わり**。**ii は IV の代わり**。**vii° は V の代わり**。短調では、V（E）が長三和音だと終止が強くなり、♭VII（G）だと柔らかい（ロック向き）。
- 「T→SD→D→T」から外れる動き（D→SD、T→D など）は、ロックやポップスで普通にある。逆行（V→IV）は「ロックの開放感」になる。
- **強進行**（根音が4度上がる＝5度下がる）の連続は、自然に引っぱる。I→IV→vii°→iii→vi→ii→V→I の順に並べた「5度の輪」は、ほどよく先へ進むので、迷ったらこの輪の順に2〜3個たどる。

### 主なキーでの度数→コード名（主音を C 以外にするときの早見）

| キー | I | ii | iii | IV | V | vi | ♭VII | ♭VI | ♭III | iv（借用） |
|---|---|---|---|---|---|---|---|---|---|---|
| C | C | Dm | Em | F | G | Am | Bb | Ab | Eb | Fm |
| G | G | Am | Bm | C | D | Em | F | Eb | Bb | Cm |
| D | D | Em | F#m | G | A | Bm | C | Bb | F | Gm |
| A | A | Bm | C#m | D | E | F#m | G | F | C | Dm |
| E | E | F#m | G#m | A | B | C#m | D | C | G | Am |
| F | F | Gm | Am | Bb | C | Dm | Eb | Db | Ab | Bbm |
| Bb | Bb | Cm | Dm | Eb | F | Gm | Ab | Gb | Db | Ebm |
| Eb | Eb | Fm | Gm | Ab | Bb | Cm | Db | B（=C♭） | Gb | Abm |

| 短調のキー | i | ♭III | iv | v（または V） | ♭VI | ♭VII |
|---|---|---|---|---|---|---|
| Am | Am | C | Dm | Em（E） | F | G |
| Em | Em | G | Am | Bm（B） | C | D |
| Dm | Dm | F | Gm | Am（A） | Bb | C |
| Gm | Gm | Bb | Cm | Dm（D） | Eb | F |
| Bm | Bm | D | Em | F#m（F#） | G | A |
| F#m | F#m | A | Bm | C#m（C#） | D | E |
| Cm | Cm | Eb | Fm | Gm（G） | Ab | Bb |

### 和音の種類と性格（うちで読める種類だけ）

| 書き方 | 性格 | 使いどころ |
|---|---|---|
| 長3和音 `C` | 明るい・素直 | サビ・勝利 |
| 短3和音 `Am` | 暗い・切ない | Aメロ・悲しみ |
| `maj7` `Cmaj7` | 浮遊・おしゃれ・都会的 | バラード・ジャズ・R&B、サビの頭 |
| `m7` `Am7` | やわらかい短調 | Aメロ・ローファイ・ボサ |
| `7` `G7` | 引力・渋み | 解決直前、ブルース、副ドミナント |
| `sus4` `Gsus4` | 宙づり（4度がぶら下がる） | 解決の引き延ばし、和風、EDM |
| `sus2` `Csus2` | 開けた・透明 | イントロ、アルペジオ、和風、ダンジョン |
| `dim` `Bdim` | 不安・つなぎ | 経過（半音の橋）、ダンジョン、ボス |
| `aug` `Gaug` | ふしぎ・魔法・不安定 | 変身・魔法・ダンジョンの色づけ |

---

## 3. ジャンル別の進行の型

各表の「例」はそのまま `chords:` に書ける。★は「既存の A〜R と同系」。1コード＝1小節（`barsPerChord: 1`）で書いてあるが、2小節ずつにしてもよい。度数の矢印は「–」で書く。

### 3-1. ロック

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| ミクソリディアの揺れ★L | I–♭VII–IV–I | `E D A E`（E） | 長調のまま荒っぽい。リフの土台 |
| 開放の連続 | I–IV–♭VII–IV | `A D G D`（A） | ♭VII と IV の往復で広がる。平原・疾走 |
| 5度から落ちる | I–V–♭VII–IV | `A E G D`（A） | 下りながら広がる。サビ向き |
| 短調ロック★E | i–♭VI–♭III–♭VII | `Dm Bb F C`（Dm） | 重いが前向き。戦闘・疾走 |
| 借用ivで曇らせる★C | I–iii–IV–iv | `G Bm C Cm`（G） | 明るい曲の最後の1小節だけ曇る |
| 渋い締め | i–♭VII–iv–V7 | `Em D Am B7`（Em） | 長三和音のV7で強く締める。決意 |

### 3-2. パンク（速い・シンプル・勢い）

パワーコード（根音＋5度）は書式にないので、**長3・短3・sus2 で代用**。上の音が増えても、ギターは「5度だけ」で弾く編曲にできる。

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| 三大和音の折り返し | I–IV–V–IV | `G C D C`（G） | 最短で勢い。同じ形を4回転 |
| ♭VIIで跳ねる | I–♭VII–IV–V | `D C G A`（D） | 荒々しいのに明るい |
| IIIを長三和音にする | I–III–IV–V | `G B C D`（G） | B（長）が飛び込んで「叫ぶ」感じ |
| 青春の回り道 | I–IV–vi–V | `A D F#m E`（A） | 泣きと勢いの同居 |
| 短調パンク | i–♭III–iv–♭VI | `Em G Am C`（Em） | 暗い疾走。Aメロ向き |
| sus2の往復 | I–IV(sus2)–I–V | `A Dsus2 A E`（A） | 3度を抜いて骨太に聞かせる |

### 3-3. メタル

メタルの要は**短調・フリジア（♭II）・トライトーン（♭V）・半音下降**。長3和音で♭IIや♭Vを入れると、ぐっと暗くなる。

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| フリジアの引力 | i–♭II–i–♭VII | `Em F Em D`（Em） | ♭II→i の半音の引きずり。重く邪悪 |
| エオリアン下降 | i–♭VI–♭VII–i | `Dm Bb C Dm`（Dm） | 壮大・英雄的 |
| 三度の階段 | i–♭III–♭VII–♭VI | `Bm D A G`（Bm） | 持ち上げてから沈む |
| トライトーン | i–♭V–i–♭II | `Em Bb Em F`（Em） | 悪魔の音程。ボス前 |
| 下降の4音★E | i–♭VII–♭VI–V7 | `Gm F Eb D7`（Gm） | 最後のD7が強く引っぱる |
| ♭IIの入れ替え | i–♭VI–♭II–V7 | `Am F Bb E7`（Am） | ナポリ風。悲壮 |

### 3-4. ポップス

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| 上昇ベース | I–iii–IV–V | `Bb Dm Eb F`（Bb） | 根音が階段で上がる。期待が膨らむ |
| 4と5を遅らせる | I–IV–vi–V | `G C Em D`（G） | 王道の変形。最後がV（開く）で次の頭へ回りやすい |
| 循環 | I–vi–ii–V | `F Dm Gm C`（F） | 5度で順に進む。昔ながらの心地よさ |
| 下降の逆再生 | vi–V–IV–V | `Bm A G A`（D） | 短調の気配のまま明るく締まる |
| iiiを経由 | I–iii–vi–IV | `A C#m F#m D`（A） | 3度で滑る。穏やか |
| ♭VIIで始まる回遊 | I–♭VII–vi–IV | `C Bb Am F`（C） | 借用→vi→IVと降りる。ほろ苦い |

### 3-5. J-POPの「型」（一般的な名前で呼ばれているもの）

名前は日本の音楽解説でよく使われる通称。**度数の並びを借りるだけで、旋律・リズム・主音は必ず自作に**する。

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| 王道進行 | IV–V–iii–vi | `Fmaj7 G7 Em7 Am7`（C）／`Gmaj7 A7 F#m7 Bm7`（D） | 明るく上がってiiiで急に陰る「切なさ」。サビ向き。多用すると短調に聞こえるので、別のパートでIを鳴らす |
| 小室進行 | vi–IV–V–I | `C#m A B E`（E） | 短調始まりで長調の主和音に着地。劇的。ループしても繋がる |
| カノン進行 | I–V–vi–iii–IV–I–IV–V | `D A Bm F#m G D G A`（D） | 5度・2度・4度の動きだけでできた8コード。厳か・感動。終盤・エンディング |
| 丸サ型（IVmaj7→III7→vi7→I7） | IVmaj7–III7–vi7–I7 | `Cmaj7 B7 Em7 G7`（G） | 副ドミナントIII7が「半音で上がる緊張」を作る。おしゃれ。4コードで1周するとI7がIVへ引っぱり、ループがなめらか ※この型の度数は一般的な解説による（本調査では詳細ページを読み切れていない） |
| 4156進行 | IV–I–V–vi | `A E B C#m`（E） | 変終止でvi（静かな着地）。控えめな哀愁 |
| ドキドキ進行 | vi–iii–IV–V | `Dm Am Bb C`（F） | 根音が1歩ずつ上がる。B→サビの導入 |
| 王道進行・改 | IV–V–III–vi | `C D B Em`（G） | iiiをIII（長）に替える＝副ドミナント。緊張が一段上がる |

### 3-6. バラード

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| 下降ベース★B | I–V/7–vi–I/5–IV | `G D/F# Em G/D C`（G）※分数 | 低音が階段で下る。感動の定番 |
| 偽終止で止める★G | I–vi–IV–V7–vi | `C Am F G7 Am`（C） | 解決しないまま、続きを聴かせる |
| 一音ずつ曇る | I–Imaj7–IV–iv | `Eb Ebmaj7 Ab Abm`（Eb） | maj7で夢を見て、ivで現実に戻る |
| susで引き延ばす | vi–IV–I–Vsus4–V | `F#m D A Esus4 E`（A） | 解決の直前で1小節ためる |
| 壮大な締め | ♭VI–♭VII–I | `C D E`（E） | 長調の終わりに借用を2つ続けて、勝ち鬨 |
| 7thで流す | ii–V–I–IV（maj7版） | `Bbm7 Eb7 Abmaj7 Dbmaj7`（Ab） | ジャズ寄りのバラード。夜 |

### 3-7. ジャズ

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| ii–V–I | ii7–V7–Imaj7 | `Cm7 F7 Bbmaj7`（Bb） | 基本。すべての土台 |
| ターンアラウンド | Imaj7–VI7–ii7–V7 | `Cmaj7 A7 Dm7 G7`（C） | A7（副ドミナント）がii7を強く引く。曲末から頭へ |
| 裏コード★O | ii7–♭II7–Imaj7 | `Dm7 Db7 Cmaj7`（C） | G7の代わりにDb7。低音が半音で下りる |
| バックドア | iv7–♭VII7–Imaj7 | `Fm7 Bb7 Cmaj7`（C） | V→Iを使わず後ろ口から主音へ。柔らかい着地 |
| ii–Vの連鎖 | ii–V–(I)を5度ずつ下降 | `Em7 A7 Dm7 G7 Cmaj7`（C） | 小さな転調が連続する。ジャズの「流れ」 |
| 短調のii–V–i | ii°–V7–i | `Ddim G7 Cm7`（Cm） | ii°の代わりに `dim`（`m7b5` は読めない） |

### 3-8. ブルース（12小節＝12個のコードを並べる）

| 型 | 例（キーA） | 解説 |
|---|---|---|
| 基本の12小節 | `A A A A D D A A E D A E` | I×4 / IV×2, I×2 / V, IV, I, V |
| クイックチェンジ | `A D A A D D A A E D A E` | 2小節目だけIVに寄って戻る |
| 7th版（全部ドミナント） | `A7 D7 A7 A7 D7 D7 A7 A7 E7 D7 A7 E7` | 全部7thにすると「ブルースの音」になる |
| ジャズブルース | `A7 D7 A7 A7 D7 D7 A7 F#7 Bm7 E7 A7 E7` | 8小節目に F#7（VI7）、9〜10に ii–V |
| マイナーブルース | `Am Am Am Am Dm Dm Am Am F E7 Am E7` | 9小節目 ♭VI→10 V7 でなめらかに降りる |
| 8小節ブルース | `D D A A E D A E` | 前半4小節を省いた短い形（IV IV I I V IV I V） |

### 3-9. ファンク（解決しない・1〜2コード）

ファンクでは進行が主役ではなく、**リズムが主役**。コードは1〜2個で、拍の位置（どこでコードが変わるか）の方が大事。

| 型 | 例（キー） | 解説 |
|---|---|---|
| ドリアンの1コード | `Em7 Em7 A7 Em7`（Em） | i7が居座り、4小節目手前でだけ A7（IV7）が顔を出す |
| ii–Vの往復 | `Dm7 G7 Dm7 G7` | 解決しないii–V。ドリアンの旋律が乗る |
| I7とIV7の往復 | `E7 A7 E7 A7` | 全部ドミナント7th。ブルース色のファンク |
| 半音ずらし | `Am7 Bbm7 Am7 D7` | 上の半音のm7へ一瞬ずらして戻る（横滑り） |
| 低く居座る | `Gm7 Gm7 Gm7 C7`（Gm） | 3小節ためてC7で一撃 |

### 3-10. R&B・ネオソウル

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| 下降の7th | IVmaj7–iii7–ii7–Imaj7 | `Abmaj7 Gm7 Fm7 Ebmaj7`（Eb） | 7thの階段。とろける |
| ii–V–iii–vi | ii7–V7–iii7–vi7 | `Dm7 G7 Em7 Am7`（C） | Iを通らずviに着地。余韻 |
| 経過のdim | Imaj7–♯Idim–ii7–V7 | `Cmaj7 C#dim Dm7 G7`（C） | 半音で橋渡し。滑らか |
| 借用のm7 | Imaj7–IVmaj7–iv7–Imaj7 | `Dbmaj7 Gbmaj7 Gbm7 Dbmaj7`（Db） | maj7→m7の「同じ根音で色だけ曇る」 |
| 短調の連鎖 | i7–♭VII7–♭VImaj7–V7 | `Fm7 Eb7 Dbmaj7 C7`（Fm） | 順に降りてC7が引っぱる |
| 副ドミナントの挿入 | Imaj7–III7–vi7–ii7–V7 | `Gmaj7 B7 Em7 Am7 D7`（G） | B7が一瞬だけ別の調に連れ出す |

### 3-11. ボサノバ

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| ドミナントIIの寄り道 | Imaj7–II7–ii7–V7 | `Fmaj7 G7 Gm7 C7`（F） | II7（G7）が一瞬リディアン風に明るい |
| 短調の終止 | i7–ii°–V7–i7 | `Am7 Bdim E7 Am7`（Am） | 短調が基本。dimで代用 |
| 半音の下降ベース | Imaj7–VII7–♭VII7–vi7 | `Cmaj7 Bm7 Bb7 Am7`（C） | 低音が C–B–B♭–A と半音で降りる |
| ii–V–Iのキー移動 | ii–V–I→全音上のii–V–I | `Dm7 G7 Cmaj7 Em7 A7 Dmaj7` | ジャズ的な転調の連鎖 |
| 回し | Imaj7–vi7–ii7–V7–iii7–VI7–ii7–V7 | `Cmaj7 Am7 Dm7 G7 Em7 A7 Dm7 G7` | 8コードの循環。ゆったり流れる |

### 3-12. EDM（ダンス・トランス・フューチャーベース）

EDMは「短調の4コードを延々回す」ので、**ドロップ前後で変える**のが肝。

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| 短調の循環 | i–♭VI–♭III–♭VII | `F#m D A E`（F#m） | 定番の高揚。ビルドとサビ |
| 下降の往復 | i–♭VII–♭VI–♭VII | `Dm C Bb C` | 波のように上下。長く続けても飽きにくい |
| ビルド→ドロップ | ♭VI–♭VII–i–i | `Bb C Dm Dm`（Dm） | 上り詰めてiで1小節ためる |
| susでぼかす | i–♭VI（sus2）–♭III–♭VII（sus4） | `Em Csus2 G Dsus4`（Em） | 3度を消して浮遊。シンセ向き |
| 2コードの揺れ | i–♭VI | `Gm Eb Gm Eb` | ミニマル。落ち着いたパート |
| 7thの透明感 | ♭VImaj7–v7–i7–ivsus4 | `Abmaj7 Gm7 Cm7 Fsus4`（Cm） | フューチャーベース風のきれいな響き |

### 3-13. 民族・和風・異国

| 型 | 度数 | 例（キー） | 効果・使いどころ |
|---|---|---|---|
| ドリアン往復★K | i–IV | `Em A Em A`（Em） | 短調なのに6度が明るい。古い街・冒険 |
| フリジア | i–♭II | `Am Bb Am Bb`（Am） | 半音の引きずり。砂漠・敵地 |
| 和風のsus | I–IV–V（全部sus4）–I | `Csus4 Fsus4 Gsus4 C` | 3度を外すと、洋風の明暗がなくなる |
| 都節の風 | i–♭II–iv–i | `Am Bb Dm Am`（Am） | 都節音階 A–B♭–D–E–F の音で作る哀愁 |
| 律（明るい和風） | I–vi–ii–V–I | `D Bm Em A D`（D） | ペンタトニック的。祭り・里 |
| ミクソリディア★L | I–♭VII–IV–I | `D C G D`（D） | 土の匂い。旅・平原 |
| アンダルシア | i–♭VII–♭VI–V7 | `Am G F E7`（Am） | 下降4音。情熱・決闘・砂漠 |
| 琉球の風 | Imaj7–IVsus2–iii–IVsus2 | `Cmaj7 Fsus2 Em Fsus2` | 2度と6度の音を避ける音階。sus2が合う |

---

## 4. ゲーム音楽の場面別の進行

調査で確かめられたこと（要約）: RPGの音楽は、**町・フィールド・ダンジョン・戦闘**の4種で性格が分かれる。町は安定した形（言い切るカデンツ）、フィールドは前へ進む動きのある形、ダンジョンは機能がはっきりしない（静的・曖昧）で反復が多い。うちの設計には次のように落とす。

| 場面 | 基本の方針 | 例（キー） | 補足 |
|---|---|---|---|
| フィールド（明るい） | 5度の往復＋♭VII。解決を先送りして歩く | `G D C G`（G） | I–V–IV–I。前へ進む足取り |
| フィールド（旅・風） | I–♭VII–IV–I | `A D A G`（A） | 風の流れる感じ。ミクソリディア |
| フィールド（空・乗り物） | リディアン（I–II） | `Cmaj7 D Cmaj7 Em7`（C） | Dmaj系のII（D）が空へ抜ける |
| フィールド（広がり） | I–iii–IV–V | `F Am Bb C`（F） | 上昇ベース。地平線 |
| 町（穏やか） | 循環で言い切る | `G Em Am D`（G）／`F Bb F C7`（F） | ふつうに終止してよい（町は「安定」が仕事） |
| 町（古い・異国） | ドリアン | `Em A Em Bm`（Em） | i–IV–v |
| 町（夜・酒場） | ii–V–I＋副ドミナント | `Dm7 G7 Cmaj7 A7`（C） | A7がDm7へ戻す。ループになる |
| 町（祭り） | I–♭VII–IV–I | `A G D A`（A） | 跳ねるリズムと合わせる |
| 宿屋・休息 | 7thの循環 | `Cmaj7 Am7 Dm7 G7`（C） | のんびり |
| ダンジョン（不安） | 半音の往復 | `Em F Em F`（Em） | ♭IIを往復。機能がない＝足場が揺れる |
| ダンジョン（呪い） | dimを往復 | `Dm Edim Dm Edim` | ii°とiの往復 |
| ダンジョン（魔法） | aug（V+）を挟む | `Cm Gaug Cm Fm`（Cm） | Gaugが宙に浮いた「V」になる |
| ダンジョン（気配） | 半音ずらしとトライトーン | `Em F Em Bb`（Em） | 悪い予感。F→Bb が不穏 |
| 戦闘（疾走） | 短調の循環 | `Em C D Em`（Em）／`Gm Bb Eb F`（Gm） | 8分の刻みと合う |
| 戦闘（悲壮） | アンダルシア | `Dm C Bb A7`（Dm） | 下降→A7で引き戻す |
| 戦闘（激しい） | ♭II・♭VII | `Bm C A Bm`（Bm） | 半音のぶつかり |
| 戦闘（決意） | iv・V7で締める | `Cm Ab Fm G7`（Cm） | 一周の終わりにG7 |
| ボス（威圧） | トライトーン＋V7 | `Dm Ab Dm A7`（Dm） | A♭がD–Aの真反対 |
| ボス（影） | ♭II＋dim | `Cm Db Gdim G7`（Cm） | 不安→V7で吐き出す |
| ボス（壮大） | ♭VIと♭IIIの階段 | `Em C G B7`（Em） | 大きな足取り |
| ボス（重く） | iv→V7 | `Fm Db Bbm C7`（Fm） | ♭VI–iv–V7 |
| 勝利 | ♭VII–IV–I | `C Bb F C`（C） | 凱旋の開放 |
| タイトル | sus2＋アルペジオ | `Csus2 G Am Fsus2`（C） | 明暗を決めすぎず、想像に預ける |
| ゲームオーバー | 短調の言い切り | `Dm Gm Dm A7`（Dm） | i–iv–i–V7 の素朴な暗さ |
| エンディング | カノン型＋偽終止 | `D A Bm F#m G D G A`（D） | 最後にVの次をviにして余韻を残す |

---

## 5. セクションごとの変え方（Aメロ／Bメロ／サビ／間奏／アウトロ）

### 5-1. 役割の違い（調査のまとめ）

- **Aメロ（詞）**: 進行は「ゆるく旅をする」。主和音は匂わせる程度で、ときどき借用・副ドミナントも混ぜてよい。**弱くて曖昧**な側。
- **Bメロ（準備）**: サビへ向かう**上昇ベース**・ドミナントで終わる（半終止）・ドミナントの上でペダル。ここで「溜めて」サビで放つ。
- **サビ**: **短く、はっきり、直線的**。進行は4〜8コードで、機能がわかりやすい。始まりのコードをAメロと変える（Aメロ Iから、サビ IVから）。**コードを長くする（1小節→2小節）だけでも感動が増す**。
- **間奏**: 2コード往復・ペダル・ブルースの形・遠いキー。ドラムを抜く。
- **ブリッジ（Cメロ）**: **主和音から始めない**。逆の調性（長調の曲なら平行短調）へ寄り道して、後半でピボット和音で戻る。**最後のサビの前に置く**（うちの arrangement ガイドと同じ）。
- **アウトロ**: 解決を長くする（IV→I の「アーメン終止」）、偽終止で止める、冒頭のコードに戻る（ループBGM向き）。

### 5-2. 切り替えの道具（表）

| 手 | やり方 | 例 |
|---|---|---|
| 始まりを変える | Aメロ I 始まり → サビ IV 始まり | A: `C Am ...` / サビ: `F G ...` |
| コードの長さを変える | A: 1小節、サビ: 2小節（コードを繰り返す） | サビの `F F G G Am Am G G` |
| 上昇ベースで溜める | Bメロで根音を1歩ずつ上げてVで止まる | `Em7 Am7 Cmaj7 D` |
| ドミナント・ペダル | Bメロで低音をVに固定 | `C/G Dm/G G7` ※分数 |
| 借用を入れる | サビの終わりにivや♭VI | `...G Gm C`（長調でivを一瞬） |
| 副ドミナント | Aメロの終わりに V7/vi、サビの頭に V7/IV | `... E7 Am` |
| 偽終止 | 1周目のサビはV→vi、2周目でV→I | `G7 Am` → `G7 C` |
| 平行調へ | ブリッジは長→短 | C の曲なら `Am Dm F E7` |
| 半拍・倍速 | 最後のサビでコードの回転を倍にする | 2小節→1小節ずつ |
| 全休止 | 最後のサビ前に1小節止める | 全パート R |

### 5-3. 通しの設計例（そのまま `chords:` に書ける。`barsPerChord: 1`、`repeats: 1`、`sections` を併用）

**例1 ポップな曲（G・24小節）** — 導入4 / Aメロ8 / Bメロ4 / サビ8

```
chords: Gsus2 Gsus2 Cmaj7 Cmaj7 G Bm7 Cmaj7 G Em7 Am7 Bm7 D Em7 Am7 Cmaj7 D Cmaj7 D Bm7 Em7 Cmaj7 D G Gsus4
sections: intro 4 / verse 8 / pre 4 / chorus 8
```

- 導入はsus2で開けておく（主和音をまだ確定しない）。
- Aメロは I 始まり、4小節目でI、後半は vi へ進み、Dで半終止。
- Bメロは `Em7 Am7 Cmaj7 D` と根音が上がり、最後のDで止める。
- サビは **IV（Cmaj7）始まり**で、Aメロと入り口を変える。最後は Gsus4 で宙づりにして、ループ時にイントロへ戻す。

**例2 戦闘曲（Em・24小節）** — 導入4 / Aメロ8 / Bメロ4 / サビ8

```
chords: Em Em Em Bb Em C D Em Em C Bm B7 Am C Am B7 C D Em G C D B7 Em
```

- 導入は主和音の居座りに、最後の1小節だけ Bb（トライトーン）で不穏にして頭へ。
- Aメロの後半は Bm → B7 でVの準備。
- Bメロは Am（iv）の上で C へ上がって Am、B7 で止める。
- サビは ♭VI（C）始まり、Em G（i–♭III）で一度明るく持ち上げて、B7→Em で閉じる。

---

## 6. 転調の技法（表）

転調は**1曲に1回**が基本。準備（V7・全休止・フィル）と、歌える（弾ける）音域を確認する。

| 技法 | 手順 | 例 | 効果 | 向く場面 |
|---|---|---|---|---|
| 直接・半音上 | 最後のコードの次の小節で、そのまま半音上の調へ | `Am F C G Bbm Gb Db Ab`（Am→B♭m） | 勢いが跳ねる。定番 | 最後のサビ |
| 直接・全音上 | 全音上の調へ飛ぶ | `C Am F G D Bm G A`（C→D） | 半音より少し大きく開く | 終盤 |
| 新キーのV7を挟む | 新しい主音のV7を、行き先の直前に置く | `C F G7 Ab7 Db Gb Ab7 Db`（C→D♭） | 準備ありで自然。Ab7 が橋 | 静かな転調 |
| ピボット（共通和音） | 両方の調に属する和音を橋にする | `C F Am D7 G C`（C→G。Am が橋） | 気づかないほど滑らか | 中盤、ブリッジ |
| 平行調（長↔短） | 同じ音で主音だけ変える | `C F G C Am Dm E7 Am` | 明→暗が自然 | A→B、ブリッジ |
| 同主調（C→Cm） | 主音は同じで3度を下げる | `C F G C Cm Fm G Cm` | 運命が暗転 | 悲劇への落下 |
| 小3度上 | 3度上へ飛ぶ | `C Am F G Eb Cm Ab Bb` | 大きな跳躍。世界が開く | 終盤、エンディング |
| dimで橋を作る | 新キーの導音のdimを経由 | `C F G C C#dim Dm Gm A7 Dm`（C→Dm） | 半音で引き上げる | 転調を目立たせたいとき |
| 上げる→元に戻す | 一時的に半音上げて戻る | `C F G7 Ab Db Eb7 Ab G7 C` | 一瞬だけ別世界 | 間奏 |
| ii–V–Iの連鎖 | ii–V–I を全音ずつ上げる | `Dm7 G7 Cmaj7 Em7 A7 Dmaj7` | ジャズ的に連続転調 | ボサ・夜の街 |

- **下げる転調**は元気がなくなるので、静かな場面（回想・終わり）に限る。
- **歌い手の音域**: 上げすぎると届かない。ゲームBGMでも、旋律の最高音が高音域の限界（A5以上）に届いたら半音上げをやめる。
- **ループBGM**: 転調した曲はループの継ぎ目で元の調に戻る橋が要る（最後のコードを V7 や ♭VII にして、頭へつなぐ）。

---

## 7. メロディとコードの関係

### 7-1. コードトーン・経過音・テンション

- **強拍・長い音**は、コードの構成音（根音・3度・5度・7度）に置く。弱拍で、**スケールの音**を経過音・刺繍音（上下に寄って戻る）としてつなぐ。コード外の音の割合は強拍で2割以下が目安（music-knowledge と同じ）。
- **先取音**（次のコードの音を半拍早く鳴らす）と**掛留音**（前のコードの音を引き伸ばしてからずらす）は、コードが変わる所の「なめらかさ」を作る。
- **テンション**（9度・11度・13度など）は、コードの性質に合うものだけ。目安:
  - `maj7`: 9度、♯11度（リディアンの色）、13度。11度（=4度）は半音ぶつかるので避ける。
  - `m7`: 9度、11度。
  - `7`（ドミナント）: 9度、13度。♭9・♯9は、短調へ向かうとき限定。
  - メロディの音がテンション（9度など）なら、コード側に同じ音を足さない（ぶつかる）。

### 7-2. アヴォイドノート（長調の7和音の上で気をつける音）

アヴォイドノート＝**コードトーンの半音上にある音階内の音**。長く伸ばすと、和音の性格がこわれる。短い経過音や弱拍ならよい。

| キーC | コード | 避ける音 | 理由 |
|---|---|---|---|
| I | Cmaj7 | F（4度） | 3度（E）の半音上でぶつかる |
| ii | Dm7 | ほぼなし | ドリアン的に13度（B）も使える |
| iii | Em7 | F（♭9）、C（♭13） | 根音・5度の半音上 |
| IV | Fmaj7 | ほぼなし | ♯11（B）はリディアン風に使える |
| V | G7 | C（4度） | 3度（B）の半音上でぶつかる |
| vi | Am7 | F（♭13） | 5度（E）の半音上 |
| vii° | Bdim | C（♭9）、F（♭5と同音） | 根音の半音上 |

- 使うルール: **「長く」「強拍で」「最高音で」アヴォイドを使わない**。どうしても使うなら、すぐに半音下の構成音に解決する。
- 借用コード上は、借用したモードの音階で見る（たとえば ♭VI（Ab）の上では、元の調のC長調の音を使うなら B と D は半音ぶつかる）。

### 7-3. ベースラインとの関係

- 基本は**根音**。変えどころは、コードの変わり目の手前で**次の根音の半音下／上から入る**（経過音）。
- **転回形（スラッシュ）でベースが歩く**と、同じコードでも別物に聞こえる（例: C–C/E–F–F/A–G）。
- **ペダル**: 低音を同じ音に固定。和音を替えても不安が増して、解決で一気に解ける。
- **クリシェ**: 低音または内声が半音で下がる（Am–Am/G#–Am/G–Am/F#）。うちの書式で和音名を変えるなら、`Am` と `Am7` の往復＋ベースの経過音で近づけられる。
- 旋律とベースは**反行**（一方が上がるとき一方が下がる）にすると、広がる。同方向（平行）に動く5度・8度は避ける。

### 7-4. ボイシングとボイスリーディング（自動伴奏の内側で起きていること）

- ピアノなどの和音は、**共通音を同じ声部に残し、ほかの声部は2度や3度までの小さな動き**にすると滑らか（うちの `voiceLead` 関数がこの原則で動く）。
- 3度と7度（ガイドトーン）がコードの色を決める。7thコードの連続では、3度と7度が半音または同音で次へつながるように並べる。
- **進行が飛ぶとき（根音が大きく動く）でも、上の声部は近くに置く**と、聞き手は「近い」と感じる。
- 声部が多すぎる（5〜6個）と濁るので、低音域の3度は避ける（根音と5度だけにする）。

---

## 8. うちの機能への対応表

| 理論の道具 | うちの書式で書く方法 | 現状の制約・注意 |
|---|---|---|
| ダイアトニックの置き換え | 度数→コード名の早見（2節）で書く | なし |
| 副ドミナント | `E7 Am`、`A7 Dm7`（長三和音＋7）。`7` で書く | なし |
| 借用和音 | `Fm`（iv）、`Bb`（♭VII）、`Ab`（♭VI） | なし |
| 裏コード | `Db7`（G7の代わり） | なし |
| ツーファイブ | `Dm7 G7 Cmaj7` | `m7b5` は読めない → `dim` か `m7` で代用 |
| 偽終止 | `G7 Am` | なし |
| ペダルポイント | 低音固定の分数コード | **分数コードは、読み込みで止まる疑いがある**（下の注） |
| クリシェ | `Am Am7` の往復 | `Am(maj7)` は読めない |
| 転回形・下降ベース | `C/E` など | 同上 |
| sus・dim・aug | `Gsus4` `Bdim` `Eaug` | 読める。サウンドは「根音＋3和音」 |
| 6th・9th・add9・5（パワーコード） | — | **読めない**（`QUALITY` に無い） |
| 1コードの長さを不揃いに | — | `barsPerChord` は全体で1か2のみ。コードを並べて小節数を変えるしかない |
| セクションごとに進行を変える | 全体の `chords` を通して書く（`repeats: 1`） | `sections` はアレンジ（音の出し入れ）だけで、進行は変えない |
| 転調 | 単に別のキーのコードを書く | 旋律パート（`parts`）の音も手で書き直す。チェッカーは度数が崩れる |
| 進行の似かよいチェック | `song.mjs` の build 警告 | 回して書くと別物扱い（下の注） |

注（確認ずみのこと）:
- `src/audio/newsong.ts` の `parseChord` は `^([A-G])([#b]?)(.*)$` で品質を完全一致で引くため、`G/B` は品質が `/B` となって見つからず **「読めないコードがあります」で止まる**はず（コードを読んで推定。実際に走らせての確認まではしていない）。ガイドに書いてある「分数コード（G/B）」が使えるかは、必ず `song.mjs` で試すこと。
- `chord-variety.mjs` は、最初のコードを主音として度数の並びを作り、4コード連続の一致で比べる。実際に走らせて確認: `C G Am F …` と `Am F C G …`（同じ4コードの回し方違い）は一致率 0 になる。つまり「王道を回して書き直す」とすり抜ける。

---

## 9. 取り入れる提案（実装できる単位で）

優先度は、効果と手間の釣り合いで並べた。

1. **分数コードを読めるようにする（小・先にやる）**
   `newsong.ts` の `parseChord` で、`/` 以降を切り出して「低音」にする。ベース・ピアノの最低音をその音にする。`chord-variety.mjs` の `parseChord` も、低音を `bass` として返す。これでガイドの B・H レシピ（下降ベース・ペダル）が書ける。テストは `G/B` が読めること、低音が B になること。

2. **和音の種類を増やす（小）**
   `QUALITY` に `6`・`m6`・`9`・`add9`・`5`・`m7b5`（別名 `m7-5`）・`7sus4`・`mmaj7`（`m(maj7)` の別名）を足す。構成音は `[0,4,7,9]` `[0,3,7,9]` `[0,4,7,10,14]` `[0,4,7,14]` `[0,7]`（パワーコード）`[0,3,6,10]` `[0,5,7,10]` `[0,3,7,11]`。ジャズ・R&B・ボサ・パンクの型が、そのまま書ける。`AI_SONG_GUIDE` の使える一覧も更新。

3. **コードごとの長さ指定（中）**
   `Am*2`（2小節）、`Am/2`（半小節）などの書き方を足す。`buildNewSong` が小節に展開するときに数える。サビだけコードを長くする、ブリッジで回転を倍にする、といった手が使える（5節の道具）。チェッカーでは繰り返しを1つにまとめるので影響は小さい。

4. **セクション別の進行（中）**
   `sections` と対応する `sectionChords: { verse: "...", chorus: "..." }` を足す。省略すると今の動き。指定すれば、各セクションの小節数に合わせて進行を繰り返して並べる。これで「Aメロ I 始まり／サビ IV 始まり」が、通しで書かなくても作れる。

5. **チェッカーを「回して書いても」見つける（中）**
   度数の並びを「主音からの度数」でなく「**前のコードからの根音の移動量＋長短**」に直し、**ループとして回転も比べる**（並びを2周つなげて4コード単位で一致を数える）。これで `C G Am F` と `Am F C G` を同じと判定できる。同時に、**転調しても度数が崩れない**ようにできる（移動量は移調しても同じ）。

6. **チェッカーに「型ラベル」を足す（小〜中）**
   進行を既知の型（王道・小室・カノン・循環・アンダルシア・12小節ブルースなど）に当てて、警告に型名を出す（「この進行は『王道進行』の形です。直前の曲も同じ型です」）。型の定義は `docs/sound/data/chord-recipes.json`（新規）にまとめ、チェッカーと作曲前の選択ツールが同じデータを読む。

7. **進行の選択ツール（中）**
   `tools/composer/chord-pick.mjs --scene battle --avoid-last 3 --key random` のような小さな道具を作る。場面（フィールド・戦闘・ボスなど）とジャンルから、データの型を絞り、直近の曲と違うものを選び、C 以外のキーに移して、候補を3つ出す。「毎回 Am F C G になる」を作曲の前で止められる。

8. **最後のサビの転調オプション（中）**
   `modulate: { atBar: 17, semitones: 1 }` を足し、`atBar` 以降のコードと**旋律パートの音名**を指定の半音数だけ上げる（音名は文字列なので、移調は機械的にできる）。ドラムは動かさない。ガイドが何度も勧めている「最後のサビの半音上げ」を、手で書き直さずにできる。

9. **アヴォイドノート警告（中〜大）**
   build 時に、旋律パートの「強拍または1拍以上の音」が、そのときのコードの**構成音の半音上にある音階内の音**なら警告する（music-knowledge 14節の「強拍のコード外音の割合」と同じ系統のチェック）。警告文は「3小節目の強拍の F は Cmaj7 とぶつかります。E か G に」のように、小節・音・直し方を出す。

10. **ループ末尾の変化（小）**
    `loopTail: "deceptive" | "dominant"` のような指定で、ループの最終小節を V7 や vi に置き換えて、頭へのつなぎを滑らかにする（偽終止で次の周へ続ける）。BGMのループに向く小さな工夫。

---

## 10. 参考にした情報源

本文はすべて自分の言葉で書き直した。考え方・用語・事実関係を確かめるために読んだページ。

機能和声・代理・終止
1. [Learn Jazz Standards: 機能和声（T/SD/D、代理）](https://www.learnjazzstandards.com/blog/functional-harmony/)
2. [Music Theory Practice: 副ドミナントの解説](https://music-theory-practice.com/guides/secondary-dominants-explained)
3. [Secrets of Songwriting: 偽終止で進行をおもしろくする](https://www.secretsofsongwriting.com/2017/10/18/using-deceptive-cadences-to-make-chord-progressions-more-interesting/)
4. [The Jazz Piano Site: ii–V の代理（裏コード・バックドア）](https://www.thejazzpianosite.com/jazz-piano-lessons/jazz-reharmonization/ii-v-substitution/)
5. [FaChords: 借用和音の例](https://www.fachords.com/borrowed-chords/)
6. [guitar.samesound.ru: ♭VII–IV–I のロック的終止](https://guitar.samesound.ru/en/reference/cadences/bvii-iv-i)
7. [The Jazz Piano Site: ラインクリシェ](https://www.thejazzpianosite.com/jazz-piano-lessons/jazz-chord-progressions/line-cliches/)
8. [Secrets of Songwriting: ペダルポイントの力](https://www.secretsofsongwriting.com/2013/10/24/chord-progressions-and-the-power-of-the-pedal-point/)
9. [Music Theory for Guitar: クロマティック・メディアント（映画的進行）](https://www.musictheoryforguitar.com/Chromatic-Mediant-Progressions-Guitar.html)
10. [Wikipedia: アンダルシア終止](https://en.wikipedia.org/wiki/Andalusian_cadence)

ジャンル別
11. [Musiversal: ロックの定番進行](https://musiversal.com/blog/rock-chord-progressions)
12. [Musiversal: フリジアン（メタル・フラメンコ・映画）](https://musiversal.com/blog/master-phrygian-mode)
13. [Premier Guitar: ブルース進行の基本と変形](https://www.premierguitar.com/style-guide-essential-blues-progressions)
14. [Happy Bluesman: 12小節ブルースのよくある変形](https://happybluesman.com/common-variations-12-bar-blues/)
15. [eMastered: ボサノバのコード進行](https://emastered.com/blog/bossa-nova-chord-progressions)
16. [Piano With Jonny: ボサノバ（ジョビン流）の進行の分析](https://pianowithjonny.com/piano-lessons/the-jobim-chord-progression/)
17. [eMastered: ネオソウル／R&Bの進行](https://emastered.com/blog/neo-soul-chord-progressions)
18. [Ethan Hein: グルーヴ・ハーモニー（静的な和声・モード往復）](https://ethanhein.substack.com/p/groove-harmony)
19. [No Treble: ファンクのドリアン・ii–V ヴァンプ](https://www.notreble.com/?p=110686)
20. [UtaTen: J-POPのコード進行（カノン・王道・小室ほか）](https://utaten.com/live/?p=10660)
21. [サウンドハウス: 王道進行などJ-POPの型](https://www.soundhouse.co.jp/contents/staff-blog/index?post=3461)
22. [Wikipedia: 王道進行（Royal road progression）](https://en.wikipedia.org/wiki/Royal_road_progression)
23. [Tetsu7017: 和風曲の音階とコード付け](https://www.tetsu7017.com/blog/hoto-create-japanese-music-cubase/)

ゲーム音楽
24. [Rutgers 博士論文要旨: RPGの町・フィールド・戦闘の音楽](https://rucore.libraries.rutgers.edu/rutgers-lib/62986/record)
25. [NACVGM 2020 の発表概要: JRPGの楽曲形式と場面](https://www.theunofficialconventionarchive.com/nacvgm-2020-musical-form-and-gameplay-context-in-the-japanese-role-playing-game/)
26. [Hooktheory: ゲーム曲の楽譜サイト（構成の確認のみ）](https://www.hooktheory.com/theorytab/view/nobuo-uematsu/final-fantasy---battle)

メロディ・声部・アヴォイド
27. [Sleepfreaks DTM: アヴォイドノート](https://sleepfreaks-dtm.com/en/music-theory-beginner/avoid-note)
28. [Berklee Online: ボイスリーディングの原則](https://online.berklee.edu/takenote/voice-leading-paradigms-for-harmony-in-music-composition/)

セクションごとの変え方
29. [Secrets of Songwriting: ブリッジのコードは何をすべきか](https://www.secretsofsongwriting.com/2013/01/08/what-should-chords-in-a-songs-bridge-do/)
30. [Secrets of Songwriting: 詞・サビ・ブリッジの和声の違い](https://www.secretsofsongwriting.com/2012/12/10/comparing-verse-and-bridge-song-sections/)
31. [Secrets of Songwriting: 詞とサビで同じ進行でも対比をつける](https://www.secretsofsongwriting.com/2019/08/13/an-idea-for-songs-that-use-the-same-chord-progression-for-verse-and-chorus/)
32. [American Songwriter: セクションの対比（旋律・和声・リズム）](https://americansongwriter.com/creating-a-standout-chorus-use-changes-and-variations-in-your-theme/)

転調
33. [Fresno State: 転調の種類（直接・共通音・共通和音・半音階）](https://zimmer.fresnostate.edu/~sasanr/Music/Music-Theory/Modulation.htm)
34. [Planetary Group: 半音／全音上げの3つの方法](https://planetarygroup.com/modulating-songs-up-a-key-three-ways/)
35. [Orphiq: 転調の種類・使う音程・使いどころ](https://orphiq.com/resources/what-is-a-key-change)
36. [Splice: 転調の技法と感情の効果](https://splice.com/blog/what-is-modulation-in-music/)

既存文書が参考にしていた先（`chord-variety-guide.md` 冒頭）
37. [Secrets of Songwriting: 定番進行をおもしろくする5つの案](https://www.secretsofsongwriting.com/2021/06/11/making-standard-chord-progressions-more-interesting-try-these-five-ideas/)
38. [Learn Jazz Standards: 借用和音](https://www.learnjazzstandards.com/blog/modal-interchange/)
39. [Yamaha: ギタリストのコード代理ガイド2](https://hub.yamaha.com/guitars/g-how-to/a-guitaristss-guide-to-chord-substitutions-part-2-beyond-diatonic/)
40. [eMastered: 映画音楽のコード進行](https://emastered.com/ja/blog/cinematic-chord-progressions)

読めなかった（本文を取れなかった）ページ: ニコニコ大百科「小室進行」、Samplefocus・Violet Recording の EDM／R&B 記事（取得制限）。EDM の型は、一般的な理論（短調の循環・往復・ビルドとドロップ）から自分で組んだもので、出典の文章に頼っていない。

---

## 11. 実装状況（2026-10-11）

9節の提案10個のうち、10個とも何らかの形で入れた（一部は書式を変えている）。

| 提案 | 状態 | 入れたもの・場所 |
|---|---|---|
| 1 分数コード | 入れた | 作曲ソフト側（`newsong.ts` の `parseChord`）は先に対応ずみ。**今回は点検側**を直した: `chord-variety.mjs` の `parseChord` が低音（`bass`）を返す、`score-lib.mjs` の `chordPcs` が低音を和音の音に含める（8節の注「読み込みで止まる疑い」「度数が崩れる」は、もう当てはまらない） |
| 2 和音の種類 | 一部 | `newsong.ts` で 6・m6・9・maj9・m9・add9・madd9・m7b5（`m7(b5)`）・dim7・7sus4・m(maj7) は読める。**`5`（パワーコード）・`m7-5`・`mmaj7` は読めないまま**（`newsong.ts` は別の作業が同時に変更しているため触っていない）。点検側（`chord-variety.mjs`・`score-lib.mjs`）は m7b5・mmaj7・6・9・add9 を読む |
| 3 コードごとの長さ | 入れた（書式を変更） | `chords` に `Am*2`（2小節）と書く。**半小節（`Am/2`）は入れていない**（`G/B` の分数コードの書式とぶつかるため。小節の単位でだけ数える）。`src/audio/song-plan.ts` の `prepareSong` が、1小節1コードの形に展開してから `buildNewSong` に渡す。`barsPerChord` と混ぜてよい（`*N` が優先） |
| 4 セクション別の進行 | 入れた | `sectionChords: { "verse": "Em C G D", "chorus": "C G Am*2 D", "verse2": "Em D" }`。`sections` を配列で書いたときだけ効く（自動の `"auto"` は小節数が先に決まらないため）。各セクションの進行は、そのセクションの小節数に合わせて繰り返す／切る。同じ種類の2回目は `verse2`・`chorus2` のキーで別に指定でき、無ければ `verse` を使う。曲の長さは sections の合計になるので `repeats` は使われない |
| 5 回して書いても見つける | 入れた | `chord-variety.mjs` の `signature` を、**「前のコードからの根音の移動量＋長短」の輪（ループ）**にした。移調しても、回して書いても（`C G Am F` と `Am F C G`）一致率 100%。繰り返して書いた進行は最小の1周にまとめる。調を主音からの度数で比べる代わりに、移動量で比べるので、主音の推定がいらない（テストあり） |
| 6 型ラベル | 入れた | `docs/sound/data/chord-recipes.json`（46の型。度数・長短・場面・使いすぎ注意のフラグ）。`chord-variety.mjs` の `recipeOf` が進行から型を当て、警告に型名を出す（「王道」など使いすぎ注意の型、他の曲と同じ型）。回転しただけの同じ型は1つにまとめた |
| 7 進行の選択ツール | 入れた | `node tools/composer/chord-pick.mjs --scene battle --avoid-last 3 --key random --count 3 [--seed N] [--last 曲名,..]`。場面に合い、直近の曲と違う型を選び、C 以外の主音に移して、コード名で出す。使いすぎ注意の型は `--allow-overused` を付けたときだけ |
| 8 後半の転調 | 入れた | `modulate: { "atBar": 17, "semitones": 1 }`。`atBar`（1から数える）以降のコードと、ドラム以外のパートの音名を移す（パートは曲の長さまで展開してから移すので、短い型を繰り返しているパートも途中から上がる）。ドラム（タムの音名も）は動かさない。`ai-song.ts` の `AI_SONG_SCHEMA` と `AI_SONG_GUIDE` に追記 |
| 9 アヴォイドノート警告 | 入れた | `score-check.mjs --facts` が、小節ごとに「強拍（1拍目・3拍目）か1拍以上の音が、和音の構成音の半音上にある音階内の音」を出し、近い構成音を2つ直し方として添える。`build` の注意にも件数が出る（`tools/composer/workflow-check.mjs`）。`song-check.ts`（TypeScript 側）は触っていない |
| 10 ループ末尾 | 入れた | `loopTail: "dominant"`（最後の小節を V7）／`"deceptive"`（長調は vi、短調は ♭VI）。転調と併用すると、転調後の調の V7 になる |

使い方の例（すべて同じ曲に書ける）
```json
"chords": "Em Cmaj7*2 G/B D", "sections": [{"kind":"verse","bars":8},{"kind":"chorus","bars":8}],
"sectionChords": { "verse": "Em Cmaj7*2 G/B", "chorus": "C G Am*2 D" },
"modulate": { "atBar": 13, "semitones": 2 }, "loopTail": "dominant"
```
注意: これらの書式は `aiSongToScore` の最初で、ふつうの形（`chords` を1小節1コードで並べる、`barsPerChord: 1`、`repeats: 1`）に直される。ゲームに登録される曲（`sunshine-song.json`）は直したあとの楽譜なので、再生側の変更はいらない。
