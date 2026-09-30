import type { Combatant } from "./types";

/**
 * 芯環塔・環奥の敵（`docs/story/secret-boss.md` 4・5章、roadmap 6-8〜6-11）。
 * 数値は自動シミュレーション300回（`chapter12-balance.test.ts`）で調整する。Lv1の6人パーティに対する勝率の目安は、
 * 塔の強敵が約75〜85%、宝の番人・裂け目の守り手が約60〜70%、ラスト裏ボス「全環」が約30〜50%。
 */
export interface DungeonEnemyData {
  id: string;
  name: string;
  maxHp: number;
  attack: number;
  defense: number;
  speed: number;
  expReward: number;
}

export const DUNGEON_ENEMIES: DungeonEnemyData[] = [
  { id: "tower2-guard", name: "雲路の結晶獣", maxHp: 314, attack: 27, defense: 12, speed: 13, expReward: 350 },
  { id: "tower3-guard", name: "環光の番人", maxHp: 300, attack: 29, defense: 12, speed: 14, expReward: 600 },
  { id: "kanou3-guard", name: "裂け目の守り手", maxHp: 302, attack: 29, defense: 12, speed: 14, expReward: 700 },
  { id: "zenkan", name: "全環", maxHp: 310, attack: 30, defense: 12, speed: 15, expReward: 2000 },
];

export function createDungeonEnemy(data: DungeonEnemyData): Combatant {
  return {
    id: data.id,
    name: data.name,
    maxHp: data.maxHp,
    hp: data.maxHp,
    maxMp: 0,
    mp: 0,
    attack: data.attack,
    defense: data.defense,
    speed: data.speed,
    isEnemy: true,
    guarding: false,
    expReward: data.expReward,
  };
}
