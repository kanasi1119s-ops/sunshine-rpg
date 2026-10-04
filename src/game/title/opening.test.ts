import { describe, expect, it } from "vitest";
import {
  advanceOpening,
  OPENING_SCENES,
  revealDurationMs,
  sceneDurationMs,
  skipOpening,
  startOpening,
  updateOpening,
  visibleChars,
} from "./opening";

describe("オープニング", () => {
  it("場面は複数あり、どの場面にも文字がある（行は画面に収まる長さ）", () => {
    expect(OPENING_SCENES.length).toBeGreaterThanOrEqual(7);
    for (const scene of OPENING_SCENES) {
      expect(scene.lines.length).toBeGreaterThan(0);
      expect(scene.lines.length).toBeLessThanOrEqual(3);
      for (const line of scene.lines) expect(line.length).toBeLessThanOrEqual(26);
    }
  });

  it("時間がたつと文字が1文字ずつ増える", () => {
    const scene = OPENING_SCENES[0];
    expect(visibleChars(scene, 0)).toBe(0);
    expect(visibleChars(scene, revealDurationMs(scene))).toBe(scene.lines.join("").length);
    expect(visibleChars(scene, 2000)).toBeGreaterThan(0);
  });

  it("決定: 途中なら全部出し、全部出ていれば次の場面へ", () => {
    let state = startOpening();
    state = advanceOpening(state);
    expect(state.scene).toBe(0);
    expect(state.elapsedMs).toBe(revealDurationMs(OPENING_SCENES[0]));
    state = advanceOpening(state);
    expect(state.scene).toBe(1);
    expect(state.elapsedMs).toBe(0);
  });

  it("放っておいても最後の場面まで進み、終わると閉じる", () => {
    let state = startOpening();
    let guard = 0;
    while (state.open && guard++ < 100000) {
      state = updateOpening(state, 100);
    }
    expect(state.open).toBe(false);
    expect(guard).toBeLessThan(OPENING_SCENES.reduce((sum, s) => sum + sceneDurationMs(s), 0) / 100 + 10);
  });

  it("スキップするとすぐ閉じる", () => {
    expect(skipOpening(startOpening()).open).toBe(false);
  });
});
