/**
 * 録音音源の各チャンネルに、楽器ごとの「アンプ・キャビネット・ミキサー」をかける。
 * ギター: オーバードライブ（歪みは浅く粘る）／ディストーション（深く歪む）／メタルゾーン（高音域を絞り、低音を締め、中域をえぐって、強く歪ませる）
 * ベース: 重低音を持ち上げ、メタルでは歪みをまぜて、弦の輪郭も出す
 * ドラム: ロックは温かい厚み、メタルは低音の重さと3〜5kHzのアタックを強調
 */

export type Tone = "rock" | "metal" | "prs";
type Role = "overdrive" | "distortion" | "metal" | "prs" | "clean" | "bass" | "bassMetal" | "drumsRock" | "drumsMetal" | "thru";

const CURVES = new Map<string, Float32Array<ArrayBuffer>>();
/** 真空管アンプのように、少し非対称にクリップする波形。drive が大きいほど深く歪む。 */
function curve(drive: number, bias: number): Float32Array<ArrayBuffer> {
  const key = `${drive}|${bias}`;
  let c = CURVES.get(key);
  if (!c) {
    c = new Float32Array(4096);
    const offset = Math.tanh(drive * bias);
    for (let i = 0; i < c.length; i++) {
      const x = (i / (c.length - 1)) * 2 - 1;
      c[i] = Math.tanh(drive * (x + bias)) - offset;
    }
    CURVES.set(key, c);
  }
  return c;
}

const GUITAR_PROGRAMS = { overdrive: 29, distortion: 30, clean: 27 };
const BASS_PROGRAMS = new Set([32, 33, 34, 35, 36, 37, 38, 39]);

export class AmpRack {
  private inputs: GainNode[];
  private built: AudioNode[][] = [];

  constructor(private ctx: BaseAudioContext, private destination: AudioNode) {
    this.inputs = Array.from({ length: 16 }, () => ctx.createGain());
    this.built = Array.from({ length: 16 }, () => []);
    for (let ch = 0; ch < 16; ch++) {
      this.inputs[ch].connect(destination);
      this.built[ch] = [];
    }
  }

  input(channel: number): AudioNode {
    return this.inputs[channel];
  }

  /** 曲が変わるたびに、各チャンネルの楽器（GMの番号）と曲の音色に合わせて、機材をつなぎ直す。 */
  configure(programs: Record<number, number>, tone: Tone, drumChannel = 9): void {
    for (let ch = 0; ch < 16; ch++) {
      const input = this.inputs[ch];
      input.disconnect();
      for (const node of this.built[ch]) node.disconnect();
      this.built[ch] = [];
      const role = this.roleOf(ch === drumChannel ? -1 : programs[ch], tone);
      const nodes = this.build(role, input);
      this.built[ch] = nodes;
    }
  }

  private roleOf(program: number | undefined, tone: Tone): Role {
    if (program === -1) return tone !== "rock" ? "drumsMetal" : "drumsRock";
    if (program === undefined) return "thru";
    if (program === GUITAR_PROGRAMS.overdrive) return "overdrive";
    if (program === GUITAR_PROGRAMS.distortion) return tone === "metal" ? "metal" : tone === "prs" ? "prs" : "distortion";
    if (program === GUITAR_PROGRAMS.clean) return "clean";
    if (BASS_PROGRAMS.has(program)) return tone !== "rock" ? "bassMetal" : "bass";
    return "thru";
  }

  private filter(type: BiquadFilterType, freq: number, gain = 0, q = 0.7): BiquadFilterNode {
    const f = this.ctx.createBiquadFilter();
    f.type = type;
    f.frequency.value = freq;
    f.gain.value = gain;
    f.Q.value = q;
    return f;
  }
  private shaper(drive: number, bias: number): WaveShaperNode {
    const s = this.ctx.createWaveShaper();
    s.curve = curve(drive, bias);
    s.oversample = "4x";
    return s;
  }
  private gain(value: number): GainNode {
    const g = this.ctx.createGain();
    g.gain.value = value;
    return g;
  }

  /** ノードを順番につないで、最後を出口につなぐ。 */
  private chain(input: AudioNode, nodes: AudioNode[]): AudioNode[] {
    let prev: AudioNode = input;
    for (const n of nodes) {
      prev.connect(n);
      prev = n;
    }
    prev.connect(this.destination);
    return nodes;
  }

  private build(role: Role, input: AudioNode): AudioNode[] {
    switch (role) {
      case "overdrive":
        // オーバードライブ: ゆるく歪み、弾き方の強弱が音に残る。中域（900Hz付近）が前に出る
        return this.chain(input, [this.filter("highpass", 85), this.filter("peaking", 900, 4.5, 0.8), this.gain(3.4), this.shaper(3.4, 0.09), this.filter("peaking", 2400, 2, 1), this.filter("lowpass", 5600, 0, 0.9), this.gain(0.5)]);
      case "distortion":
        // ディストーション: 深く歪み、音が伸びる。低音は少し締める
        return this.chain(input, [this.filter("highpass", 110), this.filter("peaking", 1100, 3, 0.9), this.gain(3.6), this.shaper(5, 0.06), this.filter("peaking", 3000, 1, 0.9), this.filter("lowpass", 4200, 0, 0.8), this.gain(0.46)]);
      case "metal":
        // メタルゾーン: 前段で低音をしっかり削って音を「締め」、中域を持ち上げて強く歪ませ（2段）、後段で中域をえぐって、高音の刺さりと重い低音を足す
        return this.chain(input, [
          this.filter("highpass", 130, 0, 0.8), this.filter("peaking", 750, 5, 0.8), this.gain(4.6), this.shaper(9.5, 0.06),
          this.filter("lowpass", 5200, 0, 0.7), this.gain(1.9), this.shaper(3.8, 0.04),
          this.filter("peaking", 480, -4, 1), this.filter("peaking", 3400, 3, 1), this.filter("lowshelf", 110, 4), this.filter("lowpass", 4700, 0, 0.8), this.gain(0.34),
        ]);
      case "prs":
        // 粒立ちがよく歌う、なめらかなギター（PRS系のような澄んだ倍音）: 深すぎない歪みで、弾き方の強弱と1弦ずつの輪郭が残る。
        // 中域（1.2kHz）で「歌う」芯を出し、3.8kHzの輝きは足しつつ、6.5kHz付近のジャリつきを抑え、低音は締めすぎず丸く
        return this.chain(input, [
          this.filter("highpass", 95, 0, 0.8), this.filter("peaking", 1200, 3, 0.9), this.gain(2.8), this.shaper(4.4, 0.07),
          this.filter("peaking", 220, 1.5, 0.9), this.filter("peaking", 3800, 1.8, 0.9), this.filter("peaking", 6500, -2.5, 1), this.filter("lowpass", 6000, 0, 0.6), this.filter("lowshelf", 120, 1.5),
          this.compressor(-18, 2.2, 0.02, 0.2), this.gain(0.5),
        ]);
      case "clean":
        return this.chain(input, [this.filter("highpass", 70), this.filter("peaking", 3500, 2.5, 0.9), this.filter("highshelf", 8000, 2), this.gain(0.95)]);
      case "bass":
        return this.chain(input, [this.filter("lowshelf", 80, 4), this.filter("peaking", 750, 2.5, 1), this.gain(1.05)]);
      case "bassMetal":
        // メタルのベース: 重低音（60〜80Hz）を強く持ち上げ、軽く歪ませて弦の輪郭（700Hz〜1.5kHz）を出す
        return this.chain(input, [this.filter("lowshelf", 75, 8.5), this.filter("peaking", 65, 3, 1.1), this.shaper(2.2, 0.04), this.filter("peaking", 900, 3.5, 1), this.filter("peaking", 2200, 2, 1), this.filter("lowpass", 5200), this.gain(0.95)]);
      case "drumsRock":
        // ロックのドラム: 太鼓の胴鳴りと部屋の響きが感じられる、温かく厚い音
        return this.chain(input, [this.filter("lowshelf", 90, 3), this.filter("peaking", 380, -2, 1), this.filter("peaking", 3000, 2.5, 0.9), this.filter("highshelf", 9500, 2), this.compressor(-16, 3, 0.012, 0.14), this.gain(1.1)]);
      case "drumsMetal":
        // メタルのドラム: キックの重さ（60〜80Hz）と、3〜5kHzのアタックの立ち上がりを強く出し、箱鳴りの帯域を削って締める。強くつぶして密度を上げる
        return this.chain(input, [this.filter("lowshelf", 80, 4.5), this.filter("peaking", 320, -4, 1.1), this.filter("peaking", 4200, 5, 1), this.filter("highshelf", 10000, 3), this.compressor(-20, 5, 0.006, 0.1), this.gain(1.2)]);
      default:
        return this.chain(input, []);
    }
  }

  private compressor(threshold: number, ratio: number, attack: number, release: number): DynamicsCompressorNode {
    const c = this.ctx.createDynamicsCompressor();
    c.threshold.value = threshold;
    c.knee.value = 6;
    c.ratio.value = ratio;
    c.attack.value = attack;
    c.release.value = release;
    return c;
  }
}
