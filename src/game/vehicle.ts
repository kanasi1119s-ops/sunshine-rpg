import type { TileMapData } from "./map/types";
import { WORLD_TOWNS } from "./map/world/world-map.generated";
import { TOWER_CLOUD_TILES } from "./map/world/tower-cloud.generated";
import { WORLD_TOWER } from "./map/world/world-map.generated";

/**
 * 乗り物（船・飛空艇）。世界地図の地形のID: 1=海 2=平原 3=森 4=山 5=砂漠 6=雪 7=道 8=丘 9=湖・川 10=雲 11=荒れ地 12=雪の森 13=渦の輪 14=渦の切れ目。
 *  - 徒歩: 海・山・湖・渦は通れない。
 *  - 船: 海を進む。陸は、海に接するマス（海岸）にだけ上がれる（上がったら自動で降りる。雲の上には上がれない）。山・湖・渦は通れない。
 *  - 飛空艇: 山・海・湖の上も飛べる。芯環塔のまわりの大滝（19）の上は、嵐で通れない。決定ボタンで、歩ける地形に着陸できる。
 *  （渦の輪 13・14 は、2026-10-05 になくした。世界地図を作るときに海になる）
 *  - 芯環塔の上の積乱雲の下の海（TOWER_CLOUD_TILES）は、船は進める（雲は船より上に描くので、雲のうしろを通って見える）。
 *    飛空艇は、嵐の雲の中へは入れない（2026-10-05）。
 */
export type Vehicle = "foot" | "ship" | "air";

export const OCEAN = 1;
/** 雲（空の町のまわりの空の島）。 */
const CLOUD = 10;
/** 徒歩で歩ける地形。 */
export const WALKABLE_GROUND = new Set([2, 3, 5, 6, 7, 8, 10, 11, 12]);
/** 飛空艇も通れない地形: 渦の輪（いまは地図にない）と、芯環塔のまわりの大滝（嵐）。 */
const STORM = new Set([13, 14, 19]);

export const VEHICLE_SPEED: Record<Vehicle, number> = { foot: 1, ship: 1.6, air: 2.2 };

function groundAt(data: TileMapData, x: number, y: number): number {
  if (data.wrap) {
    x = ((x % data.width) + data.width) % data.width;
    y = ((y % data.height) + data.height) % data.height;
  }
  if (x < 0 || y < 0 || x >= data.width || y >= data.height) {
    return 0;
  }
  return data.layers[0].data[y * data.width + x];
}

const islandCache = new WeakMap<TileMapData, Set<number>>();

/**
 * 空の町のまわりの「空の島」のマス（町のすぐ下から、歩いて行けるマス。雲と、はしの雪の地面）。
 * ここには、船で上がれず、飛空艇も着陸できない（町の中に飛空艇をとめて入る）。世界地図でなければ、空。
 */
export function skyIslandTiles(data: TileMapData): Set<number> {
  const cached = islandCache.get(data);
  if (cached) return cached;
  const out = new Set<number>();
  const pos = WORLD_TOWNS[SKY_TOWN];
  const col = data.collision;
  if (pos && col && data.width > pos.x && data.height > pos.y + 1) {
    const w = data.width, h = data.height;
    const start = (pos.y + 1) * w + pos.x;
    if (col[start] === 0) {
      out.add(start);
      const q = [start];
      for (let i = 0; i < q.length; i++) {
        const x = q[i] % w, y = Math.floor(q[i] / w);
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          const nx = (x + dx + w) % w, ny = (y + dy + h) % h, ni = ny * w + nx;
          if (!out.has(ni) && col[ni] === 0) {
            out.add(ni);
            q.push(ni);
          }
        }
      }
    }
  }
  islandCache.set(data, out);
  return out;
}

/** 乗り物ごとの通行判定（1=通れない）。 */
export function buildVehicleCollision(data: TileMapData, kind: "ship" | "air"): number[] {
  const out = new Array<number>(data.width * data.height).fill(1);
  const island = kind === "ship" ? skyIslandTiles(data) : new Set<number>();
  for (let y = 0; y < data.height; y++) {
    for (let x = 0; x < data.width; x++) {
      const g = groundAt(data, x, y);
      let ok = false;
      if (kind === "air") {
        ok = !STORM.has(g);
      } else if (g === OCEAN) {
        ok = true;
      } else if (WALKABLE_GROUND.has(g) && g !== CLOUD && !island.has(y * data.width + x)) {
        // 海岸に上がれる（雲の上には上がれない。空の町は、飛空艇でしか行けない）
        ok = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => groundAt(data, x + dx, y + dy) === OCEAN);
      }
      out[y * data.width + x] = ok ? 0 : 1;
    }
  }
  // 芯環塔の上の積乱雲の下（世界地図だけ）: 飛空艇だけ入れない
  if (kind === "air" && data.width >= WORLD_TOWER.x + 12 && data.height >= WORLD_TOWER.y + 12) {
    for (const [dx, dy] of TOWER_CLOUD_TILES) {
      const x = WORLD_TOWER.x + dx, y = WORLD_TOWER.y + dy;
      if (x >= 0 && y >= 0 && x < data.width && y < data.height) out[y * data.width + x] = 1;
    }
  }
  return out;
}


/**
 * 空に浮かぶ町（浮嶼）。飛空艇でしか入れない（2026-10-06、人間の指示「空を飛んでる町ですが、飛行船でしか入れないように。
 * 飛行船は町の中に止めれるように」）。飛空艇で町の上に来て決定ボタンを押すと、町の中に飛空艇をとめて降りる。
 * 町の中の飛空艇に話しかけると、乗って飛び立つ。雲の上（町のまわりの空の島）には、着陸できない。
 */
export const SKY_TOWN = "fushima-town";
/** 町の中の、飛空艇をとめる所（絵の足もと）と、降りて立つ所。 */
export const SKY_TOWN_DOCK = { tileX: 30, tileY: 7 };
export const SKY_TOWN_ARRIVAL = { tileX: 30, tileY: 9 };
/** 飛空艇が空の町にとまっているあいだ立つフラグ。 */
export const AIRSHIP_DOCKED_FLAG = "airship_docked_sky";

/** 着陸できる地形か（雲の上には着陸できない）。 */
export function canLandOn(groundId: number): boolean {
  return WALKABLE_GROUND.has(groundId) && groundId !== CLOUD;
}

export function groundIdAt(data: TileMapData, x: number, y: number): number {
  return groundAt(data, x, y);
}
