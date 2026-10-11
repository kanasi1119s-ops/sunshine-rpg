import { timeSignatureOf } from "./time-signature";
import { GM_DEFAULT_BY_WAVE, GM_DRUM_NOTE, GM_LAYER, GM_PROGRAM, METAL_LEAD, SYNTH_LEAD, SYNTH_PAD } from "./gm-map";
import { noteNameToMidi } from "./note";
import { grooveOffsetBeats, humanize, REST, velocityScale, type AmpSetting, type Instrument, type Score, type Track } from "./score";
import { pushBeatsOf, swingOf, trackHumanMult, triangular } from "./groove-feel";
import { makeTempoClock } from "./tempo-map";

/**
 * 曲（Score）を、録音音源（サウンドフォント）で鳴らすための標準MIDIファイル（SMF）に変換する。
 * 楽器はGMの番号に置き換え、ドラムはチャンネル10、左右の位置（pan）・残響・強さも引き継ぐ。
 */

const PPQ = 480;
const DRUM_CHANNEL = 9;
/** ピッチベンドの幅（半音）。チャンネルごとに RPN で設定する。±12半音を 0〜16383 に割りあてる。 */
const BEND_RANGE = 12;
const bendValue = (semitones: number): number => Math.max(0, Math.min(0x3fff, Math.round(0x2000 + (semitones / BEND_RANGE) * 0x2000)));
const clampSemi = (x: number): number => Math.max(-BEND_RANGE, Math.min(BEND_RANGE, x));
const smooth = (x: number): number => {
  const t = Math.max(0, Math.min(1, x));
  return t * t * (3 - 2 * t);
};

/**
 * 1つの音の、ピッチベンドの動き（相対時刻[tick] → 半音数）。
 * しゃくり・ベンド・フォールを重ねたもの。何も指定がなければ null。
 */
export function bendCurve(n: { bend?: number; scoop?: number; fall?: number; slide?: number; bendT?: number; scoopT?: number; fallAt?: number }, durTicks: number): ((rel: number) => number) | null {
  const bend = clampSemi(n.bend ?? 0);
  const scoop = clampSemi(n.scoop ?? 0);
  const fall = clampSemi(n.fall ?? 0);
  const slide = clampSemi(n.slide ?? 0);
  if (!bend && !scoop && !fall && !slide) return null;
  // 形のパラメータ（bendT＝上がる拍数、scoopT＝しゃくりの拍数、fallAt＝戻し始める位置の割合）。省略は今までの値
  const scoopEnd = Math.max(1, n.scoopT ? Math.min(durTicks, n.scoopT * PPQ) : Math.min(durTicks * 0.4, PPQ * 0.3));
  const bendEnd = Math.max(1, n.bendT ? Math.min(durTicks, n.bendT * PPQ) : Math.min(durTicks * 0.35, PPQ * 0.5));
  const fallStart = durTicks * (n.fallAt ?? 0.7);
  // スライド: 音の 15% から 75% の間で、行き先の音程までなめらかに動く
  const slideStart = durTicks * 0.15;
  const slideLen = Math.max(1, durTicks * 0.6);
  return (rel) => {
    const sc = scoop && rel < scoopEnd ? -scoop * (1 - smooth(rel / scoopEnd)) : 0;
    const bd = bend ? bend * smooth(rel / bendEnd) : 0;
    const fl = fall && rel > fallStart ? -fall * smooth((rel - fallStart) / Math.max(1, durTicks - fallStart)) : 0;
    const sl = slide ? slide * smooth((rel - slideStart) / slideLen) : 0;
    return sc + bd + fl + sl;
  };
}

/** グライド（アームの揺れ）: 2 つの正弦波（速さ比 1 : 1.7）を足した、ゆっくり不規則な ±depth セントの揺れ。phase は音ごとに変える。 */
export function glideCurve(spec: { depth?: number; rate?: number }, durTicks: number, relSec: (rel: number) => number, phase = 0): (rel: number) => number {
  const rate = Math.max(0.05, Math.min(1, spec.rate ?? 0.2));
  const depth = Math.max(20, Math.min(150, spec.depth ?? 100)) / 100;
  return (rel) => {
    const t = relSec(rel);
    const fade = smooth(t / 0.4) * smooth((durTicks - rel) / 90);
    return depth * fade * (0.62 * Math.sin(2 * Math.PI * rate * t + phase) + 0.38 * Math.sin(2 * Math.PI * rate * 1.7 * t + phase * 2.3 + 1));
  };
}

/** ビブラートの自前生成（ピッチベンドの正弦波）。rate＝Hz、depth＝セント、delay＝揺れ始めるまでの tick。relSec は音の頭からの経過秒。 */
export function vibratoCurve(spec: { rate?: number; depth?: number; delay?: number }, durTicks: number, relSec: (rel: number) => number, minDelayTicks = 0): (rel: number) => number {
  const rate = Math.max(3, Math.min(8, spec.rate ?? 5.5));
  const depth = Math.max(8, Math.min(60, spec.depth ?? 30)) / 100;
  const delayTicks = Math.max(minDelayTicks, Math.round((spec.delay ?? 0.4) * PPQ));
  const delaySec = relSec(delayTicks);
  return (rel) => {
    if (rel < delayTicks) return 0;
    const t = relSec(rel) - delaySec;
    const fadeIn = smooth(t / 0.25);
    const fadeOut = smooth((durTicks - rel) / 60);
    return depth * fadeIn * fadeOut * Math.sin(2 * Math.PI * rate * t);
  };
}

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
function velocityOf(volume: number, boost: number, trackVolume = volume, wide = false): number {
  // 音量の大きいパートは 34 + 音量×430 が 127 を超え、弱い音も 127 に張りついて強弱が消えていた。
  // 127 に収まる分を「そのパートの最大の強さ」とし、音ごとの強さの比（volume / trackVolume）をその上にかける
  if (!(trackVolume > 0)) return Math.max(18, Math.min(127, Math.round((34 + volume * 430) * boost)));
  const ratio = volume / trackVolume;
  if (wide) {
    // 強弱を広げる版: 下駄を小さく（34→8）、比を少し強調して、弱い音をはっきり弱くする
    const top = Math.min(127 / boost, 34 + trackVolume * 430);
    return Math.max(10, Math.min(127, Math.round((8 + (top - 8) * Math.pow(ratio, 1.25)) * boost)));
  }
  const full = Math.min(127 / boost - 34, trackVolume * 430);
  return Math.max(18, Math.min(127, Math.round((34 + full * ratio) * boost)));
}

// 楽器ごとの強さの補正（録音音源は楽器によって元の大きさが違うため）
const BOOST: Partial<Record<Instrument, number>> = { brass: 0.95, slap: 1.0, strings: 1.05, pad: 1.0, guitar: 1.0, crunch: 0.95, distGuitar: 0.9, leadGuitar: 0.95, lead: 0.9, bass: 1.05, sub808: 1.0, keys: 1.0, piano: 1.05, harpsichord: 1.05, bell: 1.0, kick: 1.0, snare: 1.0, hihat: 0.9, crash: 0.95 };
// 残響の量（MIDIのCC91）
const REVERB: Partial<Record<Instrument, number>> = { pad: 70, choir: 80, strings: 55, bell: 70, chime: 60, echoGuitar: 60, bird: 40, wind: 60, stream: 40, rain: 40, lead: 40, leadGuitar: 40, piano: 40, keys: 35, guitar: 35 };
// コーラス（音を広げる揺らぎ）の量（MIDIのCC93）
const CHORUS: Partial<Record<Instrument, number>> = { strings: 30, pad: 35, choir: 30, keys: 22, guitar: 20, echoGuitar: 20, crunch: 12, distGuitar: 8, bell: 12, harpsichord: 10 };
/** 歪ませないアンプ（これらのときは、元の音色をそのまま使う）。 */
const CLEAN_AMP_TYPES = new Set<string>(["clean", "jazz", "funk", "lofi", "retro8bit", "radio", "delicate", "crystal", "sparkleClean"]);
const SWELL_INSTRUMENTS = new Set<Instrument>(["lead", "leadGuitar", "pad", "strings", "choir", "brass"]);
const DETUNE_INSTRUMENTS = new Set<Instrument>(["lead", "leadGuitar", "guitar", "echoGuitar", "strings", "pad", "brass"]);
const ECHO_INSTRUMENTS = new Set<Instrument>(["lead", "leadGuitar", "cowbell", "bell", "keys"]);

function channelKey(track: Track, program: number): string {
  // 残響・コーラス・明るさ・キックへの凹みが違うパートは、別のチャンネルに分ける
  const mix = [track.reverb, track.chorus, track.bright, track.duck].some((v) => v !== undefined) ? `|${track.reverb ?? ""},${track.chorus ?? ""},${track.bright ?? ""},${track.duck ?? ""}` : "";
  // 音程のずれ・立ち上がり・余韻が違うパートも、別のチャンネルに分ける
  const tone = [track.detune, track.attack, track.release].some((v) => v) ? `|t${track.detune ?? 0},${track.attack ?? ""},${track.release ?? ""}` : "";
  return `${program}|${(track.pan ?? 0).toFixed(2)}|${track.instrument ?? track.waveform}${mix}${tone}`;
}
const clamp127 = (v: number): number => Math.max(0, Math.min(127, Math.round(v)));
/** ドラムの太鼓の種類 → GMのキー */
const DRUM_GROUP_KEYS = { kick: [35, 36], snare: [37, 38, 39, 40], hat: [42, 44, 46], tom: [41, 43, 45, 47, 48, 50], crash: [49, 52, 55, 57] } as const;

export function scoreToMidi(score: Score): Uint8Array {
  return scoreToMidiInfo(score).midi;
}

/** MIDIと、チャンネルごとの楽器（GMの番号）。機材（アンプ・ドラムの仕上げ）を選ぶために使う。 */
export function scoreToMidiInfo(score: Score): { midi: Uint8Array; programs: Record<number, number>; amps: Record<number, { amp: AmpSetting; pan: number }> } {
  const programs: Record<number, number> = {};
  const amps: Record<number, { amp: AmpSetting; pan: number }> = {};
  const tracksBytes: number[][] = [];
  // 指揮者トラック（テンポと曲の長さ）
  const totalBeats = Math.max(...score.tracks.map((t) => t.notes.reduce((s, n) => s + n.durationBeats, 0)));
  const endTick = Math.round(totalBeats * PPQ);
  const clock = makeTempoClock(score.tempoBpm, score.tempoMap);
  const tempoBytes = (bpm: number): number[] => {
    const usec = Math.round(60_000_000 / bpm);
    return [0xff, 0x51, 0x03, (usec >> 16) & 255, (usec >> 8) & 255, usec & 255];
  };
  const conductor: number[] = [0, ...tempoBytes(clock.segs[0].bpm)];
  // 拍子（例: 7/8 → 分子7・分母は2の3乗）
  const sig = timeSignatureOf(score);
  conductor.push(0, 0xff, 0x58, 0x04, sig.num, Math.round(Math.log2(sig.den)), 24, 8);
  // ループの始まりと終わり（曲の頭から最後の拍まで、ぴったりくり返す）
  const marker = (text: string): number[] => [0xff, 0x06, text.length, ...[...text].map((c) => c.charCodeAt(0))];
  conductor.push(0, ...marker("loopstart"));
  // テンポマップ: 途中のテンポの変わり目（tempoMap が無い曲は何も足さない）
  let prevTempoTick = 0;
  for (const seg of clock.segs.slice(1)) {
    const at = Math.round(seg.beat * PPQ);
    if (at <= 0 || at >= endTick) continue;
    conductor.push(...vlq(at - prevTempoTick), ...tempoBytes(seg.bpm));
    prevTempoTick = at;
  }
  conductor.push(...vlq(endTick - prevTempoTick), ...marker("loopend"));
  conductor.push(0, 0xff, 0x2f, 0x00);
  tracksBytes.push(conductor);

  const channelOf = new Map<string, number>();
  let nextChannel = 0;
  const allocate = (key: string): number => {
    let ch = channelOf.get(key);
    if (ch === undefined) {
      if (nextChannel === DRUM_CHANNEL) nextChannel++;
      if (nextChannel > 15) {
        // チャンネルが足りないときは、同じ楽器（GMの番号）のチャンネルを使い回す（別の楽器と混ざらないように）
        const program = key.split("|")[0];
        const same = [...channelOf.entries()].find(([k]) => k.split("|")[0] === program);
        ch = same ? same[1] : 15;
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

  const H = Math.max(0, Math.min(1, Number(score.human) || 0));
  /** 同じ入力なら同じ結果になる 0〜1 の疑似乱数（人間らしさのばらつき用）。 */
  const rnd = (a: number): number => { const x = Math.sin(a * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); };
  /** タイミング・強さのずれの元になる 0.93〜1.07 の値。humanDist が "triangle" なら三角分布（2つの一様な値の平均）。 */
  const hz = (x: number): number => (score.humanDist === "triangle" ? triangular(humanize(x), humanize(x + 17.3)) : humanize(x));
  // キックが鳴る位置（サイドチェイン風の音量の凹みと、lockToKick に使う）
  const kickTicks: number[] = [];
  const kickBeats: number[] = [];
  for (const t of score.tracks) {
    if (t.instrument !== "kick") continue;
    let b = 0;
    const sw = swingOf(score, t);
    const pushB = pushBeatsOf(t, score.tempoBpm);
    for (const n of t.notes) {
      if (n.note !== REST) {
        kickTicks.push(Math.max(0, Math.round((b + grooveOffsetBeats(sw.swing, pushB, b, sw.swing16)) * PPQ)));
        kickBeats.push(b);
      }
      b += n.durationBeats;
    }
  }
  kickBeats.sort((a, b) => a - b);
  // lockToKick: キックと同じ種・同じ幅でずらすための、キックの音の「タイミングのずれ」（ティック）
  const kickTrack = score.tracks.find((t) => t.instrument === "kick");
  const DRUM_SEED = (DRUM_CHANNEL + 1) * 7.31;
  const kickJitterAt = (kb: number): number => {
    if (!kickTrack || kb <= 0) return 0;
    const hm = trackHumanMult(score, kickTrack);
    if (hm === 0) return 0;
    const Ht = H * hm * (kickTrack.humanTiming ?? 1);
    return Math.round((hz(clock.beatToSec(kb) + 3.7 + DRUM_SEED) - 1) * (score.edition === "real" ? 1.6 : 1) * 45 * (1 + 2.5 * Ht));
  };
  const nearestKickBeat = (beat: number): number | null => {
    let lo = 0, hi = kickBeats.length - 1, best: number | null = null;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      if (kickBeats[mid] <= beat + 1e-9) { best = kickBeats[mid]; lo = mid + 1; } else hi = mid - 1;
    }
    return best !== null && beat - best <= 0.25 + 1e-9 ? best : null;
  };
  kickTicks.sort((a, b) => a - b);
  const uniqueKicks = kickTicks.filter((t, i) => i === 0 || t - kickTicks[i - 1] > 10);
  for (const track of score.tracks) {
    const inst = track.instrument;
    const drumNote = inst ? GM_DRUM_NOTE[inst] : undefined;
    const isDrum = drumNote !== undefined;
    // パート別の human（Track.human／Score.humanRoles。指定が無ければ 1 で、今までと同じ）
    const hm = trackHumanMult(score, track);
    const quant = hm === 0;
    const Hp = H * hm;
    const Ht = Hp * (track.humanTiming ?? 1);
    const Hv = Hp * (track.humanVelocity ?? 1);
    const trackSwing = swingOf(score, track);
    const trackPush = pushBeatsOf(track, score.tempoBpm);
    const lockKick = !isDrum && (track.lockToKick ?? (score.lockToKick === true && (inst === "bass")));
    let program = track.program ?? (inst ? GM_PROGRAM[inst] ?? GM_DEFAULT_BY_WAVE[track.waveform] : GM_DEFAULT_BY_WAVE[track.waveform]);
    // リードとパッド: 電子音楽では電子的な音色、メタル調ではオーバードライブのギター、それ以外は生楽器に近い音色
    if (inst === "lead" && track.program === undefined) program = score.synth ? SYNTH_LEAD : score.tone === "metal" || score.tone === "prs" ? METAL_LEAD : program;
    if (inst === "pad" && score.synth && track.program === undefined) program = SYNTH_PAD;
    // 歪みの二重がけを避ける: 歪ませるアンプを指定したギターは、録音がすでに歪んだ音色（オーバードライブ29・ディストーション30）ではなく、
    // クリーン（27）を元にして、歪みはアンプだけでかける
    if (track.amp && (program === 29 || program === 30) && track.program === undefined && !CLEAN_AMP_TYPES.has(track.amp.type)) program = 27;
    const setupChannel = (prog: number, key: string, gainBoost: number): { channel: number; list: Ev[] } => {
      const channel = isDrum ? DRUM_CHANNEL : allocate(key);
      const list = midiTrackFor(channel);
      if (channel === DRUM_CHANNEL) {
        if (!list.some((e) => e.bytes[0] === 0xc9)) list.push({ tick: 0, order: 0, bytes: [0xc9, score.drumKit ?? 0] });
        // 太鼓ごとのミックス（ドラムNRPN: 26=音量、28=左右、29=残響。データ120が標準の音量、64が中央）
        if (score.drumMix && !list.some((e) => e.bytes[0] === 0xb9 && e.bytes[1] === 99 && e.bytes[2] !== 24)) {
          for (const [group, cfg] of Object.entries(score.drumMix) as [keyof typeof DRUM_GROUP_KEYS, { level?: number; pan?: number; reverb?: number; spread?: number; tune?: number }][]) {
            for (const key of DRUM_GROUP_KEYS[group] ?? []) {
              const put = (msb: number, data: number): void => { for (const [cc, v] of [[99, msb], [98, key], [6, clamp127(data)]] as const) list.push({ tick: 0, order: 0, bytes: [0xb9, cc, v] }); };
              if (cfg.level !== undefined) put(26, 120 * Math.max(0, Math.min(1.05, cfg.level)));
              if (cfg.pan !== undefined) put(28, Math.max(1, 64 + Math.max(-1, Math.min(1, cfg.pan)) * 63));
              // タムの広がり: 高いタムを左、低いフロアを右へ振り分ける（聴き手から見て。ドラマー視点のセット配置）
              if (group === "tom" && cfg.spread !== undefined) {
                const order = [50, 48, 47, 45, 43, 41];
                const at = order.indexOf(key);
                const pos = at < 0 ? 0 : (at / (order.length - 1)) * 2 - 1;
                put(28, Math.max(1, 64 + Math.max(-1, Math.min(1, (cfg.pan ?? 0) + pos * Math.min(1, cfg.spread))) * 63));
              }
              if (cfg.tune !== undefined) put(24, 64 + Math.max(-6, Math.min(6, cfg.tune)) * 2);
              if (cfg.reverb !== undefined) put(29, cfg.reverb * 127);
            }
          }
          for (const [cc, v] of [[99, 127], [98, 127]] as const) list.push({ tick: 0, order: 0, bytes: [0xb9, cc, v] });
        }
        // スネアの音程調整（ドラムNRPN 24: データ64が元のまま、1あたり50セント）
        if (score.snareTune && score.drumMix?.snare?.tune === undefined) {
          const data = Math.max(0, Math.min(127, Math.round(64 + score.snareTune * 2)));
          for (const key of [38, 40]) for (const [cc, v] of [[99, 24], [98, key], [6, data]] as const) list.push({ tick: 0, order: 0, bytes: [0xb9, cc, v] });
          for (const [cc, v] of [[99, 127], [98, 127]] as const) list.push({ tick: 0, order: 0, bytes: [0xb9, cc, v] });
        }
      } else if (!list.some((e) => e.bytes[0] === (0xc0 | channel))) {
        const pan = Math.round(64 + (track.pan ?? 0) * 63);
        list.push({ tick: 0, order: 0, bytes: [0xc0 | channel, prog] });
        list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 7, Math.round(118 * gainBoost)] });
        list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 10, Math.max(0, Math.min(127, pan))] });
        list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 91, track.reverb !== undefined ? clamp127(track.reverb * 127) : inst ? REVERB[inst] ?? 30 : 30] });
        list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 93, track.chorus !== undefined ? clamp127(track.chorus * 127) : inst ? CHORUS[inst] ?? 0 : 0] });
        // 明るさ（CC74。64が標準。下げると高域が丸くなる）
        if (track.bright) list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 74, clamp127(64 + Math.max(-1, Math.min(0.5, track.bright)) * 48)] });
        // ピッチベンドの幅を ±12半音に（RPN 0）。ベンド・しゃくり・フォールの深さに使う
        for (const [cc, v] of [[101, 0], [100, 0], [6, BEND_RANGE], [38, 0], [101, 127], [100, 127]] as const) list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, cc, v] });
        // 音程のずれ（RPN 1 ＝チャンネルのファインチューン。セント単位、±100セントを 0〜16383 に）
        if (track.detune) {
          const v = Math.max(0, Math.min(0x3fff, Math.round(0x2000 + (Math.max(-50, Math.min(50, track.detune)) / 100) * 0x2000)));
          for (const [cc, d] of [[101, 0], [100, 1], [6, (v >> 7) & 0x7f], [38, v & 0x7f], [101, 127], [100, 127]] as const) list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, cc, d] });
        }
        // 立ち上がり（CC73）と余韻（CC72）。64 が音源のまま
        if (track.attack !== undefined) list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 73, clamp127(Math.max(0, Math.min(1, track.attack)) * 127)] });
        if (track.release !== undefined) list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 72, clamp127(Math.max(0, Math.min(1, track.release)) * 127)] });
        // 主旋律の楽器には、揺らぎ（ビブラート）を少し
        if (inst === "leadGuitar" || inst === "lead" || inst === "brass") list.push({ tick: 0, order: 0, bytes: [0xb0 | channel, 1, score.tone === "prs" ? 40 : 26] });
      }
      return { channel, list };
    };
    const main = setupChannel(program, channelKey(track, program), 1);
    const channel = main.channel;
    // ばらつきの種は、チャンネルごと。同じチャンネルに重ねた声部（ギターのストロークの各弦など）は、同じようにずれて、和音がそろったままになる
    const trackSeed = (channel + 1) * 7.31;
    if (channel !== DRUM_CHANNEL) programs[channel] = program;
    if (channel !== DRUM_CHANNEL && track.amp) amps[channel] = { amp: track.amp, pan: track.pan ?? 0 };
    const list = main.list;
    const layerSpec = inst && track.program === undefined ? GM_LAYER[inst] : undefined;
    const layer = layerSpec ? setupChannel(layerSpec.program, `${channelKey(track, layerSpec.program)}|layer`, 1) : null;
    if (layer && layer.channel !== DRUM_CHANNEL) programs[layer.channel] = layerSpec!.program;
    // ピアノ系は、およそ1小節ごとにペダルを踏み替えて、音をつなげる
    if ((inst === "piano" || inst === "keys") && track.pedal) {
      // ペダルの指定がある: chord／bar は踏み替える拍（changes）で、none は踏まない
      if (track.pedal.mode !== "none") {
        const points = [0, ...track.pedal.changes.map((b) => Math.round(b * PPQ))].filter((t, i, a2) => t < endTick && (i === 0 || t > a2[i - 1]));
        for (const at of points) {
          for (const c of layer ? [channel, layer.channel] : [channel]) {
            const l = c === channel ? list : layer!.list;
            if (at > 0) l.push({ tick: at - 6, order: 1, bytes: [0xb0 | c, 64, 0] });
            l.push({ tick: at, order: 1, bytes: [0xb0 | c, 64, 127] });
          }
        }
      }
    } else if (inst === "piano" || inst === "keys") {
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
    if (score.pump && (inst === "pad" || inst === "choir" || inst === "strings")) {
      for (let at = 0; at < endTick; at += PPQ) {
        list.push({ tick: at, order: 1, bytes: [0xb0 | channel, 11, 62] });
        list.push({ tick: at + Math.round(PPQ * 0.3), order: 1, bytes: [0xb0 | channel, 11, 100] });
        list.push({ tick: at + Math.round(PPQ * 0.65), order: 1, bytes: [0xb0 | channel, 11, 127] });
      }
    }
    // キックに合わせた音量の凹み（duck）。キックの頭で凹み、約0.45拍かけて戻る（CC7。音量は値の2乗に比例するので平方根で）
    if (track.duck && track.duck > 0 && !isDrum && channel !== DRUM_CHANNEL) {
      const base = Math.round(118);
      const depth = Math.max(0, Math.min(0.95, track.duck));
      const REL = Math.round(PPQ * 0.45);
      const gainAt = (t: number): number => 1 - depth * (1 - t / REL) ** 2;
      uniqueKicks.forEach((kt, i) => {
        const nextKick = uniqueKicks[i + 1] ?? Infinity;
        for (const frac of [0, 0.2, 0.4, 0.6, 0.8, 1]) {
          const at = kt + Math.round(REL * frac);
          if (at >= nextKick - 4 && frac > 0) break;
          list.push({ tick: at, order: 1, bytes: [0xb0 | channel, 7, clamp127(base * Math.sqrt(gainAt(REL * frac)))] });
        }
      });
    }
    const boost = inst ? BOOST[inst] ?? 1 : 1;
    let beat = 0;
    for (const n of track.notes) {
      const startBeat = beat;
      beat += n.durationBeats;
      if (n.note === REST) continue;
      const secStart = clock.beatToSec(startBeat);
      // 手で弾いたような、ごくわずかなタイミングのずれ（鍵盤・ギター・ベース）
      // 実楽器版は、人が演奏するように、タイミングのずれを大きめに
      const human = score.edition === "real" ? 1.6 : 1;
      // slap・sub808・パッドなど、ふだんはずらさない楽器も、Track.human を 0 より大きく書けばずれる
      const optIn = track.human !== undefined && track.human > 0;
      const looseness = quant ? 0 : human * (inst && ["keys", "piano", "guitar", "echoGuitar", "bass", "harpsichord", "strings", "lead", "leadGuitar", "brass", "crunch", "distGuitar"].includes(inst) ? 70 : inst && ["kick", "snare", "hihat", "tom", "crash"].includes(inst) ? 45 : optIn ? 70 : 0);
      const kb = lockKick && startBeat > 0 && !quant ? nearestKickBeat(startBeat) : null;
      const jitter = kb !== null ? kickJitterAt(kb) : looseness > 0 && startBeat > 0 ? Math.round((hz(secStart + 3.7 + trackSeed) - 1) * looseness * (1 + (drumNote !== undefined ? 2.5 : 4) * Ht)) : 0;
      const grooveTicks = Math.round(grooveOffsetBeats(trackSwing.swing, trackPush, startBeat, trackSwing.swing16) * PPQ);
      // バンド全体の、ゆるやかな走り・溜め（全パート同じだけずれるので、アンサンブルはそろったまま）
      const drift = H > 0 && !quant ? Math.round(H * (12 * Math.sin((startBeat * 2 * Math.PI) / 17.3) + 8 * Math.sin((startBeat * 2 * Math.PI) / 41 + 1.3))) : 0;
      const tick = Math.max(0, Math.round(startBeat * PPQ) + jitter + grooveTicks + drift);
      let vol = track.volume * velocityScale(n.velocity) * (inst && !quant ? 1 + (hz(secStart + trackSeed * 0.37) - 1) * (1 + 3 * Hv) : 1);
      let drumKey = drumNote;
      // タム: 音名でタムの高さを選ぶ（C4 高い → A2 低いフロア）。C2（既定）は今までどおり 47
      if (inst === "tom" && n.note !== "C2") {
        const mp = noteNameToMidi(n.note);
        const TOMS: [number, number][] = [[45, 41], [48, 43], [52, 45], [55, 47], [57, 48], [60, 50]];
        drumKey = TOMS.reduce((best, t) => (Math.abs(t[0] - mp) < Math.abs(best[0] - mp) ? t : best), TOMS[3])[1];
      }
      let lenScale = drumNote !== undefined ? 0.5 : 0.97;
      if (inst === "hihat") {
        // 表拍は強く、裏拍は弱く。16分の細かい音はさらに弱く。ときどき開いたハイハット
        const frac = startBeat - Math.floor(startBeat);
        vol *= frac === 0 ? 1.15 : Math.abs(frac - 0.5) < 1e-6 ? 0.85 : 0.62;
        if (n.open) {
          // 指定されたオープンハイハット: 開いて長く、拍の位置の弱さに関係なく、はっきり鳴らす
          drumKey = 46;
          lenScale = 1;
          vol *= frac === 0 ? 1 : frac === 0.5 ? 1.55 : 2;
        } else if (Math.abs(frac - 0.75) < 1e-6 && humanize(secStart + 1.3) < 0.95) {
          drumKey = 46;
          lenScale = 1;
        }
      } else if (inst === "snare") {
        if (!quant) vol *= 1 + (humanize(secStart + 9.1) - 1) * 1.5;
      } else if (inst === "crash") {
        lenScale = 3;
      }
      // 曲の頭の2拍は強く（聴き手をつかむ、最初の一撃）
      const strike = score.opening && startBeat < 2 ? 1.22 : 1;
      // 特別曲用（prs）の刻みギターは、強すぎないよう控えめに
      const rhythmSoft = score.tone === "prs" && (inst === "distGuitar" || inst === "crunch") ? 0.78 : 1;
      const velocity = Math.min(127, Math.round(velocityOf(vol, boost, track.volume, score.dynamicRange === "wide") * strike * rhythmSoft));
      // 音の長さのばらつき（人の弾き方）: 短い音は、少し短く切れたり、つながったり
      if (Hp > 0 && drumNote === undefined && n.gate === undefined && n.durationBeats <= 1) lenScale *= 1 - 0.14 * Hp * rnd(startBeat * 3.1 + trackSeed);
      const len = Math.max(20, Math.round((n.open && inst === "hihat" ? Math.max(n.durationBeats, 0.5) : n.durationBeats) * PPQ * lenScale * (drumNote === undefined ? n.gate ?? 1 : 1)));
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
      // ベンド・しゃくり・フォール: 音符に指定があれば、その深さで。なければ、ギターの長い音は下から音程を持ち上げて入る
      const durTicks = Math.max(1, Math.round(n.durationBeats * PPQ));
      const explicitBend = n.bend || n.scoop || n.fall || n.slide;
      const autoScoop = (track.autoScoop ?? score.autoScoop !== false) && !explicitBend && (inst === "leadGuitar" || inst === "guitar") && n.durationBeats >= 1 && startBeat > 0;
      const baseCurve = autoScoop ? (rel: number): number => (rel < 16 ? -1 : rel < 34 ? -0.5 : 0) : durTicks >= 60 ? bendCurve(n, durTicks) : null;
      // ビブラートの自前生成: パートの vibrato 指定がある音、または ~~~（vibrato > 1）の音。ベンドした音は、上がりきってから揺らす（ベンドビブラート）
      const wantVib = !!n.vibrato && n.durationBeats >= 0.4 && durTicks >= 120 && (track.vibratoSpec !== undefined || n.vibrato > 1);
      const bendRise = n.bend ? Math.max(1, n.bendT ? Math.min(durTicks, n.bendT * PPQ) : Math.min(durTicks * 0.35, PPQ * 0.5)) : 0;
      const vibCurve = wantVib ? vibratoCurve(track.vibratoSpec ?? {}, durTicks, (rel) => clock.beatToSec(startBeat + rel / PPQ) - secStart, Math.round(bendRise)) : null;
      const gliding = track.glide !== undefined && n.durationBeats >= 1 && durTicks >= PPQ && !explicitBend;
      const glide = gliding ? glideCurve(track.glide ?? {}, durTicks, (rel) => clock.beatToSec(startBeat + rel / PPQ) - secStart, rnd(startBeat * 1.7 + trackSeed) * 6.28) : null;
      const curve = vibCurve || glide ? (rel: number): number => (baseCurve ? baseCurve(rel) : 0) + (vibCurve ? vibCurve(rel) : 0) + (glide ? glide(rel) : 0) : baseCurve;
      const bendTargets = layer && layer.channel !== DRUM_CHANNEL ? [main, layer] : [main];
      if (curve) {
        for (const t of bendTargets) {
          const setBend = (at: number, semi: number): void => {
            const v = bendValue(semi);
            t.list.push({ tick: Math.max(0, at), order: 1, bytes: [0xe0 | t.channel, v & 0x7f, (v >> 7) & 0x7f] });
          };
          if (autoScoop && !vibCurve && !glide) {
            setBend(tick - 3, -1);
            setBend(tick + 16, -0.5);
            setBend(tick + 34, 0);
          } else {
            // なめらかに動くよう、およそ12tickごとに値を送る。音の終わりで元に戻す
            setBend(tick - 3, curve(0));
            for (let rel = 12; rel < durTicks - 6; rel += 12) setBend(tick + rel, curve(rel));
            setBend(tick + durTicks - 5, 0);
          }
        }
      }
      // ビブラート: 音が出て少したってから揺れ始め、音の終わりで元の深さに戻す（モジュレーション CC1）
      if (n.vibrato && !vibCurve && n.durationBeats >= 0.4 && (inst === undefined || GM_DRUM_NOTE[inst] === undefined)) {
        const depth = Math.max(0, Math.min(1, n.vibrato));
        const base = inst === "leadGuitar" || inst === "lead" || inst === "brass" ? (score.tone === "prs" ? 40 : 26) : 0;
        const peak = Math.max(base, Math.round(depth * 127));
        const delay = Math.round(Math.min(durTicks * 0.3, PPQ * 0.4));
        for (const t of bendTargets) {
          t.list.push({ tick: tick + delay, order: 1, bytes: [0xb0 | t.channel, 1, Math.round(base + (peak - base) * 0.4)] });
          t.list.push({ tick: tick + delay + Math.round(PPQ * 0.15), order: 1, bytes: [0xb0 | t.channel, 1, peak] });
          t.list.push({ tick: tick + durTicks - 5, order: 1, bytes: [0xb0 | t.channel, 1, base] });
        }
      }
      // ボリューム奏法（< > ）: 音量（CC11）を、音の長さをかけて立ち上げる／減らす。デクレッシェンドは、音のあとに 127 へ戻す
      if (n.swell && channel !== DRUM_CHANNEL && durTicks >= 120) {
        for (const t of bendTargets) {
          const cc = (at: number, v: number): void => { t.list.push({ tick: Math.min(endTick, Math.max(0, at)), order: 1, bytes: [0xb0 | t.channel, 11, clamp127(v)] }); };
          const steps = 8;
          for (let k = 0; k <= steps; k++) {
            const x = smooth(k / steps);
            cc(tick + Math.round(((durTicks * 0.9) * k) / steps) - (k === 0 ? 2 : 0), n.swell > 0 ? 24 + 103 * x : 127 - 87 * x);
          }
          cc(tick + durTicks + (n.swell > 0 ? -2 : 24), 127);
        }
      }
      // 長い音の音量の山（CC11）: 立ち上がって、中ほどで最大、終わりへ少し引く。リード・パッド・弦・ブラス・合唱
      if (Hp > 0 && !n.swell && !score.pump && inst && SWELL_INSTRUMENTS.has(inst) && durTicks >= PPQ) {
        for (const t of bendTargets) {
          const cc = (at: number, v: number): void => { t.list.push({ tick: at, order: 1, bytes: [0xb0 | t.channel, 11, Math.max(40, Math.min(127, v))] }); };
          cc(tick, 127 - Math.round(38 * Hp));
          cc(tick + Math.round(durTicks * 0.35), 127);
          cc(tick + Math.round(durTicks * 0.8), 127 - Math.round(16 * Hp));
          cc(tick + durTicks - 2, 127);
        }
      }
      // 音程のごくわずかなずれ（±8セント）: リード・ギター・弦。ベンドの指定がない音だけ
      if (Hp > 0 && !curve && inst && DETUNE_INSTRUMENTS.has(inst) && durTicks >= 60) {
        const semi = (rnd(startBeat * 5.7 + trackSeed * 1.3) - 0.5) * 2 * 0.08 * Hp;
        for (const t of bendTargets) {
          const v = bendValue(semi);
          t.list.push({ tick: Math.max(0, tick - 3), order: 1, bytes: [0xe0 | t.channel, v & 0x7f, (v >> 7) & 0x7f] });
          const v0 = bendValue(0);
          t.list.push({ tick: tick + durTicks - 5, order: 1, bytes: [0xe0 | t.channel, v0 & 0x7f, (v0 >> 7) & 0x7f] });
        }
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
  return { midi: Uint8Array.from(out), programs, amps };
}
