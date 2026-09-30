import type { Combatant } from "./types";

/**
 * 終章のラスボス「虚灯をまとうエドレア」（`docs/story/structure.md`「終章（虚灯宮）」参照）。
 * 虚灯宮の「静めの間」の力を身にまとったエドレアとの最終決戦。
 * 数値は roadmap 4-43 の自動シミュレーション300回（`chapter9-balance.test.ts`）で調整する（目安70〜90%）。
 * ユーリ・レト・ミナ・ガイド・オルカ・アヤメの6人パーティ（Lv1想定）を前提にする。
 */
export function createKyotoukyuEdreaYugami(): Combatant {
  return {
    id: "kyotoukyu-yugami",
    name: "虚灯をまとうエドレア",
    maxHp: 316,
    hp: 316,
    maxMp: 0,
    mp: 0,
    attack: 28,
    defense: 12,
    speed: 14,
    isEnemy: true,
    guarding: false,
    expReward: 400,
  };
}
