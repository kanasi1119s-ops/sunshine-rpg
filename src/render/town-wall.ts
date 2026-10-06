import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import type { TileMap } from "../game/map/tile-map";
import type { Camera } from "./camera";

/**
 * 町を囲む石の塀（2026-10-06、人間の指示「町は基本立体的な塀で囲むようにしてください」）。
 * 地図のいちばん外の1マスに、上と下のはしは「横の塀」（笠石と積んだ石の面）、左右のはしは「たての塀」（上から見た笠石）、
 * 四すみと門（出入り口）の両わきには、一段高い柱を立てる。出入り口のマスは、あけたまま（門）。
 * 絵は `assets-src/pixel-practice/r20-props/townwall.py`（エディタで確かめたもの）。地形のすぐあと、飾り・人より前に描く。
 */
export function renderTownWall(ctx: CanvasRenderingContext2D, map: TileMap, camera: Camera): void {
  const d = map.data;
  if (!d.townWall) return;
  const ts = d.tileWidth;
  const w = d.width, h = d.height;
  const isExit = (x: number, y: number): boolean => !!d.exits?.some((e) => e.tileX === x && e.tileY === y);
  const art = (k: string): HTMLCanvasElement | null => getSpriteCanvas(`prop:${k}`, SPRITE_DATA);
  const hA = art("townwall-h"), hB = art("townwall-h2"), vA = art("townwall-v"), vB = art("townwall-v2"), post = art("townwall-post");
  if (!hA || !hB || !vA || !vB || !post) return;
  const x0 = Math.max(0, Math.floor(camera.x / ts) - 1), x1 = Math.min(w - 1, Math.ceil((camera.x + camera.viewportWidth) / ts) + 1);
  const y0 = Math.max(0, Math.floor(camera.y / ts) - 1), y1 = Math.min(h - 1, Math.ceil((camera.y + camera.viewportHeight) / ts) + 1);
  const at = (img: HTMLCanvasElement, x: number, y: number): void => {
    // 絵は足もとのマスの下にそろえる（柱は上へはみ出す）。絵のまわりのあき（正方形にそろえた余白）は、下・まんなかでそろえる
    ctx.drawImage(img, Math.round(x * ts + ts / 2 - img.width / 2 - camera.x), Math.round(y * ts + ts - img.height - camera.y));
  };
  ctx.imageSmoothingEnabled = false;
  const posts: Array<[number, number]> = [];
  const ring = (x: number, y: number): boolean => x === 0 || y === 0 || x === w - 1 || y === h - 1;
  for (let y = y0; y <= y1; y++) {
    for (let x = x0; x <= x1; x++) {
      if (!ring(x, y) || isExit(x, y)) continue;
      const corner = (x === 0 || x === w - 1) && (y === 0 || y === h - 1);
      const gateSide = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => ring(x + dx, y + dy) && isExit(x + dx, y + dy));
      if (corner || gateSide) {
        posts.push([x, y]);
        continue;
      }
      if (y === 0 || y === h - 1) at((x + y) % 2 === 0 ? hA : hB, x, y);
      else at(y % 2 === 0 ? vA : vB, x, y);
    }
  }
  for (const [x, y] of posts) at(post, x, y);
}
