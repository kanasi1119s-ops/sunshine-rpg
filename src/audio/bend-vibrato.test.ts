import { describe, expect, it } from "vitest";
import { parseNotes } from "./ai-song";
import { bendCurve, scoreToMidi } from "./midi-export";
import type { Score } from "./score";

/** MIDIから、指定の種類（ピッチベンド=0xE0、コントローラ=0xB0）のイベントを、（時刻, チャンネル, 値）で取り出す。 */
function events(bytes: Uint8Array, kind: number): { tick: number; ch: number; a: number; b: number }[] {
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const tracks = dv.getUint16(10);
  let pos = 14;
  const out: { tick: number; ch: number; a: number; b: number }[] = [];
  for (let t = 0; t < tracks; t++) {
    const len = dv.getUint32(pos + 4);
    let p = pos + 8;
    const end = p + len;
    let tick = 0;
    while (p < end) {
      let delta = 0;
      let b: number;
      do {
        b = bytes[p++];
        delta = (delta << 7) | (b & 0x7f);
      } while (b & 0x80);
      tick += delta;
      if (bytes[p] === 0xff) {
        p += 3 + bytes[p + 2];
        continue;
      }
      const status = bytes[p++];
      const k = status & 0xf0;
      if (k === 0xc0) p += 1;
      else {
        if (k === kind) out.push({ tick, ch: status & 15, a: bytes[p], b: bytes[p + 1] });
        p += 2;
      }
    }
    pos = end;
  }
  return out;
}

const bend14 = (e: { a: number; b: number }): number => e.a | (e.b << 7);
const semis = (e: { a: number; b: number }): number => ((bend14(e) - 0x2000) / 0x2000) * 12;

function song(notes: Score["tracks"][0]["notes"], instrument: "piano" | "bass" | "leadGuitar" = "piano"): Score {
  return {
    id: "t",
    name: "t",
    tempoBpm: 120,
    loop: false,
    tracks: [{ instrument, waveform: "sine", volume: 0.2, notes }],
  } as unknown as Score;
}

describe("ピッチベンドとビブラート", () => {
  it("ベンドの指定がなければ、ピアノにはピッチベンドが入らない", () => {
    const midi = scoreToMidi(song([{ note: "C4", durationBeats: 2 }, { note: "E4", durationBeats: 2 }]));
    expect(events(midi, 0xe0).length).toBe(0);
  });
  it("bend: 2 なら、音のあいだに全音ぶん持ち上がり、終わりで元に戻る", () => {
    const midi = scoreToMidi(song([{ note: "C4", durationBeats: 1 }, { note: "E4", durationBeats: 2, bend: 2 }, { note: "G4", durationBeats: 1 }]));
    const ev = events(midi, 0xe0);
    expect(ev.length).toBeGreaterThan(5);
    const values = ev.map(semis);
    expect(Math.max(...values)).toBeCloseTo(2, 1);
    expect(Math.min(...values)).toBeGreaterThan(-0.01);
    expect(values[values.length - 1]).toBeCloseTo(0, 5);
    // 値はなめらかに増える（途中で後戻りしない）
    const up = values.slice(0, values.indexOf(Math.max(...values)) + 1);
    for (let i = 1; i < up.length; i++) expect(up[i]).toBeGreaterThanOrEqual(up[i - 1] - 1e-9);
  });
  it("scoop: 1 なら、半音下から入って元の音程へ上がる", () => {
    const midi = scoreToMidi(song([{ note: "C4", durationBeats: 1 }, { note: "E4", durationBeats: 2, scoop: 1 }]));
    const ev = events(midi, 0xe0);
    expect(semis(ev[0])).toBeCloseTo(-1, 1);
    expect(semis(ev[ev.length - 1])).toBeCloseTo(0, 5);
  });
  it("fall: 2 なら、音の終わりへ向けて全音下がる", () => {
    const midi = scoreToMidi(song([{ note: "E4", durationBeats: 2, fall: 2 }, { note: "G4", durationBeats: 1 }]));
    const values = events(midi, 0xe0).map(semis);
    expect(Math.min(...values)).toBeLessThan(-1.5);
    expect(values[values.length - 1]).toBeCloseTo(0, 5);
  });
  it("vibrato: 音が出て少したってからモジュレーション（CC1）が上がり、終わりで戻る", () => {
    const midi = scoreToMidi(song([{ note: "E4", durationBeats: 2, vibrato: 1 }, { note: "G4", durationBeats: 1 }]));
    const cc1 = events(midi, 0xb0).filter((e) => e.a === 1);
    const values = cc1.map((e) => e.b);
    expect(Math.max(...values)).toBe(127);
    expect(values[values.length - 1]).toBe(0);
    const ramp = cc1.filter((e) => e.b > 0);
    expect(ramp[0].tick).toBeGreaterThan(0);
  });
  it("ベンドの幅（RPN 0）が ±12半音に設定される", () => {
    const midi = scoreToMidi(song([{ note: "E4", durationBeats: 2, bend: 1 }]));
    const cc = events(midi, 0xb0);
    expect(cc.some((e) => e.a === 6 && e.b === 12)).toBe(true);
  });
  it("短すぎる音（0.1拍）にはベンドをかけない", () => {
    const midi = scoreToMidi(song([{ note: "E4", durationBeats: 0.1, bend: 2 }, { note: "G4", durationBeats: 3.9 }]));
    expect(events(midi, 0xe0).length).toBe(0);
  });
  it("bendCurve: 指定がなければ null", () => {
    expect(bendCurve({}, 480)).toBeNull();
    expect(bendCurve({ bend: 1 }, 480)?.(480)).toBeCloseTo(1, 5);
  });
});

describe("AIソング形式の記号 ~ ^ / \\", () => {
  const parse = (text: string) => {
    const errors: string[] = [];
    const notes = parseNotes(text, false, errors, "t");
    return { notes, errors };
  };
  it("~ はビブラート、~~ は深いビブラート", () => {
    const { notes, errors } = parse("E5:2~ E5:2~~");
    expect(errors).toEqual([]);
    expect(notes[0].vibrato).toBe(0.7);
    expect(notes[1].vibrato).toBe(1);
  });
  it("^ は半音、^^ は全音のベンドアップ", () => {
    const { notes } = parse("A4:1^ A4:1^^");
    expect(notes[0].bend).toBe(1);
    expect(notes[1].bend).toBe(2);
  });
  it("/ はしゃくり、\\ はフォール", () => {
    const { notes, errors } = parse("A4:1/ A4:1// A4:1\\ A4:1\\\\");
    expect(errors).toEqual([]);
    expect(notes[0].scoop).toBe(1);
    expect(notes[1].scoop).toBe(2);
    expect(notes[2].fall).toBe(1);
    expect(notes[3].fall).toBe(2);
  });
  it("記号は重ねられる（アクセント＋ビブラート＋ベンド）", () => {
    const { notes, errors } = parse("A4:2!^^~");
    expect(errors).toEqual([]);
    expect(notes[0]).toMatchObject({ velocity: 1.3, bend: 2, vibrato: 0.7 });
  });
});
