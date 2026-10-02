import { describe, expect, it } from "vitest";
import { noteNameToMidi } from "./note";
import { generateMotifMelody, type MotifRole } from "./melody-motif";
import { makeRng } from "./songwriter";

const MINOR = [0, 2, 3, 5, 7, 8, 10];
const MAJOR = [0, 2, 4, 5, 7, 9, 11];
const CHORDS8 = ["Am", "F", "C", "G", "Am", "F", "G", "Am"];
const RANGE: Record<string, [number, number]> = { verse: [60, 74], bridge: [62, 77], chorus: [65, 79], solo: [67, 88], intro: [64, 82], outro: [62, 80] };

interface N { midi: number | null; dur: number; start: number }
function parse(s: string): N[] {
  let pos = 0;
  return s.split(" ").map((t) => {
    const [name, d] = t.split(":");
    const n = { midi: name === "R" ? null : noteNameToMidi(name), dur: Number(d), start: pos };
    pos += Number(d);
    return n;
  });
}
const gen = (seed: number, role: MotifRole, over: { chords?: string[]; beats?: number; singable?: boolean; scale?: number[]; tonic?: number } = {}): string => {
  const [lo, hi] = RANGE[role];
  return generateMotifMelody(makeRng(seed), over.scale ?? MINOR, over.tonic ?? 9, over.chords ?? CHORDS8, over.beats ?? 4, { lo, hi, role, singable: over.singable });
};

describe("モチーフ展開型のメロディ", () => {
  it("どの種・役割・拍子でも、1小節ずつ拍の合計がぴったり合い、音域と音階の中に収まる", () => {
    for (const beats of [3, 4, 7]) {
      for (const role of ["verse", "bridge", "chorus", "solo", "intro", "outro"] as const) {
        for (let seed = 1; seed <= 25; seed++) {
          const chords = role === "intro" ? CHORDS8.slice(0, 4) : CHORDS8;
          const notes = parse(gen(seed, role, { beats, chords }));
          expect(notes.reduce((s, n) => s + n.dur, 0), `${beats}拍 ${role} ${seed}`).toBe(chords.length * beats);
          for (const n of notes) {
            if (n.midi === null) continue;
            expect(n.midi).toBeGreaterThanOrEqual(RANGE[role][0]);
            expect(n.midi).toBeLessThanOrEqual(RANGE[role][1]);
            expect(MINOR.includes(((n.midi - 9) % 12 + 12) % 12), `${n.midi}`).toBe(true);
          }
        }
      }
    }
  });

  it("同じ種からは同じ旋律。種を変えると別の旋律", () => {
    expect(gen(7, "chorus")).toBe(gen(7, "chorus"));
    const set = new Set(Array.from({ length: 12 }, (_, i) => gen(i + 1, "chorus")));
    expect(set.size).toBeGreaterThanOrEqual(11);
  });

  it("モチーフが展開される: 1小節目と3小節目の拍の並びと音の動きが同じ（くり返し）、5小節目は上へ移る", () => {
    for (let seed = 1; seed <= 20; seed++) {
      const notes = parse(gen(seed, "verse")).filter((n) => n.midi !== null);
      const bar = (b: number): N[] => notes.filter((n) => n.start >= b * 4 && n.start < (b + 1) * 4);
      const rhythm = (b: number): string => bar(b).map((n) => n.dur).join(",");
      expect(rhythm(2), `seed ${seed}`).toBe(rhythm(0));
      expect(rhythm(4)).toBe(rhythm(0));
      const lead = (b: number): number => bar(b)[0].midi!;
      expect(lead(4)).toBeGreaterThanOrEqual(lead(0)); // B は同じかそれより高い所から
    }
  });

  it("強い拍（小節の頭・長い音）の音は、その小節のコードの音が多い（8割以上）", () => {
    const pcs: Record<string, number[]> = { Am: [9, 0, 4], F: [5, 9, 0], C: [0, 4, 7], G: [7, 11, 2] };
    let strong = 0;
    let hit = 0;
    for (let seed = 1; seed <= 30; seed++) {
      for (const n of parse(gen(seed, "chorus")).filter((x) => x.midi !== null)) {
        if (n.start % 4 === 0 || n.dur >= 2) {
          strong++;
          if (pcs[CHORDS8[Math.floor(n.start / 4)]].includes(n.midi! % 12)) hit++;
        }
      }
    }
    expect(hit / strong).toBeGreaterThan(0.8);
  });

  it("サビはAメロより高い。サビは最後を長い音でおさめ、最後の音はコードの音", () => {
    let chorusHigher = 0;
    for (let seed = 1; seed <= 30; seed++) {
      const avg = (role: MotifRole): number => {
        const m = parse(gen(seed, role)).filter((n) => n.midi !== null);
        return m.reduce((s, n) => s + n.midi!, 0) / m.length;
      };
      if (avg("chorus") > avg("verse")) chorusHigher++;
      const last = parse(gen(seed, "chorus")).filter((n) => n.midi !== null).pop()!;
      expect(last.dur).toBeGreaterThanOrEqual(2);
      expect([9, 0, 4]).toContain(last.midi! % 12); // 最後の和音 Am の音
    }
    expect(chorusHigher).toBe(30);
  });

  it("歌えるメロディ: 最短0.5拍・大きな跳躍が少ない・単調でない（音が5種類以上）", () => {
    for (let seed = 1; seed <= 30; seed++) {
      const notes = parse(gen(seed, "verse", { singable: true }));
      expect(Math.min(...notes.map((n) => n.dur))).toBeGreaterThanOrEqual(0.5);
      const m = notes.filter((n) => n.midi !== null).map((n) => n.midi!);
      let leaps = 0;
      for (let i = 1; i < m.length; i++) if (Math.abs(m[i] - m[i - 1]) > 7) leaps++;
      expect(leaps).toBeLessThanOrEqual(2);
      expect(new Set(m).size).toBeGreaterThanOrEqual(5);
    }
  });

  it("長調でも動く。ソロは細かい音が多い", () => {
    const major = parse(gen(3, "verse", { scale: MAJOR, tonic: 0, chords: ["C", "G", "Am", "F", "C", "G", "F", "C"] }));
    expect(major.length).toBeGreaterThan(10);
    const solo = parse(gen(3, "solo"));
    const verse = parse(gen(3, "verse"));
    expect(solo.length).toBeGreaterThan(verse.length);
  });
});
