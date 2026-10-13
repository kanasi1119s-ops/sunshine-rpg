// タム（ロートタム・キャノンタム・インチ違いのタム）の音を、計算で作る（録音素材は使わない＝ライセンスの心配なし）。
// 太鼓の皮（円形の膜）の振動モードを足し合わせ、打った直後に音程が少し高くなって落ちる「皮の伸び」と、スティックの当たる音（ノイズ）を加える。
//   打面の直径（インチ）が大きいほど、基本の音程が低く、響きが長い。基本周波数 f0 ≈ 1500 / インチ（Hz。胴の深さや張りで変わる目安）。
//   鍵盤の音名がそのまま太鼓の基本の高さ（音名 ↔ インチは inchToMidi / midiToInch）。
export const SR = 44100;
export const TOM_KINDS = {
  // ロートタム: 胴のない片面の太鼓。皮を回して音程を変える。ピンと張った明るい打音と、長めの伸びのある響き（打った直後に音が少し上がってから落ちる）
  roto: { program: 117, name: "Roto Tom", modes: [[1, 1, 1], [1.593, 0.28, 0.55], [2.136, 0.14, 0.4], [2.296, 0.06, 0.3]], tau0: 0.36, tauInch: 0.02, bend: 0.05, bendSec: 0.05, click: 3.2, clickHz: 5200, thud: 0.5, release: 1.0, len: 1.6 },
  // キャノンタム: 両側が開いた筒状の太鼓（コンサートタム）。胴鳴りが短く、深く「ポン」と抜ける。余韻はごく短い
  cannon: { program: 118, name: "Cannon Tom", modes: [[1, 1, 1], [1.5, 0.22, 0.45], [2.05, 0.1, 0.3]], tau0: 0.2, tauInch: 0.012, bend: 0.012, bendSec: 0.025, click: 2.6, clickHz: 3400, thud: 0.9, release: 0.3, len: 0.7 },
  // インチ違いのタム: 普通の2枚張りのタム。大きいほど低く、太く、長く響く
  inch: { program: 119, name: "Inch Tom", modes: [[1, 1, 1], [1.51, 0.38, 0.6], [2.0, 0.2, 0.45], [2.44, 0.12, 0.35], [2.9, 0.06, 0.25]], tau0: 0.2, tauInch: 0.022, bend: 0.02, bendSec: 0.035, click: 3.0, clickHz: 4200, thud: 0.7, release: 0.6, len: 1.2 },
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
  // ノイズで鳴らす共鳴（皮のふぞろいなうねり。純粋な正弦波だけだと電子音に聞こえるので、各モードに混ぜる）
  for (const [ratio, amp, dec] of k.modes) {
    const fr = f0 * ratio * (1 + 0.004 * rnd());
    const w = (2 * Math.PI * fr) / SR, r = Math.exp(-1 / (SR * tau * dec * 0.9));
    const c1 = 2 * r * Math.cos(w), c2 = -r * r;
    let y1 = 0, y2 = 0;
    for (let i = 0; i < n; i++) {
      const x = i < SR * 0.006 ? rnd() * (1 - i / (SR * 0.006)) : 0;
      const y = x * (1 - r) * 3 + c1 * y1 + c2 * y2;
      y2 = y1; y1 = y;
      out[i] += amp * 0.9 * y * 4;
    }
  }
  // 打音: スティックが皮に当たる音。高域の「カッ」（0.002秒で消える）と、中域の「コツ」（0.012秒）、皮を叩く鈍い低域。強く叩くほど明るく、大きい
  let lp1 = 0, lp2 = 0, lp3 = 0, hp = 0;
  const a1 = Math.exp((-2 * Math.PI * (k.clickHz * (0.7 + 0.6 * loud))) / SR);
  const a2 = Math.exp((-2 * Math.PI * Math.min(900, f0 * 4)) / SR);
  const a3 = Math.exp((-2 * Math.PI * 1400) / SR);
  for (let i = 0; i < n && i < SR * 0.12; i++) {
    const t = i / SR, x = rnd();
    lp1 = a1 * lp1 + (1 - a1) * x; hp = x - lp1; // 高域だけ
    lp2 = a2 * lp2 + (1 - a2) * x; // 低域だけ
    lp3 = a3 * lp3 + (1 - a3) * x; const mid = lp3 - lp2; // 中域（コツ）
    out[i] += (k.click * (0.4 + 0.6 * loud)) * hp * Math.exp(-t / 0.0022) + 1.6 * mid * (0.4 + 0.6 * loud) * Math.exp(-t / 0.012) + k.thud * 1.4 * lp2 * Math.exp(-t / 0.012);
  }
  // 強く叩いたときの、わずかな歪み（皮が叩かれて詰まる感じ）
  const drive = 1 + 1.2 * loud;
  for (let i = 0; i < n; i++) out[i] = Math.tanh(out[i] * drive) / Math.tanh(drive);
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

// ───────── バスドラムのトリガー（打撃の音だけを足す層。キックに重ねて「カチッ」と抜けさせる） ─────────
// 鍵盤の高さは音程ではなく、種類の選択: 24〜35＝punch（低い胴＋カチッ）、36〜47＝tack（高域のカチッだけ。メタルのツーバス向き）、48〜59＝knock（木と皮の「ドン」の中域）
export const TRIGGER_KINDS = { punch: [24, 35], tack: [36, 47], knock: [48, 59] };
export function synthTrigger(kind, loud) {
  const n = Math.floor(SR * (kind === "punch" ? 0.25 : kind === "knock" ? 0.12 : 0.06));
  const out = new Float32Array(n);
  let seed = 4242 + kind.length * 77 + Math.round(loud * 50);
  const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 2147483648) - 1;
  let lp = 0, lq = 0;
  const hz = kind === "tack" ? 6500 : kind === "knock" ? 2400 : 4200;
  const a = Math.exp((-2 * Math.PI * hz * (0.75 + 0.5 * loud)) / SR), b = Math.exp((-2 * Math.PI * 700) / SR);
  let ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR, x = rnd();
    lp = a * lp + (1 - a) * x; const hi = x - lp;
    lq = b * lq + (1 - b) * x;
    let v = hi * Math.exp(-t / (kind === "tack" ? 0.0018 : 0.003)) * 1.6;
    if (kind !== "tack") v += lq * 1.2 * Math.exp(-t / 0.008);
    if (kind === "punch") { const f = 48 + 90 * Math.exp(-t / 0.018); ph += (2 * Math.PI * f) / SR; v += 1.1 * Math.sin(ph) * Math.exp(-t / 0.07); }
    if (kind === "knock") { const f = 150 + 80 * Math.exp(-t / 0.01); ph += (2 * Math.PI * f) / SR; v += 0.8 * Math.sin(ph) * Math.exp(-t / 0.03); }
    out[i] = v;
  }
  let pk = 0; for (const v of out) pk = Math.max(pk, Math.abs(v));
  const g = (0.5 + 0.35 * loud) / pk, fade = Math.floor(SR * 0.01);
  for (let i = 0; i < n; i++) { out[i] *= g * (i > n - fade ? (n - i) / fade : 1); }
  return out;
}

// ───────── インパクト（映画の「ドン！」。場面の変わり目・サビ頭・ボスの登場に） ─────────
// 鍵盤＝低い胴鳴りの高さ（E1〜C4）。音程が一気に下がる低音＋割れる打音＋うなる中低域＋長い残響
export function synthImpact(midi, loud) {
  const f0 = 440 * 2 ** ((midi - 69) / 12);
  const len = 3.2, n = Math.floor(SR * len);
  const out = new Float32Array(n);
  let seed = 31337 + midi * 13 + Math.round(loud * 40);
  const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 2147483648) - 1;
  let ph = 0, ph2 = 0, l1 = 0, l2 = 0, tail = 0, tail2 = 0;
  const a1 = Math.exp((-2 * Math.PI * 5000) / SR), a2 = Math.exp((-2 * Math.PI * 300) / SR);
  for (let i = 0; i < n; i++) {
    const t = i / SR, x = rnd();
    const f = f0 * (1 + 2.2 * Math.exp(-t / 0.045));
    ph += (2 * Math.PI * f) / SR; ph2 += (2 * Math.PI * f0 * 1.5 * (1 + 0.8 * Math.exp(-t / 0.05))) / SR;
    l1 = a1 * l1 + (1 - a1) * x; const crack = x - l1;
    l2 = a2 * l2 + (1 - a2) * x;
    // 長い残響のようなうなり（暗いノイズがゆっくり消える）
    tail = 0.995 * tail + 0.005 * x; tail2 = 0.9 * tail2 + 0.1 * tail;
    out[i] = 1.3 * Math.sin(ph) * Math.exp(-t / 0.9) + 0.35 * Math.sin(ph2) * Math.exp(-t / 0.25)
      + 1.8 * crack * Math.exp(-t / 0.006) * (0.4 + 0.6 * loud) + 1.2 * l2 * Math.exp(-t / 0.05) + 14 * tail2 * Math.exp(-t / 1.0);
  }
  for (let i = 0; i < n; i++) out[i] = Math.tanh(out[i] * (1 + 1.5 * loud)) ;
  let pk = 0; for (const v of out) pk = Math.max(pk, Math.abs(v));
  const g = (0.55 + 0.4 * loud) / pk, fade = Math.floor(SR * 0.4);
  for (let i = 0; i < n; i++) out[i] *= g * (i > n - fade ? (n - i) / fade : 1);
  return out;
}
