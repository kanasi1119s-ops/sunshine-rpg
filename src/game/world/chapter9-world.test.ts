import { describe, expect, it } from "vitest";
import { WORLD_MAPS } from "./world";
import { CHAPTER9_MAPS, CHAPTER9_NPCS, CHAPTER9_OPENING_COMMANDS } from "./chapter9-world";
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

const KNOWN_BATTLE_IDS = new Set(["kyotoukyu-yugami"]);

/** main.ts側（戦闘勝利）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["chapter9_yugami_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER9_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

function npcById(mapId: string, id: string) {
  const npc = CHAPTER9_NPCS[mapId]?.find((n) => n.id === id);
  if (!npc) {
    throw new Error(`${id} が見つからない`);
  }
  return npc;
}

const muralLeft = () => npcById("kyotoukyu-corridor", "kyotoukyu-mural-left");
const muralRight = () => npcById("kyotoukyu-corridor", "kyotoukyu-mural-right");
const edrea = () => npcById("kyotoukyu-sanctum", "kyotoukyu-edrea");
const grandfather = () => npcById("kyotoukyu-sanctum", "kyotoukyu-grandfather");

describe("終章のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER9_NPCS)) {
      const map = createTileMap(CHAPTER9_MAPS[mapId]);
      for (const npc of npcs) {
        expect(isWalkable(map, npc.tileX, npc.tileY), `${mapId} の ${npc.id} が通行不可タイルにある`).toBe(true);
      }
    }
  });

  it("参照するフラグは、どこかのsetFlagで立てられている", () => {
    const all = [...CHAPTER9_OPENING_COMMANDS, ...allNpcCommands()];
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
});

describe("終章の壁画・最終決戦・祖父の救出・エンディング", () => {
  it("壁画を左右とも読むと、真相がつながる。片方だけでは足りない", () => {
    const one: Flags = {};
    runScripted(muralRight().commands, one);
    expect(one.chapter9_truth_known).toBeUndefined();
    const both: Flags = {};
    runScripted(muralLeft().commands, both);
    runScripted(muralRight().commands, both);
    expect(both.chapter9_truth_known).toBe(true);
  });

  it("エドレアの最後の計画を聞くと、最終決戦につながる", () => {
    const flags: Flags = {};
    const texts = runScripted(edrea().commands, flags).join("");
    expect(flags.chapter9_edrea_told).toBe(true);
    expect(texts).toContain("静めの間");
    expect(collectBattleIds(edrea().commands)).toEqual(new Set(["kyotoukyu-yugami"]));
  });

  it("決戦に勝つとエドレアが投降し、その前は祖父を起こせない（C-017）", () => {
    const early: Flags = {};
    runScripted(grandfather().commands, early);
    expect(early.chapter9_grandfather_rescued).toBeUndefined();
    const flags: Flags = { chapter9_yugami_defeated: true };
    runScripted(edrea().commands, flags);
    expect(flags.chapter9_edrea_surrendered).toBe(true);
  });

  it("祖父を救出するとメインストーリーをクリアし、裏ボスへの道が開く（C-020）", () => {
    const flags: Flags = { chapter9_yugami_defeated: true, chapter9_edrea_surrendered: true };
    const texts = runScripted(grandfather().commands, flags).join("");
    expect(flags.chapter9_grandfather_rescued).toBe(true);
    expect(flags.chapter9_cleared).toBe(true);
    expect(flags.chapter9_secret_open).toBe(true);
    expect(texts).toContain("まだ、何かが眠っておる");
  });
});
