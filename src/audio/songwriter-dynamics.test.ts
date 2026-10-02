import { describe, expect, it } from "vitest";
import { composeSong } from "./songwriter";

describe("曲の起伏（S-5）", () => {
  it("出だしの小節は、サビ付近より小さく鳴る", () => {
    const score = composeSong({ style: "jpop", tonic: "C", minor: false, bpm: 120, seed: 7, targetSec: 90 } as never);
    const mean = (from: number, to: number): number => {
      let sum = 0;
      let n = 0;
      for (const t of score.tracks) {
        let pos = 0;
        for (const ev of t.notes) {
          if (pos >= from * 4 && pos < to * 4 && ev.note !== "R") {
            sum += ev.velocity ?? 1;
            n++;
          }
          pos += ev.durationBeats;
        }
      }
      return n ? sum / n : 0;
    };
    expect(mean(0, 2)).toBeLessThan(mean(14, 20) * 0.85);
  });
});
