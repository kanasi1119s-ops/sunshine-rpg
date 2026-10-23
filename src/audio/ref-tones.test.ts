import { describe, expect, it } from "vitest";
import { LEAD_GUITAR, REF_TONES, applyRefTone, applyRefToneToSong } from "./ref-tones";
import type { Score } from "./score";
import type { FxSpec } from "./fx-chain";

const score = (): Score => ({
  bpm: 120, beatsPerBar: 4,
  tracks: [
    { waveform: "square", instrument: "distGuitar", volume: 0.1, pan: -0.5, notes: [], fx: [{ type: "room", mix: 0.1 }, { type: "eq", low: 0, mid: 3, midHz: 1000, high: 0 }] },
    { waveform: "square", instrument: "distGuitar", volume: 0.05, pan: 0.35, notes: [], fx: [{ type: "delay", mix: 0.25 }] },
    { waveform: "square", instrument: "bass", volume: 0.1, notes: [] },
    { waveform: "square", instrument: "snare", volume: 0.1, notes: [] },
  ],
} as unknown as Score);

describe("参考の音", () => {
  it("6つあり、どれもギター・ベース・ドラムの EQ を持つ", () => {
    expect(Object.keys(REF_TONES)).toHaveLength(6);
    for (const t of Object.values(REF_TONES)) for (const k of ["guitar", "bass", "drums"] as const) expect(t[k].length).toBeGreaterThan(0);
  });
  it("EQ とフィルターだけを置きかえ、ルームなどは残す。音量は変えない", () => {
    const tone = REF_TONES["bright-pop-rock"];
    const out = applyRefTone(score(), tone);
    const g = out.tracks[0];
    expect(g.fx?.some((f) => f.type === "room")).toBe(true);
    expect(g.fx?.filter((f) => f.type === "eq" || f.type === "filter")).toEqual(tone.guitar);
    expect(g.volume).toBe(0.1);
    expect(out.tracks[2].fx).toEqual(tone.bass);
    expect(out.tracks[3].fx).toEqual(tone.drums);
  });
  it("やまびこの付いたギター（空気の層）は「そのほか」の EQ と大きさにし、やまびこは残す", () => {
    const tone = REF_TONES["bright-pop-rock"];
    const out = applyRefTone(score(), tone);
    expect(out.tracks[1].fx?.filter((f) => f.type === "eq" || f.type === "filter")).toEqual(tone.other);
    expect(out.tracks[1].fx?.some((f) => f.type === "delay")).toBe(true);
    expect(out.tracks[1].volume).toBeCloseTo(0.05 * Math.pow(10, (tone.balanceDb?.other ?? 0) / 20), 3);
  });
  it("ベース・ドラムは大きさの比（balanceDb）を掛ける", () => {
    const tone = REF_TONES["wide-dark-wall"];
    const out = applyRefTone(score(), tone);
    expect(out.tracks[2].volume).toBeCloseTo(0.1 * Math.pow(10, (tone.balanceDb?.bass ?? 0) / 20), 3);
    expect(out.tracks[3].volume).toBeCloseTo(0.1 * Math.pow(10, (tone.balanceDb?.drums ?? 0) / 20), 3);
  });
  it("別の参考の音に選びなおしても、音量は重ならない", () => {
    const a = REF_TONES["wide-dark-wall"], b = REF_TONES["glossy-jrock"];
    const twice = applyRefTone(applyRefTone(score(), a), b), once = applyRefTone(score(), b);
    twice.tracks.forEach((t, i) => expect(t.volume).toBeCloseTo(once.tracks[i].volume, 3));
  });
  it("書き出し用（曲の JSON）: リードは歌、空気の層はそのほか、リフ・リズムは左右いっぱい（wide のとき）", () => {
    const tone = REF_TONES["wide-dark-wall"];
    const song: { parts: { role: string; instrument: string; patch?: string; volume: number; fx?: FxSpec[] }[] } = { parts: [
      { role: "看板リフ", instrument: "distGuitar", volume: 0.1, fx: [{ type: "plate", mix: 0.03 }, { type: "room", mix: 0.08 }] },
      { role: "リード（旋律）", instrument: "distGuitar", volume: 0.13, fx: [{ type: "room", mix: 0.12 }] },
      { role: "きれいな音の分散和音（空気の層）", instrument: "distGuitar", volume: 0.055, fx: [{ type: "delay", mix: 0.25 }] },
      { role: "シンバルの効果音", instrument: "guitar", patch: "cymbalFx", volume: 0.06 },
    ] };
    const out = applyRefToneToSong(song, tone) as typeof song & { parts: (typeof song.parts[number] & { double?: unknown })[] };
    expect(out.parts[0].double).toEqual({ spread: 1 });
    expect(out.parts[0].volume).toBeCloseTo(0.1 * 1.1, 3);   // BMTH のリフは 1.1倍
    expect(out.parts[0].fx?.map((f) => f.type)).not.toContain("plate");
    expect(out.parts[1].fx).toEqual(LEAD_GUITAR.fx);   // リードギターは、歌の EQ ではなくリード専用の音作り（6つで共通）
    expect((out.parts[1] as { amp?: string }).amp).toBe("namArchonL1");
    expect(out.parts[1].volume).toBeCloseTo(0.13 * Math.pow(10, (tone.balanceDb?.vocal ?? 0) / 20), 3);
    expect(out.parts[2].fx?.some((f) => f.type === "delay")).toBe(true);
    expect(out.parts[3]).toEqual(song.parts[3]);
  });
  it("guitarWide なら左右に分かれた歪みギターを左右いっぱいに", () => {
    const out = applyRefTone(score(), REF_TONES["wide-dark-wall"]);
    expect(out.tracks[0].pan).toBe(-1);
  });
  it("何度当てても同じ", () => {
    const t = REF_TONES["glossy-jrock"];
    expect(applyRefTone(applyRefTone(score(), t), t)).toEqual(applyRefTone(score(), t));
  });
});
