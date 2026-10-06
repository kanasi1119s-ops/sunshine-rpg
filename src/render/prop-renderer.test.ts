import { describe, expect, it } from "vitest";
import { propSpriteKey } from "./prop-renderer";

describe("動く飾りのコマ", () => {
  it("噴水は4コマを順番に見せる（水が流れる）", () => {
    const keys = [0, 140, 280, 420, 560].map((t) => propSpriteKey("fountain", t));
    expect(keys).toEqual(["prop:fountain", "prop:fountain-1", "prop:fountain-2", "prop:fountain-3", "prop:fountain"]);
  });
  it("暖炉の火も4コマで動く", () => {
    expect([0, 140, 280, 420].map((t) => propSpriteKey("hearth", t))).toEqual(["prop:hearth", "prop:hearth-1", "prop:hearth-2", "prop:hearth-3"]);
  });
  it("コマのない飾りは、いつも同じ絵", () => {
    expect(propSpriteKey("barrel", 0)).toBe("prop:barrel");
    expect(propSpriteKey("barrel", 999)).toBe("prop:barrel");
  });
});
