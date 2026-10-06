import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import { KYOTOUKYU_DREAM_LANDMARKS, KYOTOUKYU_STAIR_LANDMARKS } from "../map/chapter9/kyotoukyu-maps";
import { say } from "./side-story";

/**
 * 終章を厚くするために足した、光の階段と眠りの回廊（2026-10-06、人間の指示「8章クリアしてからのエドレアバトルが簡単すぎる。
 * 何か間色々入れたい」）。外庭 → 光の階段 → 環の回廊（壁画）→ 眠りの回廊 → 奥の間（エドレア、2段階の戦い）。
 *  - 光の階段: 石碑の手がかりから、月・星・陽の3つの台を正しい順にともす（まちがえると、ぜんぶ消える）。橋がかかると北へ渡れ、
 *    細い通路で「光の守り手」と戦う（小説の「光の守り手戦」）。
 *  - 眠りの回廊: 静めの間の力が漏れ、仲間5人それぞれに「眠りの誘い」の夢を見せる扉がある。夢の中で、目を覚ます答えを選ぶ
 *    （壁画の「みずから望みて」がヒント）。眠るほうを選ぶと、まどろみの番人と戦い、勝つと目が覚める。5つ越えると奥の扉が開く。
 * 夢は、各章でわかっている出来事だけを使い、新しい事実は足さない（伏線台帳に影響なし）。
 */

const S = KYOTOUKYU_STAIR_LANDMARKS;
const D = KYOTOUKYU_DREAM_LANDMARKS;

// ───────────── 光の階段 ─────────────
type Light = "moon" | "star" | "sun";
const LIGHT_NAME: Record<Light, string> = { moon: "月", star: "星", sun: "陽" };
/** 正しい順番: 夜（月）→ 夜明け前（星が消える前の明けの星）→ 朝（陽）。石碑の詩が手がかり。 */
const ORDER: Light[] = ["moon", "star", "sun"];
const litFlag = (l: Light): string => `chapter9_stair_${l}`;
export const STAIR_BRIDGE_FLAG = "chapter9_stair_bridge";
export const GUARDIAN_DEFEATED_FLAG = "chapter9_guardian_defeated";

function resetLights(): EventCommand[] {
  return ORDER.map((l) => ({ type: "setFlag", flag: litFlag(l), value: false }) as EventCommand);
}

function lightCommands(light: Light): EventCommand[] {
  const i = ORDER.indexOf(light);
  const name = LIGHT_NAME[light];
  const right: EventCommand[] = [
    say(undefined, `${name}の紋の台に、灯りを入れた。台が、やわらかく光りはじめる。`),
    { type: "setFlag", flag: litFlag(light), value: true },
    ...(i === ORDER.length - 1
      ? [
          say(undefined, "三つの台の光が、ひとすじに結ばれた。裂け目の上に、音もなく、光の橋がかかっていく。"),
          say("コハク", "やった！ ……ほら、言ったでしょ。夜があけるみたいに、って。"),
          { type: "setFlag", flag: STAIR_BRIDGE_FLAG, value: true } as EventCommand,
        ]
      : []),
  ];
  const wrong: EventCommand[] = [
    say(undefined, `${name}の紋の台に、灯りを入れた。……ほかの台の光が、ふっと、ぜんぶ消えてしまった。`),
    ...resetLights(),
    say("アヤメ", "順番が、ちがうみたい。石碑の詩を、もう一度、読んでみましょう。"),
  ];
  // 正しい順番の手前の台がともっていれば正解（最初の台はいつでも正解）
  const prev = ORDER[i - 1];
  const decide: EventCommand[] = prev ? [{ type: "if", flag: litFlag(prev), equals: true, then: right, else: wrong }] : [...resetLights(), ...right];
  return [
    {
      type: "if",
      flag: STAIR_BRIDGE_FLAG,
      equals: true,
      then: [say(undefined, `${name}の紋の台は、静かに光っている。`)],
      else: [{ type: "if", flag: litFlag(light), equals: true, then: [say(undefined, `${name}の紋の台は、もう光っている。`)], else: decide }],
    },
  ];
}

const STELE: EventCommand[] = [
  say(undefined, "古い石碑に、詩が刻まれている。"),
  say(undefined, "「夜に、白き面は、海を照らし。白きが沈めば、ひとつ残る、明けの光。その光も消えて、はじめて、橋はかかる。朝の、名において」"),
  say("レト", "白き面は、月だな。明けの光は……夜明け前に、最後まで残る星か。で、朝の名は、陽。"),
  say("ユーリ", "月、星、陽の順に、ともせばいいのかな。"),
];

const BRIDGE: EventCommand[] = [
  {
    type: "if",
    flag: STAIR_BRIDGE_FLAG,
    equals: true,
    then: [
      say(undefined, "光の橋を、一歩ずつ渡った。足の下は、底の見えない、白い闇だ。"),
      say("オルカ", "下は見るな。……前だけ見ろ。"),
      { type: "warp", mapId: "kyotoukyu-stair", tileX: S.across.tileX, tileY: S.across.tileY },
    ],
    else: [say(undefined, "裂け目の向こうに、細い通路が見える。だが、ここには、橋がない。三つの台に、何か仕掛けがありそうだ。")],
  },
];

const GUARDIAN: EventCommand[] = [
  {
    type: "if",
    flag: "chapter9_guardian_told",
    equals: true,
    then: [say(undefined, "光の守り手が、ふたたび、剣をかかげた。"), { type: "startBattle", battleId: "kyotoukyu-guardian" }],
    else: [
      { type: "cinematic", on: true },
      say(undefined, "細い通路の先に、光でできた人影が立っている。手には、光の剣。"),
      say("光の守り手", "……ここは、静めの間へ通じる道。宮の主の許しなく、通すことはできぬ。"),
      say("ユーリ", "主は、もういません。ここにいるのは、宮の力を勝手に使っている人です。ぼくたちは、それを止めに来ました。"),
      say("光の守り手", "言葉では、わからぬ。わたしは、眠る者たちを守るために造られた。……おまえたちの灯りが、眠る者を起こす灯りかどうか、確かめさせてもらう。"),
      say("ミナ", "起こしに来たんです。二十年、眠らされている人たちを。"),
      { type: "setFlag", flag: "chapter9_guardian_told", value: true },
      say(undefined, "光の守り手が、剣をかかげた！"),
      { type: "startBattle", battleId: "kyotoukyu-guardian" },
    ],
  },
];

/** 光の守り手を倒したあと（戦いのすぐあとに流れる）。 */
export const GUARDIAN_AFTER_VICTORY: EventCommand[] = [
  say("光の守り手", "……おまえたちの灯りは、あたたかい。眠りを奪う灯りではなく、目覚めを待つ灯りだ。"),
  say("光の守り手", "わたしは、四百年、ここに立っていた。眠る者を守るために。……いつのまにか、眠らせる者を、守らされていた。"),
  say("光の守り手", "行け。眠る者たちを、起こしてやってくれ。"),
  say(undefined, "光の守り手は、細かな光の粒になって、階段の上へ、ゆっくりと昇っていった。"),
];

// ───────────── 眠りの回廊 ─────────────
interface Dream {
  key: string;
  who: string;
  door: string;
  dream: EventCommand[];
  /** 選択肢（どれか1つが目を覚ます答え）。 */
  question: string;
  options: string[];
  awake: number;
  wake: EventCommand[];
  drowseName: string;
}

const DREAMS: Dream[] = [
  {
    key: "mina",
    who: "ミナ",
    door: "扉の向こうから、水の音と、子どもの笑い声が聞こえる。",
    dream: [
      say(undefined, "――麦香野の、初夏の夕暮れ。泉へつづく橋のたもと。"),
      say(undefined, "水色の灯り石を首から下げた女の子が、ふり返って、手をふっている。"),
      say("ハル", "ミナ、おそいよ。……ねえ、もう走らなくていいよ。ここで、ずっと、いっしょに遊ぼう。"),
      say("ハル", "ここなら、誰もいなくならないよ。怖いことも、悲しいことも、ないよ。"),
    ],
    question: "ミナに、何と声をかけますか？",
    options: ["「ここにいよう。ハルがいるなら」", "「ミナさん。ハルは、起きるのを待ってる」", "「怖いなら、眠ってもいい」"],
    awake: 1,
    wake: [say("ミナ", "……うん。ほんとうのハルは、この先で、眠ってる。夢のハルじゃなくて、起きたハルに、会いたい。"), say("ミナ", "ごめんね。今度は、わたしが、迎えに行くから。")],
    drowseName: "まどろみの水影",
  },
  {
    key: "orca",
    who: "オルカ",
    door: "扉の向こうから、つるはしの音と、男たちの笑い声が聞こえる。",
    dream: [
      say(undefined, "――鉄鏈の三番坑。崩れる前の、明るい坑道。"),
      say(undefined, "若い仲間たちが、灯りのついたヘルメットをかぶって、手をふっている。"),
      say("坑夫の仲間", "オルカ、遅いぞ。今日は早じまいだ。……なあ、もういいだろう。おまえは、十分、背負った。"),
      say("坑夫の仲間", "ここで、休んでいけ。もう誰も、おまえのせいだなんて、言わないから。"),
    ],
    question: "オルカに、何と声をかけますか？",
    options: ["「休んでいいと思います」", "「オルカさん。背負った荷は、ぼくたちが半分持ちます」", "「ここなら、誰も責めない」"],
    awake: 1,
    wake: [say("オルカ", "……そうだったな。ひとりで持たなくていい荷も、ある。お前たちが、そう教えた。"), say("オルカ", "すまん。まだ、休めん。病んだ若い衆の見舞いに、行かにゃならん。")],
    drowseName: "まどろみの坑道",
  },
  {
    key: "kohaku",
    who: "コハク",
    door: "扉の向こうから、そろばんの音と、にぎやかな市の声が聞こえる。",
    dream: [
      say(undefined, "――硝子湖の、湖鳥商会。帳簿はすべて正しく、密輸のうわさもない、明るい店先。"),
      say("ロウガ", "コハク、帰ったか。旅なんぞ、もうやめろ。ここで帳簿をつけていれば、誰も傷つかん。"),
      say("ロウガ", "危ない橋は、もう渡らなくていい。……商会の名も、おまえの名も、きれいなままだ。"),
    ],
    question: "コハクに、何と声をかけますか？",
    options: ["「きれいな帳簿のほうが、得だよ」", "「お父さんの言うとおりにしよう」", "「コハク。帳簿に書けないものを、取りに行こう」"],
    awake: 2,
    wake: [say("コハク", "……だよね。損得で決めるなら、この夢がいちばん得。でも、あたし、もう、そういう勘定はしないんだ。"), say("コハク", "父さんは、ほんとは、あたしに頭を下げてくれたんだよ。夢の父さんより、そっちのほうが、ずっといい。")],
    drowseName: "まどろみの帳場",
  },
  {
    key: "reto",
    who: "レト",
    door: "扉の向こうから、ペンの走る音と、なつかしい声が聞こえる。",
    dream: [
      say(undefined, "――灯芯都の、古い下宿。机に向かう兄の背中。床に寝ころんで、字の練習をする小さな弟。"),
      say("レトの兄", "また字を間違えたな。……いいさ、ゆっくりでいい。この街は、静かだからな。"),
      say("レトの兄", "ずっと、ここにいろ。俺も、どこにも行かない。静まりの年なんて、来なかったんだ。"),
    ],
    question: "レトに、何と声をかけますか？",
    options: ["「レトさん。お兄さんは、あの寝台で、待ってます」", "「来なかったことにしても、いいんじゃないですか」", "「もう少し、ここにいましょう」"],
    awake: 0,
    wake: [say("レト", "……ああ。わかってる。こいつは、兄貴じゃない。兄貴は、こんなに、甘いことは言わねえ。"), say("レト", "起こしに行くぞ。小言を言われに、な。")],
    drowseName: "まどろみの下宿",
  },
  {
    key: "ayame",
    who: "アヤメ",
    door: "扉の向こうから、雪をふむ音と、静かな祈りの声が聞こえる。",
    dream: [
      say(undefined, "――霜原の戦跡。雪の中、遺品に、酒をひとしずくかけて手を合わせる老人。"),
      say("ハクエイ", "アヤメ。よく来たね。……もう、調べなくていい。観察も、記録も、いらない。"),
      say("ハクエイ", "ここで、いっしょに、眠りを見守っていよう。眠る者の邪魔をせず、ただ、静かに。"),
    ],
    question: "アヤメに、何と声をかけますか？",
    options: ["「見守るだけで、いいと思います」", "「静かなのは、いいことです」", "「アヤメさん。おじいさんに、初めましてを言いに行こう」"],
    awake: 2,
    wake: [say("アヤメ", "……ええ。わたしの祖父は、眠りを、邪魔しないように手を合わせる人だった。眠らせる側に立つ人じゃない。"), say("アヤメ", "観察者は、もうやめたの。……行きましょう。起きた祖父に、孫ですって、言うために。")],
    drowseName: "まどろみの雪原",
  },
];

export const dreamDoneFlag = (key: string): string => `chapter9_dream_${key}_done`;
export const drowseBattleId = (key: string): string => `kyotoukyu-drowse-${key}`;

function dreamCommands(d: Dream): EventCommand[] {
  const fall: EventCommand[] = [
    say(undefined, "まどろみが、深くなっていく。夢の景色が、ゆがみ、ひとつの影になって、立ちあがった！"),
    { type: "startBattle", battleId: drowseBattleId(d.key) },
  ];
  return [
    {
      type: "if",
      flag: dreamDoneFlag(d.key),
      equals: true,
      then: [say(undefined, `${d.who}の夢の扉は、静かに閉じている。`)],
      else: [
        say(undefined, d.door),
        say(undefined, `扉にふれると、${d.who}が、ふらりと、扉の向こうへ吸いこまれた。みんなで、あとを追う。`),
        { type: "cinematic", on: true },
        { type: "screen", dark: true },
        ...d.dream,
        say(undefined, `${d.who}は、うっとりと目を細めている。このままでは、目を覚まさないかもしれない。`),
        {
          type: "choice",
          text: d.question,
          options: d.options.map((label, i) => ({
            label,
            commands:
              i === d.awake
                ? [{ type: "screen", dark: false } as EventCommand, ...d.wake, { type: "setFlag", flag: dreamDoneFlag(d.key), value: true } as EventCommand, say(undefined, `${d.who}が、目を覚ました。`)]
                : [say(`${d.who}`, "……そう、だね。このまま……。"), ...fall],
          })),
        },
      ],
    },
  ];
}

/** まどろみの番人を倒したあと（目が覚める）。 */
export function drowseAfterVictory(key: string): EventCommand[] {
  const d = DREAMS.find((x) => x.key === key)!;
  return [say(undefined, "影が砕け、夢の景色が、ひび割れていく。"), ...d.wake, { type: "setFlag", flag: dreamDoneFlag(d.key), value: true }, say(undefined, `${d.who}が、目を覚ました。`)];
}

export const DROWSE_BATTLES = DREAMS.map((d) => ({ key: d.key, battleId: drowseBattleId(d.key), name: d.drowseName }));

/** 眠りの回廊の扉（夢がひとつでも残っていれば、とざされている）。 */
function gateCommands(): EventCommand[] {
  const locked = [say(undefined, "北の扉は、眠りの紋にとざされている。……仲間たちの夢を、すべて越えなければ、開かないようだ。")];
  let cmds: EventCommand[] = [
    say(undefined, "五つの夢の扉が、すべて閉じた。北の扉に刻まれた紋が、ゆっくりと光を失っていく。"),
    say("ユーリ", "……みんな、いる？ ミナさん、オルカさん、コハク、レトさん、アヤメさん。"),
    say("レト", "いるよ。全員、起きてる。……さあ、行こう。最後の、奥の間だ。"),
    { type: "warp", mapId: "kyotoukyu-sanctum", tileX: 9, tileY: 11 },
  ];
  for (const d of [...DREAMS].reverse()) {
    cmds = [{ type: "if", flag: dreamDoneFlag(d.key), equals: true, then: cmds, else: locked }];
  }
  return cmds;
}

export const CHAPTER9_TRIAL_NPCS: Record<string, Npc[]> = {
  "kyotoukyu-stair": [
    { id: "kyotoukyu-stair-pedestal-moon", ...S.moon, color: "#c8d0f0", commands: lightCommands("moon") },
    { id: "kyotoukyu-stair-pedestal-star", ...S.star, color: "#f0f0c8", commands: lightCommands("star") },
    { id: "kyotoukyu-stair-pedestal-sun", ...S.sun, color: "#f8d088", commands: lightCommands("sun") },
    { id: "kyotoukyu-stair-stele", ...S.stele, color: "#8a8aa0", commands: STELE },
    { id: "kyotoukyu-stair-bridge", ...S.bridge, color: "#a8d4e8", commands: BRIDGE },
    { id: "kyotoukyu-guardian", ...S.guardian, color: "#e8f0ff", hideWhenFlag: GUARDIAN_DEFEATED_FLAG, commands: GUARDIAN },
  ],
  "kyotoukyu-dream": [
    ...DREAMS.map((d, i): Npc => ({ id: `kyotoukyu-dream-door-${d.key}`, ...D.doors[i], color: "#9a8ab8", commands: dreamCommands(d) })),
    { id: "kyotoukyu-dream-gate", ...D.gate, color: "#c8b8e8", commands: gateCommands() },
  ],
};
