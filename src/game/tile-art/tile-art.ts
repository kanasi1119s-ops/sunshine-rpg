import { hashCell, shadeColor } from "../color-utils";

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

/** 1タイルぶんの描画関数。`ramp`は暗い→明るいの5階調、`variant`は同じ地形の見た目の揺らぎ（0〜3）。 */
type PatternFn = (ramp: string[], row: number, col: number, variant: number) => string | null;

const CENTER = (TILE_ART_SIZE - 1) / 2;
export const TILE_VARIANTS = 4;

/** 基本色・明色・暗色から、暗い→明るいの5階調（SFC後期風に多めの階調で陰影を作る）を作る。 */
function buildRamp(spec: TileArtSpec): string[] {
  return [
    shadeColor(spec.accentDark, -0.35),
    spec.accentDark,
    spec.base,
    spec.accentLight,
    shadeColor(spec.accentLight, 0.35),
  ];
}

function wrap(n: number): number {
  return ((n % TILE_ART_SIZE) + TILE_ART_SIZE) % TILE_ART_SIZE;
}

/** 草の房（「ハの字」に伸びる葉先）の、タイル内での位置。 */
function tuftAt(row: number, col: number, variant: number): number {
  for (let n = 0; n < 3; n++) {
    const tx = hashCell(n + variant * 7, 11) % TILE_ART_SIZE;
    const ty = hashCell(n + variant * 7, 23) % TILE_ART_SIZE;
    if (wrap(col - tx) === 0 && wrap(row - ty) === 0) return 3; // 根もと（暗）
    if (wrap(col - tx) === 0 && wrap(row - ty) === TILE_ART_SIZE - 1) return 4; // 中央の葉先
    if (wrap(col - tx + 1) === 0 && wrap(row - ty) === TILE_ART_SIZE - 1) return 3;
    if (wrap(col - tx - 1) === 0 && wrap(row - ty) === TILE_ART_SIZE - 1) return 4;
  }
  return 0;
}

const PATTERNS: Record<TilePatternKind, PatternFn> = {
  // 草: 5階調のまだら＋ハの字の葉先。同じタイルが並んでも単調にならないよう4種の揺らぎを持つ。
  grass: (ramp, row, col, variant) => {
    const h = hashCell(col + variant * 31, row + variant * 17);
    const tuft = tuftAt(row, col, variant);
    if (tuft === 4) return ramp[4];
    if (tuft === 3) return ramp[3];
    // 低周波のまだら（2×2ドット単位）で明暗の広がりを作る
    const blotch = hashCell(Math.floor(col / 3) + variant * 5, Math.floor(row / 3)) % 5;
    let k = blotch === 0 ? 3 : blotch === 4 ? 1 : 2;
    if (h % 9 === 0) k = Math.min(4, k + 1);
    else if (h % 13 === 0) k = Math.max(0, k - 1);
    return ramp[k];
  },
  // 水: うろこ状の波（2ドット単位の斜め格子）と、まれな白い輝き。
  water: (ramp, row, col, variant) => {
    const h = hashCell(col + variant * 13, row + variant * 29);
    const scale = (Math.floor(col / 2) + Math.floor(row / 2) + (Math.floor(row / 4) % 2) * 1) % 4;
    let k = scale === 0 ? 3 : scale === 2 ? 1 : 2;
    if (h % 31 === 0) k = 4;
    else if (h % 17 === 0) k = Math.max(0, k - 1);
    return ramp[k];
  },
  // 道: 踏み固めた土。小石（明るい上面＋暗い下面）を散らす。
  path: (ramp, row, col, variant) => {
    const h = hashCell(col + variant * 19, row + variant * 7);
    const stoneX = hashCell(variant, 5) % 12;
    const stoneY = hashCell(variant, 9) % 12;
    if (row === stoneY && col >= stoneX && col <= stoneX + 2) return ramp[4];
    if (row === stoneY + 1 && col >= stoneX && col <= stoneX + 2) return ramp[3];
    if (row === stoneY + 2 && col >= stoneX && col <= stoneX + 2) return ramp[0];
    if (h % 11 === 0) return ramp[1];
    if (h % 17 === 0) return ramp[3];
    return h % 3 === 0 ? ramp[2] : ramp[2];
  },
  // 木: 小さな葉のかたまり4つを重ねた樹冠。塊ごとに左上が明るく右下が暗い。全体を暗い縁で囲み、下に幹。
  treeCanopy: (ramp, row, col, variant) => {
    const blobs: [number, number, number][] = [
      [CENTER - 3 + (variant % 2), 5, 4.4],
      [CENTER + 3, 6 + (variant % 3) - 1, 4.2],
      [CENTER - 1, 8, 4.8],
      [CENTER + 4 - (variant % 2), 9, 3.6],
    ];
    // 幹
    if (row >= TILE_ART_SIZE - 3 && Math.abs(col - CENTER) <= 1.5) {
      return col < CENTER ? ramp[1] : ramp[0];
    }
    const inAny = (r: number, c: number): boolean => blobs.some(([bx, by, br]) => (c - bx) ** 2 + (r - by) ** 2 <= br * br);
    if (!inAny(row, col)) {
      const edge = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dr, dc]) => inAny(row + dr, col + dc));
      return edge ? ramp[0] : null;
    }
    let best = -9;
    let d2Best = 1;
    for (const [bx, by, br] of blobs) {
      const d2 = ((col - bx) ** 2 + (row - by) ** 2) / (br * br);
      if (d2 <= 1) {
        const light = (-(col - bx) * 0.6 - (row - by) * 0.8) / br;
        if (light > best) {
          best = light;
          d2Best = d2;
        }
      }
    }
    let k = best > 0.45 ? 4 : best > 0.05 ? 3 : best > -0.4 ? 2 : 1;
    if (d2Best > 0.8 && best < 0) k = 1;
    if (hashCell(col + variant, row) % 9 === 0) k = Math.max(1, k - 1);
    return ramp[k];
  },
};

/** 指定したタイル模様の、実際に描く色の一覧を作る（タイル座標だけで決まり、時刻に依存しない）。 */
export function buildTileArtCells(spec: TileArtSpec, variant = 0): TileArtCell[] {
  const fn = PATTERNS[spec.pattern];
  const ramp = buildRamp(spec);
  const cells: TileArtCell[] = [];
  for (let row = 0; row < TILE_ART_SIZE; row++) {
    for (let col = 0; col < TILE_ART_SIZE; col++) {
      const color = fn(ramp, row, col, variant);
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
  grass: { base: "#3f8f2c", accentLight: "#6fc236", accentDark: "#25671f", pattern: "grass" },
  water: { base: "#1a6d8c", accentLight: "#3fa5b0", accentDark: "#0f4468", pattern: "water" },
  path: { base: "#b3853f", accentLight: "#d8b060", accentDark: "#85552a", pattern: "path" },
  treeCanopy: { base: "#2b8022", accentLight: "#5fbb31", accentDark: "#185019", pattern: "treeCanopy" },
};
