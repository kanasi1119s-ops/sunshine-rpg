/**
 * 鍵盤・シンセ用のアンプ／ラック（2026-10-11、docs/sound/keys-synth-guide.md）。
 *
 * 録音音源（サウンドフォント）の鍵盤・パッド・弦・シンセの音に、現代的できれいな味付けを足す。ギター用のアンプ（amp-rack.ts の各ロール）は
 * 歪みとキャビネットが中心だが、鍵盤に効くのは「テープの温かさ」「揺れ（コーラス・トレモロ・フェイザー・回転スピーカー）」「帯域の整え」なので、別のロールにした。
 * どれも `amp: "tapeWarm"` のようにパートに書いたときだけ働く（書かなければ、これまでの曲の音は1つも変わらない）。
 * 外部のソフト・プラグイン・インパルス応答は使わない。Web Audio の部品（フィルター・ウェーブシェイパー・ディレイ・LFO・圧縮）だけで作る。
 * 実在の機材（特定のエレピ・オルガン・回転スピーカー・シンセ）のモデリングではなく、音の性格の一般的な数値に沿った近似（CLAUDE.md 1-1）。
 *
 * 揺れの部品の数値は、物理から決めた（guide §3）:
 *   テープの揺れ: 速さの変動 ±x% を、遅延の振れ Δτ = x / (2π f) で作る（wow 0.6Hz・±0.15% → 0.4ms、flutter 7Hz・±0.05% → 0.011ms）。
 *   回転スピーカー: ホーンの半径 r≒0.1m、回転 ω のドップラー幅 ≒ r·ω/c。r/c ≒ 0.3ms を遅延の振れにする（6.7Hz で ±1.3%、0.8Hz で ±0.15%）。
 */

/** 鍵盤・シンセ用に足したアンプの種類（`AmpSetting.type` に書ける）。 */
export type KeysAmpType =
  | "tapeWarm" | "vintageKeys" | "tremKeys" | "phaserKeys" | "leslie" | "leslieFast"
  | "padWide" | "stringsEnsemble" | "synthLead" | "synthBass" | "pianoPolish" | "lofiKeys";

export const KEYS_AMP_TYPES: KeysAmpType[] = ["tapeWarm", "vintageKeys", "tremKeys", "phaserKeys", "leslie", "leslieFast", "padWide", "stringsEnsemble", "synthLead", "synthBass", "pianoPolish", "lofiKeys"];

/** 日本語の呼び名と向く場面（作曲ソフトの選択欄と、AIへの案内に使う）。 */
export const KEYS_AMP_INFO: Record<KeysAmpType, { label: string; use: string }> = {
  tapeWarm: { label: "テープの温かさ", use: "鍵盤・パッド・弦なんでも。角を丸めて接着する（ローファイ寄りでない、きれいな温かさ）" },
  vintageKeys: { label: "ヴィンテージ鍵盤", use: "エレピ（keys・fmEpiano）。こもりを引き、2〜3kHz の鈴のような輪郭と、強く弾いたときの軽いバークを足す" },
  tremKeys: { label: "トレモロ（左右に揺れるエレピ）", use: "エレピのバラード・ソウル・ローファイ。約4.8Hz で左右に揺れる" },
  phaserKeys: { label: "フェイザー（ゆっくり）", use: "エレピ・弦・ギターの間奏。約0.3Hz のゆっくりした位相の揺れ（ファンク・AOR・シティポップ）" },
  leslie: { label: "回転スピーカー（ゆっくり）", use: "オルガン（drawbarOrgan）のコラール。0.8Hz のゆっくりした渦" },
  leslieFast: { label: "回転スピーカー（速い）", use: "オルガンの盛り上がり（トレモロ）。約6.7Hz の速い揺れ" },
  padWide: { label: "広いパッド", use: "パッド・合唱・シンセパッド。低域を空け、3〜4kHz の刺さりを引き、3声のアンサンブル・コーラスで左右に広げる" },
  stringsEnsemble: { label: "ストリングス・アンサンブル", use: "弦・シンセ弦。ゆっくり浅い3声のコーラスで、弦の群れの厚み" },
  synthLead: { label: "シンセリード", use: "シンセのリード（sawLead・squareLead 等）。濁りと2〜4kHz の痛さを抑え、軽く歪ませて前に出す" },
  synthBass: { label: "シンセベース", use: "シンセベース・808。低域は素直なまま、上の倍音だけ歪ませて、小さなスピーカーでも聞こえるようにする" },
  pianoPolish: { label: "ピアノの整え", use: "アコースティックピアノ（piano）。箱鳴り（380Hz）を引き、存在感（3.4kHz）と空気（10kHz）をほんの少し足す" },
  lofiKeys: { label: "ローファイ鍵盤", use: "ローファイ・チル。高域を落とし、テープの揺れを深めにして、軽くつぶす（階段状の荒れはなし）" },
};

export interface KeysOptions {
  /** 歪みの深さの倍率（0.5〜2、既定1）。 */
  drive: number;
  /** 高音の調整（dB）。 */
  toneDb: number;
  /** 出力の倍率。 */
  level: number;
}

export interface KeysSegment {
  input: AudioNode;
  output: AudioNode;
  /** 切りはなすときに disconnect する部品すべて。 */
  nodes: AudioNode[];
  /** LFO など、止める必要がある音源。 */
  sources: AudioScheduledSourceNode[];
}

/** 原点の傾きが1の、やわらかく潰れる曲線（k が大きいほど深い）。bias で上下を非対称にする（偶数次の倍音が増える）。 */
export function softSatCurve(k: number, bias = 0, size = 2049): Float32Array<ArrayBuffer> {
  const c = new Float32Array(size);
  const off = Math.tanh(k * bias);
  for (let i = 0; i < size; i++) {
    const x = (i / (size - 1)) * 2 - 1;
    c[i] = (Math.tanh(k * (x + bias)) - off) / k;
  }
  return c;
}

/** 部品を作って記録する道具。 */
class Kit {
  nodes: AudioNode[] = [];
  sources: AudioScheduledSourceNode[] = [];
  constructor(readonly ctx: BaseAudioContext) {}
  private keep<T extends AudioNode>(n: T): T {
    this.nodes.push(n);
    return n;
  }
  gain(v: number): GainNode {
    const g = this.keep(this.ctx.createGain());
    g.gain.value = v;
    return g;
  }
  biquad(type: BiquadFilterType, freq: number, gain = 0, q = 0.7): BiquadFilterNode {
    const f = this.keep(this.ctx.createBiquadFilter());
    f.type = type;
    f.frequency.value = freq;
    f.gain.value = gain;
    f.Q.value = q;
    return f;
  }
  /** 4次（-24dB/oct）のローパス／ハイパス（同じ周波数の2段。つなぐのは呼び出し側）。クロスオーバーに使う。 */
  lr4(type: "lowpass" | "highpass", freq: number): [BiquadFilterNode, BiquadFilterNode] {
    return [this.biquad(type, freq, 0, -3.01), this.biquad(type, freq, 0, -3.01)];
  }
  shaper(k: number, bias = 0, oversample: OverSampleType = "2x"): WaveShaperNode {
    const s = this.keep(this.ctx.createWaveShaper());
    s.curve = softSatCurve(k, bias);
    s.oversample = oversample;
    return s;
  }
  comp(threshold: number, ratio: number, attack: number, release: number, knee = 6): DynamicsCompressorNode {
    const c = this.keep(this.ctx.createDynamicsCompressor());
    c.threshold.value = threshold;
    c.knee.value = knee;
    c.ratio.value = ratio;
    c.attack.value = attack;
    c.release.value = release;
    return c;
  }
  delay(centerSec: number, maxSec = 0.05): DelayNode {
    const d = this.keep(this.ctx.createDelay(maxSec));
    d.delayTime.value = centerSec;
    return d;
  }
  /** 正弦の LFO。phase（ラジアン）だけ位相をずらす（sin(ωt + phase)）。 */
  lfo(hz: number, phase = 0): OscillatorNode {
    const o = this.ctx.createOscillator();
    if (phase === 0) o.type = "sine";
    else o.setPeriodicWave(this.ctx.createPeriodicWave(new Float32Array([0, Math.sin(phase)]), new Float32Array([0, Math.cos(phase)])));
    o.frequency.value = hz;
    o.start();
    this.sources.push(o);
    return this.keep(o);
  }
  /** LFO を amount 倍して、param に足す。 */
  modulate(param: AudioParam, hz: number, amount: number, phase = 0): void {
    const g = this.gain(amount);
    this.lfo(hz, phase).connect(g);
    g.connect(param);
  }
  /** 入口から順につなぐ。最後の部品を返す。 */
  chain(...nodes: AudioNode[]): AudioNode {
    for (let i = 0; i + 1 < nodes.length; i++) nodes[i].connect(nodes[i + 1]);
    return nodes[nodes.length - 1];
  }
  /** 左右に分ける（0=左・1=右）。 */
  splitter(): ChannelSplitterNode {
    return this.keep(this.ctx.createChannelSplitter(2));
  }
  merger(): ChannelMergerNode {
    return this.keep(this.ctx.createChannelMerger(2));
  }
  /** 左右の和を1チャンネルにする入口。 */
  monoSum(): GainNode {
    const g = this.gain(1);
    g.channelCount = 1;
    g.channelCountMode = "explicit";
    return g;
  }
}

interface Voice {
  /** LFO の速さ（Hz）。 */
  hz: number;
  /** 位相（ラジアン）。 */
  phase: number;
}

/**
 * 左右で逆の位相に揺らす、複数声のコーラス（アンサンブル）。入力はステレオ。
 * center＝遅れの中心（秒）、depth＝遅れの振れ（秒）、wet＝揺らした音の量、dry＝そのままの音の量。
 */
function ensembleChorus(k: Kit, input: AudioNode, voices: Voice[], centerSec: number, depthSec: number, wet: number, dry: number): AudioNode {
  const out = k.gain(1);
  const dryG = k.gain(dry);
  input.connect(dryG);
  dryG.connect(out);
  const sp = k.splitter();
  const mg = k.merger();
  input.connect(sp);
  const per = wet / Math.sqrt(voices.length);
  for (let ch = 0; ch < 2; ch++) {
    const sum = k.gain(per);
    voices.forEach((v, i) => {
      // 声ごとに遅れの中心を少しずらして、くし形の凹みが重ならないようにする
      const d = k.delay(centerSec * (1 + 0.12 * (i - (voices.length - 1) / 2)), Math.max(0.05, centerSec * 3));
      k.modulate(d.delayTime, v.hz, depthSec, v.phase + ch * Math.PI);
      sp.connect(d, ch, 0);
      d.connect(sum);
    });
    sum.connect(mg, 0, ch);
  }
  mg.connect(out);
  return out;
}

/** テープの揺れ（wow と flutter）。速さの変動を遅延の振れにしたもの。wowSec／flutterSec＝遅れの振れ（秒）。 */
function tapeWobble(k: Kit, wowSec: number, flutterSec: number): DelayNode {
  const d = k.delay(0.004, 0.05);
  k.modulate(d.delayTime, 0.6, wowSec);
  k.modulate(d.delayTime, 0.93, wowSec * 0.5, 1.3);
  k.modulate(d.delayTime, 7.1, flutterSec, 0.7);
  return d;
}

/** 左右に揺れる（オートパン。エレピのトレモロ）。左右の音量を逆の位相で ±depth/2 揺らす。入口と出口を返す。 */
function autoPan(k: Kit, hz: number, depth: number): { first: AudioNode; last: AudioNode } {
  const sp = k.splitter();
  const mg = k.merger();
  for (let ch = 0; ch < 2; ch++) {
    const g = k.gain(1 - depth / 2);
    k.modulate(g.gain, hz, depth / 2, ch * Math.PI);
    sp.connect(g, ch, 0);
    g.connect(mg, 0, ch);
  }
  return { first: sp, last: mg };
}

/** 4段のオールパスのフェイザー（位相の凹みが動く）。hz＝揺れの速さ、sweep＝凹みの動く幅（中心周波数に対する倍率 0〜1）、mix＝揺らした音の量。 */
function phaser(k: Kit, hz: number, sweep: number, mix: number): { first: AudioNode; last: AudioNode } {
  const input = k.gain(1);
  const out = k.gain(1);
  const dry = k.gain(1 - mix * 0.5);
  const wet = k.gain(mix);
  input.connect(dry);
  dry.connect(out);
  let prev: AudioNode = input;
  for (const f0 of [350, 800, 1700, 3500]) {
    const ap = k.biquad("allpass", f0, 0, 0.8);
    k.modulate(ap.frequency, hz, f0 * sweep);
    prev.connect(ap);
    prev = ap;
  }
  prev.connect(wet);
  wet.connect(out);
  return { first: input, last: out };
}

/**
 * 回転スピーカー（ホーンとドラム）。入力を 800Hz で分け、上（ホーン）と下（ドラム）を別の速さで回す。
 * 回るたびに、左右の耳（マイク）に届くまでの遅れ（ドップラー）と音量（向き）が、左右で逆の位相に変わる。
 */
function rotary(k: Kit, hornHz: number, drumHz: number): { first: AudioNode; last: AudioNode } {
  const input = k.gain(1);
  const mono = k.monoSum();
  input.connect(mono);
  const [hpA, hpB] = k.lr4("highpass", 800);
  const [lpA, lpB] = k.lr4("lowpass", 800);
  k.chain(hpA, hpB);
  k.chain(lpA, lpB);
  mono.connect(hpA);
  mono.connect(lpA);
  const mg = k.merger();
  const out = k.gain(1);
  const dryG = k.gain(0.22);
  input.connect(dryG);
  dryG.connect(out);
  const rotor = (src: AudioNode, hz: number, swingSec: number, am: number, level: number): void => {
    for (let ch = 0; ch < 2; ch++) {
      const del = k.delay(0.0012, 0.01);
      // 遅れが減っていく（近づく）あたりで音量が最大: 音量 = (1 - am/2) - (am/2)cos(ωt)
      k.modulate(del.delayTime, hz, swingSec, ch * Math.PI);
      const g = k.gain((1 - am / 2) * level);
      k.modulate(g.gain, hz, (am / 2) * level, ch * Math.PI - Math.PI / 2);
      src.connect(del);
      del.connect(g);
      g.connect(mg, 0, ch);
    }
  };
  rotor(hpB, hornHz, 0.0003, 0.55, 0.9);
  rotor(lpB, drumHz, 0.00012, 0.3, 1.0);
  mg.connect(out);
  return { first: input, last: out };
}

/** 全体の仕上げ（高音の調整→出力）と、入口・出口をそろえる。 */
function finish(k: Kit, o: KeysOptions, first: AudioNode, last: AudioNode): KeysSegment {
  const input = k.gain(1);
  const output = k.gain(o.level);
  const tone = k.biquad("highshelf", 3500, o.toneDb);
  input.connect(first);
  last.connect(tone);
  tone.connect(output);
  return { input, output, nodes: k.nodes, sources: k.sources };
}

/** 順につないで、先頭と末尾を返す。 */
function line(k: Kit, ...nodes: AudioNode[]): { first: AudioNode; last: AudioNode } {
  k.chain(...nodes);
  return { first: nodes[0], last: nodes[nodes.length - 1] };
}

/** 2つの区間を続ける。 */
function join(k: Kit, a: { first: AudioNode; last: AudioNode }, b: { first: AudioNode; last: AudioNode }): { first: AudioNode; last: AudioNode } {
  a.last.connect(b.first);
  void k;
  return { first: a.first, last: b.last };
}

/** 3声のアンサンブル・コーラスの区間（入口の gain → 出口）。 */
function ensemble(k: Kit, voices: Voice[], centerSec: number, depthSec: number, wet: number, dry: number): { first: AudioNode; last: AudioNode } {
  const input = k.gain(1);
  return { first: input, last: ensembleChorus(k, input, voices, centerSec, depthSec, wet, dry) };
}
const THIRDS = [0, (2 * Math.PI) / 3, (4 * Math.PI) / 3];
const voices3 = (hz: number | [number, number, number]): Voice[] => THIRDS.map((phase, i) => ({ hz: Array.isArray(hz) ? hz[i] : hz, phase }));

/** 鍵盤・シンセ用のロールを組み立てる。 */
export function buildKeysAmp(ctx: BaseAudioContext, role: KeysAmpType, o: KeysOptions): KeysSegment {
  const k = new Kit(ctx);
  const d = Math.max(0.5, Math.min(2, o.drive));
  const eq = (type: BiquadFilterType, f: number, g = 0, q = 0.7): BiquadFilterNode => k.biquad(type, f, g, q);
  const dc = (): BiquadFilterNode => eq("highpass", 20);
  let seg: { first: AudioNode; last: AudioNode };
  switch (role) {
    case "tapeWarm":
      // 低域のふくらみ（ヘッドバンプ 90Hz +1.5dB）→ 箱鳴り 350Hz −1dB → やわらかい飽和 → 高域を丸める（9kHz〜 −2.5dB・13kHz で切る）→ 揺れ → ごく弱い圧縮
      seg = line(k, eq("highpass", 28), eq("lowshelf", 90, 1.5), eq("peaking", 350, -1, 0.8), k.shaper(1.8 * d, 0.02), dc(), eq("highshelf", 9000, -2.5), eq("lowpass", 13000, 0, 0.6), tapeWobble(k, 0.0003, 0.00001), k.comp(-30, 1.5, 0.03, 0.25));
      break;
    case "vintageKeys":
      seg = line(k, eq("highpass", 60), eq("peaking", 300, -2.5, 0.8), eq("peaking", 2600, 2, 0.9), k.shaper(2.4 * d, 0.05), dc(), eq("highshelf", 7500, -3), eq("lowpass", 11000, 0, 0.6), k.comp(-28, 2, 0.02, 0.2));
      break;
    case "tremKeys":
      seg = join(k, line(k, eq("highpass", 60), eq("peaking", 300, -2.5, 0.8), eq("peaking", 2600, 2, 0.9), k.shaper(2.4 * d, 0.05), dc(), eq("highshelf", 7500, -3), eq("lowpass", 11000, 0, 0.6)), join(k, autoPan(k, 4.8, 0.4), line(k, k.comp(-28, 2, 0.02, 0.2))));
      break;
    case "phaserKeys":
      seg = join(k, line(k, eq("highpass", 60), eq("peaking", 300, -2, 0.8), k.shaper(1.6 * d, 0.03), dc(), eq("highshelf", 8000, -2), eq("lowpass", 12000, 0, 0.6)), join(k, phaser(k, 0.3, 0.6, 0.6), line(k, k.comp(-28, 1.8, 0.02, 0.2))));
      break;
    case "leslie":
      seg = join(k, line(k, k.shaper(1.5 * d, 0.03), dc()), rotary(k, 0.8, 0.67));
      break;
    case "leslieFast":
      seg = join(k, line(k, k.shaper(1.5 * d, 0.03), dc()), rotary(k, 6.7, 5.7));
      break;
    case "padWide":
      seg = join(k, line(k, eq("highpass", 150), eq("peaking", 3600, -3.5, 0.8)), join(k, ensemble(k, voices3([0.37, 0.61, 0.83]), 0.014, 0.003, 0.5, 0.75), line(k, eq("lowpass", 10500, 0, 0.6), k.comp(-26, 1.8, 0.05, 0.3))));
      break;
    case "stringsEnsemble":
      seg = join(k, line(k, eq("highpass", 100), eq("lowshelf", 250, 1), eq("peaking", 2600, -2, 1)), join(k, ensemble(k, voices3(0.55), 0.0055, 0.0016, 0.45, 0.8), line(k, eq("lowpass", 9500, 0, 0.6), k.comp(-26, 1.8, 0.05, 0.3))));
      break;
    case "synthLead":
      seg = line(k, eq("highpass", 130), eq("peaking", 220, -2, 0.9), eq("peaking", 1200, 1.2, 0.8), eq("peaking", 3100, -2.5, 1), k.shaper(1.6 * d, 0.04), dc(), eq("highshelf", 8000, -2), eq("lowpass", 11500, 0, 0.6), k.comp(-24, 3, 0.008, 0.12));
      break;
    case "synthBass": {
      // 低域（140Hz 未満）は素直に、上（140Hz 以上）だけ歪ませて足す（小さなスピーカーでも聞こえる倍音）
      const input = k.gain(1);
      const out = k.gain(1);
      const low = line(k, ...k.lr4("lowpass", 140));
      const hi = line(k, ...k.lr4("highpass", 140), k.shaper(8 * d, 0.03), dc(), eq("lowpass", 3500, 0, 0.7), k.gain(0.5));
      input.connect(low.first);
      input.connect(hi.first);
      low.last.connect(out);
      hi.last.connect(out);
      seg = join(k, { first: input, last: out }, line(k, eq("highpass", 30), k.comp(-22, 4, 0.015, 0.09)));
      break;
    }
    case "pianoPolish":
      seg = line(k, eq("highpass", 55), eq("lowshelf", 120, 1), eq("peaking", 380, -2, 1), eq("peaking", 3400, 1.2, 0.8), eq("highshelf", 10000, 1.5), eq("lowpass", 15000, 0, 0.6), k.comp(-26, 2, 0.025, 0.2));
      break;
    case "lofiKeys":
      seg = line(k, eq("highpass", 90), eq("peaking", 350, -1, 0.8), k.shaper(2.4 * d, 0.04), dc(), eq("highshelf", 3000, -3), eq("lowpass", 5200, 0, 0.7), tapeWobble(k, 0.0006, 0.00004), k.comp(-28, 2, 0.02, 0.2));
      break;
  }
  return finish(k, o, seg.first, seg.last);
}
