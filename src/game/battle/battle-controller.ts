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
  | { kind: "skillList"; actorId: string; skills: Skill[]; cursor: number }
  /** 「どうぐ」を選んだときの一覧（持っている回復アイテムと数）。 */
  | { kind: "itemList"; actorId: string; stacks: ItemStack[]; cursor: number }
  | {
      kind: "target";
      actorId: string;
      commandKind: "attack" | "skill" | "item";
      candidateIds: string[];
      cursor: number;
      /** 「とくぎ」のとき、選んだ特技。 */
      skill?: Skill;
      /** 「どうぐ」のとき、選んだ道具。 */
      item?: BattleItem;
    }
  | { kind: "message"; text: string }
  | { kind: "finished"; outcome: BattleOutcome };

/** 持っている回復アイテム1種類と、あと何個使えるか。 */
export interface ItemStack {
  item: BattleItem;
  quantity: number;
}

/** 使える人がいない場合の最後の手段。何も設定し忘れたときに戦闘が壊れないようにするための保険。 */
const FALLBACK_SKILL: Skill = { id: "fallback", name: "とくぎ", mpCost: 0, powerMultiplier: 1 };

export interface BattleControllerOptions {
  /** 味方1人ごとのとくぎ（キャラクターIDをキーにする）。複数人パーティでは各キャラが別のとくぎを持つ。 */
  skills: Record<string, Skill>;
  /** 数に限りのない道具（`items` を渡さないときの昔のしくみ。テスト用）。 */
  item?: BattleItem;
  /** 持っている回復アイテムと数。数が尽きた道具は選べない。使った数は `getItemUsage()` で受け取る。 */
  items?: ItemStack[];
  /** ジョブで覚えた特技（キャラクターIDをキーにする）。あれば「とくぎ」を選んだとき一覧が出る。 */
  extraSkills?: Record<string, Skill[]>;
}

/**
 * 戦闘のUI進行（コマンド選択→対象選択→行動確定を全員分→処理→ログ表示）を管理する。
 * 実際の勝敗・ダメージ計算は battle-engine（純粋関数）に任せる。
 */
export class BattleController {
  private state: BattleState;
  private readonly rng: () => number;
  private readonly skills: Record<string, Skill>;
  private readonly stacks: ItemStack[];
  private readonly used: Record<string, number> = {};
  private readonly extraSkills: Record<string, Skill[]>;

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
    this.skills = options.skills;
    this.stacks = options.items ?? (options.item ? [{ item: options.item, quantity: Infinity }] : []);
    this.extraSkills = options.extraSkills ?? {};
    this.turnQueue = this.state.party.filter(isAlive).map((c) => c.id);
    this.phase = this.currentCommandPhase();
  }

  getState(): BattleState {
    return this.state;
  }

  /** いま出ているメッセージの行動が終わった時点の、みんなのHP（メッセージ表示中のみ。それ以外は null）。 */
  getShownHp(): Record<string, number> | null {
    if (this.phase.kind !== "message") return null;
    const idx = this.state.log.length - this.messageQueue.length - 1;
    const entry = (this.state.hpTrail ?? []).find((e) => e.end > idx);
    return entry ? entry.hp : null;
  }

  /** いま出ているメッセージの行動が始まる前の、みんなのHP。 */
  getHpBeforeMessage(): Record<string, number> | null {
    if (this.phase.kind !== "message") return null;
    const idx = this.state.log.length - this.messageQueue.length - 1;
    const before = (this.state.hpTrail ?? []).filter((e) => e.end <= idx);
    return before.length ? before[before.length - 1].hp : null;
  }

  getUiState(): BattleUiState {
    return this.phase;
  }

  /** 戦闘で使った回復アイテムの数（IDごと）。終わったあと、持ち物から引く。 */
  getItemUsage(): Record<string, number> {
    return { ...this.used };
  }

  /** いま使える回復アイテムがあるか（「どうぐ」を選べるか）。 */
  hasUsableItems(): boolean {
    return this.remainingStacks().length > 0;
  }

  private remainingStacks(): ItemStack[] {
    return this.stacks
      .map((s) => ({ item: s.item, quantity: s.quantity - (this.used[s.item.id] ?? 0) }))
      .filter((s) => s.quantity > 0);
  }

  moveCursor(delta: number): void {
    if (this.phase.kind === "command") {
      const count = COMMANDS.length;
      this.phase = { ...this.phase, cursor: (this.phase.cursor + delta + count) % count };
    } else if (this.phase.kind === "skillList") {
      const count = this.phase.skills.length;
      this.phase = { ...this.phase, cursor: (this.phase.cursor + delta + count) % count };
    } else if (this.phase.kind === "itemList") {
      const count = this.phase.stacks.length;
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
    if (this.phase.kind === "skillList") {
      const skill = this.phase.skills[this.phase.cursor];
      const actorId = this.phase.actorId;
      // 敵全体・味方全体に効く特技は、対象を選ばずに決まる。
      if (skill.effect === "damageAll" || skill.effect === "debuffAll" || skill.effect === "healAll" || skill.effect === "buffAll") {
        const towardEnemies = skill.effect === "damageAll" || skill.effect === "debuffAll";
        const anyTarget = towardEnemies ? this.state.enemies.find(isAlive)?.id : actorId;
        if (anyTarget) {
          this.pushAction(actorId, "skill", anyTarget, skill);
          this.phase = this.advanceAfterAction();
        }
        return;
      }
      this.phase = this.targetPhase(actorId, "skill", skill);
      return;
    }
    if (this.phase.kind === "itemList") {
      const stack = this.phase.stacks[this.phase.cursor];
      if (stack) {
        this.phase = this.targetPhase(this.phase.actorId, "item", undefined, stack.item);
      }
      return;
    }
    if (this.phase.kind === "target") {
      const targetId = this.phase.candidateIds[this.phase.cursor];
      if (!targetId) {
        return;
      }
      this.pushAction(this.phase.actorId, this.phase.commandKind, targetId, this.phase.skill, this.phase.item);
      this.phase = this.advanceAfterAction();
      return;
    }
    if (this.phase.kind === "message") {
      this.phase = this.popMessageOrAdvance();
      return;
    }
    // finished: 呼び出し側が戦闘終了処理をする（ここでは何もしない）
  }

  /**
   * ひとつ前に戻る（もどるボタン）。対象選択→とくぎ一覧／コマンド、とくぎ一覧→コマンド、
   * コマンドで押すと、前の人が選んだ行動を取り消して、その人の選び直しに戻る。ログ表示中・終了後は何もしない。
   */
  cancel(): void {
    if (this.phase.kind === "itemList") {
      this.phase = { kind: "command", actorId: this.phase.actorId, cursor: 0 };
      return;
    }
    if (this.phase.kind === "target") {
      const { actorId, commandKind } = this.phase;
      if (commandKind === "item") {
        this.phase = { kind: "itemList", actorId, stacks: this.remainingStacks(), cursor: 0 };
        return;
      }
      const extras = this.extraSkills[actorId] ?? [];
      if (commandKind === "skill" && extras.length > 0) {
        const base = this.skills[actorId] ?? FALLBACK_SKILL;
        this.phase = { kind: "skillList", actorId, skills: [base, ...extras], cursor: 0 };
      } else {
        this.phase = { kind: "command", actorId, cursor: 0 };
      }
      return;
    }
    if (this.phase.kind === "skillList") {
      this.phase = { kind: "command", actorId: this.phase.actorId, cursor: 0 };
      return;
    }
    if (this.phase.kind === "command" && this.pendingActions.length > 0) {
      const last = this.pendingActions.pop();
      if (last && last.type === "item") {
        this.used[last.item.id] = Math.max(0, (this.used[last.item.id] ?? 0) - 1);
      }
      if (last) {
        this.turnQueue.unshift(last.actorId);
        this.phase = { kind: "command", actorId: last.actorId, cursor: 0 };
      }
    }
  }

  private confirmCommand(actorId: string, commandKind: CommandKind): void {
    if (commandKind === "defend" || commandKind === "flee") {
      this.pendingActions.push({ type: commandKind, actorId });
      this.phase = this.advanceAfterAction();
      return;
    }

    if (commandKind === "skill") {
      const extras = this.extraSkills[actorId] ?? [];
      if (extras.length > 0) {
        const base = this.skills[actorId] ?? FALLBACK_SKILL;
        this.phase = { kind: "skillList", actorId, skills: [base, ...extras], cursor: 0 };
        return;
      }
    }
    if (commandKind === "item") {
      const stacks = this.remainingStacks();
      if (stacks.length > 0) {
        this.phase = { kind: "itemList", actorId, stacks, cursor: 0 };
      }
      return;
    }
    this.phase = this.targetPhase(actorId, commandKind);
  }

  private targetPhase(actorId: string, commandKind: "attack" | "skill" | "item", skill?: Skill, item?: BattleItem): BattleUiState {
    const candidateIds =
      commandKind === "item" || skill?.effect === "heal" || skill?.effect === "buff"
        ? this.state.party.filter(isAlive).map((c) => c.id)
        : this.state.enemies.filter(isAlive).map((c) => c.id);
    return { kind: "target", actorId, commandKind, candidateIds, cursor: 0, skill, item };
  }

  private pushAction(
    actorId: string,
    commandKind: "attack" | "skill" | "item",
    targetId: string,
    chosenSkill?: Skill,
    chosenItem?: BattleItem,
  ): void {
    if (commandKind === "attack") {
      this.pendingActions.push({ type: "attack", actorId, targetId });
    } else if (commandKind === "skill") {
      const skill = chosenSkill ?? this.skills[actorId] ?? FALLBACK_SKILL;
      this.pendingActions.push({ type: "skill", actorId, targetId, skill });
    } else {
      const item = chosenItem ?? this.stacks[0]?.item;
      if (!item) return;
      this.used[item.id] = (this.used[item.id] ?? 0) + 1;
      this.pendingActions.push({ type: "item", actorId, targetId, item });
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
