import {
  chooseEnemyAction,
  createBattleState,
  runTurn,
  checkOutcome,
  type BattleOutcome,
} from "./battle-engine";
import type { BattleAction, BattleItem, BattleState, Combatant, Skill } from "./types";
import { isAlive } from "./types";

export type CommandKind = "attack" | "skill" | "item" | "defend" | "flee";

export const COMMANDS: { kind: CommandKind; label: string }[] = [
  { kind: "attack", label: "たたかう" },
  { kind: "skill", label: "とくぎ" },
  { kind: "item", label: "どうぐ" },
  { kind: "defend", label: "ぼうぎょ" },
  { kind: "flee", label: "にげる" },
];

export type BattleUiState =
  | { kind: "command"; actorId: string; cursor: number }
  | { kind: "target"; actorId: string; commandKind: "attack" | "skill" | "item"; candidateIds: string[]; cursor: number }
  | { kind: "message"; text: string }
  | { kind: "finished"; outcome: BattleOutcome };

export interface BattleControllerOptions {
  skill: Skill;
  item: BattleItem;
}

/**
 * 戦闘のUI進行（コマンド選択→対象選択→行動確定を全員分→処理→ログ表示）を管理する。
 * 実際の勝敗・ダメージ計算は battle-engine（純粋関数）に任せる。
 */
export class BattleController {
  private state: BattleState;
  private readonly rng: () => number;
  private readonly skill: Skill;
  private readonly item: BattleItem;

  private pendingActions: BattleAction[] = [];
  /** このターンでまだコマンドを選んでいない、生きている味方のID一覧。先頭が今選んでいる人。 */
  private turnQueue: string[] = [];
  private messageQueue: string[] = [];
  private phase: BattleUiState;

  constructor(
    party: Combatant[],
    enemies: Combatant[],
    rng: () => number,
    options: BattleControllerOptions,
  ) {
    this.state = createBattleState(party, enemies);
    this.rng = rng;
    this.skill = options.skill;
    this.item = options.item;
    this.turnQueue = this.state.party.filter(isAlive).map((c) => c.id);
    this.phase = this.currentCommandPhase();
  }

  getState(): BattleState {
    return this.state;
  }

  getUiState(): BattleUiState {
    return this.phase;
  }

  moveCursor(delta: number): void {
    if (this.phase.kind === "command") {
      const count = COMMANDS.length;
      this.phase = { ...this.phase, cursor: (this.phase.cursor + delta + count) % count };
    } else if (this.phase.kind === "target") {
      const count = this.phase.candidateIds.length;
      if (count === 0) {
        return;
      }
      this.phase = { ...this.phase, cursor: (this.phase.cursor + delta + count) % count };
    }
  }

  confirm(): void {
    if (this.phase.kind === "command") {
      this.confirmCommand(this.phase.actorId, COMMANDS[this.phase.cursor].kind);
      return;
    }
    if (this.phase.kind === "target") {
      const targetId = this.phase.candidateIds[this.phase.cursor];
      if (!targetId) {
        return;
      }
      this.pushAction(this.phase.actorId, this.phase.commandKind, targetId);
      this.phase = this.advanceAfterAction();
      return;
    }
    if (this.phase.kind === "message") {
      this.phase = this.popMessageOrAdvance();
      return;
    }
    // finished: 呼び出し側が戦闘終了処理をする（ここでは何もしない）
  }

  private confirmCommand(actorId: string, commandKind: CommandKind): void {
    if (commandKind === "defend" || commandKind === "flee") {
      this.pendingActions.push({ type: commandKind, actorId });
      this.phase = this.advanceAfterAction();
      return;
    }

    const candidateIds =
      commandKind === "item"
        ? this.state.party.filter(isAlive).map((c) => c.id)
        : this.state.enemies.filter(isAlive).map((c) => c.id);

    this.phase = { kind: "target", actorId, commandKind, candidateIds, cursor: 0 };
  }

  private pushAction(actorId: string, commandKind: "attack" | "skill" | "item", targetId: string): void {
    if (commandKind === "attack") {
      this.pendingActions.push({ type: "attack", actorId, targetId });
    } else if (commandKind === "skill") {
      this.pendingActions.push({ type: "skill", actorId, targetId, skill: this.skill });
    } else {
      this.pendingActions.push({ type: "item", actorId, targetId, item: this.item });
    }
  }

  /** 今、先頭にいる人のコマンド選択フェーズを返す。誰も残っていなければ集計へ進む。 */
  private currentCommandPhase(): BattleUiState {
    const actorId = this.turnQueue[0];
    if (!actorId) {
      return this.resolveRound();
    }
    return { kind: "command", actorId, cursor: 0 };
  }

  /** 今の人の行動が決まったので、キューから外して次の人へ進む。 */
  private advanceAfterAction(): BattleUiState {
    this.turnQueue.shift();
    return this.currentCommandPhase();
  }

  private resolveRound(): BattleUiState {
    const enemyActions = this.state.enemies
      .filter(isAlive)
      .map((enemy) => chooseEnemyAction(enemy, this.state.party, this.rng));
    const allActions = [...this.pendingActions, ...enemyActions];
    const logBefore = this.state.log.length;
    this.state = runTurn(this.state, allActions, this.rng);
    this.pendingActions = [];
    this.messageQueue = this.state.log.slice(logBefore);
    return this.popMessageOrAdvance();
  }

  private popMessageOrAdvance(): BattleUiState {
    const next = this.messageQueue.shift();
    if (next) {
      return { kind: "message", text: next };
    }
    const outcome = checkOutcome(this.state);
    if (outcome !== "ongoing") {
      return { kind: "finished", outcome };
    }
    this.turnQueue = this.state.party.filter(isAlive).map((c) => c.id);
    return this.currentCommandPhase();
  }
}
