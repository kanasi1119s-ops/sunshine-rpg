import { describe, expect, it } from "vitest";
import { measureLufs, normalizeLoudness } from "./loudness";

const sine = (amp: number, sec = 4, fs = 48000) => {
  const x = new Float32Array(sec * fs);
  for (let i = 0; i < x.length; i++) x[i] = amp * Math.sin((2 * Math.PI * 1000 * i) / fs);
  return [x, new Float32Array(x)];
};

describe("loudness", () => {
  it("1kHzのサイン波（ピーク0.1）は約 -23 LUFS（左右とも同じなので +3dB で約 -20）", () => {
    const l = measureLufs(sine(0.1), 48000);
    expect(l).toBeGreaterThan(-21.5);
    expect(l).toBeLessThan(-19);
  });
  it("大きさが違う2曲を、同じ LUFS にそろえる", () => {
    const a = sine(0.05), b = sine(0.4);
    normalizeLoudness(a, 48000, -16); normalizeLoudness(b, 48000, -16);
    expect(Math.abs(measureLufs(a, 48000) - measureLufs(b, 48000))).toBeLessThan(1.5);
  });
  it("山は ceiling を超えない", () => {
    const a = sine(0.9);
    normalizeLoudness(a, 48000, -8, 0.97);
    let peak = 0;
    for (const v of a[0]) peak = Math.max(peak, Math.abs(v));
    expect(peak).toBeLessThanOrEqual(0.97);
  });
  it("無音はそのまま", () => {
    const z = [new Float32Array(48000), new Float32Array(48000)];
    expect(normalizeLoudness(z, 48000).gainDb).toBe(0);
  });
});
