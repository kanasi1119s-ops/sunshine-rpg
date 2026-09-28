import { describe, expect, it } from "vitest";
import { CHAPTER2_MAPS, CHAPTER2_NPCS, CHAPTER2_OPENING_COMMANDS } from "./chapter2-world";
import { collectBattleIds, collectReferencedFlags, collectSetFlags, collectWarpTargets } from "../event/inspect";
import { createTileMap, isWalkable } from "../map/tile-map";
import { createEventRunner } from "../event/event-runner";
import type { Flags } from "../event/types";

function guideNpc() {
  const guide = CHAPTER2_NPCS["garasuko-town"]?.find((npc) => npc.id === "garasuko-guide");
  if (!guide) {
    throw new Error("garasuko-guide が見つからない");
  }
  return guide;
}

function dorunNpc() {
  const dorun = CHAPTER2_NPCS["garasuko-warehouse"]?.find((npc) => npc.id === "garasuko-dorun");
  if (!dorun) {
    throw new Error("garasuko-dorun が見つからない");
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

const KNOWN_BATTLE_IDS = new Set(["chapter0-yugami", "mugikano-yugami", "garasuko-yugami"]);

/** イベントスクリプトのsetFlagではなく、main.ts側（戦闘勝利など）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["chapter2_yugami_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER2_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

describe("第2章のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER2_NPCS)) {
      const data = CHAPTER2_MAPS[mapId];
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
    const allCommands = [...CHAPTER2_OPENING_COMMANDS, ...allNpcCommands()];
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
      expect(CHAPTER2_MAPS[mapId], `${mapId} という地図が存在しない`).toBeDefined();
    }
  });

  it("startBattleコマンドが指す戦闘IDは、main.ts側に登録されているものと一致する", () => {
    const battleIds = collectBattleIds(allNpcCommands());
    for (const battleId of battleIds) {
      expect(KNOWN_BATTLE_IDS.has(battleId), `${battleId} という戦闘データが登録されていない`).toBe(true);
    }
  });
});

describe("第2章・ガイドとのやり取り", () => {
  it("依頼を受ける前は、倉庫の調査を持ちかける", () => {
    const flags: Flags = {};
    const texts = runScripted(guideNpc().commands, flags, [0]);
    expect(flags.chapter2_quest_accepted).toBe(true);
    expect(texts.join("")).toContain("桟橋の先の倉庫");
  });

  it("歪みを倒したあと、報告するとC-005の伏線フラグは立たず、報告済みになる", () => {
    const flags: Flags = { chapter2_yugami_defeated: true };
    const texts = runScripted(guideNpc().commands, flags, [0]);
    expect(flags.chapter2_reported_to_guide).toBe(true);
    expect(texts.join("")).toContain("灯り石は片付いた");
  });

  it("一緒に来てほしいを選ぶと、仲間になる", () => {
    const flags: Flags = { chapter2_yugami_defeated: true };
    runScripted(guideNpc().commands, flags, [0]);
    expect(flags.chapter2_guide_joined).toBe(true);
  });

  it("商会優先を選ぶと、まだ仲間にならない", () => {
    const flags: Flags = { chapter2_yugami_defeated: true };
    runScripted(guideNpc().commands, flags, [1]);
    expect(flags.chapter2_guide_joined).toBeUndefined();
  });

  it("報告済みの再訪問で、従兄をめぐる伏線（C-005）の会話が一度だけ出る", () => {
    const flags: Flags = { chapter2_yugami_defeated: true, chapter2_reported_to_guide: true };
    const firstVisit = runScripted(guideNpc().commands, flags);
    expect(flags.chapter2_guide_cousin_hint_seen).toBe(true);
    expect(firstVisit.join("")).toContain("早口だった");

    const secondVisit = runScripted(guideNpc().commands, flags);
    expect(secondVisit.join("")).not.toContain("早口だった");
  });
});

describe("第2章・ドルンとの遭遇", () => {
  it("初対面でC-003・C-004の伏線フラグが立ち、戦闘が始まる", () => {
    const flags: Flags = {};
    const texts = runScripted(dorunNpc().commands, flags);
    expect(flags.chapter2_clue_c003_found).toBe(true);
    expect(flags.chapter2_clue_c004_found).toBe(true);
    expect(texts.join("")).toContain("灯芯都からの依頼でね");
  });

  it("歪みを倒したあとは、静かになったという説明のみになる", () => {
    const flags: Flags = { chapter2_yugami_defeated: true };
    const texts = runScripted(dorunNpc().commands, flags);
    expect(texts.join("")).toContain("静かになった");
    expect(texts.join("")).not.toContain("灯芯都からの依頼でね");
  });
});
