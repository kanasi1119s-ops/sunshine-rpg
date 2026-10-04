import { describe, expect, it } from "vitest";
import { createEventRunner } from "./event-runner";
import type { EventCommand, Flags } from "./types";

describe("createEventRunner", () => {
  it("メッセージを順番に返し、最後は done になる", () => {
    const commands: EventCommand[] = [
      { type: "message", text: "こんにちは" },
      { type: "message", text: "元気ですか" },
    ];
    const runner = createEventRunner(commands, {});

    const first = runner.next();
    expect(first.done).toBe(false);
    expect(first.step).toEqual({ kind: "message", text: "こんにちは", speaker: undefined });

    const second = runner.next({ kind: "advance" });
    expect(second.step).toEqual({ kind: "message", text: "元気ですか", speaker: undefined });

    const third = runner.next({ kind: "advance" });
    expect(third.done).toBe(true);
  });

  it("選択肢で選んだ方の枝だけを実行する", () => {
    const commands: EventCommand[] = [
      {
        type: "choice",
        text: "どうする？",
        options: [
          { label: "はい", commands: [{ type: "message", text: "はいを選んだ" }] },
          { label: "いいえ", commands: [{ type: "message", text: "いいえを選んだ" }] },
        ],
      },
    ];
    const runner = createEventRunner(commands, {});

    const choiceStep = runner.next();
    expect(choiceStep.step).toEqual({
      kind: "choice",
      text: "どうする？",
      labels: ["はい", "いいえ"],
    });

    const afterChoice = runner.next({ kind: "choose", index: 1 });
    expect(afterChoice.step).toEqual({
      kind: "message",
      text: "いいえを選んだ",
      speaker: undefined,
    });
  });

  it("setFlag と if で分岐する", () => {
    const flags: Flags = {};
    const commands: EventCommand[] = [
      { type: "setFlag", flag: "met_villager", value: true },
      {
        type: "if",
        flag: "met_villager",
        equals: true,
        then: [{ type: "message", text: "また会いましたね" }],
        else: [{ type: "message", text: "はじめまして" }],
      },
    ];
    const runner = createEventRunner(commands, flags);

    const step = runner.next();
    expect(step.step).toEqual({ kind: "message", text: "また会いましたね", speaker: undefined });
    expect(flags.met_villager).toBe(true);
  });

  it("warpコマンドはUIを止めず、onWarpに通知してそのまま次へ進む", () => {
    const warps: { mapId: string; tileX: number; tileY: number }[] = [];
    const commands: EventCommand[] = [
      { type: "warp", mapId: "room", tileX: 3, tileY: 4 },
      { type: "message", text: "移動しました" },
    ];
    const runner = createEventRunner(commands, {}, { onWarp: (w) => warps.push(w) });

    const step = runner.next();
    expect(warps).toEqual([{ mapId: "room", tileX: 3, tileY: 4 }]);
    expect(step.step).toEqual({ kind: "message", text: "移動しました", speaker: undefined });
  });

  it("startBattleコマンドはonStartBattleに戦闘IDを通知して終了する", () => {
    const startedBattles: string[] = [];
    const commands: EventCommand[] = [
      { type: "message", text: "歪みが姿を現した！" },
      { type: "startBattle", battleId: "chapter0-yugami" },
    ];
    const runner = createEventRunner(commands, {}, {
      onStartBattle: (id) => startedBattles.push(id),
    });

    runner.next();
    const afterBattleStart = runner.next({ kind: "advance" });
    expect(startedBattles).toEqual(["chapter0-yugami"]);
    expect(afterBattleStart.done).toBe(true);
  });
});

describe("宿屋（inn）", () => {
  it("とまると灯貨を払って全快し、足りなければ断られる", () => {
    for (const ok of [true, false]) {
      let called = 0;
      const runner = createEventRunner([{ type: "inn", price: 10 }], {}, { onInnStay: () => { called++; return ok; } });
      const first = runner.next();
      expect(first.step?.kind).toBe("choice");
      const second = runner.next({ kind: "choose", index: 0 });
      expect(called).toBe(1);
      expect(second.step).toMatchObject({ kind: "message" });
      expect((second.step as { text: string }).text).toContain(ok ? "全回復" : "足りない");
    }
  });
  it("やめるを選ぶと、何も払わない", () => {
    let called = 0;
    const runner = createEventRunner([{ type: "inn", price: 10 }], {}, { onInnStay: () => { called++; return true; } });
    runner.next();
    const r = runner.next({ kind: "choose", index: 1 });
    expect(called).toBe(0);
    expect((r.step as { text: string }).text).toContain("また");
  });
});
