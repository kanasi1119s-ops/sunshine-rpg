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

describe("弦の雑音（2026-10-21）", () => {
  it("休みの前に「止める」音、5半音以上の跳躍の前に「すべる」音を、同じアンプのパートとして足す", async () => {
    const { expandGuitarTech } = await import("./guitar-tech");
    const p = { instrument: "distGuitar", role: "刻み", volume: 0.1, pan: 0.3, amp: "namDD", stringNoise: true, notes: "E2:1 R:1 A2:0.5 E3:1 R:1" } as unknown as AiPart;
    const list = expandGuitarTech(p, { bpm: 120, beatsPerBar: 4, totalBeats: 8, chordBars: [], tonic: null, scale: null }, []);
    expect(list).toHaveLength(2);
    const n = list[1];
    expect(n.patch).toBe("guitarNoise");
    expect(n.amp).toBe("namDD");
    expect(String(n.notes)).toContain("G2:");
    expect(String(n.notes)).toContain("C2:");
    expect((list[0] as { stringNoise?: unknown }).stringNoise).toBeUndefined();
    // 長い休みは 8 拍以下に分かれる
    const far = expandGuitarTech({ ...p, notes: "R:8 R:8 R:8 E2:1 R:1 C3:1" } as unknown as AiPart, { bpm: 120, beatsPerBar: 4, totalBeats: 30, chordBars: [], tonic: null, scale: null }, []);
    for (const tok of String(far[1].notes).split(" ")) expect(Number(tok.split(":")[1].replace(/[^0-9.]/g, ""))).toBeLessThanOrEqual(8);
  });
});

describe("トランスゲートの形（2026-10-21）", () => {
  it("x は鳴り（1）、. は切れる（1-depth）。係数から戻した形が合う", async () => {
    const { gateWaveCoefficients } = await import("./fx-extra");
    const { dc, real, imag } = gateWaveCoefficients("x.", 1);
    expect(dc).toBeGreaterThan(0.45);
    expect(dc).toBeLessThan(0.55);
    const at = (t: number): number => { let v = dc; for (let h = 1; h < real.length; h++) v += real[h] * Math.cos(2 * Math.PI * h * t) + imag[h] * Math.sin(2 * Math.PI * h * t); return v; };
    expect(at(0.2)).toBeGreaterThan(0.9);
    expect(at(0.7)).toBeLessThan(0.1);
  });
});
