import { describe, expect, it } from "vitest";
import { InputState } from "./input-state";

describe("InputState", () => {
  it("押した方向を返す", () => {
    const input = new InputState();
    input.press("left");
    expect(input.getDirection()).toBe("left");
  });

  it("離すとその方向は返さなくなる", () => {
    const input = new InputState();
    input.press("left");
    input.release("left");
    expect(input.getDirection()).toBeNull();
  });

  it("あとから押した方向を優先し、それを離すと前の方向に戻る", () => {
    const input = new InputState();
    input.press("up");
    input.press("right");
    expect(input.getDirection()).toBe("right");
    input.release("right");
    expect(input.getDirection()).toBe("up");
  });
});
