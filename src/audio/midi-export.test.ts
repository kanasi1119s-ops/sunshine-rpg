import { describe, expect, it } from "vitest";
import { CATALOG, getTrack } from "./catalog";
import { USED_GM_PROGRAMS } from "./gm-map";
import { scoreToMidi } from "./midi-export";

/** 標準MIDIファイルを、最小限だけ読む（ヘッダーと各トラックの長さ・チャンネルごとの音数）。 */
function inspect(bytes: Uint8Array): { format: number; tracks: number; ppq: number; noteOns: Map<number, number>; programs: Set<number>; ticks: number } {
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  expect(String.fromCharCode(...bytes.slice(0, 4))).toBe("MThd");
  const format = dv.getUint16(8);
  const tracks = dv.getUint16(10);
  const ppq = dv.getUint16(12);
  let pos = 14;
  const noteOns = new Map<number, number>();
  const programs = new Set<number>();
  let maxTicks = 0;
  for (let t = 0; t < tracks; t++) {
    expect(String.fromCharCode(...bytes.slice(pos, pos + 4))).toBe("MTrk");
    const len = dv.getUint32(pos + 4);
    let p = pos + 8;
    const end = p + len;
    let tick = 0;
    let status = 0;
    while (p < end) {
      let delta = 0;
      let b: number;
      do {
        b = bytes[p++];
        delta = (delta << 7) | (b & 0x7f);
      } while (b & 0x80);
      tick += delta;
      if (bytes[p] === 0xff) {
        const l = bytes[p + 2];
        p += 3 + l;
        continue;
      }
      status = bytes[p++];
      const kind = status & 0xf0;
      const ch = status & 0x0f;
      if (kind === 0xc0) programs.add(bytes[p++]);
      else {
        if (kind === 0x90 && bytes[p + 1] > 0) noteOns.set(ch, (noteOns.get(ch) ?? 0) + 1);
        p += 2;
      }
    }
    maxTicks = Math.max(maxTicks, tick);
    pos = end;
  }
  return { format, tracks, ppq, noteOns, programs, ticks: maxTicks };
}

describe("MIDIへの変換（録音音源で鳴らすため）", () => {
  it("全52曲が、正しい標準MIDIファイルになり、曲の長さがぴったり合う", () => {
    for (const e of CATALOG) {
      const score = getTrack(e.id);
      const info = inspect(scoreToMidi(score));
      expect(info.format).toBe(1);
      expect(info.ppq).toBe(480);
      const beats = score.tracks[0].notes.reduce((s, n) => s + n.durationBeats, 0);
      expect(info.ticks, e.id).toBe(Math.round(beats * 480));
      expect([...info.noteOns.values()].reduce((a, b) => a + b, 0), e.id).toBeGreaterThan(50);
    }
  });
  it("ドラムはチャンネル10（番号9）に入る", () => {
    const info = inspect(scoreToMidi(getTrack("boss-touri")));
    expect(info.noteOns.get(9)).toBeGreaterThan(50);
  });
  it("使う楽器は、切り出すサウンドフォントの一覧（USED_GM_PROGRAMS）の中にある", () => {
    for (const e of CATALOG) {
      const info = inspect(scoreToMidi(getTrack(e.id)));
      for (const p of info.programs) {
        // チャンネル9のプログラム番号はドラムセット
        if ([0, 8, 16, 24, 25, 32].includes(p)) continue;
        expect(USED_GM_PROGRAMS, `${e.id}: ${p}`).toContain(p);
      }
    }
  });
});
