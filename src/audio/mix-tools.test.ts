import { describe, expect, it } from "vitest";
import { ROLE_DEFAULTS, addGhostLayer, applyGameDuck, checkMixRoles, duckRecoverMs, recommendDuck, reverbDecayHint, suggestPartDefaults, syncDelaySeconds } from "./mix-tools";
import type { Instrument, Score } from "./score";

const tr = (instrument: Instrument, volume: number, pan = 0, extra: Record<string, number> = {}) => ({ waveform: "square" as const, instrument, volume, pan, notes: [{ note: "C3", durationBeats: 1 }], ...extra });
const mk = (tracks: ReturnType<typeof tr>[]): Score => ({ tempoBpm: 120, loop: false, edition: "real", tracks });

describe("テンポ同期", () => {
  it("BPM 120 の長さ（秒）", () => {
    const t = syncDelaySeconds(120);
    expect(t.quarter).toBe(0.5);
    expect(t.eighth).toBe(0.25);
    expect(t.dottedEighth).toBe(0.375);
    expect(t.sixteenth).toBe(0.125);
    expect(t.eighthTriplet).toBeCloseTo(0.166667, 5);
    expect(t.bar).toBe(2);
  });
  it("BPM 128 の付点8分は 351.6ms", () => {
    expect(Math.round(syncDelaySeconds(128).dottedEighth * 10000) / 10).toBe(351.6);
  });
  it("0 以下の BPM は受けつけない", () => {
    expect(() => syncDelaySeconds(0)).toThrow();
  });
  it("残響の長さの目安は 1 拍の 0.5〜1 倍", () => {
    expect(reverbDecayHint(120)).toEqual({ min: 0.25, max: 0.5 });
  });
});

describe("duck の推奨値", () => {
  it("戻りは約 0.45 拍（BPM 174 で約 155ms、BPM 70 で約 386ms）", () => {
    expect(duckRecoverMs(174)).toBe(155);
    expect(duckRecoverMs(70)).toBe(386);
  });
  it("ベースは ロック .15〜.3、EDM はもっと深く、ジャズは浅い", () => {
    const rock = recommendDuck("bass", "rock", 120);
    expect(rock.range).toEqual([0.15, 0.3]);
    expect(recommendDuck("bass", "edm", 128).duck).toBeGreaterThan(rock.duck);
    expect(recommendDuck("bass", "jazz", 120).duck).toBeLessThan(rock.duck);
  });
  it("EDM 以外では 0.4 を超えない", () => {
    expect(recommendDuck("pad", "metal", 120).range[1]).toBeLessThanOrEqual(0.4);
  });
  it("速いテンポでは注意が付く", () => {
    expect(recommendDuck("bass", "punk", 200).notes.some((n) => n.includes("ポンピング"))).toBe(true);
  });
});

describe("ミックスの検査", () => {
  it("中央でない低域・低音の残響・音量の合計を警告する", () => {
    const w = checkMixRoles(mk([tr("kick", 0.3, 0.5), tr("bass", 0.3, 0, { reverb: 0.3 }), tr("lead", 0.4)]));
    expect(w.some((x) => x.includes("中央にありません"))).toBe(true);
    expect(w.some((x) => x.includes("残響"))).toBe(true);
    expect(w.some((x) => x.includes("合計"))).toBe(true);
  });
  it("問題のない曲は警告なし", () => {
    expect(checkMixRoles(mk([tr("kick", 0.09), tr("bass", 0.09), tr("leadGuitar", 0.1), tr("guitar", 0.07, -0.5)]))).toEqual([]);
  });
  it("違う楽器の主役が同じ値だと警告、同じ楽器の左右ペアは警告しない", () => {
    expect(checkMixRoles(mk([tr("lead", 0.1), tr("piano", 0.1)])).some((x) => x.includes("主役"))).toBe(true);
    expect(checkMixRoles(mk([tr("distGuitar", 0.1, -0.8), tr("distGuitar", 0.1, 0.8)])).some((x) => x.includes("主役"))).toBe(false);
  });
  it("同じ側に 3 パート以上で警告", () => {
    expect(checkMixRoles(mk([tr("guitar", 0.05, -0.6), tr("piano", 0.05, -0.5), tr("strings", 0.05, -0.4)])).some((x) => x.includes("左側"))).toBe(true);
  });
  it("低域のパートが 4 個で警告", () => {
    expect(checkMixRoles(mk([tr("kick", 0.05), tr("bass", 0.05), tr("sub808", 0.05), tr("slap", 0.05)])).some((x) => x.includes("3 個まで"))).toBe(true);
  });
});

describe("ゴースト層とゲーム用の席空け", () => {
  it("ゴースト層は元のパートを残して、小さく・奥に・暗い複製を足す", () => {
    const base = mk([tr("snare", 0.08), tr("kick", 0.1)]);
    const out = addGhostLayer(base, "snare");
    expect(out.tracks).toHaveLength(3);
    expect(out.tracks[2].volume).toBe(0.02);
    expect(out.tracks[2].reverb).toBe(0.25);
    expect(out.tracks[2].bright).toBe(-0.25);
    expect(base.tracks).toHaveLength(2);
    expect(addGhostLayer(base, "bell")).toBe(base);
  });
  it("1〜4kHz のパートだけ下げ、低域とドラムは変えない", () => {
    const out = applyGameDuck(mk([tr("lead", 0.1), tr("kick", 0.1), tr("bass", 0.1), tr("piano", 0.1)]), 6);
    expect(out.tracks[0].volume).toBeCloseTo(0.0501, 3);
    expect(out.tracks[1].volume).toBe(0.1);
    expect(out.tracks[2].volume).toBe(0.1);
    expect(out.tracks[3].bright).toBeCloseTo(-0.1, 5);
  });
});

describe("役割の初期値", () => {
  it("低音と旋律は中央、和音は指定した側", () => {
    expect(suggestPartDefaults("bass").pan).toBe(0);
    expect(suggestPartDefaults("melody", -1).pan).toBe(0);
    expect(suggestPartDefaults("chord", -1).pan).toBe(-0.4);
    expect(suggestPartDefaults("space", 1).reverb).toBe(ROLE_DEFAULTS.space.reverb);
  });
  it("階層: 旋律 > 低音 > 和音 > 飾り > 空気", () => {
    const v = (r: keyof typeof ROLE_DEFAULTS) => ROLE_DEFAULTS[r].volume;
    expect(v("melody")).toBeGreaterThan(v("bass"));
    expect(v("bass")).toBeGreaterThan(v("chord"));
    expect(v("chord")).toBeGreaterThan(v("ornament"));
    expect(v("ornament")).toBeGreaterThan(v("space"));
  });
});
