import { describe, expect, it } from "vitest";
import { STYLE_LABEL } from "./catalog";
import { isModernStyle, MODERN_STYLE_LABEL } from "./genres";
import { REST } from "./score";
import { composeSong, type Style } from "./songwriter";

const beats = (notes: { durationBeats: number }[]): number => notes.reduce((a, n) => a + n.durationBeats, 0);

describe("最新ジャンルの曲づくり", () => {
  const styles = Object.keys(MODERN_STYLE_LABEL) as Style[];
  it("22のジャンルが、曲の種類の一覧（STYLE_LABEL）に入っている", () => {
    expect(styles.length).toBe(22);
    for (const s of styles) expect(STYLE_LABEL[s]).toBeTruthy();
  });
  for (const style of styles) {
    it(`${style}: 全トラックの長さがそろい、音が鳴る`, () => {
      const score = composeSong({ id: "t", title: "t", scene: "", style, tonic: "F", minor: true, bpm: 0, seed: 7 });
      expect(isModernStyle(style)).toBe(true);
      expect(score.tempoBpm).toBeGreaterThan(60);
      const lens = score.tracks.map((t) => beats(t.notes));
      expect(new Set(lens.map((x) => Math.round(x * 4))).size).toBe(1);
      expect(score.tracks.some((t) => t.notes.some((n) => n.note !== REST))).toBe(true);
    });
  }
  it("同じ種なら同じ曲、種を変えると別の曲になる", () => {
    const mk = (seed: number) => JSON.stringify(composeSong({ id: "t", title: "t", scene: "", style: "trap", tonic: "C", minor: true, bpm: 140, seed }));
    expect(mk(3)).toBe(mk(3));
    expect(mk(3)).not.toBe(mk(4));
  });
});
