import { describe, expect, it } from "vitest";
import { CHAPTER1_MAPS, CHAPTER1_NPCS, CHAPTER1_OPENING_COMMANDS } from "./chapter1-world";
import { collectBattleIds, collectReferencedFlags, collectSetFlags, collectWarpTargets } from "../event/inspect";
import { createTileMap, isWalkable } from "../map/tile-map";
import { createEventRunner } from "../event/event-runner";
import type { Flags } from "../event/types";

function elderNpc() {
  const elder = CHAPTER1_NPCS["mugikano-village"]?.find((npc) => npc.id === "mugikano-elder");
  if (!elder) {
    throw new Error("mugikano-elder が見つからない");
  }
  return elder;
}

function minaNpc() {
  const mina = CHAPTER1_NPCS["mugikano-village"]?.find((npc) => npc.id === "mugikano-mina");
  if (!mina) {
    throw new Error("mugikano-mina が見つからない");
  }
  return mina;
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

const KNOWN_BATTLE_IDS = new Set(["chapter0-yugami", "mugikano-yugami"]);

/** イベントスクリプトのsetFlagではなく、main.ts側（戦闘勝利など）で立てられるフラグ。 */
const EXTERNALLY_SET_FLAGS = new Set(["chapter1_yugami_defeated"]);

function allNpcCommands() {
  return Object.values(CHAPTER1_NPCS).flatMap((npcs) => npcs.flatMap((npc) => npc.commands));
}

describe("第1章のイベントデータの整合性", () => {
  it("NPCはすべて実在するマップの、通行可能なタイルに置かれている", () => {
    for (const [mapId, npcs] of Object.entries(CHAPTER1_NPCS)) {
      const data = CHAPTER1_MAPS[mapId];
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
    const allCommands = [...CHAPTER1_OPENING_COMMANDS, ...allNpcCommands()];
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
      expect(CHAPTER1_MAPS[mapId], `${mapId} という地図が存在しない`).toBeDefined();
    }
  });

  it("startBattleコマンドが指す戦闘IDは、main.ts側に登録されているものと一致する", () => {
    const battleIds = collectBattleIds(allNpcCommands());
    for (const battleId of battleIds) {
      expect(KNOWN_BATTLE_IDS.has(battleId), `${battleId} という戦闘データが登録されていない`).toBe(true);
    }
  });
});

describe("第1章・村長とのやり取り", () => {
  it("依頼を受ける前は、水路の事情を説明して依頼を持ちかける", () => {
    const flags: Flags = {};
    const texts = runScripted(elderNpc().commands, flags, [0]);
    expect(flags.chapter1_quest_accepted).toBe(true);
    expect(texts.join("")).toContain("水源の様子を見てきてほしい");
  });

  it("歪みを倒したあと、採掘跡を見つけていなければ、もう一度見てくるよう促す（報告フラグは立たない）", () => {
    const flags: Flags = { chapter1_yugami_defeated: true };
    runScripted(elderNpc().commands, flags);
    expect(flags.chapter1_reported_to_elder).toBeUndefined();
  });

  it("採掘跡を見つけたあとに報告すると、伏線C-002のフラグが立ち、報告済みになる", () => {
    const flags: Flags = { chapter1_yugami_defeated: true, chapter1_excavation_found: true };
    const texts = runScripted(elderNpc().commands, flags);
    expect(flags.chapter1_clue_c002_found).toBe(true);
    expect(flags.chapter1_reported_to_elder).toBe(true);
    expect(texts.join("")).toContain("採掘跡");
  });
});

describe("第1章・ミナとのやり取り", () => {
  it("報告前は、まだ仲間にならない", () => {
    const flags: Flags = { chapter1_quest_accepted: true };
    runScripted(minaNpc().commands, flags);
    expect(flags.chapter1_mina_joined).toBeUndefined();
  });

  it("報告後に同行を申し出て「一緒に来てください」を選ぶと、仲間になる", () => {
    const flags: Flags = { chapter1_reported_to_elder: true };
    const texts = runScripted(minaNpc().commands, flags, [0]);
    expect(flags.chapter1_mina_joined).toBe(true);
    expect(texts.join("")).toContain("足を引っ張らないよう");
  });

  it("同行を断ると、まだ仲間にならない", () => {
    const flags: Flags = { chapter1_reported_to_elder: true };
    const texts = runScripted(minaNpc().commands, flags, [1]);
    expect(flags.chapter1_mina_joined).toBeUndefined();
    expect(texts.join("")).toContain("気が変わったら");
  });

  it("仲間になった後、最初の会話で幼なじみを匂わせる伏線が一度だけ出る", () => {
    const flags: Flags = { chapter1_reported_to_elder: true, chapter1_mina_joined: true };
    const firstVisit = runScripted(minaNpc().commands, flags);
    expect(flags.chapter1_mina_friend_hint_seen).toBe(true);
    expect(firstVisit.join("")).toContain("表情を曇らせた");

    const secondVisit = runScripted(minaNpc().commands, flags);
    expect(secondVisit.join("")).not.toContain("表情を曇らせた");
  });
});
