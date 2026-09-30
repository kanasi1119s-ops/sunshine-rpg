import type { Combatant } from "./types";

/**
 * 8神（`docs/story/secret-boss.md` 3章、roadmap 6-4〜6-7）。各地方の禁域を守る8体の裏ボス。
 * 数値は自動シミュレーション300回（`chapter11-balance.test.ts`）で、Lv1の6人パーティに対する勝率が目安60〜75%になるよう調整。
 * 実際のクリア後は、仲間はもっと育っているはずなので、これはいちばん厳しい場合の目安。
 */
export interface GodData {
  /** 1〜8（本編の章の番号と同じ）。 */
  no: number;
  /** 戦闘・フラグに使うID。例: "god-1"。 */
  id: string;
  /** 総称。 */
  kind: string;
  /** 正式な名（敵の名前として表示）。 */
  name: string;
  maxHp: number;
  attack: number;
  defense: number;
  speed: number;
}

export const GODS: GodData[] = [
  { no: 1, id: "god-1", kind: "女神", name: "恵みの残照", maxHp: 6371, attack: 100, defense: 32, speed: 28 },
  { no: 2, id: "god-2", kind: "蟲神", name: "理不尽の羽音", maxHp: 6452, attack: 100, defense: 32, speed: 28 },
  { no: 3, id: "god-3", kind: "鬼神", name: "坩堝の顎", maxHp: 6499, attack: 100, defense: 32, speed: 28 },
  { no: 4, id: "god-4", kind: "無神", name: "在らざる歌", maxHp: 6371, attack: 100, defense: 32, speed: 28 },
  { no: 5, id: "god-5", kind: "純神", name: "透き徹る誓い", maxHp: 6426, attack: 100, defense: 32, speed: 28 },
  { no: 6, id: "god-6", kind: "武神", name: "不敗の咎人", maxHp: 6650, attack: 100, defense: 32, speed: 28 },
  { no: 7, id: "god-7", kind: "異神", name: "境界を見ぬ者", maxHp: 6452, attack: 100, defense: 32, speed: 28 },
  { no: 8, id: "god-8", kind: "冥神", name: "無音の弔鐘", maxHp: 6689, attack: 100, defense: 32, speed: 28 },
];

export function createGodYugami(god: GodData): Combatant {
  return {
    id: god.id,
    name: god.name,
    maxHp: god.maxHp,
    hp: god.maxHp,
    maxMp: 0,
    mp: 0,
    attack: god.attack,
    defense: god.defense,
    speed: god.speed,
    isEnemy: true,
    guarding: false,
    expReward: 9000,
  };
}
