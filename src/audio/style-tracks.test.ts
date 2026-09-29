import { describe, expect, it } from "vitest";
import { flattenScore, getScoreDurationSec, type Instrument } from "./score";
import { STYLE_TRACKS } from "./style-tracks";

const KNOWN: Instrument[] = ["kick", "snare", "hihat", "crash", "bass", "guitar", "echoGuitar", "crunch", "distGuitar", "leadGuitar", "keys", "piano", "harpsichord", "strings", "pad", "bell", "lead", "sfxDown", "sfxUp", "impact", "swoosh", "chime", "wind", "rain", "stream", "bird", "crickets", "sub808", "cowbell", "pierce", "slap", "tom", "brass", "choir"];

describe.each(STYLE_TRACKS.map((t) => [t.title, t] as const))("新曲: %s", (_name, t) => {
  it("長さが1分〜1分半", () => {
    const sec = getScoreDurationSec(t.score);
    expect(sec).toBeGreaterThanOrEqual(60);
    expect(sec).toBeLessThanOrEqual(90);
  });
  it("全パートの合計拍数がそろっている（ループがずれない）", () => {
    const beats = t.score.tracks.map((tr) => tr.notes.reduce((s, n) => s + n.durationBeats, 0));
    for (const b of beats) expect(b).toBeCloseTo(beats[0], 6);
  });
  it("音名がすべて読め、楽器名が正しい", () => {
    expect(() => flattenScore(t.score)).not.toThrow();
    for (const tr of t.score.tracks) if (tr.instrument) expect(KNOWN).toContain(tr.instrument);
  });
  it("ループする曲で、音が鳴るパートが2つ以上ある", () => {
    expect(t.score.loop).toBe(true);
    expect(t.score.tracks.filter((tr) => tr.notes.some((n) => n.note !== "R")).length).toBeGreaterThan(1);
  });
});
