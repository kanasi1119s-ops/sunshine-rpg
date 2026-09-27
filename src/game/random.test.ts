import { describe, expect, it } from "vitest";
import { createRng } from "./random";

describe("createRng", () => {
  it("同じシードなら同じ結果を再現する", () => {
    const a = createRng(42);
    const b = createRng(42);
    const seqA = [a(), a(), a()];
    const seqB = [b(), b(), b()];
    expect(seqA).toEqual(seqB);
  });

  it("0以上1未満の値を返す", () => {
    const rng = createRng(1);
    for (let i = 0; i < 20; i++) {
      const value = rng();
      expect(value).toBeGreaterThanOrEqual(0);
      expect(value).toBeLessThan(1);
    }
  });

  it("シードが違えば結果も変わる（極端な偏りがない）", () => {
    const a = createRng(1)();
    const b = createRng(2)();
    expect(a).not.toBe(b);
  });
});
