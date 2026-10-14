import { describe, expect, it } from "vitest";
import data from "../../docs/sound/data/chord-patterns-100.json";
import { parseChord } from "./newsong";

describe("コード進行100通り（docs/sound/chord-patterns-100.md）", () => {
  it("100個あり、進行が重ならない", () => {
    expect(data.patterns.length).toBeGreaterThanOrEqual(100);
    expect(new Set(data.patterns.map((p) => p.chords)).size).toBe(data.patterns.length);
  });
  it("すべてのコード名を作曲ソフトが読める", () => {
    for (const p of data.patterns) for (const c of p.chords.split(" ")) expect(parseChord(c), `${p.no} ${p.name}: ${c}`).not.toBeNull();
  });
});
