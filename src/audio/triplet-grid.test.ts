import { describe, expect, it } from "vitest";
import { aiSongToScore, parseNotes } from "./ai-song";
import { parseTripletGrid } from "./triplet-grid";
import { scoreToMidi } from "./midi-export";
import { readMidi, ROCK_SONG } from "./rhythm-fixtures";
import { REST } from "./score";

const sum = (ns: { durationBeats: number }[]): number => ns.reduce((s, n) => s + n.durationBeats, 0);

describe("三連グリッド t:（提案4）", () => {
  it("3文字で1拍: 0.3333・0.3333・0.3334 で合計がちょうど1拍、4/4の1小節は12文字＝4拍", () => {
    const errors: string[] = [];
    const ns = parseTripletGrid("xxxxxxxxxxxx", errors, "w")!;
    expect(errors).toEqual([]);
    expect(ns.length).toBe(12);
    expect(ns.slice(0, 3).map((n) => n.durationBeats)).toEqual([0.3333, 0.3333, 0.3334]);
    expect(sum(ns.slice(0, 3))).toBeCloseTo(1, 10);
    expect(sum(ns)).toBeCloseTo(4, 10);
  });
  it("x X o O . - の意味（強さ・オープン・休み）", () => {
    const ok = parseTripletGrid("xXoO.-xxx", [], "w")!;
    expect(ok[0].velocity).toBeUndefined();
    expect(ok[1].velocity).toBe(1.3);
    expect(ok[2].velocity).toBe(0.5);
    expect(ok[3]).toMatchObject({ velocity: 1.25, open: true });
    expect(ok[4].note).toBe(REST);
    expect(ok[5].note).toBe(REST);
  });
  it("3の倍数でない・使えない文字はエラー", () => {
    const e1: string[] = [];
    expect(parseTripletGrid("xx", e1, "parts[0]")).toBeNull();
    expect(e1[0]).toContain("3の倍数");
    const e2: string[] = [];
    expect(parseTripletGrid("xaz", e2, "parts[0]")).toBeNull();
    expect(e2[0]).toContain("x X o O");
  });
  it("parseNotes: ドラムで t: が読める。ふつうのグリッド g: と混ぜられる。ドラム以外では使えない", () => {
    const errors: string[] = [];
    const ns = parseNotes("g:x...x... t:x.xx.xx.xx.x", true, errors, "w");
    expect(errors).toEqual([]);
    expect(sum(ns)).toBeCloseTo(2 + 4, 10);
    expect(ns.filter((n) => n.note !== REST).length).toBe(2 + 8);
    const errs: string[] = [];
    parseNotes("t:xxx", false, errs, "w");
    expect(errs.length).toBe(1);
  });
  it("シャッフル（1拍＝長・短の三連）を AIソングで書ける。swing の影響を受けない", () => {
    const hat = "t:x.xx.xx.xx.x";
    const song = { ...ROCK_SONG, swing: 0.8, human: 0, autoAccompaniment: false, parts: [{ instrument: "hihat", role: "h", volume: 0.1, pan: 0, amp: "auto", notes: hat }] };
    const { score } = aiSongToScore(song);
    const hatTrack = score.tracks[0];
    expect(sum(hatTrack.notes)).toBeCloseTo(32, 6); // 曲の長さまで1小節の型をくり返す
    // MIDI の位置: 1拍目の2つ目の三連は 1/3 拍＝160ティック、三連の位置が swing で動かない
    const m = readMidi(scoreToMidi(score));
    const ticks = m.notes.filter((n) => n.ch === 9).map((n) => n.tick);
    expect(ticks.slice(0, 4).map((t) => Math.round(t / 10) * 10)).toEqual([0, 320, 480, 800]);
  });
  it("三連のロール（トラップ）: 4/4の1小節を 12文字で書いて合計4拍", () => {
    const { score } = aiSongToScore({ ...ROCK_SONG, autoAccompaniment: false, parts: [{ instrument: "hihat", role: "h", volume: 0.1, pan: 0, amp: "auto", notes: "g:x.x.x.x.x.x.x.x. g:x.x.x.x.x.x.x.x. g:x.x.x.x.x.x.x.x. g:x.x.x.x.x.x.x.x. t:x.xx.xxxxxxx" }] });
    expect(score.tracks[0].notes.length).toBeGreaterThan(60);
  });
});
