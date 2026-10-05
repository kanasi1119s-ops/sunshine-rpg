import { createKiriArchiveData, KIRI_ARCHIVE_LANDMARKS } from "../map/chapter5/kiri-archive";
import { createKiriTownData, KIRI_CHURCH_TOWN_DOOR, KIRI_TOWN_LANDMARKS } from "../map/chapter5/kiri-town";
import { createKiriChurchData, KIRI_CHURCH_SPOTS } from "../map/chapter5/kiri-church";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第5章（霧断崖）の世界。`docs/story/structure.md`「第5章（霧断崖）」・`docs/story/mystery.md`を反映。
 * 伏線 C-010（静まりの年に要人が失脚・失踪した記録）と C-011（記録の中のユーリの祖父の名）を実装（roadmap 4-22）。
 * 敵データ・バランスは4-23、専用BGMは`src/audio/catalog.ts`（town-kiri・archive・boss-kiri）。
 */
export const CHAPTER5_MAPS: Record<string, TileMapData> = {
  "kiri-town": createKiriTownData(),
  "kiri-archive": createKiriArchiveData(),
  "kiri-church": createKiriChurchData(KIRI_CHURCH_TOWN_DOOR),
};

/** 霧断崖へ到着したとき、一度だけ流す場面つなぎ（`chapter5_intro_seen` フラグで管理）。 */
export const CHAPTER5_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――断崖に張り付く、霧の古都・霧断崖。" },
  {
    type: "message",
    text: "砂音で聞いた「合議会に近い誰か」の噂。その手がかりと、紙切れの「静まりの年」の意味を求めて、ユーリたちは環信仰の聖地を訪ねた。",
  },
  { type: "message", text: "門の石柱には、三つの環が刻まれている。いちばん小さな環だけが、欠けている。環信仰のしるしだ。" },
  {
    type: "message",
    text: "町は深い霧に包まれている。巡礼者たちは声をひそめ、荷造りをして町を去る家族の姿もある。",
  },
  { type: "setFlag", flag: "chapter5_intro_seen", value: true },
];

export const CHAPTER5_NPCS: Record<string, Npc[]> = {
  // 司祭は、環の聖堂の中の祭壇の前にいる（2026-10-05、聖堂の中を作ったので町の広場から移した）
  "kiri-church": [
    {
      id: "kiri-priest",
      tileX: KIRI_CHURCH_SPOTS.priest.tileX,
      tileY: KIRI_CHURCH_SPOTS.priest.tileY,
      color: "#d8d0b8",
      commands: priestCommands(),
    },
    {
      id: "kiri-church-friar",
      tileX: KIRI_CHURCH_SPOTS.friar.tileX,
      tileY: KIRI_CHURCH_SPOTS.friar.tileY,
      color: "#6a5a7a",
      commands: [
        { type: "message", speaker: "修道士", text: "ようこそ、環の聖堂へ。奥の大きな窓の三つの環を、ご覧になりましたか。" },
        { type: "message", speaker: "修道士", text: "いちばん小さな環だけが、欠けているでしょう。欠けたままでも、環は環。そう教わってきました。" },
      ],
    },
    {
      id: "kiri-church-worshipper",
      tileX: KIRI_CHURCH_SPOTS.worshipper.tileX,
      tileY: KIRI_CHURCH_SPOTS.worshipper.tileY,
      color: "#8a7a60",
      commands: [
        { type: "message", speaker: "祈る人", text: "……霧が晴れますように。町を出ていった家族が、無事でありますように。" },
        { type: "message", text: "静かに手を合わせている。ろうそくの火が、かすかにゆれた。" },
      ],
    },
  ],
  "kiri-town": [
    {
      id: "kiri-pilgrim",
      tileX: KIRI_TOWN_LANDMARKS.pilgrim.tileX,
      tileY: KIRI_TOWN_LANDMARKS.pilgrim.tileY,
      color: "#7a8aa0",
      commands: pilgrimCommands(),
    },
    {
      id: "kiri-scribe",
      tileX: KIRI_TOWN_LANDMARKS.scribe.tileX,
      tileY: KIRI_TOWN_LANDMARKS.scribe.tileY,
      color: "#5a5a6a",
      commands: scribeCommands(),
    },
  ],
  "kiri-archive": [
    {
      id: "kiri-record",
      tileX: KIRI_ARCHIVE_LANDMARKS.record.tileX,
      tileY: KIRI_ARCHIVE_LANDMARKS.record.tileY,
      color: "#c8b890",
      commands: recordCommands(),
    },
    {
      id: "kiri-ledger",
      tileX: KIRI_ARCHIVE_LANDMARKS.ledger.tileX,
      tileY: KIRI_ARCHIVE_LANDMARKS.ledger.tileY,
      color: "#8a6a4a",
      commands: ledgerCommands(),
    },
    {
      id: "kiri-keeper",
      tileX: KIRI_ARCHIVE_LANDMARKS.keeper.tileX,
      tileY: KIRI_ARCHIVE_LANDMARKS.keeper.tileY,
      color: "#3a3a4a",
      commands: keeperCommands(),
    },
  ],
};

function priestCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter5_reported",
      equals: true,
      then: [
        {
          type: "message",
          text: "環の教えは、人を怖がらせるためのものではありません。それを取り戻せたのは、あなた方のおかげです。",
          speaker: "司祭",
        },
        {
          type: "message",
          text: "灯りの芯を、一本お持ちください。旅の先で、あなたの灯りが消えませんように。",
          speaker: "司祭",
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter5_quest_accepted",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter5_yugami_defeated",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "そうですか……記録の間の予言の碑文は、誰かが書き換えていたのですね。",
                  speaker: "司祭",
                },
                {
                  type: "message",
                  text: "実は二十年前、碑の欄が削られたとき、私は気づいていました。気づいて、黙っていたのです。",
                  speaker: "司祭",
                },
                {
                  type: "message",
                  text: "「静まりの年」に、合議会の要人が四人職を退き、三人が行方を絶った。その記録が、碑から消されていたとは。",
                  speaker: "司祭",
                },
                {
                  type: "message",
                  text: "しかも、原本の綴りには、ハクエイ殿、トウマ殿、そしてあなたの祖父君、ソウイチ殿の名が残っていたのですね。",
                  speaker: "司祭",
                },
                {
                  type: "message",
                  text: "……祖父が、合議会員を二期も務めた人だったなんて。ぼくは、何も知りませんでした。",
                  speaker: "ユーリ",
                },
                {
                  type: "message",
                  text: "綴りには「ほか、随行の者数名。名は略す」とあった。数えられなかった人たちが、まだいるんだ。",
                  speaker: "レト",
                },
                { type: "message", text: "レトは、それ以上は何も言わず、静かに拳を握った。" },
                {
                  type: "message",
                  text: "写字官は、碑を元の形に戻すと誓いました。町の人々には、私からすべてを話します。",
                  speaker: "司祭",
                },
                {
                  type: "message",
                  text: "私に分かるのは、ここまでです。真実を知る者は、灯芯都にいるでしょう。どうか、気をつけて。",
                  speaker: "司祭",
                },
                {
                  type: "message",
                  text: "禁域の縄の先にも、いつか来ます。祖父の名前を、ぼくは知りたいんです。",
                  speaker: "ユーリ",
                },
                { type: "setFlag", flag: "chapter5_reported", value: true },
              ],
              else: [
                {
                  type: "message",
                  text: "調べは、北の岩壁の「記録の間」からお願いします。碑文の写しは、そこにあります。",
                  speaker: "司祭",
                },
                {
                  type: "message",
                  text: "鍵は書記のユキヒサが持っています。町の書記の話も、聞いてみてください。",
                  speaker: "司祭",
                },
              ],
            },
          ],
          else: [
            {
              type: "message",
              text: "ようこそ、霧断崖へ。司祭のホウゲンです。五十年近く、この聖堂に仕えてまいりました。",
              speaker: "司祭",
            },
            {
              type: "message",
              text: "五日前の朝、予言の碑に「霧が町を呑み、人々は灯を失う」という一節が、光って浮かび上がったのです。",
              speaker: "司祭",
            },
            {
              type: "message",
              text: "日が沈むと薄れ、翌朝また現れます。巡礼者は怯え、町を去る家族も出ています。",
              speaker: "司祭",
            },
            {
              type: "message",
              text: "けれど、私は碑の写しを何千回も読みました。こんな一節は、古い記録にありません。",
              speaker: "司祭",
            },
            {
              type: "choice",
              text: "記録の間を調べますか？",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter5_quest_accepted", value: true },
                    { type: "message", text: "お任せください。", speaker: "ユーリ" },
                    { type: "message", text: "碑文は、一文字ずつ。書架も、綴りの奥まで、隅々まで調べてください。ほんの小さな違いが、大きな真実を隠していることがあります。", speaker: "司祭" },
                    { type: "message", text: "ありがとうございます。記録の間は、町の北の岩壁にあります。", speaker: "司祭" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [{ type: "message", text: "お気持ちが決まったら、いつでもどうぞ。", speaker: "司祭" }],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function pilgrimCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter5_reported",
      equals: true,
      then: [
        { type: "message", text: "碑が元に戻ったそうだね。霧は、この町の毛布。やっぱり、歌のとおりだったよ。", speaker: "巡礼者" },
        { type: "message", text: "霧が晴れたら、また巡礼を続けるよ。教えの道は、まだ先だからね。", speaker: "巡礼者" },
      ],
      else: [
        { type: "message", text: "今年で四十一回目の巡礼だけど、碑に「霧が町を呑む」と出たそうでね。もう帰ろうかと思ってたんだよ。", speaker: "巡礼者" },
        {
          type: "message",
          text: "でも、不思議なんだ。巡礼歌の四番には「霧は町を抱き　灯をつつむ」とある。碑の言葉と、正反対なんだよ。",
          speaker: "巡礼者",
        },
        {
          type: "message",
          text: "みんな怖いから、碑を信じるほうが楽なんだろうねえ。怖い理由があれば、逃げる言い訳もできるから。",
          speaker: "巡礼者",
        },
      ],
    },
  ];
}

function scribeCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter5_ledger_found",
      equals: true,
      then: [
        { type: "message", text: "原本と写しの綴りが合わない……。書き手の癖まで、真似ていたのですね。", speaker: "書記" },
        { type: "message", text: "もう、黙っていません。私が見たことは、すべてお話しします。", speaker: "書記" },
      ],
      else: [
        { type: "message", text: "私は聖堂の書記、ユキヒサです。記録の間の書き写しも、私の役目でして。", speaker: "書記" },
        {
          type: "message",
          text: "六年ほど前から、古い巻物の一部が「修復」の名目で、灯芯都から来た写字官の方に預けられているのです。",
          speaker: "書記",
        },
        {
          type: "message",
          text: "返ってきた巻物は、文字の癖が、ほんの少し違いました。気のせいだと思って……黙っていたのです。怖くて。",
          speaker: "書記",
        },
        { type: "message", text: "灯芯都から……？", speaker: "レト" },
        {
          type: "message",
          text: "責めやしないさ。気づいて黙ってた人間を責めたら、世の中の九割は罪人だ。だが、これからは黙らないでくれ。",
          speaker: "レト",
        },
      ],
    },
  ];
}

function recordCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter5_record_found",
      equals: true,
      then: [{ type: "message", text: "書き換えられた碑文の写し。「静まりの年」の欄だけ、インクの色が違う。" }],
      else: [
        { type: "message", text: "閲覧机に、予言の碑文の写しが広げられている。統暦392年、「静まりの年」の欄に目が留まった。" },
        {
          type: "message",
          text: "「この年、灯芯都にて、疫病の噂あり。町は静まり、人々は語らず」……疫病じゃない。「噂あり」としか書いてない。",
          speaker: "レト",
        },
        {
          type: "message",
          text: "この欄だけ、インクが新しいです。それに、行の間隔が詰まっています。長い文を削って、詰め直したみたい。",
          speaker: "ミナ",
        },
        {
          type: "message",
          text: "削られた跡から、元の文字がうっすら読める。「この年、合議会の要人、四名が職を退き、うち三名は行方を絶つ」……。",
          speaker: "ユーリ",
        },
        {
          type: "message",
          text: "合議会の要人が、一度に三人も消えた……？ それを隠したい誰かが、「疫病の噂」に置き換えたんだ。",
          speaker: "レト",
        },
        { type: "message", text: "レトの声は平らだった。平らすぎるほど、平らだった。" },
        { type: "setFlag", flag: "chapter5_record_found", value: true },
        { type: "message", text: "疫病じゃなくて、人が消えた……。あたしの従兄の件と、同じにおいがする。", speaker: "コハク" },
        { type: "message", text: "……書き換えた者は、書き手より上の人間だ。そうでなければ、消せん。", speaker: "オルカ" },
      ],
    },
  ];
}

function ledgerCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter5_ledger_found",
      equals: true,
      then: [{ type: "message", text: "書架の奥の綴り。祖父の名が記された一枚は、預かっておこう。" }],
      else: [
        {
          type: "if",
          flag: "chapter5_record_found",
          equals: true,
          then: [
            {
              type: "message",
              text: "書架の最下段に、布で包まれた古い綴りが隠されていた。封蝋は割れて粉になっている。書き換えられる前の、原本のようだ。",
            },
            {
              type: "message",
              text: "「統暦三九二年　合議会人事異動の件。一、合議会員四名、職を退く。一、うち三名は所在不明。一、碑への記載は、疫病の噂の一行にとどめる」",
            },
            {
              type: "message",
              text: "失踪した三名の名が、縦に並んでいる。ハクエイ。トウマ。その一番下の名前に、ユーリの目が止まった。",
            },
            { type: "message", text: "「ソウイチ」……。祖父の名前だ。", speaker: "ユーリ" },
            {
              type: "message",
              text: "名の脇に、小さな肩書がある。「灯里出身。元・相談所調査員。合議会員として二期目」。その下に、「ほか、随行の者数名。名は略す」。",
            },
            {
              type: "message",
              text: "灯里の調査員から、合議会員に……。そして、消された三人のうちの一人か。",
              speaker: "レト",
            },
            {
              type: "message",
              text: "ユーリ。怒っても、泣いても、分からないままでもいいんです。折れたところは、みんなで支えますから。",
              speaker: "ミナ",
            },
            {
              type: "message",
              text: "お前の祖父さんは、まっすぐな人だったんだろう。だから消された。……重さは、みんなで分けよう。",
              speaker: "レト",
            },
            { type: "message", text: "ユーリ、顔を上げて。あたしたちが、ついてるんだから。", speaker: "コハク" },
            { type: "message", text: "……重い荷は、持ち手が多いほど軽くなる。", speaker: "オルカ" },
            { type: "setFlag", flag: "chapter5_ledger_found", value: true },
          ],
          else: [{ type: "message", text: "古い綴りの棚だ。まずは、閲覧机の碑文の写しを確かめたほうがよさそうだ。" }],
        },
      ],
    },
  ];
}

function keeperCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter5_yugami_defeated",
      equals: true,
      then: [
        {
          type: "message",
          text: "写字官のオウギは、床に膝をついたまま動かない。「碑は、私が元の形に戻します」と、小さくつぶやいた。",
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter5_ledger_found",
          equals: true,
          then: [
            { type: "message", text: "「……原本を見つけてしまいましたか」――黒いローブの男が、書架の陰から振り向いた。" },
            {
              type: "message",
              text: "写字官のオウギと申します。合議会書庫局から派遣されております。碑を書き換えたのは、私です。",
              speaker: "写字官",
            },
            {
              type: "message",
              text: "誰の命令で、こんなことを！ 行方を絶った三人の中に、ぼくの祖父がいるんです。",
              speaker: "ユーリ",
            },
            {
              type: "message",
              text: "ソウイチさま……削るようにと渡された、名の一覧にありました。私は、人が消えていたと、初めて知ったのです。",
              speaker: "写字官",
            },
            {
              type: "message",
              text: "命じたのは、灯芯都の高い場所におられる方です。お名前は存じません。文には「記録を、正しい形に」と。",
              speaker: "写字官",
            },
            {
              type: "message",
              text: "灯芯都には、娘がおります。「保護」の名の人質です。私は、従うほかなかった……。",
              speaker: "写字官",
            },
            {
              type: "message",
              text: "まだ間に合います。碑を元に戻して、娘さんのことは、ぼくたちが相談所に伝えます。",
              speaker: "ユーリ",
            },
            {
              type: "message",
              text: "だめです。あの方は、すべてご存じなのです。……すまない、すまない。",
              speaker: "写字官",
            },
            {
              type: "message",
              text: "写字官が黒い灯り石を握りつぶすと、碑文の文字が霧になって立ち上がり、歪みの姿になった！",
            },
            { type: "setFlag", flag: "chapter5_keeper_met", value: true },
            { type: "startBattle", battleId: "kiri-yugami" },
          ],
          else: [{ type: "message", text: "黒いローブの男が、書架の前で巻物を整理している。今は話しかけづらい雰囲気だ。" }],
        },
      ],
    },
  ];
}
