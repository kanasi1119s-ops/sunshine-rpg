import { ENCOUNTER_ZONES, encounterMonsterSpec } from "../encounter/encounter";
import { MONSTERS } from "../monster/monsters";
import type { MapExit, TileMapData } from "../map/types";
import { carveMap } from "../map/carve-map";
import { serpentineLayout, type Landmarks, type SerpentineLayout } from "../map/serpentine";
import { isWalkable, createTileMap } from "../map/tile-map";
import type { Npc } from "../npc";
import type { EventCommand } from "../event/types";
import { chestNpc, leverNpc, loreNpc } from "./dungeon-objects";
import { DUNGEON_BIOME, DUNGEON_PARENT } from "./dungeon-parent";

/**
 * 第2章〜第8章の「町 → ボス」の間に、洞窟や塔のダンジョンを2つ足す
 * （人間の指摘「ボスまでのダンジョン的なものは必要。塔でも洞窟でもいい」2026-10-05）。
 * 町の出口に条件（情報屋の話を聞く）をつけ、1つ目のダンジョンで宝箱と寄り道、2つ目で左右のレバー（2つとも動かすと奥の門が開く）を置く。
 * 地図の形は章ごとに共通で、見た目（洞窟・塔・遺跡・施設）と文だけが章ごとに変わる。
 */
interface ChapterDungeon {
  n: number;
  town: string;
  boss: string;
  /** 足す地図のID（`<id>-1`・`<id>-2`）。 */
  id: string;
  theme: "mine" | "tower" | "ruins" | "facility";
  biome: "cave" | "ruins";
  /** 地図の名前（表示用ではなく、ヒントの文に使う）。 */
  place: [string, string];
  /** 町の情報屋。 */
  informant: { name: string; color: string; lines: string[]; afterLines: string[] };
  /** 2つ目のダンジョンのレバー。 */
  lever: { thing: string; pull: string };
  chestText: [string, string, string];
  travelerLines: string[];
  loreLines: string[];
}

const DUNGEONS: ChapterDungeon[] = [
  {
    n: 2, town: "garasuko-town", boss: "garasuko-warehouse", id: "garasuko-cave", theme: "mine", biome: "cave",
    place: ["湖畔の洞窟", "倉庫の裏の坑道"],
    informant: {
      name: "船頭", color: "#9ab0c8",
      lines: ["密輸倉庫へ行くのかい。表の道は見張りがいる。湖畔の洞窟を抜ければ、倉庫の裏手に出られるよ。", "洞窟の奥の門は、左右の「荷揚げ台」を動かすと開く仕掛けだ。昔の船乗りが作ったらしい。"],
      afterLines: ["洞窟は暗くて足もとが濡れてる。足をとられないように行きな。"],
    },
    lever: { thing: "荷揚げ台", pull: "荷揚げ台の綱を引く" },
    chestText: ["洞窟の岩かげの宝箱を開けた！", "くぼみの古い宝箱を開けた！", "裏手の坑道の宝箱を開けた！"],
    travelerLines: ["この洞窟は、湖の底の水が岩に染みて、いつも湿っているんだ。", "東の脇道と、南西のくぼみに、運び屋が隠した宝箱があるって話だよ。"],
    loreLines: ["岩に、船乗りの落書きがある。「ふたつの台を引けば、裏戸が開く」"],
  },
  {
    n: 3, town: "tetsukusari-town", boss: "tetsukusari-mine", id: "tetsukusari-cave", theme: "mine", biome: "cave",
    place: ["旧い坑道", "崩れかけの深坑"],
    informant: {
      name: "古参の鉱夫", color: "#a08060",
      lines: ["坑内の実験装置の話か。会社の入口は閉ざされてるが、昔掘った旧い坑道から回り込める。", "ただ、旧坑の奥の落盤止めは、左右のトロッコ分岐レバーを引かないと開かん。二人で引く仕掛けだ。"],
      afterLines: ["旧坑は崩れかけだ。無茶はするな。"],
    },
    lever: { thing: "トロッコ分岐レバー", pull: "トロッコの分岐レバーを引く" },
    chestText: ["旧坑の木箱を開けた！", "くぼみの古い木箱を開けた！", "深坑の宝箱を開けた！"],
    travelerLines: ["旧坑には、昔の鉱夫が置いてったお宝が、まだ眠ってるらしいよ。", "東の脇道と、南西のくぼみを探してみな。"],
    loreLines: ["坑道の壁に、鉱夫の刻み文字がある。「分かれ道は、ふたりで引け」"],
  },
  {
    n: 4, town: "sanone-town", boss: "sanone-camp", id: "sanone-ruins", theme: "ruins", biome: "ruins",
    place: ["砂に埋もれた遺跡", "古い隊商路の奥"],
    informant: {
      name: "古老", color: "#c8a868",
      lines: ["野営地への近道がある。砂丘の下に眠る古い遺跡を抜けるのだ。", "遺跡の奥の石戸は、左右の「風見の石」を回すと開く。風が、鍵なのだよ。"],
      afterLines: ["遺跡の中は砂が崩れやすい。気をつけて。"],
    },
    lever: { thing: "風見の石", pull: "風見の石を回す" },
    chestText: ["砂に埋もれた宝箱を開けた！", "遺跡のくぼみの宝箱を開けた！", "奥の間の宝箱を開けた！"],
    travelerLines: ["遺跡には、昔の隊商の財宝が残ってるんだとさ。", "東の脇道と、南西のくぼみに、砂をかぶった箱があるよ。"],
    loreLines: ["石壁に、風の模様が彫られている。「ふたつの風が揃うとき、戸は開く」"],
  },
  {
    n: 5, town: "kiri-town", boss: "kiri-archive", id: "kiri-tower", theme: "tower", biome: "ruins",
    place: ["崖ぞいの石の塔", "塔の上層の回廊"],
    informant: {
      name: "巡礼の案内人", color: "#a0a8c0",
      lines: ["記録の間へは、崖ぞいの石の塔をのぼるのが、古い巡礼の道だよ。", "塔の上の扉は、左右の「封印の書見台」に灯りをかざすと開く。ふたつ揃えるのがきまりだ。"],
      afterLines: ["塔は霧でぬれて滑る。足もとに気をつけて。"],
    },
    lever: { thing: "封印の書見台", pull: "書見台に灯りをかざす" },
    chestText: ["塔の隅の宝箱を開けた！", "くぼみの宝箱を開けた！", "回廊の宝箱を開けた！"],
    travelerLines: ["塔には、昔の司祭が隠したお布施が残っているって噂だよ。", "東の脇道と、南西のくぼみを探してごらん。"],
    loreLines: ["石碑に文字がある。「記録を守る者は、ふたつの灯をともせ」"],
  },
  {
    n: 6, town: "shimohara-town", boss: "shimohara-facility", id: "shimohara-ruins", theme: "facility", biome: "ruins",
    place: ["雪原の戦跡", "施設の地下通路"],
    informant: {
      name: "古い兵の子孫", color: "#a0a0b8",
      lines: ["戦跡の施設へは、雪の下の古い通路から入れる。入口は雪で隠れているが、わしが道を教えよう。", "地下通路の隔壁は、左右の「凍った制御盤」を動かさないと開かん。ふたつ同時に生きている盤だ。"],
      afterLines: ["地下は冷える。凍えないようにな。"],
    },
    lever: { thing: "凍った制御盤", pull: "凍った制御盤の氷をはらって押す" },
    chestText: ["雪に埋もれた箱を開けた！", "くぼみの鉄箱を開けた！", "地下通路の宝箱を開けた！"],
    travelerLines: ["戦の頃の兵糧や武具が、まだ雪の下に眠ってるって話さ。", "東の脇道と、南西のくぼみに、鉄の箱があるはずだよ。"],
    loreLines: ["錆びた銘板がある。「ふたつの盤を生かせ。さもなくば、隔壁は閉ざされたまま」"],
  },
  {
    n: 7, town: "fushima-town", boss: "fushima-base", id: "fushima-tower", theme: "tower", biome: "ruins",
    place: ["浮橋の古い塔", "基地へ続く塔の上層"],
    informant: {
      name: "雲海衆の見張り", color: "#8090b0",
      lines: ["基地へは、浮橋のさきの古い塔を抜けていく。わしらの先祖が建てた塔だ。", "塔の上の門は、左右の「風車の歯車」を回すと開く。風を二つ、そろえるんだ。"],
      afterLines: ["塔は風が強い。落ちないようにな。"],
    },
    lever: { thing: "風車の歯車", pull: "風車の歯車を回す" },
    chestText: ["塔の隅の宝箱を開けた！", "くぼみの宝箱を開けた！", "上層の宝箱を開けた！"],
    travelerLines: ["雲海衆は、塔のあちこちに宝を隠すのが習わしなのさ。", "東の脇道と、南西のくぼみを探してみるといい。"],
    loreLines: ["塔の壁に、雲海衆の言葉。「ふたつの風を揃えよ。さらば、空は開く」"],
  },
  {
    n: 8, town: "toushin-town", boss: "toushin-hall", id: "toushin-tower", theme: "tower", biome: "ruins",
    place: ["都の古い塔", "会堂へ続く回廊"],
    informant: {
      name: "年老いた書記", color: "#8a90b0",
      lines: ["合議会堂の審問へ行くなら、表の道は衛兵が固めておる。都の古い塔から回廊に出られる。", "回廊の扉は、左右の「灯りの燭台」に火を入れると開く。古い規則でな。"],
      afterLines: ["会堂は静かだが、油断するな。"],
    },
    lever: { thing: "灯りの燭台", pull: "燭台に火を入れる" },
    chestText: ["塔の隅の宝箱を開けた！", "くぼみの宝箱を開けた！", "回廊の宝箱を開けた！"],
    travelerLines: ["この塔は、会堂ができる前からあるんだってさ。", "東の脇道と、南西のくぼみに、古い箱があるって聞いたよ。"],
    loreLines: ["壁の銘文。「ふたつの灯がともるとき、審問の間は開かれる」"],
  },
];

const FLOOR = 1;
const WALL = 2;
const COLORS: Record<number, string> = { [FLOOR]: "#5a4630", [WALL]: "#2a1f16" };

/** 章ごとに、形（小部屋の位置）を変える。通路は5本で、フィールドを歩くように長い。 */
function layoutsFor(n: number): [SerpentineLayout, SerpentineLayout] {
  return [
    serpentineLayout({ lanes: 5, wall: WALL, floor: FLOOR, seed: n * 10 + 1 }),
    serpentineLayout({ lanes: 5, wall: WALL, floor: FLOOR, seed: n * 10 + 2 }),
  ];
}

const pick = (l: Landmarks, i: number): { tileX: number; tileY: number } => l.alcoves[Math.min(i, l.alcoves.length - 1)];

function say(text: string, speaker?: string): EventCommand {
  return { type: "message", text, speaker };
}

function findExit(data: TileMapData | undefined, target: string): MapExit | undefined {
  return data?.exits?.find((e) => e.targetMapId === target);
}

/** 出口から歩いて3〜6マス離れた、通れる場所（情報屋を置く）。 */
function pickInformantTile(town: TileMapData, taken: Set<string>, from: { x: number; y: number }): { tileX: number; tileY: number } | null {
  const map = createTileMap(town);
  const seen = new Map<string, number>([[`${from.x},${from.y}`, 0]]);
  const queue = [{ x: from.x, y: from.y }];
  const candidates: { x: number; y: number; d: number }[] = [];
  while (queue.length > 0) {
    const cur = queue.shift()!;
    const d = seen.get(`${cur.x},${cur.y}`)!;
    if (d >= 3 && d <= 6 && !taken.has(`${cur.x},${cur.y}`)) candidates.push({ ...cur, d });
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = cur.x + dx;
      const ny = cur.y + dy;
      if (isWalkable(map, nx, ny) && !seen.has(`${nx},${ny}`)) {
        seen.set(`${nx},${ny}`, d + 1);
        queue.push({ x: nx, y: ny });
      }
    }
  }
  const pick = candidates.find((c) => c.d === 4) ?? candidates[0];
  return pick ? { tileX: pick.x, tileY: pick.y } : null;
}

function informantCommands(d: ChapterDungeon): EventCommand[] {
  const n = d.n;
  const who = d.informant.name;
  return [
    {
      type: "if",
      flag: `chapter${n}_prep_done`,
      equals: true,
      then: d.informant.afterLines.map((t) => say(t, who)),
      else: [
        {
          type: "if",
          flag: `chapter${n}_quest_accepted`,
          equals: true,
          then: [...d.informant.lines.map((t) => say(t, who)), { type: "setFlag", flag: `chapter${n}_prep_done`, value: true }],
          else: [say("何か困りごとかい？ 相談所の依頼を受けてから、また来な。道を教えてやろう。", who)],
        },
      ],
    },
  ];
}

/**
 * 地図とNPCに、ダンジョンを足す。`maps` は、章の地図と模様の指定がすべて済んだ状態のもの。
 * `npcsByMap` は、章のNPCをまとめたもの（ここに足す）。
 */
export function addChapterDungeons(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  for (const d of DUNGEONS) {
    const town = maps[d.town];
    const boss = maps[d.boss];
    const toBoss = findExit(town, d.boss);
    const toTown = findExit(boss, d.town);
    if (!town || !boss || !toBoss || !toTown) continue;
    const id1 = `${d.id}-1`;
    const id2 = `${d.id}-2`;
    const gateOpen = `chapter${d.n}_gate_open`;

    const [lay1, lay2] = layoutsFor(d.n);
    const l1 = lay1.landmarks;
    const l2 = lay2.landmarks;
    const common = { tileColors: COLORS, tileArt: { [FLOOR]: "tint:flagstone", [WALL]: "tint:brick" } };
    const map1 = carveMap(lay1.spec, {
      ...common,
      exits: [
        { tileX: l1.south.x, tileY: l1.south.y, targetMapId: d.town, targetTileX: toTown.targetTileX, targetTileY: toTown.targetTileY },
        { tileX: l1.north.x, tileY: l1.north.y, targetMapId: id2, targetTileX: l2.southArrival.tileX, targetTileY: l2.southArrival.tileY },
      ],
    });
    const map2 = carveMap(lay2.spec, {
      ...common,
      exits: [
        { tileX: l2.south.x, tileY: l2.south.y, targetMapId: id1, targetTileX: l1.northArrival.tileX, targetTileY: l1.northArrival.tileY },
        {
          tileX: l2.north.x,
          tileY: l2.north.y,
          targetMapId: d.boss,
          targetTileX: toBoss.targetTileX,
          targetTileY: toBoss.targetTileY,
          requireFlag: gateOpen,
          blockedMessage: `奥の門は固く閉ざされている。ダンジョンのあちこちにある${d.lever.thing}を、ふたつとも探して動かしてみよう。`,
        },
      ],
    });
    map1.theme = d.theme;
    map2.theme = d.theme;
    maps[id1] = map1;
    maps[id2] = map2;

    // つなぎかえ: 町 → 1つ目 → 2つ目 → ボスの地図 → (戻ると) 2つ目
    toBoss.targetMapId = id1;
    toBoss.targetTileX = l1.southArrival.tileX;
    toBoss.targetTileY = l1.southArrival.tileY;
    toBoss.requireFlag = `chapter${d.n}_prep_done`;
    toBoss.blockedMessage = `${d.place[0]}を通ってボスのもとへ向かう道があるらしい。まず町で、${d.informant.name}に話を聞いてみよう（相談所の依頼を受けてから）。`;
    toTown.targetMapId = id2;
    toTown.targetTileX = l2.northArrival.tileX;
    toTown.targetTileY = l2.northArrival.tileY;

    DUNGEON_PARENT[id1] = d.boss;
    DUNGEON_PARENT[id2] = d.boss;
    DUNGEON_BIOME[id1] = d.biome;
    DUNGEON_BIOME[id2] = d.biome;
    const zone = ENCOUNTER_ZONES[d.boss];
    if (zone) {
      ENCOUNTER_ZONES[id1] = { ...zone, level: Math.max(2, zone.level - 1) };
      ENCOUNTER_ZONES[id2] = { ...zone };
      // 敵の絵（`monsters.ts` は先に作られているので、足した地図の分をここで足す）
      for (const mapId of [id1, id2]) {
        for (let variant = 0; variant < ENCOUNTER_ZONES[mapId].names.length; variant++) {
          MONSTERS[`enc-${mapId}-${variant}`] = encounterMonsterSpec(ENCOUNTER_ZONES[mapId], variant);
        }
      }
    }

    // NPC
    const gold = d.n * 40;
    (npcsByMap[id1] ??= []).push(
      loreNpc(`${d.id}-lore-sign`, l1.nearExit, d.loreLines),
      {
        id: `${d.id}-traveler`,
        ...l1.nearEntry,
        color: "#7a9ab0",
        commands: d.travelerLines.map((l) => say(l, "旅人")),
      },
      chestNpc(`${d.id}-chest-east`, pick(l1, 2), `chapter${d.n}_chest_east`, { gold }, d.chestText[0]),
      chestNpc(`${d.id}-chest-hidden`, pick(l1, 6), `chapter${d.n}_chest_hidden`, { gold: Math.round(gold * 1.5) }, d.chestText[1]),
    );
    (npcsByMap[id2] ??= []).push(
      leverNpc(`${d.id}-panel-west`, pick(l2, 1), `chapter${d.n}_lever_west`, `chapter${d.n}_lever_east`, gateOpen, {
        pull: `西の${d.lever.thing}。${d.lever.pull}と、低い音が響いた。`,
        already: `西の${d.lever.thing}は、もう動かしてある。`,
        opened: `東の${d.lever.thing}も動いている。奥で、重い門の開く音がした！`,
        waiting: "遠くで何かが目覚める気配がする。反対側にも、同じものがあるはずだ。",
      }),
      leverNpc(`${d.id}-panel-east`, pick(l2, 6), `chapter${d.n}_lever_east`, `chapter${d.n}_lever_west`, gateOpen, {
        pull: `東の${d.lever.thing}。${d.lever.pull}と、低い音が響いた。`,
        already: `東の${d.lever.thing}は、もう動かしてある。`,
        opened: `西の${d.lever.thing}も動いている。奥で、重い門の開く音がした！`,
        waiting: "遠くで何かが目覚める気配がする。反対側にも、同じものがあるはずだ。",
      }),
      chestNpc(`${d.id}-chest-deep`, pick(l2, 4), `chapter${d.n}_chest_deep`, { gold: gold * 2 }, d.chestText[2]),
      loreNpc(`${d.id}-lore-wall`, l2.nearExit, [`${d.place[1]}。`, ...d.loreLines]),
    );
    // 町の情報屋
    const taken = new Set((npcsByMap[d.town] ?? []).map((n) => `${n.tileX},${n.tileY}`));
    const tile = pickInformantTile(town, taken, { x: toBoss.tileX, y: toBoss.tileY });
    if (tile) {
      (npcsByMap[d.town] ??= []).push({
        id: `${d.id}-informant`,
        ...tile,
        color: d.informant.color,
        commands: informantCommands(d),
      });
    }
  }
}

/** 章ごとの、足したダンジョンの準備・仕掛けのフラグ（ボスを倒した人は、済んでいるものとして扱う）。 */
export const DUNGEON_PREP_FLAGS: { boss: string; flags: string[] }[] = DUNGEONS.map((d) => ({
  boss: `chapter${d.n}_yugami_defeated`,
  flags: [`chapter${d.n}_quest_accepted`, `chapter${d.n}_prep_done`, `chapter${d.n}_lever_west`, `chapter${d.n}_lever_east`, `chapter${d.n}_gate_open`],
}));
