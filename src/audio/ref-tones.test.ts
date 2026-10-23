import { describe, expect, it } from "vitest";
import { REF_TONES, applyRefTone } from "./ref-tones";
import type { Score } from "./score";

const score = (): Score => ({
  bpm: 120, beatsPerBar: 4,
  tracks: [
    { waveform: "square", instrument: "distGuitar", volume: 0.1, pan: -0.5, notes: [], fx: [{ type: "room", mix: 0.1 }, { type: "eq", low: 0, mid: 3, midHz: 1000, high: 0 }] },
    { waveform: "square", instrument: "distGuitar", volume: 0.05, pan: 0.35, notes: [], fx: [{ type: "delay", mix: 0.25 }] },
    { waveform: "square", instrument: "bass", volume: 0.1, notes: [] },
    { waveform: "square", instrument: "snare", volume: 0.1, notes: [] },
  ],
} as unknown as Score);

describe("参考の音", () => {
  it("6つあり、どれもギター・ベース・ドラムの EQ を持つ", () => {
    expect(Object.keys(REF_TONES)).toHaveLength(6);
    for (const t of Object.values(REF_TONES)) for (const k of ["guitar", "bass", "drums"] as const) expect(t[k].length).toBeGreaterThan(0);
  });
  it("EQ とフィルターだけを置きかえ、ルームなどは残す。音量は変えない", () => {
    const tone = REF_TONES["bright-pop-rock"];
    const out = applyRefTone(score(), tone);
    const g = out.tracks[0];
    expect(g.fx?.some((f) => f.type === "room")).toBe(true);
    expect(g.fx?.filter((f) => f.type === "eq" || f.type === "filter")).toEqual(tone.guitar);
    expect(g.volume).toBe(0.1);
    expect(out.tracks[2].fx).toEqual(tone.bass);
    expect(out.tracks[3].fx).toEqual(tone.drums);
  });
  it("やまびこの付いたギター（空気の層）は、そのほかの値が無ければ変えない", () => {
    const out = applyRefTone(score(), REF_TONES["bright-pop-rock"]);
    expect(out.tracks[1].fx).toEqual([{ type: "delay", mix: 0.25 }]);
  });
  it("guitarWide なら左右に分かれた歪みギターを左右いっぱいに", () => {
    const out = applyRefTone(score(), REF_TONES["wide-dark-wall"]);
    expect(out.tracks[0].pan).toBe(-1);
  });
  it("何度当てても同じ", () => {
    const t = REF_TONES["glossy-jrock"];
    expect(applyRefTone(applyRefTone(score(), t), t)).toEqual(applyRefTone(score(), t));
  });
});
