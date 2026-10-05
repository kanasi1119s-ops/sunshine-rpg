import type { Combatant } from "./types";

/**
 * 歯ごたえの調整（2026-10-05、人間の指示「仲間が増えてからの敵はもっと強くてもいい。ボスももっと強くていい」）。
 *  - ランダムエンカウントの敵は、仲間が増えるほど強くなる（体力 +4%・攻撃 +1.5% を、仲間1人ごとに）。
 *  - ボスは、全員、体力と攻撃を上げる（ボスの元のデータは変えず、戦闘に出すときに掛ける）。
 */
export const ENCOUNTER_HP_PER_COMPANION = 0.04;
export const ENCOUNTER_ATK_PER_COMPANION = 0.015;
export const BOSS_HP_MULT = 1.06;
export const BOSS_ATK_MULT = 1.0;

/** 仲間の人数（ユーリをのぞく）に応じて、ザコ1体の体力・攻撃にかける倍率。 */
export function encounterScale(companions: number): { hp: number; atk: number } {
  const c = Math.max(0, companions);
  return { hp: 1 + ENCOUNTER_HP_PER_COMPANION * c, atk: 1 + ENCOUNTER_ATK_PER_COMPANION * c };
}

/** ボスを、より強くする（戦闘に出す直前に使う）。 */
export function strengthenBoss(boss: Combatant): Combatant {
  const maxHp = Math.round(boss.maxHp * BOSS_HP_MULT);
  return { ...boss, maxHp, hp: Math.round(boss.hp * BOSS_HP_MULT), attack: Math.round(boss.attack * BOSS_ATK_MULT) };
}
