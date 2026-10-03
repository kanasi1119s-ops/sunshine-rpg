import { getTileId, type TileMap } from "../game/map/tile-map";
import { hashCell } from "../game/color-utils";
import type { Camera } from "./camera";

/**
 * 地面のしあげ。見本のマップ（道がうねり、池に岸があり、草地に小さな草花が散っている）から学んだこと:
 *  1. 地形の境目はまっすぐにせず、ギザギザにして草が道に食い込み、池には岸と浅瀬の縁を付ける。
 *  2. 木の下の地面には影を落として、木と地面をなじませる。
 *  3. 何もない草地にも、小さな草・花・小石をまばらに散らして、「何もない」感じをなくす。
 * どれもタイル座標だけから決まるので、毎フレーム同じ絵になる（ちらつかない）。マップのデータは変えない。
 */
type Kind = "grass" | "path" | "water" | "tree" | "other";

const KIND_BY_ART: Record<string, Kind> = { grass: "grass", path: "path", water: "water", treeCanopy: "tree" };

const GRASS_DARK = "#3f7a35";
const GRASS_MID = "#5f9f46";
const GRASS_LIGHT = "#86bf5c";
const BANK = "#4a3c2a";
const SHALLOW = "#7ab6d8";
const FOAM = "#c4e4f2";
const SHADOW = "rgba(14, 40, 24, 0.34)";
const FLOWERS = ["#f4f0e0", "#f2c14e", "#e86a8a", "#9a8ae8"];

function kindAt(map: TileMap, x: number, y: number): Kind {
  if (x < 0 || y < 0 || x >= map.data.width || y >= map.data.height) {
    return "other";
  }
  const id = getTileId(map, 0, x, y);
  const art = id ? map.data.tileArt?.[id] : undefined;
  return (art && KIND_BY_ART[art]) || "other";
}

function dot(ctx: CanvasRenderingContext2D, x: number, y: number, color: string, w = 1, h = 1): void {
  ctx.fillStyle = color;
  ctx.fillRect(Math.round(x), Math.round(y), w, h);
}

/** 辺ごとの向き: [隣のずれ x, y]。辺に沿った点の位置を返す関数も持つ。 */
const SIDES: Array<{ dx: number; dy: number; at: (i: number, d: number, s: number) => [number, number] }> = [
  { dx: 0, dy: -1, at: (i, d) => [i, d] },
  { dx: 0, dy: 1, at: (i, d, s) => [i, s - 1 - d] },
  { dx: -1, dy: 0, at: (i, d) => [d, i] },
  { dx: 1, dy: 0, at: (i, d, s) => [s - 1 - d, i] },
];

/** 道の縁: 隣が草なら、草がギザギザに食い込む。 */
function pathEdge(ctx: CanvasRenderingContext2D, ox: number, oy: number, s: number, tx: number, ty: number, side: number): void {
  for (let i = 0; i < s; i++) {
    const h = hashCell(tx * 31 + i + side * 7, ty * 17 + side);
    const depth = h % 7 < 3 ? 1 : h % 7 < 6 ? 2 : 3;
    for (let d = 0; d < depth; d++) {
      const [px, py] = SIDES[side].at(i, d, s);
      dot(ctx, ox + px, oy + py, d === depth - 1 && depth > 1 ? GRASS_DARK : d === 0 ? GRASS_MID : GRASS_MID);
    }
    if (h % 5 === 0) {
      const [px, py] = SIDES[side].at(i, 0, s);
      dot(ctx, ox + px, oy + py, GRASS_LIGHT);
    }
  }
}

/** 池の縁: 隣が陸なら、岸の線と、水側の浅瀬・あわ。 */
function waterEdge(ctx: CanvasRenderingContext2D, ox: number, oy: number, s: number, tx: number, ty: number, side: number): void {
  for (let i = 0; i < s; i++) {
    const h = hashCell(tx * 29 + i + side * 5, ty * 13 + side);
    const [bx, by] = SIDES[side].at(i, 0, s);
    dot(ctx, ox + bx, oy + by, BANK);
    const [sx, sy] = SIDES[side].at(i, 1, s);
    dot(ctx, ox + sx, oy + sy, h % 3 === 0 ? FOAM : SHALLOW);
    if (h % 4 === 0) {
      const [qx, qy] = SIDES[side].at(i, 2, s);
      dot(ctx, ox + qx, oy + qy, SHALLOW);
    }
  }
}

/** 木の下（南どなりの草地）に落ちる影。市松でなじませる。 */
function treeShadow(ctx: CanvasRenderingContext2D, ox: number, oy: number, s: number, tx: number, ty: number): void {
  for (let i = 0; i < s; i++) {
    const h = hashCell(tx * 19 + i, ty * 23);
    const depth = 3 + (h % 3);
    for (let d = 0; d < depth; d++) {
      if (d === depth - 1 && (i + d) % 2 === 0) {
        continue;
      }
      dot(ctx, ox + i, oy + d, SHADOW);
    }
  }
}

/** 草地にまばらに散らす小さな草・花・小石。 */
function grassDecor(ctx: CanvasRenderingContext2D, ox: number, oy: number, s: number, tx: number, ty: number): void {
  const h = hashCell(tx * 73 + 5, ty * 91 + 11);
  const slot = h % 100;
  if (slot >= 34) {
    return;
  }
  const px = ox + 2 + (hashCell(tx, ty * 3 + 1) % (s - 5));
  const py = oy + 3 + (hashCell(tx * 5 + 2, ty) % (s - 6));
  if (slot < 17) {
    // 草のかたまり（V字の3本）
    dot(ctx, px, py, GRASS_DARK);
    dot(ctx, px + 2, py, GRASS_DARK);
    dot(ctx, px + 1, py - 1, GRASS_LIGHT);
    dot(ctx, px, py - 1, GRASS_MID);
    dot(ctx, px + 2, py - 2, GRASS_LIGHT);
    dot(ctx, px + 1, py, GRASS_MID);
  } else if (slot < 26) {
    // 花（茎と花びら）
    const c = FLOWERS[h % FLOWERS.length];
    dot(ctx, px, py + 1, GRASS_DARK);
    dot(ctx, px, py, c);
    dot(ctx, px - 1, py - 1, c);
    dot(ctx, px + 1, py - 1, c);
    dot(ctx, px, py - 1, "#f2c14e");
    dot(ctx, px, py - 2, c);
  } else if (slot < 30) {
    // 小石
    dot(ctx, px, py, "#9a9488", 3, 1);
    dot(ctx, px + 1, py - 1, "#c2bcae", 2, 1);
    dot(ctx, px, py + 1, "#5e5a52", 3, 1);
  } else {
    // 落ち葉や小さな点々
    dot(ctx, px, py, GRASS_LIGHT);
    dot(ctx, px + 2, py + 1, GRASS_LIGHT);
    dot(ctx, px + 1, py + 2, GRASS_DARK);
  }
}

/** タイルの描画のあとに呼ぶ。カメラに映る範囲だけを処理する。 */
export function renderGroundDecor(ctx: CanvasRenderingContext2D, map: TileMap, camera: Camera): void {
  const { tileWidth: s, tileHeight } = map.data;
  if (s !== 16 || tileHeight !== 16 || !map.data.tileArt) {
    return;
  }
  const startX = Math.max(0, Math.floor(camera.x / s));
  const startY = Math.max(0, Math.floor(camera.y / s));
  const endX = Math.min(map.data.width - 1, Math.floor((camera.x + camera.viewportWidth) / s));
  const endY = Math.min(map.data.height - 1, Math.floor((camera.y + camera.viewportHeight) / s));
  for (let ty = startY; ty <= endY; ty++) {
    for (let tx = startX; tx <= endX; tx++) {
      const kind = kindAt(map, tx, ty);
      if (kind === "other") {
        continue;
      }
      const ox = tx * s - camera.x;
      const oy = ty * s - camera.y;
      if (kind === "grass") {
        grassDecor(ctx, ox, oy, s, tx, ty);
        if (kindAt(map, tx, ty - 1) === "tree") {
          treeShadow(ctx, ox, oy, s, tx, ty);
        }
        continue;
      }
      if (kind !== "path" && kind !== "water") {
        continue;
      }
      SIDES.forEach((side, index) => {
        const n = kindAt(map, tx + side.dx, ty + side.dy);
        if (kind === "path" && n === "grass") {
          pathEdge(ctx, ox, oy, s, tx, ty, index);
        } else if (kind === "water" && (n === "grass" || n === "path")) {
          waterEdge(ctx, ox, oy, s, tx, ty, index);
        }
      });
    }
  }
}
