import { hashCell, shadeColor } from "../color-utils";

/**
 * マップタイル用のドット絵パターン。`docs/decisions.md`（ドット絵のクオリティを
 * 高める方針）に基づき、単色べた塗り＋斑点模様（`tile-map-renderer.ts`の
 * 汎用テクスチャ）の次の段階として、草・水・道・木という代表的な地形カテゴリに
 * ジャンルでよく使われる技法（草のディザリング、水の波模様、道の踏み跡、
 * 木の樹冠＋幹）を適用する。既存の特定作品のタイルセットは参照していない。
 */
export type TilePatternKind = "grass" | "water" | "path" | "treeCanopy" | "flagstone" | "brick" | "sand" | "snow" | "plank" | "cloud" | "roof" | "crate" | "pillar" | "machine" | "pipe" | "carpet" | "crystal" | "void";

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

  // 石畳: 段ごとに半分ずらした敷石。縁が暗く、左上が明るい。
  flagstone: (ramp, row, col, variant) => {
    const band = Math.floor(row / 5);
    const localX = (col + (band % 2) * 4 + (variant % 2) * 2) % 8;
    const localY = row % 5;
    if (localY === 4 || localX === 7) return ramp[1];
    if (localY === 0 || localX === 0) return ramp[3];
    const h = hashCell(col + variant * 5, row + band * 3);
    return h % 9 === 0 ? ramp[1] : h % 7 === 0 ? ramp[3] : ramp[2];
  },
  // 煉瓦・切り石の壁: 段ごとに半分ずらした長方形。継ぎ目が暗く、上の縁が明るい。
  brick: (ramp, row, col, variant) => {
    const band = Math.floor(row / 4);
    const localX = (col + (band % 2) * 4) % 8;
    const localY = row % 4;
    if (localY === 3 || localX === 7) return ramp[0];
    if (localY === 0) return ramp[3];
    const h = hashCell(col + variant * 3, row + band);
    return h % 8 === 0 ? ramp[1] : h % 11 === 0 ? ramp[3] : ramp[2];
  },
  // 砂: 風のさざ波の斜めの筋と、細かな粒。
  sand: (ramp, row, col, variant) => {
    const wave = (col + row * 2 + variant * 3) % 9;
    const h = hashCell(col + variant * 11, row + variant * 3);
    if (wave < 2) return ramp[3];
    if (wave === 5) return ramp[1];
    if (h % 23 === 0) return ramp[4];
    if (h % 17 === 0) return ramp[1];
    return ramp[2];
  },
  // 雪・氷: ほぼ白で、やわらかな影のかたまりと、まれなきらめき。
  snow: (ramp, row, col, variant) => {
    const blotch = hashCell(Math.floor(col / 3) + variant * 3, Math.floor(row / 3)) % 6;
    const h = hashCell(col + variant * 7, row + variant * 13);
    if (h % 37 === 0) return ramp[4];
    if (blotch === 0) return ramp[1];
    if (blotch === 1) return ramp[3];
    return ramp[2];
  },
  // 板張り: 縦の板。継ぎ目・木目・板の端の継ぎ目。
  plank: (ramp, row, col, variant) => {
    const localX = col % 4;
    if (localX === 3) return ramp[1];
    if ((row + (hashCell(Math.floor(col / 4), variant) % 16)) % 16 === 0) return ramp[1];
    const h = hashCell(col + variant * 9, row);
    if (localX === 0 && h % 3 !== 0) return ramp[3];
    return h % 7 === 0 ? ramp[3] : h % 11 === 0 ? ramp[1] : ramp[2];
  },
  // 屋根: 段ごとに半分ずらした、丸みのある瓦。段の下の縁が暗く、上が明るい。
  roof: (ramp, row, col, variant) => {
    const band = Math.floor(row / 4);
    const localY = row % 4;
    const localX = (col + (band % 2) * 4) % 8;
    // 瓦の下の縁は、真ん中がふくらんだ曲線（両端が1段高い）
    const edge = localX === 0 || localX === 7 ? 2 : 3;
    if (localY === edge) return ramp[0];
    if (localY > edge) return ramp[1];
    if (localY === 0) return ramp[3];
    const h = hashCell(col + variant * 7, row + band * 5);
    return h % 9 === 0 ? ramp[1] : h % 13 === 0 ? ramp[3] : ramp[2];
  },
  // 木箱: 外枠と、斜めの補強板。
  crate: (ramp, row, col, variant) => {
    if (row === 0 || col === 0 || row === TILE_ART_SIZE - 1 || col === TILE_ART_SIZE - 1) return ramp[0];
    if (row === 1 || col === 1) return ramp[3];
    if (row === TILE_ART_SIZE - 2 || col === TILE_ART_SIZE - 2) return ramp[1];
    if (row === col || row + col === TILE_ART_SIZE - 1) return ramp[1];
    const h = hashCell(col + variant * 3, row * 5);
    return h % 7 === 0 ? ramp[3] : ramp[2];
  },
  // 柱: 縦の溝（フルート）。左が明るく右が暗い丸みと、上下の石の継ぎ目。
  pillar: (ramp, row, col, variant) => {
    if (row === 0 || row === TILE_ART_SIZE - 1) return ramp[0];
    if (row === 1 || row === TILE_ART_SIZE - 2) return ramp[1];
    const x = col % 4;
    const round = col < 5 ? 3 : col > 10 ? 1 : 2;
    if (x === 3) return ramp[Math.max(0, round - 1)];
    const h = hashCell(col + variant * 5, row);
    return h % 17 === 0 ? ramp[Math.max(0, round - 1)] : ramp[round + (x === 0 ? 1 : 0) > 4 ? 4 : round + (x === 0 ? 1 : 0)];
  },
  // 機械: 金属の板に、四隅のリベット、操作盤の小さな光。
  machine: (ramp, row, col, variant) => {
    const edge = row === 0 || col === 0 || row === TILE_ART_SIZE - 1 || col === TILE_ART_SIZE - 1;
    if (edge) return ramp[0];
    if (row === 1 || col === 1) return ramp[3];
    if (row === TILE_ART_SIZE - 2 || col === TILE_ART_SIZE - 2) return ramp[1];
    if ((row === 3 || row === TILE_ART_SIZE - 4) && (col === 3 || col === TILE_ART_SIZE - 4)) return ramp[4];
    if (row >= 6 && row <= 9 && col >= 5 && col <= 10) {
      const lamp = (col + variant) % 3 === 0 && row === 7;
      return lamp ? ramp[4] : ramp[0];
    }
    return hashCell(col + variant * 3, row) % 9 === 0 ? ramp[3] : ramp[2];
  },
  // 管・配線: 横に走る太い管。上が明るく、下が暗い丸み。継ぎ目の輪。
  pipe: (ramp, row, col, variant) => {
    const band = row % 8;
    if (band === 0) return ramp[0];
    if (col % 8 === (variant * 3) % 8) return ramp[1];
    if (band === 1) return ramp[4];
    if (band === 2) return ramp[3];
    if (band <= 5) return ramp[2];
    return band === 6 ? ramp[1] : ramp[0];
  },
  // 絨毯: ふちどりと、菱形の織り模様。
  carpet: (ramp, row, col, variant) => {
    if (row === 0 || row === TILE_ART_SIZE - 1) return ramp[3];
    if (row === 1 || row === TILE_ART_SIZE - 2) return ramp[1];
    const dx = Math.abs(col - CENTER), dy = Math.abs(row - CENTER);
    if (dx + dy === 5) return ramp[3];
    if (dx + dy < 3) return ramp[4];
    const h = hashCell(col + variant * 5, row + variant);
    return h % 8 === 0 ? ramp[1] : ramp[2];
  },
  // 水晶・光る石: 面ごとに明るさが違う、ひし形のかけら。
  crystal: (ramp, row, col, variant) => {
    const cx = 4 + (variant % 2) * 4 + ((row >> 3) % 2) * 4, cy = 4 + (variant >> 1) * 3 + (row >> 3) * 0;
    const local = { x: (col + 16 - cx) % 8 - 4, y: (row + 16 - cy) % 8 - 4 };
    const d = Math.abs(local.x) + Math.abs(local.y);
    if (d === 4) return ramp[0];
    if (d > 4) return hashCell(col, row + variant) % 5 === 0 ? ramp[1] : ramp[2];
    if (d === 0) return ramp[4];
    return local.x < 0 ? (local.y < 0 ? ramp[4] : ramp[3]) : (local.y < 0 ? ramp[3] : ramp[2]);
  },
  // 虚（何もない暗がり）: ほぼ黒で、ごくまれに遠い光。
  void: (ramp, row, col, variant) => {
    const h = hashCell(col + variant * 13, row + variant * 7);
    if (h % 61 === 0) return ramp[4];
    if (h % 23 === 0) return ramp[3];
    return h % 5 === 0 ? ramp[1] : ramp[0];
  },
  // 雲・霧: やわらかなふくらみ。
  cloud: (ramp, row, col, variant) => {
    const blotch = hashCell(Math.floor(col / 4) + variant, Math.floor(row / 4)) % 4;
    const h = hashCell(col + variant * 5, row + variant * 3);
    if (h % 19 === 0) return ramp[4];
    if (blotch === 0) return ramp[3];
    if (blotch === 3) return ramp[1];
    return ramp[2];
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

/**
 * 「地図のタイルの色」を基本色にして、模様だけを重ねる指定（`tileArt` の値を `tint:<模様>` にする）。
 * 例: `tint:flagstone`。地方ごとに色が違う石畳・壁・砂・雪などを、同じ模様の作りで描くための仕組み。
 */
export const TINT_PREFIX = "tint:";

export function tintedSpec(pattern: TilePatternKind, base: string): TileArtSpec {
  return { base, accentLight: shadeColor(base, 0.22), accentDark: shadeColor(base, -0.28), pattern };
}
