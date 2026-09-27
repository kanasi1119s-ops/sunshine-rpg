import { describe, expect, it } from "vitest";
import { computeDamage, computeFleeChance } from "./formulas";

describe("computeDamage", () => {
  it("こうげきがぼうぎょを上回るほどダメージが増える", () => {
    const rng = () => 0.5; // ばらつき100%、会心なし
    const low = computeDamage(10, 20, 1, rng);
    const high = computeDamage(30, 5, 1, rng);
    expect(high.amount).toBeGreaterThan(low.amount);
  });

  it("最低でも1のダメージは出る", () => {
    const rng = () => 0.5;
    const result = computeDamage(1, 999, 1, rng);
    expect(result.amount).toBeGreaterThanOrEqual(1);
  });

  it("会心のとき、ダメージが約2倍になる", () => {
    // 1回目のrng()はばらつき用（1.0固定にするため0.5）、2回目は会心判定用（0を返して必ず会心）。
    let call = 0;
    const rng = () => (call++ === 0 ? 0.5 : 0);
    const result = computeDamage(20, 0, 1, rng);
    expect(result.critical).toBe(true);
    expect(result.amount).toBe(40);
  });

  it("威力倍率が高いほどダメージが増える", () => {
    const rng = () => 0.5;
    const normal = computeDamage(20, 0, 1, rng);
    const skill = computeDamage(20, 0, 2, rng);
    expect(skill.amount).toBeGreaterThan(normal.amount);
  });
});

describe("computeFleeChance", () => {
  it("すばやさが同じなら50%", () => {
    expect(computeFleeChance(10, 10)).toBe(0.5);
  });

  it("上限90%・下限10%に収める", () => {
    expect(computeFleeChance(1000, 1)).toBe(0.9);
    expect(computeFleeChance(1, 1000)).toBe(0.1);
  });
});
