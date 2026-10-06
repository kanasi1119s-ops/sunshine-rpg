import { getTileId, type TileMap } from "../game/map/tile-map";
import { hashCell } from "../game/color-utils";
import { getSpriteCanvas } from "../game/art/sprite";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import type { Camera } from "./camera";

/**
 * 地面のしあげ。見本のマップ（道がうねり、池に岸があり、草地に小さな草花が散っている）から学んだこと:
 *  1. 地形の境目はまっすぐにせず、ギザギザにして草が道に食い込み、池には岸と浅瀬の縁を付ける。
 *  2. 木の下の地面には影を落として、木と地面をなじませる。
 *  3. 何もない草地にも、小さな草・花・小石をまばらに散らして、「何もない」感じをなくす。
 * どれもタイル座標だけから決まるので、毎フレーム同じ絵になる（ちらつかない）。マップのデータは変えない。
 */
type Kind = "grass" | "path" | "water" | "tree" | "land" | "other";

const KIND_BY_ART: Record<string, Kind> = {
  grass: "grass", hills: "grass", path: "path", water: "water", treeCanopy: "tree", worldforest: "tree", snowforest: "tree",
  mountain: "land", peaks: "land", chasm: "land", lava: "land", "tint:sand": "land", "tint:snow": "land", "tint:cloud": "land", "tint:flagstone": "land",
};

const GRASS_DARK = "#3f7a35";
const GRASS_MID = "#5f9f46";
const GRASS_LIGHT = "#86bf5c";
const BANK = "#4a3c2a";
const SHALLOW = "#7ab6d8";
const FOAM = "#c4e4f2";
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
function waterEdge(ctx: CanvasRenderingContext2D, ox: number, oy: number, s: number, tx: number, ty: number, side: number, coastal: boolean): void {
  for (let i = 0; i < s; i++) {
    const h = hashCell(tx * 29 + i + side * 5, ty * 13 + side);
    const [bx, by] = SIDES[side].at(i, 0, s);
    dot(ctx, ox + bx, oy + by, coastal ? FOAM : BANK);
    const [sx, sy] = SIDES[side].at(i, 1, s);
    dot(ctx, ox + sx, oy + sy, h % 3 === 0 ? FOAM : SHALLOW);
    if (h % 4 === 0) {
      const [qx, qy] = SIDES[side].at(i, 2, s);
      dot(ctx, ox + qx, oy + qy, SHALLOW);
    }
  }
}

/**
 * 山のタイル（mountain=山、peaks=高峰）。タイルの「模様」ではなく、世界座標の高さ（尾根ノイズ＋ふちからの距離）から1ドットずつ描く。
 * 隣のタイルとも稜線がつながり、塊の外ふちは自然にくずれ、光は左上。タイルごとに一度だけ描いてキャッシュする（見た目は座標だけで決まる）。
 */
const ROCK_RAMP = ["#363a42", "#4e5560", "#6c747e", "#929ba6", "#bcc4cc"];
const PEAK_RAMP = ["#343a44", "#4c5662", "#6e7c8a", "#98a8b6", "#d6e0ea"];
const mountainCache = new Map<string, HTMLCanvasElement>();

function vnoise(x: number, y: number, seed: number): number {
  const ix = Math.floor(x), iy = Math.floor(y);
  const fx = x - ix, fy = y - iy;
  const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
  const h = (a: number, b: number): number => (hashCell(a * 7 + seed, b * 13 + seed * 3) % 1000) / 1000;
  const top = h(ix, iy) * (1 - sx) + h(ix + 1, iy) * sx;
  const bot = h(ix, iy + 1) * (1 - sx) + h(ix + 1, iy + 1) * sx;
  return top * (1 - sy) + bot * sy;
}

function mountainTile(map: TileMap, tx: number, ty: number, peaks: boolean): HTMLCanvasElement | null {
  if (typeof document === "undefined") return null;
  const key = `${tx},${ty},${peaks ? 1 : 0}`;
  const hit = mountainCache.get(key);
  if (hit) return hit;
  const mass = (x: number, y: number): boolean => {
    const a = artAt(map, x, y) ?? "";
    return a === "mountain" || a === "peaks";
  };
  const N = mass(tx, ty - 1), S = mass(tx, ty + 1), W = mass(tx - 1, ty), E = mass(tx + 1, ty);
  const NW = mass(tx - 1, ty - 1), NE = mass(tx + 1, ty - 1), SW = mass(tx - 1, ty + 1), SE = mass(tx + 1, ty + 1);
  const sideColor = (x: number, y: number): string => {
    const k = kindAt(map, x, y);
    if (k === "water") return "#7a7a72";
    const id = getTileId(map, 0, x, y);
    return NEIGHBOR_COLOR[k] ?? (id ? map.data.tileColors?.[id] ?? "#5a9040" : "#5a9040");
  };
  const ramp = peaks ? PEAK_RAMP : ROCK_RAMP;
  const canvas = document.createElement("canvas");
  canvas.width = 16; canvas.height = 16;
  const c = canvas.getContext("2d");
  if (!c) return null;
  const wx0 = tx * 16, wy0 = ty * 16;
  // ふちからの距離（塊の内側が正）と、いちばん近い外側の方向
  const edge = (px: number, py: number): { d: number; out: string } => {
    let d = 8, side = "";
    const upd = (v: number, tag: string): void => { if (v < d) { d = v; side = tag; } };
    if (!N) upd(py + 0.5, "N");
    if (!S) upd(15.5 - py, "S");
    if (!W) upd(px + 0.5, "W");
    if (!E) upd(15.5 - px, "E");
    if (N && W && !NW) upd(Math.hypot(px + 0.5, py + 0.5), "NW");
    if (N && E && !NE) upd(Math.hypot(15.5 - px, py + 0.5), "NE");
    if (S && W && !SW) upd(Math.hypot(px + 0.5, 15.5 - py), "SW");
    if (S && E && !SE) upd(Math.hypot(15.5 - px, 15.5 - py), "SE");
    return { d, out: side };
  };
  const dxy: Record<string, [number, number]> = { N: [0, -1], S: [0, 1], W: [-1, 0], E: [1, 0], NW: [-1, -1], NE: [1, -1], SW: [-1, 1], SE: [1, 1] };
  // 1ドットの書き込み先（タイルの外は捨てる）
  const buf: (string | null)[][] = Array.from({ length: 16 }, () => Array<string | null>(16).fill(null));
  const put = (px: number, py: number, color: string): void => {
    if (px >= 0 && px < 16 && py >= 0 && py < 16) buf[py][px] = color;
  };
  // 山と山のすき間の岩肌（ゆるい市松で暗い2色）
  for (let py = 0; py < 16; py++) {
    for (let px = 0; px < 16; px++) {
      put(px, py, ramp[1]);
    }
  }
  // 山を1つずつ描いて、奥（上）から手前（下）へ重ねる。山は格子の目ごとに1つ、少しずらして置く。
  const CW = peaks ? 18 : 15, CH = peaks ? 14 : 12;
  const list: Array<{ cx: number; by: number; h: number; seed: number }> = [];
  for (let gy = Math.floor((wy0 - 2) / CH); gy <= Math.floor((wy0 + 16 + 26) / CH); gy++) {
    for (let gx = Math.floor((wx0 - 16) / CW); gx <= Math.floor((wx0 + 16 + 16) / CW); gx++) {
      const hh = hashCell(gx * 41 + 7, gy * 29 + 3);
      const hh2 = hashCell(gx * 17 + 11, gy * 53 + 5);
      const baseH = peaks ? 15 : 11;
      list.push({ cx: gx * CW + 3 + (hh % (CW - 5)), by: gy * CH + 4 + (hh2 % (CH - 3)), h: baseH + (hh2 >> 3) % (peaks ? 8 : 6), seed: hh % 97 });
    }
  }
  list.sort((p1, p2) => p1.by - p2.by);
  for (const m of list) {
    const hw = Math.round(m.h * 0.78);
    const snowRows = peaks && m.h >= 18 ? Math.round(m.h * 0.34) : 0;
    for (let r = 0; r < m.h; r++) {
      const y = m.by - m.h + 1 + r - wy0;
      if (y < -1 || y > 15) continue;
      const w = Math.round(hw * Math.pow((r + 0.6) / m.h, 0.92) + ((hashCell(m.seed + r, 3) % 3) - 1) * 0.6);
      // 背骨: 山頂から根もとへ、ジグザグに下りる明暗の境目
      const split = m.cx + Math.round(Math.sin(r * 0.85 + m.seed) * 1.3) + (r > m.h * 0.55 ? 1 : 0);
      for (let x = -w; x <= w; x++) {
        const wxp = m.cx + x;
        const px = wxp - wx0;
        const lit = wxp < split;
        // 明るい面に、斜めに下りる尾根の線を1本だけ入れる（ごちゃつかせない）
        const ridge = lit && r > 3 && x === -Math.round(w * 0.45) + (r % 2 === 0 ? 0 : 0);
        let idx = lit ? 3 : 1;
        if (ridge) idx = 2;
        if (r < 2) idx = Math.min(4, idx + 1);
        if (x === w && r > 1) idx = 0; // 右のふちの輪郭
        let color = ramp[Math.max(0, Math.min(4, idx))];
        if (r < snowRows && Math.abs(x) < w - (r % 3 === 0 ? 1 : 0)) {
          // 雪: 頂きのまわり。下の縁はギザギザ
          const jag = r >= snowRows - 2 && hashCell(wxp * 3, r + m.seed) % 2 === 0;
          if (!jag) color = lit ? "#eef2f8" : "#b8c2d6";
        }
        put(px, y, color);
      }
    }
    // 根もとの暗い線
    for (let x = -Math.round(hw * 0.7); x <= Math.round(hw * 0.7); x += 1) {
      if (hashCell(m.cx + x, m.seed) % 3 !== 0) put(m.cx + x - wx0, m.by - wy0 + 1, ramp[0]);
    }
  }
  // 塊の外ふち（隣のタイルが山でないところ）は、自然にくずして、となりの地面の色にする
  for (let py = 0; py < 16; py++) {
    for (let px = 0; px < 16; px++) {
      const { d, out } = edge(px, py);
      const jitter = (vnoise((wx0 + px) / 3, (wy0 + py) / 3, 5) - 0.5) * 2.2;
      if (d + jitter < 0.4) {
        const [ox, oy] = dxy[out] ?? [0, 0];
        c.fillStyle = sideColor(tx + ox, ty + oy);
      } else {
        c.fillStyle = buf[py][px] ?? ramp[1];
      }
      c.fillRect(px, py, 1, 1);
    }
  }
  if (mountainCache.size > 4000) mountainCache.clear();
  mountainCache.set(key, canvas);
  return canvas;
}

/** 大きな塊（森・山）の外ふちを、まっすぐにしない: 角を丸め、辺を波うたせて、となりの地面の色を食い込ませる。 */
const MASS_ART = new Set(["worldforest", "snowforest", "mountain", "peaks"]);
const NEIGHBOR_COLOR: Partial<Record<Kind, string>> = { grass: "#5a9040", path: "#a87c3c" };

function artAt(map: TileMap, x: number, y: number): string | undefined {
  if (x < 0 || y < 0 || x >= map.data.width || y >= map.data.height) return undefined;
  const id = getTileId(map, 0, x, y);
  return id ? map.data.tileArt?.[id] : undefined;
}

function erodeMass(ctx: CanvasRenderingContext2D, map: TileMap, ox: number, oy: number, s: number, tx: number, ty: number): void {
  const art = artAt(map, tx, ty);
  const isMass = (x: number, y: number): boolean => MASS_ART.has(artAt(map, x, y) ?? "");
  const colorOf = (x: number, y: number): string | null => {
    const k = kindAt(map, x, y);
    if (k === "water" || k === "other") return null;
    if (MASS_ART.has(artAt(map, x, y) ?? "")) return null;
    const id = getTileId(map, 0, x, y);
    return NEIGHBOR_COLOR[k] ?? (id ? map.data.tileColors?.[id] ?? null : null);
  };
  const forest = art === "worldforest" || art === "snowforest";
  // 同じ模様のくり返しに見えないよう、塊の内側の明暗を、タイルごとに少しゆらす
  const tone = hashCell(tx * 5 + 1, ty * 11 + 3) % 6;
  // 2026-10-06 人間の指示「フィールドに謎の影」: タイルまるごと暗くする四角（森・山の中に四角い影が見えた）はやめた
  if (tone === 1 && !forest) {
    ctx.fillStyle = "rgba(255,255,255,0.07)";
    ctx.fillRect(ox, oy, s, s);
  }
  // 辺: 外側に隣が地面のとき、1〜2ドットの波を削る
  const sides: Array<[number, number, (i: number, d: number) => [number, number]]> = [
    [0, -1, (i, d) => [i, d]], [0, 1, (i, d) => [i, s - 1 - d]], [-1, 0, (i, d) => [d, i]], [1, 0, (i, d) => [s - 1 - d, i]],
  ];
  sides.forEach(([dx, dy, at], si) => {
    const c = colorOf(tx + dx, ty + dy);
    if (!c) return;
    for (let i = 0; i < s; i++) {
      const h = hashCell(tx * 31 + i + si * 7, ty * 17 + si);
      const depth = h % 7 === 0 ? 3 : h % 4 === 0 ? 2 : h % 2 === 0 ? 1 : 0;
      for (let d = 0; d < depth; d++) {
        const [px, py] = at(i, d);
        dot(ctx, ox + px, oy + py, c);
      }
      // 森は、削ったすぐ内側に暗い縁（樹冠の影）を引く
      if (forest && depth > 0) {
        const [px, py] = at(i, depth);
        dot(ctx, ox + px, oy + py, "rgba(10,40,20,0.55)");
      }
    }
  });
  // 角: 両どなりが外なら、丸く削る（半径4〜6）
  const corners: Array<[number, number, number, number]> = [[-1, -1, 0, 0], [1, -1, s - 1, 0], [-1, 1, 0, s - 1], [1, 1, s - 1, s - 1]];
  corners.forEach(([dx, dy, cx, cy], ci) => {
    if (isMass(tx + dx, ty) || isMass(tx, ty + dy)) return;
    const c = colorOf(tx + dx, ty) ?? colorOf(tx, ty + dy);
    if (!c) return;
    const r = 6 + (hashCell(tx * 13 + ci, ty * 29) % 3);
    for (let y = 0; y < r; y++) {
      for (let x = 0; x < r; x++) {
        const px = cx === 0 ? x : s - 1 - x;
        const py = cy === 0 ? y : s - 1 - y;
        if (x + y < r - 1 || (x + y === r - 1 && (x + y + tx) % 2 === 0)) dot(ctx, ox + px, oy + py, c);
      }
    }
  });
}

/** 山・森のふもとの影（光は左上。塊の下と右の地面に落ちる）と、山すその小石。 */
function massShadow(ctx: CanvasRenderingContext2D, map: TileMap, ox: number, oy: number, s: number, tx: number, ty: number): void {
  const above = artAt(map, tx, ty - 1) ?? "";
  if (MASS_ART.has(above)) {
    const peak = above === "mountain" || above === "peaks";
    // 影の深さを、なめらかにゆらし（まっすぐな帯にしない）、うすく、下へ行くほど消す
    for (let i = 0; i < s; i++) {
      const w = tx * s + i;
      const a = Math.floor(w / 6), f = w / 6 - a, t = f * f * (3 - 2 * f);
      const v = (k: number): number => (hashCell(k * 13 + 7, ty * 5 + 2) % 1000) / 1000;
      const depth = (peak ? 2 : 1) + Math.round((v(a) * (1 - t) + v(a + 1) * t) * 3);
      for (let d = 0; d < depth; d++) dot(ctx, ox + i, oy + d, `rgba(14,30,20,${(0.2 * (1 - d / (depth + 0.5))).toFixed(3)})`);
    }
    if (peak && hashCell(tx, ty) % 3 === 0) dot(ctx, ox + 3 + (hashCell(tx, ty + 1) % 10), oy + 6, "#7a7068", 2, 1);
  }
  // 2026-10-06「雪原にも謎の影あるよ山間とか」: 森・山の右どなりに引いていた、たての暗い2列の線（まっすぐな影に見えた）はやめた
}

/** 水面のきらめき: 細い光の筋が、ゆっくり現れては消える（時刻でゆらぐ）。 */
function waterShimmer(ctx: CanvasRenderingContext2D, ox: number, oy: number, tx: number, ty: number, nowMs: number): void {
  for (let n = 0; n < 2; n++) {
    const h = hashCell(tx * 13 + n * 5, ty * 29 + n);
    const phase = nowMs / 650 + (h % 628) / 100;
    const a = Math.sin(phase);
    if (a <= 0.2) {
      continue;
    }
    const x = 1 + (h % 11) + (Math.floor(phase / 6.28) % 2);
    const y = 2 + ((h >> 8) % 12);
    ctx.fillStyle = `rgba(235,248,255,${(a * 0.5).toFixed(2)})`;
    ctx.fillRect(ox + x, oy + y, 3, 1);
    ctx.fillStyle = `rgba(235,248,255,${(a * 0.25).toFixed(2)})`;
    ctx.fillRect(ox + x + 3, oy + y, 1, 1);
  }
}

/** 溶岩の脈動: 明るい部分がゆっくり強まったり弱まったりし、ときどき火の粉が立ちのぼる。 */
function lavaGlow(ctx: CanvasRenderingContext2D, ox: number, oy: number, tx: number, ty: number, nowMs: number): void {
  const h = hashCell(tx * 17 + 3, ty * 23 + 1);
  const pulse = (Math.sin(nowMs / 900 + (h % 628) / 100) + 1) / 2;
  ctx.fillStyle = `rgba(255,150,40,${(0.05 + pulse * 0.16).toFixed(2)})`;
  ctx.fillRect(ox, oy, 16, 16);
  const spark = (nowMs / 1400 + (h % 100) / 100) % 1;
  if (h % 3 === 0) {
    ctx.fillStyle = `rgba(255,220,120,${(1 - spark).toFixed(2)})`;
    ctx.fillRect(ox + 2 + (h % 11), oy + 12 - Math.round(spark * 12), 1, 1);
  }
}

/** 海岸の砂浜: 水に接する陸のふちに、不ぞろいな砂のおびと、水ぎわの濡れた砂。 */
function beachEdge(ctx: CanvasRenderingContext2D, ox: number, oy: number, s: number, tx: number, ty: number, side: number): void {
  for (let i = 0; i < s; i++) {
    const h = hashCell(tx * 37 + i + side * 11, ty * 19 + side);
    const depth = 2 + (h % 3 === 0 ? 1 : 0) + (h % 7 === 0 ? 1 : 0);
    for (let d = 0; d < depth; d++) {
      const [px, py] = SIDES[side].at(i, d, s);
      dot(ctx, ox + px, oy + py, d === 0 ? "#b89c68" : d === depth - 1 && depth > 2 ? "#e8d9a8" : "#dccb92");
    }
  }
}

/** 木の下（南どなりの草地）に落ちる影。2026-10-06「謎の影」: 四角い暗い帯に見えたので、うすく、深さをなめらかにゆらし、下へ行くほど消える。 */
function treeShadow(ctx: CanvasRenderingContext2D, ox: number, oy: number, s: number, tx: number, ty: number): void {
  for (let i = 0; i < s; i++) {
    const w = tx * s + i;
    const a = Math.floor(w / 6), f = w / 6 - a, t = f * f * (3 - 2 * f);
    const v = (k: number): number => (hashCell(k * 11 + 5, ty * 7 + 1) % 1000) / 1000;
    const depth = 1 + Math.round((v(a) * (1 - t) + v(a + 1) * t) * 3);
    for (let d = 0; d < depth; d++) {
      dot(ctx, ox + i, oy + d, `rgba(14,40,24,${(0.2 * (1 - d / (depth + 0.5))).toFixed(3)})`);
    }
  }
}

/** なめらかな値ノイズ（0〜1）。ワールド座標で決まるので、タイルをまたいでつながり、繰り返しに見えない。 */
function smoothNoise(wx: number, wy: number): number {
  const sp = 28;
  const gx = Math.floor(wx / sp), gy = Math.floor(wy / sp);
  const fx = (wx / sp - gx), fy = (wy / sp - gy);
  const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
  const v = (a: number, b: number): number => (hashCell(a + 101, b + 57) % 1000) / 1000;
  const top = v(gx, gy) * (1 - sx) + v(gx + 1, gy) * sx;
  const bottom = v(gx, gy + 1) * (1 - sx) + v(gx + 1, gy + 1) * sx;
  return top * (1 - sy) + bottom * sy;
}

/** 草地の色むら: 明るい日なた・暗い日かげを、4ドット単位のうすい色で重ねる（広い草原の単調さをなくす）。 */
function grassPatches(ctx: CanvasRenderingContext2D, ox: number, oy: number, tx: number, ty: number): void {
  // 2026-10-06「フィールドに謎の影」: 暗いむらが、四角いしみ（影）に見えたので、2ドット単位でなめらかにし、暗い側はうすく
  for (let by = 0; by < 8; by++) {
    for (let bx = 0; bx < 8; bx++) {
      const n = smoothNoise(tx * 16 + bx * 2 + 1, ty * 16 + by * 2 + 1) - 0.5;
      const a = Math.round(Math.abs(n) * (n > 0 ? 0.4 : 0.18) * 100) / 100;
      if (a < 0.03) continue;
      ctx.fillStyle = n > 0 ? `rgba(190,226,96,${a})` : `rgba(8,44,28,${a})`;
      ctx.fillRect(ox + bx * 2, oy + by * 2, 2, 2);
    }
  }
}

/** 雪の地方の木のタイル: 枝の上に雪がのる（上のとなりが木でなければ、てっぺんに厚く）。 */
function snowOnTree(ctx: CanvasRenderingContext2D, ox: number, oy: number, s: number, tx: number, ty: number, topEdge: boolean): void {
  for (let y = 0; y < s; y++) {
    for (let x = 0; x < s; x++) {
      const n = hashCell(tx * 16 + x, ty * 16 + y);
      const limit = topEdge ? (y < 4 ? 90 : y < 8 ? 45 : 22) : y < 8 ? 26 : 14;
      if (n % 100 < limit) {
        dot(ctx, ox + x, oy + y, n % 3 === 0 ? "#dbe7f5" : "#f6faff");
      }
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

/** 水のタイルの、岸からの近さ（1〜4。水でなければ 0）。地図ごとに一度だけ数えて、おぼえておく。 */
const waterNearCache = new WeakMap<object, Int8Array>();
function waterNear(map: TileMap, tx: number, ty: number): number {
  const { width: w, height: h } = map.data;
  if (tx < 0 || ty < 0 || tx >= w || ty >= h) return 0;
  let c = waterNearCache.get(map.data);
  if (!c) {
    c = new Int8Array(w * h).fill(-1);
    waterNearCache.set(map.data, c);
  }
  const i = ty * w + tx;
  if (c[i] < 0) c[i] = waterNearRaw(map, tx, ty);
  return c[i];
}

function waterNearRaw(map: TileMap, tx: number, ty: number): number {
  if (kindAt(map, tx, ty) !== "water") return 0;
  for (let r = 1; r <= 3; r++) {
    for (let dy = -r; dy <= r; dy++) {
      for (let dx = -r; dx <= r; dx++) {
        if (Math.max(Math.abs(dx), Math.abs(dy)) === r && kindAt(map, tx + dx, ty + dy) !== "water") return r;
      }
    }
  }
  return 4;
}

/** 町の草むら（treeCanopy）と芝（草地）のさかいを、四角いタイルの境目にせず、なめらかな形でまぜる
 *  （2026-10-06 人間の指示「草むら馴染んでないんだよね。四角なのがいけないと思う。しげみと芝って四角で境目分かれてないと思うんだ」）。
 *  タイルのまんなかの「草むらかどうか（1/0）」を、となりのタイルとの間でなめらかにつなぎ、ゆれ（ノイズ）を足して、
 *  0.5 より上の所は草むらの絵、下の所は芝の絵にする（さかいの近くの、芝のタイルにも草むらがはみ出す）。
 *  さかいのタイルの絵は、一度だけ作って、おぼえておく。 */
const canopyTileCache = new Map<string, HTMLCanvasElement | null>();
function canopyBlend(ctx: CanvasRenderingContext2D, map: TileMap, ox: number, oy: number, s: number, tx: number, ty: number): void {
  const isC = (x: number, y: number): number => (kindAt(map, x, y) === "tree" && artAt(map, x, y) === "treeCanopy" ? 1 : 0);
  const here = isC(tx, ty);
  const grassish = (x: number, y: number): boolean => { const k = kindAt(map, x, y); return k === "grass" || isC(x, y) === 1; };
  if (!grassish(tx, ty)) return;
  let mixed = false;
  for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) if (grassish(tx + dx, ty + dy) && isC(tx + dx, ty + dy) !== here) mixed = true;
  if (!mixed) return;
  const key = `${map.data.width}x${map.data.height}:${tx},${ty}:${getTileId(map, 0, 0, 0)}`;
  let tile = canopyTileCache.get(key);
  if (tile === undefined) {
    tile = null;
    const canopy = getSpriteCanvas("terrain:forest", SPRITE_DATA);
    if (canopy && typeof document !== "undefined") {
      const c = document.createElement("canvas");
      c.width = s; c.height = s;
      const g = c.getContext("2d");
      if (g) {
        g.imageSmoothingEnabled = false;
        const cv = (x: number, y: number): number => (grassish(x, y) ? isC(x, y) : here);
        for (let py = 0; py < s; py++) {
          for (let px = 0; px < s; px++) {
            const fx = (px + 0.5) / s - 0.5, fy = (py + 0.5) / s - 0.5;
            const ix = fx < 0 ? tx - 1 : tx, iy = fy < 0 ? ty - 1 : ty;
            const wx = fx < 0 ? fx + 1 : fx, wy = fy < 0 ? fy + 1 : fy;
            let v = (cv(ix, iy) * (1 - wx) + cv(ix + 1, iy) * wx) * (1 - wy) + (cv(ix, iy + 1) * (1 - wx) + cv(ix + 1, iy + 1) * wx) * wy;
            const gx = tx * s + px, gy = ty * s + py;
            v += (smoothNoise(gx * 2.3, gy * 2.3) - 0.5) * 0.55 + ((hashCell(gx, gy) % 100) / 100 - 0.5) * 0.12;
            if (v > 0.5) {
              g.drawImage(canopy, ((gx % 128) + 128) % 128, ((gy % 128) + 128) % 128, 1, 1, px, py, 1, 1);
            } else {
              const key2 = ["terrain:grass-a", "terrain:grass-b"][hashCell(Math.floor(tx / 8), Math.floor(ty / 8)) % 2];
              const grass = getSpriteCanvas(key2, SPRITE_DATA);
              if (grass) g.drawImage(grass, ((gx % 128) + 128) % 128, ((gy % 128) + 128) % 128, 1, 1, px, py, 1, 1);
            }
          }
        }
        tile = c;
      }
    }
    if (canopyTileCache.size > 3000) canopyTileCache.clear();
    canopyTileCache.set(key, tile);
  }
  if (tile) ctx.drawImage(tile, ox, oy);
}

/** 全体フィールドの、平らな地面どうし（雪・草・砂・道など）のさかいを、四角くせず、波うつ形でまぜる
 *  （2026-10-06 人間の指示「フィールドのドット絵違和感なくなるようにして」）。順位の高い地面が、低い地面のふちへ、
 *  なめらかにゆれる深さ（1〜4ドット）だけ、自分の絵で食い込む。かどは丸く。 */
const FLAT_PRIO: Record<string, number> = {
  "terrain:w-road": 0, "terrain:w-sand": 1, "terrain:w-ash": 1, "terrain:w-waste": 1, "terrain:w-grass": 2, "terrain:w-hills": 2, "terrain:w-snow": 3,
};
function texKey(map: TileMap, x: number, y: number): string | null {
  if (x < 0 || y < 0 || x >= map.data.width || y >= map.data.height) return null;
  return map.data.tileTexture?.[getTileId(map, 0, x, y)] ?? null;
}
function texPixel(ctx: CanvasRenderingContext2D, key: string, wx: number, wy: number, dx: number, dy: number): void {
  const tex = getSpriteCanvas(key, SPRITE_DATA);
  if (!tex) return;
  ctx.drawImage(tex, ((wx % 128) + 128) % 128, ((wy % 128) + 128) % 128, 1, 1, dx, dy, 1, 1);
}
function waveDepth(w: number, salt: number, max: number): number {
  const a = Math.floor(w / 5), f = w / 5 - a, t = f * f * (3 - 2 * f);
  const v = (k: number): number => (hashCell(k * 7 + salt, salt * 13 + 3) % 1000) / 1000;
  return 1 + Math.round((v(a) * (1 - t) + v(a + 1) * t) * (max - 1));
}
function flatBlend(ctx: CanvasRenderingContext2D, map: TileMap, ox: number, oy: number, s: number, tx: number, ty: number): void {
  const here = texKey(map, tx, ty);
  if (!here || !(here in FLAT_PRIO)) return;
  const myP = FLAT_PRIO[here];
  const sides: Array<[number, number, (i: number, d: number) => [number, number], number]> = [
    [0, -1, (i, d) => [i, d], 1], [0, 1, (i, d) => [i, s - 1 - d], 2], [-1, 0, (i, d) => [d, i], 3], [1, 0, (i, d) => [s - 1 - d, i], 4],
  ];
  for (const [dx, dy, at, salt] of sides) {
    const nk = texKey(map, tx + dx, ty + dy);
    if (!nk || !(nk in FLAT_PRIO) || FLAT_PRIO[nk] <= myP) continue;
    const lineSalt = salt * 97 + (dx !== 0 ? tx + (dx > 0 ? 1 : 0) : ty + (dy > 0 ? 1 : 0)) * 31 + (dx !== 0 ? 5000 : 0);
    for (let i = 0; i < s; i++) {
      const along = dx !== 0 ? ty * s + i : tx * s + i;
      const depth = waveDepth(along, lineSalt, 4);
      for (let d = 0; d < depth; d++) {
        const [px, py] = at(i, d);
        texPixel(ctx, nk, tx * s + px, ty * s + py, ox + px, oy + py);
      }
    }
  }
  // かど: 両どなりが同じ「上の地面」なら、丸く食い込む
  const corners: Array<[number, number, number, number]> = [[-1, -1, 0, 0], [1, -1, s - 1, 0], [-1, 1, 0, s - 1], [1, 1, s - 1, s - 1]];
  for (const [dx, dy, cx, cy] of corners) {
    const a = texKey(map, tx + dx, ty), b = texKey(map, tx, ty + dy);
    if (!a || a !== b || !(a in FLAT_PRIO) || FLAT_PRIO[a] <= myP) continue;
    const r = 6 + (hashCell(tx * 13 + dx, ty * 29 + dy) % 3);
    for (let y = 0; y < r; y++) for (let x = 0; x < r; x++) {
      if ((r - x - 0.5) ** 2 + (r - y - 0.5) ** 2 <= r * r) continue;
      const px = cx === 0 ? x : s - 1 - x, py = cy === 0 ? y : s - 1 - y;
      texPixel(ctx, a, tx * s + px, ty * s + py, ox + px, oy + py);
    }
  }
}

/** 小さな水たまり・沼（まわりが陸の水のタイル）のかどを、まるく陸の絵でけずる（2026-10-06「入れない沼も自然な形にして」）。 */
function roundPond(ctx: CanvasRenderingContext2D, map: TileMap, ox: number, oy: number, s: number, tx: number, ty: number): void {
  const isW = (x: number, y: number): boolean => kindAt(map, x, y) === "water";
  const corners: Array<[number, number, number, number]> = [[-1, -1, 0, 0], [1, -1, s - 1, 0], [-1, 1, 0, s - 1], [1, 1, s - 1, s - 1]];
  for (const [dx, dy, cx, cy] of corners) {
    if (isW(tx + dx, ty) || isW(tx, ty + dy) || isW(tx + dx, ty + dy)) continue;
    const land = texKey(map, tx + dx, ty) ?? texKey(map, tx, ty + dy);
    if (!land) continue;
    const r = 6 + (hashCell(tx * 17 + dx, ty * 23 + dy) % 3);
    for (let y = 0; y < r; y++) for (let x = 0; x < r; x++) {
      const d2 = (r - x - 0.5) ** 2 + (r - y - 0.5) ** 2;
      if (d2 <= r * r) {
        if (d2 > (r - 1.2) ** 2) dot(ctx, ox + (cx === 0 ? x : s - 1 - x), oy + (cy === 0 ? y : s - 1 - y), "rgba(196,228,242,0.55)");   // 水ぎわの白いふち
        continue;
      }
      const px = cx === 0 ? x : s - 1 - x, py = cy === 0 ? y : s - 1 - y;
      texPixel(ctx, land, tx * s + px, ty * s + py, ox + px, oy + py);
    }
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
  const nowMs = typeof performance !== "undefined" ? performance.now() : 0;
  for (let ty = startY; ty <= endY; ty++) {
    for (let tx = startX; tx <= endX; tx++) {
      const kind = kindAt(map, tx, ty);
      if (kind === "other") {
        continue;
      }
      const ox = tx * s - camera.x;
      const oy = ty * s - camera.y;
      const artHere = map.data.tileArt[getTileId(map, 0, tx, ty)] ?? "";
      if (map.data.tileTexture) {
        flatBlend(ctx, map, ox, oy, s, tx, ty);
      }
      if (!map.data.tileTexture && (kind === "grass" || artHere === "treeCanopy")) {
        canopyBlend(ctx, map, ox, oy, s, tx, ty);
      }
      if ((artHere === "mountain" || artHere === "peaks") && !map.data.theme && !map.data.tileTexture) {   // 地形テクスチャのある地図（全体フィールド）は、テクスチャの岩山をそのまま見せる
        const tile = mountainTile(map, tx, ty, artHere === "peaks");
        if (tile) {
          ctx.drawImage(tile, ox, oy);
          continue;
        }
      }
      if (MASS_ART.has(artHere)) {
        erodeMass(ctx, map, ox, oy, s, tx, ty);
      } else if (kind === "grass" || kind === "path" || (kind === "land" && map.data.coastal)) {
        massShadow(ctx, map, ox, oy, s, tx, ty);
      }
      if (map.data.tileArt[getTileId(map, 0, tx, ty)] === "lava") {
        lavaGlow(ctx, ox, oy, tx, ty, nowMs);
        continue;
      }
      if (kind === "grass") {
        // 全体フィールドは、地面のテクスチャ（ground_tex.py）に草の株・花・小石まで描いてあるので、古い明るい緑の飾りは重ねない（2026-10-06）
        if (!map.data.tileTexture) grassPatches(ctx, ox, oy, tx, ty);
        if (!map.data.tileTexture && !map.data.coastal || hashCell(tx * 3 + 1, ty * 7 + 2) % 4 === 0) {
          grassDecor(ctx, ox, oy, s, tx, ty);
        }
        if (kindAt(map, tx, ty - 1) === "tree" && artAt(map, tx, ty - 1) !== "treeCanopy") {   // 草むらは芝とまざるので、帯の影はつけない
          treeShadow(ctx, ox, oy, s, tx, ty);
        }
        if (map.data.coastal) {
          SIDES.forEach((side, index) => {
            if (kindAt(map, tx + side.dx, ty + side.dy) === "water") {
              beachEdge(ctx, ox, oy, s, tx, ty, index);
            }
          });
        }
        continue;
      }
      if (kind === "water") {
        // 岸から離れるほど、水の色が濃く（深く）なる
        let near = 4;
        for (let r = 1; r <= 3 && near === 4; r++) {
          for (let dy = -r; dy <= r && near === 4; dy++) {
            for (let dx = -r; dx <= r; dx++) {
              if (Math.max(Math.abs(dx), Math.abs(dy)) === r && kindAt(map, tx + dx, ty + dy) !== "water") {
                near = r;
                break;
              }
            }
          }
        }
        // 深さの色は、タイルごとの四角にせず、となりのタイルとの間をなめらかにつなぐ（2026-10-06「謎の影」: 湖に四角い暗い所が見えた）
        const depthA = (x: number, y: number): number => {
          const n = waterNear(map, x, y);
          return n <= 1 ? 0 : n === 2 ? 0.1 : n === 3 ? 0.18 : 0.26;
        };
        for (let by = 0; by < 4; by++) {
          for (let bx = 0; bx < 4; bx++) {
            // タイルのまんなかどうしの間を、線形にまぜる（となりのタイル4つ）
            const fx = (bx + 0.5) / 4 - 0.5, fy = (by + 0.5) / 4 - 0.5;
            const ix = fx < 0 ? tx - 1 : tx, iy = fy < 0 ? ty - 1 : ty;
            const wx = fx < 0 ? fx + 1 : fx, wy = fy < 0 ? fy + 1 : fy;
            const a = (depthA(ix, iy) * (1 - wx) + depthA(ix + 1, iy) * wx) * (1 - wy) + (depthA(ix, iy + 1) * (1 - wx) + depthA(ix + 1, iy + 1) * wx) * wy;
            if (a < 0.02) continue;
            ctx.fillStyle = `rgba(6,24,64,${a.toFixed(3)})`;
            ctx.fillRect(ox + bx * 4, oy + by * 4, 4, 4);
          }
        }
        // 海（濃い青）と湖（明るい青）のテクスチャのさかいを、なめらかにまぜる（2026-10-06「謎の影」: 湖の中に、四角い濃い所が見えた）
        if (map.data.tileTexture) {
          const tex = (x: number, y: number): number => {
            if (x < 0 || y < 0 || x >= map.data.width || y >= map.data.height || kindAt(map, x, y) !== "water") return -1;
            const k = map.data.tileTexture?.[getTileId(map, 0, x, y)] ?? "";
            return k.endsWith("w-sea") ? 1 : 0;
          };
          const here = tex(tx, ty);
          const vAt = (x: number, y: number): number => { const v = tex(x, y); return v < 0 ? here : v; };
          let mixed = false;
          for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]) if (vAt(tx + dx, ty + dy) !== here) mixed = true;
          if (mixed) {
            for (let by = 0; by < 8; by++) {
              for (let bx = 0; bx < 8; bx++) {
                const fx = (bx + 0.5) / 8 - 0.5, fy = (by + 0.5) / 8 - 0.5;
                const ix = fx < 0 ? tx - 1 : tx, iy = fy < 0 ? ty - 1 : ty;
                const wx = fx < 0 ? fx + 1 : fx, wy = fy < 0 ? fy + 1 : fy;
                const v = (vAt(ix, iy) * (1 - wx) + vAt(ix + 1, iy) * wx) * (1 - wy) + (vAt(ix, iy + 1) * (1 - wx) + vAt(ix + 1, iy + 1) * wx) * wy;
                const d = v - here;
                if (Math.abs(d) < 0.04) continue;
                ctx.fillStyle = d > 0 ? `rgba(18,58,120,${(d * 0.55).toFixed(3)})` : `rgba(64,128,190,${(-d * 0.55).toFixed(3)})`;
                ctx.fillRect(ox + bx * 2, oy + by * 2, 2, 2);
              }
            }
          }
        }
        waterShimmer(ctx, ox, oy, tx, ty, nowMs);
      }
      if (kind === "tree" && map.data.snowy) {
        snowOnTree(ctx, ox, oy, s, tx, ty, kindAt(map, tx, ty - 1) !== "tree");
        continue;
      }
      if (kind !== "path" && kind !== "water") {
        continue;
      }
      SIDES.forEach((side, index) => {
        const n = kindAt(map, tx + side.dx, ty + side.dy);
        if (kind === "path" && n === "grass" && !map.data.tileTexture) {   // 全体フィールドの道と草のさかいは flatBlend がまぜる
          pathEdge(ctx, ox, oy, s, tx, ty, index);
        } else if (kind === "water" && (n === "grass" || n === "path" || n === "land" || n === "tree")) {
          waterEdge(ctx, ox, oy, s, tx, ty, index, !!map.data.coastal);
        }
      });
      // 沼・水たまりのかどは、水ぎわの線をかいたあとで、まるくけずる
      if (kind === "water" && map.data.tileTexture) roundPond(ctx, map, ox, oy, s, tx, ty);
    }
  }
}
