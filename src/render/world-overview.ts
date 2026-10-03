import type { TileMap } from "../game/map/tile-map";
import { WORLD_BEACONS, WORLD_TOWNS } from "../game/map/world/world-map.generated";
import { BEACON_COLORS } from "../game/world/world-map-world";

let cached: { canvas: HTMLCanvasElement; w: number; h: number } | null = null;

/** 世界地図の全体図（1マス＝1ドット）。地形の色は、地図の `tileColors`。 */
function overviewCanvas(map: TileMap): HTMLCanvasElement | null {
  if (typeof document === "undefined") {
    return null;
  }
  const { width: w, height: h } = map.data;
  if (cached && cached.w === w && cached.h === h) {
    return cached.canvas;
  }
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  const c = canvas.getContext("2d");
  if (!c) {
    return null;
  }
  const ground = map.data.layers[0].data;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      c.fillStyle = map.data.tileColors[ground[y * w + x]] ?? "#000";
      c.fillRect(x, y, 1, 1);
    }
  }
  cached = { canvas, w, h };
  return canvas;
}

/** 世界地図の全体図を、画面いっぱいに出す。町・環灯台（ともっていれば神の色）・いまの位置を重ねる。 */
export function renderWorldOverview(
  ctx: CanvasRenderingContext2D,
  map: TileMap,
  playerTile: { x: number; y: number },
  lit: Set<number>,
  screenWidth: number,
  screenHeight: number,
  nowMs: number,
): void {
  const canvas = overviewCanvas(map);
  ctx.fillStyle = "#0c1020";
  ctx.fillRect(0, 0, screenWidth, screenHeight);
  if (!canvas) {
    return;
  }
  const ox = Math.floor((screenWidth - map.data.width) / 2);
  const oy = Math.floor((screenHeight - map.data.height) / 2) + 6;
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, ox, oy);
  ctx.strokeStyle = "#f2c14e";
  ctx.strokeRect(ox - 1.5, oy - 1.5, map.data.width + 3, map.data.height + 3);
  ctx.font = "8px monospace";
  ctx.textBaseline = "top";
  ctx.textAlign = "center";
  for (const [, t] of Object.entries(WORLD_TOWNS)) {
    ctx.fillStyle = "#e8483c";
    ctx.fillRect(ox + t.x - 1, oy + t.y - 1, 3, 3);
    ctx.fillStyle = "#000";
    ctx.fillText(t.name, ox + t.x + 1, oy + t.y + 3);
    ctx.fillStyle = "#fff";
    ctx.fillText(t.name, ox + t.x, oy + t.y + 2);
  }
  WORLD_BEACONS.forEach((b, i) => {
    ctx.fillStyle = lit.has(i + 1) ? BEACON_COLORS[i] : "#50566a";
    ctx.fillRect(ox + b.x - 1, oy + b.y - 1, 2, 2);
  });
  if (Math.floor(nowMs / 350) % 2 === 0) {
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(ox + playerTile.x - 2, oy + playerTile.y - 2, 5, 5);
    ctx.fillStyle = "#e8483c";
    ctx.fillRect(ox + playerTile.x - 1, oy + playerTile.y - 1, 3, 3);
  }
  ctx.textAlign = "left";
  ctx.fillStyle = "#f2c14e";
  ctx.font = "9px monospace";
  ctx.fillText("世界地図（Vキーか決定でとじる）　赤＝町　点＝環灯台", 8, 3);
}
