import { describe, expect, it } from "vitest";
import { notesToEvents, toggleNote, trackToNotes, trackTotalBeats } from "./edit";
import type { Track } from "./score";

const base: Track = { waveform: "triangle", volume: 0.2, notes: [{ note: "C4", durationBeats: 1 }, { note: "R", durationBeats: 1 }, { note: "E4", durationBeats: 2 }] };

describe("ピアノロールの編集道具", () => {
  it("トラックから位置つきの音を取り出せる（休みはのぞく）", () => {
    expect(trackToNotes(base)).toEqual([{ start: 0, dur: 1, note: "C4" }, { start: 2, dur: 2, note: "E4" }]);
  });
  it("音の一覧から、全体の長さ（4拍）にそろったトラックの列を作れる", () => {
    const events = notesToEvents(trackToNotes(base), 4);
    expect(events.reduce((s, n) => s + n.durationBeats, 0)).toBe(4);
    expect(events.map((e) => e.note)).toEqual(["C4", "R", "E4"]);
  });
  it("空いた場所をクリックすると音が足され、音の上をクリックすると消える。長さはそろったまま", () => {
    const added = toggleNote(base, 1, "G4", 1, 4);
    expect(trackTotalBeats(added)).toBe(4);
    expect(trackToNotes(added).map((n) => n.note)).toEqual(["C4", "G4", "E4"]);
    const removed = toggleNote(added, 1.5, "G4", 1, 4);
    expect(trackToNotes(removed).map((n) => n.note)).toEqual(["C4", "E4"]);
    expect(trackTotalBeats(removed)).toBe(4);
  });
  it("重なる音は、あとの音の始まりで切られる", () => {
    const empty: Track = { ...base, notes: [{ note: "R", durationBeats: 4 }] };
    const a = toggleNote(empty, 0, "A4", 4, 4); // 4拍の長い音
    const b = toggleNote(a, 3, "B4", 1, 4); // 3拍めは A4 の上なので、消える
    expect(trackToNotes(b)).toEqual([]);
    const c = toggleNote({ ...empty, notes: notesToEvents([{ start: 0, dur: 4, note: "A4" }], 4) }, 5, "B4", 1, 4); // 範囲外は足されない
    expect(trackTotalBeats(c)).toBe(4);
    const d = notesToEvents([{ start: 0, dur: 4, note: "A4" }, { start: 3, dur: 1, note: "B4" }], 4);
    expect(d.map((e) => [e.note, e.durationBeats])).toEqual([["A4", 3], ["B4", 1]]);
  });
});
