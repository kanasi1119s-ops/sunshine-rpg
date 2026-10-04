import {
  createKyotoukyuCorridorData,
  createKyotoukyuCourtData,
  createKyotoukyuSanctumData,
  KYOTOUKYU_CORRIDOR_LANDMARKS,
  KYOTOUKYU_COURT_LANDMARKS,
  KYOTOUKYU_SANCTUM_LANDMARKS,
} from "../map/chapter9/kyotoukyu-maps";
import type { TileMapData } from "../map/types";
import { say } from "./side-story";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 終章（虚灯宮）の世界。`docs/story/structure.md`「終章（虚灯宮）」・`docs/story/mystery.md`を反映。
 * 壁画で「灯の環」と「静めの仕組み」の由来を知る（真相の完全解明）→ エドレアの最後の計画 → 最終決戦
 * → 祖父ソウイチの救出（C-017の回収）→ エンディング → 「まだ何かが眠っている」（C-020、裏ボスへの入口）。
 * ボスは `src/game/battle/chapter9-enemies.ts`。仮: 守り手・壁画の文章は簡易、地形は単色タイル。
 */
export const CHAPTER9_MAPS: Record<string, TileMapData> = {
  "kyotoukyu-court": createKyotoukyuCourtData(),
  "kyotoukyu-corridor": createKyotoukyuCorridorData(),
  "kyotoukyu-sanctum": createKyotoukyuSanctumData(),
};

/** 虚灯宮へ着いたとき、一度だけ流す場面つなぎ（`chapter9_intro_seen` フラグで管理）。 */
export const CHAPTER9_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――神話伝承の最果て、虚灯宮。" },
  {
    type: "message",
    text: "雲のさらに上、光の床が果てしなく続いている。水平線の彼方では、黒い雲が渦を巻いていた。",
  },
  { type: "message", text: "おじいちゃん……きっと、この奥にいる。ぼく、まだ一度も、会ったことがないんだ。", speaker: "ユーリ" },
  { type: "message", text: "行こう、ユーリ。ここまで来たんだ。みんなで、最後まで。", speaker: "レト" },
  { type: "setFlag", flag: "chapter9_intro_seen", value: true },
];

export const CHAPTER9_NPCS: Record<string, Npc[]> = {
  "kyotoukyu-court": [
    {
      id: "kyotoukyu-keeper",
      tileX: KYOTOUKYU_COURT_LANDMARKS.keeper.tileX,
      tileY: KYOTOUKYU_COURT_LANDMARKS.keeper.tileY,
      color: "#c8d8e8",
      commands: [
        { type: "message", text: "……久しぶりに、人の足音を聞きました。わたしは、この宮の灯守り。", speaker: "灯守り" },
        { type: "message", text: "……ああ。やはり、あなたが。ソウイチ殿の腕輪と、同じ石ですね。", speaker: "灯守り" },
        { type: "message", text: "おじいちゃんは、ここにいるんですね。生きて。", speaker: "ユーリ" },
        { type: "message", text: "生きておられます。眠っておられますが。……わたしが、ずっと、見守っておりました。", speaker: "灯守り" },
        { type: "message", text: "見守って……いた？ あなたが、ずっと、ここにいて。", speaker: "オルカ" },
        {
          type: "message",
          text: "はい。エドレア殿が、ソウイチ殿をお連れしたとき、寝台へ運び入れる手を、わたしは、止めませんでした。",
          speaker: "灯守り",
        },
        { type: "message", text: "……怖かったのです。合議会の印を携えた方の言葉は、この宮では、命令に等しかった。", speaker: "灯守り" },
        { type: "message", text: "「一人の眠りで大勢が救われるなら」と、自分に言い聞かせました。……それは、エドレア殿が、わたしに差し出した言い訳でもありました。", speaker: "灯守り" },
        { type: "message", text: "灯を守るために、人ひとりを差し出したんですか。", speaker: "ガイド" },
        { type: "message", text: "ええ。そういうことです。", speaker: "灯守り" },
        { type: "message", text: "……あなたを、許すとは言えません。おじいちゃんが二十年、眠らされたことは、なくならないから。", speaker: "ユーリ" },
        { type: "message", text: "でも、隠さずに、教えてくれました。だから、話を聞きます。最後まで、ちゃんと。", speaker: "ユーリ" },
        { type: "message", text: "……ありがとう、ございます。それが、償いの、いちばん最初なのかもしれません。", speaker: "灯守り" },
        {
          type: "message",
          text: "奥の回廊の壁には、この宮のいわれが刻まれています。読んでから進んでも、遅くはありませんよ。",
          speaker: "灯守り",
        },
        { type: "message", text: "エドレア殿は、奥の間でお待ちです。ですが、あの方は、もう逃げません。……逃げる先が、ないのです。", speaker: "灯守り" },
      ],
    },
  ],
  "kyotoukyu-corridor": [
    {
      id: "kyotoukyu-mural-left",
      tileX: KYOTOUKYU_CORRIDOR_LANDMARKS.muralLeft.tileX,
      tileY: KYOTOUKYU_CORRIDOR_LANDMARKS.muralLeft.tileY,
      color: "#7a5a8a",
      commands: [
        { type: "message", text: "左の壁に、光の柱が空から降り、砕け散る絵が刻まれている。" },
        {
          type: "message",
          text: "灯の環は、人々の争いを見て、自らを砕いた。……そう読める。砕けた力は山や海になり、一部は「歪み」として地に残ったんだ。",
          speaker: "レト",
        },
        { type: "message", text: "灯り石は、その歪みを呼び覚ましてしまう欠片。だから、人の手で歪みを起こすこともできてしまう。", speaker: "アヤメ" },
        { type: "setFlag", flag: "chapter9_mural_left", value: true },
      ],
    },
    {
      id: "kyotoukyu-mural-right",
      tileX: KYOTOUKYU_CORRIDOR_LANDMARKS.muralRight.tileX,
      tileY: KYOTOUKYU_CORRIDOR_LANDMARKS.muralRight.tileY,
      color: "#7a5a8a",
      commands: [
        { type: "message", text: "右の壁には、眠る人々と、それを見守る宮の絵が刻まれている。" },
        {
          type: "message",
          text: "「静めの間」……争いを起こす者の記憶を、眠りの中に封じる、古い仕組みがあったらしい。",
          speaker: "ガイド",
        },
        {
          type: "message",
          text: "二十年前の「静まりの年」に、要人たちが記憶を失って消えたのは、これのせいか。エドレアは、合議会の古い封印の記録から、この仕組みを知ったんだな。",
          speaker: "オルカ",
        },
        { type: "message", text: "絵の横に、古い文字が刻まれている。「悲しみが深く、憎しみが尽きぬ者、みずから望みて、ここに眠れ」" },
        { type: "message", text: "「目覚めたとき、その者が望むなら、苦しみは返す。望まぬなら、返さぬ」。……これ、強制じゃないんですね。", speaker: "ユーリ" },
        { type: "message", text: "本来は、慈悲の仕組みだったんだ。エドレアは、「みずから、望みて」という、いちばん大事な一言を、はぎ取った。", speaker: "レト" },
        { type: "setFlag", flag: "chapter9_mural_right", value: true },
        {
          type: "if",
          flag: "chapter9_mural_left",
          equals: true,
          then: [
            { type: "message", text: "灯の環の由来と、静めの仕組み。二つがそろって、エドレアのやったことのすべてが、一本の線につながった。" },
            { type: "message", text: "戦わなきゃいけないなら、戦います。でも、その前に、ちゃんと話します。", speaker: "ユーリ" },
            { type: "setFlag", flag: "chapter9_truth_known", value: true },
          ],
        },
      ],
    },
  ],
  "kyotoukyu-sanctum": [
    {
      id: "kyotoukyu-grandfather",
      tileX: KYOTOUKYU_SANCTUM_LANDMARKS.grandfather.tileX,
      tileY: KYOTOUKYU_SANCTUM_LANDMARKS.grandfather.tileY,
      color: "#b8a8c8",
      spriteName: "ソウイチ",
      commands: grandfatherCommands(),
    },
    {
      id: "kyotoukyu-deep-stairs",
      tileX: 15,
      tileY: 3,
      color: "#a8d4e8",
      commands: [
        {
          type: "if",
          flag: "side_s028_done",
          equals: true,
          then: [
            say(undefined, "祭壇の裏の階段が、深部へ続いている。冷たい光が、下から昇ってくる。"),
            { type: "choice", text: "虚灯宮・深部へ降りますか？", options: [
              { label: "降りる", commands: [{ type: "warp", mapId: "deep-1", tileX: 10, tileY: 11 }] },
              { label: "やめておく", commands: [] },
            ] },
          ],
          else: [say(undefined, "祭壇の裏の床は、ただの石だ。今は、何も起きない。")],
        },
      ],
    },
    {
      id: "kyotoukyu-edrea",
      tileX: KYOTOUKYU_SANCTUM_LANDMARKS.edrea.tileX,
      tileY: KYOTOUKYU_SANCTUM_LANDMARKS.edrea.tileY,
      color: "#3a4a7a",
      spriteName: "エドレア",
      commands: edreaCommands(),
    },
  ],
};

function edreaCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter9_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter9_edrea_surrendered",
          equals: true,
          then: [{ type: "message", text: "わたしは、合議会の裁きを受けます。……祖父君を、お連れください。", speaker: "エドレア" }],
          else: [
            { type: "message", text: "光が静まった。エドレアは膝をつき、手にしていた灯り石の杖を床に落とした。" },
            {
              type: "message",
              text: "……負けました。二十年、信じてきた「平和」が、こんな結末を迎えるとは。",
              speaker: "エドレア",
            },
            {
              type: "message",
              text: "人を眠らせて作った静けさは、平和じゃない。眠りから覚めたとき、その人の時間は、二十年前で止まってるんだ。",
              speaker: "ユーリ",
            },
            { type: "message", text: "……ええ。それを、わたしは見ないふりをしてきた。", speaker: "エドレア" },
            { type: "message", text: "ぼくが斬ったのは、あなたの手から、人を眠らせる力だけです。あなたは、目を開けて、自分のしたことの結果を、見続けてください。" , speaker: "ユーリ" },
            { type: "message", text: "それが、罰です。そして、償いの、はじまりです。", speaker: "ユーリ" },
            { type: "message", text: "二十年、一度も、ぐっすり眠れたことが、ありません。眠らせる者は、眠ってはならないと、思っていました。", speaker: "エドレア" },
            { type: "message", text: "扉の陰から、手枷をはめたドルンが、衛兵とともに現れた。小舟で、あとを追ってきたのだ。" },
            { type: "message", text: "ミナさん。麦香野の水源は、私の装置が原因でした。あなたの幼なじみの名を、私は、報告書に一行も書かなかった。", speaker: "ドルン" },
            { type: "message", text: "許せる日は、来ないかもしれません。でも、教えます。彼女の名前は、ハルです。忘れないでください。", speaker: "ミナ" },
            { type: "message", text: "オルカさん。鉱山の若い方々の肺を悪くしたのは、私の実験でした。償う機会を、いただけませんか。", speaker: "ドルン" },
            { type: "message", text: "償いは、一日では終わらない。判決のあとで、来い。", speaker: "オルカ" },
            { type: "message", text: "ガイドさん。トキオ殿のお名前を、使いました。……ご本人に、必ず、お詫びをいたします。", speaker: "ドルン" },
            { type: "message", text: "あの方は、私を拾い、切り捨てました。恨んでおりました。ですが、恨めるのは、あの方だけだった。それが、私の罪でした。", speaker: "ドルン" },
            { type: "message", text: "ドルンは、エドレアの前に立ち、短く言った。「いっしょに、償おう」" },
            { type: "message", text: "……ええ。その言葉を、わたしは、ずっと、誰かに言ってほしかったのかもしれません。", speaker: "エドレア" },
            { type: "setFlag", flag: "chapter9_edrea_surrendered", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter9_edrea_told",
          equals: true,
          then: [
            { type: "message", text: "もう一度、お相手しましょう。宮の力は、まだわたしの手の中にあります。", speaker: "エドレア" },
            { type: "startBattle", battleId: "kyotoukyu-yugami" },
          ],
          else: [
            { type: "message", text: "来ましたね。……灯守りの言葉を聞き、壁画も読んだのでしょう。ならば、隠しごとは要りませんね。", speaker: "エドレア" },
            { type: "message", text: "あなたは、ぼくたちに助言をくれました。あれは、嘘だったんですか。", speaker: "ユーリ" },
            { type: "message", text: "嘘では、ありませんでした。ただ、語らなかったことが、山のようにあった。それだけ。", speaker: "エドレア" },
            { type: "message", text: "それを、嘘って呼ぶんです。", speaker: "ユーリ" },
            { type: "message", text: "人は、沈黙を、嘘より軽いものだと考える。軽くはありません。……わたしの言葉を信じるかどうかは、あなた方次第です。", speaker: "エドレア" },
            { type: "message", text: "わたしの祖父、ハクエイを眠らせたのは、なぜですか。祖父は、人を傷つけたことなど、一度もない。", speaker: "アヤメ" },
            { type: "message", text: "善い方でした。だからこそ、です。優しい言葉は、ときに、いちばん大きな争いの火種になる。", speaker: "エドレア" },
            { type: "message", text: "レトの兄上は、わたしが最も信頼した部下でした。疫病の届けは、わたしが書かせました。彼は、病では死んでいません。", speaker: "エドレア" },
            { type: "message", text: "あの列の、右から三つ目の寝台。彼は、そこで、二十年、眠っています。", speaker: "エドレア" },
            { type: "message", text: "……生きて、るのか。二十年、あそこで。……ふざけんなよ。", speaker: "レト" },
            { type: "message", text: "幼いあなたから、兄を奪い、真実を奪いました。わたしの罪です。消えません。", speaker: "エドレア" },
            { type: "message", text: "あんたを止める。それで、兄貴を起こす。順番は、それだ。恨み言は、そのあとで、いくらでも言ってやる。", speaker: "レト" },
            {
              type: "message",
              text: "わたしは、この宮の「静めの間」を、大陸全体に開こうとしています。争いを望む者の記憶を、すべて眠りの中へ。もう二度と、大乱期は来ない。",
              speaker: "エドレア",
            },
            { type: "message", text: "大乱期は、三十年続きました。一つ一つの悲鳴を、わたしは、二度と繰り返させたくない。", speaker: "エドレア" },
            { type: "message", text: "そんなの、みんなを二十年前のおじいちゃんと同じ目にあわせるってことじゃないか！", speaker: "ユーリ" },
            { type: "message", text: "眠りは、やさしい。眠っている間、人は、誰も傷つけません。", speaker: "エドレア" },
            { type: "message", text: "それは、平和じゃない。目覚めたとき、その人の時間は止まったままです。ぼくのおじいちゃんが、今、そうなってるんです。", speaker: "ユーリ" },
            { type: "message", text: "その目覚めを、苦しみと呼ぶなら、わたしは、彼らに苦しみを与えました。それより大きな苦しみを、防いだと信じてきたのです。", speaker: "エドレア" },
            { type: "message", text: "わたしの平和を、止められるものなら止めてごらんなさい。", speaker: "エドレア" },
            { type: "setFlag", flag: "chapter9_edrea_told", value: true },
            { type: "message", text: "エドレアが杖をかかげると、虚灯宮の光が渦を巻き、その身にまとわりついた！" },
            { type: "startBattle", battleId: "kyotoukyu-yugami" },
          ],
        },
      ],
    },
  ];
}

function grandfatherCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter9_cleared",
      equals: true,
      then: [
        { type: "message", text: "ユーリ。灯里へ帰ろう。話したいことが、山ほどある。二十年寝たんだ、今度は、二十年かけて話そうじゃないか。", speaker: "ソウイチ" },
        { type: "message", text: "これも、持っていけ。眠っているあいだ、わしがつけておった腕輪だ。帰る場所のある者に、道しるべは要らん。", speaker: "ソウイチ" },
        { type: "message", text: "二つあれば、片方がくじけても、もう片方が覚えている。……まっすぐ行け。曲がるなら、曲がった理由を、自分で言えるようにな。", speaker: "ソウイチ" },
      ],
      else: [
        {
          type: "if",
          flag: "chapter9_edrea_surrendered",
          equals: true,
          then: [
            { type: "message", text: "寝台の上で、老人が静かに眠っている。ユーリの腕輪と同じ、琥珀色の灯り石の腕輪が、その手首で鈍く曇っていた。" },
            { type: "message", text: "おじいちゃん。……ユーリだよ。迎えに来たよ。", speaker: "ユーリ" },
            { type: "message", text: "呼びかけても無理です。腕輪の光が、眠りを封じています。……わたしが、解きます。最後の仕事として。", speaker: "エドレア" },
            { type: "message", text: "エドレアが、砕けた杖の破片を腕輪に触れさせると、二つの腕輪の光が溶け合った。老人のまぶたが、ゆっくりと開く。" },
            { type: "message", text: "……ここは。宮、か。……その腕輪。わしの……。いつか生まれる孫に頼むと、そう言い残して、わしは……。", speaker: "ソウイチ" },
            { type: "message", text: "はい。ぼくが、預かっていました。", speaker: "ユーリ" },
            { type: "message", text: "生まれたのか。……大きくなったな。いくつに、なった。", speaker: "ソウイチ" },
            { type: "message", text: "十六です。おじいちゃん、ぼく、ずっと、会いたかった。会ったことは、なかったけど。", speaker: "ユーリ" },
            { type: "message", text: "わしの娘の、頑固な、まっすぐな目をしておる。……長い夢を、見ていた気がする。誰かが、「まだ、諦めるな」と言うておった。", speaker: "ソウイチ" },
            { type: "setFlag", flag: "chapter9_grandfather_rescued", value: true },
            { type: "message", text: "ユーリは、言葉にならないまま、祖父の胸に飛びこんだ。レトもミナも、そっと目をそらして笑った。" },
            {
              type: "message",
              text: "……あの日、わしは証拠を集めておった。エドレアが「争いのため」と言いながら、自分の手で争いの種をまいておることを、告発するために。",
              speaker: "ソウイチ",
            },
            { type: "message", text: "エドレア。わしの前に、立てるか。", speaker: "ソウイチ" },
            { type: "message", text: "立ちます。謝罪の言葉は、ありません。言葉で済ませられるものでは、ないから。", speaker: "エドレア" },
            { type: "message", text: "わしは、あんたを責めたかったんじゃない。あんたの恐れは、わしにも分かる。だから、一緒に考えよう、と言いたかった。", speaker: "ソウイチ" },
            { type: "message", text: "許す、とは言わんぞ。二十年は長い。だが、あんたの恐れが嘘でなかったことも、知っておる。", speaker: "ソウイチ" },
            { type: "message", text: "裁きの場で、わしは、わしの言葉で証言しよう。あんたが何をしたか、何を恐れていたか。どちらも、隠さずに。", speaker: "ソウイチ" },
            { type: "message", text: "……ありがとうございます。", speaker: "エドレア" },
            { type: "message", text: "それから二日、眠りびとたちは、一人ずつ目覚めた。エドレアが封印を解き、灯守りが、二十年呼びつづけた名前を読み上げた。" },
            { type: "message", text: "ハクエイは、枕元のアヤメを見て言った。「お嬢さん、わたしを知っているのかね」。アヤメは答えた。「孫です。初めまして、おじいさま」", speaker: undefined },
            { type: "message", text: "レトの兄も、目を覚ました。「泣くなら、理由を言え」と笑う兄に、レトは言った。「理由が、ありすぎて、分かんねえ」" },
            { type: "message", text: "トウマも、ほかの人々も、順に目覚めた。……目覚めなかった人も、三人いた。胸が、痛んだ。" },
            { type: "message", text: "歪みは、この先もまだ、各地に残っている。みんなで、少しずつ鎮めていこう。", speaker: "アヤメ" },
            { type: "message", text: "三日後の朝、議長の大きな帆船が、迎えに来た。こうして、灯りの相談所の旅は、ひとつの終わりを迎えた。" },
            { type: "message", text: "エドレアとドルンは、灯芯都の合議会の、公正な場で裁かれることになる。" },
            { type: "message", text: "――だが、宮を発つ前、祖父は、壇の裏の暗がりを見つめ、小さくつぶやいた。" },
            {
              type: "message",
              text: "……まだ、何かが眠っておる。この宮の、もっと深いところに。あれは、二十年前の事件よりも、ずっと古いものじゃ。",
              speaker: "ソウイチ",
            },
            { type: "message", text: "★ メインストーリーをクリアしました！（虚灯宮の奥に、クリア後の道が開いた）" },
            { type: "setFlag", flag: "chapter9_cleared", value: true },
            { type: "setFlag", flag: "chapter9_secret_open", value: true },
            { type: "staffRoll" },
          ],
          else: [
            { type: "message", text: "寝台の上で、老人が静かに眠っている。手首には、ユーリの腕輪とそっくりな灯り石の腕輪。" },
            { type: "message", text: "おじいちゃん……！ 起きて、ねえ、おじいちゃん！", speaker: "ユーリ" },
            { type: "message", text: "呼びかけても、目を覚まさない。腕輪の光が、眠りを封じているようだ。まず、この宮の主と話をつけなければ。" },
          ],
        },
      ],
    },
  ];
}
