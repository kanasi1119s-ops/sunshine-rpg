import { describe, expect, it } from "vitest";
import { expandDoubleTrack } from "./part-expand";
import type { AiPart } from "./ai-song";

describe("ダブルトラック（2026-10-20 ラウドロック）", () => {
  it("左右いっぱいの2パートにし、右だけ別のIR・少し浅い歪み・タイミングのずれを大きくする", () => {
    const p = { instrument: "distGuitar", role: "刻み", volume: 0.1, pan: 0, amp: "namA", ampCabIr: "a+b", notes: "C2:1" } as unknown as AiPart;
    const [l, r] = expandDoubleTrack(p, true);
    expect(l.pan).toBe(-1);
    expect(r.pan).toBe(1);
    expect(Math.abs(Number(l.detune))).toBeLessThanOrEqual(3);
    expect(r.ampCabIr).not.toBe(l.ampCabIr);
    expect(Number(r.ampDrive)).toBeLessThan(1);
    expect(Number(l.humanTiming)).toBeGreaterThan(1);
    expect((l as { double?: unknown }).double).toBeUndefined();
  });
});
