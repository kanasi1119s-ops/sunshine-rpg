import { describe, expect, it } from "vitest";
import { analyzeMix, checkScore } from "./song-check";
import type { Score } from "./score";

const notes = (names: string[], dur = 0.5) => names.map((note) => ({ note, durationBeats: dur }));
const mk = (tracks: Score["tracks"]): Score => ({ tempoBpm: 120, loop: false, tracks } as Score);
const rep = (a: string[], n: number) => Array.from({ length: n }, () => a).flat();

describe("checkScore", () => {
  it("低い音域で別パートが近い高さを同時に鳴らすと、にごりの注意", () => {
    const w = checkScore(mk([
      { waveform: "square", instrument: "bass", volume: 0.2, notes: notes(rep(["C2", "D2"], 16)) },
      { waveform: "square", instrument: "piano", volume: 0.2, notes: notes(rep(["D2", "E2"], 16)) },
    ]));
    expect(w.some((x) => x.includes("にごり"))).toBe(true);
  });
  it("ベースとメロディが離れていれば、にごりも音域の注意も出ない", () => {
    const w = checkScore(mk([
      { waveform: "square", instrument: "bass", volume: 0.2, notes: notes(rep(["C2", "G2"], 16)) },
      { waveform: "square", instrument: "lead", volume: 0.2, notes: notes(rep(["E5", "G5", "A5", "C6"], 8).map((x) => x)) },
    ].map((t, i) => (i ? { ...t, notes: t.notes.map((n, k) => ({ ...n, velocity: 1 + (k % 3) * 0.1 })) } : t)) as Score["tracks"]));
    expect(w.filter((x) => x.includes("にごり") || x.includes("同じ音域"))).toEqual([]);
  });
  it("同じ音域の2パートを見つける", () => {
    const seq = notes(rep(["C4", "E4", "G4", "E4"], 8));
    const w = checkScore(mk([{ waveform: "square", instrument: "piano", volume: 0.2, notes: seq }, { waveform: "square", instrument: "lead", volume: 0.2, notes: seq }]));
    expect(w.some((x) => x.includes("同じ音域"))).toBe(true);
  });
  it("強弱も長さも一定なら、表情を足すヒント", () => {
    const w = checkScore(mk([{ waveform: "square", instrument: "lead", volume: 0.2, notes: notes(rep(["C5", "D5", "E5", "G5"], 8)) }]));
    expect(w.some((x) => x.includes("phrase"))).toBe(true);
  });
});

describe("analyzeMix", () => {
  const sine = (amp: number, hz: number, sec: number, fs = 44100) => Float32Array.from({ length: sec * fs }, (_, i) => amp * Math.sin((2 * Math.PI * hz * i) / fs));
  it("天井に当たる音を見つける", () => {
    const x = sine(1.2, 440, 4).map((v) => Math.max(-1, Math.min(1, v)));
    expect(analyzeMix([x, x], 44100).some((w) => w.includes("割れ"))).toBe(true);
  });
  it("低い音ばかりなら低音が多すぎる", () => {
    const x = sine(0.5, 60, 4);
    expect(analyzeMix([x, x], 44100).some((w) => w.includes("低音が多すぎ"))).toBe(true);
  });
  it("ふつうの音は注意なし", () => {
    const x = sine(0.4, 1000, 4);
    expect(analyzeMix([x, x], 44100).filter((w) => w.includes("割れ") || w.includes("低音"))).toEqual([]);
  });
});
