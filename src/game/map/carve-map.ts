import type { TileMapData } from "./types";

/**
 * 「全部を壁（木・岩）で埋めておいて、通れる広場と道を彫る」やり方で、ダンジョンの地図を手早く作る道具。
 * 広場どうしが重なるようにしておけば、つながっていることが作りながら分かる。
 */
export interface Rect {
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface CarveSpec {
  width: number;
  height: number;
  /** 壁にするタイル（通れない）。 */
  wall: number;
  /** 床にするタイル。 */
  floor: number;
  /** 床の広場（四角）。 */
  rooms: Rect[];
  /** 床の上に引く道（タイルID、点の列を直線でつなぐ。幅1）。 */
  paths?: { tile: number; points: [number, number][] }[];
  /** 個別のタイル（x, y, タイルID, 通れないか）。 */
  tiles?: { x: number; y: number; tile: number; blocked?: boolean }[];
  /** 出入り口にするマス（床・道の扱いで開ける）。 */
  gates?: { x: number; y: number; tile: number }[];
}

export function carveLayers(spec: CarveSpec): { ground: number[]; collision: number[] } {
  const { width, height } = spec;
  const ground: number[] = new Array(width * height).fill(spec.wall);
  const collision: number[] = new Array(width * height).fill(1);
  const open = (x: number, y: number, tile: number, blocked = false): void => {
    if (x < 0 || y < 0 || x >= width || y >= height) return;
    ground[y * width + x] = tile;
    collision[y * width + x] = blocked ? 1 : 0;
  };
  for (const r of spec.rooms) {
    for (let y = r.y; y < r.y + r.h; y++) for (let x = r.x; x < r.x + r.w; x++) open(x, y, spec.floor);
  }
  for (const path of spec.paths ?? []) {
    for (let i = 1; i < path.points.length; i++) {
      const [x0, y0] = path.points[i - 1];
      const [x1, y1] = path.points[i];
      const steps = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0));
      for (let s = 0; s <= steps; s++) {
        open(Math.round(x0 + ((x1 - x0) * s) / (steps || 1)), Math.round(y0 + ((y1 - y0) * s) / (steps || 1)), path.tile);
      }
    }
  }
  for (const t of spec.tiles ?? []) open(t.x, t.y, t.tile, t.blocked);
  for (const g of spec.gates ?? []) open(g.x, g.y, g.tile);
  return { ground, collision };
}

export function carveMap(
  spec: CarveSpec,
  rest: Pick<TileMapData, "tileColors" | "tileArt" | "exits">,
): TileMapData {
  const { ground, collision } = carveLayers(spec);
  return {
    width: spec.width,
    height: spec.height,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    collision,
    ...rest,
  };
}
