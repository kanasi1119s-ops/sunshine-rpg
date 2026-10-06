import type { Combatant } from "./types";

/**
 * 終章のラスボス「虚灯をまとうエドレア」（`docs/story/structure.md`「終章（虚灯宮）」参照）。
 * 虚灯宮の「静めの間」の力を身にまとったエドレアとの最終決戦。
 * 数値は roadmap 4-43 の自動シミュレーション300回（`chapter9-balance.test.ts`）で調整する（目安70〜90%）。
 * ユーリ・レト・ミナ・コハク・オルカ・アヤメの6人パーティ（Lv1想定）を前提にする。
 * 【2026-09-30 再調整】想定レベルLv21の仲間つきパーティに対する勝率が目安になるよう、体力・攻撃・防御・素早さ・経験値を作り直した（`boss-balance.test.ts`）。
 * 【2026-10-06】人間の指示「簡単すぎる」で、2段階の戦いの2戦目にし、強くした（体力4948→5200・攻撃78→79・素早さ24→25。Lv21の勝率 約62%→約43%）。1戦目のあと体力は持ちこしなので、実際はもっと厳しい。
 */
export function createKyotoukyuEdreaYugami(): Combatant {
  return {
    id: "kyotoukyu-yugami",
    name: "虚灯をまとうエドレア",
    maxHp: 5200,
    hp: 5200,
    maxMp: 0,
    mp: 0,
    attack: 79,
    defense: 26,
    speed: 25,
    isEnemy: true,
    guarding: false,
    expReward: 7478,
  };
}

/**
 * 終章を厚くするために足した敵（2026-10-06、人間の指示「8章クリアしてからのエドレアバトルが簡単すぎる。何か間色々入れたい」）。
 * 光の階段の「光の守り手」、眠りの回廊で眠るほうを選んだときの「まどろみの番人」、エドレア戦の1戦目「合議会代表エドレア」。
 * エドレア戦は2段階: 1戦目に勝つと、エドレアが静めの間の力をまとい、そのまま2戦目「虚灯をまとうエドレア」になる。
 */
export function createKyotoukyuGuardian(): Combatant {
  return { id: "kyotoukyu-guardian", name: "光の守り手", maxHp: 5000, hp: 5000, maxMp: 0, mp: 0, attack: 76, defense: 25, speed: 24, isEnemy: true, guarding: false, expReward: 6200 };
}

export function createKyotoukyuDrowse(id: string, name: string): Combatant {
  return { id, name, maxHp: 3600, hp: 3600, maxMp: 0, mp: 0, attack: 72, defense: 24, speed: 23, isEnemy: true, guarding: false, expReward: 3600 };
}

export function createKyotoukyuEdreaFirst(): Combatant {
  return { id: "kyotoukyu-edrea", name: "合議会代表エドレア", maxHp: 4600, hp: 4600, maxMp: 0, mp: 0, attack: 76, defense: 26, speed: 25, isEnemy: true, guarding: false, expReward: 6800 };
}
