import type { Combatant } from "../battle/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import type { TileMapData } from "../map/types";
import { createIllusion1Data, createIllusion2Data, createIllusion3Data, ILLUSION_ENTRY, ILLUSION_GATE, ILLUSION_LANDMARKS as L } from "../map/illusion/illusion-maps";
import { say } from "./side-story";

/**
 * 幻想の禁域「まぼろしの回廊」（2026-10-06、人間の指示「禁域幻想空間的なダンジョンも追加しよう。作るときドット絵にこだわりを持ってね」
 * 「幻想のダンジョンには謎解きもほしいかも」）。
 * 初源の歪みを倒すと、虚灯宮の外庭に「まぼろしの門」が現れる。星の海に水晶の板が浮かぶ3つの階に、謎解きが1つずつある。
 *  - 1階「色の間」: 詩を手がかりに、3本の水晶の柱の色を合わせる（西=沈む日の色＝赤、まん中=空を映す水の色＝青、東=生まれる葉の色＝緑）
 *  - 2階「虚空の道」: 虚空に見えるが歩ける「見えない道」を、マスのかどの星をたよりに渡る
 *  - 3階「問いの間」: 旅の思い出についての3つの問い（まちがえると、まぼろしの影と戦う）。その奥に、まぼろしの主
 * まぼろしの主は、旅の思い出を写しとった鏡のような存在（新しい真相は足さない。伏線台帳に影響なし）。絵は図形（仮）。
 */
export const ILLUSION_MAPS: Record<string, TileMapData> = {
  "illusion-1": createIllusion1Data(),
  "illusion-2": createIllusion2Data(),
  "illusion-3": createIllusion3Data(),
};

export const ILLUSION_BOSS_ID = "illusion-boss";
export const ILLUSION_PHANTOM_ID = "illusion-phantom";
export const ILLUSION_BOSS_FLAG = "illusion_boss_defeated";

export function createIllusionBoss(): Combatant {
  return { id: ILLUSION_BOSS_ID, name: "まぼろしの主", maxHp: 7300, hp: 7300, maxMp: 0, mp: 0, attack: 106, defense: 34, speed: 30, isEnemy: true, guarding: false, expReward: 15000 };
}

export function createIllusionPhantom(): Combatant {
  return { id: ILLUSION_PHANTOM_ID, name: "まぼろしの影", maxHp: 4200, hp: 4200, maxMp: 0, mp: 0, attack: 96, defense: 31, speed: 28, isEnemy: true, guarding: false, expReward: 7000 };
}

const warpTo = (mapId: string): EventCommand => ({ type: "warp", mapId, tileX: ILLUSION_ENTRY.tileX, tileY: ILLUSION_ENTRY.tileY });

// ───────────── 1階「色の間」─────────────
type Color = "red" | "blue" | "green";
const COLOR_LABEL: Record<Color, string> = { red: "夕日のような赤", blue: "海のような青", green: "若葉のような緑" };
/** 柱（西・まん中・東）の正しい色。 */
const ANSWER: Color[] = ["red", "blue", "green"];
const pillarOk = (i: number): string => `illusion_pillar${i + 1}_ok`;
const PILLAR_NAMES = ["西の柱", "まん中の柱", "東の柱"];

function pillarCommands(i: number): EventCommand[] {
  return [
    {
      type: "if",
      flag: "illusion1_open",
      equals: true,
      then: [say(undefined, `${PILLAR_NAMES[i]}は、${COLOR_LABEL[ANSWER[i]]}に、静かに光っている。`)],
      else: [
        say(undefined, `${PILLAR_NAMES[i]}。透きとおった水晶の柱だ。手をかざすと、色が変わりそうだ。`),
        {
          type: "choice",
          text: "何色に光らせますか？",
          options: (["red", "blue", "green"] as Color[]).map((c) => ({
            label: COLOR_LABEL[c],
            commands: [say(undefined, `柱が、${COLOR_LABEL[c]}に光った。`), { type: "setFlag", flag: pillarOk(i), value: c === ANSWER[i] } as EventCommand],
          })),
        },
      ],
    },
  ];
}

const POEM: EventCommand[] = [
  say(undefined, "床に、光る文字で詩が書かれている。"),
  say(undefined, "「沈む日の色を、西に。生まれる葉の色を、東に。そのあいだに、空を映す水の色。……三つの色がそろうとき、まぼろしの扉は開く」"),
  say("ミナ", "沈む日は、夕日。生まれる葉は、若葉。空を映す水は……海、ですね。"),
];

function gate1Commands(): EventCommand[] {
  const open: EventCommand[] = [
    say(undefined, "三本の柱の光が、ひとすじに結ばれ、北の扉の紋が消えた。"),
    { type: "setFlag", flag: "illusion1_open", value: true },
    warpTo("illusion-2"),
  ];
  const locked = [say(undefined, "扉には、三つの色の紋。……柱の色が、そろっていないようだ。床の詩を、もう一度読んでみよう。")];
  let cmds = open;
  for (let i = 2; i >= 0; i--) cmds = [{ type: "if", flag: pillarOk(i), equals: true, then: cmds, else: locked }];
  return [{ type: "if", flag: "illusion1_open", equals: true, then: [warpTo("illusion-2")], else: cmds }];
}

// ───────────── 2階「虚空の道」─────────────
const STELE2: EventCommand[] = [
  say(undefined, "小さな石碑に、こう刻まれている。「見えるものだけが、道ではない。四つの星がかどにならぶところを、ふめ」"),
  say("アヤメ", "……虚空の中に、星が四つ、四角にならんでいる所があるわ。よく見て。あそこが、見えない足場なのね。"),
  say("オルカ", "一歩ずつだ。足もとの星を、たしかめながら行け。"),
];

// ───────────── 3階「問いの間」─────────────
interface Question {
  ask: string;
  options: string[];
  answer: number;
}

const QUESTIONS: Question[] = [
  { ask: "「ユーリの腕輪の灯り石は、何色にかがやく？」", options: ["水色", "琥珀色", "紫"], answer: 1 },
  { ask: "「霧断崖の記録の石に、名前が彫り直された年は？」", options: ["統暦180年", "統暦210年", "統暦392年"], answer: 2 },
  { ask: "「浮嶼の嵐の夜、ヴィオンが投げた綱は、何のためのものだった？」", options: ["つなぐため", "切るため", "しばるため"], answer: 0 },
];
const questionFlag = (i: number): string => `illusion_q${i + 1}_ok`;

function doorCommands(i: number): EventCommand[] {
  const q = QUESTIONS[i];
  const pass: EventCommand = { type: "warp", mapId: "illusion-3", tileX: L.doors[i].tileX, tileY: L.doors[i].tileY - 1 };
  const ask: EventCommand[] = [
    say(undefined, "鏡のような扉が、まぼろしの声で問いかけてきた。"),
    say("問いの扉", q.ask),
    {
      type: "choice",
      text: "答えを選んでください。",
      options: q.options.map((label, k) => ({
        label,
        commands:
          k === q.answer
            ? [say("問いの扉", "……そのとおり。おまえたちは、旅を、ちゃんと覚えている。"), { type: "setFlag", flag: questionFlag(i), value: true } as EventCommand, pass]
            : [say("問いの扉", "……ちがう。忘れたものは、まぼろしになって、おまえたちを呑む。"), { type: "startBattle", battleId: ILLUSION_PHANTOM_ID } as EventCommand],
      })),
    },
  ];
  const prev: EventCommand[] = i === 0 ? ask : [{ type: "if", flag: questionFlag(i - 1), equals: true, then: ask, else: [say(undefined, "扉は、まだ、こちらを見ていない。")] }];
  return [{ type: "if", flag: questionFlag(i), equals: true, then: [say(undefined, "扉は、静かに道をあけている。"), pass], else: prev }];
}

function bossCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "illusion_boss_told",
      equals: true,
      then: [say("まぼろしの主", "……もう一度、見せておくれ。おまえたちの、ほんとうを。"), { type: "startBattle", battleId: ILLUSION_BOSS_ID }],
      else: [
        { type: "cinematic", on: true },
        say(undefined, "水晶の床の奥に、人の形をした光が立っていた。その顔は、見るたびに、ちがう誰かの顔になる。"),
        say("まぼろしの主", "ようこそ、まぼろしの回廊へ。わたしは、この禁域に流れこむ、旅人たちの思い出のうつし。"),
        say("まぼろしの主", "ここでは、楽しかった日も、つらかった日も、みな、きれいなまぼろしになる。……ずっと、ここにいれば、いい。"),
        say("ユーリ", "思い出は、大事です。でも、ぼくたちは、思い出の中には住めない。帰る場所があるから。"),
        say("コハク", "それに、思い出は、これからも増やすんだよ。止めちゃったら、もったいないでしょ。"),
        say("まぼろしの主", "……ならば、見せておくれ。まぼろしより強い、おまえたちの、ほんとうを。"),
        { type: "setFlag", flag: "illusion_boss_told", value: true },
        { type: "startBattle", battleId: ILLUSION_BOSS_ID },
      ],
    },
  ];
}

/** まぼろしの主を倒したあと（戦いのすぐあとに流れる）。 */
export const ILLUSION_BOSS_AFTER_VICTORY: EventCommand[] = [
  say("まぼろしの主", "……ああ。まぼろしは、ほんとうには、かなわない。"),
  say("まぼろしの主", "持っておいき。この回廊でいちばん澄んだ、思い出のかけらを。……いつか、帰ってからの話を、聞かせておくれ。"),
  say(undefined, "まぼろしの主は、星の海へ、ゆっくりと溶けていった。北の扉が、外庭へ通じる光の道に変わる。"),
  { type: "giveGold", amount: 20000 },
  say(undefined, "【ごほうび】灯貨20000を手に入れた！"),
];

function exitGateCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: ILLUSION_BOSS_FLAG,
      equals: true,
      then: [say(undefined, "光の道が、虚灯宮の外庭へ続いている。"), { type: "warp", mapId: "kyotoukyu-court", tileX: 17, tileY: 7 }],
      else: [say(undefined, "扉は、まぼろしの光にとざされている。")],
    },
  ];
}

const ENTRANCE: EventCommand[] = [
  {
    type: "if",
    flag: "deep_yugami_defeated",
    equals: true,
    then: [
      say(undefined, "外庭の空中に、星の海をうつした門が、ゆらゆらと浮かんでいる。のぞきこむと、水晶の床が、どこまでも続いていた。"),
      {
        type: "choice",
        text: "まぼろしの門へ入りますか？",
        options: [
          { label: "入る", commands: [warpTo("illusion-1")] },
          { label: "やめておく", commands: [] },
        ],
      },
    ],
    else: [say(undefined, "空が、すこしだけ、ゆらいで見える。")],
  },
];

export const ILLUSION_NPCS: Record<string, Npc[]> = {
  "kyotoukyu-court": [{ id: "illusion-entrance", tileX: 17, tileY: 6, color: "#a0a0f0", showWhenFlag: "deep_yugami_defeated", commands: ENTRANCE }],
  "illusion-1": [
    ...L.pillars.map((p, i): Npc => ({ id: `illusion-pedestal-${i + 1}`, ...p, color: "#c0d0f0", commands: pillarCommands(i) })),
    { id: "illusion-lore-poem", ...L.poem, color: "#70e0f0", commands: POEM },
    { id: "illusion1-gate", ...ILLUSION_GATE, color: "#c0d0f0", commands: gate1Commands() },
  ],
  "illusion-2": [
    { id: "illusion-stele", ...L.stele2, color: "#8a8ad0", commands: STELE2 },
    { id: "illusion2-gate", ...ILLUSION_GATE, color: "#c0d0f0", commands: [say(undefined, "虚空を渡りきった。扉の向こうから、問いかけるような声が聞こえる。"), warpTo("illusion-3")] },
  ],
  "illusion-3": [
    ...L.doors.map((d, i): Npc => ({ id: `illusion-door-${i + 1}`, ...d, color: "#d0d8ff", commands: doorCommands(i) })),
    { id: "illusion-boss", ...L.boss, color: "#e0e0ff", hideWhenFlag: ILLUSION_BOSS_FLAG, commands: bossCommands() },
    { id: "illusion3-gate", ...ILLUSION_GATE, color: "#c0d0f0", commands: exitGateCommands() },
  ],
};
