import { createKiriArchiveData, KIRI_ARCHIVE_LANDMARKS } from "../map/chapter5/kiri-archive";
import { createKiriTownData, KIRI_TOWN_LANDMARKS } from "../map/chapter5/kiri-town";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第5章（霧断崖）の世界。`docs/story/structure.md`「第5章（霧断崖）」・`docs/story/mystery.md`を反映。
 * 伏線 C-010（静まりの年に要人が失脚・失踪した記録）と C-011（記録の中のユーリの祖父の名）を実装（roadmap 4-22）。
 * 敵データ・バランスは4-23、専用BGMは4-24で追加する（それまで第4章の曲を仮に流用）。
 */
export const CHAPTER5_MAPS: Record<string, TileMapData> = {
  "kiri-town": createKiriTownData(),
  "kiri-archive": createKiriArchiveData(),
};

/** 霧断崖へ到着したとき、一度だけ流す場面つなぎ（`chapter5_intro_seen` フラグで管理）。 */
export const CHAPTER5_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――断崖に張り付く、霧の古都・霧断崖。" },
  {
    type: "message",
    text: "砂音で聞いた「合議会に近い誰か」の噂。その手がかりと、紙切れの「静まりの年」の意味を求めて、ユーリたちは環信仰の聖地を訪ねた。",
  },
  {
    type: "message",
    text: "町は深い霧に包まれている。巡礼者たちは声をひそめ、しきりに聖堂のほうを気にしている。",
  },
  { type: "setFlag", flag: "chapter5_intro_seen", value: true },
];

export const CHAPTER5_NPCS: Record<string, Npc[]> = {
  "kiri-town": [
    {
      id: "kiri-priest",
      tileX: KIRI_TOWN_LANDMARKS.priest.tileX,
      tileY: KIRI_TOWN_LANDMARKS.priest.tileY,
      color: "#d8d0b8",
      commands: priestCommands(),
    },
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
                  text: "「静まりの年」に、合議会の要人が幾人も職を追われ、消えた。その記録が、原本から抜き取られていたとは。",
                  speaker: "司祭",
                },
                {
                  type: "message",
                  text: "しかも、原本の綴りには、灯芯都の元合議会員の名が――あなたの祖父君の名が、残っていたのですね。",
                  speaker: "司祭",
                },
                { type: "message", text: "……おじいちゃんの名前が、どうして……。", speaker: "ユーリ" },
                {
                  type: "message",
                  text: "私に分かるのは、ここまでです。真実を知る者は、灯芯都にいるでしょう。どうか、気をつけて。",
                  speaker: "司祭",
                },
                { type: "setFlag", flag: "chapter5_reported", value: true },
              ],
              else: [
                {
                  type: "message",
                  text: "調べは、北の岩壁の「記録の間」からお願いします。碑文の原本は、そこにあります。",
                  speaker: "司祭",
                },
              ],
            },
          ],
          else: [
            { type: "message", text: "ようこそ、霧断崖へ。灯りの相談所の方々とお見受けします。", speaker: "司祭" },
            {
              type: "message",
              text: "先日、聖堂の予言の碑に「霧が町を呑み、人々は灯を失う」という一節が浮かび上がりました。",
              speaker: "司祭",
            },
            {
              type: "message",
              text: "巡礼者は怯え、町を去る者も出ています。けれど、こんな一節は、私が知る限り古い記録にありません。",
              speaker: "司祭",
            },
            {
              type: "choice",
              text: "記録の間を調べますか?",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter5_quest_accepted", value: true },
                    { type: "message", text: "お任せください。", speaker: "ユーリ" },
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
      then: [{ type: "message", text: "霧が晴れたら、また巡礼を続けます。教えの道は、まだ先ですから。", speaker: "巡礼者" }],
      else: [
        { type: "message", text: "予言の碑に「霧が町を呑む」と出たそうです。私はもう、帰ろうかと……。", speaker: "巡礼者" },
        {
          type: "message",
          text: "でも、不思議なんです。古い巡礼歌には、そんな恐ろしい一節はないはずなのに。",
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
      then: [{ type: "message", text: "原本と写しの綴りが合わない……。書き手の癖まで、真似ていたのですね。", speaker: "書記" }],
      else: [
        { type: "message", text: "私は聖堂の書記です。記録の間の書き写しも、私の役目でして。", speaker: "書記" },
        {
          type: "message",
          text: "ただ、ここ数年、古い巻物の一部が「修復」の名目で、灯芯都から来た方に預けられているのです。",
          speaker: "書記",
        },
        { type: "message", text: "灯芯都から……?", speaker: "レト" },
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
        { type: "message", text: "閲覧机に、予言の碑文の写しが広げられている。「静まりの年」の欄に目が留まった。" },
        {
          type: "message",
          text: "この欄だけ、インクが新しい。古い文字を削って、上から書き直してある。",
          speaker: "ミナ",
        },
        {
          type: "message",
          text: "削られた跡から、元の文字がうっすら読める。「この年、合議会の要人、四名が職を退き、うち三名は行方を絶つ」……。",
          speaker: "ユーリ",
        },
        { type: "message", text: "合議会の要人が、一度に失踪した……? それを隠したい誰かが、書き換えたんだ。", speaker: "レト" },
        { type: "setFlag", flag: "chapter5_record_found", value: true },
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
            { type: "message", text: "書架の奥に、布で包まれた古い綴りが隠されていた。書き換えられる前の、原本の一部のようだ。" },
            {
              type: "message",
              text: "失踪した三名の名が並んでいる。その一番下の名前に、ユーリの目が止まった。",
            },
            { type: "message", text: "「ソウイチ」……。おじいちゃんの名前だ。", speaker: "ユーリ" },
            {
              type: "message",
              text: "灯芯都の元合議会員が、「静まりの年」に姿を消した三人のうちの一人……。",
              speaker: "レト",
            },
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
      then: [{ type: "message", text: "黒いローブの男は姿を消し、床に砕けた灯り石だけが残っている。" }],
      else: [
        {
          type: "if",
          flag: "chapter5_ledger_found",
          equals: true,
          then: [
            { type: "message", text: "「……原本を見つけてしまいましたか」――黒いローブの男が、書架の陰から振り向いた。" },
            {
              type: "message",
              text: "碑文を書き換えたのは、あなたですね。誰の命令で、こんなことを!",
              speaker: "ユーリ",
            },
            {
              type: "message",
              text: "私は「修復」を頼まれただけです。あるお方から、古い記録は正しい形に直すよう命じられて。",
              speaker: "写字官",
            },
            {
              type: "message",
              text: "名は申せません。ただ……そのお方は、灯芯都の高い場所におられる、とだけ。",
              speaker: "写字官",
            },
            {
              type: "message",
              text: "写字官が灯り石を握りつぶすと、碑文の文字が霧になって立ち上がり、歪みの姿になった！",
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
