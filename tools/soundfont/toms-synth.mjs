// タム（ロートタム・キャノンタム・インチ違いのタム）の音を、計算で作る（録音素材は使わない＝ライセンスの心配なし）。
// 太鼓の皮（円形の膜）の振動モードを足し合わせ、打った直後に音程が少し高くなって落ちる「皮の伸び」と、スティックの当たる音（ノイズ）を加える。
//   打面の直径（インチ）が大きいほど、基本の音程が低く、響きが長い。基本周波数 f0 ≈ 1500 / インチ（Hz。胴の深さや張りで変わる目安）。
//   鍵盤の音名がそのまま太鼓の基本の高さ（音名 ↔ インチは inchToMidi / midiToInch）。
export const SR = 44100;
export const TOM_KINDS = {
  // ロートタム: 胴のない片面の太鼓。皮を回して音程を変える。ピンと張った明るい打音と、長めの伸びのある響き（打った直後に音が少し上がってから落ちる）
  roto: { program: 117, name: "Roto Tom", modes: [[1, 1, 1], [1.593, 0.28, 0.55], [2.136, 0.14, 0.4], [2.296, 0.06, 0.3]], tau0: 0.55, tauInch: 0.025, bend: 0.07, bendSec: 0.05, click: 0.9, clickHz: 5200, thud: 0.25, release: 1.0, len: 1.6 },
  // キャノンタム: 両側が開いた筒状の太鼓（コンサートタム）。胴鳴りが短く、深く「ポン」と抜ける。余韻はごく短い
  cannon: { program: 118, name: "Cannon Tom", modes: [[1, 1, 1], [1.5, 0.22, 0.45], [2.05, 0.1, 0.3]], tau0: 0.2, tauInch: 0.012, bend: 0.025, bendSec: 0.025, click: 0.55, clickHz: 3400, thud: 0.6, release: 0.3, len: 0.7 },
  // インチ違いのタム: 普通の2枚張りのタム。大きいほど低く、太く、長く響く
  inch: { program: 119, name: "Inch Tom", modes: [[1, 1, 1], [1.51, 0.38, 0.6], [2.0, 0.2, 0.45], [2.44, 0.12, 0.35], [2.9, 0.06, 0.25]], tau0: 0.28, tauInch: 0.03, bend: 0.045, bendSec: 0.035, click: 0.7, clickHz: 4200, thud: 0.4, release: 0.6, len: 1.2 },
};
export const inchToMidi = (inch) => Math.round(69 + 12 * Math.log2(1500 / inch / 440));
export const midiToInch = (midi) => 1500 / (440 * 2 ** ((midi - 69) / 12));

/** 1つの音（鍵盤 midi、強さ loud=0〜1）を作る。 */
export function synthTom(kind, midi, loud) {
  const k = TOM_KINDS[kind];
  const f0 = 440 * 2 ** ((midi - 69) / 12);
  const inch = midiToInch(midi);
  const n = Math.floor(SR * k.len);
  const out = new Float32Array(n);
  let seed = 9001 + midi * 17 + Math.round(loud * 100) + kind.length * 1000;
  const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 2147483648) - 1;
  const tau = Math.max(0.05, k.tau0 + (inch - 12) * k.tauInch);
  const bend = k.bend * (0.6 + 0.8 * loud);
  for (const [ratio, amp, dec] of k.modes) {
    let ph = 0;
    for (let i = 0; i < n; i++) {
      const t = i / SR;
      const f = f0 * ratio * (1 + bend * Math.exp(-t / k.bendSec));
      ph += (2 * Math.PI * f) / SR;
      if (f > SR / 2.2) break;
      out[i] += amp * Math.exp(-t / (tau * dec)) * Math.sin(ph);
    }
  }
  // 打音: スティックの当たる音（高域のノイズ）と、皮を叩く鈍い音（低域のノイズ）。強く叩くほど明るい
  let lp1 = 0, lp2 = 0, hp = 0;
  const a1 = Math.exp((-2 * Math.PI * (k.clickHz * (0.7 + 0.6 * loud))) / SR);
  const a2 = Math.exp((-2 * Math.PI * Math.min(900, f0 * 4)) / SR);
  for (let i = 0; i < n && i < SR * 0.12; i++) {
    const t = i / SR, x = rnd();
    lp1 = a1 * lp1 + (1 - a1) * x; hp = x - lp1; // 高域だけ
    lp2 = a2 * lp2 + (1 - a2) * x; // 低域だけ
    out[i] += (k.click * (0.35 + 0.65 * loud) * 0.5) * hp * Math.exp(-t / 0.004) + k.thud * 0.9 * lp2 * Math.exp(-t / 0.012);
  }
  // 大きさをそろえる（頭から0.25秒の rms を一定に。弱い音は少し小さく）
  let s = 0; const m = Math.min(n, Math.floor(SR * 0.25));
  for (let i = 0; i < m; i++) s += out[i] * out[i];
  let g = (0.07 + 0.05 * loud) / Math.sqrt(s / m);
  let pk = 0; for (let i = 0; i < n; i++) pk = Math.max(pk, Math.abs(out[i] * g));
  if (pk > 0.95) g *= 0.95 / pk;
  const fade = Math.floor(SR * 0.06);
  for (let i = 0; i < n; i++) out[i] *= g * (i > n - fade ? (n - i) / fade : 1);
  return out;
}
