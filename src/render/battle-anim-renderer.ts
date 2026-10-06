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
const GOLD = "#f2c14e";
const GOLD_D = "#a07a20";

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
      // 剣：つか（にぎり）・つば・かしら（つかの端）まで、手にもって振る
      const dx = -Math.sin((a * Math.PI) / 180), dy = -Math.cos((a * Math.PI) / 180);
      const gx = hand.x - dx * 5, gy = hand.y - dy * 5;           // かしら
      line(ctx, gx, gy, hand.x, hand.y, WOOD_D, 3);
      line(ctx, gx, gy, hand.x, hand.y, WOOD, 1);
      dot(ctx, gx - 1, gy - 1, GOLD, 3, 3);                       // かしら
      line(ctx, hand.x + dy * 3, hand.y - dx * 3, hand.x - dy * 3, hand.y + dx * 3, GOLD_D, 2);   // つば
      line(ctx, hand.x + dy * 3, hand.y - dx * 3, hand.x - dy * 3, hand.y + dx * 3, GOLD, 1);
      line(ctx, hand.x + dx * 2, hand.y + dy * 2, tx, ty, STEEL_D, 3);
      line(ctx, hand.x + dx * 2, hand.y + dy * 2, tx, ty, STEEL, 1);
      break;
    }
    case "stab": {
      const thrust = (u: number): number => Math.sin(clamp01((u - 0.1) / 0.3) * Math.PI) + Math.sin(clamp01((u - 0.5) / 0.3) * Math.PI);
      const e = thrust(t);
      const hx = hand.x - e * 4;                                  // 短剣ぜんたいが前へつき出る
      const tipx = hx - 3 - e * 5;
      // つか（にぎり）・つば・かしら
      line(ctx, hx + 6, hand.y, hx + 1, hand.y, WOOD_D, 3);
      line(ctx, hx + 6, hand.y, hx + 1, hand.y, WOOD, 1);
      dot(ctx, hx + 6, hand.y - 1, GOLD, 2, 3);                   // かしら
      dot(ctx, hx, hand.y - 3, GOLD_D, 2, 7);                     // つば
      dot(ctx, hx, hand.y - 3, GOLD, 1, 7);
      line(ctx, hx - 1, hand.y, tipx - 5, hand.y, STEEL_D, 3);
      line(ctx, hx - 1, hand.y, tipx - 5, hand.y, STEEL, 1);
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
      // 斧：えの手元（にぎるところ）まで、手にもって振る
      const bx = hand.x + Math.sin((a * Math.PI) / 180) * 5, by = hand.y + Math.cos((a * Math.PI) / 180) * 5;
      line(ctx, bx, by, tx, ty, WOOD_D, 3);
      line(ctx, bx, by, tx, ty, WOOD, 1);
      dot(ctx, bx - 1, by - 1, GOLD_D, 3, 3);                     // えじり（石づき）
      dot(ctx, hand.x - 1, hand.y - 1, GOLD, 2, 2);               // にぎりの巻き
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
  const rx = Math.max(20, w * 0.85), ry = rx * 0.32;
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
  const pillar = ease(u * 1.4) * h * 1.7;
  for (let i = 0; i < 7; i++) {
    const a = (i / 7) * Math.PI * 2;
    const px = at.x + Math.cos(a) * rx * 0.9;
    const base = feet + Math.sin(a) * ry * 0.9;
    ctx.globalAlpha = 0.45 * fadeIn * (a > Math.PI ? 0.6 : 1);
    for (let y = 0; y < pillar; y += 2) dot(ctx, px, base - y, y % 4 === 0 ? "#ffffff" : color);
  }
  // 外がわを、光の紋様（小さな四角）がまわりながら、体へ吸いこまれていく
  ctx.globalAlpha = fadeIn;
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * Math.PI * 2 + u * 8;
    const rr = (1 - ((u * 2 + i / 10) % 1)) * rx * 1.8 + 4;
    const x = at.x + Math.cos(a) * rr, y = at.y + Math.sin(a) * rr * 0.6;
    dot(ctx, x - 1, y - 1, color, 3, 3);
    dot(ctx, x, y, "#ffffff", 1, 1);
  }
  // 属性ごとのため: 炎＝陣のふちから小さな炎、雷＝陣のふちを走る電光
  if (fx === "fire") {
    // 陣のふちが、炎の帯になる（赤い根もと→だいだい→黄の先）
    ctx.globalAlpha = 0.95 * fadeIn;
    for (let i = 0; i < 52; i++) {
      const a = (i / 52) * Math.PI * 2;
      const fl = 3 + Math.round(rnd(i, Math.floor(u * 26)) * 12 * u) + Math.round(Math.sin(u * 30 + i) * 2);
      const fx0 = at.x + Math.cos(a) * rx * 1.04, fy0 = feet + Math.sin(a) * ry * 1.04;
      dot(ctx, fx0 - 1, fy0 - fl, "#ffd040", 3, Math.max(1, Math.floor(fl * 0.35)));
      dot(ctx, fx0 - 1, fy0 - Math.floor(fl * 0.65), "#f4862a", 3, Math.max(1, Math.floor(fl * 0.35)));
      dot(ctx, fx0 - 1, fy0 - Math.floor(fl * 0.3), "#c8381c", 3, Math.max(1, Math.floor(fl * 0.3)));
      if (rnd(i, 61) > 0.8) dot(ctx, fx0 + (rnd(i, 62) - 0.5) * 6, fy0 - fl - 3 - rnd(i, 63) * 6, "#ffe890", 1, 1);
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
  const r = 1 + Math.round(u * 7);
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

/** 攻撃の魔法（当たったとき、衝撃・画面のゆれを出す）。 */
export const DAMAGE_FX: ReadonlySet<FxId> = new Set<FxId>(["fire", "water", "light", "wind", "ice", "bolt", "rock", "burst"]);
/** 状態のしるし（毎ターン出る小さなもの。暗くしたり光らせたりしない）。 */
const STATUS_FX: ReadonlySet<FxId> = new Set<FxId>(["sleep", "poison", "confuse"]);

/** 術・魔法のあいだ、画面を少し暗くする（光が引き立つように）。prog は動き全体の進み（0〜1）。 */
export function drawSpellDim(ctx: CanvasRenderingContext2D, fx: FxId, prog: number, w: number, h: number): void {
  if (STATUS_FX.has(fx)) return;
  const env = Math.min(1, prog / 0.12, (1 - prog) / 0.15);
  if (env <= 0) return;
  ctx.save();
  ctx.globalAlpha = 0.5 * clamp01(env);
  ctx.fillStyle = "#06040f";
  ctx.fillRect(-8, -8, w + 16, h + 16);
  ctx.restore();
}

/** 唱え終えて、魔法を解き放つ瞬間: 使い手から、光の輪がはじけ、光の線が四方へ走る。k は 0〜1。 */
export function drawRelease(ctx: CanvasRenderingContext2D, at: Pt, color: string, k: number): void {
  const u = clamp01(k);
  ctx.save();
  ctx.globalAlpha = 0.28 * (1 - u);
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(-8, -8, 420, 240);
  for (let r = 0; r < 3; r++) {
    const v = clamp01(u * 1.3 - r * 0.15);
    if (v > 0 && v < 1) ring(ctx, at.x, at.y, 6 + v * 40, 6 + v * 40, r === 0 ? "#ffffff" : color, 1 - v);
  }
  ctx.globalAlpha = 1 - u;
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    const r0 = 4 + u * 20, r1 = 10 + u * 50;
    line(ctx, at.x + Math.cos(a) * r0, at.y + Math.sin(a) * r0, at.x + Math.cos(a) * r1, at.y + Math.sin(a) * r1, i % 2 ? color : "#ffffff");
  }
  star(ctx, at.x, at.y, Math.max(1, Math.round(10 * (1 - u))), color);
  ctx.restore();
}

/** 魔法が当たったときの衝撃: 色のついた光で画面がひかり、衝撃の輪が2重に広がり、火花が飛び散る。 */
function drawImpact(ctx: CanvasRenderingContext2D, tx: number, ty: number, gy: number, color: string, t: number, sc: number, first: boolean): void {
  const u = clamp01(t / 0.45);
  if (u >= 1) return;
  ctx.save();
  if (first && t < 0.16) {
    ctx.globalAlpha = 0.3 * (1 - t / 0.16);
    ctx.fillStyle = color;
    ctx.fillRect(-8, -8, 420, 240);
  }
  for (let k = 0; k < 2; k++) {
    const v = clamp01(u * 1.2 - k * 0.2);
    if (v > 0 && v < 1) {
      ring(ctx, tx, ty, (6 + v * 30) * sc, (6 + v * 30) * sc, k ? color : "#ffffff", 1 - v);
      ring(ctx, tx, gy, (8 + v * 34) * sc, (3 + v * 9) * sc, color, (1 - v) * 0.8);
    }
  }
  for (let i = 0; i < 18; i++) {
    const a = rnd(i, 31) * Math.PI * 2;
    const sp = (18 + rnd(i, 32) * 30) * sc;
    const x = tx + Math.cos(a) * sp * u;
    const y = ty + Math.sin(a) * sp * u + u * u * 18;
    ctx.globalAlpha = 1 - u;
    dot(ctx, x, y, i % 3 === 0 ? "#ffffff" : color, 2, 2);
  }
  if (t < 0.12) star(ctx, tx, ty, Math.round(12 * sc * (1 - t / 0.12)) + 2, color);
  ctx.restore();
}

export const FX_COLOR: Record<FxId, string> = {
  fire: "#ff9a40", water: "#6ab4ff", light: "#fff0a0", wind: "#a8f0d0", ice: "#bfe8ff", bolt: "#ffe848", rock: "#c8a070",
  burst: "#ffffff", heal: "#88f0a8", buff: "#ffd860", debuff: "#b080e8", sleep: "#9ab0ff", poison: "#b060e0", confuse: "#ffe070",
  meteor: "#c070ff", judgement: "#ffd860", blessing: "#fff0a0",
};

/** 魔法・状態のエフェクト。target は対象のからだの中心。 */
export function drawFx(ctx: CanvasRenderingContext2D, fx: FxId, t: number, target: Pt, opts: { from?: Pt; area?: boolean; first?: boolean } = {}): void {
  const { x: tx, y: ty } = target;
  const fade = 1 - t;
  // 対象の大きさ（人は1、大きい敵ほど炎も大きく、足もとはその人の足もとに）
  const sc = Math.min(2.2, Math.max(0.9, (target.h ?? 32) / 32));
  const gy = ty + (target.h ?? 32) / 2 - 2;
  const first = opts.first ?? true;
  // 当たる瞬間（飛んでいく魔法は、飛び終わってから）の衝撃
  if (DAMAGE_FX.has(fx) && fx !== "fire" && fx !== "bolt") {
    const hitAt = opts.from && !opts.area && (fx === "water") ? 0.45 : fx === "rock" ? 0.3 : fx === "ice" ? 0.2 : 0.08;
    if (t >= hitAt) drawImpact(ctx, tx, ty, gy, FX_COLOR[fx], (t - hitAt) / (1 - hitAt), sc, first);
  } else if (fx === "fire" || fx === "bolt") {
    if (t >= 0.1) drawImpact(ctx, tx, ty, gy, FX_COLOR[fx], (t - 0.1) / 0.9, sc * 0.8, false);
  }
  ctx.save();
  switch (fx) {
    case "fire": {
      // 炎（見本の動画のまね）: 火の玉は彗星のかたち。爆発は、衝撃の輪・黄白の核・飛び散る火の粉・けむり、画面も赤く光る。火柱は、太く高く、ねじれて立ち、地面にも炎が走る
      if (opts.area) {
        // 火柱（全体）: 全員の足もとから、太い炎の柱がいくつも高く燃えあがり（先は赤、中はだいだい、根もとは黄と白）、
        // 終わりに赤いしずく型の炎が残り、灰色のけむりがのぼる。画面が赤く染まる
        const u = clamp01(t * 1.08);
        ctx.globalAlpha = 0.24 * Math.sin(Math.min(1, u * 1.3) * Math.PI);
        ctx.fillStyle = "#ff6a20";
        ctx.fillRect(-4, -4, 420, 240);
        ctx.globalAlpha = 1;
        const rise = ease(Math.min(1, u * 1.5));
        const fall = u > 0.7 ? (u - 0.7) / 0.3 : 0;
        const sa = Math.min(sc, 1.25);
        const hgt = 96 * sa * rise * (1 - fall * 0.85);
        for (let col = -2; col <= 2; col++) {
          const cx = tx + col * 9 * Math.min(sc, 1.4);
          const colH = hgt * (0.7 + 0.3 * rnd(col + 5, 90) + Math.sin(t * 16 + col) * 0.06);
          for (let y = 0; y < colH; y += 1) {
            const q = y / Math.max(1, colH);
            const half = Math.max(1, Math.round((9 * Math.min(sc, 1.15) - q * 6 * Math.min(sc, 1.15)) + (rnd(Math.floor(y / 2) + col * 31, Math.floor(t * 22)) - 0.5) * 4));
            const sway = Math.round(Math.sin(y * 0.14 + t * 15 + col * 2) * (1.5 + q * 3));
            const c2 = q < 0.15 ? "#fffbe0" : q < 0.35 ? "#ffd050" : q < 0.7 ? "#f4862a" : "#d83a1c";
            dot(ctx, cx + sway - half, gy - y, c2, half * 2, 1);
          }
          if (u > 0.55) {
            // 先に残る、赤いしずく型の炎
            const dropY = gy - colH - 3;
            ctx.globalAlpha = 1 - fall * 0.7;
            dot(ctx, cx - 2, dropY, "#d83a1c", 5, 6);
            dot(ctx, cx - 1, dropY - 2, "#d83a1c", 3, 2);
            dot(ctx, cx - 1, dropY + 1, "#f4862a", 3, 4);
            ctx.globalAlpha = 1;
          }
        }
        // 火の粉と灰色のけむり
        for (let i = 0; i < 36; i++) {
          const v = clamp01(t * 1.3 - rnd(i, 32) * 0.4);
          if (v <= 0 || v >= 1) continue;
          dot(ctx, tx + (rnd(i, 33) - 0.5) * 50 + Math.sin(v * 9 + i) * 3, (gy - 2) - v * 90, v < 0.6 ? "#ffd050" : "#ff8a30", 2, 2);
        }
        ctx.globalAlpha = 0.55;
        for (let i = 0; i < 12; i++) {
          const v = clamp01(t * 1.2 - 0.25 - rnd(i, 25) * 0.25);
          if (v > 0 && v < 1) dot(ctx, tx + (rnd(i, 26) - 0.5) * 40 + v * 6, ty - 30 - v * 30, "#6a6670", 7, 5);
        }
        ctx.globalAlpha = 1;
        break;
      }
      const f = opts.from;
      const flight = f ? clamp01(t / 0.42) : 1;
      if (f && flight < 1) {
        // 大きな火の玉: 先がまるく白く、うしろにほそくなる炎の尾（彗星のかたち）
        const arc = (q: number): Pt => ({ x: f.x + (tx - f.x) * q, y: f.y + (ty - f.y) * q - Math.sin(q * Math.PI) * 18 });
        const head = arc(flight);
        const back = arc(Math.max(0, flight - 0.3));
        const dx = head.x - back.x, dy = head.y - back.y, len = Math.max(1, Math.hypot(dx, dy));
        const ux = dx / len, uy = dy / len;
        for (let k = 0; k <= len; k += 1) {
          const q = k / len;                              // 0＝尾の先、1＝頭
          const half = Math.max(1, Math.round(1 + q * 7 + (rnd(k, Math.floor(t * 40)) - 0.5) * 2));
          const px = back.x + ux * k, py = back.y + uy * k;
          dot(ctx, px - half, py - half, q > 0.7 ? "#f4862a" : "#c8381c", half * 2 + 1, half * 2 + 1);
          if (half >= 3) dot(ctx, px - half + 1, py - half + 1, q > 0.8 ? "#ffd050" : "#f4862a", half * 2 - 1, half * 2 - 1);
          if (half >= 5) dot(ctx, px - half + 3, py - half + 3, "#fff6c0", half * 2 - 5, half * 2 - 5);
        }
        for (let i = 0; i < 8; i++) dot(ctx, back.x + (head.x - back.x) * rnd(i, 70) + (rnd(i, 71) - 0.5) * 12, back.y + (head.y - back.y) * rnd(i, 70) + (rnd(i, 72) - 0.5) * 12, "#ffd050", 2, 2);
        break;
      }
      // 着弾: 白い大爆発（細い火線が四方へ走る）→ 対象の上に、しずく型の大きな炎が燃えあがる → 弱まって消える
      const e = f ? clamp01((t - 0.42) / 0.58) : t;
      if (e < 0.22) { ctx.globalAlpha = 0.5 * (1 - e / 0.22); ctx.fillStyle = "#fff0c0"; ctx.fillRect(-4, -4, 420, 240); ctx.globalAlpha = 1; }
      else if (e < 0.7) { ctx.globalAlpha = 0.14 * (1 - (e - 0.22) / 0.48); ctx.fillStyle = "#ff5a18"; ctx.fillRect(-4, -4, 420, 240); ctx.globalAlpha = 1; }
      if (e < 0.55) {
        const rad = (4 + ease(e / 0.55) * 20) * sc;
        ctx.globalAlpha = 1 - Math.max(0, e / 0.55 - 0.5) * 1.6;
        for (let yy = -Math.floor(rad); yy <= rad; yy++) for (let xx = -Math.floor(rad); xx <= rad; xx++) {
          const d = Math.hypot(xx, yy * 1.1) + (rnd(xx * 7 + yy, Math.floor(e * 14)) - 0.5) * 0.18 * rad;
          if (d > rad) continue;
          dot(ctx, tx + xx, ty + yy, d < rad * 0.4 ? "#fffbe0" : d < rad * 0.68 ? "#ffd050" : "#f4862a");
        }
        ctx.globalAlpha = 1;
        // 細く長い火線
        for (let i = 0; i < 16; i++) {
          const a = (i / 16) * Math.PI * 2 + 0.17 + (rnd(i, 80) - 0.5) * 0.3;
          const r0 = rad + 2, r1 = rad + 8 + ease(e / 0.55) * (16 + rnd(i, 81) * 26);
          line(ctx, tx + Math.cos(a) * r0, ty + Math.sin(a) * r0, tx + Math.cos(a) * r1, ty + Math.sin(a) * r1, rnd(i, 82) > 0.5 ? "#ffb040" : "#ff7a28");
        }
        ring(ctx, tx, ty + 6, 6 + e * 40, 3 + e * 16, "#ffe8a0", 1 - e * 1.4);
      }
      if (e > 0.12) {
        // しずく型の炎（根もとが太く、先がとがる。赤い外側・だいだい・黄・白い芯）
        const life = (e - 0.12) / 0.88;
        const H = Math.sin(Math.min(1, life * 1.15) * Math.PI) ** 0.7 * 50 * sc + 4;
        const base = gy;
        for (let y = 0; y < H; y++) {
          const q = y / H;
          const half = Math.max(0, Math.round(11 * sc * Math.sin(Math.PI * Math.min(1, (q + 0.12) / 1.12)) ** 0.9 * (1 - q * 0.45) + (rnd(y, Math.floor(t * 28)) - 0.5) * 3));
          if (half <= 0) continue;
          const sway = Math.round(Math.sin(y * 0.18 + t * 20) * 2.2 * q);
          dot(ctx, tx - half + sway, base - y, "#c8381c", half * 2, 1);
          const h2 = Math.round(half * 0.78);
          dot(ctx, tx - h2 + sway, base - y, "#f4862a", h2 * 2, 1);
          const h3 = Math.round(half * 0.5);
          if (h3 > 0) dot(ctx, tx - h3 + sway, base - y, "#ffd050", h3 * 2, 1);
          const h4 = Math.round(half * 0.22);
          if (h4 > 0 && q < 0.6) dot(ctx, tx - h4 + sway, base - y, "#fffbe0", h4 * 2, 1);
        }
        for (let i = 0; i < 14; i++) {
          const v = clamp01(life * 1.4 - rnd(i, 83) * 0.5);
          if (v > 0 && v < 1) dot(ctx, tx + (rnd(i, 84) - 0.5) * 26 + Math.sin(v * 8 + i) * 3, base - 6 - v * 60, v < 0.5 ? "#ffd050" : "#ff8a30", 2, 2);
        }
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
      // 水柱: 足もとから太い水の柱が噴き上がり、てっぺんでしぶきが広がって、落ちてくる
      {
        const w0 = Math.round(9 * Math.min(sc, 1.4));
        const rise = ease(clamp01(t / 0.3));
        const fall = clamp01((t - 0.62) / 0.38);
        const hgt = (70 * Math.min(sc, 1.4)) * rise * (1 - fall);
        for (let y = 0; y < hgt; y++) {
          const q = y / Math.max(1, hgt);
          const half = Math.max(2, Math.round(w0 * (1 - q * 0.45) + Math.sin(y * 0.3 + t * 30) * 1.5));
          dot(ctx, tx - half, gy - y, "#2a5ea8", half * 2, 1);
          dot(ctx, tx - half + 2, gy - y, q > 0.85 ? "#e8f6ff" : "#5aa0f0", Math.max(1, half * 2 - 4), 1);
          if ((y + Math.floor(t * 40)) % 7 === 0) dot(ctx, tx - half + 3 + ((y * 3) % Math.max(1, half)), gy - y, "#ffffff", 2, 1);
        }
        if (hgt > 10) for (let i = 0; i < 14; i++) {
          const a = Math.PI + (i / 13) * Math.PI;
          const v = clamp01(t * 2 - 0.4);
          dot(ctx, tx + Math.cos(a) * (6 + v * 24), gy - hgt - Math.sin(a) * (4 + v * 10) * -1 + v * v * 20, i % 2 ? "#ffffff" : "#9ad0ff", 2, 2);
        }
      }
      for (let k = 0; k < 3; k++) {
        const u = clamp01(t * 1.3 - k * 0.18);
        if (u > 0 && u < 1) ring(ctx, tx, (gy - 2), 4 + u * 30, 1.5 + u * 9, k === 0 ? "#e8f6ff" : "#6ab4ff", 1 - u);
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
      // 天から光が降りそそぐ: 画面が白くかがやき、十字の光が走り、光の羽がまう
      if (first && t < 0.3) { ctx.globalAlpha = 0.28 * (1 - t / 0.3); ctx.fillStyle = "#fff6d0"; ctx.fillRect(-8, -8, 420, 240); ctx.globalAlpha = 1; }
      {
        const cr = Math.sin(clamp01(t / 0.7) * Math.PI);
        ctx.globalAlpha = 0.85 * cr;
        dot(ctx, tx - 40 * cr * sc, ty - 1, "#fff6c0", Math.round(80 * cr * sc), 3);
        dot(ctx, tx - 1, ty - 40 * cr * sc, "#fff6c0", 3, Math.round(80 * cr * sc));
        dot(ctx, tx - 30 * cr * sc, ty, "#ffffff", Math.round(60 * cr * sc), 1);
        dot(ctx, tx, ty - 30 * cr * sc, "#ffffff", 1, Math.round(60 * cr * sc));
        ctx.globalAlpha = 1;
        for (let i = 0; i < 10; i++) {
          const u = (t * 0.9 + rnd(i, 41)) % 1;
          const x = tx + (rnd(i, 42) - 0.5) * 50 + Math.sin(u * 6 + i) * 4;
          const y = -4 + u * (gy + 4);
          ctx.globalAlpha = Math.sin(u * Math.PI) * fade;
          dot(ctx, x, y, "#ffffff", 2, 1);
          dot(ctx, x + 1, y + 1, "#ffe890", 1, 2);
        }
        ctx.globalAlpha = 1;
      }
      const w = Math.max(1, Math.round(16 * Math.min(sc, 1.5) * (1 - Math.abs(t - 0.4) * 1.6)));
      ctx.globalAlpha = 0.5 * fade + 0.2;
      dot(ctx, tx - w, 0, "#ffe890", w * 2, gy);
      ctx.globalAlpha = 0.9;
      dot(ctx, tx - Math.ceil(w / 3), 0, "#ffffff", Math.ceil(w / 3) * 2, gy);
      ctx.globalAlpha = 1;
      for (let i = 0; i < 9; i++) {
        const u = clamp01(t * 1.4 - rnd(i, 6) * 0.4);
        if (u <= 0 || u >= 1) continue;
        star(ctx, tx + (rnd(i, 7) - 0.5) * 30, ty + (rnd(i, 8) - 0.5) * 30 - u * 6, u < 0.5 ? 2 : 1, "#ffe890");
      }
      ring(ctx, tx, (gy - 2), 6 + t * 18, 2 + t * 5, "#fff6c0", 1 - t);
      break;
    }
    case "wind": {
      // 竜巻: 足もとから、らせんの風の柱が立ち、木の葉や砂が巻き上げられる
      {
        const grow = ease(clamp01(t / 0.3)) * (1 - clamp01((t - 0.75) / 0.25));
        const hgt = 64 * Math.min(sc, 1.4) * grow;
        for (let y = 0; y < hgt; y += 2) {
          const q = y / Math.max(1, hgt);
          const rr = (5 + q * 16) * Math.min(sc, 1.3);
          for (let k = 0; k < 2; k++) {
            const a = y * 0.35 - t * 40 + k * Math.PI;
            const x = tx + Math.cos(a) * rr;
            ctx.globalAlpha = (Math.sin(a) > 0 ? 1 : 0.5) * grow;
            dot(ctx, x - 1, gy - y, k ? "#a8f0d0" : "#ffffff", 4, 2);
            dot(ctx, tx - (x - tx) - 1, gy - y, "#6ad0a0", 2, 2);
          }
        }
        for (let i = 0; i < 12; i++) {
          const q = (t * 1.6 + rnd(i, 51)) % 1;
          const a = q * 20 + i;
          const rr = (6 + q * 18) * Math.min(sc, 1.3);
          ctx.globalAlpha = grow * Math.sin(q * Math.PI);
          dot(ctx, tx + Math.cos(a) * rr, gy - q * hgt, i % 3 ? "#7ad890" : "#c8a070", 2, 2);
        }
        ctx.globalAlpha = 1;
      }
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
      // 足もとが凍りつき、大きな氷の柱が何本も突き出て、最後にくだけ散る
      {
        if (first && t < 0.25) { ctx.globalAlpha = 0.2 * (1 - t / 0.25); ctx.fillStyle = "#dff4ff"; ctx.fillRect(-8, -8, 420, 240); ctx.globalAlpha = 1; }
        const shatter = clamp01((t - 0.68) / 0.32);
        ring(ctx, tx, gy, 22 * Math.min(sc, 1.5) * ease(t / 0.25), 6 * Math.min(sc, 1.5) * ease(t / 0.25), "#e8f8ff", 1 - shatter);
        for (let i = 0; i < 5; i++) {
          const off = (i - 2) * 8 * Math.min(sc, 1.4);
          const tall = (16 + (i === 2 ? 22 : rnd(i, 61) * 14)) * Math.min(sc, 1.5);
          const g = ease(clamp01((t - i * 0.03) / 0.18));
          const hgt = tall * g;
          if (shatter <= 0) {
            for (let y = 0; y < hgt; y++) {
              const half = Math.max(1, Math.round(4 * (1 - y / tall) + 1));
              dot(ctx, tx + off - half, gy - y, "#7ac0f0", half * 2, 1);
              dot(ctx, tx + off - half + 1, gy - y, y > hgt - 3 ? "#ffffff" : "#bfe8ff", Math.max(1, half - 1), 1);
            }
          } else {
            for (let k = 0; k < 6; k++) {
              const a = rnd(i * 7 + k, 62) * Math.PI * 2;
              ctx.globalAlpha = 1 - shatter;
              dot(ctx, tx + off + Math.cos(a) * shatter * 26, gy - tall * 0.5 + Math.sin(a) * shatter * 20 + shatter * shatter * 14, k % 2 ? "#ffffff" : "#bfe8ff", 2, 2);
            }
            ctx.globalAlpha = 1;
          }
        }
      }
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
        const jag = (y: number, k: number): number => tx + (rnd(Math.floor(y / 6) + k * 9, wob) - 0.5) * 12 * (1 - y / (gy));
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
        if (u > 0 && u < 1) ring(ctx, tx, gy, 5 + u * 20, 2 + u * 6, k ? "#ffffff" : "#7ac8ff", 1 - u);
      }
      break;
    }
    case "rock": {
      // 地面が割れて、岩のとげが突き出し、土けむりが舞う
      {
        const up = ease(clamp01((t - 0.25) / 0.15)) * (1 - clamp01((t - 0.75) / 0.25));
        for (let i = 0; i < 6; i++) {
          const off = (i - 2.5) * 9 * Math.min(sc, 1.4);
          const full = (18 + rnd(i, 71) * 22) * Math.min(sc, 1.4);
          const tall = full * up;
          for (let y = 0; y < tall; y++) {
            const half = Math.max(1, Math.round(6 * (1 - y / Math.max(1, full)) + 1));
            dot(ctx, tx + off - half, gy - y, "#4a3220", half * 2, 1);
            dot(ctx, tx + off - half + 1, gy - y, "#8a6a48", Math.max(1, half - 1), 1);
            dot(ctx, tx + off, gy - y, "#b8946a", Math.max(1, Math.floor(half / 2)), 1);
          }
        }
        for (let i = 0; i < 10; i++) {
          const v = clamp01((t - 0.3) * 1.6 - rnd(i, 72) * 0.2);
          if (v <= 0 || v >= 1) continue;
          ctx.globalAlpha = 0.6 * (1 - v);
          const r = 3 + v * 7;
          dot(ctx, tx + (rnd(i, 73) - 0.5) * 50 * v - r, gy - 4 - v * 16 - r, "#b09a80", r * 2, r * 1.4);
        }
        ctx.globalAlpha = 1;
        // 大岩（上から落ちてくる）
        const fallU = clamp01(t / 0.3);
        if (fallU < 1) {
          const by = -20 + (ty + 10) * fallU * fallU;
          const R = Math.round(13 * Math.min(sc, 1.5));
          dot(ctx, tx - R, by - R, "#5a3a22", R * 2, R * 2);
          dot(ctx, tx - R + 1, by - R + 1, "#a0784e", R * 2 - 3, R * 2 - 3);
          dot(ctx, tx - R + 2, by - R + 2, "#c8a070", R - 1, R - 2);
        }
      }
      for (let i = 0; i < 6; i++) {
        const x = tx + (rnd(i, 19) - 0.5) * 28;
        const u = clamp01(t * 1.3 - rnd(i, 20) * 0.3);
        if (u <= 0 || u >= 1) continue;
        const y = ty - 30 + (u < 0.55 ? u * 70 : 38 + (u - 0.55) * 8);
        dot(ctx, x, y, "#7a5a3a", 4, 4);
        dot(ctx, x, y, "#c8a070", 3, 3);
        dot(ctx, x + 2, y + 2, "#5a3a22", 2, 2);
        if (u > 0.55) { ctx.globalAlpha = 1 - u; dot(ctx, x - 3 - (u - 0.55) * 8, (gy - 2), "#b09a80", 3, 2); dot(ctx, x + 3 + (u - 0.55) * 8, (gy - 2), "#b09a80", 3, 2); ctx.globalAlpha = 1; }
      }
      break;
    }
    case "heal": {
      // やわらかな光の柱が降り、足もとに緑の紋様がまわり、光の粒と葉が舞いあがる
      {
        const env = Math.sin(clamp01(t) * Math.PI);
        const cw = Math.round(14 * Math.min(sc, 1.4));
        ctx.globalAlpha = 0.35 * env;
        dot(ctx, tx - cw, -4, "#c8ffd8", cw * 2, gy + 4);
        ctx.globalAlpha = 0.5 * env;
        dot(ctx, tx - Math.round(cw / 3), -4, "#ffffff", Math.round(cw / 3) * 2, gy + 4);
        ctx.globalAlpha = env;
        for (let i = 0; i < 12; i++) {
          const a = (i / 12) * Math.PI * 2 + t * 6;
          dot(ctx, tx + Math.cos(a) * 18 * Math.min(sc, 1.4), gy + Math.sin(a) * 5, i % 2 ? "#ffffff" : "#88f0a8", 2, 1);
        }
        ring(ctx, tx, gy, 18 * Math.min(sc, 1.4), 5, "#a8ffc8", env);
        for (let i = 0; i < 6; i++) {
          const u = (t * 1.4 + i / 6) % 1;
          ctx.globalAlpha = Math.sin(u * Math.PI);
          const x = tx + Math.sin(u * 7 + i) * 14, y = gy - u * 50;
          dot(ctx, x, y, "#4ac070", 3, 2);
          dot(ctx, x + 1, y, "#a8ffc8", 1, 1);
        }
        ctx.globalAlpha = 1;
      }
      ctx.globalAlpha = 0.22 * Math.sin(Math.min(1, t) * Math.PI);
      dot(ctx, tx - 14, ty - 22, "#88f0a8", 28, 40);
      ctx.globalAlpha = 1;
      ring(ctx, tx, gy, 6 + t * 10, 2 + t * 3, "#a8ffc8", 1 - t);
      for (let i = 0; i < 12; i++) {
        const u = (t * 1.2 + rnd(i, 21)) % 1;
        const x = tx + (rnd(i, 22) - 0.5) * 24, y = gy - u * 36;
        ctx.globalAlpha = Math.sin(u * Math.PI);
        if (i % 3 === 0) { dot(ctx, x - 1, y, "#ffffff", 3, 1); dot(ctx, x, y - 1, "#ffffff", 1, 3); }
        else dot(ctx, x, y, i % 2 ? "#a8ffc8" : "#ffffff", 2, 2);
      }
      ctx.globalAlpha = 1;
      break;
    }
    case "buff": {
      // 金色のオーラが、体を包んで燃えあがる
      {
        const env = Math.sin(clamp01(t) * Math.PI);
        ctx.globalAlpha = 0.3 * env;
        dot(ctx, tx - 13, gy - 56, "#ffe890", 26, 56);
        ctx.globalAlpha = 0.45 * env;
        dot(ctx, tx - 6, gy - 56, "#fff6d0", 12, 56);
      }
      for (let i = 0; i < 36; i++) {
        const u = (t * 1.5 + rnd(i, 81)) % 1;
        const x = tx + (rnd(i, 82) - 0.5) * 30 + Math.sin(u * 9 + i) * 2;
        ctx.globalAlpha = Math.sin(u * Math.PI) * (1 - t * 0.5);
        dot(ctx, x, gy - u * 60, i % 3 ? "#ffd860" : "#ffffff", 2, 4);
      }
      ctx.globalAlpha = 1;
      ring(ctx, tx, gy, 16 + Math.sin(t * 20) * 2, 5, "#fff0a0", 1 - t * 0.6);
      ring(ctx, tx, gy, 10 + t * 4, 3, "#ffd860", 1 - t * 0.6);
      for (let i = 0; i < 4; i++) {
        const u = (t * 1.1 + i / 4) % 1;
        const x = tx + (i - 1.5) * 7, y = (gy - 2) - u * 34;
        ctx.globalAlpha = Math.sin(u * Math.PI);
        for (let k = 0; k < 4; k++) { dot(ctx, x - k, y + k, "#ffd860"); dot(ctx, x + k, y + k, "#ffd860"); }
        dot(ctx, x, y, "#ffffff");
      }
      ctx.globalAlpha = 1;
      break;
    }
    case "debuff": {
      // 黒むらさきの霧が、上からのしかかり、鎖のような輪がしめつける
      {
        const env = Math.sin(clamp01(t) * Math.PI);
        ctx.globalAlpha = 0.35 * env;
        dot(ctx, tx - 20, ty - 34, "#2a0a4a", 40, 60);
      }
      for (let i = 0; i < 34; i++) {
        const u = (t * 1.3 + rnd(i, 91)) % 1;
        const x = tx + (rnd(i, 92) - 0.5) * 40;
        ctx.globalAlpha = 0.8 * Math.sin(u * Math.PI);
        dot(ctx, x, ty - 40 + u * 56, i % 2 ? "#5a2a8a" : "#b080e8", 4, 3);
      }
      ctx.globalAlpha = 1;
      for (let k = 0; k < 3; k++) {
        const shrink = 1 - clamp01(t * 1.5 - k * 0.1) * 0.5;
        ring(ctx, tx, ty - 8 + k * 10, 24 * shrink, 6 * shrink, k === 1 ? "#e8d0ff" : "#9060d0", 1 - t * 0.7);
        ring(ctx, tx, ty - 7 + k * 10, 24 * shrink, 6 * shrink, "#5a2a8a", 1 - t * 0.7);
      }
      ring(ctx, tx, gy, 10 + t * 4, 3, "#9060d0", 1 - t * 0.6);
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
        const x = tx + (rnd(i, 24) - 0.5) * 20 + Math.sin(u * 8 + i) * 2, y = gy - u * 34;
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
      for (let k = 0; k < 3; k++) {
        const v = clamp01(t * 1.4 - k * 0.12);
        if (v > 0 && v < 1) ring(ctx, tx, ty, (8 + v * 34) * sc, (8 + v * 34) * sc, k === 1 ? "#ffe890" : "#ffffff", 1 - v);
      }
      for (let i = 0; i < 16; i++) {
        const a = (i / 16) * Math.PI * 2;
        const r0 = 4 + t * 10, r1 = 10 + t * 40;
        line(ctx, tx + Math.cos(a) * r0, ty + Math.sin(a) * r0, tx + Math.cos(a) * r1, ty + Math.sin(a) * r1, i % 2 ? "#ffe890" : "#ffffff");
      }
      if (t < 0.3) star(ctx, tx, ty, 8 - Math.round(t * 20), "#ffffff");
    }
  }
  ctx.restore();
}
