import { describe, expect, it } from "vitest";
import { resolveDirection, type Direction } from "./direction";

describe("resolveDirection", () => {
  it("何も押されていなければnull", () => {
    expect(resolveDirection(new Set())).toBeNull();
  });

  it("1つだけ押されていればその方向", () => {
    const pressed = new Set<Direction>(["up"]);
    expect(resolveDirection(pressed)).toBe("up");
  });

  it("複数押されていれば最後に追加された方向を優先する", () => {
    const pressed = new Set<Direction>();
    pressed.add("up");
    pressed.add("right");
    expect(resolveDirection(pressed)).toBe("right");
  });
});
