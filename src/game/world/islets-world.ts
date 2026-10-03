import { BEFORE_GATE, buildFloor, DEEP_ENTRY, DEEP_LANDMARKS } from "../map/chapter10/deep-maps";
import { WORLD_ISLETS } from "../map/world/world-map.generated";
import { describeBonus } from "../economy/shop";
import { TREASURE_ITEMS } from "../economy/treasure";
import { CHEST } from "../map/chapter12/dungeons";
import type { EventCommand } from "../event/types";
import type { TileMapData } from "../map/types";
import type { Npc } from "../npc";
import { gate, pedestal } from "./chapter10-world";
import { say } from "./side-story";

/**
 * 隠しダンジョンの小島（世界地図の海に浮かぶ4つの島）。それぞれ2階層（灯り石の台2つ→封印の扉→宝の間）。
 * 島へ渡るには、船・飛空艇と、物語の進み具合の条件が要る（`ISLET_REQUIREMENTS`）。
 * 宝箱には灯貨と、ここでしか手に入らない装備（`economy/treasure.ts`）が入っている。仮: ボスは置いていない。
 */
interface Islet {
  name: string;
  palette: { floor: string; wall: string; block: string; glow: string };
  blocks: [number, number][];
  intro: string;
  padA: string;
  padB: string;
  lore: string;
  chestText: string;
  gold: number;
  /** 渡る・入るために必要なフラグ（すべて立っていること）と、足りないときのヒント。 */
  requires: Array<{ flag: string; hint: string }>;
}

export const ISLETS: Islet[] = [
  {
    name: "月影の島",
    palette: { floor: "#8a98b8", wall: "#222a3c", block: "#4a5a7a", glow: "#e8f0ff" },
    blocks: [[5, 8], [14, 8], [3, 11], [16, 4]],
    intro: "月の光が、崩れた庭にだけ射している。島の名は、月影の島。",
    padA: "月のしずくのような灯り石が、そっと光った。",
    padB: "苔むした台の灯り石に、青白い光がともった。",
    lore: "崩れた石碑に、古い文字が彫られている。「環の守り人は、海のかなたの嵐を、ここから見守っていた」",
    chestText: "月影の庭の奥で、古い宝箱を開けた。中には、月のように白い装備が眠っていた。",
    gold: 5000,
    requires: [
      { flag: "has_ship", hint: "海を渡る船が要る。" },
      { flag: "chapter5_reported", hint: "霧断崖の予言の件を、片づけてから来よう。" },
    ],
  },
  {
    name: "底なしの井戸の島",
    palette: { floor: "#5a4a40", wall: "#1c1410", block: "#3a2c24", glow: "#ffb860" },
    blocks: [[6, 5], [13, 5], [9, 9], [2, 10]],
    intro: "島の中央に、底の見えない井戸が口を開けている。まわりの洞窟は、熱をはらんでいる。",
    padA: "洞窟の壁の灯り石が、赤く熱を帯びて光った。",
    padB: "井戸のふちの台が、ごうごうと遠い音を立てて、ともった。",
    lore: "井戸の底から、火山の息のような風が吹き上げる。「ここは、大地の鼓動を聞く場所」と、岩に刻まれている。",
    chestText: "洞窟の奥で、熱い宝箱を開けた。中には、火の力を宿した装備があった。",
    gold: 6500,
    requires: [
      { flag: "has_ship", hint: "海を渡る船が要る。" },
      { flag: "chapter6_reported", hint: "霜原の戦跡の件を、終えてから来よう。" },
    ],
  },
  {
    name: "古灯台の島",
    palette: { floor: "#a0a8a0", wall: "#2c302c", block: "#6a746a", glow: "#fff0a0" },
    blocks: [[4, 4], [15, 4], [7, 9], [12, 9]],
    intro: "海に突き出した岩の上に、折れた古い灯台が立っている。ここも、環灯台の仲間だったのかもしれない。",
    padA: "灯台の火皿のかけらに、小さな光がともった。",
    padB: "灯室のレンズのかけらが、日の光をはね返した。",
    lore: "「八つの灯台のほかに、もうひとつ、環を見守る灯台があった」。灯室の壁の記録が、そこで途切れている。",
    chestText: "灯室の奥の宝箱を開けた。中には、嵐をしのぐ外套と、深い海の底にも光を届ける「灯室のレンズ」があった。",
    gold: 7500,
    requires: [
      { flag: "has_ship", hint: "海を渡る船が要る。" },
      { flag: "chapter7_reported", hint: "浮嶼の件を、片づけてから来よう。" },
    ],
  },
  {
    name: "忘れられた砦の島",
    palette: { floor: "#585068", wall: "#1a1624", block: "#3a3048", glow: "#d8a0ff" },
    blocks: [[7, 8], [12, 8], [5, 11], [14, 11]],
    intro: "雲の上から見下ろすと、海の果てに、小さな砦の島が浮かんでいる。空からでなければ、近づけない。",
    padA: "砦の見張り台の灯り石が、紫の光をともした。",
    padB: "砦の広間の台に、灯が入った。旗が、ひとりでに揺れた。",
    lore: "「ここは、浮嶼平定戦のとき、雲海衆が最後まで守った砦」。壁に、奪われた空への祈りが彫られている。",
    chestText: "砦の奥の宝箱を開けた。中には、空を駆ける風のような装備があった。",
    gold: 9000,
    requires: [
      { flag: "has_airship", hint: "空から行く手段が要る。" },
      { flag: "chapter8_reported", hint: "灯芯都の件を、終えてから来よう。" },
    ],
  },
  {
    name: "青い穴の洲",
    palette: { floor: "#2a5a78", wall: "#0a1a30", block: "#1a3c5a", glow: "#80e8ff" },
    blocks: [[4, 5], [15, 5], [8, 9], [12, 9]],
    intro: "青い穴をくぐると、息ができた。灯りの消えた街並みが、海の底に沈んでいる。ここは、沈んだ灯の都。",
    padA: "珊瑚の灯り石が、青い光をゆらゆらと放った。",
    padB: "沈んだ広場の台に、泡のような灯がともった。",
    lore: "「海が環を飲みこむ前、ここにも灯の都があった」。傾いた石碑の文字を、魚の群れがかすめていく。",
    chestText: "沈んだ神殿の奥の宝箱を開けた。中には、潮の流れをあやつる装備が眠っていた。",
    gold: 11000,
    requires: [
      { flag: "has_ship", hint: "海を渡る船が要る。" },
      { flag: "chapter7_reported", hint: "浮嶼の件を、片づけてから来よう。" },
      { flag: "islet3_treasure", hint: "海の底は暗い。古灯台の島の「灯室のレンズ」を手に入れてから潜ろう。" },
    ],
  },
  {
    name: "火口の迷宮",
    palette: { floor: "#6a3022", wall: "#1c0a08", block: "#3c1a12", glow: "#ff8a30" },
    blocks: [[5, 5], [14, 5], [3, 10], [16, 10]],
    intro: "火山の腹の中は、赤い光に満ちている。溶岩の川が、迷宮の床すれすれを流れていく。",
    padA: "溶岩の熱を吸った灯り石が、ごうっと燃え上がった。",
    padB: "黒曜石の台に、火の粉のような灯がともった。",
    lore: "「大地の鼓動は、環の鼓動でもある」。冷えた溶岩に、そんな言葉が焼きつけられている。",
    chestText: "火口の底の宝箱を開けた。熱でゆがんだ蓋の下から、燃え立つ赤い装備が現れた。",
    gold: 13000,
    requires: [
      { flag: "chapter8_reported", hint: "灯芯都の件を、終えてから来よう。" },
      { flag: "islet2_treasure", hint: "火口の熱は、ふつうの装備では耐えられない。底なしの井戸の島の「火を宿した装備」を手に入れよう。" },
    ],
  },
];

/** 小島の入口に必要な条件を、世界地図で確かめる（`main.ts`）。足りなければ、ヒントの文を返す。 */
export function isletRequirementHint(isletMapId: string, flags: Record<string, boolean>): string[] {
  const n = Number(isletMapId.replace("islet-", "").split("-")[0]);
  const islet = ISLETS[n - 1];
  if (!islet) {
    return [];
  }
  return islet.requires.filter((r) => !flags[r.flag]).map((r) => r.hint);
}

const isletMapId = (n: number, floor: 1 | 2): string => `islet-${n}-${floor}`;

export const ISLET_MAPS: Record<string, TileMapData> = Object.fromEntries(
  ISLETS.flatMap((islet, i) => {
    const n = i + 1;
    const pos = WORLD_ISLETS[i];
    return [
      [isletMapId(n, 1), buildFloor(islet.palette, islet.blocks, { targetMapId: "world-map", targetTileX: pos.x, targetTileY: pos.y + 1 })],
      [isletMapId(n, 2), buildFloor(islet.palette, [[5, 8], [14, 8]], { targetMapId: isletMapId(n, 1), targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY })],
    ];
  }),
);

function chest(n: number, islet: Islet): Npc {
  const flag = `islet${n}_treasure`;
  const treasure = TREASURE_ITEMS[n - 1];
  const commands: EventCommand[] = [
    {
      type: "if",
      flag,
      equals: true,
      then: [say(undefined, "宝箱は、すでに空だ。")],
      else: [
        say(undefined, islet.chestText),
        { type: "giveGold", amount: islet.gold },
        say(undefined, `【ごほうび】灯貨${islet.gold}を手に入れた！`),
        { type: "giveEquipment", itemId: treasure.id },
        say(undefined, `【ごほうび】${treasure.name}を手に入れた！（${describeBonus(treasure)}）強ければ、その場で身につけた。`),
        { type: "setFlag", flag, value: true },
      ],
    },
  ];
  return { id: `islet${n}-chest`, ...CHEST, color: "#e8c860", commands };
}

export const ISLET_NPCS: Record<string, Npc[]> = Object.fromEntries(
  ISLETS.flatMap((islet, i) => {
    const n = i + 1;
    const L = DEEP_LANDMARKS;
    return [
      [
        isletMapId(n, 1),
        [
          { id: `islet${n}-pedestal-a`, ...L.pedestalA, color: islet.palette.glow, commands: pedestal(`islet${n}`, "a", islet.padA) },
          { id: `islet${n}-pedestal-b`, ...L.pedestalB, color: islet.palette.glow, commands: pedestal(`islet${n}`, "b", islet.padB) },
          { id: `islet${n}-lore`, ...L.echo, color: "#9a9aa8", commands: [say(undefined, islet.intro), say(undefined, islet.lore)] },
          { id: `islet${n}-gate`, ...L.gate, color: islet.palette.glow, commands: gate(`islet${n}`, isletMapId(n, 2), DEEP_ENTRY) },
        ],
      ],
      [isletMapId(n, 2), [chest(n, islet)]],
    ];
  }),
);
