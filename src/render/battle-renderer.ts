import { COMMANDS, type BattleUiState } from "../game/battle/battle-controller";
import type { BattleState, Combatant } from "../game/battle/types";
import { findCombatant } from "../game/battle/types";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
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
  ctx.fillText(enemy.name, 12, 10);
  drawHpBar(ctx, enemy, 12, 24, 110);
  return true;
}

export function renderBattle(
  ctx: CanvasRenderingContext2D,
  battleState: BattleState,
  uiState: BattleUiState,
  screenWidth: number,
  screenHeight: number,
): void {
  ctx.fillStyle = "#1c1030";
  ctx.fillRect(0, 0, screenWidth, screenHeight);

  ctx.font = "10px monospace";
  ctx.textBaseline = "top";

  battleState.enemies.forEach((enemy, index) => {
    if (drawBossSprite(ctx, enemy, screenWidth)) {
      return;
    }
    const x = 60 + index * 90;
    const y = 24;
    drawEnemySprite(ctx, enemy, x, y, 40);
    ctx.fillStyle = "#f0f0f0";
    ctx.fillText(enemy.name, x, y + 44);
    drawHpBar(ctx, enemy, x, y + 56, 40);
  });

  // 味方の状態一覧。
  const partyY = screenHeight - 120;
  battleState.party.forEach((member, index) => {
    const y = partyY + index * LINE_HEIGHT * 2;
    const isActing = uiState.kind === "command" && uiState.actorId === member.id;
    ctx.fillStyle = isActing ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(`${member.name} HP:${member.hp}/${member.maxHp} MP:${member.mp}/${member.maxMp}`, 8, y);
    drawHpBar(ctx, member, 8, y + LINE_HEIGHT, 100);
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
    ctx.fillText("どのとくぎ？", 8, boxY + 6);
    uiState.skills.forEach((skill, index) => {
      const cursor = index === uiState.cursor ? "▶" : " ";
      ctx.fillText(`${cursor} ${skill.name} MP${skill.mpCost}`, 16 + (index % 2) * 140, boxY + 20 + Math.floor(index / 2) * LINE_HEIGHT);
    });
    return;
  }

  if (uiState.kind === "target") {
    ctx.fillText("だれに？", 8, boxY + 6);
    uiState.candidateIds.forEach((id, index) => {
      const target = findCombatant(battleState, id);
      const cursor = index === uiState.cursor ? "▶" : " ";
      ctx.fillText(`${cursor} ${target?.name ?? id}`, 16 + index * 90, boxY + 20);
    });
    return;
  }

  if (uiState.kind === "message") {
    ctx.fillText(uiState.text, 8, boxY + 6);
    return;
  }

  const outcomeText =
    uiState.outcome === "won" ? "勝利した！" : uiState.outcome === "lost" ? "全滅してしまった…" : "逃げ出した";
  ctx.fillText(outcomeText, 8, boxY + 6);
}
