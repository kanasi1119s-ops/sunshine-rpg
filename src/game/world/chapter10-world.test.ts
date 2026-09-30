import { describe, expect, it } from "vitest";
import { WORLD_MAPS } from "./world";
import { CHAPTER10_MAPS, CHAPTER10_NPCS } from "./chapter10-world";
import { collectBattleIds, collectReferencedFlags, collectSetFlags, collectWarpTargets } from "../event/inspect";
import { createTileMap, isWalkable } from "../map/tile-map";
import { createEventRunner } from "../event/event-runner";
import type { Flags } from "../event/types";

/** メッセージ・選択肢のstepをすべて拾い集める。選択肢に出会うたびchoiceIndicesを順番に使う（足りなければ0番目）。 */
function runScripted(
  commands: Parameters<typeof createEventRunner>[0],
  flags: Flags,
  choiceIndices: number[] = [],
): string[] {
  const runner = createEventRunner(commands, flags);
  const texts: string[] = [];
  let choiceCount = 0;
  let result = runner.next();
  while (!result.done) {
    if (result.step?.kind === "message") {
      texts.push(result.step.text);
      result = runner.next({ kind: "advance" });
    } else if (result.step?.kind === "choice") {
      const index = choiceIndices[choiceCount] ?? 0;
      choiceCount++;
      result = runner.next({ kind: "choose", index });
    } else {
      break;
    }
  }
  return texts;
}

const KNOWN_BATTLE_IDS = new Set(["deep3-yugami", "deep-yugami"]);

/** main.ts側（戦闘勝利）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set([
  "deep3_yugami_defeated", "deep_yugami_defeated",
  ...Array.from({ length: 8 }, (_, i) => `god${i + 1}_fragment`), // 8神の禁域（chapter11-world.ts）で立つ
]);

function allNpcCommands() {
  return Object.values(CHAPTER10_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

function npcById(id: string) {
  for (const npcs of Object.values(CHAPTER10_NPCS)) {
    const found = npcs.find((n) => n.id === id);
    if (found) {
      return found;
    }
  }
  throw new Error(`${id} が見つからない`);
}

describe("虚灯宮・深部のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれ、重ならない", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER10_NPCS)) {
      const map = createTileMap(CHAPTER10_MAPS[mapId]);
      const seen = new Set<string>();
      for (const npc of npcs) {
        expect(isWalkable(map, npc.tileX, npc.tileY), `${mapId} の ${npc.id} が通行不可タイルにある`).toBe(true);
        const key = `${npc.tileX},${npc.tileY}`;
        expect(seen.has(key), `${mapId} の ${key} にNPCが重なる`).toBe(false);
        seen.add(key);
      }
    }
  });

  it("参照するフラグは、どこかのsetFlagで立てられている", () => {
    const all = allNpcCommands();
    const setFlags = collectSetFlags(all);
    for (const flag of collectReferencedFlags(all)) {
      if (!EXTERNALLY_SET_FLAGS.has(flag)) {
        expect(setFlags.has(flag), `フラグ "${flag}" がどこにも setFlag されていない`).toBe(true);
      }
    }
  });

  it("warpの移動先は実在し、startBattleの戦闘IDは登録済み", () => {
    for (const mapId of collectWarpTargets(allNpcCommands())) {
      expect(WORLD_MAPS[mapId]).toBeDefined();
    }
    for (const battleId of collectBattleIds(allNpcCommands())) {
      expect(KNOWN_BATTLE_IDS.has(battleId)).toBe(true);
    }
  });

  it("各階層の出入り口は、実在する地図の歩ける場所を指し、着いた瞬間に出入り口にならない", () => {
    for (const [mapId, data] of Object.entries(CHAPTER10_MAPS)) {
      for (const exit of data.exits ?? []) {
        const target = WORLD_MAPS[exit.targetMapId];
        expect(target, `${mapId} の出入り口の行き先が無い`).toBeDefined();
        const map = createTileMap(target);
        expect(isWalkable(map, exit.targetTileX, exit.targetTileY)).toBe(true);
        expect((target.exits ?? []).some((e) => e.tileX === exit.targetTileX && e.tileY === exit.targetTileY)).toBe(false);
      }
    }
  });
});

describe("虚灯宮・深部の仕掛けと裏ボス", () => {
  it("灯り石の台を2つともらすと封印の扉が開き、片方だけでは開かない", () => {
    const flags: Flags = {};
    runScripted(npcById("deep1-gate").commands, flags);
    expect(collectWarpTargets(npcById("deep1-gate").commands)).toEqual(new Set(["deep-2"]));
    runScripted(npcById("deep1-pedestal-a").commands, flags);
    expect(flags.deep1_lit).toBeUndefined();
    runScripted(npcById("deep1-pedestal-b").commands, flags);
    expect(flags.deep1_lit).toBe(true);
  });

  it("第1・第2階層で、大乱期の利用の形跡（C-018）と封印記録（C-019）が読める", () => {
    const flags: Flags = {};
    runScripted(npcById("deep1-tablet").commands, flags);
    runScripted(npcById("deep2-echo").commands, flags);
    expect(flags.deep1_tablet_read).toBe(true);
    expect(flags.deep2_record_read).toBe(true);
  });

  it("第3階層の残響は戦闘につながり、倒すと道が静まる。裏ボスは前置きのあと戦闘につながる", () => {
    expect(collectBattleIds(npcById("deep3-echo").commands)).toEqual(new Set(["deep3-yugami"]));
    const flags: Flags = {};
    runScripted(npcById("deep4-boss").commands, flags);
    expect(flags.deep_boss_told).toBe(true);
    expect(collectBattleIds(npcById("deep4-boss").commands)).toEqual(new Set(["deep-yugami"]));
  });

  it("裏ボスを倒すと転移陣の刻印が読め、クリア後の道が示される（C-021）。倒す前は進めない", () => {
    const before: Flags = {};
    runScripted(npcById("deep4-circle").commands, before);
    expect(before.deep_cleared).toBeUndefined();
    const after: Flags = { deep_yugami_defeated: true };
    const texts = runScripted(npcById("deep4-circle").commands, after).join("");
    expect(after.deep_cleared).toBe(true);
    expect(texts).toContain("八柱の神");
  });
});
