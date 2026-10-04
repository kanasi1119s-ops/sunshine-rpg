import { describe, expect, it } from "vitest";
import { cycleMoveSpeed, DEFAULT_MOVE_SPEED, loadMoveSpeed, MOVE_SPEEDS, saveMoveSpeed } from "./move-speed";

describe("歩く速さ", () => {
  it("ふつうが1倍で、ぐるっと切りかわる", () => {
    expect(MOVE_SPEEDS[DEFAULT_MOVE_SPEED].factor).toBe(1);
    expect(cycleMoveSpeed(0, -1)).toBe(MOVE_SPEEDS.length - 1);
    expect(cycleMoveSpeed(MOVE_SPEEDS.length - 1, 1)).toBe(0);
  });
  it("保存と読みこみ。おかしな値はふつうにもどる", () => {
    const mem: Record<string, string> = {};
    const st = { getItem: (k: string) => mem[k] ?? null, setItem: (k: string, v: string) => void (mem[k] = v) };
    expect(loadMoveSpeed(st)).toBe(DEFAULT_MOVE_SPEED);
    saveMoveSpeed(st, 3);
    expect(loadMoveSpeed(st)).toBe(3);
    saveMoveSpeed(st, 99);
    expect(loadMoveSpeed(st)).toBe(DEFAULT_MOVE_SPEED);
  });
});
