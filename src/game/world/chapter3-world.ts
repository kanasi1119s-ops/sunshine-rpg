import { createTetsukusariMineData, TETSUKUSARI_MINE_LANDMARKS } from "../map/chapter3/tetsukusari-mine";
import { createTetsukusariTownData, TETSUKUSARI_TOWN_LANDMARKS } from "../map/chapter3/tetsukusari-town";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第3章（鉄鏈鉱山）の世界。`docs/story/structure.md`「第3章（鉄鏈鉱山）」・
 * `docs/story/mystery.md`・`docs/story/clue-ledger.md`（伏線 C-006・C-007）を反映。
 */
export const CHAPTER3_MAPS: Record<string, TileMapData> = {
  "tetsukusari-town": createTetsukusariTownData(),
  "tetsukusari-mine": createTetsukusariMineData(),
};

/** 鉄鏈鉱山へ到着したとき、一度だけ流す短い場面つなぎ（`chapter3_intro_seen` フラグで管理）。 */
export const CHAPTER3_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――灯り石の鉱山町、鉄鏈鉱山。" },
  {
    type: "message",
    text: "硝子湖の一件のあと、ユーリたちは「灯り石の出どころ」を確かめるため、大陸いちの産地であるこの町を訪ねた。",
  },
  {
    type: "message",
    text: "ところが町は、鉱山会社と労働組合の言い争いでぴりぴりしている。北の崖の坑道は、もう何日も閉ざされているらしい。",
  },
  { type: "setFlag", flag: "chapter3_intro_seen", value: true },
];

export const CHAPTER3_NPCS: Record<string, Npc[]> = {
  "tetsukusari-town": [
    {
      id: "tetsukusari-orca",
      tileX: TETSUKUSARI_TOWN_LANDMARKS.orca.tileX,
      tileY: TETSUKUSARI_TOWN_LANDMARKS.orca.tileY,
      color: "#7a5a3a",
      spriteName: "オルカ",
      commands: orcaCommands(),
    },
    {
      id: "tetsukusari-clerk",
      tileX: TETSUKUSARI_TOWN_LANDMARKS.officeClerk.tileX,
      tileY: TETSUKUSARI_TOWN_LANDMARKS.officeClerk.tileY,
      color: "#6a7a8a",
      commands: clerkCommands(),
    },
    {
      id: "tetsukusari-miner",
      tileX: TETSUKUSARI_TOWN_LANDMARKS.miner.tileX,
      tileY: TETSUKUSARI_TOWN_LANDMARKS.miner.tileY,
      color: "#9a8a5a",
      commands: minerCommands(),
    },
  ],
  "tetsukusari-mine": [
    {
      id: "tetsukusari-machine",
      tileX: TETSUKUSARI_MINE_LANDMARKS.machine.tileX,
      tileY: TETSUKUSARI_MINE_LANDMARKS.machine.tileY,
      color: "#5a4a70",
      commands: machineCommands(),
    },
    {
      id: "tetsukusari-dorun",
      tileX: TETSUKUSARI_MINE_LANDMARKS.dorun.tileX,
      tileY: TETSUKUSARI_MINE_LANDMARKS.dorun.tileY,
      color: "#5a3a6a",
      spriteName: "ドルン",
      commands: dorunCommands(),
    },
  ],
};

function orcaCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter3_reported_to_orca",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter3_orca_hint_seen",
              equals: true,
              then: [{ type: "message", text: "……行くぞ。立ち止まっている暇はない。", speaker: "オルカ" }],
              else: [
                { type: "message", text: "オルカさん、坑道の入口をずっと見てましたね。", speaker: "ミナ" },
                { type: "message", text: "……昔、あそこで落盤があった。それだけだ。", speaker: "オルカ" },
                { type: "message", text: "（それだけ、という顔ではなかった）", speaker: "レト" },
                { type: "setFlag", flag: "chapter3_orca_hint_seen", value: true },
              ],
            },
          ],
          else: [
            {
              type: "message",
              text: "……話は聞いた。装置も、あの紙切れも。組合の仲間が、こんなものに使われていたとはな。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "会社との言い争いは、目くらましだったのか。……俺が気づくべきだった。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "礼を言う。それと、頼みがある。この件の続きを追うなら、俺も連れていけ。",
              speaker: "オルカ",
            },
            {
              type: "choice",
              text: "オルカの申し出にどう答える？",
              options: [
                {
                  label: "一緒に来てほしい",
                  commands: [
                    { type: "message", text: "……俺がやる。足は引っ張らん。", speaker: "オルカ" },
                    { type: "setFlag", flag: "chapter3_orca_joined", value: true },
                  ],
                },
                {
                  label: "まず町のことを優先してほしい",
                  commands: [
                    {
                      type: "message",
                      text: "……そうか。気が変わったら、詰め所に来い。",
                      speaker: "オルカ",
                    },
                  ],
                },
              ],
            },
            { type: "setFlag", flag: "chapter3_reported_to_orca", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter3_quest_accepted",
          equals: true,
          then: [{ type: "message", text: "坑道は北の崖だ。奥に、見慣れない装置があるらしい。気をつけろ。", speaker: "オルカ" }],
          else: [
            { type: "message", text: "……調査員か。組合の代表のオルカだ。", speaker: "オルカ" },
            {
              type: "message",
              text: "坑道が閉まって、もう何日にもなる。会社は「安全点検だ」と言い張るが、そんなはずはない。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "夜になると、坑道の奥から妙な光と唸り声がする。組合の者も、何人か入ったきり戻らん。",
              speaker: "オルカ",
            },
            {
              type: "choice",
              text: "坑道の奥を調べますか？",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter3_quest_accepted", value: true },
                    { type: "message", text: "わかった。行ってくる。", speaker: "ユーリ" },
                    { type: "message", text: "……頼む。入口は町の北、崖の上だ。", speaker: "オルカ" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [{ type: "message", text: "……急いでくれ。時間がない。", speaker: "オルカ" }],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function clerkCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [
        { type: "message", text: "坑道の件、上から「立ち入り禁止を解く」と連絡がありました。……私は何も知らないんです、本当に。", speaker: "事務員" },
      ],
      else: [
        { type: "message", text: "組合の方々は誤解しています。坑道は、ただの安全点検で閉じているだけですよ。", speaker: "事務員" },
        { type: "message", text: "……ただ、点検の指示書は本社からで、私も中身は見せてもらえないんです。", speaker: "事務員" },
      ],
    },
  ];
}

function minerCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "坑道の唸り声が止んだな。あんたたちのおかげか。ありがとよ。" }],
      else: [
        { type: "message", text: "会社も組合も、言い分ばかりで話にならねえ。おれたちは灯り石を掘りたいだけなんだがな。" },
        { type: "message", text: "最近の灯り石は、掘り出すたびに妙な熱を持ってやがる。気味が悪い。" },
      ],
    },
  ];
}

function machineCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter3_clue_c007_found",
          equals: true,
          then: [{ type: "message", text: "装置は沈黙している。散らばった指示書は、すべて拾い集めた。" }],
          else: [
            { type: "message", text: "壊れた装置の下に、焦げた紙束が落ちている。" },
            { type: "message", text: "「――実験計画書。目的：静まりの年の再現に向けた、発生装置の出力調整――」" },
            { type: "message", text: "……「静まりの年」。祖父の話にも出てきた言葉だ。", speaker: "ユーリ" },
            { type: "message", text: "ただの鉱山の事件じゃないな、これは。", speaker: "レト" },
            { type: "setFlag", flag: "chapter3_clue_c007_found", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter3_machine_found",
          equals: true,
          then: [{ type: "message", text: "灯り石を吸い込んで唸る装置。近づくと、肌がちりちりする。" }],
          else: [
            { type: "message", text: "坑道の奥に、見慣れない大きな装置があった。管が何本も、鉱脈の灯り石につながっている。" },
            { type: "message", text: "灯り石から力を吸い上げて、何かを……作り出している？", speaker: "ミナ" },
            { type: "message", text: "これは、歪みを人の手で作る装置だ。序章の歪みも、きっと……。", speaker: "ユーリ" },
            { type: "setFlag", flag: "chapter3_machine_found", value: true },
          ],
        },
      ],
    },
  ];
}

function dorunCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "男の姿はもうない。足跡だけが、坑道の奥の闇へ消えている。" }],
      else: [
        { type: "message", text: "「やあ、また会ったね」――見覚えのある声が、坑道に響いた。" },
        { type: "message", text: "……ドルン！ 硝子湖の倉庫にいた男だな。", speaker: "ユーリ" },
        {
          type: "message",
          text: "労働争議は、いい煙幕だったよ。みんな会社と組合の喧嘩に気を取られて、奥で何をしているか、誰も見ない。",
          speaker: "ドルン",
        },
        { type: "message", text: "この装置で何をしている！ 答えろ！", speaker: "レト" },
        {
          type: "message",
          text: "調整だよ、ただの。……でも、今日はここまでだ。後始末は、装置に任せよう。",
          speaker: "ドルン",
        },
        { type: "message", text: "男が装置の栓を引き抜くと、灯り石が悲鳴のような音を立てて歪み始めた！" },
        { type: "startBattle", battleId: "tetsukusari-yugami" },
      ],
    },
  ];
}
