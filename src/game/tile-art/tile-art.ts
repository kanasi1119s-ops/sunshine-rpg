import { hashCell, shadeColor } from "../color-utils";

/**
 * マップタイル用のドット絵パターン。`docs/decisions.md`（ドット絵のクオリティを
 * 高める方針）に基づき、単色べた塗り＋斑点模様（`tile-map-renderer.ts`の
 * 汎用テクスチャ）の次の段階として、草・水・道・木という代表的な地形カテゴリに
 * ジャンルでよく使われる技法（草のディザリング、水の波模様、道の踏み跡、
 * 木の樹冠＋幹）を適用する。既存の特定作品のタイルセットは参照していない。
 */
export type TilePatternKind = "grass" | "water" | "path" | "treeCanopy" | "flagstone" | "brick" | "sand" | "snow" | "plank" | "cloud" | "roof" | "crate" | "pillar" | "machine" | "pipe" | "carpet" | "crystal" | "void" | "gate" | "mural" | "bed" | "rift" | "mountain" | "worldforest" | "hills";

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

  // 石畳: 段ごとに石の幅が不ぞろいな敷石。目地は暗く、石の左上の縁だけ明るく、右下の縁は少し暗い。
  // 石ごとの色の差はまれにだけ付け（ざらざらした斑点は付けない）、ときどきひびを入れる。
  flagstone: (ramp, row, col, variant) => {
    const bandH = [5, 5, 6];
    const starts = [0, 5, 10];
    const band = row < 5 ? 0 : row < 10 ? 1 : 2;
    const localY = row - starts[band];
    // この段の石の境目の位置（タイルの外へも続けて、隣のタイルと切れ目なくつなぐ）
    let x0 = -(hashCell(band + variant * 2, 5) % 5);
    let w = 4 + (hashCell(x0 + band * 7, variant) % 4);
    while (x0 + w <= col) {
      x0 += w;
      w = 4 + (hashCell(x0 + band * 7, variant) % 4);
    }
    const localX = col - x0;
    if (localY === 0 || localX === 0) return ramp[1];
    const tone = hashCell(x0 * 3 + band, variant + 7) % 9;
    const crack = tone === 0 && localX === Math.floor(w / 2) && localY > 1 && localY < bandH[band] - 1;
    if (crack) return ramp[1];
    if (localX === 1 || localY === 1) return ramp[3];
    if (localX === w - 1 || localY === bandH[band] - 1) return ramp[1];
    return tone === 1 ? ramp[3] : tone === 2 ? ramp[1] : ramp[2];
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
  // 雪・氷: ほぼ白。まるい吹きだまりのくぼみ（淡い影）を2つ置き、縁は市松でなじませる。まれに小さなきらめき。
  snow: (ramp, row, col, variant) => {
    const soft = shadeColor(ramp[2], -0.07);
    const h = hashCell(col + variant * 7, row + variant * 13);
    if (h % 53 === 0) return ramp[4];
    for (let n = 0; n < 2; n++) {
      const cx = hashCell(n + variant * 5, 31) % TILE_ART_SIZE;
      const cy = hashCell(n + variant * 5, 47) % TILE_ART_SIZE;
      const rx = 3 + (hashCell(n, variant + 3) % 3);
      const ry = 2 + (hashCell(n + 9, variant) % 2);
      // タイルの端をまたぐ（左右・上下でつながる）ように、距離は回り込みで測る
      const dx = Math.min(Math.abs(col - cx), TILE_ART_SIZE - Math.abs(col - cx)) / rx;
      const dy = Math.min(Math.abs(row - cy), TILE_ART_SIZE - Math.abs(row - cy)) / ry;
      const d = dx * dx + dy * dy;
      if (d < 0.5) return soft;
      if (d < 1 && (col + row) % 2 === 0) return soft;
    }
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
  // 扉: 縦に板を並べ、四辺に金具のふちどり。中央に合わせ目と取っ手。
  gate: (ramp, row, col, variant) => {
    const last = TILE_ART_SIZE - 1;
    if (row === 0 || col === 0) return ramp[4];
    if (row === last || col === last) return ramp[0];
    if (row === 1 || row === last - 1 || col === 1 || col === last - 1) return ramp[1];
    if (col === 7 || col === 8) return ramp[0];
    if ((col === 5 || col === 10) && row >= 6 && row <= 9) return ramp[4];
    const h = hashCell(col + variant * 11, row);
    return col % 4 === 2 ? ramp[3] : h % 9 === 0 ? ramp[1] : ramp[2];
  },
  // 壁画: 暗い下地に、ふちの帯と、線で描いた渦（意味のある絵ではなく模様）。
  mural: (ramp, row, col, variant) => {
    if (row <= 1 || row >= TILE_ART_SIZE - 2) return row % 2 === 0 ? ramp[3] : ramp[1];
    const dx = col - CENTER, dy = row - CENTER;
    const ring = Math.round(Math.hypot(dx, dy * 1.2) + (variant % 2) * 0.5);
    if (ring === 3 || ring === 6) return ramp[4];
    if (ring === 4) return ramp[3];
    return hashCell(col + variant, row) % 6 === 0 ? ramp[1] : ramp[2];
  },
  // 寝台: 上半分が枕と掛け布、下に木の枠。
  bed: (ramp, row, col, variant) => {
    if (row >= TILE_ART_SIZE - 3) return row === TILE_ART_SIZE - 1 ? ramp[0] : ramp[1];
    if (row <= 1 || col <= 1 || col >= TILE_ART_SIZE - 2) return ramp[1];
    if (row >= 2 && row <= 5 && col >= 3 && col <= TILE_ART_SIZE - 4) return row === 2 ? ramp[4] : ramp[3];
    if (row === 6) return ramp[0];
    return (row + col + variant) % 7 === 0 ? ramp[3] : ramp[2];
  },
  // 歪みの地面: ひび割れた地面から、紫の光がにじむ。
  rift: (ramp, row, col, variant) => {
    const h = hashCell(col + variant * 7, row + variant * 3);
    const crack = (col + 2 * Math.floor(row / 3) * (variant % 2 ? -1 : 1) + 32) % 9;
    if (crack === 0) return h % 3 === 0 ? ramp[4] : ramp[3];
    if (crack === 1 || crack === 8) return ramp[0];
    return h % 5 === 0 ? ramp[1] : h % 13 === 0 ? ramp[3] : ramp[2];
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
  // 世界地図の山: 2つの峰。左の面が明るく右の面が暗い。てっぺんは雪。峰のまわりは暗い縁取り、足元は岩の地面。
  mountain: (ramp, row, col, variant) => {
    const peaks = [
      { x: 4 + (variant % 3), y: 3 + (variant % 2) * 2, slope: 1.15 },
      { x: 11 + (variant % 2) - 1, y: 6 + ((variant >> 1) % 2) * 2, slope: 1.0 },
    ];
    const topAt = (c: number): { y: number; peak: number } => {
      let best = { y: 99, peak: -1 };
      peaks.forEach((p, i) => {
        const y = p.y + Math.abs(c - p.x) * p.slope;
        if (y < best.y) best = { y, peak: i };
      });
      return best;
    };
    const inside = (r: number, c: number): { peak: number; depth: number } | null => {
      if (c < 0 || c >= TILE_ART_SIZE || r > 14) return null;
      const t = topAt(c);
      return r >= t.y ? { peak: t.peak, depth: r - t.y } : null;
    };
    const here = inside(row, col);
    if (here) {
      const p = peaks[here.peak];
      if (here.depth < 3.2 && Math.abs(col - p.x) < 4) return col <= p.x ? ramp[4] : ramp[3]; // 雪
      if (col === p.x) return ramp[2]; // 稜線
      const crack = hashCell(col + variant * 7, row) % 11 === 0;
      if (col < p.x) return crack ? ramp[2] : ramp[3];
      return crack ? ramp[0] : ramp[1];
    }
    const edge = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dr, dc]) => inside(row + dr, col + dc));
    if (edge) return ramp[0];
    return row >= 14 ? ramp[0] : hashCell(col + variant * 3, row) % 7 === 0 ? ramp[2] : ramp[1];
  },
  // 世界地図の森: 小さな樹冠が4つ。塊ごとに左上が明るく、すき間は暗い。
  worldforest: (ramp, row, col, variant) => {
    const crowns: [number, number, number][] = [
      [4 + (variant % 2), 4 + ((variant >> 1) % 2), 4.3],
      [11, 5 + (variant % 3 === 0 ? 1 : 0), 4.3],
      [5, 11, 4.4],
      [12 - (variant % 2), 12, 4.2],
    ];
    let best = -9;
    let covered = false;
    for (const [bx, by, br] of crowns) {
      const d2 = ((col - bx) ** 2 + (row - by) ** 2) / (br * br);
      if (d2 <= 1) {
        covered = true;
        const light = (-(col - bx) * 0.6 - (row - by) * 0.8) / br;
        if (light > best) best = light;
      }
    }
    if (!covered) {
      const near = crowns.some(([bx, by, br]) => ((col - bx) ** 2 + (row - by) ** 2) / (br * br) <= 1.5);
      return near ? ramp[0] : shadeColor(ramp[0], -0.2);
    }
    const k = best > 0.3 ? 3 : best > -0.1 ? 2 : 1;
    return hashCell(col + variant * 5, row) % 13 === 0 ? ramp[Math.max(1, k - 1)] : ramp[k];
  },
  // 世界地図の丘: 草の地面に、なだらかな盛り上がりが2つ（左上が明るく、下の縁に影）。
  hills: (ramp, row, col, variant) => {
    const mounds = [
      { x: 5 + (variant % 4), y: 8, rx: 6.2, ry: 4.2 },
      { x: 12 - (variant % 3), y: 12, rx: 5.2, ry: 3.2 },
    ];
    for (const m of mounds) {
      const nx = (col - m.x) / m.rx;
      const ny = (row - m.y) / m.ry;
      const d = nx * nx + ny * ny;
      if (d <= 1) {
        if (ny > 0.55) return ramp[1];
        return nx * 0.7 + ny * 0.9 < -0.25 ? ramp[3] : ramp[2];
      }
    }
    const h = hashCell(col + variant * 7, row + variant * 3);
    return h % 17 === 0 ? ramp[3] : h % 13 === 0 ? ramp[1] : ramp[2];
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
  mountain: { base: "#857c74", accentLight: "#b8b0a2", accentDark: "#4e4640", pattern: "mountain" },
  worldforest: { base: "#3a8a30", accentLight: "#7cd048", accentDark: "#1c5a24", pattern: "worldforest" },
  snowforest: { base: "#3a6a50", accentLight: "#eef4f8", accentDark: "#1c3c3c", pattern: "worldforest" },
  hills: { base: "#5a9a40", accentLight: "#82bc58", accentDark: "#3a7032", pattern: "hills" },
};

/**
 * 「地図のタイルの色」を基本色にして、模様だけを重ねる指定（`tileArt` の値を `tint:<模様>` にする）。
 * 例: `tint:flagstone`。地方ごとに色が違う石畳・壁・砂・雪などを、同じ模様の作りで描くための仕組み。
 */
export const TINT_PREFIX = "tint:";

export function tintedSpec(pattern: TilePatternKind, base: string): TileArtSpec {
  return { base, accentLight: shadeColor(base, 0.22), accentDark: shadeColor(base, -0.28), pattern };
}
