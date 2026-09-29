import { describe, expect, it } from "vitest";
import { CHORD_SHAPES, chordIntervals } from "./chord-input";
import { normalizePeak } from "./offline-render";

describe("和音入力とWAVの仕上げ", () => {
  it("和音の形から構成音（半音の数）を作る。知らない形は単音", () => {
    expect(chordIntervals("major")).toEqual([0, 4, 7]);
    expect(chordIntervals("power")).toEqual([0, 7, 12]);
    expect(chordIntervals("???")).toEqual([0]);
    expect(new Set(CHORD_SHAPES.map(([k]) => k)).size).toBe(CHORD_SHAPES.length);
  });
  it("音の山（ピーク）をそろえる。無音はそのまま", () => {
    const c = [new Float32Array([0.1, -0.5]), new Float32Array([0.25, 0])];
    normalizePeak(c, 1);
    expect(c[0][1]).toBeCloseTo(-1);
    expect(c[1][0]).toBeCloseTo(0.5);
    const z = [new Float32Array(3)];
    normalizePeak(z);
    expect([...z[0]]).toEqual([0, 0, 0]);
  });
});
