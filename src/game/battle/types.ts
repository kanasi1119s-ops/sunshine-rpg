export interface Combatant {
  id: string;
  name: string;
  maxHp: number;
  hp: number;
  maxMp: number;
  mp: number;
  attack: number;
  defense: number;
  speed: number;
  isEnemy: boolean;
  /** 「ぼうぎょ」コマンドの効果。次に受けるダメージが半分になる。 */
  guarding: boolean;
  /** 倒したとき、パーティ全員が入手する経験値（敵のみ使用）。 */
  expReward?: number;
}

export interface Skill {
  id: string;
  name: string;
  mpCost: number;
  /** たたかう（威力倍率1.0）を基準にした威力倍率。 */
  powerMultiplier: number;
  /**
   * 効果の種類。省略は「敵1体にダメージ」。
   * multi=敵1体に`hits`回、damageAll=敵全体にダメージ、heal=味方1人のHPを回復、healAll=味方全体のHPを回復。
   */
  effect?: "multi" | "damageAll" | "heal" | "healAll";
  /** multi の回数。 */
  hits?: number;
  /** 回復の量（使った人のこうげき × この値）。heal・healAll。 */
  healRatio?: number;
  /** 使うたびに、使った人の最大HPのこの割合（0〜1）を支払う（HPは1より下がらない）。悪神ジョブのリスク。 */
  hpCost?: number;
  /** 敵1体を、このチャンス（0〜1）で一撃で倒す。体力が大きい敵（最大HP500超）には効かない。 */
  koChance?: number;
}

export interface BattleItem {
  id: string;
  name: string;
  healAmount: number;
}

export type BattleAction =
  | { type: "attack"; actorId: string; targetId: string }
  | { type: "skill"; actorId: string; targetId: string; skill: Skill }
  | { type: "item"; actorId: string; targetId: string; item: BattleItem }
  | { type: "defend"; actorId: string }
  | { type: "flee"; actorId: string };

export interface BattleState {
  party: Combatant[];
  enemies: Combatant[];
  log: string[];
  fled: boolean;
}

export function isAlive(combatant: Combatant): boolean {
  return combatant.hp > 0;
}

export function findCombatant(state: BattleState, id: string): Combatant | undefined {
  return [...state.party, ...state.enemies].find((c) => c.id === id);
}
