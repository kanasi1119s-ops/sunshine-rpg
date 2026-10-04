/**
 * 戦闘画面の背景（場所ごと）。画像ファイルは使わず、小さな絵を一度だけ描いて使い回す。
 * 空・遠景・近景の層（ディザでなじませた帯、雲、丘、木、洞窟の石筍と水晶、砂丘、雪の松、遺跡の柱）で奥行きを出す。
 */
import { EXTRA_BIOMES, paintExtraBackdrop, type ExtraBiome } from "./battle-backdrop-extra";

export type Biome = "grass" | "cave" | "desert" | "snow" | "ruins" | ExtraBiome;

/** 戦闘の背景の種類ぜんぶ（先に作っておくときに使う） */
export const ALL_BIOMES: Biome[] = ["grass", "cave", "desert", "snow", "ruins", ...EXTRA_BIOMES];

const BIOME_BY_PREFIX: Array<[string, Biome]> = [
  ["tetsukusari-mine", "cave"], ["deep-", "ruins"], ["kyotoukyu", "ruins"],
  ["god-shrine", "shrine"], ["tower-", "shrine"], ["kanou-", "shrine"], ["islet-1", "shrine"], ["islet-2", "lava"], ["islet-3", "coast"], ["islet-4", "sky"], ["islet-5", "deep"], ["islet-6", "lava"], ["shimohara", "snow"], ["sanone", "desert"], ["garasuko-warehouse", "cave"],
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
  // 丸い塊をいくつか重ねた雲。1ドットずつ、欠けなく塗る（上が明るく、下が青み）。底は平らに切る。
  const blobs: Array<[number, number, number]> = [[0, 0, 9], [-9, 3, 7], [9, 3, 7], [17, 5, 5], [-16, 5, 5], [4, -4, 6]];
  const rx = 1.35;
  const covered = (x: number, y: number): number => {
    let hit = -99;
    for (const [dx, dy, r] of blobs) {
      const nx = (x - dx * s) / (r * rx * s), ny = (y - dy * s * 0.7) / (r * s * 0.8);
      const d = nx * nx + ny * ny;
      if (d <= 1) hit = Math.max(hit, 1 - d);
    }
    return hit;
  };
  const x0 = Math.floor(-24 * s * rx), x1 = Math.ceil(24 * s * rx);
  const y0 = Math.floor(-14 * s), y1 = Math.ceil(10 * s);
  const bottom = 6 * s * 0.7;
  for (let y = y0; y <= y1; y++) {
    for (let x = x0; x <= x1; x++) {
      if (y > bottom) continue;
      const c = covered(x, y);
      if (c < 0) continue;
      const rim = covered(x + 1, y + 1) < 0 || covered(x, y + 1) < 0;
      const low = y > bottom - 3 * s * 0.7 || covered(x - 2, y - 2) < 0.02 && x > 0;
      px(ctx, cx + x, cy + y, rim && y > 0 ? shade : low ? shade : light);
    }
  }
}

/** 遠くの山並み。尾根をギザギザにして、左の面は明るく右の面は暗く、てっぺんに雪、ふもとは霞ませる。 */
function mountains(ctx: Ctx, w: number, baseY: number, seed: number, scale: number, lit: string, side: string, snow: string, haze: string): void {
  const peaks: Array<[number, number, number]> = [];
  for (let x = -10; x < w + 20; x += 52 + hash(seed, x) * 30) {
    peaks.push([x, (26 + hash(seed + 1, x) * 30) * scale, 40 + hash(seed + 2, x) * 24]);
  }
  for (let x = 0; x < w; x++) {
    let top = baseY;
    let face = 0;
    for (const [cx, ht, half] of peaks) {
      const d = Math.abs(x - cx) / half;
      if (d >= 1) continue;
      const jag = (hash(seed, Math.floor(x / 3)) - 0.5) * 3;
      const y = baseY - ht * (1 - d) + jag;
      if (y < top) {
        top = y;
        face = x < cx ? 0 : 1;
      }
    }
    const t = Math.round(top);
    if (t >= baseY) continue;
    const snowLine = t + Math.max(3, Math.round((baseY - t) * 0.22));
    for (let y = t; y < baseY; y++) {
      const dither = ((x + y) % 2 === 0);
      let c = face === 0 ? lit : side;
      if (y < snowLine - (dither ? 0 : 1) && baseY - t > 22) c = face === 0 ? snow : "#c8d6ea";
      const fog = (y - t) / (baseY - t);
      if (fog > 0.7 && dither) c = haze;
      px(ctx, x, y, c);
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
  cloud(ctx, 60, 26, 2, "#ffffff", "#d0e0f2");
  cloud(ctx, 210, 18, 2.4, "#ffffff", "#c8daee");
  cloud(ctx, 150, 52, 1.4, "#f8fbff", "#d4e4f2");
  cloud(ctx, 340, 46, 1.2, "#f8fbff", "#d4e4f2");
  mountains(ctx, w, 96, 3, 1.1, "#8aa8cc", "#6a88b0", "#f4f8ff", "#a8c4de");
  mountains(ctx, w, 100, 9, 0.6, "#7a9cc0", "#5e80a8", "#e8f0fa", "#98b8d4");
  hills(ctx, w, h, 100, 5, 1.3, "#6a9ab8", "#92bad0");
  hills(ctx, w, h, 104, 6, 4.1, "#4e8c58", "#7ac07a", "#3a7048");
  // 森：大小の木を2列、後ろの列は色を淡く（空気遠近）
  for (let i = 0; i < 30; i++) {
    const x = 4 + i * 10.5 + hash(i, 1) * 5;
    const y = 104 + Math.sin(x * 0.021 + 4.1) * 6 + Math.sin(x * 0.057 + 9.4) * 2.7;
    tree(ctx, x, y, 0.8 + hash(i, 2) * 0.35, "#6ab070", "#4a8a58", "#2e6842");
  }
  for (let i = 0; i < 20; i++) {
    const x = 8 + i * 15.5 + hash(i, 11) * 6;
    const y = 110 + Math.sin(x * 0.021 + 4.1) * 6 + Math.sin(x * 0.057 + 9.4) * 2.7 + 4;
    tree(ctx, x, y, 1.1 + (hash(i, 12) > 0.5 ? 0.35 : 0), "#5aa860", "#3a7e48", "#245a34");
  }
  bands(ctx, w, 116, h, ["#4a9a48", "#42903f", "#3a8638", "#337c32", "#2c722c", "#266826"]);
  // 草原をうねって奥へのびる小道（手前ほど幅広）
  for (let y = 118; y < h; y++) {
    const t = (y - 118) / (h - 118);
    const cx = 96 + Math.sin(y * 0.05) * (10 + 26 * t) + t * 24;
    const hw = 3 + t * 22;
    for (let x = Math.floor(cx - hw); x <= cx + hw; x++) {
      const edge = x < cx - hw + 1 || x > cx + hw - 1;
      px(ctx, x, y, edge ? "#8a6a3e" : hash(x, y) < 0.12 ? "#d8bc84" : hash(x, y + 9) < 0.1 ? "#a88852" : "#c4a468");
    }
  }
  for (let i = 0; i < 300; i++) {
    const x = hash(i, 5) * w, y = 120 + hash(i, 6) * (h - 120);
    const big = (y - 116) / (h - 116);
    px(ctx, x, y, "#7ac85a"); px(ctx, x - 1, y - 1 - big * 1.5, "#7ac85a"); px(ctx, x + 1, y - 1 - big * 1.5, "#7ac85a");
    px(ctx, x, y + 1, "#1e5a20");
  }
  for (let i = 0; i < 40; i++) {
    const x = hash(i, 7) * w, y = 122 + hash(i, 8) * (h - 128);
    const c = ["#ffffff", "#ffe060", "#ff8aa8"][i % 3];
    px(ctx, x, y, c); px(ctx, x + 1, y, c); px(ctx, x, y - 1, c); px(ctx, x, y + 1, "#2a7a2a");
  }
  // 手前の岩と茂み（大きく、濃く）
  for (const [bx, by, bs] of [[16, h - 8, 1.7], [372, h - 10, 1.9]] as Array<[number, number, number]>) {
    for (let yy = -9; yy <= 3; yy++) {
      for (let xx = -13; xx <= 13; xx++) {
        const n = (xx * xx) / 169 + (yy * yy) / 70;
        if (n > 1) continue;
        const lum = -xx * 0.04 - yy * 0.08;
        px(ctx, bx + xx * bs * 0.7, by + yy * bs * 0.8, lum > 0.45 ? "#4a9a50" : lum > 0 ? "#2e7a3c" : "#1c5a2c", Math.ceil(bs * 0.7), Math.ceil(bs * 0.8));
      }
    }
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
    // 水晶のまわりのやわらかい光（四角ではなく丸く広がる）
    const glow = ctx.createRadialGradient(cx, cy - 8 * s, 2, cx, cy - 8 * s, 30 * s);
    glow.addColorStop(0, "rgba(120,220,255,0.22)");
    glow.addColorStop(1, "rgba(120,220,255,0)");
    ctx.fillStyle = glow;
    ctx.fillRect(cx - 32 * s, cy - 40 * s, 64 * s, 64 * s);
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
  // 遠くの岩山（メサ）: 横の地層のしま、てっぺんは段々に崩れ、右の面は影
  for (const [x, wd, ht] of [[24, 44, 24], [118, 30, 14], [170, 58, 18], [262, 34, 28], [330, 40, 16]] as Array<[number, number, number]>) {
    for (let xx = 0; xx < wd; xx++) {
      const step = Math.floor(hash(x, Math.floor(xx / 5)) * 4);
      const top = ht - (xx < 3 || xx > wd - 4 ? 3 : 0) - step;
      for (let yy = 0; yy < top; yy++) {
        const strata = Math.floor((yy + x) / 4) % 3;
        const shadow = xx > wd * 0.72;
        const base = shadow ? ["#7a4234", "#6e3a2e", "#84483a"] : ["#b86a52", "#a85e48", "#c47458"];
        px(ctx, x + xx, 90 - yy, base[strata]);
      }
      px(ctx, x + xx, 90 - top, "#d89070");
    }
  }
  hills(ctx, w, h, 100, 9, 5.7, "#e8b46a", "#f8d896", "#c8944e");
  hills(ctx, w, h, 122, 7, 1.1, "#dca458", "#f2cc86", "#b88440");
  bands(ctx, w, 138, h, ["#d49a50", "#cc9048", "#c48640", "#bc7c38"]);
  for (let i = 0; i < 220; i++) {
    const x = hash(i, 5) * w, y = 124 + hash(i, 6) * (h - 124);
    px(ctx, x, y, "#f4d48a", 3, 1); px(ctx, x + 1, y + 1, "#a87438", 3, 1);
  }
  // 手前のサボテン（左が明るく、右が暗い。腕つき）
  for (const [cx, cy, sc] of [[372, 160, 0.9], [14, 150, 0.6]] as Array<[number, number, number]>) {
    const bodyH = Math.round(30 * sc), bw = Math.max(2, Math.round(3.4 * sc));
    for (let yy = 0; yy < bodyH; yy++) {
      for (let xx = -bw; xx <= bw; xx++) {
        px(ctx, cx + xx, cy - yy, xx < -bw * 0.3 ? "#5aa05a" : xx < bw * 0.5 ? "#3e8040" : "#2a5e30");
      }
      px(ctx, cx - bw - 1, cy - yy, "#1e4426");
      px(ctx, cx + bw + 1, cy - yy, "#1e4426");
    }
    for (const dir of [-1, 1]) {
      const ay = cy - Math.round(bodyH * (dir < 0 ? 0.45 : 0.62));
      for (let k = 0; k < Math.round(8 * sc); k++) {
        px(ctx, cx + dir * (bw + 1 + k), ay, "#3e8040", 1, Math.round(4 * sc));
      }
      for (let k = 0; k < Math.round(10 * sc); k++) {
        px(ctx, cx + dir * (bw + 1 + Math.round(8 * sc)), ay - k, "#3e8040", Math.round(4 * sc), 1);
      }
    }
    px(ctx, cx - bw, cy + 1, "rgba(60,30,10,0.35)", bw * 4, 3);
  }
}

function snowBackdrop(ctx: Ctx, w: number, h: number): void {
  bands(ctx, w, 0, 100, ["#a8b8d8", "#b8c8e4", "#c8d6ec", "#d8e2f2", "#e6edf8", "#f2f6fc"]);
  cloud(ctx, 80, 30, 2.2, "#f8fbff", "#d0dcf0");
  cloud(ctx, 240, 22, 1.8, "#f8fbff", "#d0dcf0");
  mountains(ctx, w, 92, 5, 1.2, "#9ab0d4", "#7890b8", "#ffffff", "#c0d0e8");
  hills(ctx, w, h, 92, 6, 0.6, "#8aa0c8", "#b8c8e4", "#7088b0");
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
    default:
      if (EXTRA_BIOMES.includes(biome as ExtraBiome)) {
        paintExtraBackdrop(biome as ExtraBiome, ctx, w, h);
      } else {
        grassBackdrop(ctx, w, h);
      }
      break;
  }
  cache.set(key, canvas);
  return canvas;
}
