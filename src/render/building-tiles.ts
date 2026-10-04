import { getTileId, type TileMap } from "../game/map/tile-map";
import { hashCell, shadeColor } from "../game/color-utils";

/**
 * 町の建物（壁のタイルが四角くかたまっている部分）を、屋根と壁の絵で描く。
 *  - 一番上の段は屋根（互い違いの瓦、棟の明るい縁、のき先の影）。
 *  - それより下は壁（しっくい、窓とよろい戸、土台の石、のきの下の影）。光は左上。
 * 地図ごとの屋根・壁の色は `map-tile-art.ts` で決める。タイル座標だけから決まるので、毎フレーム同じ絵になる。
 */
export interface BuildingStyle {
  walls: number[];
  roof: string;
  plaster: string;
  /** true なら、屋根と壁ではなく、しま模様の布のテント（隊商の町）として描く。 */
  tent?: boolean;
}

const SIZE = 16;
const cache = new Map<string, HTMLCanvasElement>();

type Put = (x: number, y: number, c: string) => void;

function roofTile(style: BuildingStyle, variant: number, left: boolean, right: boolean, belowWall: boolean): (put: Put) => void {
  const base = style.roof;
  return (put) => {
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        const row = Math.floor(y / 4);
        const ry = y % 4;
        const off = row % 2 === 0 ? 0 : 4;
        const sx = (x + off) % 8;
        const tile = hashCell(Math.floor((x + off) / 8) + row * 3 + variant, 5);
        let c = tile % 3 === 0 ? shadeColor(base, 0.08) : tile % 3 === 1 ? base : shadeColor(base, -0.08);
        if (ry === 3) c = shadeColor(base, -0.38);
        else if (ry === 0) c = shadeColor(c, 0.2);
        if (sx === 7) c = shadeColor(base, -0.3);
        if (y === 0) c = shadeColor(base, 0.38);
        if (belowWall && y >= 14) c = shadeColor(base, y === 14 ? -0.45 : -0.6);
        put(x, y, c);
      }
    }
    if (!left) {
      for (let y = 0; y < SIZE; y++) put(0, y, shadeColor(base, 0.3));
    }
    if (!right) {
      for (let y = 0; y < SIZE; y++) put(SIZE - 1, y, shadeColor(base, -0.5));
    }
  };
}

function wallTile(style: BuildingStyle, variant: number, tx: number, ty: number, below: boolean, left: boolean, right: boolean, aboveRoof: boolean): (put: Put) => void {
  const base = style.plaster;
  return (put) => {
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        const n = hashCell(x * 3 + variant, y * 5 + tx);
        let c = n % 13 === 0 ? shadeColor(base, -0.07) : n % 17 === 0 ? shadeColor(base, 0.06) : base;
        if (!below && y >= 13) c = y === 13 ? shadeColor(base, -0.35) : shadeColor("#6a6a72", (hashCell(x, y + tx) % 5) * 0.03 - (y - 13) * 0.08);
        if (aboveRoof && y < 4) c = shadeColor(c, -0.46 + y * 0.1);
        put(x, y, c);
      }
    }
    // 角の柱（左右のはし）
    if (!left) for (let y = 0; y < SIZE; y++) put(0, y, shadeColor(base, 0.25));
    if (!right) for (let y = 0; y < SIZE; y++) put(SIZE - 1, y, shadeColor(base, -0.35));
    // 窓: 市松に並べる。濃い枠、空色のガラス、左上の反射、よろい戸、窓台。
    if ((tx + ty) % 2 === 0 && below === false || (tx + ty) % 2 === 0 && variant === 1) {
      const wx = 4, wy = 4, ww = 8, wh = 7;
      for (let y = wy; y < wy + wh; y++) {
        for (let x = wx; x < wx + ww; x++) {
          const edge = x === wx || y === wy || x === wx + ww - 1 || y === wy + wh - 1;
          const mid = x === wx + ww / 2 || y === wy + 3;
          put(x, y, edge ? "#3a2a1e" : mid ? "#5a4026" : y < wy + 3 ? "#9cc8e8" : "#6a9cc4");
        }
      }
      put(wx + 1, wy + 1, "#e8f6ff");
      put(wx + 2, wy + 1, "#e8f6ff");
      for (let x = wx - 1; x <= wx + ww; x++) put(x, wy + wh, shadeColor(base, -0.3));
      for (let y = wy; y < wy + wh; y++) {
        put(wx - 2, y, shadeColor(style.roof, -0.1));
        put(wx + ww + 1, y, shadeColor(style.roof, -0.3));
      }
    } else {
      // 木のはり
      for (let x = 0; x < SIZE; x++) put(x, 7, shadeColor(base, -0.2));
    }
  };
}

/** テント: 縦じまの布。上の段は屋根の勾配（ひだと棟の縄）、下の段は垂れ布のすそ（波形）と地面の影。 */
function tentTile(style: BuildingStyle, top: boolean, tx: number, left: boolean, right: boolean): (put: Put) => void {
  return (put) => {
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        const stripe = Math.floor((x + tx * 16) / 4) % 2 === 0;
        let c = stripe ? style.roof : style.plaster;
        const fold = (x + tx * 16) % 4;
        if (fold === 0) c = shadeColor(c, 0.1);
        else if (fold === 3) c = shadeColor(c, -0.18);
        if (top) {
          if (y < 2) c = shadeColor(style.plaster, -0.25);
          if (y === 2) c = shadeColor(c, -0.3);
          if (y > 12) c = shadeColor(c, -0.14 * (y - 12));
        } else {
          const hem = 11 + (Math.floor((x + tx * 16) / 4) % 2 === 0 ? 2 : 0);
          if (y > hem) c = y === hem + 1 ? shadeColor(c, -0.45) : "rgba(0,0,0,0)";
        }
        if (c !== "rgba(0,0,0,0)") put(x, y, c);
      }
    }
    if (!left) for (let y = 0; y < SIZE; y++) put(0, y, shadeColor(style.roof, -0.5));
    if (!right) for (let y = 0; y < SIZE; y++) put(SIZE - 1, y, shadeColor(style.roof, -0.5));
  };
}

function canvasFor(key: string, paint: (put: Put) => void): HTMLCanvasElement | null {
  if (typeof document === "undefined") {
    return null;
  }
  let canvas = cache.get(key);
  if (!canvas) {
    canvas = document.createElement("canvas");
    canvas.width = SIZE;
    canvas.height = SIZE;
    const c = canvas.getContext("2d");
    if (!c) {
      return null;
    }
    paint((x, y, color) => {
      if (x < 0 || y < 0 || x >= SIZE || y >= SIZE) return;
      c.fillStyle = color;
      c.fillRect(x, y, 1, 1);
    });
    cache.set(key, canvas);
  }
  return canvas;
}

/** 建物の壁のタイルなら、屋根か壁の絵で描く。描いたら true。 */
export function drawBuildingTile(
  ctx: CanvasRenderingContext2D,
  map: TileMap,
  tileId: number,
  tx: number,
  ty: number,
  screenX: number,
  screenY: number,
): boolean {
  const style = map.data.building;
  if (!style || !style.walls.includes(tileId)) {
    return false;
  }
  const isB = (x: number, y: number): boolean => style.walls.includes(getTileId(map, 0, x, y));
  const above = isB(tx, ty - 1), below = isB(tx, ty + 1), left = isB(tx - 1, ty), right = isB(tx + 1, ty);
  const variant = hashCell(tx, ty) % 3;
  const key = `${style.roof}|${style.plaster}|${above ? "w" : "r"}${below ? 1 : 0}${left ? 1 : 0}${right ? 1 : 0}|${variant}|${(tx + ty) % 2}|${tx % 3}`;
  const paint = style.tent
    ? tentTile(style, !above, tx, left, right)
    : above
      ? wallTile(style, variant, tx, ty, below, left, right, false)
      : roofTile(style, variant, left, right, below);
  const canvas = canvasFor(`${style.tent ? "t" : ""}${key}`, paint);
  if (!canvas) {
    return false;
  }
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, screenX, screenY, map.data.tileWidth, map.data.tileHeight);
  return true;
}

/** 建物の出入り口（真上が建物の壁で、出口がある場所）なら、木の扉の絵で描く。描いたら true。 */
export function drawDoorTile(
  ctx: CanvasRenderingContext2D,
  map: TileMap,
  tx: number,
  ty: number,
  screenX: number,
  screenY: number,
): boolean {
  const style = map.data.building;
  if (!style || style.tent || !style.walls.includes(getTileId(map, 0, tx, ty - 1))) {
    return false;
  }
  if (!(map.data.exits ?? []).some((e) => e.tileX === tx && e.tileY === ty)) {
    return false;
  }
  const canvas = canvasFor("door|" + style.plaster, (put) => {
    const wood = "#7a4a26";
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        let c = shadeColor(style.plaster, y > 12 ? -0.14 * (y - 12) : 0);
        if (x >= 3 && x <= 12 && y >= 1) {
          // 石の枠
          c = "#5a4a3c";
          if (x >= 4 && x <= 11 && y >= 2) {
            // 板の扉（縦の継ぎ目と、上の丸み）
            const arch = y < 5 && (x === 4 || x === 11) && y < 4 - (y === 2 ? 0 : 1) ? "#5a4a3c" : null;
            c = arch ?? (x === 7 || x === 8 ? shadeColor(wood, -0.25) : x % 2 === 0 ? wood : shadeColor(wood, 0.1));
            if (y === 9) c = shadeColor(wood, -0.35);
          }
        }
        put(x, y, c);
      }
    }
    // ドアノブ
    put(10, 9, "#f2c14e");
    put(10, 10, "#f2c14e");
    // 敷居の石
    for (let x = 2; x <= 13; x++) {
      put(x, 14, "#9a8a78");
      put(x, 15, "#7a6a58");
    }
  });
  if (!canvas) {
    return false;
  }
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, screenX, screenY, map.data.tileWidth, map.data.tileHeight);
  return true;
}
