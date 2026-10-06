import { PROP_BOX } from "../map/town-tidy";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import type { MapProp, TileMapData } from "../map/types";
import { INN_PRICES, INN_SPOTS } from "../map/town-decor";
import { doorOffsetX, propFootprintTiles, propOverhangTiles } from "../map/map-props";
import { DUNGEON_PARENT } from "./dungeon-parent";

/**
 * 宿屋の建物の中（2026-10-05、人間の依頼）。町の2階建ての屋敷が宿屋で、中は2階建て。広さは、ふつうの家（11×8）の8倍ほど（1階・2階とも30×12）。
 *  - 1階: 受付カウンター（カウンターの奥に店員。カウンターの前で話しかけると「とまる」を選べる）、ベッドが6つ並んだ大部屋、階段のホール。
 *  - 2階: 2つの部屋（それぞれベッドが2つ）。部屋にはテーブルと棚がある。
 */
const FLOOR = 1;
const WALL = 2;
const STAIR = 3;
export const INN_W = 30;
export const INN_H = 12;

interface Floor {
  ground: number[];
  collision: number[];
  props: MapProp[];
  npcs: Npc[];
}

function newFloor(): Floor {
  const ground = new Array<number>(INN_W * INN_H).fill(FLOOR);
  const collision = new Array<number>(INN_W * INN_H).fill(0);
  const wall = (x: number, y: number): void => {
    ground[y * INN_W + x] = WALL;
    collision[y * INN_W + x] = 1;
  };
  for (let x = 0; x < INN_W; x++) { wall(x, 0); wall(x, 1); wall(x, INN_H - 1); }   // 奥の壁は2段（家具を壁にぴったりつけるため）
  for (let y = 0; y < INN_H; y++) { wall(0, y); wall(INN_W - 1, y); }
  return { ground, collision, props: [], npcs: [] };
}

const wallAt = (f: Floor, x: number, y: number): void => {
  f.ground[y * INN_W + x] = WALL;
  f.collision[y * INN_W + x] = 1;
};
const blockAt = (f: Floor, x: number, y: number): void => {
  f.collision[y * INN_W + x] = 1;
};

const BED_LINES = ["ふかふかのベッドだ。シーツが、きれいにのばしてある。", "お日さまのにおいがする、清潔なベッドだ。", "まくらもとに、小さなランプがある。", "ぐっすり眠れそうなベッドだ。"];
const SHELF_LINES = ["棚には、旅の地図と、この町の案内がならんでいる。", "棚には、宿帳と、ぬいぐるみの熊が置いてある。", "棚には、毛布がきれいにたたんで積んである。"];
const TABLE_LINES = ["テーブルの上に、水さしとコップが置いてある。", "テーブルの上に、読みかけの旅の手紙がある。", "テーブルの上に、ろうそくと、くだものを入れたかごがある。"];

type FurnitureKind = "bed" | "shelf" | "table";

function addFurniture(f: Floor, idBase: string, kind: FurnitureKind, x: number, y: number, n: number, text: string): void {
  f.npcs.push({
    id: `${idBase}-${kind}-${n}`,
    tileX: x,
    tileY: y,
    color: kind === "bed" ? ["#6a8ab0", "#b07090", "#7a9a6a", "#c0a050"][n % 4] : kind === "shelf" ? "#7a5228" : "#d8cbb0",
    commands: [{ type: "message", text }],
  });
  // 横にはばのある家具は、となりのマスも通れなくする
  for (const dx of [-1, 1]) blockAt(f, x + dx, y);
}

function mapOf(f: Floor, exits: TileMapData["exits"]): TileMapData {
  return {
    width: INN_W,
    height: INN_H,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: f.ground }],
    tileColors: { [FLOOR]: "#9a7a4a", [WALL]: "#6a5a4a", [STAIR]: "#6a4a28" },
    tileArt: { [FLOOR]: "tint:plank", [WALL]: "tint:brick", [STAIR]: "tint:plank" },
    theme: "interior",
    collision: f.collision,
    props: f.props,
    exits,
  };
}

/** 宿屋の主人（受付の店員）のせりふ。町にもとからいる宿屋の主人（物語のせりふつき）がいれば、それを使う。 */
function clerkCommands(existing: Npc | undefined, price: number): EventCommand[] {
  const inn: EventCommand = { type: "inn", price };
  const base = existing ? existing.commands.filter((c) => c.type !== "inn") : [{ type: "message", text: "いらっしゃいませ。ようこそ、宿屋へ。", speaker: "宿屋の主人" } as EventCommand];
  return [...base, inn];
}

export function addInnInteriors(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  for (const [town, spot] of INN_SPOTS) {
    const data = maps[town];
    if (!data?.collision) continue;
    const w = data.width, h = data.height;
    const exits = data.exits ?? (data.exits = []);
    const list = npcsByMap[town] ?? (npcsByMap[town] = []);
    const door = { x: spot.x + doorOffsetX(spot.kind), y: spot.y + 1 };
    const walkable = (x: number, y: number): boolean => x >= 0 && y >= 0 && x < w && y < h && data.collision![y * w + x] === 0;
    const exitAt = (x: number, y: number): boolean => exits.some((e) => e.tileX === x && e.tileY === y);
    const free = (x: number, y: number): boolean => walkable(x, y) && !exitAt(x, y) && !list.some((p) => p.tileX === x && p.tileY === y);
    if (!walkable(door.x, door.y) || exitAt(door.x, door.y)) continue;
    const ret = [[0, 1], [-1, 1], [1, 1], [0, 2], [-1, 0], [1, 0], [-2, 1], [2, 1]].map(([dx, dy]) => ({ x: door.x + dx, y: door.y + dy })).find((c) => free(c.x, c.y));
    if (!ret) continue;

    const id1 = `inn-${town}-1f`;
    const id2 = `inn-${town}-2f`;
    const price = INN_PRICES[town] ?? 20;
    // 町にもとからいる宿屋の主人は、建物の中の受付に移す
    const oldIdx = list.findIndex((n) => /-innkeeper$/.test(n.id));
    const old = oldIdx >= 0 ? list[oldIdx] : undefined;
    if (oldIdx >= 0) list.splice(oldIdx, 1);
    const talk = clerkCommands(old, price);

    // ── 1階 ──
    const f1 = newFloor();
    for (let x = 0; x <= 23; x++) if (x !== 7) wallAt(f1, x, 6);       // 大部屋と受付の間の壁（x=7 が出入り口）
    for (let y = 2; y <= 6; y++) wallAt(f1, 23, y);                     // 大部屋と階段ホールの間の壁
    // 大部屋: ベッド6つ・棚・テーブル
    [5, 8, 11, 14, 17, 20].forEach((x, i) => addFurniture(f1, id1, "bed", x, 2, i, i === 0 ? "六つ並んだベッドのひとつだ。大部屋で、みんな一緒に泊まれる。" : BED_LINES[i % BED_LINES.length]));
    addFurniture(f1, id1, "shelf", 2, 2, 0, SHELF_LINES[0]);
    addFurniture(f1, id1, "table", 11, 4, 0, TABLE_LINES[0]);
    f1.npcs.push({ id: `${id1}-guest`, tileX: 16, tileY: 4, color: "#a0a070", commands: [{ type: "message", text: "旅の途中でね。大部屋は安いし、いろんな人と話せるから好きなんだ。", speaker: "旅の人" }] });
    // 階段ホール
    addFurniture(f1, id1, "shelf", 26, 2, 1, SHELF_LINES[1]);
    f1.props.push({ kind: "flowerbed", tileX: 25, tileY: 5 });
    // 受付: カウンター（前から話しかけられる）・奥の店員
    for (let x = 12; x <= 17; x++) {
      f1.npcs.push({ id: `${id1}-counter-${x}`, tileX: x, tileY: 8, color: "#8a5a2c", commands: talk });
    }
    f1.npcs.push({ id: `${id1}-clerk`, tileX: 14, tileY: 7, color: "#b08a5a", commands: talk });
    f1.props.push({ kind: "barrel", tileX: 11, tileY: 7 }, { kind: "barrel", tileX: 18, tileY: 7 });
    blockAt(f1, 11, 7);
    blockAt(f1, 18, 7);
    f1.props.push({ kind: "flowerbed", tileX: 2, tileY: 10 }, { kind: "flowerbed", tileX: 27, tileY: 10 });
    // 出入り口（玄関）と階段
    f1.ground[(INN_H - 1) * INN_W + 14] = FLOOR;
    f1.collision[(INN_H - 1) * INN_W + 14] = 0;
    f1.ground[3 * INN_W + 28] = STAIR;

    // ── 2階 ──
    const f2 = newFloor();
    for (let x = 0; x < INN_W; x++) if (x !== 7 && x !== 21) wallAt(f2, x, 6);   // 部屋と廊下の間の壁（x=7・x=21 が出入り口）
    for (let y = 2; y <= 6; y++) wallAt(f2, 14, y);                               // 2つの部屋の間の壁
    // 部屋A
    [3, 6].forEach((x, i) => addFurniture(f2, id2, "bed", x, 2, i, BED_LINES[i]));
    addFurniture(f2, id2, "shelf", 11, 2, 0, SHELF_LINES[2]);
    addFurniture(f2, id2, "table", 9, 4, 0, TABLE_LINES[1]);
    // 部屋B
    [17, 20].forEach((x, i) => addFurniture(f2, id2, "bed", x, 2, i + 2, BED_LINES[i + 2]));
    addFurniture(f2, id2, "shelf", 26, 2, 1, SHELF_LINES[1]);
    addFurniture(f2, id2, "table", 23, 4, 1, TABLE_LINES[2]);
    f2.npcs.push({ id: `${id2}-guest`, tileX: 18, tileY: 4, color: "#b07090", commands: [{ type: "message", text: "……ふあ。長い旅で、へとへとなの。この部屋の窓から見える夕日が、とてもきれいでね。", speaker: "疲れた旅人" }] });
    f2.ground[9 * INN_W + 28] = STAIR;

    maps[id1] = mapOf(f1, [
      { tileX: 14, tileY: INN_H - 1, targetMapId: town, targetTileX: ret.x, targetTileY: ret.y },
      { tileX: 28, tileY: 3, targetMapId: id2, targetTileX: 27, targetTileY: 9 },
    ]);
    maps[id2] = mapOf(f2, [{ tileX: 28, tileY: 9, targetMapId: id1, targetTileX: 27, targetTileY: 3 }]);
    npcsByMap[id1] = f1.npcs;
    npcsByMap[id2] = f2.npcs;
    DUNGEON_PARENT[id1] = town;
    DUNGEON_PARENT[id2] = town;
    // 玄関のよこに、宿屋の木の看板（ほかの飾りの絵がはみ出すマスの奥には置かない）
    const covered = new Set<number>();
    for (const prop of data.props ?? []) {
      const tiles = propFootprintTiles(prop);
      if (!tiles.length) continue;
      const top = Math.min(...tiles.map((t) => t.y)) - propOverhangTiles(prop.kind, data.tileHeight);
      // 絵が横のマスへはみ出す飾り（木・井戸など。PROP_BOX ではかった幅）は、となりのマスもふさぐ
      const box = PROP_BOX[prop.kind];
      const pad = prop.kind === "tree" || (box && (box[0] < -(data.tileWidth / 2 + 2) || box[1] > data.tileWidth / 2 + 2)) ? 1 : 0;
      const x0 = Math.min(...tiles.map((t) => t.x)) - pad, x1 = Math.max(...tiles.map((t) => t.x)) + pad;
      for (let yy = top; yy <= prop.tileY; yy++) for (let xx = x0; xx <= x1; xx++) covered.add(yy * w + xx);
    }
    // ほかの地図から来たときに立つ場所（到着地点）にも置かない
    const arrivals = new Set<number>();
    for (const m of Object.values(maps)) for (const e of m.exits ?? []) if (e.targetMapId === town) arrivals.add(e.targetTileY * w + e.targetTileX);
    const signSpot = [[3, 1], [-3, 1], [2, 1], [-2, 1]].map(([dx, dy]) => ({ x: door.x + dx, y: door.y + dy })).find((c) => free(c.x, c.y) && !covered.has(c.y * w + c.x) && !arrivals.has(c.y * w + c.x) && (c.x !== ret.x || c.y !== ret.y));
    if (signSpot) {
      list.push({ id: `${town}-inn-sign`, tileX: signSpot.x, tileY: signSpot.y, color: "#a0723c", commands: [{ type: "message", text: "「宿屋　旅の人、ようこそ。一晩ごとに、とまれます」と書いてある。" }] });
    }
    exits.push({ tileX: door.x, tileY: door.y, targetMapId: id1, targetTileX: 14, targetTileY: INN_H - 2, enter: "up" });
  }
}
