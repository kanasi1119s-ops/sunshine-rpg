import { COMMANDS, type BattleUiState } from "../game/battle/battle-controller";
import type { BattleState, Combatant } from "../game/battle/types";
import { findCombatant } from "../game/battle/types";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import { hueOfHex, mobPalette } from "../game/art/mob-palette";
import { getBackdropCanvas, type Biome } from "./battle-backdrop";

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
function drawBossSprite(ctx: CanvasRenderingContext2D, enemy: Combatant, screenWidth: number): boolean {
  if (enemy.hp <= 0) {
    return false;
  }
  const canvas = getSpriteCanvas(`boss:${enemy.id}`, SPRITE_DATA);
  if (!canvas) {
    return false;
  }
  // 右寄りに大きく描き、名前とHPは左上に置く（味方の一覧と重ならない）
  const size = 150;
  const x = screenWidth - size - 20;
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";
  ctx.drawImage(canvas, x, 4, size, size);
  ctx.fillStyle = "#f0f0f0";
  shadowText(ctx, enemy.name, 12, 10);
  drawHpBar(ctx, enemy, 12, 24, 110);
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
    // 1体だけの強敵（ボス・神など、体力が大きい敵）は、中央に大きく描く。
    if (battleState.enemies.length === 1 && enemy.maxHp >= 250 && enemy.hp > 0 && MONSTERS[enemy.id]) {
      const size = 80;
      const bx = Math.round(screenWidth / 2 - size / 2 - 40);
      // 手描きの絵がある形は、2倍（128）で大きく描く（きれいに拡大できる整数倍）
      if (drawMobSprite(ctx, enemy, bx - 24, 0, 128)) {
        ctx.fillStyle = "#f0f0f0";
        shadowText(ctx, enemy.name, bx + size + 32, 30);
        drawHpBar(ctx, enemy, bx + size + 32, 46, 110);
        return;
      }
      drawEnemySprite(ctx, enemy, bx, 6, size);
      ctx.fillStyle = "#f0f0f0";
      shadowText(ctx, enemy.name, bx + size + 12, 30);
      drawHpBar(ctx, enemy, bx + size + 12, 46, 110);
      return;
    }
    const x = 60 + index * 90;
    if (drawMobSprite(ctx, enemy, x - 12, 4)) {
      ctx.fillStyle = "#f0f0f0";
      shadowText(ctx, enemy.name, x - 12, 70);
      drawHpBar(ctx, enemy, x - 12, 82, 64);
      return;
    }
    const y = 24;
    drawEnemySprite(ctx, enemy, x, y, 40);
    ctx.fillStyle = "#f0f0f0";
    shadowText(ctx, enemy.name, x, y + 44);
    drawHpBar(ctx, enemy, x, y + 56, 40);
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

  // 味方の状態一覧。4人以上のときは2列に並べる（6人でもコマンド欄に重ならない）。
  const boxTop = screenHeight - 56;
  const columns = battleState.party.length > 3 ? 2 : 1;
  const rowsPerColumn = Math.ceil(battleState.party.length / columns);
  const partyY = boxTop - rowsPerColumn * LINE_HEIGHT * 2 - 4;
  const columnWidth = Math.floor((screenWidth - 16) / columns);
  battleState.party.forEach((member, index) => {
    const column = Math.floor(index / rowsPerColumn);
    const row = index % rowsPerColumn;
    const x = 8 + column * columnWidth;
    const y = partyY + row * LINE_HEIGHT * 2;
    const isActing = uiState.kind === "command" && uiState.actorId === member.id;
    ctx.fillStyle = isActing ? "#f2c14e" : "#f0f0f0";
    const text = columns === 2 ? `${member.name} HP${member.hp}/${member.maxHp} MP${member.mp}` : `${member.name} HP:${member.hp}/${member.maxHp} MP:${member.mp}/${member.maxMp}`;
    shadowText(ctx, text, x, y);
    drawHpBar(ctx, member, x, y + LINE_HEIGHT, columns === 2 ? columnWidth - 12 : 100);
  });

  const boxY = screenHeight - 56;
  ctx.fillStyle = "rgba(10, 10, 24, 0.92)";
  ctx.fillRect(0, boxY, screenWidth, 56);
  ctx.strokeStyle = "#f0f0f0";
  ctx.strokeRect(0, boxY, screenWidth, 56);
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
