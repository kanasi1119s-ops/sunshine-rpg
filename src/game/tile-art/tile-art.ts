import { hashCell } from "../color-utils";

/**
 * マップタイル用のドット絵パターン。`docs/decisions.md`（ドット絵のクオリティを
 * 高める方針）に基づき、単色べた塗り＋斑点模様（`tile-map-renderer.ts`の
 * 汎用テクスチャ）の次の段階として、草・水・道・木という代表的な地形カテゴリに
 * ジャンルでよく使われる技法（草のディザリング、水の波模様、道の踏み跡、
 * 木の樹冠＋幹）を適用する。既存の特定作品のタイルセットは参照していない。
 */
export type TilePatternKind = "grass" | "water" | "path" | "treeCanopy";

export interface TileArtSpec {
  base: string;
  accentLight: string;
  accentDark: string;
  pattern: TilePatternKind;
}

/** 1タイル＝16×16ドット（実際のタイルサイズ`tileWidth`/`tileHeight`と同じ）。 */
export const TILE_ART_SIZE = 16;

export interface TileArtCell {
  row: number;
  col: number;
  color: string;
}

type PatternFn = (spec: TileArtSpec, row: number, col: number) => string | null;

const CENTER = (TILE_ART_SIZE - 1) / 2;

const PATTERNS: Record<TilePatternKind, PatternFn> = {
  // 草: 散らばった葉先の模様で、単色の草地よりも茂み感を出す。
  grass: (spec, row, col) => {
    const h = hashCell(col, row);
    if (h % 7 === 0) return spec.accentLight;
    if (h % 11 === 0) return spec.accentDark;
    return spec.base;
  },
  // 水: 横方向の帯で緩やかな波を表し、まれに明るい輝きを置く。
  water: (spec, row, col) => {
    const band = Math.floor((row + Math.floor(col / 5)) / 2) % 2;
    const base = band === 0 ? spec.base : spec.accentLight;
    const h = hashCell(col, row);
    if (h % 29 === 0) return spec.accentDark;
    return base;
  },
  // 道: 踏み固められた土のイメージで、小石・踏み跡を散らす。
  path: (spec, row, col) => {
    const h = hashCell(col, row);
    if (h % 13 === 0) return spec.accentDark;
    if (h % 19 === 0) return spec.accentLight;
    return spec.base;
  },
  // 木: 円形の樹冠（左上を光源にした明暗）＋下中央にのぞく幹。
  treeCanopy: (spec, row, col) => {
    const radius = TILE_ART_SIZE / 2 - 0.5;
    if (row >= TILE_ART_SIZE - 3 && Math.abs(col - CENTER) <= 1) {
      return spec.accentDark;
    }
    const dx = col - CENTER;
    const dy = row - CENTER;
    const dist = Math.sqrt(dx * dx + dy * dy);
    if (dist > radius) {
      return null;
    }
    if (dx + dy < -radius * 0.6) {
      return spec.accentLight;
    }
    if (dist > radius * 0.7) {
      return spec.accentDark;
    }
    return spec.base;
  },
};

/** 指定したタイル模様の、実際に描く色の一覧を作る（タイル座標だけで決まり、時刻に依存しない）。 */
export function buildTileArtCells(spec: TileArtSpec): TileArtCell[] {
  const fn = PATTERNS[spec.pattern];
  const cells: TileArtCell[] = [];
  for (let row = 0; row < TILE_ART_SIZE; row++) {
    for (let col = 0; col < TILE_ART_SIZE; col++) {
      const color = fn(spec, row, col);
      if (color) {
        cells.push({ row, col, color });
      }
    }
  }
  return cells;
}

/**
 * 地形カテゴリ名（`TileMapData.tileArt`の値）をキーにした共通パレット。
 * すべてのマップで同じ配色を使うことで、世界としての統一感を出す。
 */
export const TILE_ART: Record<string, TileArtSpec> = {
  grass: { base: "#4a8a42", accentLight: "#6bac57", accentDark: "#396b34", pattern: "grass" },
  water: { base: "#3a6ea5", accentLight: "#5a8fc4", accentDark: "#2c5484", pattern: "water" },
  path: { base: "#c2a06a", accentLight: "#d6b784", accentDark: "#a08650", pattern: "path" },
  treeCanopy: { base: "#2b6b3f", accentLight: "#4a8f57", accentDark: "#1c4a2b", pattern: "treeCanopy" },
};
