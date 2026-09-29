import { createSanoneCampData, SANONE_CAMP_LANDMARKS } from "../map/chapter4/sanone-camp";
import { createSanoneTownData, SANONE_TOWN_LANDMARKS } from "../map/chapter4/sanone-town";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第4章（砂音）の世界。`docs/story/structure.md`「第4章（砂音）」・`docs/story/mystery.md`を反映。
 * 伏線 C-005（ガイドの潔白）の回収と C-008（合議会関係者の噂）を実装（roadmap 4-17）。
 * ボス戦は4-18で追加（専用BGMは4-19まで、第3章のボス曲を仮に流用）。
 */
export const CHAPTER4_MAPS: Record<string, TileMapData> = {
  "sanone-town": createSanoneTownData(),
  "sanone-camp": createSanoneCampData(),
};

/** 砂音へ到着したとき、一度だけ流す場面つなぎ（`chapter4_intro_seen` フラグで管理）。 */
export const CHAPTER4_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――砂の海に浮かぶ、隊商の都・砂音。" },
  {
    type: "message",
    text: "鉄鏈鉱山で見つけた「静まりの年」の紙切れ。その手がかりを求めて、ユーリたちは物資の集まるこの町を訪ねた。",
  },
  {
    type: "message",
    text: "町は隊商の荷が行き交い、にぎやかだ。けれど組合の天幕のあたりでは、大人たちが険しい顔で言い争っている。",
  },
  { type: "setFlag", flag: "chapter4_intro_seen", value: true },
];

export const CHAPTER4_NPCS: Record<string, Npc[]> = {
  "sanone-town": [
    {
      id: "sanone-guildmaster",
      tileX: SANONE_TOWN_LANDMARKS.guildMaster.tileX,
      tileY: SANONE_TOWN_LANDMARKS.guildMaster.tileY,
      color: "#8a5a3a",
      commands: guildMasterCommands(),
    },
    {
      id: "sanone-merchant",
      tileX: SANONE_TOWN_LANDMARKS.merchant.tileX,
      tileY: SANONE_TOWN_LANDMARKS.merchant.tileY,
      color: "#6a8a5a",
      commands: merchantCommands(),
    },
    {
      id: "sanone-informant",
      tileX: SANONE_TOWN_LANDMARKS.informant.tileX,
      tileY: SANONE_TOWN_LANDMARKS.informant.tileY,
      color: "#4a4a5a",
      commands: informantCommands(),
    },
  ],
  "sanone-camp": [
    {
      id: "sanone-wagon",
      tileX: SANONE_CAMP_LANDMARKS.wagon.tileX,
      tileY: SANONE_CAMP_LANDMARKS.wagon.tileY,
      color: "#7a5a3a",
      commands: wagonCommands(),
    },
    {
      id: "sanone-dorun",
      tileX: SANONE_CAMP_LANDMARKS.dorun.tileX,
      tileY: SANONE_CAMP_LANDMARKS.dorun.tileY,
      color: "#5a3a6a",
      spriteName: "ドルン",
      commands: dorunCommands(),
    },
  ],
};

function guildMasterCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_reported",
      equals: true,
      then: [
        {
          type: "message",
          text: "帆走車は好きに使ってくれ。組合として、あんたたちの旅を応援するよ。",
          speaker: "組合長",
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter4_quest_accepted",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter4_yugami_defeated",
              equals: true,
              then: [
                { type: "message", text: "……野営地で、あの男に会ったのか。詳しく聞かせてくれ。", speaker: "組合長" },
                {
                  type: "message",
                  text: "荷馬車の帳面は、組合の印を偽って書かれていた。荷の出どころに、名前の使われた者がいるんだ。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "ガイドくん。硝子湖の元締めは、君の従兄だと噂されていたね。……済まない、私も一度は疑った。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "だが帳面の筆跡は従兄殿のものではなかった。従兄殿は名前を勝手に使われていただけだ。君も無関係だと、はっきりした。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "……そうか。よかった。ずっと胸につかえていたんだ。",
                  speaker: "ガイド",
                },
                { type: "message", text: "（これで、疑いは晴れたんだね）", speaker: "ミナ" },
                { type: "setFlag", flag: "chapter4_guide_cleared", value: true },
                {
                  type: "message",
                  text: "礼に、組合の帆走車を貸そう。砂の上でも、風に乗ってどこまでも走れる。",
                  speaker: "組合長",
                },
                { type: "setFlag", flag: "chapter4_sailcar_obtained", value: true },
                {
                  type: "message",
                  text: "そのとき、天幕に旅装の使者が駆け込んできた。胸に、灯芯都の合議会の紋章がある。",
                },
                {
                  type: "message",
                  text: "灯りの相談所の皆さまですね。合議会代表・エドレアが、あなた方にお会いしたいと申しております。",
                  speaker: "使者",
                },
                {
                  type: "message",
                  text: "……合議会の代表が、僕たちに? 何のために……。",
                  speaker: "ユーリ",
                },
                {
                  type: "message",
                  text: "詳しくは、灯芯都でお伝えするとのことです。どうか、お越しください。",
                  speaker: "使者",
                },
                { type: "setFlag", flag: "chapter4_reported", value: true },
              ],
              else: [
                {
                  type: "message",
                  text: "調査は、南の野営地の荷馬車列から頼む。あそこの帳面に、答えがあるはずだ。",
                  speaker: "組合長",
                },
              ],
            },
          ],
          else: [
            { type: "message", text: "旅の調査員かね。私は隊商組合の長だ。", speaker: "組合長" },
            {
              type: "message",
              text: "近ごろ、隊商同士が「あいつらが抜け荷をしている」と疑い合っていてな。組合が割れかけている。",
              speaker: "組合長",
            },
            {
              type: "message",
              text: "だが、抜け荷の荷は本物だ。誰かが、隊商の荷にこっそり別の荷を混ぜている。",
              speaker: "組合長",
            },
            {
              type: "choice",
              text: "野営地の荷馬車列を調べますか?",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter4_quest_accepted", value: true },
                    { type: "message", text: "任せてください。", speaker: "ユーリ" },
                    { type: "message", text: "頼もしいな。野営地は、町の南の門の先だ。", speaker: "組合長" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [{ type: "message", text: "決まったら、また声をかけてくれ。", speaker: "組合長" }],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function merchantCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_sailcar_obtained",
      equals: true,
      then: [{ type: "message", text: "帆走車かい。風をつかまえるコツは、帆を欲張らないことさ。", speaker: "商人" }],
      else: [
        { type: "message", text: "いらっしゃい! 砂漠の香辛料に、干した果物、なんでもあるよ。", speaker: "商人" },
        {
          type: "message",
          text: "ただ最近、荷の数が帳面と合わなくてねえ。隊商のあいだで、みんな疑心暗鬼さ。",
          speaker: "商人",
        },
      ],
    },
  ];
}

function informantCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_rumor_heard",
      equals: true,
      then: [{ type: "message", text: "噂は噂さ。信じるも信じないも、あんたたち次第だよ。", speaker: "情報屋" }],
      else: [
        { type: "message", text: "おっと、灯りの相談所の人かい。耳寄りな話がある。銭はいらないよ。", speaker: "情報屋" },
        {
          type: "message",
          text: "隊商の抜け荷を仕切ってる男の後ろに、もっと上の依頼主がいる、って噂だ。それも、灯芯都の合議会に近い人物らしい。",
          speaker: "情報屋",
        },
        { type: "message", text: "合議会の……? まさか。", speaker: "レト" },
        { type: "message", text: "あくまで噂だよ。名前までは、わたしの耳にも入らない。", speaker: "情報屋" },
        { type: "setFlag", flag: "chapter4_rumor_heard", value: true },
      ],
    },
  ];
}

function wagonCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_wagon_found",
      equals: true,
      then: [{ type: "message", text: "荷馬車の帳面は、預かった。組合長に見せよう。" }],
      else: [
        { type: "message", text: "野営地の荷馬車の底に、二重の板が仕込まれている。中から、灯り石の木箱が出てきた。" },
        { type: "message", text: "帳面には、組合の印が押してある。でも、この印……少し歪んでないか?", speaker: "ミナ" },
        { type: "message", text: "偽の印だ。隊商のせいにして、荷を流している者がいる。", speaker: "ユーリ" },
        { type: "setFlag", flag: "chapter4_wagon_found", value: true },
      ],
    },
  ];
}

function dorunCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "男の姿はもうない。砂の上に、足跡だけが残っている。" }],
      else: [
        {
          type: "if",
          flag: "chapter4_wagon_found",
          equals: true,
          then: [
            { type: "message", text: "「おや、荷馬車の底を見つけましたか。さすがですね」――ドルンが、天幕の陰から現れた。" },
            { type: "message", text: "また君か! 今度は何を企んでいる!", speaker: "レト" },
            {
              type: "message",
              text: "隊商の荷に別の荷を混ぜる。簡単な仕事ですよ。私は、頼まれた仕事をこなしているだけです。",
              speaker: "ドルン",
            },
            { type: "message", text: "頼まれた……? 誰に頼まれた!", speaker: "ユーリ" },
            {
              type: "message",
              text: "それは言えません。ただ、私の上にも、さらに上の方がいる。とだけ申し上げておきましょう。",
              speaker: "ドルン",
            },
            {
              type: "message",
              text: "ドルンが荷の灯り石を蹴り砕くと、砂が渦を巻いて立ち上がり、歪みの姿になった！",
            },
            { type: "setFlag", flag: "chapter4_dorun_met", value: true },
            { type: "startBattle", battleId: "sanone-yugami" },
          ],
          else: [{ type: "message", text: "焚き火のそばで、見慣れない男が背を向けて座っている。今は話しかけづらい雰囲気だ。" }],
        },
      ],
    },
  ];
}
