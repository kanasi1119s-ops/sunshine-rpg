import { describe, expect, it } from "vitest";
import { CHAPTER0_MAPS, CHAPTER0_NPCS, CHAPTER0_OPENING_COMMANDS, CHAPTER0_START } from "./chapter0-world";
import { collectBattleIds, collectReferencedFlags, collectSetFlags, collectWarpTargets } from "../event/inspect";
import { createTileMap, isWalkable } from "../map/tile-map";
import { createEventRunner } from "../event/event-runner";
import type { Flags } from "../event/types";

function retoNpc() {
  const reto = CHAPTER0_NPCS["touri-branch"]?.find((npc) => npc.id === "touri-reto");
  if (!reto) {
    throw new Error("touri-reto が見つからない");
  }
  return reto;
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

const KNOWN_BATTLE_IDS = new Set(["chapter0-yugami"]);

/** イベントスクリプトのsetFlagではなく、main.ts側（戦闘勝利など）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["chapter0_yugami_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER0_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

describe("序章のイベントデータの整合性", () => {
  it("開始地点のマップが実在し、通行可能なタイルに立つ", () => {
    const map = createTileMap(CHAPTER0_MAPS[CHAPTER0_START.mapId]);
    expect(map).toBeDefined();
    expect(isWalkable(map, CHAPTER0_START.tileX, CHAPTER0_START.tileY)).toBe(true);
  });

  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER0_NPCS)) {
      const data = CHAPTER0_MAPS[mapId];
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
    const allCommands = [...CHAPTER0_OPENING_COMMANDS, ...allNpcCommands()];
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
      expect(CHAPTER0_MAPS[mapId], `${mapId} という地図が存在しない`).toBeDefined();
    }
  });

  it("startBattleコマンドが指す戦闘IDは、main.ts側に登録されているものと一致する", () => {
    const battleIds = collectBattleIds(allNpcCommands());
    for (const battleId of battleIds) {
      expect(KNOWN_BATTLE_IDS.has(battleId), `${battleId} という戦闘データが登録されていない`).toBe(true);
    }
  });
});

describe("序章の推理パート（レトとのやり取り）", () => {
  it("手がかり（C-001）を見つける前は、推理クイズを出さずに調査を促す", () => {
    const flags: Flags = { chapter0_yugami_defeated: true };
    const texts = runScripted(retoNpc().commands, flags);
    expect(texts.join("")).toContain("もう一度見ておいで");
    expect(flags.chapter0_reto_joined).toBeUndefined();
  });

  it("手がかりを見つけた後、正解を選ぶとレトに褒められ、そのまま仲間になる", () => {
    const flags: Flags = { chapter0_yugami_defeated: true, chapter0_clue_c001_found: true };
    const texts = runScripted(retoNpc().commands, flags, [0]);
    expect(flags.chapter0_reasoning_correct).toBe(true);
    expect(texts.join("")).toContain("その通りだと思う");
    expect(flags.chapter0_reto_joined).toBe(true);
  });

  it("不正解を選んでも、手がかりを振り返るヒントが出たうえで、そのまま仲間になる（進行は止まらない）", () => {
    const flags: Flags = { chapter0_yugami_defeated: true, chapter0_clue_c001_found: true };
    const texts = runScripted(retoNpc().commands, flags, [1]);
    expect(flags.chapter0_reasoning_correct).toBe(false);
    expect(texts.join("")).toContain("惜しいな");
    expect(flags.chapter0_reto_joined).toBe(true);
  });

  it("すでに仲間になっていれば、クイズを繰り返さない", () => {
    const flags: Flags = {
      chapter0_yugami_defeated: true,
      chapter0_clue_c001_found: true,
      chapter0_reto_joined: true,
    };
    const texts = runScripted(retoNpc().commands, flags);
    expect(texts.join("")).not.toContain("せっかくだから");
  });
});
