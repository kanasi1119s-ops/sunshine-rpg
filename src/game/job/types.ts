import type { StatBonus } from "../items/equipment";

export type JobId =
  | "sword-guard"
  | "fist-fighter"
  | "archer"
  | "flame-mage"
  | "ripple-mage"
  | "wind-mage"
  | "earth-guard"
  | "wanderer"
  // 上級ジョブ（各初期ジョブを☆15まで育てると解放）
  | "sword-saint"
  | "sky-fist"
  | "hundred-archer"
  | "inferno-guide"
  | "stream-sage"
  | "gale-dancer"
  | "immovable-guardian"
  | "many-faced-artist"
  // 天神・悪神ジョブ（8神を倒すと解放。一点特化で、必ず弱点がある）
  | "goddess-shaman"
  | "pure-paladin"
  | "demon-breaker"
  | "bug-curser";

export interface JobSkill {
  /** 特技名（オリジナル。既存作品の特技名とは一致させない）。 */
  name: string;
  /** 習得に必要な熟練度（☆の数）。 */
  requiredStars: number;
  /** 一言の効果説明（戦闘への接続は今後の作業）。 */
  description: string;
  /** 戦闘で使える特技だけが持つ。効果の種類は `Skill.effect`（複数回・全体攻撃・回復）。強化・弱体・状態異常は未対応。 */
  battle?: { mpCost: number; powerMultiplier: number; effect?: "multi" | "damageAll" | "heal" | "healAll"; hits?: number; healRatio?: number; hpCost?: number; koChance?: number };
}

export interface JobData {
  id: JobId;
  /** 上級ジョブだけが持つ。この初期ジョブを最大の☆まで育てると解放される。 */
  baseJob?: JobId;
  /** 天神・悪神ジョブだけが持つ。このフラグが立つ（その神を倒す）と、だれでも装備できる。 */
  unlockFlag?: string;
  name: string;
  reading: string;
  role: string;
  /** そのジョブを装備している間だけ有効な能力値ボーナス（熟練度ごとに増える分は含まない）。 */
  statBonus: StatBonus;
  /** 熟練度が1☆上がるごとに加わる能力値ボーナス。 */
  bonusPerStar: StatBonus;
  skills: JobSkill[];
}

/** ジョブごとの熟練度（経験値）。キャラクターごとに持つ。 */
export type JobMastery = Partial<Record<JobId, number>>;

/** キャラクター1人ぶんのジョブ状態（セーブデータに保存する）。 */
export interface JobState {
  /** いま装備しているジョブ。未装備なら undefined。 */
  equipped?: JobId;
  mastery: JobMastery;
}
