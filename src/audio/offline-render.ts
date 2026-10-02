import { BasicMIDI } from "spessasynth_core";
import { WorkletSynthesizer } from "spessasynth_lib";
import { AmpRack } from "./amp-rack";
import { configureAudioRack, decodeClip, scheduleAudioTracks } from "./audio-clips";
import { scoreToMidiInfo } from "./midi-export";
import type { NamHost } from "./nam/nam-host";
import { getScoreDurationSec, type Score } from "./score";
import { createBgmBus, createHallImpulse } from "./voices";

export interface OfflineRenderOptions {
  /** サウンドフォント（.sf3）の中身。 */
  soundfont: ArrayBuffer;
  /** spessasynth のワークレットのURL。 */
  processorUrl: string;
  /** 版（高音の丸め・ホール残響の量）。曲そのものの編成は、呼び出し側で版に合わせておく。 */
  edition: "modern" | "ps2" | "real";
  nam?: NamHost | null;
  /** 曲の終わりのあとに残す余韻（秒）。 */
  tailSec?: number;
  sampleRate?: number;
}

/**
 * 曲を、実時間より速く音にする（WAVの書き出し用）。
 * ゲームと同じつなぎ方（録音音源 → 楽器ごとのアンプ → 仕上げ → 版の段）を、OfflineAudioContext の上に組み立てて描き出す。
 */
export async function renderScoreOffline(score: Score, options: OfflineRenderOptions): Promise<AudioBuffer> {
  const sampleRate = options.sampleRate ?? 44100;
  // 録音した音が曲より長ければ、その終わりまで描き出す
  const spb = 60 / score.tempoBpm;
  const clipEnd = Math.max(0, ...(score.audioTracks ?? []).flatMap((t) => t.clips.map((c) => c.startBeat * spb + c.seconds)));
  const seconds = Math.max(getScoreDurationSec(score), clipEnd) + (options.tailSec ?? 2.5);
  const ctx = new OfflineAudioContext(2, Math.ceil(seconds * sampleRate), sampleRate);
  await ctx.audioWorklet.addModule(options.processorUrl);

  // 版の段（AudioEngine と同じ値）: 高音を丸める低域通過フィルターと、ホール残響
  const out = ctx.createGain();
  out.gain.value = 0.8;
  out.connect(ctx.destination);
  const lp = ctx.createBiquadFilter();
  lp.type = "lowpass";
  lp.frequency.value = options.edition === "ps2" ? 15500 : options.edition === "real" ? 19000 : 22000;
  lp.Q.value = 0.6;
  lp.connect(out);
  const hallLevel = options.edition === "ps2" ? 0.34 : options.edition === "real" ? 0.15 : 0;
  if (hallLevel > 0) {
    const hall = ctx.createConvolver();
    hall.buffer = createHallImpulse(ctx);
    const send = ctx.createGain();
    send.gain.value = hallLevel;
    lp.connect(send);
    send.connect(hall);
    hall.connect(out);
  }
  const bus = createBgmBus(ctx, lp, 0.1);
  bus.gain.value = Math.pow(10, (score.preDb ?? 0) / 20);

  // アンプ（NAMのモデルの読み込みを含む）を先に用意してから、シンセサイザーを作って描き出しを始める
  const { midi, programs, amps } = scoreToMidiInfo(score);
  const rack = new AmpRack(ctx, bus);
  rack.setNam(options.nam ?? null);
  rack.configure(programs, score.tone ?? "rock", 9, amps, score.namModels ?? {}, score.ampPlugins ?? {});
  await rack.whenReady();
  // 録音トラック（実際の楽器・声）: 別のアンプラックを通して、曲の頭から予約する
  if (score.audioTracks?.length) {
    const audioRack = new AmpRack(ctx, bus);
    audioRack.setNam(options.nam ?? null);
    configureAudioRack(audioRack, score);
    await audioRack.whenReady();
    for (const t of score.audioTracks) for (const c of t.clips) await decodeClip(ctx, c);
    await scheduleAudioTracks(ctx, score, audioRack, 0, 0);
  }

  const synth = new WorkletSynthesizer(ctx);
  for (let ch = 0; ch < 16; ch++) {
    synth.connectChannel(rack.input(ch), ch);
  }
  (synth as unknown as { worklet: AudioWorkletNode }).worklet.connect(bus, 0);
  const binary = midi.buffer.slice(midi.byteOffset, midi.byteOffset + midi.byteLength) as ArrayBuffer;
  await synth.startOfflineRender({
    midiSequence: BasicMIDI.fromArrayBuffer(binary, "song.mid"),
    loopCount: 0,
    soundBankList: [{ bankOffset: 0, soundBankBuffer: options.soundfont.slice(0) }],
  });
  return ctx.startRendering();
}

/** 音の大きさの山（ピーク）を、target（0〜1）にそろえる。小さすぎるときだけ持ち上げ、大きすぎるときは下げる。 */
export function normalizePeak(channels: Float32Array[], target = 0.89): void {
  let peak = 0;
  for (const c of channels) for (let i = 0; i < c.length; i++) peak = Math.max(peak, Math.abs(c[i]));
  if (peak < 1e-6) return;
  const g = target / peak;
  for (const c of channels) for (let i = 0; i < c.length; i++) c[i] *= g;
}
