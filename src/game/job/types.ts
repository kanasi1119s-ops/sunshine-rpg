import type { StatBonus } from "../items/equipment";

export type JobId =
  | "sword-guard"
  | "fist-fighter"
  | "archer"
  | "flame-mage"
  | "ripple-mage"
  | "wind-mage"
  | "earth-guard"
  | "wanderer";

export interface JobSkill {
  /** 特技名（オリジナル。既存作品の特技名とは一致させない）。 */
  name: string;
  /** 習得に必要な熟練度（☆の数）。 */
  requiredStars: number;
  /** 一言の効果説明（戦闘への接続は今後の作業）。 */
  description: string;
}

export interface JobData {
  id: JobId;
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
