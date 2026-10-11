/**
 * スマホのスピーカー向けの確認（docs/sound/game-music-guide.md §10 の提案8）。
 * 書き出したWAVについて、次を数値で見る（実機の聞き比べの手間を減らす）:
 *  ① 800Hz 以上だけの大きさ（全体との差）… 小さいと、スマホの小さなスピーカーでは音がやせる／聞こえにくい
 *  ② ベースの倍音（250〜1000Hz）の量 … ベース（40〜150Hz）に対して少なすぎると、スマホでは低音の音程が消える
 *  ③ モノラルにたたんだときの損失 … 逆相の成分が多いと、全体と旋律（500〜4000Hz）が痩せる
 * 数字は目安で、耳の確認の代わりではない。しきい値は PHONE_LIMITS。
 */
export const PHONE_LIMITS = {
  /** 800Hz以上の大きさが全体より何dB下まで許すか。 */
  highShareMinDb: -13,
  /** 250〜1000Hz が 40〜150Hz より何dB下まで許すか。 */
  bassHarmonicsMinDb: -16,
  /** モノラルにたたんだときの全体の損失（dB）の上限。 */
  monoLossMaxDb: 3,
  /** モノラルにたたんだときの旋律の帯域（500〜4000Hz）の損失（dB）の上限。 */
  monoMelodyLossMaxDb: 2.5,
};

interface Biquad { b0: number; b1: number; b2: number; a1: number; a2: number }

function biquad(type: "lp" | "hp", f: number, fs: number, q = Math.SQRT1_2): Biquad {
  const w = (2 * Math.PI * Math.min(f, fs * 0.45)) / fs;
  const cos = Math.cos(w), alpha = Math.sin(w) / (2 * q);
  const a0 = 1 + alpha;
  const b = type === "lp" ? [(1 - cos) / 2, 1 - cos, (1 - cos) / 2] : [(1 + cos) / 2, -(1 + cos), (1 + cos) / 2];
  return { b0: b[0] / a0, b1: b[1] / a0, b2: b[2] / a0, a1: (-2 * cos) / a0, a2: (1 - alpha) / a0 };
}

function run(x: Float32Array | number[], c: Biquad): Float32Array {
  const y = new Float32Array(x.length);
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
  for (let i = 0; i < x.length; i++) {
    const v = c.b0 * x[i] + c.b1 * x1 + c.b2 * x2 - c.a1 * y1 - c.a2 * y2;
    y[i] = v; x2 = x1; x1 = x[i]; y2 = y1; y1 = v;
  }
  return y;
}

/** 帯域 [lo, hi]（Hz。0 や Infinity で片側なし）を、2段（約24dB/oct）で通す。 */
export function bandPass(x: Float32Array | number[], lo: number, hi: number, fs: number): Float32Array {
  let y: Float32Array = x instanceof Float32Array ? x : Float32Array.from(x);
  if (lo > 0) for (let i = 0; i < 2; i++) y = run(y, biquad("hp", lo, fs));
  if (hi < fs * 0.45) for (let i = 0; i < 2; i++) y = run(y, biquad("lp", hi, fs));
  return y;
}

const power = (x: Float32Array): number => {
  let s = 0;
  for (let i = 0; i < x.length; i++) s += x[i] * x[i];
  return x.length ? s / x.length : 0;
};
const db = (p: number): number => (p > 1e-20 ? 10 * Math.log10(p) : -200);

export interface PhoneReport {
  fullDb: number;
  /** 800Hz以上の大きさ（全体との差。0に近いほど高域が多い）。 */
  highShareDb: number;
  /** 250〜1000Hz − 40〜150Hz（dB）。ベースの倍音が残っているか。 */
  bassHarmonicsDb: number;
  /** モノラルにたたんだときの全体の損失（dB。0＝損失なし）。 */
  monoLossDb: number;
  /** 旋律の帯域（500〜4000Hz）の損失（dB）。 */
  monoMelodyLossDb: number;
  warnings: string[];
}

/** 2ch（またはモノ）の波形を測る。 */
export function phoneCheck(channels: Float32Array[], sampleRate: number): PhoneReport {
  const L = channels[0], R = channels[1] ?? channels[0];
  const stereoPower = (a: Float32Array, b: Float32Array): number => (power(a) + power(b)) / 2;
  const full = stereoPower(L, R);
  const hiP = stereoPower(bandPass(L, 800, Infinity, sampleRate), bandPass(R, 800, Infinity, sampleRate));
  const bassP = stereoPower(bandPass(L, 40, 150, sampleRate), bandPass(R, 40, 150, sampleRate));
  const harmP = stereoPower(bandPass(L, 250, 1000, sampleRate), bandPass(R, 250, 1000, sampleRate));
  const mono = new Float32Array(L.length);
  for (let i = 0; i < L.length; i++) mono[i] = (L[i] + (R[i] ?? 0)) / 2;
  const monoLoss = Math.min(60, Math.max(0, db(full) - db(power(mono))));
  const melStereo = stereoPower(bandPass(L, 500, 4000, sampleRate), bandPass(R, 500, 4000, sampleRate));
  const melMono = power(bandPass(mono, 500, 4000, sampleRate));
  const melLoss = Math.min(60, Math.max(0, db(melStereo) - db(melMono)));
  const rep: PhoneReport = {
    fullDb: round(db(full)), highShareDb: round(db(hiP) - db(full)), bassHarmonicsDb: round(bassP > 1e-12 ? db(harmP) - db(bassP) : 0),
    monoLossDb: round(monoLoss), monoMelodyLossDb: round(melLoss), warnings: [],
  };
  const lim = PHONE_LIMITS;
  if (full < 1e-10) { rep.warnings.push("ほぼ無音です。測れません"); return rep; }
  if (rep.highShareDb < lim.highShareMinDb) rep.warnings.push(`800Hz 以上の大きさが全体より ${-rep.highShareDb}dB 小さいです（目安 ${lim.highShareMinDb}dB まで）。スマホのスピーカーでは低音が出ないので、音がやせて聞こえにくくなります。旋律・和音の楽器の高域（bright を上げる）や、ベースの倍音（アンプの歪みを少し足す）を見直してください`);
  if (bassP > 1e-12 && rep.bassHarmonicsDb < lim.bassHarmonicsMinDb) rep.warnings.push(`ベースの倍音（250〜1000Hz）がベース本体（40〜150Hz）より ${-rep.bassHarmonicsDb}dB 小さいです（目安 ${lim.bassHarmonicsMinDb}dB まで）。スマホでは低音の音程が消えます。ベースに軽い歪み（アンプ overdrive など）か、1オクターブ上の重ねを足してください`);
  if (rep.monoLossDb > lim.monoLossMaxDb) rep.warnings.push(`モノラルにたたむと全体が ${rep.monoLossDb}dB 小さくなります（目安 ${lim.monoLossMaxDb}dB まで）。左右が逆相気味の成分（chorus・ダブル・広い残響・widen の強すぎ）があります`);
  if (rep.monoMelodyLossDb > lim.monoMelodyLossMaxDb) rep.warnings.push(`モノラルにたたむと旋律の帯域（500〜4000Hz）が ${rep.monoMelodyLossDb}dB 小さくなります（目安 ${lim.monoMelodyLossMaxDb}dB まで）。旋律のパートは pan を 0 に、chorus を外してください`);
  return rep;
}

const round = (x: number): number => Math.round(x * 10) / 10;

/** 16bit PCM のWAV（ステレオ／モノ）を読む。 */
export function readWavPcm16(bytes: Uint8Array): { channels: Float32Array[]; sampleRate: number } {
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  if (String.fromCharCode(...bytes.slice(0, 4)) !== "RIFF") throw new Error("WAVではありません");
  let pos = 12, fmt: { ch: number; rate: number; bits: number } | null = null;
  while (pos + 8 <= bytes.length) {
    const id = String.fromCharCode(...bytes.slice(pos, pos + 4));
    const size = dv.getUint32(pos + 4, true);
    if (id === "fmt ") fmt = { ch: dv.getUint16(pos + 10, true), rate: dv.getUint32(pos + 12, true), bits: dv.getUint16(pos + 22, true) };
    else if (id === "data") {
      if (!fmt) throw new Error("fmt チャンクがありません");
      if (fmt.bits !== 16) throw new Error(`16bit のWAVだけ読めます（${fmt.bits}bit）`);
      const frames = Math.floor(Math.min(size, bytes.length - pos - 8) / (2 * fmt.ch));
      const channels = Array.from({ length: fmt.ch }, () => new Float32Array(frames));
      for (let i = 0; i < frames; i++) for (let c = 0; c < fmt.ch; c++) channels[c][i] = dv.getInt16(pos + 8 + (i * fmt.ch + c) * 2, true) / 32768;
      return { channels, sampleRate: fmt.rate };
    }
    pos += 8 + size + (size % 2);
  }
  throw new Error("data チャンクがありません");
}

export function formatPhoneReport(r: PhoneReport, name = ""): string {
  const ok = (v: boolean): string => (v ? "○" : "要確認");
  const lim = PHONE_LIMITS;
  return [
    `■ スマホ確認${name ? `: ${name}` : ""}`,
    `  ${ok(r.highShareDb >= lim.highShareMinDb)}  800Hz以上の大きさ: 全体より ${r.highShareDb}dB（目安 ${lim.highShareMinDb}dB 以上）`,
    `  ${ok(r.bassHarmonicsDb >= lim.bassHarmonicsMinDb)}  ベースの倍音: 本体より ${r.bassHarmonicsDb}dB（目安 ${lim.bassHarmonicsMinDb}dB 以上）`,
    `  ${ok(r.monoLossDb <= lim.monoLossMaxDb)}  モノ化の損失（全体）: ${r.monoLossDb}dB（目安 ${lim.monoLossMaxDb}dB 以下）`,
    `  ${ok(r.monoMelodyLossDb <= lim.monoMelodyLossMaxDb)}  モノ化の損失（旋律の帯域）: ${r.monoMelodyLossDb}dB（目安 ${lim.monoMelodyLossMaxDb}dB 以下）`,
    ...r.warnings.map((w) => `  注意: ${w}`),
  ].join("\n");
}
