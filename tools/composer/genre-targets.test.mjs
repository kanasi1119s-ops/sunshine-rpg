import { test } from "node:test";
import assert from "node:assert";
import { spawnSync } from "child_process";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath } from "url";
import { resolveGenre, genreTargets, genreJudge, tempoMedian, tempoShift, headStyle, tailStyle, STYLE_MAP, loadTargets, describeGenre, listGenreNames } from "./genre-targets.mjs";
import { judgeGenre, formatGate, saveMeasurement, judge, measureWav } from "./gate.mjs";
import { spectralMetrics, fft } from "./spectral-metrics.mjs";
import { masterReport } from "./master-report.mjs";

const SONG = fileURLToPath(new URL("./song.mjs", import.meta.url));
const hasFfmpeg = !spawnSync("ffmpeg", ["-version"]).error;
const noFfmpeg = hasFfmpeg ? false : "ffmpeg なし";

test("スタイル名の対応表: 作曲ソフトの名前がすべて目標の表に行き着く", () => {
  for (const name of Object.keys(STYLE_MAP)) {
    const r = resolveGenre(name);
    assert.ok(r, `${name} が解決できない`);
    assert.ok(r.stats.LRA && r.stats.PLR && r.stats["頭"] && r.stats["余韻"], `${name} の表に指標が足りない`);
  }
  assert.equal(resolveGenre("battle").label, "ボス/戦闘");
  assert.equal(resolveGenre("game-field").label, "フィールド/町/ダンジョン");
  assert.equal(resolveGenre("ballad").label, "バラード/子守歌");
  assert.equal(resolveGenre("ボス/戦闘").label, "ボス/戦闘", "日本語のスタイル名もそのまま使える");
  assert.equal(resolveGenre("game-bgm").source, "nihonichi-site", "サイトのジャンル名も使える");
  assert.equal(resolveGenre("そんなジャンルはない"), null);
  assert.equal(resolveGenre(""), null);
  assert.ok(listGenreNames().includes("wafu"));
});

test("対応表: mix-targets.json の家族名・別名もすべて引ける（既存の表は壊さない）", () => {
  const mix = JSON.parse(fs.readFileSync(new URL("../../docs/sound/data/mix-targets.json", import.meta.url), "utf8"));
  for (const k of [...Object.keys(mix.families), ...Object.keys(mix.aliases)]) assert.ok(resolveGenre(k), `${k} が引けない`);
  assert.ok(mix.families.rock.bass !== undefined && mix.tolerance_dB, "mix-targets.json は読むだけで変えていない");
});

test("50曲測定の表: 1000曲の表に無いジャンルだけ、曲数が足りていれば使う", () => {
  const stats = (lra) => ({ n: 40, LRA: { p10: lra - 1, med: lra, p90: lra + 1 }, PLR: { p10: 12, med: 13, p90: 14 } });
  const data = { nihonichi: { groups: {}, by_site_genre: { "game-bgm": stats(5) }, by_tempo: {} }, site50: { groups: { "Lo-Fi": stats(4.7), "少数": { ...stats(3), n: 5 }, "game-bgm": stats(9) } } };
  assert.equal(resolveGenre("lofi", { data }).source, "site50");
  assert.equal(resolveGenre("lofi", { data }).stats.LRA.med, 4.7);
  assert.equal(resolveGenre("少数", { data }), null, "曲数が少ない表は使わない");
  assert.equal(resolveGenre("game-bgm", { data }).stats.LRA.med, 5, "1000曲の表を優先");
});

test("テンポ: BPM が上がるほど LRA・PLR の目標が小さくなる", () => {
  let prevL = Infinity, prevP = Infinity;
  for (const bpm of [60, 90, 110, 130, 150, 180]) {
    const l = tempoMedian("LRA", bpm), p = tempoMedian("PLR", bpm);
    assert.ok(l < prevL && p < prevP, `BPM ${bpm} で下がらない`);
    prevL = l; prevP = p;
  }
  assert.equal(tempoMedian("LRA", 30), tempoMedian("LRA", 65), "範囲の外は端の値");
  assert.ok(tempoMedian("LRA", 100) > tempoMedian("LRA", 110) && tempoMedian("LRA", 100) < tempoMedian("LRA", 90), "間は補間");
  assert.equal(tempoShift("LRA", 120, 120), 0);
  assert.ok(tempoShift("LRA", 170, 80) < -1.5, "遅い曲の基準から速い曲へは LRA が 1.5 以上下がる");
  const slow = genreTargets("jazz", { bpm: 70 }), fast = genreTargets("jazz", { bpm: 170 }), none = genreTargets("jazz");
  assert.ok(slow.ranges.lra.med > fast.ranges.lra.med && slow.ranges.plr.med > fast.ranges.plr.med);
  assert.equal(none.bpm, null);
  assert.deepEqual(none.shift, { LRA: 0, PLR: 0 });
  assert.equal(slow.ranges.corr.med, fast.ranges.corr.med, "corr などはテンポでずらさない");
  assert.ok(fast.ranges.lra.lo >= 0.5 && fast.ranges.lra.hi > fast.ranges.lra.lo, "LRA は 0 以下にならない");
});

test("頭・余韻の型: ジャンルで小さく始める／全開、長い／短いが変わる", () => {
  assert.equal(headStyle(-3.2).label, "すぐ全開");
  assert.equal(headStyle(-7.9).label, "小さく始める");
  assert.equal(headStyle(-5.5).label, "中間");
  assert.equal(tailStyle(2.55).label, "長い");
  assert.equal(tailStyle(0.74).label, "短い");
  assert.equal(genreTargets("solo").tail.label, "長い");
  assert.equal(genreTargets("retro").tail.label, "短い");
  assert.equal(genreTargets("jazz").head.label, "すぐ全開");
  assert.equal(genreTargets("orch").head.label, "小さく始める");
  assert.ok(describeGenre("ballad", { bpm: 60 }).includes("余韻") && describeGenre("ballad").includes("頭"));
  assert.ok(describeGenre("xxx").includes("目標がありません"));
});

const ballad = { lra: 7.5, plr: 13.5, corr: 0.48, flat: 0.05, air: -40, intro: -7, tail: 2.3 };
const battle = { lra: 3.4, plr: 10.8, corr: 0.74, flat: 0.29, air: -18.8, intro: -5, tail: 0.9 };

test("ジャンル判定: そのジャンルらしい数字は○、別ジャンルの数字は要直し＋直し方", () => {
  const ok = genreJudge(ballad, "ballad", { bpm: 70 });
  assert.ok(ok.rows.every((r) => r.ok), JSON.stringify(ok.rows.filter((r) => !r.ok)));
  assert.deepEqual(ok.rows.map((r) => r.key), ["lra", "plr", "head", "tail", "corr", "flat", "air"]);
  const bad = genreJudge(ballad, "battle", { bpm: 150 });
  const ng = bad.rows.filter((r) => !r.ok).map((r) => r.key);
  for (const k of ["lra", "plr", "corr", "flat", "air", "tail"]) assert.ok(ng.includes(k), `${k} が要直しにならない`);
  assert.ok(bad.rows.find((r) => r.key === "flat").hint.includes("ざらつき") && bad.rows.find((r) => r.key === "corr").hint.includes("左右"));
  assert.ok(genreJudge(battle, "battle", { bpm: 150 }).rows.every((r) => r.ok));
  assert.equal(genreJudge(battle, "存在しない"), null);
  // 測れなかった値（NaN）は要直しにしない
  assert.ok(genreJudge({ ...battle, flat: NaN, air: NaN }, "battle").rows.every((r) => r.ok));
});

test("ジャンル判定: 同じ LRA でも、遅い曲では足りず速い曲では十分、と BPM で変わる", () => {
  const m = { ...battle, lra: 2.2 };
  const fast = genreJudge(m, "battle", { bpm: 190 }).rows.find((r) => r.key === "lra");
  const slow = genreJudge(m, "battle", { bpm: 70 }).rows.find((r) => r.key === "lra");
  assert.equal(fast.ok, true);
  assert.equal(slow.ok, false);
  assert.ok(slow.hint.includes("起伏が小さい"));
});

test("合否表(gate): --genre の表は共通の判定(音量・ピーク・無音)＋ジャンルの7項目。頭・余韻の目安が文に出る", () => {
  const m = { lufs: -14, tp: -1.5, lra: 7.5, plr: 13.5, corr: 0.48, headVsMax: -7, midSilences: [], durationSec: 120, ...ballad };
  const g = judgeGenre(m, "ballad", { bpm: 70 });
  assert.deepEqual(g.rows.map((r) => r.key), ["lufs", "tp", "lra", "plr", "head", "tail", "corr", "flat", "air", "silence"]);
  assert.ok(g.rows.every((r) => r.ok));
  const text = formatGate(m, g.rows, "a.wav", { genre: g.target });
  assert.ok(text.includes("ジャンル目標「バラード/子守歌」") && text.includes("小さく始める") && text.includes("余韻"));
  assert.ok(text.includes("小さく始めて育てる") && text.includes("長く消える"), "頭と余韻の目安が合否表に出る");
  assert.equal(judgeGenre(m, "xxx"), null);
  // ジャンル無しの既定の判定は変わらない
  assert.equal(judge(m).length, 7);
  const bad = judgeGenre({ ...m, lra: 1, plr: 8 }, "ballad", { bpm: 70 });
  assert.ok(bad.rows.some((r) => !r.ok && r.key === "lra"));
});

test("測定の保存: ジャンル表でも値を取り違えない（キーで引く）", () => {
  const m = { lufs: -14, tp: -1.5, lra: 7.5, plr: 13.5, corr: 0.48, headVsMax: -7, midSilences: [], durationSec: 120, ...ballad };
  const g = judgeGenre(m, "ballad", { bpm: 70 });
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "gt-"));
  const s = saveMeasurement(root, "t1", m, g.rows, -14, "ballad");
  assert.equal(s.entry.lufs, -14); assert.equal(s.entry.lra, 7.5); assert.equal(s.entry.corr, 0.48); assert.equal(s.entry.genre, "ballad");
  assert.equal(s.entry.flat, 0.05); assert.equal(s.entry.tail, 2.3);
  const s2 = saveMeasurement(root, "t2", m, judge(m), -14);
  assert.equal(s2.entry.lra, 7.5); assert.equal(s2.entry.plr, 13.5);
});

// ---- スペクトル指標 ----
const SR = 44100;
const rnd = (() => { let s = 12345; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296) * 2 - 1; })();

test("FFT: 正弦波のピークが正しい場所に出る", () => {
  const N = 1024, re = new Float64Array(N), im = new Float64Array(N);
  for (let i = 0; i < N; i++) re[i] = Math.sin((2 * Math.PI * 64 * i) / N);
  fft(re, im);
  let best = 0;
  for (let k = 1; k < N / 2; k++) if (re[k] ** 2 + im[k] ** 2 > re[best] ** 2 + im[best] ** 2) best = k;
  assert.equal(best, 64);
});

test("スペクトル指標: ノイズは flat が大きく、正弦波は小さい。空気は高い音ほど多い", () => {
  const n = SR * 6;
  const noise = new Float32Array(n).map(() => rnd() * 0.3);
  const sine = new Float32Array(n).map((_, i) => 0.3 * Math.sin((2 * Math.PI * 440 * i) / SR));
  const hi = new Float32Array(n).map((_, i) => 0.3 * Math.sin((2 * Math.PI * 10000 * i) / SR));
  const a = spectralMetrics(noise, noise, SR), b = spectralMetrics(sine, sine, SR), c = spectralMetrics(hi, hi, SR);
  assert.ok(a.flat > 0.4 && b.flat < 0.15, `flat noise=${a.flat} sine=${b.flat}`);
  assert.ok(c.air > -1 && b.air < -40, `air hi=${c.air} low=${b.air}`);
  assert.ok(a.air < -4 && a.air > -12, `白色ノイズの 8〜16k は全体の約1/3 (${a.air})`);
});

test("スペクトル指標: 頭（小さく始まる曲は負）と余韻（消えるまでの秒数）", () => {
  const n = SR * 20;
  const fade = new Float32Array(n);
  for (let i = 0; i < n; i++) fade[i] = (i < SR * 5 ? 0.05 : 0.4) * Math.sin((2 * Math.PI * 220 * i) / SR);
  const x = spectralMetrics(fade, fade, SR);
  assert.ok(x.intro < -15 && x.intro > -20, `頭 ${x.intro}（20log(0.05/0.4)=-18）`);
  // 14秒まで鳴って、そのあと指数で減衰（−60dB/2秒）。大きさ −20→−50dB は 30dB ぶん ≒ 1秒
  const dec = new Float32Array(n);
  for (let i = 0; i < n; i++) { const t = i / SR; dec[i] = 0.5 * Math.sin((2 * Math.PI * 220 * i) / SR) * (t < 10 ? 1 : Math.pow(10, (-60 * (t - 10)) / 2 / 20)); }
  const d = spectralMetrics(dec, dec, SR);
  assert.ok(d.tail > 0.7 && d.tail < 1.4, `余韻 ${d.tail}`);
  const short = spectralMetrics(new Float32Array(100), new Float32Array(100), SR);
  assert.ok(Number.isNaN(short.flat));
});

function makeWav(file, filt) {
  const r = spawnSync("ffmpeg", ["-y", "-loglevel", "error", "-f", "lavfi", "-i", "anoisesrc=d=8:c=white:r=44100:a=0.2:seed=7", "-af", filt, "-ac", "2", file]);
  assert.equal(r.status, 0, String(r.stderr));
}

test("measureWav・report: flat と空気が出る", { skip: noFfmpeg }, () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "gt-wav-"));
  const f = path.join(dir, "n.wav");
  makeWav(f, "anull");
  const m = measureWav(f);
  assert.ok(m.flat > 0.4 && Number.isFinite(m.air) && Number.isFinite(m.intro), JSON.stringify(m));
  assert.ok(Number.isNaN(measureWav(f, { spectral: false }).flat), "spectral:false なら測らない");
  const r = masterReport(f, { lufs: -14, tp: -1.5, loop: false, genre: "battle", bpm: 150 });
  assert.match(r.line, /\/ 継ぎ目 - \/ flat [\d.]+ \/ 空気 -?[\d.]+/);
  assert.ok(r.line.includes("ジャンル「ボス/戦闘」") && r.genre.rows.length === 7);
  assert.ok(Number.isFinite(r.metrics.flat) && Number.isFinite(r.metrics.air));
  const noGenre = masterReport(f, { loop: false });
  assert.ok(!noGenre.line.includes("ジャンル") && noGenre.genre === null);
  assert.ok(masterReport(f, { loop: false, genre: "xx" }).line.includes("目標がありません"));
});

test("コマンド: gate --genre／genre-target／--song の genre と bpm", { skip: noFfmpeg }, () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "gt-cli-"));
  const f = path.join(dir, "n.wav");
  makeWav(f, "anull");
  const run = (...a) => spawnSync("node", [SONG, ...a], { encoding: "utf8" });
  const g = run("gate", f, "--genre", "battle", "--bpm", "150");
  assert.ok(g.stdout.includes("ジャンル目標「ボス/戦闘」") && g.stdout.includes("ざらつき") && g.stdout.includes("空気"), g.stdout + g.stderr);
  const sj = path.join(dir, "s.json");
  fs.writeFileSync(sj, JSON.stringify({ drumGenre: "ballad", bpm: 60 }));
  const g2 = run("gate", f, "--song", sj);
  assert.ok(g2.stdout.includes("バラード/子守歌") && g2.stdout.includes("BPM 60"), g2.stdout);
  const bad = run("gate", f, "--genre", "zzz");
  assert.ok((bad.stdout + bad.stderr).includes("目標がありません"));
  const t = run("genre-target", "ballad", "--bpm", "60");
  assert.ok(t.stdout.includes("バラード/子守歌") && t.stdout.includes("余韻"));
  const j = JSON.parse(run("gate", f, "--genre", "battle", "--json").stdout);
  assert.equal(j.genre, "battle");
});
