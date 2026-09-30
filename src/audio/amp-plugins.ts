import { AMP_PRESETS, makeDistortionCurve, type AmpPresetName, type AmpShape } from "./amp";

/**
 * アンプの追加のしくみ（アンプ定義ファイル `.sunshine-amp.json`）。
 * ほかのアンプシミュレーターを、あとから自由に組み込めるように、アンプを「段（ステージ）の並び」として書く。
 *
 * 段の種類:
 * - gain: 音量を変える
 * - drive: 歪み（soft・hard・asym・steps の形。amp.ts と同じ）
 * - eq: フィルター・イコライザー（Web Audio の BiquadFilter の種類）
 * - compressor: 音の大小をそろえる
 * - ir: キャビネットや部屋の響き（インパルス応答のWAVを、base64で埋め込む）
 * - worklet: 自分で書いた音の処理（AudioWorklet のプログラム）。プログラムを含むので、信頼できる配布元のものだけ使う
 * - nam: NAMのモデル（.nam の中身を埋め込む。作曲ソフトだけで鳴る）
 *
 * ファイルは、作曲ソフトの「アンプ定義を読み込む」か、デスクトップ版の「アンプの追加フォルダ」に置いて使う。
 * 書き方は docs/design/amp-plugins.md。
 */
export type AmpStage =
  | { type: "gain"; value: number }
  | { type: "drive"; shape: AmpShape; hardness: number; asymmetry?: number; amount?: number }
  | { type: "eq"; kind: BiquadFilterType; freq: number; gain?: number; q?: number }
  | { type: "compressor"; threshold: number; ratio: number; attack?: number; release?: number }
  | { type: "ir"; wav: string; mix?: number }
  | { type: "worklet"; name: string; code: string; params?: Record<string, number> }
  | { type: "nam"; model: string };

export interface AmpPluginDef {
  format: "sunshine-amp";
  version: 1;
  /** 英小文字・数字・「-」。 */
  id: string;
  label: string;
  description?: string;
  author?: string;
  /** 利用条件（例: "MIT"、"CC0"、「作者の許可あり」）。販売物に入れるときは必ず確かめる。 */
  license?: string;
  stages: AmpStage[];
}

const FILTERS: BiquadFilterType[] = ["lowpass", "highpass", "bandpass", "lowshelf", "highshelf", "peaking", "notch", "allpass"];
const SHAPES: AmpShape[] = ["soft", "hard", "asym", "steps"];
const num = (x: unknown): x is number => typeof x === "number" && Number.isFinite(x);

/** アンプ定義を確かめる。おかしなところは、すべてまとめてエラーにする。 */
export function validateAmpPlugin(data: unknown): AmpPluginDef {
  const d = data as Partial<AmpPluginDef> | null;
  const errors: string[] = [];
  if (!d || d.format !== "sunshine-amp") throw new Error("アンプ定義ファイル（format: \"sunshine-amp\"）ではありません");
  if (d.version !== 1) errors.push(`version は 1（${d.version}）`);
  if (typeof d.id !== "string" || !/^[a-z0-9][a-z0-9-]{0,63}$/.test(d.id)) errors.push(`id は英小文字・数字・「-」（${d.id}）`);
  if (typeof d.label !== "string" || !d.label) errors.push("label（表示名）がありません");
  if (!Array.isArray(d.stages) || d.stages.length === 0) errors.push("stages（段の並び）がありません");
  if (Array.isArray(d.stages) && d.stages.length > 64) errors.push("段が多すぎます（64まで）");
  (d.stages ?? []).forEach((s, i) => {
    const at = `stages[${i}]`;
    switch (s?.type) {
      case "gain":
        if (!num(s.value) || s.value < 0 || s.value > 100) errors.push(`${at}: value は 0〜100`);
        break;
      case "drive":
        if (!SHAPES.includes(s.shape)) errors.push(`${at}: shape は ${SHAPES.join("・")}`);
        if (!num(s.hardness) || s.hardness <= 0 || s.hardness > 64) errors.push(`${at}: hardness は 0より大きく64まで`);
        break;
      case "eq":
        if (!FILTERS.includes(s.kind)) errors.push(`${at}: kind は ${FILTERS.join("・")}`);
        if (!num(s.freq) || s.freq < 10 || s.freq > 22000) errors.push(`${at}: freq は 10〜22000`);
        break;
      case "compressor":
        if (!num(s.threshold) || !num(s.ratio)) errors.push(`${at}: threshold と ratio が必要`);
        break;
      case "ir":
        if (typeof s.wav !== "string" || s.wav.length < 60) errors.push(`${at}: wav（base64のWAV）が必要`);
        break;
      case "worklet":
        if (typeof s.name !== "string" || !/^[a-z0-9-]+$/.test(s.name) || typeof s.code !== "string") errors.push(`${at}: name（英小文字）と code（プログラム）が必要`);
        break;
      case "nam":
        if (typeof s.model !== "string" || !s.model.startsWith("{")) errors.push(`${at}: model（.nam の中身）が必要`);
        break;
      default:
        errors.push(`${at}: 知らない段の種類（${(s as { type?: string })?.type}）`);
    }
  });
  if (errors.length) throw new Error(errors.join("\n"));
  return d as AmpPluginDef;
}

/** プログラム（worklet）を含むか。含むものは、読み込む前に利用者に確かめる。 */
export function hasCode(def: AmpPluginDef): boolean {
  return def.stages.some((s) => s.type === "worklet");
}

/** ジャンル別アンプ（amp.ts）を、アンプ定義の形にする（見本・書き方の手本）。 */
export function presetToPlugin(name: AmpPresetName): AmpPluginDef {
  const p = AMP_PRESETS[name];
  return {
    format: "sunshine-amp", version: 1, id: `genre-${name}`, label: p.label, description: p.genre, author: "サンシャインソフトウェア", license: "このソフトの一部",
    stages: [
      { type: "gain", value: p.drive },
      { type: "drive", shape: p.shape, hardness: p.hardness, asymmetry: p.asymmetry },
      { type: "eq", kind: "lowshelf", freq: 200, gain: p.bassDb },
      { type: "eq", kind: "peaking", freq: p.midHz, gain: p.midDb, q: 0.9 },
      { type: "eq", kind: "highshelf", freq: 3000, gain: p.trebleDb },
      { type: "eq", kind: "highpass", freq: p.highpassHz },
      { type: "eq", kind: "lowpass", freq: p.lowpassHz },
      { type: "gain", value: p.level },
    ],
  };
}

/** 音を作る道具（NAM を使うとき）。 */
export interface AmpPluginHost {
  nam?: { createAmp(ctx: BaseAudioContext, modelJson: string): Promise<AudioWorkletNode> } | null;
}

function base64ToBytes(b64: string): Uint8Array<ArrayBuffer> {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

const loadedWorklets = new WeakMap<BaseAudioContext, Set<string>>();

/**
 * アンプ定義から、音の部品の並びを作る（非同期: IRの読み込み・プログラムの読み込みがあるため）。
 * 返す値は、つないだ部品の一覧（最初が入口、最後が出口）。
 */
export async function buildAmpPlugin(ctx: BaseAudioContext, def: AmpPluginDef, host: AmpPluginHost = {}): Promise<AudioNode[]> {
  const nodes: AudioNode[] = [];
  const push = (n: AudioNode): void => {
    if (nodes.length) nodes[nodes.length - 1].connect(n);
    nodes.push(n);
  };
  push(ctx.createGain());
  for (const s of def.stages) {
    if (s.type === "gain") {
      const g = ctx.createGain();
      g.gain.value = s.value;
      push(g);
    } else if (s.type === "drive") {
      const w = ctx.createWaveShaper();
      w.curve = makeDistortionCurve(s.shape, s.hardness, s.asymmetry ?? 0);
      w.oversample = "4x";
      if (s.amount !== undefined) {
        const g = ctx.createGain();
        g.gain.value = s.amount;
        push(g);
      }
      push(w);
    } else if (s.type === "eq") {
      const f = ctx.createBiquadFilter();
      f.type = s.kind;
      f.frequency.value = s.freq;
      f.gain.value = s.gain ?? 0;
      f.Q.value = s.q ?? 0.7;
      push(f);
    } else if (s.type === "compressor") {
      const c = ctx.createDynamicsCompressor();
      c.threshold.value = s.threshold;
      c.ratio.value = Math.max(1, Math.min(20, s.ratio));
      c.attack.value = s.attack ?? 0.01;
      c.release.value = s.release ?? 0.2;
      push(c);
    } else if (s.type === "ir") {
      const buffer = await ctx.decodeAudioData(base64ToBytes(s.wav).buffer);
      const conv = ctx.createConvolver();
      conv.buffer = buffer;
      const mix = Math.max(0, Math.min(1, s.mix ?? 1));
      const inGain = ctx.createGain();
      const out = ctx.createGain();
      const wet = ctx.createGain();
      const dry = ctx.createGain();
      wet.gain.value = mix;
      dry.gain.value = 1 - mix;
      inGain.connect(conv);
      conv.connect(wet);
      wet.connect(out);
      inGain.connect(dry);
      dry.connect(out);
      push(inGain);
      nodes.push(conv, wet, dry, out);
    } else if (s.type === "worklet") {
      const done = loadedWorklets.get(ctx) ?? new Set<string>();
      if (!done.has(s.name)) {
        await ctx.audioWorklet.addModule(`data:text/javascript;base64,${btoa(unescape(encodeURIComponent(s.code)))}`);
        done.add(s.name);
        loadedWorklets.set(ctx, done);
      }
      push(new AudioWorkletNode(ctx, s.name, { numberOfInputs: 1, numberOfOutputs: 1, outputChannelCount: [2], parameterData: s.params ?? {} }));
    } else if (s.type === "nam") {
      if (!host.nam) continue; // NAM が使えない場所（ゲーム本体）では、この段をとばす
      push(await host.nam.createAmp(ctx, s.model));
    }
  }
  return nodes;
}
