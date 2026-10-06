import { describe, expect, it } from "vitest";
import { propSpriteKey } from "./prop-renderer";

describe("動く飾りのコマ", () => {
  it("噴水は4コマを順番に見せる（水が流れる）", () => {
    const keys = [0, 140, 280, 420, 560].map((t) => propSpriteKey("fountain", t));
    expect(keys).toEqual(["prop:fountain", "prop:fountain-1", "prop:fountain-2", "prop:fountain-3", "prop:fountain"]);
  });
  it("コマのない飾りは、いつも同じ絵", () => {
    expect(propSpriteKey("barrel", 0)).toBe("prop:barrel");
    expect(propSpriteKey("barrel", 999)).toBe("prop:barrel");
  });
});
