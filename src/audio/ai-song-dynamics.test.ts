import { describe, expect, it } from "vitest";
import { applyArc } from "./ai-song";

describe("AIソングの起伏", () => {
  it("出だしは小さく、中盤で引き、ほかは元の強さ", () => {
    const notes = Array.from({ length: 32 }, () => ({ note: "C4", durationBeats: 1 }));
    const [t] = applyArc([{ waveform: "sawtooth", volume: 0.2, notes } as never], 32, 4);
    const v = t.notes.map((n) => n.velocity ?? 1);
    expect(v[0]).toBeLessThan(0.6);
    expect(v[16]).toBeCloseTo(0.75);
    expect(v[10]).toBe(1);
    expect(v[31]).toBe(1);
  });
});
