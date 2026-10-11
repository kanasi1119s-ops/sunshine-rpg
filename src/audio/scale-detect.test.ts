import { describe, expect, it } from "vitest";
import { SCALES } from "./scales";
// @ts-ignore tools の .mjs（型の宣言はない）
import { loadScales, rankScales, topScales } from "../../tools/audio-check/scale-detect.mjs";

const histOf = (pcs: number[], w = 1): number[] => { const h = new Array(12).fill(0); for (const p of pcs) h[p] += w; return h; };

describe("音階の推定（tools/audio-check/scale-detect.mjs）", () => {
  it("scales.json は src/audio/scales.ts と一致している", () => {
    const json = loadScales() as { id: string; semis: number[]; approx?: number[] }[];
    expect(json.length).toBe(SCALES.length);
    json.forEach((j, i) => {
      expect(j.id).toBe(SCALES[i].id);
      expect(j.semis).toEqual(SCALES[i].semis);
      expect(j.approx).toEqual(SCALES[i].approx);
    });
  });
  it("都節の D（D Eb G A Bb）を聞かせると、都節 D が 100% で一番に出る", () => {
    const top = topScales(histOf([2, 3, 7, 9, 10]), 3, { tonicHints: [2] });
    expect(top[0]).toMatchObject({ id: "miyako", tonicName: "D" });
    expect(top[0].coverage).toBe(1);
  });
  it("主音のヒントで、同じ音の並びの長調と短調を区別する", () => {
    const h = histOf([0, 2, 4, 5, 7, 9, 11]);
    expect(topScales(h, 1, { tonicHints: [0] })[0]).toMatchObject({ id: "ionian", tonicName: "C" });
    expect(topScales(h, 1, { tonicHints: [9] })[0]).toMatchObject({ id: "aeolian", tonicName: "A" });
  });
  it("ヒジャーズ（E F# ではなく D Eb F# G A Bb C）: フリジアン・ドミナントが出る", () => {
    const top = rankScales(histOf([2, 3, 6, 7, 9, 10, 0]), { tonicHints: [2] })[0];
    expect(top).toMatchObject({ id: "phrygian-dominant", tonicName: "D" });
  });
  it("音が空なら空", () => {
    expect(rankScales(new Array(12).fill(0))).toEqual([]);
  });
});
