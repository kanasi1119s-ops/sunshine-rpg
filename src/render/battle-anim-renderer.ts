import type { FxId, WeaponMotion } from "../game/battle/battle-anim";

/**
 * 戦闘の動きの絵（ドット）: 武器をふる・つく・矢をはなつ・杖をかざす、と、魔法のエフェクト。
 * 画像は使わず、1ドットずつの四角で描く。経過 t（0〜1）だけで決まる（毎フレーム同じ絵になる）。
 * 味方は右、敵は左にいて、味方は左（敵のほう）を向く。
 */
export interface Pt {
  x: number;
  y: number;
  /** 大きさ（人・敵の絵の幅と高さ。魔法のため（魔法陣・光の柱）の大きさに使う）。 */
  w?: number;
  h?: number;
}

function dot(ctx: CanvasRenderingContext2D, x: number, y: number, c: string, w = 1, h = 1): void {
  ctx.fillStyle = c;
  ctx.fillRect(Math.round(x), Math.round(y), w, h);
}
function line(ctx: CanvasRenderingContext2D, x0: number, y0: number, x1: number, y1: number, c: string, thick = 1): void {
  let x = Math.round(x0), y = Math.round(y0);
  const xe = Math.round(x1), ye = Math.round(y1);
  const dx = Math.abs(xe - x), dy = -Math.abs(ye - y);
  const sx = x < xe ? 1 : -1, sy = y < ye ? 1 : -1;
  let err = dx + dy;
  for (let n = 0; n < 200; n++) {
    dot(ctx, x, y, c, thick, thick);
    if (x === xe && y === ye) break;
    const e2 = 2 * err;
    if (e2 >= dy) { err += dy; x += sx; }
    if (e2 <= dx) { err += dx; y += sy; }
  }
}
function rnd(i: number, k = 0): number {
  const h = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453;
  return h - Math.floor(h);
}
const clamp01 = (v: number): number => Math.max(0, Math.min(1, v));
const ease = (v: number): number => 1 - (1 - clamp01(v)) ** 2;
function ring(ctx: CanvasRenderingContext2D, cx: number, cy: number, rx: number, ry: number, c: string, alpha = 1): void {
  ctx.save();
  ctx.globalAlpha = clamp01(alpha);
  const n = Math.max(12, Math.round((rx + ry) * 1.6));
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2;
    dot(ctx, cx + Math.cos(a) * rx, cy + Math.sin(a) * ry, c);
  }
  ctx.restore();
}
/** 4方向に光る星（＋）。 */
function star(ctx: CanvasRenderingContext2D, x: number, y: number, r: number, c: string, core = "#ffffff"): void {
  for (let k = 1; k <= r; k++) {
    dot(ctx, x - k, y, c); dot(ctx, x + k, y, c); dot(ctx, x, y - k, c); dot(ctx, x, y + k, c);
  }
  dot(ctx, x, y, core);
}

/** 動いている味方の、前（敵のほう）へ出る量。 */
export function lungeOffset(motion: WeaponMotion, t: number): number {
  switch (motion) {
    case "slash": return -Math.round(Math.sin(clamp01((t - 0.1) / 0.6) * Math.PI) * 14);
    case "chop": return -Math.round(Math.sin(clamp01((t - 0.15) / 0.65) * Math.PI) * 14);
    case "stab": return -Math.round(Math.sin(clamp01((t - 0.1) / 0.5) * Math.PI) * 12);
    case "thrust": return -Math.round(Math.sin(clamp01((t - 0.1) / 0.55) * Math.PI) * 14);
    case "shoot": return t > 0.4 && t < 0.55 ? 1 : 0;    // はなった反動で、ほんの少し後ろへ
    default: return 0;
  }
}

const STEEL = "#e8eef8";
const STEEL_D = "#8a96b0";
const WOOD = "#8a5a2c";
const WOOD_D = "#5a3a1c";

/** 武器をふる動き。hand は味方の手の位置。 */
export function drawWeaponMotion(ctx: CanvasRenderingContext2D, motion: WeaponMotion, t: number, hand: Pt, target: Pt, glow = "#9ad0ff"): void {
  switch (motion) {
    case "slash": {
      const th = (u: number): number => -50 + ease(clamp01((u - 0.12) / 0.4)) * 170;      // 角度（上=0、前（左）へ正）
      const a = th(t);
      const L = 13;
      // 軌跡（さっきまでの刃の通った弧）
      for (let k = 0; k < 14; k++) {
        const aa = th(t - k * 0.014);
        if (aa >= a - 0.01 && k > 0) continue;
        const rr = L + 1 - (k > 8 ? 1 : 0);
        const px = hand.x - Math.sin((aa * Math.PI) / 180) * rr;
        const py = hand.y - Math.cos((aa * Math.PI) / 180) * rr;
        ctx.save(); ctx.globalAlpha = 0.9 - k * 0.06; dot(ctx, px, py, "#ffffff"); dot(ctx, px, py + 1, "#bfe0ff"); ctx.restore();
      }
      const tx = hand.x - Math.sin((a * Math.PI) / 180) * L;
      const ty = hand.y - Math.cos((a * Math.PI) / 180) * L;
      line(ctx, hand.x, hand.y, tx, ty, STEEL_D, 3);
      line(ctx, hand.x, hand.y, tx, ty, STEEL, 1);
      dot(ctx, hand.x - 1, hand.y, WOOD, 3, 2);
      break;
    }
    case "stab": {
      const thrust = (u: number): number => Math.sin(clamp01((u - 0.1) / 0.3) * Math.PI) + Math.sin(clamp01((u - 0.5) / 0.3) * Math.PI);
      const e = thrust(t);
      const tipx = hand.x - 3 - e * 9;
      line(ctx, hand.x, hand.y, tipx - 5, hand.y, STEEL_D, 3);
      line(ctx, hand.x - 1, hand.y, tipx - 5, hand.y, STEEL, 1);
      dot(ctx, hand.x - 1, hand.y - 1, WOOD, 2, 3);
      if (e > 0.6) for (let k = 0; k < 3; k++) dot(ctx, tipx - 7 - k * 2, hand.y + (k % 2 ? 1 : -1), "#ffffff");
      break;
    }
    case "chop": {
      const th = (u: number): number => -95 + ease(clamp01((u - 0.2) / 0.4)) * 205;
      const a = th(t);
      const L = 12;
      const tx = hand.x - Math.sin((a * Math.PI) / 180) * L;
      const ty = hand.y - Math.cos((a * Math.PI) / 180) * L;
      for (let k = 1; k < 12; k++) {
        const aa = th(t - k * 0.016);
        if (aa >= a) continue;
        ctx.save(); ctx.globalAlpha = 0.75 - k * 0.055;
        dot(ctx, hand.x - Math.sin((aa * Math.PI) / 180) * (L + 2), hand.y - Math.cos((aa * Math.PI) / 180) * (L + 2), "#ffe9b0", 2, 2);
        ctx.restore();
      }
      line(ctx, hand.x, hand.y, tx, ty, WOOD, 2);
      // 刃（先の太い部分）
      dot(ctx, tx - 3, ty - 3, STEEL_D, 6, 6);
      dot(ctx, tx - 2, ty - 2, STEEL, 4, 4);
      if (t > 0.62 && t < 0.8) { ring(ctx, hand.x - 14, hand.y + 8, (t - 0.62) * 70, 3, "#fff2c0", 1 - (t - 0.62) * 5); }
      break;
    }
    case "thrust": {
      const e = Math.sin(clamp01((t - 0.12) / 0.5) * Math.PI);
      const back = t < 0.12 ? t * 20 : 0;
      const x0 = hand.x + 4 + back, y0 = hand.y;
      const x1 = hand.x - 14 - e * 11, y1 = hand.y - 1;
      line(ctx, x0, y0, x1, y1, WOOD, 2);
      // 穂先
      line(ctx, x1, y1, x1 - 5, y1 - 0.5, STEEL, 2);
      dot(ctx, x1 - 6, y1, "#ffffff");
      dot(ctx, x1 + 1, y1 - 2, "#b8402c", 2, 1);          // 房
      if (e > 0.7) for (let k = 0; k < 4; k++) dot(ctx, x1 - 8 - k * 3, y1 + (k % 2 ? 2 : -2), "#dff0ff");
      break;
    }
    case "shoot": {
      // 弓: かまえ（0〜0.4）→はなつ→矢が飛ぶ（0.4〜0.78）
      const draw = clamp01(t / 0.4);
      const bx = hand.x - 5;
      for (let k = -7; k <= 7; k++) {
        const bow = Math.round((k * k) / 14);
        dot(ctx, bx - 2 + bow, hand.y + k, WOOD, 2, 1);
        dot(ctx, bx - 3 + bow, hand.y + k, WOOD_D);
      }
      const stringX = t < 0.4 ? bx + 1 + draw * 5 : bx + 1;
      line(ctx, bx + 3, hand.y - 7, stringX, hand.y, "#f0e8d0");
      line(ctx, stringX, hand.y, bx + 3, hand.y + 7, "#f0e8d0");
      if (t < 0.4) {
        line(ctx, stringX, hand.y, bx - 7, hand.y, "#d8c8a0");
        dot(ctx, bx - 9, hand.y - 1, "#e8eef8", 2, 3);
      } else {
        const f = clamp01((t - 0.4) / 0.38);
        const ax = bx - 9 + (target.x - (bx - 9)) * f;
        const ay = hand.y + (target.y - hand.y) * f - Math.sin(f * Math.PI) * 8;
        const px = bx - 9 + (target.x - (bx - 9)) * Math.max(0, f - 0.12);
        const py = hand.y + (target.y - hand.y) * Math.max(0, f - 0.12) - Math.sin(Math.max(0, f - 0.12) * Math.PI) * 8;
        if (f < 1) {
          line(ctx, px, py, ax, ay, "#d8c8a0", 1);
          dot(ctx, ax - 1, ay - 1, STEEL, 3, 3);
          dot(ctx, px + 2, py - 1, "#d85a4a", 2, 1);
          dot(ctx, px + 2, py + 1, "#d85a4a", 2, 1);
          for (let k = 1; k < 5; k++) { ctx.save(); ctx.globalAlpha = 0.5 - k * 0.1; dot(ctx, px + k * 3, py + k * 0.6, "#ffffff"); ctx.restore(); }
        }
      }
      break;
    }
    case "cast": {
      // 杖を高くかかげ、先の玉が光る。足もとに魔法陣
      const up = ease(t / 0.3);
      const sx = hand.x + 1, top = hand.y - 6 - up * 12;
      line(ctx, sx, hand.y + 2, sx, top, WOOD, 2);
      dot(ctx, sx - 1, top - 1, WOOD_D, 4, 1);
      const pulse = 1 + Math.sin(t * 40) * 0.5;
      ctx.save();
      ctx.globalAlpha = 0.35;
      ring(ctx, sx + 0.5, top - 2, 4 + pulse, 4 + pulse, glow);
      ctx.restore();
      dot(ctx, sx - 1, top - 4, glow, 4, 4);
      dot(ctx, sx, top - 3, "#ffffff", 2, 2);
      for (let k = 0; k < 6; k++) {
        const u = (t * 1.6 + k / 6) % 1;
        dot(ctx, sx + (rnd(k) - 0.5) * 14, top + 6 - u * 22, glow);
      }
      break;
    }
  }
}

/**
 * 魔法の「ため」（唱えているあいだ）: 足もとに、回る二重の魔法陣。体の上のほうに光の玉がふくらみ、陣のふちから光の柱が立ちのぼる。
 * 体のまわりに、小さな火花が走る。人（味方）にも敵（ボスなど大きな絵）にも使う。at は体の中心、w・h は体の大きさ。
 */
export function drawCharge(ctx: CanvasRenderingContext2D, at: Pt, color: string, t: number, fx?: FxId): void {
  const u = clamp01(t);
  const w = at.w ?? 16, h = at.h ?? 32;
  const feet = at.y + h / 2 - 2;
  const rx = Math.max(13, w * 0.62), ry = rx * 0.3;
  ctx.save();
  // 魔法陣（外の輪は右まわり、内の輪は左まわりに、ひし形の目盛りがすすむ）
  const fadeIn = Math.min(1, u * 3);
  ctx.globalAlpha = 0.85 * fadeIn;
  ring(ctx, at.x, feet, rx, ry, color);
  ring(ctx, at.x, feet, rx * 0.68, ry * 0.68, "#ffffff");
  ring(ctx, at.x, feet, rx * 1.12, ry * 1.12, color, 0.45);
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2 + u * 5;
    dot(ctx, at.x + Math.cos(a) * rx * 0.84, feet + Math.sin(a) * ry * 0.84, "#ffffff", 1, 1);
    const b = (i / 16) * Math.PI * 2 - u * 7;
    dot(ctx, at.x + Math.cos(b) * rx * 0.5, feet + Math.sin(b) * ry * 0.5, color, 1, 1);
  }
  // 光の柱（陣のふちから、だんだん高く）
  const pillar = ease(u * 1.4) * h * 1.1;
  for (let i = 0; i < 7; i++) {
    const a = (i / 7) * Math.PI * 2;
    const px = at.x + Math.cos(a) * rx * 0.9;
    const base = feet + Math.sin(a) * ry * 0.9;
    ctx.globalAlpha = 0.45 * fadeIn * (a > Math.PI ? 0.6 : 1);
    for (let y = 0; y < pillar; y += 2) dot(ctx, px, base - y, y % 4 === 0 ? "#ffffff" : color);
  }
  // 属性ごとのため: 炎＝陣のふちから小さな炎、雷＝陣のふちを走る電光
  if (fx === "fire") {
    ctx.globalAlpha = 0.9 * fadeIn;
    for (let i = 0; i < 30; i++) {
      const a = (i / 30) * Math.PI * 2;
      const fl = 3 + Math.round(rnd(i, Math.floor(u * 30)) * 10 * u);
      const fx0 = at.x + Math.cos(a) * rx, fy0 = feet + Math.sin(a) * ry;
      dot(ctx, fx0, fy0 - fl, "#ffd040", 1, fl);
      dot(ctx, fx0, fy0 - fl + 2, "#f06a20", 1, Math.max(1, fl - 2));
    }
  } else if (fx === "bolt") {
    ctx.globalAlpha = 0.9 * fadeIn;
    for (let i = 0; i < 6; i++) {
      const a = rnd(i, Math.floor(u * 20)) * Math.PI * 2;
      const x0 = at.x + Math.cos(a) * rx, y0 = feet + Math.sin(a) * ry;
      line(ctx, x0, y0, x0 + (rnd(i, 7) - 0.5) * 8, y0 - 4 - rnd(i, 9) * 8, "#ffffff");
    }
  }
  // 光の玉（頭の上）
  const orbY = at.y - h / 2 - 2;
  const r = 1 + Math.round(u * 5);
  ctx.globalAlpha = 0.3 + 0.2 * Math.sin(u * 40);
  ring(ctx, at.x, orbY, r + 3, r + 3, color);
  ctx.globalAlpha = 1;
  dot(ctx, at.x - r, orbY - r, color, r * 2 + 1, r * 2 + 1);
  dot(ctx, at.x - Math.max(1, r - 2), orbY - Math.max(1, r - 2), "#ffffff", Math.max(1, r - 2) * 2 + 1, Math.max(1, r - 2) * 2 + 1);
  if (u > 0.4) for (let i = 0; i < 6; i++) {
    const a = (i / 6) * Math.PI * 2 + u * 9;
    line(ctx, at.x + Math.cos(a) * (r + 2), orbY + Math.sin(a) * (r + 2), at.x + Math.cos(a) * (r + 6 + rnd(i, Math.floor(u * 30)) * 4), orbY + Math.sin(a) * (r + 6 + rnd(i, Math.floor(u * 30)) * 4), "#ffffff");
  }
  // 体のまわりの火花
  for (let i = 0; i < 10; i++) {
    const k = Math.floor(u * 24);
    const sx = at.x + (rnd(i, k) - 0.5) * w * 1.1, sy = at.y + (rnd(i, k + 50) - 0.5) * h;
    dot(ctx, sx, sy, i % 2 ? "#ffffff" : color);
    dot(ctx, sx + 1, sy + 1, color);
  }
  ctx.restore();
}

export const FX_COLOR: Record<FxId, string> = {
  fire: "#ff9a40", water: "#6ab4ff", light: "#fff0a0", wind: "#a8f0d0", ice: "#bfe8ff", bolt: "#ffe848", rock: "#c8a070",
  burst: "#ffffff", heal: "#88f0a8", buff: "#ffd860", debuff: "#b080e8", sleep: "#9ab0ff", poison: "#b060e0", confuse: "#ffe070",
};

/** 魔法・状態のエフェクト。target は対象のからだの中心。 */
export function drawFx(ctx: CanvasRenderingContext2D, fx: FxId, t: number, target: Pt, opts: { from?: Pt; area?: boolean } = {}): void {
  const { x: tx, y: ty } = target;
  const fade = 1 - t;
  ctx.save();
  switch (fx) {
    case "fire": {
      // 炎: 派手に。火の玉は大きく、長い尾と火の粉。爆発は、衝撃の輪・黄白の核・飛び散る火の粉・けむり、画面も赤く光る。火柱は、太く高く、ねじれて立ち、地面にも炎が走る
      const flame = (x: number, y: number, size: number, k: number): void => {
        dot(ctx, x - size, y - size, "#8a2a14", size * 2 + 1, size * 2 + 1);
        dot(ctx, x - size + 1, y - size + 1, "#e8501c", size * 2 - 1, size * 2 - 1);
        if (size >= 2) dot(ctx, x - size + 2, y - size + 2, "#ffc040", size * 2 - 3, size * 2 - 3);
        if (size >= 3) dot(ctx, x - 1, y - 1, "#fff6c0", 3, 3);
        void k;
      };
      if (opts.area) {
        const u = clamp01(t * 1.1);
        // 画面の赤い光
        ctx.globalAlpha = 0.22 * Math.sin(Math.min(1, u * 1.3) * Math.PI);
        ctx.fillStyle = "#ff6a20";
        ctx.fillRect(-4, -4, 420, 240);
        ctx.globalAlpha = 1;
        // 地面を走る炎
        for (let i = 0; i < 26; i++) {
          const gx = tx - 26 + rnd(i, 30) * 52, gh = 3 + Math.sin(t * 20 + i) * 2 + rnd(i, 31) * 5;
          dot(ctx, gx, ty + 15 - gh, i % 3 ? "#f06a20" : "#ffc040", 2, gh);
        }
        const hgt = Math.sin(Math.min(1, u * 1.15) * Math.PI) * 76;
        for (let col = -2; col <= 2; col++) {
          const cx = tx + col * 6 + Math.sin(t * 14 + col) * 2;
          for (let y = 0; y < hgt; y++) {
            const swirl = Math.sin(y * 0.22 + t * 18 + col * 1.7) * (2 + y * 0.05);
            const half = Math.max(1, Math.round(6 - (y / Math.max(1, hgt)) * 5 + (rnd(y + col * 31, Math.floor(t * 26)) - 0.5) * 3));
            dot(ctx, cx + swirl - half, ty + 14 - y, y < hgt * 0.3 ? "#fffbe0" : y < hgt * 0.55 ? "#ffd050" : y < hgt * 0.8 ? "#f4862a" : "#c8381c", half * 2, 1);
          }
        }
        // 火の粉と、のぼるけむり
        for (let i = 0; i < 34; i++) {
          const v = clamp01(t * 1.3 - rnd(i, 32) * 0.4);
          if (v <= 0 || v >= 1) continue;
          dot(ctx, tx + (rnd(i, 33) - 0.5) * 40 + Math.sin(v * 9 + i) * 3, ty + 12 - v * 70, v < 0.6 ? "#ffd050" : "#ff8a30", 2, 2);
        }
        ctx.globalAlpha = 0.5;
        for (let i = 0; i < 10; i++) {
          const v = clamp01(t * 1.2 - 0.3 - rnd(i, 25) * 0.2);
          if (v > 0 && v < 1) dot(ctx, tx + (rnd(i, 26) - 0.5) * 32, ty - hgt * 0.7 - v * 22, "#5a5660", 6, 4);
        }
        ctx.globalAlpha = 1;
        break;
      }
      const f = opts.from;
      const flight = f ? clamp01(t / 0.45) : 1;
      if (f && flight < 1) {
        // 大きな火の玉（長い尾と火の粉）
        const arc = (q: number): Pt => ({ x: f.x + (tx - f.x) * q, y: f.y + (ty - f.y) * q - Math.sin(q * Math.PI) * 18 });
        for (let k = 14; k >= 1; k--) {
          const q = arc(Math.max(0, flight - k * 0.035));
          flame(q.x + (rnd(k, Math.floor(t * 30)) - 0.5) * 3, q.y + (rnd(k, 5) - 0.5) * 3, Math.max(1, 4 - Math.floor(k / 4)), k);
        }
        const head = arc(flight);
        flame(head.x, head.y, 5, 0);
        for (let i = 0; i < 6; i++) dot(ctx, head.x + (rnd(i, Math.floor(t * 40)) - 0.5) * 14, head.y + (rnd(i, 44) - 0.5) * 14, "#ffd050", 2, 2);
        break;
      }
      // 着弾の大爆発
      const e = f ? clamp01((t - 0.45) / 0.55) : t;
      if (e < 0.25) { ctx.globalAlpha = 0.5 * (1 - e / 0.25); ctx.fillStyle = "#fff0c0"; ctx.fillRect(-4, -4, 420, 240); ctx.globalAlpha = 1; }
      else if (e < 0.7) { ctx.globalAlpha = 0.16 * (1 - (e - 0.25) / 0.45); ctx.fillStyle = "#ff5a18"; ctx.fillRect(-4, -4, 420, 240); ctx.globalAlpha = 1; }
      const rad = 5 + ease(e) * 24;
      ctx.globalAlpha = 1 - Math.max(0, e - 0.4) * 1.5;
      for (let yy = -Math.floor(rad); yy <= rad; yy++) for (let xx = -Math.floor(rad); xx <= rad; xx++) {
        const d = Math.hypot(xx, yy * 1.1);
        if (d > rad) continue;
        const wob = (rnd(xx * 7 + yy, Math.floor(e * 14)) - 0.5) * 0.18 * rad;
        const dd = d + wob;
        dot(ctx, tx + xx, ty + yy, dd < rad * 0.38 ? "#fffbe0" : dd < rad * 0.62 ? "#ffd050" : dd < rad * 0.84 ? "#f4862a" : "#c8381c");
      }
      ctx.globalAlpha = 1;
      // 衝撃の輪
      ring(ctx, tx, ty + 6, 6 + e * 34, 3 + e * 14, "#ffe8a0", 1 - e);
      ring(ctx, tx, ty + 6, 3 + e * 24, 2 + e * 9, "#ffb040", (1 - e) * 0.8);
      // 放射状の火線と、飛び散る火の粉
      for (let i = 0; i < 14; i++) {
        const a = (i / 14) * Math.PI * 2 + 0.2;
        line(ctx, tx + Math.cos(a) * (rad + 2), ty + Math.sin(a) * (rad + 2), tx + Math.cos(a) * (rad + 6 + e * 18), ty + Math.sin(a) * (rad + 6 + e * 18), i % 2 ? "#ffc040" : "#ff7a28", 2);
      }
      for (let i = 0; i < 22; i++) {
        const a = rnd(i, 51) * Math.PI * 2, d = e * (14 + rnd(i, 52) * 34);
        dot(ctx, tx + Math.cos(a) * d, ty + Math.sin(a) * d * 0.8 + e * e * 10, e < 0.6 ? "#ffd050" : "#ff8a30", 2, 2);
      }
      if (e > 0.35) {
        ctx.globalAlpha = Math.min(0.55, (e - 0.35) * 1.2) * (1 - e * 0.5);
        for (let i = 0; i < 6; i++) dot(ctx, tx + (rnd(i, 53) - 0.5) * 30, ty - 8 - (e - 0.35) * 36 - rnd(i, 54) * 8, "#5a5660", 7, 5);
        ctx.globalAlpha = 1;
      }
      break;
    }
    case "water": {
      if (opts.from && !opts.area && t < 0.45) {
        const flight = clamp01(t / 0.45);
        const f = opts.from;
        const bx = f.x + (tx - f.x) * flight, by = f.y + (ty - f.y) * flight - Math.sin(flight * Math.PI) * 12;
        for (let k = 6; k >= 1; k--) {
          const bf = Math.max(0, flight - k * 0.04);
          dot(ctx, f.x + (tx - f.x) * bf - 1, f.y + (ty - f.y) * bf - Math.sin(bf * Math.PI) * 12 - 1, k > 3 ? "#3a78c8" : "#6ab4ff", 3, 3);
        }
        dot(ctx, bx - 3, by - 3, "#3a78c8", 7, 7);
        dot(ctx, bx - 2, by - 2, "#9ad0ff", 5, 5);
        dot(ctx, bx - 1, by - 1, "#ffffff", 2, 2);
        break;
      }
      for (let k = 0; k < 3; k++) {
        const u = clamp01(t * 1.3 - k * 0.18);
        if (u > 0 && u < 1) ring(ctx, tx, ty + 12, 4 + u * 20, 1.5 + u * 6, k === 0 ? "#e8f6ff" : "#6ab4ff", 1 - u);
      }
      for (let i = 0; i < 18; i++) {
        const u = clamp01(t * 1.5 - rnd(i, 4) * 0.5);
        if (u <= 0 || u >= 1) continue;
        const x = tx + (rnd(i, 5) - 0.5) * 26;
        const y = ty - 34 + u * 46;
        dot(ctx, x, y, "#cfe8ff", 1, 3);
        dot(ctx, x, y + 1, "#6ab4ff", 1, 2);
        if (u > 0.85) dot(ctx, x + (i % 2 ? 2 : -2), ty + 10, "#9ad0ff", 2, 1);
      }
      break;
    }
    case "light": {
      const w = Math.max(1, Math.round(10 * (1 - Math.abs(t - 0.4) * 1.6)));
      ctx.globalAlpha = 0.5 * fade + 0.2;
      dot(ctx, tx - w, 0, "#ffe890", w * 2, ty + 14);
      ctx.globalAlpha = 0.9;
      dot(ctx, tx - Math.ceil(w / 3), 0, "#ffffff", Math.ceil(w / 3) * 2, ty + 14);
      ctx.globalAlpha = 1;
      for (let i = 0; i < 9; i++) {
        const u = clamp01(t * 1.4 - rnd(i, 6) * 0.4);
        if (u <= 0 || u >= 1) continue;
        star(ctx, tx + (rnd(i, 7) - 0.5) * 30, ty + (rnd(i, 8) - 0.5) * 30 - u * 6, u < 0.5 ? 2 : 1, "#ffe890");
      }
      ring(ctx, tx, ty + 12, 6 + t * 18, 2 + t * 5, "#fff6c0", 1 - t);
      break;
    }
    case "wind": {
      for (let k = 0; k < 3; k++) {
        const u = clamp01(t * 1.4 - k * 0.14);
        if (u <= 0 || u >= 1) continue;
        const cx = tx + 12 - u * 24, cy = ty + (k - 1) * 9;
        for (let a = -50; a <= 50; a += 5) {
          const rad = (a * Math.PI) / 180;
          ctx.globalAlpha = 1 - u * 0.8;
          dot(ctx, cx - Math.cos(rad) * 12 * (1 - Math.abs(a) / 120), cy + Math.sin(rad) * 12, k === 0 ? "#ffffff" : "#a8f0d0");
        }
      }
      ctx.globalAlpha = 1;
      for (let i = 0; i < 8; i++) {
        const u = clamp01(t * 1.2 - rnd(i, 9) * 0.3);
        if (u > 0 && u < 1) dot(ctx, tx + 16 - u * 40 + rnd(i, 10) * 6, ty + (rnd(i, 11) - 0.5) * 28, "#7ad890", 2, 1);
      }
      break;
    }
    case "ice": {
      for (let i = 0; i < 7; i++) {
        const ang = (i / 7) * Math.PI * 2;
        const cx = tx + Math.cos(ang) * (8 + rnd(i, 12) * 6), cy = ty + Math.sin(ang) * (6 + rnd(i, 13) * 6);
        const grow = clamp01(t * 3 - rnd(i, 14) * 0.5);
        const s = Math.round(grow * (3 + rnd(i, 15) * 3));
        if (t > 0.72) {
          const u = (t - 0.72) / 0.28;
          ctx.globalAlpha = 1 - u;
          dot(ctx, cx + Math.cos(ang) * u * 14, cy + Math.sin(ang) * u * 14, "#ffffff", 2, 2);
          ctx.globalAlpha = 1;
        } else if (s > 0) {
          for (let k = 0; k <= s; k++) {
            dot(ctx, cx - k, cy - s + k, "#bfe8ff", k * 2 + 1, 1);
            dot(ctx, cx - k, cy + s - k, "#7ac0f0", k * 2 + 1, 1);
          }
          dot(ctx, cx - 1, cy - s, "#ffffff", 1, 2);
        }
      }
      break;
    }
    case "bolt": {
      // 落雷: 白いせんこう → 太いいなずま（白い芯、黄と水色のふち）→ 足もとに水色の輪。画面も一瞬白く光る
      const strike = t > 0.06 && t < 0.62;
      if (t < 0.18) { ctx.globalAlpha = 0.34 * (1 - t / 0.18); ctx.fillStyle = "#ffffff"; ctx.fillRect(-4, -4, 420, 240); ctx.globalAlpha = 1; }
      if (strike) {
        const wob = Math.floor(t * 28);
        const jag = (y: number, k: number): number => tx + (rnd(Math.floor(y / 6) + k * 9, wob) - 0.5) * 12 * (1 - y / (ty + 14));
        for (const [thick, color, shift] of [[7, "#7ac8ff", 0], [5, "#fff08a", 0], [3, "#ffffff", 0]] as const) {
          let x = jag(0, 1), y = 0;
          while (y < ty + 8) {
            const ny = y + 5 + rnd(Math.floor(y), wob) * 4;
            const nx = ny >= ty + 8 ? tx : jag(ny, 1);
            ctx.globalAlpha = thick === 7 ? 0.5 : 1;
            line(ctx, x + shift, y, nx + shift, ny, color, thick);
            x = nx; y = ny;
          }
        }
        ctx.globalAlpha = 1;
        // 枝わかれ
        for (let b = 0; b < 3; b++) {
          const by = 10 + rnd(b, wob) * (ty - 10);
          const bx = jag(by, 1);
          const dir = b % 2 ? 1 : -1;
          line(ctx, bx, by, bx + dir * (6 + rnd(b, 3) * 8), by + 8 + rnd(b, 4) * 8, "#d8f0ff", 1);
        }
        star(ctx, tx, ty + 6, 6, "#fff8a0");
      }
      // 足もとの輪（水色）
      for (let k = 0; k < 2; k++) {
        const u = clamp01((t - 0.12) * 1.4 - k * 0.14);
        if (u > 0 && u < 1) ring(ctx, tx, ty + 14, 5 + u * 20, 2 + u * 6, k ? "#ffffff" : "#7ac8ff", 1 - u);
      }
      break;
    }
    case "rock": {
      for (let i = 0; i < 6; i++) {
        const x = tx + (rnd(i, 19) - 0.5) * 28;
        const u = clamp01(t * 1.3 - rnd(i, 20) * 0.3);
        if (u <= 0 || u >= 1) continue;
        const y = ty - 30 + (u < 0.55 ? u * 70 : 38 + (u - 0.55) * 8);
        dot(ctx, x, y, "#7a5a3a", 4, 4);
        dot(ctx, x, y, "#c8a070", 3, 3);
        dot(ctx, x + 2, y + 2, "#5a3a22", 2, 2);
        if (u > 0.55) { ctx.globalAlpha = 1 - u; dot(ctx, x - 3 - (u - 0.55) * 8, ty + 12, "#b09a80", 3, 2); dot(ctx, x + 3 + (u - 0.55) * 8, ty + 12, "#b09a80", 3, 2); ctx.globalAlpha = 1; }
      }
      break;
    }
    case "heal": {
      ctx.globalAlpha = 0.22 * Math.sin(Math.min(1, t) * Math.PI);
      dot(ctx, tx - 14, ty - 22, "#88f0a8", 28, 40);
      ctx.globalAlpha = 1;
      ring(ctx, tx, ty + 14, 6 + t * 10, 2 + t * 3, "#a8ffc8", 1 - t);
      for (let i = 0; i < 12; i++) {
        const u = (t * 1.2 + rnd(i, 21)) % 1;
        const x = tx + (rnd(i, 22) - 0.5) * 24, y = ty + 14 - u * 36;
        ctx.globalAlpha = Math.sin(u * Math.PI);
        if (i % 3 === 0) { dot(ctx, x - 1, y, "#ffffff", 3, 1); dot(ctx, x, y - 1, "#ffffff", 1, 3); }
        else dot(ctx, x, y, i % 2 ? "#a8ffc8" : "#ffffff", 2, 2);
      }
      ctx.globalAlpha = 1;
      break;
    }
    case "buff": {
      ring(ctx, tx, ty + 14, 10 + t * 4, 3, "#ffd860", 1 - t * 0.6);
      for (let i = 0; i < 4; i++) {
        const u = (t * 1.1 + i / 4) % 1;
        const x = tx + (i - 1.5) * 7, y = ty + 12 - u * 34;
        ctx.globalAlpha = Math.sin(u * Math.PI);
        for (let k = 0; k < 4; k++) { dot(ctx, x - k, y + k, "#ffd860"); dot(ctx, x + k, y + k, "#ffd860"); }
        dot(ctx, x, y, "#ffffff");
      }
      ctx.globalAlpha = 1;
      break;
    }
    case "debuff": {
      ring(ctx, tx, ty + 14, 10 + t * 4, 3, "#9060d0", 1 - t * 0.6);
      ctx.globalAlpha = 0.22 * Math.sin(Math.min(1, t) * Math.PI);
      dot(ctx, tx - 14, ty - 22, "#5a2a8a", 28, 40);
      ctx.globalAlpha = 1;
      for (let i = 0; i < 4; i++) {
        const u = (t * 1.1 + i / 4) % 1;
        const x = tx + (i - 1.5) * 7, y = ty - 22 + u * 34;
        ctx.globalAlpha = Math.sin(u * Math.PI);
        for (let k = 0; k < 4; k++) { dot(ctx, x - k, y - k, "#b080e8"); dot(ctx, x + k, y - k, "#b080e8"); }
        dot(ctx, x, y, "#e8d0ff");
      }
      ctx.globalAlpha = 1;
      break;
    }
    case "sleep": {
      for (let i = 0; i < 3; i++) {
        const u = clamp01(t * 1.2 - i * 0.18);
        if (u <= 0 || u >= 1) continue;
        const x = tx + 6 + i * 6 + u * 4, y = ty - 14 - i * 6 - u * 10;
        ctx.globalAlpha = Math.sin(u * Math.PI);
        const s = 3 + i;
        // Z の字
        dot(ctx, x, y, "#e8f0ff", s, 1);
        line(ctx, x + s - 1, y, x, y + s - 1, "#e8f0ff");
        dot(ctx, x, y + s - 1, "#e8f0ff", s, 1);
        dot(ctx, x, y + 1, "#9ab0ff", 0, 0);
      }
      ctx.globalAlpha = 1;
      break;
    }
    case "poison": {
      for (let i = 0; i < 10; i++) {
        const u = (t * 1.1 + rnd(i, 23)) % 1;
        const x = tx + (rnd(i, 24) - 0.5) * 20 + Math.sin(u * 8 + i) * 2, y = ty + 14 - u * 34;
        const r = 1 + (i % 3);
        ctx.globalAlpha = Math.sin(u * Math.PI);
        dot(ctx, x - r + 1, y, "#a050d8", r * 2 - 1, r * 2 - 1);
        dot(ctx, x - r + 1, y, "#d8a0ff", 1, 1);
        dot(ctx, x - r + 2, y + r * 2 - 2, "#6a2a9a", Math.max(1, r * 2 - 3), 1);
      }
      ctx.globalAlpha = 0.18 * Math.sin(Math.min(1, t) * Math.PI);
      dot(ctx, tx - 12, ty - 20, "#7a30b0", 24, 38);
      ctx.globalAlpha = 1;
      break;
    }
    case "confuse": {
      for (let i = 0; i < 3; i++) {
        const a = t * 9 + (i / 3) * Math.PI * 2;
        const x = tx + Math.cos(a) * 11, y = ty - 20 + Math.sin(a) * 3;
        star(ctx, x, y, 2, "#ffe070");
      }
      ctx.globalAlpha = 0.8 * fade + 0.2;
      for (let a = 0; a < 18; a++) {
        const rr = 1 + a * 0.4;
        dot(ctx, tx + Math.cos(a * 0.9 + t * 8) * rr, ty - 28 + Math.sin(a * 0.9 + t * 8) * rr * 0.5, "#ffffff");
      }
      ctx.globalAlpha = 1;
      break;
    }
    default: {
      // burst
      for (let i = 0; i < 10; i++) {
        const a = (i / 10) * Math.PI * 2;
        const r0 = 4 + t * 8, r1 = 8 + t * 26;
        line(ctx, tx + Math.cos(a) * r0, ty + Math.sin(a) * r0, tx + Math.cos(a) * r1, ty + Math.sin(a) * r1, i % 2 ? "#ffe890" : "#ffffff");
      }
      if (t < 0.3) star(ctx, tx, ty, 8 - Math.round(t * 20), "#ffffff");
    }
  }
  ctx.restore();
}
