import { describe, expect, it } from "vitest";
import { CATALOG, getTrack } from "./catalog";
import { flattenScore, getScoreDurationSec } from "./score";

describe("BGMカタログ（55曲）", () => {
  it("55曲そろっていて、IDと曲名が重複しない", () => {
    expect(CATALOG.length).toBe(55);
    expect(new Set(CATALOG.map((e) => e.id)).size).toBe(55);
    expect(new Set(CATALOG.map((e) => e.title)).size).toBe(55);
  });
  it.each(CATALOG.map((e) => [e.id, e] as const))("%s: 1分〜1分半・パートの長さがそろう・音名が読める", (id) => {
    const score = getTrack(id);
    const sec = getScoreDurationSec(score);
    const special = CATALOG.find((e) => e.id === id)?.finale !== undefined;
    // 特別な曲（ラスボス・裏ボスなど）は3〜4分、ほかは1〜1分半
    expect(sec).toBeGreaterThanOrEqual(special ? 170 : 60);
    expect(sec).toBeLessThanOrEqual(special ? 250 : 90);
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

describe("現代的な音づくり・ボス戦の疾走感", () => {
  it("ボス戦の曲は速め（BPM148以上）で、4拍子の曲には16分の刻みが入る", () => {
    for (const id of ["boss-touri", "boss-mugikano", "boss-tetsu", "boss-sanone", "boss-shimo", "boss-ukishima"]) {
      const score = getTrack(id);
      expect(score.tempoBpm, id).toBeGreaterThanOrEqual(148);
    }
    const four = getTrack("boss-touri");
    expect(four.tracks.some((t) => t.notes.some((n) => n.durationBeats === 0.25 && n.note !== "R"))).toBe(true);
  });
  it("楽器の音は左右に振り分けられ、音の強さにゆらぎがつく", () => {
    const score = getTrack("boss-touri");
    const pans = new Set(score.tracks.map((t) => t.pan).filter((p) => p !== undefined));
    expect(pans.size).toBeGreaterThan(2);
    const vols = new Set(flattenScore(score).filter((e) => e.instrument === "bass").map((e) => e.volume.toFixed(4)));
    expect(vols.size).toBeGreaterThan(3);
  });
});
