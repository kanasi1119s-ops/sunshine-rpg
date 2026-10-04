import { describe, expect, it } from "vitest";
import {
  advanceBattleTransition,
  canSkipTransition,
  coverMs,
  isCoverPhase,
  skipToReveal,
  startBattleTransition,
  totalMs,
} from "./battle-transition";

describe("戦闘に入る演出", () => {
  it("ふつうの戦闘は1秒かからず、ボス登場はそれより長い", () => {
    expect(totalMs(startBattleTransition(false))).toBeLessThan(1000);
    expect(totalMs(startBattleTransition(true, "灯里の歪み"))).toBeGreaterThan(totalMs(startBattleTransition(false)) * 3);
  });

  it("前半はフィールドを見せ、そのあと戦闘画面がひらき、終わったら null になる", () => {
    let t: ReturnType<typeof startBattleTransition> | null = startBattleTransition(false);
    expect(isCoverPhase(t)).toBe(true);
    t = advanceBattleTransition(t, coverMs(t) + 1);
    expect(t && isCoverPhase(t)).toBe(false);
    expect(advanceBattleTransition(t!, 10000)).toBeNull();
  });

  it("ボス登場は、名前が出たあとなら決定でとばせる（前半の終わりまで）", () => {
    const early = startBattleTransition(true, "ボス");
    expect(canSkipTransition(early)).toBe(false);
    const later = { ...early, ms: 1200 };
    expect(canSkipTransition(later)).toBe(true);
    expect(skipToReveal(later).ms).toBe(coverMs(later));
    expect(canSkipTransition(startBattleTransition(false))).toBe(false);
  });
});
