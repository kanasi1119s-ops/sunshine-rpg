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

describe("シンセ音色（patch）", () => {
  it("patch がGM番号になり、層が重ならない", async () => {
    const { aiSongToScore, SYNTH_PATCHES } = await import("./ai-song");
    const { score, warnings } = aiSongToScore({
      title: "t", bpm: 120, beats: 4, repeats: 1, chords: "C", barsPerChord: 1, autoAccompaniment: false,
      parts: [{ instrument: "lead", role: "r", volume: 0.2, pan: 0, amp: "auto", patch: "warmPad", notes: "C4:4" },
              { instrument: "lead", role: "x", volume: 0.2, pan: 0, amp: "auto", patch: "nope", notes: "C4:4" }],
    } as never);
    const tracks = (score as { tracks: { program?: number }[] }).tracks;
    expect(SYNTH_PATCHES.warmPad).toBe(89);
    expect(tracks[0].program).toBe(89);
    expect(tracks[1].program).toBeUndefined();
    expect(JSON.stringify(warnings)).toContain("nope");
  });
});

describe("シンセ音色は版（real）で上書きされない", () => {
  it("patch を選んだトラックの program が realEdition を通っても残る", async () => {
    const { realEdition } = await import("./real-edition");
    const { aiSongToScore } = await import("./ai-song");
    const { score } = aiSongToScore({
      title: "t", bpm: 120, beats: 4, repeats: 1, chords: "C", barsPerChord: 1, autoAccompaniment: false,
      parts: [{ instrument: "bass", role: "b", volume: 0.2, pan: 0, amp: "auto", patch: "synthBass1", notes: "C2:4" }],
    } as never);
    expect(realEdition(score).tracks[0].program).toBe(38);
  });
});

describe("人間らしさ（human）", () => {
  const mk = (human?: number): Score => ({
    tempoBpm: 120, loop: false, edition: "real",
    ...(human !== undefined ? { human } : {}),
    tracks: [
      { waveform: "sawtooth", instrument: "lead", volume: 0.2, pan: 0, notes: Array.from({ length: 16 }, () => ({ note: "A4", durationBeats: 1 })) },
      { waveform: "sine", instrument: "pad", volume: 0.1, pan: 0, notes: Array.from({ length: 4 }, () => ({ note: "C4", durationBeats: 4 })) },
      { waveform: "square", instrument: "kick", volume: 0.2, pan: 0, notes: Array.from({ length: 16 }, () => ({ note: "C2", durationBeats: 1 })) },
    ],
  });
  const hex = (b: Uint8Array): string => Array.from(b).join(",");
  const events = (b: Uint8Array, status: number, data1?: number): number => {
    let n = 0;
    for (let i = 0; i < b.length - 2; i++) if ((b[i] & 0xf0) === status && (data1 === undefined || b[i + 1] === data1) && b[i] < 0xf0) n++;
    return n;
  };
  it("0 または省略なら、これまでと同じMIDI", () => {
    expect(hex(scoreToMidi(mk(0)))).toBe(hex(scoreToMidi(mk())));
  });
  it("同じ入力なら、いつも同じ結果", () => {
    expect(hex(scoreToMidi(mk(0.6)))).toBe(hex(scoreToMidi(mk(0.6))));
  });
  it("大きくすると、音量の山（CC11）と音程のずれ（ピッチベンド）が入り、MIDIが変わる", () => {
    const plain = scoreToMidi(mk(0));
    const human = scoreToMidi(mk(0.6));
    expect(hex(human)).not.toBe(hex(plain));
    expect(events(human, 0xb0, 11)).toBeGreaterThan(events(plain, 0xb0, 11));
    expect(events(human, 0xe0)).toBeGreaterThan(events(plain, 0xe0));
  });
  it("AIソングの human がスコアに入り、0〜1に収まる", async () => {
    const { aiSongToScore } = await import("./ai-song");
    const base = { title: "t", bpm: 120, beats: 4, repeats: 1, chords: "C", barsPerChord: 1, autoAccompaniment: false, parts: [{ instrument: "lead", role: "m", volume: 0.2, pan: 0, amp: "auto", notes: "A4:4" }] };
    expect(aiSongToScore({ ...base, human: 0.5 } as never).score.human).toBe(0.5);
    expect(aiSongToScore({ ...base, human: 9 } as never).score.human).toBe(1);
    expect(aiSongToScore(base as never).score.human).toBeUndefined();
  });
});
