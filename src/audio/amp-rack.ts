/**
 * 録音音源の各チャンネルに、楽器ごとの「アンプ・キャビネット・ミキサー」をかける。
 * ギター: オーバードライブ（歪みは浅く粘る）／ディストーション（深く歪む）／メタルゾーン（高音域を絞り、低音を締め、中域をえぐって、強く歪ませる）
 * ベース: 重低音を持ち上げ、メタルでは歪みをまぜて、弦の輪郭も出す
 * ドラム: ロックは温かい厚み、メタルは低音の重さと3〜5kHzのアタックを強調
 */

import type { AmpSetting, GenreAmpType } from "./score";
import { AMP_PRESETS, makeDistortionCurve } from "./amp";
import { buildAmpPlugin, type AmpPluginDef } from "./amp-plugins";
import type { NamHost } from "./nam/nam-host";

export type Tone = "rock" | "metal" | "prs";
/** チャンネルごとの、音づくりの上書き（トラックの`amp`と、左右の位置）。 */
export interface ChannelAmp {
  amp: AmpSetting;
  pan: number;
}
type Role = "plugin" | "genre" | "nam" | "overdrive" | "distortion" | "metal" | "prs" | "clean" | "bass" | "bassMetal" | "drumsRock" | "drumsMetal" | "kick" | "snare" | "hat" | "cym" | "thru" | GenreAmpType;

/** ジャンル別のアンプの種類（`score.ts` の `GenreAmpType` と同じ並び）。 */
/** ドラムを太鼓ごとに分けたときの、チャンネルの役割。 */
export type DrumPiece = "kick" | "snare" | "hat" | "cym";

export const GENRE_AMP_TYPES: GenreAmpType[] = ["jazz", "blues", "funk", "crunch", "hardrock", "punk", "fuzz", "shoegaze", "lofi", "retro8bit", "radio", "loudmetal", "loudrock", "delicate"];

const STEP_CURVES = new Map<number, Float32Array<ArrayBuffer>>();
/** 波形を階段状にする（ビットを落としたような粗い音）。levels は片側の段数。 */
export function stepCurve(levels: number): Float32Array<ArrayBuffer> {
  let c = STEP_CURVES.get(levels);
  if (!c) {
    c = new Float32Array(4097);
    for (let i = 0; i < c.length; i++) {
      const x = (i / (c.length - 1)) * 2 - 1;
      c[i] = Math.round(x * levels) / levels;
    }
    STEP_CURVES.set(levels, c);
  }
  return c;
}

/**
 * amp.ts のプリセット（type=genre）を、実際に鳴らす種類にする。
 * 同じジャンルの直接の種類（jazz など。実ブラウザで音量をそろえたもの）があれば、そちらで鳴らす。rock だけは amp.ts の組み立てで鳴らす。
 */
function genreToType(amp: AmpSetting): AmpSetting["type"] {
  if (amp.type !== "genre") return amp.type;
  const p = amp.preset ?? "rock";
  if ((GENRE_AMP_TYPES as string[]).includes(p)) return p as GenreAmpType;
  if (p === "clean" || p === "metal") return p;
  return "genre";
}

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
  private nam: NamHost | null = null;
  private models: Record<string, string> = {};
  private plugins: Record<string, AmpPluginDef> = {};
  private generation = 0;
  private pending: Promise<unknown>[] = [];
  private tone: Tone = "rock";
  /** 太鼓ごとの経路の出口。ここで、原音＋強く圧縮した音（パラレルコンプ）に分けて、まとめて出口へ送る。 */
  private drumBus: GainNode;

  constructor(private ctx: BaseAudioContext, private destination: AudioNode) {
    this.drumBus = ctx.createGain();
    this.drumBus.connect(destination);
    const wetComp = this.compressor(-26, 8, 0.01, 0.08);
    const wetGain = this.gain(0.3);
    this.drumBus.connect(wetComp);
    wetComp.connect(wetGain);
    wetGain.connect(destination);
    this.inputs = Array.from({ length: 16 }, () => ctx.createGain());
    this.built = Array.from({ length: 16 }, () => []);
    for (let ch = 0; ch < 16; ch++) {
      this.inputs[ch].connect(destination);
      this.built[ch] = [];
    }
  }

  /** NAM（実際のアンプを学習したモデル）を使えるようにする（作曲ソフトだけ）。 */
  setNam(host: NamHost | null): void {
    this.nam = host;
  }

  /** NAMのアンプの準備（モデルの読み込み）が終わるのを待つ。WAVの書き出し（オフライン）用。 */
  async whenReady(): Promise<void> {
    await Promise.all(this.pending);
  }

  input(channel: number): AudioNode {
    return this.inputs[channel];
  }

  /** 曲が変わるたびに、各チャンネルの楽器（GMの番号）と曲の音色に合わせて、機材をつなぎ直す。 */
  configure(programs: Record<number, number>, tone: Tone, drumChannel = 9, amps: Record<number, ChannelAmp> = {}, models: Record<string, string> = {}, plugins: Record<string, AmpPluginDef> = {}, drums: Record<number, DrumPiece> = {}): void {
    this.generation++;
    this.tone = tone;
    this.models = models;
    this.plugins = plugins;
    this.pending = [];
    for (let ch = 0; ch < 16; ch++) {
      const input = this.inputs[ch];
      input.disconnect();
      for (const node of this.built[ch]) node.disconnect();
      this.built[ch] = [];
      const override = ch === drumChannel || drums[ch] ? undefined : amps[ch];
      const role: Role = drums[ch] ? drums[ch] : override && override.amp.type !== "auto" ? this.roleFromType(genreToType(override.amp), ch === drumChannel ? -1 : programs[ch], tone) : this.roleOf(ch === drumChannel ? -1 : programs[ch], tone);
      const nodes = this.build(role, input, override);
      this.built[ch] = nodes;
    }
  }

  private roleFromType(type: AmpSetting["type"], program: number | undefined, tone: Tone): Role {
    if (type === "nam") return this.nam ? "nam" : this.roleOf(program, tone);
    if (type === "genre") return "genre";
    if (type === "plugin") return "plugin";
    if (type === "clean" || type === "overdrive" || type === "distortion" || type === "metal" || type === "prs") return type;
    if ((GENRE_AMP_TYPES as string[]).includes(type)) return type as GenreAmpType;
    return this.roleOf(program, tone);
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
  private chain(input: AudioNode, nodes: AudioNode[], dest: AudioNode = this.destination): AudioNode[] {
    let prev: AudioNode = input;
    for (const n of nodes) {
      prev.connect(n);
      prev = n;
    }
    prev.connect(dest);
    return nodes;
  }

  private build(role: Role, input: AudioNode, override?: ChannelAmp): AudioNode[] {
    const d = override?.amp.drive ?? 1;
    const toneDb = override?.amp.tone ?? 0;
    const level = override?.amp.level ?? 1;
    // 音づくりの上書き（歪みの深さ・高音・出力）がある歪み系のギターは、最後に高音の調整と出力の段を足す
    const tail = (nodes: AudioNode[]): AudioNode[] => (override ? [...nodes, this.filter("highshelf", 3500, toneDb), this.gain(level)] : nodes);
    switch (role) {
      case "nam":
        return this.buildNam(input, override!);
      case "plugin":
        return this.buildPlugin(input, override!);
      case "genre": {
        // ジャンル別アンプ（amp.ts）: 入力の増幅 → 歪み → 低音・中音・高音 → キャビネット（低域・高域カット） → 出力
        const p = AMP_PRESETS[override?.amp.preset ?? "rock"] ?? AMP_PRESETS.rock;
        const shaper = this.ctx.createWaveShaper();
        shaper.curve = makeDistortionCurve(p.shape, p.hardness, p.asymmetry);
        shaper.oversample = "4x";
        // 録音音源の1チャンネルの音は小さめなので、合成音のときより少し強めに入れる
        return this.chain(input, tail([
          this.gain(Math.max(1, p.drive * 1.6) * d), shaper,
          this.filter("lowshelf", 200, p.bassDb), this.filter("peaking", p.midHz, p.midDb, 0.9), this.filter("highshelf", 3000, p.trebleDb),
          this.filter("highpass", p.highpassHz, 0, 0.7), this.filter("lowpass", p.lowpassHz, 0, 0.7), this.gain(p.level * (p.drive > 1.5 ? 0.6 : 0.95)),
        ]));
      }
      case "overdrive":
        // オーバードライブ: ゆるく歪み、弾き方の強弱が音に残る。中域（900Hz付近）が前に出る
        return this.chain(input, tail([this.filter("highpass", 85), this.filter("peaking", 900, 4.5, 0.8), this.gain(3.4 * d), this.shaper(3.4 * d, 0.09), this.filter("peaking", 2400, 2, 1), this.filter("lowpass", 5600, 0, 0.9), this.gain(0.5)]));
      case "distortion":
        // ディストーション: 深く歪み、音が伸びる。低音は少し締める
        return this.chain(input, tail([this.filter("highpass", 110), this.filter("peaking", 1100, 3, 0.9), this.gain(3.6 * d), this.shaper(5 * d, 0.06), this.filter("peaking", 3000, 1, 0.9), this.filter("lowpass", 4200, 0, 0.8), this.gain(0.46)]));
      case "metal":
        // メタルゾーン: 前段で低音をしっかり削って音を「締め」、中域を持ち上げて強く歪ませ（2段）、後段で中域をえぐって、高音の刺さりと重い低音を足す
        return this.chain(input, tail([
          this.filter("highpass", 130, 0, 0.8), this.filter("peaking", 750, 5, 0.8), this.gain(4.6 * d), this.shaper(9.5 * d, 0.06),
          this.filter("lowpass", 5200, 0, 0.7), this.gain(1.9), this.shaper(3.8, 0.04),
          this.filter("peaking", 480, -4, 1), this.filter("peaking", 3400, 3, 1), this.filter("lowshelf", 110, 4), this.filter("lowpass", 4700, 0, 0.8), this.gain(0.34),
        ]));
      case "prs":
        // 粒立ちがよく歌う、なめらかなギター（PRS系のような澄んだ倍音）: 深すぎない歪みで、弾き方の強弱と1弦ずつの輪郭が残る。
        // 中域（1.2kHz）で「歌う」芯を出し、3.8kHzの輝きは足しつつ、6.5kHz付近のジャリつきを抑え、低音は締めすぎず丸く
        return this.chain(input, tail([
          this.filter("highpass", 95, 0, 0.8), this.filter("peaking", 1200, 3, 0.9), this.gain(2.8 * d), this.shaper(4.4 * d, 0.07),
          this.filter("peaking", 220, 1.5, 0.9), this.filter("peaking", 3800, 1.8, 0.9), this.filter("peaking", 6500, -2.5, 1), this.filter("lowpass", 6000, 0, 0.6), this.filter("lowshelf", 120, 1.5),
          this.compressor(-18, 2.2, 0.02, 0.2), this.gain(0.5),
        ]));
      case "clean":
        return this.chain(input, [this.filter("highpass", 70), this.filter("peaking", 3500, 2.5, 0.9), this.filter("highshelf", 8000, 2), this.gain(0.95)]);
      case "bass":
        // ベース: 30Hz以下の不要な低音を切り、60〜120Hzで重さ、250〜400Hzの濁りを少し削り、700Hz〜1kHzで輪郭を出す。
        // 弾いた瞬間（ピック・指のアタック）を残すため、アタックを遅め（25ms）にして軽く圧縮し、音量をそろえる
        return this.chain(input, [this.filter("highpass", 32, 0, 0.7), this.filter("lowshelf", 80, 4), this.filter("peaking", 320, -2, 1), this.filter("peaking", 750, 2.5, 1), this.compressor(-20, 3, 0.025, 0.12), this.gain(1.05)]);
      case "bassMetal":
        // メタルのベース: 低音と高音で道を分ける（約200Hz）。低い側は歪ませず重く（60〜80Hz）、高い側だけ軽く歪ませて弦の輪郭（700Hz〜2kHz）を出す。
        // 低音まで歪ませると濁るので、歪みは上の帯域だけにかける。最後にアタック遅めで軽く圧縮
        return this.parallel(input, [
          [this.filter("highpass", 32, 0, 0.7), this.filter("lowpass", 200, 0, 0.7), this.filter("lowshelf", 75, 6), this.filter("peaking", 65, 3, 1.1)],
          [this.filter("highpass", 200, 0, 0.7), this.shaper(2.4, 0.04), this.filter("peaking", 900, 3.5, 1), this.filter("peaking", 2200, 2, 1), this.filter("lowpass", 5200, 0, 0.8), this.gain(0.9)],
        ], [this.compressor(-20, 3, 0.025, 0.12), this.gain(0.95)]);
      case "drumsRock":
        // ロックのドラム: 太鼓の胴鳴りと部屋の響きが感じられる、温かく厚い音。足元の不要な低音（35Hz以下）は切る。
        // 原音に、強く圧縮した音を混ぜて（パラレルコンプ）、アタックを残したまま厚みを足す
        return this.parallel(input, [
          [this.filter("highpass", 35, 0, 0.7), this.filter("lowshelf", 90, 3), this.filter("peaking", 380, -2, 1), this.filter("peaking", 3000, 2.5, 0.9), this.filter("highshelf", 9500, 2), this.compressor(-16, 3, 0.02, 0.14)],
          [this.filter("highpass", 35, 0, 0.7), this.compressor(-30, 10, 0.008, 0.08), this.gain(0.4)],
        ], [this.gain(1.1)]);
      case "drumsMetal":
        // メタルのドラム: キックの重さ（60〜80Hz）と、3〜5kHzのアタックの立ち上がりを強く出し、箱鳴りの帯域（200〜400Hz）を削って締める。
        // 原音のアタックを残しつつ、強く圧縮した音を混ぜて（パラレルコンプ）密度を上げる
        return this.parallel(input, [
          [this.filter("highpass", 35, 0, 0.7), this.filter("lowshelf", 80, 4.5), this.filter("peaking", 320, -4, 1.1), this.filter("peaking", 4200, 5, 1), this.filter("highshelf", 10000, 3), this.compressor(-18, 4, 0.012, 0.1)],
          [this.filter("highpass", 35, 0, 0.7), this.filter("peaking", 320, -3, 1.1), this.compressor(-32, 12, 0.006, 0.07), this.gain(0.45)],
        ], [this.gain(1.15)]);
      // ── 太鼓ごとの経路（2026-10-02）。調べた定石（docs/sound/guitar-bass-drums-sound-design.md）に沿って、1つずつ仕上げる ──
      case "kick": {
        // キック: 足元の不要な低音（30Hz以下）を切り、60〜80Hzで重さ、200〜400Hzのこもりを削り、3〜5kHzで「カチッ」を出す。アタック25msで3〜5dB圧縮
        const metal = this.tone !== "rock";
        return this.chain(input, [this.filter("highpass", 30, 0, 0.7), this.filter("lowshelf", 70, metal ? 4.5 : 3), this.filter("peaking", 320, metal ? -4.5 : -3.5, 1.1), this.filter("peaking", 4000, metal ? 5 : 3, 1), this.compressor(-18, 4, 0.025, 0.1), this.gain(1.1)], this.drumBus);
      }
      case "snare": {
        // スネア: 500Hz〜1kHzの箱鳴りを削り、3〜5kHzで打撃の立ち上がり、8kHz以上の持ち上げで抜けをよくする。速めのアタックでパンチを少し整える
        const metal = this.tone !== "rock";
        return this.chain(input, [this.filter("highpass", 80, 0, 0.7), this.filter("peaking", 220, 1.5, 1), this.filter("peaking", 750, metal ? -4 : -3, 1), this.filter("peaking", 4000, metal ? 4.5 : 3.5, 1), this.filter("highshelf", 9000, 2), this.compressor(-20, 3, 0.012, 0.1), this.gain(1.1)], this.drumBus);
      }
      case "hat":
        // ハイハット: 200〜300Hz以下は切り、1〜2kHzの金属的な刺さりを削り、8kHz以上で空気感。耳に痛い高域は14kHzで丸める。圧縮はしない
        return this.chain(input, [this.filter("highpass", 300, 0, 0.7), this.filter("peaking", 1500, -2.5, 1), this.filter("highshelf", 9000, 1.5), this.filter("lowpass", 14000, 0, 0.7), this.gain(0.9)], this.drumBus);
      case "cym":
        // シンバル・タム: タムは胴鳴り（350Hz）を少し削り、シンバルは低い所（250Hz以下）を切って、10kHz以上を持ち上げて広げる。圧縮はしない
        return this.chain(input, [this.filter("highpass", 60, 0, 0.7), this.filter("peaking", 350, -3, 1), this.filter("highshelf", 10000, 1.2), this.gain(1)], this.drumBus);
      // ── ジャンル別（2026-09-30 追加）。特定の機材や製品の音を写したものではなく、ジャンルの一般的な音の性格に合わせた ──
      case "jazz":
        // ジャズ: ほぼ歪ませず、低音を少し足して高音を大きく丸める（太く柔らかい、指で弾いたような音）
        return this.chain(input, tail([this.filter("highpass", 70), this.filter("lowshelf", 200, 3), this.filter("peaking", 800, -2, 0.9), this.shaper(1.3, 0.02), this.filter("highshelf", 3000, -6), this.filter("lowpass", 4500, 0, 0.7), this.gain(0.7)]));
      case "blues":
        // ブルース: 浅い歪みを上下で非対称にして（温かい倍音）、中域（900Hz）を前に出す。弾き方の強弱が残る
        return this.chain(input, tail([this.filter("highpass", 90), this.filter("peaking", 900, 4, 0.8), this.gain(2.4 * d), this.shaper(2.8 * d, 0.12), this.filter("peaking", 2200, 1, 1), this.filter("lowpass", 5200, 0, 0.8), this.gain(0.55)]));
      case "funk":
        // ファンク: 低音を削って高音を明るく、強く圧縮して粒をそろえる（歯切れのよいカッティング向き）
        return this.chain(input, tail([this.filter("highpass", 140), this.filter("lowshelf", 200, -3), this.filter("peaking", 1800, 2, 1), this.filter("highshelf", 3000, 5), this.compressor(-22, 4, 0.003, 0.1), this.gain(1.6 * d), this.shaper(1.6 * d, 0.02), this.filter("lowpass", 7500, 0, 0.8), this.gain(0.7)]));
      case "crunch":
        // クランチ: オーバードライブより少し浅い、ざらっとした歪み。和音の1音1音が聞き分けられる
        return this.chain(input, tail([this.filter("highpass", 100), this.filter("peaking", 1000, 3, 0.9), this.gain(3 * d), this.shaper(3 * d, 0.08), this.filter("peaking", 2500, 2, 1), this.filter("lowpass", 6200, 0, 0.8), this.gain(0.52)]));
      case "hardrock":
        // ハードロック: ディストーションとメタルの間。深く歪ませ、低音と高音（3kHz）を少し足す
        return this.chain(input, tail([this.filter("highpass", 110), this.filter("peaking", 900, 3, 0.9), this.gain(4 * d), this.shaper(6.5 * d, 0.05), this.filter("lowshelf", 110, 3), this.filter("peaking", 3000, 3, 1), this.filter("lowpass", 5000, 0, 0.8), this.gain(0.38)]));
      case "punk":
        // パンク: 対称に角を立てて強く歪ませ、中高域（1.5kHz）を押し出す。低音は締める（勢いで押す音）
        return this.chain(input, tail([this.filter("highpass", 150), this.filter("peaking", 1500, 4, 0.9), this.gain(4.2 * d), this.shaper(7 * d, 0), this.filter("highshelf", 3000, 3), this.filter("lowpass", 6200, 0, 0.8), this.gain(0.4)]));
      case "fuzz":
        // ファズ: 非常に深く、上下の非対称も大きく歪ませる。低音を太く、中域を少しえぐり、高音は丸める（荒々しく不穏）
        return this.chain(input, tail([this.filter("highpass", 70), this.gain(6 * d), this.shaper(14 * d, 0.2), this.filter("lowshelf", 150, 5), this.filter("peaking", 600, -3, 0.9), this.filter("lowpass", 3800, 0, 0.7), this.gain(0.24)]));
      case "shoegaze":
        // シューゲイザー: 深く歪ませたうえで高音を大きく落とし、圧縮で音の壁のように平らにする（霞んだ音）
        return this.chain(input, tail([this.filter("highpass", 90), this.gain(4.5 * d), this.shaper(8 * d, 0.15), this.filter("peaking", 1400, 1, 0.9), this.filter("highshelf", 3000, -5), this.filter("lowpass", 3600, 0, 0.7), this.compressor(-24, 3, 0.02, 0.3), this.gain(0.8)]));
      case "lofi":
        // ローファイ: 音域を狭め（120Hz〜3.2kHz）、波形を細かい階段にして粗くする（古い録音・眠たげな音）
        return this.chain(input, tail([this.filter("highpass", 120), this.filter("lowpass", 3200, 0, 0.7), this.shaper(1.5, 0), this.stepper(24), this.filter("highshelf", 3000, -8), this.gain(0.7)]));
      case "retro8bit":
        // レトロ8bit: 波形を粗い階段にする（昔のゲーム機のような、ざらついた音）。音域は広いまま
        return this.chain(input, tail([this.filter("highpass", 60), this.stepper(8), this.filter("highshelf", 3000, 2), this.filter("lowpass", 9000, 0, 0.7), this.gain(0.85)]));
      case "radio":
        // ラジオ・電話: 400Hz〜3kHzだけを通し、中域を持ち上げて軽く歪ませる（遠くの・機械ごしの音）
        return this.chain(input, tail([this.filter("highpass", 400, 0, 0.8), this.filter("lowpass", 3000, 0, 0.8), this.filter("peaking", 1500, 6, 1), this.gain(2 * d), this.shaper(3 * d, 0), this.gain(0.55)]));
      // ── ラウド系・繊細系（2026-10-02）。出口は音割れしないよう小さめ。歪みは2段で、段の間で高音を落とし、ざらつきを抑える ──
      case "loudmetal":
        // ラウドメタル: 前段で低音（130Hz未満）を削って刻みを締め、2段で強く歪ませ、後段で中域（600Hz）をえぐって低音（90Hz）と存在感（3kHz）を足す。刺さる高域（5kHz〜）は落とす
        return this.chain(input, tail([
          this.filter("highpass", 130, 0, 0.8), this.filter("peaking", 800, 4, 0.8), this.gain(4.2 * d), this.shaper(8 * d, 0.03),
          this.filter("lowpass", 5000, 0, 0.7), this.gain(1.6), this.shaper(3, 0.02),
          this.filter("peaking", 600, -4.5, 1), this.filter("peaking", 3000, 2.5, 1), this.filter("lowshelf", 90, 3.5), this.filter("lowpass", 4600, 0, 0.8), this.gain(0.3),
        ]));
      case "loudrock":
        // ラウドロック: 中域（1kHz）が厚い太い歪み。上下を少し非対称にして温かみを残し、軽く圧縮して壁のように平らにする
        return this.chain(input, tail([
          this.filter("highpass", 105, 0, 0.8), this.filter("peaking", 1000, 4, 0.8), this.gain(3.6 * d), this.shaper(6 * d, 0.1),
          this.filter("lowshelf", 120, 2.5), this.filter("peaking", 2800, 2, 1), this.filter("lowpass", 5400, 0, 0.8), this.compressor(-20, 2.5, 0.01, 0.15), this.gain(0.36),
        ]));
      case "delicate":
        // 繊細: 歪ませない。強弱をそのまま残し、低音は軽く削り、高音（4kHz〜）をやわらかく丸める。ごく弱い圧縮で小さな音の粒をそろえる
        return this.chain(input, tail([this.filter("highpass", 90, 0, 0.7), this.filter("peaking", 2200, 1, 0.9), this.filter("highshelf", 4000, -2), this.filter("lowpass", 7000, 0, 0.7), this.compressor(-30, 1.6, 0.02, 0.25), this.gain(1.0)]));
      default:
        return this.chain(input, []);
    }
  }

  private stepper(levels: number): WaveShaperNode {
    const s = this.ctx.createWaveShaper();
    s.curve = stepCurve(levels);
    return s;
  }

  /**
   * NAMのアンプ: 入力 →（モデルを読み込んだワークレット）→ 左右の位置 → 出力。モデルが準備できるまでは、そのまま通す。
   * 準備できたら、その場でつなぎ替える（曲の再生は止めない）。
   */
  private buildNam(input: AudioNode, override: ChannelAmp): AudioNode[] {
    const dry = this.gain(1);
    const hub = this.gain(1);
    input.connect(dry);
    dry.connect(this.destination);
    const nodes: AudioNode[] = [dry, hub];
    const modelJson = override.amp.model ? this.models[override.amp.model] : undefined;
    const generation = this.generation;
    if (!this.nam || !modelJson) {
      return nodes;
    }
    const done = this.nam.createAmp(this.ctx, modelJson).then((node) => {
      if (generation !== this.generation) {
        node.disconnect();
        return;
      }
      const panner = this.ctx.createStereoPanner();
      panner.pan.value = Math.max(-1, Math.min(1, override.pan));
      const out = this.gain((override.amp.level ?? 1) * Math.pow(10, 0 / 20));
      const tone = this.filter("highshelf", 3500, override.amp.tone ?? 0);
      // 入力の大きさ（歪みの深さ）と、耳に痛い高音を丸めるキャビネットのかわりのフィルター
      const pre = this.gain(override.amp.drive ?? 1);
      const cab = this.filter("lowpass", 7000, 0);
      input.connect(pre);
      pre.connect(node);
      node.connect(tone);
      tone.connect(cab);
      cab.connect(panner);
      panner.connect(out);
      out.connect(this.destination);
      // 音が出はじめたら、元の音（ドライ）を切る
      dry.disconnect();
      this.built[this.built.findIndex((list) => list.includes(dry))]?.push(node, pre, tone, cab, panner, out);
    });
    this.pending.push(done.catch((error: unknown) => console.warn("NAMのアンプを用意できませんでした:", error)));
    return nodes;
  }

  /**
   * 追加したアンプ（アンプ定義ファイル）: 用意ができるまでは元の音を通し、できたら、その場でつなぎ替える。
   * 定義が見つからない・読み込めないときは、元の音のまま。
   */
  private buildPlugin(input: AudioNode, override: ChannelAmp): AudioNode[] {
    const dry = this.gain(1);
    input.connect(dry);
    dry.connect(this.destination);
    const nodes: AudioNode[] = [dry];
    const def = override.amp.plugin ? this.plugins[override.amp.plugin] : undefined;
    if (!def) return nodes;
    const generation = this.generation;
    const done = buildAmpPlugin(this.ctx, def, { nam: this.nam }).then((chain) => {
      if (generation !== this.generation) {
        for (const n of chain) n.disconnect();
        return;
      }
      const drive = this.gain(override.amp.drive ?? 1);
      const tone = this.filter("highshelf", 3500, override.amp.tone ?? 0);
      const panner = this.ctx.createStereoPanner();
      panner.pan.value = Math.max(-1, Math.min(1, override.pan));
      const out = this.gain(override.amp.level ?? 1);
      input.connect(drive);
      drive.connect(chain[0]);
      chain[chain.length - 1].connect(tone);
      tone.connect(panner);
      panner.connect(out);
      out.connect(this.destination);
      dry.disconnect();
      this.built[this.built.findIndex((list) => list.includes(dry))]?.push(drive, ...chain, tone, panner, out);
    });
    this.pending.push(done.catch((error: unknown) => console.warn("追加したアンプを用意できませんでした:", error)));
    return nodes;
  }

  /** 入力を複数の道に分けて同時に通し、足し合わせて、あとの段（tail）を通して出口へつなぐ（分けた道・足し合わせ・あとの段のノードを全部返す）。 */
  private parallel(input: AudioNode, paths: AudioNode[][], tail: AudioNode[]): AudioNode[] {
    const sum = this.gain(1);
    const all: AudioNode[] = [sum];
    for (const path of paths) {
      let prev: AudioNode = input;
      for (const n of path) {
        prev.connect(n);
        prev = n;
        all.push(n);
      }
      prev.connect(sum);
    }
    let prev: AudioNode = sum;
    for (const n of tail) {
      prev.connect(n);
      prev = n;
      all.push(n);
    }
    prev.connect(this.destination);
    return all;
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
