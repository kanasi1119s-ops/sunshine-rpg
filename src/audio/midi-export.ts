import { timeSignatureOf } from "./time-signature";
import { GM_DEFAULT_BY_WAVE, GM_DRUM_NOTE, GM_LAYER, GM_PROGRAM, METAL_LEAD, SYNTH_LEAD, SYNTH_PAD } from "./gm-map";
import { noteNameToMidi } from "./note";
import type { DrumPiece } from "./amp-rack";
import { grooveOffsetBeats, humanize, REST, type AmpSetting, type Instrument, type Score, type Track } from "./score";

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
const BOOST: Partial<Record<Instrument, number>> = { brass: 0.95, slap: 1.0, strings: 1.05, pad: 1.0, guitar: 1.0, crunch: 0.95, distGuitar: 0.9, leadGuitar: 0.95, lead: 0.9, bass: 1.05, sub808: 1.0, keys: 1.0, piano: 1.05, harpsichord: 1.05, bell: 1.0, kick: 1.0, snare: 1.0, hihat: 0.9, crash: 0.95 };
// 残響の量（MIDIのCC91）
const REVERB: Partial<Record<Instrument, number>> = { pad: 70, choir: 80, strings: 55, bell: 70, chime: 60, echoGuitar: 60, bird: 40, wind: 60, stream: 40, rain: 40, lead: 40, leadGuitar: 40, piano: 40, keys: 35, guitar: 35 };
// コーラス（音を広げる揺らぎ）の量（MIDIのCC93）
const CHORUS: Partial<Record<Instrument, number>> = { strings: 30, pad: 35, choir: 30, keys: 22, guitar: 20, echoGuitar: 20, crunch: 12, distGuitar: 8, bell: 12, harpsichord: 10 };
/** 歪ませないアンプ（これらのときは、元の音色をそのまま使う）。 */
const CLEAN_AMP_TYPES = new Set<string>(["clean", "jazz", "funk", "lofi", "retro8bit", "radio", "delicate"]);
/** キックに合わせて音量が凹む（サイドチェイン風）楽器。和音・パッド・ベース・リード。キックとドラムは凹まない。 */
const PUMP_INSTRUMENTS = new Set<Instrument>(["pad", "choir", "strings", "keys", "lead", "bell", "sub808", "bass", "echoGuitar", "harp"]);
const ECHO_INSTRUMENTS = new Set<Instrument>(["lead", "leadGuitar", "cowbell", "bell", "keys"]);

function channelKey(track: Track, program: number): string {
  return `${program}|${(track.pan ?? 0).toFixed(2)}|${track.instrument ?? track.waveform}`;
}

export function scoreToMidi(score: Score): Uint8Array {
  return scoreToMidiInfo(score).midi;
}

/** MIDIと、チャンネルごとの楽器（GMの番号）。機材（アンプ・ドラムの仕上げ）を選ぶために使う。 */
/** ドラムの太鼓ごとの分け方（楽器 → 役割）。 */
const DRUM_PIECE: Partial<Record<Instrument, DrumPiece>> = { kick: "kick", snare: "snare", hihat: "hat", crash: "cym", tom: "cym" };
/** 太鼓ごとに割り当てるチャンネル（メロディの楽器は使わない）。 */
const DRUM_PIECE_CHANNELS: Record<DrumPiece, number> = { kick: 15, snare: 14, hat: 13, cym: 12 };

/** GSの SysEx: 指定したチャンネルをドラムパートにする（ドラムキットはプログラムチェンジで選ぶ）。 */
function gsDrumPartSysex(channel: number): number[] {
  const block = channel === 9 ? 0x10 : channel < 9 ? 0x11 + channel : 0x10 + channel;
  const body = [0x40, block, 0x15, 0x01];
  const checksum = (128 - (body.reduce((a, b) => a + b, 0) % 128)) % 128;
  const data = [0x41, 0x10, 0x42, 0x12, ...body, checksum, 0xf7];
  return [0xf0, data.length, ...data];
}

/**
 * MIDIと、チャンネルごとの楽器（GMの番号）。機材（アンプ・ドラムの仕上げ）を選ぶために使う。
 * `splitDrums`: true なら、キック・スネア・ハイハット・シンバル/タムを別のチャンネル（GSのドラムパート）に分けて、
 * 太鼓ごとに別のEQ・圧縮をかけられるようにする（`drums` に役割を返す）。書き出す .mid ファイルでは使わない（GM機器で鳴らすと別の楽器になるため）。
 */
export function scoreToMidiInfo(score: Score, opts: { splitDrums?: boolean } = {}): { midi: Uint8Array; programs: Record<number, number>; amps: Record<number, { amp: AmpSetting; pan: number }>; drums: Record<number, DrumPiece> } {
  const drums: Record<number, DrumPiece> = {};
  const split = opts.splitDrums === true;
  const reserved = new Set<number>();
  if (split) {
    for (const t of score.tracks) {
      const piece = t.instrument ? DRUM_PIECE[t.instrument] : undefined;
      if (piece) reserved.add(DRUM_PIECE_CHANNELS[piece]);
    }
  }
  const programs: Record<number, number> = {};
  const amps: Record<number, { amp: AmpSetting; pan: number }> = {};
  const tracksBytes: number[][] = [];
  // 指揮者トラック（テンポと曲の長さ）
  const totalBeats = Math.max(...score.tracks.map((t) => t.notes.reduce((s, n) => s + n.durationBeats, 0)));
  const endTick = Math.round(totalBeats * PPQ);
  const usecPerBeat = Math.round(60_000_000 / score.tempoBpm);
  const conductor: number[] = [0, 0xff, 0x51, 0x03, (usecPerBeat >> 16) & 255, (usecPerBeat >> 8) & 255, usecPerBeat & 255];
  // 拍子（例: 7/8 → 分子7・分母は2の3乗）
  const sig = timeSignatureOf(score);
  conductor.push(0, 0xff, 0x58, 0x04, sig.num, Math.round(Math.log2(sig.den)), 24, 8);
  // ループの始まりと終わり（曲の頭から最後の拍まで、ぴったりくり返す）
  const marker = (text: string): number[] => [0xff, 0x06, text.length, ...[...text].map((c) => c.charCodeAt(0))];
  conductor.push(0, ...marker("loopstart"));
  conductor.push(...vlq(endTick), ...marker("loopend"));
  conductor.push(0, 0xff, 0x2f, 0x00);
  tracksBytes.push(conductor);

  const channelOf = new Map<string, number>();
  let nextChannel = 0;
  const allocate = (key: string): number => {
    let ch = channelOf.get(key);
    if (ch === undefined) {
      while (nextChannel === DRUM_CHANNEL || reserved.has(nextChannel)) nextChannel++;
      if (nextChannel > 15) {
        // チャンネルが足りないときは、同じ楽器（GMの番号）のチャンネルを使い回す（別の楽器と混ざらないように）
        const program = key.split("|")[0];
        const same = [...channelOf.entries()].find(([k]) => k.split("|")[0] === program);
        ch = same ? same[1] : reserved.has(15) ? 11 : 15;
      } else {
        ch = nextChannel;
        nextChannel++;
      }
      channelOf.set(key, ch);
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
    let program = track.program ?? (inst ? GM_PROGRAM[inst] ?? GM_DEFAULT_BY_WAVE[track.waveform] : GM_DEFAULT_BY_WAVE[track.waveform]);
    // リードとパッド: 電子音楽では電子的な音色、メタル調ではオーバードライブのギター、それ以外は生楽器に近い音色
    if (inst === "lead" && track.program === undefined) program = score.synth ? SYNTH_LEAD : score.tone === "metal" || score.tone === "prs" ? METAL_LEAD : program;
    if (inst === "pad" && score.synth && track.program === undefined) program = SYNTH_PAD;
    // 歪みの二重がけを避ける: 歪ませるアンプを指定したギターは、録音がすでに歪んだ音色（オーバードライブ29・ディストーション30）ではなく、
    // クリーン（27）を元にして、歪みはアンプだけでかける
    if (track.amp && (program === 29 || program === 30) && track.program === undefined && !CLEAN_AMP_TYPES.has(track.amp.type)) program = 27;
    const piece = split && inst ? DRUM_PIECE[inst] : undefined;
    const setupChannel = (prog: number, key: string, gainBoost: number): { channel: number; list: Ev[] } => {
      const channel = isDrum ? (piece ? DRUM_PIECE_CHANNELS[piece] : DRUM_CHANNEL) : allocate(key);
      const list = midiTrackFor(channel);
      if (isDrum) {
        if (!list.some((e) => e.bytes[0] === (0xc0 | channel))) {
          if (piece) {
            list.push({ tick: 0, order: 0, bytes: gsDrumPartSysex(channel) });
            drums[channel] = piece;
            // 太鼓ごとの左右の位置（曲のパートの pan）
            list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 10, Math.max(0, Math.min(127, Math.round(64 + (track.pan ?? 0) * 63)))] });
          }
          list.push({ tick: 0, order: 0, bytes: [0xc0 | channel, score.drumKit ?? 0] });
        }
      } else if (!list.some((e) => e.bytes[0] === (0xc0 | channel))) {
        const pan = Math.round(64 + (track.pan ?? 0) * 63);
        list.push({ tick: 0, order: 0, bytes: [0xc0 | channel, prog] });
        list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 7, Math.round(118 * gainBoost)] });
        list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 10, Math.max(0, Math.min(127, pan))] });
        list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 91, inst ? REVERB[inst] ?? 30 : 30] });
        list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 93, inst ? CHORUS[inst] ?? 0 : 0] });
        // 主旋律の楽器には、揺らぎ（ビブラート）を少し
        if (inst === "leadGuitar" || inst === "lead" || inst === "brass") list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 1, score.tone === "prs" ? 40 : 26] });
      }
      return { channel, list };
    };
    const main = setupChannel(program, channelKey(track, program), 1);
    const channel = main.channel;
    if (!isDrum) programs[channel] = program;
    if (!isDrum && track.amp) amps[channel] = { amp: track.amp, pan: track.pan ?? 0 };
    const list = main.list;
    const layerSpec = inst ? GM_LAYER[inst] : undefined;
    const layer = layerSpec ? setupChannel(layerSpec.program, `${channelKey(track, layerSpec.program)}|layer`, 1) : null;
    if (layer && layer.channel !== DRUM_CHANNEL) programs[layer.channel] = layerSpec!.program;
    // ピアノ系は、およそ1小節ごとにペダルを踏み替えて、音をつなげる
    if (inst === "piano" || inst === "keys") {
      const totalTicks = endTick;
      for (let at = 0; at < totalTicks; at += PPQ * 4) {
        for (const c of layer ? [channel, layer.channel] : [channel]) {
          const l = c === channel ? list : layer!.list;
          if (at > 0) l.push({ tick: at - 6, order: 1, bytes: [0xb0 | c, 64, 0] });
          l.push({ tick: at, order: 1, bytes: [0xb0 | c, 64, 127] });
        }
      }
    }
    // キックに合わせた音量の凹み（電子音楽風のポンプ感）。1拍ごとに、頭で凹んで、次の拍に向かって戻る
    if (score.pump && inst && PUMP_INSTRUMENTS.has(inst)) {
      for (let at = 0; at < endTick; at += PPQ) {
        list.push({ tick: at, order: 1, bytes: [0xb0 | channel, 11, 62] });
        list.push({ tick: at + Math.round(PPQ * 0.3), order: 1, bytes: [0xb0 | channel, 11, 100] });
        list.push({ tick: at + Math.round(PPQ * 0.65), order: 1, bytes: [0xb0 | channel, 11, 127] });
      }
    }
    const boost = inst ? BOOST[inst] ?? 1 : 1;
    let beat = 0;
    for (const n of track.notes) {
      const startBeat = beat;
      beat += n.durationBeats;
      if (n.note === REST) continue;
      const secStart = (startBeat * 60) / score.tempoBpm;
      // 手で弾いたような、ごくわずかなタイミングのずれ（鍵盤・ギター・ベース）
      // 実楽器版は、人が演奏するように、タイミングのずれを大きめに
      const human = score.edition === "real" ? 1.6 : 1;
      const looseness = human * (inst && ["keys", "piano", "guitar", "echoGuitar", "bass", "harpsichord", "strings", "lead", "leadGuitar", "brass", "crunch", "distGuitar"].includes(inst) ? 70 : inst && ["kick", "snare", "hihat", "tom", "crash"].includes(inst) ? 45 : 0);
      const jitter = looseness > 0 && startBeat > 0 ? Math.round((humanize(secStart + 3.7) - 1) * looseness) : 0;
      const grooveTicks = Math.round(grooveOffsetBeats(score.swing, track.push, startBeat) * PPQ);
      const tick = Math.max(0, Math.round(startBeat * PPQ) + jitter + grooveTicks);
      let vol = track.volume * (n.velocity ?? 1) * (inst ? humanize(secStart) : 1);
      let drumKey = drumNote;
      let lenScale = drumNote !== undefined ? 0.5 : 0.97;
      if (inst === "hihat") {
        // 表拍は強く、裏拍は弱く。16分の細かい音はさらに弱く。ときどき開いたハイハット
        const frac = startBeat - Math.floor(startBeat);
        vol *= frac === 0 ? 1.15 : Math.abs(frac - 0.5) < 1e-6 ? 0.85 : 0.62;
        if (Math.abs(frac - 0.75) < 1e-6 && humanize(secStart + 1.3) < 0.95) {
          drumKey = 46;
          lenScale = 1;
        }
      } else if (inst === "snare") {
        vol *= 1 + (humanize(secStart + 9.1) - 1) * 1.5;
      } else if (inst === "crash") {
        lenScale = 3;
      }
      // 曲の頭の2拍は強く（聴き手をつかむ、最初の一撃）
      const strike = score.opening && startBeat < 2 ? 1.22 : 1;
      // 特別曲用（prs）の刻みギターは、強すぎないよう控えめに
      const rhythmSoft = score.tone === "prs" && (inst === "distGuitar" || inst === "crunch") ? 0.78 : 1;
      const velocity = Math.min(127, Math.round(velocityOf(vol, boost) * strike * rhythmSoft));
      const len = Math.max(20, Math.round(n.durationBeats * PPQ * lenScale * (drumNote === undefined ? n.gate ?? 1 : 1)));
      const push = (pitch: number, at: number, vel: number, length: number, target: { channel: number; list: Ev[] } = { channel, list }): void => {
        const p = Math.max(0, Math.min(127, pitch));
        target.list.push({ tick: at, order: 2, bytes: [0x90 | target.channel, p, vel] });
        target.list.push({ tick: Math.min(at + length, endTick), order: 0, bytes: [0x80 | target.channel, p, 0] });
      };
      if (drumKey !== undefined) {
        push(drumKey, tick, velocity, len);
        // 厚みとパンチ: キックは別のバスドラムを重ね、スネアはポップ・ロック系のセットで手拍子を薄く重ねる
        if (inst === "kick") push(35, tick, Math.round(velocity * 0.55), len);
        if (inst === "snare" && [8, 16, 24, 25].includes(score.drumKit ?? 0)) push(score.tone === "metal" || score.tone === "prs" ? 40 : 39, tick, Math.round(velocity * (score.tone === "metal" || score.tone === "prs" ? 0.55 : 0.32)), len);
        continue;
      }
      const pitch = noteNameToMidi(n.note);
      // ギターの長い音は、下から音程を持ち上げて入る（ベンド）。ほかの音に影響しないよう、音の後で戻す
      if ((inst === "leadGuitar" || inst === "guitar") && n.durationBeats >= 1 && startBeat > 0) {
        const bendFrom = 0x2000 - 0x1000;
        const setBend = (at: number, v: number): void => {
          list.push({ tick: Math.max(0, at), order: 1, bytes: [0xe0 | channel, v & 0x7f, (v >> 7) & 0x7f] });
        };
        setBend(tick - 3, bendFrom);
        setBend(tick + 16, 0x2000 - 0x800);
        setBend(tick + 34, 0x2000);
      }
      push(pitch, tick, velocity, len);
      if (layer && layerSpec) push(pitch, tick, Math.max(14, Math.round(velocity * layerSpec.gain)), len, layer);
      if (inst === "crunch" || inst === "distGuitar") push(pitch + 7, tick, velocity, len); // パワーコードの5度
      if (inst === "distGuitar" && score.tone !== "prs") push(pitch + 12, tick, Math.round(velocity * 0.45), len);
      // 重低音: メタルのベースには、1オクターブ下の音を重ねる
      if (score.tone !== "rock" && score.tone !== undefined && (inst === "bass" || inst === "slap") && pitch - 12 >= 23) push(pitch - 12, tick, Math.round(velocity * 0.6), len);
      // 重さ: ディストーションギターには、1オクターブ下の音を薄く重ねる
      if ((inst === "distGuitar" || inst === "crunch") && pitch - 12 >= 28) push(pitch - 12, tick, Math.round(velocity * (score.tone === "prs" ? 0.25 : 0.45)), len);
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

  // 曲の頭の一撃: クラッシュとバスドラムを最大の強さで、同時に鳴らす（ループのたびに、聴き手をつかむ）
  if (score.opening) {
    const list = midiTrackFor(DRUM_CHANNEL);
    if (!list.some((e) => e.bytes[0] === 0xc9)) list.push({ tick: 0, order: 0, bytes: [0xc9, score.drumKit ?? 0] });
    for (const [note, vel, len] of [[49, 127, PPQ * 3], [36, 127, 200], [35, 110, 200], [38, 96, 200]] as const) {
      list.push({ tick: 0, order: 2, bytes: [0x99, note, vel] });
      list.push({ tick: Math.min(len, endTick), order: 0, bytes: [0x89, note, 0] });
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
  return { midi: Uint8Array.from(out), programs, amps, drums };
}
