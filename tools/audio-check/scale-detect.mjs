// 音階の推定（docs/sound/scales-world-guide.md の提案 6）。曲の音（拍の重みつき）に一番合う音階を、42 種×12 の主音の中から上位 N 個返す。
// 音階の表は docs/sound/data/scales.json（src/audio/scales.ts の写し。src/audio/scale-detect.test.ts が一致を確かめる）。
import fs from "fs";

const NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"];
let cache = null;
export function loadScales() {
  if (!cache) cache = JSON.parse(fs.readFileSync(new URL("../../docs/sound/data/scales.json", import.meta.url), "utf8"));
  return cache;
}

/**
 * hist: 長さ 12 の配列（音名 0〜11 ごとの拍の合計）。
 * opts.tonicHints: 主音の候補（0〜11）。曲の最初のコードの根音・旋律の最後の音など。当たれば少し加点する。
 * 点数 = 適合率（音階に入る音の割合）と再現率（音階の音のうち、実際に使われた割合。全体の 1.5% 以上を「使われた」と数える）の調和平均 + 主音の加点 0.04。
 * 返り値: [{ id, name, tonic, tonicName, coverage, score }]（点数の高い順）。
 */
export function rankScales(hist, opts = {}) {
  const total = hist.reduce((a, b) => a + b, 0);
  if (!(total > 0)) return [];
  const hints = new Set(opts.tonicHints ?? []);
  const out = [];
  for (const sc of loadScales()) {
    const semis = (sc.approx ?? sc.semis).map(Math.round);
    for (let tonic = 0; tonic < 12; tonic++) {
      const pcs = new Set(semis.map((s) => (s + tonic) % 12));
      let inside = 0;
      let used = 0;
      for (let pc = 0; pc < 12; pc++) if (pcs.has(pc)) { inside += hist[pc]; if (hist[pc] / total >= 0.015) used++; }
      const p = inside / total;
      const r = used / pcs.size;
      const f = p + r > 0 ? (2 * p * r) / (p + r) : 0;
      out.push({ id: sc.id, name: sc.name, tonic, tonicName: NAMES[tonic], coverage: p, score: f + (hints.has(tonic) ? 0.04 : 0) });
    }
  }
  return out.sort((a, b) => b.score - a.score || b.coverage - a.coverage);
}

/** 上位 n 個を、同じ音の並びの重複（長調ペンタと呂など、同じ主音で同じ音のもの）をまとめて返す。 */
export function topScales(hist, n = 3, opts = {}) {
  const seen = new Set();
  const out = [];
  for (const r of rankScales(hist, opts)) {
    const sc = loadScales().find((s) => s.id === r.id);
    const key = [...new Set((sc.approx ?? sc.semis).map((s) => (Math.round(s) + r.tonic) % 12))].sort((a, b) => a - b).join(",");
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(r);
    if (out.length >= n) break;
  }
  return out;
}
