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
    text: "雲の上に張られた綱を、籠舟で渡ると、板張りの通りの向こうに、空を見上げる人々の暮らしがあった。ここは、かつて「雲海衆」と呼ばれた人々の島だ。",
  },
  { type: "message", text: "子どもたちの数え歌が聞こえる。「かえして、かえして、空の島」。島の挨拶は、「いい風を」だという。" },
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
        { type: "message", text: "空の乗り物は、あなた方のものです。雲の上でも、どうかご無事で。いい風を。", speaker: "雲海衆の長老" },
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
                  text: "北の整備区画に、そんな部屋が……。わたしたちの島が、ずっと見張られていたというのか。",
                  speaker: "雲海衆の長老",
                },
                {
                  type: "message",
                  text: "奪われた空の上に、まだ奪うものがあったとはな。……けれど、知らないまま見られ続けるよりは、ずっといい。",
                  speaker: "雲海衆の長老",
                },
                {
                  type: "message",
                  text: "礼として、島に一隻だけ隠してきた空の乗り物を、あなた方に託します。二十七年、誰にも触れさせませんでした。",
                  speaker: "雲海衆の長老",
                },
                {
                  type: "message",
                  text: "名は「風待ち」。大切だからこそ、お渡しします。あなた方には、行かなければならない場所があるのでしょう。",
                  speaker: "雲海衆の長老",
                },
                {
                  type: "message",
                  text: "二十七年ぶりに、空に浮かぶんです。操縦は、わしが引き受けましょう。",
                  speaker: "渡し守",
                },
                { type: "message", text: "空の乗り物「風待ち」を手に入れた！（浮嶼の渡し守に頼むと、これまで訪れた町へ飛べる）" },
                { type: "setFlag", flag: "chapter7_airship_obtained", value: true },
                { type: "setFlag", flag: "chapter7_reported", value: true },
              ],
              else: [
                {
                  type: "message",
                  text: "北の整備区画は、町の北の入口です。夜ごと、見知らぬ船が出入りしていると、渡し守が言っていました。",
                  speaker: "雲海衆の長老",
                },
                {
                  type: "message",
                  text: "ドルンという少年を預かっていた老人が、島の東の端におります。サザンといいます。頑固ですが、あなた方になら話すでしょう。",
                  speaker: "雲海衆の長老",
                },
              ],
            },
          ],
          else: [
            { type: "message", text: "灯りの相談所の方々ですね。ようこそ、浮嶼へ。長老をしております。いい風を。", speaker: "雲海衆の長老" },
            {
              type: "message",
              text: "二十七年前まで、この空は、わたしたちのものでした。合議会は「浮嶼平定戦」と呼びますが、わたしたちは「奪われた空」と呼びます。",
              speaker: "雲海衆の長老",
            },
            {
              type: "message",
              text: "島の北の整備区画は、そのとき合議会が「接収」し、以来、わたしたちは近づけません。",
              speaker: "雲海衆の長老",
            },
            {
              type: "message",
              text: "ところが近ごろ、そこに青白い明かりがともり、船が夜ごと出入りしています。兵の姿は、誰も見ていません。それが、いちばん不気味なのです。",
              speaker: "雲海衆の長老",
            },
            {
              type: "message",
              text: "合議会の役所の方ではない、あなた方だから、お頼みできます。どうか、中を確かめてはもらえませんか。",
              speaker: "雲海衆の長老",
            },
            {
              type: "choice",
              text: "整備区画を調べますか？",
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
        { type: "message", text: "遠くの空に、いつも黒い雲が渦を巻いているでしょう？ あれは嵐雲ですよ。昔からああです。", speaker: "宿屋の主人" },
        { type: "message", text: "あの渦のせいで、東の空へは船で出られません。だから、東のほうへは、誰も行きません。", speaker: "宿屋の主人" },
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
      text: "どちらの空へ行きますか？",
      options: [
        ...AIRSHIP_DESTINATIONS.map((area) => ({
          label: area.area,
          commands: [
            {
              type: "choice" as const,
              text: "どの町へ降りますか？",
              options: [
                ...area.towns.map((town) => ({
                  label: town.label,
                  commands: gated(town.gate, [
                    { type: "message" as const, text: `${town.label}へ向かいます。しっかりつかまって！`, speaker: "渡し守" },
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
      then: [{ type: "message", text: "帳簿の最後の欄には、「灯芯都・合議会　書記長　処置責任者」の宛名と、擦れた署名の跡が残っている。" }],
      else: [
        { type: "message", text: "長い廊下の奥の部屋に、ユーリの腕輪が応えて、鍵がかちりと開いた。壁ぎわの棚に、厚い帳簿が並んでいる。" },
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
        { type: "message", text: "麦香野だけは、「村の工事で偶発的に起動。計画外。修正不要」……。水が枯れて困ったことが、「修正不要」。", speaker: "ミナ" },
        { type: "message", text: "硝子湖には、「商家の縁者を看板に使う。潔白は問わない」とあるよ。……分かってたのに、文字で見ると、ちがうね。", speaker: "ガイド" },
        { type: "message", text: "灯里は、「目立たない試験地」……。ぼくの町が、そう呼ばれてたのか。", speaker: "ユーリ" },
        { type: "message", text: "棚の端に、濃紺の背表紙の帳簿が一冊あった。題は、ただ「静まりの年」。" },
        {
          type: "message",
          text: "最初の頁に、三つの名前。「ソウイチ　処置済　保全」「ハクエイ　処置済　保全」「トウマ　処置済　保全」。",
        },
        { type: "message", text: "……祖父です。なかったことにされていたんじゃない。ちゃんと、書かれていた。", speaker: "アヤメ" },
        { type: "message", text: "「処置済」と「保全」。……「殺した」とは、書いてない。生きてるかもしれないぞ。", speaker: "レト" },
        {
          type: "message",
          text: "最後の頁の署名欄は、「書記長　処置責任者」。名は擦れて読めないが、最後の払いだけが、細く長く残っていた。",
        },
        { type: "message", text: "この筆跡……祖父に届いた、茶会の招待状の署名と、同じです。", speaker: "アヤメ" },
        { type: "message", text: "全部は持ち出せない。写せるだけ写して、まず外へ出よう。「静まりの年」の一冊は、持っていけるはずだ。", speaker: "レト" },
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
              text: "見て。灯里から霜原まで、光点が一本の線でつながってる。……そして、線の行き先は灯芯都です。",
              speaker: "ミナ",
            },
            { type: "message", text: "ぼくたちの旅の順番と、同じだ。……辿らされてきたのかもしれない。", speaker: "ユーリ" },
            {
              type: "message",
              text: "この小さな白い光は、何でしょう。……動いているものも、あります。",
              speaker: "アヤメ",
            },
            { type: "message", text: "人だ。白い点は、一人ひとりの人です。ぼくたちが旅をしている間も、ずっと、見張られていた。", speaker: "ユーリ" },
            { type: "setFlag", flag: "chapter7_console_found", value: true },
            { type: "message", text: "ミナの指先が、卓の端にふれた。青白い光が爆ぜ、卓は歪みの姿となって襲いかかってきた！" },
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
            { type: "message", text: "静まった卓の向こうから、ゆっくりと足音が近づいてきた。紺の衣をまとった、五十代半ばの女性だ。" },
            {
              type: "message",
              text: "見事な戦いでした。ここまで辿り着く人は、そう多くありません。……あなた方が、初めてです。",
              speaker: "エドレア",
            },
            { type: "message", text: "合議会代表の……エドレア！ あなたが、これを？", speaker: "ユーリ" },
            {
              type: "message",
              text: "わたしの言葉を信じるかどうかは、あなた方次第です。ただ、ここで多くを語るつもりはありません。",
              speaker: "エドレア",
            },
            { type: "message", text: "祖父の名は、ハクエイといいます。祖父は、どこにいるのですか。", speaker: "アヤメ" },
            {
              type: "message",
              text: "ハクエイ殿。穏やかな方でした。何度か、茶をご一緒しました。……それを、ここで話すつもりはありません。",
              speaker: "エドレア",
            },
            {
              type: "message",
              text: "レトさん。お兄さまは、合議会の書記官でしたね。聡明な方でした。",
              speaker: "エドレア",
            },
            { type: "message", text: "……兄の名を、口にするな。", speaker: "レト" },
            {
              type: "message",
              text: "ユーリさん。あなたは、お祖父さまに似ておいでです。人の話を、最後まで聞く方でした。",
              speaker: "エドレア",
            },
            { type: "message", text: "祖父を、知っているんですか。", speaker: "ユーリ" },
            {
              type: "message",
              text: "続きは、灯芯都で。合議会の広間で、お待ちしています。……真実が知りたければ、いらっしゃい。",
              speaker: "エドレア",
            },
            {
              type: "message",
              text: "わたしは、大乱期を二度と繰り返さないために生きてきました。平和は、あなた方が思うより、ずっと脆いものです。",
              speaker: "エドレア",
            },
            { type: "message", text: "エドレアは静かに背を向け、待たせていた空の船に乗って雲の向こうへ消えた。" },
            {
              type: "message",
              text: "床に、書き付けが落ちていた。「灯芯都・合議会堂にて、お待ちしております」。最後の払いは、帳簿の署名と同じ形だった。",
            },
            { type: "message", text: "あの顔を、何年も、信じてたんだぞ。……合議会の代表は、正しい人だって。", speaker: "レト" },
            { type: "message", text: "信じたかったから、信じたんです。それは、弱さじゃありません。", speaker: "ユーリ" },
            { type: "setFlag", flag: "chapter7_edrea_appeared", value: true },
          ],
        },
      ],
      else: [{ type: "message", text: "拠点の奥は静かだ。人の気配は、まだ感じられない。" }],
    },
  ];
}
