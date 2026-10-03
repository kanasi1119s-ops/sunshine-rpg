/**
 * 戦闘画面の背景（場所ごと）。画像ファイルは使わず、小さな絵を一度だけ描いて使い回す。
 * 空・遠景・近景の層（ディザでなじませた帯、雲、丘、木、洞窟の石筍と水晶、砂丘、雪の松、遺跡の柱）で奥行きを出す。
 */
export type Biome = "grass" | "cave" | "desert" | "snow" | "ruins";

const BIOME_BY_PREFIX: Array<[string, Biome]> = [
  ["tetsukusari-mine", "cave"], ["deep-", "ruins"], ["tower-", "ruins"], ["kanou-", "ruins"], ["kyotoukyu", "ruins"],
  ["god-shrine", "ruins"], ["shimohara", "snow"], ["sanone", "desert"], ["garasuko-warehouse", "cave"],
  ["kiri-archive", "ruins"], ["fushima-base", "ruins"], ["toushin", "ruins"], ["mugikano-water", "cave"],
];

/** 地図の名前から、戦闘の背景を決める。 */
export function biomeForMap(mapId: string): Biome {
  for (const [prefix, biome] of BIOME_BY_PREFIX) {
    if (mapId.startsWith(prefix)) {
      return biome;
    }
  }
  return "grass";
}

function hash(a: number, b: number): number {
  let h = (Math.floor(a) * 374761393 + Math.floor(b) * 668265263) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

type Ctx = CanvasRenderingContext2D;

function px(ctx: Ctx, x: number, y: number, color: string, w = 1, h = 1): void {
  ctx.fillStyle = color;
  ctx.fillRect(Math.round(x), Math.round(y), w, h);
}

/** 縦の色の帯。隣り合う帯の境目は1行だけ市松でなじませる。 */
function bands(ctx: Ctx, w: number, y0: number, y1: number, colors: string[]): void {
  const n = colors.length;
  const bh = (y1 - y0) / n;
  for (let i = 0; i < n; i++) {
    const ya = Math.round(y0 + i * bh);
    const yb = Math.round(y0 + (i + 1) * bh);
    ctx.fillStyle = colors[i];
    ctx.fillRect(0, ya, w, yb - ya);
    if (i + 1 < n) {
      ctx.fillStyle = colors[i + 1];
      for (let x = 0; x < w; x++) {
        if ((x + yb) % 2 === 0) {
          ctx.fillRect(x, yb - 1, 1, 1);
        }
      }
    }
  }
}

/** 丘のシルエット（なだらかな波）。上の縁を明るく。 */
function hills(ctx: Ctx, w: number, h: number, base: number, amp: number, seed: number, body: string, rim: string, shade?: string): void {
  for (let x = 0; x < w; x++) {
    const y = base + Math.sin(x * 0.021 + seed) * amp + Math.sin(x * 0.057 + seed * 2.3) * amp * 0.45;
    const top = Math.round(y);
    ctx.fillStyle = body;
    ctx.fillRect(x, top, 1, h - top);
    px(ctx, x, top, rim);
    if (shade) {
      // 右下へ向かって暗い帯（左上から光）
      const k = Math.round(2 + Math.sin(x * 0.04 + seed) * 1.5);
      px(ctx, x, top + 1, rim);
      for (let i = 0; i < k; i++) {
        if ((x + i) % 2 === 0) px(ctx, x, top + 3 + i, shade);
      }
    }
  }
}

function cloud(ctx: Ctx, cx: number, cy: number, s: number, light: string, shade: string): void {
  const blobs: Array<[number, number, number]> = [[0, 0, 9], [-9, 3, 7], [9, 3, 7], [16, 5, 5], [-15, 5, 5]];
  for (const [dx, dy, r] of blobs) {
    for (let y = -r; y <= r; y++) {
      for (let x = -r * 1.4; x <= r * 1.4; x++) {
        const nx = x / (r * 1.4), ny = y / r;
        if (nx * nx + ny * ny > 1) continue;
        px(ctx, cx + (dx + x) * s, cy + (dy + y) * s * 0.7, ny > 0.35 || nx > 0.55 ? shade : light, Math.max(1, s), Math.max(1, s * 0.7));
      }
    }
  }
}

function tree(ctx: Ctx, x: number, y: number, s: number, light: string, mid: string, dark: string): void {
  ctx.fillStyle = dark;
  ctx.fillRect(x - 1, y, 2, 4 * s);
  const rings: Array<[number, number, number]> = [[0, -3 * s, 5 * s], [-3 * s, -1 * s, 4 * s], [3 * s, -1 * s, 4 * s]];
  for (const [dx, dy, r] of rings) {
    for (let yy = -r; yy <= r; yy++) {
      for (let xx = -r; xx <= r; xx++) {
        if (xx * xx + yy * yy > r * r) continue;
        const lum = -xx * 0.5 - yy * 0.7;
        px(ctx, x + dx + xx, y + dy + yy, lum > r * 0.45 ? light : lum > -r * 0.2 ? mid : dark);
      }
    }
  }
}

function grassBackdrop(ctx: Ctx, w: number, h: number): void {
  bands(ctx, w, 0, 100, ["#5a9ad8", "#6aaae2", "#7ab8ea", "#92c8f0", "#aedaf4", "#cfe8f6", "#e8f4f8"]);
  cloud(ctx, 60, 26, 2, "#ffffff", "#d8e6f4");
  cloud(ctx, 210, 18, 2.4, "#ffffff", "#d0e0f0");
  cloud(ctx, 150, 48, 1.5, "#f4f8fc", "#d8e6f2");
  hills(ctx, w, h, 86, 7, 1.3, "#7aa0c4", "#a0c0dc");
  hills(ctx, w, h, 98, 6, 4.1, "#4e8c58", "#7ac07a", "#3a7048");
  for (let i = 0; i < 22; i++) {
    const x = 10 + i * 14.5 + hash(i, 1) * 6;
    const y = 98 + Math.sin(x * 0.021 + 4.1) * 6 + Math.sin(x * 0.057 + 9.4) * 2.7 + 4;
    tree(ctx, x, y, 1 + (hash(i, 2) > 0.6 ? 0.3 : 0), "#5aa860", "#3a7e48", "#245a34");
  }
  bands(ctx, w, 108, h, ["#4a9a48", "#42903f", "#3a8638", "#337c32", "#2c722c", "#266826"]);
  for (let i = 0; i < 260; i++) {
    const x = hash(i, 5) * w, y = 112 + hash(i, 6) * (h - 112);
    const big = (y - 108) / (h - 108);
    px(ctx, x, y, "#7ac85a"); px(ctx, x - 1, y - 1 - big * 1.5, "#7ac85a"); px(ctx, x + 1, y - 1 - big * 1.5, "#7ac85a");
    px(ctx, x, y + 1, "#1e5a20");
  }
  for (let i = 0; i < 30; i++) {
    const x = hash(i, 7) * w, y = 118 + hash(i, 8) * (h - 124);
    const c = ["#ffffff", "#ffe060", "#ff8aa8"][i % 3];
    px(ctx, x, y, c); px(ctx, x + 1, y, c); px(ctx, x, y - 1, c); px(ctx, x, y + 1, "#2a7a2a");
  }
}

function caveBackdrop(ctx: Ctx, w: number, h: number): void {
  bands(ctx, w, 0, h, ["#120e1c", "#181226", "#1e1830", "#241c38", "#2a2040", "#2e2446"]);
  // 岩壁の質感
  for (let i = 0; i < 700; i++) {
    const x = hash(i, 1) * w, y = hash(i, 2) * h;
    px(ctx, x, y, hash(i, 3) > 0.5 ? "#3a2e50" : "#0e0a16", 1 + Math.floor(hash(i, 4) * 3), 1);
  }
  // 石筍（上から）と柱
  for (let i = 0; i < 16; i++) {
    const x = i * 21 + hash(i, 9) * 10, len = 14 + hash(i, 10) * 34, half = 5 + hash(i, 11) * 6;
    for (let y = 0; y < len; y++) {
      const hw = half * (1 - y / len);
      for (let xx = -hw; xx <= hw; xx++) {
        const lum = -xx / (hw || 1);
        px(ctx, x + xx, y, lum > 0.35 ? "#5a4a78" : lum > -0.3 ? "#3e3258" : "#251c38");
      }
    }
  }
  // 光る水晶（足元の奥と左右）
  const crystals: Array<[number, number, number]> = [[26, 126, 1.3], [58, 134, 0.9], [262, 122, 1.4], [292, 134, 1], [230, 130, 0.8], [100, 128, 0.7]];
  for (const [cx, cy, s] of crystals) {
    for (let k = 0; k < 3; k++) {
      const ox = (k - 1) * 6 * s, hgt = (16 - Math.abs(k - 1) * 6) * s;
      for (let y = 0; y < hgt; y++) {
        const hw = (4 * s) * (1 - y / hgt * 0.55);
        for (let xx = -hw; xx <= hw; xx++) px(ctx, cx + ox + xx, cy - y, xx < -hw * 0.2 ? "#b8f0ff" : xx < hw * 0.4 ? "#58c0e8" : "#2a78b0");
      }
    }
    ctx.fillStyle = "rgba(120,220,255,0.10)";
    ctx.fillRect(cx - 22 * s, cy - 18 * s, 44 * s, 22 * s);
  }
  // 床
  bands(ctx, w, 136, h, ["#2c2240", "#261e38", "#20182e", "#1a1426"]);
  for (let i = 0; i < 40; i++) {
    const x = hash(i, 14) * w, y = 140 + hash(i, 15) * (h - 144);
    px(ctx, x, y, "#3e3258", 5 + Math.floor(hash(i, 16) * 8), 1);
    px(ctx, x, y + 1, "#120e1c", 5 + Math.floor(hash(i, 16) * 8), 1);
  }
}

function desertBackdrop(ctx: Ctx, w: number, h: number): void {
  bands(ctx, w, 0, 96, ["#e87a4a", "#ee8e52", "#f4a05a", "#f8b468", "#fcc878", "#ffdc90", "#ffeaa8"]);
  for (let y = -12; y <= 12; y++) for (let x = -12; x <= 12; x++) if (x * x + y * y <= 144) px(ctx, 230 + x, 40 + y, x * x + y * y < 90 ? "#fff4c8" : "#ffe0a0");
  hills(ctx, w, h, 88, 4, 2.2, "#c8785a", "#e09a74");
  // 遠くの岩山（メサ）
  for (const [x, wd, ht] of [[40, 38, 22], [150, 52, 16], [270, 30, 26]] as Array<[number, number, number]>) {
    for (let yy = 0; yy < ht; yy++) for (let xx = 0; xx < wd; xx++) px(ctx, x + xx, 90 - yy, xx < wd * 0.3 ? "#b86a52" : xx < wd * 0.75 ? "#9a5642" : "#7a4234");
    for (let xx = 0; xx < wd; xx++) px(ctx, x + xx, 90 - ht, "#d08a68");
  }
  hills(ctx, w, h, 100, 9, 5.7, "#e8b46a", "#f8d896", "#c8944e");
  hills(ctx, w, h, 122, 7, 1.1, "#dca458", "#f2cc86", "#b88440");
  bands(ctx, w, 138, h, ["#d49a50", "#cc9048", "#c48640", "#bc7c38"]);
  for (let i = 0; i < 220; i++) {
    const x = hash(i, 5) * w, y = 124 + hash(i, 6) * (h - 124);
    px(ctx, x, y, "#f4d48a", 3, 1); px(ctx, x + 1, y + 1, "#a87438", 3, 1);
  }
}

function snowBackdrop(ctx: Ctx, w: number, h: number): void {
  bands(ctx, w, 0, 100, ["#a8b8d8", "#b8c8e4", "#c8d6ec", "#d8e2f2", "#e6edf8", "#f2f6fc"]);
  cloud(ctx, 80, 30, 2.2, "#f8fbff", "#d0dcf0");
  cloud(ctx, 240, 22, 1.8, "#f8fbff", "#d0dcf0");
  hills(ctx, w, h, 80, 10, 0.6, "#8aa0c8", "#b8c8e4", "#7088b0");
  hills(ctx, w, h, 100, 6, 3.3, "#dce8f6", "#ffffff", "#b8c8e0");
  for (let i = 0; i < 18; i++) {
    const x = 12 + i * 18 + hash(i, 1) * 8, y = 112 + hash(i, 2) * 10, s = 1 + hash(i, 3) * 0.6;
    for (let k = 0; k < 4; k++) {
      const wd = (3 + k * 2.4) * s, yy = y - 18 * s + k * 5 * s;
      for (let xx = -wd; xx <= wd; xx++) px(ctx, x + xx, yy + Math.abs(xx) * 0.3, xx < -wd * 0.2 ? "#3e7a5a" : "#245a40", 1, 5 * s);
      px(ctx, x - wd * 0.6, yy, "#f4fbff", Math.max(2, wd * 0.8), 1);
    }
    px(ctx, x - 1, y, "#4a3020", 2, 5);
  }
  bands(ctx, w, 120, h, ["#e8f0fa", "#dee8f6", "#d2deee", "#c6d4e8", "#bccce2"]);
  for (let i = 0; i < 160; i++) { const x = hash(i, 5) * w, y = 122 + hash(i, 6) * (h - 122); px(ctx, x, y, "#ffffff", 2, 1); px(ctx, x + 1, y + 1, "#a8b8d4", 2, 1); }
  for (let i = 0; i < 90; i++) px(ctx, hash(i, 8) * w, hash(i, 9) * h * 0.8, "#ffffff");
}

function ruinsBackdrop(ctx: Ctx, w: number, h: number): void {
  bands(ctx, w, 0, 110, ["#0e0a22", "#150f2e", "#1c1438", "#241a44", "#2e2252", "#3a2c62", "#4a3a74"]);
  for (let i = 0; i < 70; i++) px(ctx, hash(i, 1) * w, hash(i, 2) * 80, hash(i, 3) > 0.8 ? "#ffffff" : "#a8a0d8");
  for (let y = -10; y <= 10; y++) for (let x = -10; x <= 10; x++) if (x * x + y * y <= 100) px(ctx, 60 + x, 34 + y, x + y < -4 ? "#fff8e0" : x * x + y * y > 70 ? "#d8d0b8" : "#f0e8cc");
  hills(ctx, w, h, 96, 6, 2.5, "#2a2048", "#4a3a78");
  // 折れた柱の列
  const pillars: Array<[number, number, number]> = [[20, 70, 12], [70, 54, 12], [128, 62, 14], [204, 50, 14], [262, 68, 12], [300, 58, 10]];
  for (const [x, top, wd] of pillars) {
    for (let y = top; y < 120; y++) {
      for (let xx = 0; xx < wd; xx++) {
        const k = xx < wd * 0.25 ? "#6a5e98" : xx < wd * 0.7 ? "#4a4078" : "#30285a";
        px(ctx, x + xx, y, k);
      }
      if ((y - top) % 9 === 0) px(ctx, x, y, "#8478b8", wd, 1);
    }
    px(ctx, x - 2, top - 3, "#7a6eb0", wd + 4, 3);
    for (let i = 0; i < 4; i++) px(ctx, x + hash(x, i) * wd, top - 4 - i, "#4a4078", 2, 1);
  }
  // 床（遠近の石畳）
  bands(ctx, w, 118, h, ["#3a3066", "#342a5c", "#2e2452", "#281e48", "#221a3e"]);
  for (let r = 0; r < 12; r++) {
    const y = 120 + r * r * 0.45 + r * 2;
    if (y > h) break;
    px(ctx, 0, y, "#4e4488", w, 1);
    const cell = 14 + r * 3;
    for (let x = ((r % 2) * cell) / 2; x < w; x += cell) px(ctx, x, y, "#4e4488", 1, Math.max(2, r * 1.2));
  }
  ctx.fillStyle = "rgba(150,130,230,0.12)";
  ctx.fillRect(0, 108, w, 14);
}

const cache = new Map<string, HTMLCanvasElement>();

/** 戦闘の背景の絵（キャッシュ）。ブラウザ以外では null。 */
export function getBackdropCanvas(biome: Biome, w: number, h: number): HTMLCanvasElement | null {
  if (typeof document === "undefined") {
    return null;
  }
  const key = `${biome}:${w}x${h}`;
  const hit = cache.get(key);
  if (hit) {
    return hit;
  }
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return null;
  }
  ctx.imageSmoothingEnabled = false;
  switch (biome) {
    case "cave": caveBackdrop(ctx, w, h); break;
    case "desert": desertBackdrop(ctx, w, h); break;
    case "snow": snowBackdrop(ctx, w, h); break;
    case "ruins": ruinsBackdrop(ctx, w, h); break;
    default: grassBackdrop(ctx, w, h); break;
  }
  cache.set(key, canvas);
  return canvas;
}
