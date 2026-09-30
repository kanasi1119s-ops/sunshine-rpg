import { describe, expect, it } from "vitest";
import { WORLD_MAPS } from "./world";
import { CHAPTER8_MAPS, CHAPTER8_NPCS, CHAPTER8_OPENING_COMMANDS } from "./chapter8-world";
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

const KNOWN_BATTLE_IDS = new Set(["toushin-yugami"]);

/** main.ts側（戦闘勝利）で立てられるフラグと、前の章で立つフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set([
  "chapter8_yugami_defeated", "chapter7_ledger_found", "chapter5_record_found",
]);

function allNpcCommands() {
  return Object.values(CHAPTER8_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

function npcById(mapId: string, id: string) {
  const npc = CHAPTER8_NPCS[mapId]?.find((n) => n.id === id);
  if (!npc) {
    throw new Error(`${id} が見つからない`);
  }
  return npc;
}

const clerk = () => npcById("toushin-town", "toushin-clerk");
const chair = () => npcById("toushin-hall", "toushin-chair");
const edrea = () => npcById("toushin-hall", "toushin-edrea");

describe("第8章のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER8_NPCS)) {
      const map = createTileMap(CHAPTER8_MAPS[mapId]);
      for (const npc of npcs) {
        expect(isWalkable(map, npc.tileX, npc.tileY), `${mapId} の ${npc.id} が通行不可タイルにある`).toBe(true);
      }
    }
  });

  it("参照するフラグは、どこかのsetFlagで立てられている", () => {
    const all = [...CHAPTER8_OPENING_COMMANDS, ...allNpcCommands()];
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

describe("第8章の審問・エドレアの告白・章の引き", () => {
  it("議事官の依頼を受けると受注フラグが立つ。断ると立たない", () => {
    const a: Flags = {};
    runScripted(clerk().commands, a, [0]);
    expect(a.chapter8_quest_accepted).toBe(true);
    const b: Flags = {};
    runScripted(clerk().commands, b, [1]);
    expect(b.chapter8_quest_accepted).toBeUndefined();
  });

  it("依頼を受ける前は、議長は審問を始めない", () => {
    const flags: Flags = {};
    runScripted(chair().commands, flags);
    expect(flags.chapter8_hearing_done).toBeUndefined();
  });

  it("手がかりを持って正しい証拠を示すと、推理が2問とも成功する（正解の並びは2番目）", () => {
    const flags: Flags = { chapter8_quest_accepted: true, chapter7_ledger_found: true, chapter5_record_found: true };
    runScripted(chair().commands, flags, [1, 1]);
    expect(flags.chapter8_q1_ok).toBe(true);
    expect(flags.chapter8_q2_ok).toBe(true);
    expect(flags.chapter8_quiz_perfect).toBe(true);
    expect(flags.chapter8_hearing_done).toBe(true);
  });

  it("手がかりが無ければ正解を選んでも成功にならない。間違えても審問は進む（フェアプレイ）", () => {
    const flags: Flags = { chapter8_quest_accepted: true };
    runScripted(chair().commands, flags, [1, 1]);
    expect(flags.chapter8_q1_ok).toBeUndefined();
    expect(flags.chapter8_quiz_perfect).toBeUndefined();
    expect(flags.chapter8_hearing_done).toBe(true);
  });

  it("審問の前は、エドレアは戦いにならない。審問のあとは正体と動機を認め、番人戦につながる（C-016）", () => {
    const before: Flags = {};
    runScripted(edrea().commands, before);
    expect(before.chapter8_edrea_revealed).toBeUndefined();
    const after: Flags = { chapter8_hearing_done: true };
    const texts = runScripted(edrea().commands, after).join("");
    expect(after.chapter8_edrea_revealed).toBe(true);
    expect(texts).toContain("平和");
    expect(collectBattleIds(edrea().commands)).toEqual(new Set(["toushin-yugami"]));
  });

  it("番人を倒すとエドレアが虚灯宮へ去り、報告で終章への道が開く。逃亡の前に報告しても開かない", () => {
    const early: Flags = { chapter8_yugami_defeated: true };
    runScripted(chair().commands, early);
    expect(early.chapter8_kyotoukyu_open).toBeUndefined();
    const flags: Flags = { chapter8_yugami_defeated: true, chapter8_hearing_done: true };
    const texts = runScripted(edrea().commands, flags).join("");
    expect(texts).toContain("虚灯宮");
    expect(flags.chapter8_edrea_fled).toBe(true);
    runScripted(chair().commands, flags);
    expect(flags.chapter8_reported).toBe(true);
    expect(flags.chapter8_kyotoukyu_open).toBe(true);
  });
});
