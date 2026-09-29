import { describe, expect, it } from "vitest";
import { addNotes, copyNotes, moveNotes, noteStartAt, notesInRange, notesToEvents, pasteNotes, removeNotes, resizeNote, setNotesLength, toggleNote, trackToNotes, trackTotalBeats } from "./edit";
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

  it("音の長さを変えられる（のばす・縮める）。全体の長さはそろったまま", () => {
    const longer = resizeNote(base, 0, 2, 4);
    expect(longer.notes.map((e) => [e.note, e.durationBeats])).toEqual([["C4", 2], ["E4", 2]]);
    const shorter = resizeNote(base, 2, 0.5, 4);
    expect(shorter.notes.map((e) => [e.note, e.durationBeats])).toEqual([["C4", 1], ["R", 1], ["E4", 0.5], ["R", 1.5]]);
    expect(trackTotalBeats(shorter)).toBe(4);
    expect(resizeNote(base, 1, 2, 4)).toBe(base);
  });
  it("位置を覆っている音の始まりを返す", () => {
    expect(noteStartAt(base, 3)).toBe(2);
    expect(noteStartAt(base, 1.5)).toBeNull();
  });
});

describe("複数の音の選択と編集", () => {
  const mk = (): Track => ({ waveform: "sine", volume: 0.2, notes: notesToEvents([{ start: 0, dur: 1, note: "C4" }, { start: 1, dur: 1, note: "D4" }, { start: 2, dur: 1, note: "E4" }], 8) });
  const up = (n: string, s: number): string => ({ C4: "D4", D4: "E4", E4: "F#4" } as Record<string, string>)[n] ?? (s ? n : n);
  it("範囲で選べる（音の高さでもしぼれる）", () => {
    expect(notesInRange(mk(), 0.5, 1.5)).toEqual([0, 1]);
    const pitch = (n: string): number => ({ C4: 60, D4: 62, E4: 64 } as Record<string, number>)[n];
    expect(notesInRange(mk(), 0, 8, 61, 70, pitch)).toEqual([1, 2]);
  });
  it("選んだ音を動かせる（曲の外へははみ出さない）", () => {
    const r = moveNotes(mk(), [1, 2], 2, 2, up);
    expect(trackToNotes(r.track)).toEqual([{ start: 0, dur: 1, note: "C4" }, { start: 3, dur: 1, note: "E4" }, { start: 4, dur: 1, note: "F#4" }]);
    expect(r.starts).toEqual([3, 4]);
    expect(moveNotes(mk(), [2], 100, 0, up).starts).toEqual([7]);
    expect(moveNotes(mk(), [0], -3, 0, up).starts).toEqual([0]);
  });
  it("コピーと貼り付け・長さをそろえる・消す", () => {
    const clip = copyNotes(mk(), [1, 2]);
    expect(clip).toEqual([{ start: 0, dur: 1, note: "D4" }, { start: 1, dur: 1, note: "E4" }]);
    const p = pasteNotes(mk(), clip, 6.5);
    expect(trackToNotes(p.track).slice(3)).toEqual([{ start: 6.5, dur: 1, note: "D4" }, { start: 7.5, dur: 0.5, note: "E4" }]);
    expect(trackTotalBeats(p.track)).toBe(8);
    expect(trackToNotes(setNotesLength(mk(), [0], 0.5))[0].dur).toBe(0.5);
    expect(trackToNotes(removeNotes(mk(), [0, 2])).map((n) => n.note)).toEqual(["D4"]);
  });
  it("足す音と重なる元の音は、上書きされる", () => {
    const t = addNotes(mk(), [{ start: 0.5, dur: 1, note: "G4" }], 8);
    expect(trackToNotes(t)).toEqual([{ start: 0.5, dur: 1, note: "G4" }, { start: 2, dur: 1, note: "E4" }]);
  });
});
