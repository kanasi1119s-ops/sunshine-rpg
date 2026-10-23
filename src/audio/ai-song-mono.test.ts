import { describe, expect, it } from "vitest";
import { applyMono, applySustain } from "./ai-song";
import { REST } from "./score";

describe("applyMono（単音の楽器として弾く）", () => {
  it("伸ばした音が次の音に重ならないよう切り、休符の前の音は伸ばしたまま残す", () => {
    const ev = applyMono(applySustain([{ note: "E4", durationBeats: 1 }, { note: "G4", durationBeats: 2 }, { note: REST, durationBeats: 2 }, { note: "A4", durationBeats: 1 }], 2));
    expect(ev[0].gate).toBeCloseTo(0.98);
    expect(ev[1].gate).toBe(1.96); // 休符（2拍）をはさんでも、次の音の頭（4拍後）まで
    expect(ev[3].gate).toBe(2);
  });
  it("休符が短くて、伸ばした音が次の音に届くときは、次の音の頭で止める", () => {
    const ev = applyMono(applySustain([{ note: "F#5", durationBeats: 1 }, { note: REST, durationBeats: 0.5 }, { note: "E4", durationBeats: 1 }], 2));
    expect(ev[0].gate).toBeCloseTo(1.47);
  });
});
