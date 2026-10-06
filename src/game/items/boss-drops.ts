import type { EquipmentItemData, ItemTrait } from "./types";

/**
 * ボスを倒すと落とす、特殊効果つきのかざり。ボスの戦闘ID（`STORY_BATTLES` のキー）ごとに1つ。
 * 店では売っていない。効果は `traits`（`items/types.ts`）。数値は仮。
 */
interface DropDef {
  battleId: string;
  name: string;
  statBonus: EquipmentItemData["statBonus"];
  traits: ItemTrait[];
  description: string;
}

const G = (status: "poison" | "sleep" | "confuse"): ItemTrait => ({ kind: "guard", status });

const DROPS: DropDef[] = [
  { battleId: "chapter0-yugami", name: "灯りの幸運石", statBonus: { maxHp: 6 }, traits: [{ kind: "luck", value: 3 }], description: "灯里の歪みが落とした小さな石。持つと運がよくなる。" },
  { battleId: "mugikano-yugami", name: "水脈のしずく飾り", statBonus: { maxMp: 4 }, traits: [{ kind: "regenMp", value: 2 }], description: "ターンの終わりに、魔力が少しもどる。" },
  { battleId: "garasuko-yugami", name: "積荷の目利き札", statBonus: { attack: 3 }, traits: [{ kind: "crit", value: 4 }], description: "急所を見ぬく札。会心の一撃が出やすい。" },
  { battleId: "tetsukusari-yugami", name: "坑夫の護り輪", statBonus: { defense: 4 }, traits: [G("poison")], description: "毒を寄せつけない鉄の輪。" },
  { battleId: "sanone-yugami", name: "砂よけの瞳石", statBonus: { speed: 3 }, traits: [{ kind: "evade", value: 6 }], description: "砂嵐の中でも目を守る石。敵の攻撃がはずれやすくなる。" },
  { battleId: "kiri-yugami", name: "霧晴れの鈴", statBonus: {}, traits: [G("confuse"), { kind: "luck", value: 2 }], description: "澄んだ音で、頭の霧を晴らす。混乱しない。" },
  { battleId: "shimohara-yugami", name: "霜越えの炉石", statBonus: { maxHp: 20 }, traits: [{ kind: "regenHp", percent: 3 }], description: "ほんのり温かい石。毎ターンHPが少し回復する。" },
  { battleId: "fushima-yugami", name: "浮嶼の羽根飾り", statBonus: { speed: 6 }, traits: [{ kind: "multi", value: 4 }], description: "体が軽くなる羽根。連続攻撃がしやすい。" },
  { battleId: "toushin-yugami", name: "灯芯の誓いの飾り", statBonus: { maxHp: 30 }, traits: [G("sleep")], description: "灯りの誓いが眠気をはらう。眠らない。" },
  { battleId: "kyotoukyu-yugami", name: "虚灯のかけら", statBonus: { attack: 10 }, traits: [{ kind: "crit", value: 6 }, { kind: "luck", value: 4 }], description: "虚灯宮の光のかけら。運と会心がのびる。" },
  { battleId: "deep3-yugami", name: "残響の耳飾り", statBonus: { maxMp: 20 }, traits: [{ kind: "regenMp", value: 4 }], description: "消えない響きが魔力をよぶ。" },
  { battleId: "deep-yugami", name: "初源の灯り", statBonus: { maxHp: 40 }, traits: [{ kind: "regenHp", percent: 4 }, G("poison"), G("sleep"), G("confuse"), { kind: "luck", value: 5 }], description: "最初の灯り。あらゆる状態異常をふせぎ、HPも少しずつ回復する。" },
  { battleId: "tower2-guard", name: "結晶獣の心核", statBonus: { defense: 20 }, traits: [{ kind: "regenHp", percent: 3 }], description: "かたい結晶の核。" },
  { battleId: "tower6-guard", name: "星図の栞", statBonus: { maxMp: 30 }, traits: [{ kind: "regenMp", value: 5 }], description: "星の並びを写した栞。心が澄む。" },
  { battleId: "tower7-guard", name: "嵐切りの羽かざり", statBonus: { speed: 10 }, traits: [{ kind: "multi", value: 6 }], description: "嵐の風を切った羽。" },
  { battleId: "tower3-guard", name: "環光の冠かざり", statBonus: {}, traits: [{ kind: "luck", value: 6 }, { kind: "crit", value: 5 }], description: "輪の光をまとった飾り。" },
  { battleId: "kanou3-guard", name: "裂け目の指輪", statBonus: { speed: 8 }, traits: [{ kind: "evade", value: 10 }], description: "裂け目をすり抜ける軽い指輪。" },
  { battleId: "zenkan", name: "全環の輪", statBonus: { attack: 20 }, traits: [{ kind: "crit", value: 8 }, { kind: "multi", value: 8 }, { kind: "luck", value: 8 }], description: "すべての環を束ねた輪。" },
  { battleId: "god-1", name: "残照の加護", statBonus: { maxHp: 60 }, traits: [{ kind: "regenHp", percent: 5 }], description: "恵みの光が、毎ターン傷をいやす。" },
  { battleId: "god-2", name: "羽音の護符", statBonus: { speed: 10 }, traits: [{ kind: "evade", value: 12 }], description: "羽音のように、攻撃をかわす。" },
  { battleId: "god-3", name: "坩堝の牙飾り", statBonus: { attack: 25 }, traits: [{ kind: "crit", value: 6 }], description: "あらゆる力を溶かした牙。" },
  { battleId: "god-4", name: "無歌の指輪", statBonus: { defense: 10 }, traits: [G("poison"), G("sleep"), G("confuse")], description: "音のない歌が、状態異常をはじく。" },
  { battleId: "god-5", name: "誓いの水晶", statBonus: { maxHp: 80 }, traits: [G("poison"), G("sleep")], description: "透きとおる誓い。毒と眠りをふせぐ。" },
  { battleId: "god-6", name: "咎人の腕輪", statBonus: { attack: 30 }, traits: [{ kind: "multi", value: 6 }], description: "負けを知らぬ腕輪。連続攻撃がしやすい。" },
  { battleId: "god-7", name: "境界の鍵かざり", statBonus: {}, traits: [{ kind: "luck", value: 10 }, { kind: "evade", value: 8 }], description: "境のすき間を開ける鍵。" },
  { battleId: "god-8", name: "弔鐘の鈴", statBonus: { maxMp: 40 }, traits: [{ kind: "regenMp", value: 6 }], description: "静かな鐘の音が、魔力をうるおす。" },
];

export const BOSS_DROP_ITEMS: EquipmentItemData[] = DROPS.map((d) => ({
  id: `boss-${d.battleId}`,
  name: d.name,
  category: "accessory",
  price: 0,
  statBonus: d.statBonus,
  traits: d.traits,
  description: d.description,
}));

export const BOSS_DROP_ITEMS_BY_ID: Record<string, EquipmentItemData> = Object.fromEntries(BOSS_DROP_ITEMS.map((i) => [i.id, i]));

/** そのボスの戦闘IDが落とすかざりのID（落とさない戦闘は undefined）。 */
export function bossDropFor(battleId: string): string | undefined {
  const id = `boss-${battleId}`;
  return BOSS_DROP_ITEMS_BY_ID[id] ? id : undefined;
}
