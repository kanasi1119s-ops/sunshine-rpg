import { WORLD_BEACONS, WORLD_FERRY, WORLD_TOWNS } from "../map/world/world-map.generated";
import { GODS } from "../battle/chapter11-enemies";
import type { EventCommand } from "../event/types";
import type { TileMapData } from "../map/types";
import type { Npc } from "../npc";
import { say } from "./side-story";

/**
 * 世界地図（大陸アルテシア）のつなぎと、クリア後の「渦への航路」のイベント（`docs/story/secret-boss.md` 4-2b）。
 *  - 各町の南の門と、世界地図の町のアイコンをつなぐ。
 *  - 8神の欠片を、各地方にある「環灯台」にささげる（8つ）。8つともともると、渦を覆う常嵐が割れ、渡し場から芯環塔へ船が出る。
 *  - 虚灯宮・深部の転移陣（`chapter10-world.ts`）は、欠片8つに加えて、この航路が開いていないと起動しない。
 */

/** 世界地図から町へ入るために、前の章を終えている必要があるフラグ（なければ入れない）。 */
export const WORLD_ENTRY_FLAG: Record<string, string> = {
  "mugikano-village": "chapter0_reported_to_kasen",
  "garasuko-town": "chapter1_reported_to_elder",
  "tetsukusari-town": "chapter2_reported_to_guide",
  "sanone-town": "chapter3_reported_to_orca",
  "kiri-town": "chapter4_reported",
  "shimohara-town": "chapter5_reported",
  "fushima-town": "chapter6_reported",
  "toushin-town": "chapter7_reported",
  "kyotoukyu-court": "chapter8_reported",
};

/** 環灯台の番号（神の番号）と、置かれる地方。 */
const BEACON_REGIONS = ["麦香野", "硝子湖", "鉄鏈鉱山", "砂音", "霧断崖", "霜原", "浮嶼", "灯芯都"];

/** 環灯台に灯る光の色（神ごと）。 */
export const BEACON_COLORS = ["#a8e070", "#7ad0e8", "#f08a3c", "#c8c0f0", "#f4f0d8", "#e0584c", "#d890f0", "#8a98c8"];

const ROUTE_LINES = [
  "ひとつ、水は高みから低みへ。流れに逆らわず、海へ出よ。",
  "ふたつ、羽音の止む朝に、霧は薄れる。",
  "みっつ、火は海を照らす道となる。",
  "よっつ、風の歌の止む夜に、海は黙る。",
  "いつつ、誓いは羅針となる。",
  "むっつ、争いの果ての岸辺を過ぎよ。",
  "ななつ、境を見ぬ者が、渦の目を教える。",
  "やっつ、鐘の鳴らぬ潮に、舟は沈まない。",
];

const beaconFlag = (no: number): string => `beacon${no}_lit`;

function allLitThen(then: EventCommand[], no: number): EventCommand[] {
  // 自分以外の7つが、すでにともっているか。
  let inner: EventCommand[] = then;
  for (let n = 8; n >= 1; n--) {
    if (n === no) continue;
    inner = [{ type: "if", flag: beaconFlag(n), equals: true, then: inner }];
  }
  return inner;
}

function beacon(no: number, pos: { x: number; y: number }): Npc {
  const god = GODS[no - 1];
  const region = BEACON_REGIONS[no - 1];
  return {
    id: `world-beacon-${no}`,
    tileX: pos.x,
    tileY: pos.y,
    color: BEACON_COLORS[no - 1],
    commands: [
      {
        type: "if",
        flag: "deep_yugami_defeated",
        equals: true,
        then: [
          {
            type: "if",
            flag: beaconFlag(no),
            equals: true,
            then: [say(undefined, `${region}の環灯台は、${god.kind}の光で、海をまっすぐに照らしている。`), say(undefined, `「${ROUTE_LINES[no - 1]}」`)],
            else: [
              {
                type: "if",
                flag: `god${no}_fragment`,
                equals: true,
                then: [
                  say(undefined, `${region}の海辺に、古い灯台が立っている。台座のくぼみが、${god.kind}の欠片と、ぴったり合う。`),
                  say(undefined, `欠片を台座に置くと、${god.kind}の光が塔をかけ上がり、海へ、一本の光の道をのばした。`),
                  say(undefined, `台座に、古い文字が浮かぶ。「${ROUTE_LINES[no - 1]}」`),
                  { type: "setFlag", flag: beaconFlag(no), value: true },
                  ...allLitThen(
                    [
                      say(undefined, "八つの環灯台の光が、海の上で、ひとつの環になった。"),
                      say(undefined, "遠い水平線で、渦を覆っていた常嵐が、音もなく、割れていく。"),
                      say(undefined, "★ 渦への航路が開いた！ 東の渡し場へ行こう。"),
                      { type: "setFlag", flag: "vortex_route_open", value: true },
                    ],
                    no,
                  ),
                ],
                else: [
                  say(undefined, `${region}の海辺に、古い灯台が立っている。台座のくぼみは、まだ空だ。`),
                  say(undefined, `${god.kind}を鎮めて、環の欠片を持ち帰れば、ここに光がともるだろう。`),
                ],
              },
            ],
          },
        ],
        else: [say(undefined, `${region}の海辺に、光のない古い灯台が立っている。いまは、ただの古い石塔だ。`)],
      },
    ],
  };
}

function ferryman(): Npc {
  return {
    id: "world-ferry",
    tileX: WORLD_FERRY.x,
    tileY: WORLD_FERRY.y,
    color: "#8a6a40",
    commands: [
      {
        type: "if",
        flag: "vortex_route_open",
        equals: true,
        then: [
          say("渡し守", "ほう、八つの灯りがそろったか。海が、こんなに静かなのは、初めて見る。"),
          {
            type: "choice",
            text: "渦の塔へ、船で渡りますか？",
            options: [
              {
                label: "渡る",
                commands: [
                  say("渡し守", "しっかりつかまっていな。渦の縁は、少し揺れるぞ。"),
                  say(undefined, "船は、光の道をたどって沖へ出た。やがて、空と海を巻きこむ大渦が、目の前に口を開ける。"),
                  say(undefined, "渦の中心に、雲の上までそびえる塔が見えた。船は、渦の目へ、静かに滑りこんでいく。"),
                  { type: "setFlag", flag: "tower_gate_open", value: true },
                  { type: "warp", mapId: "tower-1", tileX: 10, tileY: 11 },
                ],
              },
              { label: "まだ準備する", commands: [say("渡し守", "いつでも言いな。灯りが消えない限り、船は出せる。")] },
            ],
          },
        ],
        else: [
          {
            type: "if",
            flag: "deep_yugami_defeated",
            equals: true,
            then: [
              say("渡し守", "沖に、いつも嵐雲が見えるだろう。あの下に、大渦がある。常嵐が割れない限り、船は出せないよ。"),
              say("渡し守", "昔から言い伝えがある。大陸のあちこちにある古い灯台に、光をともせば、嵐が道をあける、とな。"),
            ],
            else: [say("渡し守", "沖の嵐雲は、いつもああさ。近づく者はいないよ。")],
          },
        ],
      },
    ],
  };
}

export const WORLD_MAP_NPCS: Record<string, Npc[]> = {
  "world-map": [...WORLD_BEACONS.map((pos, i) => beacon(i + 1, pos)), ferryman()],
};

/**
 * 世界地図と各町を、出入り口でつなぐ。町の地図の南のふち（真ん中から近い、通れる場所）に門を開け、
 * 世界地図の町のアイコンの下に着く。地図・飾りを作ったあとに呼ぶ。
 */
export function connectWorldMap(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  const world = maps["world-map"];
  if (!world) {
    return;
  }
  for (const [townId, pos] of Object.entries(WORLD_TOWNS)) {
    const data = maps[townId];
    if (!data) {
      continue;
    }
    const gate = findSouthGate(data, npcsByMap[townId] ?? []);
    if (!gate) {
      continue;
    }
    const w = data.width;
    // 町の側: 南のふちに門を開ける（下の通れるタイルと同じ地面にする）
    const below = (gate.y - 1) * w + gate.x;
    data.layers[0].data[gate.y * w + gate.x] = data.layers[0].data[below];
    data.collision![gate.y * w + gate.x] = 0;
    data.exits = [...(data.exits ?? []), { tileX: gate.x, tileY: gate.y, targetMapId: "world-map", targetTileX: pos.x, targetTileY: pos.y + 1 }];
    // 世界地図の側: 町のアイコンの上が出入り口
    world.exits = [...(world.exits ?? []), { tileX: pos.x, tileY: pos.y, targetMapId: townId, targetTileX: gate.x, targetTileY: gate.y - 1 }];
  }
}

function findSouthGate(data: TileMapData, npcs: Npc[]): { x: number; y: number } | null {
  const { width: w, height: h } = data;
  const collision = data.collision ?? [];
  const y = h - 1;
  const exitAt = (x: number, yy: number): boolean => (data.exits ?? []).some((e) => e.tileX === x && e.tileY === yy);
  // 出入り口（最初のもの）から歩いて行ける場所だけを候補にする
  const start = data.exits?.[0];
  const reachable = new Set<number>();
  if (start) {
    const stack: Array<[number, number]> = [[start.tileX, start.tileY]];
    reachable.add(start.tileY * w + start.tileX);
    while (stack.length) {
      const [x, yy] = stack.pop()!;
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const nx = x + dx, ny = yy + dy;
        if (nx < 0 || ny < 0 || nx >= w || ny >= h || collision[ny * w + nx] === 1 || reachable.has(ny * w + nx)) continue;
        reachable.add(ny * w + nx);
        stack.push([nx, ny]);
      }
    }
  }
  const order = Array.from({ length: w - 2 }, (_, i) => i + 1).sort((a, b) => Math.abs(a - w / 2) - Math.abs(b - w / 2));
  for (const x of order) {
    const clear = (cx: number, cy: number): boolean => !npcs.some((n) => Math.abs(n.tileX - cx) <= 1 && Math.abs(n.tileY - cy) <= 1);
    if (reachable.has((y - 1) * w + x) && collision[y * w + x] === 1 && !exitAt(x, y) && !exitAt(x, y - 1) && clear(x, y - 1) && clear(x, y - 2)) {
      return { x, y };
    }
  }
  return null;
}
