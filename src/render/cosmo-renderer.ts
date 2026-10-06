import type { BattleState, Combatant } from "../game/battle/types";
import type { BattleAnimSpec } from "../game/battle/battle-anim";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import { drawSpellFrame } from "./spell-fx-renderer";
import type { Pt } from "./battle-anim-renderer";

/**
 * レジェンドの装備「コスモリングライト」の戦闘の見た目（2026-10-06、人間の指示）。
 *  - 戦闘のはじめ: 環がかがやき、鎧がはまる（装着。`cosmo/charge` のコマ）。それまではふだんの姿
 *  - 装着したあと: 宙に浮き、体のまわりがいつも光る。6基の追尾砲台が、まわりをぐるぐる回る（待機中）
 *  - たたかう: 攻撃態勢（腕砲を敵へ向け、羽を広げる）。砲台が舞い上がって敵のまわりへ飛び、まわりを飛び回りながら、
 *    1基ずつ雷のビーム（`cosmo/bolt`）を撃つ。当たると命中の光（`cosmo/hit`）。6発撃ったら、持ち主のまわりへもどる
 * ユーリは、ドット絵エディタで描いた鎧の絵（`cosmo:idle`・`cosmo:attack`、50×50）。ほかの人は、ふだんの姿に光の環と砲台。
 */

const PODS = 6;
/** 待機の絵（50×50）の中で、体（16×32）の左上の位置。 */
const BODY_OX = 17;
const BODY_OY = 12;

/** 装着がすんだ人。戦闘ごとに、`resetCosmo` で空にする。 */
const armed = new Set<string>();
interface PodMemory {
  pos: { x: number; y: number }[];
  at: number;
  last: "deploy" | "shot" | null;
  lastShot: number;
  target: Pt | null;
}
const memory = new Map<string, PodMemory>();

/** 新しい戦闘が始まったときに呼ぶ（装着をやり直す）。 */
export function resetCosmo(): void {
  armed.clear();
  memory.clear();
}

/** 浮いている高さ（ドット。上がマイナス）。ゆっくり上下にゆれる（人間の指示「もっと飛んでもいいや」で高く）。 */
export function cosmoHover(nowMs: number, id: string): number {
  return -20 + Math.round(Math.sin(nowMs / 520 + id.length) * 3);
}

function activeSpec(anim: { spec: BattleAnimSpec; elapsedMs: number } | null | undefined, id: string): { spec: BattleAnimSpec; p: number } | null {
  if (!anim || anim.elapsedMs >= anim.spec.durationMs || !anim.spec.cosmo || anim.spec.actorId !== id) return null;
  return { spec: anim.spec, p: anim.elapsedMs / anim.spec.durationMs };
}

/** 装着がすんでいるか（装着の動きの途中なら、半分すぎてから）。装着の文が出なかった戦闘では、最初の攻撃で装着する。 */
export function cosmoArmed(member: Combatant, anim: { spec: BattleAnimSpec; elapsedMs: number } | null | undefined): boolean {
  if (!member.cosmo || member.hp <= 0) return false;
  const a = activeSpec(anim, member.id);
  if (a?.spec.cosmo === "equip") {
    if (a.p >= 0.55) armed.add(member.id);
    return a.p >= 0.55;
  }
  if (a) armed.add(member.id);
  return armed.has(member.id);
}

const ease = (t: number): number => t * t * (3 - 2 * t);

/** 砲台の位置（と、どの砲台が手前か・どこを向くか）。 */
function podPositions(member: Combatant, center: { x: number; y: number }, anim: { spec: BattleAnimSpec; elapsedMs: number } | null | undefined, pointOf: (id: string) => Pt, nowMs: number): { x: number; y: number; front: boolean; aim: { x: number; y: number } | null }[] {
  // 待機中は、体のまわりを縦にぐるぐる回る（人間の指示「縦にぐるぐる回る感じにして」）。
  // 背中（右）側を上り、頭の上をこえて、前（左）側を下りる。前を通る砲台は体より手前に描く
  // もう1つの動き方（人間の指示「周辺を不規則に自由に飛んでる感じでもいいや」）: 砲台ごとにちがう速さの波を重ねて、
  // まわりを気ままに飛びまわる。2つの動き方は、10秒ごとに、なめらかに入れかわる（縦に回る→自由に飛ぶ→縦に回る…）
  const orbit = (i: number, t: number): { x: number; y: number; front: boolean } => {
    const a = t / 800 + (i * Math.PI * 2) / PODS;
    const vx = center.x + 2 - Math.cos(a) * 13, vy = center.y - 2 + Math.sin(a) * 27, vf = Math.cos(a) > 0;
    const s = t / 1000, ph = i * 1.7;
    const fx = center.x + Math.sin(s * (0.9 + i * 0.13) + ph) * 26 + Math.sin(s * 2.3 + ph * 2) * 7;
    const fy = center.y - 4 + Math.sin(s * (1.3 + i * 0.11) + ph * 1.3) * 22 + Math.cos(s * 3.1 + ph) * 5;
    const ff = Math.cos(s * (0.9 + i * 0.13) + ph) > 0;
    const c = (t / 10000) % 1;
    const w = c < 0.42 ? 0 : c < 0.5 ? ease((c - 0.42) / 0.08) : c < 0.92 ? 1 : 1 - ease((c - 0.92) / 0.08);
    return { x: vx + (fx - vx) * w, y: vy + (fy - vy) * w, front: w < 0.5 ? vf : ff };
  };
  const formation = (i: number, tp: Pt, t: number): { x: number; y: number } => {
    const big = (tp.h ?? 32) >= 90;
    const R = big ? 70 : 40;
    const a = (i * Math.PI * 2) / PODS + t / 650 + Math.sin(t / 300 + i) * 0.25;
    return { x: tp.x + Math.cos(a) * R + Math.sin(t / 210 + i * 2) * 4, y: tp.y + Math.sin(a) * R * 0.62 + Math.cos(t / 260 + i) * 3 };
  };
  const mem = memory.get(member.id) ?? { pos: [], at: 0, last: null, lastShot: 0, target: null };
  memory.set(member.id, mem);
  const a = activeSpec(anim, member.id);
  const out: { x: number; y: number; front: boolean; aim: { x: number; y: number } | null }[] = [];
  if (a && (a.spec.cosmo === "deploy" || a.spec.cosmo === "shot") && a.spec.targetIds[0]) {
    const tp = pointOf(a.spec.targetIds[0]);
    for (let i = 0; i < PODS; i++) {
      let pos: { x: number; y: number };
      if (a.spec.cosmo === "deploy") {
        // 舞い上がり（上へ）→ うずを巻きながら敵のまわりへ。1基ずつ少しずらして飛び立つ
        const q = Math.max(0, Math.min(1, (a.p - i * 0.05) / 0.7));
        const from = orbit(i, nowMs - anim!.elapsedMs);
        const to = formation(i, tp, nowMs);
        const e = ease(q);
        const lift = Math.sin(q * Math.PI) * (40 + i * 6);
        const swirl = Math.sin(q * Math.PI * 2 + i) * 18 * (1 - q);
        pos = { x: from.x + (to.x - from.x) * e + swirl, y: from.y + (to.y - from.y) * e - lift };
      } else {
        pos = formation(i, tp, nowMs);
      }
      out.push({ ...pos, front: true, aim: { x: tp.x, y: tp.y } });
    }
    mem.pos = out.map((o) => ({ x: o.x, y: o.y }));
    mem.at = nowMs;
    mem.last = a.spec.cosmo;
    mem.lastShot = a.spec.cosmoShot ?? 0;
    mem.target = tp;
    return out;
  }
  // 撃っているあいだ（次の文を待つあいだ）は、敵のまわりを飛び回りつづける。撃ち終わったら、持ち主のまわりへもどる
  const since = nowMs - mem.at;
  const holding = mem.target && mem.last && (mem.last === "deploy" || mem.lastShot < PODS - 1) && since < 1600;
  if (holding && mem.target) {
    for (let i = 0; i < PODS; i++) out.push({ ...formation(i, mem.target, nowMs), front: true, aim: { x: mem.target.x, y: mem.target.y } });
    mem.pos = out.map((o) => ({ x: o.x, y: o.y }));
    return out;
  }
  const back = mem.pos.length === PODS && since < 700 ? ease(Math.min(1, since / 700)) : 1;
  for (let i = 0; i < PODS; i++) {
    const o = orbit(i, nowMs);
    if (back < 1) {
      const f = mem.pos[i];
      out.push({ x: f.x + (o.x - f.x) * back, y: f.y + (o.y - f.y) * back - Math.sin(back * Math.PI) * 20, front: true, aim: null });
    } else {
      out.push({ ...o, aim: null });
    }
  }
  return out;
}

function drawPod(ctx: CanvasRenderingContext2D, x: number, y: number, aim: { x: number; y: number } | null, alpha: number, nowMs: number, i: number, scale = 1): void {
  const pod = getSpriteCanvas("cosmo:pod", SPRITE_DATA);
  if (!pod) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.translate(Math.round(x), Math.round(y));
  ctx.scale(scale, scale);
  // 絵は左向き（砲口が左）。ねらう相手があれば、そちらへ向ける（右を向くときは、上下が逆さにならないように裏返す）
  if (aim) {
    const ang = Math.atan2(aim.y - y, aim.x - x);
    const right = Math.cos(ang) > 0;
    ctx.rotate(right ? ang : ang - Math.PI);
    if (right) ctx.scale(-1, 1);
  }
  // 推進の光（ちらちら）
  ctx.globalCompositeOperation = "lighter";
  ctx.fillStyle = `rgba(90, 210, 255, ${0.35 + 0.25 * Math.sin(nowMs / 60 + i)})`;
  ctx.fillRect(4, -1, 3 + ((nowMs / 50 + i) % 3), 2);
  ctx.globalCompositeOperation = "source-over";
  ctx.imageSmoothingEnabled = false;
  // 9×9の正方形のうち、絵は下の5行（中心は 4.5, 6.5）
  ctx.drawImage(pod, -4.5, -6.5);
  ctx.restore();
}

/** いつもの光（体のまわりの、ゆっくり脈打つ水色の光と、立ちのぼる光の粒）。 */
function drawAura(ctx: CanvasRenderingContext2D, cx: number, cy: number, nowMs: number, strong: boolean): void {
  // ドット絵エディタで描いた、いつもの輝きのコマ（くり返す。脈打つ光・広がる光の輪・まわる光の粒・立ちのぼる光のすじ）
  drawSpellFrame(ctx, "cosmo", "aura", 0, { x: cx, y: cy }, { loopMs: nowMs });
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  const pulse = 0.5 + 0.5 * Math.sin(nowMs / 350);
  const r = 22 + pulse * 3;
  const g = ctx.createRadialGradient(cx, cy, 2, cx, cy, r);
  g.addColorStop(0, `rgba(170, 240, 255, ${(strong ? 0.42 : 0.26) + pulse * 0.08})`);
  g.addColorStop(0.5, `rgba(60, 170, 255, ${(strong ? 0.2 : 0.12) + pulse * 0.05})`);
  g.addColorStop(1, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = g;
  ctx.fillRect(cx - r, cy - r, r * 2, r * 2);
  for (let i = 0; i < 10; i++) {
    const rr = Math.sin(i * 77.7) * 43758.5453;
    const f = rr - Math.floor(rr);
    const rise = ((nowMs / 1400 + f) % 1) * 26;
    ctx.globalAlpha = 1 - rise / 26;
    ctx.fillStyle = i % 3 ? "#9ae8ff" : "#ffffff";
    ctx.fillRect(Math.round(cx - 12 + f * 24), Math.round(cy + 14 - rise), 1, i % 4 ? 1 : 2);
  }
  ctx.restore();
}

/** 光の環（ユーリ以外の人の背に。ユーリは鎧の絵に描いてある）。 */
function drawRing(ctx: CanvasRenderingContext2D, cx: number, cy: number, nowMs: number): void {
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  ctx.strokeStyle = `rgba(120, 228, 255, ${0.7 + 0.3 * Math.sin(nowMs / 300)})`;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.ellipse(cx, cy, 13, 12, 0, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}

/**
 * 味方の姿を、コスモリングライトの姿で描く（装着ずみのときだけ）。描いたら true（ふだんの姿は描かない）。
 * left・feetY は、ふだんの姿（16×32）の左はしと足もと。
 */
export function drawCosmoWearer(
  ctx: CanvasRenderingContext2D,
  member: Combatant,
  specKey: string,
  left: number,
  feetY: number,
  normal: HTMLCanvasElement | null,
  anim: { spec: BattleAnimSpec; elapsedMs: number } | null | undefined,
  state: BattleState,
  pointOf: (id: string) => Pt,
  nowMs: number,
  feetRow: number,
): boolean {
  if (!cosmoArmed(member, anim)) return false;
  const hover = cosmoHover(nowMs, member.id);
  const top = feetY - (feetRow + 1) + hover;
  const center = { x: left + 8, y: top + 18 };
  const a = activeSpec(anim, member.id);
  const mem = memory.get(member.id);
  const attacking = (a && (a.spec.cosmo === "deploy" || a.spec.cosmo === "shot")) || (!!mem?.last && nowMs - mem.at < 900 && (mem.last === "deploy" || mem.lastShot < PODS - 1));
  // 地面の影（浮いているので、小さくうすく）
  ctx.fillStyle = "rgba(0,0,0,0.2)";
  ctx.fillRect(left + 3, feetY - 1, 10, 2);
  drawAura(ctx, center.x, center.y, nowMs, !!attacking);
  const pods = podPositions(member, center, anim, pointOf, nowMs);
  pods.forEach((p, i) => { if (!p.front) drawPod(ctx, p.x, p.y, p.aim, 0.85, nowMs, i); });
  const art = specKey === "ユーリ" ? getSpriteCanvas(attacking ? "cosmo:attack" : "cosmo:idle", SPRITE_DATA) : null;
  if (art) {
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(art, left - BODY_OX, top - BODY_OY);
  } else {
    drawRing(ctx, center.x, center.y - 2, nowMs);
    if (normal) ctx.drawImage(normal, left, top);
  }
  // 体の上にも、うすく輝きを重ねる（体そのものが光って見えるように）
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  ctx.globalAlpha = 0.22 + 0.12 * Math.sin(nowMs / 280);
  drawSpellFrame(ctx, "cosmo", "aura", 0, { x: center.x, y: center.y }, { loopMs: nowMs + 300 });
  ctx.restore();
  pods.forEach((p, i) => { if (p.front && !p.aim) drawPod(ctx, p.x, p.y, p.aim, 1, nowMs, i); });
  void state;
  return true;
}

/**
 * 味方の絵より手前に重ねるもの: 敵のまわりを飛ぶ砲台・雷のビーム・命中の光・装着の光。
 * battle-renderer の、動き（エフェクト）を重ねるところで呼ぶ。
 */
export function drawCosmoOverlay(
  ctx: CanvasRenderingContext2D,
  state: BattleState,
  anim: { spec: BattleAnimSpec; elapsedMs: number } | null | undefined,
  pointOf: (id: string) => Pt,
  nowMs: number,
  screenW: number,
  screenH: number,
): void {
  for (const member of state.party) {
    if (!member.cosmo || member.hp <= 0) continue;
    const base = pointOf(member.id);
    const a = activeSpec(anim, member.id);
    // 装着: 環がかがやき、鎧がはまる
    if (a?.spec.cosmo === "equip") {
      const feet = { x: base.x, y: base.y + 16 + Math.round(cosmoHover(nowMs, member.id) * Math.min(1, a.p / 0.55)) };
      const info = drawSpellFrame(ctx, "cosmo", "charge", a.p, feet);
      if (info && info.flash > 0) {
        ctx.fillStyle = `rgba(216, 246, 255, ${info.flash * 0.55})`;
        ctx.fillRect(0, 0, screenW, screenH);
      }
      continue;
    }
    if (!cosmoArmed(member, anim)) continue;
    // 体のまん中（drawCosmoWearer と同じ: 足もと base.y+16 から、絵の上はし −29、そこから +18）
    const center = { x: base.x, y: base.y + 5 + cosmoHover(nowMs, member.id) };
    const pods = podPositions(member, center, anim, pointOf, nowMs);
    // 舞い上がるあいだは、画面を少し暗くし、砲台に光の尾をつける
    if (a?.spec.cosmo === "deploy") {
      ctx.fillStyle = `rgba(4, 10, 30, ${0.28 * Math.sin(a.p * Math.PI)})`;
      ctx.fillRect(0, 0, screenW, screenH);
      for (let k = 1; k <= 4; k++) {
        const past = podPositions(member, center, { spec: a.spec, elapsedMs: Math.max(0, a.p * a.spec.durationMs - k * 40) }, pointOf, nowMs - k * 40);
        past.forEach((p, i) => {
          ctx.save();
          ctx.globalCompositeOperation = "lighter";
          ctx.fillStyle = `rgba(90, 210, 255, ${0.35 - k * 0.07})`;
          ctx.fillRect(Math.round(p.x) - 1, Math.round(p.y) - 1, 3, 3);
          ctx.restore();
          void i;
        });
      }
      // 尾を描くために呼んだぶん、今の位置を覚え直す
      podPositions(member, center, anim, pointOf, nowMs);
    }
    // 敵のまわりを飛ぶ砲台は、2倍の大きさで（手前へ飛び出してくる）
    pods.forEach((p, i) => { if (p.aim) drawPod(ctx, p.x, p.y, p.aim, 1, nowMs, i, 2); });
    // 雷のビーム（1基ずつ）
    if (a?.spec.cosmo === "shot" && a.spec.targetIds[0]) {
      const n = a.spec.cosmoShot ?? 0;
      const pod = pods[n];
      const tp = pointOf(a.spec.targetIds[0]);
      const big = (tp.h ?? 32) >= 90 ? 2 : 1;
      if (a.p >= 0.06 && a.p < 0.62) {
        const dx = tp.x - pod.x, dy = tp.y - pod.y;
        const dist = Math.hypot(dx, dy);
        const muzzle = { x: pod.x + (dx / dist) * 10, y: pod.y + (dy / dist) * 10 };
        // 絵のビームは左向き（砲口が右はし）。敵の向きへ回し、長さを合わせる（大きな敵には太く）
        drawSpellFrame(ctx, "cosmo", "bolt", 0, muzzle, { scale: big, rotate: Math.atan2(dy, dx) - Math.PI, stretchX: Math.max(0.3, (dist - 10) / 111 / big), loopMs: anim!.elapsedMs });
        // 撃つ砲台の光
        ctx.save();
        ctx.globalCompositeOperation = "lighter";
        ctx.fillStyle = "rgba(200, 248, 255, 0.8)";
        ctx.fillRect(Math.round(muzzle.x) - 2, Math.round(muzzle.y) - 2, 5, 5);
        ctx.restore();
      }
      if (a.p >= 0.12) {
        const info = drawSpellFrame(ctx, "cosmo", "hit", (a.p - 0.12) / 0.88, { x: tp.x, y: tp.y }, { scale: big });
        if (info && info.flash > 0) {
          ctx.fillStyle = `rgba(216, 246, 255, ${info.flash * 0.45})`;
          ctx.fillRect(0, 0, screenW, screenH);
        }
      }
    }
  }
}
