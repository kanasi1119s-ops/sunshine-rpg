import { describe, expect, it } from "vitest";
import { createGameLoop } from "./game-loop";

describe("createGameLoop", () => {
  it("delta時間に関わらずupdateを一定刻み(stepMs)で呼ぶ", () => {
    const updates: number[] = [];
    const loop = createGameLoop(
      { update: (dt) => updates.push(dt), render: () => {} },
      { stepMs: 10 },
    );

    loop.tick(0);
    loop.tick(35);

    expect(updates).toEqual([10, 10, 10]);
  });

  it("極端に大きなdeltaはmaxDeltaMsで打ち切る（スパイラル・オブ・デス対策）", () => {
    const updates: number[] = [];
    const loop = createGameLoop(
      { update: (dt) => updates.push(dt), render: () => {} },
      { stepMs: 10, maxDeltaMs: 50 },
    );

    loop.tick(0);
    loop.tick(10000);

    expect(updates.length).toBe(5);
  });

  it("1秒分のtickでFPSを計算する", () => {
    const loop = createGameLoop(
      { update: () => {}, render: () => {} },
      { stepMs: 100, maxDeltaMs: 1000 },
    );

    loop.tick(0);
    loop.tick(500);
    loop.tick(1000);

    expect(loop.getFps()).toBe(3);
  });
});
