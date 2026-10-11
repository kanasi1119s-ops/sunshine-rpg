import { describe, expect, it } from "vitest";
import { applyNaturalDynamics, bigArc, phraseBreath, beatAccent } from "./dynamics";

describe("自然な強弱", () => {
  it("出だしは小さく、7割あたりが頂点、終わりは静か", () => {
    expect(bigArc(0, 100)).toBeLessThan(0.7);
    expect(bigArc(70, 100)).toBeCloseTo(1);
    expect(bigArc(100, 100)).toBeLessThan(0.75);
  });
  it("フレーズは張って引く", () => {
    expect(phraseBreath(2)).toBeGreaterThan(phraseBreath(0));
    expect(phraseBreath(3)).toBeLessThan(phraseBreath(2));
  });
  it("1拍目は強く裏拍は弱い", () => {
    expect(beatAccent(0, 4)).toBeGreaterThan(beatAccent(0.5, 4));
    expect(beatAccent(0, 4)).toBeGreaterThan(beatAccent(1, 4));
  });
  it("同じ曲は何度やっても同じ、強弱の幅が広がる", () => {
    const notes = Array.from({ length: 64 }, () => ({ note: "C4", durationBeats: 1 }));
    const tr = [{ waveform: "sawtooth", volume: 0.2, instrument: "guitar", notes }] as never;
    const a = applyNaturalDynamics(tr, 64, 4)[0].notes.map((n) => n.velocity!);
    const b = applyNaturalDynamics(tr, 64, 4)[0].notes.map((n) => n.velocity!);
    expect(a).toEqual(b);
    expect(Math.max(...a) / Math.min(...a)).toBeGreaterThan(1.8);
    expect(Math.max(...a)).toBeLessThanOrEqual(1.07);
  });
});

describe("自動の伴奏の強さ", () => {
  it("MIDIの数字（112など）は0〜1の比に直してから強弱をかける", () => {
    const notes = [{ note: "C2", durationBeats: 1, velocity: 100 }];
    const [t] = applyNaturalDynamics([{ waveform: "square", volume: 0.3, instrument: "kick", notes } as never], 64, 4);
    expect(t.notes[0].velocity).toBeLessThan(1.2);
  });
});
