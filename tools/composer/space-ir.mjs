// 空間（残響）の畳み込み用のインパルスレスポンスを、自分で作る。外部の残響データは使わない（規約の問題を避けるため。docs/sound/realism-roadmap.md）。
// 作り方: 初期反射（間引いた数発の反射）＋ 指数で減衰する左右別々のノイズ。高い音ほど早く減衰する（空気と壁の吸収）。
import fs from "fs";

export const SPACES = {
  room: { rt60: 0.7, predelay: 0.008, bright: 0.55, early: 6 },
  hall: { rt60: 1.9, predelay: 0.022, bright: 0.45, early: 9 },
  plate: { rt60: 1.3, predelay: 0.004, bright: 0.8, early: 3 },
  // 2026-10-20 人間「空間も感じれるといいな」（ケルト異世界ファンタジー）: 外の広い場所（丘・森・谷）。
  //   最初の反射が遅く（遠くの地面や木）、長くやわらかく消える（高い音は早く消える）
  vale: { rt60: 2.6, predelay: 0.045, bright: 0.38, early: 5 },
  // 2026-10-25 人間「空間も意識して。頭の中を全て支配するような感じで」（ケルトの幻想）: 大聖堂のような、とても大きくやわらかい空間。
  //   最初の反射はさらに遅く、4秒以上かけて消え、高い音は早めに消える（耳を包む・暗く広い）
  dome: { rt60: 4.4, predelay: 0.065, bright: 0.36, early: 7 },
  // 2026-10-25 人間「全体的にこもるように聞こえる。煌めきがあるような音に。空間を支配しよう」: 大きく広いのに、高い音が長く残る明るい空間（空・ガラスの吹きぬけ）
  sky: { rt60: 3.0, predelay: 0.04, bright: 0.85, early: 8 },
};

function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

/** ステレオのIR（Float32Array 2本）。 */
export function makeIr(kind = "hall", sr = 48000) {
  const sp = SPACES[kind];
  if (!sp) throw new Error(`空間は ${Object.keys(SPACES).join("・")} のどれか（${kind}）`);
  const n = Math.round((sp.rt60 * 1.15 + sp.predelay) * sr);
  const out = [new Float32Array(n), new Float32Array(n)];
  for (let ch = 0; ch < 2; ch++) {
    const r = rng(7001 + ch * 131 + kind.length);
    const pre = Math.round(sp.predelay * sr);
    let lp = 0;
    for (let i = pre; i < n; i++) {
      const t = (i - pre) / sr;
      const env = Math.pow(10, (-3 * t) / sp.rt60); // -60dB が rt60 秒
      const white = r() * 2 - 1;
      // 時間がたつほど高域が丸くなる（1次ローパスの係数を時間で変える）
      const a = Math.min(0.97, sp.bright * Math.exp(-t * 1.4) + 0.06);
      lp += a * (white - lp);
      out[ch][i] = lp * env * (1 - Math.exp(-t * 60)); // 立ち上がりをなめらかに
    }
    // 初期反射
    for (let k = 0; k < sp.early; k++) {
      const at = pre + Math.round((0.004 + r() * 0.05) * sr);
      if (at < n) out[ch][at] += (r() < 0.5 ? -1 : 1) * (0.6 - k * 0.05);
    }
  }
  // ピークをそろえる
  let peak = 0; for (const c of out) for (const v of c) peak = Math.max(peak, Math.abs(v));
  for (const c of out) for (let i = 0; i < n; i++) c[i] /= peak || 1;
  return out;
}

export function writeWav(file, chans, sr = 48000) {
  const n = chans[0].length, buf = Buffer.alloc(44 + n * chans.length * 2);
  buf.write("RIFF", 0); buf.writeUInt32LE(36 + n * chans.length * 2, 4); buf.write("WAVEfmt ", 8); buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20); buf.writeUInt16LE(chans.length, 22); buf.writeUInt32LE(sr, 24); buf.writeUInt32LE(sr * chans.length * 2, 28);
  buf.writeUInt16LE(chans.length * 2, 32); buf.writeUInt16LE(16, 34); buf.write("data", 36); buf.writeUInt32LE(n * chans.length * 2, 40);
  for (let i = 0; i < n; i++) for (let c = 0; c < chans.length; c++) buf.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round(chans[c][i] * 32767))), 44 + (i * chans.length + c) * 2);
  fs.writeFileSync(file, buf);
}
