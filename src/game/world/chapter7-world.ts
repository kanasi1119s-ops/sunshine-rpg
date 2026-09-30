import { createFushimaBaseData, FUSHIMA_BASE_LANDMARKS } from "../map/chapter7/fushima-base";
import { createFushimaTownData, FUSHIMA_TOWN_LANDMARKS } from "../map/chapter7/fushima-town";
import { TOUSHIN_TOWN_ENTRY } from "../map/chapter8/toushin-town";
import { TOURI_TOWN_SPAWN } from "../map/chapter0/touri-town";
import { MUGIKANO_VILLAGE_ENTRY } from "../map/chapter1/mugikano-village";
import { GARASUKO_TOWN_ENTRY } from "../map/chapter2/garasuko-town";
import { TETSUKUSARI_TOWN_ENTRY } from "../map/chapter3/tetsukusari-town";
import { SANONE_TOWN_ENTRY } from "../map/chapter4/sanone-town";
import { KIRI_TOWN_ENTRY } from "../map/chapter5/kiri-town";
import { SHIMOHARA_TOWN_ENTRY } from "../map/chapter6/shimohara-town";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第7章（浮嶼）の世界。`docs/story/structure.md`「第7章（浮嶼）」・`docs/story/mystery.md`を反映。
 * 伏線 C-014（各地の事件が黒幕の拠点につながる）と C-015（黒幕が姿を見せ、灯芯都で待つと告げる）を実装（roadmap 4-32）。
 * ボス「監視卓の歪み」は4-33（`src/game/battle/chapter7-enemies.ts`）。専用BGMは4-34で追加予定（それまで霜原などの曲を仮に流用）。
 * 空の乗り物（`chapter7_airship_obtained`）を手に入れると、渡し守に頼んで訪れた町へ飛べる（roadmap 4-35。町を選ぶ簡易な移動で、フィールド上の操縦は無い）。
 */
/** 空の乗り物で飛べる町。3つの方面に分けて、二段階の選択肢で選ぶ。 */
export const AIRSHIP_DESTINATIONS: { area: string; towns: { label: string; mapId: string; tileX: number; tileY: number; gate?: string }[] }[] = [
  {
    area: "西の空（灯里・麦香野・硝子湖）",
    towns: [
      { label: "灯里の町", mapId: "touri-town", ...TOURI_TOWN_SPAWN },
      { label: "麦香野の村", mapId: "mugikano-village", ...MUGIKANO_VILLAGE_ENTRY },
      { label: "硝子湖の町", mapId: "garasuko-town", ...GARASUKO_TOWN_ENTRY },
    ],
  },
  {
    area: "中ほどの空（鉄鏈・砂音）",
    towns: [
      { label: "鉄鏈鉱山の町", mapId: "tetsukusari-town", ...TETSUKUSARI_TOWN_ENTRY },
      { label: "砂音の町", mapId: "sanone-town", ...SANONE_TOWN_ENTRY },
    ],
  },
  {
    area: "東の空（霧断崖・霜原）",
    towns: [
      { label: "霧断崖の町", mapId: "kiri-town", ...KIRI_TOWN_ENTRY },
      { label: "霜原の町", mapId: "shimohara-town", ...SHIMOHARA_TOWN_ENTRY },
    ],
  },
  {
    area: "中央の空（灯芯都）",
    towns: [{ label: "灯芯都", mapId: "toushin-town", ...TOUSHIN_TOWN_ENTRY }],
  },
  {
    area: "最果ての空（虚灯宮）",
    towns: [{ label: "虚灯宮", mapId: "kyotoukyu-court", tileX: 12, tileY: 13, gate: "chapter8_kyotoukyu_open" }],
  },
];

export const CHAPTER7_MAPS: Record<string, TileMapData> = {
  "fushima-town": createFushimaTownData(),
  "fushima-base": createFushimaBaseData(),
};

/** 浮嶼へ到着したとき、一度だけ流す場面つなぎ（`chapter7_intro_seen` フラグで管理）。 */
export const CHAPTER7_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――雲の海に浮かぶ島々、浮嶼。" },
  {
    type: "message",
    text: "ドルンは「あの方」と言い残して消えた。これまでの事件を、ひとつの糸がつないでいるのなら、その端がここにあるのかもしれない。",
  },
  {
    type: "message",
    text: "板張りの通りの向こうに、空を見上げる人々の暮らしがあった。ここは、かつて「雲海衆」と呼ばれた人々の島だ。",
  },
  { type: "setFlag", flag: "chapter7_intro_seen", value: true },
];

export const CHAPTER7_NPCS: Record<string, Npc[]> = {
  "fushima-town": [
    {
      id: "fushima-elder",
      tileX: FUSHIMA_TOWN_LANDMARKS.elder.tileX,
      tileY: FUSHIMA_TOWN_LANDMARKS.elder.tileY,
      color: "#7a8fa6",
      commands: elderCommands(),
    },
    {
      id: "fushima-innkeeper",
      tileX: FUSHIMA_TOWN_LANDMARKS.innkeeper.tileX,
      tileY: FUSHIMA_TOWN_LANDMARKS.innkeeper.tileY,
      color: "#9a7a5a",
      commands: innkeeperCommands(),
    },
    {
      id: "fushima-ferryman",
      tileX: FUSHIMA_TOWN_LANDMARKS.ferryman.tileX,
      tileY: FUSHIMA_TOWN_LANDMARKS.ferryman.tileY,
      color: "#6a9a8a",
      commands: ferrymanCommands(),
    },
  ],
  "fushima-base": [
    {
      id: "fushima-ledger",
      tileX: FUSHIMA_BASE_LANDMARKS.ledger.tileX,
      tileY: FUSHIMA_BASE_LANDMARKS.ledger.tileY,
      color: "#b8a878",
      commands: ledgerCommands(),
    },
    {
      id: "fushima-console",
      tileX: FUSHIMA_BASE_LANDMARKS.console.tileX,
      tileY: FUSHIMA_BASE_LANDMARKS.console.tileY,
      color: "#6a8a9a",
      commands: consoleCommands(),
    },
    {
      id: "fushima-edrea",
      tileX: FUSHIMA_BASE_LANDMARKS.guard.tileX,
      tileY: FUSHIMA_BASE_LANDMARKS.guard.tileY,
      color: "#3a4a7a",
      spriteName: "エドレア",
      commands: edreaCommands(),
    },
  ],
};

function elderCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter7_reported",
      equals: true,
      then: [
        { type: "message", text: "空の乗り物は、あなた方のものです。雲の上でも、どうかご無事で。", speaker: "雲海衆の長老" },
      ],
      else: [
        {
          type: "if",
          flag: "chapter7_quest_accepted",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter7_edrea_appeared",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "北の整備区画に、そんな部屋が……。わしらの島が、ずっと見張られていたというのか。",
                  speaker: "雲海衆の長老",
                },
                {
                  type: "message",
                  text: "奪われた空の上に、まだ奪うものがあったとはな。……礼として、島に一隻だけ残っていた空の乗り物を、あなた方に託そう。",
                  speaker: "雲海衆の長老",
                },
                { type: "message", text: "空の乗り物を手に入れた！（浮嶼の渡し守に頼むと、これまで訪れた町へ飛べる）" },
                { type: "setFlag", flag: "chapter7_airship_obtained", value: true },
                { type: "setFlag", flag: "chapter7_reported", value: true },
              ],
              else: [
                {
                  type: "message",
                  text: "北の整備区画は、町の北の入口です。夜ごと、見知らぬ船が出入りしていると、渡し守が言っていました。",
                  speaker: "雲海衆の長老",
                },
              ],
            },
          ],
          else: [
            { type: "message", text: "灯りの相談所の方ですね。浮嶼の長老をしております。", speaker: "雲海衆の長老" },
            {
              type: "message",
              text: "この島の北に、立入りを禁じられた整備区画があります。二十年以上前、合議会が「接収」して以来、わしらは近づけません。",
              speaker: "雲海衆の長老",
            },
            {
              type: "message",
              text: "近ごろ、そこに明かりがともり、船が出入りしています。どうか、中を確かめてはもらえませんか。",
              speaker: "雲海衆の長老",
            },
            {
              type: "choice",
              text: "整備区画を調べますか?",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter7_quest_accepted", value: true },
                    { type: "message", text: "任せてください。", speaker: "ユーリ" },
                    { type: "message", text: "ありがとうございます。空の上の風は気まぐれです。どうか、お気をつけて。", speaker: "雲海衆の長老" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [{ type: "message", text: "お待ちしています。", speaker: "雲海衆の長老" }],
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
      flag: "chapter7_reported",
      equals: true,
      then: [{ type: "message", text: "雲の上の朝焼けは格別ですよ。ゆっくり休んでいってください。", speaker: "宿屋の主人" }],
      else: [
        { type: "message", text: "ようこそ、浮嶼へ。風が強い日は、板の通りが少し揺れますが、慣れれば心地いいものです。", speaker: "宿屋の主人" },
        { type: "message", text: "遠くの空に、いつも黒い雲が渦を巻いているでしょう? あれは嵐雲ですよ。昔からああです。", speaker: "宿屋の主人" },
      ],
    },
  ];
}

function ferrymanCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter7_airship_obtained",
      equals: true,
      then: [
        { type: "message", text: "空の乗り物は、島々を結ぶ道です。行きたい所へ、風が連れて行ってくれますよ。", speaker: "渡し守" },
        ...airshipDestinationCommands(),
      ],
      else: [
        { type: "message", text: "島と島の間は、綱と小舟で渡っています。北の整備区画のほうは、昔から誰も近づきません。", speaker: "渡し守" },
        { type: "message", text: "でも最近、夜になると、あそこから青白い光がのぞくんです。", speaker: "渡し守" },
      ],
    },
  ];
}

/** 行き先に開放の条件（フラグ）があるとき、満たしていなければ断る。 */
function gated(flag: string | undefined, commands: EventCommand[]): EventCommand[] {
  if (!flag) {
    return commands;
  }
  return [
    {
      type: "if",
      flag,
      equals: true,
      then: commands,
      else: [{ type: "message", text: "あそこへの空路は、まだ開かれていません。合議会の許しが要ります。", speaker: "渡し守" }],
    },
  ];
}

function airshipDestinationCommands(): EventCommand[] {
  return [
    {
      type: "choice",
      text: "どちらの空へ行きますか?",
      options: [
        ...AIRSHIP_DESTINATIONS.map((area) => ({
          label: area.area,
          commands: [
            {
              type: "choice" as const,
              text: "どの町へ降りますか?",
              options: [
                ...area.towns.map((town) => ({
                  label: town.label,
                  commands: gated(town.gate, [
                    { type: "message" as const, text: `${town.label}へ向かいます。しっかりつかまって!`, speaker: "渡し守" },
                    { type: "warp" as const, mapId: town.mapId, tileX: town.tileX, tileY: town.tileY },
                  ]),
                })),
                { label: "やめる", commands: [] },
              ],
            },
          ],
        })),
        { label: "やめる", commands: [] },
      ],
    },
  ];
}

function ledgerCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter7_ledger_found",
      equals: true,
      then: [{ type: "message", text: "帳簿の最後の欄には、「灯芯都・合議会」の宛名と、代表の署名の跡が残っている。" }],
      else: [
        { type: "message", text: "壁ぎわの棚に、厚い帳簿が並んでいる。" },
        {
          type: "message",
          text: "灯里、麦香野、硝子湖、鉄鏈鉱山、砂音、霧断崖、霜原……。全部そろってる。歪みが起きた場所と、その日付だ。",
          speaker: "レト",
        },
        {
          type: "message",
          text: "起きた「あと」の記録じゃない。「起こす前」の計画の欄に、印がついてる。……全部、ここで決められていたんだ。",
          speaker: "ミナ",
        },
        { type: "setFlag", flag: "chapter7_ledger_found", value: true },
      ],
    },
  ];
}

function consoleCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter7_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "監視卓の光は消えた。映っていた光点も、もう見えない。" }],
      else: [
        {
          type: "if",
          flag: "chapter7_ledger_found",
          equals: true,
          then: [
            { type: "message", text: "奥の大きな卓に、大陸の地図が浮かんでいる。歪みの起きた場所に、赤い光点がともっている。" },
            {
              type: "message",
              text: "見て。灯里から霜原まで、光点が一本の線でつながってる。……そして、線の行き先は灯芯都だ。",
              speaker: "アヤメ",
            },
            { type: "setFlag", flag: "chapter7_console_found", value: true },
            { type: "message", text: "触れた瞬間、卓が青白く光り、歪みの姿となって襲いかかってきた！" },
            { type: "startBattle", battleId: "fushima-yugami" },
          ],
          else: [{ type: "message", text: "奥に大きな卓がある。まずは周りの記録を調べてからのほうがよさそうだ。" }],
        },
      ],
    },
  ];
}

function edreaCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter7_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter7_edrea_appeared",
          equals: true,
          then: [{ type: "message", text: "エドレアの姿はもうない。床に、灯芯都の紋章の入った書き付けだけが残っている。" }],
          else: [
            { type: "message", text: "静まった卓の向こうから、ゆっくりと足音が近づいてきた。" },
            {
              type: "message",
              text: "見事な戦いでした。ここまで辿り着く人は、そう多くありません。",
              speaker: "エドレア",
            },
            { type: "message", text: "合議会代表の……エドレア! あなたが、これを?", speaker: "ユーリ" },
            {
              type: "message",
              text: "わたしの言葉を信じるかどうかは、あなた方次第です。ただ、ここで多くを語るつもりはありません。",
              speaker: "エドレア",
            },
            {
              type: "message",
              text: "続きは、灯芯都で。合議会の広間で、お待ちしています。……真実が知りたければ、いらっしゃい。",
              speaker: "エドレア",
            },
            { type: "message", text: "エドレアは静かに背を向け、待たせていた空の船に乗って雲の向こうへ消えた。" },
            { type: "setFlag", flag: "chapter7_edrea_appeared", value: true },
          ],
        },
      ],
      else: [{ type: "message", text: "拠点の奥は静かだ。人の気配は、まだ感じられない。" }],
    },
  ];
}
