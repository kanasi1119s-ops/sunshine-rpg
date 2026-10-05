import type { TileMap } from "../game/map/tile-map";

const cache = new Map<string, HTMLCanvasElement>();

/** 色（#rrggbb）を、割合 k だけ暗くする。 */
function darken(hex: string, k: number): string {
  const v = parseInt(hex.slice(1), 16);
  const f = (n: number): number => Math.round(n * (1 - k));
  return `rgb(${f((v >> 16) & 255)}, ${f((v >> 8) & 255)}, ${f(v & 255)})`;
}

/** その地図ぜんたいを、1マス＝1ドットで描いた絵（通れないマスは暗く）。 */
function areaCanvas(map: TileMap, key: string): HTMLCanvasElement | null {
  if (typeof document === "undefined") return null;
  const cached = cache.get(key);
  if (cached) return cached;
  const { width: w, height: h } = map.data;
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  const c = canvas.getContext("2d");
  if (!c) return null;
  const ground = map.data.layers[0].data;
  const collision = map.data.collision;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const base = map.data.tileColors[ground[y * w + x]] ?? "#202030";
      const blocked = collision ? collision[y * w + x] === 1 : false;
      c.fillStyle = base.startsWith("#") ? (blocked ? darken(base, 0.45) : base) : base;
      c.fillRect(x, y, 1, 1);
    }
  }
  cache.set(key, canvas);
  return canvas;
}

/** 町・ダンジョンなどの、いまの地図ぜんたい（出入り口と、いまの位置つき）。世界地図の全体図とは別。 */
export function renderAreaMap(
  ctx: CanvasRenderingContext2D,
  map: TileMap,
  mapKey: string,
  title: string,
  playerTile: { x: number; y: number },
  screenWidth: number,
  screenHeight: number,
  nowMs: number,
): void {
  ctx.fillStyle = "#0c1020";
  ctx.fillRect(0, 0, screenWidth, screenHeight);
  const canvas = areaCanvas(map, mapKey);
  if (!canvas) return;
  const { width: w, height: h } = map.data;
  const availW = screenWidth - 16, availH = screenHeight - 28;
  const scale = Math.max(1, Math.floor(Math.min(availW / w, availH / h)));
  const dw = w * scale, dh = h * scale;
  const ox = Math.floor((screenWidth - dw) / 2), oy = Math.floor((screenHeight - dh) / 2) + 8;
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, ox, oy, dw, dh);
  ctx.strokeStyle = "#f2c14e";
  ctx.strokeRect(ox - 1.5, oy - 1.5, dw + 3, dh + 3);
  // 出入り口
  ctx.fillStyle = "#f2c14e";
  for (const e of map.data.exits ?? []) {
    ctx.fillRect(ox + e.tileX * scale, oy + e.tileY * scale, Math.max(2, scale), Math.max(2, scale));
  }
  // いまの位置（点滅）
  if (Math.floor(nowMs / 350) % 2 === 0) {
    const px = ox + playerTile.x * scale + scale / 2, py = oy + playerTile.y * scale + scale / 2;
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(Math.round(px) - 3, Math.round(py) - 3, 7, 7);
    ctx.fillStyle = "#e8483c";
    ctx.fillRect(Math.round(px) - 2, Math.round(py) - 2, 5, 5);
  }
  ctx.textAlign = "left";
  ctx.textBaseline = "top";
  ctx.fillStyle = "#f2c14e";
  ctx.font = "9px monospace";
  ctx.fillText(`${title}（Vキー・地図ボタン・決定でとじる）　赤＝いまの場所　金＝出入り口`, 8, 3);
}
