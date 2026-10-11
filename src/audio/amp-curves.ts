/**
 * 歪みの波形曲線（ウェーブシェイパーの表）。どれも、小さい音の増幅は同じ（原点の傾き1）、0を入れたら0を返す（DCずれなし）。
 * - tanh: これまでの標準（なめらかに潰れる。`amp-rack.ts` の curve() と同じ式）
 * - softsqrt: x/√(1+x²)。tanh よりゆっくり丸まる（倍音が少し穏やか・軽い）
 * - diode: 上下で潰れ方を変える（上は深く、下は浅く。偶数倍音で温かい）
 * - deadzone: 0の付近に不感帯（クロスオーバー）。ラジオやローファイの味付け
 */
export type CurveKind = "tanh" | "softsqrt" | "diode" | "deadzone";
export const CURVE_KINDS: CurveKind[] = ["tanh", "softsqrt", "diode", "deadzone"];

function shape(kind: CurveKind, g: number): number {
  switch (kind) {
    case "softsqrt":
      return g / Math.sqrt(1 + g * g);
    case "diode":
      return g >= 0 ? Math.tanh(g) : 0.7 * Math.tanh(g / 0.7);
    case "deadzone": {
      const dz = 0.15;
      const a = Math.max(0, Math.abs(g) - dz);
      return Math.sign(g) * Math.tanh(a);
    }
    default:
      return Math.tanh(g);
  }
}

const CACHE = new Map<string, Float32Array<ArrayBuffer>>();
/** drive: 歪みの深さ。bias: 上下のずれ（非対称）。size: 表の点の数（drive が 8 以上のときは細かく）。 */
export function shapeCurve(kind: CurveKind, drive: number, bias: number, size = 4096): Float32Array<ArrayBuffer> {
  const key = `${kind}|${drive}|${bias}|${size}`;
  let c = CACHE.get(key);
  if (!c) {
    c = new Float32Array(size);
    const offset = shape(kind, drive * bias);
    // deadzone は、入力の端 (x=1) で tanh と同じ高さになるようにそろえる（音量が急に下がらないように）
    const norm = kind === "deadzone" ? shape("tanh", drive) / Math.max(1e-6, shape(kind, drive)) : 1;
    for (let i = 0; i < size; i++) {
      const x = (i / (size - 1)) * 2 - 1;
      c[i] = (shape(kind, drive * (x + bias)) - offset) * norm;
    }
    CACHE.set(key, c);
  }
  return c;
}
