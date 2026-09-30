import { buildSideStoryNpcs, say, type SideStory } from "./side-story";
import { SIDE_STORIES_LATE } from "./side-stories-late";
import type { Npc } from "../npc";

/**
 * サブストーリー（`docs/story/side-stories.md` の骨子を実装したもの。形式は `side-story.ts`）。
 * 仮: 報酬（灯貨・品物・信頼度）は「ごほうび（仮）」の会話のみ。セリフは簡易。
 */
export const SIDE_STORIES: SideStory[] = [
  ...SIDE_STORIES_LATE,
  // ===== 序章（灯里）=====
  {
    id: "S-001",
    key: "s001",
    title: "迷子の「灯り貂」",
    unlockFlags: ["chapter0_yugami_defeated"],
    giver: { mapId: "touri-town", tileX: 9, tileY: 3, color: "#e0a060" },
    locked: [say("子ども", "……あっ、ううん、なんでもない。")],
    offer: [
      say("子ども", "ねえ、お兄ちゃん、お姉ちゃん。ぼくの灯り貂の「ルル」がいなくなっちゃったんだ。"),
      say("子ども", "灯り貂は、灯り石のそばで、ぽっと光るふわふわの生き物だよ。町のどこかにいるはずなんだ。"),
    ],
    offerPrompt: "ルルを捜しますか?",
    acceptLabel: "捜してみる",
    hint: [say("子ども", "ルル、まだ見つからないの……? 市場の近くかな。倉庫のほうも見てほしいな。")],
    steps: [
      {
        mapId: "touri-town", tileX: 2, tileY: 7, color: "#c8a878",
        commands: [say(undefined, "市場の売り場のうしろに、小さな足あとが残っている。干し魚のかけらが、ちょっとかじられていた。")],
      },
      {
        mapId: "touri-town", tileX: 17, tileY: 7, color: "#c8a878",
        commands: [
          say(undefined, "倉庫の裏の木箱の上で、ふわふわの小さな生き物が丸くなっている。ぽっと、やさしく光った。"),
          say("ユーリ", "見つけた。市場の匂いに誘われて、迷いこんでいたんだな。"),
        ],
      },
    ],
    complete: [
      say("子ども", "ルルだ! よかった、ありがとう! 干し魚を食べすぎて、動けなくなってたんだね。"),
      say("子ども", "お礼に、おかあさんが作った灯り草をあげる。ちょっと苦いけど、よく効くんだよ。"),
    ],
    reward: "灯り草をもらった。",
    after: [say("子ども", "ルルは、いまぼくのひざの上でぐっすり寝てるよ。ありがとう!")],
  },
  {
    id: "S-002",
    key: "s002",
    title: "レトの忘れ物",
    unlockFlags: ["chapter0_reto_joined"],
    giver: { mapId: "touri-branch", tileX: 6, tileY: 3, color: "#8a9ab8" },
    locked: [say("資料室の係", "資料室は、灯りの相談所の調査員のための部屋です。")],
    offer: [
      say("資料室の係", "レトさんが、資料室の古い棚に、封筒を預けたままなんです。取りに行くのを、手伝っていただけませんか?"),
      say("資料室の係", "棚の奥の、一番下です。わたしは腰が痛くて……。"),
    ],
    offerPrompt: "封筒を取りに行きますか?",
    acceptLabel: "取りに行く",
    hint: [say("資料室の係", "封筒は、棚の奥の、一番下です。埃をかぶっているので、お気をつけて。")],
    steps: [
      {
        mapId: "touri-branch", tileX: 2, tileY: 4, color: "#a08a6a",
        commands: [
          say(undefined, "棚の一番下に、古い封筒が挟まっている。表には、几帳面な字で「静まりの年 覚え書き」と書かれていた。"),
          say("レト", "……あ、それ。ありがとう。中身は、まだ見せられないんだ。ごめん。"),
        ],
      },
    ],
    complete: [
      say("資料室の係", "ああ、見つかりましたか。ありがとうございます。レトさんに、渡しておきますね。"),
      say("資料室の係", "お礼に、この資料室は、いつでも自由にお使いください。"),
    ],
    reward: "灯里支部の資料室が、いつでも使えるようになった。",
    after: [say("資料室の係", "資料室は、いつでもどうぞ。棚の整理を、ときどき手伝ってくれるとうれしいですけどね。")],
  },
  // ===== 第1章（麦香野）=====
  {
    id: "S-003",
    key: "s003",
    title: "水車小屋の修理",
    unlockFlags: ["chapter1_reported_to_elder"],
    giver: { mapId: "mugikano-village", tileX: 5, tileY: 7, color: "#b09070" },
    locked: [say("水車小屋の老人", "水が戻るのは、いつになることやら……。")],
    offer: [
      say("水車小屋の老人", "水は戻ったが、水車の羽根が折れたままでな。わし一人じゃ、直せん。"),
      say("水車小屋の老人", "板と縄を、集めてきてくれんか。村の物置と、水路のそばに転がっとるはずじゃ。"),
    ],
    offerPrompt: "水車を直すのを手伝いますか?",
    acceptLabel: "手伝う",
    hint: [say("水車小屋の老人", "板は物置に、縄は水路のそばじゃ。頼んだぞ。")],
    steps: [
      { mapId: "mugikano-village", tileX: 13, tileY: 5, color: "#a08a6a", commands: [say(undefined, "物置の隅に、まだ使えそうな丈夫な板が積んである。かついで持っていくことにした。")] },
      { mapId: "mugikano-village", tileX: 11, tileY: 11, color: "#a08a6a", commands: [say(undefined, "水路のそばに、太い縄が束ねて置いてある。水を吸って重いが、しっかりしている。")] },
    ],
    complete: [
      say("水車小屋の老人", "うむ、これで直せる。……ほれ、ぎいっと回った。ひさしぶりの音じゃ。"),
      say("水車小屋の老人", "歪みが去ったあとの暮らしは、こうやって少しずつ戻っていくんじゃな。ありがとうよ。"),
    ],
    reward: "麦香野の特産・麦のクッキーをもらった。",
    after: [say("水車小屋の老人", "水車がまわると、小屋じゅうが小麦の匂いになる。いい村じゃろう?")],
  },
  {
    id: "S-004",
    key: "s004",
    title: "ミナの幼なじみを探して（前編）",
    unlockFlags: ["chapter1_mina_joined"],
    giver: { mapId: "mugikano-village", tileX: 16, tileY: 8, color: "#9a7a8a" },
    locked: [say("洗濯おばさん", "今日はいい天気ねえ。洗濯物がよく乾くわ。")],
    offer: [
      say("洗濯おばさん", "ミナちゃんの、あの子のことかい? 幼なじみの男の子ね。最後に見たのは、水源の古い橋のあたりだったよ。"),
      say("ミナ", "……ユーリ。調べるの、つきあってくれる? 一人だと、怖くて。"),
    ],
    offerPrompt: "幼なじみの手がかりを探しますか?",
    acceptLabel: "つきあう",
    hint: [say("洗濯おばさん", "水源の古い橋のあたりと、井戸端で聞いてみるといいよ。")],
    steps: [
      {
        mapId: "mugikano-village", tileX: 8, tileY: 4, color: "#b0a070",
        commands: [
          say("井戸端の少年", "その子なら、歪みが出た日の前の晩、水源のほうへ走っていくのを見たよ。手に、青い石を持ってた。"),
          say("ミナ", "青い石……あの子が、宝物にしてた、水色の灯り石だ。"),
        ],
      },
      {
        mapId: "mugikano-water-source", tileX: 6, tileY: 6, color: "#8aa8b8",
        commands: [
          say(undefined, "古い橋のたもとに、小さな足あとの跡が乾いて残っている。その先に、水色の欠片がひとつ落ちていた。"),
          say("ミナ", "……これ、あの子の石の欠片。無事でいて、お願い。"),
        ],
      },
    ],
    complete: [
      say("ミナ", "手がかりは見つかったけど、本人にはまだ会えなかったね。でも、ひとりじゃなかったから、最後まで調べられた。ありがとう、ユーリ。"),
      say("洗濯おばさん", "ミナちゃんの顔が、少し明るくなったねえ。あの子の続きは、また遠くで見つかるかもしれないよ。"),
    ],
    reward: "ミナとの絆が深まった。",
    after: [say("洗濯おばさん", "きっと、どこかで元気にしてるよ。信じて待つのも、大事なことさ。")],
  },
  {
    id: "S-005",
    key: "s005",
    title: "水争いの後始末",
    unlockFlags: ["chapter1_reported_to_elder"],
    giver: { mapId: "mugikano-village", tileX: 19, tileY: 5, color: "#8a9a70" },
    locked: [say("農夫", "水が枯れてから、ほかの田の連中と、口もきいとらん。")],
    offer: [
      say("農夫", "水争いのとき、わしは隣の田のやつに、ひどいことを言ってしもうた。謝りたいんじゃが、きっかけがなくてな。"),
      say("農夫", "この、麦の束を、隣の田のあいつに届けてくれんか。わしからだとは、言わんでもええ。"),
    ],
    offerPrompt: "麦の束を届けますか?",
    acceptLabel: "届ける",
    hint: [say("農夫", "隣の田のやつは、水路の向こうにおる。麦の束、頼んだぞ。")],
    steps: [
      {
        mapId: "mugikano-village", tileX: 8, tileY: 12, color: "#8a9a70",
        commands: [
          say("隣の田の農夫", "……この麦、あいつの田のものだな。まったく、素直じゃないんだから。"),
          say("隣の田の農夫", "俺も言いすぎたんだ。今度の収穫祭には、こっちから声をかけるよ、と伝えてくれ。"),
        ],
      },
    ],
    complete: [
      say("農夫", "……そうか。あいつも、そう言うたか。やれやれ、ええ年をして、意地を張りおって。"),
      say("農夫", "灯里の事件とちがって、人の争いは、話せばおさまるもんじゃな。ありがとう。"),
    ],
    reward: "麦の穂の飾りをもらった。",
    after: [say("農夫", "収穫祭には、あいつと二人で酒を酌み交わすつもりじゃ。")],
  },
  // ===== 第2章（硝子湖）=====
  {
    id: "S-006",
    key: "s006",
    title: "湖上市場の値切り合戦",
    unlockFlags: ["chapter2_intro_seen"],
    giver: { mapId: "garasuko-town", tileX: 8, tileY: 4, color: "#d0a050" },
    locked: [say("商人の少年", "いらっしゃい! 今日もいい品がそろってるよ!")],
    offer: [
      say("商人の少年", "お兄さん、お姉さん、旅の人だろ? 俺と勝負しないか。この干し果物、一番安く買えた人が勝ちだ。"),
      say("商人の少年", "市場の三軒を回って、いちばん安い値をつけた店を見つけてきなよ。俺は、もう見つけたけどね!"),
    ],
    offerPrompt: "値切り勝負を受けますか?",
    acceptLabel: "受けて立つ",
    hint: [say("商人の少年", "三軒とも回ったかい? 値切るときは、笑顔が大事なんだぜ。")],
    steps: [
      { mapId: "garasuko-town", tileX: 3, tileY: 6, color: "#c0a878", commands: [say("魚屋", "その干し果物? 百二十灯貨だね。まけて、百だ!")] },
      { mapId: "garasuko-town", tileX: 12, tileY: 3, color: "#c0a878", commands: [say("布屋", "干し果物なら、うちは九十五灯貨。あなたの笑顔に免じて、九十!")] },
      { mapId: "garasuko-town", tileX: 18, tileY: 6, color: "#c0a878", commands: [say("香辛料屋", "うちは八十五灯貨さ。旅の人には、特別に八十にしとくよ。")] },
    ],
    complete: [
      say("商人の少年", "へえ、八十灯貨か! やるじゃないか、俺の負けだ。俺は八十五までしか、まけさせられなかった。"),
      say("商人の少年", "お礼に、うちの店の割引券をあげるよ。今度は、俺に勝てるかな?"),
    ],
    reward: "道具屋の割引券をもらった。",
    after: [say("商人の少年", "また勝負しようぜ! ……ところで、俺、いつか大きな商会を持つのが夢なんだ。")],
  },
  {
    id: "S-007",
    key: "s007",
    title: "ガイドの従兄の噂",
    unlockFlags: ["chapter2_guide_joined"],
    giver: { mapId: "garasuko-town", tileX: 16, tileY: 5, color: "#8a8aa8" },
    locked: [say("船乗り", "港は今日も、風向きが悪いな。")],
    offer: [
      say("船乗り", "密輸の元締めがガイドの従兄だって噂、聞いたか? 町じゅうの噂だぜ。"),
      say("船乗り", "確かめたいなら、港と市場で聞いてみな。ただし、本人の前では言わないほうがいい。"),
    ],
    offerPrompt: "噂を聞き込みますか?",
    acceptLabel: "聞き込む",
    hint: [say("船乗り", "港の桟橋と、市場の裏で、口の軽いやつが話してるはずだ。")],
    steps: [
      { mapId: "garasuko-town", tileX: 2, tileY: 4, color: "#a09080", commands: [say("桟橋の男", "ああ、あの一家か。従兄は、あちこちの港に顔がきくらしい。金回りが、妙にいいんだ。")] },
      { mapId: "garasuko-town", tileX: 14, tileY: 8, color: "#a09080", commands: [say("市場の女", "ガイドくん、いい子なんだけどねえ。あの従兄が来ると、いつも青い顔をしてたわ。")] },
    ],
    complete: [
      say("船乗り", "な、疑わしい話ばかりだろ。……まあ、ガイドが何も知らないって保証は、俺にはできねえがな。"),
      say("ユーリ", "うーん……。ガイド本人に、直接聞けるのは、まだ先になりそうだ。"),
    ],
    reward: "灯貨の入った小さな袋をもらった。",
    after: [say("船乗り", "噂は噂だ。あんたたちの目で、確かめるのがいい。")],
  },
  {
    id: "S-008",
    key: "s008",
    title: "湖の渡し守の昔語り",
    unlockFlags: ["chapter2_intro_seen"],
    giver: { mapId: "garasuko-town", tileX: 19, tileY: 2, color: "#7a9aa8" },
    locked: [say("渡し守", "湖の上は、今日も静かだ。")],
    offer: [say("渡し守", "湖の話を、聞いていくかい? 灯り石の交易が始まった頃の、古い話だよ。")],
    offerPrompt: "昔語りを聞きますか?",
    acceptLabel: "聞く",
    hint: [],
    steps: [],
    complete: [
      say("渡し守", "昔、この湖は、ただの澄んだ水たまりだった。灯り石を運ぶ小舟が、一艘、また一艘と増えて、いまの町になったんだ。"),
      say("渡し守", "石は人を豊かにしたが、争いのタネにもなった。それでも人は、石を運ぶのをやめなかった。……人ってのは、そういうもんさ。"),
    ],
    reward: "灯貨をもらった。",
    after: [say("渡し守", "湖は、何もかも見てきた。あんたたちの旅も、きっと覚えているよ。")],
  },
  // ===== 第3章（鉄鏈鉱山）=====
  {
    id: "S-009",
    key: "s009",
    title: "組合の書類整理",
    unlockFlags: ["chapter3_intro_seen"],
    giver: { mapId: "tetsukusari-town", tileX: 9, tileY: 3, color: "#8a8aa0" },
    locked: [say("組合の事務員", "書類の山が、崩れそうです……。")],
    offer: [
      say("組合の事務員", "労働争議で、組合の書類がぐちゃぐちゃなんです。日付順に並べ直すのを、手伝っていただけませんか?"),
      say("組合の事務員", "床に散らばった分と、棚から落ちた分の、二か所です。"),
    ],
    offerPrompt: "書類の整理を手伝いますか?",
    acceptLabel: "手伝う",
    hint: [say("組合の事務員", "床の分と、棚の分。どちらも、日付順にお願いします。")],
    steps: [
      { mapId: "tetsukusari-town", tileX: 6, tileY: 6, color: "#b8b0a0", commands: [say(undefined, "床いっぱいの書類を拾い集め、日付を確かめながら、一枚ずつそろえていく。")] },
      { mapId: "tetsukusari-town", tileX: 15, tileY: 6, color: "#b8b0a0", commands: [say(undefined, "棚から落ちた帳簿は、背表紙の番号がバラバラだ。番号順に、きれいに戻していく。")] },
    ],
    complete: [
      say("組合の事務員", "おかげで、書類が全部そろいました。ありがとうございます!"),
      say("組合の事務員", "そういえば、うちの代表のオルカさんは、書類仕事だけは、いつも後回しにするんですよ。"),
    ],
    reward: "灯貨をもらった。",
    after: [say("組合の事務員", "書類がそろうと、気持ちまでそろう気がします。またお願いするかもしれません。")],
  },
  {
    id: "S-010",
    key: "s010",
    title: "ミナの幼なじみを探して（後編）",
    unlockFlags: ["chapter3_orca_joined", "side_s004_done"],
    giver: { mapId: "tetsukusari-town", tileX: 3, tileY: 8, color: "#9a7a8a" },
    locked: [say("旅の女", "……なんでもないの、ただの旅の者よ。")],
    offer: [
      say("旅の女", "あなたたち、水色の灯り石を探している子のことを、知ってる? 麦香野から来たって聞いたけど。"),
      say("旅の女", "その子なら、鉱山の町のはずれで、静かに暮らしてる。会ってみる?"),
      say("ミナ", "……ユーリ、お願い。行こう。"),
    ],
    offerPrompt: "その人に会いに行きますか?",
    acceptLabel: "会いに行く",
    hint: [say("旅の女", "町のはずれの、古い石の家よ。落ち着いて、ゆっくり話してね。")],
    steps: [
      {
        mapId: "tetsukusari-town", tileX: 19, tileY: 8, color: "#a0a8c0",
        commands: [
          say("幼なじみ", "……ミナ? ミナなのか?"),
          say("ミナ", "うん。ずっと、探してた。無事でよかった……。"),
          say("幼なじみ", "あの日、歪みに巻きこまれて、記憶が曖昧になって、家に戻れなかったんだ。心配かけて、ごめん。"),
          say("ミナ", "ううん、いいの。生きていてくれれば。……ありがとう、ユーリ、みんな。"),
        ],
      },
    ],
    complete: [
      say("旅の女", "会えたのね。よかった。あの子、ずっと誰かを待っているような顔をしてたの。"),
      say("ミナ", "歪みが怖くて、目をそらしてたけど、向き合ってよかった。これからも、みんなと戦えるよ。"),
    ],
    reward: "ミナがさらに頼もしくなった。",
    after: [say("旅の女", "あの二人、これからは時々、手紙のやり取りをするそうよ。")],
  },
  {
    id: "S-011",
    key: "s011",
    title: "事故の記憶",
    unlockFlags: ["chapter3_orca_joined"],
    giver: { mapId: "tetsukusari-town", tileX: 12, tileY: 6, color: "#8a7a6a" },
    locked: [say("年配の鉱夫", "坑道の奥は、まだ通れんよ。")],
    offer: [
      say("年配の鉱夫", "……あんたたち、オルカの仲間だな。あの子は、昔の落盤で、仲間を助けられんかったことを、今も背負っておる。"),
      say("年配の鉱夫", "事故のあった坑口に、花を供えに行く日じゃ。ついていってやってくれんか。"),
    ],
    offerPrompt: "オルカに付き添いますか?",
    acceptLabel: "付き添う",
    hint: [say("年配の鉱夫", "坑口は、町の北の、古い入口じゃ。花は、もう供えてある。")],
    steps: [
      {
        mapId: "tetsukusari-mine", tileX: 8, tileY: 7, color: "#9a9aa8",
        commands: [
          say(undefined, "古い坑口の前に、色あせた花束が置かれている。オルカは、黙ってそこに立っていた。"),
          say("オルカ", "……あの日、わたしが、もう少し早く気づいていれば。"),
          say("ユーリ", "オルカ。あなたのせいじゃない。みんな、それを分かってる。"),
          say("オルカ", "……そうか。ありがとう。そう言ってもらえると、少し、肩が軽くなる。"),
        ],
      },
    ],
    complete: [
      say("年配の鉱夫", "あの子が、誰かに背中を見せたのは、初めてじゃ。ありがとうよ。"),
      say("年配の鉱夫", "岩はな、崩れることもあるが、積み直すこともできる。あの子も、きっと、そうなれる。"),
    ],
    reward: "オルカとの絆が深まった。",
    after: [say("年配の鉱夫", "オルカが、前より笑うようになった。それだけで、わしは十分じゃ。")],
  },
  // ===== 第4章（砂音）=====
  {
    id: "S-012",
    key: "s012",
    title: "隊商の道案内",
    unlockFlags: ["chapter4_intro_seen"],
    giver: { mapId: "sanone-town", tileX: 8, tileY: 3, color: "#c0a060" },
    locked: [say("隊商の若者", "砂は、今日も風で動いてるな。")],
    offer: [
      say("隊商の若者", "砂の上は、道が毎日変わるんだ。隊商を安全な経路へ、先導してもらえないか。"),
      say("隊商の若者", "目印は、風に削られた三本の岩さ。順番に、確かめてきてほしい。"),
    ],
    offerPrompt: "隊商の先導を引き受けますか?",
    acceptLabel: "引き受ける",
    hint: [say("隊商の若者", "三本の岩は、町の外れに向かって並んでる。順番に、頼むよ。")],
    steps: [
      { mapId: "sanone-camp", tileX: 5, tileY: 4, color: "#b8a078", commands: [say(undefined, "一本目の岩には、風が削った、矢印のような模様がある。東を指している。")] },
      { mapId: "sanone-camp", tileX: 11, tileY: 4, color: "#b8a078", commands: [say(undefined, "二本目の岩の根元の砂は、しっかり固まっている。ここなら、荷馬車も沈まない。")] },
      { mapId: "sanone-camp", tileX: 17, tileY: 5, color: "#b8a078", commands: [say(undefined, "三本目の岩の向こうに、緑の見える窪地が広がっている。ここが目的地だ。")] },
    ],
    complete: [
      say("隊商の若者", "さすがだ、砂を読むのが上手いな。これで、隊商も安全に着ける。"),
      say("隊商の若者", "風をつかまえるコツは、帆を欲張らないこと。……ん、これ、聞いたことあるか?"),
    ],
    reward: "灯貨と、風の読み方のヒントをもらった。",
    after: [say("隊商の若者", "砂の上の旅は、ひとりじゃできない。あんたたちがいると、心強いよ。")],
  },
  {
    id: "S-013",
    key: "s013",
    title: "隊商の掟破り",
    unlockFlags: ["chapter4_intro_seen"],
    giver: { mapId: "sanone-town", tileX: 20, tileY: 4, color: "#a08060" },
    locked: [say("隊商の見張り", "この先の抜け道は、通行止めだ。")],
    offer: [
      say("隊商の見張り", "うちの若いのが、掟を破って、危ない抜け道を通ろうとしている。止めてくれないか。"),
      say("隊商の見張り", "……いや、事情があるのかもしれん。話だけでも、聞いてやってくれ。"),
    ],
    offerPrompt: "若者に会いに行きますか?",
    acceptLabel: "会いに行く",
    hint: [say("隊商の見張り", "若いのは、野営地の、東の外れにおるはずだ。")],
    steps: [
      {
        mapId: "sanone-camp", tileX: 14, tileY: 7, color: "#b09070",
        commands: [
          say("若い隊商員", "……わかってる、掟破りだって。でも、病気の妹に、遠い町の薬を早く届けたいんだ。"),
          {
            type: "choice",
            text: "どうしますか?",
            options: [
              { label: "掟を守るよう説得する", commands: [say("ユーリ", "掟は、みんなの命を守るためのものだ。遠回りでも、確かな道を行こう。"), say("若い隊商員", "……そうだな。俺が倒れたら、薬も届かない。安全な道で行くよ。"), { type: "setFlag", flag: "side_s013_kept_rule", value: true }] },
              { label: "事情を汲んで見逃す", commands: [say("ユーリ", "気をつけて。危ないと思ったら、すぐ引き返すんだ。"), say("若い隊商員", "ありがとう! 必ず、無事に届けてみせる。"), { type: "setFlag", flag: "side_s013_let_go", value: true }] },
            ],
          },
        ],
      },
    ],
    complete: [
      say("隊商の見張り", "そうか、そういう話だったか。……どちらの選択も、間違いじゃない。ご苦労だったな。"),
      say("隊商の見張り", "掟は、人を縛るためじゃない。守るためにある。それを分かってくれる者がいて、安心した。"),
    ],
    reward: "灯貨をもらった。（選んだ道によって、隊商の見張りの言葉が少し変わる）",
    after: [say("隊商の見張り", "あの若者の妹は、無事に薬を飲めたそうだ。……よかった。")],
  },
];

export const SIDE_STORY_NPCS: Record<string, Npc[]> = buildSideStoryNpcs(SIDE_STORIES);
