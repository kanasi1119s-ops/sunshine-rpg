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
  /** 仲間の装備（`equipment` は後から足した項目。古いセーブには無い）。 */
  companions: Record<string, { stats: LeveledStats; equipment?: EquipmentSlots }>;
  /** ジョブの装備・熟練度（キャラクターIDをキーにする。主人公は "hero"。version 3で追加）。 */
  jobs: Record<string, JobState>;
  inventory: Inventory;
  /** 所持している灯貨（お金。version 4で追加）。 */
  gold: number;
  flags: Flags;
  /** モード（"easy" | "normal"）と、ノーマルで持ち越すHP・MP。古いセーブには無い（オプション）。 */
  difficulty?: "easy" | "normal";
  vitals?: Record<string, { hp: number; mp: number }>;
  /** ゲームの中の時間（ミリ秒。0＝朝）。古いセーブには無い（オプション）。 */
  clockMs?: number;
  /** 世界地図の乗り物（船・飛空艇の置き場所と、いま乗っているもの）。古いセーブには無い（オプション）。 */
  vehicles?: { mode: "foot" | "ship" | "air"; ship: { x: number; y: number }; airship: { x: number; y: number } };
}
