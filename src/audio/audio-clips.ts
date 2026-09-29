import type { AmpRack } from "./amp-rack";
import type { AmpSetting, Score } from "./score";

/** 録音した音のかたまり（1回の録音）。 */
export interface AudioClip {
  id: string;
  /** 曲のどこから鳴らすか（拍。4分音符=1拍）。 */
  startBeat: number;
  /** 音の中身（FLAC を base64 にしたもの。音質はそのまま）。 */
  flac: string;
  /** 長さ（秒）。 */
  seconds: number;
}

/** 録音したトラック。アンプ（ギター・ベースのライン録りに）を通して鳴らせる。 */
export interface AudioTrack {
  name: string;
  /** 0〜1.5 くらい。 */
  volume: number;
  pan: number;
  amp?: AmpSetting;
  muted?: boolean;
  clips: AudioClip[];
}

export function base64ToBytes(b64: string): Uint8Array<ArrayBuffer> {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
export function bytesToBase64(bytes: Uint8Array): string {
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}

const decoded = new WeakMap<BaseAudioContext, Map<string, AudioBuffer>>();
/** 録音の音を、鳴らせる形にする（同じ場所では1回だけ）。 */
export async function decodeClip(ctx: BaseAudioContext, clip: AudioClip): Promise<AudioBuffer> {
  let cache = decoded.get(ctx);
  if (!cache) {
    cache = new Map();
    decoded.set(ctx, cache);
  }
  const hit = cache.get(clip.id);
  if (hit) return hit;
  const buf = await ctx.decodeAudioData(base64ToBytes(clip.flac).buffer);
  cache.set(clip.id, buf);
  return buf;
}

/** 録音トラックのアンプを、アンプラックにまとめて設定する（i 番目のトラック = i 番目の入口）。 */
export function configureAudioRack(rack: AmpRack, score: Score): void {
  const amps: Record<number, { amp: AmpSetting; pan: number }> = {};
  (score.audioTracks ?? []).forEach((t, i) => {
    // 左右の位置は、アンプの前（scheduleAudioTracks）で決めるので、ここでは真ん中
    if (i < 16 && t.amp && t.amp.type !== "auto") amps[i] = { amp: t.amp, pan: 0 };
  });
  // ドラムのチャンネルはない（-1）。アンプを選んでいないトラックは、そのまま通す
  rack.configure({}, score.tone ?? "rock", -1, amps, score.namModels ?? {}, score.ampPlugins ?? {});
}

/**
 * 録音トラックの音を予約する。曲の頭が ctx の時刻 songStartAt にあたるとして、その時刻より後の部分を鳴らす。
 * 返す関数で、止められる。
 */
export async function scheduleAudioTracks(ctx: BaseAudioContext, score: Score, rack: AmpRack, songStartAt: number, fromSec = 0): Promise<() => void> {
  const sources: AudioBufferSourceNode[] = [];
  const spb = 60 / score.tempoBpm;
  const tracks = score.audioTracks ?? [];
  for (let i = 0; i < Math.min(16, tracks.length); i++) {
    const t = tracks[i];
    if (t.muted) continue;
    const gain = ctx.createGain();
    gain.gain.value = t.volume;
    const panner = ctx.createStereoPanner();
    panner.pan.value = Math.max(-1, Math.min(1, t.pan));
    gain.connect(panner);
    panner.connect(rack.input(i));
    for (const clip of t.clips) {
      const buf = await decodeClip(ctx, clip);
      const clipStart = clip.startBeat * spb;
      const clipEnd = clipStart + buf.duration;
      if (clipEnd <= fromSec) continue;
      const src = ctx.createBufferSource();
      src.buffer = buf;
      src.connect(gain);
      const offset = Math.max(0, fromSec - clipStart);
      src.start(Math.max(ctx.currentTime, songStartAt + clipStart + offset), offset);
      sources.push(src);
    }
  }
  return () => {
    for (const s of sources) {
      try {
        s.stop();
      } catch {
        // すでに止まっている
      }
      s.disconnect();
    }
  };
}
