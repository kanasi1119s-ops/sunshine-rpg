import type { TileMap } from "../game/map/tile-map";
import { getTileId } from "../game/map/tile-map";
import { WORLD_TOWER } from "../game/map/world/world-map.generated";
import { BASIN_PIT_R, FALLS } from "../game/map/world/world-map";
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

function hash2(x: number, y: number, k: number): number {
  let h = (x * 374761393 + y * 668265263 + k * 2147483647) >>> 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

/**
 * 塔のまわりの陥没と大滝（2026-10-05）。ふち（大滝）のマスでは、海の水が白い筋になって穴のほうへ流れ落ち、
 * 穴のふちからは水しぶきの霧が立ちのぼる。穴は、まんなかへ行くほど深く暗い。地形のすぐあと（建物・人より前）に描く。
 */
export function renderBasin(ctx: CanvasRenderingContext2D, map: TileMap, camera: Camera, nowMs: number): void {
  if (map.data.width < WORLD_TOWER.x + 12) return;
  const s = map.data.tileWidth;
  const cxp = (WORLD_TOWER.x + 0.5) * s;
  const cyp = (WORLD_TOWER.y + 0.5) * s;
  if (Math.abs(cxp - (camera.x + camera.viewportWidth / 2)) > camera.viewportWidth / 2 + 14 * s) return;
  if (Math.abs(cyp - (camera.y + camera.viewportHeight / 2)) > camera.viewportHeight / 2 + 14 * s) return;
  const startX = Math.max(0, Math.floor(camera.x / s));
  const startY = Math.max(0, Math.floor(camera.y / s));
  const endX = Math.min(map.data.width - 1, Math.floor((camera.x + camera.viewportWidth) / s));
  const endY = Math.min(map.data.height - 1, Math.floor((camera.y + camera.viewportHeight) / s));
  const t = nowMs / 1000;
  ctx.save();
  for (let ty = startY; ty <= endY; ty++) {
    for (let tx = startX; tx <= endX; tx++) {
      const id = getTileId(map, 0, tx, ty);
      const ox = tx * s - camera.x;
      const oy = ty * s - camera.y;
      const mx = (tx + 0.5) * s - cxp;
      const my = (ty + 0.5) * s - cyp;
      const d = Math.hypot(mx, my) / s;
      if (id === 16 && d <= BASIN_PIT_R + 0.5) {
        // 穴: まんなかほど深く暗い（4段の暗さ）。ふちの近くは、水しぶきの白い霧がゆらぐ
        const depth = 1 - Math.min(1, d / BASIN_PIT_R);
        ctx.globalAlpha = 1;
        ctx.fillStyle = `rgba(6,8,18,${(0.45 + depth * 0.45).toFixed(2)})`;
        ctx.fillRect(ox, oy, s, s);
        // 穴の中をゆっくり流れる霧の帯（明るさは控えめ）
        const band = Math.sin(((ty * s) + t * 9) / 14 + tx * 0.3);
        if (band > 0.55) {
          ctx.globalAlpha = (band - 0.55) * 0.35;
          ctx.fillStyle = "#b8c8e0";
          ctx.fillRect(ox, oy, s, s);
        }
        if (d > BASIN_PIT_R - 1.6) {
          for (let k = 0; k < 2; k++) {
            const ph = (t * 0.35 + hash2(tx, ty, k)) % 1;
            const px = ox + hash2(tx, ty, k + 7) * s;
            const py = oy + s - ph * s * 1.4;
            ctx.globalAlpha = 0.28 * Math.sin(ph * Math.PI);
            ctx.fillStyle = "#e8f2ff";
            ctx.fillRect(Math.round(px) - 2, Math.round(py) - 1, 5, 3);
            ctx.fillRect(Math.round(px) - 1, Math.round(py) - 2, 3, 5);
          }
        }
      } else if (id === FALLS) {
        // 大滝: 穴のほうへ流れ落ちる白い筋（ふちの外がわから内がわへ動く）
        const ux = -mx / (d * s), uy = -my / (d * s);
        const vx = -uy, vy = ux;
        ctx.globalAlpha = 1;
        ctx.fillStyle = "rgba(120,180,230,0.35)";
        ctx.fillRect(ox, oy, s, s);
        for (let k = 0; k < 5; k++) {
          const ph = (t * 1.3 + hash2(tx, ty, k)) % 1;
          const off = (k - 2) * 3 + (hash2(tx, ty, k + 3) - 0.5) * 2;
          const bx = ox + s / 2 + vx * off - ux * 7 + ux * ph * 14;
          const by = oy + s / 2 + vy * off - uy * 7 + uy * ph * 14;
          ctx.fillStyle = ph > 0.6 ? "#ffffff" : "#d6ecff";
          for (let j = 0; j < 4; j++) ctx.fillRect(Math.round(bx + ux * j), Math.round(by + uy * j), 1, 1);
        }
        // 内がわのふち（落ち口）の白い泡
        ctx.fillStyle = "#f4faff";
        for (let k = 0; k < 3; k++) {
          const w = (hash2(tx, ty, k + 11) - 0.5) * 12;
          const pulse = 0.5 + 0.5 * Math.sin(t * 5 + k + tx);
          ctx.globalAlpha = 0.5 + pulse * 0.4;
          ctx.fillRect(Math.round(ox + s / 2 + ux * 6 + vx * w), Math.round(oy + s / 2 + uy * 6 + vy * w), 2, 2);
        }
      }
    }
  }
  // 2回目: 大滝の水のカーテン（穴の内がわの崖を、白い水が画面の下へ流れ落ちる）と、落ちた先の霧
  for (let ty = startY - 1; ty <= endY; ty++) {
    for (let tx = startX; tx <= endX; tx++) {
      if (getTileId(map, 0, tx, ty) !== FALLS) continue;
      const below = getTileId(map, 0, tx, ty + 1) === 16;
      const diag = getTileId(map, 0, tx - 1, ty + 1) === 16 || getTileId(map, 0, tx + 1, ty + 1) === 16;
      if (!below && !diag) continue;
      const ox = tx * s - camera.x;
      const top = (ty + 1) * s - camera.y - 3;
      const len = (below ? 44 : 26) + Math.round(hash2(tx, ty, 21) * 12);
      for (let col = 0; col < s; col++) {
        const shade = (col + tx * 3) % 5;
        const base = shade === 0 ? "#ffffff" : shade === 1 || shade === 3 ? "#cfe8fb" : shade === 2 ? "#8cc2ec" : "#5e9ad4";
        const speed = 70 + (shade * 13) % 40;
        const off = (nowMs / 1000 * speed + hash2(tx, col, 5) * 40) % 10;
        for (let y = 0; y < len; y++) {
          const fade = 1 - y / len;
          // 流れのすじ（下へ動く切れ目）
          const gap = (y + 10 - off) % 10 < 1.4;
          if (gap && shade !== 0) continue;
          ctx.globalAlpha = Math.min(1, 0.35 + fade * 0.75);
          ctx.fillStyle = base;
          ctx.fillRect(ox + col, top + y, 1, 1);
        }
      }
      // 落ち口のふくらみ（白い泡の線）
      ctx.globalAlpha = 1;
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(ox, top - 1, s, 2);
      // 滝つぼの霧（ふくらんでは消える）
      for (let k = 0; k < 3; k++) {
        const ph = (t * 0.6 + hash2(tx, ty, k + 30)) % 1;
        const r = 3 + ph * 7;
        ctx.globalAlpha = 0.35 * (1 - ph);
        ctx.fillStyle = "#eef6ff";
        ctx.beginPath();
        ctx.arc(ox + s / 2 + (hash2(tx, ty, k + 40) - 0.5) * 14, top + len - 2 - ph * 6, r, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }
  ctx.restore();
}

/** 嵐: 塔のまわりを、暗い雲が覆い、雨が降り、ときどき稲光が走る（2026-10-05から、航路が開いたあとも、いつも嵐）。 */
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
  // 雨: ななめに降る細い線（嵐のまんなかほど多い）
  ctx.save();
  ctx.strokeStyle = "rgba(200,215,240,0.45)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  for (let i = 0; i < 90; i++) {
    const seedX = hash2(i, 3, 1), seedY = hash2(i, 5, 2);
    const fall = ((nowMs / 420 + seedY) % 1);
    const x = cx - 230 + seedX * 460 + fall * 18;
    const y = cy - 230 + ((seedY * 460 + fall * 460) % 460);
    if (Math.hypot(x - cx, y - cy) > 225) continue;
    ctx.moveTo(Math.round(x), Math.round(y));
    ctx.lineTo(Math.round(x - 3), Math.round(y + 7));
  }
  ctx.stroke();
  ctx.restore();
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
