import type { EquipmentItemData, ItemData, WeaponType } from "./types";

/**
 * 専用武器。キャラクターごとに持てる武器の種類が決まっている（杖のミナが剣を持たない、など）。
 * 主人公のキャラクターIDは "hero"。
 */
export const WEAPON_TYPE_OF: Record<string, WeaponType> = {
  hero: "sword",
  reto: "dagger",
  mina: "staff",
  guide: "bow",
  orca: "axe",
  ayame: "spear",
};

export const WEAPON_LABEL: Record<WeaponType, string> = {
  sword: "剣",
  dagger: "短剣",
  staff: "杖",
  bow: "弓",
  axe: "斧",
  spear: "槍",
};

/** 武器の種類 → アイコンの名前（`icon:weapon-*`）。 */
export const WEAPON_ICON: Record<WeaponType, string> = {
  sword: "weapon-sword",
  dagger: "weapon-dagger",
  staff: "weapon-staff",
  bow: "weapon-bow",
  axe: "weapon-axe",
  spear: "weapon-spear",
};

export function weaponTypeOf(item: ItemData): WeaponType | undefined {
  return item.category === "weapon" ? (item as EquipmentItemData).weaponType ?? "sword" : undefined;
}

/** その人が、その品を身につけられるか（武器だけ、種類が合うものに限る）。 */
export function canEquip(owner: string, item: ItemData): boolean {
  const type = weaponTypeOf(item);
  if (type !== undefined && WEAPON_TYPE_OF[owner] !== type && !(item as EquipmentItemData).anyWielder) return false;
  const wearers = item.category === "consumable" ? undefined : (item as EquipmentItemData).wearers;
  return !wearers || wearers.includes(owner);
}

/** その武器を持てる人のキャラクターID。 */
export function wielderOf(type: WeaponType): string | undefined {
  return Object.entries(WEAPON_TYPE_OF).find(([, t]) => t === type)?.[0];
}

/** キャラクターIDごとの名前（画面に出す用）。 */
export const WIELDER_NAME: Record<string, string> = { hero: "ユーリ", reto: "レト", mina: "ミナ", guide: "コハク", orca: "オルカ", ayame: "アヤメ" };

/** その種類の武器を持つ人の名前。 */
export function wielderName(type: WeaponType): string {
  const id = wielderOf(type);
  return (id && WIELDER_NAME[id]) || "";
}
