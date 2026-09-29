import { describe, expect, it } from "vitest";
import { CHAPTER4_MAPS, CHAPTER4_NPCS, CHAPTER4_OPENING_COMMANDS } from "./chapter4-world";
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

const KNOWN_BATTLE_IDS = new Set(["chapter0-yugami", "mugikano-yugami", "garasuko-yugami", "tetsukusari-yugami"]);

function allNpcCommands() {
  return Object.values(CHAPTER4_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

function npcById(mapId: string, id: string) {
  const npc = CHAPTER4_NPCS[mapId]?.find((n) => n.id === id);
  if (!npc) {
    throw new Error(`${id} が見つからない`);
  }
  return npc;
}

const guild = () => npcById("sanone-town", "sanone-guildmaster");

describe("第4章のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER4_NPCS)) {
      const data = CHAPTER4_MAPS[mapId];
      expect(data, `${mapId} という地図が存在しない`).toBeDefined();
      const map = createTileMap(data);
      for (const npc of npcs) {
        expect(isWalkable(map, npc.tileX, npc.tileY), `${mapId} の ${npc.id} が通行不可タイルにある`).toBe(true);
      }
    }
  });

  it("会話・オープニングが参照するフラグは、どこかのsetFlagで立てられている", () => {
    const allCommands = [...CHAPTER4_OPENING_COMMANDS, ...allNpcCommands()];
    const setFlags = collectSetFlags(allCommands);
    for (const flag of collectReferencedFlags(allCommands)) {
      expect(setFlags.has(flag), `フラグ "${flag}" がどこにも setFlag されていない`).toBe(true);
    }
  });

  it("warpの移動先は実在し、startBattleの戦闘IDは登録済み", () => {
    for (const mapId of collectWarpTargets(allNpcCommands())) {
      expect(CHAPTER4_MAPS[mapId], `${mapId} が存在しない`).toBeDefined();
    }
    for (const battleId of collectBattleIds(allNpcCommands())) {
      expect(KNOWN_BATTLE_IDS.has(battleId)).toBe(true);
    }
  });
});

describe("第4章の依頼と調査", () => {
  it("組合長の依頼を受けると受注フラグが立つ", () => {
    const flags: Flags = {};
    runScripted(guild().commands, flags, [0]);
    expect(flags.chapter4_quest_accepted).toBe(true);
  });

  it("「少し考えます」では受注されない", () => {
    const flags: Flags = {};
    runScripted(guild().commands, flags, [1]);
    expect(flags.chapter4_quest_accepted).toBeUndefined();
  });

  it("荷馬車を調べると帳面の偽の印が見つかる", () => {
    const flags: Flags = {};
    runScripted(npcById("sanone-camp", "sanone-wagon").commands, flags);
    expect(flags.chapter4_wagon_found).toBe(true);
  });

  it("荷馬車を調べる前のドルンは会話にならず、調べた後に「さらに上の方」と語る（C-008）", () => {
    const dorun = npcById("sanone-camp", "sanone-dorun");
    const before: Flags = {};
    runScripted(dorun.commands, before);
    expect(before.chapter4_dorun_met).toBeUndefined();

    const after: Flags = { chapter4_wagon_found: true };
    const texts = runScripted(dorun.commands, after);
    expect(after.chapter4_dorun_met).toBe(true);
    expect(texts.join("")).toContain("さらに上の方");
  });

  it("情報屋から合議会関係者の噂を聞ける（C-008）", () => {
    const flags: Flags = {};
    const texts = runScripted(npcById("sanone-town", "sanone-informant").commands, flags);
    expect(flags.chapter4_rumor_heard).toBe(true);
    expect(texts.join("")).toContain("合議会");
  });
});

describe("第4章の報告と章の引き", () => {
  it("ドルンと会う前に報告しても、章は進まない", () => {
    const flags: Flags = { chapter4_quest_accepted: true };
    runScripted(guild().commands, flags);
    expect(flags.chapter4_reported).toBeUndefined();
    expect(flags.chapter4_guide_cleared).toBeUndefined();
  });

  it("ドルンと会った後の報告で、ガイドの潔白（C-005回収）・帆走車入手・使者の登場まで進む", () => {
    const flags: Flags = { chapter4_quest_accepted: true, chapter4_dorun_met: true };
    const texts = runScripted(guild().commands, flags).join("");
    expect(flags.chapter4_guide_cleared).toBe(true);
    expect(flags.chapter4_sailcar_obtained).toBe(true);
    expect(flags.chapter4_reported).toBe(true);
    expect(texts).toContain("エドレア");
  });

  it("報告後は、繰り返し話しても帆走車の入手が重複しない", () => {
    const flags: Flags = { chapter4_reported: true, chapter4_sailcar_obtained: true };
    const texts = runScripted(guild().commands, flags).join("");
    expect(texts).not.toContain("エドレア");
  });
});
