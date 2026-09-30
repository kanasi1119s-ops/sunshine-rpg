import type { BattleState } from "../battle/types";

/** 敵1体を倒したときに手に入る灯貨（経験値の約6割）。 */
export function goldForEnemy(expReward: number): number {
  return Math.max(1, Math.round(expReward * 0.6));
}

/** 戦闘に勝ったときの灯貨の合計（倒した敵ぶん）。 */
export function computeVictoryGold(state: BattleState): number {
  return state.enemies.reduce((sum, enemy) => sum + goldForEnemy(enemy.expReward ?? 0), 0);
}

/** 灯貨を足す（0未満にはならない）。 */
export function addGold(current: number, amount: number): number {
  return Math.max(0, Math.floor(current + amount));
}

/** 灯貨を払う。足りなければ null。 */
export function spendGold(current: number, price: number): number | null {
  return current >= price ? current - price : null;
}
