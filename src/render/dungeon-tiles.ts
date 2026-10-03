import { getTileId, type TileMap } from "../game/map/tile-map";
import { hashCell, shadeColor } from "../game/color-utils";

/**
 * ダンジョン・塔・洞窟・遺跡の床と壁（スーファミ後期＝32メガビット級の質感を目標にした描き方）。
 *  - 壁は「正面（石組み・欠け・縁の光）」と「上面（暗い天面）」を、足元のマスが床かどうかで描き分けて厚みを出す。
 *  - 床は、壁のすぐ下に影、壁の横にも影を落とす（光は左上）。
 *  - 材質ごとに5階調の色（暗→明）を持ち、石畳は面取り（左上が明るく右下が暗い）、土は小石とひび、岩は欠けた塊で描く。
 * タイル座標だけから決まるので、毎フレーム同じ絵になる。ブラウザ以外（自動テスト）では何も描かず false を返す。
 */
export type DungeonTheme = "tower" | "mine" | "ruins" | "facility" | "interior";

interface ThemeSpec {
  floorKind: "slab" | "dirt" | "cobble" | "plank";
  wallKind: "brick" | "rock" | "plaster";
  floor: string[];
  wall: string[];
  cap: string[];
  moss: boolean;
  glint: string | null;
}

const THEMES: Record<DungeonTheme, ThemeSpec> = {
  tower: {
    floorKind: "slab", wallKind: "brick", moss: false, glint: null,
    floor: ["#3a4058", "#4a5270", "#5c6688", "#7280a2", "#9aa8c6"],
    wall: ["#1e2236", "#2e3452", "#434b70", "#5c668c", "#8490b4"],
    cap: ["#12141f", "#1a1d2e", "#262a40"],
  },
  mine: {
    floorKind: "cobble", wallKind: "rock", moss: false, glint: "#7ad8f0",
    floor: ["#2e2418", "#433422", "#5a4630", "#745c40", "#927650"],
    wall: ["#1a130e", "#2a1f16", "#3e2e22", "#584432", "#7a6048"],
    cap: ["#0e0a07", "#16100b", "#20170f"],
  },
  ruins: {
    floorKind: "cobble", wallKind: "brick", moss: true, glint: null,
    floor: ["#2c2842", "#3a3558", "#4a446c", "#5e5886", "#7e78a8"],
    wall: ["#181428", "#262040", "#38305a", "#4c4474", "#6c6498"],
    cap: ["#0c0a16", "#14101f", "#1c1830"],
  },
  facility: {
    floorKind: "slab", wallKind: "brick", moss: false, glint: null,
    floor: ["#2e3a40", "#3c4a52", "#4e5e68", "#64767f", "#8498a2"],
    wall: ["#1a2228", "#26323a", "#364650", "#4c606c", "#6c8492"],
    cap: ["#0e1418", "#151d22", "#1e282e"],
  },
  interior: {
  floorKind: "plank", wallKind: "plaster", moss: false, glint: null,
  floor: ["#2e1c10", "#4a2f1a", "#68452a", "#84603a", "#a07a4c"],
  wall: ["#2a1e16", "#4a3a2c", "#d8ccb0", "#c0b294", "#e8dec6"],
  cap: ["#1e140e", "#2c1e14", "#3a281a"],
  },
};


const MOSS = ["#3a5a32", "#52743e", "#6e8e50"];
const SIZE = 16;

type Painter = (x: number, y: number, put: (px: number, py: number, color: string) => void) => void;

function floorSlab(t: ThemeSpec, variant: number, tx: number, ty: number): Painter {
  return (_x, _y, put) => {
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        const row = y >> 3;
        const sx = (x + (row % 2 === 0 ? 0 : 4)) % 8;
        const sy = y % 8;
        const slab = hashCell(((x + (row % 2 === 0 ? 0 : 4)) >> 3) + variant * 5 + tx, row + ty * 3);
        let c: string;
        if (sx === 0 || sy === 0) {
          c = shadeColor(t.floor[1], -0.15);
        } else if (sx === 1 || sy === 1) {
          c = shadeColor(t.floor[2], 0.16);
        } else if (sx === 7 || sy === 7) {
          c = shadeColor(t.floor[2], -0.16);
        } else {
          c = slab % 3 === 0 ? shadeColor(t.floor[2], 0.07) : slab % 3 === 1 ? t.floor[2] : shadeColor(t.floor[2], -0.06);
          const n = hashCell(x * 7 + variant, y * 13 + tx);
          if (n % 23 === 0) c = shadeColor(c, -0.12);
          else if (n % 29 === 0) c = shadeColor(c, 0.1);
        }
        put(x, y, c);
      }
    }
    // ひび（斜めに細く）
    if (variant === 1 || variant === 3) {
      let cx = 3 + (variant === 3 ? 6 : 0), cy = 2;
      for (let i = 0; i < 6; i++) {
        put(cx, cy, t.floor[0]);
        cx += i % 2 === 0 ? 1 : 0;
        cy += 1;
        if (i === 3) cx -= 2;
      }
    }
    // 目地ぎわのコケ
    if (t.moss && variant >= 2) {
      for (let i = 0; i < 7; i++) {
        const mx = (hashCell(i + variant, tx) % 14) + 1;
        const my = i % 2 === 0 ? 1 : 8 + (hashCell(i, ty) % 2);
        put(mx, my, MOSS[i % 3]);
        if (i % 2 === 0) put(mx + 1, my, MOSS[0]);
      }
    }
  };
}

/** 丸みのある不ぞろいな敷石（洞窟・遺跡の床）。段ごとに石の幅を変え、角を落とし、左上を明るく、すき間を暗く。 */
function stoneGrid(pal: string[], variant: number, tx: number, ty: number, put: (x: number, y: number, c: string) => void, gap: string): void {
  const bands = [0, 5, 10, 16];
  for (let b = 0; b < 3; b++) {
    const y0 = bands[b], y1 = bands[b + 1];
    let x = -((hashCell(b + variant, tx + 3) % 5));
    while (x < SIZE) {
      const w = 4 + (hashCell(x + b * 7 + variant, ty + b) % 3);
      const tone = hashCell(x * 3 + b + variant, tx * 5 + ty) % 4;
      const base = tone === 0 ? shadeColor(pal[2], 0.09) : tone === 1 ? shadeColor(pal[2], -0.08) : pal[2];
      for (let yy = y0; yy < y1; yy++) {
        for (let xx = x; xx < x + w; xx++) {
          if (xx < 0 || xx >= SIZE) continue;
          const lx = xx - x, ly = yy - y0, sw = w, sh = y1 - y0;
          let c = base;
          if (lx === 0 || ly === 0) c = gap;
          else if ((lx === 1 && ly === 1) || (lx === sw - 1 && ly === sh - 1) || (lx === sw - 1 && ly === 1) || (lx === 1 && ly === sh - 1)) c = shadeColor(gap, 0.25);
          else if (lx === 1 || ly === 1) c = shadeColor(base, 0.2);
          else if (lx === sw - 1 || ly === sh - 1) c = shadeColor(base, -0.2);
          else if (hashCell(xx * 7 + variant, yy * 3 + tx) % 17 === 0) c = shadeColor(base, -0.1);
          put(xx, yy, c);
        }
      }
      x += w;
    }
  }
}

function floorCobble(t: ThemeSpec, variant: number, tx: number, ty: number): Painter {
  return (_x, _y, put) => {
    stoneGrid(t.floor, variant, tx, ty, put, shadeColor(t.floor[0], -0.2));
    if (t.moss && variant >= 2) {
      for (let i = 0; i < 6; i++) {
        const mx = hashCell(i + variant, tx + 9) % 15;
        const my = (hashCell(i, ty + 4) % 3) * 5;
        put(mx, my, MOSS[i % 3]);
        if (i % 2 === 0) put(mx + 1, my, MOSS[0]);
      }
    }
  };
}

/** 板張りの床（横に長い板。段ごとに継ぎ目の位置をずらし、板ごとに色を少し変え、木目の筋とくぎを入れる）。 */
function floorPlank(t: ThemeSpec, variant: number, tx: number, ty: number): Painter {
  return (_x, _y, put) => {
    for (let y = 0; y < SIZE; y++) {
      const board = Math.floor(y / 4);
      const ly = y % 4;
      const joint = (hashCell(board + variant * 3, tx + 5) % 12) + 2;
      for (let x = 0; x < SIZE; x++) {
        const seg = x < joint ? 0 : 1;
        const tone = hashCell(board * 2 + seg + variant, ty + tx * 3) % 5;
        const base = tone === 0 ? shadeColor(t.floor[2], 0.08) : tone === 1 ? shadeColor(t.floor[2], -0.08) : t.floor[2];
        let c = base;
        if (ly === 3) c = t.floor[1];
        else if (ly === 0) c = shadeColor(base, 0.12);
        if (x === joint && ly !== 3) c = t.floor[0];
        if ((ly === 1 || ly === 2) && hashCell(x * 5 + board * 3 + variant, ly + tx) % 9 === 0) c = shadeColor(base, -0.12);
        put(x, y, c);
      }
    }
    for (let board = 0; board < 4; board++) {
      const joint = (hashCell(board + variant * 3, tx + 5) % 12) + 2;
      put(Math.min(15, joint + 2), board * 4 + 1, t.floor[0]);
    }
  };
}

/** しっくいの壁の正面: 上にのき飾り、白い壁、下に腰板（羽目板）と幅木。 */
function wallFrontPlaster(t: ThemeSpec, variant: number, tx: number): Painter {
  const wood = ["#2c1e14", "#4a321e", "#6a4828", "#845c34"];
  return (_x, _y, put) => {
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        let c: string;
        if (y === 0) c = wood[3];
        else if (y === 1) c = wood[2];
        else if (y === 2) c = wood[0];
        else if (y < 9) {
          const n = hashCell(x * 3 + variant, y * 7 + tx);
          c = n % 11 === 0 ? t.wall[3] : t.wall[2];
          if (y === 3) c = t.wall[3];
        } else if (y === 9) c = wood[3];
        else if (y < 14) {
          const panel = x % 8;
          c = panel === 0 || panel === 7 ? wood[0] : y === 10 ? wood[3] : y === 13 ? wood[1] : wood[2];
        } else c = y === 14 ? wood[0] : t.cap[0];
        put(x, y, c);
      }
    }
  };
}

function floorDirt(t: ThemeSpec, variant: number, tx: number, ty: number): Painter {
  return (_x, _y, put) => {
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        const n = hashCell(x * 5 + variant * 17 + tx, y * 11 + ty);
        const blob = hashCell((x >> 2) + variant, (y >> 2) + tx * 2) % 4;
        let c = t.floor[2];
        if (blob === 0) c = shadeColor(t.floor[2], -0.1);
        else if (blob === 3) c = shadeColor(t.floor[2], 0.08);
        if (n % 17 === 0) c = t.floor[1];
        else if (n % 19 === 0) c = t.floor[3];
        put(x, y, c);
      }
    }
    // 小石（明るい面と影つき）
    for (let i = 0; i < 3; i++) {
      const px = 1 + (hashCell(i * 3 + variant, tx + 1) % 12);
      const py = 2 + (hashCell(i * 5 + variant, ty + 2) % 11);
      put(px, py, t.floor[4]);
      put(px + 1, py, t.floor[3]);
      put(px, py + 1, t.floor[0]);
      put(px + 1, py + 1, t.floor[0]);
    }
    if (variant === 2) {
      for (let i = 0; i < 7; i++) put(2 + i, 6 + (i % 3 === 1 ? 1 : 0), t.floor[0]);
    }
  };
}

function wallFrontBrick(t: ThemeSpec, variant: number, tx: number): Painter {
  return (_x, _y, put) => {
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        let c: string;
        if (y === 0) {
          c = t.wall[4];
        } else if (y === 1) {
          c = t.wall[3];
        } else if (y >= 14) {
          c = y === 14 ? t.wall[0] : t.cap[0];
        } else {
          const course = Math.floor((y - 2) / 4);
          const cy = (y - 2) % 4;
          const off = course % 2 === 0 ? 0 : 4;
          const bx = (x + off) % 8;
          const brick = hashCell(Math.floor((x + off) / 8) + course * 3 + variant, tx);
          if (cy === 3 || bx === 7) {
            c = t.wall[0];
          } else if (cy === 0) {
            c = t.wall[3];
          } else if (bx === 0) {
            c = t.wall[3];
          } else {
            c = brick % 4 === 0 ? t.wall[3] : brick % 4 === 1 ? t.wall[1] : t.wall[2];
            if (hashCell(x + variant * 9, y * 5 + tx) % 12 === 0) c = t.wall[1];
          }
          if (cy === 2 && c === t.wall[2]) c = t.wall[1];
        }
        put(x, y, c);
      }
    }
  };
}

function wallFrontRock(t: ThemeSpec, variant: number, tx: number): Painter {
  return (_x, _y, put) => {
    // 下の段は、石組みの壁（敷石と同じ作りの暗い色）
    stoneGrid(t.wall, variant, tx, 7, put, t.wall[0]);
    // 上は、ぎざぎざに垂れる岩の天井（つらら状の岩のへり）
    for (let x = 0; x < SIZE; x++) {
      const depth = 4 + (hashCell((x >> 1) + variant * 3, tx + 11) % 5);
      for (let y = 0; y < depth; y++) {
        const edge = y === depth - 1;
        put(x, y, edge ? t.wall[0] : y === 0 ? t.wall[4] : y < depth - 2 ? (hashCell(x + y, tx) % 4 === 0 ? t.wall[2] : t.wall[3]) : t.wall[1]);
      }
    }
    for (let y = 14; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) put(x, y, y === 14 ? t.wall[0] : t.cap[0]);
    }
    // 光る鉱石のかけら
    if (t.glint && variant === 2) {
      put(5, 9, t.glint);
      put(6, 9, "#d8f8ff");
      put(5, 10, "#3a9ac0");
      put(10, 11, t.glint);
      put(10, 12, "#3a9ac0");
    }
    // 木の補強（縦の支柱）
    if (t.glint && variant === 0) {
      for (let y = 1; y < 14; y++) {
        put(7, y, "#6a4a2a");
        put(8, y, "#8a6238");
        put(9, y, "#4a3220");
      }
    }
  };
}

function wallCap(t: ThemeSpec, variant: number, tx: number, ty: number): Painter {
  return (_x, _y, put) => {
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        const n = hashCell(x * 3 + variant, y * 7 + tx + ty * 5);
        put(x, y, n % 9 === 0 ? t.cap[2] : n % 5 === 0 ? t.cap[1] : t.cap[0]);
      }
    }
  };
}

const tileCache = new Map<string, HTMLCanvasElement>();

function canvasFor(key: string, paint: Painter, overlay?: (c: CanvasRenderingContext2D) => void): HTMLCanvasElement | null {
  if (typeof document === "undefined") {
    return null;
  }
  let canvas = tileCache.get(key);
  if (!canvas) {
    canvas = document.createElement("canvas");
    canvas.width = SIZE;
    canvas.height = SIZE;
    const c = canvas.getContext("2d");
    if (!c) {
      return null;
    }
    paint(0, 0, (x, y, color) => {
      if (x < 0 || y < 0 || x >= SIZE || y >= SIZE) return;
      c.fillStyle = color;
      c.fillRect(x, y, 1, 1);
    });
    overlay?.(c);
    tileCache.set(key, canvas);
  }
  return canvas;
}

const SHADE = "16,14,28";

/** 壁か。マップの外も壁とみなす。 */
function isWall(map: TileMap, x: number, y: number): boolean {
  if (x < 0 || y < 0 || x >= map.data.width || y >= map.data.height) {
    return true;
  }
  const id = getTileId(map, 0, x, y);
  return map.data.tileArt?.[id] === "tint:brick" || map.data.collision?.[y * map.data.width + x] === 1 && map.data.tileArt?.[id] === "tint:flagstone";
}

function isFloor(art: string | undefined): boolean {
  return art === "tint:flagstone";
}

/** テーマつきの地図で、床と壁を描く。描いたら true。 */
export function drawDungeonTile(
  ctx: CanvasRenderingContext2D,
  map: TileMap,
  tileId: number,
  tx: number,
  ty: number,
  screenX: number,
  screenY: number,
): boolean {
  const themeName = map.data.theme as DungeonTheme | undefined;
  const t = themeName && THEMES[themeName];
  if (!t) {
    return false;
  }
  const art = map.data.tileArt?.[tileId];
  const variant = hashCell(tx, ty) % 4;
  let canvas: HTMLCanvasElement | null = null;
  if (art === "tint:brick") {
    const below = isWall(map, tx, ty + 1);
    const above = isWall(map, tx, ty - 1);
    const left = isWall(map, tx - 1, ty);
    const right = isWall(map, tx + 1, ty);
    if (!below) {
      const front = t.wallKind === "brick" ? wallFrontBrick(t, variant, tx % 3) : t.wallKind === "plaster" ? wallFrontPlaster(t, variant, tx % 3) : wallFrontRock(t, variant, tx % 3);
      canvas = canvasFor(`${themeName}|front|${variant}|${tx % 3}`, front);
    } else {
      const mask = `${above ? 1 : 0}${left ? 1 : 0}${right ? 1 : 0}`;
      canvas = canvasFor(`${themeName}|cap|${variant}|${mask}|${tx % 2}${ty % 2}`, wallCap(t, variant, tx % 2, ty % 2), (c) => {
        if (!above) {
          c.fillStyle = t.wall[3];
          c.fillRect(0, 0, SIZE, 1);
          c.fillStyle = t.cap[2];
          c.fillRect(0, 1, SIZE, 1);
        }
        if (!left) {
          c.fillStyle = t.wall[2];
          c.fillRect(0, 0, 1, SIZE);
        }
        if (!right) {
          c.fillStyle = t.cap[2];
          c.fillRect(SIZE - 1, 0, 1, SIZE);
        }
      });
    }
  } else if (isFloor(art) || (themeName === "interior" && tileId === 1)) {
    const above = isWall(map, tx, ty - 1);
    const left = isWall(map, tx - 1, ty);
    const right = isWall(map, tx + 1, ty);
    const mask = `${above ? 1 : 0}${left ? 1 : 0}${right ? 1 : 0}`;
    const paint = t.floorKind === "slab" ? floorSlab(t, variant, tx % 3, ty % 3) : t.floorKind === "plank" ? floorPlank(t, variant, tx % 3, ty % 3) : t.floorKind === "cobble" ? floorCobble(t, variant, tx % 3, ty % 3) : floorDirt(t, variant, tx % 3, ty % 3);
    canvas = canvasFor(`${themeName}|floor|${variant}|${mask}|${tx % 3}${ty % 3}`, paint, (c) => {
      if (above) {
        [0.55, 0.36, 0.2, 0.09].forEach((a, i) => {
          c.fillStyle = `rgba(${SHADE},${a})`;
          c.fillRect(0, i, SIZE, 1);
        });
      }
      if (left) {
        c.fillStyle = `rgba(${SHADE},0.28)`;
        c.fillRect(0, 0, 1, SIZE);
        c.fillStyle = `rgba(${SHADE},0.14)`;
        c.fillRect(1, 0, 1, SIZE);
      }
      if (right) {
        c.fillStyle = `rgba(${SHADE},0.2)`;
        c.fillRect(SIZE - 1, 0, 1, SIZE);
      }
    });
  }
  if (!canvas) {
    return false;
  }
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, screenX, screenY, map.data.tileWidth, map.data.tileHeight);
  return true;
}

/** 壁のたいまつ: ところどころの壁に、ゆれる炎とまわりの光（床と壁を明るく照らす）を重ねる。時刻でゆらぐ。 */
export function renderDungeonLights(ctx: CanvasRenderingContext2D, map: TileMap, camera: { x: number; y: number; viewportWidth: number; viewportHeight: number }, nowMs: number): void {
  const themeName = map.data.theme as DungeonTheme | undefined;
  if (!themeName || themeName === "interior" || !THEMES[themeName]) {
    return;
  }
  const s = map.data.tileWidth;
  const startX = Math.max(0, Math.floor(camera.x / s) - 2);
  const endX = Math.min(map.data.width - 1, Math.floor((camera.x + camera.viewportWidth) / s) + 2);
  const startY = Math.max(0, Math.floor(camera.y / s) - 2);
  const endY = Math.min(map.data.height - 1, Math.floor((camera.y + camera.viewportHeight) / s) + 3);
  for (let ty = startY; ty <= endY; ty++) {
    for (let tx = startX; tx <= endX; tx++) {
      const id = getTileId(map, 0, tx, ty);
      const torchAt = (x: number): boolean => hashCell(x * 7 + 3, ty * 5) % 9 === 0 && x % 2 === 0;
      if (map.data.tileArt?.[id] !== "tint:brick" || isWall(map, tx, ty + 1) || !torchAt(tx) || torchAt(tx - 2) || torchAt(tx + 2)) {
        continue;
      }
      const x = tx * s - camera.x;
      const y = ty * s - camera.y;
      const flick = Math.sin(nowMs / 90 + tx * 2.1 + ty) * 0.5 + Math.sin(nowMs / 37 + tx) * 0.3;
      // 光（足元の床まで届く丸い明かり）
      const g = ctx.createRadialGradient(x + 8, y + 8, 2, x + 8, y + 14, 44 + flick * 5);
      g.addColorStop(0, `rgba(255,190,90,${0.26 + flick * 0.05})`);
      g.addColorStop(1, "rgba(255,150,60,0)");
      ctx.save();
      ctx.globalCompositeOperation = "lighter";
      ctx.fillStyle = g;
      ctx.fillRect(x - 40, y - 36, s + 80, s + 90);
      ctx.restore();
      // たいまつ本体: 受け金具、棒、炎（外は赤、中は橙、芯は黄）
      ctx.fillStyle = "#1a1210";
      ctx.fillRect(x + 6, y + 9, 4, 1);
      ctx.fillStyle = "#4a3220";
      ctx.fillRect(x + 7, y + 6, 2, 5);
      const lean = flick > 0.3 ? 1 : flick < -0.3 ? -1 : 0;
      const fh = 4 + (flick > 0 ? 1 : 0);
      ctx.fillStyle = "#c8381c";
      ctx.fillRect(x + 6 + lean, y + 6 - fh, 4, fh);
      ctx.fillStyle = "#f08a24";
      ctx.fillRect(x + 7 + lean, y + 6 - fh + 1, 2, fh - 1);
      ctx.fillStyle = "#ffe070";
      ctx.fillRect(x + 7 + lean, y + 6 - Math.max(2, fh - 2), 2, Math.max(2, fh - 2));
    }
  }
}
