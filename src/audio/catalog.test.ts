import { describe, expect, it } from "vitest";
import { CATALOG, getTrack } from "./catalog";
import { flattenScore, getScoreDurationSec } from "./score";

describe("BGMカタログ（52曲）", () => {
  it("52曲そろっていて、IDと曲名が重複しない", () => {
    expect(CATALOG.length).toBe(52);
    expect(new Set(CATALOG.map((e) => e.id)).size).toBe(52);
    expect(new Set(CATALOG.map((e) => e.title)).size).toBe(52);
  });
  it.each(CATALOG.map((e) => [e.id, e] as const))("%s: 1分〜1分半・パートの長さがそろう・音名が読める", (id) => {
    const score = getTrack(id);
    const sec = getScoreDurationSec(score);
    expect(sec).toBeGreaterThanOrEqual(60);
    expect(sec).toBeLessThanOrEqual(90);
    const beats = score.tracks.map((t) => t.notes.reduce((s, n) => s + n.durationBeats, 0));
    for (const b of beats) expect(b).toBeCloseTo(beats[0], 6);
    expect(() => flattenScore(score)).not.toThrow();
    const sounding = score.tracks.filter((t) => t.notes.some((n) => n.note !== "R"));
    expect(sounding.length).toBeGreaterThan(1);
    expect(score.loop).toBe(true);
  });
  it("同じ設計図からは同じ曲ができる（作り直しても変わらない）", () => {
    const a = JSON.stringify(getTrack("battle"));
    expect(a.length).toBeGreaterThan(1000);
  });
});
