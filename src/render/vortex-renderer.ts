import type { TileMap } from "../game/map/tile-map";
import { getTileId } from "../game/map/tile-map";
import { WORLD_TOWER } from "../game/map/world/world-map.generated";
import type { Camera } from "./camera";

/** 世界地図の「渦の輪」（嵐）。芯環塔のまわりを、うずまく流れ（2本の渦のうで）が囲む。航路が開くまで通れない。時刻で回る。 */
const FOAM = "#e8f4ff";
const LIGHT = "#6aa8e0";
const MID = "#2a5ea8";
const DEEP = "#143a78";

export function renderVortex(ctx: CanvasRenderingContext2D, map: TileMap, camera: Camera, nowMs: number): void {
  if (map.data.width < WORLD_TOWER.x + 12) {
    return;
  }
  const s = map.data.tileWidth;
  const startX = Math.max(0, Math.floor(camera.x / s));
  const startY = Math.max(0, Math.floor(camera.y / s));
  const endX = Math.min(map.data.width - 1, Math.floor((camera.x + camera.viewportWidth) / s));
  const endY = Math.min(map.data.height - 1, Math.floor((camera.y + camera.viewportHeight) / s));
  const cx = (WORLD_TOWER.x + 0.5) * s;
  const cy = (WORLD_TOWER.y + 0.5) * s;
  const t = nowMs / 1000;
  for (let ty = startY; ty <= endY; ty++) {
    for (let tx = startX; tx <= endX; tx++) {
      const id = getTileId(map, 0, tx, ty);
      if (id !== 13 && id !== 14) {
        continue;
      }
      const ox = tx * s - camera.x;
      const oy = ty * s - camera.y;
      for (let by = 0; by < s; by += 4) {
        for (let bx = 0; bx < s; bx += 4) {
          const px = tx * s + bx + 2 - cx;
          const py = ty * s + by + 2 - cy;
          const r = Math.hypot(px, py) / s;
          const a = Math.atan2(py, px);
          const v = Math.sin(r * 1.5 - a * 2 - t * 2.4) + Math.sin(r * 0.9 + a * 3 - t * 1.3) * 0.35;
          ctx.fillStyle = v > 1.0 ? FOAM : v > 0.35 ? LIGHT : v > -0.5 ? MID : DEEP;
          ctx.fillRect(ox + bx, oy + by, 4, 4);
        }
      }
    }
  }
}

/** 嵐: 渦の輪のあたりを、暗い雲が覆い、ときどき稲光が走る（航路が開くまで）。 */
export function renderStorm(ctx: CanvasRenderingContext2D, map: TileMap, camera: Camera, nowMs: number): void {
  const s = map.data.tileWidth;
  const cx = (WORLD_TOWER.x + 0.5) * s - camera.x;
  const cy = (WORLD_TOWER.y + 0.5) * s - camera.y;
  if (cx < -260 || cx > camera.viewportWidth + 260 || cy < -260 || cy > camera.viewportHeight + 260) {
    return;
  }
  const g = ctx.createRadialGradient(cx, cy, 20, cx, cy, 230);
  g.addColorStop(0, "rgba(30,34,52,0.12)");
  g.addColorStop(0.55, "rgba(24,28,44,0.38)");
  g.addColorStop(1, "rgba(24,28,44,0)");
  ctx.fillStyle = g;
  ctx.fillRect(cx - 240, cy - 240, 480, 480);
  // ゆっくり流れる雲のかたまり
  for (let i = 0; i < 7; i++) {
    const ang = nowMs / 9000 + i * 0.9;
    const rad = 120 + (i % 3) * 22;
    const x = cx + Math.cos(ang) * rad;
    const y = cy + Math.sin(ang) * rad * 0.7;
    const cg = ctx.createRadialGradient(x, y, 4, x, y, 54);
    cg.addColorStop(0, "rgba(58,62,84,0.55)");
    cg.addColorStop(1, "rgba(58,62,84,0)");
    ctx.fillStyle = cg;
    ctx.fillRect(x - 56, y - 56, 112, 112);
  }
  // 稲光: 約5秒おきに、一瞬だけ白く光る
  const phase = nowMs % 5200;
  if (phase < 110 || (phase > 220 && phase < 300)) {
    ctx.fillStyle = "rgba(230,240,255,0.22)";
    ctx.fillRect(cx - 200, cy - 200, 400, 400);
    ctx.strokeStyle = "rgba(250,250,255,0.9)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    const bx = cx + ((Math.floor(nowMs / 5200) * 37) % 120) - 60;
    ctx.moveTo(bx, cy - 150);
    ctx.lineTo(bx - 8, cy - 100);
    ctx.lineTo(bx + 6, cy - 80);
    ctx.lineTo(bx - 4, cy - 40);
    ctx.stroke();
  }
}
