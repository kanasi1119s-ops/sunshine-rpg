import type { FxId, WeaponMotion } from "../game/battle/battle-anim";

/**
 * 戦闘の動きの絵（ドット）: 武器をふる・つく・矢をはなつ・杖をかざす、と、魔法のエフェクト。
 * 画像は使わず、1ドットずつの四角で描く。経過 t（0〜1）だけで決まる（毎フレーム同じ絵になる）。
 * 味方は右、敵は左にいて、味方は左（敵のほう）を向く。
 */
export interface Pt {
  x: number;
  y: number;
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
      if (t > 0.05 && t < 0.7) {
        ctx.save();
        ctx.globalAlpha = Math.min(1, (0.7 - t) * 3) * 0.8;
        ring(ctx, hand.x + 1, hand.y + 16, 12 * ease(t / 0.25), 4 * ease(t / 0.25), glow);
        ring(ctx, hand.x + 1, hand.y + 16, 8 * ease(t / 0.25), 2.6 * ease(t / 0.25), "#ffffff");
        ctx.restore();
      }
      for (let k = 0; k < 6; k++) {
        const u = (t * 1.6 + k / 6) % 1;
        dot(ctx, sx + (rnd(k) - 0.5) * 14, top + 6 - u * 22, glow);
      }
      break;
    }
  }
}

/** 魔法を唱える敵の足もとに、光が集まる（唱えはじめ〜魔法が出るまで）。 */
export function drawCastGlow(ctx: CanvasRenderingContext2D, at: Pt, color: string, t: number): void {
  const u = clamp01(t);
  ctx.save();
  ctx.globalAlpha = 0.25 + 0.5 * u;
  ring(ctx, at.x, at.y + 12, 18 - 8 * u, 6 - 2 * u, color);
  ring(ctx, at.x, at.y + 12, 12 - 6 * u, 4 - 2 * u, "#ffffff");
  ctx.globalAlpha = 1;
  for (let i = 0; i < 10; i++) {
    const r = 22 * (1 - u) + 4;
    const a = (i / 10) * Math.PI * 2 + u * 3;
    dot(ctx, at.x + Math.cos(a) * r, at.y + 6 + Math.sin(a) * r * 0.6, i % 2 ? color : "#ffffff", 2, 2);
  }
  if (u > 0.7) star(ctx, at.x, at.y, 3, color);
  ctx.restore();
}

export const FX_COLOR: Record<FxId, string> = {
  fire: "#ff9a40", water: "#6ab4ff", light: "#fff0a0", wind: "#a8f0d0", ice: "#bfe8ff", bolt: "#ffe848", rock: "#c8a070",
  burst: "#ffffff", heal: "#88f0a8", buff: "#ffd860", debuff: "#b080e8", sleep: "#9ab0ff", poison: "#b060e0", confuse: "#ffe070",
};

/** 魔法・状態のエフェクト。target は対象のからだの中心。 */
export function drawFx(ctx: CanvasRenderingContext2D, fx: FxId, t: number, target: Pt): void {
  const { x: tx, y: ty } = target;
  const fade = 1 - t;
  ctx.save();
  switch (fx) {
    case "fire": {
      if (t < 0.22) { ctx.globalAlpha = 1 - t * 4; ring(ctx, tx, ty, 4 + t * 70, 4 + t * 60, "#fff2a0"); ctx.globalAlpha = 1; }
      for (let i = 0; i < 26; i++) {
        const life = clamp01(t * 1.25 - rnd(i, 1) * 0.25);
        if (life <= 0 || life >= 1) continue;
        const x = tx + (rnd(i, 2) - 0.5) * 24;
        const y = ty + 14 - life * (26 + rnd(i, 3) * 14);
        const size = Math.max(1, Math.round(4 * (1 - life) + 1));
        dot(ctx, x, y, life < 0.3 ? "#fff6c0" : life < 0.55 ? "#ffc040" : life < 0.8 ? "#f06a20" : "#8a2a14", size, size);
      }
      break;
    }
    case "water": {
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
      const flash = (t > 0.08 && t < 0.3) || (t > 0.45 && t < 0.62);
      if (flash) {
        ctx.globalAlpha = 0.25;
        dot(ctx, tx - 40, 0, "#fff8c0", 80, ty + 20);
        ctx.globalAlpha = 1;
        let x = tx + (rnd(Math.floor(t * 20), 16) - 0.5) * 8, y = 0;
        while (y < ty + 8) {
          const nx = tx + (rnd(Math.floor(y), 17 + Math.floor(t * 12)) - 0.5) * 14 * (1 - y / (ty + 10));
          const ny = y + 6 + rnd(Math.floor(y), 18) * 5;
          line(ctx, x, y, nx, ny, "#ffe040", 3);
          line(ctx, x, y, nx, ny, "#ffffff", 1);
          x = nx; y = ny;
        }
        star(ctx, tx, ty + 6, 6, "#fff8a0");
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
