import { test } from "node:test";
import assert from "node:assert";
import fs from "fs";
import os from "os";
import path from "path";
import { percentile, summarize, extractMetrics, parseJsonl, buildTargets, run, expandInputs } from "./build-genre-targets.mjs";
import { resolveGenre, clearTargetCache } from "../composer/genre-targets.mjs";

const song = (p, genre, over = {}, bpm = 100) => ({
  path: p, title: p, genre, dur_site: 100, bpm_site: bpm,
  metrics: { I: -14, LRA: 4, TP: -1, PLR: 13, crest_dB: 14, band_dB: { sub: -8, bass: -3, lowmid: -7, mid: -12, presence: -22, air: -25 }, side_minus_mid_dB: { sub: -20, bass: -10, lowmid: -5, mid: -4, presence: -5, air: -5 }, corr: 0.7, centroid_Hz: 400, tilt_dB_oct: -5, flatness_2k8k: 0.15, intro_vs_max_dB: -6, end_vs_max_dB: -3, tail_s: 1.2, dur_s: 100, ...over },
  chords: { bpm: 90, key_tonic: 0 },
});

test("パーセンタイル: numpy と同じ（線形補間）", () => {
  assert.equal(percentile([1, 2, 3, 4, 5], 50), 3);
  assert.equal(percentile([1, 2, 3, 4], 50), 2.5);
  assert.equal(percentile([0, 10], 10), 1);
  assert.deepEqual(summarize([5, 1, 3, NaN, 2, 4]), { p10: 1.4, med: 3, p90: 4.6 });
  assert.equal(summarize([]), null);
});

test("1曲の指標: 1000曲の表と同じキー名。数でない値は入れない", () => {
  const m = extractMetrics(song("a", "x", { tail_s: undefined, LRA: NaN }));
  assert.equal(m.PLR, 13); assert.equal(m["頭"], -6); assert.equal(m["帯域_air"], -25); assert.equal(m["広がり_mid"], -4); assert.equal(m.bpm, 100); assert.equal(m["重心"], 400);
  assert.ok(!("余韻" in m) && !("LRA" in m));
});

test("jsonl: 壊れた行・書きかけの最後の行は飛ばす。同じ曲は後の行を使う", () => {
  const lines = [JSON.stringify(song("a", "g1")), "", "{broken", JSON.stringify(song("b", "g1")), JSON.stringify(song("a", "g1", { LRA: 9 })), '{"path":"c","metrics":{"I":-1'].join("\n");
  const r = parseJsonl(lines);
  assert.equal(r.songs.length, 2);
  assert.equal(r.bad, 2);
  assert.equal(r.songs.find((s) => s.path === "a").metrics.LRA, 9);
});

test("集計: ジャンルごとに p10・中央値・p90、少ないジャンルは n_small、全体とテンポ別も出る", () => {
  const songs = [];
  for (let i = 0; i < 10; i++) songs.push(song("a" + i, "game", { LRA: 1 + i, flatness_2k8k: 0.1 + i / 100 }, 60 + i * 20));
  songs.push(song("z", "few", { LRA: 20 }));
  const t = buildTargets(songs, { minN: 5, sources: ["/x/results-0.jsonl"], bad: 1 });
  assert.equal(t.n_total, 11); assert.equal(t.n_skipped_lines, 1); assert.deepEqual(t.sources, ["results-0.jsonl"]);
  assert.equal(t.groups.game.n, 10);
  assert.deepEqual(t.groups.game.LRA, { p10: 1.9, med: 5.5, p90: 9.1 });
  assert.equal(t.groups.game.flat.med, 0.15);
  assert.ok(!t.groups.game.n_small && t.groups.few.n_small);
  assert.equal(t.groups["(全体)"].n, 11);
  assert.ok(t.by_tempo["0-80"] === undefined || t.by_tempo["0-80"].n >= 5);
  assert.deepEqual(buildTargets([]).groups, {});
});

test("実行: 入力は読むだけ。出力を genre-targets.mjs がそのまま読める", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "bgt-"));
  const f0 = path.join(dir, "results-0.jsonl"), f1 = path.join(dir, "results-1.jsonl");
  const w = (genre, n, lra, pre = "") => Array.from({ length: n }, (_, i) => JSON.stringify(song(`${pre}${genre}${i}`, genre, { LRA: lra + i / 10 }))).join("\n") + "\n";
  fs.writeFileSync(f0, w("Lo-Fi", 12, 4));
  fs.writeFileSync(f1, w("Lo-Fi", 8, 5, "b") + w("seasonal", 6, 6) + "{書きかけ");
  const before = [fs.readFileSync(f0, "utf8"), fs.readFileSync(f1, "utf8")];
  const out = path.join(dir, "out", "site50.json");
  const r = run({ inputs: [dir], out });
  assert.deepEqual(expandInputs([dir]), [f0, f1]);
  assert.equal(r.n_total, 26); // Lo-Fi は path が重ならないので 12+8、seasonal 6
  assert.equal(r.n_skipped_lines, 1);
  assert.deepEqual([fs.readFileSync(f0, "utf8"), fs.readFileSync(f1, "utf8")], before, "入力は書き換えない");
  const saved = JSON.parse(fs.readFileSync(out, "utf8"));
  assert.equal(saved.groups["Lo-Fi"].n, 20);
  // 目標の表として読める（lofi → Lo-Fi。n≥15）。seasonal は6曲なので使わない
  clearTargetCache();
  const data = { nihonichi: { groups: {}, by_site_genre: {}, by_tempo: {} }, site50: saved };
  assert.equal(resolveGenre("lofi", { data }).source, "site50");
  assert.equal(resolveGenre("seasonal", { data }), null);
  assert.throws(() => run({ inputs: [] }), /入力がありません/);
  assert.throws(() => run({ inputs: [path.join(dir, "nothing.jsonl")] }), /ファイルがありません/);
});

test("コミット済みの site50 表（今ある分の集計）が genre-targets の形式で読める", () => {
  const p = new URL("../../docs/sound/data/genre-targets-site50.json", import.meta.url);
  if (!fs.existsSync(p)) return;
  const t = JSON.parse(fs.readFileSync(p, "utf8"));
  assert.ok(t.n_total > 0 && t.groups["(全体)"]);
  for (const [g, v] of Object.entries(t.groups)) for (const k of ["LRA", "PLR", "corr", "flat"]) assert.ok(v[k].p10 <= v[k].med && v[k].med <= v[k].p90, `${g}.${k}`);
});
