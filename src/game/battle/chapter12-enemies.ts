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
  { id: "tower2-guard", name: "雲路の結晶獣", maxHp: 6477, attack: 106, defense: 34, speed: 29, expReward: 12633 },
  { id: "tower6-guard", name: "星図の書守", maxHp: 6950, attack: 109, defense: 34, speed: 29, expReward: 13200 },
  { id: "tower3-guard", name: "環光の番人", maxHp: 7534, attack: 112, defense: 35, speed: 30, expReward: 13896 },
  { id: "tower7-guard", name: "嵐を纏う階守", maxHp: 7860, attack: 115, defense: 36, speed: 30, expReward: 14500 },
  { id: "kanou3-guard", name: "裂け目の守り手", maxHp: 8194, attack: 118, defense: 37, speed: 31, expReward: 15198 },
  { id: "zenkan", name: "全環", maxHp: 9404, attack: 124, defense: 39, speed: 33, expReward: 16539 },
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
