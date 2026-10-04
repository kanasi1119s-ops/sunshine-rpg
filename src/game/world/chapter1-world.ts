import {
  createMugikanoVillageData,
  MUGIKANO_VILLAGE_LANDMARKS,
} from "../map/chapter1/mugikano-village";
import {
  createMugikanoWaterSourceData,
  MUGIKANO_WATER_SOURCE_LANDMARKS,
} from "../map/chapter1/mugikano-water-source";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第1章（麦香野）の世界。`docs/story/structure.md`「第1章（麦香野）」・
 * `docs/story/mystery.md`（真相）・`docs/story/clue-ledger.md`（伏線 C-002）を反映。
 */
export const CHAPTER1_MAPS: Record<string, TileMapData> = {
  "mugikano-village": createMugikanoVillageData(),
  "mugikano-water-source": createMugikanoWaterSourceData(),
};

/**
 * 麦香野へ到着したとき、一度だけ流す短い場面つなぎ（`chapter1_intro_seen` フラグで管理）。
 */
export const CHAPTER1_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――数日後、麦香野。" },
  {
    type: "message",
    text: "灯里での一件を灯芯都へ報告したカセンの指示で、ユーリとレトは次の依頼地・麦香野へ向かった。",
  },
  {
    type: "message",
    text: "村に着くなり、慌ただしい様子の村人たちに出迎えられる。水路の水が、突然涸れてしまったのだという。",
  },
  { type: "setFlag", flag: "chapter1_intro_seen", value: true },
];

export const CHAPTER1_NPCS: Record<string, Npc[]> = {
  "mugikano-village": [
    {
      id: "mugikano-elder",
      tileX: MUGIKANO_VILLAGE_LANDMARKS.elder.tileX,
      tileY: MUGIKANO_VILLAGE_LANDMARKS.elder.tileY,
      color: "#8a7a4a",
      commands: elderCommands(),
    },
    {
      id: "mugikano-mina",
      tileX: MUGIKANO_VILLAGE_LANDMARKS.mina.tileX,
      tileY: MUGIKANO_VILLAGE_LANDMARKS.mina.tileY,
      color: "#5a9ac9",
      spriteName: "ミナ",
      commands: minaCommands(),
    },
  ],
  "mugikano-water-source": [
    {
      id: "mugikano-excavation-mark",
      tileX: MUGIKANO_WATER_SOURCE_LANDMARKS.excavationMark.tileX,
      tileY: MUGIKANO_WATER_SOURCE_LANDMARKS.excavationMark.tileY,
      color: "#8a7a5a",
      commands: excavationMarkCommands(),
    },
    {
      id: "mugikano-yugami",
      tileX: MUGIKANO_WATER_SOURCE_LANDMARKS.yugami.tileX,
      tileY: MUGIKANO_WATER_SOURCE_LANDMARKS.yugami.tileY,
      color: "#8a4fd6",
      commands: mugikanoYugamiCommands(),
    },
  ],
};

function elderCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter1_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter1_reported_to_elder",
          equals: true,
          then: [
            {
              type: "message",
              text: "水路の水も戻って、村もようやく落ち着いたよ。ありがとうな、ふたりとも。",
              speaker: "村長",
            },
          ],
          else: [
            {
              type: "if",
              flag: "chapter1_excavation_found",
              equals: true,
              then: [
                { type: "message", text: "戻ったか。水源はどうだった？", speaker: "村長" },
                {
                  type: "message",
                  text: "しずめてきました。それと、水源の奥に、古い採掘の跡のようなものがありました。",
                  speaker: "ユーリ",
                },
                { type: "message", text: "……採掘跡？", speaker: "村長" },
                {
                  type: "message",
                  text: "灯里の町外れで見た焼け跡と、似た感じがするんです。あそこも、歪みが起きた場所でした。",
                  speaker: "ユーリ",
                },
                {
                  type: "message",
                  text: "歪みが出る場所には、決まって古い灯り石の採掘跡がある……そういうことか？",
                  speaker: "レト",
                },
                {
                  type: "message",
                  text: "偶然、では片付けられなさそうだな。カセンさんにも報告しておいた方がいい。",
                  speaker: "レト",
                },
                { type: "setFlag", flag: "chapter1_clue_c002_found", value: true },
                {
                  type: "message",
                  text: "とにかく、水路の水が戻ってくれて助かったよ。本当にありがとう。",
                  speaker: "村長",
                },
                { type: "setFlag", flag: "chapter1_reported_to_elder", value: true },
              ],
              else: [
                { type: "message", text: "戻ったか。水源はどうだった？", speaker: "村長" },
                {
                  type: "message",
                  text: "しずめてきましたが……もう一度、水源の奥をよく見てみようと思います。",
                  speaker: "ユーリ",
                },
              ],
            },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter1_quest_accepted",
          equals: true,
          then: [
            {
              type: "message",
              text: "北の水源、頼んだよ。危ないと思ったら、決して無理はしないでおくれ。",
              speaker: "村長",
            },
          ],
          else: [
            { type: "message", text: "灯りの相談所の人たちかい。よく来てくれた……！", speaker: "村長" },
            {
              type: "message",
              text: "数日前から、村の水路の水が急に涸れてしまってな。水車小屋の水も止まって、みんな気が立っているんだ。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "このままだと、田畑を持つ家と水車小屋の間で、いさかいになりかねない。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "水路の水は、北の水源から引いている。ところが、ここ何日か、夜になると水源の方から低い唸り声のようなものが聞こえるんだ。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "水車小屋の主が、水源のあたりで紫色の光が揺れるのを見たとも言っている。町で言う「歪み」が、水の流れを乱しているのかもしれん。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "歪みというのは、灯り石の力が乱れて形を持ったもの。放っておけば、水源そのものが駄目になってしまう。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "水源の様子を見てきてほしい。北の道を行った先だ。もし歪みがいたら、しずめてもらえると助かる。それと、水が涸れた原因になりそうなものがないか、よく見てきておくれ。",
              speaker: "村長",
            },
            {
              type: "choice",
              text: "依頼を受けますか？",
              options: [
                {
                  label: "受けます",
                  commands: [
                    { type: "setFlag", flag: "chapter1_quest_accepted", value: true },
                    { type: "message", text: "わかりました。見てきます。", speaker: "ユーリ" },
                    {
                      type: "message",
                      text: "頼む。……ああ、それと、ミナという村の子が心配して自分で見に行きたがっていてな。危ないから止めてはいるんだが……",
                      speaker: "村長",
                    },
                    { type: "message", text: "念のため、あの子にも声をかけてやってくれないか。", speaker: "村長" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [
                    {
                      type: "message",
                      text: "そうか……。でも、あまり長くは待てそうにないんだ。頼むよ。",
                      speaker: "村長",
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function minaCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter1_mina_joined",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter1_mina_friend_hint_seen",
          equals: true,
          then: [
            {
              type: "message",
              text: "次はどこに行きましょうか。わたしも、できる限りお手伝いします。",
              speaker: "ミナ",
            },
          ],
          else: [
            { type: "message", text: "水源が元に戻って、本当によかったです。", speaker: "ミナ" },
            { type: "message", text: "……あの、歪みって、人を襲うことも、あるんですよね。", speaker: "ミナ" },
            { type: "message", text: "え、ええ。今回は、幸い誰も襲われていませんでしたが……", speaker: "ユーリ" },
            { type: "message", text: "そう、ですよね。……すみません、変なことを聞いて。", speaker: "ミナ" },
            {
              type: "message",
              text: "（ミナは、一瞬だけ表情を曇らせた。……何か、思うところがあるのかもしれない）",
            },
            { type: "message", text: "……おい、今の顔。何か知ってるのか？", speaker: "レト" },
            {
              type: "message",
              text: "……いえ、なんでもないです！　それより、次はどこに向かうんですか？",
              speaker: "ミナ",
            },
            { type: "setFlag", flag: "chapter1_mina_friend_hint_seen", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter1_reported_to_elder",
          equals: true,
          then: [
            {
              type: "message",
              text: "水源、直してきてくださったんですね。ありがとうございます……！",
              speaker: "ミナ",
            },
            {
              type: "message",
              text: "あの、わたしも水紋系の力が少し使えるんです。よかったら、これからの調査、ご一緒させてもらえませんか？",
              speaker: "ミナ",
            },
            { type: "message", text: "村のみんなのためにも、わたしにできることをしたくて……。", speaker: "ミナ" },
            {
              type: "choice",
              text: "ミナの申し出にどう答える？",
              options: [
                {
                  label: "一緒に来てください",
                  commands: [
                    { type: "message", text: "はい！　足を引っ張らないよう、頑張ります。", speaker: "ミナ" },
                    { type: "setFlag", flag: "chapter1_mina_joined", value: true },
                  ],
                },
                {
                  label: "危ないから村に残ってください",
                  commands: [
                    {
                      type: "message",
                      text: "……そう、ですよね。でも、やっぱり、力になりたいです。気が変わったら、いつでも声をかけてください。",
                      speaker: "ミナ",
                    },
                  ],
                },
              ],
            },
          ],
          else: [
            {
              type: "if",
              flag: "chapter1_quest_accepted",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "水源のこと、お願いしますね。……本当は、わたしも一緒に行きたいんですけど。",
                  speaker: "ミナ",
                },
                { type: "message", text: "村長さんに止められてしまって。大人しく待ってます。", speaker: "ミナ" },
              ],
              else: [
                { type: "message", text: "はじめまして。麦香野で生まれ育った、ミナといいます。", speaker: "ミナ" },
                {
                  type: "message",
                  text: "水路の水が涸れてしまって……みんな心配しているんです。何とかなるといいんですが。",
                  speaker: "ミナ",
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function excavationMarkCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter1_excavation_found",
      equals: true,
      then: [{ type: "message", text: "掘り返された古い跡が、静かに広がっている。" }],
      else: [
        { type: "message", text: "地面が大きく掘り返されている。随分と古い跡のようだ。" },
        { type: "message", text: "……これは、灯り石の採掘跡？　こんな所に？" },
        { type: "setFlag", flag: "chapter1_excavation_found", value: true },
      ],
    },
  ];
}

function mugikanoYugamiCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter1_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "水源はすっかり静かになった。水も、少しずつ戻り始めている。" }],
      else: [
        { type: "message", text: "涸れた水源の奥、掘り返された土の中から、何かがうごめいている。" },
        { type: "message", text: "「歪み」が、姿を現した！" },
        { type: "startBattle", battleId: "mugikano-yugami" },
      ],
    },
  ];
}
