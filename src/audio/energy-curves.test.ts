import { describe, expect, it } from "vitest";
import { aiSongToScore, AI_SONG_GUIDE, type AiSong } from "./ai-song";
import { CURVE_TABLE, EXTRA_CURVE_NAMES, curveSections, parseSectionText } from "./energy-curves";
import { ENERGY_CURVES, parseEnergy, resampleEnergy } from "./scene";

describe("エネルギー曲線の追加", () => {
  it("ガイド §3 の曲線が ENERGY_CURVES に入っている（もとの6つ＋追加）", () => {
    for (const name of ["mountain", "twoPeaks", "valley", "stairs", "flat", "bigValley", ...EXTRA_CURVE_NAMES]) expect(ENERGY_CURVES).toHaveProperty(name);
    expect(EXTRA_CURVE_NAMES.length).toBeGreaterThanOrEqual(10);
  });

  it("すべて 1〜10 で、resampleEnergy で長さが合う", () => {
    for (const [name, curve] of Object.entries(ENERGY_CURVES)) {
      expect(curve.length, name).toBeGreaterThan(0);
      for (const v of curve) { expect(v, name).toBeGreaterThanOrEqual(1); expect(v, name).toBeLessThanOrEqual(10); }
      for (const n of [1, 3, 7, 12]) expect(resampleEnergy(name as keyof typeof ENERGY_CURVES, n), `${name}/${n}`).toHaveLength(n);
    }
  });

  it("sections の数が energy の数と一致する（そのまま使える）", () => {
    for (const name of EXTRA_CURVE_NAMES) {
      expect(curveSections(name).length, name).toBe(CURVE_TABLE[name].energy.length);
    }
  });

  it("sections の合計がガイドの表の小節数どおり", () => {
    const total = (n: (typeof EXTRA_CURVE_NAMES)[number]): number => curveSections(n).reduce((a, s) => a + s.bars, 0);
    expect(total("sawtooth")).toBe(72);
    expect(total("classic")).toBe(76);
    expect(total("dropChorus")).toBe(72);
    expect(total("highFlat")).toBe(16);
    expect(total("triumph")).toBe(7);
  });

  it("parseEnergy が追加の名前を受け付ける", () => {
    const w: string[] = [];
    const layers = parseEnergy("sawtooth", undefined, 7, w);
    expect(layers).toHaveLength(7);
    expect(w).toEqual([]);
  });

  it("のこぎり：ドロップの直前（ブレイク）が谷になる", () => {
    const e = CURVE_TABLE.sawtooth.energy;
    expect(e[3]).toBeLessThan(e[2]);
    expect(e[5]).toBeGreaterThanOrEqual(e[2]);
  });

  it("山は後ほど高い（偽の終わり・定番・落ちサビ）", () => {
    for (const n of ["fakeEnd", "classic", "dropChorus"] as const) {
      const e = CURVE_TABLE[n].energy;
      expect(Math.max(...e.slice(-4)), n).toBeGreaterThanOrEqual(Math.max(...e.slice(0, 4)));
    }
  });

  it("パース: kind:小節/from", () => {
    const w: string[] = [];
    expect(parseSectionText("pre:4/riser drop:8 foo:2 verse:x", w)).toEqual([{ kind: "pre", bars: 4, from: "riser" }, { kind: "drop", bars: 8 }]);
    expect(w).toHaveLength(2);
  });

  it("AI向けの説明に曲線の名前が出る", () => {
    for (const n of EXTRA_CURVE_NAMES) expect(AI_SONG_GUIDE).toContain(n);
  });

  it("曲に energy: 名前 で書いて組み立てられる（警告なし）", () => {
    const song: AiSong = {
      title: "t", description: "d", bpm: 128, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 18, autoAccompaniment: true, feel: "dance", tone: "rock",
      form: "sawtooth", parts: [{ instrument: "lead", role: "メロディ", volume: 0.25, pan: 0, amp: "auto", notes: "A4:4" }],
    };
    const { score, warnings } = aiSongToScore(song);
    expect(score.tracks.length).toBeGreaterThan(1);
    expect(warnings.filter((w) => w.includes("energy"))).toEqual([]);
  });
});
