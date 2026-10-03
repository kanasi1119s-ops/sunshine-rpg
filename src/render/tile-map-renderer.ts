import { getTileId, type TileMap } from "../game/map/tile-map";
import type { Camera } from "./camera";
import { renderGroundDecor } from "./ground-decor";
import { drawDungeonTile } from "./dungeon-tiles";
import { drawBuildingTile } from "./building-tiles";
import { hashCell, shadeColor } from "../game/color-utils";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import { buildTileArtCells, TILE_ART, TILE_ART_SIZE, TILE_VARIANTS, TINT_PREFIX, tintedSpec, type TilePatternKind, type TileArtCell } from "../game/tile-art/tile-art";

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
/** 地形カテゴリ → 128×128の地形テクスチャ（`sprite-data.generated.ts`）。草だけは2種を128マスごとに切り替えて繰り返しを減らす。 */
const TERRAIN_TEXTURE: Record<string, string[]> = {
  grass: ["terrain:grass-a", "terrain:grass-b"],
  water: ["terrain:water"],
  path: ["terrain:dirt"],
  treeCanopy: ["terrain:forest"],
};
const TEXTURE_SIZE = 128;

/** 大きな地形テクスチャがあれば、そのタイル位置にあたる16×16の窓を切り出して描く（隣のタイルと絵がつながる）。 */
function drawTerrainTexture(
  ctx: CanvasRenderingContext2D,
  categoryKey: string,
  screenX: number,
  screenY: number,
  tileWidth: number,
  tileHeight: number,
  tileX: number,
  tileY: number,
): boolean {
  const keys = TERRAIN_TEXTURE[categoryKey];
  if (!keys) {
    return false;
  }
  const perSide = TEXTURE_SIZE / TILE_ART_SIZE;
  const block = hashCell(Math.floor(tileX / perSide), Math.floor(tileY / perSide));
  const canvas = getSpriteCanvas(keys[block % keys.length], SPRITE_DATA);
  if (!canvas) {
    return false;
  }
  const sx = (((tileX * TILE_ART_SIZE) % TEXTURE_SIZE) + TEXTURE_SIZE) % TEXTURE_SIZE;
  const sy = (((tileY * TILE_ART_SIZE) % TEXTURE_SIZE) + TEXTURE_SIZE) % TEXTURE_SIZE;
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, sx, sy, TILE_ART_SIZE, TILE_ART_SIZE, screenX, screenY, tileWidth, tileHeight);
  return true;
}

const cellCache = new Map<string, TileArtCell[]>();

/** 地形カテゴリ×見た目の揺らぎごとに、描画データを一度だけ作って使い回す。 */
function cellsFor(categoryKey: string, variant: number, tileColor: string): TileArtCell[] | null {
  // `tint:<模様>` は、そのタイルの色を基本色にして模様を重ねる。
  const spec = categoryKey.startsWith(TINT_PREFIX)
    ? tintedSpec(categoryKey.slice(TINT_PREFIX.length) as TilePatternKind, tileColor)
    : TILE_ART[categoryKey];
  if (!spec) {
    return null;
  }
  const key = categoryKey.startsWith(TINT_PREFIX) ? `${categoryKey}:${tileColor}:${variant}` : `${categoryKey}:${variant}`;
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
  tileColor: string,
): boolean {
  if (drawTerrainTexture(ctx, categoryKey, screenX, screenY, tileWidth, tileHeight, tileX, tileY)) {
    return true;
  }
  const cells = cellsFor(categoryKey, hashCell(tileX, tileY) % TILE_VARIANTS, tileColor);
  if (!cells) {
    return false;
  }
  // ブラウザでは、模様を一度だけ小さなキャンバスに描いておき、画像として貼る（1タイルにつき256回の塗りを避ける）。
  const cached = tileCanvasFor(categoryKey, hashCell(tileX, tileY) % TILE_VARIANTS, tileColor, cells);
  if (cached) {
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(cached, screenX, screenY, tileWidth, tileHeight);
    return true;
  }
  const cellWidth = tileWidth / TILE_ART_SIZE;
  const cellHeight = tileHeight / TILE_ART_SIZE;
  for (const cell of cells) {
    ctx.fillStyle = cell.color;
    ctx.fillRect(screenX + cell.col * cellWidth, screenY + cell.row * cellHeight, cellWidth, cellHeight);
  }
  return true;
}

const tileCanvasCache = new Map<string, HTMLCanvasElement>();

/** 模様の描画データから、16×16の小さなキャンバスを作って使い回す。ブラウザ以外（自動テスト）では null。 */
function tileCanvasFor(categoryKey: string, variant: number, tileColor: string, cells: TileArtCell[]): HTMLCanvasElement | null {
  if (typeof document === "undefined") {
    return null;
  }
  const key = categoryKey.startsWith(TINT_PREFIX) ? `${categoryKey}:${tileColor}:${variant}` : `${categoryKey}:${variant}`;
  let canvas = tileCanvasCache.get(key);
  if (!canvas) {
    canvas = document.createElement("canvas");
    canvas.width = TILE_ART_SIZE;
    canvas.height = TILE_ART_SIZE;
    const c = canvas.getContext("2d");
    if (!c) {
      return null;
    }
    for (const cell of cells) {
      c.fillStyle = cell.color;
      c.fillRect(cell.col, cell.row, 1, 1);
    }
    tileCanvasCache.set(key, canvas);
  }
  return canvas;
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
        if (map.data.building && drawBuildingTile(ctx, map, tileId, tileX, tileY, screenX, screenY)) {
          continue;
        }
        if (map.data.theme && drawDungeonTile(ctx, map, tileId, tileX, tileY, screenX, screenY)) {
          continue;
        }
        const artKey = map.data.tileArt?.[tileId];
        if (artKey && drawTileArt(ctx, artKey, screenX, screenY, tileWidth, tileHeight, tileX, tileY, color)) {
          continue;
        }
        drawTileTexture(ctx, color, screenX, screenY, tileWidth, tileHeight, tileX, tileY);
      }
    }
  }
  renderGroundDecor(ctx, map, camera);
}
