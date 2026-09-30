import { describe, expect, it } from "vitest";
import { CHAPTER7_MAPS, CHAPTER7_NPCS, CHAPTER7_OPENING_COMMANDS } from "./chapter7-world";
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

const KNOWN_BATTLE_IDS = new Set(["fushima-yugami"]);

/** main.ts側（戦闘勝利）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["chapter7_yugami_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER7_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

function npcById(mapId: string, id: string) {
  const npc = CHAPTER7_NPCS[mapId]?.find((n) => n.id === id);
  if (!npc) {
    throw new Error(`${id} が見つからない`);
  }
  return npc;
}


const elder = () => npcById("fushima-town", "fushima-elder");
const ledger = () => npcById("fushima-base", "fushima-ledger");
const konsole = () => npcById("fushima-base", "fushima-console");
const edrea = () => npcById("fushima-base", "fushima-edrea");

describe("第7章のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER7_NPCS)) {
      const map = createTileMap(CHAPTER7_MAPS[mapId]);
      for (const npc of npcs) {
        expect(isWalkable(map, npc.tileX, npc.tileY), `${mapId} の ${npc.id} が通行不可タイルにある`).toBe(true);
      }
    }
  });

  it("参照するフラグは、どこかのsetFlagで立てられている", () => {
    const all = [...CHAPTER7_OPENING_COMMANDS, ...allNpcCommands()];
    const setFlags = collectSetFlags(all);
    for (const flag of collectReferencedFlags(all)) {
      if (!EXTERNALLY_SET_FLAGS.has(flag)) {
        expect(setFlags.has(flag), `フラグ "${flag}" がどこにも setFlag されていない`).toBe(true);
      }
    }
  });

  it("warpの移動先は実在し、startBattleの戦闘IDは登録済み", () => {
    for (const mapId of collectWarpTargets(allNpcCommands())) {
      expect(CHAPTER7_MAPS[mapId]).toBeDefined();
    }
    for (const battleId of collectBattleIds(allNpcCommands())) {
      expect(KNOWN_BATTLE_IDS.has(battleId)).toBe(true);
    }
  });
});

describe("第7章の依頼・拠点調査・章の引き", () => {
  it("長老の依頼を受けると受注フラグが立つ。「少し考えます」では立たない", () => {
    const a: Flags = {};
    runScripted(elder().commands, a, [0]);
    expect(a.chapter7_quest_accepted).toBe(true);
    const b: Flags = {};
    runScripted(elder().commands, b, [1]);
    expect(b.chapter7_quest_accepted).toBeUndefined();
  });

  it("帳簿で、各地の事件が計画されていたと分かる（C-014）", () => {
    const flags: Flags = {};
    const texts = runScripted(ledger().commands, flags).join("");
    expect(flags.chapter7_ledger_found).toBe(true);
    expect(texts).toContain("計画");
  });

  it("監視卓は帳簿を調べる前は戦いにならず、調べた後は戦闘「監視卓の歪み」につながる", () => {
    const before: Flags = {};
    runScripted(konsole().commands, before);
    expect(before.chapter7_console_found).toBeUndefined();
    const after: Flags = { chapter7_ledger_found: true };
    runScripted(konsole().commands, after);
    expect(after.chapter7_console_found).toBe(true);
    expect(collectBattleIds(konsole().commands)).toEqual(new Set(["fushima-yugami"]));
  });

  it("ボスを倒すと、エドレアが姿を見せ、灯芯都で待つと告げる（C-015）", () => {
    const flags: Flags = { chapter7_yugami_defeated: true };
    const texts = runScripted(edrea().commands, flags).join("");
    expect(texts).toContain("灯芯都");
    expect(flags.chapter7_edrea_appeared).toBe(true);
  });

  it("エドレアと会う前に報告しても章は進まない。会った後は報告でき、空の乗り物を得る", () => {
    const early: Flags = { chapter7_quest_accepted: true };
    runScripted(elder().commands, early);
    expect(early.chapter7_reported).toBeUndefined();
    const flags: Flags = { chapter7_quest_accepted: true, chapter7_edrea_appeared: true };
    runScripted(elder().commands, flags);
    expect(flags.chapter7_reported).toBe(true);
    expect(flags.chapter7_airship_obtained).toBe(true);
  });
});
