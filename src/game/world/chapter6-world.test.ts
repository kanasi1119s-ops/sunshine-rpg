import { describe, expect, it } from "vitest";
import { CHAPTER6_MAPS, CHAPTER6_NPCS, CHAPTER6_OPENING_COMMANDS } from "./chapter6-world";
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

const KNOWN_BATTLE_IDS = new Set(["shimohara-yugami"]);

/** main.ts側（戦闘勝利）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["chapter6_yugami_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER6_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

function npcById(mapId: string, id: string) {
  const npc = CHAPTER6_NPCS[mapId]?.find((n) => n.id === id);
  if (!npc) {
    throw new Error(`${id} が見つからない`);
  }
  return npc;
}

const watchman = () => npcById("shimohara-town", "shimohara-watchman");
const ayame = () => npcById("shimohara-town", "shimohara-ayame");
const dorun = () => npcById("shimohara-facility", "shimohara-dorun");

describe("第6章のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER6_NPCS)) {
      const data = CHAPTER6_MAPS[mapId];
      expect(data, `${mapId} という地図が存在しない`).toBeDefined();
      const map = createTileMap(data);
      for (const npc of npcs) {
        expect(isWalkable(map, npc.tileX, npc.tileY), `${mapId} の ${npc.id} が通行不可タイルにある`).toBe(true);
      }
    }
  });

  it("会話・オープニングが参照するフラグは、どこかのsetFlagで立てられている", () => {
    const allCommands = [...CHAPTER6_OPENING_COMMANDS, ...allNpcCommands()];
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
      expect(CHAPTER6_MAPS[mapId], `${mapId} が存在しない`).toBeDefined();
    }
    for (const battleId of collectBattleIds(allNpcCommands())) {
      expect(KNOWN_BATTLE_IDS.has(battleId)).toBe(true);
    }
  });
});

describe("第6章の依頼と調査", () => {
  it("番所の依頼を受けると受注フラグが立つ。「少し考えます」では立たない", () => {
    const a: Flags = {};
    runScripted(watchman().commands, a, [0]);
    expect(a.chapter6_quest_accepted).toBe(true);
    const b: Flags = {};
    runScripted(watchman().commands, b, [1]);
    expect(b.chapter6_quest_accepted).toBeUndefined();
  });

  it("アヤメは初対面では観察者のようにふるまう（C-012）", () => {
    const flags: Flags = {};
    const texts = runScripted(ayame().commands, flags).join("");
    expect(flags.chapter6_ayame_met).toBe(true);
    expect(texts).toContain("深入りしません");
  });

  it("運用記録を調べると、歪みが人為的に作られたと分かる", () => {
    const flags: Flags = {};
    const texts = runScripted(npcById("shimohara-facility", "shimohara-log").commands, flags).join("");
    expect(flags.chapter6_log_found).toBe(true);
    expect(texts).toContain("発生装置");
  });

  it("ドルンは記録を調べる前は戦いにならず、調べた後は戦闘「試作機の歪み」につながる", () => {
    const before: Flags = {};
    runScripted(dorun().commands, before);
    expect(before.chapter6_dorun_met).toBeUndefined();
    const after: Flags = { chapter6_log_found: true };
    runScripted(dorun().commands, after);
    expect(after.chapter6_dorun_met).toBe(true);
    expect(collectBattleIds(dorun().commands)).toEqual(new Set(["shimohara-yugami"]));
  });
});

describe("第6章の報告・ドルンの捨て台詞・アヤメの加入", () => {
  it("ボスを倒す前に報告しても、章は進まない", () => {
    const flags: Flags = { chapter6_quest_accepted: true };
    runScripted(watchman().commands, flags);
    expect(flags.chapter6_reported).toBeUndefined();
  });

  it("ボス撃破後、ドルンが「あの方の領分」と言い残して姿を消す（C-013）", () => {
    const flags: Flags = { chapter6_yugami_defeated: true };
    const texts = runScripted(dorun().commands, flags).join("");
    expect(texts).toContain("あの方の領分");
    expect(flags.chapter6_dorun_farewell).toBe(true);
    expect(runScripted(dorun().commands, flags).join("")).not.toContain("あの方の領分");
  });

  it("報告後、アヤメが目的を打ち明け、誘うと仲間になる。断っても後で誘い直せる", () => {
    const flags: Flags = { chapter6_quest_accepted: true, chapter6_yugami_defeated: true };
    runScripted(watchman().commands, flags);
    expect(flags.chapter6_reported).toBe(true);
    runScripted(ayame().commands, flags, [1]);
    expect(flags.chapter6_ayame_joined).toBeUndefined();
    const texts = runScripted(ayame().commands, flags, [0]).join("");
    expect(texts).toContain("静まりの年");
    expect(flags.chapter6_ayame_joined).toBe(true);
  });
});
