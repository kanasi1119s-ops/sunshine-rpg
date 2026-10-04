import { COMMANDS, type BattleUiState } from "../game/battle/battle-controller";
import type { BattleState, Combatant } from "../game/battle/types";
import { baseEnemyId, findCombatant } from "../game/battle/types";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import { drawSmooth } from "./smooth-draw";
import { hueOfHex, mobPalette } from "../game/art/mob-palette";
import { getBackdropCanvas, type Biome } from "./battle-backdrop";
import { drawWindow } from "./ui-frame";
import { PORTRAITS } from "../game/portrait/portraits";
import { spriteSpecFromPortrait } from "../game/sprite/character-specs";
import { drawSprite } from "./sprite-renderer";
import { frameAt, SPRITE_FEET_ROW } from "../game/sprite/overworld-sprite";

let currentBiome: Biome = "grass";
let currentVariant = 0;

/** これから始まる戦闘の背景（場所）を決める。 */
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

function renderBattleBody(
  ctx: CanvasRenderingContext2D,
  battleState: BattleState,
  uiState: BattleUiState,
  screenWidth: number,
  screenHeight: number,
  effectView?: BattleEffectView | null,
): void {
  ctx.imageSmoothingEnabled = false;
  ctx.fillStyle = "#1c1030";
  ctx.fillRect(0, 0, screenWidth, screenHeight);
  const backdrop = getBackdropCanvas(currentBiome, screenWidth, screenHeight - 56, currentVariant);
  if (backdrop) {
    ctx.drawImage(backdrop, 0, 0);
  }

  const progress = effectView ? effectView.elapsedMs / effectView.effect.duration : 1;
  const active = effectView && progress < 1 ? effectView.effect.kind : null;

  ctx.font = "10px monospace";
  ctx.textBaseline = "top";

  // 会心の一撃のときは、敵だけを短く小きざみにゆらす。
  const enemyShake = active === "crit" && effectView ? shakeOffset(progress, effectView.elapsedMs) : 0;
  ctx.save();
  ctx.translate(enemyShake, 0);
  battleState.enemies.forEach((enemy) => {
    if (drawBossSprite(ctx, enemy, screenWidth)) {
      return;
    }
    // 1体だけの強敵（ボス・神など、体力が大きい敵）は、敵の側に大きく描く。
    if (battleState.enemies.length === 1 && enemy.maxHp >= 250 && enemy.hp > 0 && MONSTERS[baseEnemyId(enemy.id)]) {
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
      // 倒した敵は描かない（灰色の四角が背景に残らないように）
      enemy.hp > 0 &&
      !(
        enemy.hp > 0 &&
        (getSpriteCanvas(`boss:${baseEnemyId(enemy.id)}`, SPRITE_DATA) ||
          (battleState.enemies.length === 1 && enemy.maxHp >= 250 && MONSTERS[baseEnemyId(enemy.id)]))
      ),
  );
  const slots = groundSlots(crowd.length);
  crowd
    .map((enemy, i) => ({ enemy, slot: slots[i] }))
    .sort((a, b) => a.slot.feet - b.slot.feet)
    .forEach(({ enemy, slot }) => {
      const flying = isFlying(enemy);
      const bob = flying ? Math.round(Math.sin(performance.now() / 450 + slot.x) * 3) : 0;
      const sx = slot.x;
      const sy = slot.feet - 62 - (flying ? 18 : 0) + bob;
      if (enemy.hp > 0) {
        drawGroundShadow(ctx, sx + 32, slot.feet, 22, flying);
      }
      if (!drawMobSprite(ctx, enemy, sx, sy)) {
        drawEnemySprite(ctx, enemy, sx + 12, sy + 20, 40);
      }
      ctx.fillStyle = "#f0f0f0";
      shadowText(ctx, enemy.name, sx, slot.feet + 2);
      drawHpBar(ctx, enemy, sx, slot.feet + 13, 64);
    });

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
    if (!spec || member.hp <= 0) {
      return;
    }
    const row = index % 2;
    const col = Math.floor(index / 2);
    const feetY = groundY - row * 18;
    const leftX = ENEMIES_ON_RIGHT ? 20 + col * 30 + row * 14 : screenWidth - 40 - col * 30 - row * 14;
    const x = leftX + (isActing ? (ENEMIES_ON_RIGHT ? 4 : -4) : 0);
    const step = isActing ? frameAt(true, nowMs) : 0;
    ctx.fillStyle = "rgba(0,0,0,0.28)";
    ctx.fillRect(x + 1, feetY - 2, 14, 3); // 足元の影
    ctx.save();
    ctx.translate(x, feetY - SPR * (SPRITE_FEET_ROW + 1));
    ctx.scale(SPR, SPR);
    drawSprite(ctx, spec, ENEMIES_ON_RIGHT ? "right" : "left", step, 0, 0);
    ctx.restore();
  });
  void count;

  const boxY = screenHeight - 56;
  drawWindow(ctx, 2, boxY, screenWidth - 4, 54);
  ctx.fillStyle = "#f0f0f0";

  if (uiState.kind === "command") {
    const actor = findCombatant(battleState, uiState.actorId);
    ctx.fillText(`${actor?.name ?? ""} の コマンド`, 8, boxY + 6);
    COMMANDS.forEach((command, index) => {
      const cursor = index === uiState.cursor ? "▶" : " ";
      ctx.fillText(`${cursor} ${command.label}`, 16 + (index % 3) * 90, boxY + 20 + Math.floor(index / 3) * LINE_HEIGHT);
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
): void {
  ctx.save();
  if (effectView && effectView.effect.kind === "shake") {
    ctx.translate(shakeOffset(effectView.elapsedMs / effectView.effect.duration, effectView.elapsedMs), 0);
  }
  renderBattleBody(ctx, battleState, uiState, screenWidth, screenHeight, effectView);
  ctx.restore();
}
