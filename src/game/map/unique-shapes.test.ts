import { describe, expect, it } from "vitest";
import { WORLD_MAPS } from "../world/world";

describe("同じ形のダンジョンを使いまわさない", () => {
  it("ダンジョン・塔・祠・小島の地図は、どれも形（通れないマスの並び）がちがう", () => {
    const byShape = new Map<string, string[]>();
    for (const [id, m] of Object.entries(WORLD_MAPS)) {
      if (!/(cave|canal|tunnel|forest|deep|tower|kanou|god-shrine|islet|ruins|archive|facility|mine)/.test(id) || !m.collision) continue;
      const key = `${m.width}x${m.height}:${m.collision.join("")}`;
      byShape.set(key, [...(byShape.get(key) ?? []), id]);
    }
    expect([...byShape.values()].filter((ids) => ids.length > 1)).toEqual([]);
  });
});
