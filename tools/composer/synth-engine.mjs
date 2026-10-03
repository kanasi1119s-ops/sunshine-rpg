// 作曲ソフト専用のシンセサイザー（計算で音を作る）。render-node.mjs が使う。
// 音源（サウンドフォント）の電子的な音色の代わりに、音の立ち上がり・明るさの変化・揺れを細かく作る。外部のソフトや素材は使わない。
//
// 音の作り（減算方式）: 発振器（のこぎり波・矩形波・正弦波。PolyBLEP で折り返しノイズを抑える）を、少しずつずらして重ね（ユニゾン）、
//   フィルター（2極の状態変数フィルター）で明るさを削り、エンベロープ（ADSR）で音量と明るさを時間で動かし、LFO でビブラートをかける。
// エレクトリックピアノは FM 方式（2つの正弦波。強く弾くほど倍音が増えて明るく、時間とともに丸くなる）。
const SR = 44100;
const TAU = Math.PI * 2;

/** 曲調・パートごとの音色。 */
export const PRESETS = {
  // 主旋律のリード: のこぎり2本（±7セント）＋1オクターブ下の矩形。弾いた直後は明るく、だんだん丸く。音と音のあいだはなめらかにつなぐ
  lead: {
    osc: [{ wave: "saw", detune: -7, gain: 0.5 }, { wave: "saw", detune: 7, gain: 0.5 }, { wave: "square", detune: 0, octave: -1, gain: 0.25 }],
    unison: 1, spread: 0.25,
    amp: { a: 0.006, d: 0.25, s: 0.8, r: 0.18 },
    filter: { cutoff: 1800, res: 0.25, env: 2.2, keytrack: 0.5, vel: 1.0 },
    fenv: { a: 0.004, d: 0.35, s: 0.3, r: 0.25 },
    vibrato: { rate: 5.4, depth: 14, delay: 0.28 },
    glide: 0.045, mono: true, gain: 0.55,
  },
  // 背景のパッド: のこぎり7本を広く（±18セント）ずらし、左右に広げる。ゆっくり立ち上がり、明るさがゆっくり揺れる
  pad: {
    osc: [{ wave: "saw", detune: 0, gain: 1 }],
    unison: 7, unisonCents: 18, spread: 0.9,
    amp: { a: 0.6, d: 0.8, s: 0.85, r: 1.4 },
    filter: { cutoff: 1500, res: 0.15, env: 0.8, keytrack: 0.3, vel: 0.4, lfoRate: 0.17, lfoOct: 0.35 },
    fenv: { a: 0.9, d: 1.5, s: 0.6, r: 1.5 },
    gain: 0.32,
  },
  // シンセベース: のこぎり＋1オクターブ下の正弦（重さ）。弾いた瞬間だけ明るい（短いフィルターのエンベロープ）
  synthBass: {
    osc: [{ wave: "saw", detune: 0, gain: 0.6 }, { wave: "sine", detune: 0, octave: -1, gain: 0.7 }],
    unison: 1, spread: 0,
    amp: { a: 0.003, d: 0.2, s: 0.85, r: 0.08 },
    filter: { cutoff: 260, res: 0.3, env: 2.6, keytrack: 0.3, vel: 1.2 },
    fenv: { a: 0.002, d: 0.18, s: 0.15, r: 0.1 },
    gain: 0.7, mono: true, glide: 0.0,
  },
  // 808: 正弦波の音程を、叩いた直後に下げる（ドンという当たり）。軽く歪ませて小さなスピーカーでも聞こえるように
  bass808: {
    osc: [{ wave: "sine", detune: 0, gain: 1 }],
    unison: 1, spread: 0,
    amp: { a: 0.002, d: 1.2, s: 0.55, r: 0.25 },
    pitchDrop: { semis: 12, time: 0.06 },
    drive: 2.2, gain: 0.8, mono: true, glide: 0.09,
  },
  // エレクトリックピアノ（FM）: 弾いた瞬間の金属的な響き（14倍の倍音）と、強さで明るさが変わる胴の音（1倍）。左右にゆっくり揺れる
  epiano: { fm: true, amp: { a: 0.002, d: 2.6, s: 0.0, r: 0.35 }, gain: 0.55, tremolo: { rate: 4.2, depth: 0.25 } },
};

/** PolyBLEP（のこぎり波・矩形波の角をなめらかにして、高い音のざらつきを減らす）。 */
function polyblep(t, dt) {
  if (t < dt) {
    const x = t / dt;
    return x + x - x * x - 1;
  }
  if (t > 1 - dt) {
    const x = (t - 1) / dt;
    return x * x + x + x + 1;
  }
  return 0;
}

function env(adsr, t, relAt) {
  const { a, d, s, r } = adsr;
  let v;
  if (t < a) v = t / Math.max(1e-4, a);
  else v = s + (1 - s) * Math.exp(-((t - a) / Math.max(1e-4, d)) * 3);
  if (relAt !== null && t > relAt) {
    const atRel = relAt < a ? relAt / Math.max(1e-4, a) : s + (1 - s) * Math.exp(-((relAt - a) / Math.max(1e-4, d)) * 3);
    v = atRel * Math.exp(-((t - relAt) / Math.max(1e-4, r)) * 4.6);
  }
  return v;
}

const midiHz = (k) => 440 * Math.pow(2, (k - 69) / 12);

/**
 * 音符の並びを音にする。notes: [{ start, end, key, vel }]（秒）。戻り値: { L, R }。
 * mono の音色は、重なった音をつなぎ（後の音が前の音を引きつぐ）、glide の時間で音程をなめらかに移す。
 */
export function renderSynth(presetName, notes, total, { seed = 1 } = {}) {
  const P = PRESETS[presetName];
  const L = new Float32Array(total), R = new Float32Array(total);
  if (!P) return { L, R };
  const sorted = [...notes].sort((a, b) => a.start - b.start);
  if (P.fm) return renderFm(P, sorted, total, L, R);
  let rnd = seed >>> 0;
  const rand = () => ((rnd = (Math.imul(rnd ^ (rnd >>> 15), 2246822507) + 0x9e3779b9) >>> 0) / 4294967296);
  let prevKey = null;
  for (let ni = 0; ni < sorted.length; ni++) {
    const n = sorted[ni];
    const next = sorted[ni + 1];
    // mono: 次の音が来たら、この音はそこで終わる（なめらかにつなぐ）
    const endT = P.mono && next && next.start < n.end ? next.start : n.end;
    const relAt = endT - n.start;
    const len = Math.min(total - Math.round(n.start * SR), Math.round((relAt + P.amp.r * 1.6) * SR));
    if (len <= 0) continue;
    const s0 = Math.round(n.start * SR);
    const vel = n.vel / 127;
    const fromKey = P.mono && P.glide && prevKey !== null && sorted[ni - 1] && sorted[ni - 1].end >= n.start - 0.02 ? prevKey : n.key;
    prevKey = n.key;
    // 発振器の一覧（ユニゾンで増やす）
    const voices = [];
    for (const o of P.osc ?? []) {
      const u = P.unison ?? 1;
      for (let i = 0; i < u; i++) {
        const spreadPos = u > 1 ? (i / (u - 1)) * 2 - 1 : 0;
        const cents = (o.detune ?? 0) + spreadPos * (P.unisonCents ?? 0);
        const pan = spreadPos * (P.spread ?? 0) + (u === 1 && P.osc.length > 1 ? Math.sign(o.detune ?? 0) * (P.spread ?? 0) : 0);
        voices.push({ o, cents, phase: rand(), gl: Math.cos(((pan + 1) / 2) * (Math.PI / 2)), gr: Math.sin(((pan + 1) / 2) * (Math.PI / 2)), g: (o.gain ?? 1) / Math.sqrt(u) });
      }
    }
    // フィルターの状態（左右）
    let lowL = 0, bandL = 0, lowR = 0, bandR = 0;
    const F = P.filter;
    for (let t = 0; t < len; t++) {
      const sec = t / SR;
      const aenv = env(P.amp, sec, relAt);
      if (aenv < 1e-5 && sec > relAt) break;
      // 音程: グライド・ピッチの落下（808）・ビブラート
      let key = n.key;
      if (fromKey !== n.key && P.glide) key = fromKey + (n.key - fromKey) * Math.min(1, sec / P.glide);
      if (P.pitchDrop) key += P.pitchDrop.semis * Math.exp(-sec / P.pitchDrop.time);
      if (P.vibrato && sec > P.vibrato.delay) key += (P.vibrato.depth / 100) * Math.min(1, (sec - P.vibrato.delay) / 0.4) * Math.sin(TAU * P.vibrato.rate * sec);
      let sl = 0, sr = 0;
      for (const v of voices) {
        const hz = midiHz(key + (v.o.octave ?? 0) * 12) * Math.pow(2, v.cents / 1200);
        const dt = hz / SR;
        v.phase += dt;
        if (v.phase >= 1) v.phase -= 1;
        let x;
        if (v.o.wave === "saw") x = 2 * v.phase - 1 - polyblep(v.phase, dt);
        else if (v.o.wave === "square") x = (v.phase < 0.5 ? 1 : -1) + polyblep(v.phase, dt) - polyblep((v.phase + 0.5) % 1, dt);
        else x = Math.sin(TAU * v.phase);
        sl += x * v.g * v.gl;
        sr += x * v.g * v.gr;
      }
      if (F) {
        // 明るさ: 基準 × 鍵盤の高さ × 強さ × フィルターのエンベロープ × ゆっくりした揺れ
        const fe = env(P.fenv, sec, relAt);
        const oct = F.env * fe * (0.5 + 0.5 * vel * F.vel) + (F.lfoRate ? F.lfoOct * Math.sin(TAU * F.lfoRate * (n.start + sec)) : 0);
        const fc = Math.min(SR * 0.42, F.cutoff * Math.pow(2, oct + (F.keytrack * (n.key - 60)) / 12));
        const f = 2 * Math.sin((Math.PI * fc) / SR);
        const q = 1 - Math.min(0.95, F.res);
        // 状態変数フィルター（ローパス）を左右に
        lowL += f * bandL;
        const highL = sl - lowL - q * bandL;
        bandL += f * highL;
        lowR += f * bandR;
        const highR = sr - lowR - q * bandR;
        bandR += f * highR;
        sl = lowL;
        sr = lowR;
      }
      if (P.drive) {
        sl = Math.tanh(sl * P.drive) / Math.tanh(P.drive);
        sr = Math.tanh(sr * P.drive) / Math.tanh(P.drive);
      }
      const g = aenv * P.gain * (0.55 + 0.45 * vel);
      L[s0 + t] += sl * g;
      R[s0 + t] += sr * g;
    }
  }
  return { L, R };
}

/** エレクトリックピアノ（2つの演算子の FM ＋ 弾いた瞬間の金属的な響き）。 */
function renderFm(P, notes, total, L, R) {
  for (const n of notes) {
    const s0 = Math.round(n.start * SR);
    const relAt = n.end - n.start;
    const len = Math.min(total - s0, Math.round((Math.min(relAt, 6) + P.amp.r * 2) * SR));
    if (len <= 0) continue;
    const vel = n.vel / 127;
    const hz = midiHz(n.key);
    // 高い音ほど、倍音（変調の深さ）を控えめに（高音がきつくならないように）
    const keyScale = Math.pow(2, -(n.key - 60) / 36);
    let pc = 0, pm = 0, pt = 0;
    for (let t = 0; t < len; t++) {
      const sec = t / SR;
      const a = env(P.amp, sec, relAt);
      if (a < 1e-5 && sec > relAt) break;
      // 胴の音: 変調の深さは、強さとともに増え、時間とともに減る（弾いた直後は明るく、だんだん丸く）
      const index = (0.6 + 2.4 * vel * vel) * keyScale * Math.exp(-sec / 0.9) + 0.25;
      pm += (hz * 1) / SR;
      pc += hz / SR;
      const body = Math.sin(TAU * pc + index * Math.sin(TAU * pm));
      // 弾いた瞬間の金属的な響き（14倍）
      pt += (hz * 14) / SR;
      const tine = Math.sin(TAU * pt) * 0.18 * vel * Math.exp(-sec / 0.05);
      const x = (body + tine) * a * P.gain * (0.45 + 0.55 * vel);
      // 左右にゆっくり揺れる（トレモロ）
      const tr = P.tremolo ? P.tremolo.depth * Math.sin(TAU * P.tremolo.rate * (n.start + sec)) : 0;
      L[s0 + t] += x * (1 - tr) * 0.9;
      R[s0 + t] += x * (1 + tr) * 0.9;
    }
  }
  return { L, R };
}
