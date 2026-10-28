# ケルト・フルート曲の作り方 — 勉強ノート（2026-10-28）

旭さんの「正直このままじゃつまらない曲になる」を受けて、作り方を根本から見直すために調べたこと。
三つに分けて調べた（①笛の装飾と歌い方 ②伝統曲の形とリズム ③編曲・曲の流れ）。数値のうち【推定】は資料をもとにした初期値で、耳で確かめて直す。
**既存の曲の旋律は写さない。型（形・リズム・装飾の決まり）だけを学ぶ。**

## A. これまでの曲がつまらなかった理由
1. 全曲が同じ型（始まり→歌1→歌2→山→終わり、1小節1和音、4小節ごとに「4分で動いて最後にのばして休む」）
2. 旋律に動機（覚えられる形）がなく、育てていない（音階歩きだけ）
3. 全部 4/4・4分音符。リズムの個性がない
4. ケルトの笛の装飾（cut・tap・roll・cran・slide）がない
5. 楽器の出入り・転調・B部分の対比がなく、厚みが最初から最後まで同じ

## B. 笛の装飾と歌い方（①）
- cut：主音の頭に、2〜3度上の音を一瞬（実装 20〜40ms・主音の 60〜80% の強さ）。主音は拍ちょうど。使う所＝同じ音が続く区切り／進行で着いた音の頭／長い音の途中（拍の分割点）
- tap（strike）：ほぼ2度下を一瞬。下がって長い音に着地するときに。低い D には使えない
- ロングロール：付点4分を8分×3に。主音・(cut)主音・(tap)主音＝「主・上・主・下・主」。ショートロール：8分×2（cut→tap）。密度＝リール2小節に1回、ジグ1〜2小節に1回、同じ小節に2つ入れない
- cran：低い D に、3度・4度・5度上の cut を 25〜35ms ずつ3回
- slide：下から 1〜2 半音すべり込む（80〜200ms）。エアの入り・強調したい長い音
- 3連符：8分×2 の時間に3音（上行・下行・回り込み）
- 避けること：入れすぎ、拍の前に出す装飾（クラシックの前打音）、拍やはずみを崩すこと
- スロー・エア：感情の山（節の終わり）で延ばす（最高音・最後の音・強拍の付点音を 1.2〜1.6 倍）、経過音は短く、2〜4小節ごとに 150〜400ms の間、装飾は少なく簡素に。ビブラートは長い音（0.8 秒以上）だけ、遅れて始め、浅く、1フレーズ1〜2回まで。長い音は少し膨らんで抜ける
- ダンス曲：基本はスラー。区切りは cut/tap と喉の区切り。リールの4つ組は 1番目が最も長く強く、3番目が次（長短 54:46〜58:42）。ジグの3つ組は 38:28:34 くらい。ホーンパイプは 62:38〜67:33。強拍 +1.5〜3dB

## C. 伝統曲の形とリズム（②）
| 種類 | 拍子・速さ | 1小節の型 | 形 |
|---|---|---|---|
| スロー・エア | 自由（下敷き ♩50–70） | 長い音と装飾 | AABA。B（3行目）で上のオクターブへ |
| ダブル・ジグ | 6/8・付点4分 100–110 | 8 8 8｜8 8 8、4 8 8 8 8、8 8 8 4 8 | 8小節×2部 AABB。終止 8 8 8 4. か 4. 4. |
| スライド | 12/8 | 4 8 4 8 | 4小節の部分 |
| スリップ・ジグ | 9/8 | 8 8 8×3、4 8 4 8 4. | AABB |
| リール | 2/2・2分 90–120 | 8分×8（4つ組2つ） | AABB 57.5%、AB 28.8% |
| ホーンパイプ | 2/2・リールより遅い | 付点の跳ね 8. 16。3拍目に3連符 | 部分の終わりは 4 4 4 r |
| ポルカ | 2/4 | 8 8 8 8｜4 4 | AABB 32小節 |
| ワルツ | 3/4 | 4 4 4、2 4、4. 8 4 | 8小節×2部 |
| マズルカ | 3/4 | 8 8 4 4（2小節で1組） | 8小節×2部 |
| ストラスペイ | 4/4 | スコッチ・スナップ 16 8. と 8. 16 | リールと同じ骨組み |
- ダンス曲は4小節目で止めない。止めるのは8小節目だけ（終止の型で）。次の部分へは弱起（2〜3音）で入る
- 8小節の型：a b a c／a a' b 結び／a b a' c／a a b b'（前半4小節は2度か5度で開いて終わり、後半は主音で閉じる）
- B部分：上の音域で始める／♭VII や IV で始める／最高音はBの4小節目あたり／Bの最後の2小節＝Aの最後の2小節
- 反復進行は2回まで。変奏＝音価を倍・半分、強勢をずらす、弱起で始める
- 1拍の動き方の型を混ぜる：分散和音（1-3-5）、回り込み（5-6-5-3）、3度で下りる（1-6-4-2）、隣へ行って戻る（3-4-3-2）、同じ音（ロールの場所）。跳躍のあとは逆向きに順次で戻す
- 結び：3-2-1、5-2-1、♭7-1、6-5-1
- 音域は1曲で9〜12度
- 旋法：Dorian は i⇄♭VII、Mixolydian は I⇄♭VII、Aeolian は i–♭VI–♭VII。二重主音（全音違いの2和音を2小節ずつ）。導音つきの V7→I は避ける。5音・6音音階
- 和音は1〜2小節に1つ（エアは2小節に1つかドローンだけ）。ii–V–I・二次ドミナントは使わない。変化は和音の数ではなく重ね方で出す
- 盛り上がりは速さより「音の密度・音域・楽器の数」。セット（エア→ジグ→リール）、調の替え方（同じ調で上の音域へ・4度上・全音上・平行調）
- 落ち着いた曲の型：前奏（ドローン＋環境音）→笛ひとりのエア→伴奏が入るエア→3/4か6/8のゆっくりした曲 AABB×2→最後のエアで高いオクターブ→冒頭の句が戻る
- 明るい曲の型：ジグ×2周（楽器を足す）→ドローンだけのつなぎ2小節→リール×3周（2周目は1オクターブ上、3周目は全員）→4度上へ→4 4 4 か 4. 4. で一斉に止める
- 2周目以降は必ず「装飾を足す・音域を変える・伴奏の役を交代・Bだけ変奏」のどれかをする

## D. 編曲と曲の流れ（③）
- 楽器を最初から最後まで全部鳴らさない。8〜16小節ごとに少なくとも1つ入れるか抜く。伴奏の和音を全部鳴らすのは2周目から
- 盛り上げは音域・旋法を明るく・転調だけでもできる。ケルトの楽器を「ファンタジーらしさ」の近道にしない（物語のために選ぶ）
- 曲の形15種：①独奏のエア→合奏 ②ゆっくり→速い（2曲つなぎ）③掛け合い ④輪唱 ⑤主題と変奏 ⑥リズム隊から積み上げ ⑦笛だけの合唱 ⑧細くなっていく逆アーチ ⑨最後の1周で全音上げ ⑩ストップタイム ⑪ピアノ組曲 ⑫行進・物語型 A–B–A′–コーダ ⑬ドローンの瞑想（旋法だけ変える）⑭ダンスの入れ子 リール–エア–リール ⑮2つの楽器のデュエット。近い番号の曲で同じ形を続けない
- 動きを出す手法：ドロップアウト（山の直前1〜2小節は笛だけ）、ハーフタイム感、反行する対旋律（チェロ・ホルンの全音符・2分音符）、山はユニゾン→オクターブに開く、同じ旋律を低い音域→高い音域、ペダルポイント（低い主音のまま上の和音だけ ♭VII→IV→I）
- ボーラン：ジグ＝下上下・下上下（1・4拍目アクセント）、リール＝16分の下上（アクセントを1・3拍と2・4拍で交互）、ホーンパイプ＝下（休）上、スロー＝1小節に1〜2打で皮を押さえてこもらせ、だんだん開く。大きくしすぎない
- ギター（DADGAD の響き）：3度を抜いた開放和音（D5・G/D・Asus4）、ジグは下上下のストラム、リールは8分＋裏拍アクセント、静かな曲は1本ずつのアルペジオ（開放弦を鳴らしたまま）
- ハープ：根音のドローン（1小節に1〜2回）、分散和音（上がって→下がって）、ローヴィング・サム（根音・5度・オクターブ＋経過音）、右手のオスティナート（3音を回す）。1つの音型をしばらく続ける
- ピアノ：ダンス＝左手が拍頭のベース・右手が裏拍の軽い和音。静か＝左手 5度とオクターブ、右手 3度・6度の長い和音。1周目は単音か5度だけ
- オーケストラ：ピチカートで刻み、持続の弦は2周目から。ホルンはテーマか長い和音だけ。ティンパニは区切りのロールと山の1打。グロッケンは笛の要所を1オクターブ上で光らせるだけ
- ミックス：笛は中央からわずかにずらし、乾いた音を前に。低音担当は1つ（チェロかピアノ左手）、ほかは 150〜250Hz より下を切る。リバーブはプリディレイ 30〜60ms、近い部屋＋遠いホールの2段。環境音は笛が休む小節でだけ聞こえるくらい

## 出典
（①）Grey Larsen「Down the Back Lane」第2・3章、「Essential Guide」第21章・p.41、ISMIR 2014、DAFx 2004、BCU（cut と strike の検出）、Maynooth ELE-Bob2、OAIM、Brother Steve（ビブラート）、woodenflute.com、irishtune.info、The Celtic Room、Irish Flute Guide、Chiff & Fipple の各スレッド、Robert Bigio（Chris Norman）、Smithsonian Folkways（sean-nós）
- https://greylarsen.com/wp-content/uploads/2013/12/DtBL-Ch.-2-Excerpt-Ornamentation.pdf
- https://greylarsen.com/wp-content/uploads/2013/12/DtBL-Ch.-3-Excerpt-Phrasing.pdf
- https://greylarsen.com/revisions/minorchanges/p.41.pdf
- https://archives.ismir.net/ismir2014/paper/000203.pdf
- https://www.rogermillington.com/siamsa/brosteve/vibrato.html
（②）
- https://www.irishtune.info/rhythm/reel-structure.html ・ https://www.irishtune.info/faq/modes.htm
- https://jsmi.musicologyireland.ie/index.php/journal/article/view/215
- https://www.mcgee-flutes.com/CeolRince1.htm（Breathnach）
- https://colinhume.com/tunes.htm ・ https://epearlman.substack.com/p/lets-write-a-tune
- https://www.joeweed.com/pdfs/Basics%20for%20Writing%20a%20Fiddle%20Tune.pdf
- https://folkworks.org/article/guide-to-irish-tune-types/ ・ https://rscds.org/learn/music-resources/types-tunes
- https://dannycarnahan.com/writing/the-darker-side-of-irish-jigs/
（③）
- https://dannycarnahan.com/writing/%EF%BF%BCan-energy-kick-from-key-changes/
- https://simonchadwick.net/2018/02/traditional-music-ireland.html
- https://tradirishmusic.com/tutorials-2/bodhran.html
- https://pegheadnation.com/string-school/courses/irish-backup-guitar/evolution-irish-backup-guitar/
- https://oaim.ie/guitar/dadgad-guitar-accompaniment/
- https://myharpsdelight.com/tag/roving-thumb ・ https://myharpsdelight.com/improvising-with-an-ostinato
- https://en.wikipedia.org/wiki/Kan_ha_diskan
- https://otakukart.com/frieren-composer-evan-call-says-celtic-music-was-used-to-add-emotion-instead-of-creating-a-generic-fantasy-soundtrack/
- https://www.izotope.com/en/learn/essential-tips-for-mixing-reverb.html
