// 「日本一フリーBGM のジャンル別50曲測定」の結果（1行1曲のJSON: genre・metrics・chords。音声は無い）を集計して、
// ジャンルごとの目標（p10／中央値／p90）を docs/sound/data/genre-targets-site50.json に書く。
// 形は docs/sound/data/genre-targets-nihonichi.json の groups と同じ（tools/composer/genre-targets.mjs がそのまま読める）。
//   node tools/audio-check/build-genre-targets.mjs --in results-0.jsonl results-1.jsonl [--out docs/sound/data/genre-targets-site50.json] [--min-n 5]
//   --in には .jsonl のファイルか、.jsonl の入ったフォルダを書ける。入力は読むだけで、書き換えない。
// 途中の行が壊れている（測定の最中で書きかけ）・同じ曲が2回ある場合も動く（壊れた行は数えて飛ばす、同じ path は後のものを使う）。
// 数字だけ（音声・旋律・和音は入れない。chords は使わない）。
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const ROOT = path.resolve(fileURLToPath(new URL("../../", import.meta.url)));
const BANDS = ["sub", "bass", "lowmid", "mid", "presence", "air"];
export const TEMPO_BINS = [["0-80", 0, 80], ["80-100", 80, 100], ["100-120", 100, 120], ["120-140", 120, 140], ["140-160", 140, 160], ["160-300", 160, 300]];

/** 1曲分の行 → 指標の表（genre-targets-nihonichi.json と同じキー名）。数値でないものは入れない。 */
export function extractMetrics(song) {
  const m = song?.metrics ?? {};
  const out = {
    I: m.I, PLR: m.PLR, crest: m.crest_dB, LRA: m.LRA, corr: m.corr, "重心": m.centroid_Hz, tilt: m.tilt_dB_oct, flat: m.flatness_2k8k,
    "頭": m.intro_vs_max_dB, "余韻": m.tail_s, "長さ": m.dur_s ?? song?.dur_site, bpm: song?.bpm_site,
  };
  for (const b of BANDS) { out[`帯域_${b}`] = m.band_dB?.[b]; out[`広がり_${b}`] = m.side_minus_mid_dB?.[b]; }
  for (const k of Object.keys(out)) if (typeof out[k] !== "number" || !Number.isFinite(out[k])) delete out[k];
  return out;
}

/** numpy.percentile と同じ（線形補間）。sorted は昇順の配列。 */
export function percentile(sorted, p) {
  if (!sorted.length) return NaN;
  const pos = ((sorted.length - 1) * p) / 100, lo = Math.floor(pos), hi = Math.ceil(pos);
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
}
const round2 = (x) => Math.round(x * 100) / 100;

/** 値の配列 → { p10, med, p90 } */
export function summarize(values) {
  const s = values.filter((v) => Number.isFinite(v)).sort((a, b) => a - b);
  if (!s.length) return null;
  return { p10: round2(percentile(s, 10)), med: round2(percentile(s, 50)), p90: round2(percentile(s, 90)) };
}

/** 曲の配列 → 指標ごとの { p10, med, p90 } と曲数 n。 */
export function summarizeGroup(songs) {
  const rows = songs.map(extractMetrics);
  const keys = [...new Set(rows.flatMap((r) => Object.keys(r)))];
  const g = { n: songs.length };
  for (const k of keys) { const s = summarize(rows.map((r) => r[k]).filter((v) => v !== undefined)); if (s) g[k] = s; }
  return g;
}

/** jsonl の本文 → { songs, bad }。壊れた行（書きかけ）は数えて飛ばす。同じ path は後の行を使う。 */
export function parseJsonl(text) {
  const byPath = new Map();
  let bad = 0, k = 0;
  for (const line of String(text).split("\n")) {
    const t = line.trim();
    if (!t) continue;
    try {
      const d = JSON.parse(t);
      if (!d || typeof d !== "object" || !d.metrics) { bad++; continue; }
      byPath.set(d.path ?? `#${k++}`, d);
    } catch { bad++; }
  }
  return { songs: [...byPath.values()], bad };
}

/** 曲の配列 → 出力の形。minN 未満のジャンルは n_small: true を付ける（目標としては使われない）。 */
export function buildTargets(songs, { minN = 5, sources = [], bad = 0 } = {}) {
  const byGenre = new Map();
  for (const s of songs) {
    const g = s.genre ?? "(不明)";
    if (!byGenre.has(g)) byGenre.set(g, []);
    byGenre.get(g).push(s);
  }
  const groups = {};
  for (const [g, list] of [...byGenre.entries()].sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0]))) {
    groups[g] = summarizeGroup(list);
    if (list.length < minN) groups[g].n_small = true;
  }
  if (songs.length) groups["(全体)"] = summarizeGroup(songs);
  const by_tempo = {};
  for (const [name, lo, hi] of TEMPO_BINS) {
    const list = songs.filter((s) => Number.isFinite(s.bpm_site) && s.bpm_site >= lo && s.bpm_site < hi);
    if (list.length >= minN) by_tempo[name] = summarizeGroup(list);
  }
  return {
    note: "日本一フリーBGMの「ジャンル別50曲測定」の結果をジャンルごとに集計した値（p10/中央値/p90）。数字だけで、音声・旋律・和音は含まない。キー名は genre-targets-nihonichi.json と同じ。n が小さいジャンル（n_small）は目安が粗い。tools/audio-check/build-genre-targets.mjs で作る。",
    generated: new Date().toISOString().slice(0, 10),
    sources: sources.map((p) => path.basename(p)),
    n_total: songs.length,
    n_skipped_lines: bad,
    groups,
    by_tempo,
  };
}

/** --in の指定（ファイル／フォルダ）→ jsonl ファイルの一覧 */
export function expandInputs(inputs) {
  const files = [];
  for (const p of inputs) {
    if (fs.existsSync(p) && fs.statSync(p).isDirectory()) files.push(...fs.readdirSync(p).filter((f) => f.endsWith(".jsonl")).sort().map((f) => path.join(p, f)));
    else files.push(p);
  }
  return files;
}

/** 読み込み → 集計 → 書き出し。戻り値は出力の中身。 */
export function run({ inputs, out, minN = 5 }) {
  const files = expandInputs(inputs);
  if (!files.length) throw new Error("入力がありません（--in に .jsonl かフォルダを指定）");
  const all = new Map();
  let bad = 0;
  for (const f of files) {
    if (!fs.existsSync(f)) throw new Error(`ファイルがありません: ${f}`);
    const r = parseJsonl(fs.readFileSync(f, "utf8")); // 読むだけ
    bad += r.bad;
    for (const s of r.songs) all.set(s.path ?? `${f}#${all.size}`, s);
  }
  const result = buildTargets([...all.values()], { minN, sources: files, bad });
  if (out) { fs.mkdirSync(path.dirname(out), { recursive: true }); fs.writeFileSync(out, JSON.stringify(result, null, 1) + "\n"); }
  return result;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const a = process.argv.slice(2);
  const inIdx = a.indexOf("--in");
  const inputs = [];
  if (inIdx >= 0) for (let i = inIdx + 1; i < a.length && !a[i].startsWith("--"); i++) inputs.push(a[i]);
  const opt = (n, d) => { const i = a.indexOf(n); return i >= 0 ? a[i + 1] : d; };
  try {
    const out = path.resolve(opt("--out", path.join(ROOT, "docs/sound/data/genre-targets-site50.json")));
    const r = run({ inputs, out, minN: Number(opt("--min-n", 5)) });
    console.log(`集計: ${r.n_total}曲（壊れた行 ${r.n_skipped_lines}）→ ${path.relative(ROOT, out)}`);
    for (const [g, v] of Object.entries(r.groups)) console.log(`  ${g.padEnd(12)} n=${String(v.n).padStart(3)}${v.n_small ? "（少ない）" : ""}  LRA ${v.LRA?.med ?? "-"} / PLR ${v.PLR?.med ?? "-"} / 頭 ${v["頭"]?.med ?? "-"} / 余韻 ${v["余韻"]?.med ?? "-"} / corr ${v.corr?.med ?? "-"} / flat ${v.flat?.med ?? "-"} / 空気 ${v["帯域_air"]?.med ?? "-"}`);
  } catch (e) {
    console.error("エラー: " + e.message);
    console.error("使い方: node tools/audio-check/build-genre-targets.mjs --in <a.jsonl> [<b.jsonl> ...|フォルダ] [--out <json>] [--min-n 5]");
    process.exit(1);
  }
}
