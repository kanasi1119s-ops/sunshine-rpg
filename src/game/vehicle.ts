import { WORLD_CHANNEL } from "./map/world/world-map.generated";
import type { TileMapData } from "./map/types";

/**
 * 乗り物（船・飛空艇）。世界地図の地形のID: 1=海 2=平原 3=森 4=山 5=砂漠 6=雪 7=道 8=丘 9=湖・川 10=雲 11=荒れ地 12=雪の森 13=渦の輪 14=渦の切れ目。
 *  - 徒歩: 海・山・湖・渦は通れない。
 *  - 船: 海を進む。陸は、海に接するマス（海岸）にだけ上がれる（上がったら自動で降りる）。山・湖・渦は通れない。
 *  - 飛空艇: 山・海・湖の上も飛べる。渦の輪（嵐）だけは通れない。決定ボタンで、歩ける地形に着陸できる。
 */
export type Vehicle = "foot" | "ship" | "air";

export const OCEAN = 1;
/** 徒歩で歩ける地形。 */
export const WALKABLE_GROUND = new Set([2, 3, 5, 6, 7, 8, 10, 11, 12]);
const STORM = new Set([13, 14]);

export const VEHICLE_SPEED: Record<Vehicle, number> = { foot: 1, ship: 1.6, air: 2.2 };

function groundAt(data: TileMapData, x: number, y: number): number {
  if (x < 0 || y < 0 || x >= data.width || y >= data.height) {
    return 0;
  }
  return data.layers[0].data[y * data.width + x];
}

/** 乗り物ごとの通行判定（1=通れない）。 */
export function buildVehicleCollision(data: TileMapData, kind: "ship" | "air"): number[] {
  const out = new Array<number>(data.width * data.height).fill(1);
  for (let y = 0; y < data.height; y++) {
    for (let x = 0; x < data.width; x++) {
      const g = groundAt(data, x, y);
      let ok = false;
      if (kind === "air") {
        ok = !STORM.has(g);
      } else if (g === OCEAN) {
        ok = true;
      } else if (WALKABLE_GROUND.has(g)) {
        ok = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => groundAt(data, x + dx, y + dy) === OCEAN);
      }
      out[y * data.width + x] = ok ? 0 : 1;
    }
  }
  return out;
}

/** 航路が開いたとき、渦の輪の切れ目（14）を海（1）にする。変えたら true。 */
export function openVortexChannel(data: TileMapData): boolean {
  let changed = false;
  for (const [x, y] of WORLD_CHANNEL) {
    const i = y * data.width + x;
    if (data.layers[0].data[i] !== OCEAN) {
      data.layers[0].data[i] = OCEAN;
      changed = true;
    }
  }
  return changed;
}

/** 着陸できる地形か。 */
export function canLandOn(groundId: number): boolean {
  return WALKABLE_GROUND.has(groundId);
}

export function groundIdAt(data: TileMapData, x: number, y: number): number {
  return groundAt(data, x, y);
}
