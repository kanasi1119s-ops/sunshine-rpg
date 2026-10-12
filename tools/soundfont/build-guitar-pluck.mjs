// 使い方: node --experimental-strip-types tools/soundfont/build-guitar-pluck.mjs
// 弦モデル（Karplus-Strong 系）のクリーンギターの SoundFont を作る（assets-src/soundfont/extra/guitar-pluck.sf3）。
// 録音ではなく数式で合成するので、音の大きさ・立ち上がり・減り方が音ごとにそろい、「粒」が均一になる。
// 作曲ソフトでは `--guitar pluck`（warm）・`pluck-soft`・`pluck-clear` で、GMのジャズギター(26)とクリーンギター(27)を入れかえる。外部の素材は使わない（CLAUDE.md 1-1）。
//
// 音のつくり（docs/sound/guitar-solo-guide.md §6）:
//  1. 弦: 遅延線（長さ SR/f0、小数部は全域通過フィルターで合わせる）＋ループのローパス（1ゼロ）＋減衰（T60 を音域で変える）
//  2. はじく位置: 励起のノイズに「くし形」（弦長の β の位置）をかける。βが小さいほど明るい
//  3. 強さ（p/mf/f）: 励起のローパスの開き方を変える（強いほど明るい）。音の大きさは SoundFont の強さ曲線に任せ、各サンプルのピークはそろえる
//  4. ピックアップ: 拾う位置のくし形＋2kHz付近までなだらかな山、6kHz以上をなだらかに落とす（刺さりを出さない）
import fs from "fs";
import path from "path";
import { SR, loadBank, monoSample, timecents, compressBank, BasicSoundBank, GeneratorTypes, emptyPresetFrom } from "./lib.mjs";

const OUT = path.resolve("assets-src/soundfont/extra");
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
const SECONDS = 6;
/** 音色の版。clear＝空気感が強い（9.5kHz）、soft＝少しやわらかい（7.2kHz。人間が「保存」と言った版）、warm＝softと最初の暗めの版の中間。 */
const VARIANTS = {
  clear: { label: "弦モデル（クリア。空気感が強い）", lp1: 9500, lp2: 12000, comb: 0.6 },
  soft: { label: "弦モデル（少しやわらかい。保存版）", lp1: 7200, lp2: 9500, comb: 0.72 },
  warm: { label: "弦モデル（やわらかく温かい。soft と暗めの中間。人間が「保存」と言った版）", lp1: 6100, lp2: 8650, comb: 0.78 },
  deep: { label: "弦モデル（重く低音寄り。mellow に低域の厚みを足す）", lp1: 5550, lp2: 8225, comb: 0.815, body: true },
  deepair: { label: "弦モデル（deep＋弾き始めの高域の抜け。人間が「保存」と言った版）", lp1: 5550, lp2: 8225, comb: 0.815, body: true, air: 0.3, release26: 3 },
  mellow: { label: "弦モデル（さらにまろやか。warm と暗めの中間）", lp1: 5550, lp2: 8225, comb: 0.815 },
};
const LAYERS = { p: { vel: [1, 45], bright: 0.35 }, mf: { vel: [46, 95], bright: 0.6 }, f: { vel: [96, 127], bright: 0.85 } };

/** 乱数（固定の種。毎回同じ音になる）。 */
function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0) / 4294967296) * 2 - 1;
}

/** 1音を合成する。midi＝音の高さ、bright＝0〜1（強いほど明るい）。 */
export function pluck(midi, bright, seconds = SECONDS, v = VARIANTS.warm) {
  const f0 = 440 * 2 ** ((midi - 69) / 12);
  const total = Math.floor(seconds * SR);
  const L = SR / f0;
  const N = Math.floor(L - 0.5); // 整数部（ループのローパスが 0.5 サンプル遅らせる）
  const frac = L - 0.5 - N;
  const ap = (1 - frac) / (1 + frac); // 全域通過の係数（小数遅延）
  const r = rng(1000 + midi);
  // 励起: ノイズ → はじく位置のくし形 → 強さに応じたローパス
  const beta = 0.14 + 0.04 * (1 - bright);
  const lag = Math.max(1, Math.round(beta * N));
  const w = new Float32Array(N + lag);
  for (let i = 0; i < w.length; i++) w[i] = r();
  const exc = new Float32Array(N);
  for (let i = 0; i < N; i++) exc[i] = w[i + lag] - w[i];
  const cut = 0.1 + 0.55 * bright; // 1極ローパスの係数（大きいほど明るい）
  let y1 = 0;
  for (let i = 0; i < N; i++) { y1 += cut * (exc[i] - y1); exc[i] = y1; }
  // 弦のループ
  const t60 = Math.min(14, Math.max(5, 14 - (midi - 40) * 0.12)); // 2026-10-12: 「音が伸びない」ので長くした（A4 で約 10 秒。以前は約 3 秒）
  const rho = 10 ** (-3 / (t60 * f0));
  const b = 0.26 - 0.08 * bright; // ループのローパス。小さいほど高い倍音が長く残る // ループのローパス（小さいほど明るい＝減衰が遅い）
  const buf = new Float32Array(N);
  buf.set(exc);
  const str = new Float32Array(total);
  let idx = 0, prev = 0, apx = 0, apy = 0;
  for (let n = 0; n < total; n++) {
    const cur = buf[idx];
    str[n] = cur;
    // ローパス（1ゼロ）＋減衰
    const lp = rho * ((1 - b) * cur + b * prev);
    prev = cur;
    // 小数遅延（全域通過）
    const o = ap * (lp - apy) + apx;
    apx = lp; apy = o;
    buf[idx] = o;
    idx = (idx + 1) % N;
  }
  // ピックアップ: 拾う位置のくし形
  const pu = Math.max(1, Math.round(0.17 * L));
  const pick = new Float32Array(total);
  for (let n = 0; n < total; n++) pick[n] = str[n] - (n >= pu ? str[n - pu] * v.comb : 0);
  // 音色: 90Hz未満を切る → 3.2kHz付近をなだらかに −3dB（刺さりの帯域）→ 7.2kHz以上をなだらかに落とす（空気感を少し残す）
  let pre = pick;
  if (v.body) pre = biquad(biquad(pick, "ls", 250, 0.7, 3), "peak", 400, 1.0, 2);
  const out = biquad(biquad(biquad(biquad(pre, "hp", v.body ? 65 : 90, 0.7), "peak", 3200, 0.9, -3), "lp", v.lp1, 0.6), "lp", v.lp2, 0.5);
  // 弾いた瞬間の「コツ」（短いノイズ）を少しだけ。粒の立ち上がりをはっきりさせる
  const rc = rng(7000 + midi);
  const click = Math.floor(0.003 * SR);
  for (let i = 0; i < click; i++) out[i] += rc() * 0.015 * bright * (1 - i / click);
  // 弾き始めの「抜け」: 4.5kHz 以上の成分を、頭 50ms の音量に対する割合（v.air）で足し、0.07 秒で消す。
  // 正規化の「前」に足す（後で足して全体を縮めると、頭の高域まで一緒に小さくなる）。
  if (v.air) {
    const hi = biquad(biquad(out, "hp", 4500, 0.7), "lp", 11000, 0.6);
    const w = Math.floor(0.05 * SR);
    let ro = 0, rh = 0;
    for (let n = 0; n < w; n++) { ro += out[n] * out[n]; rh += hi[n] * hi[n]; }
    const k = rh > 0 ? Math.sqrt(ro / rh) * v.air * (0.4 + 0.6 * bright) : 0;
    const tau = 0.07 * SR;
    for (let n = 0; n < Math.min(total, Math.floor(0.5 * SR)); n++) out[n] += hi[n] * k * Math.exp(-n / tau);
  }
  // 立ち上がり 1ms のフェードイン、最後は 0.3 秒のフェードアウト
  const fi = Math.floor(0.001 * SR), fo = Math.floor(0.3 * SR);
  for (let i = 0; i < fi; i++) out[i] *= i / fi;
  for (let i = 0; i < fo; i++) out[total - 1 - i] *= i / fo;
  // ピークをそろえる
  let pk = 0;
  for (let i = 0; i < total; i++) pk = Math.max(pk, Math.abs(out[i]));
  const g = 0.8 / (pk || 1);
  for (let i = 0; i < total; i++) out[i] *= g;
  return out;
}

/** RBJ の biquad（hp・lp・ls＝ローシェルフ・peak）。 */
function biquad(x, type, f, q, gainDb = 0) {
  const w0 = 2 * Math.PI * f / SR, c = Math.cos(w0), s = Math.sin(w0), al = s / (2 * q), A = 10 ** (gainDb / 40);
  let b0, b1, b2, a0, a1, a2;
  if (type === "lp") { b0 = (1 - c) / 2; b1 = 1 - c; b2 = (1 - c) / 2; a0 = 1 + al; a1 = -2 * c; a2 = 1 - al; }
  else if (type === "ls") {
    const sq = 2 * Math.sqrt(A) * al;
    b0 = A * ((A + 1) - (A - 1) * c + sq); b1 = 2 * A * ((A - 1) - (A + 1) * c); b2 = A * ((A + 1) - (A - 1) * c - sq);
    a0 = (A + 1) + (A - 1) * c + sq; a1 = -2 * ((A - 1) + (A + 1) * c); a2 = (A + 1) + (A - 1) * c - sq;
  }
  else if (type === "hp") { b0 = (1 + c) / 2; b1 = -(1 + c); b2 = (1 + c) / 2; a0 = 1 + al; a1 = -2 * c; a2 = 1 - al; }
  else { b0 = 1 + al * A; b1 = -2 * c; b2 = 1 - al * A; a0 = 1 + al / A; a1 = -2 * c; a2 = 1 - al / A; }
  const y = new Float32Array(x.length);
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
  for (let i = 0; i < x.length; i++) {
    const v = (b0 * x[i] + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2) / a0;
    x2 = x1; x1 = x[i]; y2 = y1; y1 = v; y[i] = v;
  }
  return y;
}

if (process.argv[1] && import.meta.url.endsWith(path.basename(process.argv[1]))) {
  for (const [id, v] of Object.entries(VARIANTS)) {
    const out = new BasicSoundBank();
    out.soundBankInfo = { ...base.soundBankInfo, name: `Guitar Pluck ${id}` };
    const keys = [];
    for (let k = 40; k <= 88; k += 3) keys.push(k); // E2〜E6 を3半音おき
    const byKey = new Map();
    for (const k of keys) {
      byKey.set(k, []);
      for (const [name, layer] of Object.entries(LAYERS)) {
        const smp = monoSample(`pluck ${id} ${k} ${name}`, pluck(k, layer.bright, SECONDS, v), k);
        out.addSamples(smp);
        byKey.get(k).push({ smp, layer });
      }
    }
    for (const program of [26, 27]) {
      const preset = emptyPresetFrom(base, out, { program: 27 });
      preset.program = program;
      preset.name = `Guitar Pluck ${id}`;
      const inst = preset.zones[0].instrument;
      while (inst.zones.length) inst.deleteZone(0, true);
      for (const k of keys) {
        for (const { smp, layer } of byKey.get(k)) {
          const z = inst.createZone(smp);
          z.keyRange = { min: k === keys[0] ? 28 : k - 1, max: k === keys[keys.length - 1] ? 96 : k + 1 };
          z.velRange = { min: layer.vel[0], max: layer.vel[1] };
          z.setGenerator(GeneratorTypes.attackVolEnv, timecents(0.001));
          z.setGenerator(GeneratorTypes.holdVolEnv, timecents(0.001));
          z.setGenerator(GeneratorTypes.decayVolEnv, timecents(1));
          z.setGenerator(GeneratorTypes.sustainVolEnv, 0);
          z.setGenerator(GeneratorTypes.chorusEffectsSend, 0);
          z.setGenerator(GeneratorTypes.initialFilterQ, 0);
          z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(program === 26 && v.release26 ? v.release26 : 0.25)); // 26番(jazzGuitar)だけ余韻を長くできる（イントロの和音の「伸び」用）
          z.setGenerator(GeneratorTypes.overridingRootKey, k);
        }
      }
    }
    out.flush();
    await compressBank(out, 6);
    const buf = out.writeSF2({});
    const file = path.join(OUT, `guitar-pluck-${id}.sf3`);
    fs.writeFileSync(file, Buffer.from(buf));
    console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "音:", keys.length, v.label);
  }
}
