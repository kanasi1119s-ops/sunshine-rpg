import { createMugikanoVillageData } from "../map/chapter1/mugikano-village";
import { createMugikanoWaterSourceData } from "../map/chapter1/mugikano-water-source";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第1章（麦香野）の世界。`docs/story/structure.md`「第1章（麦香野）」・
 * `docs/story/mystery.md`（真相）・`docs/story/clue-ledger.md`（伏線 C-002）を反映。
 */
export const CHAPTER1_MAPS: Record<string, TileMapData> = {
  "mugikano-village": createMugikanoVillageData(),
  "mugikano-water-source": createMugikanoWaterSourceData(),
};

/**
 * 麦香野へ到着したとき、一度だけ流す短い場面つなぎ（`chapter1_intro_seen` フラグで管理）。
 */
export const CHAPTER1_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――数日後、麦香野。" },
  {
    type: "message",
    text: "灯里での一件を灯芯都へ報告したカセンの指示で、ユーリとレトは次の依頼地・麦香野へ向かった。",
  },
  {
    type: "message",
    text: "村に着くなり、慌ただしい様子の村人たちに出迎えられる。水路の水が、突然涸れてしまったのだという。",
  },
  { type: "setFlag", flag: "chapter1_intro_seen", value: true },
];

export const CHAPTER1_NPCS: Record<string, Npc[]> = {
  "mugikano-village": [],
  "mugikano-water-source": [],
};
