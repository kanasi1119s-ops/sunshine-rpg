import type { Combatant } from "./types";

/** 仲間ごとの「運」の初期値（レベルが3上がるごとに1ふえる）。運は、会心の一撃の出やすさと、攻撃のミスのしやすさ・されやすさに関わる。 */
const BASE_LUCK: Record<string, number> = { hero: 4, reto: 4, mina: 6, guide: 5, orca: 3, ayame: 7 };

export const DEFAULT_LUCK = 5;

/** 味方の運（ユーリ・仲間のID、レベルから決まる）。 */
export function allyLuck(id: string, level: number): number {
  return (BASE_LUCK[id] ?? DEFAULT_LUCK) + Math.floor(level / 3);
}

/** ランダムエンカウントの敵の運（出る場所のレベルから）。 */
export function enemyLuck(level: number): number {
  return 7 + Math.floor(level / 3);
}

/** 運。決まっていない敵（ボスなど）は、すばやさから決める（強い敵ほど運もよい）。 */
export function luckOf(c: Combatant): number {
  if (c.luck !== undefined) return c.luck;
  return c.isEnemy ? Math.floor(c.speed * 0.77) : DEFAULT_LUCK;
}
