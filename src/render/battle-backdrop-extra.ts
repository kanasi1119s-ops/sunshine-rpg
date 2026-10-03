/**
 * 戦闘画面の背景（追加の6つ）。battle-backdrop.ts と同じ作り方（画像ファイルなし・Canvas 2D で一度だけ描く）。
 * 規則: 光は左上、ハイライト（照り）は使わない、ディザは市松、色は帯ごとに5〜7段、奥ほど淡く手前ほど濃く。
 * 画面の下側は戦闘のウィンドウや名前の表示が重なるので、見せ場は中ほどに置く。
 *
 * 本体に組み込むには tools/backdrop-preview/README.md を読むこと。
 */
export type ExtraBiome = "forest" | "swamp" | "coast" | "sky" | "lava" | "shrine" | "deep";

export const EXTRA_BIOMES: ExtraBiome[] = ["forest", "swamp", "coast", "sky", "lava", "shrine", "deep"];

type Ctx = CanvasRenderingContext2D;

// ---------------------------------------------------------------- 部品

function hash(a: number, b: number): number {
  let h = (Math.floor(a) * 374761393 + Math.floor(b) * 668265263) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

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
      // 境目の1つ上の行は逆の市松（なだらかに見せる）
      ctx.fillStyle = colors[i];
      for (let x = 0; x < w; x++) {
        if ((x + yb) % 2 === 1) {
          ctx.fillRect(x, yb, 1, 1);
        }
      }
    }
  }
}

/** 半透明の色を市松で塗る（霧・光の筋・赤い光に使う）。 */
function dither(ctx: Ctx, x: number, y: number, w: number, h: number, color: string): void {
  ctx.fillStyle = color;
  for (let yy = 0; yy < h; yy++) {
    for (let xx = 0; xx < w; xx++) {
      if ((x + xx + y + yy) % 2 === 0) {
        ctx.fillRect(x + xx, y + yy, 1, 1);
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
      const k = Math.round(2 + Math.sin(x * 0.04 + seed) * 1.5);
      px(ctx, x, top + 1, rim);
      for (let i = 0; i < k; i++) {
        if ((x + i) % 2 === 0) px(ctx, x, top + 3 + i, shade);
      }
    }
  }
}

/** 雲。丸い塊を重ね、上が明るく下が影。底は平ら。 */
function cloud(ctx: Ctx, cx: number, cy: number, s: number, light: string, shade: string): void {
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
      const low = y > bottom - 3 * s * 0.7 || (covered(x - 2, y - 2) < 0.02 && x > 0);
      px(ctx, cx + x, cy + y, rim && y > 0 ? shade : low ? shade : light);
    }
  }
}

/** 雲海の一列。もこもこの上の縁。右へ下る斜面は影。 */
function cloudBank(ctx: Ctx, w: number, h: number, base: number, amp: number, seed: number, top: string, mid: string, shade: string): void {
  const yAt = (x: number): number =>
    base - amp * (Math.abs(Math.sin(x * 0.034 + seed)) * 0.62 + Math.abs(Math.sin(x * 0.09 + seed * 2.1)) * 0.28 + Math.abs(Math.sin(x * 0.21 + seed * 3.3)) * 0.1);
  for (let x = 0; x < w; x++) {
    const t = Math.round(yAt(x));
    const slope = yAt(x + 2) - yAt(x - 2);
    ctx.fillStyle = mid;
    ctx.fillRect(x, t, 1, h - t);
    px(ctx, x, t, top);
    px(ctx, x, t + 1, top);
    if (slope > 0.25) {
      // 右へ下る面は影（市松で2〜4行）
      const k = Math.min(5, Math.round(slope * 2.2) + 2);
      for (let i = 0; i < k; i++) {
        if ((x + i) % 2 === 0 || i < 2) px(ctx, x, t + 2 + i, shade);
      }
    } else if (slope < -0.25 && (x + t) % 2 === 0) {
      px(ctx, x, t + 2, top);
    }
  }
}

function disc(ctx: Ctx, cx: number, cy: number, r: number, pick: (dx: number, dy: number, d2: number) => string | null): void {
  for (let y = -r; y <= r; y++) {
    for (let x = -r; x <= r; x++) {
      const d2 = x * x + y * y;
      if (d2 > r * r) continue;
      const c = pick(x, y, d2);
      if (c) px(ctx, cx + x, cy + y, c);
    }
  }
}

function glow(ctx: Ctx, cx: number, cy: number, r: number, rgb: string, a0: number): void {
  const g = ctx.createRadialGradient(cx, cy, 1, cx, cy, r);
  g.addColorStop(0, `rgba(${rgb},${a0})`);
  g.addColorStop(1, `rgba(${rgb},0)`);
  ctx.fillStyle = g;
  ctx.fillRect(Math.round(cx - r), Math.round(cy - r), r * 2, r * 2);
}

/** 幹。左が明るく右が暗い4段。樹皮の縦すじ。lit=苔の色（左側の下の方に付く）。 */
function trunk(ctx: Ctx, x: number, y0: number, y1: number, wd: number, cols: [string, string, string, string], seed: number, moss?: [string, string], flareK = 0.55): void {
  for (let y = y0; y < y1; y++) {
    const flare = Math.max(0, y - (y1 - 16)) * flareK;
    const cx = x + Math.sin(y * 0.018 + seed) * 2;
    const hw = wd / 2 + flare;
    for (let xx = Math.floor(-hw); xx <= hw; xx++) {
      const t = (xx + hw) / (2 * hw + 1);
      let c = t < 0.2 ? cols[0] : t < 0.58 ? cols[1] : t < 0.86 ? cols[2] : cols[3];
      if (hash(Math.floor(xx * 0.8) + seed * 7, Math.floor(y / 5)) < 0.14) c = t < 0.58 ? cols[2] : cols[3];
      if (moss && t < 0.55 && y > y0 + (y1 - y0) * 0.4 && hash(xx + seed, Math.floor(y / 2)) < 0.28 + (y - y0) / (y1 - y0) * 0.35) {
        c = t < 0.25 ? moss[0] : moss[1];
      }
      px(ctx, cx + xx, y, c);
    }
  }
}

// ---------------------------------------------------------------- 1. 深い森

function lightShaft(ctx: Ctx, x0: number, slope: number, hw0: number, spread: number, yStart: number, yEnd: number, seed: number): void {
  for (let y = yStart; y < yEnd; y++) {
    const cx = x0 + y * slope;
    const hw = hw0 + (y - yStart) * spread;
    const fade = 1 - (y - yStart) / (yEnd - yStart) * 0.6;
    for (let x = Math.floor(cx - hw); x <= cx + hw; x++) {
      const d = Math.abs(x - cx) / hw;
      const n = hash(x + seed, Math.floor(y / 3));
      if (d > 0.82 && (x + y) % 2 === 0) continue;
      if (n > fade + 0.25) continue;
      ctx.fillStyle = d < 0.45 ? "rgba(255,246,176,0.30)" : d < 0.8 ? "rgba(255,240,160,0.18)" : "rgba(255,236,150,0.10)";
      ctx.fillRect(x, y, 1, 1);
    }
  }
}

function fern(ctx: Ctx, x: number, y: number, s: number, light: string, dark: string): void {
  for (let k = -3; k <= 3; k++) {
    const len = (7 - Math.abs(k) * 1.2) * s;
    for (let i = 0; i < len; i++) {
      const fx = x + k * i * 0.5 * s;
      const fy = y - i * 0.9 - (i * i) * 0.045 * (k === 0 ? 0.3 : 1) + Math.abs(k) * 0.8;
      px(ctx, fx, fy, k <= 0 ? light : dark);
      if (i % 2 === 0) px(ctx, fx + (k <= 0 ? -1 : 1), fy + 1, dark);
    }
  }
}

function forestBackdrop(ctx: Ctx, w: number, h: number): void {
  // 空気遠近: 上は濃い葉の影、地平は霞んで明るい
  bands(ctx, w, 0, 126, ["#0c261f", "#12342a", "#1a4430", "#265a3a", "#3a7448", "#5e9660", "#92bc84"]);
  // 奥の幹（霞に溶ける、細い。間隔も太さもばらばら）
  for (let i = 0; i < 24; i++) {
    const x = 4 + i * 17 + hash(i, 1) * 14;
    const far = hash(i, 5) > 0.5;
    trunk(ctx, x, 16, 126, 3 + hash(i, 2) * 4, far ? ["#86b27c", "#78a572", "#6c9a68", "#628f60"] : ["#7aa874", "#6a9a68", "#5c8a5c", "#52804f"], i, undefined, 0.15);
  }
  // 霞の層
  for (let y = 70; y < 128; y += 2) dither(ctx, 0, y, w, 1, `rgba(190,226,170,${((y - 70) / 58) * 0.22})`);
  // 奥の茂み（地平線ぎわ）
  for (let i = 0; i < 34; i++) {
    const x = hash(i, 61) * w, y = 124 + hash(i, 62) * 4, r = 6 + Math.floor(hash(i, 63) * 6);
    disc(ctx, x, y - 2, r, (dx, dy) => (dx + dy * 1.2 < -r * 0.35 ? "#5a9058" : dx + dy < r * 0.3 ? "#487e4c" : "#386a3e"));
  }
  // 中ほどの幹（太さと高さにばらつき、枝が張り出す）
  for (let i = 0; i < 7; i++) {
    const x = 30 + i * 52 + hash(i, 3) * 30;
    const wd = 8 + hash(i, 4) * 8;
    trunk(ctx, x, 6, 134, wd, ["#4a7a4e", "#3a6640", "#2c5232", "#22442a"], i + 40, ["#6aa05a", "#4a8648"], 0.4);
  }
  // 木漏れ日の筋（左上から右下へ）
  lightShaft(ctx, 58, 0.34, 6, 0.08, 0, 150, 1);
  lightShaft(ctx, 150, 0.34, 9, 0.1, 0, 160, 2);
  lightShaft(ctx, 246, 0.34, 7, 0.09, 0, 150, 3);
  lightShaft(ctx, 318, 0.34, 10, 0.1, 0, 164, 4);
  // 天井の葉（上の縁にかかる濃い葉の房）
  for (let x = 0; x < w; x++) {
    const d = 9 + Math.sin(x * 0.07) * 4 + Math.sin(x * 0.19 + 1) * 3 + hash(x, 5) * 4;
    ctx.fillStyle = "#07180f";
    ctx.fillRect(x, 0, 1, Math.round(d));
    for (let y = Math.round(d) - 5; y < d + 4; y++) {
      if ((x + y) % 2 === 0 && hash(x, y) < 0.55) px(ctx, x, y, y < d ? "#0e2a1a" : "#143a24");
    }
    if (hash(Math.floor(x / 2), 9) < 0.3) px(ctx, x, d + 1, "#2a6a3a");
  }
  // 地面（苔と落ち葉）。なだらかな起伏を3つ重ねる
  bands(ctx, w, 124, h, ["#4c7c44", "#42703c", "#386434", "#2e582e"]);
  hills(ctx, w, h, 146, 3, 0.7, "#336030", "#5a9650", "#2a5028");
  hills(ctx, w, h, 172, 4, 2.9, "#2a5228", "#4a8444", "#204420");
  hills(ctx, w, h, 200, 4, 5.1, "#1f4022", "#386c36", "#18341c");
  for (let i = 0; i < 380; i++) {
    const x = hash(i, 11) * w, y = 128 + hash(i, 12) * (h - 128);
    const c = hash(i, 13);
    px(ctx, x, y, c < 0.4 ? "#6aa050" : c < 0.7 ? "#7a6a38" : "#173218", 2 + Math.floor(hash(i, 14) * 3), 1);
  }
  // 倒れた苔むす丸太（右、手前寄り）
  for (let x = 236; x < 332; x++) {
    const sag = Math.sin((x - 236) * 0.03) * 2;
    for (let k = 0; k < 11; k++) {
      const t = k / 10;
      let c = t < 0.2 ? "#5a8c4a" : t < 0.45 ? "#4a7a40" : t < 0.75 ? "#3a5e32" : "#2a4426";
      if (hash(x, k + 3) < 0.15) c = "#26402a";
      if (k < 4 && hash(Math.floor(x / 2), k) < 0.45) c = "#6aa05a";
      px(ctx, x, 176 + sag + k, c);
    }
  }
  disc(ctx, 236, 181, 6, (_dx, _dy, d2) => (d2 < 7 ? "#7a6240" : d2 < 20 ? "#5a4a32" : "#3e3a28"));
  // 木漏れ日が当たった地面（丸い光だまり、市松のふち）
  for (const [cx, cy, rx] of [[110, 170, 26], [230, 185, 32], [330, 160, 22]] as Array<[number, number, number]>) {
    for (let y = -7; y <= 7; y++) {
      for (let x = -rx; x <= rx; x++) {
        const d = (x * x) / (rx * rx) + (y * y) / 49;
        if (d > 1) continue;
        if (d > 0.7 && (x + y) % 2 === 0) continue;
        ctx.fillStyle = d < 0.4 ? "rgba(255,244,160,0.30)" : "rgba(255,244,160,0.16)";
        ctx.fillRect(cx + x, cy + y, 1, 1);
      }
    }
  }
  // 手前の太い幹（両端、苔むして根が張る）
  trunk(ctx, 14, 0, h + 2, 34, ["#3c6a3c", "#2e5230", "#223e26", "#192e1d"], 91, ["#5a9a50", "#3e7a3c"]);
  trunk(ctx, 388, 0, h + 2, 40, ["#3a6638", "#2c4e2e", "#203a24", "#162a1a"], 92, ["#5a9a50", "#3e7a3c"]);
  // しだ
  for (const [x, y, s] of [[60, 205, 1.5], [96, 150, 0.8], [292, 148, 0.9], [330, 208, 1.6], [176, 156, 0.7], [44, 160, 1]] as Array<[number, number, number]>) {
    fern(ctx, x, y, s, "#6ab25a", "#2e6a34");
  }
  // 舞う光の粒
  for (let i = 0; i < 46; i++) {
    const x = hash(i, 21) * w, y = 20 + hash(i, 22) * 150;
    px(ctx, x, y, hash(i, 23) > 0.5 ? "#fff4b0" : "#d8f0a0");
  }
}

// ---------------------------------------------------------------- 2. 沼

function deadTree(ctx: Ctx, x: number, y: number, hgt: number, th: number, seed: number, light: string, dark: string): void {
  // 幹はゆるく曲がって上へ。枝は左右へ折れ曲がりながら細くなる。
  const branch = (bx: number, by: number, dir: number, len: number, t: number, depth: number): void => {
    let cx = bx, cy = by;
    for (let i = 0; i < len; i++) {
      cx += dir * (0.9 + hash(seed + depth, i) * 0.4);
      cy -= 0.35 + hash(seed + depth * 3, Math.floor(i / 3)) * 0.7 - (i > len * 0.6 ? 0.5 : 0);
      px(ctx, cx, cy, dark, Math.max(1, Math.round(t)), Math.max(1, Math.round(t)));
      if (dir < 0 && t >= 2) px(ctx, cx - 1, cy, light);
      if (depth < 2 && i === Math.floor(len * 0.55)) branch(cx, cy, -dir, Math.round(len * 0.55), t * 0.6, depth + 1);
      if (depth < 2 && i === Math.floor(len * 0.8)) branch(cx, cy, dir, Math.round(len * 0.4), t * 0.5, depth + 1);
    }
  };
  for (let i = 0; i < hgt; i++) {
    const t = th * (1 - (i / hgt) * 0.7);
    const cx = x + Math.sin(i * 0.05 + seed) * 3 - i * 0.04;
    const hw = Math.max(1, Math.round(t));
    ctx.fillStyle = dark;
    ctx.fillRect(Math.round(cx - hw), y - i, hw * 2, 1);
    if (hw >= 2) px(ctx, cx - hw, y - i, light, Math.max(1, Math.round(hw * 0.6)), 1);
    if (i > hgt * 0.35 && i % Math.floor(hgt / 4) === 0) {
      branch(cx, y - i, i % 2 === 0 ? -1 : 1, Math.round(10 + hash(seed, i) * 10 + th * 3), Math.max(1, t * 0.5), 0);
    }
  }
  branch(x - 2, y - hgt, -1, Math.round(8 + th * 2), Math.max(1, th * 0.4), 0);
  branch(x + 2, y - hgt, 1, Math.round(9 + th * 2), Math.max(1, th * 0.4), 1);
}

function swampBackdrop(ctx: Ctx, w: number, h: number): void {
  // 夕暮れの空
  bands(ctx, w, 0, 104, ["#30244c", "#46305c", "#64406a", "#85506c", "#a86670", "#c88074", "#e49a78", "#f2b886"]);
  // 低い太陽（半分は霧にかくれる）
  disc(ctx, 262, 94, 16, (_dx, dy, d2) => (dy > 8 ? null : d2 > 200 ? "#f4a870" : d2 > 120 ? "#f8c488" : "#fcdca0"));
  glow(ctx, 262, 94, 70, "255,190,120", 0.28);
  // 細くたなびく雲
  for (const [cx, cy, s, a] of [[70, 34, 1.7, 0], [200, 26, 2.1, 1], [330, 52, 1.3, 2], [120, 66, 1.1, 3]] as Array<[number, number, number, number]>) {
    cloud(ctx, cx, cy, s, a % 2 === 0 ? "#b88aa0" : "#c898a4", "#7a5072");
  }
  // 遠い枯れ林と岸のシルエット
  hills(ctx, w, h, 100, 3, 0.8, "#6a4a64", "#8a6078");
  for (let i = 0; i < 15; i++) {
    const x = 10 + i * 27 + hash(i, 1) * 16;
    deadTree(ctx, x, 106, 14 + hash(i, 2) * 16, 1, i + 3, "#8a6a80", "#5a3e58");
  }
  // 水面（空を映して濁る）
  bands(ctx, w, 104, h, ["#8a6a74", "#78606c", "#675564", "#584a5a", "#4a3f4e", "#3e3542", "#322b38"]);
  // 夕日の映り込み（縦に揺れる帯。きらめき）
  for (let y = 108; y < 170; y += 2) {
    const wd = 4 + (y - 108) * 0.28;
    const off = Math.sin(y * 0.6) * 6;
    for (let x = -wd; x <= wd; x++) {
      if (hash(x + 9, y) > 0.8 - (170 - y) / 100) continue;
      px(ctx, 262 + off + x, y, (x + y) % 4 === 0 ? "#fcdca0" : "#e8a070", 1 + (hash(x, y) > 0.5 ? 1 : 0), 1);
    }
  }
  // さざ波（奥は細かく、手前は長く）
  for (let i = 0; i < 160; i++) {
    const y = 110 + Math.pow(hash(i, 5), 1.4) * (h - 110);
    const len = 3 + (y - 106) * 0.08 + hash(i, 6) * 5;
    const x = hash(i, 7) * w;
    px(ctx, x, y, hash(i, 8) > 0.5 ? "#a08490" : "#2a2230", len, 1);
  }
  // 霧（水面にたちこめる市松の層）
  for (let y = 100; y < 150; y += 2) {
    const a = 0.2 - Math.abs(y - 118) / 200;
    dither(ctx, 0, y, w, 1, `rgba(232,200,208,${Math.max(0.04, a)})`);
  }
  // 泥の岸と枯れ木（中景）
  for (const [x, hgt, th, s] of [[52, 78, 3, 11], [342, 90, 3.4, 21], [168, 54, 2, 31]] as Array<[number, number, number, number]>) {
    const by = 138 + (x === 168 ? -6 : 6);
    // 水に映る影
    for (let i = 0; i < hgt * 0.5; i++) {
      if (i % 2 === 0) px(ctx, x - 4 + Math.sin(i * 0.8) * 2, by + 2 + i, "rgba(30,20,36,0.5)", 8 - i * 0.1, 1);
    }
    deadTree(ctx, x, by, hgt, th, s, "#7a5a72", "#2c1e34");
    px(ctx, x - 10, by, "#2a2030", 22, 3);
    px(ctx, x - 8, by - 1, "#3a2c40", 14, 1);
  }
  // 浮かぶ草（水草の島）
  for (let i = 0; i < 26; i++) {
    const x = hash(i, 31) * w, y = 128 + Math.pow(hash(i, 32), 1.2) * 70;
    const s = 1 + (y - 128) / 40;
    const rx = Math.round(4 * s), ry = Math.max(1, Math.round(1.2 * s));
    for (let yy = -ry; yy <= ry; yy++) {
      for (let xx = -rx; xx <= rx; xx++) {
        if ((xx * xx) / (rx * rx) + (yy * yy) / (ry * ry + 0.01) > 1) continue;
        px(ctx, x + xx, y + yy, yy < 0 ? "#6e9a4a" : xx < 0 ? "#4e7a3a" : "#34582c");
      }
    }
    if (hash(i, 33) > 0.6) px(ctx, x + 1, y - ry - 1, "#e8d8a0", 2, 1);
  }
  // 手前の岸（暗い泥）と、葦・がま
  hills(ctx, w, h, 206, 3, 4.4, "#1e1826", "#3a2e42", "#2a2034");
  for (let i = 0; i < 40; i++) {
    const side = i % 2 === 0;
    const x = side ? hash(i, 41) * 90 : 310 + hash(i, 42) * 90;
    const base = 214, hgt = 24 + hash(i, 43) * 38;
    for (let k = 0; k < hgt; k++) {
      const bend = Math.sin(k * 0.06 + i) * 2 + (side ? k * 0.03 : -k * 0.03);
      px(ctx, x + bend, base - k, k > hgt - 9 ? "#3a2a22" : "#38502c");
      if (k > 3 && k < hgt - 12 && k % 7 === 0) px(ctx, x + bend + (k % 2 ? -2 : 1), base - k, "#4e7038", 2, 1);
    }
    if (hash(i, 44) > 0.45) px(ctx, x + Math.sin(hgt * 0.06 + i) * 2 - 1, base - hgt, "#4a3226", 3, 8);
  }
  // ほたる状の淡い光
  for (let i = 0; i < 18; i++) px(ctx, hash(i, 51) * w, 120 + hash(i, 52) * 70, "#d8e8a0");
}

// ---------------------------------------------------------------- 3. 海辺

function rock(ctx: Ctx, cx: number, by: number, rw: number, rh: number, seed: number, cols: [string, string, string, string]): void {
  // 左が明るく右が暗い岩。上の縁はごつごつ。底に影。
  for (let xx = -rw; xx <= rw; xx++) {
    const u = xx / rw;
    const top = rh * (1 - Math.pow(Math.abs(u), 1.7)) * (0.85 + hash(seed, Math.floor(xx / 3)) * 0.3);
    for (let y = 0; y < top; y++) {
      const lum = -u * 0.6 + (y / top) * 0.3 - 0.1;
      let c = lum < -0.22 ? cols[0] : lum < 0.12 ? cols[1] : lum < 0.4 ? cols[2] : cols[3];
      if (hash(xx + seed, Math.floor(y / 3)) < 0.12) c = cols[2];
      px(ctx, cx + xx, by - y, c);
    }
  }
  px(ctx, cx - rw, by, "rgba(40,30,20,0.35)", rw * 2 + 3, 2);
}

function gull(ctx: Ctx, x: number, y: number, s: number): void {
  for (let i = 0; i <= 3 * s; i++) {
    px(ctx, x - i, y - Math.round(i * 0.5), "#ffffff");
    px(ctx, x + i + 1, y - Math.round(i * 0.5), "#ffffff");
  }
  px(ctx, x, y + 1, "#c8d4e4", 2, 1);
}

function coastBackdrop(ctx: Ctx, w: number, h: number): void {
  bands(ctx, w, 0, 92, ["#3a84d4", "#4c98dc", "#62aae4", "#7ebcec", "#9ccef2", "#bcdff6", "#dcf0f8"]);
  cloud(ctx, 76, 28, 2.1, "#ffffff", "#cfe0f2");
  cloud(ctx, 232, 20, 1.7, "#ffffff", "#c8dcf0");
  cloud(ctx, 338, 50, 1.5, "#f8fcff", "#d2e4f4");
  cloud(ctx, 160, 62, 1.0, "#f8fcff", "#d4e6f4");
  // 水平線の海（奥は濃く、手前は明るい青緑）
  bands(ctx, w, 90, 146, ["#2a68a8", "#2e78b6", "#3688c0", "#4098c8", "#4ca8ce", "#5cb8d0", "#72c8d2"]);
  // 遠くの島のかげ
  for (let x = 250; x < 340; x++) {
    const u = (x - 295) / 45;
    const t = Math.round(90 - 12 * Math.max(0, 1 - u * u) - hash(x, 1) * 1.5);
    for (let y = t; y < 91; y++) px(ctx, x, y, y - t < 3 ? "#7c9a9c" : (x + y) % 2 ? "#6a8aa8" : "#7494b0");
  }
  // 帆かげ
  for (let i = 0; i < 12; i++) px(ctx, 120 + i * 0.3, 78 + i * 0.9, "#f8f4ea", Math.max(1, 6 - Math.floor(i / 2)), 1);
  px(ctx, 117, 89, "#6a4a38", 12, 1);
  // 波の筋（奥は短く、手前は長く）。きらめきは光る物
  for (let i = 0; i < 230; i++) {
    const y = 93 + Math.pow(hash(i, 5), 1.3) * 52;
    const len = 2 + (y - 90) * 0.18 + hash(i, 6) * 5;
    const x = hash(i, 7) * w;
    px(ctx, x, y, hash(i, 8) > 0.35 ? "#8ad0e0" : "#2a6aa4", len, 1);
    if (hash(i, 9) > 0.55) px(ctx, x + 1, y + 1, "#2a6aa4", len - 1, 1);
  }
  for (let i = 0; i < 46; i++) {
    const x = 200 + (hash(i, 10) - 0.5) * 220 * (0.4 + hash(i, 11)), y = 94 + hash(i, 12) * 46;
    px(ctx, x, y, "#ffffff", 1 + Math.floor(hash(i, 13) * 2), 1);
  }
  // 砂浜（波うちぎわ）
  const shore = (x: number): number => 142 + Math.sin(x * 0.03 + 1) * 5 + Math.sin(x * 0.09) * 2 + x * 0.015;
  for (let x = 0; x < w; x++) {
    const s0 = Math.round(shore(x));
    // 浅瀬（青緑がかった薄色）
    for (let y = s0 - 6; y < s0; y++) {
      px(ctx, x, y, y < s0 - 3 ? ((x + y) % 2 ? "#78d0d2" : "#6cc4d0") : (x + y) % 2 ? "#a4e0d6" : "#90d8d4");
    }
    // 泡
    px(ctx, x, s0 - 1 - ((x * 7) % 3 === 0 ? 1 : 0), "#ffffff");
    if (hash(x, 3) > 0.7) px(ctx, x, s0 - 3, "#ffffff");
    // 濡れた砂 → 乾いた砂
    const cols = ["#b8a07c", "#c8b088", "#d8c498", "#e4d2a6", "#ecdcb4", "#e6d4a8", "#dcc89a", "#d0bc8e"];
    for (let k = 0; k < 8; k++) {
      const ya = s0 + 1 + k * 8, yb = s0 + 1 + (k + 1) * 8;
      ctx.fillStyle = cols[k];
      ctx.fillRect(x, ya, 1, (k === 7 ? h : Math.min(h, yb)) - ya);
      if (k < 7 && (x + yb) % 2 === 0) px(ctx, x, yb - 1, cols[k + 1]);
    }
    px(ctx, x, s0, "#8a7458");
  }
  for (let i = 0; i < 260; i++) {
    const x = hash(i, 21) * w, y = 150 + hash(i, 22) * (h - 150);
    if (y < shore(x) + 4) continue;
    px(ctx, x, y, hash(i, 23) > 0.5 ? "#f4e8c4" : "#a8906a", 2, 1);
  }
  // 岩（左は大きく、右は小さめ。波が足もとに）
  rock(ctx, 38, 168, 36, 44, 3, ["#8a8aa0", "#6c6e88", "#54566e", "#3e4058"]);
  rock(ctx, 74, 172, 20, 24, 8, ["#8a8aa0", "#6c6e88", "#54566e", "#3e4058"]);
  rock(ctx, 352, 176, 28, 30, 5, ["#8a8aa0", "#6c6e88", "#54566e", "#3e4058"]);
  rock(ctx, 316, 166, 14, 14, 9, ["#8a8aa0", "#6c6e88", "#54566e", "#3e4058"]);
  // 岩の上の海草と貝がら
  for (let i = 0; i < 9; i++) px(ctx, 20 + i * 4, 128 - hash(i, 61) * 4, "#3a7a4a", 2, 3);
  // 海辺の草
  for (let i = 0; i < 16; i++) {
    const x = 118 + i * 9, y = 202 + hash(i, 71) * 14;
    for (let k = 0; k < 7; k++) {
      px(ctx, x + k * 0.45, y - k * 1.5, "#6a9a4a");
      px(ctx, x - k * 0.45, y - k * 1.3, "#4a7a3a");
    }
  }
  // かもめ
  gull(ctx, 150, 44, 3);
  gull(ctx, 178, 56, 2);
  gull(ctx, 296, 34, 3);
  gull(ctx, 352, 70, 2);
  gull(ctx, 60, 70, 2);
}

// ---------------------------------------------------------------- 4. 空の上

function floatIsland(ctx: Ctx, cx: number, top: number, wd: number, depth: number, seed: number, pal: { grass: string; grassDark: string; rockL: string; rockM: string; rockD: string }): void {
  for (let xx = -wd; xx <= wd; xx++) {
    const u = xx / wd;
    const topY = top + Math.pow(Math.abs(u), 3) * 3;
    const bot = top + 4 + depth * Math.pow(1 - Math.abs(u), 1.15) * (0.8 + hash(seed, Math.floor(xx / 3)) * 0.4);
    for (let y = Math.round(topY); y < bot; y++) {
      const dy = y - topY;
      let c: string;
      if (dy < 2) c = xx < wd * 0.3 ? pal.grass : pal.grassDark;
      else if (dy < 4 && (xx + y) % 2 === 0) c = pal.grassDark;
      else c = u < -0.25 ? pal.rockL : u < 0.35 ? pal.rockM : pal.rockD;
      if (dy >= 4 && hash(xx + seed, Math.floor(y / 3)) < 0.14) c = u < 0.1 ? pal.rockM : pal.rockD;
      px(ctx, cx + xx, y, c);
    }
  }
  // 上の小さな木
  for (let i = 0; i < Math.floor(wd / 9); i++) {
    const x = cx - wd * 0.7 + i * (wd * 1.3 / Math.max(1, Math.floor(wd / 9))) + hash(seed, i) * 4;
    disc(ctx, Math.round(x), Math.round(top - 3), 3, (dx, dy) => (dx + dy < -1 ? pal.grass : pal.grassDark));
    px(ctx, x, top - 1, pal.rockD, 1, 2);
  }
}

function skyBackdrop(ctx: Ctx, w: number, h: number): void {
  bands(ctx, w, 0, 150, ["#3866d0", "#4678dc", "#5c8ee4", "#7ca4ea", "#a0b8ee", "#c4c6ee", "#e2cdea", "#f4d4e0"]);
  // 高い雲（細長い）
  cloud(ctx, 66, 24, 1.6, "#ffffff", "#d4d4f0");
  cloud(ctx, 300, 30, 2.0, "#fff8fc", "#d8d0ee");
  cloud(ctx, 186, 16, 1.1, "#ffffff", "#d4d4f0");
  // 日の光（左上）
  glow(ctx, 40, -10, 150, "255,244,214", 0.22);
  // 遠い浮島（霞んで淡い）
  floatIsland(ctx, 112, 74, 24, 18, 1, { grass: "#a4bcd8", grassDark: "#8ea8cc", rockL: "#a0a4d0", rockM: "#8c90c2", rockD: "#7a7eb4" });
  floatIsland(ctx, 330, 66, 18, 14, 2, { grass: "#a8bede", grassDark: "#94acd0", rockL: "#a4a8d2", rockM: "#9094c4", rockD: "#7e82b6" });
  // 雲海（奥から手前へ、手前ほど白く濃い）
  cloudBank(ctx, w, h, 112, 12, 0.6, "#f4d4e4", "#e4c4e0", "#c4aad4");
  // 中くらいの浮島（滝つき）
  floatIsland(ctx, 262, 96, 38, 34, 3, { grass: "#78b868", grassDark: "#4e9058", rockL: "#9a8ca8", rockM: "#7c7094", rockD: "#5e5478" });
  for (let y = 108; y < 150; y++) {
    px(ctx, 276 + Math.sin(y * 0.3) * 0.6, y, (y + 1) % 3 === 0 ? "#e8f4ff" : "#a8d4f4", 2, 1);
  }
  floatIsland(ctx, 60, 108, 28, 24, 4, { grass: "#7ec06e", grassDark: "#52965a", rockL: "#9e90ac", rockM: "#807498", rockD: "#625880" });
  cloudBank(ctx, w, h, 138, 14, 2.4, "#ffffff", "#f0e0f0", "#c8b4dc");
  cloudBank(ctx, w, h, 164, 14, 4.9, "#ffffff", "#e8e4f8", "#b8bce0");
  // 浮かぶ石の足場（前の円盤。上面は奥へ消えるように石畳が細かくなる）
  const pcx = 200, pcy = 170, prx = 176, pry = 28, thick = 30;
  const vpY = pcy - pry - 46;
  for (let y = pcy - pry; y <= pcy + pry + thick; y++) {
    for (let x = pcx - prx; x <= pcx + prx; x++) {
      const u = (x - pcx) / prx;
      const ey = Math.sqrt(Math.max(0, 1 - u * u)) * pry;
      const topEdge = pcy - ey, frontEdge = pcy + ey;
      if (y < topEdge) continue;
      if (y <= frontEdge) {
        const k = 1 / (y - vpY);
        const rowF = 3 / k / 40;
        const row = Math.floor(rowF);
        const colF = ((x - pcx) * k * 5) + (row % 2) * 0.5;
        const col = Math.floor(colF);
        const edgeLine = rowF - row < 1.6 * k * 8 * 0.18 || colF - col < 0.09;
        const base = (col + row) % 3 === 0 ? ["#bcb8d0", "#a8a4c0"] : ["#ccc8de", "#b6b2cc"];
        let c = u < -0.05 ? base[0] : base[1];
        if (edgeLine) c = "#8a86a8";
        if (y - topEdge < 1.5 || frontEdge - y < 1) c = "#e4e0f0";
        px(ctx, x, y, c);
      } else {
        // 側面の岩（下へすぼまって尖る）
        const dy = y - frontEdge;
        const th = thick * Math.pow(1 - Math.abs(u), 1.3) * (0.8 + hash(Math.floor(x / 5), 5) * 0.4);
        if (dy > th) continue;
        let c = u < -0.3 ? "#8a82a8" : u < 0.3 ? "#6e6690" : "#544c78";
        if (dy < 2) c = "#a8a2c4";
        if (hash(x, Math.floor(y / 3)) < 0.12) c = u < 0 ? "#6e6690" : "#544c78";
        px(ctx, x, y, c);
      }
    }
  }
  // 足場に立つ折れた石柱と小さな石の破片
  for (const [x, hgt] of [[58, 26], [336, 34]] as Array<[number, number]>) {
    for (let y = 0; y < hgt; y++) {
      for (let xx = 0; xx < 10; xx++) {
        px(ctx, x + xx, 160 - y, xx < 3 ? "#d8d4ea" : xx < 7 ? "#b4b0cc" : "#8a86a8");
      }
      if (y % 8 === 0) px(ctx, x - 1, 160 - y, "#8a86a8", 12, 1);
    }
    px(ctx, x - 2, 160 - hgt - 2, "#e4e0f0", 14, 2);
  }
  for (const [x, y, s] of [[180, 86, 6], [20, 76, 5], [376, 98, 7], [128, 112, 4]] as Array<[number, number, number]>) {
    floatIsland(ctx, x, y, s, Math.round(s * 1.1), x, { grass: "#78b868", grassDark: "#4e9058", rockL: "#9a8ca8", rockM: "#7c7094", rockD: "#5e5478" });
  }
  // 舞う光
  for (let i = 0; i < 30; i++) px(ctx, hash(i, 91) * w, hash(i, 92) * 120, "#ffffff");
}

// ---------------------------------------------------------------- 5. 火山の洞窟

function ember(ctx: Ctx, x: number, y: number, s: number): void {
  px(ctx, x, y, s > 0.66 ? "#ffe890" : "#ff9a30");
  px(ctx, x, y + 1, "#c8381c");
  if (s > 0.8) px(ctx, x + 1, y + 3, "#8a2414");
}

function lavaBackdrop(ctx: Ctx, w: number, h: number): void {
  // 洞窟の暗い壁（赤黒）
  bands(ctx, w, 0, 130, ["#0e0606", "#180a08", "#220e0a", "#2e120c", "#3e1810", "#541e10", "#6e2812"]);
  for (let i = 0; i < 500; i++) {
    const x = hash(i, 1) * w, y = hash(i, 2) * 130;
    px(ctx, x, y, hash(i, 3) > 0.55 ? "#3a1a14" : "#0a0404", 1 + Math.floor(hash(i, 4) * 3), 1);
  }
  // 奥の溶岩だまりの光
  glow(ctx, 200, 118, 150, "255,110,30", 0.4);
  glow(ctx, 200, 120, 60, "255,190,70", 0.35);
  // 天井のつらら状の岩（黒い。左の面がうっすら赤く照らされる）
  for (let i = 0; i < 15; i++) {
    const x = i * 28 + hash(i, 9) * 14, len = 14 + hash(i, 10) * 40, half = 5 + hash(i, 11) * 7;
    for (let y = 0; y < len; y++) {
      const hw = half * (1 - y / len);
      for (let xx = -hw; xx <= hw; xx++) {
        const lum = -xx / (hw || 1) + (y / len) * 0.5;
        px(ctx, x + xx, y, lum > 0.75 ? "#6a2a1a" : lum > 0 ? "#34160f" : "#1a0a08");
      }
    }
  }
  // 奥の岩壁のシルエット（遠い黒い山）
  hills(ctx, w, h, 112, 10, 3.2, "#2a100c", "#7a3216");
  hills(ctx, w, h, 124, 7, 1.6, "#1c0a08", "#5a2410", "#2a100c");
  // 溶岩の川: 奥の一点から手前へ広がり、うねる
  const cxAt = (y: number): number => 200 + Math.sin(y * 0.045) * (14 + (y - 120) * 0.45) - (y - 120) * 0.12;
  const hwAt = (y: number): number => 10 + (y - 120) * 1.15;
  for (let y = 120; y < h; y++) {
    const cx = cxAt(y), hw = hwAt(y);
    for (let x = Math.floor(cx - hw - 2); x <= cx + hw + 2; x++) {
      const d = Math.abs(x - cx) / hw;
      if (d > 1.04) continue;
      const flow = Math.sin(x * 0.09 + y * 0.35 + Math.sin(y * 0.11) * 3) * 0.5 + Math.sin(x * 0.21 - y * 0.2) * 0.5;
      const heat = (1 - d) * 0.75 + flow * 0.22 + hash(Math.floor(x / 2), Math.floor(y / 2)) * 0.1;
      let c: string;
      if (d > 0.96) c = "#3a140e"; // 冷えて固まったふち
      else if (heat > 0.78) c = "#ffe27a";
      else if (heat > 0.6) c = "#ffb23a";
      else if (heat > 0.42) c = "#f27a20";
      else if (heat > 0.26) c = "#d44418";
      else if (heat > 0.14) c = "#a02a14";
      else c = "#5e1c10";
      // 黒い殻の板（流れに乗って浮かぶ）
      if (heat < 0.62 && flow > 0.55 && hash(Math.floor(x / 5), Math.floor(y / 3)) < 0.5) c = (x + y) % 2 === 0 ? "#2a100c" : "#46180f";
      px(ctx, x, y, c);
    }
  }
  // 川を取り巻く黒い岩の床（ひび割れが赤く光る）
  for (let y = 124; y < h; y++) {
    const cx = cxAt(y), hw = hwAt(y);
    const shade = (y - 124) / (h - 124);
    for (let x = 0; x < w; x++) {
      if (Math.abs(x - cx) <= hw + 2) continue;
      const near = Math.max(0, 1 - (Math.abs(x - cx) - hw) / 46);
      const n = hash(Math.floor(x / 7), Math.floor(y / 4));
      let c = shade < 0.3 ? "#2c1410" : shade < 0.6 ? "#220f0c" : "#180a08";
      if (n < 0.3) c = shade < 0.5 ? "#341810" : "#26120c";
      if (hash(x, y) < 0.04) c = "#3c1c14";
      if (near > 0.85 && (x + y) % 2 === 0) c = "#8c3a14";
      else if (near > 0.6 && (x + y) % 2 === 0) c = "#64280f";
      else if (near > 0.3 && (x + y) % 2 === 0 && n < 0.5) c = "#3e1a0e";
      px(ctx, x, y, c);
    }
  }
  // ひび割れ
  for (let i = 0; i < 26; i++) {
    let x = hash(i, 31) * w, y = 134 + hash(i, 32) * (h - 140);
    const cx = cxAt(y), hw = hwAt(y);
    if (Math.abs(x - cx) < hw + 6) continue;
    const len = 6 + Math.floor(hash(i, 33) * 12);
    for (let k = 0; k < len; k++) {
      px(ctx, x, y, k % 3 === 0 ? "#ffa030" : "#d84a18");
      x += hash(i, 40 + k) > 0.5 ? 1 : -1 + (hash(i, 60 + k) > 0.6 ? 1 : 0);
      y += hash(i, 50 + k) > 0.55 ? 1 : 0;
    }
  }
  // 川から立ちのぼる赤い熱気
  for (let y = 96; y < 170; y += 2) dither(ctx, 0, y, w, 1, `rgba(255,96,32,${0.1 - Math.abs(y - 128) / 700})`);
  // 手前の大きな黒い岩（両側）
  for (const [bx, by, bw, bh2] of [[22, h + 4, 50, 70], [382, h + 6, 46, 58]] as Array<[number, number, number, number]>) {
    for (let xx = -bw; xx <= bw; xx++) {
      const u = xx / bw;
      const t = bh2 * (1 - Math.pow(Math.abs(u), 1.8)) * (0.88 + hash(bx, Math.floor(xx / 4)) * 0.24);
      for (let y = 0; y < t; y++) {
        const lum = -u * 0.5 + (y / t) * 0.35;
        // 溶岩に近い側（川に向いた面）はうっすら赤く
        const toward = bx < 200 ? u > 0.35 : u < -0.35;
        let c = lum < -0.1 ? "#3a1a12" : lum < 0.25 ? "#241008" : "#150906";
        if (toward && y < t * 0.8) c = (xx + y) % 2 === 0 ? "#5a2414" : c;
        px(ctx, bx + xx, by - y, c);
      }
    }
  }
  // 火の粉（溶岩の上から舞い上がる）
  for (let i = 0; i < 90; i++) {
    const u = hash(i, 71);
    const y = 40 + Math.pow(hash(i, 72), 0.8) * 160;
    const cx = cxAt(Math.max(124, y + 40));
    const spread = 20 + (y - 40) * 0.9;
    const x = cx + (hash(i, 73) - 0.5) * spread * 2 - (200 - y) * 0.05;
    ember(ctx, x, y, u);
  }
}

// ---------------------------------------------------------------- 6. 神殿・禁域

/** 環の紋様: 点 (dx,dy) の色。null なら描かない。 */
function ringColor(dx: number, dy: number, R: number): string | null {
  const r = Math.sqrt(dx * dx + dy * dy);
  const ang = Math.atan2(dy, dx);
  if (r > R + 1) return null;
  if (r >= R - 2 && r <= R) return "#c8f6fa";
  if (r > R) return "#2a6a88";
  if (r >= R - 4 && r < R - 2) return "#1a4a68";
  // 目盛りの輪
  if (r >= R - 12 && r <= R - 6) {
    const seg = Math.floor(((ang + Math.PI) / (Math.PI * 2)) * 48);
    if (seg % 2 === 0) return r < R - 8 ? "#6adcea" : "#3a9cc0";
    return null;
  }
  if (r >= R - 15 && r <= R - 14) return "#58c8e0";
  // 星形（2つの三角形）
  const rs = R * 0.66;
  for (let t = 0; t < 2; t++) {
    for (let k = 0; k < 3; k++) {
      const a1 = (t * 60 + k * 120 - 90) * (Math.PI / 180), a2 = (t * 60 + (k + 1) * 120 - 90) * (Math.PI / 180);
      const x1 = Math.cos(a1) * rs, y1 = Math.sin(a1) * rs, x2 = Math.cos(a2) * rs, y2 = Math.sin(a2) * rs;
      const vx = x2 - x1, vy = y2 - y1;
      const u = Math.max(0, Math.min(1, ((dx - x1) * vx + (dy - y1) * vy) / (vx * vx + vy * vy)));
      const d = Math.hypot(dx - (x1 + vx * u), dy - (y1 + vy * u));
      if (d < 0.9) return t === 0 ? "#9aeaf4" : "#74d4e8";
    }
  }
  if (r >= rs - 1 && r <= rs + 0.5) return "#4ab4d2";
  if (r < R * 0.13) return r < R * 0.07 ? "#eafcff" : "#9aeaf4";
  if (r >= R * 0.2 && r <= R * 0.2 + 1.2) return "#58c8e0";
  return null;
}

function shrineBackdrop(ctx: Ctx, w: number, h: number): void {
  const floorY = 128;
  // 奥の壁（青黒い石）
  bands(ctx, w, 0, floorY, ["#050d1a", "#08152a", "#0c1c36", "#102442", "#172e50", "#1e3a5e", "#26466c"]);
  // 石組みの目地
  for (let r = 0; r < 12; r++) {
    const y = r * 11 + 2;
    px(ctx, 0, y, "rgba(2,8,20,0.55)", w, 1);
    const off = (r % 2) * 20;
    for (let x = off; x < w; x += 40) px(ctx, x, y, "rgba(2,8,20,0.55)", 1, 11);
  }
  for (let i = 0; i < 260; i++) {
    const x = hash(i, 1) * w, y = hash(i, 2) * floorY;
    px(ctx, x, y, hash(i, 3) > 0.5 ? "#2e5078" : "#06101e", 1 + Math.floor(hash(i, 4) * 2), 1);
  }
  // 環のまわりのやわらかい光
  const rcx = 200, rcy = 66, R = 56;
  glow(ctx, rcx, rcy, 120, "90,200,230", 0.34);
  glow(ctx, rcx, rcy, 62, "160,240,250", 0.2);
  // 環の紋様
  for (let y = -R - 1; y <= R + 1; y++) {
    for (let x = -R - 1; x <= R + 1; x++) {
      const c = ringColor(x, y, R);
      if (c) px(ctx, rcx + x, rcy + y, c);
    }
  }
  // 環の外側に漂う小さな刻印（周りの12の点）
  for (let k = 0; k < 12; k++) {
    const a = (k / 12) * Math.PI * 2;
    px(ctx, rcx + Math.cos(a) * (R + 9), rcy + Math.sin(a) * (R + 9), "#58c8e0", 2, 2);
  }
  // 左右の石柱（奥行きのある太い柱）
  const pillar = (x: number, wd: number, light: string, mid: string, dark: string): void => {
    for (let y = 0; y < floorY + 4; y++) {
      for (let xx = 0; xx < wd; xx++) {
        const t = xx / wd;
        px(ctx, x + xx, y, t < 0.2 ? light : t < 0.65 ? mid : dark);
      }
      if (y % 18 === 0) px(ctx, x - 2, y, "#0a1628", wd + 4, 2);
    }
    px(ctx, x - 3, floorY - 4, "#3a5a82", wd + 6, 4);
    px(ctx, x - 3, 0, "#3a5a82", wd + 6, 6);
  };
  pillar(8, 26, "#4a6a92", "#2c4668", "#1a2c48");
  pillar(366, 26, "#4a6a92", "#2c4668", "#1a2c48");
  pillar(66, 16, "#3a5a82", "#243c5c", "#14243c");
  pillar(318, 16, "#3a5a82", "#243c5c", "#14243c");
  // 青白い光の柱（天井から床へ。市松でふちをなじませる）
  const beams: Array<[number, number]> = [[110, 11], [290, 11], [200, 7]];
  for (const [bx, bw] of beams) {
    for (let y = 0; y < floorY; y++) {
      for (let x = -bw - 4; x <= bw + 4; x++) {
        const d = Math.abs(x) / bw;
        if (d > 1.0 && (x + y) % 2 === 0) continue;
        if (d > 1.4) continue;
        const a = d < 0.35 ? 0.34 : d < 0.7 ? 0.24 : d < 1 ? 0.15 : 0.08;
        ctx.fillStyle = `rgba(190,240,255,${a})`;
        ctx.fillRect(bx + x, y, 1, 1);
      }
    }
  }
  // 床: 石畳（遠近）
  bands(ctx, w, floorY, h, ["#2a4264", "#243a5a", "#1e3250", "#182a46", "#12213a", "#0e1a30"]);
  for (let r = 0; r < 14; r++) {
    const y = floorY + 2 + r * r * 0.5 + r * 2;
    if (y > h) break;
    px(ctx, 0, y, "#0a1426", w, 1);
    const cell = 20 + r * 6;
    for (let x = ((r % 2) * cell) / 2 - 40; x < w; x += cell) {
      // 消失点（画面中央・奥）へ向かって少し傾く縦の目地
      const lean = (x - 200) * (r * 0.02);
      px(ctx, x + lean, y, "#0a1426", 1, Math.max(2, r * 1.6 + 2));
    }
  }
  // 床に映る環と光の柱（上下反転して、薄く）
  for (let y = floorY + 1; y < h; y++) {
    const sy = floorY - (y - floorY) / 0.62;
    const dy = sy - rcy;
    if (Math.abs(dy) > R + 1) continue;
    for (let x = -R - 1; x <= R + 1; x++) {
      const c = ringColor(x, dy, R);
      if (!c) continue;
      const ripple = Math.sin(y * 1.3) > 0.6 ? 1 : 0;
      if ((x + y + ripple) % 2 !== 0) continue;
      px(ctx, rcx + x, y, c.replace("#", "#") + "", 1, 1);
      ctx.fillStyle = "rgba(10,24,48,0.55)";
      ctx.fillRect(rcx + x, y, 1, 1);
    }
  }
  for (const [bx, bw] of beams) {
    for (let y = floorY; y < h; y++) {
      const fade = 1 - (y - floorY) / (h - floorY);
      for (let x = -bw; x <= bw; x++) {
        if ((x + y) % 2 === 0 && Math.abs(x) > bw * 0.5) continue;
        ctx.fillStyle = `rgba(170,230,250,${0.28 * fade * (1 - Math.abs(x) / (bw + 2))})`;
        ctx.fillRect(bx + x, y, 1, 1);
      }
    }
    // 光が床に当たる丸い光だまり
    for (let x = -bw * 2; x <= bw * 2; x++) {
      for (let y = -3; y <= 3; y++) {
        const d = (x * x) / (bw * bw * 4) + (y * y) / 9;
        if (d > 1 || ((x + y) % 2 === 0 && d > 0.55)) continue;
        ctx.fillStyle = d < 0.4 ? "rgba(210,248,255,0.34)" : "rgba(190,240,255,0.18)";
        ctx.fillRect(bx + x, floorY + 4 + y, 1, 1);
      }
    }
  }
  // 床の目地に走る淡い光の線
  for (let x = 0; x < w; x++) {
    if (hash(x, 77) > 0.55) px(ctx, x, floorY + 1, "#4a8ab0");
  }
  // 漂う光の粒
  for (let i = 0; i < 54; i++) {
    const x = hash(i, 81) * w, y = hash(i, 82) * 190;
    px(ctx, x, y, hash(i, 83) > 0.6 ? "#e8fcff" : "#7ad4ea");
  }
}

// ---------------------------------------------------------------- 海底

function seaweed(ctx: Ctx, x: number, by: number, hgt: number, seed: number, light: string, dark: string): void {
  for (let i = 0; i < hgt; i++) {
    const sway = Math.round(Math.sin(i * 0.45 + seed) * 2);
    px(ctx, x + sway, by - i, i % 3 === 0 ? dark : light, 2, 1);
    if (i % 5 === 3) px(ctx, x + sway + (seed % 2 === 0 ? 2 : -1), by - i, light, 1, 1);
  }
}

function coral(ctx: Ctx, cx: number, by: number, s: number, seed: number, light: string, mid: string, dark: string): void {
  for (let b = -2; b <= 2; b++) {
    const bh = Math.round(s * (0.55 + hash(seed, b) * 0.6));
    const bx = cx + b * Math.round(s * 0.28);
    for (let i = 0; i < bh; i++) {
      const spread = Math.round(Math.sin(i * 0.5 + b) * 1.2) + Math.round(b * i * 0.12);
      px(ctx, bx + spread, by - i, i > bh * 0.7 ? light : i % 4 === 0 ? dark : mid, 2, 1);
    }
  }
}

function deepBackdrop(ctx: Ctx, w: number, h: number): void {
  // 水の色: 上は明るい青緑、下へいくほど濃い群青（奥ほど淡く、手前ほど濃く）
  bands(ctx, w, 0, h, ["#3a8aa8", "#2f7a9c", "#276a90", "#1e5a82", "#164a72", "#103a60", "#0b2c4c", "#071e3a"]);
  // 左上からさしこむ光の筋（市松でなじませる）
  for (let k = 0; k < 5; k++) {
    const x0 = 20 + k * 78 + Math.round(hash(k, 3) * 14);
    for (let y = 0; y < 150; y++) {
      const half = 6 + Math.round(y * 0.1);
      const sx = x0 + Math.round(y * 0.35);
      dither(ctx, sx - half, y, half * 2, 1, y < 60 ? "#6ab8c8" : y < 110 ? "#4a9ab8" : "#3a86a8");
    }
  }
  // 遠くの沈んだ神殿の柱（淡い影）
  for (let i = 0; i < 7; i++) {
    const x = 30 + i * 52 + Math.round(hash(i, 9) * 18);
    const hgt = 38 + Math.round(hash(i, 4) * 40);
    const top = 150 - hgt;
    for (let y = top; y < 152; y++) {
      px(ctx, x, y, "#1a4a72", 7, 1);
      px(ctx, x + 5, y, "#143c60", 2, 1);
    }
    px(ctx, x - 2, top, "#215a80", 11, 3);
    if (i % 3 === 1) for (let y = top - 6; y < top; y++) px(ctx, x + 1 + (top - y) % 3, y, "#1a4a72", 3, 1);
  }
  // 海底の砂地（なだらかな起伏。上の縁を明るく）
  hills(ctx, w, h, 160, 8, 5, "#7a8a78", "#a8b496", "#5a6a60");
  hills(ctx, w, h, 182, 7, 11, "#5a6a62", "#84927c", "#3e4c48");
  ctx.fillStyle = "#34423e";
  ctx.fillRect(0, 205, w, h - 205);
  // 砂のさざ波
  for (let y = 168; y < 205; y += 4) {
    for (let x = (y * 7) % 11; x < w; x += 11) px(ctx, x, y, y < 185 ? "#6a7a6a" : "#46544e", 5, 1);
  }
  // 海藻と珊瑚
  for (let i = 0; i < 12; i++) {
    seaweed(ctx, 14 + i * 34 + Math.round(hash(i, 1) * 12), 190 + Math.round(hash(i, 2) * 8), 22 + Math.round(hash(i, 6) * 26), i, "#3a9a5a", "#1e6a3e");
  }
  coral(ctx, 70, 196, 30, 3, "#f08a7a", "#c85a6a", "#8a3a52");
  coral(ctx, 200, 200, 24, 8, "#f0c070", "#c88a4a", "#8a5a34");
  coral(ctx, 330, 196, 32, 5, "#b08ae8", "#8a5ac8", "#5a3a8a");
  // 泡
  for (let i = 0; i < 26; i++) {
    const x = 10 + Math.round(hash(i, 7) * (w - 20));
    const y = 20 + Math.round(hash(i, 8) * 150);
    const r = hash(i, 5) > 0.7 ? 2 : 1;
    px(ctx, x, y, "#a8e0ea", r, r);
    if (r === 2) px(ctx, x + 1, y + 1, "#6ab8c8", 1, 1);
  }
  // 手前を暗くして、奥行きを出す
  glow(ctx, 0, h, 90, "4,16,32", 0.55);
  glow(ctx, w, h, 90, "4,16,32", 0.55);
}

// ---------------------------------------------------------------- 入口

/** 追加の背景を描く。w×h は戦闘の背景と同じ 400×225 を想定（座標は固定値）。 */
export function paintExtraBackdrop(kind: ExtraBiome, ctx: CanvasRenderingContext2D, w: number, h: number): void {
  ctx.imageSmoothingEnabled = false;
  switch (kind) {
    case "forest": forestBackdrop(ctx, w, h); break;
    case "swamp": swampBackdrop(ctx, w, h); break;
    case "coast": coastBackdrop(ctx, w, h); break;
    case "sky": skyBackdrop(ctx, w, h); break;
    case "lava": lavaBackdrop(ctx, w, h); break;
    case "shrine": shrineBackdrop(ctx, w, h); break;
    case "deep": deepBackdrop(ctx, w, h); break;
  }
}
