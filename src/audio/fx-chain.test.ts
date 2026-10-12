import { describe, expect, it } from "vitest";
import { aiSongToScore } from "./ai-song";
import { FX_INFO, FX_TYPES } from "./fx-chain";
import { scoreToMidiInfo } from "./midi-export";

const base = {
  title: "エフェクターテスト", description: "テスト", bpm: 120, beats: 4, chords: "C G Am F", barsPerChord: 1, repeats: 1,
  autoAccompaniment: false, feel: "rock", tone: "rock",
} as const;
const mk = (fx: unknown) => aiSongToScore({ ...base, parts: [{ instrument: "leadGuitar", role: "メロディ", volume: 0.3, notes: "C4:4 D4:4 E4:4 G4:4", fx }] });

describe("エフェクター（fx）", () => {
  it("22種類すべてに、日本語の名前と使いどころがある", () => {
    expect(FX_TYPES.length).toBe(22);
    for (const t of FX_TYPES) {
      expect(FX_INFO[t].label.length).toBeGreaterThan(0);
      expect(FX_INFO[t].use.length).toBeGreaterThan(0);
    }
  });
  it("beats はテンポ（120bpm）から ms に直る", () => {
    const { score } = mk([{ type: "delay", beats: 0.75, mix: 0.2 }]);
    expect(score.tracks[0].fx?.[0].ms).toBeCloseTo(375, 5);
    expect(score.tracks[0].fx?.[0].mix).toBe(0.2);
  });
  it("知らない種類は注意を出して飛ばし、書いた順を保つ", () => {
    const { score, warnings } = mk([{ type: "plate" }, { type: "ふしぎ" }, { type: "tremolo" }]);
    expect(score.tracks[0].fx?.map((f) => f.type)).toEqual(["plate", "tremolo"]);
    expect(warnings.some((w) => w.includes("ふしぎ"))).toBe(true);
  });
  it("fx がなければトラックに付かず、チャンネル別に取り出せる", () => {
    expect(mk(undefined).score.tracks[0].fx).toBeUndefined();
    const info = scoreToMidiInfo(mk([{ type: "spring" }]).score);
    expect(Object.values(info.fx)[0][0].type).toBe("spring");
  });
  it("非NAMのアンプでも ampDrive/ampLevel/ampTone が AmpSetting に入る", () => {
    const { score } = aiSongToScore({ ...base, parts: [{ instrument: "leadGuitar", role: "メロディ", volume: 0.3, notes: "C4:16", amp: "crunch", ampDrive: 0.85, ampLevel: 1.1, ampTone: -1 }] });
    expect(score.tracks[0].amp).toMatchObject({ type: "crunch", drive: 0.85, level: 1.1, tone: -1 });
  });
});
