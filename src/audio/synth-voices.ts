/**
 * 音源の追加（synth-sfx-guide.md §10 の 7・9）の、数字の部分。Web Audio に依存しない純関数で、voices.ts が使う。
 * fmBell / fmEpiano（FM の数字は §3）、drawbarOrgan（倍音 1・3・2・4・6・8 の足し算）、unisonSaw（ボイス数と spread）、
 * bitcrush（階段カーブ）、shaper（ウェーブシェーパー）。
 */

/** FM ベル：キャリア 1：モジュレーター 3.5（非整数比）。インデックスは時間とともに下げる。 */
export const FM_BELL = { ratio: 3.5, index0: 3, index1: 0, indexSec: 0.8, decaySec: 2.4 } as const;
/** FM エレピ：1：1 のキャリアとモジュレーター（短く減衰）に、14 倍の高い倍音で打鍵の「コッ」を足す。 */
export const FM_EPIANO = { ratio: 1, index0: 1.6, index1: 0.3, indexSec: 0.6, decaySec: 1.4, tineRatio: 14, tineIndex: 0.5, tineSec: 0.08 } as const;

/** ドローバー：倍音（基音に対する倍率）と、その強さ。1・3・2・4・6・8 の順に 8 を最大とする古典的な並び。 */
export const DRAWBAR: { ratio: number; level: number }[] = [
  { ratio: 1, level: 1 }, { ratio: 3, level: 0.7 }, { ratio: 2, level: 0.6 }, { ratio: 4, level: 0.45 }, { ratio: 6, level: 0.3 }, { ratio: 8, level: 0.2 },
];

/** ユニゾンソー：voices 本のデチューン（cents）。spread＝両端の幅（cents）。voices=1 は [0]。 */
export function unisonDetunes(voices: number, spread: number): number[] {
  const n = Math.max(1, Math.round(voices));
  if (n === 1) return [0];
  return Array.from({ length: n }, (_, i) => (i / (n - 1) - 0.5) * 2 * spread);
}

/** ビットクラッシュの階段カーブ（WaveShaper 用）。bits＝1〜16。 */
export function bitcrushCurve(bits: number, size = 2049): Float32Array {
  const b = Math.max(1, Math.min(16, Math.round(bits)));
  const steps = 2 ** (b - 1);
  const c = new Float32Array(size);
  for (let i = 0; i < size; i++) {
    const x = (i / (size - 1)) * 2 - 1;
    c[i] = Math.round(x * steps) / steps;
  }
  return c;
}

/** ウェーブシェーパー（tanh の丸め）。drive＝1〜20。出力は −1〜1 に収まり、drive が大きいほど角ばる。 */
export function shaperCurve(drive: number, size = 2049): Float32Array {
  const k = Math.max(1, Math.min(20, drive));
  const norm = Math.tanh(k);
  const c = new Float32Array(size);
  for (let i = 0; i < size; i++) {
    const x = (i / (size - 1)) * 2 - 1;
    c[i] = Math.tanh(k * x) / norm;
  }
  return c;
}
