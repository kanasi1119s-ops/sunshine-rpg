import { describe, expect, it } from "vitest";
import { stickDirection } from "./touch-controls";

describe("スティックの向き", () => {
  it("まんなか付近は動かない", () => expect(stickDirection(0.1, 0.1)).toBeNull());
  it("たてよこで大きいほうの向きになる", () => {
    expect(stickDirection(0.8, 0.2)).toBe("right");
    expect(stickDirection(-0.8, 0.2)).toBe("left");
    expect(stickDirection(0.2, 0.8)).toBe("down");
    expect(stickDirection(0.2, -0.8)).toBe("up");
  });
});
