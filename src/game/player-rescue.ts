import { isWalkable, type TileMap } from "./map/tile-map";

/**
 * セーブした場所が、あとから置かれた飾りなどでふさがっていたとき（立っているマスが通れない・まわりを囲まれて動けない）に、
 * いちばん近い、ほかの広い場所につながるマスへ、プレイヤーを移す。動けなくなって固まるのを防ぐ。
 */
const MIN_AREA = 12;

function reachableCount(map: TileMap, sx: number, sy: number, limit: number): number {
  const w = map.data.width, h = map.data.height;
  const seen = new Set<number>([sy * w + sx]);
  const queue: [number, number][] = [[sx, sy]];
  while (queue.length > 0 && seen.size < limit) {
    const [x, y] = queue.shift()!;
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = x + dx, ny = y + dy;
      if (nx < 0 || ny < 0 || nx >= w || ny >= h || seen.has(ny * w + nx) || !isWalkable(map, nx, ny)) continue;
      seen.add(ny * w + nx);
      queue.push([nx, ny]);
    }
  }
  return seen.size;
}

/** その場所から、歩いて動ける広さがあるか。 */
export function isOpenSpot(map: TileMap, tx: number, ty: number): boolean {
  return isWalkable(map, tx, ty) && reachableCount(map, tx, ty, MIN_AREA) >= MIN_AREA;
}

/** 動けないマスにいるなら、いちばん近い動けるマスを返す。いまの場所で動けるなら null。 */
export function rescueTile(map: TileMap, tx: number, ty: number): { x: number; y: number } | null {
  if (isOpenSpot(map, tx, ty)) return null;
  const maxR = Math.max(map.data.width, map.data.height);
  for (let r = 1; r <= maxR; r++) {
    for (let dy = -r; dy <= r; dy++) {
      for (let dx = -r; dx <= r; dx++) {
        if (Math.max(Math.abs(dx), Math.abs(dy)) !== r) continue;
        const x = tx + dx, y = ty + dy;
        if (x < 0 || y < 0 || x >= map.data.width || y >= map.data.height) continue;
        if (isOpenSpot(map, x, y)) return { x, y };
      }
    }
  }
  return null;
}
