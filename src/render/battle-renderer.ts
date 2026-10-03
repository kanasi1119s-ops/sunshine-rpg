import { COMMANDS, type BattleUiState } from "../game/battle/battle-controller";
import type { BattleState, Combatant } from "../game/battle/types";
import { findCombatant } from "../game/battle/types";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import { hueOfHex, mobPalette } from "../game/art/mob-palette";
import { getBackdropCanvas, type Biome } from "./battle-backdrop";
import { drawWindow } from "./ui-frame";
import { PORTRAITS } from "../game/portrait/portraits";
import { spriteSpecFromPortrait } from "../game/sprite/character-specs";
import { drawSprite } from "./sprite-renderer";
import { frameAt, SPRITE_FEET_ROW } from "../game/sprite/overworld-sprite";

let currentBiome: Biome = "grass";
/** これから始まる戦闘の背景（場所）を決める。 */
export function setBattleBiome(biome: Biome): void {
  currentBiome = biome;
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
): void {
  const ratio = combatant.maxHp > 0 ? combatant.hp / combatant.maxHp : 0;
  ctx.fillStyle = "#333";
  ctx.fillRect(x, y, width, 4);
  ctx.fillStyle = ratio > 0.3 ? "#4caf50" : "#e05555";
  ctx.fillRect(x, y, width * Math.max(0, ratio), 4);
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
  const spec = enemy.hp > 0 ? MONSTERS[enemy.id] : undefined;
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
  const spec = enemy.hp > 0 ? MONSTERS[enemy.id] : undefined;
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

function drawBossSprite(ctx: CanvasRenderingContext2D, enemy: Combatant, screenWidth: number): boolean {
  if (enemy.hp <= 0) {
    return false;
  }
  const canvas = getSpriteCanvas(`boss:${enemy.id}`, SPRITE_DATA);
  if (!canvas) {
    return false;
  }
  // 敵の側（右）に大きく描き、名前とHPは絵の下に置く
  const size = 132;
  const x = enemySideX(screenWidth, size);
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";
  ctx.drawImage(canvas, x, 2, size, size);
  ctx.fillStyle = "#f0f0f0";
  shadowText(ctx, enemy.name, x, 136);
  drawHpBar(ctx, enemy, x, 150, size);
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
  ctx.fillStyle = "#1c1030";
  ctx.fillRect(0, 0, screenWidth, screenHeight);
  const backdrop = getBackdropCanvas(currentBiome, screenWidth, screenHeight - 56);
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
  battleState.enemies.forEach((enemy, index) => {
    if (drawBossSprite(ctx, enemy, screenWidth)) {
      return;
    }
    // 1体だけの強敵（ボス・神など、体力が大きい敵）は、敵の側に大きく描く。
    if (battleState.enemies.length === 1 && enemy.maxHp >= 250 && enemy.hp > 0 && MONSTERS[enemy.id]) {
      const size = 80;
      const bx = enemySideX(screenWidth, 128);
      // 手描きの絵がある形は、2倍（128）で大きく描く（きれいに拡大できる整数倍）
      if (drawMobSprite(ctx, enemy, bx, 2, 128)) {
        ctx.fillStyle = "#f0f0f0";
        shadowText(ctx, enemy.name, bx, 134);
        drawHpBar(ctx, enemy, bx, 148, 110);
        return;
      }
      drawEnemySprite(ctx, enemy, bx + 24, 10, size);
      ctx.fillStyle = "#f0f0f0";
      shadowText(ctx, enemy.name, bx, 134);
      drawHpBar(ctx, enemy, bx, 148, 110);
      return;
    }
    // ふつうの敵は、敵の側に、少しずらして縦に並べる（名前とHPは絵の内側＝画面の中央がわ）
    const stagger = (index % 2) * 34;
    const sx = ENEMIES_ON_RIGHT ? screenWidth - 64 - 14 - stagger : 14 + stagger;
    const sy = 4 + index * 48;
    const labelX = ENEMIES_ON_RIGHT ? sx - 70 : sx + 68;
    if (drawMobSprite(ctx, enemy, sx, sy)) {
      ctx.fillStyle = "#f0f0f0";
      shadowText(ctx, enemy.name, labelX, sy + 20);
      drawHpBar(ctx, enemy, labelX, sy + 34, 64);
      return;
    }
    drawEnemySprite(ctx, enemy, sx + 12, sy + 10, 40);
    ctx.fillStyle = "#f0f0f0";
    shadowText(ctx, enemy.name, labelX, sy + 20);
    drawHpBar(ctx, enemy, labelX, sy + 34, 40);
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
  battleState.party.forEach((member, index) => {
    const isActing = uiState.kind === "command" && uiState.actorId === member.id;
    // 状態表示（1人1行）
    const ty = 2 + index * 12;
    ctx.fillStyle = isActing ? "#f2c14e" : "#f0f0f0";
    shadowText(ctx, `${member.name.split(/[\s　]/)[0]} ${member.hp}/${member.maxHp} MP${member.mp}`, textX, ty);
    drawHpBar(ctx, member, textX, ty + 9, 118);
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
