import { hashCell } from "../color-utils";
import type { Npc } from "../npc";
import type { TileMapData } from "./types";

/**
 * 同じ形のダンジョンを使いまわさない（2026-10-04、人間の依頼）。
 * もとの手づくりの部屋（神の祠・小島・塔・坑道など）は、同じ型を何度も使っていた。そこで、地図ごとに決まった乱数（地図のIDから）で、
 * 床のところどころに「柱・岩のかたまり」（1×1〜2×2、まわりは床）を置いて、形をかえる。
 * 柱は、まわりをぐるっと床にかこまれた場所にだけ置くので、通路をふさがない。出入り口・人のいる所・そのまわりにも置かない。
 */
const DUNGEON_ID = /^(deep|tower|kanou)-\d+$|^god-shrine-\d+$|^islet-\d+-\d+$|^shimohara-facility$/;

function seedOf(id: string): number {
  let h = 2166136261;
  for (let i = 0; i < id.length; i++) h = Math.imul(h ^ id.charCodeAt(i), 16777619) >>> 0;
  return h;
}

export function applyVariantWalls(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  for (const [mapId, data] of Object.entries(maps)) {
    if (!DUNGEON_ID.test(mapId) || !data.collision) continue;
    const w = data.width;
    const h = data.height;
    const ground = data.layers[0].data;
    const collision = data.collision;
    const npcs = npcsByMap[mapId] ?? [];
    const exits = data.exits ?? [];
    // 壁のタイル（通れない地面でいちばん多いもの）と、床のタイル
    const wallCount = new Map<number, number>();
    const floorCount = new Map<number, number>();
    for (let i = 0; i < ground.length; i++) {
      const m = collision[i] ? wallCount : floorCount;
      m.set(ground[i], (m.get(ground[i]) ?? 0) + 1);
    }
    const top = (m: Map<number, number>): number | undefined => [...m.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
    const wallId = top(wallCount);
    if (wallId === undefined) continue;
    const seed = seedOf(mapId);
    const free = (x: number, y: number): boolean => x > 0 && y > 0 && x < w - 1 && y < h - 1 && collision[y * w + x] === 0;
    const protectedNear = (x: number, y: number): boolean =>
      npcs.some((n) => Math.abs(n.tileX - x) <= 2 && Math.abs(n.tileY - y) <= 2) || exits.some((e) => Math.abs(e.tileX - x) <= 2 && Math.abs(e.tileY - y) <= 2);
    const cells: Array<[number, number]> = [];
    for (let y = 2; y < h - 2; y++) for (let x = 2; x < w - 2; x++) cells.push([x, y]);
    cells.sort((a, b) => hashCell(a[0] * 31 + (seed % 9973), a[1] * 17 + (seed % 7919)) - hashCell(b[0] * 31 + (seed % 9973), b[1] * 17 + (seed % 7919)));
    const open = cells.filter(([x, y]) => free(x, y)).length;
    const want = Math.max(4, Math.round(open / 16));
    let placed = 0;
    for (const [x, y] of cells) {
      if (placed >= want) break;
      const bw = 1 + (hashCell(x + seed, y) % 2);
      const bh = 1 + (hashCell(x, y + seed) % 2);
      let ok = true;
      // 置く範囲と、そのまわり1マスが、すべて床
      for (let dy = -1; dy <= bh && ok; dy++) {
        for (let dx = -1; dx <= bw; dx++) {
          if (!free(x + dx, y + dy) || protectedNear(x + dx, y + dy)) {
            ok = false;
            break;
          }
        }
      }
      if (!ok) continue;
      for (let dy = 0; dy < bh; dy++) {
        for (let dx = 0; dx < bw; dx++) {
          collision[(y + dy) * w + (x + dx)] = 1;
          ground[(y + dy) * w + (x + dx)] = wallId;
        }
      }
      placed++;
    }
  }
}
