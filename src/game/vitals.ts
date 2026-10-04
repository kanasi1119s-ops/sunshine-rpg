import type { Combatant } from "./battle/types";

/**
 * 今のHP・MP（ノーマルモードで、戦闘のあとも持ち越す値）。キャラクターのIDごと（主人公は "hero"）。
 * 入っていない人は、全快（最大HP・最大MP）。装備やジョブで最大値が変わっても、最大値をこえないように合わせる。
 */
export interface Vital {
  hp: number;
  mp: number;
}
export type Vitals = Record<string, Vital>;

/** 戦闘に出す人の、HP・MPを持ち越した値にする。 */
export function applyVital(c: Combatant, vital: Vital | undefined): Combatant {
  if (!vital) return c;
  return { ...c, hp: Math.max(1, Math.min(c.maxHp, vital.hp)), mp: Math.max(0, Math.min(c.maxMp, vital.mp)) };
}

/** 戦闘が終わったときの味方のHP・MPを、持ち越す値にする。倒れた人は、HP1で立ち上がる。全滅（負け）のときは、全員HP1。 */
export function vitalsAfterBattle(party: Combatant[], lost: boolean): Vitals {
  const result: Vitals = {};
  for (const c of party) {
    if (c.isEnemy) continue;
    result[c.id] = { hp: lost ? 1 : Math.max(1, c.hp), mp: Math.max(0, c.mp) };
  }
  return result;
}

/** 全員（または指定の人）のHP・MPを全快にする（持ち越しの値を消す）。 */
export function fullRestore(vitals: Vitals, ids?: string[]): Vitals {
  if (!ids) return {};
  const next = { ...vitals };
  for (const id of ids) delete next[id];
  return next;
}

/** 回復の量を足す（最大値は、渡された effective の最大値）。 */
export function healVital(vitals: Vitals, id: string, max: { maxHp: number; maxMp: number }, hp: number, mp: number): Vitals {
  const cur = vitals[id] ?? { hp: max.maxHp, mp: max.maxMp };
  return { ...vitals, [id]: { hp: Math.min(max.maxHp, cur.hp + hp), mp: Math.min(max.maxMp, cur.mp + mp) } };
}

/** レベルアップで最大値が増えたぶん、今の値も増やす（持ち越しの値がある人だけ）。 */
export function growVital(vitals: Vitals, id: string, hpGain: number, mpGain: number): Vitals {
  const cur = vitals[id];
  if (!cur) return vitals;
  return { ...vitals, [id]: { hp: cur.hp + Math.max(0, hpGain), mp: cur.mp + Math.max(0, mpGain) } };
}
