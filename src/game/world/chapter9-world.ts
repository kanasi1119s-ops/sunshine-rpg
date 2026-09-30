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
  { type: "message", text: "おじいちゃん……きっと、この奥にいる。", speaker: "ユーリ" },
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
        {
          type: "message",
          text: "奥の回廊の壁には、この宮のいわれが刻まれています。読んでから進んでも、遅くはありませんよ。",
          speaker: "灯守り",
        },
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
          text: "二十年前の「静まりの年」に、要人たちが記憶を失って消えたのは、これのせいか。エドレアは、合議会の古い封印の記録から、この仕組みを知ったんだ。",
          speaker: "オルカ",
        },
        { type: "setFlag", flag: "chapter9_mural_right", value: true },
        {
          type: "if",
          flag: "chapter9_mural_left",
          equals: true,
          then: [
            { type: "message", text: "灯の環の由来と、静めの仕組み。二つがそろって、エドレアのやったことのすべてが、一本の線につながった。" },
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
            { type: "choice", text: "虚灯宮・深部へ降りますか?", options: [
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
            { type: "message", text: "ドルンが、扉の陰から静かに現れ、エドレアの前に立った。「いっしょに、償おう」と、短く言った。" },
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
            {
              type: "message",
              text: "わたしは、この宮の「静めの間」を、大陸全体に開こうとしています。争いを望む者の記憶を、すべて眠りの中へ。もう二度と、大乱期は来ない。",
              speaker: "エドレア",
            },
            { type: "message", text: "そんなの、みんなを二十年前のおじいちゃんと同じ目にあわせるってことじゃないか!", speaker: "ユーリ" },
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
        { type: "message", text: "ユーリ、大きくなったな。……さあ、灯里へ帰ろう。話したいことが、山ほどある。", speaker: "ソウイチ" },
      ],
      else: [
        {
          type: "if",
          flag: "chapter9_edrea_surrendered",
          equals: true,
          then: [
            { type: "message", text: "寝台の上で、老人が静かに眠っている。ユーリの腕輪と同じ、灯り石の腕輪が、その手首に光っていた。" },
            { type: "message", text: "おじいちゃん。……ユーリだよ。迎えに来たよ。", speaker: "ユーリ" },
            { type: "message", text: "エドレアが杖に手を触れると、腕輪の光が静かに解けていった。老人のまぶたが、ゆっくりと開く。" },
            { type: "message", text: "……ユーリ、か。ずいぶん、背が伸びたな。長い夢を、見ていた気がする。", speaker: "ソウイチ" },
            { type: "setFlag", flag: "chapter9_grandfather_rescued", value: true },
            { type: "message", text: "ユーリは、言葉にならないまま、祖父の胸に飛びこんだ。レトもミナも、そっと目をそらして笑った。" },
            {
              type: "message",
              text: "……あの日、わしは証拠を集めておった。エドレアが「争いのため」と言いながら、自分の手で争いの種をまいておることを、告発するために。",
              speaker: "ソウイチ",
            },
            { type: "message", text: "歪みは、この先もまだ、各地に残っている。みんなで、少しずつ鎮めていこう。", speaker: "アヤメ" },
            { type: "message", text: "こうして、灯りの相談所の旅は、ひとつの終わりを迎えた。灯芯都の合議会は、エドレアとドルンを、公正な場で裁くことになる。" },
            { type: "message", text: "――だが、帰り支度をするユーリの耳に、祖父の小さなつぶやきが届いた。" },
            {
              type: "message",
              text: "……まだ、何かが眠っておる。この宮の、もっと深いところに。あれは、二十年前の事件よりも、ずっと古いものじゃ。",
              speaker: "ソウイチ",
            },
            { type: "message", text: "★ メインストーリーをクリアしました！（虚灯宮の奥に、クリア後の道が開いた）" },
            { type: "setFlag", flag: "chapter9_cleared", value: true },
            { type: "setFlag", flag: "chapter9_secret_open", value: true },
          ],
          else: [
            { type: "message", text: "寝台の上で、老人が静かに眠っている。手首には、ユーリの腕輪とそっくりな灯り石の腕輪。" },
            { type: "message", text: "おじいちゃん……! 起きて、ねえ、おじいちゃん!", speaker: "ユーリ" },
            { type: "message", text: "呼びかけても、目を覚まさない。腕輪の光が、眠りを封じているようだ。まず、この宮の主と話をつけなければ。" },
          ],
        },
      ],
    },
  ];
}
