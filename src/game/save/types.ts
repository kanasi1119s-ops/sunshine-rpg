import type { Direction } from "../../input/direction";
import type { Flags } from "../event/types";
import type { LeveledStats } from "../growth/types";
import type { EquipmentSlots } from "../items/equipment";
import type { Inventory } from "../items/inventory";
import type { JobState } from "../job/types";

/**
 * セーブデータの構造バージョン。構造を変えるときは1つ上げて、
 * `migrateSaveData` に「古いバージョン → 新しいバージョン」の変換を追加する。
 */
export const SAVE_VERSION = 4;

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
  /** ジョブの装備・熟練度（キャラクターIDをキーにする。主人公は "hero"。version 3で追加）。 */
  jobs: Record<string, JobState>;
  inventory: Inventory;
  /** 所持している灯貨（お金。version 4で追加）。 */
  gold: number;
  flags: Flags;
}
