import { describe, expect, it } from "vitest";
import { createStaffRollState, skipStaffRoll, STAFF_ROLL_LINES, staffRollLength, startStaffRoll, updateStaffRoll } from "./staff-roll";

describe("スタッフロール", () => {
  it("始めると流れ始め、十分な時間がたつと自動で終わる", () => {
    let state = startStaffRoll();
    expect(state.open).toBe(true);
    state = updateStaffRoll(state, 1000, 225);
    expect(state.offset).toBeGreaterThan(0);
    expect(state.open).toBe(true);
    state = updateStaffRoll(state, 10 * 60 * 1000, 225);
    expect(state.open).toBe(false);
  });

  it("決定で飛ばせる。始める前は流れない", () => {
    expect(skipStaffRoll().open).toBe(false);
    expect(updateStaffRoll(createStaffRollState(), 1000, 225).offset).toBe(0);
  });

  it("全体は、1〜2分ほどで流れきる", () => {
    const seconds = staffRollLength(225) / 22;
    expect(seconds).toBeGreaterThan(30);
    expect(seconds).toBeLessThan(150);
  });

  it("素材のクレジットと、遊んでくれたことへのお礼が入っている", () => {
    const text = STAFF_ROLL_LINES.join("");
    expect(text).toContain("ぴぽや");
    expect(text).toContain("Frank Wen");
    expect(text).toContain("ありがとうございました");
    expect(text).toContain("旭洋平");
  });
});
