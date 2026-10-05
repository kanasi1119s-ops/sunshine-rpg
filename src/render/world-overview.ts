import type { TileMap } from "../game/map/tile-map";
import { WORLD_BEACONS, WORLD_TOWNS } from "../game/map/world/world-map.generated";
import { BEACON_COLORS } from "../game/world/world-map-world";
import { WORLD_OVERVIEW } from "../game/map/world/world-overview.generated";
import { decodeSprite } from "../game/art/sprite";

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
  // 全体フィールドの見本の絵をトレースした全体図（地図と同じ大きさのとき）。なければ地形の色で描く。
  if (WORLD_OVERVIEW.width === w && WORLD_OVERVIEW.height === h) {
    const size = Math.max(w, h);
    const cells = decodeSprite({ size, palette: WORLD_OVERVIEW.palette, rle: WORLD_OVERVIEW.rle });
    const img = c.createImageData(w, h);
    for (let n = 0; n < w * h; n++) {
      const v = parseInt(WORLD_OVERVIEW.palette[cells[n]]?.slice(1) ?? "000000", 16);
      img.data[n * 4] = (v >> 16) & 255;
      img.data[n * 4 + 1] = (v >> 8) & 255;
      img.data[n * 4 + 2] = v & 255;
      img.data[n * 4 + 3] = 255;
    }
    c.putImageData(img, 0, 0);
    cached = { canvas, w, h };
    return canvas;
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
  // 画面に収まる大きさに縮めて描く（上の見出し14ドットぶんをあける）。収まるなら等倍。
  const k = Math.min(1, (screenWidth - 8) / map.data.width, (screenHeight - 18) / map.data.height);
  const dw = Math.floor(map.data.width * k);
  const dh = Math.floor(map.data.height * k);
  const ox = Math.floor((screenWidth - dw) / 2);
  const oy = 14 + Math.floor((screenHeight - 14 - dh) / 2);
  ctx.imageSmoothingEnabled = k < 1;
  ctx.drawImage(canvas, ox, oy, dw, dh);
  ctx.strokeStyle = "#f2c14e";
  ctx.strokeRect(ox - 1.5, oy - 1.5, dw + 3, dh + 3);
  ctx.font = "8px monospace";
  ctx.textBaseline = "top";
  ctx.textAlign = "center";
  for (const [, t] of Object.entries(WORLD_TOWNS)) {
    ctx.fillStyle = "#e8483c";
    const tx = ox + Math.round(t.x * k);
    const ty = oy + Math.round(t.y * k);
    ctx.fillRect(tx - 1, ty - 1, 3, 3);
    ctx.fillStyle = "#000";
    ctx.fillText(t.name, tx + 1, ty + 3);
    ctx.fillStyle = "#fff";
    ctx.fillText(t.name, tx, ty + 2);
  }
  WORLD_BEACONS.forEach((b, i) => {
    ctx.fillStyle = lit.has(i + 1) ? BEACON_COLORS[i] : "#50566a";
    ctx.fillRect(ox + Math.round(b.x * k) - 1, oy + Math.round(b.y * k) - 1, 2, 2);
  });
  if (Math.floor(nowMs / 350) % 2 === 0) {
    ctx.fillStyle = "#ffffff";
    const px = ox + Math.round(playerTile.x * k);
    const py = oy + Math.round(playerTile.y * k);
    ctx.fillRect(px - 2, py - 2, 5, 5);
    ctx.fillStyle = "#e8483c";
    ctx.fillRect(px - 1, py - 1, 3, 3);
  }
  ctx.textAlign = "left";
  ctx.fillStyle = "#f2c14e";
  ctx.font = "9px monospace";
  ctx.fillText("世界地図（Vキー・地図ボタン・決定でとじる）　赤＝町　点＝環灯台", 8, 3);
}
