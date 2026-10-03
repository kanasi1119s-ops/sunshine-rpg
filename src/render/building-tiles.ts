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
  const canvas = canvasFor(key, above ? wallTile(style, variant, tx, ty, below, left, right, false) : roofTile(style, variant, left, right, below));
  if (!canvas) {
    return false;
  }
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, screenX, screenY, map.data.tileWidth, map.data.tileHeight);
  return true;
}
