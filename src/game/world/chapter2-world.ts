import {
  createGarasukoTownData,
  GARASUKO_TOWN_LANDMARKS,
} from "../map/chapter2/garasuko-town";
import {
  createGarasukoWarehouseData,
  GARASUKO_WAREHOUSE_LANDMARKS,
} from "../map/chapter2/garasuko-warehouse";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第2章（硝子湖）の世界。`docs/story/structure.md`「第2章（硝子湖）」・
 * `docs/story/mystery.md`（ドルンの初登場）・`docs/story/clue-ledger.md`
 * （伏線 C-003・C-004・C-005）を反映。
 */
export const CHAPTER2_MAPS: Record<string, TileMapData> = {
  "garasuko-town": createGarasukoTownData(),
  "garasuko-warehouse": createGarasukoWarehouseData(),
};

/**
 * 硝子湖へ到着したとき、一度だけ流す短い場面つなぎ（`chapter2_intro_seen` フラグで管理）。
 */
export const CHAPTER2_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――湖上の交易都市、硝子湖。" },
  {
    type: "message",
    text: "麦香野での一件をカセンへ報告した帰り、灯り石の密輸が絡む事件の噂を耳にしたユーリたちは、硝子湖に立ち寄ることにした。",
  },
  {
    type: "message",
    text: "湖に張り出した桟橋の先に、使われなくなったはずの倉庫がある。最近、そこに人の出入りがあるらしい。",
  },
  { type: "setFlag", flag: "chapter2_intro_seen", value: true },
];

export const CHAPTER2_NPCS: Record<string, Npc[]> = {
  "garasuko-town": [
    {
      id: "garasuko-guide",
      tileX: GARASUKO_TOWN_LANDMARKS.guide.tileX,
      tileY: GARASUKO_TOWN_LANDMARKS.guide.tileY,
      color: "#5a9ac9",
      spriteName: "ガイド",
      commands: guideCommands(),
    },
  ],
  "garasuko-warehouse": [
    {
      id: "garasuko-crate-pile",
      tileX: GARASUKO_WAREHOUSE_LANDMARKS.cratePile.tileX,
      tileY: GARASUKO_WAREHOUSE_LANDMARKS.cratePile.tileY,
      color: "#8a6a3f",
      commands: cratePileCommands(),
    },
    {
      id: "garasuko-dorun",
      tileX: GARASUKO_WAREHOUSE_LANDMARKS.dorun.tileX,
      tileY: GARASUKO_WAREHOUSE_LANDMARKS.dorun.tileY,
      color: "#5a3a6a",
      spriteName: "ドルン",
      commands: dorunCommands(),
    },
  ],
};

function guideCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter2_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter2_reported_to_guide",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter2_guide_cousin_hint_seen",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "次はどっちへ行く？ 案内なら任せてよ。",
                  speaker: "ガイド",
                },
              ],
              else: [
                { type: "message", text: "……なあ、さっきの男、名前くらいは知ってるんだろ？", speaker: "レト" },
                {
                  type: "message",
                  text: "え？ いや、あんな怪しい奴、知り合うわけないでしょ。……知らないよ、本当に。",
                  speaker: "ガイド",
                },
                {
                  type: "message",
                  text: "（少し早口だった。……気のせい、かしら）",
                  speaker: "ミナ",
                },
                { type: "setFlag", flag: "chapter2_guide_cousin_hint_seen", value: true },
              ],
            },
          ],
          else: [
            { type: "message", text: "……あの怪しい男、まんまと逃げられたか。悔しいなあ。", speaker: "ガイド" },
            {
              type: "message",
              text: "でも、倉庫の灯り石は片付いた。これで湖の商売も、少しは落ち着くはず。ありがとう、助かったよ。",
              speaker: "ガイド",
            },
            {
              type: "message",
              text: "あたしも、家業のためにずっとこの件を追ってたの。……正直、一人じゃここまで来られなかった。",
              speaker: "ガイド",
            },
            {
              type: "choice",
              text: "ガイドの申し出にどう答える？",
              options: [
                {
                  label: "一緒に来てほしい",
                  commands: [
                    {
                      type: "message",
                      text: "話が早いな。損はさせないよ、これから先は仲間として付き合うから。",
                      speaker: "ガイド",
                    },
                    { type: "setFlag", flag: "chapter2_guide_joined", value: true },
                  ],
                },
                {
                  label: "商会の仕事を優先してほしい",
                  commands: [
                    {
                      type: "message",
                      text: "……そうか。まあ、気が変わったらいつでも声をかけて。桟橋のあたりにいるから。",
                      speaker: "ガイド",
                    },
                  ],
                },
              ],
            },
            { type: "setFlag", flag: "chapter2_reported_to_guide", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter2_quest_accepted",
          equals: true,
          then: [
            {
              type: "message",
              text: "頼んだよ。桟橋の先の倉庫だから、気をつけてね。",
              speaker: "ガイド",
            },
          ],
          else: [
            { type: "message", text: "見ない顔だね。旅の調査員か何か？", speaker: "ガイド" },
            {
              type: "message",
              text: "実は、湖の向こう、桟橋の先の倉庫で妙な動きがあってね。灯り石が絡んでるらしいって噂を聞いて、放っておけなくて。",
              speaker: "ガイド",
            },
            {
              type: "message",
              text: "うちは代々、この湖で交易をやってる家でね。おかしな噂が立つのは商売の邪魔なのよ。",
              speaker: "ガイド",
            },
            {
              type: "choice",
              text: "一緒に倉庫を調べますか？",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter2_quest_accepted", value: true },
                    { type: "message", text: "わかった。見てくる。", speaker: "ユーリ" },
                    {
                      type: "message",
                      text: "助かる。あたしは町の用があるから、ここで待ってるね。",
                      speaker: "ガイド",
                    },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [
                    {
                      type: "message",
                      text: "急がなくてもいいけど、あんまり長引くと湖の人たちが困るの。頼むよ。",
                      speaker: "ガイド",
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

function cratePileCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter2_crates_found",
      equals: true,
      then: [{ type: "message", text: "片付けられた木箱の跡が残っている。" }],
      else: [
        { type: "message", text: "木箱の山だ。中を覗くと、灯り石がぎっしりと詰め込まれている。" },
        { type: "message", text: "……こんな量、とても普通の交易品とは思えない。" },
        { type: "setFlag", flag: "chapter2_crates_found", value: true },
      ],
    },
  ];
}

function dorunCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter2_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "倉庫はすっかり静かになった。木箱の灯り石も、もう暴れ出す気配はない。" }],
      else: [
        { type: "message", text: "闇の中から、静かな声がした。「……客とは珍しい」" },
        { type: "message", text: "姿を見せたのは、人当たりのよさそうな、それでいてどこか底の読めない男だった。", speaker: "ユーリ" },
        {
          type: "message",
          text: "驚かせたね。俺はただの仲介人さ。この荷物の面倒を見てるだけの、な。",
          speaker: "ドルン",
        },
        { type: "setFlag", flag: "chapter2_clue_c003_found", value: true },
        { type: "message", text: "灯り石をこんなに集めて、一体何をするつもりだ？", speaker: "レト" },
        {
          type: "message",
          text: "さあね。……っと、そろそろお暇するとしよう。荷物の始末は、こいつに任せた。",
          speaker: "ドルン",
        },
        { type: "message", text: "男が木箱に軽く触れると、積まれた灯り石が唸りを上げて歪み始めた！" },
        {
          type: "message",
          text: "悪いが、灯芯都からの依頼でね。……邪魔はさせないよ。",
          speaker: "ドルン",
        },
        { type: "setFlag", flag: "chapter2_clue_c004_found", value: true },
        { type: "message", text: "男はそう言い残し、闇の中へ姿を消した。" },
        { type: "startBattle", battleId: "garasuko-yugami" },
      ],
    },
  ];
}
