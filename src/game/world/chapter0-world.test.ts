import { describe, expect, it } from "vitest";
import { CHAPTER0_MAPS, CHAPTER0_NPCS, CHAPTER0_OPENING_COMMANDS, CHAPTER0_START } from "./chapter0-world";
import { collectBattleIds, collectReferencedFlags, collectSetFlags, collectWarpTargets } from "../event/inspect";
import { createTileMap, isWalkable } from "../map/tile-map";

const KNOWN_BATTLE_IDS = new Set(["chapter0-yugami"]);

/** イベントスクリプトのsetFlagではなく、main.ts側（戦闘勝利など）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["chapter0_yugami_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER0_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

describe("序章のイベントデータの整合性", () => {
  it("開始地点のマップが実在し、通行可能なタイルに立つ", () => {
    const map = createTileMap(CHAPTER0_MAPS[CHAPTER0_START.mapId]);
    expect(map).toBeDefined();
    expect(isWalkable(map, CHAPTER0_START.tileX, CHAPTER0_START.tileY)).toBe(true);
  });

  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER0_NPCS)) {
      const data = CHAPTER0_MAPS[mapId];
      expect(data, `${mapId} という地図が存在しない`).toBeDefined();
      const map = createTileMap(data);
      for (const npc of npcs) {
        expect(
          isWalkable(map, npc.tileX, npc.tileY),
          `${mapId} の ${npc.id} (${npc.tileX},${npc.tileY}) が通行不可タイルに置かれている`,
        ).toBe(true);
      }
    }
  });

  it("会話・オープニングが参照するフラグは、どこかのsetFlagで立てられている", () => {
    const allCommands = [...CHAPTER0_OPENING_COMMANDS, ...allNpcCommands()];
    const setFlags = collectSetFlags(allCommands);
    const referencedFlags = collectReferencedFlags(allCommands);
    for (const flag of referencedFlags) {
      if (EXTERNALLY_SET_FLAGS.has(flag)) {
        continue;
      }
      expect(setFlags.has(flag), `フラグ "${flag}" がどこにも setFlag されていない`).toBe(true);
    }
  });

  it("warpコマンドの移動先は、すべて実在するマップ", () => {
    const targets = collectWarpTargets(allNpcCommands());
    for (const mapId of targets) {
      expect(CHAPTER0_MAPS[mapId], `${mapId} という地図が存在しない`).toBeDefined();
    }
  });

  it("startBattleコマンドが指す戦闘IDは、main.ts側に登録されているものと一致する", () => {
    const battleIds = collectBattleIds(allNpcCommands());
    for (const battleId of battleIds) {
      expect(KNOWN_BATTLE_IDS.has(battleId), `${battleId} という戦闘データが登録されていない`).toBe(true);
    }
  });
});
