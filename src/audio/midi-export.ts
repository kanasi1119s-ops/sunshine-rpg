import { GM_DEFAULT_BY_WAVE, GM_DRUM_NOTE, GM_PROGRAM } from "./gm-map";
import { noteNameToMidi } from "./note";
import { humanize, REST, type Instrument, type Score, type Track } from "./score";

/**
 * 曲（Score）を、録音音源（サウンドフォント）で鳴らすための標準MIDIファイル（SMF）に変換する。
 * 楽器はGMの番号に置き換え、ドラムはチャンネル10、左右の位置（pan）・残響・強さも引き継ぐ。
 */

const PPQ = 480;
const DRUM_CHANNEL = 9;

interface Ev {
  tick: number;
  /** 同じ時刻の順序（ノートオフ→その他→ノートオン）。 */
  order: number;
  bytes: number[];
}

function vlq(n: number): number[] {
  const out = [n & 0x7f];
  n >>= 7;
  while (n > 0) {
    out.unshift((n & 0x7f) | 0x80);
    n >>= 7;
  }
  return out;
}
const u32 = (n: number): number[] => [(n >>> 24) & 255, (n >>> 16) & 255, (n >>> 8) & 255, n & 255];
const u16 = (n: number): number[] => [(n >>> 8) & 255, n & 255];

/** 音の強さ（0〜127）。トラックの音量0〜0.3ほどを、MIDIの強さへ。 */
function velocityOf(volume: number, boost: number): number {
  return Math.max(18, Math.min(127, Math.round((34 + volume * 430) * boost)));
}

// 楽器ごとの強さの補正（録音音源は楽器によって元の大きさが違うため）
const BOOST: Partial<Record<Instrument, number>> = { strings: 1.05, pad: 1.0, guitar: 1.0, crunch: 0.95, distGuitar: 0.9, leadGuitar: 0.95, lead: 0.9, bass: 1.05, sub808: 1.0, keys: 1.0, piano: 1.05, harpsichord: 1.05, bell: 1.0, kick: 1.0, snare: 1.0, hihat: 0.9, crash: 0.95 };
// 残響の量（MIDIのCC91）
const REVERB: Partial<Record<Instrument, number>> = { pad: 70, strings: 55, bell: 70, chime: 60, echoGuitar: 60, bird: 40, wind: 60, stream: 40, rain: 40, lead: 40, leadGuitar: 40, piano: 40, keys: 35, guitar: 35 };
const ECHO_INSTRUMENTS = new Set<Instrument>(["lead", "leadGuitar", "cowbell", "bell", "keys"]);

function channelKey(track: Track, program: number): string {
  return `${program}|${(track.pan ?? 0).toFixed(2)}|${track.instrument ?? track.waveform}`;
}

export function scoreToMidi(score: Score): Uint8Array {
  const tracksBytes: number[][] = [];
  // 指揮者トラック（テンポと曲の長さ）
  const totalBeats = Math.max(...score.tracks.map((t) => t.notes.reduce((s, n) => s + n.durationBeats, 0)));
  const endTick = Math.round(totalBeats * PPQ);
  const usecPerBeat = Math.round(60_000_000 / score.tempoBpm);
  const conductor: number[] = [0, 0xff, 0x51, 0x03, (usecPerBeat >> 16) & 255, (usecPerBeat >> 8) & 255, usecPerBeat & 255];
  conductor.push(...vlq(endTick), 0xff, 0x2f, 0x00);
  tracksBytes.push(conductor);

  const channelOf = new Map<string, number>();
  let nextChannel = 0;
  const allocate = (key: string): number => {
    let ch = channelOf.get(key);
    if (ch === undefined) {
      if (nextChannel === DRUM_CHANNEL) nextChannel++;
      ch = Math.min(nextChannel, 15);
      if (ch === DRUM_CHANNEL) ch = 14;
      channelOf.set(key, ch);
      nextChannel++;
    }
    return ch;
  };

  const events: Ev[][] = [];
  const setup = new Map<number, Ev[]>();
  const midiTrackFor = (channel: number): Ev[] => {
    let list = setup.get(channel);
    if (!list) {
      list = [];
      setup.set(channel, list);
      events.push(list);
    }
    return list;
  };

  for (const track of score.tracks) {
    const inst = track.instrument;
    const drumNote = inst ? GM_DRUM_NOTE[inst] : undefined;
    const isDrum = drumNote !== undefined;
    const program = inst ? GM_PROGRAM[inst] ?? GM_DEFAULT_BY_WAVE[track.waveform] : GM_DEFAULT_BY_WAVE[track.waveform];
    const channel = isDrum ? DRUM_CHANNEL : allocate(channelKey(track, program));
    const list = midiTrackFor(channel);
    if (channel === DRUM_CHANNEL) {
      if (!list.some((e) => e.bytes[0] === 0xc9)) list.push({ tick: 0, order: 0, bytes: [0xc9, score.drumKit ?? 0] });
    } else if (!list.some((e) => e.bytes[0] === (0xc0 | channel))) {
      const pan = Math.round(64 + (track.pan ?? 0) * 63);
      list.push({ tick: 0, order: 0, bytes: [0xc0 | channel, program] });
      list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 7, 118] });
      list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 10, Math.max(0, Math.min(127, pan))] });
      list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 91, inst ? REVERB[inst] ?? 30 : 30] });
    }
    const boost = inst ? BOOST[inst] ?? 1 : 1;
    let beat = 0;
    for (const n of track.notes) {
      const startBeat = beat;
      beat += n.durationBeats;
      if (n.note === REST) continue;
      const tick = Math.round(startBeat * PPQ);
      const secStart = (startBeat * 60) / score.tempoBpm;
      const vol = track.volume * (n.velocity ?? 1) * (inst ? humanize(secStart) : 1);
      const velocity = velocityOf(vol, boost);
      const len = Math.max(20, Math.round(n.durationBeats * PPQ * (drumNote !== undefined ? 0.5 : 0.97)));
      const push = (pitch: number, at: number, vel: number, length: number): void => {
        const p = Math.max(0, Math.min(127, pitch));
        list.push({ tick: at, order: 2, bytes: [0x90 | channel, p, vel] });
        list.push({ tick: Math.min(at + length, endTick), order: 0, bytes: [0x80 | channel, p, 0] });
      };
      if (drumNote !== undefined) {
        push(drumNote, tick, velocity, len);
        continue;
      }
      const pitch = noteNameToMidi(n.note);
      push(pitch, tick, velocity, len);
      if (inst === "crunch" || inst === "distGuitar") push(pitch + 7, tick, velocity, len); // パワーコードの5度
      if (inst === "distGuitar") push(pitch + 12, tick, Math.round(velocity * 0.8), len);
      // 主旋律のエコー（付点8分・付点4分）。テンポに合わせて、少しずつ小さく
      if (inst && ECHO_INSTRUMENTS.has(inst) && n.durationBeats >= 0.4) {
        for (const [beats, gain] of [[0.75, 0.42], [1.5, 0.22]] as const) {
          const at = tick + Math.round(beats * PPQ);
          if (at < endTick) push(pitch, at, Math.max(14, Math.round(velocity * gain)), Math.min(len, PPQ));
        }
      }
      if (inst === "echoGuitar") {
        for (const [beats, gain] of [[1, 0.5], [2, 0.25], [3, 0.12]] as const) {
          const at = tick + Math.round(beats * PPQ);
          if (at < endTick) push(pitch, at, Math.max(14, Math.round(velocity * gain)), Math.min(len, PPQ));
        }
      }
    }
  }

  for (const list of events) {
    list.sort((a, b) => a.tick - b.tick || a.order - b.order);
    const bytes: number[] = [];
    let prev = 0;
    for (const e of list) {
      bytes.push(...vlq(e.tick - prev), ...e.bytes);
      prev = e.tick;
    }
    bytes.push(...vlq(Math.max(0, endTick - prev)), 0xff, 0x2f, 0x00);
    tracksBytes.push(bytes);
  }

  const out: number[] = [0x4d, 0x54, 0x68, 0x64, ...u32(6), ...u16(1), ...u16(tracksBytes.length), ...u16(PPQ)];
  for (const t of tracksBytes) out.push(0x4d, 0x54, 0x72, 0x6b, ...u32(t.length), ...t);
  return Uint8Array.from(out);
}
