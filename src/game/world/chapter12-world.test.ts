import { describe, expect, it } from "vitest";
import { WORLD_MAPS } from "./world";
import { CHAPTER12_MAPS, CHAPTER12_NPCS } from "./chapter12-world";
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

const KNOWN_BATTLE_IDS = new Set(["tower2-guard", "tower3-guard", "kanou3-guard", "zenkan"]);

/** main.ts側（戦闘勝利）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["tower2_guard_defeated", "tower3_guard_defeated", "kanou3_guard_defeated", "zenkan_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER12_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

function npcById(id: string) {
  for (const npcs of Object.values(CHAPTER12_NPCS)) {
    const found = npcs.find((n) => n.id === id);
    if (found) {
      return found;
    }
  }
  throw new Error(`${id} が見つからない`);
}

describe("芯環塔・環奥のイベントデータの整合性", () => {
  it("NPCは実在するマップの、通行可能なタイルに置かれ、重ならない。出入り口・到着地点の上にも置かない", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER12_NPCS)) {
      const data = CHAPTER12_MAPS[mapId];
      const map = createTileMap(data);
      const arrivals = Object.values(WORLD_MAPS).flatMap((m) => m.exits ?? []).filter((e) => e.targetMapId === mapId);
      const seen = new Set<string>();
      for (const npc of npcs) {
        expect(isWalkable(map, npc.tileX, npc.tileY), `${mapId} の ${npc.id} が通行不可タイルにある`).toBe(true);
        const key = `${npc.tileX},${npc.tileY}`;
        expect(seen.has(key), `${mapId} の ${key} にNPCが重なる`).toBe(false);
        seen.add(key);
        expect((data.exits ?? []).some((e) => e.tileX === npc.tileX && e.tileY === npc.tileY), `${npc.id} が出入り口の上`).toBe(false);
        expect(arrivals.some((e) => e.targetTileX === npc.tileX && e.targetTileY === npc.tileY), `${npc.id} が到着地点の上`).toBe(false);
      }
    }
  });

  it("参照するフラグはどこかで立てられ、warpの行き先は実在し、戦闘IDは登録済み", () => {
    const all = allNpcCommands();
    const setFlags = collectSetFlags(all);
    for (const flag of collectReferencedFlags(all)) {
      if (!EXTERNALLY_SET_FLAGS.has(flag)) {
        expect(setFlags.has(flag), `フラグ "${flag}" がどこにも setFlag されていない`).toBe(true);
      }
    }
    for (const mapId of collectWarpTargets(all)) {
      expect(WORLD_MAPS[mapId]).toBeDefined();
    }
    expect(collectBattleIds(all)).toEqual(KNOWN_BATTLE_IDS);
  });

  it("各階層の出入り口は、実在する地図の歩ける場所を指し、着いた瞬間に出入り口にならない", () => {
    for (const [mapId, data] of Object.entries(CHAPTER12_MAPS)) {
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

describe("芯環塔・環奥の仕掛けとラスト裏ボス", () => {
  it("環光の階で、二つの紋様を読むと世界の真実が分かる。片方だけでは分からない", () => {
    const flags: Flags = {};
    runScripted(npcById("tower3-mural-a").commands, flags);
    runScripted(npcById("tower3-truth").commands, flags);
    expect(flags.tower_truth_known).toBeUndefined();
    runScripted(npcById("tower3-mural-b").commands, flags);
    runScripted(npcById("tower3-truth").commands, flags);
    expect(flags.tower_truth_known).toBe(true);
  });

  it("環奥の分かれ道は、灯り石を灯す前は進めず、光の照らす道（先頭）が正解。ほかの道は戻される", () => {
    const flags: Flags = {};
    const before = runScripted(npcById("kanou1-fork").commands, flags).join("");
    expect(before).toContain("三つに分かれている");
    flags.kanou1_lit = true;
    const wrong = runScripted(npcById("kanou1-fork").commands, flags, [1]).join("");
    expect(wrong).toContain("同じ場所に戻ってきてしまう");
    const right = runScripted(npcById("kanou1-fork").commands, flags, [0]).join("");
    expect(right).toContain("光をたどる");
  });

  it("全環は前置きのあと戦闘につながり、倒すとエンディング（仮）に進む。倒す前はエンディングにならない", () => {
    const flags: Flags = {};
    runScripted(npcById("kanou4-boss").commands, flags);
    expect(flags.zenkan_told).toBe(true);
    expect(flags.epilogue_all_seen).toBeUndefined();
    flags.zenkan_defeated = true;
    const texts = runScripted(npcById("kanou4-boss").commands, flags).join("");
    expect(flags.epilogue_all_seen).toBe(true);
    expect(texts).toContain("すべての物語を終えました");
  });
});
