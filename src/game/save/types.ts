import type { Direction } from "../../input/direction";
import type { Flags } from "../event/types";
import type { LeveledStats } from "../growth/types";
import type { EquipmentSlots } from "../items/equipment";
import type { Inventory } from "../items/inventory";

/**
 * セーブデータの構造バージョン。構造を変えるときは1つ上げて、
 * `migrateSaveData` に「古いバージョン → 新しいバージョン」の変換を追加する。
 */
export const SAVE_VERSION = 2;

export interface SaveData {
  version: typeof SAVE_VERSION;
  savedAt: string;
  player: {
    mapId: string;
    tileX: number;
    tileY: number;
    direction: Direction;
  };
  hero: {
    stats: LeveledStats;
    equipment: EquipmentSlots;
  };
  /** 仲間に加わったキャラクターのステータス（キャラクターIDをキーにする。version 2で追加）。 */
  companions: Record<string, { stats: LeveledStats }>;
  inventory: Inventory;
  flags: Flags;
}
