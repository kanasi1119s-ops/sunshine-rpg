/** リズム・グルーヴ関連のテスト用の見本曲（既存の出力が変わっていないことの確認にも使う）。 */
export const fnv = (b: Uint8Array | string): string => {
  let h = 0x811c9dc5;
  const a = typeof b === "string" ? [...b].map((c) => c.charCodeAt(0)) : b;
  for (let i = 0; i < a.length; i++) { h ^= a[i]; h = Math.imul(h, 0x01000193) >>> 0; }
  return h.toString(16);
};

const kick = "g:X.......X.x.....";
const snare = "g:....X.......X...";
const hat = "g:x.x.x.x.x.x.x.x.";

/** ロック、4/4、human・swing・push あり。 */
export const ROCK_SONG = {
  title: "rock", description: "t", bpm: 120, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 2, autoAccompaniment: false, feel: "rock", tone: "rock", human: 0.5, swing: 0.2,
  parts: [
    { instrument: "kick", role: "k", volume: 0.14, pan: 0, amp: "auto", notes: kick },
    { instrument: "snare", role: "s", volume: 0.12, pan: 0, push: 0.03, amp: "auto", notes: snare },
    { instrument: "hihat", role: "h", volume: 0.1, pan: 0.3, push: -0.01, amp: "auto", notes: hat },
    { instrument: "bass", role: "b", volume: 0.25, pan: 0, amp: "auto", notes: "A2:1 A2:0.5 C3:0.5 A2:1 E3:1 F2:1 F2:0.5 A2:0.5 F2:1 C3:1" },
    { instrument: "piano", role: "p", volume: 0.16, pan: 0.2, amp: "auto", notes: "C4:2 E4:1 D4:1 C4:2 G4:2" },
    { instrument: "lead", role: "l", volume: 0.2, pan: 0, amp: "auto", notes: "E5:1 D5:0.5 C5:0.5 A4:2 R:1 G4:1" },
  ],
};

/** ジャズ、drumGenre つき、自動伴奏あり。 */
export const JAZZ_SONG = {
  title: "jazz", description: "t", bpm: 140, beats: 4, chords: "Dm7 G7 Cmaj7 A7", barsPerChord: 1, repeats: 2, autoAccompaniment: true, feel: "jazz", tone: "rock", drumGenre: "jazz",
  parts: [{ instrument: "lead", role: "l", volume: 0.2, pan: 0, amp: "auto", notes: "F5:1 E5:1 D5:2 C5:1 B4:1 C5:2" }],
};

/** ワルツ、3/4。 */
export const WALTZ_SONG = {
  title: "waltz", description: "t", bpm: 96, beats: 3, chords: "C G Am F", barsPerChord: 1, repeats: 2, autoAccompaniment: true, feel: "pop", tone: "rock", human: 0.3,
  parts: [{ instrument: "lead", role: "l", volume: 0.2, pan: 0, amp: "auto", notes: "E5:1 G5:1 E5:1 D5:3 C5:3" }],
};

/** 三連・拍子・テンポの新しい項目を使った曲（挙動の確認用）。 */
export function newFeatureSong(extra: Record<string, unknown> = {}): Record<string, unknown> {
  return { ...ROCK_SONG, ...extra };
}

export interface MidiRead {
  ppq: number;
  tempos: { tick: number; usec: number }[];
  notes: { tick: number; ch: number; pitch: number; vel: number }[];
}

/** 標準MIDIファイルから、テンポの変わり目とノートオンだけを読む（テスト用）。 */
export function readMidi(bytes: Uint8Array): MidiRead {
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const ntrk = dv.getUint16(10);
  const ppq = dv.getUint16(12);
  let pos = 14;
  const tempos: MidiRead["tempos"] = [];
  const notes: MidiRead["notes"] = [];
  for (let t = 0; t < ntrk; t++) {
    const len = dv.getUint32(pos + 4);
    let p = pos + 8;
    const end = p + len;
    let tick = 0;
    while (p < end) {
      let delta = 0;
      let b: number;
      do { b = bytes[p++]; delta = (delta << 7) | (b & 0x7f); } while (b & 0x80);
      tick += delta;
      if (bytes[p] === 0xff) {
        const type = bytes[p + 1];
        const l = bytes[p + 2];
        if (type === 0x51) tempos.push({ tick, usec: (bytes[p + 3] << 16) | (bytes[p + 4] << 8) | bytes[p + 5] });
        p += 3 + l;
        continue;
      }
      const status = bytes[p++];
      const kind = status & 0xf0;
      if (kind === 0xc0 || kind === 0xd0) p += 1;
      else {
        if (kind === 0x90 && bytes[p + 1] > 0) notes.push({ tick, ch: status & 0x0f, pitch: bytes[p], vel: bytes[p + 1] });
        p += 2;
      }
    }
    pos = end;
  }
  return { ppq, tempos, notes };
}
