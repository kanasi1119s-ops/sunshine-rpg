import { equip, type EquipmentSlots } from "../items/equipment";
import type { EquipmentItemData, ItemData } from "../items/types";
import { SAMPLE_ITEMS_BY_ID } from "../battle/sample-battle";
import { spendGold } from "./gold";
import { TREASURE_ITEMS_BY_ID } from "./treasure";

/**
 * 町のお店（武具屋）で買える装備。町の順（第0章の灯里〜灯芯都）に1段ずつ強くなり、
 * 各店は「その町の段」と「ひとつ前の段」の武器・防具・飾りを売る。数値は仮。
 * 装備できるのはユーリだけ（仲間には装備の仕組みがまだない）。買うとその場で装備する。
 */
interface Tier {
  weapon: { name: string; attack: number };
  armor: { name: string; defense: number };
  charm: { name: string; maxHp: number };
}

const TIERS: Tier[] = [
  { weapon: { name: "灯り鉄の剣", attack: 9 }, armor: { name: "灯編みの服", defense: 4 }, charm: { name: "灯りの腕飾り", maxHp: 8 } },
  { weapon: { name: "水鏡の剣", attack: 14 }, armor: { name: "麦藁の外套", defense: 7 }, charm: { name: "水滴の首飾り", maxHp: 14 } },
  { weapon: { name: "湖光の刃", attack: 20 }, armor: { name: "湖織りの服", defense: 11 }, charm: { name: "湖珠の耳飾り", maxHp: 22 } },
  { weapon: { name: "鉄鎖断ちの大剣", attack: 28 }, armor: { name: "坑夫の胸当て", defense: 16 }, charm: { name: "鉄の輪", maxHp: 32 } },
  { weapon: { name: "砂風の曲刀", attack: 37 }, armor: { name: "砂よけの外套", defense: 22 }, charm: { name: "砂の指輪", maxHp: 44 } },
  { weapon: { name: "霧割りの剣", attack: 47 }, armor: { name: "霧絹の衣", defense: 29 }, charm: { name: "霧の飾り", maxHp: 58 } },
  { weapon: { name: "霜刃", attack: 58 }, armor: { name: "霜毛の外套", defense: 37 }, charm: { name: "氷の飾り", maxHp: 74 } },
  { weapon: { name: "雲裂きの剣", attack: 71 }, armor: { name: "雲糸の鎧", defense: 46 }, charm: { name: "雲の腕輪", maxHp: 92 } },
  { weapon: { name: "灯芯の聖剣", attack: 86 }, armor: { name: "灯芯の鎧", defense: 56 }, charm: { name: "灯芯の護り", maxHp: 112 } },
];

const BASE_PRICE = [80, 150, 290, 550, 1050, 2000, 3800, 7200, 13700];

function tierItems(index: number): EquipmentItemData[] {
  const tier = TIERS[index];
  const price = BASE_PRICE[index];
  return [
    { id: `weapon-${index + 1}`, name: tier.weapon.name, category: "weapon", price, statBonus: { attack: tier.weapon.attack } },
    { id: `armor-${index + 1}`, name: tier.armor.name, category: "armor", price: Math.round(price * 0.8), statBonus: { defense: tier.armor.defense } },
    { id: `charm-${index + 1}`, name: tier.charm.name, category: "accessory", price: Math.round(price * 0.6), statBonus: { maxHp: tier.charm.maxHp } },
  ];
}

/** 店で売る装備すべて（ID→データ）。 */
export const SHOP_ITEMS_BY_ID: Record<string, EquipmentItemData> = Object.fromEntries(
  TIERS.flatMap((_, i) => tierItems(i)).map((item) => [item.id, item]),
);

/** 戦闘・つよさ画面で使う、すべての品物（最初の剣＋店の装備）。 */
export const ALL_ITEMS_BY_ID: Record<string, ItemData> = { ...SAMPLE_ITEMS_BY_ID, ...SHOP_ITEMS_BY_ID, ...TREASURE_ITEMS_BY_ID };

/** 店ID: `tier-1`〜`tier-9`。並ぶ品は、その段とひとつ前の段（1段目は、その段の3品だけ）。 */
export function shopStock(shopId: string): EquipmentItemData[] {
  const match = /^tier-(\d+)$/.exec(shopId);
  const tier = match ? Number(match[1]) : 0;
  if (tier < 1 || tier > TIERS.length) {
    return [];
  }
  return [...(tier >= 2 ? tierItems(tier - 2) : []), ...tierItems(tier - 1)];
}

function bonusTotal(item: EquipmentItemData): number {
  return Object.values(item.statBonus).reduce((sum, v) => sum + (v ?? 0), 0);
}

export type BuyResult =
  | { ok: true; gold: number; equipment: EquipmentSlots; message: string }
  | { ok: false; message: string };

/** 1つ買う。同じ種類の、いまの装備より強いときだけ買え、買うとその場で装備する。 */
export function buyItem(itemId: string, gold: number, equipment: EquipmentSlots): BuyResult {
  const item = SHOP_ITEMS_BY_ID[itemId];
  if (!item) {
    return { ok: false, message: "その品は、売っていない" };
  }
  const currentId = equipment[item.category];
  const current = currentId ? ALL_ITEMS_BY_ID[currentId] : undefined;
  if (currentId === item.id) {
    return { ok: false, message: "すでに装備している" };
  }
  if (current && current.category !== "consumable" && bonusTotal(current) >= bonusTotal(item)) {
    return { ok: false, message: "いまの装備のほうが強い" };
  }
  const left = spendGold(gold, item.price);
  if (left === null) {
    return { ok: false, message: "灯貨が足りない" };
  }
  return { ok: true, gold: left, equipment: equip(equipment, item), message: `${item.name}を買って、装備した！` };
}

export type PurchaseResult =
  | { ok: true; gold: number; item: EquipmentItemData; message: string }
  | { ok: false; message: string };

/** 買うだけ（装備は、買ったあとに「だれにつけるか」を選んで決める）。強さに関係なく、灯貨が足りれば買える。 */
export function purchaseItem(itemId: string, gold: number): PurchaseResult {
  const item = SHOP_ITEMS_BY_ID[itemId];
  if (!item) {
    return { ok: false, message: "その品は、売っていない" };
  }
  const left = spendGold(gold, item.price);
  if (left === null) {
    return { ok: false, message: "灯貨が足りない" };
  }
  return { ok: true, gold: left, item, message: `${item.name}を買った！` };
}

/** 装備のボーナスの説明（例: 「こうげき+9」）。 */
export function describeBonus(item: EquipmentItemData): string {
  const names: Record<string, string> = { attack: "こうげき", defense: "ぼうぎょ", speed: "すばやさ", maxHp: "HP", maxMp: "MP" };
  return Object.entries(item.statBonus).map(([k, v]) => `${names[k] ?? k}+${v}`).join(" ");
}

/** 宝の装備を受け取る。いまの装備より強ければその場で装備し、そうでなければ装備はそのまま。 */
export function receiveTreasure(itemId: string, equipment: EquipmentSlots): { equipment: EquipmentSlots; equipped: boolean } {
  const item = TREASURE_ITEMS_BY_ID[itemId];
  if (!item) {
    return { equipment, equipped: false };
  }
  const currentId = equipment[item.category];
  const current = currentId ? ALL_ITEMS_BY_ID[currentId] : undefined;
  if (current && current.category !== "consumable" && bonusTotal(current) >= bonusTotal(item)) {
    return { equipment, equipped: false };
  }
  return { equipment: equip(equipment, item), equipped: true };
}
