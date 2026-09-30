import { createShimoharaFacilityData, SHIMOHARA_FACILITY_LANDMARKS } from "../map/chapter6/shimohara-facility";
import { createShimoharaTownData, SHIMOHARA_TOWN_LANDMARKS } from "../map/chapter6/shimohara-town";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第6章（霜原）の世界。`docs/story/structure.md`「第6章（霜原）」・`docs/story/mystery.md`を反映。
 * 伏線 C-012（アヤメの観察者めいた態度）と C-013（ドルンの捨て台詞）を実装（roadmap 4-27）。
 * ボス「試作機の歪み」は4-28（`src/game/battle/chapter6-enemies.ts`）、専用BGMは4-29で追加予定（それまで灯里の町の曲を仮に流用）。
 * ジョブチェンジ・システムの解禁（`docs/design/jobs.md`）は、システム本体の実装後に別項目で行う。
 */
export const CHAPTER6_MAPS: Record<string, TileMapData> = {
  "shimohara-town": createShimoharaTownData(),
  "shimohara-facility": createShimoharaFacilityData(),
};

/** 霜原へ到着したとき、一度だけ流す場面つなぎ（`chapter6_intro_seen` フラグで管理）。 */
export const CHAPTER6_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――雪に閉ざされた北の町・霜原。" },
  {
    type: "message",
    text: "霧断崖の原本に残っていた、祖父の名。「静まりの年」に何があったのか、その痕跡が、大乱期の戦跡に眠っているという。",
  },
  {
    type: "message",
    text: "白い息を吐きながら町に入ると、雪の中に、ひとり静かに立っている人影があった。",
  },
  { type: "setFlag", flag: "chapter6_intro_seen", value: true },
];

export const CHAPTER6_NPCS: Record<string, Npc[]> = {
  "shimohara-town": [
    {
      id: "shimohara-watchman",
      tileX: SHIMOHARA_TOWN_LANDMARKS.watchman.tileX,
      tileY: SHIMOHARA_TOWN_LANDMARKS.watchman.tileY,
      color: "#6a7a8a",
      commands: watchmanCommands(),
    },
    {
      id: "shimohara-innkeeper",
      tileX: SHIMOHARA_TOWN_LANDMARKS.innkeeper.tileX,
      tileY: SHIMOHARA_TOWN_LANDMARKS.innkeeper.tileY,
      color: "#9a7a5a",
      commands: innkeeperCommands(),
    },
    {
      id: "shimohara-ayame",
      tileX: SHIMOHARA_TOWN_LANDMARKS.hunter.tileX,
      tileY: SHIMOHARA_TOWN_LANDMARKS.hunter.tileY,
      color: "#9a8fd0",
      spriteName: "アヤメ",
      commands: ayameCommands(),
    },
  ],
  "shimohara-facility": [
    {
      id: "shimohara-log",
      tileX: SHIMOHARA_FACILITY_LANDMARKS.log.tileX,
      tileY: SHIMOHARA_FACILITY_LANDMARKS.log.tileY,
      color: "#b8a878",
      commands: logCommands(),
    },
    {
      id: "shimohara-panel",
      tileX: SHIMOHARA_FACILITY_LANDMARKS.panel.tileX,
      tileY: SHIMOHARA_FACILITY_LANDMARKS.panel.tileY,
      color: "#6a8a9a",
      commands: panelCommands(),
    },
    {
      id: "shimohara-dorun",
      tileX: SHIMOHARA_FACILITY_LANDMARKS.guard.tileX,
      tileY: SHIMOHARA_FACILITY_LANDMARKS.guard.tileY,
      color: "#5a3a6a",
      spriteName: "ドルン",
      commands: dorunCommands(),
    },
  ],
};

function watchmanCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_reported",
      equals: true,
      then: [{ type: "message", text: "施設の入口は、番所で封をしました。雪がやめば、また静かな町に戻るでしょう。", speaker: "番所の守り" }],
      else: [
        {
          type: "if",
          flag: "chapter6_quest_accepted",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter6_yugami_defeated",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "地下の光が消えたのですね。あの施設が、そんな恐ろしいものだったとは……。",
                  speaker: "番所の守り",
                },
                {
                  type: "message",
                  text: "戦跡の下に何かがあると、先代からは聞いていました。けれど中身までは、誰も知らなかった。",
                  speaker: "番所の守り",
                },
                { type: "setFlag", flag: "chapter6_reported", value: true },
              ],
              else: [
                {
                  type: "message",
                  text: "入口は町の北、古い柵の先です。雪の下から、夜ごと青白い光が漏れています。",
                  speaker: "番所の守り",
                },
              ],
            },
          ],
          else: [
            { type: "message", text: "灯りの相談所の方ですね。霜原の番所を預かっています。", speaker: "番所の守り" },
            {
              type: "message",
              text: "ひと月前から、北の戦跡の雪の下に、地下への入口が現れました。青白い光が漏れ、近づいた猟師が体調を崩しています。",
              speaker: "番所の守り",
            },
            {
              type: "choice",
              text: "地下の施設を調べますか？",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter6_quest_accepted", value: true },
                    { type: "message", text: "任せてください。", speaker: "ユーリ" },
                    { type: "message", text: "ありがとうございます。どうか、お気をつけて。", speaker: "番所の守り" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [{ type: "message", text: "お待ちしています。", speaker: "番所の守り" }],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function innkeeperCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_reported",
      equals: true,
      then: [{ type: "message", text: "温かいスープでも飲んでいってください。今夜は、ゆっくり眠れそうです。", speaker: "宿屋の主人" }],
      else: [
        { type: "message", text: "ここは戦跡のそばの宿です。昔から、雪の下で何かが唸る夜があると言われていましてね。", speaker: "宿屋の主人" },
        { type: "message", text: "大乱期の兵器の名残だと、年寄りたちは言いますが……。", speaker: "宿屋の主人" },
      ],
    },
  ];
}

function ayameCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_ayame_joined",
      equals: true,
      then: [{ type: "message", text: "……行きましょう。", speaker: "アヤメ" }],
      else: [
        {
          type: "if",
          flag: "chapter6_reported",
          equals: true,
          then: [
            {
              type: "message",
              text: "施設の中で、あなた方が戦うのを見ていました。ひとつ、打ち明けなければならないことがあります。",
              speaker: "アヤメ",
            },
            {
              type: "message",
              text: "わたしの祖父は、「静まりの年」に職を追われ、姿を消した三人のうちの一人です。",
              speaker: "アヤメ",
            },
            {
              type: "message",
              text: "だから、あなた方に近づきました。霧断崖の原本を見つけた人たちなら、真相に届くと思ったから。……ただの案内人、というのは嘘です。",
              speaker: "アヤメ",
            },
            {
              type: "message",
              text: "わたしが調べていた相手は、合議会の内側にいます。名を言うのは、証拠が揃ってから。今はまだ、それだけしか。",
              speaker: "アヤメ",
            },
            { type: "message", text: "それでも、あなたのおじいさんも同じ三人の一人だ。……目的は、同じだよ。", speaker: "ユーリ" },
            {
              type: "choice",
              text: "アヤメの申し出にどう答える？",
              options: [
                {
                  label: "一緒に来てほしい",
                  commands: [
                    { type: "message", text: "……ありがとう。調べる相手ではなく、仲間として、お供します。", speaker: "アヤメ" },
                    { type: "setFlag", flag: "chapter6_ayame_joined", value: true },
                  ],
                },
                {
                  label: "少し考えさせてほしい",
                  commands: [{ type: "message", text: "分かりました。気持ちが決まったら、声をかけてください。", speaker: "アヤメ" }],
                },
              ],
            },
          ],
          else: [
            {
              type: "if",
              flag: "chapter6_quest_accepted",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "北の施設なら、案内します。ただ、わたしはただの案内人です。戦いの矢面には立ちません。",
                  speaker: "アヤメ",
                },
              ],
              else: [
                { type: "message", text: "……灯りの相談所の方ですね。霜原の案内人、アヤメです。", speaker: "アヤメ" },
                {
                  type: "message",
                  text: "この町のことなら何でも。ただし、あなた方の事情には、深入りしません。",
                  speaker: "アヤメ",
                },
                { type: "message", text: "（表情がほとんど動かない。まるで、こちらを観察しているようだ）", speaker: "ミナ" },
                { type: "setFlag", flag: "chapter6_ayame_met", value: true },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function logCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_log_found",
      equals: true,
      then: [{ type: "message", text: "試作機の運用記録。「静まりの年」の日付と、責任者の署名の欄が、黒く塗りつぶされている。" }],
      else: [
        { type: "message", text: "壁ぎわの棚に、凍りついた運用記録が残っていた。" },
        {
          type: "message",
          text: "「灯り石の暴走を人為的に起こす、発生装置の試作一号機。静まりの年の前年、試験運用を開始」……。",
          speaker: "レト",
        },
        { type: "message", text: "歪みは、ここで「作られた」んだ。……自然に起きたものじゃなかった。", speaker: "ミナ" },
        { type: "setFlag", flag: "chapter6_log_found", value: true },
      ],
    },
  ];
}

function panelCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "操作盤の光は消え、静まり返っている。" }],
      else: [
        { type: "message", text: "操作盤が、いまも青白く点滅している。誰かが最近まで触れていたようだ。" },
        { type: "message", text: "指示の記録がある。……送り先は「灯芯都」。他の施設と同じ宛先だ。", speaker: "レト" },
      ],
    },
  ];
}

function dorunCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter6_dorun_farewell",
          equals: true,
          then: [{ type: "message", text: "ドルンの姿はない。床に、砕けた灯り石が散っているだけだ。" }],
          else: [
            {
              type: "message",
              text: "ドルンは肩で息をしながら、壊れた装置にもたれかかっている。",
            },
            { type: "message", text: "……ここまでですか。あなた方は、思ったより厄介だ。", speaker: "ドルン" },
            { type: "message", text: "これ以上は、あの方の領分だ。私の出る幕じゃない。", speaker: "ドルン" },
            { type: "message", text: "待て！ 「あの方」って、誰のことだ！", speaker: "ユーリ" },
            { type: "message", text: "ドルンは灯り石を砕き、白い光の中に姿を消した。" },
            { type: "setFlag", flag: "chapter6_dorun_farewell", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter6_log_found",
          equals: true,
          then: [
            { type: "message", text: "「おや、あなたたちでしたか。ちょうどいい、少し道を空けてもらえますか」――ドルンが装置の前で振り向いた。" },
            { type: "message", text: "ドルン！ この装置は、お前が動かしていたのか！", speaker: "ユーリ" },
            {
              type: "message",
              text: "動かしていた？ 少し違いますね。私は「整備」を任されているだけです。壊れかけの試作機を、もう一度だけ。",
              speaker: "ドルン",
            },
            {
              type: "message",
              text: "ドルンが装置に灯り石を投げ込むと、青白い光が渦を巻き、歪みの姿になった！",
            },
            { type: "setFlag", flag: "chapter6_dorun_met", value: true },
            { type: "startBattle", battleId: "shimohara-yugami" },
          ],
          else: [{ type: "message", text: "奥の装置の前に、黒い外套の男が立っている。まずは周りの記録を調べてからのほうがよさそうだ。" }],
        },
      ],
    },
  ];
}
