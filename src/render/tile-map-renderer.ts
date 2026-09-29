import { getTileId, type TileMap } from "../game/map/tile-map";
import type { Camera } from "./camera";
import { hashCell, shadeColor } from "../game/color-utils";
import { buildTileArtCells, TILE_ART, TILE_ART_SIZE, TILE_VARIANTS, type TileArtCell } from "../game/tile-art/tile-art";

/**
 * 単色べた塗りだと平坦に見えるため、タイルごとに決まった模様（隅の陰影＋
 * 斑点2つ）を重ねて、簡易的な質感を出す。`hashCell`はタイル座標だけから
 * 決まるので、毎フレーム同じ模様になり（ちらつかない）、新しいタイル絵を
 * 増やさなくても既存のマップ全体の見た目を底上げできる。
 */
function drawTileTexture(
  ctx: CanvasRenderingContext2D,
  color: string,
  screenX: number,
  screenY: number,
  tileWidth: number,
  tileHeight: number,
  tileX: number,
  tileY: number,
): void {
  ctx.fillStyle = color;
  ctx.fillRect(screenX, screenY, tileWidth, tileHeight);

  // 左上を少し明るく、右下を少し暗くして、立体感を出す。
  const bevel = Math.max(1, Math.floor(Math.min(tileWidth, tileHeight) / 8));
  ctx.fillStyle = shadeColor(color, 0.12);
  ctx.fillRect(screenX, screenY, tileWidth, bevel);
  ctx.fillRect(screenX, screenY, bevel, tileHeight);
  ctx.fillStyle = shadeColor(color, -0.12);
  ctx.fillRect(screenX, screenY + tileHeight - bevel, tileWidth, bevel);
  ctx.fillRect(screenX + tileWidth - bevel, screenY, bevel, tileHeight);

  // タイル固有の斑点を2つ置いて、単調な繰り返し感を減らす。
  const hash = hashCell(tileX, tileY);
  const speckleSize = Math.max(1, Math.floor(Math.min(tileWidth, tileHeight) / 6));
  const maxOffsetX = Math.max(1, tileWidth - speckleSize);
  const maxOffsetY = Math.max(1, tileHeight - speckleSize);
  ctx.fillStyle = shadeColor(color, ((hash & 0xff) / 255) * 0.16 - 0.08);
  ctx.fillRect(
    screenX + ((hash >>> 8) % maxOffsetX),
    screenY + ((hash >>> 16) % maxOffsetY),
    speckleSize,
    speckleSize,
  );
  ctx.fillStyle = shadeColor(color, (((hash >>> 24) & 0xff) / 255) * 0.16 - 0.08);
  ctx.fillRect(
    screenX + ((hash >>> 4) % maxOffsetX),
    screenY + ((hash >>> 20) % maxOffsetY),
    speckleSize,
    speckleSize,
  );
}

/**
 * `tileArt`に地形カテゴリの指定があれば、ドット絵パターンで描く。
 * 描けた場合はtrue、カテゴリが未登録の場合はfalse（呼び出し側は
 * `drawTileTexture`にフォールバックする）。
 */
const cellCache = new Map<string, TileArtCell[]>();

/** 地形カテゴリ×見た目の揺らぎごとに、描画データを一度だけ作って使い回す。 */
function cellsFor(categoryKey: string, variant: number): TileArtCell[] | null {
  const spec = TILE_ART[categoryKey];
  if (!spec) {
    return null;
  }
  const key = `${categoryKey}:${variant}`;
  let cells = cellCache.get(key);
  if (!cells) {
    cells = buildTileArtCells(spec, variant);
    cellCache.set(key, cells);
  }
  return cells;
}

function drawTileArt(
  ctx: CanvasRenderingContext2D,
  categoryKey: string,
  screenX: number,
  screenY: number,
  tileWidth: number,
  tileHeight: number,
  tileX: number,
  tileY: number,
): boolean {
  const cells = cellsFor(categoryKey, hashCell(tileX, tileY) % TILE_VARIANTS);
  if (!cells) {
    return false;
  }
  const cellWidth = tileWidth / TILE_ART_SIZE;
  const cellHeight = tileHeight / TILE_ART_SIZE;
  for (const cell of cells) {
    ctx.fillStyle = cell.color;
    ctx.fillRect(screenX + cell.col * cellWidth, screenY + cell.row * cellHeight, cellWidth, cellHeight);
  }
  return true;
}

/** カメラに映る範囲のタイルだけを描画する。 */
export function renderTileMap(
  ctx: CanvasRenderingContext2D,
  map: TileMap,
  camera: Camera,
): void {
  const { tileWidth, tileHeight } = map.data;

  const startX = Math.max(0, Math.floor(camera.x / tileWidth));
  const startY = Math.max(0, Math.floor(camera.y / tileHeight));
  const endX = Math.min(
    map.data.width - 1,
    Math.floor((camera.x + camera.viewportWidth) / tileWidth),
  );
  const endY = Math.min(
    map.data.height - 1,
    Math.floor((camera.y + camera.viewportHeight) / tileHeight),
  );

  for (let layerIndex = 0; layerIndex < map.data.layers.length; layerIndex++) {
    for (let tileY = startY; tileY <= endY; tileY++) {
      for (let tileX = startX; tileX <= endX; tileX++) {
        const tileId = getTileId(map, layerIndex, tileX, tileY);
        if (tileId === 0) {
          continue;
        }
        const color = map.data.tileColors[tileId];
        if (!color) {
          continue;
        }
        const screenX = tileX * tileWidth - camera.x;
        const screenY = tileY * tileHeight - camera.y;
        const artKey = map.data.tileArt?.[tileId];
        if (artKey && drawTileArt(ctx, artKey, screenX, screenY, tileWidth, tileHeight, tileX, tileY)) {
          continue;
        }
        drawTileTexture(ctx, color, screenX, screenY, tileWidth, tileHeight, tileX, tileY);
      }
    }
  }
}
