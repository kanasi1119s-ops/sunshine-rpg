import { describe, expect, it } from "vitest";
import { DRUM_KINDS, DRUM_SETTINGS, drumTailSec, isDrumKind, makeWhiteNoise } from "./drums";
import { flattenScore, REST, type Score } from "./score";

describe("DRUM_SETTINGS（打楽器の設定）", () => {
  it("主要な打楽器がそろっている", () => {
    for (const k of ["K", "S", "H", "O", "C", "T", "L", "P", "R2"]) {
      expect(isDrumKind(k)).toBe(true);
    }
  });

  it("休符の記号（R）や音名は、打楽器として扱わない", () => {
    expect(isDrumKind(REST)).toBe(false);
    expect(isDrumKind("C4")).toBe(false);
    expect(isDrumKind("")).toBe(false);
  });

  it.each(DRUM_KINDS)("%s: 設定値が正しい範囲にあり、何かしらの音が鳴る", (kind) => {
    const s = DRUM_SETTINGS[kind];
    expect(s.label.length).toBeGreaterThan(0);
    expect(s.noiseGain > 0 || s.toneGain > 0).toBe(true);
    expect(s.noiseFilterHz).toBeGreaterThan(20);
    expect(s.noiseFilterHz).toBeLessThan(20000);
    expect(s.bursts).toBeGreaterThanOrEqual(1);
    if (s.noiseGain > 0) {
      expect(s.noiseDecaySec).toBeGreaterThan(0);
    }
    if (s.toneGain > 0) {
      // 指数カーブで下げるため、周波数・時間はどれも正の値が必要
      expect(s.toneStartHz).toBeGreaterThan(0);
      expect(s.toneEndHz).toBeGreaterThan(0);
      expect(s.toneDecaySec).toBeGreaterThan(0);
    }
    expect(drumTailSec(kind)).toBeGreaterThan(0);
    expect(drumTailSec(kind)).toBeLessThan(1.5);
  });

  it("キックはハイハットより低く、長く鳴る。クラッシュはいちばん長い", () => {
    expect(DRUM_SETTINGS.K.toneEndHz).toBeLessThan(DRUM_SETTINGS.H.noiseFilterHz);
    expect(drumTailSec("K")).toBeGreaterThan(drumTailSec("H"));
    expect(drumTailSec("O")).toBeGreaterThan(drumTailSec("H"));
    for (const k of DRUM_KINDS) {
      expect(drumTailSec("C")).toBeGreaterThanOrEqual(drumTailSec(k));
    }
  });
});

describe("makeWhiteNoise", () => {
  it("指定の長さで、値は -1〜1、平均はほぼ0で、ばらつきがある", () => {
    const data = makeWhiteNoise(8000);
    expect(data).toHaveLength(8000);
    let sum = 0;
    for (const v of data) {
      expect(v).toBeGreaterThanOrEqual(-1);
      expect(v).toBeLessThanOrEqual(1);
      sum += v;
    }
    expect(Math.abs(sum / data.length)).toBeLessThan(0.05);
    expect(new Set(Array.from(data.slice(0, 100))).size).toBeGreaterThan(90);
  });

  it("同じ種なら毎回同じ音になる", () => {
    expect(Array.from(makeWhiteNoise(64, 7))).toEqual(Array.from(makeWhiteNoise(64, 7)));
    expect(Array.from(makeWhiteNoise(64, 7))).not.toEqual(Array.from(makeWhiteNoise(64, 8)));
  });
});

describe("楽譜のドラムのパート", () => {
  const score = (notes: string[]): Score => ({
    tempoBpm: 120,
    loop: false,
    tracks: [{ waveform: "noise", volume: 0.3, notes: notes.map((note) => ({ note, durationBeats: 1 })) }],
  });

  it("打楽器の記号を、ドラムの音として並べる（休符は飛ばす）", () => {
    const events = flattenScore(score(["K", REST, "S"]));
    expect(events).toHaveLength(2);
    expect(events[0].drum).toBe("K");
    expect(events[0].frequency).toBe(0);
    expect(events[1].drum).toBe("S");
    expect(events[1].startSec).toBeCloseTo(1.0, 5);
  });

  it("打楽器でない記号があると、分かりやすいエラーにする", () => {
    expect(() => flattenScore(score(["K", "C4"]))).toThrow(/打楽器でない記号/);
  });

  it("ふつうのパートでは、drum は入らない", () => {
    const events = flattenScore({
      tempoBpm: 120,
      loop: false,
      tracks: [{ waveform: "square", volume: 0.3, notes: [{ note: "C4", durationBeats: 1 }] }],
    });
    expect("drum" in events[0]).toBe(false);
  });
});
