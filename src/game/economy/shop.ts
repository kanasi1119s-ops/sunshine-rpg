import { equip, type EquipmentSlots } from "../items/equipment";
import type { EquipmentItemData, ItemData, WeaponType } from "../items/types";
import { canEquip } from "../items/weapon-types";
import { SAMPLE_ITEMS_BY_ID } from "../battle/sample-battle";
import { spendGold } from "./gold";
import { TREASURE_ITEMS_BY_ID } from "./treasure";
import { CONSUMABLES_BY_ID, MAX_CONSUMABLE_STACK, consumableStock } from "../items/consumables";

/**
 * 町のお店（武具屋）で買える装備。町の順（第0章の灯里〜灯芯都）に1段ずつ強くなり、
 * 各店は「その町の段」と「ひとつ前の段」の武器・防具・飾りを売る。数値は仮。
 * 武器はキャラクターごとに種類が決まっている（`items/weapon-types.ts`）。
 */
interface Tier {
  /** 武器: 種類ごとの名前（攻撃力はどの種類も同じ）。 */
  weapons: Record<WeaponType, string>;
  attack: number;
  armor: { name: string; defense: number };
  charm: { name: string; maxHp: number };
}

const W = (sword: string, dagger: string, staff: string, bow: string, axe: string, spear: string): Record<WeaponType, string> => ({ sword, dagger, staff, bow, axe, spear });

const TIERS: Tier[] = [
  { weapons: W("灯り鉄の剣", "灯り鉄の短剣", "灯り木の杖", "灯り木の弓", "灯り鉄の斧", "灯り鉄の槍"), attack: 9, armor: { name: "灯編みの服", defense: 4 }, charm: { name: "灯りの腕飾り", maxHp: 8 } },
  { weapons: W("水鏡の剣", "水鏡の短剣", "水鏡の杖", "水鏡の弓", "水鏡の斧", "水鏡の槍"), attack: 14, armor: { name: "麦藁の外套", defense: 7 }, charm: { name: "水滴の首飾り", maxHp: 14 } },
  { weapons: W("湖光の刃", "湖光の小刃", "湖光の杖", "湖光の弓", "湖光の斧", "湖光の槍"), attack: 20, armor: { name: "湖織りの服", defense: 11 }, charm: { name: "湖珠の耳飾り", maxHp: 22 } },
  { weapons: W("鉄鎖断ちの大剣", "鉄鎖の短刀", "鉄輪の杖", "鉄弦の弓", "鉄鎖断ちの大斧", "鉄鎖の槍"), attack: 28, armor: { name: "坑夫の胸当て", defense: 16 }, charm: { name: "鉄の輪", maxHp: 32 } },
  { weapons: W("砂風の曲刀", "砂風の小曲刀", "砂風の杖", "砂風の弓", "砂風の斧", "砂風の槍"), attack: 37, armor: { name: "砂よけの外套", defense: 22 }, charm: { name: "砂の指輪", maxHp: 44 } },
  { weapons: W("霧割りの剣", "霧割りの短剣", "霧の杖", "霧割りの弓", "霧割りの斧", "霧割りの槍"), attack: 47, armor: { name: "霧絹の衣", defense: 29 }, charm: { name: "霧の飾り", maxHp: 58 } },
  { weapons: W("霜刃", "霜の小刃", "霜華の杖", "霜弦の弓", "霜刃の斧", "霜刃の槍"), attack: 58, armor: { name: "霜毛の外套", defense: 37 }, charm: { name: "氷の飾り", maxHp: 74 } },
  { weapons: W("雲裂きの剣", "雲裂きの短剣", "雲糸の杖", "雲裂きの弓", "雲裂きの斧", "雲裂きの槍"), attack: 71, armor: { name: "雲糸の鎧", defense: 46 }, charm: { name: "雲の腕輪", maxHp: 92 } },
  { weapons: W("灯芯の聖剣", "灯芯の短剣", "灯芯の聖杖", "灯芯の聖弓", "灯芯の聖斧", "灯芯の聖槍"), attack: 86, armor: { name: "灯芯の鎧", defense: 56 }, charm: { name: "灯芯の護り", maxHp: 112 } },
];

const BASE_PRICE = [80, 150, 290, 550, 1050, 2000, 3800, 7200, 13700];

/** 武器の種類 → 店のID（剣は、むかしからの `weapon-N`）。 */
const WEAPON_ID_PREFIX: Record<WeaponType, string> = { sword: "weapon", dagger: "dagger", staff: "staff", bow: "bow", axe: "axe", spear: "spear" };
const WEAPON_ORDER: WeaponType[] = ["sword", "dagger", "staff", "bow", "axe", "spear"];

function tierItems(index: number): EquipmentItemData[] {
  const tier = TIERS[index];
  const price = BASE_PRICE[index];
  return [
    ...WEAPON_ORDER.map((type): EquipmentItemData => ({
      id: `${WEAPON_ID_PREFIX[type]}-${index + 1}`,
      name: tier.weapons[type],
      category: "weapon",
      price,
      statBonus: { attack: tier.attack },
      weaponType: type,
    })),
    { id: `armor-${index + 1}`, name: tier.armor.name, category: "armor", price: Math.round(price * 0.8), statBonus: { defense: tier.armor.defense } },
    { id: `charm-${index + 1}`, name: tier.charm.name, category: "accessory", price: Math.round(price * 0.6), statBonus: { maxHp: tier.charm.maxHp } },
  ];
}

/** 店で売る装備すべて（ID→データ）。 */
export const SHOP_ITEMS_BY_ID: Record<string, EquipmentItemData> = Object.fromEntries(
  TIERS.flatMap((_, i) => tierItems(i)).map((item) => [item.id, item]),
);

/** 戦闘・つよさ画面で使う、すべての品物（最初の剣＋店の装備）。 */
export const ALL_ITEMS_BY_ID: Record<string, ItemData> = { ...SAMPLE_ITEMS_BY_ID, ...SHOP_ITEMS_BY_ID, ...TREASURE_ITEMS_BY_ID, ...CONSUMABLES_BY_ID };

/** 店ID: `tier-1`〜`tier-9`。並ぶ品は、その段の、武器（剣・短剣・杖・弓・斧・槍の6種）・防具・飾り。 */
export function shopStock(shopId: string): EquipmentItemData[] {
  const match = /^tier-(\d+)$/.exec(shopId);
  const tier = match ? Number(match[1]) : 0;
  if (tier < 1 || tier > TIERS.length) {
    return [];
  }
  return tierItems(tier - 1);
}

/** お店の画面に並べる品。店ID `tier-N` は装備、`items-N` は回復アイテム（道具屋）。 */
export function shopItems(shopId: string): ItemData[] {
  const itemsShop = /^items-(\d+)$/.exec(shopId);
  return itemsShop ? consumableStock(Number(itemsShop[1])) : shopStock(shopId);
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

/** 回復アイテムを1つ買う（所持数が上限なら買えない）。 */
export function purchaseConsumable(itemId: string, gold: number, owned: number): { ok: true; gold: number; message: string } | { ok: false; message: string } {
  const item = CONSUMABLES_BY_ID[itemId];
  if (!item) return { ok: false, message: "その品は、売っていない" };
  if (owned >= MAX_CONSUMABLE_STACK) return { ok: false, message: `${item.name}は、これ以上もてない` };
  const left = spendGold(gold, item.price);
  if (left === null) return { ok: false, message: "灯貨が足りない" };
  return { ok: true, gold: left, message: `${item.name}を買った！` };
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
  if (!canEquip("hero", item)) {
    return { equipment, equipped: false };
  }
  const currentId = equipment[item.category];
  const current = currentId ? ALL_ITEMS_BY_ID[currentId] : undefined;
  if (current && current.category !== "consumable" && bonusTotal(current) >= bonusTotal(item)) {
    return { equipment, equipped: false };
  }
  return { equipment: equip(equipment, item), equipped: true };
}
