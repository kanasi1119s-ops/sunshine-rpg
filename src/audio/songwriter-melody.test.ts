import { describe, expect, it } from "vitest";
import { generateMelody, keyOf, makeRng } from "./songwriter";
import { noteNameToMidi } from "./note";

const key = keyOf({ tonic: "A", minor: true });
const chords = ["Am", "F", "C", "G", "Am", "F", "C", "G", "Am", "F", "C", "G", "Am", "F", "G", "Am"];
const make = (seed: number) => generateMelody(makeRng(seed), key, chords, 4, { lo: 64, hi: 84, density: "normal" });
const parse = (m: string) => m.split(" ").map((t) => { const [n, d] = t.split(":"); return { n, d: Number(d) }; });

describe("generateMelody（展開・跳躍のあとの戻り）", () => {
  it("同じシードなら同じ旋律。長さは小節数ぴったり。すべて曲の音階の音", () => {
    expect(make(7)).toBe(make(7));
    for (let seed = 1; seed <= 30; seed++) {
      const notes = parse(make(seed));
      expect(notes.reduce((s, x) => s + x.d, 0)).toBeCloseTo(chords.length * 4, 6);
      for (const x of notes) if (x.n !== "R") expect(key.scale).toContain(((noteNameToMidi(x.n) - key.tonic) % 12 + 12) % 12);
    }
  });
  it("2小節目が1小節目の形のずらし（反復進行）になる旋律が、たくさんの曲のうち何割かに出る", () => {
    let seq = 0, total = 0;
    for (let seed = 1; seed <= 60; seed++) {
      const bars: { n: string; d: number }[][] = [];
      let cur: { n: string; d: number }[] = [], beat = 0;
      for (const x of parse(make(seed))) { cur.push(x); beat += x.d; if (beat >= 4 - 1e-9) { bars.push(cur); cur = []; beat = 0; } }
      for (let b = 1; b < bars.length - 1; b += 4) {
        total++;
        const a = bars[b - 1], c = bars[b];
        if (a.length === c.length && a.length > 1 && a.every((x, i) => x.d === c[i].d) && a.every((x) => x.n !== "R")) {
          const da = a.map((x, i) => noteNameToMidi(x.n) - noteNameToMidi(a[0].n) - 0 * i);
          const dc = c.map((x) => noteNameToMidi(x.n) - noteNameToMidi(c[0].n));
          if (da.every((v, i) => Math.abs(v - dc[i]) <= 2) && a[0].n !== c[0].n) seq++;
        }
      }
    }
    expect(seq / total).toBeGreaterThan(0.15);
  });
});
