import { describe, expect, it } from "vitest";
import { CHAPTER5_MAPS, CHAPTER5_NPCS, CHAPTER5_OPENING_COMMANDS } from "./chapter5-world";
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

const KNOWN_BATTLE_IDS = new Set(["chapter0-yugami", "mugikano-yugami", "garasuko-yugami", "tetsukusari-yugami", "sanone-yugami", "kiri-yugami"]);

/** main.ts側（戦闘勝利）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["chapter5_yugami_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER5_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

function npcById(mapId: string, id: string) {
  const npc = CHAPTER5_NPCS[mapId]?.find((n) => n.id === id);
  if (!npc) {
    throw new Error(`${id} が見つからない`);
  }
  return npc;
}

const priest = () => npcById("kiri-town", "kiri-priest");

describe("第5章のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER5_NPCS)) {
      const data = CHAPTER5_MAPS[mapId];
      expect(data, `${mapId} という地図が存在しない`).toBeDefined();
      const map = createTileMap(data);
      for (const npc of npcs) {
        expect(isWalkable(map, npc.tileX, npc.tileY), `${mapId} の ${npc.id} が通行不可タイルにある`).toBe(true);
      }
    }
  });

  it("会話・オープニングが参照するフラグは、どこかのsetFlagで立てられている", () => {
    const allCommands = [...CHAPTER5_OPENING_COMMANDS, ...allNpcCommands()];
    const setFlags = collectSetFlags(allCommands);
    for (const flag of collectReferencedFlags(allCommands)) {
      if (EXTERNALLY_SET_FLAGS.has(flag)) {
        continue;
      }
      expect(setFlags.has(flag), `フラグ "${flag}" がどこにも setFlag されていない`).toBe(true);
    }
  });

  it("warpの移動先は実在し、startBattleの戦闘IDは登録済み", () => {
    for (const mapId of collectWarpTargets(allNpcCommands())) {
      expect(CHAPTER5_MAPS[mapId], `${mapId} が存在しない`).toBeDefined();
    }
    for (const battleId of collectBattleIds(allNpcCommands())) {
      expect(KNOWN_BATTLE_IDS.has(battleId)).toBe(true);
    }
  });
});

describe("第5章の依頼と調査", () => {
  it("司祭の依頼を受けると受注フラグが立つ。「少し考えます」では立たない", () => {
    const a: Flags = {};
    runScripted(priest().commands, a, [0]);
    expect(a.chapter5_quest_accepted).toBe(true);
    const b: Flags = {};
    runScripted(priest().commands, b, [1]);
    expect(b.chapter5_quest_accepted).toBeUndefined();
  });

  it("碑文の写しを調べると、要人の失踪記録の改ざんが分かる（C-010）", () => {
    const flags: Flags = {};
    const texts = runScripted(npcById("kiri-archive", "kiri-record").commands, flags).join("");
    expect(flags.chapter5_record_found).toBe(true);
    expect(texts).toContain("行方を絶つ");
  });

  it("原本の綴りは、碑文の写しを調べた後でないと見つからない。見つけると祖父の名が分かる（C-011）", () => {
    const ledger = npcById("kiri-archive", "kiri-ledger");
    const before: Flags = {};
    runScripted(ledger.commands, before);
    expect(before.chapter5_ledger_found).toBeUndefined();
    const after: Flags = { chapter5_record_found: true };
    const texts = runScripted(ledger.commands, after).join("");
    expect(after.chapter5_ledger_found).toBe(true);
    expect(texts).toContain("ソウイチ");
  });

  it("写字官は原本を見つける前は戦いにならず、見つけた後は戦闘「予言の歪み」につながる", () => {
    const keeper = npcById("kiri-archive", "kiri-keeper");
    const before: Flags = {};
    runScripted(keeper.commands, before);
    expect(before.chapter5_keeper_met).toBeUndefined();
    const after: Flags = { chapter5_ledger_found: true };
    runScripted(keeper.commands, after);
    expect(after.chapter5_keeper_met).toBe(true);
    expect(collectBattleIds(keeper.commands)).toEqual(new Set(["kiri-yugami"]));
  });
});

describe("第5章の報告と章の引き", () => {
  it("ボスを倒す前に報告しても、章は進まない", () => {
    const flags: Flags = { chapter5_quest_accepted: true };
    runScripted(priest().commands, flags);
    expect(flags.chapter5_reported).toBeUndefined();
  });

  it("ボスを倒した後の報告で、祖父の名が記録にあったことが語られ、章が完了する", () => {
    const flags: Flags = { chapter5_quest_accepted: true, chapter5_yugami_defeated: true };
    const texts = runScripted(priest().commands, flags).join("");
    expect(flags.chapter5_reported).toBe(true);
    expect(texts).toContain("祖父");
  });
});
