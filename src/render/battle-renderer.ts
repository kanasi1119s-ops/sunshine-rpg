import { COMMANDS, type BattleUiState } from "../game/battle/battle-controller";
import type { BattleState, Combatant } from "../game/battle/types";
import { baseEnemyId, findCombatant } from "../game/battle/types";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { drawSmooth } from "./smooth-draw";
import { getSpriteCanvas } from "../game/art/sprite";
import { hueOfHex, mobPalette } from "../game/art/mob-palette";
import { getBackdropCanvas, type Biome } from "./battle-backdrop";
import { drawWindow } from "./ui-frame";
import { PORTRAITS } from "../game/portrait/portraits";
import { spriteSpecFromPortrait } from "../game/sprite/character-specs";
import { drawSprite } from "./sprite-renderer";
import { frameAt, SPRITE_FEET_ROW } from "../game/sprite/overworld-sprite";
import { VOLLEY_FX, type BattleAnimSpec } from "../game/battle/battle-anim";
import { allyStateOf, getAllyCanvas, type AllyState } from "./ally-states";
import { drawSpellFrame, hasSpellFx } from "./spell-fx-renderer";
import { drawCosmoOverlay, drawCosmoWearer } from "./cosmo-renderer";
import { DAMAGE_FX, drawCharge, drawFx, drawRelease, drawSpellDim, drawWeaponMotion, FX_COLOR, lungeOffset, type Pt } from "./battle-anim-renderer";

let currentBiome: Biome = "grass";
let currentVariant = 0;

/** これから始まる戦闘の背景（場所）を決める。 */
/**
 * 戦闘の背景の絵を、先にぜんぶ作っておく（はじめて行く場所の戦闘で、絵を作るあいだ画面が止まらないように）。
 * 遊びはじめて少したってから、手のあいた時に1枚ずつ作る。
 */
export function warmBattleBackdrops(biomes: Biome[], screenWidth: number, screenHeight: number): void {
  const queue = [...biomes];
  const next = (): void => {
    const b = queue.shift();
    if (!b) return;
    getBackdropCanvas(b, screenWidth, screenHeight - 56);
    setTimeout(next, 30);
  };
  setTimeout(next, 30);
}

export function setBattleBiome(biome: Biome): void {
  currentBiome = biome;
  // 同じ場所に絵が2枚あるときの、どちらを使うか（戦闘ごとに選ぶ）
  currentVariant = Math.floor(Math.random() * 1000);
}
import { wrapText } from "./text-wrap";
import { shakeOffset, type BattleEffect } from "../game/battle/battle-effect";

/** 進行中の演出（種類と経過ミリ秒）。 */
export interface BattleEffectView {
  effect: BattleEffect;
  elapsedMs: number;
}

/** 進行中の「動き」（武器をふる・魔法のエフェクト・のけぞり）と、経過ミリ秒。 */
export interface BattleAnimView {
  spec: BattleAnimSpec;
  elapsedMs: number;
}
import { buildMonsterCells, MONSTER_GRID_SIZE, MONSTERS } from "../game/monster/monsters";

const LINE_HEIGHT = 12;

function drawHpBar(
  ctx: CanvasRenderingContext2D,
  combatant: Combatant,
  x: number,
  y: number,
  width: number,
  height = 4,
): void {
  const ratio = combatant.maxHp > 0 ? combatant.hp / combatant.maxHp : 0;
  ctx.fillStyle = "#333";
  ctx.fillRect(x, y, width, height);
  ctx.fillStyle = ratio > 0.3 ? "#4caf50" : "#e05555";
  ctx.fillRect(x, y, width * Math.max(0, ratio), height);
}

/**
 * `MONSTERS`に登録がある敵は、手続き的なドット絵で描く。未登録の敵
 * （動作確認用の仮データなど）や、倒された敵は、これまで通り色付き
 * 四角のままにする（倒れた・消えたことが一目で分かるように）。
 */
function drawEnemySprite(
  ctx: CanvasRenderingContext2D,
  enemy: Combatant,
  x: number,
  y: number,
  size: number,
): void {
  const spec = enemy.hp > 0 ? MONSTERS[baseEnemyId(enemy.id)] : undefined;
  if (!spec) {
    ctx.fillStyle = enemy.hp > 0 ? "#8a4a4a" : "#333";
    ctx.fillRect(x, y, size, size);
    return;
  }
  const cellSize = size / MONSTER_GRID_SIZE;
  for (const cell of buildMonsterCells(spec)) {
    ctx.fillStyle = cell.color;
    ctx.fillRect(x + cell.col * cellSize, y + cell.row * cellSize, cellSize, cellSize);
  }
}

/** 雑魚の敵の絵（64×64。形ごとの手描きの絵を、地方の色相で塗る）。描けたら true。 */
function drawMobSprite(ctx: CanvasRenderingContext2D, enemy: Combatant, x: number, y: number, size = 64): boolean {
  // その敵だけの絵（`enemy:<id>`、96×96。AIの下絵→ドット絵化→手直し→エディタで描いたもの）があれば、それを使う
  const own = enemy.hp > 0 ? getSpriteCanvas(`enemy:${baseEnemyId(enemy.id)}`, SPRITE_DATA) : null;
  if (own) {
    drawSmooth(ctx, own, 0, 0, own.width, own.height, x, y, size, size);
    return true;
  }
  const spec = enemy.hp > 0 ? MONSTERS[baseEnemyId(enemy.id)] : undefined;
  if (!spec?.shape || spec.shape === "blob") {
    return false;
  }
  const canvas = getSpriteCanvas(`mob:${spec.shape}`, SPRITE_DATA, mobPalette(hueOfHex(spec.body)));
  if (!canvas) {
    return false;
  }
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, x, y, size, size);
  return true;
}

/** ボスの大きな絵（256×256）。あれば画面の中央に大きく描く。描けたら true。 */
/** 戦闘画面の左右: 敵が右、味方が左（`ENEMIES_ON_RIGHT` を false にすると逆になる）。 */
const ENEMIES_ON_RIGHT = false;
/** 状態表示の1行の高さ（論理のドット） */
const STATUS_PITCH = 14;

/** 敵の側の、絵の左端x（絵の幅 w。画面の端から余白を空ける）。 */
function enemySideX(screenWidth: number, w: number): number {
  return ENEMIES_ON_RIGHT ? screenWidth - w - 16 : 16;
}

const partySpecCache = new Map<string, ReturnType<typeof spriteSpecFromPortrait> | null>();
function partySpecFor(name: string): ReturnType<typeof spriteSpecFromPortrait> | null {
  if (!partySpecCache.has(name)) {
    const portrait = PORTRAITS[name];
    partySpecCache.set(name, portrait ? spriteSpecFromPortrait(portrait, name) : null);
  }
  return partySpecCache.get(name) ?? null;
}

/** 飛べる敵の形（こうもり・目・影）。それ以外は地面に立つ。 */
const FLYING_SHAPES = new Set<string>(["bat", "eye", "ghost"]);

function isFlying(enemy: Combatant): boolean {
  const shape = MONSTERS[baseEnemyId(enemy.id)]?.shape;
  return shape !== undefined && FLYING_SHAPES.has(shape);
}

/** 飛べるボス（名前に空・羽などの言葉があるもの）。 */
function isFlyingBoss(enemy: Combatant): boolean {
  return /羽|風|雲|空|鳥|翼|竜|龍|目/.test(enemy.name) || isFlying(enemy);
}

/** 足元の影。飛んでいる敵は、小さくうすい影を地面に落とす。 */
function drawGroundShadow(ctx: CanvasRenderingContext2D, cx: number, groundY: number, rx: number, flying: boolean): void {
  ctx.save();
  ctx.fillStyle = flying ? "rgba(0, 0, 0, 0.22)" : "rgba(0, 0, 0, 0.38)";
  ctx.beginPath();
  ctx.ellipse(cx, groundY, flying ? rx * 0.7 : rx, flying ? 3 : 5, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

/** 倒れた敵が、体の上から消えていく長さ（ミリ秒）。 */
const DIE_MS = 900;
const deathAt = new Map<string, number>();
/** 倒れた敵の消え方の進み（0〜1）。生きていれば null、消え終わったら 1。 */
function dyingProgress(enemy: Combatant, now: number): number | null {
  if (enemy.hp > 0) {
    deathAt.delete(enemy.id);
    return null;
  }
  let t = deathAt.get(enemy.id);
  if (t === undefined) {
    t = now;
    deathAt.set(enemy.id, t);
  }
  return Math.min(1, (now - t) / DIE_MS);
}
/** 体の上から消えていく: 上から k の割合ぶんを切り取って描き、切り口が白く光り、光の粒が立ちのぼる。 */
function dissolve(ctx: CanvasRenderingContext2D, k: number, x: number, y: number, w: number, h: number, draw: () => void): void {
  const cut = Math.round(y + k * h);
  ctx.save();
  ctx.beginPath();
  ctx.rect(x - 8, cut, w + 16, y + h + 24 - cut);
  ctx.clip();
  draw();
  ctx.restore();
  ctx.save();
  ctx.globalAlpha = 0.9 * (1 - k * 0.5);
  ctx.fillStyle = "#ffe8b0";
  ctx.fillRect(Math.round(x + w * 0.1), cut - 1, Math.round(w * 0.8), 1);
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(Math.round(x + w * 0.15), cut, Math.round(w * 0.7), 1);
  for (let i = 0; i < 16; i++) {
    const r = Math.sin(i * 91.7 + 3.1) * 43758.5453;
    const f = r - Math.floor(r);
    const rise = ((k * 2 + f) % 1) * 22;
    ctx.globalAlpha = (1 - k) * (1 - rise / 22);
    ctx.fillStyle = i % 3 ? "#ffe8b0" : "#ffffff";
    ctx.fillRect(Math.round(x + w * (0.1 + f * 0.8)), Math.round(cut - 2 - rise), i % 2 ? 2 : 1, i % 2 ? 2 : 1);
  }
  ctx.restore();
}

/** 戦闘の背景にかける、時刻の色（夜の深さ 0〜1・夕方のあかね色 0〜1）。外の戦いのときだけ main.ts が入れる。 */
let battleNight = 0;
let battleGlow = 0;
export function setBattleTimeOfDay(night: number, glow: number): void {
  battleNight = night;
  battleGlow = glow;
}
function drawBattleSkyTint(ctx: CanvasRenderingContext2D, w: number, h: number): void {
  if (battleGlow > 0.02) {
    ctx.fillStyle = `rgba(255, 140, 60, ${0.2 * battleGlow})`;
    ctx.fillRect(0, 0, w, h);
  }
  const n = battleNight;
  if (n <= 0.01) return;
  ctx.save();
  ctx.globalCompositeOperation = "multiply";
  const lerp = (a: number, b: number): number => Math.round(a + (b - a) * n);
  ctx.fillStyle = `rgb(${lerp(255, 78)}, ${lerp(255, 92)}, ${lerp(255, 158)})`;
  ctx.fillRect(0, 0, w, h);
  ctx.restore();
  ctx.fillStyle = `rgba(16, 24, 80, ${0.14 * n})`;
  ctx.fillRect(0, 0, w, h);
  // 夜空の星（画面の上のほうだけ。ゆっくりまたたく）
  if (n >= 0.7) {
    const t = typeof performance !== "undefined" ? performance.now() / 1000 : 0;
    for (let i = 0; i < 26; i++) {
      const r = Math.sin(i * 127.1 + 3.7) * 43758.5453;
      const fx = r - Math.floor(r);
      const r2 = Math.sin(i * 311.7 + 1.3) * 43758.5453;
      const fy = r2 - Math.floor(r2);
      const tw = 0.5 + 0.5 * Math.sin(t * (1.2 + (i % 5) * 0.3) + i);
      ctx.globalAlpha = (n - 0.6) * 2 * (0.35 + 0.65 * tw);
      ctx.fillStyle = i % 4 === 0 ? "#fff6d0" : "#dfe8ff";
      ctx.fillRect(Math.round(fx * w), Math.round(4 + fy * h * 0.18), 1, 1);
      if (i % 7 === 0 && tw > 0.7) {
        ctx.fillRect(Math.round(fx * w) - 1, Math.round(4 + fy * h * 0.18), 3, 1);
        ctx.fillRect(Math.round(fx * w), Math.round(3 + fy * h * 0.18), 1, 3);
      }
    }
    ctx.globalAlpha = 1;
  }
}

/** ふつうの敵の立つ場所（足元のy）。奥の敵を先に描くので、手前ほどyが大きい。 */
function groundSlots(count: number): { x: number; feet: number }[] {
  if (count <= 1) return [{ x: 70, feet: 140 }];
  if (count === 2) return [{ x: 24, feet: 122 }, { x: 104, feet: 146 }];
  const slots = [{ x: 10, feet: 118 }, { x: 84, feet: 146 }, { x: 158, feet: 122 }];
  for (let i = 3; i < count; i++) slots.push({ x: 20 + (i - 3) * 60, feet: 132 });
  return slots;
}

function drawBossSprite(ctx: CanvasRenderingContext2D, enemy: Combatant, screenWidth: number): boolean {
  if (enemy.hp <= 0) {
    return false;
  }
  const canvas = getSpriteCanvas(`boss:${baseEnemyId(enemy.id)}`, SPRITE_DATA);
  if (!canvas) {
    return false;
  }
  // 敵の側に大きく描き、名前とHPは絵の下に置く。飛べる敵以外は、地面の上に立つ（足元に影）。
  const size = 132;
  const x = enemySideX(screenWidth, size);
  const flying = isFlyingBoss(enemy);
  const y = flying ? 2 + Math.round(Math.sin(performance.now() / 500) * 3) : 14;
  drawGroundShadow(ctx, x + size / 2, 147, size * 0.36, flying);
  drawSmooth(ctx, canvas, 0, 0, canvas.width, canvas.height, x, y, size, size);
  ctx.fillStyle = "#f0f0f0";
  shadowText(ctx, enemy.name, x, 149);
  drawHpBar(ctx, enemy, x, 160, size);
  return true;
}

/** 戦闘の画面で、その人のからだの中心の位置（エフェクトを重ねる場所）。 */
function combatantPoint(state: BattleState, id: string, screenWidth: number, screenHeight: number): Pt {
  const ally = state.party.findIndex((c) => c.id === id);
  if (ally >= 0) {
    const row = ally % 2;
    const col = Math.floor(ally / 2);
    const feetY = screenHeight - 56 - 4 - row * 18;
    const leftX = ENEMIES_ON_RIGHT ? 20 + col * 30 + row * 14 : screenWidth - 40 - col * 30 - row * 14;
    return { x: leftX + 8, y: feetY - 16, w: 16, h: 32 };
  }
  const enemy = state.enemies.find((c) => c.id === id);
  if (!enemy) return { x: 80, y: 80 };
  const boss = !!getSpriteCanvas(`boss:${baseEnemyId(enemy.id)}`, SPRITE_DATA);
  const strong = state.enemies.length === 1 && enemy.maxHp >= 250 && !!MONSTERS[baseEnemyId(enemy.id)];
  if (boss) return { x: enemySideX(screenWidth, 132) + 66, y: 80, w: 100, h: 132 };
  if (strong) return { x: enemySideX(screenWidth, 128) + 64, y: 56 + 24, w: 90, h: 100 };
  const crowd = state.enemies.filter((e) => e.hp > 0 && !getSpriteCanvas(`boss:${baseEnemyId(e.id)}`, SPRITE_DATA) && !(state.enemies.length === 1 && e.maxHp >= 250 && MONSTERS[baseEnemyId(e.id)]));
  const idx = crowd.findIndex((e) => e.id === id);
  const slots = groundSlots(idx >= 0 ? crowd.length : state.enemies.length);
  const slot = slots[idx >= 0 ? idx : Math.max(0, state.enemies.indexOf(enemy)) % slots.length];
  return { x: slot.x + 32, y: slot.feet - 28, w: 40, h: 56 };
}

function renderBattleBody(
  ctx: CanvasRenderingContext2D,
  battleState: BattleState,
  uiState: BattleUiState,
  screenWidth: number,
  screenHeight: number,
  effectView?: BattleEffectView | null,
  itemsAvailable = true,
  animView?: BattleAnimView | null,
): void {
  ctx.imageSmoothingEnabled = false;
  ctx.fillStyle = "#1c1030";
  ctx.fillRect(0, 0, screenWidth, screenHeight);
  const backdrop = getBackdropCanvas(currentBiome, screenWidth, screenHeight - 56, currentVariant);
  if (backdrop) {
    ctx.drawImage(backdrop, 0, 0);
  }
  // 外の戦い（世界地図・町・村）では、フィールドと同じ時刻の色を背景にかける（夕方はあかね色、夜は青く暗く）
  drawBattleSkyTint(ctx, screenWidth, screenHeight - 56);

  const progress = effectView ? effectView.elapsedMs / effectView.effect.duration : 1;
  const active = effectView && progress < 1 ? effectView.effect.kind : null;

  ctx.font = "10px monospace";
  ctx.textBaseline = "top";

  // 魔法を唱えているあいだ（ため）は、唱える人のまわりが、術の色にぼんやり光る
  const setGlow = (id: string): void => {
    const sp = animView && animView.elapsedMs < animView.spec.durationMs ? animView.spec : null;
    const casting = sp && sp.fx && sp.fxStart > 0 && animView!.elapsedMs / sp.durationMs < sp.fxStart + 0.08 && (sp.casterId === id || (sp.motion === "cast" && sp.actorId === id));
    ctx.shadowColor = casting && sp?.fx ? FX_COLOR[sp.fx] : "transparent";
    ctx.shadowBlur = casting ? 9 : 0;
  };
  const clearGlow = (): void => { ctx.shadowColor = "transparent"; ctx.shadowBlur = 0; };

  // 会心の一撃のときは、敵だけを短く小きざみにゆらす。
  const enemyShake = active === "crit" && effectView ? shakeOffset(progress, effectView.elapsedMs) : 0;
  ctx.save();
  ctx.translate(enemyShake, 0);
  const nowDie = performance.now();
  const dieK = new Map(battleState.enemies.map((e) => [e.id, dyingProgress(e, nowDie)] as const));
  /** 倒れて消えている途中か（消え終わった敵・生きている敵は false）。 */
  const isDying = (e: Combatant): boolean => { const k = dieK.get(e.id); return k !== null && k !== undefined && k < 1; };
  /** 消えている途中の敵を、生きているときの絵で描くための写し（HPは0に見える）。 */
  const asShown = (e: Combatant): Combatant => (e.hp > 0 ? e : { ...e, hp: 0.0001 });
  battleState.enemies.forEach((enemy0) => {
    setGlow(enemy0.id);
    if (enemy0.hp <= 0 && !isDying(enemy0)) return;
    const k = enemy0.hp > 0 ? 0 : dieK.get(enemy0.id) ?? 1;
    const enemy = asShown(enemy0);
    if (getSpriteCanvas(`boss:${baseEnemyId(enemy.id)}`, SPRITE_DATA)) {
      const bx = enemySideX(screenWidth, 132);
      if (k > 0) {
        let drawn = false;
        dissolve(ctx, k, bx, 2, 132, 146, () => { drawn = drawBossSprite(ctx, enemy, screenWidth); });
        if (drawn) return;
      } else if (drawBossSprite(ctx, enemy, screenWidth)) {
        return;
      }
    }
    // 1体だけの強敵（ボス・神など、体力が大きい敵）は、敵の側に大きく描く。
    if (battleState.enemies.length === 1 && enemy.maxHp >= 250 && MONSTERS[baseEnemyId(enemy.id)]) {
      if (k > 0) {
        const bx0 = enemySideX(screenWidth, 128);
        dissolve(ctx, k, bx0, 2, 128, 144, () => {
          if (!drawMobSprite(ctx, enemy, bx0, 16, 128)) drawEnemySprite(ctx, enemy, bx0 + 24, 24, 80);
        });
        return;
      }
      const size = 80;
      const bx = enemySideX(screenWidth, 128);
      const flyingMob = isFlying(enemy);
      const by = flyingMob ? 2 + Math.round(Math.sin(performance.now() / 500) * 3) : 16;
      drawGroundShadow(ctx, bx + 64, 146, 46, flyingMob);
      // 手描きの絵がある形は、2倍（128）で大きく描く（きれいに拡大できる整数倍）
      if (drawMobSprite(ctx, enemy, bx, by, 128)) {
        ctx.fillStyle = "#f0f0f0";
        shadowText(ctx, enemy.name, bx, 148);
        drawHpBar(ctx, enemy, bx, 160, 110);
        return;
      }
      drawEnemySprite(ctx, enemy, bx + 24, by + 8, size);
      ctx.fillStyle = "#f0f0f0";
      shadowText(ctx, enemy.name, bx, 148);
      drawHpBar(ctx, enemy, bx, 160, 110);
      return;
    }
    // ふつうの敵は、地面の上に立つ（手前ほど下）。飛べる敵（こうもり・目・影）だけ、浮かんで足元に影を落とす。
    // 奥の敵を先に描くため、いったんここでは何もせず、あとでまとめて描く。
    return;
  });

  // ふつうの敵（1体のボス・強敵を除く）を、立ち位置の奥から手前の順に描く。
  const crowd = battleState.enemies.filter(
    (enemy) =>
      // 倒した敵は、体の上から消えていくあいだだけ描く（消え終わったら描かない）
      (enemy.hp > 0 || isDying(enemy)) &&
      !(
        getSpriteCanvas(`boss:${baseEnemyId(enemy.id)}`, SPRITE_DATA) ||
        (battleState.enemies.length === 1 && enemy.maxHp >= 250 && MONSTERS[baseEnemyId(enemy.id)])
      ),
  );
  const slots = groundSlots(crowd.length);
  crowd
    .map((enemy, i) => ({ enemy, slot: slots[i] }))
    .sort((a, b) => a.slot.feet - b.slot.feet)
    .forEach(({ enemy, slot }) => {
      setGlow(enemy.id);
      const flying = isFlying(enemy);
      const bob = flying ? Math.round(Math.sin(performance.now() / 450 + slot.x) * 3) : 0;
      const sx = slot.x;
      const sy = slot.feet - 62 - (flying ? 18 : 0) + bob;
      if (enemy.hp <= 0) {
        // 倒れた敵: 体の上から、光りながら消えていく（名前・HPは出さない）
        const shown = asShown(enemy);
        dissolve(ctx, dieK.get(enemy.id) ?? 1, sx, sy, 64, 64, () => {
          if (!drawMobSprite(ctx, shown, sx, sy)) drawEnemySprite(ctx, shown, sx + 12, sy + 20, 40);
        });
        return;
      }
      drawGroundShadow(ctx, sx + 32, slot.feet, 22, flying);
      if (!drawMobSprite(ctx, enemy, sx, sy)) {
        drawEnemySprite(ctx, enemy, sx + 12, sy + 20, 40);
      }
      ctx.fillStyle = "#f0f0f0";
      shadowText(ctx, enemy.name, sx, slot.feet + 2);
      drawHpBar(ctx, enemy, sx, slot.feet + 13, 64);
    });
  clearGlow();

  ctx.restore();

  // 敵への命中・会心・撃破・回復の光（敵のいる上の部分だけ）。
  // 味方がダメージを受けたときは、画面のふちを赤くする（ゆれに重ねる）。
  if (active === "shake") {
    ctx.fillStyle = `rgba(220, 40, 40, ${0.18 * (1 - progress)})`;
    ctx.fillRect(0, 0, screenWidth, screenHeight - 56);
  }
  if (active && active !== "shake") {
    const fade = 1 - progress;
    const color = active === "heal" ? "80, 220, 120" : active === "crit" ? "255, 210, 90" : "255, 255, 255";
    const alpha = (active === "down" ? 0.25 : active === "heal" ? 0.22 : 0.35) * fade;
    ctx.fillStyle = `rgba(${color}, ${alpha})`;
    ctx.fillRect(0, 0, screenWidth, screenHeight - 56);
  }

  // 味方は、味方の側（右）の地面の上に、2列にずらして立つ。名前・HP・MPは上に小さく並べる。
  const count = battleState.party.length;
  const nowMs = typeof performance !== "undefined" ? performance.now() : 0;
  const SPR = 1; // 歩く絵（16×32）を等倍で描く（5人でも重ならない大きさ）
  const groundY = screenHeight - 56 - 4; // 手前の列の足元
  const textX = ENEMIES_ON_RIGHT ? 8 : screenWidth - 128;
  // 状態表示（名前・HP・MP）のうしろに、うすい暗い板。文字の下にHPの帯が重なって読みにくかったので、行の間をあけ、帯は細くする
  ctx.fillStyle = "rgba(16, 10, 30, 0.55)";
  ctx.fillRect(textX - 3, 0, 124, 2 + count * STATUS_PITCH + 1);
  battleState.party.forEach((member, index) => {
    const isActing = uiState.kind === "command" && uiState.actorId === member.id;
    // 状態表示（1人1行）
    const ty = 2 + index * STATUS_PITCH;
    ctx.fillStyle = isActing ? "#f2c14e" : "#f0f0f0";
    shadowText(ctx, `${member.name.split(/[\s　]/)[0]} ${member.hp}/${member.maxHp} MP${member.mp}`, textX, ty);
    drawHpBar(ctx, member, textX, ty + 11, 118, 2);
    // 地面に立つ姿
    const spec = partySpecFor(member.name.split(/[\s　]/)[0]);
    if (!spec) {
      return;
    }
    const row = index % 2;
    const col = Math.floor(index / 2);
    const feetY = groundY - row * 18;
    const leftX = ENEMIES_ON_RIGHT ? 20 + col * 30 + row * 14 : screenWidth - 40 - col * 30 - row * 14;
    const anim = animView && animView.elapsedMs < animView.spec.durationMs ? animView : null;
    const p = anim ? anim.elapsedMs / anim.spec.durationMs : 1;
    const acting = anim?.spec.actorId === member.id && anim.spec.motion;
    const flinch = anim?.spec.hurt && anim.spec.targetIds.includes(member.id) && p < 0.85;
    const lunge = acting && anim?.spec.motion ? lungeOffset(anim.spec.motion, p) : 0;
    const x = leftX + (isActing ? (ENEMIES_ON_RIGHT ? 4 : -4) : 0) + lunge;
    const baseState: AllyState = allyStateOf(member);
    const state: AllyState = flinch && baseState !== "ko" ? "hurt" : baseState;
    const step = isActing || acting ? frameAt(true, nowMs) : 0;
    const specKey = member.name.split(/[\s　]/)[0];
    if (state === "ko") {
      // たおれた姿（よこ向き）
      const lying = getAllyCanvas(spec, specKey, "ko", 0);
      ctx.fillStyle = "rgba(0,0,0,0.28)";
      ctx.fillRect(leftX - 8, feetY - 2, 32, 3);
      if (lying) ctx.drawImage(lying, leftX - 8, feetY - lying.height);
      return;
    }
    // コスモリングライトをまとった人: 宙に浮き、光り、砲台がまわりを回る（装着がすんでから）
    if (member.cosmo && drawCosmoWearer(ctx, member, specKey, x, feetY, getAllyCanvas(spec, specKey, state, step), anim, battleState, (id) => combatantPoint(battleState, id, screenWidth, screenHeight), nowMs, SPRITE_FEET_ROW)) {
      return;
    }
    ctx.fillStyle = "rgba(0,0,0,0.28)";
    ctx.fillRect(x + 1, feetY - 2, 14, 3); // 足元の影
    const shake = flinch ? Math.round(Math.sin(nowMs / 14) * 1.5) : 0;
    // ゆらゆら（混乱）・ぶるぶる（毒）
    const sway = state === "confuse" ? Math.round(Math.sin(nowMs / 160) * 2) : state === "poison" ? Math.round(Math.sin(nowMs / 60)) : 0;
    const canvas = getAllyCanvas(spec, specKey, state, step);
    if (canvas) {
      setGlow(member.id);
      ctx.drawImage(canvas, x + shake + sway, feetY - SPR * (SPRITE_FEET_ROW + 1));
      clearGlow();
    } else {
      ctx.save();
      ctx.translate(x, feetY - SPR * (SPRITE_FEET_ROW + 1));
      ctx.scale(SPR, SPR);
      drawSprite(ctx, spec, ENEMIES_ON_RIGHT ? "right" : "left", step, 0, 0);
      ctx.restore();
    }
    // 状態のしるし（ずっと出ている小さな動き）
    const cx = x + 8;
    const loop = (nowMs % 1800) / 1800;
    if (state === "sleep") drawFx(ctx, "sleep", loop, { x: cx - 4, y: feetY - 14 });
    else if (state === "poison") drawFx(ctx, "poison", loop, { x: cx, y: feetY - 14 });
    else if (state === "confuse") drawFx(ctx, "confuse", loop, { x: cx, y: feetY - 14 });
    // （瀕死の絵は無し）
  });
  // コスモリングライトの砲台・雷のビーム・命中・装着の光（味方の絵より手前）
  if (battleState.party.some((m) => m.cosmo)) {
    drawCosmoOverlay(ctx, battleState, animView, (id) => combatantPoint(battleState, id, screenWidth, screenHeight), nowMs, screenWidth, screenHeight - 56);
  }
  // 動き（武器・魔法のエフェクト）は、味方の絵より手前に重ねる
  if (animView && animView.elapsedMs < animView.spec.durationMs) {
    const spec2 = animView.spec;
    const prog = animView.elapsedMs / spec2.durationMs;
    const pointOf = (id: string): Pt => combatantPoint(battleState, id, screenWidth, screenHeight);
    const targets = spec2.targetIds.map(pointOf);
    const mainTarget = targets[0] ?? { x: 80, y: 80 };
    if (spec2.fx) drawSpellDim(ctx, spec2.fx, prog, screenWidth, screenHeight - 56);
    if (spec2.actorId && spec2.motion) {
      const actorPt = pointOf(spec2.actorId);
      const glow = spec2.fx ? FX_COLOR[spec2.fx] : "#9ad0ff";
      // エフェクトを長く見せるために全体を延ばしても、武器の動きは、もとの速さのまま
      const mprog = Math.min(1, spec2.motionMs ? animView.elapsedMs / spec2.motionMs : prog);
      const lunge = lungeOffset(spec2.motion, mprog);
      drawWeaponMotion(ctx, spec2.motion, mprog, { x: actorPt.x - 4 + lunge, y: actorPt.y + 2 }, mainTarget, glow);
    }
    // 魔法のため（敵が唱えるときも、魔法使いの味方が唱えるときも）
    const casterId = spec2.casterId ?? (spec2.motion === "cast" ? spec2.actorId : undefined);
    const feetOf = (pt: Pt): { x: number; y: number } => ({ x: pt.x, y: pt.y + (pt.h ?? 32) / 2 });
    const scaleOf = (pt: Pt): number => ((pt.h ?? 32) >= 100 ? 2 : 1);
    if (casterId && spec2.fx && prog < spec2.fxStart + 0.08 && spec2.fxStart > 0) {
      // ドット絵エディタで描いた「ため」のコマがあれば、それで。無ければ、これまでのコードの絵
      const cp = pointOf(casterId);
      const drawn = prog < spec2.fxStart && drawSpellFrame(ctx, spec2.fx, "charge", prog / spec2.fxStart, feetOf(cp), { scale: scaleOf(cp) });
      if (!drawn) drawCharge(ctx, cp, FX_COLOR[spec2.fx], prog / spec2.fxStart, spec2.fx);
    }
    if (spec2.fx && prog >= spec2.fxStart) {
      const ft = (prog - spec2.fxStart) / Math.max(0.01, 1 - spec2.fxStart);
      const from = spec2.fromId ? pointOf(spec2.fromId) : undefined;
      const kind = spec2.area && hasSpellFx(spec2.fx, "area") ? "area" : "hit";
      if (hasSpellFx(spec2.fx, kind)) {
        // ドット絵エディタで描いたコマ: 飛んでいく弾（ある術だけ）→ 当たる
        const FLY = 0.28;
        const flying = !!from && !spec2.area && hasSpellFx(spec2.fx, "bolt");
        if (flying && ft < FLY) {
          const q = ft / FLY;
          const tp = mainTarget;
          const x = from!.x + (tp.x - from!.x) * q;
          const y = from!.y + (tp.y - from!.y) * q - Math.sin(q * Math.PI) * 18;
          drawSpellFrame(ctx, spec2.fx, "bolt", 0, { x, y }, { flip: tp.x > from!.x, loopMs: animView.elapsedMs });
        } else {
          const ht = flying ? (ft - FLY) / (1 - FLY) : ft;
          // いっせいに落ちる魔法（流星・紋の輪）は、1人ずつ少しずらして当てる
          const stagger = VOLLEY_FX.has(spec2.fx) && targets.length > 1 ? 0.06 : 0;
          targets.forEach((t, i) => {
            const hti = stagger ? Math.max(0, Math.min(1, (ht - i * stagger) / (1 - stagger * (targets.length - 1)))) : ht;
            if (stagger && ht < i * stagger) return;
            const info = drawSpellFrame(ctx, spec2.fx!, kind, hti, feetOf(t), { scale: scaleOf(t) });
            if (info && i === 0 && info.flash > 0) {
              ctx.save();
              ctx.globalAlpha = info.flash;
              ctx.fillStyle = info.flashColor;
              ctx.fillRect(-8, -8, screenWidth + 16, screenHeight - 40);
              ctx.restore();
            }
          });
        }
      } else {
        targets.forEach((t, i) => drawFx(ctx, spec2.fx!, Math.min(1, ft), t, { from, area: spec2.area, first: i === 0 }));
      }
      // 唱え終えて解き放つ瞬間（ためのあと）、使い手から光がはじける
      const releaseK = ft * (1 - spec2.fxStart) / 0.12;
      if (casterId && spec2.fxStart > 0 && releaseK < 1) drawRelease(ctx, pointOf(casterId), FX_COLOR[spec2.fx], releaseK);
    }
  }
  void count;

  const boxY = screenHeight - 56;
  drawWindow(ctx, 2, boxY, screenWidth - 4, 54);
  ctx.fillStyle = "#f0f0f0";

  if (uiState.kind === "command") {
    const actor = findCombatant(battleState, uiState.actorId);
    ctx.fillText(`${actor?.name ?? ""} の コマンド`, 8, boxY + 6);
    COMMANDS.forEach((command, index) => {
      const cursor = index === uiState.cursor ? "▶" : " ";
      const dim = command.kind === "item" && !itemsAvailable;
      if (dim) ctx.fillStyle = "#807890";
      ctx.fillText(`${cursor} ${command.label}`, 16 + (index % 3) * 90, boxY + 20 + Math.floor(index / 3) * LINE_HEIGHT);
      if (dim) ctx.fillStyle = "#f0f0f0";
    });
    return;
  }

  if (uiState.kind === "skillList") {
    // 覚えた特技が多いときは、6つ（2列×3行）ずつのページに分けて見せる。
    const perPage = 6;
    const page = Math.floor(uiState.cursor / perPage);
    const pages = Math.ceil(uiState.skills.length / perPage);
    ctx.fillText(pages > 1 ? `どのとくぎ？（${page + 1}/${pages}）` : "どのとくぎ？", 8, boxY + 6);
    uiState.skills.slice(page * perPage, (page + 1) * perPage).forEach((skill, i) => {
      const index = page * perPage + i;
      const cursor = index === uiState.cursor ? "▶" : " ";
      ctx.fillText(`${cursor} ${skill.name} MP${skill.mpCost}`, 16 + (i % 2) * 140, boxY + 20 + Math.floor(i / 2) * LINE_HEIGHT);
    });
    return;
  }

  if (uiState.kind === "itemList") {
    const perPage = 6;
    const page = Math.floor(uiState.cursor / perPage);
    const pages = Math.ceil(uiState.stacks.length / perPage);
    ctx.fillText(pages > 1 ? `どのどうぐ？（${page + 1}/${pages}）` : "どのどうぐ？", 8, boxY + 6);
    uiState.stacks.slice(page * perPage, (page + 1) * perPage).forEach((stack, i) => {
      const index = page * perPage + i;
      const cursor = index === uiState.cursor ? "▶" : " ";
      const count = Number.isFinite(stack.quantity) ? `×${stack.quantity}` : "";
      ctx.fillText(`${cursor} ${stack.item.name} ${count}`, 16 + (i % 2) * 140, boxY + 20 + Math.floor(i / 2) * LINE_HEIGHT);
    });
    return;
  }

  if (uiState.kind === "target") {
    ctx.fillText("だれに？", 8, boxY + 6);
    uiState.candidateIds.forEach((id, index) => {
      const target = findCombatant(battleState, id);
      const cursor = index === uiState.cursor ? "▶" : " ";
      // 6人ぶんでも入るよう、3列×2行に並べる。
      ctx.fillText(`${cursor} ${target?.name ?? id}`, 16 + (index % 3) * 125, boxY + 20 + Math.floor(index / 3) * LINE_HEIGHT);
    });
    return;
  }

  if (uiState.kind === "message") {
    // 長いメッセージ（長い名前・特技名）は、コマンド欄の幅で折り返す（最大4行）。
    const lines = wrapText(uiState.text, screenWidth - 16, (segment) => ctx.measureText(segment).width);
    lines.slice(0, 4).forEach((line, i) => ctx.fillText(line, 8, boxY + 6 + i * LINE_HEIGHT));
    return;
  }

  const outcomeText =
    uiState.outcome === "won" ? "勝利した！" : uiState.outcome === "lost" ? "全滅してしまった…" : "逃げ出した";
  ctx.fillText(outcomeText, 8, boxY + 6);
}

/** 背景が明るい所でも読めるよう、暗い影をつけて文字を描く。 */
function shadowText(ctx: CanvasRenderingContext2D, text: string, x: number, y: number): void {
  const fill = ctx.fillStyle;
  ctx.fillStyle = "rgba(10, 8, 24, 0.85)";
  ctx.fillText(text, x + 1, y + 1);
  ctx.fillText(text, x - 1, y + 1);
  ctx.fillStyle = fill;
  ctx.fillText(text, x, y);
}

/** 戦闘画面を描く。味方がダメージを受けたときは画面全体をゆらす。 */
export function renderBattle(
  ctx: CanvasRenderingContext2D,
  battleState: BattleState,
  uiState: BattleUiState,
  screenWidth: number,
  screenHeight: number,
  effectView?: BattleEffectView | null,
  itemsAvailable = true,
  animView?: BattleAnimView | null,
): void {
  ctx.save();
  if (effectView && effectView.effect.kind === "shake") {
    ctx.translate(shakeOffset(effectView.elapsedMs / effectView.effect.duration, effectView.elapsedMs), 0);
  }
  // 攻撃の魔法が当たった瞬間、画面がゆれる（全体魔法は大きく）
  if (animView && animView.spec.fx && DAMAGE_FX.has(animView.spec.fx) && animView.elapsedMs < animView.spec.durationMs) {
    const sp = animView.spec;
    const ft = (animView.elapsedMs / sp.durationMs - sp.fxStart) / Math.max(0.01, 1 - sp.fxStart);
    if (ft >= 0.05 && ft < 0.4) {
      const amp = (sp.area ? 4 : 2.5) * (1 - (ft - 0.05) / 0.35);
      ctx.translate(Math.round(Math.sin(animView.elapsedMs * 0.11) * amp), Math.round(Math.cos(animView.elapsedMs * 0.17) * amp * 0.6));
    }
  }
  renderBattleBody(ctx, battleState, uiState, screenWidth, screenHeight, effectView, itemsAvailable, animView);
  ctx.restore();
}
