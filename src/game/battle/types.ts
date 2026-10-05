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
  /** 運（省略は5）。会心の一撃の出やすさ、攻撃のミスのしやすさ・されやすさ。 */
  luck?: number;
  /** 装備の特殊効果（`items/types.ts` の `ItemTrait`）。会心の出やすさの足し（0.04＝+4%）。 */
  critBonus?: number;
  /** 敵の通常攻撃がはずれやすくなる確率の足し。 */
  evade?: number;
  /** かからない状態異常。 */
  guards?: Array<"poison" | "sleep" | "confuse">;
  /** 毎ターンの終わりに回復する、最大HPの割合（0.03＝3%）。 */
  regenHp?: number;
  /** 毎ターンの終わりに回復するMP。 */
  regenMp?: number;
  /** 連続攻撃に必要な、すばやさの差から引く数。 */
  multiBonus?: number;
  isEnemy: boolean;
  /** 「ぼうぎょ」コマンドの効果。次に受けるダメージが半分になる。 */
  guarding: boolean;
  /** 倒したとき、パーティ全員が入手する経験値（敵のみ使用）。 */
  expReward?: number;
  /** 強化・弱体（能力ごとの倍率と残りターン）。ターンの終わりに1ずつ減り、0で消える。 */
  mods?: Partial<Record<StatKey, StatMod>>;
  /** 眠っている残りターン。眠っているあいだは行動できない。 */
  sleep?: number;
  /** 毒の残りターン。毎ターンの終わりに、最大HPの約6%のダメージ（HPは1より下がらない）。 */
  poison?: number;
  /** 混乱の残りターン。混乱中は、半分の確率で、敵味方かまわず攻撃してしまう。 */
  confused?: number;
  /** 敵が使う攻撃魔法。ターンごとに、chance の確率で、通常攻撃のかわりに使う。 */
  spell?: { skill: Skill; chance: number };
  /** 敵の通常攻撃が当たったとき、相手にかかる状態異常（毒・眠り・混乱）。 */
  inflicts?: { status: "poison" | "sleep" | "confuse"; chance: number; turns: number };
}

export type StatKey = "attack" | "defense" | "speed";

export interface StatMod {
  /** 倍率（1.3＝3割アップ、0.7＝3割ダウン）。 */
  mult: number;
  turns: number;
}

export const STAT_LABELS: Record<StatKey, string> = { attack: "こうげき", defense: "しゅび", speed: "すばやさ" };

/** 強化・弱体を反映した能力値。 */
export function effectiveStat(combatant: Combatant, stat: StatKey): number {
  const mod = combatant.mods?.[stat];
  return Math.max(1, Math.round(combatant[stat] * (mod && mod.turns > 0 ? mod.mult : 1)));
}

export type SkillEffect = "multi" | "damageAll" | "heal" | "healAll" | "buff" | "buffAll" | "debuff" | "debuffAll" | "sleep" | "poison" | "confuse";

export interface Skill {
  id: string;
  name: string;
  mpCost: number;
  /** たたかう（威力倍率1.0）を基準にした威力倍率。 */
  powerMultiplier: number;
  /**
   * 効果の種類。省略は「敵1体にダメージ」。
   * multi=敵1体に`hits`回、damageAll=敵全体にダメージ、heal=味方1人のHPを回復、healAll=味方全体のHPを回復、
   * buff=味方1人の能力アップ、buffAll=味方全体、debuff=敵1体の能力ダウン、debuffAll=敵全体、sleep=敵1体を眠らせる。
   */
  effect?: SkillEffect;
  /** multi の回数。 */
  hits?: number;
  /** 回復の量（使った人のこうげき × この値）。heal・healAll。 */
  healRatio?: number;
  /** 使うたびに、使った人の最大HPのこの割合（0〜1）を支払う（HPは1より下がらない）。悪神ジョブのリスク。 */
  hpCost?: number;
  /** 敵1体を、このチャンス（0〜1）で一撃で倒す。体力が大きい敵（最大HP500超）には効かない。 */
  koChance?: number;
  /** buff・debuff の対象の能力と倍率・続くターン数。 */
  stat?: StatKey;
  mult?: number;
  turns?: number;
  /** debuff・sleep が効く確率（0〜1。省略は1）。体力が大きい敵（最大HP500超）には眠りが効かない。 */
  chance?: number;
}

export interface BattleItem {
  id: string;
  name: string;
  healAmount: number;
  /** MPを回復する量（省略は0）。 */
  mpAmount?: number;
}

export type BattleAction =
  | { type: "attack"; actorId: string; targetId: string; /** 2回目以降の連続攻撃のダメージの倍率。 */ powerScale?: number }
  | { type: "skill"; actorId: string; targetId: string; skill: Skill }
  | { type: "item"; actorId: string; targetId: string; item: BattleItem }
  | { type: "defend"; actorId: string }
  | { type: "flee"; actorId: string };

export interface BattleState {
  party: Combatant[];
  enemies: Combatant[];
  log: string[];
  fled: boolean;
  /** ログの1行ごとの「その行動が終わった時点のHP」（画面で、ダメージを当たる瞬間に合わせて見せるため）。`end` は、その時点のログの行数。 */
  hpTrail?: HpTrailEntry[];
}

export interface HpTrailEntry {
  end: number;
  hp: Record<string, number>;
}

export function isAlive(combatant: Combatant): boolean {
  return combatant.hp > 0;
}

export function findCombatant(state: BattleState, id: string): Combatant | undefined {
  return [...state.party, ...state.enemies].find((c) => c.id === id);
}

/** 一団の中で同じ種類の敵を区別するための「#番号」を取り除いた、絵・データ用のID。 */
export function baseEnemyId(id: string): string {
  return id.replace(/#\d+$/, "");
}
