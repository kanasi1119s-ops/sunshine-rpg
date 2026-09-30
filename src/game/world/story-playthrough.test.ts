import { describe, expect, it } from "vitest";
import { WORLD_NPCS } from "./world";
import { createEventRunner } from "../event/event-runner";
import type { Flags } from "../event/types";

/**
 * 序章〜終章の自動通しプレイ。各章のNPCを、プレイヤーが話しかける順（章の順、依頼→調査→ボス→報告）に
 * 何周か回し、選択肢は「引き受ける・仲間にする」側（0番目）を選ぶ。ボス戦は勝ったものとして勝利フラグを立てる。
 * 進行不能（必要なフラグが立たない・行き止まり）がないか、伏線の前後関係が守られているかを確かめる。
 */
const BATTLE_VICTORY_FLAG: Record<string, string> = {
  "chapter0-yugami": "chapter0_yugami_defeated",
  "mugikano-yugami": "chapter1_yugami_defeated",
  "garasuko-yugami": "chapter2_yugami_defeated",
  "tetsukusari-yugami": "chapter3_yugami_defeated",
  "sanone-yugami": "chapter4_yugami_defeated",
  "kiri-yugami": "chapter5_yugami_defeated",
  "shimohara-yugami": "chapter6_yugami_defeated",
  "fushima-yugami": "chapter7_yugami_defeated",
  "toushin-yugami": "chapter8_yugami_defeated",
  "kyotoukyu-yugami": "chapter9_yugami_defeated",
  "deep3-yugami": "deep3_yugami_defeated",
  "deep-yugami": "deep_yugami_defeated",
  ...Object.fromEntries(Array.from({ length: 8 }, (_, i) => [`god-${i + 1}`, `god${i + 1}_defeated`])),
};

const CHAPTER_MAPS: string[][] = [
  ["touri-town", "touri-branch", "touri-outskirts"],
  ["mugikano-village", "mugikano-water-source"],
  ["garasuko-town", "garasuko-warehouse"],
  ["tetsukusari-town", "tetsukusari-mine"],
  ["sanone-town", "sanone-camp"],
  ["kiri-town", "kiri-archive"],
  ["shimohara-town", "shimohara-facility"],
  ["fushima-town", "fushima-base"],
  ["toushin-town", "toushin-hall"],
  ["kyotoukyu-court", "kyotoukyu-corridor", "kyotoukyu-sanctum"],
  ["deep-1", "deep-2", "deep-3", "deep-4"],
  ...Array.from({ length: 8 }, (_, i) => [`god-shrine-${i + 1}`]),
];

function recordingFlags(order: string[]): Flags {
  return new Proxy({} as Flags, {
    set(target, key: string, value: boolean) {
      if (value && !target[key]) {
        order.push(key);
      }
      target[key] = value;
      return true;
    },
  });
}

function playAllNpcs(mapIds: string[], flags: Flags): void {
  const npcs = mapIds.flatMap((id) => WORLD_NPCS[id] ?? []);
  for (let pass = 0; pass < 12; pass++) {
    for (const npc of npcs) {
      const runner = createEventRunner(npc.commands, flags, {
        onStartBattle: (battleId) => {
          const victory = BATTLE_VICTORY_FLAG[battleId];
          expect(victory, `戦闘ID ${battleId} の勝利フラグが未登録`).toBeDefined();
          flags[victory] = true;
        },
      });
      let result = runner.next();
      let guard = 0;
      while (!result.done && guard++ < 500) {
        result = runner.next(result.step?.kind === "choice" ? { kind: "choose", index: 0 } : { kind: "advance" });
      }
    }
  }
}

describe("序章〜終章の自動通しプレイ", () => {
  const order: string[] = [];
  const flags = recordingFlags(order);
  CHAPTER_MAPS.forEach((maps) => playAllNpcs(maps, flags));

  it("各章のボスに勝てて、仲間が順に加わる", () => {
    for (const flag of [
      "chapter0_yugami_defeated", "chapter0_reto_joined",
      "chapter1_yugami_defeated", "chapter1_mina_joined",
      "chapter2_yugami_defeated", "chapter2_guide_joined",
      "chapter3_yugami_defeated", "chapter3_orca_joined",
      "chapter4_yugami_defeated",
      "chapter5_yugami_defeated",
      "chapter6_yugami_defeated", "chapter6_ayame_joined",
      "chapter7_yugami_defeated", "chapter7_airship_obtained",
      "chapter8_yugami_defeated", "chapter8_kyotoukyu_open",
      "chapter9_yugami_defeated", "chapter9_grandfather_rescued", "chapter9_cleared", "chapter9_secret_open",
    ]) {
      expect(flags[flag], `${flag} が立たない（進行不能の疑い）`).toBe(true);
    }
  });

  it("章の依頼は、その章のボス戦より先に受けている", () => {
    for (const n of [0, 1, 2, 3, 4, 5, 6, 7, 8]) {
      const accepted = order.indexOf(`chapter${n}_quest_accepted`);
      const defeated = order.indexOf(`chapter${n}_yugami_defeated`);
      expect(accepted, `chapter${n}_quest_accepted`).toBeGreaterThanOrEqual(0);
      expect(accepted, `第${n}章の依頼受注がボス撃破より後`).toBeLessThan(defeated);
    }
  });

  it("伏線の前後関係: 第3章の装置の発見（C-006）が、指示書の発見（C-007）より先", () => {
    expect(order.indexOf("chapter3_machine_found")).toBeGreaterThanOrEqual(0);
    expect(order.indexOf("chapter3_machine_found")).toBeLessThan(order.indexOf("chapter3_clue_c007_found"));
  });

  it("伏線の前後関係: 各章の手がかりは、その章のボス撃破より前か、撃破後の調査で得られる", () => {
    for (const flag of ["chapter0_clue_c001_found", "chapter1_clue_c002_found", "chapter2_clue_c003_found", "chapter2_clue_c004_found", "chapter3_clue_c007_found"]) {
      expect(flags[flag], `${flag} が得られない`).toBe(true);
    }
  });

  it("第4章: ガイドの潔白（C-005の回収）と、エドレアの使者による章の引きに進める", () => {
    expect(flags["chapter4_guide_cleared"]).toBe(true);
    expect(flags["chapter4_rumor_heard"]).toBe(true);
    expect(flags["chapter4_sailcar_obtained"]).toBe(true);
  });
});

describe("第5章の伏線", () => {
  const order: string[] = [];
  const flags = recordingFlags(order);
  CHAPTER_MAPS.forEach((maps) => playAllNpcs(maps, flags));

  it("改ざんの発見（C-010）が、祖父の名の発見（C-011）より先で、どちらもボス撃破・報告までに得られる", () => {
    expect(order.indexOf("chapter5_record_found")).toBeGreaterThanOrEqual(0);
    expect(order.indexOf("chapter5_record_found")).toBeLessThan(order.indexOf("chapter5_ledger_found"));
    expect(order.indexOf("chapter5_ledger_found")).toBeLessThan(order.indexOf("chapter5_yugami_defeated"));
    expect(flags["chapter5_reported"]).toBe(true);
  });
});

describe("第6章の伏線", () => {
  const order: string[] = [];
  const flags = recordingFlags(order);
  CHAPTER_MAPS.forEach((maps) => playAllNpcs(maps, flags));

  it("運用記録の発見が、ドルンとの戦闘より先。ドルンの捨て台詞（C-013）と報告、アヤメの加入が順に進む", () => {
    expect(order.indexOf("chapter6_log_found")).toBeGreaterThanOrEqual(0);
    expect(order.indexOf("chapter6_log_found")).toBeLessThan(order.indexOf("chapter6_yugami_defeated"));
    expect(flags["chapter6_dorun_farewell"]).toBe(true);
    expect(order.indexOf("chapter6_reported")).toBeLessThan(order.indexOf("chapter6_ayame_joined"));
  });
});

describe("第7章の伏線", () => {
  const order: string[] = [];
  const flags = recordingFlags(order);
  CHAPTER_MAPS.forEach((maps) => playAllNpcs(maps, flags));

  it("帳簿の発見（C-014）が、ボス戦より先。エドレアの登場（C-015）のあとに報告と空の乗り物が進む", () => {
    expect(order.indexOf("chapter7_ledger_found")).toBeGreaterThanOrEqual(0);
    expect(order.indexOf("chapter7_ledger_found")).toBeLessThan(order.indexOf("chapter7_yugami_defeated"));
    expect(order.indexOf("chapter7_edrea_appeared")).toBeLessThan(order.indexOf("chapter7_reported"));
    expect(flags["chapter7_airship_obtained"]).toBe(true);
  });
});

describe("第8章の伏線", () => {
  const order: string[] = [];
  const flags = recordingFlags(order);
  CHAPTER_MAPS.forEach((maps) => playAllNpcs(maps, flags));

  it("審問→エドレアの告白→番人戦→逃亡（C-016）→報告の順に進み、虚灯宮への道が開く", () => {
    expect(order.indexOf("chapter8_hearing_done")).toBeLessThan(order.indexOf("chapter8_edrea_revealed"));
    expect(order.indexOf("chapter8_edrea_revealed")).toBeLessThan(order.indexOf("chapter8_yugami_defeated"));
    expect(order.indexOf("chapter8_yugami_defeated")).toBeLessThan(order.indexOf("chapter8_edrea_fled"));
    expect(order.indexOf("chapter8_edrea_fled")).toBeLessThan(order.indexOf("chapter8_reported"));
    expect(flags["chapter8_kyotoukyu_open"]).toBe(true);
  });
});

describe("終章の伏線", () => {
  const order: string[] = [];
  const flags = recordingFlags(order);
  CHAPTER_MAPS.forEach((maps) => playAllNpcs(maps, flags));

  it("壁画で真相がつながる→最終決戦→エドレアの投降→祖父の救出（C-017）→クリア、の順に進む", () => {
    expect(order.indexOf("chapter9_truth_known")).toBeGreaterThanOrEqual(0);
    expect(order.indexOf("chapter9_edrea_told")).toBeLessThan(order.indexOf("chapter9_yugami_defeated"));
    expect(order.indexOf("chapter9_yugami_defeated")).toBeLessThan(order.indexOf("chapter9_edrea_surrendered"));
    expect(order.indexOf("chapter9_edrea_surrendered")).toBeLessThan(order.indexOf("chapter9_grandfather_rescued"));
    expect(order.indexOf("chapter9_grandfather_rescued")).toBeLessThan(order.indexOf("chapter9_cleared"));
  });
});

describe("クリア後（サブストーリー・虚灯宮・深部）", () => {
  const order: string[] = [];
  const flags = recordingFlags(order);
  // 各章の「到着したときの場面つなぎ」（main.tsが流す）で立つフラグは、ここでは到着したものとして先に立てる。
  for (let n = 0; n <= 9; n++) {
    flags[`chapter${n}_intro_seen`] = true;
  }
  CHAPTER_MAPS.forEach((maps) => playAllNpcs(maps, flags));
  // 本編クリア後に、もう一度すべての地図を回る（サブストーリーの解放条件が、章の順ではそろわないものがあるため）。
  playAllNpcs(CHAPTER_MAPS.flat(), flags);
  playAllNpcs(CHAPTER_MAPS.flat(), flags);

  it("S-027→S-028で深部への階段が開き、4階層の仕掛けと裏ボスを越えて、転移陣の刻印まで進める", () => {
    for (const flag of [
      "side_s027_done", "side_s028_done",
      "deep1_lit", "deep2_lit", "deep3_lit", "deep3_yugami_defeated", "deep4_lit",
      "deep_yugami_defeated", "deep_cleared",
      ...Array.from({ length: 8 }, (_, i) => `god${i + 1}_fragment`),
      "tower_gate_open",
    ]) {
      expect(flags[flag], `${flag} が立たない（進行不能の疑い）`).toBe(true);
    }
  });

  it("すべてのサブストーリーが完了できる", () => {
    for (const flag of Object.keys(flags).filter((f) => /^side_s\d+_accepted$/.test(f))) {
      expect(flags[flag.replace("_accepted", "_done")], `${flag} のあとに完了しない`).toBe(true);
    }
    const doneKeys = Object.keys(flags).filter((f) => /^side_s\d+_done$/.test(f));
    expect(doneKeys.length, `完了 ${doneKeys.join(",")}`).toBe(32);
  });
});

describe("NPCの登録", () => {
  it("全マップでNPCのidが重複しない", () => {
    const ids = Object.values(WORLD_NPCS).flatMap((npcs) => npcs.map((n) => n.id));
    expect(new Set(ids).size).toBe(ids.length);
  });
});
