import { describe, expect, it } from "vitest";
import { SOUND_SETS, applySoundSet } from "./sound-sets";
import type { Score } from "./score";

const mk = (): Score => ({
  tempoBpm: 160, loop: false, edition: "real",
  tracks: [
    { waveform: "square", instrument: "kick", volume: 0.3, pan: 0, notes: [{ note: "C2", durationBeats: 4 }] },
    { waveform: "square", instrument: "distGuitar", volume: 0.3, pan: -0.9, notes: [{ note: "A2", durationBeats: 4 }] },
    { waveform: "square", instrument: "distGuitar", volume: 0.3, pan: 0.9, notes: [{ note: "A2", durationBeats: 4 }] },
    { waveform: "square", instrument: "bell", volume: 0.3, pan: 0, notes: [{ note: "C5", durationBeats: 4 }] },
  ],
});

describe("サウンドセット", () => {
  it("アンプ・音量・ドラムのミックスが当たり、合計は 0.9 をこえない", () => {
    const out = applySoundSet(mk(), SOUND_SETS["punk-run"]);
    expect(out.tracks[1].amp?.type).toBe("punk");
    expect(out.tracks[1].pan).toBe(-0.55);
    expect(out.tracks[2].pan).toBe(0.55);
    expect(out.tracks[3].volume).toBeLessThanOrEqual(0.06);
    expect(out.drumMix?.tom?.tune).toBe(-3);
    expect(out.tracks.reduce((a, t) => a + t.volume, 0)).toBeLessThanOrEqual(0.9001);
  });
  it("何度当てても同じ結果で、元の曲は変わらない", () => {
    const base = mk();
    const once = applySoundSet(base, SOUND_SETS["punk-run"]);
    const twice = applySoundSet(once, SOUND_SETS["punk-run"]);
    expect(twice).toEqual(once);
    expect(base.tracks[1].volume).toBe(0.3);
    expect(base.tracks[1].amp).toBeUndefined();
  });
  it("セットの音量の合計は 0.9 以下、使う音源の名前は作曲ソフトにある", () => {
    for (const s of Object.values(SOUND_SETS)) {
      const sum = Object.values(s.parts).reduce((a, p) => a + (p?.volume ?? 0), 0);
      expect(sum).toBeLessThanOrEqual(1.6); // 同じ楽器が複数あるので、1本ぶんの合計
      expect(["std", "finger", "pick", "rock", "metal", "jazz", "jpop"]).toContain(s.overlays.bass);
      expect(["std", "muldjord", "rock", "metal", "jazz", "jpop", "supra"]).toContain(s.overlays.drums);
      expect(["std", "gretsch", "hofner"]).toContain(s.overlays.guitar);
    }
  });
});
