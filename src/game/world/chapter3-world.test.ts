import { describe, expect, it } from "vitest";
import { CHAPTER3_MAPS, CHAPTER3_NPCS, CHAPTER3_OPENING_COMMANDS } from "./chapter3-world";
import { collectBattleIds, collectReferencedFlags, collectSetFlags, collectWarpTargets } from "../event/inspect";
import { createTileMap, isWalkable } from "../map/tile-map";
import { createEventRunner } from "../event/event-runner";
import type { Flags } from "../event/types";

function orcaNpc() {
  const orca = CHAPTER3_NPCS["tetsukusari-town"]?.find((npc) => npc.id === "tetsukusari-orca");
  if (!orca) {
    throw new Error("tetsukusari-orca が見つからない");
  }
  return orca;
}

function dorunNpc() {
  const dorun = CHAPTER3_NPCS["tetsukusari-mine"]?.find((npc) => npc.id === "tetsukusari-dorun");
  if (!dorun) {
    throw new Error("tetsukusari-dorun が見つからない");
  }
  return dorun;
}

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

/** イベントスクリプトのsetFlagではなく、main.ts側（戦闘勝利など）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["chapter3_yugami_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER3_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

describe("第3章のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER3_NPCS)) {
      const data = CHAPTER3_MAPS[mapId];
      expect(data, `${mapId} という地図が存在しない`).toBeDefined();
      const map = createTileMap(data);
      for (const npc of npcs) {
        expect(isWalkable(map, npc.tileX, npc.tileY), `${mapId} の ${npc.id} が通行不可タイルにある`).toBe(true);
      }
    }
  });

  it("会話・オープニングが参照するフラグは、どこかのsetFlagで立てられている", () => {
    const allCommands = [...CHAPTER3_OPENING_COMMANDS, ...allNpcCommands()];
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
      expect(CHAPTER3_MAPS[mapId], `${mapId} が存在しない`).toBeDefined();
    }
    for (const battleId of collectBattleIds(allNpcCommands())) {
      expect(KNOWN_BATTLE_IDS.has(battleId)).toBe(true);
    }
  });
});

function npcById(mapId: string, id: string) {
  const npc = CHAPTER3_NPCS[mapId]?.find((n) => n.id === id);
  if (!npc) {
    throw new Error(`${id} が見つからない`);
  }
  return npc;
}

describe("第3章・オルカとのやり取り", () => {
  it("依頼を受けると、受注フラグが立つ", () => {
    const flags: Flags = {};
    const texts = runScripted(orcaNpc().commands, flags, [0]);
    expect(flags.chapter3_quest_accepted).toBe(true);
    expect(texts.join("")).toContain("坑道");
  });

  it("討伐後に報告して「一緒に来てほしい」を選ぶと、仲間になる", () => {
    const flags: Flags = { chapter3_yugami_defeated: true };
    runScripted(orcaNpc().commands, flags, [0]);
    expect(flags.chapter3_reported_to_orca).toBe(true);
    expect(flags.chapter3_orca_joined).toBe(true);
  });

  it("町を優先してほしいを選ぶと、まだ仲間にならない", () => {
    const flags: Flags = { chapter3_yugami_defeated: true };
    runScripted(orcaNpc().commands, flags, [1]);
    expect(flags.chapter3_orca_joined).toBeUndefined();
  });

  it("報告済みの再訪問で、落盤の事故を匂わせる会話が一度だけ出る", () => {
    const flags: Flags = { chapter3_yugami_defeated: true, chapter3_reported_to_orca: true };
    expect(runScripted(orcaNpc().commands, flags).join("")).toContain("落盤");
    expect(flags.chapter3_orca_hint_seen).toBe(true);
    expect(runScripted(orcaNpc().commands, flags).join("")).not.toContain("落盤");
  });
});

describe("第3章・鉱山の調査と伏線", () => {
  it("装置を調べるとC-006（人為的な実験の確定）が立つ", () => {
    const flags: Flags = {};
    runScripted(npcById("tetsukusari-mine", "tetsukusari-machine").commands, flags);
    expect(flags.chapter3_machine_found).toBe(true);
  });

  it("ドルンと対峙すると戦闘が始まる（テキストに労働争議の目くらましが含まれる）", () => {
    const texts = runScripted(dorunNpc().commands, {});
    expect(texts.join("")).toContain("煙幕");
  });

  it("討伐前は指示書（C-007）が見つからず、討伐後に「静まりの年」が見つかる", () => {
    const machine = npcById("tetsukusari-mine", "tetsukusari-machine");
    const before: Flags = {};
    runScripted(machine.commands, before);
    expect(before.chapter3_clue_c007_found).toBeUndefined();

    const after: Flags = { chapter3_yugami_defeated: true };
    const texts = runScripted(machine.commands, after);
    expect(after.chapter3_clue_c007_found).toBe(true);
    expect(texts.join("")).toContain("静まりの年");
  });
});
