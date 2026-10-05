import type { Combatant } from "./types";

/**
 * 終章のラスボス「虚灯をまとうエドレア」（`docs/story/structure.md`「終章（虚灯宮）」参照）。
 * 虚灯宮の「静めの間」の力を身にまとったエドレアとの最終決戦。
 * 数値は roadmap 4-43 の自動シミュレーション300回（`chapter9-balance.test.ts`）で調整する（目安70〜90%）。
 * ユーリ・レト・ミナ・コハク・オルカ・アヤメの6人パーティ（Lv1想定）を前提にする。
 * 【2026-09-30 再調整】想定レベルLv21の仲間つきパーティに対する勝率が目安になるよう、体力・攻撃・防御・素早さ・経験値を作り直した（`boss-balance.test.ts`）。
 */
export function createKyotoukyuEdreaYugami(): Combatant {
  return {
    id: "kyotoukyu-yugami",
    name: "虚灯をまとうエドレア",
    maxHp: 4948,
    hp: 4948,
    maxMp: 0,
    mp: 0,
    attack: 78,
    defense: 26,
    speed: 24,
    isEnemy: true,
    guarding: false,
    expReward: 7478,
  };
}
